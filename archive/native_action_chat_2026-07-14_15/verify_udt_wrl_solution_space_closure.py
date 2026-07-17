#!/usr/bin/env python3
"""Exact self-checks for the WR-L solution-space closure audit.

This verifies encoded geometry and operator algebra.  It does not select an
action, a boundary ontology, a self-adjoint domain, or a mass normalization.
"""

import sympy as sp


checks = []


def check(name, statement):
    ok = bool(statement)
    checks.append((name, ok))
    print(f"[{'PASS' if ok else 'FAIL'}] {name}")
    if not ok:
        raise AssertionError(name)


r, X = sp.symbols("r X", positive=True, finite=True)
x, s = sp.symbols("x s", real=True)
alpha = sp.symbols("alpha", real=True)
ell = sp.symbols("ell", integer=True, nonnegative=True)

A = 1 - r / X
N = sp.sqrt(A)

# Residual re-centering family and endpoint lengths.
A_alpha = (1 - r / X) ** alpha
proper_primitive = -X * (1 - r / X) ** (1 - alpha / 2) / (1 - alpha / 2)
optical_primitive = -X * (1 - r / X) ** (1 - alpha) / (1 - alpha)
check("general proper-radius primitive",
      sp.simplify(sp.diff(proper_primitive, r) - (1 - r / X) ** (-alpha / 2)) == 0)
check("general optical-radius primitive",
      sp.simplify(sp.diff(optical_primitive, r) - (1 - r / X) ** (-alpha)) == 0)
check("WR-L proper radius is 2X",
      sp.integrate(A ** (-sp.Rational(1, 2)), (r, 0, X)) == 2 * X)
rstar = -X * sp.log(A)
check("WR-L tortoise derivative", sp.simplify(sp.diff(rstar, r) - 1 / A) == 0)
check("WR-L tortoise diverges at the wall", sp.limit(rstar, r, X, dir="-") == sp.oo)

# Static-slice volume and proper coordinate.
V = 4 * sp.pi * sp.integrate(r**2 / sp.sqrt(A), (r, 0, X))
check("WR-L static-patch volume", sp.simplify(V - 64 * sp.pi * X**3 / 15) == 0)
r_of_s = s - s**2 / (4 * X)
check("proper-coordinate radial profile",
      sp.expand(1 - r_of_s / X - (1 - s / (2 * X)) ** 2) == 0)
check("proper-coordinate horizon radius", r_of_s.subs(s, 2 * X) == X)
check("proper-coordinate horizon is an area extremum", sp.diff(r_of_s, s).subs(s, 2 * X) == 0)

# Four- and three-dimensional curvature scalars for the reciprocal metric.
R4 = -sp.diff(A, r, 2) - 4 * sp.diff(A, r) / r + 2 * (1 - A) / r**2
R3 = 2 * (1 - A - r * sp.diff(A, r)) / r**2
K4 = (sp.diff(A, r, 2))**2 + (2 * sp.diff(A, r) / r)**2 + (2 * (1 - A) / r**2)**2
check("four-dimensional Ricci scalar", sp.simplify(R4 - 6 / (X * r)) == 0)
check("static-slice Ricci scalar", sp.simplify(R3 - 4 / (X * r)) == 0)
check("Kretschmann scalar", sp.simplify(K4 - 8 / (X**2 * r**2)) == 0)
check("wall Ricci scalar is finite", sp.limit(R4, r, X, dir="-") == 6 / X**2)
check("wall Kretschmann scalar is finite", sp.limit(K4, r, X, dir="-") == 8 / X**4)
check("seat Ricci scalar diverges", sp.limit(R4, r, 0, dir="+") == sp.oo)
check("seat Kretschmann scalar diverges", sp.limit(K4, r, 0, dir="+") == sp.oo)

IR4 = 4 * sp.pi * sp.integrate(R4 * r**2 / sp.sqrt(A), (r, 0, X))
IR3 = 4 * sp.pi * sp.integrate(R3 * r**2 / sp.sqrt(A), (r, 0, X))
IK4 = 4 * sp.pi * sp.integrate(K4 * r**2 / sp.sqrt(A), (r, 0, X))
check("integrated four-dimensional Ricci scalar", sp.simplify(IR4 - 32 * sp.pi * X) == 0)
check("integrated static-slice Ricci scalar", sp.simplify(IR3 - 64 * sp.pi * X / 3) == 0)
check("integrated Kretschmann scalar", sp.simplify(IK4 - 64 * sp.pi / X) == 0)
check("volume-average four-dimensional Ricci scalar", sp.simplify(IR4 / V - 15 / (2 * X**2)) == 0)
check("volume-average static-slice Ricci scalar", sp.simplify(IR3 / V - 5 / X**2) == 0)

