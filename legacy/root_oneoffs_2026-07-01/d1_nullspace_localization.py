#!/usr/bin/env python3
"""D1 follow-up: WHERE do the 2448 unconstrained (null-space) directions live? Decompose the Jacobian
null space by field-block and radial layer to see whether the under-determination is concentrated in
the EXCISED core/seal layers (benign — those are meant to be BC-set) or bleeds into the interior BODY
and the physics fields (phi/winding/warps) — which would mean the banked readouts genuinely move.
NO solve — one jacrev eval + an SVD (minutes)."""
import os
os.environ.setdefault('PYTORCH_NVML_BASED_CUDA_CHECK', '0')
import torch, numpy as np
torch.set_default_dtype(torch.float64)
import p1_residual_general_einstein as P1
from full3d_spectral import attach_coord_weight, Grid3D

G = attach_coord_weight(Grid3D(Nr=8, Nth=6, Nps=8, rc=0.1, cell=8.0))
d = torch.load('solved_fields_nr8_G_kap8_1.pt', map_location='cpu', weights_only=False)
u = d['u'].to(G.dev); Xfin = float(d['Xfin'])
ncols = u.numel()
J, _ = P1.jacobian_p1(u, G, 1.0, 1.0, X=Xfin, branch='G', chunk_size=128)
U, S, Vh = torch.linalg.svd(J.double(), full_matrices=True)   # Vh: (ncols, ncols)
rank = int((S > 1e-10 * S[0]).sum())
Nullh = Vh[rank:, :]                                          # (null_dim, ncols): rows span null(J)
print(f"J {tuple(J.shape)}  rank={rank}  null_dim={ncols - rank}")

fields = ['a', 'b', 'c', 'd', 'n1', 'n2', 'n3', 'phi', 'e_rt', 'e_rp', 'e_tp']
W = (Nullh ** 2).sum(0)                                       # (ncols,) null weight per unknown
Wf = W.reshape(11, G.Nr, G.Nth, G.Nps)
perfield = Wf.sum((1, 2, 3)); perfield = perfield / perfield.sum()
perlayer = Wf.sum((0, 2, 3)); perlayer = perlayer / perlayer.sum()
rad = G.Rg.mean((1, 2)).cpu().numpy()

print("\nnull-space weight by FIELD (fraction of the 2448 unconstrained directions):")
for nm, w in zip(fields, perfield.cpu().numpy()):
    print(f"  {nm:6s} {w:.3f}")
print("\nnull-space weight by RADIAL LAYER (0=core .. 7=seal; PDE imposed only on BODY=[3,4]):")
for i, w in enumerate(perlayer.cpu().numpy()):
    print(f"  layer {i}  r={rad[i]:6.3f}  {'BODY' if 3 <= i < 5 else 'excised':8s}  {w:.3f}")

body_w = float(perlayer[3:5].sum())
phys_fields_w = float(perfield[[0,1,2,3,4,5,6,7]].sum())     # a,b,c,d,n1,n2,n3,phi (warps+matter+dilaton)
print(f"\nnull weight in BODY layers (3,4) = {body_w:.3f}   in excised core/seal = {1-body_w:.3f}")
print(f"null weight in physics fields (warps+matter+phi) = {phys_fields_w:.3f}   in off-diagonals = {1-phys_fields_w:.3f}")
print("\nREAD: null weight ~all in excised layers + benign => interior readouts (phi-depth at body,")
print("  winding degree, warp) live in the CONSTRAINED subspace -> banked results likely survive.")
print("  Heavy null weight in BODY layers and phi/n => readouts move -> re-grade required.")
