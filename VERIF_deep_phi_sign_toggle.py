# VERIF_deep_phi_sign_toggle.py
# Diagnose + correctly implement the CAUSAL TOGGLE (S4): phi-angular WELL ON vs OFF.
# The prior D2345 toggle (Q=Rmix=0) produced spurious NEGATIVE omega^2 for a pure
# positive-definite kinetic operator -> numerical pathology. Here we:
#  (1) verify the kinetic-only operator -(d/dr)(P u')=omega^2 W u is POSITIVE (box),
#      using a clean Dirichlet FD on the log grid + a positivity-safe eigensolver.
#  (2) implement the toggle as a WELL-SCALE sweep g: Veff -> g*Veff_attractive, so
#      g=1 is full native, g=0 is well-off; track the lowest mode continuously.
#  (3) confirm: well ON -> the stable box tower; well scaled up -> if a depth-
#      amplified attractive well existed it would drive omega^2 down; report sign.
import math, numpy as np, mpmath as mp
from scipy.integrate import solve_bvp
mp.mp.dps = 50
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
def log_grid(rc,ri,N): x=np.linspace(math.log(rc),math.log(ri),N); return np.exp(x)

def eig_scaled(rg,Th0,phi,xi,kappa,gwell=1.0,nev=4):
    """gwell scales the WELL (the Q & Rmix curvature pieces). gwell=1 full native,
       gwell=0 kinetic-only. Built with a Cholesky-based symmetric reduction
       (positivity-safe)."""
    r=[mp.mpf(x) for x in rg]; Th=[mp.mpf(x) for x in Th0]; ph=[mp.mpf(x) for x in phi]
    N=len(r); xi=mp.mpf(xi); kappa=mp.mpf(kappa); c=mp.mpf(TWO_PI_3); g=mp.mpf(gwell)
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
    dRm=[ (Rm[i+1]-Rm[i-1])/(r[i+1]-r[i-1]) if 0<i<N-1 else mp.mpf(0) for i in range(N)]
    Veff=[ g*(Q[i]-dRm[i]) for i in range(N) ]   # scale the WELL (curvature) by g
    n=N-2; Hm=mp.zeros(n); Wd=[None]*n
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

r_core=0.05; L=1.0
print("="*72)
print("CORRECTED CAUSAL TOGGLE: well-SCALE sweep g (g=0 kinetic-only -> g=1 native)")
print("  kinetic-only (g=0) MUST be positive box (omega^2*R^2 const); the native")
print("  well (g=1) is the physical operator. Tracks the sign continuously.")
print("="*72)
Rs=[r_core+10*L, r_core+18*L, r_core+30*L]
for p in [0.0,1.0,2.0]:
    print(f"\n----- depth p={p} -----")
    for g in [0.0, 0.5, 1.0]:
        print(f"  [well-scale g={g}]")
        for R in Rs:
            gR=solve_ground(r_core,R,1.0,1.0,p,N=1200)
            rg=log_grid(r_core,R,180); Tg=gR.sol(rg)[0]; phg,_=phi_bg(rg,p,R)
            ev=eig_scaled(rg,Tg,phg,1.0,1.0,gwell=g,nev=3)
            print(f"    R={R:6.2f}: omega^2={ev[0]:+.6e}  omega^2*R^2={ev[0]*R**2:+.4e}")
print("\nDONE toggle.")
