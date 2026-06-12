import numpy as np
from numpy import pi as PI, cos, exp
from scipy.integrate import solve_ivp

phi0=-cos(PI/5); MU2=PI/3; rstar=6.9875; me=0.5109989; r0=1e-6
C=4*PI**2*me*rstar
RMAX=12.0; NG=2000; rg=np.linspace(r0,RMAX,NG)
V=solve_ivp(lambda r,y:[y[1]*exp(2*y[0])/r**2 if r>0 else 0.0, r**2*MU2*y[0]],
            [r0,RMAX],[phi0+(MU2*phi0*exp(2*phi0)/6)*r0**2,r0**3*MU2*phi0/3],
            dense_output=True,rtol=1e-12,atol=1e-14,max_step=0.004)
phibg=V.sol(rg)[0]; phibg_p=V.sol(rg)[1]*np.exp(2*phibg)/rg**2

def resid(E,kappa):
    L=-kappa if kappa<0 else kappa
    def rhs(r,y):
        p=np.interp(r,rg,phibg); pp=np.interp(r,rg,phibg_p); g,f=y
        return [(pp-kappa/r)*g+E*exp(2*p)*f,(pp+kappa/r)*f-E*exp(2*p)*g]
    if kappa<0: G=r0**L; F=-(E*exp(2*phi0)/(2*L+1))*r0**(L+1)
    else: F=r0**L; G=(E*exp(2*phi0)/(2*L+1))*r0**(L+1)
    s=solve_ivp(rhs,[r0,rstar],[G,F],rtol=1e-9,atol=1e-11,max_step=0.01)
    p=np.interp(rstar,rg,phibg); pp=np.interp(rstar,rg,phibg_p); g,f=s.y[0,-1],s.y[1,-1]
    return (pp-kappa/rstar)*g+E*exp(2*p)*f
def eigs(kappa,nmax,Emax=14.0,nb=700):
    Es=np.linspace(0.05,Emax,nb); rs=np.array([resid(E,kappa) for E in Es]); out=[]
    for i in range(nb-1):
        if rs[i]*rs[i+1]<0:
            a,b=Es[i],Es[i+1]
            for _ in range(45):
                m=.5*(a+b)
                if resid(a,kappa)*resid(m,kappa)<0: b=m
                else: a=m
            out.append(.5*(a+b))
            if len(out)>=nmax: break
    return out

A = np.array(sorted([134.98,547.9,775.3,782.7,957.8,980.0,990.0,1019.5,1166.0,1229.5,1230.0,1275.5,1281.9,1294.0,1300.0,1318.2]))

for NMAX in [2,3,4]:
    P=[]
    for k in [-1,1,-2,2,-3,3]:
        for e in eigs(k,NMAX): P.append(e*C)
    P=np.array(sorted(P))
    # count predicted modes <1350 with NO meson within 3%
    orphans=[p for p in P if p<1350 and min(abs(p-A)/p)>0.03]
    obs_rms=np.sqrt(np.mean([min(abs(o-P)/o)**2 for o in A]))*100
    pred_rms_lt1350=np.sqrt(np.mean([min(abs(p-A)/p)**2 for p in P if p<1350]))*100
    print(f"NMAX={NMAX}: {len(P)} modes, range {P.min():.0f}-{P.max():.0f}")
    print(f"   modes<1350: {sorted([round(p,1) for p in P if p<1350])}")
    print(f"   SPURIOUS (no meson within 3%, <1350): {[round(o,1) for o in orphans]}")
    print(f"   obs->pred RMS={obs_rms:.2f}%  pred(<1350)->obs RMS={pred_rms_lt1350:.2f}%\n")
