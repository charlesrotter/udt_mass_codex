#!/usr/bin/env python3
"""
jfnk_branch_solver.py -- JACOBIAN-FREE NEWTON-KRYLOV for the UDT native-S^2
6-field coupled residual (branchGP_native_s2_coupled_OBSERVE.residual_vec),
replacing the throughput-limited dense-jacrev LM (~113 s/iter forming a full
~3900x3900 Jacobian).

Driver: Claude (Opus 4.8).  2026-06-23.  INFRA/CODE-BUILD mode.  DATA-BLIND.
NEW FILE (committed scripts are immutable).  NOT committed.

============================================================================
WHAT THIS IS
============================================================================
The branchGP residual is RECTANGULAR: nF (interior body rows + BC anchor
rows) < nU (6 nodal fields).  So the Newton step is a LINEAR LEAST-SQUARES
solve  min_du || J du + F ||  (Gauss-Newton), with LM damping
min_du || J du + F ||^2 + lam ||du||^2.  We solve it MATRIX-FREE:

  J v   (one forward-mode jvp:  torch.func.jvp(residual, (u,), (v,)))
  J^T w (one reverse-mode vjp:  torch.func.vjp(residual, u))

via LSMR on the damped rectangular operator (kappa, not kappa^2 -- the same
matrix-free Krylov used in p5a_prime_repose.lsmr, reused verbatim here).  NO
full Jacobian is ever formed.

VERIFIED jvp/vjp composability (this residual's gtw-EOM uses torch.func.grad,
which nests cleanly under jvp/vjp): jvp matches central finite differences to
1.4e-11, and <Jv,w> == <v,J^T w> to 6e-16.  No autograd-nesting workaround
needed.  (smoke tests: /tmp/smoke_jvp.py, /tmp/smoke_vjp.py.)

============================================================================
KNOBS / CONSTANTS (TAGGED -- no frozen DOF, no silent imports)
============================================================================
  * Residual physics + all FREE constants (X, xi, kap, kap8, m, p, wbc) come
    straight from branchGP_native_s2_coupled_OBSERVE -- VERBATIM, not retyped.
    Only the LINEAR-SOLVER posing changes (matrix-free LSMR vs dense lstsq).
  * lam0, lam grow/shrink factors  : LM globalization (METHOD knob).
  * inexact-Newton forcing (eta)   : inner LSMR tol = eta * (||F||/||F0||)
                                     -- loose early, tight near convergence
                                     (Eisenstat-Walker style; METHOD knob).
  * pc in {'none','jacobi'}        : right preconditioner.  'jacobi' =
                                     1/sqrt(diag(J^T J)) Hutchinson estimate
                                     (the field-block diagonal PC flagged in
                                     the repose machinery).  METHOD knob.
  * lsmr_maxit (Krylov cap), wall_cap (hard wall-clock), maxit (Newton cap).

NO physical DOF is frozen; gtw stays free at both ends (no BC row), exactly as
the residual defines it.  Bounded grids only (Nr<=12) per the anti-hang rule.
"""
import os
os.environ.setdefault('PYTORCH_NVML_BASED_CUDA_CHECK', '0')
os.environ.setdefault('PYTORCH_NO_CUDA_MEMORY_CACHING', '1')
import math
import time
import sys
import numpy as np
import torch
torch.set_default_dtype(torch.float64)
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

from torch.func import jvp, vjp

import branchGP_native_s2_coupled_OBSERVE as B


# ===========================================================================
# Matrix-free linear operators for the residual at a point u.
#   make_ops(u, ...) -> F0 (detached residual), Jv (jvp), JTw (vjp)
# One jvp per Av; one vjp per Atu.  No full Jacobian.
# ===========================================================================
def make_ops(u, G, p, X, xi, kap, m, kap8, branch, wbc):
    # The Krylov layer operates in FLAT 1-D space: u is (6,Nr,Nth,Nps) but the residual
    # is 1-D, so JTw (shaped like u) must be flattened or it collides with F-derived
    # vectors in LSMR.  We reshape u<->flat inside fwd so Jv/JTw are pure 1-D maps.
    ushape = u.shape
    def fwd(uflat):
        return B.residual_vec(uflat.reshape(ushape), G, p, X, xi, kap, m=m, kap8=kap8,
                              branch=branch, wbc=wbc)
    u_flat = u.reshape(-1)
    F0, vjp_fn = vjp(fwd, u_flat)

    def Jv(v):                     # v: 1-D (nU) -> 1-D (nF)
        _, jv = jvp(fwd, (u_flat,), (v,))
        return jv

    def JTw(w):                    # w: 1-D (nF) -> 1-D (nU)
        (g,) = vjp_fn(w)
        return g

    return F0.detach(), Jv, JTw


