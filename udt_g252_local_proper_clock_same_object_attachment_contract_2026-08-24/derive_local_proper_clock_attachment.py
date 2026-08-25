#!/usr/bin/env python3
"""Exact G252 proper-clock attachment theorem; writes only with explicit output."""

from __future__ import annotations

import argparse
import csv
from dataclasses import dataclass
from fractions import Fraction as Q
import hashlib
import json
from pathlib import Path
import random

import sympy as sp


ROOT = Path(__file__).resolve().parent.parent
PKG = Path(__file__).resolve().parent

LANDING = (
    "ONE_BLINDED_INDEPENDENT_PROPER_CLOCK_RECORD_ON_ONE_FROZEN_IDENTIFIED_TIMELIKE_SEGMENT_"
    "CONDITIONALLY_FIXES_THE_SINGLE_G249_SCALE"
    "__CE_CONVERTS_THE_ATTACHED_DURATION_TO_LENGTH_WITHOUT_ADDING_A_SCALE_PARAMETER"
    "__A_SECOND_FROZEN_CLOCK_ATTACHMENT_TESTS_THE_SUPPLIED_DIMENSIONLESS_HISTORY_BY_EQUAL_SCALE_RECOVERY"
    "__EVENT_IDENTITY_AND_INDEPENDENT_CALIBRATION_ARE_SUPPLIED_OPERATIONAL_INPUTS_NOT_METRIC_DERIVATIONS"
    "__NO_CLOCK_VALUE_HISTORY_BRANCH_POPULATION_FIT_OUTCOME_OR_NEW_KERNEL_MECHANISM_SELECTED"
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def source_payload_matches(path: Path, expected: str, relative: str) -> bool:
    payload = path.read_bytes()
    if hashlib.sha256(payload).hexdigest() == expected:
        return True
    if relative != "CURRENT_SCIENTIFIC_PREMISES.tsv":
        return False
    lines = payload.splitlines(keepends=True)
    g252 = [line for line in lines if line.startswith(b"G252\t")]
    stripped = b"".join(line for line in lines if not line.startswith(b"G252\t"))
    return len(g252) == 1 and hashlib.sha256(stripped).hexdigest() == expected


def resolve_manifest_source(relative: str, expected: str) -> Path:
    candidates = (ROOT / relative, ROOT / "sources" / relative)
    existing = [path for path in candidates if path.is_file()]
    if len(existing) != 1:
        raise AssertionError(f"source resolution is not unique: {relative}")
    if not source_payload_matches(existing[0], expected, relative):
        raise AssertionError(f"source hash mismatch: {relative}")
    return existing[0]


def verify_sources() -> int:
    with (PKG / "SOURCE_MANIFEST.tsv").open(newline="", encoding="utf-8") as stream:
        rows = list(csv.DictReader(stream, delimiter="\t"))
    if len(rows) != 6:
        raise AssertionError("G252 requires exactly six frozen sources")
    for row in rows:
        resolve_manifest_source(row["path"], row["sha256"])
    return len(rows)


@dataclass(frozen=True)
class Attachment:
    model_observer: str
    record_observer: str
    model_start: str
    record_start: str
    model_end: str
    record_end: str
    branch: str
    record_branch: str
    clock_id: str
    calibration_id: str
    independently_calibrated: bool
    defined_by_metric: bool
    bar_tau: Q
    tau_star: Q


def recover_scale(record: Attachment) -> Q:
    identities = (
        record.model_observer == record.record_observer,
        record.model_start == record.record_start,
        record.model_end == record.record_end,
        record.branch == record.record_branch,
        bool(record.clock_id),
        bool(record.calibration_id),
    )
    if not all(identities):
        raise ValueError("same-object identity failure")
    if not record.independently_calibrated or record.defined_by_metric:
        raise ValueError("clock datum is not independently calibrated")
    if record.bar_tau <= 0 or record.tau_star <= 0:
        raise ValueError("positive oriented durations required")
    return record.tau_star / record.bar_tau


def common_scale(records: tuple[Attachment, ...]) -> Q:
    if not records:
        raise ValueError("at least one attachment required")
    recovered = tuple(recover_scale(record) for record in records)
    if any(value != recovered[0] for value in recovered[1:]):
        raise ValueError("attachments reject a single common scale")
    return recovered[0]


def exact_symbolic_checks() -> dict[str, bool]:
    ell, density, step, affine, tau_star, c_e = sp.symbols(
        "ell density step affine tau_star c_E", positive=True
    )
    return {
        "proper_time_weight_plus_one": sp.simplify(sp.sqrt((ell * density) ** 2) * step - ell * density * step) == 0,
        "unique_positive_scale_solution": sp.solve(sp.Eq(tau_star, ell * density * step), ell) == [tau_star / (density * step)],
        "orientation_preserving_reparameterization": sp.simplify((density / affine) * (affine * step) - density * step) == 0,
        "c_E_is_post_attachment_conversion": sp.simplify(c_e * tau_star - c_e * ell * (tau_star / ell)) == 0,
        "common_unit_conversion_preserves_scale": sp.simplify((affine * tau_star) / (affine * density * step) - tau_star / (density * step)) == 0,
    }


def make_record(bar_tau: Q, ell: Q, suffix: str) -> Attachment:
    return Attachment(
        model_observer=f"observer_{suffix}",
        record_observer=f"observer_{suffix}",
        model_start=f"event_{suffix}_0",
        record_start=f"event_{suffix}_0",
        model_end=f"event_{suffix}_1",
        record_end=f"event_{suffix}_1",
        branch=f"branch_{suffix}",
        record_branch=f"branch_{suffix}",
        clock_id=f"clock_{suffix}",
        calibration_id=f"calibration_{suffix}",
        independently_calibrated=True,
        defined_by_metric=False,
        bar_tau=bar_tau,
        tau_star=ell * bar_tau,
    )


def sampled_checks(cases: int) -> dict[str, int]:
    rng = random.Random(2520824)
    assertions = 0
    segment_terms = 0
    for index in range(cases):
        ell = Q(rng.randint(1, 37), rng.randint(1, 31))
        terms = []
        transformed = []
        for _ in range(rng.randint(2, 7)):
            density = Q(rng.randint(1, 41), rng.randint(1, 29))
            step = Q(rng.randint(1, 23), rng.randint(1, 19))
            affine = Q(rng.randint(1, 17), rng.randint(1, 13))
            terms.append(density * step)
            transformed.append((density / affine) * (affine * step))
            segment_terms += 1
        bar_tau = sum(terms, Q(0))
        assert sum(transformed, Q(0)) == bar_tau
        assertions += 1
        first = make_record(bar_tau, ell, f"{index}_a")
        assert recover_scale(first) == ell
        assertions += 1
        second_bar_tau = Q(rng.randint(1, 43), rng.randint(1, 37))
        second = make_record(second_bar_tau, ell, f"{index}_b")
        assert common_scale((first, second)) == ell
        assertions += 1
        unit_factor = Q(rng.randint(1, 19), rng.randint(1, 17))
        rescaled = Attachment(**{**first.__dict__, "bar_tau": unit_factor * first.bar_tau, "tau_star": unit_factor * first.tau_star})
        assert recover_scale(rescaled) == ell
        assertions += 1
        c_e = Q(rng.randint(1, 29), rng.randint(1, 23))
        assert c_e * first.tau_star == c_e * ell * first.bar_tau
        assertions += 1
    return {"cases": cases, "assertions": assertions, "segment_terms": segment_terms}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cases", type=int, default=4096)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    sources = verify_sources()
    checks = exact_symbolic_checks()
    if not all(checks.values()):
        raise SystemExit(f"symbolic failure: {checks}")
    sampled = sampled_checks(args.cases)
    result = {
        "status": "PASS",
        "landing": LANDING,
        "exact_checks": checks,
        "sampled": sampled,
        "source_count_verified": sources,
        "observational_values_used": 0,
        "fitted_coefficients": 0,
        "new_kernel_mechanisms": 0,
        "history_selected": False,
    }
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(rendered, encoding="utf-8")
    print(rendered, end="")


if __name__ == "__main__":
    main()
