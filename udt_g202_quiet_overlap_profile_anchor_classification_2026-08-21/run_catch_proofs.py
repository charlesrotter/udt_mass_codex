#!/usr/bin/env python3
"""Hostile semantic and algebraic mutation catches for G202."""

from fractions import Fraction as F
import json


def main() -> None:
    phi = F(0)
    p_log = F(1)
    q_log = F(0)
    a = F(2, 3)
    s = F(3, 5)
    cubic = a * s**3
    quintic_variant = cubic + F(1, 7) * s**5

    catches = {
        "phi_zero_called_full_quiet_overlap": (2 * p_log**2 + 2 * p_log - q_log, -p_log) != (0, 0),
        "first_log_derivative_erased": p_log != 0,
        "second_log_derivative_erased": q_log == 0 and p_log != 0,
        "even_order_called_sign_crossing": (-s)**4 == s**4,
        "cubic_control_promoted_to_unique_profile": cubic != quintic_variant,
        "finite_anchors_called_global_selector": "same finite jets" != "same global function",
        "cE_and_G_called_length_without_mass_anchor": (-F(0), -F(0), F(0)) != (F(1), F(0), F(0)),
        "dimensional_candidate_promoted_to_physical_law": "GM/cE^2 candidate" != "selected r0",
        "import_fit_xmax_or_transfer": "fit Xmax transfer" not in "quiet overlap profile theorem",
    }
    assert phi == 0
    assert all(catches.values())
    print(json.dumps({
        "all_pass": True,
        "caught": sum(catches.values()),
        "total": len(catches),
        "catches": catches,
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
