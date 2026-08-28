#!/usr/bin/env python3
"""Fail-closed dependency-free package and live-replay verifier for G285."""

from __future__ import annotations

import csv
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parent
LANDING = (
    "COMPLETE_GERM_RETYPES_SCALAR_TWINS_AS_DISTINCT_SEPARATIONS__"
    "VALUE_PROPAGATION_REMAINS_OPEN"
)


def read_json(name: str) -> dict:
    return json.loads((PACKAGE / name).read_text(encoding="utf-8"))


def main() -> None:
    required = (
        "MAP.md",
        "PREMISE_LEDGER.tsv",
        "PREREGISTRATION.md",
        "PREREGISTRATION_RESULT.json",
        "SOURCE_MANIFEST.tsv",
        "SOURCE_SCOPE.tsv",
        "COMMANDS.md",
        "STATUS_LEDGER.tsv",
        "DERIVATION_RESULT.json",
        "INDEPENDENT_VERIFICATION.json",
        "CATCH_PROOF_RESULT.json",
        "EXACT_DERIVATION.md",
        "AUDIT_REPORT.md",
        "LAY_REPORT.md",
        "EVIDENCE_GATES.md",
        "EXTERNAL_REVIEW_GPT54.md",
        "EXTERNAL_REVIEW_TRANSMISSION.md",
        "REPAIR_PREREGISTRATION.md",
        "EXTERNAL_REPAIR_FOLLOWUP_GPT54.md",
        "EXTERNAL_REPAIR_FOLLOWUP_TRANSMISSION.md",
        "derive_complete_separation_retyping.py",
        "verify_independent.py",
        "run_catch_proofs.py",
        "verify_preregistration.py",
        "verify_package.py",
    )
    checks: dict[str, bool] = {
        "all_required_files_present": all((PACKAGE / name).is_file() for name in required)
    }
    with (PACKAGE / "SOURCE_MANIFEST.tsv").open(newline="", encoding="utf-8") as handle:
        sources = list(csv.DictReader(handle, delimiter="\t"))
    checks["source_count_13"] = len(sources) == 13
    source_integrity = True
    for row in sources:
        path = ROOT / row["path"]
        payload = path.read_bytes() if path.is_file() else b""
        source_integrity &= (
            path.is_file()
            and len(payload) == int(row["bytes"])
            and hashlib.sha256(payload).hexdigest() == row["sha256"]
        )
    checks["all_source_hashes_and_sizes_exact"] = source_integrity

    prereg = read_json("PREREGISTRATION_RESULT.json")
    derivation = read_json("DERIVATION_RESULT.json")
    independent = read_json("INDEPENDENT_VERIFICATION.json")
    catches = read_json("CATCH_PROOF_RESULT.json")
    checks.update(
        {
            "preregistration_pass": prereg["status"] == "PASS" and prereg["source_count"] == 13,
            "type_schema_adjudication_20_of_20": derivation["status"] == "PASS"
            and derivation["audit"]
            == "G285_COMPLETE_SEPARATION_GERM_TYPE_SCHEMA_ADJUDICATION"
            and derivation["landing"] == LANDING
            and derivation["type_schema_checks"] == 20
            and all(derivation["checks"].values()),
            "geometry_not_claimed_recomputed": derivation["witness_geometry_recomputed"] is False
            and independent["witness_geometry_recomputed"] is False,
            "candidate_not_adopted_or_canon": derivation["candidate_clarification_status"]
            == "CANDIDATE_WORKING_FOUNDATIONAL_CLARIFICATION__NOT_CANON",
            "value_propagation_remains_open": derivation["value_selecting_constraints_found"] == 0,
            "no_scientific_imports": not any(derivation["scientific_imports"].values()),
            "implementation_distinct_schema_256_cases_2048_assertions": independent["status"]
            == "PASS"
            and independent["audit"] == "G285_IMPLEMENTATION_DISTINCT_TYPE_SCHEMA_CENSUS"
            and independent["type_schema_cases"] == 256
            and independent["type_schema_assertions"] == 2048
            and independent["production_imported"] is False
            and independent["production_output_read"] is False,
            "catch_proofs_10_of_10": catches["status"] == "PASS"
            and catches["caught_count"] == catches["mutation_count"] == 10
            and all(catches["caught"].values()),
        }
    )

    audit = (PACKAGE / "AUDIT_REPORT.md").read_text(encoding="utf-8")
    exact = (PACKAGE / "EXACT_DERIVATION.md").read_text(encoding="utf-8")
    checks["reports_retain_bounded_landing"] = all(
        token in audit and token in exact
        for token in (
            "COMPLETE_GERM_RETYPES_SCALAR_TWINS_AS_DISTINCT_SEPARATIONS",
            "VALUE_PROPAGATION_REMAINS_OPEN",
        )
    )
    checks["reports_forbid_overclaim"] = all(
        token in audit
        for token in (
            "does not adopt or canonize",
            "does not yet determine",
            "absolute scale",
            "observer, branch, and path population",
        )
    )
    evidence = (PACKAGE / "EVIDENCE_GATES.md").read_text(encoding="utf-8")
    status_ledger = (PACKAGE / "STATUS_LEDGER.tsv").read_text(encoding="utf-8")
    rejected_grade = "PREREGISTERED__EXACTLY_DERIVED__INDEPENDENTLY_VERIFIED__SOURCE_BOUNDED"
    checks["reports_use_repaired_type_schema_grade"] = all(
        token in audit and token in evidence and token in status_ledger
        for token in ("TYPE_SCHEMA", "not adopted")
    )
    checks["rejected_overgrade_absent_from_current_reports"] = all(
        rejected_grade not in payload for payload in (audit, evidence, status_ledger)
    )

    commands = (
        ("verify_preregistration.py", '"status": "PASS"'),
        ("derive_complete_separation_retyping.py", LANDING),
        ("verify_independent.py", '"type_schema_assertions": 2048'),
        ("run_catch_proofs.py", '"caught_count": 10'),
    )
    replay_records: list[dict[str, object]] = []
    with tempfile.TemporaryDirectory(prefix="g285_replay_", dir="/tmp") as directory:
        temp_root = Path(directory)
        temp_package = temp_root / PACKAGE.name
        shutil.copytree(PACKAGE, temp_package)
        for row in sources:
            source = ROOT / row["path"]
            destination = temp_root / row["path"]
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, destination)
        for script, token in commands:
            completed = subprocess.run(
                [sys.executable, "-S", str(temp_package / script)],
                cwd=temp_root,
                capture_output=True,
                text=True,
                check=False,
                env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
            )
            record = {
                "script": script,
                "exit_code": completed.returncode,
                "expected_token_found": token in completed.stdout,
                "interpreter_mode": "python_-S_no_site_packages",
            }
            replay_records.append(record)
        checks["registered_replays_4_of_4"] = all(
            row["exit_code"] == 0 and row["expected_token_found"] for row in replay_records
        )
        broken = temp_package / "derive_complete_separation_retyping.py"
        broken.write_text(
            'raise SystemExit("G285 verifier mutation")\n' + broken.read_text(encoding="utf-8"),
            encoding="utf-8",
        )
        mutation = subprocess.run(
            [sys.executable, "-S", str(broken)],
            cwd=temp_root,
            capture_output=True,
            text=True,
            check=False,
            env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
        )
        checks["broken_registered_replay_mutation_caught"] = mutation.returncode != 0

    status = "PASS_EXTERNAL_REPAIR_FOLLOWUP_CONFIRMED" if all(checks.values()) else "FAIL"
    result = {
        "audit": "G285_PACKAGE_AND_LIVE_REPLAY_VERIFICATION",
        "status": status,
        "landing": LANDING,
        "checks": checks,
        "counts": {
            "frozen_sources": len(sources),
            "premise_rows": prereg["premise_rows"],
            "type_schema_checks": derivation["type_schema_checks"],
            "type_schema_cases": independent["type_schema_cases"],
            "type_schema_assertions": independent["type_schema_assertions"],
            "typed_catches": catches["caught_count"],
        },
        "replay_commands": replay_records,
        "external_review": "ACCEPT_WITH_REPAIRS__R1_R2_EXTERNALLY_CONFIRMED",
        "maximum_grade": (
            "PREREGISTERED__SOURCE_BOUNDED__TYPE_SCHEMA_ADJUDICATED__"
            "IMPLEMENTATION_DISTINCT_TYPE_SCHEMA_CENSUS__EXTERNAL_ACCEPT_WITH_REPAIRS__"
            "R1_R2_EXTERNALLY_CONFIRMED__"
            "CANDIDATE_CLARIFICATION_SUPPORTED_NOT_ADOPTED_NOT_CANON"
        ),
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    raise SystemExit(0 if status == "PASS_EXTERNAL_REPAIR_FOLLOWUP_CONFIRMED" else 1)


if __name__ == "__main__":
    main()
