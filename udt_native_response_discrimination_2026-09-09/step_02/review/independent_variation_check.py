"""Independent symbolic coordinate/tensor check; imports no scientific repo code."""
import hashlib
import json
import platform
from pathlib import Path

import sympy as s


checks = 0
records = []


def same(actual, expected, label):
    global checks
    difference = s.simplify(actual - expected)
    assert difference == 0, (label, actual, expected, difference)
    checks += 1


def matrix_same(actual, expected, label):
    for a in range(4):
        for b in range(4):
            same(actual[a, b], expected[a, b], f"{label}_{a}{b}")


def square_tf(matrix):
    squared = matrix * matrix
    return squared - s.trace(squared) * s.eye(4) / 4


t, r, theta, phi = s.symbols("t r theta phi", real=True)
epsilon, b0 = s.symbols("epsilon b0", real=True)
coords = (t, r, theta, phi)
F = s.Function("F")(r)
H = s.Function("H")(r)
metric = s.diag(-F, 1 / F, r**2, r**2 * s.sin(theta)**2)
inverse = metric.inv()
dg = [[[s.diff(metric[a, b], x) for x in coords] for b in range(4)] for a in range(4)]
connection = [[[s.simplify(sum(inverse[a, d] *
    (dg[d][c][b] + dg[d][b][c] - dg[b][c][d]) for d in range(4)) / 2)
    for c in range(4)] for b in range(4)] for a in range(4)]
ricci = s.zeros(4)
for a in range(4):
    for b in range(4):
        value = 0
        for c in range(4):
            value += s.diff(connection[c][a][b], coords[c])
            value -= s.diff(connection[c][a][c], coords[b])
            for d in range(4):
                value += connection[c][a][b] * connection[d][c][d]
                value -= connection[d][a][c] * connection[c][b][d]
        ricci[a, b] = s.simplify(value)

mixed = s.simplify(inverse * ricci)
# The reduced expressions are comparison targets, not construction inputs.
E0 = r * s.diff(F, r) + F - 1
E1 = r * s.diff(F, r) + r**2 * s.diff(F, r, 2) / 2
matrix_same(mixed, s.diag(-E1/r**2, -E1/r**2, -E0/r**2, -E0/r**2),
            "independent_full_coordinate_Ricci")
Q = square_tf(mixed).applyfunc(s.simplify)
S = (mixed - s.trace(mixed) * s.eye(4) / 4).applyfunc(s.simplify)

f0 = 1 + b0/r
fe = f0 + epsilon * H
replacement = {F: fe, s.diff(F, r): s.diff(fe, r),
               s.diff(F, r, 2): s.diff(fe, r, 2)}
Me = mixed.xreplace(replacement).applyfunc(s.simplify)
Qe = Q.xreplace(replacement).applyfunc(s.factor)
Se = S.xreplace(replacement).applyfunc(s.simplify)
ge = metric.xreplace(replacement)
g0 = metric.subs(F, f0)
matrix_same(Me.subs(epsilon, 0), s.zeros(4), "arbitrary_Ricci_flat_b0")
matrix_same(Qe.diff(epsilon).subs(epsilon, 0), s.zeros(4), "DQ_zero_all_H")
N = Me.diff(epsilon).subs(epsilon, 0)
leading = Qe.diff(epsilon, 2).subs(epsilon, 0) / 2
matrix_same(leading, square_tf(N), "mixed_second_coefficient")
Qcov = ge * Qe
matrix_same(Qcov.diff(epsilon).subs(epsilon, 0), s.zeros(4), "covariant_DQ_zero")
matrix_same(Qcov.diff(epsilon, 2).subs(epsilon, 0) / 2,
            g0 * square_tf(N), "covariant_second_coefficient")
matrix_same((ge * Se).diff(epsilon).subs(epsilon, 0),
            g0 * (N - s.trace(N) * s.eye(4) / 4), "DS_covariant")
angle = (E1 - E0).xreplace(replacement).expand()
same(angle.diff(epsilon).subs(epsilon, 0), r**2*s.diff(H, r, 2)/2-H,
     "angular_first_variation")


def substitute_direction(expr, h):
    return expr.xreplace({H: h, s.diff(H, r): s.diff(h, r),
                         s.diff(H, r, 2): s.diff(h, r, 2)}).applyfunc(s.simplify)


