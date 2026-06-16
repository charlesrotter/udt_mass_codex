import os
os.environ.setdefault("PYTORCH_NVML_BASED_CUDA_CHECK","0")
import math, torch, numpy as np
torch.set_default_dtype(torch.float64)
from full3d_spectral import (Grid3D, attach_coord_weight, build_metric, matter_el_3d,
    residuals, divT_identity, DEV, PI)
import spectral_radial_soliton as SR
rc=0.05; cell=14.0; ri=rc+cell

print("=== analytic 3-D matter EL: machine-zero on round soliton? ===")
for Nr in [48,64,96]:
  sol=SR.solve(Nr-1, rc=rc, cell=cell, p=0.4, kap8=0.05, maxit=80, tol=1e-12)
  for (Nth,Nps) in [(8,8),(8,12)]:
    G=Grid3D(Nr,Nth,Nps,rc=rc,cell=cell); G=attach_coord_weight(G)
    def E(f): return torch.tensor(f,device=DEV)[:,None,None].expand(G.Nr,G.Nth,G.Nps).contiguous()
    z=torch.zeros(G.Nr,G.Nth,G.Nps,device=DEV)
    a,b,c,d,Th=E(sol['a']),E(sol['b']),z,z,E(sol['Th'])
    el=matter_el_3d(G,a,b,c,d,Th,m=1)
    body=(G.Rg>0.8)&(G.Rg<ri-0.8)
    print(f"  Nr={Nr} Nth={Nth} Nps={Nps}: max|EL| body = {float(el[body].abs().max()):.3e}")

print("\n=== div(T) identity OFF-ROUND (psi-dependent Theta) ===")
print("   nabla_mu T^mu_nu  ==  -EL * d_nu Theta  (the off-round correctness gate)")
Nr=64
sol=SR.solve(Nr-1, rc=rc, cell=cell, p=0.4, kap8=0.05, maxit=80, tol=1e-12)
G=Grid3D(Nr,10,12,rc=rc,cell=cell); G=attach_coord_weight(G)
def E(f): return torch.tensor(f,device=DEV)[:,None,None].expand(G.Nr,G.Nth,G.Nps).contiguous()
z=torch.zeros(G.Nr,G.Nth,G.Nps,device=DEV)
a,b,c,d=E(sol['a']),E(sol['b']),z,z
Th=E(sol['Th'])
rprof=torch.exp(-((G.Rg-2.0)/1.5)**2)
Th=Th + 0.20*rprof*torch.sin(G.THg)*torch.cos(G.PSg)  # genuine non-axisym lobe
Th[0]=PI; Th[-1]=0.0
out=residuals(G,(a,b,c,d,Th),0.4,0.05,m=1)
el=out['el']; divT=divT_identity(G,out)
dTh_r=G.d_r(Th); dTh_t=G.d_th(Th); dTh_p=G.d_ps(Th)
# use a DEEP body mask to avoid the core-edge divT amplification
deep=(G.Rg>1.2)&(G.Rg<11.0)
for nu,nm,dT in [(1,'r',dTh_r),(2,'th',dTh_t),(3,'ps',dTh_p)]:
    lhs=divT[...,nu]; pred=-el*dT
    err=(lhs-pred)[deep].abs().max().item(); scale=pred[deep].abs().max().item()
    rel=err/max(scale,1e-30)
    print(f"  nu={nm:3s}: max|divT-(-EL dTh)| deep={err:.3e} scale={scale:.3e} rel={rel:.2e}")
