#!/usr/bin/env python3
"""Verify G271 sources, evidence, no-write replays, and bounded landing."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parent
REPO = ROOT.parent
OUT = ROOT / "VERIFICATION_RESULT.json"
LANDING = (
    "NATIVE_LONGITUDINAL_TRANSVERSE_FIRST_JET_SPLIT__"
    "ONE_PRIMARY_METRIC_GRADIENT_GENERATES_DEPTH_AND_TRANSPORTED_SCREEN_CHANNELS__"
    "RADIAL_AND_QUIET_STRATA_EXACT__NO_FINITE_PATH_HISTORY_DISTANCE_OR_XMAX_SELECTION"
)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def replay(script: str) -> None:
    completed = subprocess.run(
        [sys.executable, str(ROOT / script), "--no-write"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    assert completed.returncode == 0, completed.stdout + completed.stderr


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--no-write", action="store_true")
    args = parser.parse_args()

    with (ROOT / "SOURCE_MANIFEST.tsv").open(newline="", encoding="utf-8") as stream:
        sources = list(csv.DictReader(stream, delimiter="\t"))
    assert len(sources) == 5
    for row in sources:
        path = REPO / row["path"]
        assert path.is_file(), row["path"]
        assert digest(path) == row["sha256"], row["path"]

    required = (
        "AUDIT_REPORT.md",
        "CATCH_PROOF_RESULT.json",
        "COMMANDS.md",
        "DERIVATION_RESULT.json",
        "EVIDENCE_GATES.md",
        "EXACT_DERIVATION.md",
        "INDEPENDENT_VERIFICATION.json",
        "LAY_REPORT.md",
        "MAP.md",
        "PREMISE_LEDGER.tsv",
        "PREREGISTRATION.md",
        "RUN_RECORD.md",
        "SOURCE_MANIFEST.tsv",
        "STATUS_LEDGER.tsv",
        "derive_first_jet_interlock.py",
        "run_catch_proofs.py",
        "verify_first_jet_independent.py",
        "verify_package.py",
    )
    for name in required:
        assert (ROOT / name).is_file(), name

    production = json.loads((ROOT / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    independent = json.loads((ROOT / "INDEPENDENT_VERIFICATION.json").read_text(encoding="utf-8"))
    catches = json.loads((ROOT / "CATCH_PROOF_RESULT.json").read_text(encoding="utf-8"))
    assert production["status"] == independent["status"] == catches["status"] == "PASS"
    assert production["landing"] == independent["landing"] == LANDING
    assert production["selected_alternative"] == (
        "C__NATIVE_LONGITUDINAL_TRANSVERSE_FIRST_JET_SPLIT"
    )
    assert production["exact_checks"] == 30 and all(production["checks"].values())
    assert independent["exact_fraction_cases"] == 20000
    assert independent["production_imported"] is False
    assert catches["implementation_mutations_caught"] == 6
    assert catches["typed_conclusion_catches_passed"] == 6

    replay("derive_first_jet_interlock.py")
    replay("verify_first_jet_independent.py")
    replay("run_catch_proofs.py")

    report = (ROOT / "AUDIT_REPORT.md").read_text(encoding="utf-8")
    forbidden_promotions = (
        "physical history selected",
        "X_max derived",
        "distance law derived",
        "canonized",
    )
    assert not any(token in report for token in forbidden_promotions)
    assert "INTERNALLY_VERIFIED_LEAD__EXTERNAL_REVIEW_OPEN" in report

    result = {
        "status": "PASS",
        "landing": LANDING,
        "source_rows": len(sources),
        "production_checks": 30,
        "independent_exact_fraction_cases": 20000,
        "implementation_mutations_caught": 6,
        "typed_conclusion_catches_passed": 6,
        "no_write_replays": 3,
        "grade": "INTERNALLY_VERIFIED_LEAD__EXTERNAL_REVIEW_OPEN",
    }
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.no_write:
        assert OUT.read_text(encoding="utf-8") == rendered
    else:
        OUT.write_text(rendered, encoding="utf-8")
    print(rendered, end="")


if __name__ == "__main__":
    main()
