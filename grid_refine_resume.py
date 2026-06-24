#!/usr/bin/env python3
"""
grid_refine_resume.py -- RESUME flooring the Nr=16 warm field to a REAL floor.

Driver: Claude (Opus 4.8). 2026-06-24. OBSERVE. DATA-BLIND. NEW FILE.
The warm-start Nr=16 run descended 2.9e10 -> 7.8e5 in 6 iters (still converging
~0.75 order/iter) but ran out of the 720s budget. Resume from the saved field
(/tmp/uP_Nr16_X2e5_warm.pt) with a longer wall to reach a real floor, THEN read
body_flat / interior-vs-edge to firm (or flip) the boundary-layer verdict.
Bounded single process; long but finite wall.  Usage: python3 grid_refine_resume.py 16
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
P = 1.0; BR = "P"; Xt = -2e5
XI, KAP, KAP8, M = B.XI_PROD, B.KAP_PROD, B.KAP8, B.M_WIND
t0 = time.time(); log = lambda s: print(s, flush=True)
G = _grid(NR)
rfull = G.r.cpu().numpy(); bodymask = G.body.cpu().numpy()
jt, jp = G.Nth//2, G.Nps//2; body_r_idx = np.where(bodymask[:, jt, jp])[0]
src = f"/tmp/uP_Nr{NR}_X2e5_warm.pt"
u = torch.load(src).to('cuda' if torch.cuda.is_available() else 'cpu')
log("=" * 78); log(f"RESUME FLOOR Nr={NR} X=-2e5  from {src}"); log("=" * 78)


def bodyflat(dg):
    pr = np.abs(dg['proper_rho'][body_r_idx]); return float(pr.max()/max(pr.mean(),1e-30))


F0 = B.residual_vec(u, G, P, Xt, XI, KAP, m=M, kap8=KAP8, branch=BR)
log(f"resume seed Phi={float((F0*F0).sum()):.3e}")
u, hist, tsec, capped = B.lm_solve(u, G, P, Xt, XI, KAP, m=M, kap8=KAP8, branch=BR,
                                   maxit=20, lam0=1e-4, wall_cap=1700.0, verbose=True)
torch.save(u.cpu(), f"/tmp/uP_Nr{NR}_X2e5_floored.pt")
dg = B.diagnose(u, G, Xt, XI, KAP, m=M, kap8=KAP8, branch=BR)
pr = dg['proper_rho']; phir = dg['phi_r']; bi = body_r_idx
prb = np.abs(pr[bi]); imax = bi[int(np.argmax(prb))]
frac = np.where(bi == imax)[0][0]/max(len(bi)-1, 1); dpr = np.diff(prb)
interior = (0.15 < frac < 0.85) and not np.all(dpr > -1e-30) and not np.all(dpr < 1e-30)
kind = ("INTERIOR CORE (body!)" if interior else "OUTER-EDGE/seal pile-up" if frac >= 0.85
        else "CORE-concentrated" if frac <= 0.15 else "ambiguous")
log("\n" + "=" * 78)
log(f"FLOOR Nr={NR}: Phi {hist[0]:.2e}->{hist[-1]:.2e} ({len(hist)-1} it/{tsec:.0f}s capped={capped})")
log(f"  M_MS={dg['M_MS']:.4e}  AB={dg['AB']:.3e}  body_flat={bodyflat(dg):.2f}  "
    f"peak r={rfull[imax]:.2f}(frac {frac:.2f})  phi_depth={max(abs(dg['phi_min']),abs(dg['phi_max'])):.3e}")
log(f"  => {kind}")
log(f"  proper-rho(r): " + " ".join(
    f"{rfull[i]:.2f}{'*' if bodymask[i,jt,jp] else ' '}:{pr[i]:+.2e}" for i in range(len(rfull))))
log(f"  phi(r):        " + " ".join(f"{rfull[i]:.2f}:{phir[i]:+.2e}" for i in range(len(rfull))))
log(f"\n  Nr=10 ref: body_flat~2.5 AB~8.3 M_MS~750 (Phi=0.18); core/seal phi -0.40/+0.44, flat body ~0.01")
log(f"=== RESUME DONE Nr={NR}  total={time.time()-t0:.0f}s ===")
