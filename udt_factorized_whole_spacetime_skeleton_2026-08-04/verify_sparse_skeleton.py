#!/usr/bin/env python3
"""Sparse exact checks for the factorized whole-spacetime skeleton."""

from __future__ import annotations

import json
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent


def is_zero(matrix: sp.Matrix) -> bool:
    return all(sp.simplify(value) == 0 for value in matrix)


checks: dict[str, str] = {}


def check(name: str, condition: bool) -> None:
    if not condition:
        raise AssertionError(name)
    checks[name] = "PASS"


phi, phi1, phi2 = sp.symbols("phi phi1 phi2", real=True)
a, b, d = sp.symbols("a b d", real=True)
s11, s12, s21, s22 = sp.symbols("s11 s12 s21 s22", real=True)
u, v, w = sp.symbols("u v w", nonzero=True, real=True)
r11, r12, r21, r22 = sp.symbols("r11 r12 r21 r22", real=True)

H = sp.diag(-1, 1)
P = sp.diag(sp.exp(-phi), sp.exp(phi))
P1 = P.subs(phi, phi1)
P2 = P.subs(phi, phi2)
check("founded_pair_exponential", P == sp.exp(phi * H))
check("founded_pair_composition", is_zero(P2 * P1 - P.subs(phi, phi1 + phi2)))
check("founded_pair_reversal", is_zero(P.subs(phi, -phi) * P - sp.eye(2)))
check("founded_pair_determinant_one", sp.simplify(P.det()) == 1)

# Registered positive-triangular extension E(A,D,S)=[[A,0],[D S,D]].
D = sp.Matrix([[u, v], [0, w]])
S = sp.Matrix([[s11, s12], [s21, s22]])
E = P.row_join(sp.zeros(2)).col_join((D * S).row_join(D))
Einv = P.inv().row_join(sp.zeros(2)).col_join((-S * P.inv()).row_join(D.inv()))
check("sparse_block_inverse_upper", is_zero(P * P.inv() - sp.eye(2)) and is_zero(D * D.inv() - sp.eye(2)))
check(
    "sparse_block_inverse_lower",
    is_zero((D * S) * P.inv() + D * (-S * P.inv()))
    and is_zero((-S * P.inv()) * P + D.inv() * (D * S)),
)
check("sparse_block_determinant", sp.simplify(E.det() - P.det() * D.det()) == 0)

eta = sp.diag(-1, 1, 1, 1)
numeric_subs = {phi: 0, u: 2, v: 3, w: 5, s11: 1, s12: -2, s21: 4, s22: 1}
E_numeric = E.subs(numeric_subs)
g_numeric = E_numeric.T * eta * E_numeric
check("metric_readout_symmetric", g_numeric == g_numeric.T)
check("metric_determinant_factorization", g_numeric.det() == eta.det() * E_numeric.det() ** 2)

# Seven pointwise extension chart directions and their metric response at identity.
# Generator-level seven-direction, determinant, angular-metric, and mixing reductions.
K = sp.Matrix([[a, b], [0, d]])
C = sp.Matrix([[s11, s12], [s21, s22]])
X = H.row_join(sp.zeros(2)).col_join(C.row_join(K))
parameters = (a, b, d, s11, s12, s21, s22)
x_tangents = [X.diff(parameter) for parameter in parameters]
metric_tangents = [x.T * eta + eta * x for x in x_tangents]
check("seven_extension_chart_directions", len(parameters) == 7)
check("seven_extension_coframe_tangent_rank", sp.Matrix.hstack(*(x.reshape(16, 1) for x in x_tangents)).rank() == 7)
check("seven_extension_metric_tangent_rank", sp.Matrix.hstack(*(x.reshape(16, 1) for x in metric_tangents)).rank() == 7)
check("generator_trace_is_angular_trace", sp.trace(X) == a + d)
det_one_basis = [
    X.subs({a: 1, d: -1, b: 0, s11: 0, s12: 0, s21: 0, s22: 0}),
    X.diff(b), X.diff(s11), X.diff(s12), X.diff(s21), X.diff(s22),
]
base_only = H.row_join(sp.zeros(2)).col_join(sp.zeros(2, 4))
det_one_extension = [det_one_basis[0] - base_only] + det_one_basis[1:]
check("six_determinant_one_extension_directions", sp.Matrix.hstack(*(x.reshape(16, 1) for x in det_one_extension)).rank() == 6)
angular_tangent = K.T + K
check("angular_metric_tangent", angular_tangent == sp.Matrix([[2 * a, b], [b, 2 * d]]))
check("triangular_angular_invariance_forces_K_zero", sp.solve(list(angular_tangent), (a, b, d), dict=True) == [{a: 0, b: 0, d: 0}])
metric_tangent = X.T * eta + eta * X
check("mixing_metric_tangent_is_C", metric_tangent[:2, 2:] == C.T and metric_tangent[2:, :2] == C)

