#!/usr/bin/env python3
"""
gapcloser_solver.py -- THE GAP-CLOSER: a robust GAUGE-FIXED NONLINEAR solver for the
full stationary UDT metric+matter system on a (r,theta,psi) grid (or its (r,theta)
axisymmetric reduction), built to close the one capability that #57
(whole_metric_full_solve_results.md, Section 6) left OUTSTANDING:

    a fully-nonlinear, ARBITRARY-SEED, gauge-fixed solve, so that
    qualitatively-different seeds can be relaxed and CLASSIFIED -- does UDT admit a
    STABLE soliton type DISCONNECTED from the round family, or only the one round
    family?

Driver: Claude (Opus 4.8, 1M).  2026-06-15.  OBSERVE mode.  DATA-BLIND (units
L = sqrt(kappa/xi) = 1; NO wall numbers, NO comparison to nature).

=============================================================================
THE DIAGNOSED RECIPE (from #57, implemented here -- NOT new physics):

 (i)  ANCHOR/EXCISE the coordinate-singular core: the inner shell r < rc+rfreeze and
      the theta near-axis points are FROZEN to a regular seed (a center/axis-regularity
      BC), so the deep-core coordinate spike (res~442 at r=0.05 vs 1e-6 body, #55 v11.2)
      cannot dominate |F|.  Standard NR excision.  (CHOSE: numerical conditioning BC.)

 (ii) GEOMETRY-WEIGHT the residual by sqrt(proper volume) ~ r * sqrt|det g_spatial| so
      coordinate (1/r^2, 1/sin^2) amplification toward the core/axis does not swamp the
      body in the least-squares norm.  Diagonal equilibration; does NOT change the
      solution set.  (CHOSE: conditioning.)

 (iii) FIX THE GAUGE.  The Einstein residual G^mu_nu - k8 T^mu_nu has the FULL
      diffeomorphism group as an exact null space (x -> x+xi leaves a solution a
      solution): this is precisely the "wander into coordinate directions" failure mode
      of #57.  We remove it with a REFERENCE-METRIC (Brown-style) gauge condition.
      The de Donder operator H^mu := g^{ab} Gamma^mu_{ab}[g] measures the coordinates;
      its linearization spans exactly the diffeomorphism generators.  We do NOT force
      H -> 0 (that would force harmonic coordinates, and the areal-gauge round #56
      soliton is NOT harmonic -> H_ref ~ 1.5 there; penalizing |H| would PUSH the solver
      off the validated soliton -- a real bug we caught at the smoke-test stage).  Instead
      we penalize  H^mu[g] - H^mu_REF , where H_REF is computed ONCE from a FIXED round
      BACKGROUND coordinate frame (areal coordinates) and FROZEN.  Minimizing
            ||Res||^2 + w_gauge * ||H - H_ref||^2
      pins the coordinate freedom relative to that fixed frame WITHOUT restricting
      physics: the round soliton sits at H = H_ref by construction (a true fixed point,
      so the gate is preserved), while ANY pure coordinate deformation moves H away from
      H_ref and is penalized -- killing the diffeomorphism null space.  This is the
      standard NR reference-coordinate gauge; it is a COORDINATE condition
      (non-restrictive), NOT a physical constraint (we do NOT impose rho=r, do NOT impose
      diagonal, do NOT impose B=1/A).  Verified non-restrictive by the gate (#56 recovered)
      AND the perturbed-seed robustness test (relax-back).  (DERIVED-need: the gauge fixer.)

      Charter principle 4: H^mu = g^{ab}Gamma^mu_{ab} is the standard GR de Donder
      operator, transformed onto this grid; principle 1: it adds no coupling/source/
      mechanism -- it only labels coordinates.  Principle 2: full nonlinear throughout;
      the only sanctioned function-replacements are FD derivatives, autograd Jacobian-
      vector products, and clamps guarding transient iterates.

THE OBJECTIVE solved by a robust gauge-fixed Gauss-Newton / Levenberg-Marquardt with
matrix-free autograd JVP/VJP (V100-safe: dense small ops + matmul; NO broadcast
solve_triangular):
      Phi(g) = || w_geom * (G^mu_nu[g] - k8 T^mu_nu[n,g]) ||^2
             + w_gauge * || w_geom * H^mu[g] ||^2
matter field n relaxed in the same outer loop by the exact action gradient.

The Einstein engine (whole_metric_3d_core), matter stress (whole_metric_3d_matter),
and grid/FD helpers (whole_metric_3d_solver) are REUSED unchanged (validated; #55/#56).
"""
import os
os.environ.setdefault("PYTORCH_NVML_BASED_CUDA_CHECK", "0")
import math
import torch

