"""
INDEPENDENT verifier of the lepton-soliton spectrum.
Energy functional (verified to match doc, spatial measure e^{phi} r^2 sin th, m=1):
  E2_r = (2pi xi/3) e^{-phi}[ r^2 sin^2Th Th'^2 + 2 r^2 Th'^2 + 4 e^{2phi} sin^2Th ]
  E4_r = (2pi kap/3) e^{-phi}[ (2 r^2 sin^4Th + 2 r^2 sin^2Th) Th'^2 + e^{2phi} sin^4Th ]/r^2
Work in xi=kap=1. Density e(r) = a(r,Th) Th'^2 + b(r,Th)  with
  a = (2pi/3) e^{-phi}[ r^2 sin^2Th + 2 r^2 + (2 sin^4Th + 2 sin^2Th) ]
  b = (2pi/3) e^{-phi}[ 4 e^{2phi} sin^2Th + e^{2phi} sin^4Th / r^2 ]
EOM: d/dr(2 a Th') = a_Th Th'^2 + b_Th   (Euler-Lagrange).
phi background: flat (p=0) or log cell phi = -p ln(r_int/r)  (deep core).

RESCUE ATTEMPTS:
  A) static excited solitons (extra nodes) via shooting + multi-seed relaxation
  B) breathing Hessian spectrum omega_n^2 (Sturm-Liouville), O(1) vs exponential
  C) Koide Q under three readings
agent: blind-verifier 2026-06-14
"""
import numpy as np
from scipy.integrate import solve_bvp
from scipy.linalg import eigh
import sympy as sp

# ---- build a,b and their Th-derivatives symbolically (xi=kap=1), generic phi ----
r_s, Th_s, p_s = sp.symbols('r Th p', real=True)   # p = phi value (background, given)
TWO_PI_3 = 2*sp.pi/3
S = sp.sin(Th_s)
ep = sp.exp(p_s)            # e^{phi}
a_sym = TWO_PI_3*sp.exp(-p_s)*(r_s**2*S**2 + 2*r_s**2 + 2*S**4 + 2*S**2)
b_sym = TWO_PI_3*sp.exp(-p_s)*(4*ep**2*S**2 + ep**2*S**4/r_s**2)
a_Th = sp.diff(a_sym, Th_s)
b_Th = sp.diff(b_sym, Th_s)
a_r = sp.diff(a_sym, r_s)   # explicit r-dependence (phi treated as fn of r externally)

# lambdify with phi(r) and phi'(r) passed in (we substitute p=phi(r); a_r needs dphi too)
af = sp.lambdify((r_s, Th_s, p_s), a_sym, 'numpy')
bf = sp.lambdify((r_s, Th_s, p_s), b_sym, 'numpy')
aThf = sp.lambdify((r_s, Th_s, p_s), a_Th, 'numpy')
bThf = sp.lambdify((r_s, Th_s, p_s), b_Th, 'numpy')
# da/dr total = a_r|explicit + da/dp * phi'(r); da/dp:
a_p = sp.diff(a_sym, p_s)
a_rf = sp.lambdify((r_s, Th_s, p_s), a_r, 'numpy')
a_pf = sp.lambdify((r_s, Th_s, p_s), a_p, 'numpy')

# ---- background phi(r) ----
def make_phi(p_depth, r_int):
    # flat if p_depth==0 else log cell phi=-p ln(r_int/r) => phi(r_int)=0, phi(r_core)=-p ln(r_int/r_core)
    if p_depth == 0:
        return (lambda r: np.zeros_like(np.asarray(r, float)),
                lambda r: np.zeros_like(np.asarray(r, float)))
    return (lambda r: -p_depth*np.log(r_int/np.asarray(r, float)),
            lambda r: -p_depth/np.asarray(r, float))   # phi' = -p * d/dr ln(r_int/r) = p/r?
    # d/dr[-p ln(r_int/r)] = -p*( -1/r ) = p/r  -- fix sign below

def phi_funcs(p_depth, r_int):
    if p_depth == 0:
        f = lambda r: np.zeros_like(np.asarray(r, float))
        return f, f
    def f(r):
        r = np.asarray(r, float); return -p_depth*np.log(r_int/r)
    def fp(r):
        r = np.asarray(r, float); return p_depth/r
    return f, fp

