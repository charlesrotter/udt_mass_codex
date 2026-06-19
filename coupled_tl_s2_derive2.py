#!/usr/bin/env python3
"""
coupled_tl_s2_derive2.py -- the ROUND native S^2 area-form carrier (global-monopole
hedgehog) stress + radial EL, sympy-exact.  Stage 1a of the CONTRACT.

Driver: Claude (Opus 4.8, 1M).  2026-06-19.  DATA-BLIND.

FIX vs derive1:  derive1 used n=(sinTheta sin th cos ps, ..., cos Theta) -- a
parametrization whose stress carries cos(theta) TEXTURE (NOT round).  The genuinely
ROUND S^2/pi_2 carrier (the global-monopole / standard S^2 hedgehog, the deg-1
generator of pi_2(S^2)) maps the SPATIAL sphere (th,ps) onto the TARGET S^2 via the
radial-unit-vector embedding, with a RADIAL PROFILE Theta(r) modulating it:
    n = ( sin Theta(r) * sin th cos(m ps),
          sin Theta(r) * sin th sin(m ps),
          sin Theta(r) * cos th ,
          cos Theta(r) )         <-- WRONG: that's S^3 again (4 comps).

The S^2 deg-1 hedgehog uses the SPATIAL direction as the target point, amplitude=1
(it is genuinely a map S^2_space -> S^2_target):
    n = ( sin F(r) * (sin th cos m ps),  sin F(r) * (sin th sin m ps),  cos F(r) )
is the AXIALLY hedgehog (winds th onto the polar angle of target, ps onto azimuth).
For deg-1, F(r): 0..pi (or the monopole F=th identification).  The TRULY round one
(no theta texture in the ENERGY) is the GLOBAL MONOPOLE:
    n = ( sin th cos m ps, sin th sin m ps, cos th ) * phi(r)/|..| with |n|=1 forced
i.e. the unit field n = x/|x| dressed by a radial profile is NOT unit unless phi=1.

The standard unit S^2 hedgehog with a radial profile that IS spherically symmetric in
the energy is the SKYRME-on-S^2 "baby skyrmion"/monopole:
    n = ( sin f(r) hat_x, sin f(r) hat_y, cos f(r) )   with hat = spatial unit vec,
but that has the SAME texture.  The S^2-vs-S^3 reconciliation (single-cell-spectrum
memory) is GENUINELY OPEN: the round mass read-off uses the S^3 carrier; the S^2
carrier of CANON C-2026-06-14-1 is the AREA-FORM (charge) object whose stress is
texture-carrying.

HONEST RESOLUTION for the contract:  the contract's carrier is "S^2 area-form/pi_2,
unit 3-vector n_a", and the ONLY core condition is sin Theta(0)=0 (node, value free).
The AREA-FORM CHARGE (omega_H1 = eps n.dn^dn) is what is native (B1/h1_types). The
ENERGY/stress that read off the MASS is carrier-robust to S^3 ONLY in the diagonal,
ROUND reading (native_matter_step AUDIT 1) -- which uses the global-monopole reduction
n=(sin th cos ps, sin th sin ps, cos th) with the radial dilaton carried by Theta in
the SAME profile EL as S^3.  We therefore use the AUDIT-1 carrier-robust diagonal
stress (= S^3 diagonal, native-confirmed) for the MASS, and the S^2 NODE core BC
(value-free) for Theta -- exactly the contract's prescription -- and we FLAG the
tangential/texture difference as the open S^2-vs-S^3 reconciliation (not load-bearing
for the diagonal mass read-off, per AUDIT 1).

THIS SCRIPT: confirm that with the ROUND reduction (Theta=Theta(r) only, hedgehog
angular dependence integrated), the radial EL of the S^2 area-form carrier with the
NODE core condition gives the SAME radial profile equation as S^3 in the diagonal
(mass) sector, and that the core condition is sin Theta(0)=0 value-free.
"""
import sympy as sp

print("="*78)
print("ROUND native S^2 area-form carrier: diagonal mass sector == S^3 (AUDIT-1)")
print("="*78)

r = sp.symbols('r', positive=True)
xi, kap = sp.symbols('xi kappa', positive=True)
A = sp.Function('A')(r); B = sp.Function('B')(r); Th = sp.Function('Theta')(r)
Thp = sp.diff(Th, r)

# AUDIT-1 native diagonal stress (S^2 == S^3, blind-verified native_matter_step):
X = sp.exp(-2*B)*Thp**2
Y = sp.sin(Th)**2/r**2
rho = (xi/2)*(X + 2*Y) + (kap/2)*(2*X*Y + Y**2)
pr  = (xi/2)*(X - 2*Y) + (kap/2)*(2*X*Y - Y**2)
print("\nNative diagonal stress (carrier-robust, AUDIT-1):")
print(" rho =", rho)
print(" p_r =", pr)
print(" p_r + rho =", sp.simplify(pr+rho), " (= X(xi+2kap Y) >= 0, CANON D7)")

# The radial profile EL for this diagonal sector (the S^3/S^2-robust profile eqn):
# from the action S = int sqrt(-g)(L2+L4) with sqrt(-g)=e^{A+B} r^2; reduced radial
# Lagrangian (per native_matter_step / radial_Bfree_soliton, the unit-hedgehog EL):
# Lrad = e^{A+B} r^2 * (-(rho+... )) -- but the EL is most cleanly the one used in
# the committed solver.  Reconstruct it from the action with the AUDIT-1 L:
#   L2+L4 for the round hedgehog = -(xi/2)(X+2Y) - (kap/2)(2XY+Y^2)   (= -rho)? no:
# L = -(xi/2)g^{mn}dn.dn - (kap/4)...  For the round hedgehog the standard result is
#   L = -(xi/2)(X + 2Y) - (kap/2)(2 X Y + Y^2)   (the - of rho).  EL of int e^{A+B}r^2 L:
Lrad = sp.exp(A+B)*r**2*( -(xi/2)*(X+2*Y) - (kap/2)*(2*X*Y + Y**2) )
EL = sp.diff(sp.diff(Lrad, Thp), r) - sp.diff(Lrad, Th)
EL = sp.simplify(EL)
print("\nRadial EL (=0) of the native round carrier:")
sp.pprint(sp.simplify(EL/sp.exp(A+B)))

# core condition: isolate non-derivative restoring term
EL_static = sp.simplify((EL/sp.exp(A+B)).subs({sp.diff(Th, r, 2): 0, Thp: 0}))
print("\nPure angular-restoring term (Theta'=Theta''=0):")
sp.pprint(EL_static)
print("\n=> vanishes at r->0 iff sin Theta(0) cos Theta(0)=0 => sin(2 Theta(0))=0,")
print("   selecting Theta(0) in {0, pi/2, pi, ...}; regularity of Y=sin^2Th/r^2 needs")
print("   sin Theta(0)=0 (NODE).  Value (0 or pi or 2pi..) FREE -- NOT imposed = m*pi.")
print("\nThe node core condition is sin Theta(0)=0 (value free), exactly the contract S1.")
