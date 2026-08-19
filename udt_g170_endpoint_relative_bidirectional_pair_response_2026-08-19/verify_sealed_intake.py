#!/usr/bin/env python3
"""Read-only standard-library replay for a sealed G170 review intake.

The script never writes inside the intake. It verifies the sealed tree and frozen-source hashes,
copies the package and sources to a temporary directory, and reruns the independent rational and
mutation calculations there. The saved SymPy production artifact is hash-protected by the sealed
tree but is rerun only in the outer repository environment, alongside the premise verifier.
"""

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
require(scope_path.is_file(), "sealed REVIEW_SCOPE.json is required")
scope = json.loads(scope_path.read_text())

for row in scope["tree"]:
    path = INTAKE / row["path"]
    require(path.is_file(), f"sealed file missing: {row['path']}")
    require(path.stat().st_size == row["bytes"], f"sealed size mismatch: {row['path']}")
    require(hashlib.sha256(path.read_bytes()).hexdigest() == row["sha256"], f"sealed hash mismatch: {row['path']}")

manifest_rows = list(csv.DictReader((HERE / "SOURCE_MANIFEST.tsv").open(), delimiter="\t"))
require(len(manifest_rows) == 12, "source manifest count")
for row in manifest_rows:
    copied = INTAKE / "sources" / row["path"]
    require(copied.is_file(), f"copied source missing: {row['path']}")
    require(hashlib.sha256(copied.read_bytes()).hexdigest() == row["sha256"], f"copied source hash: {row['path']}")

with tempfile.TemporaryDirectory(prefix="g170_sealed_replay_") as temporary:
    replay_root = Path(temporary)
    replay_package = replay_root / HERE.name
    shutil.copytree(HERE, replay_package)
    for copied in replay_package.rglob("*"):
        copied.chmod(0o755 if copied.is_dir() else 0o644)

    for row in manifest_rows:
        source = INTAKE / "sources" / row["path"]
        target = replay_root / row["path"]
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)

    commands = ("verify_endpoint_relative_independent.py", "run_catch_proofs.py")
    command_returns: dict[str, int] = {}
    for name in commands:
        completed = subprocess.run(
            [sys.executable, "-S", str(replay_package / name)],
            cwd=replay_root,
            text=True,
            capture_output=True,
            check=False,
        )
        command_returns[name] = completed.returncode
        require(
            completed.returncode == 0,
            f"sealed replay failed: {name}\n{completed.stdout}\n{completed.stderr}",
        )

    independent = json.loads((replay_package / "INDEPENDENT_VERIFICATION.json").read_text())
    catches = json.loads((replay_package / "CATCH_PROOF_RESULT.json").read_text())

production = json.loads((HERE / "DERIVATION_RESULT.json").read_text())
require(production["checks_passed"] == production["checks_total"] == 40, "stored production artifact count")
require(independent["checks_passed"] == 21600, "independent replay count")
require(independent["angular_shift_live"] == independent["angular_trials"] == 1200, "shift-live replay")
require(independent["angular_readout_changed"] == independent["angular_trials"], "angular-live replay")
require(catches["catches_passed"] == catches["catches_total"] == 13, "mutation replay count")
require(independent["no_site"] is True, "independent child did not enforce -S")
require(catches["no_site"] is True, "mutation child did not enforce -S")

result = {
    "status": "PASS__SEALED_STDLIB_REPLAY__SYMPY_ARTIFACT_HASHED__OUTER_GATES_SEPARATE",
    "sealed_tree_files": len(scope["tree"]),
    "frozen_source_hashes": len(manifest_rows),
    "stored_sympy_production_checks": production["checks_total"],
    "sympy_production_replayed_in_sealed_sandbox": False,
    "independent_checks": independent["checks_passed"],
    "mutation_catches": catches["catches_total"],
    "commands": command_returns,
    "child_no_site_flag_enforced": True,
    "child_no_site_flags_observed": {
        "verify_endpoint_relative_independent.py": independent["no_site"],
        "run_catch_proofs.py": catches["no_site"],
    },
}
print(json.dumps(result, sort_keys=True))
