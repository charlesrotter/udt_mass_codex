#!/usr/bin/env python3
"""Adjudicate the two open flags on Claim B:
(1) is u* real/in-range on banked geometry, and what does 'deep' mean?
(2) the insulation reading: degenerate characteristic => insulating wall?
    -- is c->inf a genuine dynamical barrier or a coordinate-speed artifact?
"""
import sympy as sp, mpmath as mp

print("="*70)
print("(1) u* reality and the 'radial band'")
print("="*70)
# u*^2 = 1 - a^3 W/(a_u^2 r).  In (0,1) iff a^3 W < a_u^2 r.
# r is areal radius (rho=r theorem). deep cell = SMALL r? Charter:
# t = ln(1/r), deep = large t = small r. f = a/r LARGE at small r.
# At small r: a^3 W/(a_u^2 r) LARGE => u*^2 < 0 => NO real wall deep in.
# At large r: ratio -> 0 => u*^2 -> 1 => wall approaches the POLE (u=1).
# So the characteristic latitude:
#   - does NOT exist for r < a^3 W/a_u^2 (no degenerate latitude there)
#   - exists for r > a^3 W/a_u^2, sitting between equator(u=0) and pole.
# The committed XA2 note 'deep enough r' is AMBIGUOUS/likely BACKWARDS:
# the wall lives in the OUTER band, not the deep core. Demonstrate the
# monotone behavior:
a,au,w,r = sp.symbols('a a_u w r', positive=True)
W=(1+w)**2
u2 = 1 - a**3*W/(au**2*r)
print(" u*^2(r) monotone increasing in r:", sp.simplify(sp.diff(u2,r))>0 if sp.diff(u2,r).is_positive else "d/dr =", sp.simplify(sp.diff(u2,r)))
print(" => as r grows u* -> pole(1); as r-> a^3W/au^2+ , u*->equator(0).")
print(" => WALL EXISTS ONLY in outer radial band r > a^3 W/a_u^2; absent in deep core.")
print(" SCOPE: the cell-partition picture has walls only where the band is satisfied;")
print("        on a given cell some radii have NO interior characteristic at all.")

print()
print("="*70)
print("(2) insulation reading -- hostile adjudication")
print("="*70)
print("""
COMPUTED & THEOREM-GRADE:
  - D=0 is a real degeneracy: c_ang^2=f/D, c_rad^2=f^2 r^2 W/D both ->inf.
  - This is a genuine characteristic surface of the principal symbol
    (not removable by chart, since it's built from inverse-metric
    components = physical signal speeds).

THE READING UNDER ATTACK: 'c->inf => zero angular flux => insulating
wall => discrete cell'.  HOSTILE POINTS:

(a) c->inf is the speed DIVERGING, not vanishing. An INFINITE
    characteristic speed means signals cross INSTANTLY, i.e. the surface
    is NON-TIMELIKE / the operator changes type (elliptic<->hyperbolic).
    A type-change surface is NOT generically a reflecting/insulating
    barrier. In GR an infinite coordinate speed is the hallmark of a
    COORDINATE/horizon-like artifact (cf. Schwarzschild dr/dt->0 at
    horizon is the inverse face). The leap to 'zero angular FLUX' is
    NOT entailed: flux ~ g^thth * grad; g^thth=1/D->inf, so the flux
    coefficient BLOWS UP, it does not vanish. 'Insulating' would need
    flux->0. THE SIGN OF THE INFERENCE IS BACKWARDS at face value.

(b) W5 (banked, registry): the q-elimination ITSELF breaks down at
    Dw=0 (L_qq ~ Dw^-3 flips sign); the UNREDUCED 3-field EL is finite.
    So D|q*=0 is partly an ARTIFACT of having solved-and-substituted q*.
    The 'characteristic' is on the q*-REDUCED operator. Whether the
    unreduced coupled operator has a genuine barrier there is UNTESTED.

(c) This is structurally the resonator/eigenvalue-template risk the
    charter warns about: a degeneracy of a *coordinate-derived speed*
    is being read as a *dynamical confinement mechanism*. No flux
    computation, no energy-current argument, no reflection coefficient
    has been produced. The script ITSELF labels C3/D2 HYPOTHESIS-GRADE
    and verifier-flagged -- that labeling is HONEST and load-bearing
    claims (C3a,C3b,C4 count, D1 degree) do NOT rest on the insulation.

VERDICT ON THE DISCRETENESS CANDIDATE:
  - Theorem-grade core (metric degeneracy, 1/D speeds, wall COUNT =
    deg(Dw), count rises with ell): CONFIRMED, real derived structure.
  - The INSULATION/cell-partition LEAP: NOT supported by the algebra;
    the c->inf=>zero-flux step is at best unproven and at face value
    has the flux going the WRONG way (g^thth->inf). This is the
    template-error risk wearing new clothes UNLESS a genuine
    energy-flux/reflection argument is supplied (W6). The script's own
    HYPOTHESIS-GRADE flag is correct and must NOT be upgraded.
""")
# Quick check of point (a): the conserved angular flux for a wave
# u_tt = c_ang^2 u_thth-type operator. Flux F ~ g^thth d_theta u.
# At D->0, g^thth=1/D->inf. For F to stay finite, d_theta u must ->0,
# i.e. Neumann-like (du/dtheta->0) is the FINITE-ENERGY condition --
# NOT zero-flux-Dirichlet 'insulating node'. Note this nuance:
print("NOTE: finite-energy at g^thth->inf forces d_theta u ->0 (Neumann-like),")
print("      a SMOOTHNESS/turning condition, which is NOT the same as a")
print("      zero-flux insulating WALL that PARTITIONS into independent cells.")
print("      Neumann turning points do not decouple a domain into")
print("      dynamically independent sub-cells. The partition claim is unearned.")
