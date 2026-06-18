#!/usr/bin/env python3
"""Focused box-control confirmation for T3(b) of timerow_rest_clock.
Confirms the time-row (dphi) breathing omega^2 on the REAL soliton scales as
1/R^2 (box-controlled), NOT M_MS-tied. Standalone, fast (N=400, fewer SCF iters).
Reuses the blind-verified radial_Bfree solver. Three+ cell sizes (S3 trap)."""
import os
os.environ.setdefault("PYTORCH_NVML_BASED_CUDA_CHECK", "0")
import math, numpy as np, importlib.util
spec = importlib.util.spec_from_file_location("rbf", "radial_Bfree_soliton.py")
rbf = importlib.util.module_from_spec(spec); spec.loader.exec_module(rbf)
import torch; torch.set_default_dtype(torch.float64)

def real_soliton(p, cell_in_L, N=400, rc=0.05, kap8=0.05):
    ri = rc + cell_in_L
    rg = rbf.make_grid(1, N, rc=rc, rint=ri, geom=False)
    out = rbf.selfconsistent_Bfree(rg, 1.0, 1.0, p=p, kap8=kap8, iters=80,
                                   relax=0.4, verbose=False)
    return rg[0].cpu().numpy(), out["phi"][0].cpu().numpy(), float(out["M_MS"].item())

def omega2_lowest(r_np, phi_np, lam_v=2.0, Ni=1200):
    rr = np.linspace(r_np[0], r_np[-1], Ni)
    phi = np.interp(rr, r_np, phi_np); h = rr[1]-rr[0]
    phip = np.gradient(phi, rr); phipp = np.gradient(phip, rr)
    f = np.exp(-2*phi); E0 = phipp + 2*phip/rr - 2*phip**2
    coef = rr**2*f**2; q = 4*rr**2*f**2*E0 + lam_v*f; wt = rr**2
    ch = 0.5*(coef[:-1]+coef[1:]); n = Ni-2; A = np.zeros((n,n))
    for i in range(n):
        j=i+1; A[i,i]=(ch[j-1]+ch[j])/h**2+q[j]
        if i>0: A[i,i-1]=-ch[j-1]/h**2
        if i<n-1: A[i,i+1]=-ch[j]/h**2
    S=np.diag(1/np.sqrt(wt[1:-1])); M=S@A@S; M=0.5*(M+M.T)
    mu=np.linalg.eigvalsh(M); om2=np.sort(-mu)[::-1]
    return om2[0]   # highest omega^2 (closest to a clock)

print(f"{'cell(L)':>8} {'R':>8} {'M_MS':>9} {'omega^2':>11} {'omega^2*R^2':>13}")
rows=[]
for cellL in (6.0, 8.0, 10.0, 12.0):
    r_np, phi_np, M = real_soliton(1.0, cellL)
    om2 = omega2_lowest(r_np, phi_np)
    R = r_np[-1]; rows.append((cellL,R,M,om2,om2*R**2))
    print(f"{cellL:8.1f} {R:8.3f} {M:9.4f} {om2:11.5f} {om2*R**2:13.4f}")
om2=np.array([x[3] for x in rows]); om2R2=np.array([x[4] for x in rows])
sp_a=(om2.max()-om2.min())/np.mean(np.abs(om2))
sp_b=(om2R2.max()-om2R2.min())/np.mean(np.abs(om2R2))
print(f"\nrel spread omega^2     : {sp_a:.4f}")
print(f"rel spread omega^2*R^2 : {sp_b:.4f}")
print("M_MS spread:", f"{(np.array([x[2] for x in rows]).max()-np.array([x[2] for x in rows]).min()):.5f}",
      "(M_MS nearly constant => if omega^2 varied with M_MS it would be flat)")
print("VERDICT:", "BOX-CONTROLLED (omega^2~1/R^2; omega^2*R^2 const)" if sp_b<sp_a
      else "INTRINSIC (omega^2 const)")
print("All omega^2 < 0 (relaxation, NOT a real clock)?:", bool(np.all(om2<0)))
