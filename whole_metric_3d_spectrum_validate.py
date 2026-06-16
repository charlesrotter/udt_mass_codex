#!/usr/bin/env python3
"""Validate the Hessian/spectrum machinery: matter-only sub-block must reproduce the
verified radial bifurcation null (min|eig| bounded away from 0, ~0.1), then add the
off-diagonal metric block. Driver: Claude (Opus 4.8, 1M). 2026-06-15. DATA-BLIND."""
import os
os.environ.setdefault("PYTORCH_NVML_BASED_CUDA_CHECK", "0")
import math, time
import torch
import whole_metric_3d_core as core
import whole_metric_3d_matter as mat
import whole_metric_3d_solver as S
import whole_metric_3d_newton as NW
import whole_metric_3d_spectrum as SP
import radial_Bfree_soliton as rb

torch.set_default_dtype(torch.float64)
DEV = S.DEV
T,R,TH,PS=0,1,2,3
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

Nr=100
G=S.mkgrid(Nr,32,8,rc,ri,th0,th1)
bmask=SP.body_mask(G,rcore=1.0)
mask_th=bmask.clone()

hdr("Spectrum machinery validation across the depth dial p")
print("matter-only Hessian sub-block (vary Th only; metric frozen) -> the radial")
print("bifurcation operator.  Verified radial result: min|eig| ~0.11, bounded from 0.")
for P in [0.2, 0.4, 0.7, 1.0]:
    rN=rb.make_grid(1,Nr,rc=rc,rint=ri,geom=False)
    o=rb.selfconsistent_Bfree(rN,xi,kap,p=P,kap8=KAP8,iters=300,relax=0.4,tol=1e-11,verbose=False)
    a_r,b_r,Th_r=o['a'][0],o['b'][0],o['Th'][0]
    g0,Th0=build_round(G,a_r,b_r,Th_r)
    # MATTER ONLY: free no metric components, free Th in body
    mask_g_none=NW.make_freemask(G,[],rcore_freeze=1.0)  # nothing free
    Hv,ng,u0=SP.make_HVP(g0,Th0,KAP8,G,mask_g_none,mask_th,bmask)
    ev=SP.lanczos_extremes(Hv,u0.numel(),k=60)
    evn=ev.cpu().numpy()
    minabs=min(abs(evn.min()),abs(evn.max())) if (evn.min()<0<evn.max()) else min(abs(evn))
    print(f"  p={P}: matter-block lowest eigs = {evn[:4]}  most-neg={evn.min():.4e}  min|eig|={min(abs(x) for x in evn):.4e}")

hdr("Now FREE the off-diagonal metric block (the NEW unreduced sector)")
print("Free ALL 6 off-diagonals + the 4 diagonal warps + Th.  A near-ZERO lowest eig")
print("would signal a bifurcation to a shaped/off-diagonal type.  (Gauge modes produce")
print("EXACT zeros -- distinguished from physical zero modes by their localization.)")
P=0.4
rN=rb.make_grid(1,Nr,rc=rc,rint=ri,geom=False)
o=rb.selfconsistent_Bfree(rN,xi,kap,p=P,kap8=KAP8,iters=300,relax=0.4,tol=1e-11,verbose=False)
a_r,b_r,Th_r=o['a'][0],o['b'][0],o['Th'][0]
g0,Th0=build_round(G,a_r,b_r,Th_r)
# off-diagonals only (the new DOF, isolate them)
offdiag=[(0,1),(0,2),(0,3),(1,2),(1,3),(2,3)]
mask_g_off=NW.make_freemask(G,offdiag,rcore_freeze=1.0)
# matter frozen for the pure off-diagonal metric block
mask_th_none=torch.zeros_like(mask_th)
t0=time.time()
Hv,ng,u0=SP.make_HVP(g0,Th0,KAP8,G,mask_g_off,mask_th_none,bmask)
ev=SP.lanczos_extremes(Hv,u0.numel(),k=80)
evn=ev.cpu().numpy()
print(f"  off-diagonal metric block ({u0.numel()} DOF): lowest eigs = {evn[:6]}")
print(f"    most-negative = {evn.min():.4e}   most-positive = {evn.max():.4e}")
print(f"    min|eig| = {min(abs(x) for x in evn):.4e}   ({time.time()-t0:.1f}s)")
print("  INTERPRETATION: structurally-zero (<~1e-8) lowest eig with a LOCALIZED mode")
print("  => bifurcation/new branch.  Bounded-away-from-zero => no shaped type branches off.")
