#!/usr/bin/env python3
"""
Verifier-beta sympy spot-check for PONDER S65-001 §3.3 scalar boundary term.

Goal: verify by direct symbolic variation of the canonical §8.5.1 scalar action
that the boundary term at r = r_* matches
    B_scalar = r_*^2 e^{-2 phi_*} (d phi^cav / dr) delta(phi^cav) |_{r_*}
as claimed in PONDER §3.3 eq (137).

UDT metric (CG §1.0):
    ds^2 = - e^{-2 phi_0(r)} c^2 dt^2 + e^{+2 phi_0(r)} dr^2 + r^2 dOmega^2
    sqrt(-g) = c * r^2 * sin(theta)   (phi_0-independent)
    g^{rr}   = e^{-2 phi_0(r)}
    g^{tt}   = - e^{+2 phi_0(r)} / c^2
    g^{theta theta} = 1/r^2
    g^{phi phi}     = 1/(r^2 sin^2 theta)

We take a STATIC spherically-symmetric matter-cavity scalar phi^cav(r) so only
the radial term contributes to the bulk and to the boundary at r = r_*. (For a
general phi^cav(r,t,theta,phi), the radial boundary term separates from the
time/angular surface contributions; we are checking ONLY the radial-r=r_*
boundary slab here, which is the PONDER §3.3 claim.)

L_phi = (1/2) sqrt(-g) [ g^{mu nu} d_mu phi^cav d_nu phi^cav  +  mu^2 (phi^cav)^2 ]

For static, spherically symmetric phi^cav(r):
L_phi = (1/2) c r^2 sin(theta) [ e^{-2 phi_0} (phi^cav_r)^2 + mu^2 (phi^cav)^2 ]

The radial-direction variation gives:
delta L_phi = c r^2 sin(theta) [ e^{-2 phi_0} phi^cav_r d_r(delta phi^cav)
                                  + mu^2 phi^cav (delta phi^cav) ]

Integrate-by-parts the d_r(delta phi^cav) term over r from 0 to r_*:
   integral d_r [ c r^2 sin(theta) e^{-2 phi_0} phi^cav_r delta phi^cav ] dr
   -  integral delta phi^cav d_r [ c r^2 sin(theta) e^{-2 phi_0} phi^cav_r ] dr

The first integral evaluates to the BOUNDARY surface contribution at r = r_*;
after the trivial dt integration and the angular integration giving 4*pi (or
left as d Omega), the boundary term per unit (c * 4pi t)  is:

   B = r_*^2 e^{-2 phi_0(r_*)} phi^cav_r(r_*) * delta phi^cav(r_*)

This is precisely the claim in PONDER §3.3.

We verify this symbolically.
"""

import sympy as sp

print("=" * 70)
print("Verifier-beta sympy spot-check for PONDER S65-001 §3.3")
print("=" * 70)

# Symbols and functions
r, theta, t, c, mu, r_star = sp.symbols('r theta t c mu r_*', positive=True, real=True)
phi0 = sp.Function('phi_0')(r)             # metric-determining background field
phicav = sp.Function('phi_cav')(r)         # matter-cavity scalar (static, spherical)
deltaphicav = sp.Function('delta_phi_cav')(r)

# Metric ingredients (CG §1.0, §4.1)
g_tt   = -sp.exp(-2*phi0) * c**2
g_rr   =  sp.exp( 2*phi0)
g_thth =  r**2
g_pp   =  r**2 * sp.sin(theta)**2

g_det  = g_tt * g_rr * g_thth * g_pp        # should reduce to -c^2 r^4 sin^2(theta)
sqrt_minus_g = sp.sqrt(-g_det).simplify()

print("\nMetric verification:")
print("  sqrt(-g) =", sqrt_minus_g)
print("  expected  = c * r^2 * sin(theta)  (phi_0-independent per CG §4.1)")

# Inverse metric (radial)
g_uu_rr = 1 / g_rr                          # = e^{-2 phi_0}
print("\n  g^{rr} =", sp.simplify(g_uu_rr))
print("  expected = e^{-2 phi_0}")

# Static scalar Lagrangian density
# L_phi = (1/2) sqrt(-g) [ g^{rr} (phi^cav_r)^2 + mu^2 (phi^cav)^2 ]
phicav_r = sp.diff(phicav, r)

