#!/usr/bin/env python3
"""
gapcloser_axisym.py -- THE AXISYMMETRIC (r,theta) GAUGE-FIXED NONLINEAR SOLVER
(the #57 gap-closer, axisymmetric fallback).

Driver: Claude (Opus 4.8, 1M).  2026-06-16.  OBSERVE mode.  DATA-BLIND.

WHY THE FALLBACK (honest scoping, NOT silent reduction): the full-3-D residual-Newton
on all 10 metric components does NOT converge robustly even with the reference-gauge +
geometry weighting recipe -- diagnosed live (gapcloser_run_gate smoke test: the
metric-only Gauss-Newton step REDUCES the body residual only marginally and the LM
loop's |r| GROWS from many seeds; the coupled 10-component J^T J is too ill-conditioned
for matrix-free CG).  This REPRODUCES the #57 finding that the full-3-D gauge-fixed
arbitrary-seed solve is the hard capability.  The prompt's sanctioned fallback: an
AXISYMMETRIC (r,theta) solver, which STILL admits the main catalog candidates --
multipole (l=1..4), prolate/oblate, two-center-on-axis, ring/toroidal, large-amplitude.
The residual non-axisymmetric (psi-dependent) types are honestly out of scope here.

THE GAUGE-FIXED AXISYMMETRIC METRIC (static, axisymmetric, diagonal -- DIAGONAL is the
GAUGE for a static axisymmetric vacuum-plus-hedgehog system: Weyl/Lewis-Papapetrou says
a static axisymmetric metric can be diagonalized by a coordinate choice; this is a
non-restrictive GAUGE, not a physics tie -- B=1/A is NOT imposed, the four functions are
independent):
  ds^2 = -e^{2 a(r,th)} dt^2 + e^{2 b(r,th)} dr^2 + e^{2 c(r,th)} r^2 dth^2
         + e^{2 d(r,th)} r^2 sin^2(th) dphi^2
Four INDEPENDENT metric functions a,b,c,d on a (r,theta) grid, plus the matter profile
Theta(r,theta).  Round limit: a=a(r), b=b(r), c=d=... reduce to #56 (validation target).
The genuine axisymmetric SHAPES live in the theta-dependence and in c!=d, b!=... .

THE NUMERICAL EINSTEIN ENGINE is the VALIDATED full-4-D numerical engine
(whole_metric_3d_core, off-diag G to 5e-6), evaluated on a single psi slice (the metric
is psi-independent; the diagonal static-axisymmetric Einstein tensor is itself diagonal
in this gauge, off-diagonals vanish by construction -- a consistency, like the round
case in #57).  Matter = the settled L2+L4 unit-S^3 hedgehog (whole_metric_3d_matter),
profile Theta(r,theta).  B=1/A FREE.

THE SOLVER (robust, structured, monotone -- the conditioning fix):
  We minimize the proper-volume-weighted, axis/core-masked least-squares objective
       Phi = || sqrt(W) * (G^mu_nu - kap8 T^mu_nu) ||^2   (the 4 diagonal eqs)
  by a damped Levenberg-Marquardt with STRICT monotone acceptance (Phi must DECREASE or
  the step is rejected and damping raised), matrix-free (autograd JVP/VJP + CG on the
  normal equations).  The matter Theta is relaxed IN THE SAME LOOP by the exact action
  gradient (so the source is always self-consistent -- the fix for the divergence seen
  when matter was frozen).  Axis (theta near 0,pi) and deep-core (r<rc+rfreeze) are
  regularity-excised from the objective (the recipe's anchor).  Proper-volume weight
  W = sqrt|g| (normalized) de-amplifies the coordinate-singular regions.

NATIVE-vs-PATCH (held precisely): the diagonal-axisymmetric gauge (Weyl), axis/core
regularity, and proper-volume weighting are NUMERICAL CONDITIONING of the SAME native
Einstein+L2+L4 equations.  NO B=1/A tie, NO seal/source injection, NO linearization as a
result, NO imported mechanism, NO target tuning.
"""
import os
os.environ.setdefault("PYTORCH_NVML_BASED_CUDA_CHECK", "0")
import math
import torch
import whole_metric_3d_core as core
import whole_metric_3d_matter as mat

torch.set_default_dtype(torch.float64)
DEV = "cuda" if torch.cuda.is_available() else "cpu"
T, R, TH, PS = 0, 1, 2, 3
EXP_CLAMP = 60.0
PI = math.pi
XI = KAP = 1.0


