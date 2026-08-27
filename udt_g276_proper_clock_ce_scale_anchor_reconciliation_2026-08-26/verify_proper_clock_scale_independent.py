#!/usr/bin/env python3
"""Independent exact-rational G276 census; imports no production code/output."""

from __future__ import annotations

import argparse
from dataclasses import dataclass, replace
from fractions import Fraction as F
import json
from pathlib import Path
import random


ROOT = Path(__file__).resolve().parent
OUT = ROOT / "INDEPENDENT_VERIFICATION.json"
CASES = 20_000
LANDING = (
    "ONE_INDEPENDENT_SAME_SEGMENT_PROPER_CLOCK_RECORD_HAS_HOMOTHETY_WEIGHT_PLUS_ONE__"
    "CE_CARRIES_THE_ATTACHED_TIME_TO_A_UNIQUE_LENGTH_SCALE__"
    "CE_ALONE_DIMENSIONLESS_PROJECTIVE_STATE_AND_SELF_EVALUATION_ARE_SCALE_BLIND__"
    "NO_HISTORY_DISTANCE_PROTOCOL_OR_XMAX_SELECTED"
)


@dataclass(frozen=True)
class Record:
    model_segment: str
    observed_segment: str
    clock_id: str
    calibration_id: str
    independent: bool
    metric_generated: bool
    c_bar: F
    tau_star: F
    c_e: F


def recover(record: Record) -> F:
    if record.model_segment != record.observed_segment:
        raise ValueError("same-segment identity required")
    if not record.clock_id or not record.calibration_id:
        raise ValueError("identified calibration required")
    if not record.independent or record.metric_generated:
        raise ValueError("independent record required")
    if record.c_bar <= 0 or record.tau_star <= 0 or record.c_e <= 0:
        raise ValueError("positive clock quantities required")
    return record.c_e * record.tau_star / record.c_bar


def common_scale(records: tuple[Record, ...]) -> F:
    if not records:
        raise ValueError("at least one record required")
    values = tuple(recover(record) for record in records)
    if any(value != values[0] for value in values[1:]):
        raise ValueError("records reject one common scale")
    return values[0]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--no-write", action="store_true")
    args = parser.parse_args()

    rng = random.Random(2760826)
    assertions = 0
    inconsistent_records_rejected = 0
    self_evaluations_rejected = 0
    same_segment_mismatches_rejected = 0

    def require(condition: bool) -> None:
        nonlocal assertions
        assertions += 1
        assert condition

    for index in range(CASES):
        ell = F(rng.randint(1, 53), rng.randint(1, 47))
        c_e = F(rng.randint(1, 43), rng.randint(1, 37))
        c_bar = F(rng.randint(1, 41), rng.randint(1, 31))
        tau_star = ell * c_bar / c_e
        name = f"segment_{index}"
        first = Record(
            model_segment=name,
            observed_segment=name,
            clock_id=f"clock_{index}",
            calibration_id=f"cal_{index}",
            independent=True,
            metric_generated=False,
            c_bar=c_bar,
            tau_star=tau_star,
            c_e=c_e,
        )
        require(recover(first) == ell)
        require(c_e * tau_star == ell * c_bar)

        second_bar = F(rng.randint(1, 59), rng.randint(1, 49))
        second = replace(
            first,
            model_segment=f"second_{index}",
            observed_segment=f"second_{index}",
            c_bar=second_bar,
            tau_star=ell * second_bar / c_e,
        )
        require(recover(second) == ell)
        require(common_scale((first, second)) == ell)

        inconsistent = replace(second, tau_star=second.tau_star + F(1, 97))
        try:
            common_scale((first, inconsistent))
        except ValueError:
            inconsistent_records_rejected += 1
        require(inconsistent_records_rejected == index + 1)

        self_record = replace(first, independent=False, metric_generated=True)
        try:
            recover(self_record)
        except ValueError:
            self_evaluations_rejected += 1
        require(self_evaluations_rejected == index + 1)

        mismatch = replace(first, observed_segment=f"wrong_{index}")
        try:
            recover(mismatch)
        except ValueError:
            same_segment_mismatches_rejected += 1
        require(same_segment_mismatches_rejected == index + 1)

        # Rational hyperbolic half-angle chart: chi=tanh(delta), M=sech(delta).
        t = F(rng.randint(-19, 19), rng.randint(21, 47))
        chi = 2 * t / (1 + t * t)
        mutual = (1 - t * t) / (1 + t * t)
        require(mutual * mutual + chi * chi == 1)
        require(abs(chi) < 1)
        position = ell * chi
        require(position == c_e * tau_star * chi / c_bar)
        require(position / ell == chi)

        homothety = F(rng.randint(1, 31), rng.randint(1, 29))
        dtau_bar = F(rng.randint(1, 37), rng.randint(1, 23))
        dx_bar = F(rng.randint(1, 47), rng.randint(1, 31))
        require((homothety * dtau_bar) / (homothety * dx_bar) == dtau_bar / dx_bar)
        require(ell * F(9, 10) < ell)
        require(ell * F(9, 10) != ell)

        # Physically faithful numeric unit relabelling. C_bar is dimensionless
        # and fixed; c_E, tau_star, and the reported length scale transform.
        length_unit = F(rng.randint(1, 17), rng.randint(1, 13))
        time_unit = F(rng.randint(1, 19), rng.randint(1, 11))
        unit_changed = replace(
            first,
            c_bar=first.c_bar,
            tau_star=time_unit * first.tau_star,
            c_e=(length_unit / time_unit) * first.c_e,
        )
        require(unit_changed.c_bar == first.c_bar)
        require(recover(unit_changed) == length_unit * ell)

    require(inconsistent_records_rejected == CASES)
    require(self_evaluations_rejected == CASES)
    require(same_segment_mismatches_rejected == CASES)

    result = {
        "status": "PASS",
        "landing": LANDING,
        "production_imported": False,
        "production_output_read": False,
        "arithmetic": "fractions.Fraction exact rational",
        "cases": CASES,
        "exact_assertions": assertions,
        "inconsistent_records_rejected": inconsistent_records_rejected,
        "self_evaluations_rejected": self_evaluations_rejected,
        "same_segment_mismatches_rejected": same_segment_mismatches_rejected,
        "observational_values_used": 0,
        "history_selected": False,
        "operational_distance_selected": False,
        "X_max_selected": False,
    }
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.no_write:
        assert OUT.read_text(encoding="utf-8") == rendered
    else:
        OUT.write_text(rendered, encoding="utf-8")
    print(rendered, end="")


if __name__ == "__main__":
    main()