# ===========================================================================
# LSMR on the damped rectangular operator [J ; damp*I] x = [-F ; 0], with an
# optional RIGHT preconditioner (x = P y).  Verbatim algebra from
# p5a_prime_repose.lsmr (the repo's matrix-free Krylov), generalized to the
# 6-field residual.  Returns (du, n_iters).
# ===========================================================================
def lsmr(Jv, JTw, F, nU, damp, Papply=None, maxit=400, tol=1e-10):
    dev = F.device
    if Papply is None:
        Papply = lambda x: x

    def Av(y):
        return Jv(Papply(y))          # J P y

    def Atu(w):
        return Papply(JTw(w))         # P^T J^T w

    b = -F
    beta = float((b * b).sum()) ** 0.5
    if beta == 0:
        return torch.zeros(nU, device=dev), 0
    uu = b / beta
    v = Atu(uu)
    alpha = float((v * v).sum()) ** 0.5
    if alpha == 0:
        return torch.zeros(nU, device=dev), 0
    v = v / alpha
    h = v.clone()
    hbar = torch.zeros(nU, device=dev)
    y = torch.zeros(nU, device=dev)
    zetabar = alpha * beta
    alphabar = alpha
    rho = 1.0
    rhobar = 1.0
    cbar = 1.0
    sbar = 0.0
    normb = beta
    it = 0
    for it in range(1, maxit + 1):
        u2 = Av(v) - alpha * uu
        beta = float((u2 * u2).sum()) ** 0.5
        uu = u2 / beta
        v2 = Atu(uu) - beta * v
        alpha = float((v2 * v2).sum()) ** 0.5
        v = v2 / alpha
        alphahat = math.hypot(alphabar, damp)
        chat = alphabar / alphahat
        rhoold = rho
        rho = math.hypot(alphahat, beta)
        c = alphahat / rho
        s = beta / rho
        thetanew = s * alpha
        alphabar = c * alpha
        rhobarold = rhobar
        thetabar = sbar * rho
        rhobar = math.hypot(cbar * rho, thetanew)
        cbar = cbar * rho / rhobar
        sbar = thetanew / rhobar
        zeta = cbar * zetabar
        zetabar = -sbar * zetabar
        hbar = h - (thetabar * rho / (rhoold * rhobarold)) * hbar
        y = y + (zeta / (rho * rhobar)) * hbar
        h = v - (thetanew / rho) * h
        if abs(zetabar) < tol * normb:
            break
    return Papply(y), it


# ===========================================================================
# Jacobi right-PC: 1/sqrt(diag(J^T J)), Hutchinson-estimated.  (field-block
# diagonal PC the repose machinery flagged.)  nprobe random probes.
# ===========================================================================
def jacobi_pc(Jv, JTw, nU, dev, nprobe=6):
    diag = torch.zeros(nU, device=dev)
    for _ in range(nprobe):
        z = torch.randn(nU, device=dev)
        diag = diag + z * JTw(Jv(z))
    diag = diag / nprobe
    return 1.0 / torch.sqrt(torch.clamp(diag.abs(), min=1e-10))


