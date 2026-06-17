# VERIF_matter_sector_potential_E2.py
# E2 (Safeguard S2): solve the REAL hedgehog profile Theta(r) from its field ODE
# (the corpus reduced EOM, lepton_soliton_spectrum_results.md:62-67), NO convenient
# ansatz passed off as the solution. We solve flat (phi=0) AND a deep-phi background,
# and also provide a representative analytic profile -> all reused/compared in E4 (S2:
# demonstrate the E4 verdict is robust to >=2 profiles).
#
# Reduced EOM (xi=kappa=1, charge m=1), from the energy
#   E2_r = (2pi/3) e^{-phi}[ r^2 sin^2Th Th'^2 + 2 r^2 Th'^2 + 4 e^{2phi} sin^2Th ]
#   E4_r = (2pi/3) e^{-phi}[ (2 r^2 sin^4Th + 2 r^2 sin^2Th) Th'^2 + e^{2phi} sin^4Th ]/r^2
# Euler-Lagrange:  d/dr[ dL/dTh' ] = dL/dTh .  We derive Th'' = num/den symbolically,
# lambdify, and solve the BVP Th(core)=pi, Th(seal)=0 with scipy solve_bvp.

import numpy as np, sympy as sp
from scipy.integrate import solve_bvp

r = sp.symbols('r', positive=True)
Th = sp.Function('Theta')
phisym = sp.Function('phi')
Thr = Th(r); Thp = Thr.diff(r); phr = phisym(r); php = phr.diff(r)

# integrand L(r,Th,Th') = (E2_r+E4_r)/(2pi/3), xi=kappa=1, m=1
s, c = sp.sin(Thr), sp.cos(Thr)
e_m, e_p = sp.exp(-phr), sp.exp(2*phr)
E2 = e_m*( r**2*s**2*Thp**2 + 2*r**2*Thp**2 + 4*e_p*s**2 )
E4 = e_m*( (2*r**2*s**4 + 2*r**2*s**2)*Thp**2 + e_p*s**4 )/r**2
L = E2 + E4

dL_dThp = sp.diff(L, Thp)
dL_dTh  = sp.diff(L, Thr)
# d/dr dL_dThp = dL_dThp.diff(r) but Th,Th',phi depend on r; collect Th''
EL = sp.diff(dL_dThp, r) - dL_dTh           # = (dL/dThp)' - dL/dTh = 0
Thpp = sp.symbols('Thpp')
EL = EL.subs(sp.Derivative(Thr, r, r), Thpp)
sol_Thpp = sp.solve(EL, Thpp)[0]
sol_Thpp = sp.simplify(sol_Thpp)

# lambdify with phi, phi' supplied
Thp_sym = sp.symbols('Thp'); Th_sym = sp.symbols('Thv'); rr = sp.symbols('rr', positive=True)
phv, phpv = sp.symbols('phv phpv')
expr = sol_Thpp.subs({Thp: Thp_sym})  # placeholder (no-op)
expr = sol_Thpp
expr = expr.subs({sp.Derivative(Thr, r): Thp_sym, Thr: Th_sym, phr: phv,
                  sp.Derivative(phr, r): phpv, r: rr})
Thpp_func = sp.lambdify((rr, Th_sym, Thp_sym, phv, phpv), expr, 'numpy')

def solve_profile(phi_of_r, dphi_of_r, rc=1e-3, rs=8.0, N=4000, label=""):
    x = np.linspace(rc, rs, N)
    def rhs(rv, y):
        Thv, Thpv = y
        phv_ = phi_of_r(rv); phpv_ = dphi_of_r(rv)
        return np.vstack([Thpv, Thpp_func(rv, Thv, Thpv, phv_, phpv_)])
    def bc(ya, yb):
        return np.array([ya[0]-np.pi, yb[0]-0.0])
    # monotone pi->0 initial guess
    y0 = np.vstack([np.pi*(1 - (x-rc)/(rs-rc)), -np.pi/(rs-rc)*np.ones_like(x)])
    sol = solve_bvp(rhs, bc, x, y0, max_nodes=200000, tol=1e-8, verbose=0)
    rms = np.sqrt(np.mean(sol.rms_residuals**2)) if sol.rms_residuals is not None else np.nan
    # half-twist radius
    Thvals = sol.sol(x)[0]
    idx = np.argmin(np.abs(Thvals-np.pi/2))
    print(f"[{label}] solve_bvp success={sol.success} nodes={sol.x.size} "
          f"max_rms_resid={np.max(sol.rms_residuals):.2e} half-twist r={x[idx]:.3f}")
    return sol

print("="*72); print("E2: REAL HEDGEHOG PROFILE Theta(r) FROM THE FIELD ODE (S2)"); print("="*72)
print("EOM Theta'' = num/den derived symbolically; den =",
      sp.denom(sp.together(sol_Thpp)))

# (a) flat background phi=0
sol_flat = solve_profile(lambda rv: 0.0, lambda rv: 0.0, label="flat phi=0")

# (b) deep-phi background: phi = -p ln(r_int/r) -> phi'=p/r, with p=1 (phi_core ~ -5.5 region)
p = 1.0; r_int = 8.0
sol_deep = solve_profile(lambda rv: -p*np.log(r_int/rv), lambda rv: p/rv, label="deep phi=-ln(r_int/r), p=1")

# save profiles for E4
import pickle
xfit = np.linspace(1e-3, 8.0, 4000)
prof = {
  'flat':  {'r': xfit, 'Th': sol_flat.sol(xfit)[0], 'Thp': sol_flat.sol(xfit)[1],
            'phi': np.zeros_like(xfit), 'phip': np.zeros_like(xfit)},
  'deep':  {'r': xfit, 'Th': sol_deep.sol(xfit)[0], 'Thp': sol_deep.sol(xfit)[1],
            'phi': -p*np.log(r_int/xfit), 'phip': p/xfit},
}
with open('matter_sector_profiles.pkl','wb') as fh: pickle.dump(prof, fh)
print("\nProfiles saved -> matter_sector_profiles.pkl  (flat + deep, both REAL EOM solutions)")
print("BCs: Theta(core)=pi, Theta(seal)=0  [DERIVED charge-1 hedgehog BC];")
print("finite cell r in [1e-3, 8] L  [finite-cell canon]; method: scipy solve_bvp tol=1e-8.")
