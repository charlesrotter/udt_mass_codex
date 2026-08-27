#!/usr/bin/env python3
"""Verify frozen sources, exact artifacts, and no-write G275 replays."""

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
PREREG_COMMIT = "c42da02d"
LANDING = (
    "W5_PROJECTIVE_POSITION_IS_HOMOTHETY_INVARIANT__"
    "ONE_MATCHED_NONZERO_WEIGHT_ANCHOR_FIXES_ONE_DIMENSIONAL_SCALE__"
    "DIMENSIONFUL_REPRESENTATIVE_RETAINS_FULL_FRAME_CARRY__"
    "XMAX_EQUALS_SCALE_ONLY_AFTER_SEPARATELY_OWNED_POPULATED_BOUNDARY_COMPLETION"
)
SEALED_REVIEW = (SCOPE_ROOT / "REVIEW_SCOPE.json").is_file()


def digest_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def verify_sealed_review_root() -> None:
    """Fail closed on exact nonrecursive manifest semantics inside a sealed intake."""

    if not SEALED_REVIEW:
        return
    scope_path = SCOPE_ROOT / "REVIEW_SCOPE.json"
    manifest_path = SCOPE_ROOT / "REVIEW_MANIFEST.tsv"
    assert manifest_path.is_file()
    scope = json.loads(scope_path.read_text(encoding="utf-8"))
    with manifest_path.open(newline="", encoding="utf-8") as stream:
        rows = list(csv.DictReader(stream, delimiter="\t"))
    physical = sorted(
        path.relative_to(SCOPE_ROOT).as_posix()
        for path in SCOPE_ROOT.rglob("*")
        if path.is_file()
    )
    listed = [row["path"] for row in rows]
    expected = sorted(path for path in physical if path != "REVIEW_MANIFEST.tsv")
    assert scope["file_count_including_scope_and_manifest"] == len(physical)
    assert scope["manifest_entry_count_excluding_manifest"] == len(rows)
    assert "except itself" in scope["manifest_semantics"]
    assert len(listed) == len(set(listed))
    assert sorted(listed) == expected
    for row in rows:
        candidate = (SCOPE_ROOT / row["path"]).resolve()
        assert candidate.is_relative_to(SCOPE_ROOT)
        payload = candidate.read_bytes()
        assert digest_bytes(payload) == row["sha256"]
        assert len(payload) == int(row["bytes"])


