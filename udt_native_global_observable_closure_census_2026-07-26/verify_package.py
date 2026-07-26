#!/usr/bin/env python3
"""Fail-closed integrity and deterministic-replay verifier for this package."""

from __future__ import annotations

import csv
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
PREREG_COMMIT = "6a2fe80dd50884d5f3c50f335115e2fa23fb206a"
BASE = "c2a0feafca41d9fa95c12a7db278876acf7552f0"
PREREG_FILES = (
    "FALSIFICATION_CONTRACT.tsv", "OBSERVABLE_UNIVERSE.tsv", "PREMISE_LEDGER.tsv",
    "PREREGISTRATION.md", "PRINCIPLE_UNIVERSE.tsv", "SOURCE_MANIFEST.tsv",
    "SOURCE_SCOPE.tsv", "VARIATION_GATE_UNIVERSE.tsv", "build_source_manifest.py",
)
PRODUCTION_FILES = (
    "ASSEMBLY_BLOCKER_LEDGER.tsv", "COUNTERMODEL_LEDGER.tsv", "OBSERVABLE_DEFINITION_LEDGER.tsv",
    "OBSERVABLE_GATE_MATRIX.tsv", "PRINCIPLE_CLOSURE_MATRIX.tsv", "RESULT.json",
    "STATUS_LEDGER.tsv", "VARIATION_LEDGER.tsv",
)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def table(name: str) -> list[dict[str, str]]:
    with (HERE / name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def main() -> None:
    import sympy
    if sympy.__version__ != "1.14.0":
        raise SystemExit(f"requires pinned SymPy 1.14.0, found {sympy.__version__}")

    for name in PREREG_FILES:
        git_path = f"{HERE.name}/{name}"
        frozen = subprocess.run(["git", "show", f"{PREREG_COMMIT}:{git_path}"], cwd=ROOT,
                                check=True, capture_output=True).stdout
        if frozen != (HERE / name).read_bytes():
            raise AssertionError(f"preregistration drift: {name}")

    source_rows = table("SOURCE_MANIFEST.tsv")
    if len(source_rows) != 19 or len({row["source_id"] for row in source_rows}) != 19:
        raise AssertionError("source manifest coverage")
    for row in source_rows:
        path = ROOT / row["path"]
        frozen = subprocess.run(["git", "show", f"{BASE}:{row['path']}"], cwd=ROOT,
                                check=True, capture_output=True).stdout
        if not path.is_file() or str(path.stat().st_size) != row["size_bytes"]:
            raise AssertionError(f"source size: {row['source_id']}")
        if digest(path) != row["sha256"] or hashlib.sha256(frozen).hexdigest() != row["sha256"]:
            raise AssertionError(f"source identity: {row['source_id']}")

    before = {name: digest(HERE / name) for name in PRODUCTION_FILES}
    environment = dict(os.environ)
    environment.update({"CUDA_VISIBLE_DEVICES": "", "PYTHONDONTWRITEBYTECODE": "1"})
    pinned_site = os.environ.get("UDT_PINNED_SITE")
    if pinned_site:
        bootstrap = ("import runpy,sys;"
                     f"sys.path.insert(0,{pinned_site!r});"
                     f"runpy.run_path({str(HERE / 'derive_observable_census.py')!r},run_name='__main__')")
        production_command = [sys.executable, "-I", "-S", "-c", bootstrap]
    else:
        production_command = [sys.executable, str(HERE / "derive_observable_census.py")]
    production = subprocess.run(production_command, cwd=ROOT, env=environment,
                                text=True, capture_output=True)
    (HERE / "PRODUCTION_STDOUT.txt").write_text(production.stdout, encoding="utf-8")
    (HERE / "PRODUCTION_STDERR.txt").write_text(production.stderr, encoding="utf-8")
    if production.returncode:
        raise SystemExit(production.returncode)
    after = {name: digest(HERE / name) for name in PRODUCTION_FILES}
    if before != after:
        raise AssertionError("nondeterministic production outputs")

    independent = subprocess.run([sys.executable, str(HERE / "verify_independent.py")],
                                 cwd=ROOT, env=environment, text=True, capture_output=True)
    (HERE / "INDEPENDENT_STDOUT.txt").write_text(independent.stdout, encoding="utf-8")
    (HERE / "INDEPENDENT_STDERR.txt").write_text(independent.stderr, encoding="utf-8")
    if independent.returncode:
        raise SystemExit(independent.returncode)

    result = json.loads((HERE / "RESULT.json").read_text(encoding="utf-8"))
    independent_result = json.loads((HERE / "INDEPENDENT_RESULT.json").read_text(encoding="utf-8"))
    if result["algebra_check_count"] != 39 or set(result["checks"].values()) != {"PASS"}:
        raise AssertionError("production checks")
    if independent_result["check_count"] != 46 or independent_result["catch_count"] != 22:
        raise AssertionError("independent coverage")
    if independent_result["result"] != "PASS" or set(independent_result["checks"].values()) != {"PASS"}:
        raise AssertionError("independent checks")
    if result["maximum_supported_conclusion"] != independent_result["maximum_supported_conclusion"]:
        raise AssertionError("conclusion mismatch")

    output = {
        "schema": "udt-native-global-observable-package-verification-1.0",
        "result": "PASS",
        "python": sys.version.split()[0],
        "sympy": sympy.__version__,
        "preregistration_files_unchanged": len(PREREG_FILES),
        "source_manifest_rows_verified_at_base": len(source_rows),
        "deterministic_production_files": len(PRODUCTION_FILES),
        "production_checks": result["algebra_check_count"],
        "independent_checks": independent_result["check_count"],
        "exercised_catch_proofs": independent_result["catch_count"],
        "maximum_supported_conclusion": result["maximum_supported_conclusion"],
    }
    (HERE / "VERIFICATION_RESULT.json").write_text(json.dumps(output, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
