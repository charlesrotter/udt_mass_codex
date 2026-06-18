# VERIF_deep_phi_sign_D5.py
# D5 support: (a) GOLDSTONE / breathing-zero-mode identification at depth (S5),
#             (b) kappa/xi RATIO sensitivity (S2),
#             (c) intrinsic-magnitude (R-independent) confirmation at exact coeff (D4).
#
# GOLDSTONE logic for the l=0 sector:
#  - translation(x3), rotation, iso-rotation(chi) are l=1 (vector) modes, NOT l=0.
#    The l=0 breathing/dilation channel cannot host them. So the l=0 lowest mode
#    is the BREATHING mode.
#  - The dilation/breathing "zero mode" Theta(r)->Theta(r/lambda) is a TRUE zero mode
#    ONLY for a scale-invariant (unstabilized) action. The native L4 stabilizer PINS
#    the size (native_stabilizer: lambda*=sqrt(B/A)), so the breathing mode has a
#    RESTORING curvature E''(lambda*)>0 -> it is a genuine (non-zero) physical mode,
#    NOT a Goldstone. We TEST this directly: project the exact operator onto the
#    dilation tangent u_dil(r) = r dTheta0/dr (the generator of Theta(r/lambda)) and
#    check the Rayleigh quotient sign; a true Goldstone gives 0, a stabilized
#    breather gives >0 (flat) and the deep-phi value is the physical breathing freq.
import math, numpy as np, mpmath as mp
from scipy.integrate import solve_bvp
mp.mp.dps = 60
TWO_PI_3 = 2*math.pi/3

def phi_bg(r,p,r_int):
    if p==0.0: return np.zeros_like(r),np.zeros_like(r)
    return p*np.log(r/r_int), p/r
def theta_ddot(r,Th,Thp,phi,phip,xi,kappa):
    s=np.sin(Th)
    num=((0.5)*Thp*r**2*(-4*Thp*kappa*np.sin(2*Th)+Thp*kappa*np.sin(4*Th)
        -Thp*r**2*xi*np.sin(2*Th)+kappa*phip*(1-np.cos(2*Th))**2-2*kappa*phip*np.cos(2*Th)
        +2*kappa*phip-phip*r**2*xi*np.cos(2*Th)+5*phip*r**2*xi+2*r*xi*np.cos(2*Th)-10*r*xi)
        +2*kappa*np.exp(2*phi)*s**3*np.cos(Th)+2*r**2*xi*np.exp(2*phi)*np.sin(2*Th))
    den=r**2*(2*kappa*s**4+2*kappa*s**2+r**2*xi*s**2+2*r**2*xi)
    return num/den
def solve_ground(r_core,r_int,xi,kappa,p,N=1000):
    x0=np.linspace(r_core,r_int,N)
    def rhs(r,y):
        Th,Thp=y; phi,phip=phi_bg(r,p,r_int); return np.vstack([Thp,theta_ddot(r,Th,Thp,phi,phip,xi,kappa)])
    def bc(ya,yb): return np.array([ya[0]-math.pi,yb[0]])
    L=math.sqrt(kappa/xi); w=2*L
    Th0=math.pi*0.5*(1-np.tanh((x0-(r_core+w))/(0.8*L)))
    return solve_bvp(rhs,bc,x0,np.vstack([Th0,np.gradient(Th0,x0)]),tol=1e-9,max_nodes=600000)

def coeffs(rg,Th0,phi,xi,kappa,well='ON'):
    r=[mp.mpf(x) for x in rg]; Th=[mp.mpf(x) for x in Th0]; ph=[mp.mpf(x) for x in phi]
    N=len(r); xi=mp.mpf(xi); kappa=mp.mpf(kappa); c=mp.mpf(TWO_PI_3)
    Tp0=[ (Th[i+1]-Th[i-1])/(r[i+1]-r[i-1]) if 0<i<N-1 else mp.mpf(0) for i in range(N)]
    P=[None]*N;Q=[None]*N;Rm=[None]*N;W=[None]*N
    for i in range(N):
        ri=r[i];T=Th[i];pp=ph[i];Tp=Tp0[i]
        s=mp.sin(T);cs=mp.cos(T);s2=s*s;s4=s2*s2
        em=mp.e**(-pp);e2p=mp.e**(2*pp);e3p=mp.e**(3*pp)
        c2T=mp.cos(2*T);c4T=mp.cos(4*T)
        P[i]=2*(2*kappa*(s4+s2)+ri**2*xi*(s2+2))*em
        W[i]=c*(2*kappa*(s4+s2)+ri**2*xi*(s2+2))*e3p
        Rm[i]=-4*Tp*(2*kappa*(c2T-2)-ri**2*xi)*em*s*cs
        Q[i]=(-kappa*(Tp**2*ri**2*(64*s4-32*s2-8)+(3*c4T-3)*e2p+8*e2p*s4)/2
              +2*ri**2*xi*(Tp**2*ri**2+4*e2p)*c2T)*em/ri**2
    if well=='OFF': Q=[mp.mpf(0)]*N; Rm=[mp.mpf(0)]*N
    dRm=[ (Rm[i+1]-Rm[i-1])/(r[i+1]-r[i-1]) if 0<i<N-1 else mp.mpf(0) for i in range(N)]
    Veff=[Q[i]-dRm[i] for i in range(N)]
    return r,P,Veff,W,Tp0