# ===========================================================================
# THE JFNK SOLVE.  Outer Newton; each step = matrix-free damped-LSMR Gauss-
# Newton step with LM globalization + inexact-Newton (Eisenstat-Walker)
# inner-tolerance.  Hard wall-clock cap.  Prints per-iter so partials show.
# ===========================================================================
def jfnk_solve(u0, G, p, X, xi, kap, m=1, kap8=1.0, branch="G", wbc=30.0,
               maxit=40, lam0=1e-3, lam_min=1e-13, lam_max=1e8,
               pc='none', lsmr_maxit=200, eta0=1e-1, eta_min=1e-3,
               tol=1e-12, wall_cap=180.0, verbose=True):
    """JFNK for branchGP residual_vec.  Returns (u, hist, t_sec, capped, info)."""
    t0 = time.time()
    u = u0.detach().clone()
    fwd = lambda uu: B.residual_vec(uu, G, p, X, xi, kap, m=m, kap8=kap8,
                                    branch=branch, wbc=wbc)
    F = fwd(u)
    Phi = float((F * F).sum())
    Phi0 = Phi
    hist = [Phi]
    lsmr_iters = []
    times = [0.0]
    nU = u.numel()
    lam = lam0
    capped = False
    if verbose:
        print(f"  [JFNK:{branch}] start Phi={Phi:.4e} nU={nU} nF={F.numel()} "
              f"pc={pc}", flush=True)
    for it in range(maxit):
        if Phi < tol:
            break
        if time.time() - t0 > wall_cap:
            capped = True
            break
        F0, Jv, JTw = make_ops(u, G, p, X, xi, kap, m, kap8, branch, wbc)
        # inexact-Newton forcing: tighter inner tol as residual drops
        ratio = math.sqrt(max(Phi, 1e-300) / max(Phi0, 1e-300))
        eta = min(eta0, max(eta_min, eta0 * ratio))
        if pc == 'jacobi':
            s = jacobi_pc(Jv, JTw, nU, u.device)
            Papply = (lambda x, s=s: s * x)
        else:
            Papply = None
        accepted = False
        for _try in range(12):
            if time.time() - t0 > wall_cap:
                capped = True
                break
            damp = math.sqrt(lam)
            du, nit = lsmr(Jv, JTw, F0, nU, damp, Papply=Papply,
                           maxit=lsmr_maxit, tol=eta)
            un = u + du.reshape(u.shape)            # du is flat (nU) -> back to (6,Nr,Nth,Nps)
            Pn = float((fwd(un) ** 2).sum())
            if np.isfinite(Pn) and Pn < Phi:
                u = un
                Phi = Pn
                lam = max(lam * 0.3, lam_min)
                accepted = True
                lsmr_iters.append(nit)
                break
            lam = min(lam * 4.0, lam_max)
        hist.append(Phi)
        times.append(time.time() - t0)
        if verbose:
            print(f"  [JFNK:{branch}] it={it:2d} Phi={Phi:.4e} lam={lam:.1e} "
                  f"eta={eta:.1e} lsmr={lsmr_iters[-1] if lsmr_iters else '-'} "
                  f"t={time.time()-t0:.0f}s {'acc' if accepted else 'STALL'}",
                  flush=True)
        if not accepted:
            break
        if capped:
            break
        if time.time() - t0 > wall_cap:
            capped = True
            break
    info = dict(lsmr_iters=lsmr_iters, times=times, Phi0=Phi0)
    return u.detach(), hist, time.time() - t0, capped, info


# ===========================================================================
# CHEAP, BOUNDED, INLINE VERIFICATION.  Single process, sequential, hard caps.
# (a) Branch-G correctness vs a short dense-LM; (b) Phi-vs-time speed; (c) the
# stiff Branch P bounded floor.  Prints exact numbers.
# ===========================================================================
def _grid(NR):
    from full3d_spectral import Grid3D, attach_coord_weight
    return attach_coord_weight(Grid3D(Nr=NR, Nth=6, Nps=8, rc=0.1, cell=8.0))