# Ingoing null coordinate has a nonsingular (v,r) block at A=0.
ef_block = sp.Matrix([[-A, 1], [1, 0]])
check("ingoing-null metric block determinant", ef_block.det() == -1)
check("ingoing-null metric block finite at wall",
      ef_block.subs(r, X) == sp.Matrix([[0, 1], [1, 0]]))
q = sp.symbols("q", positive=True)
crossing_norm = -A - 2 * q
check("explicit crossing curve is timelike at wall", crossing_norm.subs(r, X) == -2 * q)
check("constant-v radial curve is null", ef_block[1, 1] == 0)

# Spatial lapse identity and raw flux.
laplace_N = sp.sqrt(A) / r**2 * sp.diff(r**2 * sp.sqrt(A) * sp.diff(N, r), r)
check("spatial lapse Laplacian", sp.simplify(laplace_N + N / (X * r)) == 0)
check("lapse-curvature identity using R4", sp.simplify(laplace_N + R4 * N / 6) == 0)
check("lapse-curvature identity using R3", sp.simplify(laplace_N + R3 * N / 4) == 0)
norm_N = 4 * sp.pi * sp.integrate(N**2 * r**2 / sp.sqrt(A), (r, 0, X))
check("spatial lapse zero mode has finite norm", sp.simplify(norm_N - 64 * sp.pi * X**3 / 105) == 0)

flux_N = 4 * sp.pi * r**2 * sp.sqrt(A) * sp.diff(N, r)
check("raw lapse flux on a sphere", sp.simplify(flux_N + 2 * sp.pi * r**2 / X) == 0)
check("raw lapse flux at wall", sp.limit(flux_N, r, X, dir="-") == -2 * sp.pi * X)
check("raw lapse flux at seat", sp.limit(flux_N, r, 0, dir="+") == 0)
bulk_laplace_N = 4 * sp.pi * sp.integrate(laplace_N * r**2 / sp.sqrt(A), (r, 0, X))
check("lapse divergence theorem", sp.simplify(bulk_laplace_N + 2 * sp.pi * X) == 0)

p = sp.symbols("p", real=True)
eps = sp.symbols("eps", positive=True)
flux_Ap = 4 * sp.pi * r**2 * sp.sqrt(A) * sp.diff(A**p, r)
check("power-lapse flux formula",
      sp.simplify(flux_Ap + 4 * sp.pi * p * r**2 * A ** (p - sp.Rational(1, 2)) / X) == 0)
check("A flux vanishes at wall", sp.limit(flux_Ap.subs(p, 1), r, X, dir="-") == 0)
check("sqrt(A) is finite-nonzero threshold",
      sp.limit(flux_Ap.subs(p, sp.Rational(1, 2)), r, X, dir="-") == -2 * sp.pi * X)
check("quarter-power flux diverges",
      sp.limit(flux_Ap.subs({p: sp.Rational(1, 4), r: X - eps}), eps, 0, dir="+") == -sp.oo)

# Scalar d'Alembertian radial reduction.
u = sp.Function("u")(r)
Rrad = u / r
k2, L = sp.symbols("k2 L", real=True)
radial_eq = sp.diff(r**2 * A * sp.diff(Rrad, r), r) + (k2 * r**2 / A - L) * Rrad
Dstar2u = A * sp.diff(A * sp.diff(u, r), r)
Vell = A * (L / r**2 + sp.diff(A, r) / r)
schrodinger_eq = Dstar2u + (k2 - Vell) * u
check("d'Alembertian-to-tortoise reduction",
      sp.simplify(A * radial_eq / r - schrodinger_eq) == 0)
check("WR-L scalar potential",
      sp.simplify(Vell - A * (L / r**2 - 1 / (X * r))) == 0)
check("wave potential vanishes at horizon", sp.limit(Vell, r, X, dir="-") == 0)

V0 = Vell.subs(L, 0)
zero_resonance = -A * sp.diff(A * sp.diff(r, r), r) + V0 * r
check("ell=0 exact zero-energy resonance u=r", sp.simplify(zero_resonance) == 0)

