#!/usr/bin/env python3
"""GATE C for P5a' (re-pose + JFNK): beat the #60 axisym-l2 stall to floor.
Branch p5a-prime-repose.  Driver: Claude Opus 4.8.  2026-06-20.  DATA-BLIND.  NEW FILE.

The #60 case: axisym-l2 control seed (a KNOWN relax-to-round case) where the
matrix-free Jacobi-PCG LM stalled ~1e-5.  PASS = re-posed JFNK drives committed Phi
to floor (<=~1e-9) where the old solver stalled.  We hold the edge gauge at the
axisym-l2 seed's OWN edges (a smooth/regular gauge consistent with the seed), then
JFNK the body DOF.  We also run the full-space dense anchor on the same seed for the
target, and (for context) the OLD matrix-free Jacobi-PCG control.
"""
import os, time, math
os.environ.setdefault("PYTORCH_NVML_BASED_CUDA_CHECK","0")
os.environ.setdefault("PYTORCH_NO_CUDA_MEMORY_CACHING","1")
import numpy as np, torch
torch.set_default_dtype(torch.float64)
from full3d_spectral import Grid3D, attach_coord_weight, residuals, diagnostics
from full3d_solver import residual_vector, round_seed, unpack, lm_solve
import full3d_newton as NW
import p5a_prime_repose as RP

NR,NTH,NPS = 12,6,8
P,KAP8 = 0.4,0.05
G = Grid3D(NR,NTH,NPS,rc=0.05,cell=14.0); G=attach_coord_weight(G)
u0,sol = round_seed(G,p=P,kap8=KAP8)
Nr=G.Nr

def phys(u,tag):
    F=residual_vector(u,G,P,KAP8); Phi=float((F*F).sum())
    out=residuals(G,unpack(u,G),P,KAP8); d=diagnostics(G,out,KAP8)
    print(f"  [{tag}] committed-Phi={Phi:.3e} M_MS={d['M_MS']:.6f} tvar={d['tvar']:.4e} psivar={d['psivar']:.4e}",flush=True)
    return Phi,d

# the #60 stall seed
useed = RP.axi_l2_seed(G,u0,amp=0.25,m=1)
print("=== #60 axisym-l2 SEED ===",flush=True); phys(useed,"seed")

# OLD matrix-free Jacobi-PCG control (the documented #60 stall)
print("=== #60 control: matrix-free Jacobi-PCG LM (full3d_solver.lm_solve) ===",flush=True)
t=time.time()
uc,hc = lm_solve(useed,G,P,KAP8,maxit=40,lam0=1e-3,verbose=True,tol=1e-11)
print(f"  control final committed-Phi={hc[-1]:.3e} iters={len(hc)-1} time={time.time()-t:.0f}s",flush=True)
phys(uc,"control")

# full-space dense anchor target on the same seed
print("=== anchor target on the #60 seed ===",flush=True)
t=time.time()
ua,ha=NW.newton_solve(useed,G,P,KAP8,maxit=30,lam0=1e-4,tol=1e-12,verbose=False)
print(f"  anchor committed-Phi={ha[-1]:.3e} iters={len(ha)-1} time={time.time()-t:.0f}s",flush=True)
_,da=phys(ua,"anchor")

# RE-POSED JFNK on the #60 seed (hold gauge = seed edges)
print("=== GATE C: re-posed JFNK on the #60 seed ===",flush=True)
rp=RP.Repose(G,p=P,m=1,edge_mode='hold',fit_deg=4); rp.set_edge_hold(useed)
ub0=rp.extract(useed)
t=time.time()
ubj,hj,its,wt=RP.reposed_jfnk_solve(ub0,rp,useed,KAP8,maxit=60,lam0=1e-4,tol=1e-12,
                                    pc='none',lsmr_maxit=1000,lsmr_tol=1e-12,verbose=True)
print(f"  GATE C JFNK reposed-Phi={hj[-1]:.3e} newton_iters={len(hj)-1} lsmr_avg={np.mean(its) if its else 0:.0f} time={wt:.0f}s",flush=True)
print(f"  residual history: {['%.2e'%x for x in hj]}",flush=True)
phys(rp.embed_vsafe(ubj),"GATE-C-JFNK->committed")
print(f"  PASS criterion: committed-Phi <= ~1e-9 where Jacobi stalled ~1e-5 -> {'PASS' if hj[-1]<=1e-9 else 'FAIL/PARTIAL'}",flush=True)
torch.save({'ubj':ubj.cpu(),'seed':useed.cpu(),'ua':ua.cpu()},'/tmp/repose_gateC.pt')
print("=== GATE C DONE ===",flush=True)
