"""
Background hedgehog profile Theta(r) for the stabilized soliton in deep-phi.
Independent derivation. Reduced energy density (per dr, sphere-integrated, with 2pi/3):
  E2_r = (2pi xi/3) e^{-phi}[ r^2 sin^2T T'^2 + 2 r^2 T'^2 + 4 e^{2phi} sin^2T ]
  E4_r = (2pi kappa/3) e^{-phi}[ (2 r^2 sin^4T + 2 r^2 sin^2T) T'^2 + e^{2phi} sin^4T ]/r^2
xi=kappa=1. phi(r) = p ln(r/r_int).
Derive EOM symbolically, integrate with solve_bvp.
"""
import numpy as np
import sympy as sp
from scipy.integrate import solve_bvp

r = sp.symbols('r', positive=True)
Tp = sp.symbols('Tp'); Tv = sp.symbols('Tv')
phi_s = sp.symbols('phi_s'); phip_s = sp.symbols('phip_s')
xi = 1; kappa = 1

e2 = sp.exp(-phi_s)*( r**2*sp.sin(Tv)**2*Tp**2 + 2*r**2*Tp**2 + 4*sp.exp(2*phi_s)*sp.sin(Tv)**2 )
e4 = sp.exp(-phi_s)*( (2*r**2*sp.sin(Tv)**4 + 2*r**2*sp.sin(Tv)**2)*Tp**2 + sp.exp(2*phi_s)*sp.sin(Tv)**4 )/r**2
L = xi*e2 + kappa*e4

dL_dTp = sp.diff(L, Tp)
dL_dTv = sp.diff(L, Tv)
Tpp = sp.symbols('Tpp')
d_dr_dL_dTp = ( sp.diff(dL_dTp, r)
              + sp.diff(dL_dTp, Tv)*Tp
              + sp.diff(dL_dTp, Tp)*Tpp
              + sp.diff(dL_dTp, phi_s)*phip_s )
EOM = d_dr_dL_dTp - dL_dTv
Tpp_sol = sp.simplify(sp.solve(EOM, Tpp)[0])
f_Tpp = sp.lambdify((r, Tv, Tp, phi_s, phip_s), Tpp_sol, 'numpy')

def solve_profile(p, r_core=0.05, R=18.0, r_int=1.0, N=6000):
    rmax = r_core + R
    def phi_f(rr): return p*np.log(rr/r_int)
    def phip_f(rr): return p/rr
    def rhs(rr, y):
        return np.vstack([y[1], f_Tpp(rr, y[0], y[1], phi_f(rr), phip_f(rr))])
    def bc(ya, yb):
        return np.array([ya[0]-np.pi, yb[0]-0.0])
    # log-spaced mesh: resolves the steep core for deep phi
    rg = np.geomspace(r_core, rmax, N)
    # core-concentrated init: width scales down with p
    w = max(0.3, 2.0/(1+p))
    Tinit = np.pi*np.exp(-(rg-r_core)/w)
    Tinit[-1] = 0.0
    yinit = np.vstack([Tinit, np.gradient(Tinit, rg)])
    sol = solve_bvp(rhs, bc, rg, yinit, max_nodes=2000000, tol=1e-6, verbose=0)
    return sol

def energy(sol, p, r_core=0.05, R=18.0, r_int=1.0):
    rmax = r_core+R
    rg = np.linspace(r_core, rmax, 6000)
    Tv_ = sol.sol(rg)[0]; Tp_ = sol.sol(rg)[1]
    ph = p*np.log(rg/r_int)
    e2v = np.exp(-ph)*( rg**2*np.sin(Tv_)**2*Tp_**2 + 2*rg**2*Tp_**2 + 4*np.exp(2*ph)*np.sin(Tv_)**2 )
    e4v = np.exp(-ph)*( (2*rg**2*np.sin(Tv_)**4 + 2*rg**2*np.sin(Tv_)**2)*Tp_**2 + np.exp(2*ph)*np.sin(Tv_)**4 )/rg**2
    dens = (2*np.pi/3)*(e2v + e4v)
    return np.trapezoid(dens, rg)

if __name__ == '__main__':
    print("Tpp_sol =", Tpp_sol)
    for p in (0,1,2):
        sol = solve_profile(p)
        E0 = energy(sol, p)
        print(f"p={p}: success={sol.success}, E0={E0:.4f}, nodes={sol.x.size}")