wave_norm_primitive = X**3 * (-x**2 / 2 - x - sp.log(1 - x))
check("constant-mode wave-norm primitive",
      sp.simplify(sp.diff(wave_norm_primitive, x) - X**3 * x**2 / (1 - x)) == 0)
check("constant mode is not wave-normalizable at horizon",
      sp.limit(wave_norm_primitive, x, 1, dir="-") == sp.oo)

# Static multipole energy identity (the endpoint term must be kept).
f = sp.Function("f")(r)
P = r**2 * A
identity = sp.diff(P * f * sp.diff(f, r), r) - (
    P * sp.diff(f, r)**2 + f * sp.diff(P * sp.diff(f, r), r)
)
check("static multipole integration-by-parts identity", sp.simplify(identity) == 0)

# Spatial and spacetime-static operators differ even on the test scalar f=r.
op_4d_on_r = sp.diff(r**2 * A, r) / r**2
op_3d_on_r = sp.sqrt(A) * sp.diff(r**2 * sp.sqrt(A), r) / r**2
check("spatial and spacetime-static scalar operators are inequivalent",
      sp.simplify(op_4d_on_r - op_3d_on_r - sp.diff(A, r) / 2) == 0)

# The lapse-curvature identity characterizes a simple reciprocal solution family.
Ag = sp.Function("Ag")(r)
ode_A = r**2 * sp.diff(Ag, r, 2) + r * sp.diff(Ag, r) - Ag + 1
c1, c2 = sp.symbols("c1 c2")
general_A = 1 + c1 * r + c2 / r
check("curvature-lapse zero-mode ODE family", sp.simplify(ode_A.subs(Ag, general_A).doit()) == 0)
check("bounded-seat plus wall selects WR-L within that family",
      sp.simplify(general_A.subs({c2: 0, c1: -1 / X}) - A) == 0)

# A minimal inverse radial functional has that ODE, but is not thereby a native action.
L_inverse = sp.Rational(1, 2) * (
    r * sp.diff(Ag, r)**2 + (Ag - 1)**2 / r
)
EL_inverse = sp.diff(sp.diff(L_inverse, sp.diff(Ag, r)), r) - sp.diff(L_inverse, Ag)
check("inverse radial functional Euler equation", sp.simplify(r * EL_inverse - ode_A) == 0)
square_form = sp.Rational(1, 2) * r * (
    sp.diff(Ag, r) - (Ag - 1) / r
) ** 2 + sp.Rational(1, 2) * sp.diff((Ag - 1)**2, r)
check("inverse functional square completion", sp.simplify(L_inverse - square_form) == 0)
I_wrl = sp.integrate(L_inverse.subs(Ag, A).doit(), (r, 0, X))
check("WR-L saturates inverse-functional bound for every X", sp.simplify(I_wrl - sp.Rational(1, 2)) == 0)

# The tempting covariant-looking fixed-spatial-metric functional fails after
# reciprocity ties the spatial metric to N and the reduced functional is varied.
n = sp.Function("n")(r)
L_reciprocal_reduced = (
    sp.Rational(1, 2) * r**2 * n * sp.diff(n, r)**2
    - n / 4 + n**3 / 4 + sp.Rational(1, 2) * r * n**2 * sp.diff(n, r)
)
EL_reciprocal_reduced = (
    sp.diff(sp.diff(L_reciprocal_reduced, sp.diff(n, r)), r)
    - sp.diff(L_reciprocal_reduced, n)
)
EL_on_wrl = sp.factor(sp.simplify(EL_reciprocal_reduced.subs(n, N).doit()))
check("fixed-metric curvature-lapse functional fails reciprocal reduced variation",
      sp.simplify(EL_on_wrl - r * (5 * r - 6 * X) / (8 * X * (X - r))) == 0)

# Homothetic scaling: all dimensionless shape data lose X.
check("dimensionless Ricci shape", sp.simplify((X**2 * R4).subs(r, X * x) - 6 / x) == 0)
check("dimensionless Kretschmann shape", sp.simplify((X**4 * K4).subs(r, X * x) - 8 / x**2) == 0)
check("dimensionless volume", sp.simplify(V / X**3 - 64 * sp.pi / 15) == 0)
check("dimensionless wall lapse flux", sp.simplify((-2 * sp.pi * X) / X + 2 * sp.pi) == 0)

passed = sum(ok for _, ok in checks)
print(f"ALL CONSISTENT ({passed}/{len(checks)} checks pass)")
print(f"SymPy {sp.__version__}")
