import numpy as np
from numpy import pi as PI, cos, exp, sqrt
from scipy.integrate import solve_ivp, simpson
from scipy.optimize import brentq
phi0=-cos(PI/5); MU2=PI/3; rstar=6.9875; r0=1e-6
rg=np.linspace(r0,rstar,3000)
V=solve_ivp(lambda r,y:[y[1]*exp(2*y[0])/r**2 if r>0 else 0.,r**2*MU2*y[0]],[r0,rstar],
            [phi0+(MU2*phi0*exp(2*phi0)/6)*r0**2,r0**3*MU2*phi0/3],dense_output=True,rtol=1e-12,atol=1e-14,max_step=0.006)
phiv=np.array([V.sol(r)[0] for r in rg]); Jv=np.array([V.sol(r)[1] for r in rg])
phif=lambda r:np.interp(r,rg,phiv); phipf=lambda r:np.interp(r,rg,Jv)*exp(2*np.interp(r,rg,phiv))/r**2
def modes(kap,nmax=3,Emax=14,npts=300):
    e0=exp(2*phi0); l=-kap if kap<0 else kap
    def sol(E):
        if kap<0: G0=r0**l; F0=-(E*e0/(2*l+1))*r0**(l+1)
        else: F0=r0**l; G0=(E*e0/(2*l+1))*r0**(l+1)
        def f(r,y):
            g,ff=y;p=phif(r);pp=phipf(r);e2=exp(2*p)
            return [(pp-kap/r)*g+E*e2*ff,(pp+kap/r)*ff-E*e2*g]
        return solve_ivp(f,[r0,rstar],[G0,F0],method='DOP853',dense_output=True,rtol=1e-10,atol=1e-12,max_step=0.02)
    def bc(E):
        s=sol(E);g,ff=s.y[:,-1];return (phipf(rstar)-kap/rstar)*g+E*exp(2*phif(rstar))*ff
    Es=np.linspace(0.05,Emax,npts);v=[bc(E) for E in Es];out=[]
    for i in range(len(Es)-1):
        if v[i]*v[i+1]<0:
            E=brentq(bc,Es[i],Es[i+1],xtol=1e-11);s=sol(E);G=s.sol(rg)[0];F=s.sol(rg)[1];out.append((E,G,F))
        if len(out)>=nmax:break
    return out
M={k:modes(k) for k in [-1,-2,-3,2]}
def ip(a,b,w): return simpson((a[1]*b[1]+a[2]*b[2])*w,rg)
print("MEASURE TEST: off-diagonal <1|2> within kappa=-1 for various weights (want ~0):")
m=M[-1]
for name,w in [('1',np.ones_like(rg)),('e^phi',exp(phiv)),('e^2phi',exp(2*phiv)),('e^-phi',exp(-phiv)),("r^2 e^2phi",rg**2*exp(2*phiv))]:
    n11=ip(m[0],m[0],w); n22=ip(m[1],m[1],w); o12=ip(m[0],m[1],w)
    print(f"  w={name:12} <1|2>/sqrt(<1|1><2|2>) = {o12/sqrt(n11*n22):+.5f}")
# pick the best and renormalize, then dipoles
def best_measure():
    m=M[-1];best=None;bo=9
    for name,w in [('1',np.ones_like(rg)),('e^phi',exp(phiv)),('e^2phi',exp(2*phiv)),('e^-phi',exp(-phiv))]:
        tot=0
        for i in range(len(m)):
            for j in range(i+1,len(m)):
                tot+=abs(ip(m[i],m[j],w)/sqrt(ip(m[i],m[i],w)*ip(m[j],m[j],w)))
        if tot<bo: bo=tot;best=(name,w)
    return best,bo
(bn,bw),bo=best_measure()
print(f"\nBEST orthogonality measure: w={bn} (sum|off-diag|={bo:.4f})")
# renormalize all modes under bw, recompute dipoles <n|r|n+1>
def norm(a,w): n=sqrt(ip(a,a,w)); return (a[0],a[1]/n,a[2]/n)
print(f"\nradial dipole <n|r|n+1> under correct measure w={bn}:")
for k in [-1,-2,-3,2]:
    mk=[norm(x,bw) for x in M[k]]
    vals=[ip(mk[i],mk[i+1],bw*rg) for i in range(len(mk)-1)]  # <n| r |n+1>
    print(f"  kappa={k:+d}: "+"  ".join(f"<{i+1}|r|{i+2}>={v:+.5f}" for i,v in enumerate(vals)))
print(f"\n<n|e^phi|n+1> under w={bn}:")
for k in [-1,-2,-3,2]:
    mk=[norm(x,bw) for x in M[k]]
    vals=[ip(mk[i],mk[i+1],bw*exp(phiv)) for i in range(len(mk)-1)]
    print(f"  kappa={k:+d}: "+"  ".join(f"<{i+1}|ephi|{i+2}>={v:+.5f}" for i,v in enumerate(vals)))
