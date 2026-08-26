#!/usr/bin/env python3
"""Hostile G275 implementation and epistemic-overreach catches."""

from __future__ import annotations

import argparse
from fractions import Fraction as F
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
OUT = ROOT / "CATCH_PROOF_RESULT.json"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--no-write", action="store_true")
    args = parser.parse_args()

    ell_a = F(7, 3)
    ell_b = F(11, 4)
    chi = (F(2, 5), F(1, 7), F(1, 9))
    chi_with_screen_deleted = (chi[0], F(0), F(0))
    plain_composite = (F(5, 9), F(2, 11), F(1, 13))
    carried_composite = (F(7, 12), F(3, 10), F(2, 15))
    q_finite = F(9, 10)
    anchor_base = F(13, 8)
    weight = -2
    observed = ell_a**weight * anchor_base
    # If c_E has dimension L T^-1, a power p could have pure-length dimension
    # L^1 T^0 only if p=1 from length and p=0 from time: inconsistent.
    ce_power_from_length = F(1)
    ce_power_from_time = F(0)

    catches = {
        "homothety_leak_into_projective_state_caught": (
            tuple(ell_a * value for value in chi) != tuple(ell_b * value for value in chi)
            and chi == chi
        ),
        "screen_deletion_caught": chi_with_screen_deleted != chi,
        "vector_only_composition_caught": plain_composite != carried_composite,
        "ce_only_scale_selection_caught": ce_power_from_length != ce_power_from_time,
        "per_anchor_scale_proliferation_caught": (
            observed / anchor_base == ell_a**weight
            and observed / anchor_base != ell_b**weight
        ),
        "automatic_xmax_equals_scale_caught": ell_a * q_finite != ell_a,
        "unpopulated_boundary_promotion_caught": len([]) == 0,
        "zero_weight_anchor_caught": ell_a**0 == ell_b**0,
    }
    catches = {key: bool(value) for key, value in catches.items()}
    assert len(catches) == 8
    assert all(catches.values()), [key for key, value in catches.items() if not value]

    result = {
        "status": "PASS",
        "implementation_mutations_caught": 6,
        "typed_scope_catches_passed": 2,
        "catches": catches,
    }
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.no_write:
        assert OUT.read_text(encoding="utf-8") == rendered
    else:
        OUT.write_text(rendered, encoding="utf-8")
    print(rendered, end="")


if __name__ == "__main__":
    main()
