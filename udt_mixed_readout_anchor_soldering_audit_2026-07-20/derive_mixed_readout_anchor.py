#!/usr/bin/env python3
"""Exact algebra for the UDT mixed-readout anchor/soldering audit."""

from __future__ import annotations

import json
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent


def require(name: str, condition, checks: dict[str, str]) -> None:
    if not bool(condition):
        raise AssertionError(name)
    checks[name] = "PASS"


def require_zero(name: str, expression, checks: dict[str, str]) -> None:
    value = sp.simplify(expression)
    if isinstance(value, sp.MatrixBase):
        good = value == sp.zeros(*value.shape)
    else:
        good = value == 0
    require(name, good, checks)


def main() -> None:
    checks: dict[str, str] = {}
    A, B, b, phi, v = sp.symbols("A B b phi v", real=True, nonzero=True)
    omega, a = sp.symbols("omega a", positive=True)
    s11, s12, s21, s22 = sp.symbols("s11 s12 s21 s22", real=True)

    H = sp.Matrix([[A, B], [B, A * b**2]])
    L = sp.diag(-1, 1)
    F = sp.Matrix([[0, b], [1 / b, 0]])
    P = sp.diag(sp.exp(-phi), sp.exp(phi))
    g = sp.simplify(P.T * H * P)
    mu = sp.simplify(B**2 / (A**2 * b**2))

    # Exact mixed-family closure inherited from the preceding audit.
    require_zero("reciprocal_generator_involution", L * L - sp.eye(2), checks)
    require_zero("spatial_seal_involution", F * F - sp.eye(2), checks)
    require_zero("spatial_seal_inverts_generator", F * L * F + L, checks)
    require_zero("spatial_seal_metric_isometry", F.T * g.subs(phi, -phi) * F - g, checks)
    require_zero("mixed_family_constant_determinant", g.det() - (A**2 * b**2 - B**2), checks)

    # A simultaneous-basis invariant of the metric/reciprocity pair.
    pair_invariant = sp.factor(sp.trace(H.inv() * L.T * H * L))
    expected_invariant = sp.factor(2 * (1 + mu) / (1 - mu))
    require_zero("pair_invariant_formula", pair_invariant - expected_invariant, checks)
    I_symbol = sp.symbols("I_symbol")
    reconstructed_mu = sp.solve(
        sp.Eq(I_symbol, 2 * (1 + sp.Symbol("m")) / (1 - sp.Symbol("m"))),
        sp.Symbol("m"),
    )[0]
    require_zero("pair_invariant_reconstructs_mu", reconstructed_mu - (I_symbol - 2) / (I_symbol + 2), checks)

    S = sp.Matrix([[s11, s12], [s21, s22]])
    H_prime = sp.simplify(S.T * H * S)
    L_prime = sp.simplify(S.inv() * L * S)
    transformed_invariant = sp.factor(
        sp.trace(H_prime.inv() * L_prime.T * H_prime * L_prime)
    )
    require_zero("pair_invariant_under_general_simultaneous_GL2", transformed_invariant - pair_invariant, checks)

    csn_invariant = sp.factor(
        sp.trace((omega**2 * H).inv() * L.T * (omega**2 * H) * L)
    )
    require_zero("pair_invariant_under_positive_CSN", csn_invariant - pair_invariant, checks)
    diagonal_gauge = sp.diag(a, 1 / a)
    H_gauge = sp.simplify(diagonal_gauge.T * H * diagonal_gauge)
    L_gauge = sp.simplify(diagonal_gauge.inv() * L * diagonal_gauge)
    gauge_invariant = sp.factor(sp.trace(H_gauge.inv() * L_gauge.T * H_gauge * L_gauge))
    require_zero("pair_invariant_under_diagonal_reciprocal_gauge", gauge_invariant - pair_invariant, checks)

    witness_invariants = {}
    for label, cross_term, expected_mu, expected_I in (
        ("MU4", -2, sp.Integer(4), sp.Rational(-10, 3)),
        ("MU9", -3, sp.Integer(9), sp.Rational(-5, 2)),
    ):
        witness_H = H.subs({A: 1, B: cross_term, b: 1})
        witness_I = sp.simplify(pair_invariant.subs({A: 1, B: cross_term, b: 1}))
        require(f"{label}_Lorentz_signature", witness_H.det() < 0, checks)
        require_zero(f"{label}_mu", mu.subs({A: 1, B: cross_term, b: 1}) - expected_mu, checks)
        require_zero(f"{label}_pair_invariant", witness_I - expected_I, checks)
        witness_invariants[label] = {
            "mu": int(expected_mu),
            "pair_invariant": str(expected_I),
            "determinant": int(witness_H.det()),
        }
    require(
        "distinct_mu_witnesses_not_simultaneously_basis_equivalent",
        witness_invariants["MU4"]["pair_invariant"] != witness_invariants["MU9"]["pair_invariant"],
        checks,
    )

    # Strong FIXED_Q_ANCHOR branch: the named q axes themselves carry an untilted symmetric c cone.
    tangent = sp.Matrix([1, v])
    null_polynomial = sp.expand((tangent.T * H * tangent)[0])
    require_zero("fixed_q_null_polynomial", null_polynomial - (A + 2 * B * v + A * b**2 * v**2), checks)
    require_zero(
        "fixed_q_cone_asymmetry",
        sp.expand(null_polynomial.subs(v, -v) - null_polynomial) + 4 * B * v,
        checks,
    )
    cone_odd_coefficient = sp.Poly(
        sp.expand(null_polynomial.subs(v, -v) - null_polynomial), v
    ).coeff_monomial(v)
    require_zero("fixed_q_symmetric_cone_odd_coefficient", cone_odd_coefficient + 4 * B, checks)
    require(
        "fixed_q_symmetric_cone_forces_B_zero",
        sp.solve(sp.Eq(sp.Symbol("B_free") * -4, 0), sp.Symbol("B_free")) == [0],
        checks,
    )
    require(
        "fixed_q_B_zero_mirror_family_not_Lorentz",
        H.det().subs(B, 0) == A**2 * b**2,
        checks,
    )
    lambda_symbol = sp.symbols("lambda_symbol", real=True, nonzero=True)
    fixed_q_orthogonal_equations = [
        sp.Eq(A, -lambda_symbol),
        sp.Eq(B, 0),
        sp.Eq(A * b**2, lambda_symbol),
    ]
    require(
        "fixed_q_exact_eta_requires_impossible_real_b_square",
        sp.solve(fixed_q_orthogonal_equations, (A, B, b), dict=True) == [],
        checks,
    )

    # Weak ORTHONORMALIZABLE_ANCHOR branch: an exact Lorentz chart with local slopes +/-1 exists.
    H4 = H.subs({A: 1, B: -2, b: 1})
    F1 = F.subs(b, 1)
    hadamard = sp.Matrix([[1, 1], [1, -1]]) / sp.sqrt(2)
    normalizer = sp.diag(1, 1 / sp.sqrt(3))
    S_anchor = sp.simplify(hadamard * normalizer)  # q = S_anchor q_orth
    eta = sp.diag(-1, 1)
    require_zero("orthonormal_anchor_metric", S_anchor.T * H4 * S_anchor - eta, checks)
    L_anchor = sp.simplify(S_anchor.inv() * L * S_anchor)
    F_anchor = sp.simplify(S_anchor.inv() * F1 * S_anchor)
    expected_L_anchor = sp.Matrix([[0, -1 / sp.sqrt(3)], [-sp.sqrt(3), 0]])
    require_zero("orthonormal_anchor_reciprocal_generator", L_anchor - expected_L_anchor, checks)
    require_zero("orthonormal_anchor_generator_still_involution", L_anchor**2 - sp.eye(2), checks)
    require_zero("orthonormal_anchor_spatial_reflection", F_anchor - sp.diag(1, -1), checks)
    require_zero("orthonormal_anchor_seal_inverts_generator", F_anchor * L_anchor * F_anchor + L_anchor, checks)
    P_anchor = sp.cosh(phi) * sp.eye(2) + sp.sinh(phi) * L_anchor
    require_zero("orthonormal_anchor_exponential_closed_form", sp.exp(phi * L_anchor) - P_anchor, checks)
    orth_null = sp.expand((sp.Matrix([1, v]).T * eta * sp.Matrix([1, v]))[0])
    require_zero("orthonormal_anchor_null_polynomial", orth_null - (-1 + v**2), checks)
    require("orthonormal_anchor_local_c_slopes", sp.solve(orth_null, v) == [-1, 1], checks)

    q_witness_null = sp.factor(null_polynomial.subs({A: 1, B: -2, b: 1}))
    require_zero("mixed_q_witness_null_polynomial", q_witness_null - (v**2 - 4 * v + 1), checks)
    require(
        "mixed_q_witness_tilted_null_slopes",
        sp.solve(q_witness_null, v) == [2 - sp.sqrt(3), sp.sqrt(3) + 2],
        checks,
    )
    require(
        "mixed_q_witness_both_null_slopes_same_sign",
        bool(2 - sp.sqrt(3) > 0) and bool(2 + sp.sqrt(3) > 0),
        checks,
    )

    # Literal coordinate time reversal and conjugated orthonormal temporal reflection are distinct.
    T_q_literal = sp.diag(-1, 1)
    literal_time_difference = sp.simplify(T_q_literal.T * H * T_q_literal - H)
    require_zero(
        "literal_q_time_reversal_difference",
        literal_time_difference - sp.Matrix([[0, -2 * B], [-2 * B, 0]]),
        checks,
    )
    B_free = sp.Symbol("B_free", real=True)
    require(
        "literal_q_time_reversal_rejects_nonzero_B_if_imposed_as_isometry",
        sp.solve(sp.Eq(-2 * B_free, 0), B_free) == [0],
        checks,
    )
    T_anchor = sp.diag(-1, 1)
    require_zero("orthonormal_temporal_reflection_is_eta_isometry", T_anchor.T * eta * T_anchor - eta, checks)
    T_anchor_in_q = sp.simplify(S_anchor * T_anchor * S_anchor.inv())
    require_zero("orthonormal_temporal_reflection_in_q", T_anchor_in_q + F1, checks)
    require_zero("orthonormal_spatial_reflection_in_q", S_anchor * sp.diag(1, -1) * S_anchor.inv() - F1, checks)
    require("literal_and_conjugated_temporal_reflections_differ", T_q_literal != T_anchor_in_q, checks)
    require_zero("conjugated_temporal_reflection_is_H4_isometry", T_anchor_in_q.T * H4 * T_anchor_in_q - H4, checks)

    # Distinguish generator, metric, and physical-slot commutation data.
    commutator = sp.simplify(L.T * H - H * L)
    anticommutator = sp.simplify(L.T * H + H * L)
    require_zero(
        "metric_generator_commutator",
        commutator - sp.Matrix([[0, -2 * B], [2 * B, 0]]),
        checks,
    )
    require_zero(
        "metric_generator_anticommutator",
        anticommutator - sp.diag(-2 * A, 2 * A * b**2),
        checks,
    )
    require("physical_phi_visible_requires_A_nonzero", sp.diff(g, phi) != sp.zeros(2), checks)
    require_zero("pure_dual_pairing_limit_is_phi_invisible", g.subs(A, 0) - sp.Matrix([[0, B], [B, 0]]), checks)

    outcomes = [
        "OBSERVATIONAL_ANCHOR_LEAVES_MU_OPEN",
        "MU_IS_INVARIANT_OF_METRIC_RECIPROCITY_PAIR",
        "FIXED_Q_AND_ORTHONORMALIZABLE_ANCHOR_BRANCHES_DIVERGE",
        "TEMPORAL_MIRROR_COMPONENT_SOLDERING_REMAINS_OPEN",
        "PHYSICAL_CLOCK_RULER_SOLDERING_RULE_ABSENT",
    ]
    result = {
        "maximum_conclusion": "UDT_MIXED_READOUT_ANCHOR_SOLDERING_STATUS_CHARACTERIZED",
        "outcomes": outcomes,
        "owner_source_resolution": {
            "c_anchor": "finite terrestrial/solar clock-length calibration",
            "q_pair": "dimension-matched reciprocal eigen-coframe; not currently declared operationally orthogonal",
            "fixed_q_anchor": "pinned-by-HABIT, retained only as a conditional branch",
            "orthonormalizable_anchor": "compatible with current source meaning but not a native soldering theorem",
            "physical_observer_transform": "OPEN",
        },
        "pair_invariant": {
            "definition": "tr(H^-1 L^T H L)",
            "value": "2*(1+mu)/(1-mu)",
            "inverse": "mu=(I-2)/(I+2)",
            "implication": "mu is not removable by a simultaneous GL(2,R) basis transformation of (H,L)",
        },
        "anchor_branches": {
            "FIXED_Q_ANCHOR": {
                "status": "CONDITIONAL_REJECTION",
                "reason": "symmetric q-chart c cone forces B=0, incompatible with Lorentzian spatial-seal family",
            },
            "ORTHONORMALIZABLE_ANCHOR": {
                "status": "CONDITIONAL_COMPATIBILITY",
                "reason": "exact orthonormal chart gives local null slopes +/-1 while reciprocity generator becomes non-diagonal",
            },
        },
        "temporal_mirror": {
            "literal_q_chart": "would force B=0 if imposed as a metric isometry",
            "orthonormal_chart": "exists and conjugates to -F in the exact witness",
            "current_udt_status": "component/basis soldering not supplied; no selection or rejection authorized",
        },
        "witnesses": witness_invariants,
        "check_count": len(checks),
        "checks": checks,
        "exclusions": [
            "observer mechanics",
            "action or field equation",
            "angular topology",
            "bootstrap or physical scale selection",
            "carrier, source, mass, and boundary completion",
        ],
    }
    (HERE / "DERIVATION_RESULT.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
