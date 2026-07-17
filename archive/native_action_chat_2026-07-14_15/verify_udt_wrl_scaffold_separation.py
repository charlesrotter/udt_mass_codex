#!/usr/bin/env python3
"""Exact inverse-variational audit of WR-L in the local F(Y) class.

The script uses the full reciprocal physical metric, varies before inserting
WR-L, solves the resulting ODE for F'(Y), and audits regularity and X
universality. It does not claim to exhaust all possible UDT actions.
"""

import sympy as sp


checks = []


def check(name, statement):
    ok = bool(statement)
    checks.append((name, ok))
    print(f"[{'PASS' if ok else 'FAIL'}] {name}")
    if not ok:
        raise AssertionError(name)


r, X, c = sp.symbols("r X c", positive=True)
phi = sp.Function("phi")(r)
phip = sp.diff(phi, r)
Aphi = sp.exp(-2 * phi)

# Full reciprocal physical metric data.
gtt = -c**2 * Aphi
grr = 1 / Aphi
det2 = sp.simplify(gtt * grr)
check("reciprocal radial determinant is field independent", det2 == -c**2)

# Group-current scalar in the static radial sector.
Yphi = sp.simplify(Aphi * phip**2)
check("physical-metric current scalar", Yphi == sp.exp(-2 * phi) * phip**2)

# Verify the arbitrary-F chain-rule Euler structure on a nonlinear test
# function; the displayed general result then follows by replacing the test
# derivative with p(Y)=F'(Y).
alpha = sp.symbols("alpha", real=True)
Ftest = Yphi / 2 + alpha * Yphi**2 / 4
Ltest = r**2 * Ftest
ELtest = sp.simplify(sp.diff(sp.diff(Ltest, phip), r) - sp.diff(Ltest, phi))
ptest = sp.diff(sp.Symbol("y") / 2 + alpha * sp.Symbol("y")**2 / 4,
                sp.Symbol("y")).subs(sp.Symbol("y"), Yphi)
ELmanual = sp.simplify(
    sp.diff(2 * r**2 * ptest * Aphi * phip, r)
    + 2 * r**2 * Yphi * ptest)
check("full nonlinear arbitrary-F Euler chain rule", sp.simplify(ELtest - ELmanual) == 0)

# WR-L data are inserted only after the variation formula is established.
A_wrl = 1 - r / X
phi_wrl = -sp.log(A_wrl) / 2
phip_wrl = sp.simplify(sp.diff(phi_wrl, r))
Y_wrl = sp.simplify(A_wrl * phip_wrl**2)
check("WR-L depth derivative",
      sp.simplify(phip_wrl - 1 / (2 * (X - r))) == 0)
check("WR-L current scalar",
      sp.simplify(Y_wrl - 1 / (4 * X * (X - r))) == 0)
check("WR-L current derivative", sp.simplify(sp.diff(Y_wrl, r) - 4 * X * Y_wrl**2) == 0)
check("regular-center current value", sp.limit(Y_wrl, r, 0, dir="+") == 1 / (4 * X**2))
check("wall current diverges", sp.limit(Y_wrl, r, X, dir="-") == sp.oo)

# Convert the WR-L Euler equation into an ODE for p(Y)=F'(Y).
y = sp.symbols("y", positive=True)
p = sp.Function("p")(y)
z = 4 * X**2 * y
r_of_y = X - 1 / (4 * X * y)
ode_lhs = sp.simplify(
    2 * p
    + r_of_y * (4 * X * y**2) * sp.diff(p, y)
    + 2 * X * r_of_y * y * p)
ode_canonical = sp.simplify(
    y * (z - 1) * sp.diff(p, y) + (z + 3) * p / 2)
check("inverse Euler equation reduction", sp.simplify(ode_lhs - ode_canonical) == 0)

# Exact nonzero solution on y>1/(4X^2).
C = sp.symbols("C", positive=True)
p_solution = C * z**sp.Rational(3, 2) / (z - 1)**2
solution_residual = sp.simplify(
    y * (z - 1) * sp.diff(p_solution, y) + (z + 3) * p_solution / 2)
check("exact inverse solution for F prime", solution_residual == 0)

# Regularity audit at the WR-L center z=1.
zeta = sp.symbols("zeta", positive=True)
p_zeta = C * zeta**sp.Rational(3, 2) / (zeta - 1)**2
check("required F prime diverges at regular center",
      sp.limit(p_zeta, zeta, 1, dir="+") == sp.oo)
check("center singularity is inverse square",
      sp.limit((zeta - 1)**2 * p_zeta, zeta, 1, dir="+") == C)
check("only zero integration coefficient removes singularity",
      sp.simplify(p_solution.subs(C, 0)) == 0)

# The canonical quadratic action p=constant fails the same general ODE.
p0 = sp.symbols("p0", nonzero=True)
quadratic_ode_residual = sp.simplify((z + 3) * p0 / 2)
check("constant F prime fails inverse equation", quadratic_ode_residual != 0)

# Recover its direct Euler residual in A variables.
A = sp.Function("A")(r)
Aprime = sp.diff(A, r)
Lquadratic = r**2 * Aprime**2 / (4 * A)
ELquadratic = sp.factor(sp.simplify(
    sp.diff(sp.diff(Lquadratic, Aprime), r) - sp.diff(Lquadratic, A)))
ELquad_wrl = sp.factor(ELquadratic.subs({
    A: A_wrl,
    sp.diff(A, r): -1 / X,
    sp.diff(A, r, 2): 0,
}))
expected_quad = -r * (4 * X - 3 * r) / (4 * (X - r)**2)
check("direct quadratic WR-L residual", sp.simplify(ELquad_wrl - expected_quad) == 0)

# X-universality audit.  Normalized required derivatives for X=1 and X=2
# are not proportional functions of y, so normalization cannot make one F
# support both profiles.
p_x1 = (4 * y)**sp.Rational(3, 2) / (4 * y - 1)**2
p_x2 = (16 * y)**sp.Rational(3, 2) / (16 * y - 1)**2
ratio = sp.simplify(p_x1 / p_x2)
check("distinct-X inverse solutions are not normalization equivalent",
      sp.simplify(sp.diff(ratio, y)) != 0)

# The wall remains infinite group depth; this says nothing about the action
# scale or the coordinate location X.
check("WR-L wall is infinite positional depth",
      sp.limit(phi_wrl, r, X, dir="-") == sp.oo)

passed = sum(ok for _, ok in checks)
print(f"ALL CONSISTENT ({passed}/{len(checks)} checks pass)")
print(f"SymPy {sp.__version__}")
