import os
os.environ.setdefault('PYTORCH_NVML_BASED_CUDA_CHECK', '0')
import torch
torch.set_default_dtype(torch.float64)
import p1_residual_general_einstein as P1
import branch_operator as BR, free_s2_matter as S2M
from full3d_spectral import attach_coord_weight, Grid3D, build_metric, T, R as RR, TH, PS
G = attach_coord_weight(Grid3D(Nr=8, Nth=6, Nps=8, rc=0.1, cell=8.0))
d = torch.load('xexplore_field_X1.pt', map_location='cpu', weights_only=False)
u = d['u'].to(G.Dr.device)
a,b,c,dd,n1,n2,n3,phi,ert,erp,etp = P1.unpack11(u,G)
n_raw=torch.stack([n1,n2,n3],-1); dn=S2M.field_dn_components_exact(G,n_raw)
E = BR.E_mixed_branch(G,a,b,c,dd,phi,dn,X=-1.0,xi=1.0,kap=1.0,m=1,kap8=1.0,e_rt=ert,e_rp=erp,e_tp=etp)
# diagonal Einstein residual magnitude per radial layer (max over angles), layer 0=core .. 7=seal
diag = (E[...,T,T]**2+E[...,RR,RR]**2+E[...,TH,TH]**2+E[...,PS,PS]**2).sqrt()
print("radial layer:           ", " ".join(f"{i:>9d}" for i in range(G.Nr)), flush=True)
print("max|E_diag| per layer:  ", " ".join(f"{float(diag[i].max()):9.2e}" for i in range(G.Nr)), flush=True)
print("\nINTERPRET: layers 0..7 = core(rc)..seal(ri). If the residual peaks at the EDGE layers (0,1 and/or 6,7)"
      " -> the determined PDE-at-stiff-edges is the floor (parity/Galerkin basis territory). If bulk-peaked -> not edges.", flush=True)
