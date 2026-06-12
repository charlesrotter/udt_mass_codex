"""SCRIPT 3b — refined numerics.
(A') capacity asymptote: capacity(k) ~ pi ln(2/(1-k)) + C as k->1  => demanded
     background never terminates at finite y; instead f_min = F(1-kappa) -> 0
     (asymptotic degeneration).  Quantify.
(B') native driverless flow: locate the finite degeneration depth y_dgn
     (kappa -> 1) precisely; robustness across initial a' and amplitude.
(C') coupled DtN on the NATIVE background at its own inner end: finite block.
(D') exact-derivative weld identity spot check.
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
SQ = np.sqrt(3/(4*np.pi))

def G1(k):  return (2*k+(k**2-1)*(np.log1p(k)-np.log1p(-k)))/k**3
def G1p(k):
    num = 2*k*(np.log1p(k)-np.log1p(-k)) - 2
    return num/k**3 - 3*(2*k+(k**2-1)*(np.log1p(k)-np.log1p(-k)))/k**4
def capacity(k): return np.pi/2*k**2*(G1(k)+k*G1p(k))

print("(A') capacity asymptote vs pi*ln(2/(1-k)):")
for k in [0.9, 0.99, 0.999, 0.9999999]:
    cap = capacity(k); asym = np.pi*np.log(2/(1-k))
    print(f"    k={k}: capacity={cap:10.4f}  pi ln(2/(1-k))={asym:10.4f}  diff={cap-asym:+.4f}")
d1 = capacity(0.999)-np.pi*np.log(2/(1-0.999))
d2 = capacity(0.9999999)-np.pi*np.log(2/(1-0.9999999))
check("(A'1) capacity - pi ln(2/(1-k)) -> finite const", abs(d2-d1) < 0.05, f"const ~ {d2:+.4f}")
# demanded background: capacity(kappa(y)) = s y^{-1/3}:
# => 1-kappa ~ 2 exp(-(s y^{-1/3} - C)/pi):  f_min = y^{-1/3}(1-kappa) -> 0 (no finite termination).
C0 = d2
print(f"    demanded f_min(y) ~ 2 y^(-1/3) exp(-(s y^(-1/3) - {C0:.3f})/pi)  -> 0 only as y->0 (asymptotic degeneration)")

# exact G1' spot-check against FD
k=0.5; h=1e-7
check("(A'2) analytic G1' correct", abs(G1p(k)-(G1(k+h)-G1(k-h))/(2*h))<1e-5)

# ---------------- (B') native flow
def P_derivs(Fv,av):
    k = av*SQ/Fv
    if k>=1: raise ValueError("degenerate")
    g, gp = G1(k), G1p(k)
    PF = -(3*av**2/(2*Fv**2))*(g+k*gp)
    Pa = (3*av/Fv)*g + (3*av**2/(2*Fv))*gp*SQ/Fv
    return PF, Pa
def rhs_bg(y,Y):
    Fv,dF,av,da = Y
    PF,Pa = P_derivs(Fv,av)
    return [dF,(0.5*PF-2*y*dF)/y**2, da,(0.5*Pa-2*y*da)/y**2]
def kap_event(y,Y):
    return Y[2]*SQ/Y[0] - (1-1e-9)
kap_event.terminal=True; kap_event.direction=1

def run_flow(a0, da0, rtol=1e-11):
    Y0=[1.,-q,a0,da0]
    sol=solve_ivp(rhs_bg,[1.,1e-6],Y0,rtol=rtol,atol=1e-13,dense_output=True,
                  events=kap_event,max_step=0.005)
    return sol

a0 = 2*np.sqrt(eta)
print("\n(B') native driverless flow, collar data F=1, F'=-1/3:")
for (aa,dd,tag) in [(a0,-a0/2,"self-similar a'"),(a0,0.,"a'=0"),(a0,-a0,"a'=-a0"),
                    (a0/2,-a0/4,"half amplitude"),(a0/5,-a0/10,"fifth amplitude")]:
    try:
        sol=run_flow(aa,dd)
        if sol.t_events[0].size:
            ye=sol.t_events[0][0]
            Fv,dF,av,da = sol.sol(ye*1.0000001) if ye<1 else sol.y[:,-1]
            print(f"    [{tag:16s}] kappa->1 at y_dgn = {ye:.6f}  (F={Fv:.3f})")
        else:
            Fv,dF,av,da=sol.y[:,-1]
            k=av*SQ/Fv
            print(f"    [{tag:16s}] no degeneration; reached y={sol.t[-1]:.2e}, kappa={k:.4f}, F={Fv:.4f}, a={av:.4f}")
    except Exception as e:
        print(f"    [{tag:16s}] integration error: {e}")

solN = run_flow(a0,-a0/2)
y_dgn = solN.t_events[0][0] if solN.t_events[0].size else None
if y_dgn:
    print(f"    primary flow: y_dgn = {y_dgn:.6f}, ln y_dgn = {np.log(y_dgn):.4f}")
    for yv in [0.9,0.7,0.5,0.4,0.35,y_dgn*1.001]:
        Fv,dF,av,da=solN.sol(yv)
        k=av*SQ/Fv
        print(f"      y={yv:.4f}  F={Fv:8.4f}  a={av:8.4f}  kappa={k:.5f}  f_min={Fv*(1-k):8.5f}")
    check("(B'1) native flow degenerates at finite depth", 0<y_dgn<1, f"y_dgn={y_dgn:.4f}")

# tolerance robustness
sol2 = run_flow(a0,-a0/2,rtol=1e-8)
y2 = sol2.t_events[0][0] if sol2.t_events[0].size else -1
check("(B'2) y_dgn tolerance-robust", abs(y2-y_dgn)<1e-4, f"{y_dgn:.6f} vs {y2:.6f}")

# ---------------- (C') coupled DtN on the NATIVE background
def V_from(Fv, k):
    if k<1e-10: return np.array([[0.,0.],[0.,1./Fv]])
    l1m=np.log1p(-k); l1p=np.log1p(k)
    Vuu=np.pi*(k**2*l1m-2*k-l1m+(1-k**2)*l1p)/(Fv*k*(k**2-1))
    Vua=np.sqrt(3*np.pi)*(-k**2*l1m+2*k+l1m+(k**2-1)*l1p)/(2*Fv*k**2*(k**2-1))
    Vaa=3*(k**2*l1m-2*k-l1m+(1-k**2)*l1p)/(4*Fv*k**3*(k**2-1))
    return np.array([[Vuu,Vua],[Vua,Vaa]])

def dtn_native(y_in):
    n=2
    def rhs(yv,X):
        X=X.reshape(2,n,n); x,dx=X[0],X[1]
        Fv,_,av,_ = solN.sol(yv)
        k=min(av*SQ/Fv,1-1e-12)
        V=V_from(Fv,k)
        return np.concatenate([dx,(2*V@x-2*yv*dx)/yv**2]).ravel()
    def integ(x0,dx0):
        so=solve_ivp(rhs,[y_in,1.],np.concatenate([x0,dx0]).ravel(),rtol=1e-10,atol=1e-13)
        return so.y[:,-1].reshape(2,n,n)
    A=integ(np.eye(n),np.zeros((n,n))); B=integ(np.zeros((n,n)),np.eye(n))
    Cm=-np.linalg.solve(B[0],A[0])
    L=-0.5*y_in**2*Cm
    return 0.5*(L+L.T)

if y_dgn:
    print("\n(C') coupled (u,a0) DtN on the NATIVE background, inner end -> y_dgn:")
    for y_in in [0.6,0.45,0.38,0.345,1.02*y_dgn,1.002*y_dgn]:
        try:
            L=dtn_native(y_in)
            w=np.linalg.eigvalsh(L)
            print(f"    y_in={y_in:.5f}: eigs {w[0]:+.6f}, {w[1]:+.6f}  Luu={L[0,0]:+.6f} Lua={L[0,1]:+.6f} Laa={L[1,1]:+.6f}")
            Llast=L
        except Exception as e:
            print(f"    y_in={y_in:.5f}: error {e}")
    check("(C'1) native-background inner DtN finite & O(1) near degeneration",
          np.all(np.isfinite(Llast)) and np.linalg.norm(Llast)>1e-2,
          f"|L|={np.linalg.norm(Llast):.4f}")

# ---------------- (D') exact weld spot check
import sympy as sp
yv=sp.Symbol('y',positive=True)
u=sp.sin(3*yv)+2; f0=yv**(-sp.Rational(1,3)); ss=sp.Rational(1,9); lamv=2
dphi=-u/(2*f0)
E0=ss/yv**2
weld=sp.diff(yv**2*f0**2*sp.diff(dphi,yv),yv)-4*yv**2*f0**2*E0*dphi-lamv*f0*dphi
target=sp.diff(yv**2*sp.diff(u,yv),yv)-(lamv*yv**sp.Rational(1,3)+2*ss)*u
resid=sp.simplify(weld + target/(2*yv**sp.Rational(1,3)))
check("(D') weld == -(1/(2 y^q)) [(y^2 u')' - (lam y^q + 2s)u] EXACT on witness", resid==0)

print(f"\nTOTALS: PASS={PASS} FAIL={FAIL}")
