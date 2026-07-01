import os; os.environ.setdefault("PYTORCH_NVML_BASED_CUDA_CHECK","0")
import numpy as np, torch
torch.set_default_dtype(torch.float64)
from spectral_radial_soliton import solve as rsolve
from spectral_catalog_solver import TGrid, matter_stress_t, metric_stack, _matEL_t
# converged round soliton
out=rsolve(96, rc=0.05, cell=14.0, p=0.4, kap8=0.05, maxit=120)
r=out['r']; a=out['a']; b=out['b']; Th=out['Th']; D=out['D']
ap=D@a; bp=D@b
# Build div_mu T^mu_r numerically using the committed torch stress in 1D (round).
# Easiest: use sympy lambdified Tmix^mu_r in round limit, take d/dr numerically + connection.
import sympy as sp
rs=sp.symbols('rs',positive=True); ths,pss=sp.symbols('ths pss')
xi=kap=1.0
A=sp.Function('A')(rs);Bf=sp.Function('Bf')(rs);TT=sp.Function('TT')(rs)
g=sp.diag(-sp.exp(2*A),sp.exp(2*Bf),rs**2,rs**2*sp.sin(ths)**2)
ginv=g.inv()
coords=[sp.symbols('t'),rs,ths,pss]
sT,cT=sp.sin(TT),sp.cos(TT);sth,cth=sp.sin(ths),sp.cos(ths)
nA=[cT,sT*sth*sp.cos(pss),sT*sth*sp.sin(pss),sT*cth]
Gmn=sp.zeros(4,4)
for mu in range(4):
 for nu in range(4):
  Gmn[mu,nu]=sum(sp.diff(nA[X],coords[mu])*sp.diff(nA[X],coords[nu]) for X in range(4))
L2=-(sp.Rational(1,2))*sum(ginv[i,j]*Gmn[i,j] for i in range(4) for j in range(4))
L4=0
for mu in range(4):
 for nu in range(4):
  for pp in range(4):
   for q in range(4):
    L4+=ginv[mu,pp]*ginv[nu,q]*(Gmn[mu,nu]*Gmn[pp,q]-Gmn[mu,q]*Gmn[pp,nu])
L4=-(sp.Rational(1,4))*L4
L=L2+L4
SSt={}
Cab=sp.zeros(4,4)
for X in range(4):
 for B2 in range(4):
  Cab[X,B2]=sum(ginv[nn,q]*(Gmn[X,B2]*Gmn[nn,q]-Gmn[X,q]*Gmn[nn,B2]) for nn in range(4) for q in range(4))
Cab=(Cab+Cab.T)/2
Tlow=xi*Gmn+kap*Cab+g*L
Tmix=ginv*Tlow
Gam=[[[sum(ginv[al,de]*(sp.diff(g[de,be],coords[ga])+sp.diff(g[de,ga],coords[be])-sp.diff(g[be,ga],coords[de])) for de in range(4))/2 for ga in range(4)] for be in range(4)] for al in range(4)]
nu=1
div=sum(sp.diff(Tmix[mu,nu],coords[mu]) for mu in range(4))
for mu in range(4):
 for l in range(4):
  div+=Gam[mu][mu][l]*Tmix[l,nu]-Gam[l][mu][nu]*Tmix[mu,l]
# lambdify div(r) with A,Bf,TT and derivs
Ap=sp.Symbol('Ap');Bp=sp.Symbol('Bp');Tp=sp.Symbol('Tp');Tpp=sp.Symbol("Tpp");App=sp.Symbol("App");Bpp=sp.Symbol("Bpp");Av=sp.Symbol('Av');Bv=sp.Symbol('Bv');Tv=sp.Symbol('Tv')
sub={sp.diff(A,rs,2):App,sp.diff(Bf,rs,2):Bpp,sp.diff(A,rs):Ap,sp.diff(Bf,rs):Bp,sp.diff(TT,rs,2):Tpp,sp.diff(TT,rs):Tp,A:Av,Bf:Bv,TT:Tv}
divexpr=div.subs(sub).subs({ths:sp.pi/2,pss:0}); divL=sp.lambdify((rs,Av,Bv,Tv,Ap,Bp,Tp,Tpp),divexpr,"numpy")
Thp=D@Th; Thpp=D@Thp
divnum=np.array([divL(r[i],a[i],b[i],Th[i],ap[i],bp[i],Thp[i],Thpp[i]) for i in range(r.size)])
# audited residual & my EL
from VERIF_indep_matter import EL_lam
import axisym_matter_el as ME
body=(r>0.6)&(r<r[-1]-0.6)
comm=np.array([ME.matter_el_resid(r[i],np.pi/2,a[i],b[i],0,0,Th[i],ap[i],bp[i],0,0,Thp[i],0,0,0,0,0,(D@ap)[i],(D@bp)[i],0,0,Thpp[i],0,0,0,0,0,0,0,0,0,0,1.0,1.0) for i in range(r.size)])
mine=np.array([EL_lam(r[i],np.pi/2,a[i],ap[i],0,(D@ap)[i],0,0,b[i],bp[i],0,(D@bp)[i],0,0,0,0,0,0,0,0,0,0,0,0,0,0,Th[i],Thp[i],0,Thpp[i],0,0,1.0,1.0) for i in range(r.size)])
print("On converged round soliton (N=96), body max-abs:")
print(f"  div_mu T^mu_r (committed stress) : {np.max(np.abs(divnum[body])):.3e}")
print(f"  committed axisym matter EL       : {np.max(np.abs(comm[body])):.3e}")
print(f"  INDEPENDENT (my) matter EL       : {np.max(np.abs(mine[body])):.3e}")
# diagnostic at end won't reach; instead print free syms before lambdify
