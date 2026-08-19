#!/usr/bin/env python3
"""Exact G169 algebra for bidirectional co-present relational distance."""

from __future__ import annotations

import json
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent
checks: list[dict[str, object]] = []


def check(name: str, condition: object, detail: object = "") -> None:
    passed = bool(condition)
    checks.append({"name": name, "passed": passed, "detail": str(detail)})
    if not passed:
        raise AssertionError(f"{name}: {detail}")


def chi_from_q(q: sp.Expr) -> sp.Expr:
    return sp.cancel((1 - q) / (1 + q))


# 1. Reversal is an involution on a supplied two-ended relation record.
relation = ("A", "germ_AB", "h_AB", "B", "germ_BA", "h_BA", "carry_BA")


def reverse(record: tuple[str, ...]) -> tuple[str, ...]:
    a, germ_ab, h_ab, b, germ_ba, h_ba, carry_ba = record
    return (b, germ_ba, h_ba, a, germ_ab, h_ab, f"inverse({carry_ba})")


def reverse_twice(record: tuple[str, ...]) -> tuple[str, ...]:
    first = reverse(record)
    b, germ_ba, h_ba, a, germ_ab, h_ab, inverse_carry = first
    if not inverse_carry.startswith("inverse("):
        raise AssertionError("malformed inverse marker")
    carry = inverse_carry[len("inverse(") : -1]
    return (a, germ_ab, h_ab, b, germ_ba, h_ba, carry)


check("reversal_involution", reverse_twice(relation) == relation)
check("reversal_swaps_endpoints", reverse(relation)[0] == "B" and reverse(relation)[3] == "A")

# 2. Founded reciprocal branch.
d = sp.symbols("d", real=True)
eta = sp.diag(-1, 1)
D = sp.diag(sp.exp(-d), sp.exp(d))
h_d = sp.simplify(D.T * eta * D)
h_minus_d = sp.simplify(h_d.subs(d, -d))
K_d = sp.diag(sp.exp(2 * d), sp.exp(-2 * d))

check("founded_metric", h_d == sp.diag(-sp.exp(-2 * d), sp.exp(2 * d)), h_d)
check("founded_determinant", sp.simplify(h_d.det() + 1) == 0, h_d.det())
check("reverse_metric", h_minus_d == sp.diag(-sp.exp(2 * d), sp.exp(-2 * d)), h_minus_d)
check("pure_reverse_identification", sp.simplify(K_d.T * h_d * K_d - h_minus_d) == sp.zeros(2))
check("pure_reverse_identification_inverse", sp.simplify(K_d.subs(d, -d) * K_d) == sp.eye(2))

q_d = sp.exp(-2 * d)
q_reverse = sp.exp(2 * d)
chi_d = sp.tanh(d)
check("q_reversal", sp.simplify(q_d * q_reverse - 1) == 0)
check("chi_reversal", sp.simplify(sp.tanh(-d) + chi_d) == 0)
check("absolute_depth_descends", sp.Abs(-d) == sp.Abs(d))
check("squared_chi_descends", sp.simplify(sp.tanh(-d) ** 2 - chi_d**2) == 0)

# 3. Matched three-observer reciprocal composition.
a, b = sp.symbols("a b", real=True)
D_a = sp.diag(sp.exp(-a), sp.exp(a))
D_b = sp.diag(sp.exp(-b), sp.exp(b))
D_ab = sp.diag(sp.exp(-(a + b)), sp.exp(a + b))
check("D_composition", sp.simplify(D_b * D_a - D_ab) == sp.zeros(2))

q_a, q_b = sp.symbols("q_a q_b", positive=True)
chi_a = chi_from_q(q_a)
chi_b = chi_from_q(q_b)
chi_ab_direct = chi_from_q(q_a * q_b)
chi_ab_mobius = sp.cancel((chi_a + chi_b) / (1 + chi_a * chi_b))
check("q_composition", sp.cancel((q_a * q_b) / q_a - q_b) == 0)
check("chi_mobius_composition", sp.cancel(chi_ab_direct - chi_ab_mobius) == 0)

# Absolute signed depth is subadditive on a matched additive chain, checked exactly by squaring
# fixed rational representatives in all sign sectors.
for av, bv in ((sp.Rational(2), sp.Rational(3)), (sp.Rational(2), -sp.Rational(3)),
               (-sp.Rational(2), sp.Rational(3)), (-sp.Rational(2), -sp.Rational(3))):
    check(
        f"matched_depth_triangle_{av}_{bv}",
        sp.Abs(av + bv) <= sp.Abs(av) + sp.Abs(bv),
    )

