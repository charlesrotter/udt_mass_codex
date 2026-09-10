#!/usr/bin/env python3
"""Preservation and registered-output checks for the scoped maintenance review."""
import hashlib
import json
import os
from pathlib import Path
import shlex
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[2]
REVIEW = Path(__file__).resolve().parent
BASELINE = "51f189679d4029d750e375be949f41e2f15420fa"


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def main():
    result = {"baseline": BASELINE, "python_version": sys.version, "commands": [], "authority_preservation": []}
    for relative in ("verify_current_scientific_premises.py", "CURRENT_SCIENTIFIC_PREMISES.tsv", "CANON.md",
                     "UDT_METRIC_KERNEL_DEVELOPMENT.md", "UDT_METRIC_KERNEL_COVERAGE.tsv"):
        old = subprocess.check_output(["git", "show", f"{BASELINE}:{relative}"], cwd=ROOT)
        current = (ROOT / relative).read_bytes()
        require(old == current, f"Protected authority/science changed: {relative}")
        result["authority_preservation"].append({"path": relative, "unchanged": True,
            "baseline_sha256": hashlib.sha256(old).hexdigest(), "current_sha256": hashlib.sha256(current).hexdigest()})
    package = ROOT / "udt_g326_g324_homogeneous_offdiagonal_linear_modes_2026-09-02"
    with tempfile.TemporaryDirectory(prefix="review_g326_output_", dir="/tmp") as temporary:
        scratch = Path(temporary) / "package"
        shutil.copytree(package, scratch, ignore=shutil.ignore_patterns(".review_runtime", "__pycache__"))
        command = shlex.split((scratch / "REPLAY_COMMANDS.txt").read_text().splitlines()[3])
        env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
        completed = subprocess.run(command, cwd=scratch, capture_output=True, text=True, timeout=40, env=env)
        result["commands"].append({"argv": command, "cwd": str(scratch), "returncode": completed.returncode,
                                  "stdout": completed.stdout, "stderr": completed.stderr})
        require(completed.returncode == 0, "Registered G326 output command failed")
        emitted = (scratch / ".review_runtime/PACKAGE_VERIFICATION_RESULT.json").read_text()
        require(emitted == completed.stdout, "G326 output file differs from stdout")
        require(json.loads(emitted)["exact_scientific_replay"] is True, "G326 output lacks scientific equality")
        require((scratch / "PACKAGE_VERIFICATION_RESULT.json").read_bytes() == (package / "PACKAGE_VERIFICATION_RESULT.json").read_bytes(), "Original aggregate overwritten")
        result["g326_registered_output_matches_stdout_original_aggregate_preserved"] = True
    result["status"] = "PASS_MAINTENANCE_SUPPLEMENT"
    (REVIEW / "supplemental_results.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"status": result["status"], "authority_files_unchanged": len(result["authority_preservation"]),
                      "registered_output_checked": True}, indent=2))


if __name__ == "__main__":
    main()
