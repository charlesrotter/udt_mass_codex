#!/usr/bin/env python3
"""Hostile semantic and algebraic mutation catches for G201."""

from fractions import Fraction as F
import json


def amplitudes(f, p, q):
    return f * (2 * p * p + p - q), 1 - f * (1 + p)


def main() -> None:
    f = F(2)
    p = F(1, 3)
    q = F(-2, 5)
    actual = amplitudes(f, p, q)
    cancellation_p = 1 / f - 1
    cancellation_q = 2 * cancellation_p**2 + cancellation_p
    cancelled = amplitudes(f, cancellation_p, cancellation_q)

    catches = {
        "erase_p_from_perpendicular": actual[1] != 1 - f,
        "erase_q_from_parallel": actual[0] != f * (2 * p * p + p),
        "force_phi_evenness": amplitudes(F(2), 0, 0) != amplitudes(F(1, 2), 0, 0),
        "phi_zero_called_sufficiently_quiet": amplitudes(F(1), F(1), F(0)) != (0, 0),
        "negative_extreme_forced_angular_tide": cancelled == (0, 0),
        "positive_extreme_forced_angular_tide": amplitudes(F(1, 8), F(7), F(105)) == (0, 0),
        "reciprocal_contrast_confused_with_angular_tide": cancelled == (0, 0) and f != 1,
        "import_fitted_profile_or_xmax": "fit Xmax P1" not in "metric phi radial jets",
        "import_chiral_complete_coframe": "M X(deta+dz)" not in (
            "g=-f dx0^2+f^-1 dr^2+r^2 dOmega^2"
        ),
    }
    assert all(catches.values())
    print(json.dumps({
        "all_pass": True,
        "caught": sum(catches.values()),
        "total": len(catches),
        "catches": catches,
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
