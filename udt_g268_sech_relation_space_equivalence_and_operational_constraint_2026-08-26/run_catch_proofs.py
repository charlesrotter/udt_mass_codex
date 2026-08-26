#!/usr/bin/env python3
"""Inject eight G268 logic mutations through one exact-rational validator."""

from __future__ import annotations

import argparse
from dataclasses import dataclass, replace
from fractions import Fraction
import json
from pathlib import Path
from typing import Callable


OUT = Path(__file__).with_name("CATCH_PROOF_RESULT.json")
State = tuple[Fraction, Fraction]


def state(r: Fraction) -> State:
    return 2 * r / (1 + r * r), (1 - r * r) / (1 + r * r)


def inverse(m: Fraction, x: Fraction) -> Fraction:
    return (1 - x) / m


def compose(a: State, b: State) -> State:
    ma, xa = a
    mb, xb = b
    den = 1 + xa * xb
    return ma * mb / den, (xa + xb) / den


def accepts_state(m: Fraction, x: Fraction) -> bool:
    return m > 0 and -1 < x < 1 and m * m + x * x == 1


def endpoint_composable(a: State, b: State) -> bool:
    return 1 + a[1] * b[1] != 0


@dataclass(frozen=True)
class Candidate:
    state: Callable[[Fraction], State]
    inverse: Callable[[Fraction, Fraction], Fraction]
    compose: Callable[[State, State], State]
    accepts_state: Callable[[Fraction, Fraction], bool]
    endpoint_composable: Callable[[State, State], bool]
    history_rejections: int
    operational_protocol_owned: bool


def validate(candidate: Candidate) -> list[str]:
    failures: list[str] = []
    ratios = (Fraction(1, 3), Fraction(1, 2), Fraction(1), Fraction(2), Fraction(3))
    for r in ratios:
        m, x = candidate.state(r)
        if not candidate.accepts_state(m, x):
            failures.append("forward_state_membership")
        if candidate.inverse(m, x) != r:
            failures.append("inverse_reconstruction")
        mi, xi = candidate.state(1 / r)
        if mi != m or xi != -x:
            failures.append("reversal_sign")
    for r1 in ratios:
        for r2 in ratios:
            if candidate.compose(candidate.state(r1), candidate.state(r2)) != candidate.state(r1 * r2):
                failures.append("composition_law")
    if candidate.accepts_state(Fraction(1, 2), Fraction(1, 2)):
        failures.append("off_circle_rejection")
    plus = (Fraction(0), Fraction(1))
    minus = (Fraction(0), Fraction(-1))
    if candidate.endpoint_composable(plus, minus):
        failures.append("opposite_endpoint_rejection")
    if candidate.history_rejections != 0:
        failures.append("zero_history_selection")
    if candidate.operational_protocol_owned:
        failures.append("open_protocol_ownership")
    return sorted(set(failures))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--no-write", action="store_true")
    args = parser.parse_args()

    baseline = Candidate(
        state=state,
        inverse=inverse,
        compose=compose,
        accepts_state=accepts_state,
        endpoint_composable=endpoint_composable,
        history_rejections=0,
        operational_protocol_owned=False,
    )
    baseline_failures = validate(baseline)
    assert not baseline_failures

    def state_without_sign(r: Fraction) -> State:
        m, x = state(r)
        return m, abs(x)

    def wrong_inverse(m: Fraction, x: Fraction) -> Fraction:
        return (1 + x) / m

    def multiplicative_m(a: State, b: State) -> State:
        ma, xa = a
        mb, xb = b
        den = 1 + xa * xb
        return ma * mb, (xa + xb) / den

    def denominator_deleted_from_chi(a: State, b: State) -> State:
        ma, xa = a
        mb, xb = b
        den = 1 + xa * xb
        return ma * mb / den, xa + xb

    mutants: dict[str, tuple[Candidate, str]] = {
        "loss_of_chi_sign": (replace(baseline, state=state_without_sign), "reversal_sign"),
        "wrong_inverse_r": (replace(baseline, inverse=wrong_inverse), "inverse_reconstruction"),
        "multiplicative_m": (replace(baseline, compose=multiplicative_m), "composition_law"),
        "deleted_composition_denominator": (
            replace(baseline, compose=denominator_deleted_from_chi),
            "composition_law",
        ),
        "off_circle_state_accepted": (
            replace(baseline, accepts_state=lambda _m, _x: True),
            "off_circle_rejection",
        ),
        "opposite_endpoints_called_regular": (
            replace(baseline, endpoint_composable=lambda _a, _b: True),
            "opposite_endpoint_rejection",
        ),
        "history_rejection_injected": (
            replace(baseline, history_rejections=1),
            "zero_history_selection",
        ),
        "operational_ownership_injected": (
            replace(baseline, operational_protocol_owned=True),
            "open_protocol_ownership",
        ),
    }

    mutation_results: dict[str, dict[str, object]] = {}
    missed: list[str] = []
    for name, (mutant, targeted_failure) in mutants.items():
        failures = validate(mutant)
        targeted_caught = targeted_failure in failures
        caught = bool(failures) and targeted_caught
        mutation_results[name] = {
            "caught": caught,
            "failures": failures,
            "targeted_failure": targeted_failure,
            "targeted_caught": targeted_caught,
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