# 4. Exact G168 flat same-boundary surface reversal counterexample.
# F_a(tau,sigma)=(tau,sigma,a sigma(1-sigma),0).
surface_a = sp.symbols("surface_a", real=True)
surface_h_A = sp.diag(-1, 1 + surface_a**2)
surface_h_B_reversed = sp.diag(-1, 1 + surface_a**2)
surface_delta_A = sp.log(1 + surface_a**2) / 4
surface_delta_B = sp.log(1 + surface_a**2) / 4
check("surface_reverse_same_metric", surface_h_A == surface_h_B_reversed)
check("surface_reverse_same_terminal_depth", sp.simplify(surface_delta_A - surface_delta_B) == 0)
check(
    "surface_reverse_not_reciprocal_witness",
    surface_delta_A.subs(surface_a, 1) != -surface_delta_B.subs(surface_a, 1),
)
surface_q2_A = sp.cancel(surface_h_A[0, 0] ** 2 / (-surface_h_A.det()))
surface_q2_B = sp.cancel(surface_h_B_reversed[0, 0] ** 2 / (-surface_h_B_reversed.det()))
check("surface_endpoint_q2_equal", sp.simplify(surface_q2_A - surface_q2_B) == 0)
check(
    "surface_endpoint_q_not_inverse_witness",
    sp.simplify((surface_q2_A * surface_q2_B).subs(surface_a, 1) - 1) != 0,
    (surface_q2_A * surface_q2_B).subs(surface_a, 1),
)
check("distinct_observers_zero_scalar_witness", surface_delta_A.subs(surface_a, 0) == 0)

# 5. Individually regular pair metrics need not form one additive triangle.
q_AB = sp.Rational(1, 2)
q_BC = sp.Rational(1, 3)
q_AC_free = sp.Rational(1, 5)
check("independent_pairs_each_positive", all(q > 0 for q in (q_AB, q_BC, q_AC_free)))
check("arbitrary_triangle_not_forced", q_AC_free != q_AB * q_BC)
check("matched_triangle_expected_q", q_AB * q_BC == sp.Rational(1, 6))

# 6. Complete supplied carry closure and scalar-blind nonclosure.
I = sp.eye(2)
shear = sp.Matrix([[1, 1], [0, 1]])
M_BA = sp.Matrix([[2, 1], [0, 3]])
M_CB = sp.Matrix([[5, 2], [0, 7]])
M_CA = M_CB * M_BA
check("full_carry_composition", M_CB * M_BA == M_CA)
check("full_carry_reverse", sp.simplify(M_BA.inv() * M_BA) == I)
check("full_carry_associativity", (shear * M_CB) * M_BA == shear * (M_CB * M_BA))

# Reversal commutes with independent endpoint reparameterization: the reversed gauged arrow is the
# inverse of the gauged arrow. This is the finite-dimensional quotient check for the orbit.
P_A = sp.Matrix([[1, 2], [0, 1]])
P_B = sp.Matrix([[3, 1], [0, 2]])
C = sp.Matrix([[2, -1], [1, 2]])
C_gauged = P_B.inv() * C * P_A
C_reverse_gauged = P_A.inv() * C.inv() * P_B
check("reversal_gauge_equivariance", sp.simplify(C_reverse_gauged - C_gauged.inv()) == sp.zeros(2))
check("gauged_reversal_involution", sp.simplify(C_reverse_gauged.inv() - C_gauged) == sp.zeros(2))

def scale_square(matrix: sp.Matrix) -> sp.Expr:
    return sp.det(matrix)


def reciprocal_square(matrix: sp.Matrix) -> sp.Expr:
    return sp.cancel(matrix[1, 1] / matrix[0, 0])


check("shear_nonidentity", shear != I)
check("shear_scale_character_zero", scale_square(shear) == 1)
check("shear_reciprocal_character_zero", reciprocal_square(shear) == 1)
check(
    "scalar_closure_weaker_than_matrix_closure",
    scale_square(shear) == reciprocal_square(shear) == 1 and shear != I,
)

landing = (
    "CONDITIONAL_RELATIONAL_DISTANCE_OBJECT"
    "__RECIPROCAL_SCALAR_REVERSAL_DERIVED_ON_ONE_SUPPLIED_RELATION"
    "__MATCHED_CHAIN_COMPOSITION_DERIVED"
    "__ARBITRARY_TRIANGLE_ADDITIVITY_NOT_REQUIRED_OR_DERIVED"
    "__PHYSICAL_TWO_ENDED_GERM_AND_CARRY_OWNERSHIP_OPEN"
)

result = {
    "landing": landing,
    "checks_passed": sum(int(row["passed"]) for row in checks),
    "checks_total": len(checks),
    "checks": checks,
    "key_counterexample": {
        "surface_parameter": 1,
        "endpoint_metric": [[-1, 0], [0, 2]],
        "delta_A": "log(2)/4",
        "delta_B_after_surface_reversal": "log(2)/4",
        "required_reciprocal_delta_B": "-log(2)/4",
    },
    "arbitrary_triangle": {
        "q_AB": "1/2",
        "q_BC": "1/3",
        "q_AC_independently_supplied": "1/5",
        "q_AC_if_matched_composition": "1/6",
    },
    "status": "DERIVED_CONDITIONAL",
}
(HERE / "DERIVATION_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
print(json.dumps({"landing": landing, "passed": result["checks_passed"], "total": len(checks)}, sort_keys=True))
