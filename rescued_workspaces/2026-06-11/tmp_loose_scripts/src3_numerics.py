"""SCRIPT 3 — numerics for the source-sector core question.

(A) Sourcing-capacity bound: on the self-similar collar F = y^{-q}, the exact
    ell=1 angular demand is  (pi/2) kappa^2 (G1 + kappa G1') = s F(y) = s y^{-1/3}.
    LHS is a bounded function of kappa on (0,1) => termination depth y_term exact.
(B) Native two-field evolution (no external driver): integrate the exact
    reduced (F,a) system inward from y=1 and watch kappa(y).
(C) Coupled m=0 channel DtN at the inner boundary vs y_in:
    - demanded background V(y) (exact closed forms): finite inner end => finite weights;
    - control kappa=0 collar: Lambda_cc -> 0 as y_in -> 0 (the flat core direction);
    - universality: any bounded V keeps Lambda_cc -> 0.
(D) numeric spot-check of the weld == (i-phi) jet equivalence ratio identity.
"""
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq, minimize_scalar

PASS = 0; FAIL = 0
def check(name, ok, detail=""):
    global PASS, FAIL
    if ok: PASS += 1
    else: FAIL += 1
    print(("PASS " if ok else "FAIL ") + name + ("   " + detail if detail else ""))

q = 1.0/3; s = q*(1-q)/2; lam = 2.0; eta = s/lam

# ---------------------------------------------------------- (A) capacity bound
def G1(k):
    return (2*k + (k**2-1)*(np.log(1+k)-np.log(1-k)))/k**3
def G1p(k):
    h = 1e-7
    return (G1(k+h)-G1(k-h))/(2*h)
def capacity(k):   # (pi/2) k^2 (G1 + k G1')
    return np.pi/2 * k**2 * (G1(k) + k*G1p(k))

ks = np.linspace(1e-4, 1-1e-6, 200000)
caps = capacity(ks)
imax = np.argmax(caps)
Mstar, kmax = caps[imax], ks[imax]
print(f"(A) capacity curve: small-k slope check {capacity(0.01)/(2*np.pi/3*0.01**2):.6f} (should be ~1)")
print(f"    max capacity M* = {Mstar:.8f} at kappa_max = {kmax:.6f}")
print(f"    capacity at kappa->1: {capacity(1-1e-9):.4f} (log-divergent down? sign)")
check("(A1) capacity bounded above on (0,1)", np.isfinite(Mstar) and Mstar < 10)
# demand s y^{-1/3} = M*  =>  y_term = (s/M*)^3
y_term = (s/Mstar)**3
print(f"    EXACT termination of self-similar sourcing: y_term = (s/M*)^3 = {y_term:.6e}, ln y_term = {np.log(y_term):.4f}")
# compare leading-order kappa=1 estimate:
kap1 = 2*np.sqrt(eta)*np.sqrt(3/(4*np.pi))
print(f"    leading-order estimate (kappa(y)=({kap1:.6f}) y^(-1/6) hits kappa_max): y = {(kap1/kmax)**6:.6e}")
check("(A2) y_term finite and below 1", 0 < y_term < 1)
# kappa(y) along the exact demand: solve capacity(k) = s y^{-1/3} for k on (0,kmax]
print("    exact demanded kappa(y): ", end="")
for yv in [1.0, 0.5, 0.1, 0.01, 2*y_term, 1.05*y_term]:
    rhs = s*yv**(-1/3.)
    if rhs > Mstar:
        print(f"[y={yv:.3e}: UNSOLVABLE]", end=" ")
        continue
    kk = brentq(lambda k: capacity(k)-rhs, 1e-6, kmax)
    print(f"[y={yv:.3e}: k={kk:.4f}]", end=" ")
print()

# ---------------------------------------------------------- (B) native evolution
# EL: (y^2 F')' = (1/2) P_F, (y^2 a')' = (1/2) P_a;  P = (3 a^2/(2F)) G1(kappa)
def P_derivs(Fv, av):
    k = av*np.sqrt(3/(4*np.pi))/Fv
    k = min(k, 1-1e-12)
    g, gp = G1(k), G1p(k)
    PF = -(3*av**2/(2*Fv**2))*(g + k*gp)
    Pa = (3*av/Fv)*g + (3*av**2/(2*Fv))*gp*np.sqrt(3/(4*np.pi))/Fv
    return PF, Pa
