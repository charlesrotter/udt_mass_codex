#!/usr/bin/env python3
"""Executable hostile semantic/algebraic mutations for the G287 sign boundary."""

from __future__ import annotations

import argparse
import json
from fractions import Fraction
from pathlib import Path


EXPECTED_NAMES = {
    "pair_reversal_changes_profile_sign",
    "directed_depth_sign_is_symmetric_regime",
    "sech_is_orientation_odd",
    "g267_two_ends_are_automatically_micro_macro",
    "negative_profile_alone_derives_mass",
    "matched_delta_equals_phi_is_universal_type_identity",
}


def correct_reverse(metric, profile, depth):
    return metric, profile, -depth


def mutant_reverse(metric, profile, depth):
    return (metric[1] * -1, metric[0] * -1), -profile, -depth


def reverse_valid(operation) -> bool:
    cases = [((-Fraction(2, 3), Fraction(3, 2)), 1, 3),
             ((-Fraction(5, 4), Fraction(4, 5)), -1, -2)]
    return all(operation(metric, profile, depth) == (metric, profile, -depth)
               for metric, profile, depth in cases)


def even_regime(depth: int) -> int:
    return abs(depth)


def mutant_signed_regime(depth: int) -> int:
    return 1 if depth > 0 else -1 if depth < 0 else 0


def reversal_invariant(classifier) -> bool:
    return all(classifier(depth) == classifier(-depth) for depth in (-7, -2, 2, 7))


def mutual(t: Fraction) -> Fraction:
    return 2 * t / (1 + t * t)


def mutant_odd_channel(t: Fraction) -> Fraction:
    return (t * t - 1) / (t * t + 1)


def channel_even(channel) -> bool:
    return all(channel(t) == channel(1 / t)
               for t in (Fraction(1, 7), Fraction(2, 3), Fraction(5, 2)))


def g267_scope_valid(statement: str) -> bool:
    normalized = " ".join(statement.split()).lower()
    return (
        "signed one-way" in normalized
        and "remains" in normalized
        and "automatically micro/cosmological profile regimes" not in normalized
    )


def mass_requires_law(profile_sign: int, has_mass_law: bool) -> bool:
    return has_mass_law


def mutant_mass_from_sign(profile_sign: int, has_mass_law: bool) -> bool:
    return profile_sign < 0 or has_mass_law


def endpoint_depth(value_a: int, value_b: int) -> int:
    return value_b - value_a


def mutant_universal_phi(value_a: int, value_b: int) -> int:
    return value_b


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    baseline_g267 = (
        "The mutual effect is symmetric at both infinite-depth ends. "
        "The signed one-way clock/frequency arrow remains first order and is not replaced."
    )
    mutant_g267 = baseline_g267 + " The ends are automatically micro/cosmological profile regimes."

    baseline_checks = {
        "pair_reversal": reverse_valid(correct_reverse),
        "regime_classifier": reversal_invariant(even_regime),
        "mutual_evenness": channel_even(mutual),
        "g267_scope": g267_scope_valid(baseline_g267),
        "mass_requires_law": not mass_requires_law(-1, False),
        "endpoint_reference": endpoint_depth(2, 5) == 3,
    }
    caught = {
        "pair_reversal_changes_profile_sign": not reverse_valid(mutant_reverse),
        "directed_depth_sign_is_symmetric_regime": not reversal_invariant(mutant_signed_regime),
        "sech_is_orientation_odd": not channel_even(mutant_odd_channel),
        "g267_two_ends_are_automatically_micro_macro": not g267_scope_valid(mutant_g267),
        "negative_profile_alone_derives_mass": (
            mutant_mass_from_sign(-1, False) != mass_requires_law(-1, False)
        ),
        "matched_delta_equals_phi_is_universal_type_identity": mutant_universal_phi(2, 5) != 3,
    }
    exact_registry = set(caught) == EXPECTED_NAMES and len(caught) == 6
    result = {
        "baseline_checks": baseline_checks,
        "caught": caught,
        "exact_mutation_registry": exact_registry,
        "mutation_count": len(caught),
        "pass": exact_registry and all(baseline_checks.values()) and all(caught.values()),
    }
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(payload, encoding="utf-8")
    print(payload, end="")
    raise SystemExit(0 if result["pass"] else 1)


if __name__ == "__main__":
    main()
