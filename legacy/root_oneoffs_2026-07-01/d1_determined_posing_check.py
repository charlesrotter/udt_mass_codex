import torch, numpy as np
torch.set_default_dtype(torch.float64)
import p1_residual_general_einstein as P1
from full3d_spectral import attach_coord_weight, Grid3D
from torch.func import jacrev
G = attach_coord_weight(Grid3D(Nr=8, Nth=6, Nps=8, rc=0.1, cell=8.0))
ncols = 11*8*6*8
# GENERIC point: the saved converged field (non-symmetric, e_rt~0.11) -- the right linearization point
d = torch.load('solved_fields_nr8_G_kap8_1.pt', map_location='cpu', weights_only=False)
u = d['u'].to(G.Dr.device)
f = lambda uu: P1.residual_vector_p1(uu, G, 1.0, 1.0, X=-2e5, branch='G', determined=True)
J = jacrev(f, chunk_size=128)(u)
sv = torch.linalg.svdvals(J.double()).cpu().numpy()
print(f"[GENERIC pt] rows={J.shape[0]} cols={ncols}",flush=True)
for tol in (1e-8,1e-10,1e-12):
    rank=int((sv>tol*sv[0]).sum()); print(f"  tol={tol:.0e}: rank={rank} null-dim={ncols-rank}",flush=True)
print(f"  smin={sv[-1]:.3e} smax={sv[0]:.3e}  smallest 8 SV: {np.array2string(sv[-8:],precision=3)}",flush=True)
# also at a symmetry-broken seed (seed + small noise) as a cross-check
torch.manual_seed(0); u2 = P1.seed_round_native(G,p=1.0,m=1) + 1e-3*torch.randn(ncols,device=G.Dr.device)
J2 = jacrev(f, chunk_size=128)(u2); sv2 = torch.linalg.svdvals(J2.double()).cpu().numpy()
print(f"[seed+noise] null-dim @1e-10={ncols-int((sv2>1e-10*sv2[0]).sum())} smin={sv2[-1]:.3e}",flush=True)
