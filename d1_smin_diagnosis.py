#!/usr/bin/env python3
"""D1 conditioning -- DIAGNOSE the near-null direction (smin~6e-9) BEFORE building the integration
preconditioner. Per the research (Hesthaven integration-preconditioning recipe), the gating risk:
- if the smallest right-singular vector is EDGE-LOCALIZED / oscillatory -> numerical (Chebyshev endpoint
  amplification) -> the left integration preconditioner lifts it -> build #1 floors.
- if it is SMOOTH / gauge-like / spread -> a POSING near-redundancy (two BC rows ~dependent) -> NO
  conditioning trick fixes it -> needs a BC/gauge correction instead.
Cheap: one Jacobian build + one SVD; reshape the null vector into the 11 named fields + radial profile.
Category-A (conditioning diagnosis). Run UNBUFFERED (python3 -u), no grep pipe."""
import os
os.environ.setdefault('PYTORCH_NVML_BASED_CUDA_CHECK', '0')
import torch, numpy as np
torch.set_default_dtype(torch.float64)
import p1_residual_general_einstein as P1
from full3d_spectral import attach_coord_weight, Grid3D
from torch.func import jacrev

G = attach_coord_weight(Grid3D(Nr=8, Nth=6, Nps=8, rc=0.1, cell=8.0))
FIELDS = ['a', 'b', 'c', 'd', 'n1', 'n2', 'n3', 'phi', 'e_rt', 'e_rp', 'e_tp']
f = lambda uu: P1.residual_vector_p1(uu, G, 1.0, 1.0, X=-2e5, branch='G', determined=True)

def analyze(u, tag):
    J = jacrev(f, chunk_size=128)(u).double()
    # economy SVD; right singular vectors are rows of Vh
    U, S, Vh = torch.linalg.svd(J, full_matrices=False)
    sv = S.cpu().numpy()
    print(f"\n=== {tag}: J{tuple(J.shape)}  smax={sv[0]:.3e} smin={sv[-1]:.3e} cond={sv[0]/sv[-1]:.3e} ===", flush=True)
    print(f"  smallest 6 SV: {np.array2string(sv[-6:], precision=3)}", flush=True)
    # look at the 2 smallest right-singular vectors (the near-null directions)
    for k in (1, 2):
        v = Vh[-k]                                   # right singular vector of the k-th-smallest SV
        comps = P1.unpack11(v, G)                    # split into the 11 named fields, each (Nr,Nth,Nps)
        fn = np.array([float((cc**2).sum()) for cc in comps])  # energy per field
        fn = fn / fn.sum()
        # radial profile (energy per radial layer, summed over fields+angles); layer 0=core, Nr-1=seal
        rad = np.array([float(sum((cc[ri]**2).sum() for cc in comps)) for ri in range(G.Nr)])
        rad = rad / rad.sum()
        top = np.argsort(fn)[::-1][:4]
        print(f"  -- null vec #{k} (SV={sv[-k]:.3e}) --", flush=True)
        print(f"     field energy frac: " + ", ".join(f"{FIELDS[i]}={fn[i]:.2f}" for i in top), flush=True)
        print(f"     radial-layer energy frac [core..seal]: {np.array2string(rad, precision=3)}", flush=True)
        edge = rad[0] + rad[-1]
        print(f"     EDGE fraction (layer0+layer{G.Nr-1}) = {edge:.2f}  -> "
              f"{'EDGE-LOCALIZED (numerical; preconditioner lifts it)' if edge > 0.6 else 'SPREAD/INTERIOR (posing/gauge -- conditioning will NOT fix; needs BC/gauge)'}", flush=True)

# generic point = the old (intact) field; cross-check at a symmetry-broken seed
d = torch.load('solved_fields_nr8_G_kap8_1.pt', map_location='cpu', weights_only=False)
analyze(d['u'].to(G.Dr.device), "OLD field (generic pt)")
torch.manual_seed(0)
u2 = P1.seed_round_native(G, p=1.0, m=1) + 1e-3*torch.randn(11*8*6*8, device=G.Dr.device)
analyze(u2, "seed+noise (cross-check)")
