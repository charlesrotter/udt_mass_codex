#!/usr/bin/env python3
"""No-write verifier for the pre-review G248 evidence package."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
PKG = Path(__file__).resolve().parent
LANDING = (
    "METRIC_OWNS_ORDERED_REGULAR_INCIDENCE_COAREA_DENSITY_R_OVER_A"
    "__SKY_PHASE_COUNTING_AND_INCIDENCE_MEASURES_ARE_DISTINCT_TYPED_OBJECTS"
    "__CSP4_COMPOSITION_LEAVES_REAL_CHARACTER_FAMILY_R_TO_ALPHA"
    "__UNIVERSAL_PHYSICAL_BRANCH_MEASURE_SOURCE_POPULATION_AND_CRITICAL_COMPLETION_REMAIN_OPEN"
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def matches_frozen_source(path: Path, expected: str, relative: str) -> bool:
    if sha256(path) == expected:
        return True
    if relative != "CURRENT_SCIENTIFIC_PREMISES.tsv":
        return False
    lines = path.read_bytes().splitlines(keepends=True)
    rows = [i for i, line in enumerate(lines) if line.startswith(b"G248\t")]
    if len(rows) != 1:
        return False
    historical = b"".join(line for i, line in enumerate(lines) if i != rows[0])
    return hashlib.sha256(historical).hexdigest() == expected


def replay(script: str, *args: str) -> dict:
    environment = dict(os.environ)
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    completed = subprocess.run(
        [sys.executable, str(PKG / script), *args],
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
        "VERIFICATION_RESULT.json",
        "derive_regular_branch_measure.py", "verify_regular_branch_measure_independent.py",
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

    saved_prod = json.loads((PKG / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    saved_ind = json.loads((PKG / "INDEPENDENT_VERIFICATION.json").read_text(encoding="utf-8"))
    saved_catch = json.loads((PKG / "CATCH_PROOF_RESULT.json").read_text(encoding="utf-8"))
    live_prod = replay("derive_regular_branch_measure.py", "--cases", "4096")
    live_ind = replay("verify_regular_branch_measure_independent.py", "--cases", "10000")
    live_catch = replay("run_catch_proofs.py")
    checks = {
        "source_manifest_rows": len(rows) == 11,
        "saved_production_pass": saved_prod.get("status") == "PASS",
        "saved_independent_pass": saved_ind.get("status") == "PASS",
        "saved_catch_pass": saved_catch.get("status") == "PASS",
        "production_landing": saved_prod.get("landing") == LANDING,
        "independent_landing": saved_ind.get("expected_landing") == LANDING,
        "production_replay_exact": live_prod == saved_prod,
        "independent_replay_exact": live_ind == saved_ind,
        "catch_replay_exact": live_catch == saved_catch,
        "production_floor": saved_prod.get("cases", 0) >= 4096
        and saved_prod.get("assertions", 0) >= 40000,
        "independent_floor": saved_ind.get("cases", 0) >= 10000
        and saved_ind.get("assertions", 0) >= 100000,
        "hostile_floor": saved_catch.get("caught", 0) >= 16
        and saved_catch.get("caught") == saved_catch.get("total"),
        "outcomes_closed": saved_prod.get("observational_outcomes") == "CLOSED_AND_UNREAD"
        and saved_ind.get("observational_outcomes") == "CLOSED_AND_UNREAD",
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
