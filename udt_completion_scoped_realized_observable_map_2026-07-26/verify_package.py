#!/usr/bin/env python3
"""Fail-closed integrity and deterministic replay for the completion map."""

from __future__ import annotations

import csv
import hashlib
import json
import os
import platform
import subprocess
import sys
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
BASE = "c1036fb498c8ed009733c82ee86cf96152a5ed6e"
PREREG = "c457bc4"
AMENDMENT = "b3325dd"
CORRECTION = "4a95a7b6f7231879ed1662d956603b1acb6326b8"
PREREG_FILES = (
    "COMPLETION_UNIVERSE.tsv", "FALSIFICATION_CONTRACT.tsv", "MAP_GATE_UNIVERSE.tsv",
    "PREMISE_LEDGER.tsv", "PREREGISTRATION.md", "READOUT_UNIVERSE.tsv",
    "RELATION_UNIVERSE.tsv", "SOURCE_MANIFEST.tsv", "SOURCE_SCOPE.tsv", "build_source_manifest.py",
)
PRODUCTION_FILES = (
    "COMPLETION_READOUT_MATRIX.tsv", "DEPENDENCY_GRAPH.json", "LOCK_LINKAGE_LEDGER.tsv",
    "RELATION_MATRIX.tsv", "RESULT.json", "R_GEOM_SCHEMA.tsv",
)


def digest_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def digest(path: Path) -> str:
    return digest_bytes(path.read_bytes())


def rows(name: str) -> list[dict[str, str]]:
    with (HERE / name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def frozen_matches(commit: str, name: str) -> bool:
    frozen = subprocess.run(["git", "show", f"{commit}:{HERE.name}/{name}"], cwd=ROOT,
                            check=True, capture_output=True).stdout
    return frozen == (HERE / name).read_bytes()


def main() -> None:
    if not all(frozen_matches(PREREG, name) for name in PREREG_FILES):
        raise AssertionError("preregistration drift")
    if not all(frozen_matches(AMENDMENT, name) for name in
               ("PREREGISTRATION_SOURCE_AMENDMENT_01.md", "SOURCE_MANIFEST_AMENDMENT_01.tsv")):
        raise AssertionError("source amendment drift")
    if not all(frozen_matches(CORRECTION, name) for name in
               ("SOURCE_MANIFEST_CORRECTION_01.md", "SOURCE_MANIFEST_CORRECTION_01.tsv")):
        raise AssertionError("source correction drift")

    source_rows = rows("SOURCE_MANIFEST.tsv") + rows("SOURCE_MANIFEST_AMENDMENT_01.tsv")
    correction_rows = rows("SOURCE_MANIFEST_CORRECTION_01.tsv")
    corrections = {(row["source_id"], row["field"]): row["corrected_value"] for row in correction_rows}
    if len(source_rows) != 21 or len({row["source_id"] for row in source_rows}) != 21:
        raise AssertionError("source coverage")
    if len(correction_rows) != 1 or set(corrections) != {("S17", "sha256")}:
        raise AssertionError("source correction overlay")
    for row in source_rows:
        path = ROOT / row["path"]
        expected = corrections.get((row["source_id"], "sha256"), row["sha256"])
        frozen = subprocess.run(["git", "show", f"{BASE}:{row['path']}"], cwd=ROOT,
                                check=True, capture_output=True).stdout
        if not path.is_file() or path.stat().st_size != int(row["size_bytes"]):
            raise AssertionError(f"source size:{row['source_id']}")
        if digest(path) != expected or digest_bytes(frozen) != expected:
            raise AssertionError(f"source identity:{row['source_id']}")

    before = {name: digest(HERE / name) for name in PRODUCTION_FILES}
    environment = dict(os.environ)
    environment.update({"CUDA_VISIBLE_DEVICES": "", "PYTHONDONTWRITEBYTECODE": "1"})
    production = subprocess.run([sys.executable, str(HERE / "derive_completion_map.py")], cwd=ROOT,
                                env=environment, text=True, capture_output=True)
    (HERE / "PRODUCTION_STDOUT.txt").write_text(production.stdout, encoding="utf-8")
    (HERE / "PRODUCTION_STDERR.txt").write_text(production.stderr, encoding="utf-8")
    if production.returncode:
        raise SystemExit(production.returncode)
    if before != {name: digest(HERE / name) for name in PRODUCTION_FILES}:
        raise AssertionError("nondeterministic production outputs")

    independent = subprocess.run([sys.executable, str(HERE / "verify_independent.py")], cwd=ROOT,
                                 env=environment, text=True, capture_output=True)
    (HERE / "INDEPENDENT_STDOUT.txt").write_text(independent.stdout, encoding="utf-8")
    (HERE / "INDEPENDENT_STDERR.txt").write_text(independent.stderr, encoding="utf-8")
    if independent.returncode:
        raise SystemExit(independent.returncode)

    result = json.loads((HERE / "RESULT.json").read_text(encoding="utf-8"))
    independent_result = json.loads((HERE / "INDEPENDENT_RESULT.json").read_text(encoding="utf-8"))
    if result["check_count"] != 29 or set(result["checks"].values()) != {"PASS"}:
        raise AssertionError("production checks")
    if independent_result["check_count"] != 31 or independent_result["catch_count"] != 22:
        raise AssertionError("independent coverage")
    if independent_result["result"] != "PASS" or set(independent_result["checks"].values()) != {"PASS"}:
        raise AssertionError("independent checks")
    if result["maximum_supported_conclusion"] != independent_result["maximum_supported_conclusion"]:
        raise AssertionError("conclusion mismatch")

    verification = {
        "schema": "udt-completion-scoped-map-package-verification-1.0",
        "result": "PASS", "python": sys.version.split()[0], "dependencies": "stdlib_only",
        "preregistration_files_unchanged": len(PREREG_FILES),
        "source_manifest_rows_verified_at_base": len(source_rows),
        "deterministic_production_files": len(PRODUCTION_FILES),
        "production_checks": result["check_count"],
        "independent_checks": independent_result["check_count"],
        "exercised_catch_proofs": independent_result["catch_count"],
        "maximum_supported_conclusion": result["maximum_supported_conclusion"],
    }
    (HERE / "VERIFICATION_RESULT.json").write_text(
        json.dumps(verification, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    run_environment = {
        "schema": "udt-completion-scoped-map-run-environment-1.0", "result": "PASS",
        "cpu_only": True, "implementation": platform.python_implementation(),
        "python": sys.version.split()[0], "platform": platform.platform(),
        "dependencies": "python_standard_library_only", "production_exit_code": production.returncode,
        "independent_exit_code": independent.returncode,
        "production_stdout_sha256": digest(HERE / "PRODUCTION_STDOUT.txt"),
        "production_stderr_sha256": digest(HERE / "PRODUCTION_STDERR.txt"),
        "independent_stdout_sha256": digest(HERE / "INDEPENDENT_STDOUT.txt"),
        "independent_stderr_sha256": digest(HERE / "INDEPENDENT_STDERR.txt"),
    }
    (HERE / "RUN_ENVIRONMENT.json").write_text(
        json.dumps(run_environment, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(verification, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
