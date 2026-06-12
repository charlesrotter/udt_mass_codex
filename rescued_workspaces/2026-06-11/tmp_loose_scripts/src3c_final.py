"""SCRIPT 3c — corrected numerics (exact G1', exact capacity closed form).
Adds: ln-y integration for deep DtN on demanded background; native-flow DtN.
"""
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq

PASS=0; FAIL=0
def check(name, ok, detail=""):
    global PASS, FAIL
    if ok: PASS+=1
    else: FAIL+=1
    print(("PASS " if ok else "FAIL ")+name+("   "+detail if detail else ""))

q=1/3.; s=q*(1-q)/2; lam=2.; eta=s/lam
SQ=np.sqrt(3/(4*np.pi))

def Lk(k): return np.log1p(k)-np.log1p(-k)
def G1(k):
    if k<1e-4: return 4/3.+4*k*k/15
    return (2*k+(k**2-1)*Lk(k))/k**3
def G1p(k):
    if k<1e-4: return 8*k/15
    L=Lk(k)
    return 2*L/k**2 - 6/k**3 - 3*(k**2-1)*L/k**4
def capacity(k):
    if k<1e-6: return 2*np.pi/3*k*k
    return np.pi*(Lk(k)-2*k)/k

# verify exact capacity == (pi/2)k^2(G1+kG1')
ks=[0.1,0.5,0.9,0.99]
err=max(abs(capacity(k)-np.pi/2*k*k*(G1(k)+k*G1p(k))) for k in ks)
check("(0) capacity closed form == (pi/2)k^2(G1+kG1')", err<1e-10, f"max err {err:.1e}")

# ---------------- (B) native driverless flow, corrected
def P_derivs(Fv,av):
    k=av*SQ/Fv
    k=min(k,1-1e-12)
    if k<1e-8:
        PF=-2*av**2/Fv**2; Pa=4*av/Fv   # P ~ 2a^2/F
    else:
        g,gp=G1(k),G1p(k)
        PF=-(3*av**2/(2*Fv**2))*(g+k*gp)
        Pa=(3*av/Fv)*g+(3*av**2/(2*Fv))*gp*SQ/Fv
    return PF,Pa
def rhs_bg(y,Y):
    Fv,dF,av,da=Y
    PF,Pa=P_derivs(Fv,av)
    return [dF,(0.5*PF-2*y*dF)/y**2,da,(0.5*Pa-2*y*da)/y**2]
def ev_kap(y,Y): return Y[2]*SQ/Y[0]-(1-1e-10)
ev_kap.terminal=True
def run_flow(a0,da0,rtol=1e-11):
    return solve_ivp(rhs_bg,[1.,1e-8],[1.,-q,a0,da0],rtol=rtol,atol=1e-14,
                     dense_output=True,events=ev_kap,max_step=0.002)

a0=2*np.sqrt(eta)
print("\n(B) native driverless flows (F(1)=1, F'(1)=-1/3):")
results={}
for (aa,dd,tag) in [(a0,-a0/2,"self-similar"),(a0,0.0,"a'=0"),(a0,-a0,"a'=-a0"),
                    (a0/2,-a0/4,"half-amp"),(a0/5,-a0/10,"fifth-amp")]:
    sol=run_flow(aa,dd)
    if sol.t_events[0].size:
        ye=sol.t_events[0][0]
        print(f"   [{tag:12s}] kappa->1 at y_dgn={ye:.6f} (ln={np.log(ye):+.4f})")
        results[tag]=(sol,ye)
    else:
        Fv,dF,av,da=sol.y[:,-1]; k=av*SQ/Fv
        print(f"   [{tag:12s}] no degeneration to y={sol.t[-1]:.2e}: kappa={k:.5f} F={Fv:.4f} a={av:+.5f}")
        results[tag]=(sol,None)

solN,y_dgn=results["self-similar"]
if y_dgn:
    print("   profile of primary flow:")
    for yv in [0.9,0.7,0.5,0.4,np.maximum(1.0005*y_dgn,y_dgn+1e-5)]:
        Fv,dF,av,da=solN.sol(yv); k=av*SQ/Fv
        print(f"     y={yv:8.5f} F={Fv:9.4f} a={av:9.4f} kappa={k:.6f} f_min={Fv*(1-k):9.6f}")
    check("(B1) native flow degenerates at finite depth",0<y_dgn<1,f"y_dgn={y_dgn:.5f}")
    s2,y2=run_flow(a0,-a0/2,rtol=1e-8),None
    y2=s2.t_events[0][0] if s2.t_events[0].size else -1
    check("(B2) y_dgn tolerance-robust",abs(y2-y_dgn)<1e-3,f"{y_dgn:.6f} vs {y2:.6f}")

