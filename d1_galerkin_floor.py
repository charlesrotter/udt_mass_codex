import os
os.environ.setdefault('PYTORCH_NVML_BASED_CUDA_CHECK', '0')
import torch
torch.set_default_dtype(torch.float64)
import p1_residual_general_einstein as P1
from full3d_spectral import attach_coord_weight, Grid3D
G = attach_coord_weight(Grid3D(Nr=8, Nth=6, Nps=8, rc=0.1, cell=8.0))
u = P1.seed_round_native(G, p=1.0, m=1)
print("GALERKIN floor test: round seed, X=-1, branch G, kap8=1, determined. Does it FLOOR (<1e-6)?", flush=True)
u, hist = P1.newton_solve_p1(u, G, 1.0, 1.0, X=-1.0, branch='G', m=1, maxit=50,
                             tol=1e-12, determined=True, step='galerkin', verbose=True)
print("final Phi=%.3e  (floored if <1e-6)" % hist[-1], flush=True)
torch.save({'u': u.cpu(),'X':-1.0,'Phi':hist[-1],'branch':'G','kap8':1.0,'determined':True}, 'galerkin_floored_X1.pt')
