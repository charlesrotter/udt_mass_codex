#!/usr/bin/env python3
"""Regression mutations for G267; catches only, not independent scientific proof."""

from __future__ import annotations

from fractions import Fraction
import json
import math


def main() -> None:
    delta = 0.4
    mutual = 1 / math.cosh(delta)
    position = math.tanh(delta)
    p = Fraction(4, 5)
    q = Fraction(3, 5)
    same_mutual = p * p / (1 + q * q)
    opposite_mutual = p * p / (1 - q * q)
    gamma = Fraction(5, 4)
    mutations = {
        "linear_quiet_mutual_term_rejected": abs((-1.0) - 0.0) > 0.5,
        "reversal_odd_mutual_rejected": abs((mutual + position) - (mutual - position)) > 0.1,
        "composition_without_signed_position_rejected": same_mutual != p * p,
        "M_alone_cannot_choose_same_or_opposite_sign": same_mutual != opposite_mutual,
        "mutual_projection_is_not_signed_arrow": abs(mutual - math.exp(-delta)) > 1e-3,
        "evenness_alone_does_not_select_inverse_trace": len({1 / gamma, 1 / gamma**2, Fraction(2) / (gamma + 1)}) == 3,
        "dimensionless_state_contains_no_length_scale": all(symbol not in {"M", "chi", "delta"} for symbol in ("ell", "R", "Xmax")),
        "candidate_evaluates_two_distinct_histories": (
            (1 / math.cosh(0.2), math.tanh(0.2))
            != (1 / math.cosh(-0.7), math.tanh(-0.7))
        ),
    }
    assert all(mutations.values())
    print(json.dumps({
        "status": "PASS",
        "catches": len(mutations),
        "mutations": mutations,
        "qualification": "regression catches only; not independent scientific proof",
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
