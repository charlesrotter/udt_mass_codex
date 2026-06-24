#!/usr/bin/env python3
"""
x_continuation.py -- CONTINUATION IN X for the Branch-P native-S^2 coupled solve.

Driver: Claude (Opus 4.8). 2026-06-24. OBSERVE mode. DATA-BLIND. NEW FILE;
reuses the IMMUTABLE branchGP residual + lm_solve verbatim.

WHY (the 2026-06-23 ponder + infrastructure audit, Charles: "continuation in X"):
  X (phi-kinetic/curvature coeff) = -2e5 is a CHOSEN placeholder (FREE within a
  Cassini-bounded half-line; nothing internal fixes the value).  At |X|=2e5:
   (a) phi is throttled ~flat (response ∝ 1/|X|) -> the "scale-free / no-
       localization" verdict may be an ARTIFACT of the huge chosen X; and
   (b) the 7-decade spread X~2e5 vs xi,kap~2e-2 makes the phi-equation
       singularly stiff -> the solver cannot floor it cold.
  ONE root cause for both.  Continuation fixes both at once: floor at MODEST |X|
  (non-stiff, phi has structure), warm-start UP a geometric ladder to -2e5,
  staying on the solution manifold (each step well-conditioned), and OBSERVE at
  every X whether a localized body / selected scale exists and how it scales
  with |X| -- does localization at modest |X| SURVIVE to -2e5 or wash out (1/|X|)?

OBSERVE, not target: both outcomes meaningful.  Bounded: Nr=10, single process,
warm-started lm_solve per step, hard wall-caps.
"""
import os
os.environ.setdefault('PYTORCH_NVML_BASED_CUDA_CHECK', '0')
import sys, time
import numpy as np
import torch
torch.set_default_dtype(torch.float64)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import branchGP_native_s2_coupled_OBSERVE as B
from jfnk_branch_solver import _grid

NR = 10; P = 1.0; BR = "P"
XI, KAP, KAP8, M = B.XI_PROD, B.KAP_PROD, B.KAP8, B.M_WIND
t0 = time.time(); log = lambda s: print(s, flush=True)

# geometric X ladder: non-stiff modest |X| -> the chosen -2e5
XLADDER = [-3.0, -10.0, -30.0, -100.0, -300.0, -1e3, -3e3, -1e4, -3e4, -1e5, -2e5]
WALL_STEP = 60.0; WALL_TOT = 820.0

log("=" * 78)
log(f"X-CONTINUATION  branch={BR}  Nr={NR}  xi={XI} kap={KAP} kap8={KAP8}")
log(f"  ladder: {XLADDER}")
log("=" * 78)

G = _grid(NR)
u = B.make_seed(G, P)
bidx = np.arange(3, G.Nr - 3)


def localization(dg):
    """proper-rho concentration: interior peak / body-mean (>1 with a true body)."""
    pr = np.abs(dg['proper_rho'][bidx])
    return float(pr.max() / max(pr.mean(), 1e-30)), dg['r_peak']


log(f"\n{'X':>10} {'Phi':>10} {'it':>3} {'M_MS':>9} {'phi_min':>10} {'phi_max':>10} "
    f"{'AB(B=1/A)':>10} {'tw':>9} {'conc':>6} {'r_peak':>7} {'t':>5}")
results = []
for k, X in enumerate(XLADDER):
    if time.time() - t0 > WALL_TOT:
        log("  [wall budget hit -- stopping ladder]"); break
    # warm-started floor at this X (cold seed only at the first, easiest rung)
    u, hist, tsec, capped = B.lm_solve(u, G, P, X, XI, KAP, m=M, kap8=KAP8,
                                       branch=BR, maxit=7, lam0=1e-3,
                                       wall_cap=WALL_STEP, verbose=False)
    dg = B.diagnose(u, G, X, XI, KAP, m=M, kap8=KAP8, branch=BR)
    conc, rpk = localization(dg)
    log(f"{X:>10.1e} {hist[-1]:>10.2e} {len(hist)-1:>3d} {dg['M_MS']:>9.4f} "
        f"{dg['phi_min']:>+10.3e} {dg['phi_max']:>+10.3e} {dg['AB']:>10.3e} "
        f"{dg['tw_amp']:>9.2e} {conc:>6.2f} {rpk:>7.2f} {time.time()-t0:>5.0f}")
    results.append((X, hist[-1], dg['M_MS'], dg['phi_min'], dg['phi_max'],
                    dg['AB'], dg['tw_amp'], conc, rpk))
    torch.save(u.cpu(), f"/tmp/uP_X{abs(X):.0e}.pt")

# ---- summary: does localization survive as |X| grows? ----
log("\n" + "=" * 78)
log("SUMMARY -- localization vs |X|  (conc>1.3 + interior r_peak => a BODY; "
    "conc~1 + flat => scale-free DEFECT)")
log(f"{'|X|':>10} {'Phi':>10} {'phi_depth':>11} {'AB':>10} {'conc':>6} {'r_peak':>7}")
for (X, Phi, MMS, pmin, pmax, AB, tw, conc, rpk) in results:
    depth = max(abs(pmin), abs(pmax))
    log(f"{abs(X):>10.1e} {Phi:>10.2e} {depth:>11.3e} {AB:>10.3e} {conc:>6.2f} {rpk:>7.2f}")
# trend readout
if len(results) >= 2:
    depths = [max(abs(r[3]), abs(r[4])) for r in results]
    concs = [r[7] for r in results]
    log(f"\n  phi-depth: {depths[0]:.2e} (|X|={abs(results[0][0]):.0e}) -> "
        f"{depths[-1]:.2e} (|X|={abs(results[-1][0]):.0e})")
    log(f"  concentration: {concs[0]:.2f} -> {concs[-1]:.2f}  "
        f"({'localizes' if max(concs)>1.3 else 'stays flat=defect'} across the ladder)")
log(f"\n=== X-CONTINUATION DONE  total={time.time()-t0:.0f}s ===")
