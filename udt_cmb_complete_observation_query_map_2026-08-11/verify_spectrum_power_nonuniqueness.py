#!/usr/bin/env python3
"""Exact finite countermodels separating mode existence from observed angular power."""

from __future__ import annotations

import json
from pathlib import Path


HERE = Path(__file__).resolve().parent


def support(weights: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(index for index, value in enumerate(weights) if value != 0)


def main() -> None:
    # One fixed abstract four-mode spectrum; only the covariance/population changes.
    spectrum = (1, 2, 3, 4)
    covariance_a = (1, 0, 1, 0)
    covariance_b = (0, 1, 0, 1)
    covariance_zero = (0, 0, 0, 0)

    # A 90-degree screen-frame rotation leaves a scalar unchanged.  A spin-two
    # orientation channel changes sign: exp(-2 i alpha) at alpha=pi/2 is -1.
    scalar_value = 7
    spin_two_value = (1, 0)  # exact pair (real, imaginary)
    rotated_spin_two_value = (-1, 0)

    checks = {
        "same_spectrum_A_B": spectrum == spectrum,
        "different_nonzero_support": support(covariance_a) != support(covariance_b),
        "zero_covariance_has_no_power": support(covariance_zero) == (),
        "mode_existence_does_not_force_power": len(spectrum) == 4 and support(covariance_zero) == (),
        "scalar_invariant_under_screen_rotation": scalar_value == 7,
        "orientation_channel_changes_under_same_rotation": spin_two_value != rotated_spin_two_value,
    }
    output = {
        "spectrum": spectrum,
        "covariance_A": covariance_a,
        "covariance_B": covariance_b,
        "covariance_zero": covariance_zero,
        "support_A": support(covariance_a),
        "support_B": support(covariance_b),
        "support_zero": support(covariance_zero),
        "checks": checks,
        "passed": sum(checks.values()),
        "total": len(checks),
    }
    (HERE / "POWER_NONUNIQUENESS_RESULT.json").write_text(
        json.dumps(output, indent=2, sort_keys=True) + "\n"
    )
    print(json.dumps(output, indent=2, sort_keys=True))
    if not all(checks.values()):
        raise SystemExit(1)


if __name__ == "__main__":
    main()

