import os
os.environ.setdefault('PYTORCH_NVML_BASED_CUDA_CHECK', '0')
import torch
torch.set_default_dtype(torch.float64)
import p1_residual_general_einstein as P1
from full3d_spectral import attach_coord_weight, Grid3D
G = attach_coord_weight(Grid3D(Nr=8, Nth=6, Nps=8, rc=0.1, cell=8.0))
d = torch.load('xexplore_field_X1.pt', map_location='cpu', weights_only=False)
u = d['u'].to(G.Dr.device)
F0 = P1.residual_vector_p1(u, G, 1.0, 1.0, X=-1.0, branch='G', determined=True)
print(f"GALERKIN warm-start from X=-1 field (collocation Phi={float((F0*F0).sum()):.3e}). Floor?", flush=True)
u, hist = P1.newton_solve_p1(u, G, 1.0, 1.0, X=-1.0, branch='G', m=1, maxit=20,
                             tol=1e-12, determined=True, step='galerkin', verbose=True)
print("final Phi=%.3e" % hist[-1], flush=True)
