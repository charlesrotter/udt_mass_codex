#!/usr/bin/env python3
"""CLAIMS 2,4,5: run the solver, check M_MS = INT kap8 r^2 rho dr, rho>=0,
R-stability (claim4), and ride-on-p/kap8/scaling (claim5). INDEPENDENT integration
of the source via my own trapezoid, and independent m_core cancellation check."""
import os
os.environ.setdefault("PYTORCH_NVML_BASED_CUDA_CHECK","0")
import math, torch
torch.set_default_dtype(torch.float64)
from radial_Bfree_soliton import selfconsistent_Bfree, make_grid

DEV="cuda" if torch.cuda.is_available() else "cpu"

def run(p, kap8, xi, kap, Rcell, N):
    L=math.sqrt(kap/xi); rc=0.05; ri=rc+Rcell*L
    r=make_grid(1,N,rc=rc,rint=ri,geom=False)
    out=selfconsistent_Bfree(r,xi,kap,p=p,kap8=kap8,iters=400,relax=0.4,tol=1e-11)
    return out

def indep_source(out, kap8):
    """independent trapezoid of kap8 r^2 rho dr over solved profile."""
    r=out['r'][0]; rho=out['rho'][0]
    integ=kap8*r**2*rho
    dr=r[1:]-r[:-1]
    return torch.sum(0.5*(integ[1:]+integ[:-1])*dr).item()

print("="*70)
print("CLAIM 2: M_MS == INT kap8 r^2 rho dr, rho>=0, m_core cancels")
out=run(0.4,0.05,1.0,1.0,14.0,1200)
M=out['M_MS'].item()
Msrc=indep_source(out,0.05)
rho=out['rho'][0]
print(f" M_MS (solver read-off) = {M:.6f}")
print(f" INT kap8 r^2 rho dr (my trapezoid) = {Msrc:.6f}")
print(f" abs diff = {abs(M-Msrc):.3e}  rel = {abs(M-Msrc)/abs(M):.3e}")
print(f" min rho = {rho.min().item():.3e}  (>=0 ?)  max rho = {rho.max().item():.3e}")
# m_core cancellation: M_MS = m_areal[seal]-m_areal[core]; m_core appears in BOTH -> cancels
ma=out['m_areal'][0]
print(f" m_areal[core]={ma[0].item():.4f} m_areal[seal]={ma[-1].item():.4f} diff={ma[-1].item()-ma[0].item():.6f}")
# vary p: m_core changes, M_MS = diff should be p-independent ONLY if rho independent of p.
# check directly:
for p in [0.1,0.8]:
    o2=run(p,0.05,1.0,1.0,14.0,1200)
    print(f"   p={p}: m_core(={0.05*(1-math.exp(2*p)):.4f}) M_MS={o2['M_MS'].item():.6f} src={indep_source(o2,0.05):.6f}")

print("="*70)
print("CLAIM 4: R-stability (cell 8,20,80 L) -- box control gate")
for R in [8.0,20.0,80.0]:
    N=int(1200*max(1,R/14.0))  # keep resolution roughly fixed
    o=run(0.4,0.05,1.0,1.0,R,N)
    print(f"  R={R:>4} L  N={N:>5}  M_MS={o['M_MS'].item():.6f}  src={indep_source(o,0.05):.6f}")

print("="*70)
print("CLAIM 5: ride on p, kap8; scale ~ sqrt(kap/xi)")
print(" -- vary p (kap8=0.05):")
for p in [0.1,0.4,0.8]:
    o=run(p,0.05,1.0,1.0,14.0,1200); print(f"    p={p}: M_MS={o['M_MS'].item():.6f}")
print(" -- vary kap8 (p=0.4):")
for k8 in [0.02,0.05,0.1]:
    o=run(0.4,k8,1.0,1.0,14.0,1200); print(f"    kap8={k8}: M_MS={o['M_MS'].item():.6f}")
print(" -- vary kappa (p=0.4,kap8=0.05) [L=sqrt(kap/xi), expect M~sqrt(kap)]:")
for kp in [0.25,1.0,4.0]:
    L=math.sqrt(kp/1.0)
    o=run(0.4,0.05,1.0,kp,14.0,1200)
    M=o['M_MS'].item()
    print(f"    kappa={kp}: L={L:.3f} M_MS={M:.6f} M/sqrt(kap)={M/math.sqrt(kp):.6f}")
