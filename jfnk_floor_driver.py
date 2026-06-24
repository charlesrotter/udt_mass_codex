#!/usr/bin/env python3
"""
jfnk_floor_driver.py -- LEAN floor driver for the JFNK branch solver.

Driver: Claude (Opus 4.8).  2026-06-23.  OBSERVE mode.  DATA-BLIND.  NEW FILE
(the committed jfnk_branch_solver.py + branchGP_native_s2_coupled_OBSERVE.py
are IMMUTABLE -- imported verbatim, nothing retyped).

PURPOSE: the LIVE next-action -- SWITCH the JFNK solver from pc='none' (which
STALLED near Phi~=4 on Branch G) to pc='jacobi' and tune the inner-tolerance/
Krylov knobs (eta0/eta_min/tol/lsmr_maxit) to BREAK THE STALL and FLOOR the
residual tightly.  This driver SKIPS the slow dense-LM controls in the
committed harness's _run_verification (those are the throughput wall we are
escaping) -- it ONLY runs the matrix-free JFNK floor + diagnose, one branch
per invocation, bounded (Nr<=12), single process.

Usage:  python3 jfnk_floor_driver.py G   (or P)   > <logfile> 2>&1
"""
import os
os.environ.setdefault('PYTORCH_NVML_BASED_CUDA_CHECK', '0')
import sys, time
import torch
torch.set_default_dtype(torch.float64)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import branchGP_native_s2_coupled_OBSERVE as B
from jfnk_branch_solver import jfnk_solve, _grid

BRANCH = sys.argv[1] if len(sys.argv) > 1 else "G"
NR = 10
P = 1.0
X, XI, KAP, KAP8, M = B.X_PROD, B.XI_PROD, B.KAP_PROD, B.KAP8, B.M_WIND

# tuned knobs (METHOD only; no physical DOF touched)
LAM0 = 1e-3 if BRANCH == "G" else 1e-2
WALL = 300.0

print("=" * 72, flush=True)
print(f"JFNK FLOOR  branch={BRANCH}  Nr={NR} Nth=6 Nps=8  pc=jacobi", flush=True)
print(f"X={X:.1e} xi={XI} kap={KAP} kap8={KAP8} m={M} p={P}  "
      f"lam0={LAM0} wall={WALL}s", flush=True)
print("=" * 72, flush=True)

G = _grid(NR)
u0 = B.make_seed(G, P)

t0 = time.time()
u, hist, tsec, capped, info = jfnk_solve(
    u0, G, P, X, XI, KAP, m=M, kap8=KAP8, branch=BRANCH,
    pc='jacobi', maxit=40,
    lam0=LAM0, lsmr_maxit=300,
    eta0=1e-1, eta_min=1e-4, tol=1e-12,
    wall_cap=WALL, verbose=True)

print(f"\n[JFNK:{BRANCH}] FINAL Phi={hist[-1]:.4e}  newton={len(hist)-1}  "
      f"t={tsec:.0f}s  capped={capped}", flush=True)
print(f"  Phi-vs-time: " +
      "  ".join(f"{tt:.0f}s:{hh:.2e}" for tt, hh in zip(info['times'], hist)),
      flush=True)
print(f"  lsmr inner iters per accepted step: {info['lsmr_iters']}", flush=True)

dg = B.diagnose(u, G, X, XI, KAP, m=M, kap8=KAP8, branch=BRANCH)
B.print_diag(f"JFNK-{BRANCH}", dg, hist, tsec, capped, G)
print(f"\n=== JFNK FLOOR branch={BRANCH} DONE  total={time.time()-t0:.0f}s ===",
      flush=True)
