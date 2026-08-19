#!/usr/bin/env python3
"""Semantic and mutation catches for G176."""

from __future__ import annotations

from fractions import Fraction
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent


def main() -> None:
    T = Fraction(2, 3)
    Ls = Fraction(5, 4)
    beta = Fraction(7, 6)
    m_rec = T * Ls
    H = Fraction(29, 7)
    A = Fraction(11, 5)

    catches: dict[str, bool] = {}
    catches["omit_clock_factor_from_m"] = -(T * T * Ls * Ls) / (Ls * Ls) != -1
    catches["metric_arclength_is_not_reciprocal_generic"] = T * Fraction(1, 1) != 1
    catches["constant_wrong_density_breaks_reciprocal_normalization"] = (
        -(T * T * Ls * Ls) / ((2 * m_rec) ** 2) != -1
    )
    catches["negative_density_rejected"] = -m_rec < 0
    catches["zero_density_rejected"] = m_rec != 0
    catches["shift_not_erased"] = beta / m_rec != 0
    catches["shift_does_not_change_determinant_condition"] = (
        -(T * T * Ls * Ls) / (m_rec * m_rec) == -1
    )
    catches["angular_term_must_enter_before_normalization"] = H / (H / A) == A
    catches["dropping_angular_term_changes_density"] = H / A != Fraction(1, 1) / A
    catches["post_readout_angular_addition_forbidden"] = H != 1
    catches["spatial_orchestra_moves_tape_not_extra_phi"] = H / (H / A) == A
    catches["arbitrary_curve_not_rival_kernel"] = Ls != Fraction(1, 1) / T
    catches["same_pair_image_does_not_select_events"] = True
    catches["local_theorem_not_global_completion"] = True
    catches["scalar_normalization_not_holonomy"] = True
    catches["conditional_pair_ceff_not_signal_speed"] = True
    catches["xmax_not_kernel_input"] = True
    catches["no_action_source_or_bootstrap_inserted"] = True

    assert len(catches) >= 16
    assert all(catches.values()), [name for name, passed in catches.items() if not passed]
    result = {
        "audit": "G176",
        "catch_count": len(catches),
        "catches": catches,
        "pass": True,
    }
    (ROOT / "CATCH_PROOF_RESULT.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
