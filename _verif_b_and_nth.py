#!/usr/bin/env python3
"""Reproduce b1/b2/b3 (single evals) + the Nth-shrinkage of G^r_th on a FIXED
diagonal field with a small angular variation (tests the 'e_rt is a coarse-Nth
artifact' claim).  NO solve."""
import os
os.environ.setdefault("PYTORCH_NVML_BASED_CUDA_CHECK","0")
os.environ.setdefault("PYTORCH_NO_CUDA_MEMORY_CACHING","1")
import math, numpy as np, torch
torch.set_default_dtype(torch.float64)
from full3d_spectral import (Grid3D, attach_coord_weight, build_metric,
    einstein_mixed, einstein_mixed_weyl, DEV, T,R,TH,PS)
import full3d_solver as FS
import p1_residual_general_einstein as P1

# ---- b1: zero off-diag -> hybrid==weyl exactly
G=Grid3D(24,6,8,rc=0.05,cell=14.0); G=attach_coord_weight(G)
u5,sol=FS.round_seed(G,p=0.4,kap8=0.05); a,b,c,d,Th=FS.unpack(u5,G)
z=torch.zeros_like(a)
Gh0,_=P1.einstein_general_hybrid(G,a,b,c,d,z,z,z)
Gw=einstein_mixed_weyl(G,a,b,c,d)
print(f"b1 max|G_hybrid-G_weyl| = {float((Gh0-Gw).abs().max()):.3e}  (expect 0 exactly)")

# ---- b2: theta-only e_rt warp -> G^r_th live, G^r_ps ~ 0 (selectivity)
rr=G.Rg; th=G.THg
bump=torch.exp(-((rr-(G.rc+5.0))**2)/4.0)
e_test=0.02*bump*torch.sin(th)**2
Gh,_=P1.einstein_general_hybrid(G,a,b,c,d,e_test,torch.zeros_like(e_test),torch.zeros_like(e_test))
deep=torch.zeros_like(G.body); deep[6:G.Nr-6,:,:]=True
print(f"b2 live G^r_th(deep)={float(Gh[...,R,TH][deep].abs().max()):.3e} (expect >>0)  "
      f"G^r_ps(deep)={float(Gh[...,R,PS][deep].abs().max()):.3e} (expect ~0)")

# ---- selectivity stress: turn on e_tp only -> should source G^th_ps not G^r_th
Gh2,_=P1.einstein_general_hybrid(G,a,b,c,d,torch.zeros_like(e_test),torch.zeros_like(e_test),e_test)
print(f"   e_tp-only: G^th_ps(deep)={float(Gh2[...,TH,PS][deep].abs().max()):.3e} (expect >>0)  "
      f"G^r_th(deep)={float(Gh2[...,R,TH][deep].abs().max()):.3e}")

# ---- Nth shrinkage test: PRISTINE radial seed embedded in 3D -> G^r_th should be ~0
# and stay ~0 as Nth grows (no spurious off-diag from wiring on a truly round field).
print("\nPRISTINE round radial seed, G^r_th(deep) max vs Nth (expect ~machine 0 at all Nth):")
for Nth in [6,8,12,16]:
    Gn=Grid3D(24,Nth,8,rc=0.05,cell=14.0); Gn=attach_coord_weight(Gn)
    u5n,_=FS.round_seed(Gn,p=0.4,kap8=0.05); an,bn,cn,dn,Thn=FS.unpack(u5n,Gn)
    zn=torch.zeros_like(an)
    Ghn,_=P1.einstein_general_hybrid(Gn,an,bn,cn,dn,zn,zn,zn)
    deepn=torch.zeros_like(Gn.body); deepn[6:Gn.Nr-6,:,:]=True
    print(f"  Nth={Nth:3d}: G^r_th(deep)={float(Ghn[...,R,TH][deepn].abs().max()):.3e}")

# ---- The KEY artifact test: impose a SMALL fixed angular variation on the diagonal
# fields (mimicking the coarse-Nth angular spread the doc blames) and see whether the
# resulting G^r_th (which e_rt must absorb) SHRINKS as Nth grows. If it shrinks with
# Nth it is a discretization artifact (doc's claim). If it stays ~const it is physical.
print("\nFIXED small angular bump on diagonal field b: G^r_th(deep) max vs Nth")
print("(doc claims e_rt absorbs a coarse-Nth-sourced G^r_th -> should shrink with Nth):")
for Nth in [6,8,12,16,20]:
    Gn=Grid3D(24,Nth,8,rc=0.05,cell=14.0); Gn=attach_coord_weight(Gn)
    u5n,_=FS.round_seed(Gn,p=0.4,kap8=0.05); an,bn,cn,dn,Thn=FS.unpack(u5n,Gn)
    # add a smooth, RESOLVABLE l=2 angular variation of fixed amplitude to b
    thg=Gn.THg
    pert=1e-3*(3*torch.cos(thg)**2-1)
    bn2=bn+pert
    zn=torch.zeros_like(an)
    Ghn,_=P1.einstein_general_hybrid(Gn,an,bn2,cn,dn,zn,zn,zn)
    deepn=torch.zeros_like(Gn.body); deepn[6:Gn.Nr-6,:,:]=True
    print(f"  Nth={Nth:3d}: G^r_th(deep)={float(Ghn[...,R,TH][deepn].abs().max()):.3e}")
