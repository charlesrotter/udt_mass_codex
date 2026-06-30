import os
os.environ.setdefault('PYTORCH_NVML_BASED_CUDA_CHECK', '0')
import torch
torch.set_default_dtype(torch.float64)
import p1_residual_general_einstein as P1
from full3d_spectral import attach_coord_weight, Grid3D
G = attach_coord_weight(Grid3D(Nr=8, Nth=6, Nps=8, rc=0.1, cell=8.0))
d = torch.load('xexplore_field_X1.pt', map_location='cpu', weights_only=False)
u = d['u'].to(G.Dr.device)
print("SVD+line-search step from saved X=-1 (Phi=2.09e-3): does it FLOOR now?", flush=True)
u, hist = P1.newton_solve_p1(u, G, 1.0, 1.0, X=-1.0, branch='G', m=1, maxit=40,
                             tol=1e-12, determined=True, step='svd_ls', verbose=True)
print("final Phi=%.3e" % hist[-1], flush=True)
torch.save({'u': u.cpu(), 'X': -1.0, 'Phi': hist[-1], 'branch':'G','kap8':1.0,'determined':True}, 'xexplore_field_X1_floored.pt')
