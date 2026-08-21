#!/usr/bin/env python3
"""Rebuild and verify the bounded G195 evidence package."""

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
        env["G195_NO_WRITE"] = "1"
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
        raise SystemExit(f"{script} did not emit one JSON object: {exc}\n{stdout}") from exc
    if not isinstance(parsed, dict):
        raise SystemExit(f"{script} emitted {type(parsed).__name__}, expected object")
    return parsed


def require_identity(label: str, fresh: dict, sealed: dict) -> None:
    if fresh != sealed:
        keys = set(fresh) | set(sealed)
        differences = sorted(key for key in keys if fresh.get(key) != sealed.get(key))
        raise SystemExit(f"{label} fresh/sealed mismatch: {differences}")


def package_digests() -> dict[str, str]:
    return {
        str(path.relative_to(PACKAGE)): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in sorted(PACKAGE.rglob("*"))
        if path.is_file() and "__pycache__" not in path.parts
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--no-write", action="store_true")
    args = parser.parse_args()
    initial_digests = package_digests() if args.no_write else None

    fresh_production = run_json("derive_antisymmetric_screen_rotation.py", args.no_write)
    fresh_independent = run_json(
        "verify_antisymmetric_screen_rotation_independent.py", args.no_write
    )
    fresh_catches = run_json("run_catch_proofs.py", args.no_write)
    run("build_source_manifest.py", args.no_write)

    production = json.loads((PACKAGE / "PRODUCTION_RESULT.json").read_text())
    independent = json.loads((PACKAGE / "INDEPENDENT_VERIFICATION.json").read_text())
    catches = json.loads((PACKAGE / "CATCH_PROOF_RESULT.json").read_text())
    require_identity("production", fresh_production, production)
    require_identity("independent", fresh_independent, independent)
    require_identity("catches", fresh_catches, catches)

    mutated = copy.deepcopy(production)
    mutated["status"] = "REGISTERED_HOSTILE_STALE_ARTIFACT"
    stale_artifact_caught = False
    try:
        require_identity("hostile-control", fresh_production, mutated)
    except SystemExit:
        stale_artifact_caught = True
    assert stale_artifact_caught

    with (PACKAGE / "SOURCE_MANIFEST.tsv").open(encoding="utf-8", newline="") as stream:
        source_rows = list(csv.DictReader(stream, delimiter="\t"))
    assert len(source_rows) == 10
    for row in source_rows:
        assert hashlib.sha256((ROOT / row["path"]).read_bytes()).hexdigest() == row["sha256"]

    landing = (
        "ROTATION_CARRIES_COVARIANTLY__GENERAL_REAL_MATRIX_"
        "FACTORIZATION_AND_NO_CAUSTIC_CLOSE"
    )
    assert production["status"] == "PASS"
    assert production["landing"] == landing
    assert len(production["assertions"]) == 22
    assert all(production["assertions"].values())
    for gate in (
        "screen_connection",
        "coordinate_tide",
        "parallel_transport",
        "parallel_tide",
        "general_factorization",
        "covariant_factorization",
        "affine_jacobi_reduction",
        "g194_limit",
        "pure_rotation_no_tide",
    ):
        assert production["assertions"][gate]

    assert independent["status"] == "PASS"
    assert independent["landing"] == landing
    assert independent["independence_grade"] == (
        "METRIC_JET_RIEMANN_AND_CONNECTION_SPOTCHECK_PLUS_"
        "FORMULA_DRIVEN_PARALLEL_MATRIX_IVP"
    )
    assert independent["seed"] == 1950820
    assert independent["history_count"] == 266
    assert independent["named_history_count"] == 10
    assert independent["random_history_count"] == 256
    assert independent["assertion_count"] == 5059
    assert independent["noncommuting_control_commutator_norm"] > 1.0e-4
    assert (
        independent["rank_transition_determinants"][0]
        * independent["rank_transition_determinants"][1]
        < 0.0
    )
    assert (
        independent["rotation_zero_crossing_values"][0]
        * independent["rotation_zero_crossing_values"][1]
        < 0.0
    )
    assert independent["max_tide_error"] < independent["ceilings"]["tensor"]
    assert independent["max_screen_connection_error"] < independent["ceilings"]["tensor"]
    assert independent["max_factorization_error"] < independent["ceilings"]["tensor"]
    assert independent["max_wronskian_error"] < independent["ceilings"]["tensor"]
    assert independent["minimum_sampled_nonvertex_determinant"] > 0.0
    named = {row["name"]: row for row in independent["profiles"][:10]}
    for name in ("pure_constant_rotation", "pure_variable_rotation"):
        assert named[name]["pure_rotation_parallel_map_error"] < independent["ceilings"]["tensor"]

    assert catches["status"] == "PASS"
    assert catches["caught_count"] == catches["catch_count"] == 18

    adjudication_path = PACKAGE / "EXTERNAL_REVIEW_ADJUDICATION.md"
    adjudication = adjudication_path.read_text() if adjudication_path.is_file() else ""
    accepted_marker = (
        "G195_NO_WRITE_EVIDENCE_REPAIR_ACCEPTED__BOUNDED_LANDING_RETAINED"
    )
    if accepted_marker in adjudication:
        external_grade = accepted_marker
        grade = "EXTERNALLY_REVIEWED_VERIFIED_WITH_CAVEATS"
    else:
        external_grade = "PENDING"
        grade = "VERIFIED_WITH_CAVEATS_PENDING_EXTERNAL_REVIEW"

    result = {
        "status": "PASS",
        "grade": grade,
        "no_write_replay": args.no_write,
        "source_rows": len(source_rows),
        "independent_histories": independent["history_count"],
        "independent_assertions": independent["assertion_count"],
        "maximum_tide_error": independent["max_tide_error"],
        "maximum_screen_connection_error": independent["max_screen_connection_error"],
        "maximum_factorization_error": independent["max_factorization_error"],
        "mutation_catches": catches["caught_count"],
        "fresh_artifact_identity": True,
        "stale_artifact_mutation_caught": stale_artifact_caught,
        "repository_premise_gate": "SEPARATE_REPOSITORY_GATE_NOT_PART_OF_SEALED_REPLAY",
        "external_review": external_grade,
    }
    if not args.no_write:
        (PACKAGE / "PACKAGE_VERIFICATION_RESULT.json").write_text(
            json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
    if args.no_write and package_digests() != initial_digests:
        raise SystemExit("no-write replay changed a package evidence file")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
