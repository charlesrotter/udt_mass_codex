import os
os.environ.setdefault('PYTORCH_NVML_BASED_CUDA_CHECK', '0')
import torch
torch.set_default_dtype(torch.float64)
import p1_residual_general_einstein as P1
from full3d_spectral import attach_coord_weight, Grid3D
from torch.func import jacrev
G = attach_coord_weight(Grid3D(Nr=8, Nth=6, Nps=8, rc=0.1, cell=8.0))
d = torch.load('xexplore_field_X1.pt', map_location='cpu', weights_only=False)
u = d['u'].to(G.Dr.device); X = d['X']
f = lambda uu: P1.residual_vector_p1(uu, G, 1.0, 1.0, X=X, branch='G', determined=True)
F = f(u)
J = jacrev(f, chunk_size=128)(u).double()
U, S, Vh = torch.linalg.svd(J, full_matrices=False)   # U: (rows, cols)
Phi = float((F*F).sum())
UtF = U.transpose(-1,-2) @ F                            # projection onto range(J)
reducible = float((UtF*UtF).sum())
irreducible = Phi - reducible                           # ||F_perp||^2 = LS floor (in left-null of J)
print(f"rows={J.shape[0]} cols={J.shape[1]} overdetermined by {J.shape[0]-J.shape[1]}", flush=True)
print(f"Phi (||F||^2)            = {Phi:.4e}", flush=True)
print(f"reducible (in range J)   = {reducible:.4e}  ({100*reducible/Phi:.1f}%)", flush=True)
print(f"IRREDUCIBLE (LS floor)   = {irreducible:.4e}  ({100*irreducible/Phi:.1f}%)", flush=True)
print("INTERPRET: if IRREDUCIBLE ~ Phi -> the posing is OVER-DETERMINED/inconsistent (no exact root; 2e-3 is a"
      " genuine LS floor). If IRREDUCIBLE ~ 0 -> F is reducible -> just slow convergence (a solver-strategy fix).", flush=True)
