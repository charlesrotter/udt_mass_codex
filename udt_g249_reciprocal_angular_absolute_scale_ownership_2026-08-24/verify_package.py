#!/usr/bin/env python3
"""No-write verifier for the bounded G249 evidence package."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parent.parent
PKG = Path(__file__).resolve().parent
LANDING = (
    "CE_AND_RECIPROCAL_REDSHIFT_FIX_DIMENSIONLESS_CLOCK_RATIOS_NOT_ABSOLUTE_LENGTH"
    "__POSITIVE_HOMOTHETY_PRESERVES_COMPLETE_DIMENSIONLESS_PHI_HISTORY_CAUSAL_STRUCTURE_AND_NORMALIZED_SHAPE_WHILE_JACOBI_AREA_SCALES_AS_LENGTH_SQUARED"
    "__PHI_VALUE_ALONE_DOES_NOT_FIX_NORMALIZED_ANGULAR_RESPONSE"
    "__FULL_DIMENSIONLESS_METRIC_AND_BRANCH_FIX_NORMALIZED_JACOBI_RESPONSE_CONDITIONALLY"
    "__ONE_INDEPENDENT_DIMENSIONFUL_ANCHOR_REMAINS_FOR_ABSOLUTE_SCALE"
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def matches_frozen_source(path: Path, expected: str, relative: str) -> bool:
    """Permit the append-only G249 registry row after integration."""
    if sha256(path) == expected:
        return True
    if relative != "CURRENT_SCIENTIFIC_PREMISES.tsv":
        return False
    lines = path.read_bytes().splitlines(keepends=True)
    rows = [index for index, line in enumerate(lines) if line.startswith(b"G249\t")]
    if len(rows) != 1 or not lines or not lines[0].startswith(b"premise_id\t"):
        return False
    historical = lines[0] + b"".join(lines[rows[0] + 1 :])
    return hashlib.sha256(historical).hexdigest() == expected


def replay(script: str, *arguments: str) -> dict:
    environment = dict(os.environ)
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    completed = subprocess.run(
        [sys.executable, str(PKG / script), *arguments],
        cwd=ROOT,
        env=environment,
        check=True,
        capture_output=True,
        text=True,
    )
    return json.loads(completed.stdout)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    required = [
        "MAP.md", "PREMISE_LEDGER.tsv", "PREREGISTRATION.md", "PREREGISTRATION_COMMIT.md",
        "SOURCE_MANIFEST.tsv", "EXACT_DERIVATION.md", "AUDIT_REPORT.md", "LAY_REPORT.md",
        "EVIDENCE_GATES.md", "STATUS_LEDGER.tsv", "COMMANDS.md", "REVIEW_REQUEST.md",
        "DERIVATION_RESULT.json", "INDEPENDENT_VERIFICATION.json", "CATCH_PROOF_RESULT.json",
        "derive_reciprocal_angular_scale.py", "verify_reciprocal_angular_scale_independent.py",
        "run_catch_proofs.py", "verify_package.py", "build_review_intake.py",
    ]
    missing = [name for name in required if not (PKG / name).is_file()]
    if missing:
        raise SystemExit(f"missing package files: {missing}")

    with (PKG / "SOURCE_MANIFEST.tsv").open(newline="", encoding="utf-8") as stream:
        rows = list(csv.DictReader(stream, delimiter="\t"))
    for row in rows:
        source = ROOT / row["path"]
        if not source.is_file() or not matches_frozen_source(source, row["sha256"], row["path"]):
            raise SystemExit(f"source freeze mismatch: {row['path']}")

    saved_production = json.loads((PKG / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    saved_independent = json.loads(
        (PKG / "INDEPENDENT_VERIFICATION.json").read_text(encoding="utf-8")
    )
    saved_catches = json.loads((PKG / "CATCH_PROOF_RESULT.json").read_text(encoding="utf-8"))
    live_production = replay("derive_reciprocal_angular_scale.py", "--cases", "4096")
    live_independent = replay(
        "verify_reciprocal_angular_scale_independent.py", "--cases", "10000"
    )
    live_catches = replay("run_catch_proofs.py")

    checks = {
        "source_manifest_rows": len(rows) == 9,
        "saved_production_pass": saved_production.get("status") == "PASS",
        "saved_independent_pass": saved_independent.get("status") == "PASS",
        "saved_catch_pass": saved_catches.get("status") == "PASS",
        "production_landing": saved_production.get("landing") == LANDING,
        "independent_landing": saved_independent.get("expected_landing") == LANDING,
        "production_replay_exact": live_production == saved_production,
        "independent_replay_exact": live_independent == saved_independent,
        "catch_replay_exact": live_catches == saved_catches,
        "production_floor": saved_production.get("cases", 0) >= 4096
        and saved_production.get("assertions", 0) >= 60000,
        "independent_floor": saved_independent.get("cases", 0) >= 10000
        and saved_independent.get("assertions", 0) >= 150000,
        "offdiagonal_floor": saved_production.get("offdiagonal_cases", 0) >= 3000
        and saved_independent.get("offdiagonal_cases", 0) >= 8000,
        "nonunit_scale_floor": saved_production.get("nonunit_scale_cases", 0) >= 3500
        and saved_independent.get("nonunit_scale_area_changes", 0) >= 9000,
        "hostile_floor": saved_catches.get("caught", 0) >= 20
        and saved_catches.get("caught") == saved_catches.get("total"),
        "outcomes_closed": saved_production.get("observational_outcomes") == "CLOSED_AND_UNREAD"
        and saved_independent.get("observational_outcomes") == "CLOSED_AND_UNREAD",
        "zero_fitted_coefficients": saved_production.get("fitted_coefficients") == 0,
    }
    failed = [name for name, value in checks.items() if not value]
    result = {"checks": checks, "failed": failed, "status": "PASS" if not failed else "FAIL"}
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    if failed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
