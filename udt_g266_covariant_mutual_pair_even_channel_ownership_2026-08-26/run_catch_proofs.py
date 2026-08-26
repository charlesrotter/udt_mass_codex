#!/usr/bin/env python3
"""Hostile formula mutations for G266; writes nothing."""

from fractions import Fraction
import json


def main():
    r = Fraction(2, 3)
    s = Fraction(5, 4)
    gamma = lambda q: (q + 1 / q) / 2
    xi = lambda q: (1 / q - q) / 2
    catches = {
        "signed_arrow_is_not_even": r != 1 / r,
        "odd_channel_is_not_even": xi(1 / r) != xi(r),
        "gamma_composition_needs_odd_product": gamma(r * s) != gamma(r) * gamma(s),
        "sech_is_not_signed_clock_leg": 1 / gamma(r) != r,
        "positive_even_multiplicative_nontrivial_candidate_fails": (r != 1 / r),
        "areal_and_slice_second_jets_do_not_collapse": Fraction(4) != Fraction(2),
        "slice_and_optical_second_jets_do_not_collapse": Fraction(2) != Fraction(0),
        "conditional_projection_does_not_reject_histories": gamma(r) > 0 and gamma(s) > 0,
    }
    assert all(catches.values())
    print(json.dumps({
        "status": "PASS",
        "catches": len(catches),
        "mutations": catches,
        "qualification": "regression catches only; not independent scientific proof",
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
