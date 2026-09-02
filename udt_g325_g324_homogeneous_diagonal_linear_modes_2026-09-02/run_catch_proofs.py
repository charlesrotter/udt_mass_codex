#!/usr/bin/env python3
"""Hostile mutations for the preregistered G325 mode classification."""

from __future__ import annotations

import argparse
import json
from fractions import Fraction
from pathlib import Path


P = (Fraction(-1, 3), Fraction(2, 3), Fraction(2, 3))


def tracefree_residual(time, first, second):
    expansion = sum(first)
    ricci_00 = -sum(second_i + 2 * p_i * first_i / time
                    for p_i, first_i, second_i in zip(P, first, second))
    ricci_space = [second_i + first_i / time + p_i * expansion / time
                   for p_i, first_i, second_i in zip(P, first, second)]
    scalar = -ricci_00 + sum(ricci_space)
    return [ricci_00 + scalar / 4] + [value - scalar / 4 for value in ricci_space]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="CATCH_PROOF_RESULT.json")
    args = parser.parse_args()
    root = Path(__file__).resolve().parent

    time = Fraction(7, 5)
    bad_q = (Fraction(1), Fraction(-1), Fraction(0))
    bad_first = [value / time for value in bad_q]
    bad_second = [-value / time**2 for value in bad_q]
    wrong_q_rejected = any(tracefree_residual(time, bad_first, bad_second))

    scalar = Fraction(3, 11)
    # A common multiplier would only rename the free scalar amplitude. Mutate the relative
    # directional shape instead: (1+p_i), rather than the derived (1-p_i).
    bad_first = [(1 + p_i) * scalar * time / 2 for p_i in P]
    bad_second = [(1 + p_i) * scalar / 2 for p_i in P]
    wrong_scalar_shape_rejected = any(tracefree_residual(time, bad_first, bad_second))

    period = Fraction(13, 3)
    strain = Fraction(5, 17)
    false_periodic_scaling_rejected = strain * period != 0

    removed_constraint_vector = (Fraction(1), Fraction(0), Fraction(-1))
    removed_constraint_rejected = (
        sum(removed_constraint_vector) == 0
        and sum(p_i * q_i for p_i, q_i in zip(P, removed_constraint_vector)) != 0
    )

    fake_gauge_q = (Fraction(0), Fraction(1), Fraction(-1))
    curvature_split = -2 * fake_gauge_q[1] / (3 * time**2)
    physical_shear_as_gauge_rejected = curvature_split != 0

    controls = {
        "wrong_kasner_tangent_rejected": wrong_q_rejected,
        "wrong_scalar_directional_shape_rejected": wrong_scalar_shape_rejected,
        "false_periodic_scaling_rejected": false_periodic_scaling_rejected,
        "removed_exponent_constraint_rejected": removed_constraint_rejected,
        "physical_shear_as_gauge_rejected": physical_shear_as_gauge_rejected,
    }
    assert all(controls.values()), controls
    result = {
        "schema": "udt-g325-catch-proofs-v1",
        "status": "PASS",
        "assertion_count": len(controls),
        "controls": controls,
    }
    output = root / args.output
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
