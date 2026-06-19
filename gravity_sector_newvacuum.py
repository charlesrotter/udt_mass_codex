#!/usr/bin/env python3
"""
gravity_sector_newvacuum.py

Given that Schwarzschild is NOT a vacuum solution of the honest (full)
field equations, find WHAT the vacuum solutions ARE, and read the physics
(boundary-tension? Lambda-like? new scale?).

The full vacuum equations (covariant, mixed, divided by f) were:
  EQ_tt  : 72 r^2 phi'^2 - 8 r^2 phi'' - 18 r phi' - e^{2phi} + 1 = 0
  EQ_thth: 82 r phi'^2 - 9 r phi'' - 10 phi' = 0
(both times e^{-2phi}/r^2 or /r). And phi-eqn (if independent) R=0:
  R=0   : -2 r^2 phi'^2 + r^2 phi'' + 4 r phi' + e^{2phi} - 1 = 0

We solve. Observe structure. Tag every BC chosen.
"""
import sympy as sp
import numpy as np

r=sp.symbols('r',positive=True)
phi=sp.Function('phi')

# --- analytic: try power law phi = k ln(r) + b far from any source (e^{2phi} negligible? no) ---
# Look for solutions where the e^{2phi}-1 term is subdominant (small phi, large r):
# linearize ONLY as hypothesis-probe (TAGGED: hypothesis, not a result):
k,b=sp.symbols('k b',real=True)
print("HYPOTHESIS-PROBE (tagged, NOT a result): small-phi behaviour.")
print("Keeping e^{2phi}~1+2phi, the tt eqn near phi~0, leading source-free balance.")

# Solve EQ_thth exactly (it has no e^{2phi}): 9 r phi'' = 82 r phi'^2 - 10 phi'
# Let u=phi'. 9 r u' = 82 r u^2 - 10 u.  Bernoulli-ish.
u=sp.Function('u')
ode_th=sp.Eq(9*r*sp.diff(u(r),r), 82*r*u(r)**2 - 10*u(r))
sol_th=sp.dsolve(ode_th)
print("\nEQ_thth as 1st-order ODE for u=phi':")
print("  ", sol_th)

# The honest VACUUM is the SIMULTANEOUS solution of tt AND thth. Numerically shoot.
print("\n=== NUMERICAL: simultaneous vacuum solve, shoot from large r with phi->0 ===")
# Variables y=[phi, phip]. Use thth to get phi'' = (82 r phi'^2 - 10 phi')/(9r),
# and CHECK tt as the constraint. If both can't hold simultaneously except phi=0,
# that means the ONLY asymptotically-flat vacuum is flat space (no Schwarzschild,
# no nontrivial profile) -> the modification KILLS vacuum mass entirely.
def rhs(rr, y):
    p,pp=y
    ppp=(82*rr*pp**2 - 10*pp)/(9*rr)
    return [pp, ppp]
def constraint_tt(rr,p,pp,ppp):
    return 72*rr**2*pp**2 - 8*rr**2*ppp - 18*rr*pp - np.exp(2*p) + 1

from scipy.integrate import solve_ivp
# start near flat with a tiny seed phip to see if tt-constraint can be satisfied
for seed in [1e-3, 1e-1, -1e-1]:
    r0=100.0; p0=0.0; pp0=seed
    sol=solve_ivp(rhs,[r0,2.0],[p0,pp0],dense_output=True,rtol=1e-9,atol=1e-12,max_step=0.5)
    # evaluate tt-constraint along the thth-solution
    rs_grid=np.linspace(r0,2.0,8)
    viol=[]
    for rr in rs_grid:
        p,pp=sol.sol(rr); ppp=(82*rr*pp**2-10*pp)/(9*rr)
        viol.append(constraint_tt(rr,p,pp,ppp))
    print(f"  seed phip0={seed:+.0e}: tt-constraint along thth-soln (should be 0 for true vacuum):")
    print("   ", np.array(viol))

print("\nINTERPRETATION will be read from whether tt-constraint can be held to 0.")
print("If only phip=0 (flat) holds it => the honest vacuum has NO nontrivial soln")
print("   => stronger than GR: the (gBox-nablanabla)f terms over-constrain vacuum.")
