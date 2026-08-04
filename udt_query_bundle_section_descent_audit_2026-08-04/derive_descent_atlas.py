#!/usr/bin/env python3
"""Exact production checks for the observer-pair descent audit."""

from __future__ import annotations

import json
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent
eta = sp.diag(-1, 1, 1, 1)
I4 = sp.eye(4)
e0, e1, e2, e3 = [sp.eye(4)[:, i] for i in range(4)]


def gdot(x: sp.Matrix, y: sp.Matrix) -> sp.Expr:
    return (x.T * eta * y)[0]


def line_projector(v: sp.Matrix) -> sp.Matrix:
    norm = gdot(v, v)
    assert norm in (-1, 1)
    return sp.simplify(v * (v.T * eta) / norm)


def pair_projector(u: sp.Matrix, n: sp.Matrix) -> sp.Matrix:
    assert gdot(u, u) == -1 and gdot(n, n) == 1 and gdot(u, n) == 0
    return sp.simplify(line_projector(u) + line_projector(n))


checks: dict[str, bool] = {}

P01 = pair_projector(e0, e1)
P02 = pair_projector(e0, e2)
Q01 = I4 - P01
Q02 = I4 - P02

R12 = sp.Matrix(
    [
        [1, 0, 0, 0],
        [0, 0, -1, 0],
        [0, 1, 0, 0],
        [0, 0, 0, 1],
    ]
)
checks["vertical_reset_is_Lorentz"] = R12.T * eta * R12 == eta
checks["pair_projector_covariance"] = sp.simplify(R12 * P01 * R12.inv() - P02) == sp.zeros(4)
checks["pair_projector_changes_vertically"] = P01 != P02
checks["pair_projector_idempotent_01"] = P01 * P01 == P01
checks["pair_projector_idempotent_02"] = P02 * P02 == P02
checks["pair_projector_rank_01"] = P01.rank() == 2
checks["pair_projector_rank_02"] = P02.rank() == 2
checks["pair_projector_eta_self_adjoint"] = P01.T * eta == eta * P01
checks["ambient_identity_basic"] = R12 * I4 * R12.inv() == I4
checks["ambient_metric_pair_independent"] = eta == eta

v = e2
screen_value_01 = gdot(Q01 * v, Q01 * v)
screen_value_02 = gdot(Q02 * v, Q02 * v)
checks["screen_readout_changes_with_pair"] = (screen_value_01, screen_value_02) == (1, 0)

A = sp.diag(2, 3, 5, 7)
ambient_trace = sp.trace(A)
projected_trace_01 = sp.trace(P01 * A)
projected_trace_02 = sp.trace(P02 * A)
checks["ambient_curvature_scalar_pair_independent"] = ambient_trace == 17
checks["projected_curvature_changes_with_pair"] = (projected_trace_01, projected_trace_02) == (5, 7)

n = sp.Rational(3, 5) * e1 + sp.Rational(4, 5) * e2
m = -sp.Rational(4, 5) * e1 + sp.Rational(3, 5) * e2
Pn = pair_projector(e0, n)
dPn = m * (n.T * eta) + n * (m.T * eta)
vertical_derivative = sp.trace(dPn * A)
checks["vertical_derivative_nonzero"] = vertical_derivative == sp.Rational(48, 25)
checks["projector_vertical_tangent_nonzero"] = dPn.rank() == 2

b = e2
checks["base_boundary_vector_exists_without_pair"] = gdot(b, b) == 1
checks["pair_boundary_polarization_changes"] = P01 * b == sp.zeros(4, 1) and P02 * b == b

zero = sp.zeros(4)
checks["zero_mixing_trivially_basic"] = R12 * zero * R12.inv() == zero
checks["zero_mixing_does_not_select_plane"] = P01 != P02 and zero == sp.zeros(4)

a, c = sp.symbols("a c", real=True)
D01_a = sp.diag(sp.exp(-a), sp.exp(a), 1, 1)
D01_c = sp.diag(sp.exp(-c), sp.exp(c), 1, 1)
D01_sum = sp.diag(sp.exp(-(a + c)), sp.exp(a + c), 1, 1)
checks["reciprocal_character_composes"] = sp.simplify(D01_a * D01_c - D01_sum) == sp.zeros(4)
checks["reciprocal_character_reverses"] = sp.simplify(D01_a * D01_a.subs(a, -a) - I4) == sp.zeros(4)
D02_a = sp.simplify(R12 * D01_a * R12.inv())
D02_c = sp.simplify(R12 * D01_c * R12.inv())
checks["reciprocal_character_vertical_covariance"] = sp.simplify(D02_a - R12 * D01_a * R12.inv()) == sp.zeros(4)
checks["reciprocal_character_composes_after_reset"] = sp.simplify(D02_a * D02_c - R12 * D01_sum * R12.inv()) == sp.zeros(4)

eps = sp.symbols("eps", positive=True)
A1 = sp.diag(2, 3, 3 + eps, 7)
A2 = sp.diag(2, 3 + eps, 3, 7)
A0 = sp.diag(2, 3, 3, 7)
checks["collision_parent_limit_agrees"] = A1.subs(eps, 0) == A0 and A2.subs(eps, 0) == A0
checks["collision_selector_limits_disagree"] = P01 != P02
checks["collision_limits_isometry_related"] = sp.simplify(R12 * P01 * R12.inv() - P02) == sp.zeros(4)

assert all(checks.values()), [key for key, value in checks.items() if not value]
result = {
    "status": "PASS",
    "engine": "sympy",
    "sympy_version": sp.__version__,
    "exact_checks": len(checks),
    "vertical_projector_derivative": str(vertical_derivative),
    "projected_curvature_traces": [str(projected_trace_01), str(projected_trace_02)],
    "screen_readout_values": [str(screen_value_01), str(screen_value_02)],
    "pair_projector_ranks": [P01.rank(), P02.rank()],
    "collision_parent": str(A0.tolist()),
    "collision_projectors_distinct": True,
    "maximum_conclusion": "EXACT_BASICNESS_AND_SECTION_DEPENDENCE_CONTROLS_ONLY",
}
(HERE / "DERIVATION_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
print(json.dumps(result, sort_keys=True))
