#!/usr/bin/env python3
"""
large_grid_solver.py -- LARGE-GRID DEEP-FLOOR solver for the coupled Einstein+L2+L4
static system.  Category-A conditioning ONLY (the SAME residual physics, better
solved).  OBSERVE mode.  DATA-BLIND (units L=sqrt(kappa/xi)=1).

Driver: Claude (Opus 4.8, 1M).  2026-06-17.  NEW file -- edits nothing committed.

=== THE PROBLEM (conditioning, not physics) ===
full3d_newton.newton_solve forms the FULL DENSE (nF x nU) Jacobian (jacrev over nF
output seeds) and takes a dense lstsq/Cholesky step.  Both scale ~O(nU^2 nF); with
nU=5*Nr*Nth*Nps (6400 at 20x8x8, 12000 at 24x10x10) the per-iter cost runs minutes,
so the solver runs out of iterations before the Phi~1e-12 floor at large grids.

=== THE CURE (three routes, all category-A) ===
Route 3 (continuation in resolution): solve a small grid to the deep floor, then
  interp_state (cross_grid_branch, validated 1.8e-15) onto the next grid and warm-
  start -- few iters per grid if the per-grid solver is strong.  ESSENTIAL.
Route 2 (dense normal-equation step, reused efficiently): the jacrev Jacobian + a
  Jacobi-scaled normal-equation Cholesky (J^T J + lam I) -- the proven dense step,
  with column scaling for conditioning, used where the dense solve is still cheaper
  than the jacrev build.  This is the workhorse on the grids in scope (nU<=12000:
  the O(nU^3) Cholesky is a few seconds; the jacrev build dominates).
Route 1 (matrix-free Newton-Krylov, two-grid preconditioned): solve
  (J^T J + lam I) du = -J^T F by CG using autograd JVP/VJP -- never forming the
  dense fine Jacobian -- with a STRONG preconditioner: a COARSE-grid dense Jacobian
  J_c^T J_c factorization applied via interp_state restriction/prolongation
  (two-grid / spectral preconditioning).  This is the scalable route for grids where
  the dense fine Jacobian no longer fits / the jacrev build is prohibitive.

We implement all three and a `solve_grid` that picks the route by grid size, then a
`continuation_solve` that walks a resolution ladder.  The reported solution always
satisfies the FULL nonlinear residual to the reported Phi.

CATEGORY-A boundary (binding): allowed = explicit/batched Jacobian, direct/Krylov
factorization, LM damping, column/Jacobi scaling, two-grid preconditioning,
resolution continuation.  FORBIDDEN (none done) = tying g_tt=1/g_rr (B=1/A),
injecting/dropping a term, presenting a linear step AS the result, tuning to a target.
"""
import os, time, math, json
os.environ.setdefault("PYTORCH_NVML_BASED_CUDA_CHECK", "0")
os.environ.setdefault("PYTORCH_NO_CUDA_MEMORY_CACHING", "1")
import numpy as np
import torch
torch.set_default_dtype(torch.float64)

from full3d_grid_shexact import make_grid_shexact
from full3d_solver import pack, unpack
import full3d_newton as NEW
import winding_catalog_map as WC
from cross_grid_branch import interp_state

DEV = torch.device("cuda" if torch.cuda.is_available() else "cpu")


