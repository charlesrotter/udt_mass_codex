"""C5 piercing: is the south-cap f<1 dip an a1-recentering gauge artifact?

Independent construction of the gauge diagnostic:
An infinitesimal recentering by displacement d of a monopole profile F(y)
generates the dipole  delta f = d cos(th) F'(y),  i.e.  a_gauge(y) = d F'(y)/sqrt3.
The momentum-only weld gauge is a(1) = 0 (f = 1 pointwise on the weld sphere).
 - gamma > 0: a_gauge(1) = -d*gamma/sqrt3 != 0 for d != 0  => NO residual
   recentering freedom; the dipole jet c is gauge-fixed; the south-cap slope
   gamma - sqrt3 c is invariant. Piercing is NOT an artifact.   [analytic]
 - gamma = 0: a_gauge(1) = 0, but a_gauge'(1) = d F''(1)/sqrt3 and the EL
   F-equation at the weld with kappa(1)=0, F'(1)=0 forces F''(1) = 0
   ((y^2F')' = -H(0) = 0). So recentering cannot generate the c-jet either.

Numeric check of the residual-gauge subtraction: project the flow's a(y) on
the gauge dipole F'(y) and verify the projection cannot cancel the
near-interface dip for a pierced flow.
"""
import numpy as np
from el_core import run_flow, SQ3

gamma, c = 1/3, 0.25   # pierced regime (c > gamma/sqrt3 = 0.1925)
sol, sealed = run_flow(gamma, c, Tmax=80.0, dense=True)
tend = sol.t[-1]
ts = np.linspace(0, min(tend, 1.0), 2001)
u = sol.sol(ts)
F, Ft, A = u[0], u[1], u[2]
y = np.exp(-ts)
Fp = -Ft/y   # F' in y
# gauge dipole shape: g(y) = F'(y)/sqrt3; admissible recentering must keep
# a(1)+a_g(1)=0  =>  d * F'(1)/sqrt3 = 0  =>  d = 0 since F'(1) = -gamma != 0.
print(f"F'(1) = {Fp[0]:+.6f} (= -gamma) => admissible d = 0; piercing gauge-invariant")
# hostile: even ALLOWING the best least-squares d, can the dip be removed?
g = Fp/SQ3
dstar = -np.trapezoid(A*g, ts)/np.trapezoid(g*g, ts)
A_res = A + dstar*g
fmin_raw = F - SQ3*A
fmin_res = F - SQ3*A_res
print(f"best-fit illegal recentering d* = {dstar:+.4f}")
print(f"  raw min f_south (t<1): {fmin_raw.min():.6f}")
print(f"  after illegal subtraction: {fmin_res.min():.6f} "
      f"(still pierced: {fmin_res.min() < 1})")
print(f"  but a_res(1) = {A_res[0]:+.6f} (≠0: violates weld gauge)" )
