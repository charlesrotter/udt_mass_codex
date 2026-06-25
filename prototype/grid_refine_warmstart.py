#!/usr/bin/env python3
"""
grid_refine_warmstart.py -- FIRM the boundary-layer reading at finer Nr by
WARM-STARTING from the converged Nr=10 solution interpolated to the fine grid.

Driver: Claude (Opus 4.8). 2026-06-24. OBSERVE. DATA-BLIND. NEW FILE; reuses the
immutable residual/lm_solve verbatim.  Usage: python3 grid_refine_warmstart.py 16

WHY: cold X-continuation at Nr=16 DIVERGED (1 dense-jacrev iter/step eats the wall;
throughput wall).  Instead, interpolate the Nr=10 tightly-floored X=-2e5 solution
(/tmp/uP_X2e5_tight.pt, the boundary-layer state, Phi=0.18) onto the Nr=16 grid and
floor at -2e5 from THAT good seed -> a few iters should floor where cold cannot.
TEST: at the finer grid, does the body stay FLAT (boundary-layer reading holds) or
develop a peaked INTERIOR core (#66 reopener => verdict flips)?  Do the core/seal
layers resolve over more nodes + AB/M_MS converge?

Bounded: single process, hard wall-cap.
"""
import os
os.environ.setdefault('PYTORCH_NVML_BASED_CUDA_CHECK', '0')
import sys, time
import numpy as np
import torch
torch.set_default_dtype(torch.float64)
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import branchGP_native_s2_coupled_OBSERVE as B
from jfnk_branch_solver import _grid

NR = int(sys.argv[1]) if len(sys.argv) > 1 else 16
P = 1.0; BR = "P"; Xt = -2e5
XI, KAP, KAP8, M = B.XI_PROD, B.KAP_PROD, B.KAP8, B.M_WIND
t0 = time.time(); log = lambda s: print(s, flush=True)

G10 = _grid(10); G = _grid(NR)
r10 = G10.r; rN = G.r
log("=" * 78); log(f"GRID-REFINE WARM-START  Nr=10 -> Nr={NR}  X={Xt:.1e}  branch={BR}"); log("=" * 78)

src = "/tmp/uP_X2e5_tight.pt"
if not os.path.exists(src):
    log(f"FATAL: missing {src} (the Nr=10 tight -2e5 boundary-layer solution)"); sys.exit(1)
u10 = torch.load(src).to('cuda' if torch.cuda.is_available() else 'cpu')   # (6,10,Nth,Nps)


def interp_r(u_src, r_src, r_dst):
    """linear interp each field along r from r_src grid to r_dst grid (per th,ps col)."""
    nf, _, nth, nps = u_src.shape
    idx = torch.searchsorted(r_src.contiguous(), r_dst.clamp(float(r_src.min()),
                             float(r_src.max())).contiguous()).clamp(1, len(r_src) - 1)
    r0 = r_src[idx - 1]; r1 = r_src[idx]; w = ((r_dst.clamp(float(r_src.min()),
                         float(r_src.max())) - r0) / (r1 - r0)).view(1, -1, 1, 1)
    f0 = u_src[:, idx - 1]; f1 = u_src[:, idx]
    return (1 - w) * f0 + w * f1


u = interp_r(u10, r10, rN).contiguous()
bodymask = G.body.cpu().numpy(); jt, jp = G.Nth // 2, G.Nps // 2
body_r_idx = np.where(bodymask[:, jt, jp])[0]
rfull = rN.cpu().numpy()
log(f"r nodes ({NR}): " + " ".join(f"{x:.2f}" for x in rfull))
dg0 = B.diagnose(u, G, Xt, XI, KAP, m=M, kap8=KAP8, branch=BR)
F0 = B.residual_vec(u, G, P, Xt, XI, KAP, m=M, kap8=KAP8, branch=BR)
log(f"interpolated seed: Phi={float((F0*F0).sum()):.3e}  M_MS={dg0['M_MS']:.4e}  AB={dg0['AB']:.3e}")


def bodyflat(dg):
    pr = np.abs(dg['proper_rho'][body_r_idx]); return float(pr.max()/max(pr.mean(),1e-30))


log("\nflooring at X=-2e5 from the warm seed ...")
u, hist, tsec, capped = B.lm_solve(u, G, P, Xt, XI, KAP, m=M, kap8=KAP8, branch=BR,
                                   maxit=10, lam0=1e-4, wall_cap=720.0, verbose=True)
torch.save(u.cpu(), f"/tmp/uP_Nr{NR}_X2e5_warm.pt")
dg = B.diagnose(u, G, Xt, XI, KAP, m=M, kap8=KAP8, branch=BR)
pr = dg['proper_rho']; phir = dg['phi_r']; bi = body_r_idx
prb = np.abs(pr[bi]); imax = bi[int(np.argmax(prb))]
frac = np.where(bi == imax)[0][0] / max(len(bi)-1, 1)
dpr = np.diff(prb)
interior = (0.15 < frac < 0.85) and not np.all(dpr > -1e-30) and not np.all(dpr < 1e-30)
kind = ("INTERIOR CORE (body!)" if interior else "OUTER-EDGE/seal pile-up" if frac >= 0.85
        else "CORE-concentrated" if frac <= 0.15 else "ambiguous")
log("\n" + "=" * 78)
log(f"RESULT Nr={NR} X=-2e5  Phi {hist[0]:.2e}->{hist[-1]:.2e} ({len(hist)-1} it/{tsec:.0f}s)")
log(f"  M_MS={dg['M_MS']:.4e}  AB={dg['AB']:.3e}  body_flat(max/mean)={bodyflat(dg):.2f}  "
    f"peak r={rfull[imax]:.2f}(frac {frac:.2f})  phi_depth={max(abs(dg['phi_min']),abs(dg['phi_max'])):.3e}")
log(f"  => {kind}")
log(f"  proper-rho(r): " + " ".join(
    f"{rfull[i]:.2f}{'*' if bodymask[i,jt,jp] else ' '}:{pr[i]:+.2e}" for i in range(len(rfull))))
log(f"  phi(r):        " + " ".join(f"{rfull[i]:.2f}:{phir[i]:+.2e}" for i in range(len(rfull))))
log(f"\n  Nr=10 ref: body_flat~2.5, AB~8.3, M_MS~750, phi core/seal layers -0.40/+0.44, flat body ~0.01")
log(f"=== DONE Nr={NR}  total={time.time()-t0:.0f}s ===")
