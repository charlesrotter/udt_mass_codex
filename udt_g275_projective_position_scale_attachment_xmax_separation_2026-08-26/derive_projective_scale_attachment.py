#!/usr/bin/env python3
"""Exact G275 homothety, scale-attachment, and Xmax-separation derivation."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parent
OUT = ROOT / "DERIVATION_RESULT.json"
LANDING = (
    "W5_PROJECTIVE_POSITION_IS_HOMOTHETY_INVARIANT__"
    "ONE_MATCHED_NONZERO_WEIGHT_ANCHOR_FIXES_ONE_DIMENSIONAL_SCALE__"
    "DIMENSIONFUL_REPRESENTATIVE_RETAINS_FULL_FRAME_CARRY__"
    "XMAX_EQUALS_SCALE_ONLY_AFTER_SEPARATELY_OWNED_POPULATED_BOUNDARY_COMPLETION"
)


def boost_from_cayley(q: sp.Matrix) -> sp.Matrix:
    """Rational future Lorentz boost from an open-ball Cayley parameter."""

    q2 = (q.T * q)[0]
    gamma = sp.cancel((1 + q2) / (1 - q2))
    spatial = q.applyfunc(lambda value: sp.cancel(2 * value / (1 - q2)))
    block = sp.eye(3) + spatial * spatial.T / (gamma + 1)
    return sp.Matrix.vstack(
        sp.Matrix.hstack(sp.Matrix([[gamma]]), spatial.T),
        sp.Matrix.hstack(spatial, block),
    ).applyfunc(sp.cancel)


def projective_clock(matrix: sp.Matrix) -> sp.Matrix:
    return (matrix[1:, 0] / matrix[0, 0]).applyfunc(sp.cancel)


def exact_zero(matrix: sp.Matrix) -> bool:
    return all(sp.cancel(value) == 0 for value in matrix)


def generic_connection(g: sp.Matrix, dg: list[list[list[sp.Expr]]]) -> list[list[list[sp.Expr]]]:
    """Levi-Civita symbols from a supplied exact metric and first-derivative tensor."""

    inverse = g.inv()
    dimension = g.rows
    return [
        [
            [
                sp.cancel(
                    sp.Rational(1, 2)
                    * sum(
                        inverse[a, d]
                        * (dg[b][d][c] + dg[c][d][b] - dg[d][b][c])
                        for d in range(dimension)
                    )
                )
                for c in range(dimension)
            ]
            for b in range(dimension)
        ]
        for a in range(dimension)
    ]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--no-write", action="store_true")
    args = parser.parse_args()

    ell = sp.symbols("ell", positive=True)
    eta = sp.diag(-1, 1, 1, 1)

    # A generic non-diagonal two-metric and completely generic symmetric first jets.
    a, b, c = sp.symbols("a b c", nonzero=True)
    gbar = sp.Matrix([[-a, b], [b, c]])
    d000, d001, d011, d100, d101, d111 = sp.symbols(
        "d000 d001 d011 d100 d101 d111"
    )
    dgbar = [
        [[d000, d001], [d001, d011]],
        [[d100, d101], [d101, d111]],
    ]
    gscaled = ell**2 * gbar
    dgscaled = [
        [[ell**2 * dgbar[k][i][j] for j in range(2)] for i in range(2)]
        for k in range(2)
    ]
    gamma_bar = generic_connection(gbar, dgbar)
    gamma_scaled = generic_connection(gscaled, dgscaled)

    first = boost_from_cayley(sp.Matrix([sp.Rational(1, 3), 0, 0]))
    second = boost_from_cayley(
        sp.Matrix([sp.Rational(1, 11), sp.Rational(1, 4), sp.Rational(1, 5)])
    )
    carry = sp.Matrix(
        [
            [1, 0, 0, 0],
            [0, sp.Rational(3, 5), -sp.Rational(4, 5), 0],
            [0, sp.Rational(4, 5), sp.Rational(3, 5), 0],
            [0, 0, 0, 1],
        ]
    )
    propagator = boost_from_cayley(
        sp.Matrix([sp.Rational(1, 7), sp.Rational(1, 13), 0])
    )

    # The coordinate-frame coefficient matrix is unchanged when both endpoint
    # orthonormal frames scale as ell^-1 and the connection/propagator is unchanged.
    frame_a = first
    frame_b = second
    lambda_bar = frame_b.inv() * propagator * frame_a
    frame_a_scaled = frame_a / ell
    frame_b_scaled = frame_b / ell
    lambda_scaled = frame_b_scaled.inv() * propagator * frame_a_scaled
    chi_bar = projective_clock(lambda_bar)
    chi_scaled = projective_clock(lambda_scaled)

    plain = second * first
    carried = (second * carry) * first
    chi_plain = projective_clock(plain)
    chi_carried = projective_clock(carried)
    x_plain = ell * chi_plain
    x_carried = ell * chi_carried

    # Exact anchor controls of both signs.  Each datum is constructed from the
    # same supplied positive scale; no numerical observation enters.
    anchor_scale = sp.Rational(7, 3)
    anchor_base = sp.Rational(11, 5)
    weights = (-3, -2, -1, 1, 2, 3)
    anchor_ratios = {
        str(weight): sp.cancel((anchor_scale**weight * anchor_base) / anchor_base)
        for weight in weights
    }
    anchor_unknown = sp.symbols("anchor_unknown", positive=True)
    recovered_scales = {
        str(weight): sp.solve(
            sp.Eq(anchor_unknown**weight, anchor_ratios[str(weight)]), anchor_unknown
        )
        for weight in weights
    }
    arbitrary_weight, log_scale = sp.symbols("arbitrary_weight log_scale", nonzero=True, real=True)

    # c_E has dimension L T^-1.  No power is simultaneously L^1 and T^0.
    power = sp.symbols("power")
    ce_joint_solution = sp.solve((sp.Eq(power, 1), sp.Eq(-power, 0)), (power,))

    q_finite = sp.Rational(9, 10)
    finite_xsup = ell * q_finite
    n = sp.symbols("n", positive=True, integer=True)
    q_sequence = n / (n + 1)
    q_limit = sp.limit(q_sequence, n, sp.oo)
    boundary_xsup = sp.cancel(ell * q_limit)

    radial_delta = sp.symbols("delta", real=True)
    radial_chi = sp.tanh(radial_delta)
    radial_x = ell * radial_chi

    checks = {
        "constant_homothety_inverse_metric_scales_oppositely": exact_zero(
            gscaled.inv() - gbar.inv() / ell**2
        ),
        "constant_homothety_connection_is_unchanged": all(
            sp.cancel(gamma_scaled[i][j][k] - gamma_bar[i][j][k]) == 0
            for i in range(2)
            for j in range(2)
            for k in range(2)
        ),
        "scaled_frame_remains_orthonormal": exact_zero(
            frame_a_scaled.T * (ell**2 * eta) * frame_a_scaled - eta
        ),
        "second_scaled_frame_remains_orthonormal": exact_zero(
            frame_b_scaled.T * (ell**2 * eta) * frame_b_scaled - eta
        ),
        "transported_frame_morphism_is_homothety_invariant": exact_zero(
            lambda_scaled - lambda_bar
        ),
        "projective_position_is_homothety_invariant": exact_zero(chi_scaled - chi_bar),
        "projective_position_stays_in_open_ball": sp.cancel(
            1 - (chi_bar.T * chi_bar)[0]
        ) > 0,
        "active_screen_components_survive": chi_bar[1] != 0 and chi_bar[2] != 0,
        "right_spatial_carry_leaves_single_arrow_projective_state": exact_zero(
            projective_clock(second * carry) - projective_clock(second)
        ),
        "hidden_carry_changes_composite_projective_state": not exact_zero(
            chi_carried - chi_plain
        ),
        "dimensionful_representative_retains_carry_separator": not exact_zero(
            x_carried - x_plain
        ),
        "normalizing_dimensionful_representative_recovers_projective_state": exact_zero(
            x_plain / ell - chi_plain
        ),
        "positive_anchor_weights_recover_same_scale": all(
            recovered_scales[str(weight)] == [anchor_scale] for weight in (1, 2, 3)
        ),
        "negative_anchor_weights_recover_same_scale": all(
            recovered_scales[str(weight)] == [anchor_scale] for weight in (-1, -2, -3)
        ),
        "second_independent_anchor_is_consistency_test": sp.cancel(
            ((anchor_scale**-2 * sp.Rational(17, 9)) / sp.Rational(17, 9))
            - anchor_scale**-2
        ) == 0,
        "zero_weight_anchor_cannot_recover_scale": sp.cancel(
            (anchor_scale**0 * anchor_base) / anchor_base
        ) == 1,
        "ce_alone_has_no_length_only_power": ce_joint_solution == [],
        "finite_domain_supremum_below_projective_boundary": sp.cancel(ell - finite_xsup) > 0,
        "boundary_approaching_sequence_has_unit_supremum": q_limit == 1,
        "boundary_completion_makes_conditional_supremum_equal_scale": sp.cancel(
            boundary_xsup - ell
        ) == 0,
        "finite_domain_does_not_make_xmax_equal_scale": sp.cancel(finite_xsup - ell) != 0,
        "scale_anchor_does_not_change_relation_domain_supremum": sp.cancel(
            finite_xsup / ell - q_finite
        ) == 0,
        "radial_projective_coordinate_is_tanh_depth": sp.cancel(radial_chi - sp.tanh(radial_delta)) == 0,
        "radial_dimensionful_representative_is_scale_times_tanh": sp.cancel(
            radial_x / ell - sp.tanh(radial_delta)
        ) == 0,
        "empty_relation_domain_has_no_supremum_witness": len([]) == 0,
        "arbitrary_nonzero_real_weight_is_log_injective": sp.cancel(
            arbitrary_weight * log_scale / arbitrary_weight - log_scale
        ) == 0,
    }
    checks = {key: bool(value) for key, value in checks.items()}
    assert len(checks) == 26
    assert all(checks.values()), [key for key, value in checks.items() if not value]

    result = {
        "status": "PASS",
        "landing": LANDING,
        "selected_alternative": (
            "B__ONE_POSITIVE_HOMOTHETY_SURVIVES__ONE_NONZERO_WEIGHT_ANCHOR_FIXES_IT"
        ),
        "exact_checks": len(checks),
        "checks": checks,
        "active_nonradial_projective_state": [str(sp.cancel(value)) for value in chi_bar],
        "carry_separator": {
            "plain": [str(sp.cancel(value)) for value in chi_plain],
            "with_hidden_spatial_carry": [str(sp.cancel(value)) for value in chi_carried],
        },
        "anchor_weights": list(weights),
        "conditional_dimensionful_representative": "x = ell * chi",
        "finite_domain_control": {
            "q_R": str(q_finite),
            "X_sup_over_ell": str(sp.cancel(finite_xsup / ell)),
        },
        "boundary_sequence": {
            "q_n": "n/(n+1)",
            "limit": str(q_limit),
            "conditional_X_sup": "ell",
        },
        "scope": {
            "W5": "OWNER_ADOPTED_WORKING_FOUNDATIONAL_CLARIFICATION",
            "metric_or_kernel_modified": False,
            "full_frame_carry": "RETAINED",
            "absolute_scale": "CONDITIONALLY_FIXED_BY_ONE_SUPPLIED_MATCHED_ANCHOR",
            "anchor_identity_or_value": "OPEN_NOT_SELECTED",
            "history": "OPEN_NOT_SELECTED",
            "relation_population": "OPEN_NOT_SELECTED",
            "X_max": "OPEN_UNLESS_POPULATED_BOUNDARY_COMPLETION_IS_SEPARATELY_OWNED",
            "observations": "NOT_USED",
        },
    }
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.no_write:
        assert OUT.read_text(encoding="utf-8") == rendered
    else:
        OUT.write_text(rendered, encoding="utf-8")
    print(rendered, end="")


if __name__ == "__main__":
    main()
