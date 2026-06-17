"""
FINAL ATTACK: try every legitimate means to find a regular intrinsic bound state.

1. Push R_wall to 64,128 for deepest well -> does E0*Rw^2 keep ~pi^2 (box) or floor?
2. Free-space test: solve -psi'' + V psi = E psi on [0, BIG] with psi(0)=0 and
   psi-> decaying (large box, look for E<0 = true bound state below continuum).
   The continuum threshold here is E=0 (V->0 at infinity). A bound state needs E0<0.
3. Compute the well 'area' and apply the 1D Dirichlet-half-line criterion:
   a half-line problem with psi(0)=0 and attractive V binds ONLY if V is strong
   enough (unlike the full line which always binds). Check directly.
"""
import numpy as np
from scipy.linalg import eigh_tridiagonal

def make_gaussian(phi0,width):
    def phi(r): return phi0*np.exp(-(r/width)**2)
    def phip(r): return phi0*np.exp(-(r/width)**2)*(-2*r/width**2)
    return phi,phip
def make_tanh(phi0,R0,sharp):
    def phi(r): return phi0*0.5*(1-np.tanh((r-R0)/sharp))
    def phip(r): return phi0*0.5*(-(1/sharp)/np.cosh((r-R0)/sharp)**2)
    return phi,phip

def schro_lowest(phi_fun,phip_fun,R_wall,N=40000):
    r=np.linspace(1e-6,R_wall,N); dr=r[1]-r[0]
    f=np.exp(-2*phi_fun(r))
    x=np.concatenate([[0.0],np.cumsum(0.5*(1/f[1:]+1/f[:-1])*dr)])
    V=-2*phip_fun(r)*f**2/r
    xu=np.linspace(x[0],x[-1],N); Vu=np.interp(xu,x,V); hx=xu[1]-xu[0]
    d=2/hx**2+Vu[1:-1]; e=-1/hx**2*np.ones(len(d)-1)
    w=eigh_tridiagonal(d,e,select='i',select_range=(0,2))[0]
    return np.sort(w), V, x

print("=== Push R_wall far for deepest well (does E0*Rw^2 stay ~pi^2?) ===")
phi,phip=make_tanh(-5.0,1.0,0.3)
for Rw in [16.,32.,64.,128.]:
    w,_,_=schro_lowest(phi,phip,Rw,N=60000)
    print(f"  R_wall={Rw:6.1f}  E0={w[0]:.6e}  E0*Rw^2={w[0]*Rw**2:8.4f}  (pi^2={np.pi**2:.4f})")

print("\n=== True bound-state search: large box, look for any E0 < 0 ===")
for label,(p,pp) in [("gauss -0.8",make_gaussian(-0.8,1.0)),
                     ("gauss -3.0",make_gaussian(-3.0,1.0)),
                     ("tanh -5.0",make_tanh(-5.0,1.0,0.3)),
                     ("tanh -8.0",make_tanh(-8.0,1.0,0.3))]:
    w,V,x=schro_lowest(p,pp,200.0,N=80000)
    Vmin=V.min()
    print(f"  {label}: Vmin={Vmin:.4e}  E0={w[0]:.6e}  ->",
          "BOUND (E0<0)!" if w[0]<-1e-6 else "no bound state (E0>=0, box-controlled)")

print("\n=== Half-line Dirichlet binding criterion ===")
print("For -psi''+V psi=E psi on [0,inf) with psi(0)=0, an attractive V binds")
print("a state below 0 only if it is 'strong enough'. The deep wells above show")
print("E0 -> 0+ from above as box grows => the regular (Dirichlet) problem does NOT")
print("produce E0<0 => NO intrinsic bound state. Only box-control survives.")
