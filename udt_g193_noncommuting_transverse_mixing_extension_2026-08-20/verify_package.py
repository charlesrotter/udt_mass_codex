#!/usr/bin/env python3
"""Rebuild and verify the bounded G193 evidence package."""

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
REVIEW_RUNTIME_NAME = ".review_runtime"


def run(script: str, no_write: bool) -> str:
    env = os.environ.copy()
    if no_write:
        env["G193_NO_WRITE"] = "1"
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
        raise SystemExit(f"{script} emitted {type(parsed).__name__}, expected object")
    return parsed


def require_identity(label: str, fresh: dict, sealed: dict) -> None:
    if fresh != sealed:
        fresh_keys = set(fresh)
        sealed_keys = set(sealed)
        differing = sorted(
            key for key in fresh_keys & sealed_keys if fresh[key] != sealed[key]
        )
        raise SystemExit(
            f"{label} fresh/sealed mismatch: "
            f"fresh_only={sorted(fresh_keys-sealed_keys)}, "
            f"sealed_only={sorted(sealed_keys-fresh_keys)}, differing={differing}"
        )


def package_file_digests() -> dict[str, str]:
    """Hash every package evidence file, excluding the ephemeral review runtime."""
    return {
        str(path.relative_to(PACKAGE)): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in sorted(PACKAGE.rglob("*"))
        if path.is_file() and REVIEW_RUNTIME_NAME not in path.parts
    }


def require_clean_review_runtime() -> Path | None:
    """Validate the only writable path permitted in a sealed follow-up intake."""
    if os.environ.get("G193_REVIEW_RUNTIME_REQUIRED") != "1":
        return None

    expected = (ROOT / REVIEW_RUNTIME_NAME).resolve()
    resolved = []
    for variable in ("TMPDIR", "TMP", "TEMP"):
        raw = os.environ.get(variable)
        if not raw:
            raise SystemExit(f"sealed replay requires {variable}")
        candidate = Path(raw)
        if not candidate.is_absolute():
            candidate = ROOT / candidate
        resolved.append(candidate.resolve())
    if any(path != expected for path in resolved):
        raise SystemExit(
            f"sealed replay temp paths must all resolve to {expected}: {resolved}"
        )
    if not expected.is_dir():
        raise SystemExit(f"sealed replay runtime is missing: {expected}")
    contents = list(expected.iterdir())
    if contents:
        raise SystemExit(f"sealed replay runtime is not empty: {contents}")
    return expected


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--no-write", action="store_true")
    args = parser.parse_args()

    review_runtime = require_clean_review_runtime()
    initial_package_digests = package_file_digests() if args.no_write else None

    fresh_production = run_json("derive_noncommuting_transverse_mixing.py", args.no_write)
    fresh_independent = run_json(
        "verify_noncommuting_transverse_mixing_independent.py", args.no_write
    )
    fresh_catches = run_json("run_catch_proofs.py", args.no_write)
    run("build_source_manifest.py", args.no_write)

    production = json.loads((PACKAGE / "PRODUCTION_RESULT.json").read_text(encoding="utf-8"))
    independent = json.loads(
        (PACKAGE / "INDEPENDENT_VERIFICATION.json").read_text(encoding="utf-8")
    )
    catches = json.loads((PACKAGE / "CATCH_PROOF_RESULT.json").read_text(encoding="utf-8"))
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

    assert production["status"] == "PASS"
    assert all(production["assertions"].values())
    assert production["assertions"]["affine_jacobi_reduction"]
    assert production["assertions"]["matrix_factorization"]
    assert production["assertions"]["g192_limit"]
    assert production["assertions"]["g190_limit"]
    assert production["exact"]["commutator"][0][1] == "A_a*nu_b - A_b*nu_a"
    assert "positive definite" in production["exact"]["caustic_sign"]

    assert independent["status"] == "PASS"
    assert independent["history_count"] == 264
    assert independent["assertion_count"] == 3961
    assert independent["noncommuting_control_commutator_norm"] > 1.0e-4
    assert independent["max_tide_error"] < independent["ceilings"]["tensor"]
    assert independent["max_factorization_error"] < independent["ceilings"]["tensor"]
    assert independent["max_wronskian_error"] < independent["ceilings"]["tensor"]
    assert independent["minimum_sampled_nonvertex_determinant"] > 0.0
    named = {row["name"]: row for row in independent["profiles"][:8]}
    assert abs(named["g192_limit"]["forward_cross_asymmetry"]) < 1.0e-14
    assert abs(named["noncommuting_rotating_axes"]["forward_cross_asymmetry"]) > 1.0e-6

    assert catches["status"] == "PASS"
    assert catches["caught_count"] == catches["catch_count"] == 15

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
    if (
        adjudication_path.is_file()
        and "G193_REPAIRS_ACCEPTED__BOUNDED_LANDING_RETAINED"
        in adjudication_path.read_text(encoding="utf-8")
    ):
        external_grade = "G193_REPAIRS_ACCEPTED__BOUNDED_LANDING_RETAINED"
        package_grade = "EXTERNALLY_REVIEWED_VERIFIED_WITH_CAVEATS"
    else:
        external_grade = "PENDING"
        package_grade = "VERIFIED_WITH_CAVEATS_PENDING_EXTERNAL_REVIEW"

    result = {
        "status": "PASS",
        "grade": package_grade,
        "no_write_replay": args.no_write,
        "source_rows": len(source_rows),
        "independent_histories": independent["history_count"],
        "independent_assertions": independent["assertion_count"],
        "maximum_tide_error": independent["max_tide_error"],
        "maximum_factorization_error": independent["max_factorization_error"],
        "mutation_catches": catches["caught_count"],
        "fresh_artifact_identity": True,
        "stale_artifact_mutation_caught": stale_artifact_caught,
        "repository_premise_gate": premise_gate,
        "external_review": external_grade,
    }
    if not args.no_write:
        (PACKAGE / "PACKAGE_VERIFICATION_RESULT.json").write_text(
            json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
    if review_runtime is not None:
        require_clean_review_runtime()
    if args.no_write and package_file_digests() != initial_package_digests:
        raise SystemExit("no-write replay changed a package evidence file")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