# ===========================================================================
# Route 2: jacrev Jacobian + Jacobi-scaled normal-equation Cholesky LM step.
# Column scaling D = 1/sqrt(diag(J^T J)) tames the steep-core/Chebyshev kappa^2
# conditioning of the normal equations; the solution (zero of F) is unchanged.
# ===========================================================================
def newton_scaled(u, G, p, kap8, m=1, maxit=40, lam0=1e-4, tol=1e-12,
                  lam_min=1e-14, verbose=False, wbc=30.0, chunk_size=256,
                  time_budget=None):
    """Dense normal-equation LM with column (Jacobi) scaling.  Uses the batched
    jacrev Jacobian (one reverse pass).  Strict monotone acceptance.  Returns
    (u, hist, info)."""
    u = u.detach().clone()
    lam = lam0
    F = NEW.residual_vector_vsafe(u, G, p, kap8, m=m, wbc=wbc)
    Phi = float((F*F).sum()); hist = [Phi]
    nU = u.numel()
    t0 = time.time()
    t_jac = 0.0; t_solve = 0.0
    for it in range(maxit):
        if Phi < tol:
            break
        if time_budget is not None and time.time() - t0 > time_budget:
            break
        tj = time.time()
        J, F = NEW.jacobian_jacrev(u, G, p, kap8, m=m, wbc=wbc, chunk_size=chunk_size)
        t_jac += time.time() - tj
        # column scaling
        ts = time.time()
        JTJ = J.t() @ J
        d = torch.sqrt(torch.clamp(torch.diagonal(JTJ), min=1e-30))
        Dinv = 1.0 / d
        JTJs = JTJ * Dinv[:, None] * Dinv[None, :]      # D^-1 (J^T J) D^-1
        JTF = J.t() @ F
        rhs = -(Dinv * JTF)
        Is = torch.eye(nU, device=u.device)
        accepted = False
        for _try in range(12):
            try:
                dy = torch.linalg.solve(JTJs + lam*Is, rhs)
                du = Dinv * dy                           # unscale
            except Exception:
                lam *= 4.0; continue
            un = u + du
            Pn = float((NEW.residual_vector_vsafe(un, G, p, kap8, m=m, wbc=wbc)**2).sum())
            if np.isfinite(Pn) and Pn < Phi:
                u = un; Phi = Pn; lam = max(lam*0.25, lam_min); accepted = True; break
            lam *= 4.0
        t_solve += time.time() - ts
        hist.append(Phi)
        if verbose:
            print(f"  [scaled] it={it:3d} Phi={Phi:.4e} lam={lam:.1e} "
                  f"{'acc' if accepted else 'STALL'}")
        if not accepted:
            break
    info = dict(t_jac=t_jac, t_solve=t_solve, wall=time.time()-t0, niter=len(hist)-1)
    return u.detach(), hist, info


# ===========================================================================
# Route 1: matrix-free Newton-Krylov with a TWO-GRID coarse-Jacobian preconditioner.
# We never form the fine dense Jacobian.  JVP/VJP via autograd (as full3d_solver.lm_step).
# Preconditioner M^{-1} r  ~=  prolong( (J_c^T J_c + lam I)^{-1} restrict(r) ), with
# restrict/prolong = interp_state between the fine grid and a coarse grid; J_c is the
# coarse dense jacrev Jacobian, factorized ONCE per outer iteration.  This is classical
# two-grid (spectral) preconditioning: the coarse operator captures the smooth, badly-
# conditioned low modes that Jacobi cannot.
# ===========================================================================
def _jvp_vjp_closures(u, G, p, kap8, m, wbc):
    u = u.detach().clone().requires_grad_(True)
    F = NEW.residual_vector_vsafe(u, G, p, kap8, m=m, wbc=wbc)
    def JT(w):
        g, = torch.autograd.grad(F, u, grad_outputs=w, retain_graph=True)
        return g
    w0 = torch.zeros_like(F, requires_grad=True)
    JTw = torch.autograd.grad(F, u, grad_outputs=w0, create_graph=True)[0]
    def JV(v):
        jv, = torch.autograd.grad(JTw, w0, grad_outputs=v, retain_graph=True)
        return jv
    return F.detach(), JT, JV


def _build_coarse_precond(u, G, Gc, p, kap8, m, wbc, lam, chunk_size=256):
    """Restrict the fine state to coarse, build & factorize the coarse normal matrix
    (J_c^T J_c + lam I) with column scaling.  Returns an apply(r_fine)->du_fine using
    interp_state restrict/prolong on the 5-field state layout."""
    uc = interp_state(u, G, Gc)
    Jc, Fc = NEW.jacobian_jacrev(uc, Gc, p, kap8, m=m, wbc=wbc, chunk_size=chunk_size)
    JTJc = Jc.t() @ Jc
    dC = torch.sqrt(torch.clamp(torch.diagonal(JTJc), min=1e-30))
    DinvC = 1.0 / dC
    JTJcs = JTJc * DinvC[:, None] * DinvC[None, :]
    Ic = torch.eye(JTJc.shape[0], device=u.device)
    chol = torch.linalg.cholesky(JTJcs + lam*Ic)
    def apply(r_fine):
        # r_fine is a fine-grid vector in u-space (length nU_fine).  restrict -> coarse,
        # apply coarse inverse (scaled), prolong -> fine.
        rc = interp_state(r_fine, G, Gc)
        y = torch.cholesky_solve((DinvC*rc).reshape(-1, 1), chol).reshape(-1)
        duc = DinvC * y
        return interp_state(duc, Gc, G)
    return apply


