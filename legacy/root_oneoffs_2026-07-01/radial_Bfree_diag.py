#!/usr/bin/env python3
"""radial_Bfree_diag.py -- gate diagnostics: res_tt truncation (FD vs real),
exterior B=1/A recovery, and the interior-warp localization. Writes a report
file so output is never lost to stdout buffering. Driver: Claude, 2026-06-15."""
import os
os.environ.setdefault("PYTORCH_NVML_BASED_CUDA_CHECK", "0")
import math, torch
torch.set_default_dtype(torch.float64)
from radial_Bfree_soliton import make_grid, selfconsistent_Bfree

L = 1.0; rc = 0.05; ri = rc + 14.0*L
lines = []
def out(s):
    lines.append(s); print(s, flush=True)

out("DIAGNOSTIC: res_tt truncation, exterior B=1/A recovery, interior warp")
out("cell rc=%.3f ri=%.3f  kap8=0.05  p=0.4  xi=kap=1" % (rc, ri))
for N in [900, 1800, 3600]:
    r = make_grid(1, N, rc=rc, rint=ri, geom=False)
    o = selfconsistent_Bfree(r, 1.0, 1.0, p=0.4, kap8=0.05, iters=400, relax=0.4, tol=1e-12)
    res = o['res']; rg = r[0]; Thp = o['Thp'][0]
    apb = (o['a'][0] + o['b'][0])
    ext = (rg > ri*0.6)                          # unwound exterior (Theta'->0)
    twist = (rg > 0.4) & (Thp.abs() > 1e-3)      # twisted body
    far = (rg > 1.0) & (rg < ri - 0.5)           # away from deep-core coord spike
    rtt_far = res['res_tt'][0][far].abs().max().item()
    rtt_full = res['res_tt'][0][(rg > 0.4) & (rg < ri-0.5)].abs().max().item()
    out("N=%d  M_MS=%.6f" % (N, o['M_MS'].item()))
    out("   res_tt: max(body r>0.4)=%.3e  max(r>1.0, off-spike)=%.3e"
        % (rtt_full, rtt_far))
    out("   res_rr: max(body)=%.3e   res_thth: max(body)=%.3e"
        % (res['res_rr'][0][twist].abs().max().item(),
           res['res_thth'][0][twist].abs().max().item()))
    out("   EXTERIOR (r>0.6 ri, Theta'~0): max|a+b|=%.3e  mean|a+b|=%.3e  (B=1/A <=> a+b=0)"
        % (apb[ext].abs().max().item(), apb[ext].abs().mean().item()))
    out("   TWIST body: max|a+b|=%.3e  mean|a+b|=%.3e  argmax at r=%.3f (Theta=%.3f)"
        % (apb[twist].abs().max().item(), apb[twist].abs().mean().item(),
           rg[apb.abs().argmax()].item(), o['Th'][0][apb.abs().argmax()].item()))

with open("radial_Bfree_diag.out", "w") as f:
    f.write("\n".join(lines) + "\n")
out("\nWROTE radial_Bfree_diag.out")
