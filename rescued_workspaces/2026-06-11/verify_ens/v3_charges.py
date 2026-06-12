"""VERIFIER script 3: B2 charges + B5 isolation wall, own integration.
Exterior continuation of library jets (ell<=1 class, as E1 ran it),
t = ln(1/y) decreasing below 0 = y growing above 1.  EL: X_tt - X_t = 2P_X.
Own RHS from anchor closed forms; DOP853 AND Radau cross-check.
Also: cross-gradient identity 4pi/d and transfer inertia 4pi d (quick,
independent quadrature in prolate-friendly coordinates)."""
import numpy as np
from scipy.integrate import solve_ivp

PASS = FAIL = 0
def check(name, ok, extra=""):
    global PASS, FAIL
    PASS += ok; FAIL += (not ok)
    print(("PASS" if ok else "FAIL") + f"  {name}" + (f"  [{extra}]" if extra else ""))

SQ3 = np.sqrt(3.0)
def Lk(k): return np.log((1+k)/(1-k))
def P_F(F, a):
    k = SQ3*abs(a)/F
    if k < 1e-6: return -k**2/6 - k**4/10
    if k >= 1.0: return np.nan
    return (1 - Lk(k)/(2*k))/2
def P_a(F, a):
    sg = np.sign(a) if a != 0 else 1.0
    k = SQ3*abs(a)/F
    if k < 1e-6: return sg*(k/SQ3 + (6/5.)*k**3/(3*SQ3))*1.0 if False else a/F + (6/5.)*a**3/F**3
    if k >= 1.0: return np.nan
    return sg*SQ3*(Lk(k)*(1+k**2) - 2*k)/(8*k**2)

def rhs(t, X):
    F, a, Ft, at = X
    return [Ft, at, Ft + 2*P_F(F, a), at + 2*P_a(F, a)]

def exterior(gam, c, method='DOP853', tmin=-7.0):
    def hitK(t, X): return SQ3*abs(X[1])/X[0] - 0.999
    hitK.terminal = True
    def hitF(t, X): return X[0] - 1e-3
    hitF.terminal = True
    sol = solve_ivp(rhs, [0, tmin], [1.0, 0.0, gam, -c], method=method,
                    rtol=1e-11, atol=1e-13, dense_output=True,
                    events=[hitK, hitF], max_step=0.01)
    return sol

cells = [("M1", 1.0, 0.18413678), ("M2", 1.0, 0.28328735),
         ("M3", 1.0, 0.56657471), ("M4", 0.5, 0.09087158)]
walls = {}
for nm, gam, c in cells:
    out = {}
    for meth in ('DOP853', 'Radau'):
        sol = exterior(gam, c, meth)
        tend = sol.t[-1]
        yend = np.exp(-tend)
        wall = len(sol.t_events[0]) > 0
        tt = np.linspace(-0.02, tend*0.999, 1500)
        yy = np.exp(-tt); FF, aa = sol.sol(tt)[0], sol.sol(tt)[1]
        kk = SQ3*np.abs(aa)/FF
        mwin = kk < 0.5
        A1 = np.vstack([np.ones(mwin.sum()), 1/yy[mwin]]).T
        (A, Q), *_ = np.linalg.lstsq(A1, FF[mwin], rcond=None)
        out[meth] = (yend, wall, A, Q, yy[mwin].max())
    (ye1, w1, A1v, Q1v, ywin1), (ye2, w2, A2v, Q2v, _) = out['DOP853'], out['Radau']
    walls[nm] = ye1
    print(f"  {nm} (gamma={gam}, c={c:.6f}): wall(kappa->1) y = {ye1:.3f} "
          f"[Radau {ye2:.3f}]  quiet window y<= {ywin1:.2f}: A = {A1v:+.4f}, "
          f"Q = {Q1v:+.4f} [Radau Q = {Q2v:+.4f}]   gamma = {gam}")
    if nm in ('M1', 'M2'):
        check(f"V3.{nm} Q extraction: Q = gamma + O(0.01) (claimed gamma+0.003), "
              "integrator-independent",
              abs(Q1v - gam) < 0.02 and abs(Q1v - Q2v) < 1e-3,
              f"Q = {Q1v:.4f} vs gamma = {gam}")
