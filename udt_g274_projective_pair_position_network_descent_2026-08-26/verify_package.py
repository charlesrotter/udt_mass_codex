#!/usr/bin/env python3
"""Verify G274 source freeze, evidence, replays, and bounded grade."""

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
    "FULL_PATH_LABELLED_FRAME_MORPHISMS_DESCEND_EXACTLY__"
    "PROJECTIVE_OPEN_BALL_VECTOR_IS_A_VALID_PAIR_COORDINATE_BUT_NOT_A_"
    "STANDALONE_NONRADIAL_COMPOSITION_LAW__SCREEN_FRAME_CARRY_IS_REQUIRED__"
    "RADIAL_MOBIUS_STRATUM_CLOSES__SCALE_HISTORY_BRANCH_POPULATION_AND_XMAX_REMAIN_OPEN"
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
    assert len(sources) == 11
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
        "PREREGISTRATION_EXECUTION_NOTE.md",
        "RUN_RECORD.md",
        "SOURCE_MANIFEST.tsv",
        "STATUS_LEDGER.tsv",
        "build_review_intake.py",
        "derive_projective_network_descent.py",
        "run_catch_proofs.py",
        "verify_package.py",
        "verify_projective_network_independent.py",
    )
    for name in required:
        assert (ROOT / name).is_file(), name

    production = json.loads((ROOT / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    independent = json.loads((ROOT / "INDEPENDENT_VERIFICATION.json").read_text(encoding="utf-8"))
    catches = json.loads((ROOT / "CATCH_PROOF_RESULT.json").read_text(encoding="utf-8"))
    assert production["status"] == independent["status"] == catches["status"] == "PASS"
    assert production["landing"] == independent["landing"] == LANDING
    assert production["selected_alternative"] == (
        "B__FULL_FRAME_MORPHISM_DESCENDS__PROJECTIVE_VECTOR_REQUIRES_CARRY__"
        "RADIAL_MOBIUS_EXACT"
    )
    assert production["exact_checks"] == 26 and all(production["checks"].values())
    assert independent["production_imported"] is False
    assert independent["cases"] == 20_000
    assert independent["exact_assertions"] == 240_004
    assert independent["active_screen_cases"] == 20_000
    assert independent["vector_only_separators"] == 20_000
    assert independent["collinear_mobius_controls"] == 20_000
    assert independent["overlap_covariance_controls"] == 20_000
    assert catches["implementation_mutations_caught"] == 5
    assert catches["typed_scope_catches_passed"] == 1

    replay("derive_projective_network_descent.py")
    replay("verify_projective_network_independent.py")
    replay("run_catch_proofs.py")

    report = (ROOT / "AUDIT_REPORT.md").read_text(encoding="utf-8")
    assert "INTERNALLY_VERIFIED_LEAD__EXTERNAL_REVIEW_OPEN" in report
    forbidden_promotions = (
        "position clarification is adopted",
        "dimensionful scale is derived",
        "history is selected",
        "X_max is derived",
        "path independence is derived",
    )
    assert not any(token in report for token in forbidden_promotions)

    result = {
        "status": "PASS",
        "landing": LANDING,
        "source_rows": len(sources),
        "source_paths_within_scope_root": len(sources),
        "production_checks": 26,
        "independent_cases": 20_000,
        "independent_exact_assertions": 240_004,
        "active_screen_cases": 20_000,
        "vector_only_separators": 20_000,
        "collinear_mobius_controls": 20_000,
        "overlap_covariance_controls": 20_000,
        "implementation_mutations_caught": 5,
        "typed_scope_catches_passed": 1,
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
