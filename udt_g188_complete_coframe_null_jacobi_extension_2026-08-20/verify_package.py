#!/usr/bin/env python3
"""Live package verifier for bounded G188, before or after external review."""

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
    "GENERAL_COMPLETE_COFRAME_NULL_JACOBI_FUNCTOR_DERIVED_CONDITIONALLY"
    "__G187_IS_THE_REFLECTION_DIAGONAL_SPECIALIZATION"
    "__GENUINE_COFRAME_MIXING_GENERATES_OFFDIAGONAL_FINITE_RESPONSE"
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
        "EXTERNAL_ADVERSARIAL_REVIEW_RAW.md",
        "EXTERNAL_ADVERSARIAL_REVIEW_TRANSCRIPT.txt.gz",
        "EXTERNAL_REVIEW_ADJUDICATION.md",
        "TRANSMISSION_RECORD.md",
        "derive_complete_coframe_null_jacobi.py",
        "verify_complete_coframe_null_jacobi_independent.py",
        "run_catch_proofs.py",
        "build_review_intake.py",
    ]
    missing = [name for name in required if not (HERE / name).is_file()]

    source_failures = []
    manifest = HERE / "SOURCE_MANIFEST.tsv"
    if manifest.is_file():
        lines = manifest.read_text(encoding="utf-8").splitlines()
        if len(lines) != 7:
            source_failures.append("SOURCE_MANIFEST.tsv:expected_6_rows")
        for line in lines[1:]:
            relative, expected, _role = line.split("\t", 2)
            source = (
                HERE / "FROZEN_CURRENT_SCIENTIFIC_PREMISES.tsv"
                if relative == "CURRENT_SCIENTIFIC_PREMISES.tsv"
                else ROOT / relative
            )
            if not source.is_file() or sha256(source) != expected:
                source_failures.append(relative)

    mapping = {
        "derive_complete_coframe_null_jacobi.py": "PRODUCTION_RESULT.json",
        "verify_complete_coframe_null_jacobi_independent.py": "INDEPENDENT_VERIFICATION.json",
        "run_catch_proofs.py": "CATCH_PROOF_RESULT.json",
    }
    replays = {script: replay(script) for script in mapping}
    stored = {
        result: json.loads((HERE / result).read_text(encoding="utf-8"))
        for result in mapping.values() if (HERE / result).is_file()
    }
    catches = stored.get("CATCH_PROOF_RESULT.json", {})
    production = stored.get("PRODUCTION_RESULT.json", {})
    independent = stored.get("INDEPENDENT_VERIFICATION.json", {})

    checks = {
        "all_required_files": not missing,
        "all_sources_immutable": not source_failures,
        "algebraic_mutation_count_14": catches.get("algebraic_mutation_catch_count") == 14,
        "artifact_scope_guard_count_11": catches.get("artifact_scope_guard_count") == 11,
        "independent_10000_pass": (
            independent.get("status") == "PASS"
            and independent.get("trials") == 10_000
            and independent.get("assertions") == 240_000
        ),
        "landing_matches": production.get("landing") == LANDING,
        "live_replays_pass": all(
            item["returncode"] == 0 and item["status"] == "PASS"
            for item in replays.values()
        ),
        "production_28_checks": (
            len(production.get("checks", {})) == 28
            and all(production.get("checks", {}).values())
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
                "premise_registry": {"historical_dispositions": 754, "rows": 172, "status": "PASS"},
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
        "G188_ACCEPTED_WITH_STATED_BOUNDS" in review_path.read_text(encoding="utf-8")
        if review_present else False
    )
    if review_present:
        checks["external_review_accepted"] = review_accepted
    status = (
        "PASS" if core_pass and review_present and review_accepted
        else "PRE_REVIEW_PASS" if core_pass and not review_present
        else "FAIL"
    )
    print(json.dumps({
        "audit": "G188_PACKAGE",
        "checks": checks,
        "missing": missing,
        "replays": replays,
        "review_present": review_present,
        "source_failures": source_failures,
        "status": status,
    }, indent=2, sort_keys=True))
    if status == "FAIL":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