torch.set_default_dtype(torch.float64)
DEV = "cuda" if torch.cuda.is_available() else "cpu"
T, R, TH, PS = 0, 1, 2, 3
XI = 1.0
KAP = 1.0
EXP_CLAMP = 60.0

import whole_metric_3d_core as core
import whole_metric_3d_matter as mat
import whole_metric_3d_solver as S

# The 10 independent symmetric components.
SYM_IDX = [(0, 0), (1, 1), (2, 2), (3, 3), (0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]


# ===========================================================================
# GAUGE FUNCTIONAL  H^mu = g^{ab} Gamma^mu_{ab}  (de Donder / harmonic).
# Built from the same Christoffel the validated engine uses.  Vanishes in
# harmonic coordinates; its linearization = the diffeomorphism generators.
# ===========================================================================
def harmonic_gauge(g, G):
    ginv = core.metric_inverse(g)
    dg = torch.zeros(*g.shape[:-2], 4, 4, 4, device=g.device)
    dg[..., R, :, :]  = S.d_dx(g, G['hr'], 3)
    dg[..., TH, :, :] = S.d_dx(g, G['hth'], 4)
    dg[..., PS, :, :] = S.d_dx(g, G['hps'], 5)
    Gamma = core.christoffel(ginv, dg)            # Gamma[...,a,b,c]=Gamma^a_{bc}
    # H^mu = g^{bc} Gamma^mu_{bc}
    H = torch.einsum('...bc,...abc->...a', ginv, Gamma)
    return H, ginv


# ===========================================================================
# Full mixed Einstein residual (validated engine).
# ===========================================================================
def residual_mixed(g, n, kap8, G):
    Gmn, ginv, Ric, Rscal = S.full_einstein(g, G)
    Tab, dn, L = S.matter_stress(n, g, ginv, G)
    Gud = torch.einsum('...am,...mb->...ab', ginv, Gmn)
    Tud = torch.einsum('...am,...mb->...ab', ginv, Tab)
    return Gud - kap8*Tud, ginv


# ===========================================================================
# GEOMETRY WEIGHT  w_geom ~ (proper-volume)^{1/2} factor that DE-amplifies the
# coordinate 1/r^2, 1/sin^2 blow-up.  Use r * sqrt(sin theta-clamped); for the
# axisymmetric (r,theta) run the psi axis is a single slice and the weight is the same.
# Diagonal equilibration of the least-squares norm -- does NOT change the solution set.
# ===========================================================================
def geom_weight(G):
    return G['Rr'] * torch.sqrt(torch.sin(G['Tht']).clamp(min=1e-3))


# ===========================================================================
# PACK / UNPACK the FREE metric components.
# ===========================================================================
def make_masks(G, free_components, mr=2, mth=2, rfreeze=1.0, axisym=False):
    """interior mask (which gridpoints are FREE) and component free-list.
    Frozen: r boundary (mr cells), theta boundary (mth cells; the axis region),
    and the inner coordinate-singular shell r<rc+rfreeze.  psi periodic (all free)."""
    Nr, Nth, Nps = G['Nr'], G['Nth'], G['Nps']
    interior = torch.zeros(Nr, Nth, Nps, dtype=torch.bool, device=DEV)
    interior[mr:Nr-mr, mth:Nth-mth, :] = True
    interior[G['rg'] < G['rc']+rfreeze, :, :] = False
    mask = torch.zeros(Nr, Nth, Nps, 10, dtype=torch.bool, device=DEV)
    for k, comp in enumerate(SYM_IDX):
        if comp in free_components or (comp[1], comp[0]) in free_components:
            mask[..., k] = interior
    return mask, interior


def g_to_flat(g):
    flat = torch.zeros(g.shape[:-2] + (10,), device=g.device)
    for k, (a, b) in enumerate(SYM_IDX):
        flat[..., k] = g[..., a, b]
    return flat


def flat_to_g(flat):
    g = torch.zeros(flat.shape[:-1] + (4, 4), device=flat.device)
    for k, (a, b) in enumerate(SYM_IDX):
        g[..., a, b] = flat[..., k]
        if a != b:
            g[..., b, a] = flat[..., k]
    return g


def g_from_x(x, g_base, mask):
    flat = g_to_flat(g_base)
    flat = flat.clone()
    flat[mask] = x
    return flat_to_g(flat)


def x_from_g(g, mask):
    return g_to_flat(g)[mask].clone()


# ===========================================================================
# THE AUGMENTED RESIDUAL VECTOR  r(x) = [ w_geom*(G-k8 T)  ;  sqrt(w_gauge)*w_geom*H ]
# stacked over the FREE interior points (Einstein eqs) and ALL interior points (gauge).
# ===========================================================================
def resid_vector(x, g_base, n, kap8, G, mask, interior, wgeom, w_gauge, H_ref=None):
    g = g_from_x(x, g_base, mask)
    Res, ginv = residual_mixed(g, n, kap8, G)            # (...,4,4) mixed
    # symmetric combination (physical content of the mixed residual)
    rflat = torch.zeros(Res.shape[:-2] + (10,), device=g.device)
    for k, (a, b) in enumerate(SYM_IDX):
        rflat[..., k] = 0.5*(Res[..., a, b] + Res[..., b, a])
    rflat = rflat * wgeom[..., None]
    einstein_part = rflat[mask]                            # only the FREE equations
    if w_gauge > 0:
        H, _ = harmonic_gauge(g, G)                        # (...,4)
        if H_ref is not None:
            H = H - H_ref                                  # REFERENCE gauge: H - H_ref
        H = H * wgeom[..., None] * math.sqrt(w_gauge)
        gauge_part = H[interior]                           # 4 per interior point
        return torch.cat([einstein_part, gauge_part.reshape(-1)])
    return einstein_part


# ===========================================================================
# MATTER relaxation: exact action gradient of the validated L2+L4 (autograd),
# preconditioned by the diagonal inverse-metric weight.  Hedgehog profile Th.
# ===========================================================================
def _matter_action(Th, g, ginv, sqrtg, G):
    n = mat.hedgehog_n(Th, G['Tht'], G['Ps'])
    dn = torch.zeros(*n.shape[:-1], 4, 4, device=DEV)
    dn[..., R, :]  = S.d_dx(n, G['hr'], 3)
    dn[..., TH, :] = S.d_dx(n, G['hth'], 4)
    dn[..., PS, :] = S.d_dx(n, G['hps'], 5)
    Gmn = mat.field_metric(dn)
    Lf, _, _, _ = mat.lagrangian(ginv, Gmn, XI, KAP)
    return (sqrtg*Lf).sum()


def relax_Th(Th, g, G, bc_core, bc_seal, steps=6, lr=0.15, max_step=0.05):
    """STABLE preconditioned action descent for the hedgehog profile Th, with a
    BACKTRACKING line search that rejects any step raising the action and a per-step
    magnitude CLAMP (max_step).  The raw explicit descent of the L2+L4 (native-Skyrme,
    4th-order) action is STIFF and diverges (caught at smoke-test: |dTh| -> 593 in 4
    steps); this version is unconditionally monotone -- the standard fix.  The matter
    EL it minimizes is the SAME validated action (whole_metric_3d_matter); no physics
    changed, only the iteration is stabilized (principle 2: sanctioned numerics)."""
    ginv = core.metric_inverse(g)
    sqrtg = torch.sqrt(torch.clamp(-torch.linalg.det(g), min=1e-30))
    w = (ginv[..., R, R].abs()/G['hr']**2 + ginv[..., TH, TH].abs()/G['hth']**2
         + ginv[..., PS, PS].abs()/G['hps']**2).clamp(min=1e-6)
    Th = Th.detach().clone()
    S0 = _matter_action(Th, g, ginv, sqrtg, G).item()
    for _ in range(steps):
        Thv = Th.clone().requires_grad_(True)
        Stot = _matter_action(Thv, g, ginv, sqrtg, G)
        grad, = torch.autograd.grad(Stot, Thv)
        d = grad/w
        # clamp the step magnitude (avoid stiff overshoot)
        scale = min(1.0, max_step/(d.abs().max().item() + 1e-30))
        d = d*scale
        accepted = False
        for ls in (lr, 0.5*lr, 0.2*lr, 0.05*lr):
            Tt = Th - ls*d
            Tt[0, :, :] = bc_core; Tt[-1, :, :] = bc_seal
            Tt = torch.clamp(Tt, -0.5, math.pi+0.5)
            St = _matter_action(Tt, g, ginv, sqrtg, G).item()
            if St <= S0:
                Th = Tt; S0 = St; accepted = True
                break
        if not accepted:
            break
    return Th


# ===========================================================================
# GAUSS-NEWTON / LEVENBERG-MARQUARDT step (matrix-free CG on normal equations).
# (J^T J + mu I) dx = -J^T r.   V100-safe.
# ===========================================================================
def gn_step(x, g_base, n, kap8, G, mask, interior, wgeom, w_gauge,
            mu=1e-4, cg_iters=40, cg_tol=1e-3, H_ref=None):
    def rfun(z):
        return resid_vector(z, g_base, n, kap8, G, mask, interior, wgeom, w_gauge, H_ref)
    x0 = x.detach()
    r0 = rfun(x0).detach()

    def Jv(v):
        _, jv = torch.autograd.functional.jvp(rfun, (x0,), (v,),
                                              create_graph=False, strict=False)
        return jv

    def JTv(w):
        xz = x0.clone().requires_grad_(True)
        rz = rfun(xz)
        gg, = torch.autograd.grad(rz, xz, grad_outputs=w, retain_graph=False)
        return gg

    b = -JTv(r0)
    dx = torch.zeros_like(b)
    rr = b.clone(); p = rr.clone()
    rs_old = (rr@rr).item()
    bn = math.sqrt((b@b).item()) + 1e-30
    for _ in range(cg_iters):
        Ap = JTv(Jv(p)) + mu*p
        denom = (p@Ap).item()
        if abs(denom) < 1e-300:
            break
        alpha = rs_old/denom
        dx = dx + alpha*p
        rr = rr - alpha*Ap
        rs_new = (rr@rr).item()
        if math.sqrt(rs_new)/bn < cg_tol:
            break
        p = rr + (rs_new/rs_old)*p
        rs_old = rs_new
    return dx.detach(), math.sqrt((r0@r0).item())


# ===========================================================================
# Body residual diagnostics (the GATE quantity): strip core/axis FD edges, report
# the max diagonal and off-diagonal mixed Einstein residual + M_MS + gauge norm.
# ===========================================================================
def body_diagnostics(g, n, kap8, G, mask_core=1.0, mth_strip=4):
    Res, ginv = residual_mixed(g, n, kap8, G)
    rmask = (G['rg'] > G['rc']+mask_core) & (G['rg'] < G['ri']-0.5)
    i0 = int(rmask.float().argmax().item())
    i1 = int(G['Nr']-1-rmask.flip(0).float().argmax().item())
    body = Res[i0:i1, mth_strip:-mth_strip, :]
    rdiag = max(body[..., a, a].abs().max().item() for a in range(4))
    roff = max((body[..., a, b].abs().max().item() for a in range(4)
                for b in range(4) if a != b), default=0.0)
    H, _ = harmonic_gauge(g, G)
    Hbody = H[i0:i1, mth_strip:-mth_strip, :]
    hmax = Hbody.abs().max().item()
    return dict(rdiag=rdiag, roff=roff, hmax=hmax, i0=i0, i1=i1)


# ===========================================================================
# Misner-Sharp-like mass from g_rr on the EQUATOR (a gauge-invariant scalar to
# compare seeds).  For a general metric we read the areal radius R_areal =
# sqrt(g_thth) and m via e^{-2b}=1-2m/R_areal using g^{rr}.  This is a SCALAR
# invariant readout, used only to COMPARE candidates at the same charge.
# ===========================================================================
def mass_readout(g, G, mask_core=1.0):
    ginv = core.metric_inverse(g)
    # areal radius from g_thth (equator)
    jeq = G['Nth']//2
    grr = ginv[..., R, R]                          # g^{rr}
    Rareal = torch.sqrt(g[..., TH, TH].clamp(min=1e-30))
    f = 1.0/grr.clamp(min=1e-30)                    # ~ 1-2m/Rareal for diagonal
    m = 0.5*Rareal*(1.0 - f)
    # take the value at the outer body (just inside the seal) on the equator
    iout = G['Nr']-3
    return m[iout, jeq, 0].item(), Rareal[iout, jeq, 0].item()


# ===========================================================================
# THE FULL GAUGE-FIXED NONLINEAR SOLVE.
# ===========================================================================
def solve(g0, Th0, kap8, G, free_components, bc_core, bc_seal,
          outer=40, lam=1.0, mu=1e-3, cg_iters=40, mask_core=1.0, rfreeze=1.0,
          w_gauge=1.0, matter_steps=6, matter_lr=0.12, mr=2, mth=2,
          tol=1e-9, verbose=True, tag="", relax_matter=True, H_ref=None, g_ref=None):
    """H_ref / g_ref: the FIXED reference-coordinate frame for the gauge condition.
    If g_ref is given, H_ref is computed from it once and frozen (the standard
    reference-metric gauge).  If neither given and w_gauge>0, H_ref is taken from g0
    (anchors coordinates to the SEED frame -- still removes the diffeo null space)."""
    g_base = g0.clone()
    mask, interior = make_masks(G, free_components, mr=mr, mth=mth, rfreeze=rfreeze)
    wgeom = geom_weight(G)
    if w_gauge > 0 and H_ref is None:
        ref = g_ref if g_ref is not None else g0
        H_ref, _ = harmonic_gauge(ref, G)
        H_ref = H_ref.detach()
    x = x_from_g(g0, mask)
    Th = Th0.clone()
    n = mat.hedgehog_n(Th, G['Tht'], G['Ps'])
    hist = []
    mu_cur = mu
    prev = None
    for it in range(outer):
        g_cur = g_from_x(x, g_base, mask)
        if relax_matter:
            Th = relax_Th(Th, g_cur, G, bc_core, bc_seal, steps=matter_steps, lr=matter_lr)
            n = mat.hedgehog_n(Th, G['Tht'], G['Ps'])
        dx, rnorm = gn_step(x, g_base, n, kap8, G, mask, interior, wgeom, w_gauge,
                            mu=mu_cur, cg_iters=cg_iters, H_ref=H_ref)
        # backtracking line search on the augmented objective
        best = None
        for ls in [lam, 0.5*lam, 0.25*lam, 0.1*lam, 0.03*lam, 0.01*lam]:
            xt = x + ls*dx
            rt = resid_vector(xt, g_base, n, kap8, G, mask, interior, wgeom, w_gauge, H_ref)
            fn = math.sqrt((rt@rt).item())
            if best is None or fn < best[1]:
                best = (xt, fn, ls)
            if fn < rnorm:
                break
        x, rnorm_new, used = best
        # adapt LM damping
        if rnorm_new < rnorm:
            mu_cur = max(mu_cur*0.7, 1e-8)
        else:
            mu_cur = min(mu_cur*2.0, 1e2)
        g_cur = g_from_x(x, g_base, mask)
        d = body_diagnostics(g_cur, n, kap8, G, mask_core=mask_core)
        hist.append((it, rnorm, rnorm_new, d['rdiag'], d['roff'], d['hmax'], used))
        if verbose and (it % 2 == 0 or it == outer-1):
            print(f"  [{tag}] it={it} |r|={rnorm:.3e}->{rnorm_new:.3e} "
                  f"body diag={d['rdiag']:.3e} off={d['roff']:.3e} H={d['hmax']:.3e} "
                  f"step={used:.3f} mu={mu_cur:.1e}", flush=True)
        if rnorm_new < tol:
            break
        if prev is not None and abs(prev - rnorm_new)/(prev+1e-30) < 1e-6 and used < 0.02:
            if verbose:
                print(f"  [{tag}] stalled at |r|={rnorm_new:.3e}", flush=True)
            break
        prev = rnorm_new
    g_final = g_from_x(x, g_base, mask)
    return dict(g=g_final, Th=Th, hist=hist, mask=mask, interior=interior)
