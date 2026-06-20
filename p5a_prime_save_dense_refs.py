#!/usr/bin/env python3
"""Stage 1: compute + save the reposed DENSE reference fixed points (needs jacrev =>
no-cache allocator).  Branch p5a-prime-repose.  Driver: Claude Opus 4.8.  2026-06-20.
Saves /tmp/dense_refs.pt with the round (G1 round-seed edge gauge) reposed-dense fixed
point ubd1 + the full-space anchor, for the fast JFNK harness to compare against."""
import os
os.environ.setdefault("PYTORCH_NVML_BASED_CUDA_CHECK","0")
os.environ.setdefault("PYTORCH_NO_CUDA_MEMORY_CACHING","1")   # set BEFORE importing RP
import torch
import sys; sys.path.insert(0,'/home/udt-admin/udt_mass_codex')
torch.set_default_dtype(torch.float64)
from full3d_spectral import Grid3D, attach_coord_weight
from full3d_solver import round_seed
import full3d_newton as NW
import p5a_prime_repose as RP

G=Grid3D(12,6,8,rc=0.05,cell=14.0); G=attach_coord_weight(G)
u0,sol=round_seed(G,p=0.4,kap8=0.05)
ua,ha=NW.newton_solve(u0,G,0.4,0.05,maxit=30,lam0=1e-4,tol=1e-12,verbose=False)
print("anchor Phi",ha[-1],flush=True)
rp=RP.Repose(G,p=0.4,m=1,edge_mode='hold',fit_deg=4); rp.set_edge_hold(u0); ub0=rp.extract(u0)
ubd,hd=RP.reposed_dense_solve_fast(ub0,rp,0.05,maxit=30,lam0=1e-4,tol=1e-13,verbose=False)
print("hold-dense G1 reposed-Phi",hd[-1],flush=True)
torch.save({'ubd1':ubd.cpu(),'ua':ua.cpu(),'u0':u0.cpu()},'/tmp/dense_refs.pt')
print("SAVED dense refs",flush=True)
