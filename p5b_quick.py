#!/usr/bin/env python3
"""p5b_quick.py -- lean PC comparison: none vs diag vs rband on the anchor round seed,
moderate LSMR cap, per-Newton-step inner-iter + Phi readout.  Confirms the PC cuts
Krylov iters before the full gate.  Driver Claude Opus 4.8 2026-06-20. DATA-BLIND."""
import os, sys, time
os.environ.setdefault("PYTORCH_NVML_BASED_CUDA_CHECK", "0")
import numpy as np, torch
torch.set_default_dtype(torch.float64)
from full3d_spectral import Grid3D, attach_coord_weight
from full3d_solver import residual_vector, round_seed
import p5a_prime_repose as RP
import p5b_pc as PC

P, KAP8 = 0.4, 0.05
NR = int(sys.argv[1]) if len(sys.argv) > 1 else 12
NTH = int(sys.argv[2]) if len(sys.argv) > 2 else 6
NPS = int(sys.argv[3]) if len(sys.argv) > 3 else 8
LCAP = int(sys.argv[4]) if len(sys.argv) > 4 else 1500
pcs = sys.argv[5].split(',') if len(sys.argv) > 5 else ['none', 'rband']

G = Grid3D(NR, NTH, NPS, rc=0.05, cell=14.0); G = attach_coord_weight(G)
u0, sol = round_seed(G, p=P, kap8=KAP8)
rp = RP.Repose(G, p=P, m=1, edge_mode='hold', fit_deg=4); rp.set_edge_hold(u0)
ub0 = rp.extract(u0)
print(f"grid ({NR},{NTH},{NPS}) nB={rp.nB} LCAP={LCAP} pcs={pcs}", flush=True)
for pc in pcs:
    t = time.time()
    ub, hist, its, wt = PC.jfnk_solve(ub0, rp, u0, KAP8, pc=pc, maxit=40, tol=1e-13,
                                      lsmr_maxit=LCAP, lsmr_tol=1e-13, verbose=True)
    print(f">>> pc={pc}: final-Phi={hist[-1]:.3e} newton={len(hist)-1} "
          f"lsmr-avg={np.mean(its) if its else 0:.0f} lsmr-tot={int(np.sum(its))} wall={wt:.0f}s",
          flush=True)
print("DONE", flush=True)
