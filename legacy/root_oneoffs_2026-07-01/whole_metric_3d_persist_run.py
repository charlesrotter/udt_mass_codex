#!/usr/bin/env python3
"""Run the nonlinear persistence test on multiple qualitatively-different 3-D seeds.
Driver: Claude (Opus 4.8, 1M). 2026-06-15. DATA-BLIND."""
import os
os.environ.setdefault("PYTORCH_NVML_BASED_CUDA_CHECK", "0")
import math, time
import torch
import whole_metric_3d_core as core
import whole_metric_3d_matter as mat
import whole_metric_3d_solver as S
import whole_metric_3d_newton as NW
import whole_metric_3d_persist as PX
import radial_Bfree_soliton as rb
torch.set_default_dtype(torch.float64)
DEV=S.DEV; T,R,TH,PS=0,1,2,3
def hdr(s): print("\n"+"="*78); print(s); print("="*78,flush=True)
xi_=kap=1.0; rc=0.05; SPAN=14.0; ri=rc+SPAN; KAP8=0.05; th0,th1=0.30,math.pi-0.30; P=0.4

Nr=60; Nth=20; Nps=8
G=S.mkgrid(Nr,Nth,Nps,rc,ri,th0,th1)
rN=rb.make_grid(1,Nr,rc=rc,rint=ri,geom=False)
o=rb.selfconsistent_Bfree(rN,xi_,kap,p=P,kap8=KAP8,iters=120,relax=0.5,tol=1e-11,verbose=False)
a_r,b_r,Th_r=o['a'][0],o['b'][0],o['Th'][0]
g0,Th0=PX.build_round(G,a_r,b_r,Th_r)
M_ref=o['M_MS'].item()
print(f"#56 round seed Nr={Nr}: M_MS={M_ref:.6f}")
bmask,freeze=PX.body_and_freeze(G,1.0); wgeom=NW.geom_weight(G)
phi0=PX.residual_norm_full(g0.clone(),Th0.clone(),G,KAP8,bmask,wgeom).item()
print(f"round-soliton residual floor phi0={phi0:.4e}")

def gauge_inv_nonaxisym(g):
    """GAUGE-INVARIANT non-axisymmetry: psi-variation of the Ricci SCALAR (a curvature
    invariant; cannot be created by a coordinate off-diagonal).  This is the honest test
    of whether a PHYSICAL shaped/non-round structure survives."""
    Gmn,ginv,Ric,Rscal=S.full_einstein(g,G)
    body=bmask.bool()
    # std over psi of the curvature scalar, relative to its mean magnitude
    rs=Rscal
    psistd=rs.std(dim=2)
    psimean=rs.abs().mean(dim=2)+1e-12
    rel=(psistd/psimean)
    return (rel*bmask[:,:,0])[body[:,:,0]].max().item()


def report(name,out,seed_g):
    g=out['g'];
    offs={'g_tr':(T,R),'g_ttheta':(T,TH),'g_tpsi':(T,PS),'g_rtheta':(R,TH),'g_rpsi':(R,PS),'g_thetapsi':(TH,PS)}
    body=bmask.bool()
    seedoff={k:(seed_g[...,a,b]*bmask)[body].abs().max().item() for k,(a,b) in offs.items()}
    finoff={k:(g[...,a,b]*bmask)[body].abs().max().item() for k,(a,b) in offs.items()}
    gi_seed=gauge_inv_nonaxisym(seed_g)
    gi_fin=gauge_inv_nonaxisym(g)
    print(f"  [{name}] final phi={out['hist'][-1]:.4e} (floor {phi0:.2e})")
    for k in offs:
        print(f"      {k}: seed={seedoff[k]:.3e} -> final={finoff[k]:.3e}")
    print(f"      GAUGE-INVARIANT psi-asymmetry of Ricci scalar: seed={gi_seed:.3e} -> final={gi_fin:.3e}")

# ---- SEED 1: rotation -- inject finite g_tpsi (frame-dragging / angular momentum)
hdr("SEED: ROTATION (finite g_tpsi)")
g_rot=g0.clone()
prof=torch.exp(-((G['rg'][:,None,None]-(rc+3.0))**2/2.0))*torch.sin(G['Tht'])**2
g_rot[...,T,PS]+=0.1*prof; g_rot[...,PS,T]=g_rot[...,T,PS]
out1=PX.relax_descent(g0,Th0,G,KAP8,seed_g=g_rot,steps=300,lr=2e-3,tag="ROT")
report("ROT",out1,g_rot)

# ---- SEED 2: non-axisymmetric (psi-dependent) shape on g_tt and Th
hdr("SEED: NON-AXISYMMETRIC (psi-dependent lobes)")
g_lobe=g0.clone()
Th_lobe=Th0.clone()
lobe=torch.cos(2*G['Ps'])*torch.exp(-((G['rg'][:,None,None]-(rc+3.0))**2/2.0))*torch.sin(G['Tht'])
Th_lobe=Th0+0.2*lobe
out2=PX.relax_descent(g0,Th0,G,KAP8,seed_g=g_lobe,seed_Th=Th_lobe,steps=300,lr=2e-3,tag="LOBE")
report("LOBE",out2,g_lobe)

# ---- SEED 3: theta-shaped (prolate/oblate) -- m=2 polar deformation
hdr("SEED: THETA-SHAPED (prolate, P2(cos theta))")
Th_pro=Th0+0.2*(1.5*torch.cos(G['Tht'])**2-0.5)*torch.exp(-((G['rg'][:,None,None]-(rc+3.0))**2/2.0))
out3=PX.relax_descent(g0,Th0,G,KAP8,seed_Th=Th_pro,steps=300,lr=2e-3,tag="PROL")
report("PROL",out3,g0)

hdr("PERSISTENCE SUMMARY")
print("If the injected off-diagonals / non-axisymmetry DECAY toward ~0 and phi returns to")
print("the round floor => the seeds RELAX BACK to the one round soliton (no new type).")
print("If an off-diagonal / lobe SURVIVES at finite amplitude with phi at the floor =>")
print("a distinct persistent TYPE (shaped/rotating) exists.")
