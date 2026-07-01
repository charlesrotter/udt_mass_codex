#!/usr/bin/env python3
"""Probe radial_Bfree residuals: WHERE do they live, did the SCF converge,
   and do they fall with N in the deep interior (excluding the inner few cells)?"""
import os
os.environ["CUDA_VISIBLE_DEVICES"] = ""
os.environ.setdefault("PYTORCH_NVML_BASED_CUDA_CHECK", "0")
import math, numpy as np, torch
torch.set_default_dtype(torch.float64)
import importlib.util
def load(m,p):
    s=importlib.util.spec_from_file_location(m,p); mod=importlib.util.module_from_spec(s)
    s.loader.exec_module(mod); return mod
rbf = load("rbf","/home/udt-admin/udt_mass_codex/radial_Bfree_soliton.py")

xi=kap=1.0; rc=0.05; ri=rc+14.0
for N in (400,800,1600):
    rgr = rbf.make_grid(1,N,rc=rc,rint=ri,geom=False,device="cpu")
    out = rbf.selfconsistent_Bfree(rgr,xi,kap,p=0.4,kap8=0.05,iters=400,relax=0.4,
                                   tol=1e-12,verbose=False)
    res=out['res']; r=out['r'][0].numpy()
    rtt=res['res_tt'][0].abs().numpy(); rrr=res['res_rr'][0].abs().numpy(); rth=res['res_thth'][0].abs().numpy()
    # SCF convergence: last hist entry deltas
    h=out['hist'][-1]
    it,db,da,dT,resth = h
    # locate worst point of res_rr
    iworst=int(np.argmax(rrr))
    # residual maxima excluding inner 5% and outer 2 cells
    lo=max(2,int(0.05*N)); hi=N-2
    print(f"N={N}: SCF last it={it} db={db:.1e} da={da:.1e} dT={dT:.1e}")
    print(f"   full-interior max res (tt,rr,thth)=({rtt[2:-2].max():.2e},{rrr[2:-2].max():.2e},{rth[2:-2].max():.2e})")
    print(f"   worst res_rr at r={r[iworst]:.3f} (index {iworst}/{N})  value={rrr[iworst]:.2e}")
    print(f"   deep-interior [{lo}:{hi}] max res (tt,rr,thth)=({rtt[lo:hi].max():.2e},{rrr[lo:hi].max():.2e},{rth[lo:hi].max():.2e})")
    # residual at a FIXED physical radius (r~2.0) across N for O(h^2) test
    j=int(np.argmin(np.abs(r-2.0)))
    print(f"   at r~2.0 (idx {j}): res_tt={rtt[j]:.3e} res_rr={rrr[j]:.3e} res_thth={rth[j]:.3e}")
    # max over r>1 (well away from core singular amplification)
    mask = r>1.0
    print(f"   for r>1.0: max res (tt,rr,thth)=({rtt[mask].max():.2e},{rrr[mask].max():.2e},{rth[mask].max():.2e})")
    print()
