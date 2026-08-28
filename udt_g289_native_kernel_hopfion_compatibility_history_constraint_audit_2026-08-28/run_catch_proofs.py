#!/usr/bin/env python3
"""Hostile recomputation and typed-promotion catches for G289."""

from __future__ import annotations

import csv
import json
from fractions import Fraction as F
from pathlib import Path


HERE = Path(__file__).resolve().parent
OUT = HERE / "CATCH_PROOF_RESULT.json"


def dot(left: tuple[F, ...], right: tuple[F, ...]) -> F:
    return sum((x * y for x, y in zip(left, right)), F(0))


def pushed_tangent_norm(
    direction: tuple[F, F, F], tangent: tuple[F, F, F], beta: F, gamma: F
) -> F:
    denominator = gamma * (1 - beta * direction[2])
    spatial = (direction[0], direction[1], gamma * (direction[2] - beta))
    denominator_derivative = -gamma * beta * tangent[2]
    spatial_derivative = (tangent[0], tangent[1], gamma * tangent[2])
    pushed = tuple(
        (derivative * denominator - component * denominator_derivative)
        / (denominator * denominator)
        for derivative, component in zip(spatial_derivative, spatial)
    )
    return dot(pushed, pushed)


def conformal_center_scalar(alpha: F, spatial_dimension: int = 3) -> F:
    # In four dimensions R[e^(2 omega) eta]=-6 e^(-2 omega)(box omega+|d omega|^2).
    # For static omega=alpha*(x^2+y^2+z^2), d omega vanishes at the center and
    # box omega is the sum of the three independently reconstructed second derivatives 2*alpha.
    center_box = sum((2 * alpha for _ in range(spatial_dimension)), F(0))
    center_gradient_square = F(0)
    return -6 * (center_box + center_gradient_square)


def normalized_hopf_connection_integral() -> F:
    # With s=sin^2(h), A=(1-s)du+s dv and dA=ds^(dv-du). Expanding A^dA in the
    # orientation ds^du^dv gives the sum -(1-s)-s, integrated over s in [0,1].
    first_term = (F(-1), F(1))
    second_term = (F(0), F(-1))
    density = tuple(x + y for x, y in zip(first_term, second_term))
    return sum((coefficient / F(power + 1) for power, coefficient in enumerate(density)), F(0))


def main() -> None:
    mutations = []

    # M1: falsely admit a nonunit direction as a null representative.
    nonunit_direction = (F(2), F(0), F(0))
    false_null_norm = -F(1) + dot(nonunit_direction, nonunit_direction)
    mutations.append({"mutation": "nonunit_direction_called_null", "caught": false_null_norm != 0})

    # M2: falsely call the exact boost witness a round-S2 isometry.
    boost_target_scale = pushed_tangent_norm(
        (F(1), F(0), F(0)), (F(0), F(1), F(0)), F(3, 5), F(5, 4)
    )
    mutations.append({"mutation": "boost_called_round_target_isometry", "caught": boost_target_scale != 1})

    # M3: falsely identify equal null cones with equal metric history.
    flat_center_scalar = conformal_center_scalar(F(0))
    curved_center_scalar = conformal_center_scalar(F(1))
    mutations.append(
        {
            "mutation": "same_null_texture_called_same_history",
            "caught": flat_center_scalar != curved_center_scalar,
        }
    )

    # M4: falsely call raw component Hopf class invariant under every local frame rotation.
    constant_component_charge = 0
    rotated_component_charge = abs(normalized_hopf_connection_integral())
    mutations.append(
        {
            "mutation": "raw_component_hopf_charge_called_full_frame_gauge_invariant",
            "caught": constant_component_charge != rotated_component_charge,
        }
    )

    # M5: promote the historical action/boundary/stability labels to native selectors.
    with (HERE / "PREMISE_LEDGER.tsv").open(newline="") as handle:
        rows = {row["item"]: row for row in csv.DictReader(handle, delimiter="\t")}
    conditional = (
        rows["historical_round_S2_carrier"]["status"] == "POSIT"
        and rows["historical_L2_plus_L4_functional"]["status"] == "CONDITIONAL_IMPORT"
        and rows["historical_fixed_box_boundary"]["status"] == "CHOSE_NUMERICALLY"
        and rows["historical_static_stability"]["status"] == "SETTLED_STATIC_FINITE_BOX_CONDITIONAL"
    )
    mutations.append({"mutation": "conditional_stability_called_native_history_selector", "caught": conditional})

    result = {
        "status": "PASS" if all(row["caught"] for row in mutations) else "FAIL",
        "caught": sum(bool(row["caught"]) for row in mutations),
        "total": len(mutations),
        "recomputing_geometric_catches": 4,
        "typed_promotion_catches": 1,
        "recomputed_witnesses": {
            "false_null_norm": str(false_null_norm),
            "boost_target_scale": str(boost_target_scale),
            "flat_center_scalar": str(flat_center_scalar),
            "curved_center_scalar": str(curved_center_scalar),
            "rotated_component_charge": str(rotated_component_charge),
        },
        "mutations": mutations,
    }
    if result["status"] != "PASS":
        raise AssertionError(result)
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
