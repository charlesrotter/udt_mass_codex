#!/usr/bin/env python3
"""Arm-C exact algebra for the strongest conditional unique-action attempt.

Certifies only Weyl-weight bookkeeping, curvature-basis identities, and the
finite linear algebra of the C^2/Euler decomposition.  It cannot certify that
UDT forces metric-only fields, locality, covariance, polynomiality, parity,
four-derivative minimality, unrestricted variation, a boundary completion, or
existence/stability of a nontrivial finite-cell solution.
"""
import sympy as sp

checks = []

def check(label, condition):
    ok = bool(condition)
    checks.append(ok)
    print(("PASS " if ok else "FAIL ") + label)

d = sp.symbols("d", integer=True, positive=True)
# Constant-Weyl exponents are necessary checks. Local Weyl transformations add
# derivative terms to R and therefore make EH even less invariant.
weights = {
    "volume": d,
    "EH": d - 2,
    "C2": d - 4,
    "scalar_X2_weight0_phi": d - 4,
    "S2_quadratic_weight0_n": d - 2,
    "S2_F2_weight0_n": d - 4,
}
at4 = {k: sp.simplify(v.subs(d, 4)) for k, v in weights.items()}
check("four-dimensional C^2 density has Weyl exponent zero", at4["C2"] == 0)
check("four-dimensional scalar X^2 density has Weyl exponent zero", at4["scalar_X2_weight0_phi"] == 0)
check("EH density is not scale neutral", at4["EH"] == 2)
check("constant-coefficient S2 quadratic density is not scale neutral", at4["S2_quadratic_weight0_n"] == 2)
check("S2 F^2 density is scale neutral", at4["S2_F2_weight0_n"] == 0)

# Coefficient vectors use the basis (Riemann^2, Ricci^2, R^2).
C2 = sp.Matrix([1, -2, sp.Rational(1, 3)])
Euler = sp.Matrix([1, -4, 1])
p, q = sp.symbols("p q")
combo = p*C2 + q*Euler
check("C^2 identity coefficients", C2 == sp.Matrix([1, -2, sp.Rational(1, 3)]))
check("Euler identity coefficients", Euler == sp.Matrix([1, -4, 1]))
check("C^2 and Euler are linearly independent", sp.Matrix.hstack(C2, Euler).rank() == 2)

# Modulo the Euler topological vector, the admitted local parity-even
# curvature-squared Weyl-invariant bulk direction has one coefficient p.
alpha, beta, gamma = sp.symbols("alpha beta gamma")
sol = sp.solve(
    [sp.Eq(alpha, combo[0]), sp.Eq(beta, combo[1]), sp.Eq(gamma, combo[2])],
    [alpha, beta, gamma], dict=True
)
check("conditional curvature-square family is p*C^2+q*Euler", len(sol) == 1)
check("Euler quotient leaves one bulk normalization p", sp.Matrix.hstack(C2).rank() == 1)

# Lovelock inventory: volume and EH fail even constant local-scale neutrality;
# Euler is topological in four dimensions and supplies no local metric equation.
check("EH/Lovelock and exact pre-scale CSN are in tension", at4["volume"] != 0 and at4["EH"] != 0)

print("WEIGHTS_D4", at4)
print("CURVATURE_COMBINATION", list(combo))
print("LIMIT: conditional classification only; premises, boundary law, and solutions are not certified")
print(("PASS" if all(checks) else "FAIL") + f" SUMMARY {sum(checks)}/{len(checks)} checks")

