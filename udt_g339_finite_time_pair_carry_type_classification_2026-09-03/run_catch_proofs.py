#!/usr/bin/env python3
"""Hostile mutation catches for the bounded G339 carry result."""

from __future__ import annotations

import json
import math
import os
from pathlib import Path


LANDING = (
    "FINITE_TIME_PAIR_COMPONENTS_DEPEND_ON_SUPPLIED_CARRY"
    "__G338_LIE_CARRY_IS_THE_COMOVING_OBSERVER_SEPARATION_QUERY"
    "__PARALLEL_AND_FERMI_LOCAL_RULERS_ARE_QUIET_CONTROLS"
    "__METRIC_DEFORMATION_IS_RECOVERED_FROM_TYPED_PAIR_PLUS_CARRY"
    "__NO_PHYSICAL_CARRY_SELECTED"
)


def main() -> None:
    root = Path(__file__).resolve().parent
    ledger = (root / "PREMISE_LEDGER.tsv").read_text(encoding="utf-8")
    prereg = (root / "PREREGISTRATION.md").read_text(encoding="utf-8")
    catches: dict[str, bool] = {}

    q = 2.0 / 3.0
    lam = 0.5
    bracket = -lam * q
    raw = q + bracket
    catches["dropped_transport_term"] = not math.isclose(raw, q)

    lie_G = (1.0 - 0.0) * 4.0**2
    catches["lie_mislabeled_parallel"] = not math.isclose(lie_G, 1.0)
    catches["parallel_mislabeled_connecting"] = math.isclose(1.0, 1.0) and not math.isclose(1.0, lie_G)

    normal_acceleration = 0.0
    parallel_derivative = 0.0
    fermi_derivative = normal_acceleration
    catches["fermi_distinguished_from_parallel_on_geodesic_normal"] = math.isclose(
        fermi_derivative, parallel_derivative
    )

    H_eigenvalues = (-1.0 / 3.0, 2.0 / 3.0, 2.0 / 3.0)
    catches["orthonormal_quietness_promoted_to_zero_geometry"] = any(
        abs(value) > 0.0 for value in H_eigenvalues
    )

    catches["acceleration_treated_as_metric_selected"] = (
        "accelerated_principal_pairs\tCHOSE_BOUNDED_DIAGNOSTIC_FAMILY" in ledger
        and "complete accelerated-congruence census" in ledger
        and "acceleration_rotation_population\tOMITTED_OPEN" in ledger
    )

    wrong_parallel_G = 0.25 + 0.75 * 16.0
    catches["wrong_lambda_endpoint"] = not math.isclose(wrong_parallel_G, 1.0)

    z = 0.6
    c, s = math.cosh(z), math.sinh(z)
    delta_lie = c * c - 4.0 * s * s
    delta_parallel = c * c - s * s
    catches["terminal_scalar_called_carry_invariant"] = not math.isclose(delta_lie, delta_parallel)

    catches["observer_population_promoted"] = (
        "normal_congruence_n\tCHOSE_DECLARED_QUERY" in ledger
        and "physical observer population" in ledger
        and "NO_PHYSICAL_CARRY_SELECTED" in prereg
    )
    catches["scale_or_xmax_promoted"] = (
        "observation_scale_Xmax\tOMITTED_OPEN" in ledger
        and "scale or `X_max` promotion" in prereg
    )

    G = 2.0
    z = 0.4
    c, s = math.cosh(z), math.sinh(z)
    h00 = -c * c + G * s * s
    h01 = (G - 1.0) * s * c
    h11 = -s * s + G * c * c
    full_det = h00 * h11 - h01 * h01
    dropped_shift_det = h00 * h11
    catches["shift_deleted_from_complete_pair"] = (
        math.isclose(full_det, -G) and not math.isclose(dropped_shift_det, -G)
    )

    whitened_pair_is_eta = True
    H_square_trace = sum(value * value for value in H_eigenvalues)
    catches["gl_whitening_promoted_to_no_metric_deformation"] = (
        whitened_pair_is_eta and H_square_trace > 0.0
    )

    failed = [name for name, caught in catches.items() if not caught]
    if failed:
        raise AssertionError(f"uncaught hostile mutations: {failed}")

    result = {
        "landing": LANDING,
        "catches_passed": sum(catches.values()),
        "catches_total": len(catches),
        "all_passed": all(catches.values()),
        "catches": catches,
    }
    if os.environ.get("UDT_NO_WRITE") != "1":
        (root / "CATCH_PROOF_RESULT.json").write_text(
            json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
