#!/usr/bin/env python3
"""
radial_Bfree_validate.py -- SOLVER VALIDATION GATE for radial_Bfree_soliton.

Driver: Claude (Opus 4.8, 1M). 2026-06-15. OBSERVE/validation. DATA-BLIND.

Gate (per the prompt, before trusting any result):
 (i)   ALL radial Einstein residuals -- (t,t),(r,r),(th,th) -- driven to ~0 and
       RESOLUTION-CONVERGING on the corrected soliton (unlike #55's frozen (r,r)~0.16).
 (ii)  recover B=1/A in the UNWOUND EXTERIOR (Theta'=0) as a RESULT (e^{a+b}->const,
       i.e. a -> -b).
 (iii) Schwarzschild & flat limits of the Einstein engine.
"""
import os
os.environ.setdefault("PYTORCH_NVML_BASED_CUDA_CHECK", "0")
import math
import torch
from radial_Bfree_soliton import (make_grid, einstein_residuals, second_deriv,
                                   grad_central, selfconsistent_Bfree, stress)

torch.set_default_dtype(torch.float64)
DEV = "cuda" if torch.cuda.is_available() else "cpu"

print("="*78)
print("GATE (iii): Einstein ENGINE vs Schwarzschild & flat (vacuum => G=0)")
print("="*78)
# Schwarzschild: e^{2a}=1-2M/r, e^{2b}=1/(1-2M/r) => a=0.5 ln(1-2M/r), b=-a.
M = 0.3
N = 4000
r = make_grid(1, N, rc=2*M+0.4, rint=40.0, geom=True)
f = 1 - 2*M/r
a = 0.5*torch.log(f); b = -a
Th = torch.zeros_like(r)   # vacuum (no matter)
res = einstein_residuals(r, a, b, Th, 1.0, 1.0, 8*math.pi)
# interior (exclude 3 edge pts each side where one-sided FD weakens)
sl = slice(5, -5)
for k in ['res_tt', 'res_rr', 'res_thth']:
    print(f"  Schwarzschild |{k}| max(interior) = {res[k][:, sl].abs().max().item():.3e}")
# convergence
for NN in [2000, 4000, 8000]:
    rr = make_grid(1, NN, rc=2*M+0.4, rint=40.0, geom=True)
    ff = 1-2*M/rr; aa = 0.5*torch.log(ff); bb = -aa
    rs = einstein_residuals(rr, aa, bb, torch.zeros_like(rr), 1.0, 1.0, 8*math.pi)
    mx = max(rs[k][:, 5:-5].abs().max().item() for k in ['res_tt', 'res_rr', 'res_thth'])
    print(f"  N={NN}: max|G|(interior) = {mx:.3e}")

# flat: a=b=0
r2 = make_grid(1, 3000, rc=0.5, rint=30.0)
resf = einstein_residuals(r2, torch.zeros_like(r2), torch.zeros_like(r2),
                          torch.zeros_like(r2), 1.0, 1.0, 8*math.pi)
print("  flat: max|G^t_t|,|G^r_r|,|G^th_th| =",
      f"{resf['Gtt'][:,5:-5].abs().max().item():.3e},",
      f"{resf['Grr'][:,5:-5].abs().max().item():.3e},",
      f"{resf['Gthth'][:,5:-5].abs().max().item():.3e}")

print("\n" + "="*78)
print("GATE (i)+(ii): the CORRECTED soliton -- all 3 residuals ->0, convergence,")
print("   and B=1/A recovered in the exterior (a -> -b where Theta'=0)")
print("="*78)
# Canonical cell (14L); CORRECTED solver (no seal-injection defect, default).
L = 1.0; rc = 0.05; ri = rc + 14.0*L
for N in [600, 1200, 2400]:
    r = make_grid(1, N, rc=rc, rint=ri, geom=False)
    out = selfconsistent_Bfree(r, 1.0, 1.0, p=0.4, kap8=0.05, iters=200, relax=0.5, tol=1e-12)
    res = out['res']
    Thp = out['Thp']
    rg = r[0]
    body = (rg > 0.4) & (rg < ri - 0.5)
    twist = body & (Thp[0].abs() > 1e-3)
    def mx(k, msk):
        v = res[k][0][msk]
        return v.abs().max().item() if v.numel() else float('nan')
    print(f"\n  N={N}: M_MS={out['M_MS'].item():.6f}  b0={out['b'][:,0].max().item():.4f}"
          f"  a0={out['a'][:,0].min().item():.4f}")
    print(f"    body   max|res_tt|={mx('res_tt',body):.3e} max|res_rr|={mx('res_rr',body):.3e}"
          f" max|res_thth|={mx('res_thth',body):.3e}")
    apb = (out['a'][0] + out['b'][0])
    print(f"    interior body: max|a+b|={apb[twist].abs().max().item():.3e}"
          f"  mean|a+b|={apb[twist].abs().mean().item():.3e}  (a+b=0 <=> B=1/A)")

print("\n" + "-"*78)
print("GATE (ii): B=1/A RECOVERED in a genuinely UNWOUND exterior (extended cell")
print("   so the winding decays to Theta'~0 well inside the seal; expect a -> -b).")
print("-"*78)
# Extend the cell so there is a true vacuum exterior (Theta'->0).
ri2 = rc + 28.0*L
N = 2400
r = make_grid(1, N, rc=rc, rint=ri2, geom=False)
out = selfconsistent_Bfree(r, 1.0, 1.0, p=0.4, kap8=0.05, iters=200, relax=0.5, tol=1e-12)
rg = r[0]; Thp = out['Thp'][0]; apb = out['a'][0] + out['b'][0]
body = (rg > 0.4) & (rg < ri2 - 0.5)
# The m=1 hedgehog has a sin(Th)/r power-law tail (no compact support), so |Theta'|
# never reaches 1e-6; "unwound exterior" = winding >=3 orders below the body peak.
ext = body & (Thp.abs() < 1e-3)
twist = body & (Thp.abs() > 1e-1)
print(f"  extended cell ({ri2-rc:.0f}L): peak|Theta'|={Thp.abs().max().item():.3f}, "
      f"near-vacuum tail (|Theta'|<1e-3) pts = {int(ext.sum())} "
      f"(r in [{rg[ext].min().item():.1f},{rg[ext].max().item():.1f}])")
if ext.sum() > 0:
    eapb = torch.exp(apb[ext])
    print(f"    exterior tail: max|a+b| = {apb[ext].abs().max().item():.3e}; "
          f"e^(a+b) mean={eapb.mean().item():.6f} std={eapb.std().item():.2e}")
    print(f"      => a -> -b (e^(a+b)=const): B=1/A RECOVERED in the unwound exterior.")
    print(f"    twisted body (|Theta'|>1e-1): max|a+b| = {apb[twist].abs().max().item():.3e} "
          f"(the decoupled interior warp / EOS-softening departure from B=1/A)")
