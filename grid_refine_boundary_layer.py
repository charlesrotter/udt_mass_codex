#!/usr/bin/env python3
"""
grid_refine_boundary_layer.py -- FIRM the Branch-P boundary-layer reading at Nr=16/24.

Driver: Claude (Opus 4.8). 2026-06-24. OBSERVE. DATA-BLIND. NEW FILE; reuses the
immutable residual/lm_solve verbatim.  Usage: python3 grid_refine_boundary_layer.py 16

WHY: the Nr=10 X-continuation read the continuation's extra structure as BC
BOUNDARY-LAYERS (phi spikes at core/seal, flat body), NOT an interior body -- but
the layers were ~1 node wide (UNDER-RESOLVED), so AB/M_MS magnitudes were
grid-dependent.  #66 reopener: a finer grid turning the flat body into a peaked
interior core would FLIP the verdict.  The layers are RADIAL (core rc, seal ri),
so refine Nr only (Nth=6,Nps=8 fixed; the Chebyshev grid clusters near both ends).
TEST at Nr: (a) does the body stay FLAT or develop an interior core?  (b) do the
core/seal layers resolve over MORE nodes (real layer) and AB/M_MS converge?

Cold seed cannot floor the stiff X=-2e5, so warm-start a TRIMMED X-continuation up
to -2e5, then dump the FULL radial profile + interior/edge classification.
Bounded: single process, hard per-step + total wall caps.
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

NR = int(sys.argv[1]) if len(sys.argv) > 1 else 16
P = 1.0; BR = "P"
XI, KAP, KAP8, M = B.XI_PROD, B.KAP_PROD, B.KAP8, B.M_WIND
XLADDER = [-3.0, -30.0, -300.0, -3e3, -3e4, -2e5]   # trimmed continuation to -2e5
WALL_STEP = 130.0; WALL_TOT = 1400.0
t0 = time.time(); log = lambda s: print(s, flush=True)

log("=" * 78); log(f"GRID-REFINE BOUNDARY-LAYER  Nr={NR} Nth=6 Nps=8  branch={BR}")
log(f"  ladder: {XLADDER}"); log("=" * 78)
G = _grid(NR)
rfull = G.r.cpu().numpy()
bodymask = G.body.cpu().numpy()
jt, jp = G.Nth // 2, G.Nps // 2
body_r_idx = np.where(bodymask[:, jt, jp])[0]
log(f"r nodes ({NR}): " + " ".join(f"{x:.2f}" for x in rfull))
log(f"body radial idx: {list(body_r_idx)} -> r[{rfull[body_r_idx.min()]:.2f},"
    f"{rfull[body_r_idx.max()]:.2f}]  (rc={G.rc:.2f} ri={G.ri:.2f})")

u = B.make_seed(G, P)
log(f"\n{'X':>10} {'Phi':>10} {'it':>3} {'M_MS':>10} {'AB':>9} {'phi_depth':>10} "
    f"{'body_flat':>9} {'t':>5}")


def bodyflat(dg):
    pr = np.abs(dg['proper_rho'][body_r_idx])
    return float(pr.max() / max(pr.mean(), 1e-30))


for X in XLADDER:
    if time.time() - t0 > WALL_TOT:
        log("  [total wall hit -- stop]"); break
    u, hist, tsec, capped = B.lm_solve(u, G, P, X, XI, KAP, m=M, kap8=KAP8, branch=BR,
                                       maxit=8, lam0=1e-3, wall_cap=WALL_STEP, verbose=False)
    dg = B.diagnose(u, G, X, XI, KAP, m=M, kap8=KAP8, branch=BR)
    depth = max(abs(dg['phi_min']), abs(dg['phi_max']))
    log(f"{X:>10.1e} {hist[-1]:>10.2e} {len(hist)-1:>3d} {dg['M_MS']:>10.4f} "
        f"{dg['AB']:>9.3e} {depth:>10.3e} {bodyflat(dg):>9.2f} {time.time()-t0:>5.0f}")
    torch.save(u.cpu(), f"/tmp/uP_Nr{NR}_X{abs(X):.0e}.pt")

# ---- full-profile dissection at the top X (=-2e5) ----
dg = B.diagnose(u, G, X, XI, KAP, m=M, kap8=KAP8, branch=BR)
pr = dg['proper_rho']; phir = dg['phi_r']
bi = body_r_idx
prb = np.abs(pr[bi])
imax = bi[int(np.argmax(prb))]
frac = np.where(bi == imax)[0][0] / max(len(bi) - 1, 1)
dpr = np.diff(prb)
interior = (0.15 < frac < 0.85) and not np.all(dpr > -1e-30) and not np.all(dpr < 1e-30)
kind = ("INTERIOR CORE (body!)" if interior else
        "OUTER-EDGE/seal pile-up" if frac >= 0.85 else
        "CORE-concentrated" if frac <= 0.15 else "ambiguous")
log("\n" + "=" * 78)
log(f"FULL PROFILE at X={X:.1e}  (Nr={NR})  Phi={hist[-1]:.2e}")
log(f"  proper-energy peak r={rfull[imax]:.2f} (body-frac {frac:.2f})  M_MS={dg['M_MS']:.4e}  "
    f"AB={dg['AB']:.3e}  body_flat(max/mean)={bodyflat(dg):.2f}  => {kind}")
log(f"  proper-rho(r): " + " ".join(
    f"{rfull[i]:.2f}{'*' if bodymask[i,jt,jp] else ' '}:{pr[i]:+.2e}" for i in range(len(rfull))))
log(f"  phi(r):        " + " ".join(f"{rfull[i]:.2f}:{phir[i]:+.2e}" for i in range(len(rfull))))
# seal-layer width: how many nodes from the seal-side phi peak back to ~0 in body
log(f"\n  READ: body_flat~1 + layers at core/seal => boundary-layer (Nr=10 had body_flat~2.5, "
    f"AB~8.3, M_MS~750); compare convergence above.")
log(f"\n=== GRID-REFINE Nr={NR} DONE  total={time.time()-t0:.0f}s ===")
