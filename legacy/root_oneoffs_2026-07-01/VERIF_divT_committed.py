import os; os.environ.setdefault("PYTORCH_NVML_BASED_CUDA_CHECK","0")
import numpy as np, torch
torch.set_default_dtype(torch.float64)
from spectral_catalog_solver import (TGrid, matter_stress_t, metric_stack,
    einstein_mixed_t, matter_el_t, round_seed, unpack)
# Build the round soliton on the 2D grid, compute committed stress Tmix, then
# div_mu T^mu_nu numerically via the SAME spectral derivative operators + connection.
G=TGrid(64,8,rc=0.05,cell=14.0)
u0,rad=round_seed(G,p=0.4,kap8=0.05)
a,b,c,d,Th=unpack(u0,G)
g,ginv=metric_stack(G,a,b,c,d)
Tmix=matter_stress_t(G,Th,a,b,c,d,ginv,g)  # T^mu_nu
# Christoffels from metric numerically (diagonal metric, use analytic-ish via spectral derivs).
# Build full Christoffel Gam^al_be_ga at all grid pts. Metric diag g_mm.
nr,nth=G.nr,G.nth
def dr(f): return G.d_r(f)
def dth(f): return G.d_th(f)
# coordinate derivs of g_{mn}: only diagonal nonzero; depends on r,theta
gd=g  # g[...,m,n]
# derivative of g wrt coord (0=t:0, 1=r, 2=theta, 3=psi:0)
dg=torch.zeros(nr,nth,4,4,4)  # dg[...,c,m,n] = d_c g_mn
for m in range(4):
    dg[...,1,m,m]=dr(g[...,m,m])
    dg[...,2,m,m]=dth(g[...,m,m])
Gam=torch.zeros(nr,nth,4,4,4)  # Gam[...,al,be,ga]
for al in range(4):
 for be in range(4):
  for ga in range(4):
   s=torch.zeros(nr,nth)
   for de in range(4):
     s=s+ginv[...,al,de]*(dg[...,ga,de,be]+dg[...,be,de,ga]-dg[...,de,be,ga])
   Gam[...,al,be,ga]=0.5*s
# div_mu T^mu_nu = d_mu T^mu_nu + Gam^mu_mu_l T^l_nu - Gam^l_mu_nu T^mu_l
def dcoord(F,cc):
    if cc==1: return dr(F)
    if cc==2: return dth(F)
    return torch.zeros_like(F)
divT=torch.zeros(nr,nth,4)
for nu in range(4):
    s=torch.zeros(nr,nth)
    for mu in range(4):
        s=s+dcoord(Tmix[...,mu,nu],mu)
        for l in range(4):
            s=s+Gam[...,mu,mu,l]*Tmix[...,l,nu]-Gam[...,l,mu,nu]*Tmix[...,mu,l]
    divT[...,nu]=s
REL=matter_el_t(G,Th,a,b,c,d)
body=(G.R>0.8)&(G.R<G.ri-0.8)
print("ROUND soliton on 2D grid (committed stress + committed EL), body max-abs:")
print(f"  committed matter EL (matter_el_t)     : {float(REL[body].abs().max()):.3e}")
print(f"  div_mu T^mu_r  (committed stress)      : {float(divT[...,1][body].abs().max()):.3e}")
print(f"  div_mu T^mu_theta (committed stress)   : {float(divT[...,2][body].abs().max()):.3e}")
# relationship: EL should be proportional to divT_r. ratio in body:
rr=(REL[body]/ (divT[...,1][body]+1e-30))
print(f"  ratio EL/divT_r  (body): mean={float(rr.mean()):.4f} std={float(rr.std()):.4f}")
