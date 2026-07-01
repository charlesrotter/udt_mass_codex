#!/usr/bin/env python3
"""CLAIM 3: independent Einstein residual convergence.

I derive G^mu_nu for ds^2=-e^{2a}dt^2+e^{2b}dr^2+r^2 dOmega^2 SYMBOLICALLY from
Christoffels (full Riemann->Ricci->Einstein), confirm it matches the formulas the
solver uses, then compute residuals at N=800,1600,3200 with my OWN central-difference
derivatives. Validate engine on Schwarzschild (res->0) and flat (exactly 0).
"""
import os
os.environ.setdefault("PYTORCH_NVML_BASED_CUDA_CHECK","0")
import math, torch, sympy as sp
torch.set_default_dtype(torch.float64)
from radial_Bfree_soliton import selfconsistent_Bfree, make_grid, stress

# ---- 1. Independent symbolic Einstein tensor from Christoffels ----
t,r,th,ph=sp.symbols('t r theta phi')
a=sp.Function('a')(r); b=sp.Function('b')(r)
coords=[t,r,th,ph]
g=sp.diag(-sp.exp(2*a),sp.exp(2*b),r**2,r**2*sp.sin(th)**2)
gi=g.inv()
n=4
# Christoffel
Gamma=[[[0]*n for _ in range(n)] for _ in range(n)]
for l in range(n):
    for i in range(n):
        for j in range(n):
            s=0
            for m in range(n):
                s+=gi[l,m]*(sp.diff(g[m,i],coords[j])+sp.diff(g[m,j],coords[i])-sp.diff(g[i,j],coords[m]))
            Gamma[l][i][j]=sp.simplify(s/2)
# Ricci
Ric=sp.zeros(n,n)
for i in range(n):
    for j in range(n):
        s=0
        for l in range(n):
            s+=sp.diff(Gamma[l][i][j],coords[l])-sp.diff(Gamma[l][i][l],coords[j])
            for m in range(n):
                s+=Gamma[l][l][m]*Gamma[m][i][j]-Gamma[l][j][m]*Gamma[m][i][l]
        Ric[i,j]=sp.simplify(s)
Rs=sp.simplify(sum(gi[i,j]*Ric[i,j] for i in range(n) for j in range(n)))
G=sp.simplify(Ric-Rs/2*g)
Gmix=sp.simplify(gi*G)  # G^mu_nu

ap=sp.diff(a,r); bp=sp.diff(b,r); app=sp.diff(a,r,2)
# solver's claimed formulas
Gtt_solver=sp.exp(-2*b)*(-2*r*bp-sp.exp(2*b)+1)/r**2
Grr_solver=sp.exp(-2*b)*(2*r*ap-sp.exp(2*b)+1)/r**2
Gthth_solver=sp.exp(-2*b)*(r*ap**2-r*ap*bp+r*app+ap-bp)/r
print("=== Independent symbolic G^mu_nu vs solver formulas ===")
print("G^t_t  match:", sp.simplify(Gmix[0,0]-Gtt_solver)==0)
print("G^r_r  match:", sp.simplify(Gmix[1,1]-Grr_solver)==0)
print("G^th_th match:", sp.simplify(Gmix[2,2]-Gthth_solver)==0)
print("G^ph_ph == G^th_th:", sp.simplify(Gmix[3,3]-Gmix[2,2])==0)

# ---- 2. Independent NUMERIC Einstein engine (central FD) ----
def grad_c(f,r):
    g=torch.zeros_like(f)
    g[1:-1]=(f[2:]-f[:-2])/(r[2:]-r[:-2])
    g[0]=(f[1]-f[0])/(r[1]-r[0]); g[-1]=(f[-1]-f[-2])/(r[-1]-r[-2])
    return g
def sec(f,r):
    fpp=torch.zeros_like(f)
    hm=r[1:-1]-r[:-2]; hp=r[2:]-r[1:-1]
    fpp[1:-1]=2*(hp*f[:-2]-(hm+hp)*f[1:-1]+hm*f[2:])/(hm*hp*(hm+hp))
    return fpp
def einstein_mix(r,a,b):
    ap=grad_c(a,r); bp=grad_c(b,r); app=sec(a,r)
    e2b=torch.exp(2*b); em2b=torch.exp(-2*b)
    Gtt=em2b*(-2*r*bp-e2b+1)/r**2
    Grr=em2b*(2*r*ap-e2b+1)/r**2
    Gthth=em2b*(r*ap**2-r*ap*bp+r*app+ap-bp)/r
    return Gtt,Grr,Gthth

# Validate: Schwarzschild a=0.5 ln(1-2M/r), b=-a
print("\n=== Engine validation ===")
for N in [800,1600,3200]:
    M=0.3
    rr=torch.linspace(2.0,12.0,N)  # outside horizon
    aa=0.5*torch.log(1-2*M/rr); bb=-aa
    Gtt,Grr,Gthth=einstein_mix(rr,aa,bb)
    interior=slice(2,-2)
    mx=max(Gtt[interior].abs().max(),Grr[interior].abs().max(),Gthth[interior].abs().max()).item()
    print(f" Schwarzschild N={N}: max|G^mu_nu| (vacuum, should ->0) = {mx:.3e}")
# flat
rr=torch.linspace(1.0,10.0,500); aa=torch.zeros_like(rr); bb=torch.zeros_like(rr)
Gtt,Grr,Gthth=einstein_mix(rr,aa,bb)
print(f" Flat: max|G| = {max(Gtt.abs().max(),Grr.abs().max(),Gthth.abs().max()).item():.3e}")

# ---- 3. Residual convergence on the solved soliton ----
print("\n=== CLAIM 3: residual convergence on solved soliton ===")
xi=kap=1.0; kap8=0.05; p=0.4; rc=0.05; ri=rc+14.0
for N in [800,1600,3200]:
    rg=make_grid(1,N,rc=rc,rint=ri,geom=False)
    out=selfconsistent_Bfree(rg,xi,kap,p=p,kap8=kap8,iters=400,relax=0.4,tol=1e-11)
    rr=rg[0]; aa=out['a'][0]; bb=out['b'][0]; Th=out['Th'][0]
    Gtt,Grr,Gthth=einstein_mix(rr,aa,bb)
    Thp=grad_c(Th,rr)
    X,Y,rho,pr,pT=stress(rr.unsqueeze(0),Th.unsqueeze(0),Thp.unsqueeze(0),bb.unsqueeze(0),xi,kap)
    rho=rho[0]; pr=pr[0]; pT=pT[0]
    res_tt=Gtt-kap8*(-rho); res_rr=Grr-kap8*pr; res_thth=Gthth-kap8*pT
    # full interior (drop 2 ghost pts each end)
    sl=slice(2,-2)
    full=max(res_tt[sl].abs().max(),res_rr[sl].abs().max(),res_thth[sl].abs().max()).item()
    # bulk excluding inner 10% of r-range
    rmin=rr[0].item(); rmax=rr[-1].item(); cut=rmin+0.10*(rmax-rmin)
    mask=(rr>cut)
    m=mask.clone(); m[-2:]=False
    bulk=max(res_tt[m].abs().max(),res_rr[m].abs().max(),res_thth[m].abs().max()).item()
    print(f" N={N:>5}: max|res| FULL interior={full:.3e}   BULK(excl inner 10%)={bulk:.3e}  (cut r={cut:.2f})")