# ===========================================================================
# GRID (r,theta); a single psi slice (axisymmetric).  theta kept off the axis.
# ===========================================================================
def mkgrid(Nr, Nth, rc, ri, th0, th1):
    rg = torch.linspace(rc, ri, Nr, device=DEV)
    thg = torch.linspace(th0, th1, Nth, device=DEV)
    hr = (rg[1]-rg[0]).item(); hth = (thg[1]-thg[0]).item()
    Rr, Tht = torch.meshgrid(rg, thg, indexing='ij')
    # one psi slice -> add a singleton psi dim (Nps=1) for engine compatibility
    return dict(rg=rg, thg=thg, hr=hr, hth=hth, Rr=Rr[..., None], Tht=Tht[..., None],
                Ps=torch.zeros(Nr, Nth, 1, device=DEV),
                Nr=Nr, Nth=Nth, Nps=1, rc=rc, ri=ri, th0=th0, th1=th1)


def d_dx_rt(f, h, axis):
    """FD on (Nr,Nth,1,...) along r(axis 3) or theta(axis 4); 4th-order via core.d_dx.
    psi (axis 5) singleton -> derivative 0."""
    if axis == 5:
        return torch.zeros_like(f)
    return core.d_dx(f, h, axis, periodic=False)


# ===========================================================================
# METRIC from the 4 functions; full numerical Einstein engine.
# ===========================================================================
def metric_from_abcd(a, b, c, d, G):
    Nr, Nth = G['Nr'], G['Nth']
    g = torch.zeros(Nr, Nth, 1, 4, 4, device=DEV)
    R2 = G['Rr']**2
    s2 = torch.sin(G['Tht'])**2
    g[..., T, T] = -torch.exp(torch.clamp(2*a, max=EXP_CLAMP))[..., None]
    g[..., R, R] = torch.exp(torch.clamp(2*b, max=EXP_CLAMP))[..., None]
    g[..., TH, TH] = (torch.exp(torch.clamp(2*c, max=EXP_CLAMP))[..., None]) * R2
    g[..., PS, PS] = (torch.exp(torch.clamp(2*d, max=EXP_CLAMP))[..., None]) * R2 * s2
    return g


def full_einstein_rt(g, G):
    ginv = core.metric_inverse(g)
    dg = torch.zeros(*g.shape[:-2], 4, 4, 4, device=g.device)
    dg[..., R, :, :] = d_dx_rt(g, G['hr'], 3)
    dg[..., TH, :, :] = d_dx_rt(g, G['hth'], 4)
    Gamma = core.christoffel(ginv, dg)
    dGamma = torch.zeros(*Gamma.shape[:-3], 4, 4, 4, 4, device=g.device)
    dGamma[..., R, :, :, :] = d_dx_rt(Gamma, G['hr'], 3)
    dGamma[..., TH, :, :, :] = d_dx_rt(Gamma, G['hth'], 4)
    Gmn, Ric, Rscal = core.einstein(g, ginv, Gamma, dGamma)
    return Gmn, ginv


def hedgehog_n_rt(Th, G):
    # Th shape (Nr,Nth); broadcast to (Nr,Nth,1) for the field builder
    return mat.hedgehog_n(Th[..., None], G['Tht'], G['Ps'])


def matter_stress_rt(n, g, ginv, G):
    dn = torch.zeros(*n.shape[:-1], 4, 4, device=n.device)
    dn[..., R, :] = d_dx_rt(n, G['hr'], 3)
    dn[..., TH, :] = d_dx_rt(n, G['hth'], 4)
    Tab, L, L2, L4 = mat.stress_tensor(g, ginv, dn, XI, KAP)
    return Tab, L


def residual_mixed_rt(a, b, c, d, Th, G, kap8):
    g = metric_from_abcd(a, b, c, d, G)
    Gmn, ginv = full_einstein_rt(g, G)
    n = hedgehog_n_rt(Th, G)
    Tab, L = matter_stress_rt(n, g, ginv, G)
    Gud = torch.einsum('...am,...mb->...ab', ginv, Gmn)
    Tud = torch.einsum('...am,...mb->...ab', ginv, Tab)
    Res = Gud - kap8*Tud
    return Res, g, ginv


