#!/usr/bin/env python3
"""Rebuild and verify the bounded G198 evidence package."""

from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor
import csv
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys


PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parent


def run(script, no_write):
    env = os.environ.copy()
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    if no_write:
        env["G198_NO_WRITE"] = "1"
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


def run_json(script, no_write):
    stdout = run(script, no_write)
    try:
        value = json.loads(stdout)
    except json.JSONDecodeError as exc:
        raise SystemExit(f"{script} did not emit one JSON object: {exc}\n{stdout}") from exc
    if not isinstance(value, dict):
        raise SystemExit(f"{script} emitted {type(value).__name__}, expected object")
    return value


def package_digests():
    return {
        str(path.relative_to(PACKAGE)): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in sorted(PACKAGE.rglob("*"))
        if path.is_file() and "__pycache__" not in path.parts
    }


def require_identity(label, fresh, sealed):
    if fresh != sealed:
        differences = sorted(
            key for key in set(fresh) | set(sealed) if fresh.get(key) != sealed.get(key)
        )
        raise SystemExit(f"{label} fresh/sealed mismatch: {differences}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--no-write", action="store_true")
    args = parser.parse_args()
    initial = package_digests() if args.no_write else None

    with ThreadPoolExecutor(max_workers=4) as executor:
        production_future = executor.submit(
            run_json, "derive_bidirectional_null_germs.py", args.no_write
        )
        independent_future = executor.submit(
            run_json, "verify_bidirectional_null_germs_independent.py", args.no_write
        )
        catches_future = executor.submit(run_json, "run_catch_proofs.py", args.no_write)
        manifest_future = executor.submit(run, "build_source_manifest.py", args.no_write)
        fresh_production = production_future.result()
        fresh_independent = independent_future.result()
        fresh_catches = catches_future.result()
        manifest_future.result()

    production = json.loads((PACKAGE / "PRODUCTION_RESULT.json").read_text())
    independent = json.loads((PACKAGE / "INDEPENDENT_VERIFICATION.json").read_text())
    catches = json.loads((PACKAGE / "CATCH_PROOF_RESULT.json").read_text())
    require_identity("production", fresh_production, production)
    require_identity("independent", fresh_independent, independent)
    require_identity("catches", fresh_catches, catches)

    with (PACKAGE / "SOURCE_MANIFEST.tsv").open(encoding="utf-8", newline="") as stream:
        rows = list(csv.DictReader(stream, delimiter="\t"))
    assert len(rows) == 7
    for row in rows:
        assert hashlib.sha256((ROOT / row["path"]).read_bytes()).hexdigest() == row["sha256"]

    landing = "OPPOSITE_GERM_NULL_CONTROL__ASYMMETRY_IS_METRIC_ENCODED"
    assert production["status"] == "PASS"
    assert production["landing"] == landing
    assert len(production["assertions"]) == 23
    assert all(production["assertions"].values())
    for gate in (
        "plus_affine",
        "minus_affine",
        "plus_connection_regression",
        "minus_connection_quiet",
        "plus_tide_regression",
        "minus_tide_control",
        "plus_jacobi_screen_closed",
        "minus_jacobi_screen_closed",
        "minus_coordinate_jacobi",
        "two_ray_alias_values",
        "two_ray_alias_first_jets",
        "two_ray_alias_offray",
    ):
        assert production["assertions"][gate]

    assert independent["status"] == "PASS"
    assert independent["landing"] == landing
    assert independent["seed"] == 1980821
    assert independent["history_count"] == 68
    assert independent["random_history_count"] == 64
    assert independent["assertion_count"] == 1838
    assert independent["base_residual_evaluations"] == 816
    for key, value in independent["max_errors"].items():
        ceiling = (
            independent["ceilings"]["algebra"]
            if key in {"metric", "frequency"}
            else independent["ceilings"]["tensor"]
        )
        assert value < ceiling
    assert independent["two_ray_alias_onray_error"] < independent["ceilings"]["algebra"]
    assert independent["two_ray_alias_offray_value"] > 1.0e-4

    assert catches["status"] == "PASS"
    assert catches["caught_count"] == catches["catch_count"] == 9

    result = {
        "status": "PASS",
        "grade": "INDEPENDENTLY_VERIFIED_WITH_CAVEATS",
        "no_write_replay": args.no_write,
        "source_rows": len(rows),
        "production_assertions": len(production["assertions"]),
        "independent_histories": independent["history_count"],
        "independent_assertions": independent["assertion_count"],
        "base_residual_evaluations": independent["base_residual_evaluations"],
        "mutation_catches": catches["caught_count"],
        "maximum_incoming_operator_error": independent["max_errors"]["incoming_operator"],
        "maximum_outgoing_operator_error": independent["max_errors"]["outgoing_operator"],
        "fresh_artifact_identity": True,
    }
    if not args.no_write:
        (PACKAGE / "PACKAGE_VERIFICATION_RESULT.json").write_text(
            json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
    if args.no_write and package_digests() != initial:
        raise SystemExit("no-write replay changed a package evidence file")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
