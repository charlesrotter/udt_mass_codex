#!/usr/bin/env python3
"""Fail-closed G262 package and frozen-source consistency verifier."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import subprocess
from pathlib import Path


PREREG_COMMIT = "fdd18b9b"
LANDING = (
    "ONE_METRIC_STATE_HIERARCHY_DERIVED"
    "__COVECTOR_ENERGY_PAIRING_CONDITIONAL"
    "__LOCAL_REST_MASS_PHYSICAL_TOTAL_MASS_XMAX_VALUE_AND_HISTORY_LAW_OPEN"
)


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def read_frozen(repo: Path, relative: str, expected: str) -> tuple[bytes, str]:
    live = repo / relative
    if live.is_file():
        data = live.read_bytes()
        if digest(data) == expected:
            return data, "live_exact"
    try:
        frozen = subprocess.check_output(
            ["git", "show", f"{PREREG_COMMIT}:{relative}"], cwd=repo, stderr=subprocess.DEVNULL
        )
    except subprocess.CalledProcessError as exc:
        raise AssertionError(f"cannot resolve frozen source {relative}") from exc
    if digest(frozen) != expected:
        raise AssertionError(f"frozen source hash mismatch: {relative}")
    return frozen, "git_object_exact"


def resolve_frozen(repo: Path, relative: str, expected: str) -> str:
    return read_frozen(repo, relative, expected)[1]


def verify(package: Path) -> dict[str, object]:
    repo = package.parent
    with (package / "DERIVATION_RESULT.json").open(encoding="utf-8") as handle:
        derivation = json.load(handle)
    with (package / "INDEPENDENT_VERIFICATION.json").open(encoding="utf-8") as handle:
        independent = json.load(handle)
    with (package / "CATCH_PROOF_RESULT.json").open(encoding="utf-8") as handle:
        catches = json.load(handle)

    if derivation["landing"] != LANDING:
        raise AssertionError("landing mismatch")
    if derivation["symbolic_check_count"] != 19:
        raise AssertionError("symbolic count mismatch")
    if independent["status"] != "PASS" or independent["assertion_count"] != 10003:
        raise AssertionError("independent replay mismatch")
    if catches["status"] != "PASS" or catches["caught_count"] != 12:
        raise AssertionError("catch proof mismatch")

    with (package / "STATUS_LEDGER.tsv").open(newline="", encoding="utf-8") as handle:
        status = {row["id"]: row for row in csv.DictReader(handle, delimiter="\t")}
    if status["S06"]["status"] != "NOT_DERIVED":
        raise AssertionError("local rest mass was promoted")
    if status["S10"]["status"] != "OPEN":
        raise AssertionError("physical UDT mass was promoted")
    if status["S11"]["status"] != "OPEN":
        raise AssertionError("history law was promoted")
    if status["S12"]["status"] != "DERIVED_METRIC_LIMIT_PREEXISTING":
        raise AssertionError("raw wall flux ownership mismatch")
    if status["S13"]["status"] != "EXTERNAL_ACCEPT_WITH_REPAIRS":
        raise AssertionError("external repair status mismatch")

    resolutions: dict[str, str] = {}
    source_rows: dict[str, dict[str, str]] = {}
    with (package / "SOURCE_MANIFEST.tsv").open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle, delimiter="\t"):
            source_rows[row["path"]] = row
            resolutions[row["path"]] = resolve_frozen(repo, row["path"], row["sha256"])

    wall_path = "asymptotic_boundary_lineage_audit_2026-07-19/AUDIT_REPORT.md"
    wall_bytes, _ = read_frozen(repo, wall_path, source_rows[wall_path]["sha256"])
    wall_source = wall_bytes.decode("utf-8")
    if "raw wall lapse flux: `-2*pi*X`" not in wall_source:
        raise AssertionError("frozen raw wall flux source missing")
    if "a raw metric flux is not a mass" not in wall_source:
        raise AssertionError("frozen raw wall flux ownership guard missing")

    report = (package / "AUDIT_REPORT.md").read_text(encoding="utf-8")
    compact_report = report.replace("\n", "")
    required = (
        "local rest-mass dilation law",
        "normalized physical mass",
        "valued history",
        "\\Phi_{\\rm wall}=-2\\pi X",
        "not a native mass or charge",
        "runtime reran the dependency-free",
        "lacked SymPy",
    )
    if LANDING not in compact_report:
        raise AssertionError("report landing absent")
    for token in required:
        if token not in report:
            raise AssertionError(f"report token absent: {token}")

    return {
        "status": "PASS",
        "landing": LANDING,
        "source_count": len(resolutions),
        "source_resolutions": resolutions,
        "symbolic_checks": derivation["symbolic_check_count"],
        "independent_assertions": independent["assertion_count"],
        "mutation_catches": catches["caught_count"],
        "qualification": "package_consistency_and_frozen_source_gate_not_independent_scientific_derivation",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    package = Path(__file__).resolve().parent
    result = verify(package)
    encoded = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(encoded, encoding="utf-8")
    else:
        print(encoded, end="")


if __name__ == "__main__":
    main()