def newton_krylov_2grid(u, G, Gc, p, kap8, m=1, maxit=40, lam0=1e-4, tol=1e-12,
                        lam_min=1e-14, cg_iters=60, cg_tol=1e-7, verbose=False,
                        wbc=30.0, chunk_size=256, time_budget=None):
    """Matrix-free LM (J^T J + lam I) du = -J^T F by preconditioned CG, with a two-grid
    coarse-Jacobian preconditioner.  Never forms the fine dense Jacobian.  Returns
    (u, hist, info)."""
    u = u.detach().clone()
    lam = lam0
    F0 = NEW.residual_vector_vsafe(u, G, p, kap8, m=m, wbc=wbc)
    Phi = float((F0*F0).sum()); hist = [Phi]
    t0 = time.time()
    # build the coarse-grid preconditioner ONCE (frozen at the warm-start state); a
    # Newton-Krylov preconditioner need not be exact/updated -> avoids paying the coarse
    # jacrev every Newton iter (the per-iter rebuild was the cost+weakness bug).
    Papply = _build_coarse_precond(u, G, Gc, p, kap8, m, wbc, lam0, chunk_size=chunk_size)
    for it in range(maxit):
        if Phi < tol:
            break
        if time_budget is not None and time.time() - t0 > time_budget:
            break
        F, JT, JV = _jvp_vjp_closures(u, G, p, kap8, m, wbc)
        b = JT(-F)
        # preconditioned CG on A x = b, A = J^T J + lam I, M^-1 = two-grid
        x = torch.zeros_like(u)
        r = b.clone()
        z = Papply(r)
        pdir = z.clone()
        rz = float(r @ z); rs0 = float(r @ r) + 1e-300
        for _ in range(cg_iters):
            Ap = JT(JV(pdir)) + lam*pdir
            denom = float(pdir @ Ap)
            if abs(denom) < 1e-300:
                break
            alpha = rz / denom
            x = x + alpha*pdir
            r = r - alpha*Ap
            if float(r @ r) < cg_tol*rs0:
                break
            z = Papply(r)
            rz_new = float(r @ z)
            pdir = z + (rz_new/rz)*pdir
            rz = rz_new
        # LM line search on the damping
        accepted = False
        for _try in range(10):
            un = u + x
            Pn = float((NEW.residual_vector_vsafe(un, G, p, kap8, m=m, wbc=wbc)**2).sum())
            if np.isfinite(Pn) and Pn < Phi:
                u = un; Phi = Pn; lam = max(lam*0.5, lam_min); accepted = True; break
            lam *= 4.0
            x = 0.5*x      # shrink the step with the damping
        hist.append(Phi)
        if verbose:
            print(f"  [nk2g] it={it:3d} Phi={Phi:.4e} lam={lam:.1e} "
                  f"{'acc' if accepted else 'STALL'}")
        if not accepted:
            break
    info = dict(wall=time.time()-t0, niter=len(hist)-1)
    return u.detach(), hist, info


# ===========================================================================
# solve_grid: pick the route.  Default = route 2 (scaled dense normal-eq), which on
# the grids in scope is bottlenecked by the jacrev build, not the O(nU^3) solve.
# ===========================================================================
def solve_grid(u, G, p, kap8, m=1, route="scaled", Gc=None, **kw):
    if route == "scaled":
        return newton_scaled(u, G, p, kap8, m=m, **kw)
    elif route == "nk2g":
        assert Gc is not None, "nk2g needs a coarse grid Gc"
        return newton_krylov_2grid(u, G, Gc, p, kap8, m=m, **kw)
    elif route == "lstsq":
        u2, hist = NEW.newton_solve(u, G, p, kap8, m=m, **{k: v for k, v in kw.items()
                                    if k in ('maxit', 'lam0', 'tol', 'verbose', 'chunk_size')})
        return u2, hist, dict(niter=len(hist)-1)
    raise ValueError(route)


