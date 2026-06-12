import numpy as np
from scipy.integrate import solve_ivp, cumulative_trapezoid
m=1.0; r0=1e-3; RMAX=80.0
rg=np.linspace(r0,RMAX,60000)
phib=0.5*np.log(rg/(2+rg)); 
# fermion kappa=-1 ground -> dimple dphi (reuse the validated source) ; sigma=-1, kappa=-1
kappa=-1
def dirac(E):
    def rhs(r,y):
        ph=0.5*np.log((2+r)/r); pp=-1.0/(r*(2+r)); e1=np.exp(ph); e2=np.exp(2*ph); g,f=y
        return [(pp-kappa/r)*g+(E*e2+m*e1)*f,(pp+kappa/r)*f-(E*e2-m*e1)*g]
    s=solve_ivp(rhs,[r0,RMAX],[r0**0.5,0.0],dense_output=True,rtol=1e-10,atol=1e-12,max_step=0.02)
    G,F=s.y[0,-1],s.y[1,-1]; q=np.sqrt(max(m*m-E*E,1e-12)); return (G+(E+m)/q*F)/np.sqrt(G*G+F*F+1e-300),s
lo,hi=0.45,0.55
for _ in range(60):
    mid=.5*(lo+hi)
    if dirac(lo)[0]*dirac(mid)[0]<0: hi=mid
    else: lo=mid
E=.5*(lo+hi); _,s=dirac(E); G=s.sol(rg)[0]; F=s.sol(rg)[1]
G/=np.sqrt(np.trapezoid(G*G+F*F,rg)); F/=np.sqrt(np.trapezoid(G*G+F*F,rg))
PHI=-phib; PHIp=1.0/(rg*(2+rg))*( -1)  # = -phi' ... careful: phi'=1/(r(2+r)), Phi'=-phi'
PHIp=-1.0/(rg*(2+rg))
T=-2*(-1)*(kappa*(F**2-G**2)/rg+PHIp*(F**2+G**2)+m*np.exp(PHI)*G*F)
qsrc=np.exp(4*phib)*T; p0=(2+rg)**2
ri=cumulative_trapezoid(p0*qsrc,rg,initial=0.0); dphip=ri/p0
dphi=-(np.trapezoid(dphip,rg)-cumulative_trapezoid(dphip,rg,initial=0.0))
print(f"fermion E={E:.5f}; dimple dphi(0)={dphi[0]:+.4f} (deepening at center)")

def veff(lam):
    # boson: -(p_d u')' = w^2 r^2 u ; p_d=(2+r)^2 e^{-4 lam dphi}, w=r^2
    pd=(2+rg)**2*np.exp(-4*lam*dphi); w=rg**2
    # Liouville: x=int sqrt(w/p) dr ; Q=(p w)^{1/4} ; V=Q_xx/Q  (then -psi_xx+V psi=w^2 psi)
    integ=np.sqrt(w/pd); x=cumulative_trapezoid(integ,rg,initial=0.0)
    Q=(pd*w)**0.25
    # d/dx = (1/integ) d/dr
    dQdr=np.gradient(Q,rg); dQdx=dQdr/integ
    d2Qdx2=np.gradient(dQdx,rg)/integ
    V=d2Qdx2/Q
    return x,V
for lam in [0.0,0.1,0.3,1.0]:
    x,V=veff(lam)
    # look at V in the interaction region (r<15) away from r->0 grid noise
    mask=(rg>0.05)&(rg<20)
    Vi=V[mask]; xi=x[mask]
    imin=np.argmin(Vi); imax=np.argmax(Vi)
    well = Vi.min()<0
    print(f" lam={lam:4.1f}: V_eff in r in[.05,20]: min={Vi.min():+.4f}@x={xi[imin]:.2f}(r={rg[mask][imin]:.2f}), "
          f"max={Vi.max():+.4f}@x={xi[imax]:.2f}(r={rg[mask][imax]:.2f})  -> {'HAS A WELL (V<0): resonances possible' if well else 'barrier/no well: NO trapped resonance'}")
print("\n(asymptotic V_eff -> 0 as r->inf for massless; a WELL below 0 between barriers can host a resonance;")
print(" a pure positive barrier reflects but does not trap. Read the shape.)")
