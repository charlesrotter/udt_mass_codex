#!/usr/bin/env python3
"""P5a GATE 2: BEAT THE #60 STALL.  NEW FILE, branch p5a-jfnk-precond.
The #60 case: an axisymmetric l=2 perturbation of the round soliton (a KNOWN
relax-to-round control) that, under matrix-free Jacobi-PCG LM, reaches Phi~4e-5 and
STALLS (mass-weighted shape tvar stuck ~0.086, spurious psivar~0.059).
PASS = JFNK + physics PC drives Phi to floor (<=~1e-9, and the shape relaxes toward
round: tvar collapsing) where Jacobi stalled.

We run BOTH PCs on the SAME seed/grid (apples-to-apples): 'jacobi' (the #60 control)
and 'radial' (the physics PC).  Report iterations, residual history, tvar/psivar, and
wall-time vs the dense-Newton anchor on the same case.
"""
import os, sys
os.environ.setdefault("PYTORCH_NVML_BASED_CUDA_CHECK", "0")
import time, numpy as np, torch
torch.set_default_dtype(torch.float64)
from full3d_spectral import Grid3D, attach_coord_weight, residuals, diagnostics
from full3d_solver import round_seed, residual_vector, unpack
import full3d_newton as NW
import p5a_jfnk_precond as P5

# grid: use the documented stall regime.  Default to a moderate grid the anchor can
# also run for cross-check; allow override.
Nr = int(sys.argv[1]) if len(sys.argv) > 1 else 24
Nth = int(sys.argv[2]) if len(sys.argv) > 2 else 6
Nps = int(sys.argv[3]) if len(sys.argv) > 3 else 6
G = Grid3D(Nr, Nth, Nps, rc=0.05, cell=14.0); G = attach_coord_weight(G)
u0, sol = round_seed(G, p=0.4, kap8=0.05)
useed = P5.axi_l2_seed(G, u0, amp=0.25)


def diag(u):
    a, b, c, d, Th = unpack(u, G)
    out = residuals(G, (a, b, c, d, Th), 0.4, 0.05)
    dg = diagnostics(G, out, 0.05)
    F = residual_vector(u, G, 0.4, 0.05)
    return float((F * F).sum()), dg['tvar'], dg['psivar'], dg['M_MS']


Phi_s, tv_s, pv_s, M_s = diag(useed)
print(f"GRID {Nr}x{Nth}x{Nps}  axi_l2 SEED: Phi={Phi_s:.3e} tvar={tv_s:.3e} "
      f"psivar={pv_s:.3e} M_MS={M_s:.5f}  nU={useed.numel()}")

# --- the #60 control: Jacobi PC ---
t = time.time()
uj, hj, cgj, dtj = P5.jfnk_solve(useed, G, 0.4, 0.05, maxit=40, lam0=1e-2, tol=1e-10,
                                 variant='jacobi', cg_maxit=120, cg_tol=1e-6, verbose=True)
Phi_j, tv_j, pv_j, M_j = diag(uj)
print(f"JACOBI(#60 control): Phi={Phi_j:.3e} tvar={tv_j:.3e} psivar={pv_j:.3e} "
      f"M_MS={M_j:.5f} iters={len(hj)-1} time={dtj:.0f}s")
print("  Phi hist:", " ".join(f"{x:.2e}" for x in hj))

# --- the physics PC ---
t = time.time()
ur, hr, cgr, dtr = P5.jfnk_solve(useed, G, 0.4, 0.05, maxit=40, lam0=1e-2, tol=1e-10,
                                 variant='radial', cg_maxit=300, cg_tol=1e-7, verbose=True)
Phi_r, tv_r, pv_r, M_r = diag(ur)
print(f"RADIAL(physics PC): Phi={Phi_r:.3e} tvar={tv_r:.3e} psivar={pv_r:.3e} "
      f"M_MS={M_r:.5f} iters={len(hr)-1} cg_avg={np.mean(cgr) if cgr else 0:.0f} time={dtr:.0f}s")
print("  Phi hist:", " ".join(f"{x:.2e}" for x in hr))

# --- anchor on the same case (cross-check, if grid small enough) ---
if Nr * Nth * Nps <= 16 * 6 * 8 * 1.6:
    t = time.time()
    uA, hA = NW.newton_solve(useed, G, 0.4, 0.05, maxit=25, tol=1e-12)
    Phi_A, tv_A, pv_A, M_A = diag(uA)
    print(f"ANCHOR(dense): Phi={Phi_A:.3e} tvar={tv_A:.3e} psivar={pv_A:.3e} "
          f"M_MS={M_A:.5f} iters={len(hA)-1} time={time.time()-t:.0f}s")
    fA = unpack(uA, G); fR = unpack(ur, G)
    d = [float((fR[i] - fA[i]).abs().max()) for i in range(5)]
    print("  RADIAL vs ANCHOR field max|diff|:", " ".join(f"{x:.2e}" for x in d))