def frozen_source_bytes(relative: str, expected: str) -> bytes:
    """Resolve exact frozen bytes; a sealed intake may never fall back outside itself."""

    sealed = (ROOT / "sources" / relative).resolve()
    source_root = (ROOT / "sources").resolve()
    if SEALED_REVIEW:
        assert sealed.is_relative_to(source_root) and sealed.is_file(), relative
        payload = sealed.read_bytes()
        assert digest_bytes(payload) == expected, relative
        return payload

    live = (SCOPE_ROOT / relative).resolve()
    if live.is_relative_to(SCOPE_ROOT) and live.is_file():
        payload = live.read_bytes()
        if digest_bytes(payload) == expected:
            return payload
    if sealed.is_relative_to(source_root) and sealed.is_file():
        payload = sealed.read_bytes()
        if digest_bytes(payload) == expected:
            return payload
    completed = subprocess.run(
        ["git", "show", f"{PREREG_COMMIT}:{relative}"],
        cwd=SCOPE_ROOT,
        capture_output=True,
        check=False,
    )
    assert completed.returncode == 0, relative
    assert digest_bytes(completed.stdout) == expected, relative
    return completed.stdout


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

    verify_sealed_review_root()

    with (ROOT / "SOURCE_MANIFEST.tsv").open(newline="", encoding="utf-8") as stream:
        sources = list(csv.DictReader(stream, delimiter="\t"))
    assert len(sources) == 10
    for row in sources:
        frozen_source_bytes(row["path"], row["sha256"])

    required = (
        "ADVERSARIAL_REVIEW_REQUEST.md",
        "AUDIT_REPORT.md",
        "CATCH_PROOF_RESULT.json",
        "COMMANDS.md",
        "DERIVATION_RESULT.json",
        "EVIDENCE_GATES.md",
        "EXTERNAL_REVIEW.md",
        "EXACT_DERIVATION.md",
        "INDEPENDENT_VERIFICATION.json",
        "LAY_REPORT.md",
        "MAP.md",
        "PREMISE_LEDGER.tsv",
        "PREREGISTRATION.md",
        "PREREGISTRATION_EXECUTION_NOTE.md",
        "REPAIR_PREREGISTRATION.md",
        "REPAIR_FOLLOWUP_REVIEW.md",
        "REPAIR_RESULT.md",
        "REPAIR_VERIFICATION_RESULT.json",
        "SECOND_REPAIR_PREREGISTRATION.md",
        "SECOND_REPAIR_FOLLOWUP_REVIEW.md",
        "RUN_RECORD.md",
        "SOURCE_MANIFEST.tsv",
        "STATUS_LEDGER.tsv",
        "build_review_intake.py",
        "derive_projective_scale_attachment.py",
        "run_catch_proofs.py",
        "verify_package.py",
        "verify_review_repairs.py",
        "verify_scale_attachment_independent.py",
    )
    for name in required:
        assert (ROOT / name).is_file(), name

    production = json.loads((ROOT / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    independent = json.loads((ROOT / "INDEPENDENT_VERIFICATION.json").read_text(encoding="utf-8"))
    catches = json.loads((ROOT / "CATCH_PROOF_RESULT.json").read_text(encoding="utf-8"))
    assert production["status"] == independent["status"] == catches["status"] == "PASS"
    assert production["landing"] == independent["landing"] == LANDING
    assert production["selected_alternative"] == (
        "B__ONE_POSITIVE_HOMOTHETY_SURVIVES__ONE_NONZERO_WEIGHT_ANCHOR_FIXES_IT"
    )
    assert production["exact_checks"] == 26 and all(production["checks"].values())
    assert independent["production_imported"] is False
    assert independent["production_output_read"] is False
    assert independent["cases"] == 20_000
    assert independent["exact_assertions"] == 340_006
    assert independent["active_screen_cases"] == 20_000
    assert independent["carry_separators"] == 20_000
    assert independent["positive_weight_cases"] > 0
    assert independent["negative_weight_cases"] > 0
    assert independent["finite_domain_controls"] == 20_000
    assert independent["boundary_approach_controls"] == 20_000
    assert independent["empty_population_control"] is True
    assert independent["zero_state_population_control"] is True
    assert catches["implementation_mutations_caught"] == 6
    assert catches["typed_scope_catches_passed"] == 2
    assert len(catches["mutation_ledger"]) == 8
    assert all(row["baseline_passed"] and row["mutant_rejected"] for row in catches["mutation_ledger"])

    replay("derive_projective_scale_attachment.py")
    replay("verify_scale_attachment_independent.py")
    replay("run_catch_proofs.py")

    report = (ROOT / "AUDIT_REPORT.md").read_text(encoding="utf-8")
    assert "EXTERNALLY_REVIEWED__R4_ACCEPTED__SCIENTIFIC_LANDING_UNCHANGED" in report
    assert "not automatically `X_max`" in report
    assert "full frame-carry requirement" in report
    forbidden = (
        "X_max is derived",
        "history is selected",
        "the anchor is native",
        "path independence is derived",
        "W5 is canon",
    )
    assert not any(token in report for token in forbidden)

    result = {
        "status": "PASS",
        "landing": LANDING,
        "source_rows": len(sources),
        "production_checks": 26,
        "independent_cases": 20_000,
        "independent_exact_assertions": 340_006,
        "active_screen_cases": 20_000,
        "carry_separators": 20_000,
        "implementation_mutations_caught": 6,
        "typed_scope_catches_passed": 2,
        "no_write_replays": 3,
        "grade": "EXTERNALLY_REVIEWED__R4_ACCEPTED__SCIENTIFIC_LANDING_UNCHANGED",
    }
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.no_write:
        assert OUT.read_text(encoding="utf-8") == rendered
    else:
        OUT.write_text(rendered, encoding="utf-8")
    print(rendered, end="")


if __name__ == "__main__":
    main()
