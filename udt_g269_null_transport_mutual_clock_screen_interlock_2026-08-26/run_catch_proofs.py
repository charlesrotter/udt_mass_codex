#!/usr/bin/env python3
"""Inject ten G269 mutations through a shared exact-rational validator."""

from __future__ import annotations

import argparse
from dataclasses import dataclass, replace
from fractions import Fraction
import json
from pathlib import Path
from typing import Callable


OUT = Path(__file__).with_name("CATCH_PROOF_RESULT.json")


@dataclass(frozen=True)
class Candidate:
    ratio: Callable[[Fraction, Fraction], Fraction]
    mutual: Callable[[Fraction], Fraction]
    gamma: Callable[[Fraction, Fraction], Fraction]
    longitudinal: Callable[[Fraction, Fraction], Fraction]
    screen_norm: Callable[[Fraction], Fraction]
    reverse_gamma: Callable[[Fraction, Fraction], Fraction]
    normalized_scale: Callable[[Fraction, Fraction], Fraction]
    universal_equality_claimed: bool
    jacobi_area_conflated: bool
    query_or_history_selected: bool


def validate(candidate: Candidate) -> list[str]:
    failures: list[str] = []
    cases = (
        (Fraction(2), Fraction(0)),
        (Fraction(1, 2), Fraction(0)),
        (Fraction(3, 2), Fraction(1, 3)),
        (Fraction(5, 3), Fraction(2, 5)),
    )

    if candidate.ratio(Fraction(3), Fraction(2)) != Fraction(3, 2):
        failures.append("frequency_ratio_orientation")

    for r, w in cases:
        w_sq = candidate.screen_norm(w)
        gamma = candidate.gamma(r, w)
        a = candidate.longitudinal(r, w)
        gamma_kernel = (r + 1 / r) / 2
        if -gamma * gamma + a * a + w_sq != -1:
            failures.append("lorentz_decomposition_sign")
        if gamma - a != 1 / r:
            failures.append("frequency_contraction")
        if gamma != gamma_kernel + r * w * w / 2:
            failures.append("screen_interlock")
        if w_sq < 0:
            failures.append("screen_nonnegative")
        if candidate.mutual(gamma) != 1 / gamma:
            failures.append("inverse_gamma_readout")
        if candidate.reverse_gamma(r, w) != gamma:
            failures.append("reversal_evenness")
        if candidate.normalized_scale(Fraction(7, 3), Fraction(5, 2)) != Fraction(2, 5):
            failures.append("affine_invariance")
        if w != 0 and candidate.universal_equality_claimed:
            failures.append("nonplanar_equality_rejection")

    if candidate.jacobi_area_conflated:
        failures.append("no_jacobi_area_conflation")
    if candidate.query_or_history_selected:
        failures.append("no_query_history_selection")
    return sorted(set(failures))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--no-write", action="store_true")
    args = parser.parse_args()

    def gamma(r: Fraction, w: Fraction) -> Fraction:
        return (r + 1 / r + r * w * w) / 2

    baseline = Candidate(
        ratio=lambda omega_a, omega_b: omega_a / omega_b,
        mutual=lambda gamma_value: 1 / gamma_value,
        gamma=gamma,
        longitudinal=lambda r, w: gamma(r, w) - 1 / r,
        screen_norm=lambda w: w * w,
        reverse_gamma=lambda r, w: (1 / r + r + (1 / r) * (r * w) ** 2) / 2,
        normalized_scale=lambda scale, omega: scale / (scale * omega),
        universal_equality_claimed=False,
        jacobi_area_conflated=False,
        query_or_history_selected=False,
    )
    baseline_failures = validate(baseline)
    assert not baseline_failures

    mutants: dict[str, tuple[Candidate, str]] = {
        "reversed_frequency_ratio": (
            replace(baseline, ratio=lambda omega_a, omega_b: omega_b / omega_a),
            "frequency_ratio_orientation",
        ),
        "missing_inverse_mutual": (
            replace(baseline, mutual=lambda gamma_value: gamma_value),
            "inverse_gamma_readout",
        ),
        "wrong_longitudinal_sign": (
            replace(baseline, longitudinal=lambda r, w: gamma(r, w) + 1 / r),
            "frequency_contraction",
        ),
        "deleted_screen_term": (
            replace(baseline, gamma=lambda r, _w: (r + 1 / r) / 2),
            "screen_interlock",
        ),
        "negative_screen_norm": (
            replace(baseline, screen_norm=lambda w: -(w * w)),
            "screen_nonnegative",
        ),
        "universal_nonplanar_equality": (
            replace(baseline, universal_equality_claimed=True),
            "nonplanar_equality_rejection",
        ),
        "reversal_not_even": (
            replace(baseline, reverse_gamma=lambda r, w: gamma(r, w) + 1),
            "reversal_evenness",
        ),
        "affine_scale_leak": (
            replace(baseline, normalized_scale=lambda scale, omega: scale / omega),
            "affine_invariance",
        ),
        "jacobi_area_conflation": (
            replace(baseline, jacobi_area_conflated=True),
            "no_jacobi_area_conflation",
        ),
        "query_history_promotion": (
            replace(baseline, query_or_history_selected=True),
            "no_query_history_selection",
        ),
    }

    mutation_results: dict[str, dict[str, object]] = {}
    missed: list[str] = []
    for name, (mutant, target) in mutants.items():
        failures = validate(mutant)
        caught = target in failures and bool(failures)
        mutation_results[name] = {
            "caught": caught,
            "failures": failures,
            "targeted_failure": target,
            "targeted_caught": target in failures,
        }
        if not caught:
            missed.append(name)

    assert not missed
    result = {
        "status": "PASS",
        "baseline_failures": baseline_failures,
        "catches": len(mutation_results),
        "mutations": mutation_results,
        "missed": missed,
        "shared_validator_exercised": True,
    }
    rendered = json.dumps(result, indent=2, sort_keys=True)
    if not args.no_write:
        OUT.write_text(rendered + "\n", encoding="utf-8")
    print(rendered)


if __name__ == "__main__":
    main()