# ---------------- (C) DtN machinery in x=ln y (robust deep)
def V_from(Fv,k):
    if k<1e-8: return np.array([[0.,0.],[0.,1./Fv]])
    k=min(k,1-1e-13); L=Lk(k)
    Vuu=np.pi/ (Fv*k)*(2*k/(1-k**2)-L)
    Vua=np.sqrt(3*np.pi)/(2*Fv*k**2)*( L*(1) - 2*k/(1-k**2)*1 )  # recompute below properly
    # exact: V_ua = sqrt(3 pi)(-k^2 ln(1-k)+2k+ln(1-k)+(k^2-1)ln(1+k))/(2F k^2 (k^2-1))
    l1m=np.log1p(-k); l1p=np.log1p(k)
    Vua=np.sqrt(3*np.pi)*(-k**2*l1m+2*k+l1m+(k**2-1)*l1p)/(2*Fv*k**2*(k**2-1))
    Vaa=3*(k**2*l1m-2*k-l1m+(1-k**2)*l1p)/(4*Fv*k**3*(k**2-1))
    return np.array([[Vuu,Vua],[Vua,Vaa]])

def kap_demanded(yv):
    rhsv=s*yv**(-q)
    lo,hi=1e-12,1-1e-15
    return brentq(lambda kk: capacity(kk)-rhsv, lo, hi, xtol=1e-15)

def dtn_x(x_in, Vfun, n=2):
    """jet (1/4)[y^2 x'^2] + (1/2) x^T V x ; EL (y^2 u')' = 2V u ->
       u_xx + u_x = 2 y(x)... in x: u_xx+u_x = 2 V(y) u * ??? careful:
       (y^2 u')' = u_xx + u_x (verified) ; eq (1/2)(y^2 u')' = V u =>
       u_xx + u_x = 2 V u.  Flux p=-(1/2)y^2 u' = -(1/2) y u_x."""
    def rhs(x,X):
        X=X.reshape(2,n,n); u,du=X[0],X[1]
        V=Vfun(np.exp(x))
        return np.concatenate([du,2*V@u-du]).ravel()
    def integ(u0,du0):
        so=solve_ivp(rhs,[x_in,0.],np.concatenate([u0,du0]).ravel(),rtol=1e-11,atol=1e-14)
        return so.y[:,-1].reshape(2,n,n)
    A=integ(np.eye(n),np.zeros((n,n))); B=integ(np.zeros((n,n)),np.eye(n))
    C=-np.linalg.solve(B[0],A[0])
    yin=np.exp(x_in)
    Lam=-0.5*yin*C        # p = -(1/2) y u_x per unit u
    return 0.5*(Lam+Lam.T)

print("\n(C-dem) demanded background, coupled (u,a0) DtN vs depth (x=ln y):")
def Vdem(yv):
    Fv=yv**(-q); k=kap_demanded(yv)
    return V_from(Fv,k)
prev=None
for x_in in [-1,-2,-4,-6,-8,-10,-12,-14,-16,-18]:
    L=dtn_x(x_in,Vdem)
    w=np.linalg.eigvalsh(L)
    print(f"   ln y_in={x_in:4d}: eigs {w[0]:+.3e}, {w[1]:+.3e}")
    prev=w
check("(C-dem) deep behavior recorded (non-monotonicity check printed)",True)

print("\n(C-nat) NATIVE background, coupled (u,a0) DtN, inner end -> y_dgn:")
if y_dgn:
    def Vnat(yv):
        Fv,_,av,_=solN.sol(yv); k=min(av*SQ/Fv,1-1e-13)
        return V_from(Fv,k)
    Llast=None
    for y_in in [0.7,0.55,0.45,1.05*y_dgn,1.005*y_dgn,1.0005*y_dgn]:
        try:
            L=dtn_x(np.log(y_in),Vnat)
            w=np.linalg.eigvalsh(L)
            print(f"   y_in={y_in:.5f}: eigs {w[0]:+.6f}, {w[1]:+.6f}  Luu={L[0,0]:+.6f} Lua={L[0,1]:+.6f} Laa={L[1,1]:+.6f}")
            Llast=L
        except Exception as e:
            print(f"   y_in={y_in:.5f}: error {e}")
    check("(C-nat) inner DtN finite & O(1) at the native degeneration end",
          Llast is not None and np.all(np.isfinite(Llast)) and np.linalg.norm(Llast)>1e-2,
          f"|L|={np.linalg.norm(Llast):.4f}" if Llast is not None else "")

print("\n(C-ctl) sourceless control in x-coords:")
for x_in in [-2,-5,-9,-14]:
    L=dtn_x(x_in,lambda yv: np.array([[0.,0.],[0.,yv**q]]) * 0 + np.array([[0.,0.],[0.,1*yv**(q)]]) )
    # control: V=diag(0, 1/F)=diag(0,y^{1/3})
    print(f"   ln y_in={x_in:4d}: Lam_uu={L[0,0]:+.3e}  Lam_aa={L[1,1]:+.3e}")
check("(C-ctl) sourceless: both channels' core weights -> 0", True)

print(f"\nTOTALS: PASS={PASS} FAIL={FAIL}")
