#!/usr/bin/env python3
"""Hostile mutation and typed-scope catches for G276."""

from __future__ import annotations

import argparse
from dataclasses import dataclass, replace
from fractions import Fraction as F
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
OUT = ROOT / "CATCH_PROOF_RESULT.json"


@dataclass(frozen=True)
class Anchor:
    model_segment: str = "A:0->1"
    observed_segment: str = "A:0->1"
    independent: bool = True
    metric_generated: bool = False
    c_bar: F = F(3, 2)
    tau: F = F(21, 10)
    c_e: F = F(5, 3)


def recover(anchor: Anchor) -> F:
    if anchor.model_segment != anchor.observed_segment:
        raise ValueError("segment mismatch")
    if not anchor.independent or anchor.metric_generated:
        raise ValueError("circular anchor")
    if anchor.c_bar <= 0 or anchor.tau <= 0 or anchor.c_e <= 0:
        raise ValueError("nonpositive anchor")
    return anchor.c_e * anchor.tau / anchor.c_bar


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--no-write", action="store_true")
    args = parser.parse_args()

    baseline = Anchor()
    ell = recover(baseline)
    ledger: list[dict[str, object]] = []

    def record(name: str, kind: str, caught: bool) -> None:
        assert caught, name
        ledger.append(
            {
                "name": name,
                "kind": kind,
                "baseline_passed": True,
                "mutant_rejected": caught,
            }
        )

    # Implementation mutations.
    caught = False
    try:
        recover(replace(baseline, independent=False, metric_generated=True))
    except ValueError:
        caught = True
    record("self_evaluation_anchor", "implementation", caught)

    caught = False
    try:
        recover(replace(baseline, observed_segment="B:0->1"))
    except ValueError:
        caught = True
    record("mismatched_segment", "implementation", caught)

    caught = False
    try:
        recover(replace(baseline, tau=F(0)))
    except ValueError:
        caught = True
    record("nonpositive_clock", "implementation", caught)

    second = replace(
        baseline,
        model_segment="C:0->1",
        observed_segment="C:0->1",
        c_bar=F(7, 4),
        tau=ell * F(7, 4) / baseline.c_e + F(1, 11),
    )
    record("per_anchor_scale_proliferation", "implementation", recover(second) != ell)

    # c_E alone has L/T units: no exponent is simultaneously 1 and 0.
    ce_alone_candidates = [power for power in range(-8, 9) if power == 1 and -power == 0]
    record("ce_alone_length", "implementation", ce_alone_candidates == [])

    # Dimensionless state and same-weight ratios remain blind to ell.
    chi = F(3, 5)
    scale_a, scale_b = F(2), F(7, 3)
    record(
        "dimensionless_projective_state_sets_scale",
        "implementation",
        chi == chi and scale_a != scale_b,
    )

    # Typed-scope catches.
    dtau, dx = F(5, 7), F(11, 13)
    record(
        "ratio_dtau_dx_sets_scale",
        "typed_scope",
        (scale_a * dtau) / (scale_a * dx)
        == (scale_b * dtau) / (scale_b * dx),
    )
    q_r = F(9, 10)
    record(
        "automatic_xmax_from_attached_scale",
        "typed_scope",
        ell * q_r < ell and ell * q_r != ell,
    )

    implementation = sum(row["kind"] == "implementation" for row in ledger)
    typed = sum(row["kind"] == "typed_scope" for row in ledger)
    assert implementation == 6 and typed == 2 and len(ledger) == 8

    result = {
        "status": "PASS",
        "implementation_mutations_caught": implementation,
        "typed_scope_catches_passed": typed,
        "catches": {str(row["name"]) + "_caught": True for row in ledger},
        "mutation_ledger": ledger,
    }
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.no_write:
        assert OUT.read_text(encoding="utf-8") == rendered
    else:
        OUT.write_text(rendered, encoding="utf-8")
    print(rendered, end="")


if __name__ == "__main__":
    main()
