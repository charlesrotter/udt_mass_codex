import numpy as np
from numpy import pi as PI, cos, exp
from scipy.integrate import solve_ivp
phi0=-cos(PI/5); MU2=PI/3; rstar=6.9875; me=0.5109989; r0=1e-6
C=4*PI**2*me*rstar
RMAX=12.0; NG=1500; rg=np.linspace(r0,RMAX,NG)
V=solve_ivp(lambda r,y:[y[1]*exp(2*y[0])/r**2 if r>0 else 0.0, r**2*MU2*y[0]],
            [r0,RMAX],[phi0+(MU2*phi0*exp(2*phi0)/6)*r0**2,r0**3*MU2*phi0/3],
            dense_output=True,rtol=1e-10,atol=1e-12,max_step=0.01)
phibg=V.sol(rg)[0]; phibg_p=V.sol(rg)[1]*np.exp(2*phibg)/rg**2
def resid(E,kappa):
    L=-kappa if kappa<0 else kappa
    def rhs(r,y):
        p=np.interp(r,rg,phibg); pp=np.interp(r,rg,phibg_p); g,f=y
        return [(pp-kappa/r)*g+E*exp(2*p)*f,(pp+kappa/r)*f-E*exp(2*p)*g]
    if kappa<0: G=r0**L; F=-(E*exp(2*phi0)/(2*L+1))*r0**(L+1)
    else: F=r0**L; G=(E*exp(2*phi0)/(2*L+1))*r0**(L+1)
    s=solve_ivp(rhs,[r0,rstar],[G,F],rtol=1e-8,atol=1e-10,max_step=0.03)
    p=np.interp(rstar,rg,phibg); pp=np.interp(rstar,rg,phibg_p); g,f=s.y[0,-1],s.y[1,-1]
    return (pp-kappa/rstar)*g+E*exp(2*p)*f
def eigs(kappa,nmax,Emax=14.0,nb=400):
    Es=np.linspace(0.05,Emax,nb); rs=np.array([resid(E,kappa) for E in Es]); out=[]
    for i in range(nb-1):
        if rs[i]*rs[i+1]<0:
            a,b=Es[i],Es[i+1]
            for _ in range(35):
                m=.5*(a+b)
                if resid(a,kappa)*resid(m,kappa)<0: b=m
                else: a=m
            out.append(.5*(a+b))
            if len(out)>=nmax: break
    return out
A = np.array(sorted([134.98,547.9,775.3,782.7,957.8,980.0,990.0,1019.5,1166.0,1229.5,1230.0,1275.5,1281.9,1294.0,1300.0,1318.2]))
allk={}
for k in [-1,1,-2,2,-3,3]:
    allk[k]=eigs(k,4)
    print(f"k={k:+d}: {[round(e*C,1) for e in allk[k]]}")
for NMAX in [2,3,4]:
    P=sorted([e*C for k in allk for e in allk[k][:NMAX]])
    P=np.array(P)
    orphans=[round(p,1) for p in P if p<1350 and min(abs(p-A)/p)>0.03]
    print(f"\nNMAX={NMAX}: modes<1350={sorted([round(p,1) for p in P if p<1350])}")
    print(f"   SPURIOUS(no meson w/in 3%,<1350)={orphans}  count={len(orphans)}")
