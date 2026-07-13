"""Downsample the 256^3 critical field to a coarser grid for the 192/128^3 Hessian arm of the hybrid
spectral test (Charles 2026-07-12). Trilinear-interpolates the field and writes correct params (N,L,h).

Usage:
  TARGET_N=192 SRC=noNull_critical_field.npz python3 noNull_downsample.py    # -> noNull_critical_field_192.npz
Then re-relax to the SAME resolution-aware criticality and Hessian at that grid:
  BASE_FIELD=noNull_critical_field_192.npz CRIT_FIELD=noNull_critical_field_192.npz \
    STAGE=nk NK_BUDGET_S=6000 PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True timeout 9000 python3 noNull_resolve.py
  BASE_FIELD=noNull_critical_field_192.npz CRIT_FIELD=noNull_critical_field_192.npz \
    STAGE=hess HESS_BW=2 HESS_BS=12 HESS_SEEDS=0,1 PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True timeout 36000 python3 noNull_resolve.py
(NB: the interpolated field is NOT critical for the coarse operator -> STAGE=nk MUST re-relax it to
 ||g_f||_M-1<0.05 before the Hessian is meaningful. bs=12 fits at 192/128^3.)"""
import os, numpy as np, torch
import torch.nn.functional as F
torch.set_default_dtype(torch.float64)
src = os.environ.get('SRC', 'noNull_critical_field.npz'); tN = int(os.environ.get('TARGET_N', '192'))
out = os.environ.get('OUT', f'noNull_critical_field_{tN}.npz')
d = np.load(src); n = torch.tensor(d['n']); L = float(d['L']); xi = float(d['xi']); kap = float(d['kappa'])
n2 = F.interpolate(n[None], size=(tN, tN, tN), mode='trilinear', align_corners=True)[0]
n2 = n2 / n2.norm(dim=0, keepdim=True)
h2 = 2 * L / (tN - 1)
np.savez(out, n=n2.numpy(), N=tN, L=L, h=h2, xi=xi, kappa=kap)
print(f"wrote {out}: N={tN} h={h2:.5f}  (from {src}, N={int(d['N'])}, L={L})")
print(f"NEXT: BASE_FIELD={out} CRIT_FIELD={out}  STAGE=nk ... (re-relax to ||g_f||<0.05)  then  STAGE=hess HESS_BS=12 ...")
