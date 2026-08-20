#!/usr/bin/env python3
"""Live package verifier for G187, valid before and after external review."""

from __future__ import annotations

import ast
import hashlib
import json
from pathlib import Path
import subprocess
import sys


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
LANDING = (
    "FINITE_NONRADIAL_JACOBI_MAP_DERIVED_CONDITIONALLY"
    "__G186_LOCAL_SCREEN_SEEDS_TWO_METRIC_FIXED_MODES"
    "__NONRADIAL_SHEAR_EMERGES_WITHOUT_EXTRA_COEFFICIENT"
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def replay(name: str) -> dict:
    completed = subprocess.run(
        [sys.executable, str(HERE / name)],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    try:
        parsed = json.loads(completed.stdout)
    except json.JSONDecodeError:
        parsed = {}
    return {
        "returncode": completed.returncode,
        "status": parsed.get("status"),
        "stdout": completed.stdout,
        "stderr": completed.stderr,
    }


def main() -> None:
    required = [
        "PREREGISTRATION.md",
        "SOURCE_MANIFEST.tsv",
        "FROZEN_CURRENT_SCIENTIFIC_PREMISES.tsv",
        "EXACT_DERIVATION.md",
        "PRODUCTION_RESULT.json",
        "INDEPENDENT_VERIFICATION.json",
        "CATCH_PROOF_RESULT.json",
        "AUDIT_REPORT.md",
        "EVIDENCE_GATES.md",
        "LAY_REPORT.md",
        "REPOSITORY_GATES.json",
        "STATUS_LEDGER.tsv",
        "ADVERSARIAL_REVIEW_REQUEST.md",
        "CERTIFICATION_REPAIR_RECORD.md",
        "EXTERNAL_ADVERSARIAL_REVIEW_RAW.md",
        "EXTERNAL_ADVERSARIAL_REVIEW_TRANSCRIPT.txt.gz",
        "EXTERNAL_REVIEW_ADJUDICATION.md",
        "REPAIR_FOLLOWUP_REQUEST.md",
        "EXTERNAL_REPAIR_FOLLOWUP_RAW.md",
        "EXTERNAL_REPAIR_FOLLOWUP_TRANSCRIPT.txt.gz",
        "EXTERNAL_REPAIR_FOLLOWUP_ADJUDICATION.md",
        "FOLLOWUP_TRANSMISSION_RECORD.md",
        "TRANSMISSION_RECORD.md",
        "derive_nonradial_jacobi.py",
        "verify_nonradial_jacobi_independent.py",
        "run_catch_proofs.py",
        "build_review_intake.py",
    ]
    missing = [name for name in required if not (HERE / name).is_file()]

    source_failures = []
    manifest = HERE / "SOURCE_MANIFEST.tsv"
    if manifest.is_file():
        for line in manifest.read_text(encoding="utf-8").splitlines()[1:]:
            relative, expected, _role = line.split("\t", 2)
            source = (
                HERE / "FROZEN_CURRENT_SCIENTIFIC_PREMISES.tsv"
                if relative == "CURRENT_SCIENTIFIC_PREMISES.tsv"
                else ROOT / relative
            )
            if not source.is_file() or sha256(source) != expected:
                source_failures.append(relative)

    mapping = {
        "derive_nonradial_jacobi.py": "PRODUCTION_RESULT.json",
        "verify_nonradial_jacobi_independent.py": "INDEPENDENT_VERIFICATION.json",
        "run_catch_proofs.py": "CATCH_PROOF_RESULT.json",
    }
    replays = {script: replay(script) for script in mapping}
    stored = {
        result: json.loads((HERE / result).read_text(encoding="utf-8"))
        for result in mapping.values() if (HERE / result).is_file()
    }

    checks = {
        "all_required_files": not missing,
        "all_sources_immutable": not source_failures,
        "algebraic_mutation_count_15": (
            stored.get("CATCH_PROOF_RESULT.json", {}).get("algebraic_mutation_catch_count") == 15
        ),
        "artifact_scope_guard_count_14": (
            stored.get("CATCH_PROOF_RESULT.json", {}).get("artifact_scope_guard_count") == 14
        ),
        "independent_10000_pass": (
            stored.get("INDEPENDENT_VERIFICATION.json", {}).get("status") == "PASS"
            and stored.get("INDEPENDENT_VERIFICATION.json", {}).get("trials") == 10_000
            and stored.get("INDEPENDENT_VERIFICATION.json", {}).get("assertions") == 220_000
        ),
        "landing_matches": stored.get("PRODUCTION_RESULT.json", {}).get("landing") == LANDING,
        "live_replays_pass": all(
            item["returncode"] == 0 and item["status"] == "PASS"
            for item in replays.values()
        ),
        "production_20_checks": (
            len(stored.get("PRODUCTION_RESULT.json", {}).get("checks", {})) == 20
            and all(stored.get("PRODUCTION_RESULT.json", {}).get("checks", {}).values())
        ),
        "no_literal_true_placeholder": not any(
            isinstance(value, ast.Constant) and value.value is True
            for node in ast.walk(ast.parse(
                (HERE / "run_catch_proofs.py").read_text(encoding="utf-8")
            ))
            if isinstance(node, ast.Dict)
            for value in node.values
        ),
        "repository_gates_pass": (
            json.loads((HERE / "REPOSITORY_GATES.json").read_text(encoding="utf-8"))
            == {
                "premise_registry": {"historical_dispositions": 754, "rows": 171, "status": "PASS"},
                "repository_tests": {"expected_xfail": 1, "passed": 130, "status": "PASS"},
            }
        ),
        "stored_results_match_live": all(
            json.loads(replays[script]["stdout"]) == stored.get(result)
            for script, result in mapping.items()
        ),
    }
    core_pass = all(checks.values())

    review_path = HERE / "EXTERNAL_ADVERSARIAL_REVIEW_RAW.md"
    review_present = review_path.is_file()
    review_accepted = (
        "G187_ACCEPTED_WITH_STATED_BOUNDS" in review_path.read_text(encoding="utf-8")
        if review_present else False
    )
    checks["external_review_accepted"] = review_present and review_accepted
    followup_path = HERE / "EXTERNAL_REPAIR_FOLLOWUP_RAW.md"
    followup_present = followup_path.is_file()
    followup_accepted = (
        "G187_CERTIFICATION_REPAIR_ACCEPTED__SCIENTIFIC_LANDING_UNCHANGED"
        in followup_path.read_text(encoding="utf-8")
        if followup_present else False
    )
    if followup_present:
        checks["certification_repair_followup_accepted"] = followup_accepted
    status = (
        "PASS" if core_pass and review_present and review_accepted and followup_present and followup_accepted
        else "PRE_FOLLOWUP_PASS" if core_pass and review_present and review_accepted and not followup_present
        else "PRE_REVIEW_PASS" if core_pass and not review_present
        else "FAIL"
    )
    print(json.dumps({
        "audit": "G187_PACKAGE",
        "checks": checks,
        "missing": missing,
        "replays": replays,
        "review_present": review_present,
        "repair_followup_present": followup_present,
        "source_failures": source_failures,
        "status": status,
    }, indent=2, sort_keys=True))
    if status == "FAIL":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
