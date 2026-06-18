#!/usr/bin/env python3
"""
phase1_geon_coeffs.py -- PHASE-1c step 1b: take the EXACT time+angle averaged
O(A^2) l=0 Einstein components produced by phase1_geon_reduce.py (full-exp run,
exit 0) and SPLIT them cleanly into the phi-operator + GW-source, and produce the
O(A^1) wave operator. Also lambdify them for the numerical solver.

Driver: Claude (Opus 4.8, 1M). 2026-06-18. DATA-BLIND. Category-A. OBSERVE. c=1.

The expressions below are TRANSCRIBED VERBATIM from the committed-run stdout of
phase1_geon_reduce.py (the full-exponential O(A^2) reduction, no Taylor shortcut),
then time-averaged (sin^2(w t) -> 1/2) here. Source of truth = that run's output.
"""
import sympy as sp

r, w = sp.symbols('r w', positive=True)
H = sp.Function('H')(r)
F = sp.Function('F')(r)
Hr = sp.diff(H, r); Hrr = sp.diff(H, r, 2)
Fr = sp.diff(F, r); Frr = sp.diff(F, r, 2)

# ---- O(A^1) WAVE operator (from reduce.py "remainder", the traceless l=2 eqn,
# divided by the angular P2 factor (3cos^2-1)/... and by cos(w t)).
# reduce.py remainder = [ -r*(3 w^2 H cos^2 - w^2 H + 3 H'' cos^2 - H'')/2
#                          - (3cos^2-1) H' ] / r
# Factor angular: let X=cos^2. group (3X-1): coefficient of (3X-1) is
#   -r/2*(w^2 H + H'')  ... check: 3X*(-r/2)(w^2H+H'') + (+r/2)(w^2H+H'')??
# Cleanest: the eqn is proportional to P2=(3cos^2-1)/2. Divide remainder by P2.
P2 = (3 * sp.cos(sp.Symbol('theta'))**2 - 1) / 2
rem_wave = (-r * (3 * w**2 * H * sp.cos(sp.Symbol('theta'))**2 - w**2 * H
                  + 3 * sp.cos(sp.Symbol('theta'))**2 * Hrr - Hrr) / 2
            - (3 * sp.cos(sp.Symbol('theta'))**2 - 1) * Hr) / r
wave_op = sp.simplify(rem_wave / P2)
print("=== O(A^1) WAVE operator (remainder / P2) ===")
print("  L_wave[H] =", sp.simplify(wave_op))
# normalize to -H'' form
wo = sp.expand(wave_op)
a2 = sp.simplify(wo.coeff(Hrr)); a1 = sp.simplify(wo.coeff(Hr))
a0 = sp.simplify((wo - a2 * Hrr - a1 * Hr).coeff(H))
print("  coeff H'':", a2, " H':", a1, " H:", a0)
if a2 != 0:
    print("  => -H'' + (%s)H' + (%s)H = 0" %
          (sp.simplify(-a1 / a2), sp.simplify(-a0 / a2)))
    print("     (expect -H'' - (2/r)H' + 6/r^2 H = w^2 H : the flat l=2 operator,")
    print("      phi ENTERS WAVE ONLY AT O(A^2) -> source of the w(A) bend.)")

# ---- O(A^2) l=0 phi-equation from G_tt (time-averaged sin^2 -> 1/2) ----
# reduce.py G_tt@O(A^2), x40r^2 = 0:
#   r^2(-2 w^2 H^2 sin^2 + 4 H H'' + 3 H'^2) + 4r(3 H H' + 20 F') + 80 F + 12 H^2
# time-avg sin^2 -> 1/2:
Gtt2 = (r**2 * (-2 * w**2 * H**2 * sp.Rational(1, 2) + 4 * H * Hrr + 3 * Hr**2)
        + 4 * r * (3 * H * Hr + 20 * Fr) + 80 * F + 12 * H**2) / (40 * r**2)
Gtt2 = sp.expand(Gtt2)
print("\n=== O(A^2) l=0 phi-equation from G_tt (=0) ===")
bF = sp.simplify(Gtt2.coeff(F)); bFr = sp.simplify(Gtt2.coeff(Fr)); bFrr = sp.simplify(Gtt2.coeff(Frr))
Src_tt = sp.simplify(Gtt2 - bF * F - bFr * Fr - bFrr * Frr)
print("  coeff F'':", bFrr, "  F':", bFr, "  F:", bF)
print("  Src_tt[H] (geon GW stress):", Src_tt)
print("  => F-operator: %s F' + %s F = -Src_tt" % (bFr, bF))
print("     i.e. (since 2/r F' + 2/r^2 F = (2/r^2) d/dr(r F)):  d/dr(r F) = -(Src_tt)*r^2/2")

# ---- O(A^2) l=0 from G_rr (second relation / check) ----
Grr2 = (r**2 * (6 * w**2 * H**2 * sp.Rational(1, 2) - 4 * w**2 * H**2 - Hr**2)
        - 4 * r * (H * Hr + 20 * Fr) - 80 * F - 12 * H**2) / (40 * r**2)
Grr2 = sp.expand(Grr2)
print("\n=== O(A^2) l=0 from G_rr (=0) ===")
cF = sp.simplify(Grr2.coeff(F)); cFr = sp.simplify(Grr2.coeff(Fr)); cFrr = sp.simplify(Grr2.coeff(Frr))
Src_rr = sp.simplify(Grr2 - cF * F - cFr * Fr - cFrr * Frr)
print("  coeff F'':", cFrr, "  F':", cFr, "  F:", cF)
print("  Src_rr[H]:", Src_rr)

# Misner-Sharp effective mass read-off: m(r) = r(1 - e^{-2phi}) ~ 2 r phi = 2 A^2 r F
# (to O(A^2)). dm/dr sign tells if positive effective mass.
print("\n=== Misner-Sharp deficit (to O(A^2)): m = r(1-e^{-2phi}) ~ 2 A^2 r F ===")
print("  m(r)/A^2 ~ 2 r F(r);  positive effective mass <=> F>0 (and m increasing).")

# ---- lambdify for the solver ----
import sympy
mods = [{'cos': sympy.cos}, 'numpy']
# Wave operator as function of (H, Hr, Hrr, w, r): L_wave = -H'' -(2/r)H' + 6/r^2 H - w^2 H
# (we will assert the symbolic normalization equals this)
print("\n=== sanity: does wave op == -H''-(2/r)H'+6/r^2 H - w^2 H ? ===")
target = -Hrr - (2 / r) * Hr + (6 / r**2) * H - w**2 * H
print("  wave_op - target (normalized) =",
      sp.simplify(sp.simplify(wave_op / a2) - target) if a2 != 0 else "n/a")

# Source for phi solver, written as  L_F[F] = RHS[H]:
# From G_tt:  (2/r)F' + (2/r^2)F  = -(Src_tt)
print("\n=== phi solver form ===")
LF = sp.simplify(bFr * Fr + bF * F)
print("  L_F[F] =", LF, "   (=", sp.simplify(LF * r**2 / 2), " /(r^2/2) )")
print("  RHS_H = -Src_tt =", sp.simplify(-Src_tt))
print("  multiply by r^2/2:  (r F)'  =  -(r^2/2) Src_tt  [Misner-Sharp form]")
RHS_MS = sp.simplify(-(r**2 / 2) * Src_tt)
print("  (r F)' = ", RHS_MS)