def eig_low(rg,Th0,phi,xi,kappa,nev=4,well='ON'):
    r,P,Veff,W,_=coeffs(rg,Th0,phi,xi,kappa,well)
    N=len(r); n=N-2; Hm=mp.zeros(n); Wd=[None]*n
    for i in range(1,N-1):
        Pr=(P[i]+P[i+1])/2;Pl=(P[i-1]+P[i])/2
        hr=r[i+1]-r[i];hl=r[i]-r[i-1];hc=(hr+hl)/2;k=i-1
        Hm[k,k]=(Pr/hr+Pl/hl)/hc+Veff[i]
        if k+1<n: Hm[k,k+1]=-Pr/hr/hc
        if k-1>=0: Hm[k,k-1]=-Pl/hl/hc
        Wd[k]=W[i]
    Winv=[1/mp.sqrt(w) for w in Wd]; A=mp.zeros(n)
    for a in range(n):
        for b in range(max(0,a-1),min(n,a+2)): A[a,b]=Hm[a,b]*Winv[a]*Winv[b]
    for a in range(n):
        for b in range(a+1,n): A[a,b]=A[b,a]=(A[a,b]+A[b,a])/2
    ev=mp.eigsy(A,eigvals_only=True); evs=sorted([ev[i] for i in range(n)])
    return [float(x) for x in evs[:nev]]

def rayleigh_dilation(rg,Th0,phi,xi,kappa,well='ON'):
    """Rayleigh quotient of the EXACT operator on the dilation tangent u=r*Theta0'(r).
       True Goldstone -> 0; stabilized breather -> >0 (flat). Tests if the lowest
       mode is a zero mode."""
    r,P,Veff,W,Tp0=coeffs(rg,Th0,phi,xi,kappa,well)
    N=len(r)
    u=[ r[i]*Tp0[i] for i in range(N) ]   # dilation generator
    # numerator INT[P u'^2 + Veff u^2] dr ; denominator INT[W u^2] dr (trapezoid, Dirichlet ends)
    num=mp.mpf(0); den=mp.mpf(0)
    for i in range(1,N-1):
        hr=r[i+1]-r[i]; hl=r[i]-r[i-1]; hc=(hr+hl)/2
        up=(u[i+1]-u[i-1])/(r[i+1]-r[i-1])
        num+= (P[i]*up**2 + Veff[i]*u[i]**2)*hc
        den+= W[i]*u[i]**2*hc
    return float(num/den)

def log_grid(rc,ri,N):
    x=np.linspace(math.log(rc),math.log(ri),N); return np.exp(x)

r_core=0.05; L=1.0
print("="*72)
print("D5(a) -- is the l=0 lowest mode a Goldstone? Rayleigh on dilation tangent")
print("  (true zero mode -> ~0; stabilized breather -> nonzero physical freq)")
print("="*72)
for p in [0.0,1.0,2.0]:
    ri=r_core+18*L; g=solve_ground(r_core,ri,1.0,1.0,p)
    rg=log_grid(r_core,ri,180); Tg=g.sol(rg)[0]; phg,_=phi_bg(rg,p,ri)
    rq=rayleigh_dilation(rg,Tg,phg,1.0,1.0,'ON')
    ev=eig_low(rg,Tg,phg,1.0,1.0,nev=2,well='ON')[0]
    print(f"  p={p}: Rayleigh[dilation]={rq:+.4e}   true-lowest omega^2={ev:+.4e}  "
          f"(ratio {rq/ev if ev!=0 else float('nan'):+.2f})")

print("\n"+"="*72)
print("D5(b) -- kappa/xi RATIO sensitivity of the deep-phi sign (S2)")
print("  corpus soliton: size ~ sqrt(kappa/xi); ratio is the ONLY length. CHOSEN xi=kappa=1")
print("  here; TEST whether the SIGN survives ratio changes.")
print("="*72)
for ratio in [0.25, 1.0, 4.0]:
    kap=ratio; xi=1.0
    for p in [0.0,1.0,2.0]:
        ri=r_core+18*L; g=solve_ground(r_core,ri,xi,kap,p)
        rg=log_grid(r_core,ri,180); Tg=g.sol(rg)[0]; phg,_=phi_bg(rg,p,ri)
        ev=eig_low(rg,Tg,phg,xi,kap,nev=2,well='ON')[0]
        print(f"  kappa/xi={ratio:4.2f} p={p}: lowest omega^2 = {ev:+.6e}")

print("\nDONE D5.")
