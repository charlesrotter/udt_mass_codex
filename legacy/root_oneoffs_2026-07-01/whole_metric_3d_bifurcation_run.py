#!/usr/bin/env python3
"""Run the bifurcation test: sigma_min of the field-equation Jacobian J around the #56
round soliton, matter sub-block (validate vs radial ~0.11) then off-diagonal metric
sector (the new unreduced DOF). Dense J^T J on a small genuinely-3D grid for exact
sigma_min. Driver: Claude (Opus 4.8, 1M). 2026-06-15. DATA-BLIND."""
import os
os.environ.setdefault("PYTORCH_NVML_BASED_CUDA_CHECK", "0")
import math, time
import torch
import whole_metric_3d_core as core
import whole_metric_3d_matter as mat
import whole_metric_3d_solver as S
import whole_metric_3d_newton as NW
import whole_metric_3d_bifurcation as BF
import radial_Bfree_soliton as rb

torch.set_default_dtype(torch.float64)
DEV=S.DEV; T,R,TH,PS=0,1,2,3
def hdr(s): print("\n"+"="*78); print(s); print("="*78, flush=True)

xi=kap=1.0; rc=0.05; SPAN=14.0; ri=rc+SPAN; KAP8=0.05; th0,th1=0.30,math.pi-0.30

def build_round(G,a_r,b_r,Th_r):
    Nr,Nth,Nps=G['Nr'],G['Nth'],G['Nps']
    g=torch.zeros(Nr,Nth,Nps,4,4,device=DEV)
    g[...,T,T]=-torch.exp(2*a_r[:,None,None].expand(Nr,Nth,Nps))
    g[...,R,R]=torch.exp(2*b_r[:,None,None].expand(Nr,Nth,Nps))
    g[...,TH,TH]=G['Rr']**2
    g[...,PS,PS]=(G['Rr']*torch.sin(G['Tht']))**2
    Thf=Th_r[:,None,None].expand(Nr,Nth,Nps).contiguous()
    return g,Thf

def dense_JTJ_smallest(F, u0, k=8):
    """Form J^T J densely (apply to each basis vector) -> exact smallest singular vals.
    Only for small DOF count."""
    n=u0.numel()
    u0=u0.detach()
    def Jv(v):
        _,jv=torch.autograd.functional.jvp(F,(u0,),(v,),strict=False); return jv
    # build J densely: columns J@e_i
    cols=[]
    I=torch.eye(n,device=DEV)
    for i in range(n):
        cols.append(Jv(I[i]))
    J=torch.stack(cols,dim=1)   # (m, n)
    JTJ=J.T@J
    ev=torch.linalg.eigvalsh(JTJ).clamp(min=0)
    sig=ev.sqrt()
    return sig, J

# SMALL genuinely-3D grid so J^T J is dense-tractable.
Nr=40; Nth=14; Nps=6
G=S.mkgrid(Nr,Nth,Nps,rc,ri,th0,th1)
bmask=BF.__dict__  # placeholder

# free DOF only in a SMALL body window (keeps J dense-tractable while genuinely 3-D)
def windowed_mask(G, comps, ri_lo, ri_hi):
    m=NW.make_freemask(G,comps,rcore_freeze=1.0)
    rok=(G['rg']>=ri_lo)&(G['rg']<=ri_hi)
    keep=torch.zeros(G['Nr'],dtype=torch.bool,device=DEV); keep[rok]=True
    m[~keep,:,:,:]=False
    return m

hdr("BIFURCATION sigma_min(J) -- MATTER sub-block (validate vs radial ~0.11)")
print("free Th only, in a body window; J = d(field eqs)/dTh.  sigma_min bounded from 0")
print("= no bifurcation (matches verified radial min|eig|~0.11, order-of-magnitude).")
for P in [0.2,0.4,0.7,1.0]:
    rN=rb.make_grid(1,Nr,rc=rc,rint=ri,geom=False)
    o=rb.selfconsistent_Bfree(rN,xi,kap,p=P,kap8=KAP8,iters=300,relax=0.4,tol=1e-11,verbose=False)
    a_r,b_r,Th_r=o['a'][0],o['b'][0],o['Th'][0]
    g0,Th0=build_round(G,a_r,b_r,Th_r)
    mask_g=NW.make_freemask(G,[],rcore_freeze=1.0)   # no metric free
    # Th free in a body window (proper spatial mask, theta interior, all psi)
    mask_th=torch.zeros(G['Nr'],G['Nth'],G['Nps'],dtype=torch.bool,device=DEV)
    rok=(G['rg']>=rc+2.0)&(G['rg']<=rc+6.0)
    mask_th[rok,2:-2,:]=True
    eqmask=mask_g.clone()
    wgeom=NW.geom_weight(G)
    F,ng=BF.build_residual_fn(g0,Th0,KAP8,G,mask_g,mask_th,eqmask,wgeom)
    u0=torch.cat([NW.x_from_g(g0,mask_g), Th0[mask_th]])
    sig,_=dense_JTJ_smallest(F,u0)
    sn=sig.cpu().numpy()
    print(f"  p={P}: DOF={u0.numel()}  sigma_min={sn.min():.4e}  sigma_max={sn.max():.4e}  (cond {sn.max()/max(sn.min(),1e-30):.1e})")

hdr("BIFURCATION sigma_min(J) -- OFF-DIAGONAL metric sector (the NEW unreduced DOF)")
print("free ALL 6 off-diagonals (g_tr,g_ttheta,g_tpsi,g_rtheta,g_rpsi,g_thetapsi) in a")
print("body window; J = d(Einstein eqs)/d(off-diag).  sigma_min->0 with localized mode")
print("= a shaped/twisted type BIFURCATES off the round soliton.  bounded from 0 = none.")
offdiag=[(0,1),(0,2),(0,3),(1,2),(1,3),(2,3)]
for P in [0.2,0.4,0.7,1.0]:
    rN=rb.make_grid(1,Nr,rc=rc,rint=ri,geom=False)
    o=rb.selfconsistent_Bfree(rN,xi,kap,p=P,kap8=KAP8,iters=300,relax=0.4,tol=1e-11,verbose=False)
    a_r,b_r,Th_r=o['a'][0],o['b'][0],o['Th'][0]
    g0,Th0=build_round(G,a_r,b_r,Th_r)
    mask_g=windowed_mask(G,offdiag,rc+2.0,rc+6.0)
    mask_th=torch.zeros(G['Nr'],G['Nth'],G['Nps'],dtype=torch.bool,device=DEV)
    eqmask=mask_g.clone()
    wgeom=NW.geom_weight(G)
    F,ng=BF.build_residual_fn(g0,Th0,KAP8,G,mask_g,mask_th,eqmask,wgeom)
    u0=NW.x_from_g(g0,mask_g)
    t0=time.time()
    sig,J=dense_JTJ_smallest(F,u0)
    sn=sig.cpu().numpy()
    print(f"  p={P}: DOF={u0.numel()}  sigma_min={sn.min():.4e}  sigma_max={sn.max():.4e}  "
          f"#(sigma<1e-6)={int((sn<1e-6).sum())}  ({time.time()-t0:.1f}s)")
print("\n  (#(sigma<1e-6) counts near-null directions; a physical bifurcation shows a")
print("   localized null mode -- gauge/frozen-window artifacts excluded by construction.)")