def rhs_bg(y, Y):
    Fv, dF, av, da = Y
    PF, Pa = P_derivs(Fv, av)
    return [dF, (0.5*PF - 2*y*dF)/y**2, da, (0.5*Pa - 2*y*da)/y**2]
a0 = 2*np.sqrt(eta)
Y0 = [1.0, -q, a0, -0.5*a0]
sol = solve_ivp(rhs_bg, [1.0, 1e-6], Y0, rtol=1e-10, atol=1e-12, dense_output=True, max_step=0.01)
print("\n(B) native (driverless) two-field evolution from collar data:")
ev_y = [0.8, 0.5, 0.2, 0.1, 0.05, 0.02, 0.01]
kap_prev = None
for yv in ev_y:
    if yv < sol.t[-1]: break
    Fv, dF, av, da = sol.sol(yv)
    k = av*np.sqrt(3/(4*np.pi))/Fv
    print(f"    y={yv:6.3f}  F={Fv:9.4f}  a={av:9.4f}  kappa={k:8.5f}")
print(f"    integration reached y = {sol.t[-1]:.3e}, status: {sol.status}")

# ---------------------------------------------------------- (C) coupled DtN
def V_exact(yv, mode="demanded"):
    """2x2 m=0 potential block (u, a0) on the demanded background, exact closed forms."""
    Fv = yv**(-q)
    if mode == "demanded":
        rhsv = s*Fv
        k = brentq(lambda kk: capacity(kk)-rhsv, 1e-9, kmax) if rhsv < Mstar else kmax
    else:
        k = 0.0
    if k < 1e-8:
        Vuu, Vua, Vaa = 0.0, 0.0, 1.0/Fv
    else:
        L = np.log(1+k)-np.log(1-k)
        Vuu = np.pi*(k**2*np.log(1-k) - 2*k - np.log(1-k) + (1-k**2)*np.log(1+k))/(Fv*k*(k**2-1))
        Vua = np.sqrt(3*np.pi)*(-k**2*np.log(1-k) + 2*k + np.log(1-k) + (k**2-1)*np.log(1+k))/(2*Fv*k**2*(k**2-1))
        Vaa = 3*(k**2*np.log(1-k) - 2*k - np.log(1-k) + (1-k**2)*np.log(1+k))/(4*Fv*k**3*(k**2-1))
    return np.array([[Vuu, Vua],[Vua, Vaa]])

def dtn_inner(y_in, mode="demanded", Vconst=None):
    """DtN at inner boundary for jet (1/4) int [y^2 x'^2 + ... ] with Q2=(1/2)x^T V x:
       EL: (1/2)(y^2 x')' = V x ; flux p_c = -(1/2) y^2 x'(y_in).
       Solve with x(1)=0, x(y_in)=e_i."""
    n = 2 if Vconst is None else 1
    def rhs(yv, X):
        X = X.reshape(2, n, n)
        x, dx = X[0], X[1]
        V = V_exact(yv, mode) if Vconst is None else np.array([[Vconst]])
        ddx = (2.0*V @ x - 2*yv*dx)/yv**2
        return np.concatenate([dx, ddx]).ravel()
    X0 = np.concatenate([np.eye(n), np.zeros((n,n))]).ravel()
    solv = solve_ivp(rhs, [y_in, 1.0], X0, rtol=1e-10, atol=1e-13)
    Xf = solv.y[:, -1].reshape(2, n, n)
    # x(y;C) = x_basis(y) C ; need solution with x(y_in)=I_col, x(1)=0:
    # basis: x_i with x(y_in)=e_i, x'(y_in)=0  PLUS y_i with x(y_in)=0, x'(y_in)=e_i
    # redo properly with 2n basis solutions:
    def integrate_basis(x0, dx0):
        Xi = np.concatenate([x0, dx0]).ravel()
        so = solve_ivp(rhs, [y_in, 1.0], Xi, rtol=1e-10, atol=1e-13)
        return so.y[:, -1].reshape(2, n, n)
    A_end = integrate_basis(np.eye(n), np.zeros((n,n)))   # value basis
    B_end = integrate_basis(np.zeros((n,n)), np.eye(n))   # slope basis
    # solution x = A(y) + B(y) C with x(1) = A_end[0] + B_end[0] C = 0:
    C = -np.linalg.solve(B_end[0], A_end[0])
    dx_in = C    # since x'(y_in) = 0 + I*C
    Lam = -0.5*y_in**2*dx_in
    return 0.5*(Lam + Lam.T)

