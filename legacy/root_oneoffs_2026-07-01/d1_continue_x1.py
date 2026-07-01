import os
os.environ.setdefault('PYTORCH_NVML_BASED_CUDA_CHECK', '0')
import torch
torch.set_default_dtype(torch.float64)
import p1_residual_general_einstein as P1
from full3d_spectral import attach_coord_weight, Grid3D
G = attach_coord_weight(Grid3D(Nr=8, Nth=6, Nps=8, rc=0.1, cell=8.0))
d = torch.load('xexplore_field_X1.pt', map_location='cpu', weights_only=False)
u = d['u'].to(G.Dr.device)
print("continue X=-1 from saved Phi=2.09e-3; does it KEEP dropping (under-converged) or PLATEAU (posing floor)?", flush=True)
u, hist = P1.newton_solve_p1(u, G, 1.0, 1.0, X=-1.0, branch='G', m=1, maxit=20, tol=1e-14, determined=True, verbose=True)
print("Phi curve:", [f"{h:.3e}" for h in hist], flush=True)