spectator = sp.diag(sp.exp(-phi), sp.exp(phi), 1, 1)
check("spectator_reduction", is_zero(E.subs({u: 1, v: 0, w: 1, s11: 0, s12: 0, s21: 0, s22: 0}) - spectator))

k = sp.symbols("k", real=True)
angular = sp.diag(sp.exp(-phi), sp.exp(phi), sp.exp(-k * phi), sp.exp(k * phi))
check("angular_counterfamily_composes", is_zero(angular.subs(phi, phi2) * angular.subs(phi, phi1) - angular.subs(phi, phi1 + phi2)))
check("angular_counterfamily_is_non_spectator", angular.subs({phi: 1, k: 1}) != spectator.subs(phi, 1))

shift_strength = sp.symbols("shift_strength", real=True)
shift = sp.eye(4)
shift[0, 0] = sp.exp(-phi)
shift[1, 1] = sp.exp(phi)
shift[2, 0] = shift_strength * (1 - sp.exp(-phi))
check("shift_counterfamily_composes", is_zero(shift.subs(phi, phi2) * shift.subs(phi, phi1) - shift.subs(phi, phi1 + phi2)))
check("shift_counterfamily_is_non_spectator", shift.subs({phi: 1, shift_strength: 1}) != spectator.subs(phi, 1))

# Screen gauge and inherited angular complex structure stay factorized.
chi = sp.symbols("chi", real=True)
Rot = sp.Matrix([[sp.cos(chi), -sp.sin(chi)], [sp.sin(chi), sp.cos(chi)]])
screen_metric = sp.simplify((Rot * D).T * (Rot * D))
check("left_screen_rotation_is_metric_gauge", is_zero(screen_metric - D.T * D))
R = sp.Matrix([[0, -1], [1, 0]])
Cscreen = sp.simplify(D * R * D.inv())
check("screen_angular_generator_squares_minus_identity", is_zero(Cscreen * Cscreen + sp.eye(2)))
check("screen_angular_generator_trace_and_determinant", sp.simplify(sp.trace(Cscreen)) == 0 and sp.simplify(Cscreen.det()) == 1)

# General stationary screen is a reduction after placing alpha in the reference pair.
alpha = sp.symbols("alpha", real=True)
Pscreen = sp.Matrix([[r11, r12], [r21, r22]])
Bbase = sp.Matrix([[1, alpha], [0, 1]])
screen_reduction = (P * Bbase).row_join(sp.zeros(2)).col_join(sp.zeros(2).row_join(Pscreen))
check("stationary_screen_reference_shift_preserves_block_determinant", sp.simplify(screen_reduction.det() - Pscreen.det()) == 0)

if len(checks) != 26:
    raise AssertionError(f"unexpected check count: {len(checks)}")

result = {
    "schema": "udt-factorized-whole-spacetime-sparse-check-1.0",
    "status": "PASS",
    "sympy_version": sp.__version__,
    "check_count": len(checks),
    "checks": checks,
    "maximum_conclusion": "SPARSE_POINTWISE_SKELETON_AND_REGISTERED_REDUCTIONS_ALGEBRAICALLY_COHERENT_ONLY",
}
(HERE / "SPARSE_SKELETON_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
print(json.dumps(result, indent=2, sort_keys=True))
