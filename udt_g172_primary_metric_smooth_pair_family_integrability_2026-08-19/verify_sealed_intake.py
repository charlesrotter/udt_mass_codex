#!/usr/bin/env python3
"""Dependency-light integrity and replay verifier for a sealed G172 intake."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile


HERE = Path(__file__).resolve().parent
INTAKE = HERE.parent


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


scope_path = INTAKE / "REVIEW_SCOPE.json"
require(scope_path.is_file(), "missing REVIEW_SCOPE.json")
scope = json.loads(scope_path.read_text())
require(scope["package"] == HERE.name, "package name mismatch")
require(scope["files_before_scope"] == len(scope["tree"]), "scope tree count mismatch")
require((HERE / "REVIEW_EXECUTION_BOUNDARY.md").is_file(), "missing execution boundary")

for row in scope["tree"]:
    path = INTAKE / row["path"]
    require(path.is_file(), f"missing sealed file: {row['path']}")
    require(path.stat().st_size == row["bytes"], f"sealed size drift: {row['path']}")
    require(hashlib.sha256(path.read_bytes()).hexdigest() == row["sha256"], f"sealed hash drift: {row['path']}")

source_rows = list(csv.DictReader((HERE / "SOURCE_MANIFEST.tsv").open(), delimiter="\t"))
require(len(source_rows) == 11, "sealed source manifest count")
for row in source_rows:
    source = INTAKE / "sources" / row["path"]
    require(source.is_file(), f"missing sealed source: {row['path']}")
    require(hashlib.sha256(source.read_bytes()).hexdigest() == row["sha256"], f"sealed source hash: {row['path']}")

with tempfile.TemporaryDirectory(prefix="udt_g172_sealed_replay_") as replay_dir:
    replay_root = Path(replay_dir)
    replay_package = replay_root / HERE.name
    shutil.copytree(HERE, replay_package)
    shutil.copytree(INTAKE / "sources", replay_root / "sources")
    for path in replay_root.rglob("*"):
        path.chmod(0o755 if path.is_dir() else 0o644)
    # The production source-hash check is git-backed by design and is therefore exercised by the
    # repository outer gate.  The independent and catch replays are fully sealed/dependency-light.
    for script in ("verify_smooth_pair_family_independent.py", "run_catch_proofs.py"):
        completed = subprocess.run(
            [sys.executable, str(replay_package / script)],
            cwd=replay_root,
            text=True,
            capture_output=True,
            check=False,
        )
        require(completed.returncode == 0, f"sealed replay failed: {script}\n{completed.stdout}\n{completed.stderr}")

    independent = json.loads((replay_package / "INDEPENDENT_VERIFICATION.json").read_text())
    catches = json.loads((replay_package / "CATCH_PROOF_RESULT.json").read_text())

production = json.loads((HERE / "DERIVATION_RESULT.json").read_text())
require(production["checks_passed"] == production["checks_total"] == 26, "sealed production artifact")
require(independent["checks_passed"] == 144000, "independent sealed replay")
require(catches["catches_passed"] == catches["catches_total"] == 19, "catch sealed replay")

result = {
    "gate": "SEALED_INTAKE_REPLAY",
    "status": "PASS__SEALED_G172_DEPENDENCY_LIGHT_REPLAY",
    "sealed_tree_files": len(scope["tree"]),
    "source_hashes": len(source_rows),
    "production_artifact_checks": production["checks_total"],
    "independent_checks": independent["checks_passed"],
    "semantic_catches": catches["catches_total"],
}
print(json.dumps(result, sort_keys=True))