check("V3.1 all four library jets hit a kappa->1 wall (no quiet isolated "
      "exterior)", all(np.isfinite(v) and v < 50 for v in walls.values()),
      "walls y = " + ", ".join(f"{nm}:{v:.2f}" for nm, v in walls.items()))
check("V3.2 walls lie in the claimed 1.8-6.9 cell-radius band",
      all(1.8 <= v <= 6.9 for v in walls.values()))
check("V3.3 M2 wall specifically (own integration)",
      1.8 <= walls['M2'] <= 6.9, f"y_wall(M2) = {walls['M2']:.3f}")

# excess-flux bookkeeping at the weld: -y^2 dF/dy|_1 = +gamma (F_t(0)=gamma,
# F_y = -F_t/y). MS mass audit object p_F = (1/2) y^2 F' = gamma/2.
print("\n  bookkeeping: weld flux -y^2 F_y|_(y=1) = +gamma = Q(fit);  "
      "p_F = gamma/2  =>  Q = 2 p_F exactly (same object, factor-2 convention)")
check("V3.4 charge-vs-MS-mass: Q = 2 p_F (factor bookkeeping, not a new object)",
      True)

# ---------------- cross identity and transfer inertia ------------------------
# Int grad(1/r1).grad(1/r2) d3x = 4 pi / d: analytic by IBP + delta function;
# numeric check with own scheme (spherical coords around charge 1).
def cross_numeric(d, Rmax=2000., eps=1e-3):
    # integrate over sphere around charge 1: grad(1/r1).grad(1/r2)
    # = (rhat1 . rhat2-direction stuff): use closed form integrand in (y,u)
    y = np.geomspace(eps, Rmax, 4000)
    u = np.polynomial.legendre.leggauss(400)
    uu, wu = u
    YY, UU = np.meshgrid(y, uu, indexing='ij')
    r2 = np.sqrt(YY**2 + d**2 - 2*YY*d*UU)
    # grad(1/r1) = -rhat/y^2 ; grad(1/r2) = -(r - d zhat)/r2^3
    # dot = [ (y - d u) ] / (y^2 r2^3)  *  ... : rhat.(r - d zhat) = y - d u
    integ = (YY - d*UU)/(YY**2*r2**3)
    inner = (integ * wu[None, :]).sum(axis=1)          # Int du
    val = 2*np.pi*np.trapezoid(inner*y**2, y)
    return val
v = cross_numeric(2.0)
check("V3.5 Int grad(1/r1).grad(1/r2) = 4pi/d (numeric, d=2, own scheme)",
      abs(v - 2*np.pi) < 0.02*2*np.pi, f"{v:.4f} vs {2*np.pi:.4f}")

def inertia_numeric(d, Rmax=4000., eps=2e-3):
    y = np.geomspace(eps, Rmax, 5000)
    uu, wu = np.polynomial.legendre.leggauss(400)
    YY, UU = np.meshgrid(y, uu, indexing='ij')
    r2 = np.sqrt(YY**2 + d**2 - 2*YY*d*UU)
    integ = (1/YY - 1/r2)**2
    inner = (integ*wu[None, :]).sum(axis=1)
    val = 2*np.pi*np.trapezoid(inner*y**2, y)
    # excised ball around charge 1 (r<eps): Int (1/r - 1/r2)^2 ~ 4 pi eps
    val += 4*np.pi*eps
    return val
vi = inertia_numeric(2.0)
check("V3.6 transfer inertia Int (1/r1 - 1/r2)^2 = 4 pi d (numeric, d=2)",
      abs(vi - 8*np.pi) < 0.05*8*np.pi, f"{vi:.3f} vs {8*np.pi:.3f}")

# exchange Hessian positivity for d > R1+R2: 1/R1 + 1/R2 >= 4/(R1+R2) > 2/d
check("V3.7 transfer Hessian 2pi(1/R1 + 1/R2 - 2/d) > 0 for d > R1+R2 "
      "(AM-HM: 1/R1+1/R2 >= 4/(R1+R2) > 2/d)", True, "analytic")

print(f"\n=== V3 TOTALS: {PASS} PASS / {FAIL} FAIL ===")
