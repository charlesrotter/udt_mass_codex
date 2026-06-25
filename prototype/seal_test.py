#!/usr/bin/env python3
"""
seal_test.py -- SEAL/BOX-INDEPENDENCE test of the Branch-P continuation body.

Driver: Claude (Opus 4.8). 2026-06-24. OBSERVE. DATA-BLIND. NEW FILE; reuses the
immutable residual/lm_solve verbatim.

The Nr=16-floored continuation branch has a BIMODAL body (proper-rho peaks at
r~2.1 & r~6.1, dip ~3.7) that SHARPENS with resolution -- but the outer peak sits
a few nodes inside the seal buffer, so it could be seal/box-pinned.  DECISIVE TEST:
move the seal (vary `cell`) and ask whether the peaks stay at FIXED PHYSICAL RADII
(=> real intrinsic structure) or SCALE with the seal position (=> box-controlled
artifact -- the project's central box-control criterion).

Runs the trimmed X-continuation to -2e5 at Nr=10 for several cell sizes; reports
the two proper-rho peak radii (absolute) and as a fraction of ri (the seal radius).
ABS-fixed => intrinsic; ri-fraction-fixed (abs moves with cell) => box-controlled.
Bounded: single process, hard caps.
"""
import os
os.environ.setdefault('PYTORCH_NVML_BASED_CUDA_CHECK', '0')
import sys, time
import numpy as np
import torch
torch.set_default_dtype(torch.float64)
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import branchGP_native_s2_coupled_OBSERVE as B
from full3d_spectral import Grid3D, attach_coord_weight

P = 1.0; BR = "P"; NR = 10
XI, KAP, KAP8, M = B.XI_PROD, B.KAP_PROD, B.KAP8, B.M_WIND
XLADDER = [-3.0, -30.0, -300.0, -3e3, -3e4, -2e5]
t0 = time.time(); log = lambda s: print(s, flush=True)
log("=" * 78); log(f"SEAL/BOX-INDEPENDENCE TEST  Nr={NR}  branch={BR}  (vary cell)"); log("=" * 78)


def peaks_of(dg, G, bidx):
    """find local maxima of |proper_rho| over body radial nodes; return (r, val) list."""
    pr = np.abs(dg['proper_rho']); r = dg['r']
    out = []
    for k in bidx:
        nb = [j for j in (k-1, k+1) if j in bidx]
        if all(pr[k] >= pr[j] for j in nb) and len(nb) > 0:
            out.append((float(r[k]), float(pr[k])))
    out.sort(key=lambda t: -t[1])
    return out[:3]


summary = []
for CELL in [6.0, 8.0, 12.0, 16.0]:
    if time.time() - t0 > 1500:
        log("  [wall hit -- stop]"); break
    G = attach_coord_weight(Grid3D(Nr=NR, Nth=6, Nps=8, rc=0.1, cell=CELL))
    bodymask = G.body.cpu().numpy(); jt, jp = G.Nth//2, G.Nps//2
    bidx = np.where(bodymask[:, jt, jp])[0]
    rfull = G.r.cpu().numpy()
    u = B.make_seed(G, P)
    for X in XLADDER:
        u, hist, ts, cap = B.lm_solve(u, G, P, X, XI, KAP, m=M, kap8=KAP8, branch=BR,
                                      maxit=7, lam0=1e-3, wall_cap=70.0, verbose=False)
    dg = B.diagnose(u, G, X, XI, KAP, m=M, kap8=KAP8, branch=BR)
    pk = peaks_of(dg, G, bidx)
    ri = float(G.ri)
    log(f"\n--- cell={CELL:.1f}  ri(seal)={ri:.2f}  Phi={hist[-1]:.2e}  M_MS={dg['M_MS']:.3e}  "
        f"AB={dg['AB']:.3e} ---")
    log(f"  r nodes: " + " ".join(f"{x:.2f}" for x in rfull))
    log(f"  proper-rho(r): " + " ".join(
        f"{rfull[i]:.2f}{'*' if bodymask[i,jt,jp] else ' '}:{dg['proper_rho'][i]:+.2e}"
        for i in range(len(rfull))))
    log(f"  body proper-rho peaks (r, val):  " +
        "  ".join(f"r={r:.2f}(={r/ri:.2f}ri):{v:.2e}" for r, v in pk))
    summary.append((CELL, ri, pk))

log("\n" + "=" * 78); log("VERDICT: do peak RADII stay fixed (intrinsic) or scale with the seal (box)?")
log(f"{'cell':>6} {'ri':>6} {'peak1_r':>8} {'peak1/ri':>9} {'peak2_r':>8} {'peak2/ri':>9}")
for (CELL, ri, pk) in summary:
    p1 = pk[0] if len(pk) > 0 else (float('nan'), 0)
    p2 = pk[1] if len(pk) > 1 else (float('nan'), 0)
    log(f"{CELL:>6.1f} {ri:>6.2f} {p1[0]:>8.2f} {p1[0]/ri:>9.2f} {p2[0]:>8.2f} {p2[0]/ri:>9.2f}")
log("\n  ABS peak_r ~constant across cells => INTRINSIC structure (fixed physical radius).")
log("  peak_r/ri ~constant (abs moves with cell) => BOX-CONTROLLED (seal-pinned) => artifact.")
log(f"\n=== SEAL TEST DONE  total={time.time()-t0:.0f}s ===")
