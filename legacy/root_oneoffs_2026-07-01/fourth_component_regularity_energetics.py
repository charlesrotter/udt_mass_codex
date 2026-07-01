#!/usr/bin/env python3
"""
fourth_component_regularity_energetics.py -- Tasks 3,4 of the decisive check.
DATA-BLIND.  Driver: Claude (Opus 4.8, 1M).  2026-06-18.

Given (from fourth_component_sourced_check.py): the bulk Theta-EL is satisfied
identically at Theta == pi/2 (n_4 = cosTheta = 0).  So n_4=0 is a consistent
BULK solution.  Two questions remain that could still FORCE the 4th component:

TASK 3 (regularity fork): at Theta == pi/2, Y = sin^2(Theta)/r^2 = 1/r^2, so
  rho ~ 1/r^2 diverges as r->0 (global-monopole / texture core).  Does
  REGULARITY at r->0 force the Theta-sweep (Theta(0)=pi => sin=0 => regular)?
  The committed UDT cell has a FINITE inner radius r_core=0.05>0 (Dirichlet
  Th(core)=m*pi, Th(seal)=0; complete_metric_sweep_stageA.py rc=0.05).  Does
  the finite cell REMOVE the r->0 regularity pressure?

TASK 4 (energetics + charge): on a finite cell [r_in, r_out], compare the
  L2+L4 proper energy of (i) the swept S^3 hedgehog vs (ii) Theta==pi/2.  Is
  Theta==pi/2 a STABLE critical point (energy minimum in the Theta direction)?
  And: can the topological charge / winding be carried by the (theta,ps) S^2
  winding alone with Theta==pi/2, or does charge conservation REQUIRE a sweep?

We use the EXACT committed stress (complete_metric_batched.py stress()):
  X = e^{-2phi}Theta'^2 ,  Y = sin^2(Theta)/r^2
  rho = (xi/2)(X+2Y) + (kappa/2)(2XY + Y^2)
NOTE: this committed (rho,p_r) is the S^3-hedgehog pointwise stress (proven in
matter_ansatz_derive.py).  The static energy density is rho = -T^t_t.
"""
import sympy as sp

r, phi0 = sp.symbols('r phi0', real=True)
xi, kap = sp.symbols('xi kappa', positive=True)
Th = sp.Function('Theta')(r)
Thp = sp.diff(Th, r)

X = sp.exp(-2*phi0)*Thp**2
Y = sp.sin(Th)**2/r**2
rho = (xi/2)*(X + 2*Y) + (kap/2)*(2*X*Y + Y**2)

print("="*70)
print("TASK 3 -- core regularity fork")
print("="*70)
# (a) energy density at Theta == pi/2 (texture): Theta'=0 => X=0, Y=1/r^2
rho_eq = rho.subs({sp.diff(Th, r): 0, Th: sp.pi/2})
print("rho(Theta=pi/2) =", sp.simplify(rho_eq), "   (the texture core density)")
print("  -> as r->0 this ~ (xi + kappa/r^2)/r^2  : DIVERGES (global-monopole core)")
# proper energy contribution INT rho * sqrt(g3) dr with sqrt(g3)=e^{phi}r^2 (sin th)
# the radial weight r^2 multiplies rho; the integrand near r->0:
integrand = sp.simplify(rho_eq * r**2)        # drop e^{phi},4pi const (positive)
print("  radial energy integrand rho*r^2 (Theta=pi/2) =", integrand)
print("    -> as r->0: xi/2 * 1 + kappa/(2 r^2).  The xi piece is INTEGRABLE")
print("       (finite), the kappa/r^2 piece DIVERGES at r=0 (log? power?).")
i_xi  = sp.integrate((xi/2), (r, sp.Symbol('a', positive=True), 1))
i_kap = sp.integrate(kap/(2*r**2), (r, sp.Symbol('a', positive=True), 1))
print("    INT_{a}^{1} xi/2 dr   =", sp.simplify(i_xi), " (finite as a->0)")
print("    INT_{a}^{1} kap/2/r^2 =", sp.simplify(i_kap), " (-> +inf as a->0: 1/a)")
print()
print("(a) r->0 regularity: the kappa (L4) piece gives a 1/r energy divergence")
print("    at strict r=0 => on an INFINITE-to-origin domain, regularity FORCES")
print("    the sweep (Theta(0)=pi => Y(0)=0).")
print()
print("(b) FINITE CELL: committed r_core = 0.05 > 0 (Dirichlet, stageA rc=0.05).")
a = sp.Rational(5, 100)
print("    On [r_core, r_out] with r_core=0.05 the integrand is BOUNDED:")
print("      rho*r^2 |_{r=0.05} =", sp.simplify(integrand.subs(r, a)),
      "(finite)")