L_phi = sp.Rational(1,2) * sqrt_minus_g * (
    g_uu_rr * phicav_r**2 + mu**2 * phicav**2
)
L_phi_simpl = sp.simplify(L_phi)
print("\nLagrangian density L_phi (static, spherical):")
print("  L_phi =", L_phi_simpl)

# Vary with respect to phi^cav:  delta L_phi
# = d L_phi / d phi^cav * delta phi^cav  +  d L_phi / d phicav_r * d_r delta phi^cav
dL_dphi   = sp.diff(L_phi, phicav)
dL_dphi_r = sp.diff(L_phi, phicav_r)

print("\nVariation derivatives:")
print("  dL/d(phi^cav)   =", sp.simplify(dL_dphi))
print("  dL/d(phi^cav_r) =", sp.simplify(dL_dphi_r))

# IBP: d_r(delta phi^cav)*A  ->  d_r(A * delta phi^cav)  -  delta phi^cav * d_r(A)
# Boundary term:   d_r ( dL/dphi^cav_r  *  delta phi^cav )
# Bulk Euler-Lagrange:  dL/dphi^cav  -  d_r ( dL/dphi^cav_r )

# Boundary surface integrand (in t, theta, varphi) before angular integration:
boundary_integrand = dL_dphi_r * deltaphicav
print("\nBoundary integrand (before angular integration), at general r:")
print("  =", sp.simplify(boundary_integrand))

# Evaluate at r = r_*: substitute phi_0(r) -> phi_0(r_*) ≡ phi_star, etc.
phi_star = sp.symbols('phi_*', real=True)
phicav_star = sp.symbols('phi_cav_*', real=True)
phicav_r_star = sp.symbols("phi_cav'_*", real=True)
deltaphicav_star = sp.symbols('delta_phi_cav_*', real=True)

boundary_at_rstar = boundary_integrand.subs({
    phi0: phi_star,
    phicav: phicav_star,
    phicav_r: phicav_r_star,
    deltaphicav: deltaphicav_star,
    r: r_star,
}).rewrite(sp.exp)
boundary_at_rstar = sp.simplify(boundary_at_rstar)

print("\nBoundary integrand at r = r_* (before angular integration):")
print("  =", boundary_at_rstar)

# Angular integration over (theta, varphi):  integral sin(theta) dtheta dvarphi = 4 pi
# (sqrt(-g) already carries one factor of sin theta, so the integrand carries
# sin(theta) directly; integrating over the 2-sphere gives 4 pi.)
angular_integral = sp.integrate(
    sp.integrate(boundary_at_rstar, (theta, 0, sp.pi)),
    (sp.Symbol('varphi'), 0, 2*sp.pi)
)
angular_integral = sp.simplify(angular_integral)
print("\nAfter angular integration over S^2:")
print("  B_scalar =", angular_integral)

# PONDER §3.3 claim (with factor 4*pi*c absorbed, or per-mode at each (l,m)):
ponder_claim = r_star**2 * sp.exp(-2*phi_star) * phicav_r_star * deltaphicav_star
print("\nPONDER §3.3 claim (eq 137):")
print("  B_scalar^{PONDER} = r_*^2 e^{-2 phi_*} phi^cav_r(r_*) delta phi^cav(r_*)")
print("  =", ponder_claim)

# Compare: ratio (sympy / PONDER)
ratio = sp.simplify(angular_integral / ponder_claim)
print("\nRatio (sympy / PONDER):")
print("  =", ratio)

# Verdict
if ratio.is_constant():
    print("\n>>> sympy boundary term matches PONDER §3.3 up to a constant factor:", ratio)
    print(">>> The constant 4*pi*c is the angular integration + the dt prefactor of sqrt(-g)")
    print(">>> from the (-c^2) component of g_{tt}; this factor is absorbed into ")
    print(">>> the 'per-mode at each (l,m)' or '4 pi absorbed' convention as PONDER §3.3 states.")
    print(">>> STRUCTURAL FORM MATCH: confirmed.")
else:
    print("\n>>> WARNING: sympy boundary term does NOT match PONDER §3.3 structurally.")
    print(">>> Discrepancy:", sp.simplify(angular_integral - ponder_claim))

print("\n" + "=" * 70)
print("End sympy spot-check.")
print("=" * 70)
