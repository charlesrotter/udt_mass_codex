#!/usr/bin/env python3
"""
p5b_anchor.py -- ANCHOR VALIDATION (dense full-space Newton) for P5b, run in a
SEPARATE process (it forces the no-cache allocator that the JFNK path avoids).

Driver: Claude (Opus 4.8, 1M).  2026-06-20.  OBSERVE/INFRA.  DATA-BLIND.  Branch p5b-pc-floor.

Reproduces the dense-Newton ANCHOR (full3d_newton.newton_solve, full-space) on a shared
case and prints its committed-Phi + diagnostics, so the JFNK floored solution (saved by
p5b_gate12 / loosethread) can be compared against the correctness reference.  Also floors
the full-space anchor at a refined Nr (resolution-robustness of the anchor itself).
"""
import os, sys
os.environ.setdefault("PYTORCH_NVML_BASED_CUDA_CHECK", "0")
os.environ.setdefault("PYTORCH_NO_CUDA_MEMORY_CACHING", "1")
import numpy as np, torch
torch.set_default_dtype(torch.float64)
from full3d_spectral import Grid3D, attach_coord_weight, residuals, diagnostics
from full3d_solver import residual_vector, round_seed, unpack
import full3d_newton as NW

P, KAP8 = 0.4, 0.05


def anchor(NR, NTH, NPS):
    G = Grid3D(NR, NTH, NPS, rc=0.05, cell=14.0); G = attach_coord_weight(G)
    u0, sol = round_seed(G, p=P, kap8=KAP8)
    ua, ha = NW.newton_solve(u0, G, P, KAP8, maxit=40, lam0=1e-4, tol=1e-12,
                             verbose=False)
    F = residual_vector(ua, G, P, KAP8); Phi = float((F*F).sum())
    out = residuals(G, unpack(ua, G), P, KAP8); d = diagnostics(G, out, KAP8)
    print(f"  ANCHOR ({NR},{NTH},{NPS}): committed-Phi={Phi:.3e} iters={len(ha)-1} "
          f"M_MS={d['M_MS']:.6f} tvar={d['tvar']:.4e}", flush=True)
    return ua, d


if __name__ == "__main__":
    cases = sys.argv[1] if len(sys.argv) > 1 else "12,6,8"
    print(f"=== P5b ANCHOR VALIDATION (dense full-space Newton) ===", flush=True)
    for cs in cases.split(';'):
        NR, NTH, NPS = [int(x) for x in cs.split(',')]
        anchor(NR, NTH, NPS)
    print("=== ANCHOR DONE ===", flush=True)
