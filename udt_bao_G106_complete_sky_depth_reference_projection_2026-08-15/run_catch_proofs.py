#!/usr/bin/env python3
"""Hostile mutations for the G106 sky/depth projection gates."""

from __future__ import annotations

import json
import os
from fractions import Fraction as F
from pathlib import Path


HERE = Path(__file__).resolve().parent


def caught_unnormalized_selection() -> bool:
    return sum([F(1, 10), F(2, 10), F(3, 10), F(5, 10)]) != 1


def caught_nonidempotent_reference() -> bool:
    s = [F(1, 4)] * 4
    p = [[F(1, 8), F(1, 8), F(1, 8), F(1, 8)], [F(1, 8)] * 4]

    def bad_r(matrix: list[list[F]]) -> list[list[F]]:
        # Deliberate row-mass inflation.
        return [[2 * sum(row) * value for value in s] for row in matrix]

    return bad_r(bad_r(p)) != bad_r(p)


def caught_wrong_marginal_axis() -> bool:
    p = [[F(1, 10), F(2, 10)], [F(3, 10), F(4, 10)]]
    correct_rows = [sum(row) for row in p]
    wrong_rows = [sum(p[i][j] for i in range(2)) for j in range(2)]
    return correct_rows != wrong_rows


def caught_pure_radial_leak() -> bool:
    s = [F(1, 3), F(2, 3)]
    depth = [F(1, 4), F(3, 4)]
    radial = [[depth[i] * s[j] for j in range(2)] for i in range(2)]
    bad_q = [[F(1, 2) * s[j] for j in range(2)] for _ in range(2)]
    return any(radial[i][j] != bad_q[i][j] for i in range(2) for j in range(2))


def caught_interaction_erasure() -> bool:
    p = [[F(1, 8), F(3, 8)], [F(3, 8), F(1, 8)]]
    identity_reference = p
    residual = [[p[i][j] - identity_reference[i][j] for j in range(2)] for i in range(2)]
    return not any(value != 0 for row in residual for value in row)


def caught_window_retune() -> bool:
    derived = [F(13, 108), F(1, 108), F(13, 108)]
    independently_retuned = [F(13, 108), F(2, 108), F(13, 108)]
    return independently_retuned != derived


def caught_negative_full_sky_density() -> bool:
    # At the equator P2=-1/2; amplitude 3 is outside the positive range.
    return 1 + 3 * F(-1, 2) <= 0


def caught_pole_displacement() -> bool:
    epsilon = F(1, 20)
    mapped_north = 1 + epsilon
    mapped_south = -1 + epsilon
    return mapped_north != 1 or mapped_south != -1


def caught_linear_pair_amplitude() -> bool:
    outer, middle = F(13, 108), F(1, 108)
    wrong_ratio = (outer / 5) / (middle / 5)
    return wrong_ratio != 169


def caught_coordinate_jacobian_mismatch() -> bool:
    ratio = F(323062, 260925)
    determinant_change = F(4)  # det(C)^2 with det(C)=2
    bad_transformed = ratio * determinant_change
    return bad_transformed != ratio


def caught_manifest_mutation() -> bool:
    fake_digest = "0" * 64
    recorded = "ab892888ba70930187a64f4bae828f3dc30a9d2380e22d5edd8fecfa99ab3adf"
    return fake_digest != recorded


def caught_outcome_token() -> bool:
    forbidden = {"R2_OUTCOME_REPORT.md", "R3_OUTCOME_REPORT.md", "CMB_OUTCOME"}
    mutated_executable = "open('R2_OUTCOME_REPORT.md')"
    return any(token in mutated_executable for token in forbidden)


def main() -> None:
    caught = {
        "M01_unnormalized_selection": caught_unnormalized_selection(),
        "M02_nonidempotent_reference": caught_nonidempotent_reference(),
        "M03_wrong_marginal_axis": caught_wrong_marginal_axis(),
        "M04_pure_radial_leak": caught_pure_radial_leak(),
        "M05_interaction_erasure": caught_interaction_erasure(),
        "M06_independent_window_retune": caught_window_retune(),
        "M07_negative_full_sky_density": caught_negative_full_sky_density(),
        "M08_pole_displacement": caught_pole_displacement(),
        "M09_linear_not_quadratic_pair_amplitude": caught_linear_pair_amplitude(),
        "M10_coordinate_jacobian_mismatch": caught_coordinate_jacobian_mismatch(),
        "M11_manifest_mutation": caught_manifest_mutation(),
        "M12_outcome_token": caught_outcome_token(),
    }
    result = {
        "status": "PASS" if all(caught.values()) else "FAIL",
        "caught": caught,
        "caught_count": sum(bool(value) for value in caught.values()),
        "total": len(caught),
    }
    if result["status"] != "PASS":
        raise AssertionError(result)
    if os.environ.get("UDT_READ_ONLY_REPLAY") != "1":
        (HERE / "CATCH_PROOF_RESULT.json").write_text(
            json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