# ===========================================================================
# MASKS + proper-volume weight.
# ===========================================================================
def make_mask_weight(G, g, rfreeze=1.0, mr=2, mth=2):
    Nr, Nth = G['Nr'], G['Nth']
    rok = torch.ones(Nr, dtype=torch.bool, device=DEV)
    rok[:mr] = False; rok[-mr:] = False
    rok &= (G['rg'] > G['rc'] + rfreeze)
    rok &= (G['rg'] < G['ri'] - 0.5)
    thok = torch.ones(Nth, dtype=torch.bool, device=DEV)
    thok[:mth] = False; thok[-mth:] = False
    mask = (rok[:, None] & thok[None, :])              # (Nr,Nth)
    sdet = torch.sqrt(torch.abs(torch.linalg.det(g)))[..., 0]   # (Nr,Nth)
    w = sdet * mask
    w = w / (w.max() + 1e-300)
    return mask, w


# ===========================================================================
# MATTER relaxation: exact action gradient (autograd), preconditioned, monotone.
# ===========================================================================
def matter_action(Th, g, ginv, sqrtg, G):
    n = hedgehog_n_rt(Th, G)
    dn = torch.zeros(*n.shape[:-1], 4, 4, device=n.device)
    dn[..., R, :] = d_dx_rt(n, G['hr'], 3)
    dn[..., TH, :] = d_dx_rt(n, G['hth'], 4)
    Gmn = mat.field_metric(dn)
    L, _, _, _ = mat.lagrangian(ginv, Gmn, XI, KAP)
    return (sqrtg * L[..., 0]).sum()


def relax_theta(Th, g, ginv, G, m=1, steps=8, max_step=0.05):
    sqrtg = torch.sqrt(torch.clamp(-torch.linalg.det(g), min=1e-30))[..., 0]
    w = (ginv[..., R, R, ].abs()/G['hr']**2 + ginv[..., TH, TH].abs()/G['hth']**2)[..., 0]
    w = w.clamp(min=1e-6)
    Th = Th.detach().clone()
    S0 = matter_action(Th, g, ginv, sqrtg, G).item()
    for _ in range(steps):
        Thv = Th.clone().requires_grad_(True)
        Stot = matter_action(Thv, g, ginv, sqrtg, G)
        grad, = torch.autograd.grad(Stot, Thv)
        dd = grad/w
        scale = min(1.0, max_step/(dd.abs().max().item() + 1e-30))
        dd = dd*scale
        acc = False
        for lr in (0.5, 0.2, 0.08, 0.03):
            Tt = Th - lr*dd
            Tt[0, :] = m*PI; Tt[-1, :] = 0.0
            Tt = torch.clamp(Tt, -0.5, m*PI+0.5)
            St = matter_action(Tt, g, ginv, sqrtg, G).item()
            if St <= S0:
                Th = Tt; S0 = St; acc = True; break
        if not acc:
            break
    return Th


# ===========================================================================
# METRIC LM STEP (matrix-free, autograd JVP/VJP + CG on normal eqs), strict
# monotone acceptance.  Unknowns u=(a,b,c,d) on the FREE interior; the OUTER ring
# of (a,b,c,d) is the gauge/asymptotic anchor (Dirichlet from the seed far field).
# ===========================================================================
def pack(a, b, c, d):
    return torch.stack([a, b, c, d], dim=0)


def matter_el_field(Th, g, ginv, sqrtg, G, m=1):
    """EL residual field for Theta from the action delta(integral sqrt|g| L)/delta Theta
    (autograd; the action IS the physics).  Returns a field (Nr,Nth)."""
    Thv = Th.detach().clone().requires_grad_(True)
    S = matter_action(Thv, g, ginv, sqrtg, G)
    grad, = torch.autograd.grad(S, Thv, create_graph=True)
    return grad