for exponent in range(-4, 5):
    h = r**exponent
    observed = substitute_direction(leading, h)
    coefficient = s.Rational((exponent + 1)**2 * (exponent**2 - 4), 8) * r**(2*exponent-4)
    matrix_same(observed, s.diag(coefficient, coefficient, -coefficient, -coefficient),
                f"monomial_{exponent}")
    expected_zero = exponent in (-2, -1, 2)
    assert (observed == s.zeros(4)) == expected_zero
    checks += 1
    records.append({"power": exponent, "quadratic_obstruction_zero": expected_zero})

alpha, beta, delta = s.symbols("alpha beta delta", real=True)
family_h = alpha*r**2 + beta/r + delta/r**2
family_leading = substitute_direction(leading, family_h)
target = 6*alpha*delta/r**4
matrix_same(family_leading, s.diag(target, target, -target, -target),
            "three_parameter_family_obstruction")
matrix_same(substitute_direction(Qe, family_h),
            epsilon**2*s.diag(target, target, -target, -target),
            "exact_mixed_Q_family")
matrix_same(family_leading.subs(delta, 0), s.zeros(4), "E_integrable")
matrix_same(family_leading.subs(alpha, 0), s.zeros(4), "Z_integrable")
assert family_leading.subs({alpha: 1, delta: 1}) != s.zeros(4)
checks += 1
ds_h = substitute_direction(Se.diff(epsilon).subs(epsilon, 0), family_h)
matrix_same(ds_h, s.diag(-delta/r**4, -delta/r**4, delta/r**4, delta/r**4),
            "S_selects_E_in_union")
same((angle.diff(epsilon).subs(epsilon, 0)).xreplace({H: family_h,
     s.diff(H, r): s.diff(family_h, r), s.diff(H, r, 2): s.diff(family_h, r, 2)}),
     2*delta/r**2, "angular_selects_E_in_union")

# Negative controls: both defects pass DQ=0 but must fail a surviving check.
defects = []
mixed_direction = r**2 + r**-2
true_mixed = substitute_direction(leading, mixed_direction)
omitted_cross = substitute_direction(leading, r**2) + substitute_direction(leading, r**-2)
assert omitted_cross == s.zeros(4) and true_mixed != omitted_cross
checks += 1
defects.append("omitting_quadratic_cross_term_detected")
linearized_accepts_everything = Qe.diff(epsilon).subs(epsilon, 0) == s.zeros(4)
assert linearized_accepts_everything and true_mixed != s.zeros(4)
checks += 1
defects.append("DQ_only_integrability_false_pass_detected")

# General-metric tensor algebra: arbitrary symmetric coefficients, no PDE realization.
eta = s.diag(-1, 1, 1, 1)
null_covector = s.Matrix([1, 1, 0, 0])
null_ricci = null_covector * null_covector.T
null_N = eta * null_ricci
assert null_N != s.zeros(4)
checks += 1
matrix_same(null_N * null_N, s.zeros(4), "Lorentz_nonzero_square_zero")
for seed in range(1, 7):
    ricci_first = s.Matrix(4, 4, lambda i, j: s.Rational((i+j+seed)%5-2, seed+1))
    metric_first = s.Matrix(4, 4, lambda i, j: s.Rational((i*j+seed)%7-3, seed+2))
    ricci_second = s.Matrix(4, 4, lambda i, j: s.Rational((i+j* i+seed)%3-1, seed+3))
    ricci_second = (ricci_second + ricci_second.T)/2
    formal_metric = eta + epsilon*metric_first
    # The inverse is needed only to the order displayed; higher terms cannot affect epsilon².
    formal_inverse = eta - epsilon*eta*metric_first*eta
    formal_ricci = epsilon*ricci_first + epsilon**2*ricci_second
    product = formal_ricci*formal_inverse*formal_ricci
    scalar = s.trace(formal_inverse*product)
    formal_Q = product - scalar*formal_metric/4
    coefficient = formal_Q.applyfunc(lambda x: s.expand(x).coeff(epsilon, 2))
    target_general = eta*square_tf(eta*ricci_first)
    matrix_same(coefficient, target_general, f"general_leading_{seed}")
    matrix_same(formal_Q.applyfunc(lambda x: s.expand(x).coeff(epsilon, 1)),
                s.zeros(4), f"general_first_zero_{seed}")

print(json.dumps({
    "status": "PASS",
    "assertions": checks,
    "python": platform.python_version(),
    "sympy": s.__version__,
    "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    "method": "independent full 4D coordinate Christoffel/Ricci; exact symbolic epsilon coefficients",
    "monomial_records": records,
    "negative_controls": defects,
    "general_algebra_cases": 6,
    "limits": "finite checks support algebra, not curve classification or general metric realization"
}, sort_keys=True, indent=2))
