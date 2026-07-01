#!/usr/bin/env python3
"""Validate the Newton 3-D solver: STAY at #56, RELAX-BACK from a perturbation.
Driver: Claude (Opus 4.8, 1M). 2026-06-15. DATA-BLIND."""
import os
os.environ.setdefault("PYTORCH_NVML_BASED_CUDA_CHECK", "0")
import math, time
import torch
import whole_metric_3d_core as core
import whole_metric_3d_matter as mat
import whole_metric_3d_solver as S
import whole_metric_3d_newton as NW
import radial_Bfree_soliton as rb

torch.set_default_dtype(torch.float64)
DEV = S.DEV
T, R, TH, PS = 0, 1, 2, 3
def hdr(s): print("\n"+"="*78); print(s); print("="*78, flush=True)

xi=kap=1.0; rc=0.05; SPAN=14.0; ri=rc+SPAN; P=0.4; KAP8=0.05
th0,th1=0.30,math.pi-0.30

def build_round(G,a_r,b_r,Th_r):
    Nr,Nth,Nps=G['Nr'],G['Nth'],G['Nps']
    g=torch.zeros(Nr,Nth,Nps,4,4,device=DEV)
    g[...,T,T]=-torch.exp(2*a_r[:,None,None].expand(Nr,Nth,Nps))
    g[...,R,R]=torch.exp(2*b_r[:,None,None].expand(Nr,Nth,Nps))
    g[...,TH,TH]=G['Rr']**2
    g[...,PS,PS]=(G['Rr']*torch.sin(G['Tht']))**2
    Thf=Th_r[:,None,None].expand(Nr,Nth,Nps).contiguous()
    return g,Thf

# small genuinely-3D grid for the capability proof
Nr=120
G=S.mkgrid(Nr,40,12,rc,ri,th0,th1)
rN=rb.make_grid(1,Nr,rc=rc,rint=ri,geom=False)
oN=rb.selfconsistent_Bfree(rN,xi,kap,p=P,kap8=KAP8,iters=300,relax=0.4,tol=1e-11,verbose=False)
a_r,b_r,Th_r=oN['a'][0],oN['b'][0],oN['Th'][0]
g0,Th0=build_round(G,a_r,b_r,Th_r)
M_ref=oN['M_MS'].item()
print(f"#56 seed on Nr={Nr}: M_MS={M_ref:.6f}")

# free the diagonal warps (g_tt,g_rr) + the two angular metric comps + ALL off-diagonals
free=[(0,0),(1,1),(2,2),(3,3),(0,1),(0,2),(0,3),(1,2),(1,3),(2,3)]

hdr("STAY -- Newton seeded at #56 (should keep |F| small, no drift)")
t0=time.time()
out=NW.solve(g0,Th0,KAP8,G,free,bc_core=math.pi,bc_seal=0.0,
             outer=8,lam=0.6,mu=1e-6,cg_iters=20,mask_core=1.0,
             matter_steps=4,matter_lr=0.1,verbose=True,tag="STAY")
print(f"  elapsed {time.time()-t0:.1f}s")

hdr("RELAX-BACK -- perturb g_rr bump + inject un-sourced g_ttheta, Newton-relax")
g_p=g0.clone()
bump=0.04*torch.exp(-((G['rg']-(rc+3.0))**2/0.5))[:,None,None].expand_as(g0[...,R,R])
g_p[...,R,R]=g0[...,R,R]*(1.0+bump)
inj=0.02*torch.sin(G['Tht'])*torch.exp(-((G['rg'][:,None,None]-(rc+3.0))**2/0.5))
g_p[...,T,TH]=inj; g_p[...,TH,T]=inj
n0=mat.hedgehog_n(Th0,G['Tht'],G['Ps'])
Res0=NW.residual_of_g(g_p,n0,KAP8,G)
i0,i1=int(0.1*Nr),int(0.9*Nr)
r0=max(Res0[i0:i1,8:-8,:][...,a,a].abs().max().item() for a in range(4))
print(f"  perturbed: body diag res={r0:.3e}, injected g_ttheta={g_p[...,T,TH].abs().max().item():.3e}")
t0=time.time()
out2=NW.solve(g_p,Th0,KAP8,G,free,bc_core=math.pi,bc_seal=0.0,
              outer=15,lam=0.6,mu=1e-6,cg_iters=20,mask_core=1.0,
              matter_steps=4,matter_lr=0.1,verbose=True,tag="BACK")
print(f"  elapsed {time.time()-t0:.1f}s")
g2=out2['g']
print(f"  surviving g_ttheta max(body)={g2[i0:i1,8:-8,:][...,T,TH].abs().max().item():.3e} (injected 0.02)")
b2=-0.5*torch.log(g2[...,R,R].clamp(min=1e-30))
m2=G['rg']*(1.0-torch.exp(-2*b2[:,G['Nth']//2,0]))
print(f"  M_MS recovered={ (m2[-1]-m2[0]).item():.6f}  ref={M_ref:.6f}")