def metric_lm_solve(a, b, c, d, Th, G, kap8, outer=30, cg_iters=80, mu0=1e-2,
                    rfreeze=1.0, mr=2, mth=2, m=1, anchor=None, verbose=True, tag="",
                    w_matter=1.0):
    """JOINT monotone LM descent on ALL FIVE fields (a,b,c,d,Theta) at once.  The
    objective Phi = ||sqrt(W)(G^mu_nu-kap8 T^mu_nu)||^2  +  w_matter*||sqrt(W) EL_Theta||^2
    -- the WHOLE coupled system in ONE least-squares.  Including Theta as an unknown (not
    an alternating sub-relax) is the fix for the cross-coupling divergence: alternating
    metric-Phi-descent with matter-action-descent is NOT jointly monotone (the matter step
    can raise the metric residual).  Strict monotone acceptance + mu floor 1e-7."""
    u = pack(a, b, c, d)                        # (4,Nr,Nth)
    Th = Th.detach().clone()
    if anchor is None:
        anchor = u[:, -1, :].clone()
    core_ring = u[:, 0, :].clone()
    # free mask over the 5-field stack
    free = torch.ones(5, *u.shape[1:], dtype=torch.bool, device=u.device)
    free[:4, -1, :] = False                     # metric outer ring (gauge anchor)
    free[:4, 0, :] = False                      # metric core ring (regularity)
    free[4, 0, :] = False; free[4, -1, :] = False   # Theta core(=m*pi)+outer(=0) BCs

    g0 = metric_from_abcd(u[0], u[1], u[2], u[3], G)
    mask, w = make_mask_weight(G, g0, rfreeze=rfreeze, mr=mr, mth=mth)
    sw = torch.sqrt(w)
    wm = math.sqrt(w_matter)

    def setbc(v):
        v = v.clone()
        v[:4, -1, :] = anchor; v[:4, 0, :] = core_ring
        v[4, 0, :] = m*PI; v[4, -1, :] = 0.0
        return v

    def Fvec(v):
        aa, bb, ccx, dd_, Tn = v[0], v[1], v[2], v[3], v[4]
        Res, g, ginv = residual_mixed_rt(aa, bb, ccx, dd_, Tn, G, kap8)
        comps = [Res[..., 0, T, T], Res[..., 0, R, R], Res[..., 0, TH, TH], Res[..., 0, PS, PS]]
        sqrtg = torch.sqrt(torch.clamp(-torch.linalg.det(g), min=1e-30))[..., 0]
        el = matter_el_field(Tn, g, ginv, sqrtg, G, m=m)
        F = torch.stack([sw*comps[0], sw*comps[1], sw*comps[2], sw*comps[3], wm*sw*el], dim=0)
        return F

    def phi(v):
        return (Fvec(v)**2).sum().item()

    v = torch.cat([u, Th[None]], dim=0)
    mu = mu0
    hist = []
    for it in range(outer):
        v0 = setbc(v).detach()
        F0 = Fvec(v0).detach()
        phi0 = (F0**2).sum().item()

        def Ffun(z):
            return Fvec(setbc(z))
        def Jv(z):
            _, jv = torch.autograd.functional.jvp(Ffun, (v0,), (z,), strict=False)
            return jv
        def JTv(y):
            vz = v0.clone().requires_grad_(True)
            Fz = Ffun(vz)
            gg, = torch.autograd.grad(Fz, vz, grad_outputs=y)
            return gg
        b_rhs = (-JTv(F0)) * free
        dd = torch.zeros_like(b_rhs)
        rr = b_rhs.clone(); p = rr.clone(); rs = (rr*rr).sum()
        bn = b_rhs.norm() + 1e-30
        for _ in range(cg_iters):
            Ap = (JTv(Jv(p*free))*free) + mu*(p*free)
            denom = (p*Ap).sum()
            if denom.abs() < 1e-300:
                break
            al = rs/denom
            dd = dd + al*p; rr = rr - al*Ap
            rsn = (rr*rr).sum()
            if rsn.sqrt()/bn < 1e-4:
                break
            p = rr + (rsn/rs)*p; rs = rsn
        dd = dd*free
        acc = False; best_phi = phi0; best_v = setbc(v0)
        for ls in (1.0, 0.5, 0.25, 0.1, 0.03, 0.01):
            vt = setbc(v0 + ls*dd); pt = phi(vt)
            if pt < best_phi:
                best_phi = pt; best_v = vt; acc = True
                if pt < 0.999*phi0:
                    break
        if acc and best_phi < phi0:
            v = best_v; mu = max(mu*0.6, 1e-7)
        else:
            mu = min(mu*5, 1e4); v = setbc(v0)
        phinew = phi(setbc(v)); maxr = Fvec(setbc(v)).abs().max().item()
        hist.append((it, phi0, phinew, maxr))
        if verbose and (it % 2 == 0 or it == outer-1):
            print(f"  [{tag}] it={it:3d} Phi={phi0:.4e}->{phinew:.4e} max|F|={maxr:.3e} "
                  f"mu={mu:.1e} acc={acc}", flush=True)
        if phinew < 1e-14:
            break
    v = setbc(v)
    return v[0], v[1], v[2], v[3], v[4], hist
