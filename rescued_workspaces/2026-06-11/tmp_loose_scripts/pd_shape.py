import numpy as np
from scipy.integrate import solve_ivp, cumulative_trapezoid
m=1.0; r0=1e-3; RMAX=80.0; rg=np.linspace(r0,RMAX,60000)
phib=0.5*np.log(rg/(2+rg)); kappa=-1
def dirac(E):
    def rhs(r,y):
        ph=0.5*np.log((2+r)/r);pp=-1.0/(r*(2+r));e1=np.exp(ph);e2=np.exp(2*ph);g,f=y
        return [(pp-kappa/r)*g+(E*e2+m*e1)*f,(pp+kappa/r)*f-(E*e2-m*e1)*g]
    s=solve_ivp(rhs,[r0,RMAX],[r0**.5,0.],dense_output=True,rtol=1e-10,atol=1e-12,max_step=0.02)
    G,F=s.y[0,-1],s.y[1,-1];q=np.sqrt(max(m*m-E*E,1e-12));return (G+(E+m)/q*F)/np.sqrt(G*G+F*F+1e-300),s
lo,hi=.45,.55
for _ in range(60):
    mid=.5*(lo+hi)
    if dirac(lo)[0]*dirac(mid)[0]<0:hi=mid
    else:lo=mid
E=.5*(lo+hi);_,s=dirac(E);G=s.sol(rg)[0];F=s.sol(rg)[1]
nn=np.sqrt(np.trapezoid(G*G+F*F,rg));G/=nn;F/=nn
PHI=-phib;PHIp=-1.0/(rg*(2+rg))
T=-2*(-1)*(kappa*(F**2-G**2)/rg+PHIp*(F**2+G**2)+m*np.exp(PHI)*G*F)
qsrc=np.exp(4*phib)*T;p0=(2+rg)**2
ri=cumulative_trapezoid(p0*qsrc,rg,initial=0.);dphip=ri/p0
dphi=-(np.trapezoid(dphip,rg)-cumulative_trapezoid(dphip,rg,initial=0.))
print(f"dimple dphi(0)={dphi[0]:+.3f}; dphi'max={dphip.max():.4f} at r={rg[np.argmax(dphip)]:.2f}")
print("\nboson stiffness p_d=(2+r)^2 exp(-4 lam dphi): does it develop a DIP (cavity) or stay monotone (reflector)?")
print("  d(ln p_d)/dr = 2/(2+r) - 4 lam dphi'  ; a sign +->-  then -->+ = a local MAX then MIN = a cavity")
for lam in [0.0,0.1,0.3,0.5,1.0,2.0,4.0]:
    dlnpd=2/(2+rg)-4*lam*dphip
    # count sign changes (away from r0 noise)
    msk=rg>0.02; sc=np.where(np.diff(np.sign(dlnpd[msk]))!=0)[0]
    rsc=rg[msk][sc]
    has_cavity = len(rsc)>=2
    tag = f"DIP/cavity at r~{rsc[0]:.2f}-{rsc[1]:.2f}" if has_cavity else ("monotone-increasing (reflector)" if np.all(dlnpd[msk]>-1e-9) else f"{len(rsc)} turning pt(s)")
    print(f"  lam={lam:4.1f}: {len(rsc)} turning point(s) -> {tag}")
print("\n=> if NO cavity at physical lam: the fermion dimple is a monotone barrier -> boson scatters smoothly,")
print("   NO trapped resonance (no spectral line). A cavity only forms above some lam threshold (if at all).")
