import os; os.environ.setdefault("PYTORCH_NVML_BASED_CUDA_CHECK","0")
import numpy as np, torch
torch.set_default_dtype(torch.float64)
from spectral_catalog_solver import TGrid, metric_stack, einstein_mixed_t, round_seed, unpack
# Sanity: contracted Bianchi  div_mu G^mu_nu = 0  for ANY metric (identity).
# Test my divergence operator on the soliton metric with the committed Einstein G.
G=TGrid(64,8,rc=0.05,cell=14.0)
u0,rad=round_seed(G,p=0.4,kap8=0.05)
a,b,c,d,Th=unpack(u0,G)
g,ginv=metric_stack(G,a,b,c,d)
comps=einstein_mixed_t(G,a,b,c,d)
nr,nth=G.nr,G.nth
Gm=torch.zeros(nr,nth,4,4)
for (m,n),v in comps.items():
    Gm[...,m,n]=v
dr=G.d_r; dth=G.d_th
dg=torch.zeros(nr,nth,4,4,4)
for m in range(4):
    dg[...,1,m,m]=dr(g[...,m,m]); dg[...,2,m,m]=dth(g[...,m,m])
Gam=torch.zeros(nr,nth,4,4,4)
for al in range(4):
 for be in range(4):
  for ga in range(4):
   s=torch.zeros(nr,nth)
   for de in range(4):
     s=s+ginv[...,al,de]*(dg[...,ga,de,be]+dg[...,be,de,ga]-dg[...,de,be,ga])
   Gam[...,al,be,ga]=0.5*s
def dcoord(F,cc):
    if cc==1: return dr(F)
    if cc==2: return dth(F)
    return torch.zeros_like(F)
body=(G.R>0.8)&(G.R<G.ri-0.8)
for nu in range(4):
    s=torch.zeros(nr,nth)
    for mu in range(4):
        s=s+dcoord(Gm[...,mu,nu],mu)
        for l in range(4):
            s=s+Gam[...,mu,mu,l]*Gm[...,l,nu]-Gam[...,l,mu,nu]*Gm[...,mu,l]
    print(f"div_mu G^mu_{nu}  body max-abs = {float(s[body].abs().max()):.3e}")
