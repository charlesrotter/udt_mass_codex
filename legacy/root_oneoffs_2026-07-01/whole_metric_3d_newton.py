#!/usr/bin/env python3
"""
whole_metric_3d_newton.py -- THE FULL 3-D COUPLED SOLVER via matrix-free Newton-Krylov
on the FULL Einstein residual, using autograd through the VALIDATED engine.

Driver: Claude (Opus 4.8, 1M).  2026-06-15.  OBSERVE mode.  DATA-BLIND.
Frame: whole_metric_solve_MAP.md realization (A).

THE CAPABILITY (the unproven one): SOLVE the full coupled stationary system -- all 10
metric components + matter, NO symmetry, off-diagonals live -- by driving the FULL
numerical Einstein residual to zero.

METHOD (charter principle 4: transformed NR numerics; principle 2: full nonlinear,
sanctioned FD/autograd, NO linearization-as-result):

  Unknown vector u = the FREE metric components on the interior grid (+ matter, sector-
  iterated).  Residual F(u) = mixed Einstein residual G^mu_nu - kappa8 T^mu_nu computed
  by the VALIDATED engine (whole_metric_3d_core/matter).  Damped Newton:
        J(u) du = -F(u),   u <- u + lambda du
  with J the EXACT Jacobian of the validated residual obtained MATRIX-FREE by torch
  autograd Jacobian-vector products (jvp), and du solved by CG on the normal equations
  (Gauss-Newton / Levenberg-Marquardt: (J^T J + mu I) du = -J^T F), which is robust for
  the over/mixed-determined Einstein system.  This is the standard NR nonlinear solver;
  the residual is the full numerical engine throughout (NO closed-form G, NO hand-derived
  elliptic reduction, NO linearization kept as a result -- the Newton step is the
  sanctioned local linearization of the solver, discarded each iterate).

  Matter (the hedgehog profile Th, and in the full run the target angles) is relaxed in
  the same outer loop by the exact action gradient (autograd of the validated L2+L4).

BC's: center/axis regularity, the seal mirror-fold (time-row off-diagonals node at the
seal), finite cell -- imposed by FREEZING those components (excluded from u).
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

import whole_metric_3d_core as core
import whole_metric_3d_matter as mat
import whole_metric_3d_solver as S


# ===========================================================================
# Residual as a function of the FULL metric tensor field g (symmetric 4x4 per point)
# and the matter field n.  Differentiable (torch).  Returns the MIXED residual stacked.
# ===========================================================================
def residual_of_g(g, n, kap8, G):
    Gmn, ginv, Ric, Rscal = S.full_einstein(g, G)
    Tab, dn, L = S.matter_stress(n, g, ginv, G)
    Gud = torch.einsum('...am,...mb->...ab', ginv, Gmn)
    Tud = torch.einsum('...am,...mb->...ab', ginv, Tab)
    return Gud - kap8*Tud      # (...,4,4) mixed residual


# ===========================================================================
# PACK / UNPACK.  The 10 independent metric components live in the symmetric 4x4.
# We optimize a vector x of the 10 components at the FREE (interior) grid points; the
# boundary points and any FROZEN components are held fixed from g_base.
# ===========================================================================
SYM_IDX = [(0, 0), (1, 1), (2, 2), (3, 3), (0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]


def make_freemask(G, free_components, mr=1, mth=1, rcore_freeze=1.0):
    """Boolean mask (Nr,Nth,Nps,10) of which (component, gridpoint) are FREE.
    Boundary in r and theta is frozen (BCs); psi periodic so all psi free.
    The INNER coordinate-singular shell r < rc+rcore_freeze is FROZEN to the seed:
    there the metric carries 1/r^2, 1/sin^2theta coordinate factors that make the
    residual a (non-physical) coordinate spike ~O(100) -- anchoring it to the regular
    radial center (a center-regularity BC, physically the soliton's smooth core) keeps
    the global solve in the REGULAR body where the equations are well-conditioned.
    This is standard NR practice (excise/anchor the coordinate-singular core); the
    #55 verifier independently documented the deep-core spike as coordinate, not physics."""
    Nr, Nth, Nps = G['Nr'], G['Nth'], G['Nps']
    mask = torch.zeros(Nr, Nth, Nps, 10, dtype=torch.bool, device=DEV)
    interior = torch.zeros(Nr, Nth, Nps, dtype=torch.bool, device=DEV)
    interior[mr:Nr-mr, mth:Nth-mth, :] = True
    rfreeze = (G['rg'] < G['rc']+rcore_freeze)
    interior[rfreeze, :, :] = False
    for k, comp in enumerate(SYM_IDX):
        if comp in free_components or (comp[1], comp[0]) in free_components:
            mask[..., k] = interior
    return mask


def g_from_x(x, g_base, mask):
    """Scatter the free vector x into a full symmetric metric tensor."""
    g = g_base.clone()
    flat = torch.zeros(g_base.shape[:-2] + (10,), device=DEV)
    flat_base = torch.zeros_like(flat)
    for k, (a, b) in enumerate(SYM_IDX):
        flat_base[..., k] = g_base[..., a, b]
    flat = flat_base.clone()
    flat[mask] = x
    for k, (a, b) in enumerate(SYM_IDX):
        g[..., a, b] = flat[..., k]
        if a != b:
            g[..., b, a] = flat[..., k]
    return g


def x_from_g(g, mask):
    flat = torch.zeros(g.shape[:-2] + (10,), device=DEV)
    for k, (a, b) in enumerate(SYM_IDX):
        flat[..., k] = g[..., a, b]
    return flat[mask].clone()


# ===========================================================================
# Residual vector F(x) (only the FREE-equation entries: the mixed residual at the
# free interior points, all components -- the equations we drive to zero).
# ===========================================================================
def geom_weight(G):
    """Per-point residual weight ~ r^2 (and sin theta) so the mixed Einstein eqs, which
    carry 1/r^2 / 1/sin^2 coordinate amplification toward the core/axis, contribute
    UNIFORMLY across the body in the least-squares norm (a diagonal equilibration of the
    normal equations -- standard; does NOT change the solution set, only conditioning)."""
    w = (G['Rr']**2) * torch.sin(G['Tht']).clamp(min=1e-3)
    return w


def F_of_x(x, g_base, n, kap8, G, mask, eqmask, wgeom=None):
    g = g_from_x(x, g_base, mask)
    Res = residual_of_g(g, n, kap8, G)        # (...,4,4) mixed
    Rflat = torch.zeros(Res.shape[:-2] + (10,), device=DEV)
    for k, (a, b) in enumerate(SYM_IDX):
        # mixed residual is NOT symmetric in general; enforce the symmetric combination
        # (the physical content) -- adequate for the stationary case.  Use (ab+ba)/2.
        Rflat[..., k] = 0.5*(Res[..., a, b] + Res[..., b, a])
    if wgeom is not None:
        Rflat = Rflat * wgeom[..., None]
    return Rflat[eqmask]


# ===========================================================================
# Matrix-free JVP and Gauss-Newton CG solve of (J^T J + mu) du = -J^T F.
# ===========================================================================
def gauss_newton_step(x, g_base, n, kap8, G, mask, eqmask, mu=1e-6, cg_iters=40,
                      cg_tol=1e-3, wgeom=None):
    x = x.detach().clone().requires_grad_(True)
    F = F_of_x(x, g_base, n, kap8, G, mask, eqmask, wgeom)
    F0 = F.detach()

    def Jv(v):  # J @ v  (forward-mode via double-backward)
        _, jv = torch.autograd.functional.jvp(
            lambda z: F_of_x(z, g_base, n, kap8, G, mask, eqmask, wgeom),
            (x.detach(),), (v,), create_graph=False, strict=False)
        return jv

    def JTv(w):  # J^T @ w
        xz = x.detach().clone().requires_grad_(True)
        Fz = F_of_x(xz, g_base, n, kap8, G, mask, eqmask, wgeom)
        g, = torch.autograd.grad(Fz, xz, grad_outputs=w, retain_graph=False)
        return g

    b = -JTv(F0)                      # rhs of normal equations
    du = torch.zeros_like(b)
    rr = b.clone()
    p = rr.clone()
    rs_old = (rr@rr).item()
    b_norm = math.sqrt((b@b).item()) + 1e-30
    for _ in range(cg_iters):
        Ap = JTv(Jv(p)) + mu*p
        alpha = rs_old/((p@Ap).item() + 1e-30)
        du = du + alpha*p
        rr = rr - alpha*Ap
        rs_new = (rr@rr).item()
        if math.sqrt(rs_new)/b_norm < cg_tol:
            break
        p = rr + (rs_new/rs_old)*p
        rs_old = rs_new
    return du.detach(), math.sqrt((F0@F0).item())


# ===========================================================================
# Matter: exact action-gradient relaxation of the hedgehog profile Th.
# ===========================================================================
def relax_Th(Th, g, G, bc_core, bc_seal, steps=6, lr=0.15):
    ginv = core.metric_inverse(g)
    w = (ginv[..., R, R].abs()/G['hr']**2 + ginv[..., TH, TH].abs()/G['hth']**2
         + ginv[..., PS, PS].abs()/G['hps']**2).clamp(min=1e-6)
    for _ in range(steps):
        Thv = Th.detach().clone().requires_grad_(True)
        n = mat.hedgehog_n(Thv, G['Tht'], G['Ps'])
        dn = torch.zeros(*n.shape[:-1], 4, 4, device=DEV)
        dn[..., R, :]  = S.d_dx(n, G['hr'], 3)
        dn[..., TH, :] = S.d_dx(n, G['hth'], 4)
        dn[..., PS, :] = S.d_dx(n, G['hps'], 5)
        Gmn = mat.field_metric(dn)
        Lf, _, _, _ = mat.lagrangian(ginv, Gmn, XI, KAP)
        sqrtg = torch.sqrt(torch.clamp(-torch.linalg.det(g), min=1e-30))
        Stot = (sqrtg*Lf).sum()
        grad, = torch.autograd.grad(Stot, Thv)
        Th = Th - lr*grad/w
        Th[0, :, :] = bc_core; Th[-1, :, :] = bc_seal
    return Th


# ===========================================================================
# THE FULL COUPLED NEWTON SOLVE.
# ===========================================================================
def solve(g0, Th0, kap8, G, free_components, bc_core, bc_seal,
          outer=30, lam=0.5, mu=1e-5, cg_iters=30, mask_core=1.0,
          matter_steps=6, matter_lr=0.12, rcore_freeze=1.0, verbose=True, tag=""):
    g_base = g0.clone()
    mask = make_freemask(G, free_components, rcore_freeze=rcore_freeze)
    eqmask = mask.clone()              # enforce the eqs at the same free points/components
    wgeom = geom_weight(G)
    x = x_from_g(g0, mask)
    Th = Th0.clone()
    n = mat.hedgehog_n(Th, G['Tht'], G['Ps'])
    rmask = (G['rg'] > G['rc']+mask_core) & (G['rg'] < G['ri']-0.5)
    i0 = int(rmask.float().argmax().item())
    i1 = int(G['Nr']-1-rmask.flip(0).float().argmax().item())
    hist = []
    for it in range(outer):
        g_cur = g_from_x(x, g_base, mask)
        Th = relax_Th(Th, g_cur, G, bc_core, bc_seal, steps=matter_steps, lr=matter_lr)
        n = mat.hedgehog_n(Th, G['Tht'], G['Ps'])
        du, Fnorm = gauss_newton_step(x, g_base, n, kap8, G, mask, eqmask,
                                      mu=mu, cg_iters=cg_iters, wgeom=wgeom)
        # damped, with a simple backtracking line search on |F|
        best = None
        for ls in [lam, 0.5*lam, 0.25*lam, 0.1*lam, 0.03*lam]:
            xt = x + ls*du
            Ft = F_of_x(xt, g_base, n, kap8, G, mask, eqmask, wgeom)
            fn = math.sqrt((Ft@Ft).item())
            if best is None or fn < best[1]:
                best = (xt, fn, ls)
            if fn < Fnorm:
                break
        x, Fnorm_new, used = best
        # body diagnostics
        g_cur = g_from_x(x, g_base, mask)
        Res = residual_of_g(g_cur, n, kap8, G)
        body = Res[i0:i1, 8:-8, :]
        rdiag = max(body[..., a, a].abs().max().item() for a in range(4))
        roff = max((body[..., a, b].abs().max().item() for a in range(4)
                    for b in range(4) if a != b), default=0.0)
        hist.append((it, Fnorm, Fnorm_new, rdiag, roff, used))
        if verbose:
            print(f"  [{tag}] it={it} |F|={Fnorm:.3e}->{Fnorm_new:.3e} "
                  f"body diag={rdiag:.3e} off={roff:.3e} step={used:.3f}", flush=True)
        if Fnorm_new < 1e-9:
            break
    g_final = g_from_x(x, g_base, mask)
    return dict(g=g_final, Th=Th, hist=hist, i0=i0, i1=i1, mask=mask)
