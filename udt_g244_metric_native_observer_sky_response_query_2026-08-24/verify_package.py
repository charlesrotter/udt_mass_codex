#!/usr/bin/env python3
"""Package replay and cross-route checks for G244."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path


PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parent
EXPECTED = (
    "METRIC_NATIVE_OBSERVER_SKY_AREA_SHAPE_QUERY_DERIVED_CONDITIONALLY"
    "__NO_FITTED_ANGULAR_COEFFICIENT"
    "__CATALOG_IDENTIFICATION_AND_HISTORY_OPEN"
)
OUTPUT = PACKAGE / "VERIFICATION_RESULT.json"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def preregistration_registry_digest(path: Path) -> str:
    """Recover the exact pre-G244 registry after the single append-only self row."""
    lines = path.read_bytes().splitlines(keepends=True)
    self_rows = [line for line in lines if line.startswith(b"G244\t")]
    if len(self_rows) != 1:
        raise RuntimeError("live registry must contain exactly one banked G244 row")
    historical = b"".join(line for line in lines if not line.startswith(b"G244\t"))
    return hashlib.sha256(historical).hexdigest()


def replay(script: str) -> dict[str, object]:
    process = subprocess.run(
        [sys.executable, str(PACKAGE / script), "--no-write"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return json.loads(process.stdout)


def verify_sources() -> int:
    lines = (PACKAGE / "SOURCE_MANIFEST.tsv").read_text(encoding="utf-8").splitlines()
    if lines[0] != "sha256\tpath\trole":
        raise RuntimeError("invalid source manifest header")
    checked = 0
    for line in lines[1:]:
        expected, relative, _role = line.split("\t")
        source = ROOT / relative
        actual = sha256(source)
        if relative == "CURRENT_SCIENTIFIC_PREMISES.tsv" and actual != expected:
            actual = preregistration_registry_digest(source)
        if actual != expected:
            raise RuntimeError(f"source hash mismatch: {relative}")
        checked += 1
    return checked


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--no-write", action="store_true")
    args = parser.parse_args()

    source_count = verify_sources()
    saved_production = json.loads((PACKAGE / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    saved_independent = json.loads((PACKAGE / "INDEPENDENT_VERIFICATION.json").read_text(encoding="utf-8"))
    saved_catches = json.loads((PACKAGE / "CATCH_PROOF_RESULT.json").read_text(encoding="utf-8"))
    replay_production = replay("derive_metric_native_sky_query.py")
    replay_independent = replay("verify_metric_native_sky_query_independent.py")
    replay_catches = replay("run_catch_proofs.py")

    checks = {
        "source_manifest": source_count == 8,
        "production_classification": saved_production["classification"] == EXPECTED,
        "independent_classification": saved_independent["classification"] == EXPECTED,
        "production_replay_exact": replay_production == saved_production,
        "independent_replay_exact": replay_independent == saved_independent,
        "catch_replay_exact": replay_catches == saved_catches,
        "cross_route_area_query": (
            saved_production["area_query_witness"]["projected_w"]["exact"]
            == saved_independent["area_query_w"]["exact"]
            == "-1/6"
        ),
        "cross_route_constant_cancellation": (
            saved_production["area_query_witness"]["constant_area_w"]["exact"]
            == saved_independent["constant_area_w"]["exact"]
            == "0/1"
        ),
        "no_fit": (
            saved_production["fitted_angular_coefficients"] == 0
            and saved_independent["fitted_angular_coefficients"] == 0
        ),
        "outcomes_closed": (
            saved_production["observational_outcomes"] == "CLOSED_AND_UNREAD"
            and saved_independent["observational_outcomes"] == "CLOSED_AND_UNREAD"
        ),
        "no_caustic_inverse": (
            saved_production["caustic_boundary"]["position_inverse_used"] is False
            and saved_independent["caustic_position_inverse_used"] is False
        ),
        "full_phase_nonmultiplicative": (
            saved_production["phase_census"]["nonmultiplicative_position_cases"] > 0
            and saved_independent["nonmultiplicative_position_cases"] > 0
        ),
        "hostile_catches": saved_catches["status"] == "PASS" and all(saved_catches["checks"].values()),
    }
    if not all(checks.values()):
        raise RuntimeError(f"G244 package failure: {checks}")
    result = {
        "status": "PASS",
        "classification": EXPECTED,
        "source_count": source_count,
        "checks": checks,
        "production_matrix_cases": saved_production["matrix_census"]["cases"],
        "independent_matrix_cases": saved_independent["matrix_cases"],
        "production_phase_cases": saved_production["phase_census"]["cases"],
        "independent_phase_cases": saved_independent["phase_cases"],
        "hostile_catches": saved_catches["caught"],
    }
    rendered = json.dumps(result, indent=2, sort_keys=True)
    if not args.no_write:
        OUTPUT.write_text(rendered + "\n", encoding="utf-8")
    print(rendered)


if __name__ == "__main__":
    main()