def _run_verification():
    X, XI, KAP, KAP8, M = B.X_PROD, B.XI_PROD, B.KAP_PROD, B.KAP8, B.M_WIND
    P = 1.0
    NR = 10
    WALL = 180.0
    print("=" * 72)
    print(f"JFNK VERIFICATION  Nr={NR} Nth=6 Nps=8  X={X:.1e} xi={XI} kap={KAP} "
          f"kap8={KAP8} m={M} p={P}")
    print("=" * 72)
    G = _grid(NR)
    u0 = B.make_seed(G, P)

    # ---------- (a)+(b) Branch G : JFNK vs dense-LM, same wall budget ----------
    print("\n--- BRANCH G ---")
    print("[dense-LM control] (the throughput-limited reference)")
    t = time.time()
    uL, histL, tL, capL = B.lm_solve(u0, G, P, X, XI, KAP, m=M, kap8=KAP8,
                                     branch="G", maxit=8, lam0=1e-3,
                                     wall_cap=WALL, verbose=True)
    print(f"  dense-LM: Phi={histL[-1]:.4e} iters={len(histL)-1} t={tL:.0f}s "
          f"capped={capL}", flush=True)

    print("\n[JFNK] Branch G (pc=jacobi)")
    uJ, histJ, tJ, capJ, infoJ = jfnk_solve(u0, G, P, X, XI, KAP, m=M, kap8=KAP8,
                                            branch="G", pc='jacobi', maxit=30,
                                            lam0=1e-3, lsmr_maxit=200,
                                            wall_cap=WALL, verbose=True)
    print(f"  JFNK[G]: Phi={histJ[-1]:.4e} newton={len(histJ)-1} t={tJ:.0f}s "
          f"capped={capJ}", flush=True)

    # field / M_MS agreement (CORRECTNESS)
    dgL = B.diagnose(uL, G, X, XI, KAP, m=M, kap8=KAP8, branch="G")
    dgJ = B.diagnose(uJ, G, X, XI, KAP, m=M, kap8=KAP8, branch="G")
    fld = (uJ - uL).abs().max().item()
    print(f"\n  CORRECTNESS(G): max|u_JFNK - u_LM| = {fld:.3e}")
    print(f"    M_MS  dense-LM={dgL['M_MS']:.6e}  JFNK={dgJ['M_MS']:.6e}")
    print(f"    phi_min dense-LM={dgL['phi_min']:.4e}  JFNK={dgJ['phi_min']:.4e}")
    print(f"  SPEED(G): dense-LM floored {histL[-1]:.3e} in {tL:.0f}s; "
          f"JFNK floored {histJ[-1]:.3e} in {tJ:.0f}s")
    print(f"    JFNK Phi-vs-time: " +
          " ".join(f"{tt:.0f}s:{hh:.2e}" for tt, hh in
                   zip(infoJ['times'], histJ)))

    # ---------- (c) Branch P : the stiff case ----------
    print("\n--- BRANCH P (STIFF) ---")
    print("[dense-LM control]")
    t = time.time()
    uLP, histLP, tLP, capLP = B.lm_solve(u0, G, P, X, XI, KAP, m=M, kap8=KAP8,
                                         branch="P", maxit=6, lam0=1e-3,
                                         wall_cap=WALL, verbose=True)
    print(f"  dense-LM[P]: Phi={histLP[-1]:.4e} iters={len(histLP)-1} "
          f"t={tLP:.0f}s capped={capLP}", flush=True)

    print("\n[JFNK] Branch P (pc=jacobi, LM-damped)")
    uJP, histJP, tJP, capJP, infoJP = jfnk_solve(u0, G, P, X, XI, KAP, m=M,
                                                 kap8=KAP8, branch="P",
                                                 pc='jacobi', maxit=30,
                                                 lam0=1e-2, lsmr_maxit=200,
                                                 wall_cap=WALL, verbose=True)
    print(f"  JFNK[P]: Phi={histJP[-1]:.4e} newton={len(histJP)-1} t={tJP:.0f}s "
          f"capped={capJP}", flush=True)
    print(f"  SPEED(P): dense-LM floored {histLP[-1]:.3e} in {tLP:.0f}s; "
          f"JFNK floored {histJP[-1]:.3e} in {tJP:.0f}s")
    print(f"    JFNK[P] Phi-vs-time: " +
          " ".join(f"{tt:.0f}s:{hh:.2e}" for tt, hh in
                   zip(infoJP['times'], histJP)))
    print("\n=== JFNK VERIFICATION DONE ===")


if __name__ == "__main__":
    _run_verification()
