#!/usr/bin/env python3
"""Verify G272 sources, evidence, no-write replays, and bounded grade."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parent
SCOPE_ROOT = ROOT.parent.resolve()
OUT = ROOT / "VERIFICATION_RESULT.json"
LANDING = (
    "COMPLETE_METRIC_DERIVES_QUERY_RELATIVE_TRANSPORTED_RAPIDITY_STATE__"
    "PLANAR_TANH_DELTA_IS_EXACT_STRATUM__SCREEN_STATE_PREVENTS_DELTA_ONLY_COMPLETENESS__"
    "CONVENTIONAL_DISTANCE_SCALE_PROFILE_HISTORY_AND_XMAX_REMAIN_OPEN"
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
    assert len(sources) == 7
    for row in sources:
        path = (SCOPE_ROOT / row["path"]).resolve()
        assert path.is_relative_to(SCOPE_ROOT), row["path"]
        assert path.is_file(), row["path"]
        assert digest(path) == row["sha256"], row["path"]

    required = (
        "ADVERSARIAL_REVIEW_REQUEST.md",
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
        "derive_complete_relation_rapidity.py",
        "run_catch_proofs.py",
        "verify_complete_relation_independent.py",
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
        "B__COMPLETE_METRIC_DERIVES_QUERY_RELATIVE_RAPIDITY_STATE_ONLY"
    )
    assert production["exact_checks"] == 20 and all(production["checks"].values())
    assert independent["production_imported"] is False
    assert independent["cases"] == 24000
    assert independent["exact_assertions"] == 168530
    assert catches["implementation_mutations_caught"] == 5
    assert catches["typed_scope_catches_passed"] == 6

    replay("derive_complete_relation_rapidity.py")
    replay("verify_complete_relation_independent.py")
    replay("run_catch_proofs.py")

    report = (ROOT / "AUDIT_REPORT.md").read_text(encoding="utf-8")
    forbidden_promotions = (
        "physical distance derived",
        "X_max derived",
        "history selected",
        "canonized",
    )
    assert not any(token in report for token in forbidden_promotions)
    assert "INTERNALLY_VERIFIED_LEAD__EXTERNAL_REVIEW_OPEN" in report

    result = {
        "status": "PASS",
        "landing": LANDING,
        "source_rows": len(sources),
        "source_paths_within_scope_root": len(sources),
        "production_checks": 20,
        "independent_cases": 24000,
        "independent_exact_assertions": 168530,
        "implementation_mutations_caught": 5,
        "typed_scope_catches_passed": 6,
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
