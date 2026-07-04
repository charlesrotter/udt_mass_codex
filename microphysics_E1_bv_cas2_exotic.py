"""microphysics_E1_bv_cas2_exotic.py -- BLIND VERIFIER chunk 2: core-class exclusion (attack 4).

Deriver probed: (1) regular rho_c>0; (2) phi->-inf with rho bounded below [flux law, exact];
(3) rho->0 regular [banked R2]; (4) rho->0 power-law with phi = beta ln s [K7'].
Deriver did NOT probe (named exotic-open): essential-singular phi, log-corrected phi, rho->inf.
This script probes those three EXTRA classes against the phi-EOM (rho^2 phi')' = (4/Z)e^{-2phi}rho'^2
(a NECESSARY condition; matter-independent since all matter is phi-blind -- verified bv_cas1 A3/A4).

Method: leading-order asymptotics as s->0+ via sympy limits of RHS/LHS (or sign clash).
"""
import sympy as sp

s = sp.symbols('s', positive=True)
Z, a, c, p0 = sp.symbols('Z a c phi0', positive=True)
al, be, pp, gam = sp.symbols('alpha beta p gamma', positive=True)
BAD = []


def ck(name, cond):
    print(("PASS " if cond else "FAIL ") + name)
    if not cond:
        BAD.append(name)


def lhs_rhs(rho_e, phi_e):
    L = sp.diff(rho_e**2 * sp.diff(phi_e, s), s)
    R = (4 / Z) * sp.exp(-2 * phi_e) * sp.diff(rho_e, s)**2
    return sp.simplify(L), sp.simplify(R)


# ---- X1: essential-singular phi -> -inf: phi = -c s^{-p}, rho = a s^alpha (rho -> 0) ----------
L1, R1 = lhs_rhs(a * s**al, -c * s**(-pp))
# ratio RHS/LHS ~ e^{2c s^-p} * s^p -> infinity: exponential in RHS, pure power in LHS.
rat1 = sp.simplify(R1 / L1)
lim1 = sp.limit(rat1.subs([(al, sp.Rational(1, 3)), (pp, sp.Rational(1, 2)),
                           (a, 1), (c, 1), (Z, 8)]), s, 0, '+')
ck("X1 essential phi=-c/s^p, rho=a s^alpha: RHS/LHS -> oo (rep. exponents 1/3,1/2)  => NO balance",
   lim1 == sp.oo)
# generic-exponent structure: RHS carries exp(+2c s^-p); LHS is a pure power => no cancellation
ck("X1' RHS contains exp(+2c s^-p) while LHS is exponential-free (structural)",
   R1.has(sp.exp) and not L1.has(sp.exp))

# ---- X2: rho -> infinity power-law core: rho = a s^{-alpha}, phi = beta ln s + phi0 ----------
L2, R2 = lhs_rhs(a * s**(-al), be * sp.log(s) + p0)
L2c = sp.simplify(L2 / s**(-2 * al - 2))          # coefficient of s^{-2al-2}
R2c = sp.simplify(R2 * s**(2 * al + 2 + 2 * be))  # coefficient of s^{-2al-2-2be}
# beta > 0 (phi -> -inf): RHS order s^{-2al-2-2be} strictly dominates LHS s^{-2al-2}; and
# LHS coefficient a^2 be (-2al-1) < 0 while RHS coefficient > 0: double obstruction.
ck("X2 rho->inf power law: LHS coeff = -a^2 be (2al+1) < 0, RHS coeff > 0, RHS lower order "
   "=> NO balance (sign AND order clash)",
   sp.simplify(L2c + a**2 * be * (2 * al + 1)) == 0
   and sp.simplify(R2c - (4 / Z) * sp.exp(-2 * p0) * a**2 * al**2) == 0)

# ---- X3: log-corrected dive: phi = beta ln s + gamma ln(ln(1/s)) + phi0, rho = a s^alpha -----
phi3 = be * sp.log(s) + gam * sp.log(sp.log(1 / s)) + p0
L3, R3 = lhs_rhs(a * s**al, phi3)
rat3 = sp.simplify(R3 / L3)
lim3 = sp.limit(rat3.subs([(al, 1), (be, sp.Rational(1, 2)), (gam, 1), (a, 1), (c, 1), (Z, 8), (p0, 1)]),
                s, 0, '+')
lim3b = sp.limit(rat3.subs([(al, 2), (be, sp.Rational(1, 4)), (gam, 3), (a, 1), (Z, 8), (p0, 2)]),
                 s, 0, '+')
ck("X3 log-corrected (beta>0, any gamma): RHS/LHS -> oo (two representative exponent sets) "
   "=> log corrections cannot bridge the s^{-2 beta} power gap", lim3 == sp.oo and lim3b == sp.oo)

# ---- X4: alpha = 1/2 special lane of K7' re-checked independently, with a correction term:
#      Phi = rho^2 phi' = const + c1 s^g (g > 0): Phi' = c1 g s^{g-1} must match RHS ~ s^{-1-2be}
#      => g = -2 be < 0, contradiction with g > 0.  (deriver's prose claim, made exact)
g_, c1 = sp.symbols('g c1', positive=True)
match_exp = sp.solve(sp.Eq(g_ - 1, -1 - 2 * be), g_)
ck("X4 alpha=1/2 lane: correction exponent must satisfy g = -2 beta < 0 -- impossible for g>0",
   match_exp == [-2 * be])

print()
print("FAILED:" if BAD else "ALL BV-CAS2 (EXOTIC CLASS) CHECKS PASS", BAD if BAD else "")
import sys
sys.exit(1 if BAD else 0)
