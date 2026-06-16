#!/usr/bin/env python3
"""
radial_Bfree_depth.py -- Tasks 3 & 4: what-changed-vs-#52 and the CORRECTED
depth-mass map, with B=1/A FREED and the legacy seal-injection defect REMOVED.

Driver: Claude (Opus 4.8, 1M). 2026-06-15. OBSERVE mode. DATA-BLIND.

Two corrections are in play and are ISOLATED here:
  (A) FREE B=1/A  -- a(r),b(r) independent (the #55 gate finding).
  (B) DROP the linear seal-injection defect -- it injected un-sourced mass and
      broke (t,t) (THIS push's gate finding; see solve_b_from_tt docstring).
Columns compare: reduced #52 (ties b=-a, has defect) ; freed+defect (B free,
defect kept) ; freed-corrected (B free, no defect = the delivered solver).
"""
import os
os.environ.setdefault("PYTORCH_NVML_BASED_CUDA_CHECK", "0")
import math
import torch
from radial_Bfree_soliton import make_grid, selfconsistent_Bfree, grad_central
import complete_metric_batched as red

torch.set_default_dtype(torch.float64)
DEV = "cuda" if torch.cuda.is_available() else "cpu"


def width_of(r, Th):
    """radial location where Theta crosses pi/2 (the soliton core size)."""
    rg = r[0]; Tg = Th[0]
    target = math.pi/2
    idx = (Tg <= target).nonzero()
    if idx.numel() == 0:
        return float('nan')
    i = idx[0].item()
    if i == 0:
        return rg[0].item()
    r0, r1 = rg[i-1].item(), rg[i].item()
    t0, t1 = Tg[i-1].item(), Tg[i].item()
    return r0 + (target - t0)*(r1 - r0)/(t1 - t0)


REPORT = []
def out(s):
    REPORT.append(s); print(s, flush=True)


KAP8 = 0.05                                        # canonical coupling
L = 1.0; rc = 0.05; ri = rc + 14.0*L
N = 600                                            # M_MS stable to 4 dp vs N=1200
ITF = 90; ITR = 100

out("="*78)
out("TASK 3/4: head-to-head at p=0.4 -- isolating the two corrections")
out("  reduced#52 (b=-a tie, seal defect) | freed+defect | freed-CORRECTED (delivered)")
out("="*78)
r = make_grid(1, N, rc=rc, rint=ri, geom=False)
red_out = red.selfconsistent_batched(r.clone(), 1.0, 1.0, m=1, p=0.4,
                                     kap8=KAP8, iters=ITR, relax=0.5, tol=1e-11)
# freed WITH legacy defect (isolates the B-freeing effect alone)
fd_out = selfconsistent_Bfree(r.clone(), 1.0, 1.0, m=1, p=0.4, kap8=KAP8,
                              iters=ITF, relax=0.5, tol=1e-12, seal_defect=True)
# freed CORRECTED (delivered)
fc_out = selfconsistent_Bfree(r.clone(), 1.0, 1.0, m=1, p=0.4, kap8=KAP8,
                              iters=ITF, relax=0.5, tol=1e-12)
mr = red_out['M_MS'].item(); mfd = fd_out['M_MS'].item(); mfc = fc_out['M_MS'].item()
out(f"  reduced #52     : M_MS={mr:.6f}  width(Th=pi/2)={width_of(r, red_out['Th']):.4f}")
out(f"  freed + defect  : M_MS={mfd:.6f}  width={width_of(r, fd_out['Th']):.4f}  "
    f"(B-freeing alone moves M by {100*(mfd-mr)/mr:+.3f}%)")
out(f"  freed CORRECTED : M_MS={mfc:.6f}  width={width_of(r, fc_out['Th']):.4f}  "
    f"(total move vs #52 {100*(mfc-mr)/mr:+.3f}%)")
Tr = red_out['Th'][0]; Tf = fc_out['Th'][0]
out(f"  max|Theta_corrected - Theta_#52| = {(Tf-Tr).abs().max().item():.4e}")
apb = fc_out['a'][0] + fc_out['b'][0]
out(f"  corrected interior max|a+b| (B=1/A departure / interior warp) = {apb.abs().max().item():.4e}")

out("\n" + "="*78)
out("TASK 4: CORRECTED depth-mass map, B=1/A freed + defect dropped (data-blind)")
out("="*78)
ps = [0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.2, 1.5]
# reduced #52 is computed only for p<=0.5 (it goes unstable / blows up deeper).
out(f"  {'p':>5} {'M_MS_corr':>13} {'M_MS_#52':>13} {'ratio':>8} {'width':>8} {'max|a+b|':>10} {'a0=phi0':>9}")
rows = []
for p in ps:
    rp = make_grid(1, N, rc=rc, rint=ri, geom=False)
    fo = selfconsistent_Bfree(rp.clone(), 1.0, 1.0, m=1, p=p, kap8=KAP8,
                              iters=ITF, relax=0.4, tol=1e-12)
    mf = fo['M_MS'].item()
    if p <= 0.5:
        ro = red.selfconsistent_batched(rp.clone(), 1.0, 1.0, m=1, p=p, kap8=KAP8,
                                        iters=ITR, relax=0.5, tol=1e-11)
        mrr = ro['M_MS'].item()
        ratio = mf/mrr if mrr != 0 else float('nan')
        mrr_s = f"{mrr:13.6f}"; ratio_s = f"{ratio:8.4f}"
    else:
        mrr_s = f"{'(unstable)':>13}"; ratio_s = f"{'--':>8}"
    w = width_of(rp, fo['Th'])
    apb = (fo['a'][0]+fo['b'][0]).abs().max().item()
    a0 = fo['a'][0].min().item()
    out(f"  {p:5.2f} {mf:13.6f} {mrr_s} {ratio_s} {w:8.4f} {apb:10.3e} {a0:9.4f}")
    rows.append((p, mf, w, apb))

import math as _m
out("\n  shape diagnostic: d(ln M_MS_corr)/dp (super-exp if RISING with p)")
for i in range(1, len(rows)):
    p0, m0 = rows[i-1][0], rows[i-1][1]
    p1, m1 = rows[i][0], rows[i][1]
    if m0 > 0 and m1 > 0:
        slope = (_m.log(m1) - _m.log(m0))/(p1 - p0)
        out(f"    p in [{p0:.2f},{p1:.2f}]: d(lnM)/dp = {slope:.4f}")

with open("radial_Bfree_depth.out", "w") as f:
    f.write("\n".join(REPORT) + "\n")
out("\nWROTE radial_Bfree_depth.out")