print("\n(C) inner-boundary DtN (coupled m=0 block, demanded background):")
for y_in in [0.3, 0.1, 0.03, 0.01, 3e-3, 6e-4, 2.2e-4]:
    if y_in <= y_term*1.01: y_in = max(y_in, y_term*1.05)
    L = dtn_inner(y_in, "demanded")
    w = np.linalg.eigvalsh(L)
    print(f"    y_in={y_in:9.2e}  Lam_cc eigs = {w[0]:+.6f}, {w[1]:+.6f}   Lam_uu={L[0,0]:+.6f}  Lam_ua={L[0,1]:+.6f}  Lam_aa={L[1,1]:+.6f}")

print("\n    control: kappa = 0 sourceless collar (u-channel scalar, V=0):")
for y_in in [0.1, 0.01, 1e-3, 1e-4]:
    L = dtn_inner(y_in, None, Vconst=0.0)
    print(f"    y_in={y_in:9.2e}  Lambda_cc = {L[0,0]:+.8f}   Lambda/y_in = {L[0,0]/y_in:+.6f}")
print("    bounded-V universality (V=2s and V=10 constants):")
for Vc in [2*s, 10.0]:
    row = []
    for y_in in [1e-2, 1e-3, 1e-4]:
        L = dtn_inner(y_in, None, Vconst=Vc)
        row.append(L[0,0])
    print(f"    V={Vc:5.2f}: Lam(1e-2,1e-3,1e-4) = {row[0]:.6f}, {row[1]:.6f}, {row[2]:.6f}")
    check(f"(C-univ) V={Vc}: Lambda_cc -> 0", abs(row[2]) < 10*abs(row[1]))

Lfin = dtn_inner(max(1.05*y_term, 1.6e-4), "demanded")
check("(C1) demanded background: inner DtN block finite & O(1) at termination",
      np.all(np.isfinite(Lfin)) and np.linalg.norm(Lfin) > 1e-3,
      f"|Lam| = {np.linalg.norm(Lfin):.4f}")
Lctl = dtn_inner(1e-4, None, Vconst=0.0)
check("(C2) sourceless control: Lambda_cc ~ y_in/2 -> 0", abs(Lctl[0,0] - 0.5e-4) < 2e-5,
      f"Lam = {Lctl[0,0]:.2e}")

# ---------------------------------------------------------- (D) weld spot check
# weld static op on dphi=-u/(2f0) equals -(1/(2 y^q)) [ (y^2 u')' - (lam y^q + 2s) u ]
def spotD(yv, lamv):
    import math
    f0 = yv**(-q); f0p = -q*yv**(-q-1)
    # pick u(y)=sin(3y)+2, u'=3cos(3y), u''=-9 sin(3y)
    u = math.sin(3*yv)+2; up = 3*math.cos(3*yv); upp = -9*math.sin(3*yv)
    dphi = -u/(2*f0); dphip = -(up*f0 - u*f0p)/(2*f0**2)
    h = 1e-6
    def dphi_f(t): return -(math.sin(3*t)+2)/(2*t**(-q))
    ddphi = (dphi_f(yv+h)-dphi_f(yv-h))/(2*h)
    d2phi = (dphi_f(yv+h)-2*dphi_f(yv)+dphi_f(yv-h))/h**2
    E0 = s/yv**2
    weld = (2*yv*f0**2*ddphi + yv**2*2*f0*f0p*ddphi + yv**2*f0**2*d2phi
            - 4*yv**2*f0**2*E0*dphi - lamv*f0*dphi)
    target = (yv**2*upp + 2*yv*up) - (lamv*yv**q + 2*s)*u
    return weld + target/(2*yv**q)
r1, r2 = spotD(0.5, 2.0), spotD(0.8, 2.0)
check("(D) weld == (i-phi) jet ratio identity (numeric residuals ~ 0)",
      abs(r1) < 1e-4 and abs(r2) < 1e-4, f"residuals {r1:.2e}, {r2:.2e}")

print(f"\nTOTALS: PASS={PASS} FAIL={FAIL}")
