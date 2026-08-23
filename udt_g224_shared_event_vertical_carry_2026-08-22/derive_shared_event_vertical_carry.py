#!/usr/bin/env python3
"""Symbolic derivation for the bounded G224 shared-event vertical carry theorem."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parent
LANDING = (
    "SHARED_MIDDLE_EVENT_AND_METRIC_UNIT_CLOCK_CANONICALLY_IDENTIFY_INCIDENT_FUTURE_NULL_VERTICAL_LINES"
    "__VERTICAL_SCALAR_CARRY_IS_THE_INVERSE_REPRESENTATION_OF_THE_ACTUAL_CLOCK_RATE_CHAIN"
    "__DISTINCT_EVENT_NORMALIZATION_IS_ABSTRACTLY_AVAILABLE_BUT_NOT_A_COMPOSABLE_VERTEX_RELATION"
    "__NO_SCREEN_MAP_OR_INDEPENDENT_DIRECT_RELATION_IS_DERIVED"
)


def require_zero(expr: sp.Expr, name: str, checks: list[str]) -> None:
    value = sp.factor(sp.simplify(expr))
    if value != 0:
        raise AssertionError(f"{name}: {value}")
    checks.append(name)


def require_nonzero(expr: sp.Expr, name: str, checks: list[str]) -> None:
    value = sp.factor(sp.simplify(expr))
    if value == 0:
        raise AssertionError(f"{name}: unexpectedly zero")
    checks.append(name)


def main(*, write_outputs: bool = True) -> None:
    checks: list[str] = []
    w1, w2, w3 = sp.symbols("w1 w2 w3", positive=True, nonzero=True)

    # Each metric clock functional mu_i is represented by multiplication by
    # w_i in an arbitrary positive basis K_i. Pairing preservation fixes the
    # unique coefficient c_21=w1/w2.
    c21 = w1 / w2
    require_zero(w2 * c21 - w1, "pairing_preserving_switch", checks)
    solution = sp.solve(sp.Eq(w2 * sp.Symbol("c"), w1), sp.Symbol("c"))
    if solution != [w1 / w2]:
        raise AssertionError(f"unique switch solution: {solution}")
    checks.append("unique_positive_line_switch")

    # Independent affine-generator rescalings alter only the coordinate
    # coefficient, not the abstract map.
    gamma1, gamma2 = sp.symbols("gamma1 gamma2", positive=True, nonzero=True)
    c21_prime = gamma1 * w1 / (gamma2 * w2)
    require_zero(c21_prime * gamma2 - gamma1 * c21, "independent_affine_rescaling", checks)

    # A common positive clock representative cancels. Metric-unit U fixes this
    # factor to one, but the cancellation checks trivialization independence.
    zeta = sp.symbols("zeta", positive=True, nonzero=True)
    require_zero((zeta * w1) / (zeta * w2) - c21, "common_clock_recalibration", checks)

    # Pair-groupoid identities at one observer event.
    c32 = w2 / w3
    c31 = w1 / w3
    require_zero(w1 / w1 - 1, "vertex_identity", checks)
    require_zero(c21 * (w2 / w1) - 1, "vertex_inverse", checks)
    require_zero(c32 * c21 - c31, "vertex_cocycle", checks)

    # Metric-normalized generators N_i=K_i/w_i have mu_i(N_i)=1 and the
    # switch sends N_1 exactly to N_2.
    require_zero(w1 * (1 / w1) - 1, "normalized_incoming_generator", checks)
    require_zero(w2 * (1 / w2) - 1, "normalized_outgoing_generator", checks)
    require_zero(c21 / w1 - 1 / w2, "switch_maps_normalized_generators", checks)

    # Affine geodesic edge transport followed by endpoint normalization has
    # coefficient omega_target/omega_source, inverse to the G220 clock ratio.
    w_a, w_b_in, w_b_out, w_c = sp.symbols(
        "w_a w_b_in w_b_out w_c", positive=True, nonzero=True
    )
    r_ab = w_a / w_b_in
    r_bc = w_b_out / w_c
    q_ab = w_b_in / w_a
    q_bc = w_c / w_b_out
    require_zero(q_ab - 1 / r_ab, "AB_vertical_inverse_clock_ratio", checks)
    require_zero(q_bc - 1 / r_bc, "BC_vertical_inverse_clock_ratio", checks)

    # The shared-event switch maps the incoming frequency-one generator to the
    # outgoing frequency-one generator, so it adds no independent scalar.
    switch_raw = w_b_in / w_b_out
    require_zero(switch_raw / w_b_in - 1 / w_b_out, "middle_switch_unit_coefficient", checks)
    q_path = q_bc * q_ab
    require_zero(q_path - 1 / (r_bc * r_ab), "two_edge_path_inverse_chain", checks)

    w_d, w_c_out = sp.symbols("w_d w_c_out", positive=True, nonzero=True)
    r_cd = w_c_out / w_d
    q_cd = w_d / w_c_out
    require_zero(q_cd * q_path - 1 / (r_cd * r_bc * r_ab), "three_edge_path_inverse_chain", checks)

    # Equality to a direct edge is an identity only under the actual-composite
    # premise r_ac=r_bc*r_ab.
    r_ac = sp.symbols("r_ac", positive=True, nonzero=True)
    require_zero(
        (1 / r_ac - q_path).subs(r_ac, r_bc * r_ab),
        "actual_direct_composite_condition",
        checks,
    )
    require_nonzero(1 / r_ac - q_path, "independent_direct_edge_unconstrained", checks)

    # Exact Minkowski witness: two different future null directions at one
    # observer event are not equated as ambient vectors, but their line scales
    # are uniquely matched by the observer clock.
    alpha, beta = sp.symbols("alpha beta", positive=True, nonzero=True)
    eta = sp.diag(-1, 1, 1, 1)
    U = sp.Matrix([1, 0, 0, 0])
    K1 = alpha * sp.Matrix([1, 1, 0, 0])
    K2 = beta * sp.Matrix([1, sp.Rational(3, 5), sp.Rational(4, 5), 0])
    dot = lambda x, y: (x.T * eta * y)[0]
    require_zero(dot(K1, K1), "minkowski_incoming_null", checks)
    require_zero(dot(K2, K2), "minkowski_outgoing_null", checks)
    require_zero(-dot(U, K1) - alpha, "minkowski_incoming_frequency", checks)
    require_zero(-dot(U, K2) - beta, "minkowski_outgoing_frequency", checks)
    require_zero((alpha / beta) * K2[0] - K1[0], "minkowski_clock_pairing_match", checks)
    require_nonzero((alpha / beta) * K2[1] - K1[1], "minkowski_directions_not_identified", checks)

    # The same frequency-one construction is algebraically available at two
    # distinct observer events. What is absent there is a shared physical
    # vertex/composable incidence, not an abstract line isomorphism.
    w_p, w_q = sp.symbols("w_p w_q", positive=True, nonzero=True)
    require_zero((w_p / w_q) / w_p - 1 / w_q, "distinct_event_abstract_line_normalization", checks)

    result = {
        "status": "PASS",
        "preregistered_outcome": "A_WITH_DISTINCT_EVENT_SCOPE_CORRECTION",
        "symbolic_checks": len(checks),
        "checks": checks,
        "metric_clock_pairing_nondegenerate": True,
        "shared_event_vertical_switch_unique": True,
        "independent_affine_rescaling_invariant": True,
        "common_clock_recalibration_invariant": True,
        "vertex_identity_inverse_cocycle": True,
        "vertical_carry_inverse_clock_representation": True,
        "actual_composite_closes": True,
        "independent_direct_relation_constrained": False,
        "ambient_null_directions_identified": False,
        "screen_map_derived": False,
        "distinct_event_abstract_line_normalization_possible": True,
        "distinct_event_physical_composition_derived": False,
        "landing": LANDING,
    }
    if write_outputs:
        (ROOT / "DERIVATION_RESULT.json").write_text(
            json.dumps(result, indent=2) + "\n", encoding="utf-8"
        )
    print(
        f"PASS: G224 symbolic derivation; {len(checks)} exact checks; "
        "shared-event vertical carry classified"
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--check-only", action="store_true")
    args = parser.parse_args()
    main(write_outputs=not args.check_only)
