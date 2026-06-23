import os,sys,math
os.environ.setdefault("PYTORCH_NVML_BASED_CUDA_CHECK","0")
import numpy as np, torch
torch.set_default_dtype(torch.float64)
sys.path.insert(0,"/home/udt-admin/udt_mass_codex"); sys.path.insert(0,"/tmp")
import whole_metric_3d_core as CORE, whole_metric_3d_matter as MAT
from full3d_spectral import Grid3D, attach_coord_weight, build_metric, DEV
import free_s2_matter as FS
import b1prime_round as RAD
PI=math.pi; X,XI,KAP,KAP8=-2e5,2e-2,2e-2,1.0
Nr=16
RG=RAD.RGrid(Nr,rc=0.05,cell=14.0)
u,Phi=RAD.solve(RG,X,XI,KAP,1.0,KAP8,m=1,maxit=120,verbose=False)
dgd=RAD.diag(RG,u,X,XI,KAP)
G=Grid3D(Nr=Nr,Nth=8,Nps=8,rc=0.05,cell=14.0); G=attach_coord_weight(G)
def lift(arr):
    t=torch.tensor(arr,device=DEV); return t[:,None,None].expand(G.Nr,G.Nth,G.Nps).contiguous()
a=lift(dgd['a']);b=lift(dgd['b']);c=torch.zeros_like(a);d=torch.zeros_like(a);phi=lift(dgd['ph'])
rc,ri=float(G.r[0]),float(G.r[-1])
rfac=torch.sin(PI*(G.Rg-rc)/(ri-rc))
g=build_metric(G,a,b,c,d); ginv=CORE.metric_inverse(g)
f=torch.exp(2*phi); sqrtg=torch.sqrt(torch.clamp(-torch.linalg.det(g),min=1e-300))
w=G.wvol_coord; mask=G.body.double()
# matter-ONLY action vs twist amplitude beta (no shear) -- isolate the twist direction.
print("beta   S_matter(matter only INT sqrt-g f L_m, body)    L2part      L4part")
for be in [-0.02,-0.01,0.0,0.01,0.02]:
    dn=FS.field_dn_freeaz(G, be*rfac, m=1)
    Gmn=MAT.field_metric(dn)
    Lm,L2,L4,_=MAT.lagrangian(ginv,Gmn,XI,KAP)
    Sm=(sqrtg*f*Lm*w*mask).sum().item()
    S2=(sqrtg*f*L2*w*mask).sum().item()
    S4=(sqrtg*f*L4*w*mask).sum().item()
    print("%+.3f   %.8e    %.4e  %.4e"%(be,Sm,S2,S4))
# Is twist beta a flat Goldstone? d/dbeta at 0 should be ~0 (it is a stationary defect).
# Curvature: matter L2 = -(xi/2) g^{mn}G_mn; G_rr = sth^2 (g')^2 with g'=be*rfac'.
# So twist ADDS positive G_rr -> g^{rr}G_rr>0 -> L2 MORE NEGATIVE -> S_matter DECREASES.
# That is the sign: action decreases. But the ENERGY (rho=-T^t_t) test:
dn0=FS.field_dn_freeaz(G, 0.0*rfac, m=1)
Tab0,*_=MAT.stress_tensor(g,ginv,dn0,XI,KAP); Tm0=torch.einsum('...ma,...an->...mn',ginv,Tab0)
print("\nENERGY (proper, rho=-T^t_t integrated over body proper volume):")
print("beta    M_energy = INT rho sqrt(g3) dV (body)   ")
g3=g[...,1:,1:]  # spatial 3-metric
sqrtg3=torch.sqrt(torch.clamp(torch.linalg.det(g3),min=1e-300))
for be in [-0.02,-0.01,0.0,0.01,0.02]:
    dn=FS.field_dn_freeaz(G, be*rfac, m=1)
    Tab,*_=MAT.stress_tensor(g,ginv,dn,XI,KAP); Tm=torch.einsum('...ma,...an->...mn',ginv,Tab)
    rho=-Tm[...,0,0]
    Mn=(rho*f*sqrtg3*w*mask).sum().item()
    print("%+.3f    %.8e"%(be,Mn))
