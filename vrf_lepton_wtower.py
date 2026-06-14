"""
INDEPENDENT VERIFIER: winding-tower lepton mass ratios.

Re-relax the reduced 1D hedgehog soliton profile SEPARATELY for each
azimuthal winding m=1,2,3 and compute M_m = E_m[Theta_m].

Model (xi=kappa=1, flat phi=0, e^phi=1), FROZEN reduced 1D functional:
  E_m = int_{r_core}^{r_int} [ a_m(r,Th) Th'^2 + b_m(r,Th) ] dr
from the verified symbolic reduction
  E2_r = (2pi/3)[ 3 r^2 sin^2 Th Th'^2 + 2 r^2 cos^2 Th Th'^2 + (3m^2+1) sin^2 Th ]
  E4_r = (2pi/3) sin^2 Th [ m^2 sin^2 Th + r^2 (m^2 sin^2 Th + 2 m^2 + sin^2 Th) Th'^2 ] / r^2

Derived (this script, sympy):
  a_m(r,Th) = (2pi/3)[ r^2 sin^2 Th + 2 r^2 + (m^2+1) sin^4 Th + 2 m^2 sin^2 Th ]
  b_m(r,Th) = (2pi/3)[ (3 m^2 + 1) r^2 sin^2 Th + m^2 sin^4 Th ] / r^2

EOM (Euler-Lagrange):  d/dr( 2 a Th' ) = a_Th Th'^2 + b_Th
  => 2 a Th'' + 2 a_r Th' + 2 a_Th Th'^2 = a_Th Th'^2 + b_Th
  => Th'' = ( b_Th - a_Th Th'^2 - 2 a_r Th' ) / (2 a)

Units: energies reported in units of (2pi/3), i.e. drop the (2pi/3) prefactor
(it is m-independent and cancels in all ratios).
"""
import numpy as np
import sympy as sp
from scipy.integrate import solve_bvp, quad

# ---- symbolic build of a, b and the partials, then lambdify (no 2pi/3 prefactor) ----
r_s, Th_s, m_s = sp.symbols('r Theta m', real=True)
s = sp.sin(Th_s); c = sp.cos(Th_s)
a_sym = r_s**2*s**2 + 2*r_s**2 + (m_s**2+1)*s**4 + 2*m_s**2*s**2
b_sym = ((3*m_s**2+1)*r_s**2*s**2 + m_s**2*s**4)/r_s**2

a_r   = sp.diff(a_sym, r_s)
a_Th  = sp.diff(a_sym, Th_s)
b_Th  = sp.diff(b_sym, Th_s)

mods = ['numpy']
a_f    = sp.lambdify((r_s, Th_s, m_s), a_sym, mods)
b_f    = sp.lambdify((r_s, Th_s, m_s), b_sym, mods)
ar_f   = sp.lambdify((r_s, Th_s, m_s), a_r,   mods)
aTh_f  = sp.lambdify((r_s, Th_s, m_s), a_Th,  mods)
bTh_f  = sp.lambdify((r_s, Th_s, m_s), b_Th,  mods)

R_CORE = 0.05
R_INT  = R_CORE + 14.0   # cell length 14

def solve_m(m):
    def rhs(r, y):
        Th, Tp = y[0], y[1]
        A  = a_f(r, Th, m)
        Tpp = (bTh_f(r, Th, m) - aTh_f(r, Th, m)*Tp**2 - 2*ar_f(r, Th, m)*Tp) / (2*A)
        return np.vstack([Tp, Tpp])
    def bc(ya, yb):
        return np.array([ya[0]-np.pi, yb[0]-0.0])

    r_mesh = np.linspace(R_CORE, R_INT, 4001)
    # initial guess: smooth monotone drop pi -> 0
    Th0 = np.pi*(1 - (r_mesh-R_CORE)/(R_INT-R_CORE))
    Tp0 = np.full_like(r_mesh, -np.pi/(R_INT-R_CORE))
    y0 = np.vstack([Th0, Tp0])
    sol = solve_bvp(rhs, bc, r_mesh, y0, tol=1e-8, max_nodes=400000, verbose=0)
    if not sol.success:
        raise RuntimeError(f"BVP failed for m={m}: {sol.message}")

    # energy by accurate quadrature on the dense solution
    def integrand(r):
        Th  = sol.sol(r)[0]
        Tp  = sol.sol(r)[1]
        return a_f(r, Th, m)*Tp**2 + b_f(r, Th, m)
    E, err = quad(integrand, R_CORE, R_INT, limit=400, epsabs=1e-10, epsrel=1e-10)
    return sol, E, err

if __name__ == "__main__":
    print("Reduced 1D winding-tower verifier (energies in units of 2pi/3)")
    print(f"r_core={R_CORE}, r_int={R_INT}, cell length=14, BCs Th(r_core)=pi, Th(r_int)=0\n")

    results = {}
    for m in (1, 2, 3):
        sol, E, err = solve_m(m)
        results[m] = E
        print(f"m={m}:  M_m = {E:.6f}   (quad err {err:.1e}, nodes {sol.x.size})")

    M1, M2, M3 = results[1], results[2], results[3]
    print()
    print(f"M_2/M_1 = {M2/M1:.4f}   (claimed 1.99)")
    print(f"M_3/M_1 = {M3/M1:.4f}   (claimed 3.64)")
    print()
    print(f"m^2-scaling would give: M2/M1=4.00, M3/M1=9.00")
    print(f"m^1-scaling would give: M2/M1=2.00, M3/M1=3.00")

    # cross-check m=1 against m=3 evaluated on m=1 shape (the doc's 'frozen shape' approx)
    sol1, _, _ = solve_m(1)
    def E_on_shape(sol, m):
        def integrand(r):
            Th = sol.sol(r)[0]; Tp = sol.sol(r)[1]
            return a_f(r, Th, m)*Tp**2 + b_f(r, Th, m)
        val, _ = quad(integrand, R_CORE, R_INT, limit=400, epsabs=1e-10, epsrel=1e-10)
        return val
    E2_on1 = E_on_shape(sol1, 2)
    E3_on1 = E_on_shape(sol1, 3)
    print()
    print("Frozen-m=1-shape approximation (doc's method):")
    print(f"  E_2[Th_1]/M_1 = {E2_on1/M1:.4f}")
    print(f"  E_3[Th_1]/M_1 = {E3_on1/M1:.4f}")
