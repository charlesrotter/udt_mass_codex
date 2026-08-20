#!/usr/bin/env python3
"""Rebuild and verify the bounded G192 evidence package."""

from __future__ import annotations

import argparse
import copy
import csv
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys


PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parent


def run(script: str, no_write: bool) -> str:
    env = os.environ.copy()
    if no_write:
        env["G192_NO_WRITE"] = "1"
    result = subprocess.run(
        [sys.executable, str(PACKAGE / script)],
        cwd=ROOT,
        env=env,
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode:
        raise SystemExit(result.stdout + result.stderr)
    return result.stdout


def run_json(script: str, no_write: bool) -> dict:
    stdout = run(script, no_write)
    try:
        parsed = json.loads(stdout)
    except json.JSONDecodeError as exc:
        raise SystemExit(f"{script} did not emit one JSON document: {exc}\n{stdout}") from exc
    if not isinstance(parsed, dict):
        raise SystemExit(f"{script} emitted JSON type {type(parsed).__name__}, expected object")
    return parsed


def require_field_identity(label: str, fresh: dict, sealed: dict) -> None:
    if fresh != sealed:
        fresh_keys = set(fresh)
        sealed_keys = set(sealed)
        differing = sorted(
            key for key in fresh_keys & sealed_keys if fresh[key] != sealed[key]
        )
        raise SystemExit(
            f"{label} fresh/sealed mismatch: "
            f"fresh_only={sorted(fresh_keys - sealed_keys)}, "
            f"sealed_only={sorted(sealed_keys - fresh_keys)}, "
            f"differing={differing}"
        )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--no-write", action="store_true")
    args = parser.parse_args()

    fresh_production = run_json("derive_smooth_timelive_mixing.py", args.no_write)
    fresh_independent = run_json("verify_smooth_timelive_mixing_independent.py", args.no_write)
    fresh_catches = run_json("run_catch_proofs.py", args.no_write)
    run("build_source_manifest.py", args.no_write)

    production = json.loads((PACKAGE / "PRODUCTION_RESULT.json").read_text(encoding="utf-8"))
    independent = json.loads((PACKAGE / "INDEPENDENT_VERIFICATION.json").read_text(encoding="utf-8"))
    catches = json.loads((PACKAGE / "CATCH_PROOF_RESULT.json").read_text(encoding="utf-8"))
    require_field_identity("production", fresh_production, production)
    require_field_identity("independent", fresh_independent, independent)
    require_field_identity("catches", fresh_catches, catches)

    mutated = copy.deepcopy(production)
    mutated["frequency_residual"] = "registered-hostile-mutation"
    stale_artifact_mutation_caught = False
    try:
        require_field_identity("hostile-control", fresh_production, mutated)
    except SystemExit:
        stale_artifact_mutation_caught = True
    assert stale_artifact_mutation_caught
    with (PACKAGE / "SOURCE_MANIFEST.tsv").open(encoding="utf-8", newline="") as stream:
        source_rows = list(csv.DictReader(stream, delimiter="\t"))

    assert production["frequency_residual"] == "0"
    assert production["geodesic_residual"] == ["0", "0", "0", "0"]
    assert all(value == "0" for row in production["parallel_screen_residual"] for value in row)
    assert production["jacobi_modes"]["y_plus_residual"] == "0"
    assert production["jacobi_modes"]["f_plus_residual"] == "0"
    assert production["jacobi_modes"]["f_minus_residual"] == "0"
    assert production["caustic_classification"]["nonvertex_zeros"] == 0
    assert production["frequency_turn_condition"].startswith("a'(eta)=0")
    assert independent["status"] == "PASS"
    assert independent["assertions"] == 2134
    assert independent["named_cases"] == 10
    assert independent["random_cases"] == 256
    assert independent["maximum_plus_mode_error"] < independent["registered_tolerance"]
    assert independent["maximum_minus_mode_error"] < independent["registered_tolerance"]
    assert independent["named_summaries"]["C03_single_turn"]["turn_count"] == 1
    assert independent["named_summaries"]["C04_multiple_turns_signed_mix"]["turn_count"] >= 2
    assert independent["named_summaries"]["C01_G191"]["cross_response"] > 0
    assert independent["named_summaries"]["C09_negative_cross_response"]["cross_response"] < 0
    assert abs(independent["named_summaries"]["C08_nonzero_mix_zero_tracefree_tide"]["cross_response"]) < 5e-12
    assert catches["status"] == "PASS" and catches["caught"] == 18
    assert len(source_rows) == 10
    for row in source_rows:
        assert hashlib.sha256((ROOT / row["path"]).read_bytes()).hexdigest() == row["sha256"]

    premise_verifier = ROOT / "verify_current_scientific_premises.py"
    if premise_verifier.is_file():
        premise = subprocess.run(
            [sys.executable, str(premise_verifier)],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        if premise.returncode:
            raise SystemExit(premise.stdout + premise.stderr)
        premise_gate = "PASS"
    else:
        premise_gate = "SEALED_INTAKE_NOT_APPLICABLE"

    adjudication_path = PACKAGE / "EXTERNAL_REVIEW_ADJUDICATION.md"
    if adjudication_path.is_file() and "G192_ACCEPTED_WITH_STATED_BOUNDS" in adjudication_path.read_text(encoding="utf-8"):
        external_grade = "G192_ACCEPTED_WITH_STATED_BOUNDS"
        package_grade = "EXTERNALLY_REVIEWED_VERIFIED_WITH_CAVEATS"
    else:
        external_grade = "PENDING"
        package_grade = "VERIFIED_WITH_CAVEATS_PENDING_EXTERNAL_REVIEW"

    result = {
        "status": "PASS",
        "grade": package_grade,
        "no_write_replay": args.no_write,
        "source_rows": len(source_rows),
        "independent_assertions": independent["assertions"],
        "maximum_jacobi_error": max(
            independent["maximum_plus_mode_error"], independent["maximum_minus_mode_error"]
        ),
        "mutation_catches": catches["caught"],
        "fresh_artifact_identity": True,
        "stale_artifact_mutation_caught": stale_artifact_mutation_caught,
        "repository_premise_gate": premise_gate,
        "external_review": external_grade,
    }
    if not args.no_write:
        (PACKAGE / "PACKAGE_VERIFICATION_RESULT.json").write_text(
            json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