# ---- EOM as first-order system for solve_bvp ----
# d/dr(2 a Th') = a_Th Th'^2 + b_Th
# 2 a Th'' + 2 (da/dr) Th' = a_Th Th'^2 + b_Th
# Th'' = [ a_Th Th'^2 + b_Th - 2 (da/dr) Th' ] / (2 a)
def make_rhs(phf, fpf):
    def rhs(r, y):
        Th, Thp = y
        p = phf(r); dp = fpf(r)
        a = af(r, Th, p)
        aTh = aThf(r, Th, p)
        bTh = bThf(r, Th, p)
        dadr = a_rf(r, Th, p) + a_pf(r, Th, p)*dp + aThf(r, Th, p)*Thp  # total da/dr along profile
        Thpp = (aTh*Thp**2 + bTh - 2*dadr*Thp) / (2*a)
        return np.vstack([Thp, Thpp])
    return rhs

def solve_ground(p_depth=0.0, r_core=0.05, cellL=14.0, N=4000, seed='mono', nodes=0):
    r_int = r_core + cellL
    phf, fpf = phi_funcs(p_depth, r_int)
    rhs = make_rhs(phf, fpf)
    x = np.linspace(r_core, r_int, N)
    # BCs: Th(core)=pi, Th(seal)=0
    def bc(ya, yb):
        return np.array([ya[0]-np.pi, yb[0]-0.0])
    # initial guess
    frac = (x-r_core)/cellL
    if seed == 'mono':
        Th0 = np.pi*(1-frac)
    elif seed == '1node':
        # overshoot once: pi -> -0.6 -> 0
        Th0 = np.pi*(1-frac) + 1.2*np.pi*np.sin(2*np.pi*frac)
    elif seed == '2node':
        Th0 = np.pi*(1-frac) + 1.2*np.pi*np.sin(3*np.pi*frac)
    elif seed == 'highcore':
        Th0 = np.pi*(1-frac)**3
    Thp0 = np.gradient(Th0, x)
    sol = solve_bvp(rhs, bc, x, np.vstack([Th0, Thp0]), max_nodes=200000, tol=1e-8, verbose=0)
    return sol, phf, fpf, r_int

def energy(sol, phf, p_depth, r_int):
    x = np.linspace(sol.x[0], sol.x[-1], 8000)
    Th, Thp = sol.sol(x)
    p = phf(x)
    a = af(x, Th, p); b = bf(x, Th, p)
    e = a*Thp**2 + b
    return np.trapz(e, x)

if __name__ == '__main__':
    print("="*70)
    print("GROUND STATE (flat p=0)")
    sol, phf, fpf, r_int = solve_ground(0.0)
    print("  converged:", sol.success, " rms residual:", np.sqrt(np.mean(sol.rms_residuals**2)))
    E0 = energy(sol, phf, 0.0, r_int)
    x = np.linspace(sol.x[0], sol.x[-1], 2000); Th = sol.sol(x)[0]
    # width where Th=pi/2
    idx = np.argmin(np.abs(Th-np.pi/2))
    print(f"  E0 = {E0:.4f}   width(Th=pi/2) = {x[idx]-sol.x[0]:.4f}   n_sign_changes(Th-? monotone): "
          f"{np.sum(np.diff(np.sign(np.diff(Th)))!=0)}")

    print("\n" + "="*70)
    print("RESCUE A: static excited solitons (seed extra nodes, relax)")
    for seed in ['1node', '2node', 'highcore']:
        s, ph2, fp2, ri2 = solve_ground(0.0, seed=seed)
        if s.success:
            E = energy(s, ph2, 0.0, ri2)
            xx = np.linspace(s.x[0], s.x[-1], 3000); Thh = s.sol(xx)[0]
            # count interior zeros of (Th) crossing & overshoots beyond [0,pi]
            over = np.sum((Thh < -0.05) | (Thh > np.pi+0.05))
            turns = np.sum(np.diff(np.sign(np.diff(Thh))) != 0)
            print(f"  seed={seed:9s} success={s.success} E={E:.5f}  monotone-turns={turns} "
                  f"out-of-[0,pi] pts={over}  -> {'COLLAPSED to ground' if abs(E-E0)<1e-2 else 'DISTINCT?'}")
        else:
            print(f"  seed={seed:9s} FAILED to converge")