print("    => the r->0 divergence is OUTSIDE the cell; regularity pressure is")
print("       REMOVED.  Theta==pi/2 is perfectly regular on the finite cell.")

print("\n" + "="*70)
print("TASK 4 -- energetics: is Theta==pi/2 a stable critical point?")
print("="*70)
# second variation of the energy in the Theta direction at Theta=pi/2.
# The Theta-direction "potential" part of rho (the X=0, gradient-free part that
# depends on Theta through Y=sin^2/r^2):  V(Theta) = xi*Y + (kappa/2)Y^2
#   = xi sin^2/r^2 + (kappa/2) sin^4/r^4
T = sp.Symbol('T', real=True)
V = xi*sp.sin(T)**2/r**2 + (kap/2)*sp.sin(T)**4/r**4
dV  = sp.diff(V, T)
d2V = sp.diff(V, T, 2)
print("V(Theta) (the Theta-potential, gradient-free part of rho):")
print("  V =", V)
print("  dV/dTheta            =", sp.simplify(dV))
print("  dV/dTheta |_{pi/2}   =", sp.simplify(dV.subs(T, sp.pi/2)),
      "  (critical point?)")
print("  d2V/dTheta2 |_{pi/2} =", sp.simplify(d2V.subs(T, sp.pi/2)))
d2 = sp.simplify(d2V.subs(T, sp.pi/2))
print("    sign:", "MAXIMUM (unstable)" if d2.subs({xi:1,kap:1,r:1})<0 else
      "MINIMUM (stable)", "in the Theta direction")
print("  d2V/dTheta2 |_{0}    =", sp.simplify(d2V.subs(T, 0)),
      "  (Theta=0/pi the poles)")

print("""
READING:
  V(Theta) = xi sin^2/r^2 + (kappa/2) sin^4/r^4 is MAXIMIZED at Theta=pi/2
  (sin=1) and MINIMIZED at Theta=0,pi (sin=0, the poles n_4=+-1).  So in the
  Theta-direction the equator Theta==pi/2 is the energy MAXIMUM, the poles are
  the minima.  => Theta==pi/2 (n_4=0) is a critical point of the bulk EL
  (Task 2) but an UNSTABLE one in Theta: any sweep toward a pole LOWERS the
  texture energy density.  This is the global-monopole 'unwinding' instability.
  Whether it actually unwinds depends on the BOUNDARY CONDITION (charge).
""")

print("="*70)
print("TASK 4b -- does charge REQUIRE the sweep?  S^2 winding vs S^3 sweep.")
print("="*70)
print("""
The S^2 (theta,ps)-winding carries degree-1 with Theta==pi/2 FIXED: the map
(theta,ps) -> equatorial S^2 covers the target sphere once.  The S^3 sweep
Theta: pi->0 carries the pi_3 (Skyrme/baryon) charge.  These are DIFFERENT
topological charges:
  * S^2 texture / equatorial m-winding: charge = degree of S^2->S^2,
    pi_2(S^2)=Z, carried by (theta,ps) alone, Theta==pi/2 allowed.
  * S^3 Skyrme: baryon number = degree of S^3->S^3, pi_3(S^3)=Z, REQUIRES
    Theta to sweep pi->0 (n_4 sweeps -1->+1) -- if Theta==pi/2 the S^3 map is
    degenerate (image is a 2-sphere equator, NOT onto S^3) => baryon number 0.
So: charge conservation REQUIRES the sweep ONLY IF the conserved charge is the
pi_3 baryon number (S^3).  If the native charge is the pi_2 degree (S^2,
omega_H1 area-form, the CANONIZED winding current), Theta==pi/2 carries it and
NO sweep is needed.  => the sweep is forced only by ASSUMING the S^3 charge,
which is the very thing under test.  Circular if used to justify S^3.
""")