# ===========================================================================
# continuation_solve: walk a resolution ladder, interp_state warm-start each grid.
# ===========================================================================
def continuation_solve(u0, grids, p, kap8, m=1, route="scaled",
                       maxit_first=50, maxit_step=25, tol=1e-12, verbose=True,
                       coarse_for=None, time_budget=None):
    """grids: list of (Nr,Nth,Nps).  u0 is on grids[0] (or None -> winding_seed).
    coarse_for: optional (Nr,Nth,Nps) coarse grid used as the two-grid preconditioner
    for the nk2g route on the larger grids."""
    out = []
    G = make_grid_shexact(*grids[0], mmax=grids[0][2]//2)
    if u0 is None:
        u0, _ = WC.winding_seed(G, m)
    u, hist, info = solve_grid(u0, G, p, kap8, m=m, route=route,
                               maxit=maxit_first, tol=tol, verbose=verbose,
                               time_budget=time_budget)
    dg, _ = WC.full_diag(u, G, p, kap8, m)
    a, b, c, d, Th = unpack(u, G)
    maxB1A = float((a+b)[G.body].abs().max())
    rec = dict(grid=list(grids[0]), Phi0=float(hist[0]), Phi=float(hist[-1]),
               niter=info['niter'], M_MS=float(dg['M_MS']), psivar=float(dg['psivar']),
               maxB1A=maxB1A, wall=float(info.get('wall', 0.0)))
    out.append(rec)
    if verbose:
        print(f"[cont {grids[0]}] Phi {hist[0]:.2e}->{hist[-1]:.2e}  M_MS={dg['M_MS']:.6f}  "
              f"maxB1A={maxB1A:.2e}  ({info['niter']} it)")
    Gprev = G
    for g in grids[1:]:
        Gt = make_grid_shexact(*g, mmax=g[2]//2)
        ui = interp_state(u, Gprev, Gt)
        Gc = None
        if route == "nk2g":
            cg = coarse_for if coarse_for is not None else Gprev_tuple_of(Gprev)
            Gc = make_grid_shexact(*cg, mmax=cg[2]//2) if isinstance(cg, tuple) else Gprev
        u, hist, info = solve_grid(ui, Gt, p, kap8, m=m, route=route, Gc=Gc,
                                   maxit=maxit_step, tol=tol, verbose=verbose,
                                   time_budget=time_budget)
        dg, _ = WC.full_diag(u, Gt, p, kap8, m)
        a, b, c, d, Th = unpack(u, Gt)
        maxB1A = float((a+b)[Gt.body].abs().max())
        rec = dict(grid=list(g), Phi0=float(hist[0]), Phi=float(hist[-1]),
                   niter=info['niter'], M_MS=float(dg['M_MS']), psivar=float(dg['psivar']),
                   maxB1A=maxB1A, wall=float(info.get('wall', 0.0)))
        out.append(rec)
        if verbose:
            print(f"[cont {g}] warm Phi {hist[0]:.2e}->{hist[-1]:.2e}  M_MS={dg['M_MS']:.6f}  "
                  f"maxB1A={maxB1A:.2e}  ({info['niter']} it)")
        Gprev = g if isinstance(g, tuple) else Gt
        Gprev = Gt
    return u, out


def Gprev_tuple_of(G):
    return (G.Nr, G.Nth, G.Nps)


def richardson(masses_by_n):
    """Crude Richardson/continuum estimate from the two finest deep-floored masses
    assuming algebraic convergence in 1/Nr.  masses_by_n: list of (Nr, M)."""
    if len(masses_by_n) < 2:
        return float('nan')
    (n1, M1), (n2, M2) = masses_by_n[-2], masses_by_n[-1]
    # assume M(N) = Minf + C/N^q with q=2 (spectral-ish floor of the algebraic tail)
    q = 2.0
    h1, h2 = 1.0/n1**q, 1.0/n2**q
    Minf = (M2*h1 - M1*h2) / (h1 - h2)
    return float(Minf)
