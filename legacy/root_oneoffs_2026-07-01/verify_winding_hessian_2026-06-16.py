#!/usr/bin/env python3
"""Blind verifier: matter-sector ENERGY Hessian eigenvalues restricted to the
psi-BREAKING subspace, on the SH-EXACT grid, at the converged axisym soliton.

Energy E = -S (S = matter action, the SAME _matter_action_scalar used by the push).
We autograd the FULL Hessian of S wrt the nodal Theta field (body nodes only,
winding-BC nodes frozen), at the converged metric (fixed), then:
  - project onto the psi-breaking subspace (modes with nonzero azimuthal content),
  - report the lowest eigenvalues of the ENERGY Hessian H_E = -H_S restricted there.
A NEGATIVE eigenvalue of H_E in the psi-breaking subspace => platonic instability
=> the 'no platonic instability' claim FAILS.

Sign calibration: also report the lowest psi-breaking eigenvalue for m=1 (known-stable
hedgehog) -- it MUST be >=0 (positive) for the energy-Hessian sign convention to hold;
if m=1 itself shows a negative psi-breaking energy eigenvalue the WHOLE probe (incl. the
push's secondvar) is sign-broken.
"""
import os, sys, json, time
os.environ.setdefault("PYTORCH_NVML_BASED_CUDA_CHECK","0")
os.environ.setdefault("PYTORCH_NO_CUDA_MEMORY_CACHING","1")
import numpy as np, torch
torch.set_default_dtype(torch.float64)
sys.path.insert(0,'/home/udt-admin/udt_mass_codex')
from full3d_grid_shexact import make_grid_shexact
from full3d_spectral import build_metric, field_dn
from full3d_solver import pack, unpack
import whole_metric_3d_core as CORE
import whole_metric_3d_matter as MAT
import full3d_newton as NEW
import winding_catalog_map as WC

def S_of_Th(G,g,ginv,Th,m):
    dn=field_dn(G,Th,m=m)
    Gmn=MAT.field_metric(dn)
    L,_,_,_=MAT.lagrangian(ginv,Gmn,1.0,1.0)
    sqrtg=torch.sqrt(torch.clamp(-torch.linalg.det(g),min=1e-30))
    return (sqrtg*L*G.wvol_coord).sum()

def run(Nr,Nth,Nps,m,p=0.4,kap8=0.05,maxit=40):
    G=make_grid_shexact(Nr,Nth,Nps,rc=0.05,cell=14.0,mmax=Nps//2)
    u0,_=WC.winding_seed(G,m,p=p,kap8=kap8)
    u,hist=NEW.newton_solve(u0,G,p,kap8,m=m,maxit=maxit,tol=1e-12,verbose=False)
    a,b,c,d,Th=unpack(u,G)
    g=build_metric(G,a,b,c,d); ginv=CORE.metric_inverse(g)
    g=g.detach(); ginv=ginv.detach()
    # full Hessian of S wrt nodal Theta
    Th0=Th.detach().clone().requires_grad_(True)
    f=lambda x: S_of_Th(G,g,ginv,x,m)
    H_S = torch.autograd.functional.hessian(f, Th0)  # (Nr,Nth,Nps, Nr,Nth,Nps)
    n=G.Nr*G.Nth*G.Nps
    H_S=H_S.reshape(n,n)
    H_E=-0.5*(H_S+H_S.t())  # energy Hessian, symmetrized
    # body interior mask (exclude winding BC rows: r-core and r-seal)
    body=torch.zeros(G.Nr,G.Nth,G.Nps,dtype=torch.bool,device=H_E.device)
    body[1:-1,:,:]=True
    bidx=body.reshape(-1).nonzero().squeeze(1)
    HB=H_E[bidx][:,bidx]
    # psi-mean (axisym) projector to split subspaces: P_axisym averages over psi.
    # Build a per-node psi-breaking indicator via the discrete psi-mean operator.
    Nr,Nth,Nps=G.Nr,G.Nth,G.Nps
    # full eigen of body Hessian
    evals=torch.linalg.eigvalsh(HB).cpu().numpy()
    # restrict to psi-breaking subspace: P removes psi-mean of each (r,th) line.
    # operator on body vector: subtract psi-average. Build matrix Q (project out psi-mean).
    I=torch.eye(bidx.numel(),device=H_E.device)
    # map body index -> (ir,ith,ips)
    flat=torch.arange(Nr*Nth*Nps,device=H_E.device).reshape(Nr,Nth,Nps)
    coords=[(int((flat==fi).nonzero()[0,0]),)*0 for fi in bidx]  # placeholder
    # simpler: build psi-mean projector directly on body grid
    Pmean=torch.zeros(bidx.numel(),bidx.numel(),device=H_E.device)
    inv_body=-torch.ones(Nr*Nth*Nps,dtype=torch.long,device=H_E.device)
    inv_body[bidx]=torch.arange(bidx.numel(),device=H_E.device)
    for ir in range(1,Nr-1):
        for ith in range(Nth):
            row_idx=[int(inv_body[int(flat[ir,ith,ips])]) for ips in range(Nps)]
            for i in row_idx:
                for j in row_idx:
                    Pmean[i,j]=1.0/Nps
    Qbreak=I-Pmean   # projector onto psi-breaking subspace
    # restricted energy Hessian on psi-breaking subspace
    Hbreak=Qbreak@HB@Qbreak
    evb=torch.linalg.eigvalsh(Hbreak).cpu().numpy()
    # drop the ~0 eigenvalues coming from the projected-out axisym directions:
    # they are exact zeros of Qbreak; sort and report the smallest NONtrivial.
    evb_sorted=np.sort(evb)
    res=dict(m=m,Nr=Nr,Nth=Nth,Nps=Nps,Phi=hist[-1],
             full_min=float(evals.min()),full_min5=[float(x) for x in np.sort(evals)[:5]],
             break_min5=[float(x) for x in evb_sorted[:5]],
             break_max=float(evb_sorted[-1]),
             n_neg_break=int((evb< -1e-8*abs(evb).max()).sum()))
    print(json.dumps(res),flush=True)
    return res

if __name__=="__main__":
    out=[]
    out.append(run(16,6,8,1))   # calibration (known stable)
    out.append(run(16,6,8,2))
    out.append(run(16,6,8,3))
    json.dump(out,open("/tmp/verify_hessian_out.json","w"),indent=1)
    print("DONE_HESSIAN",flush=True)
