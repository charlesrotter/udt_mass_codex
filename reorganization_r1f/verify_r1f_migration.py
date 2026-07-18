#!/usr/bin/env python3
"""Pre-commit verifier for the R1F move and navigation update."""

from __future__ import annotations

import csv
import hashlib
import json
import subprocess
from collections import Counter
from pathlib import Path


BASE = "14ba31a77aed1553c5df8ecd59b0f7a000c10e20"
PREREG_COMMIT = "fa21104"
REPO = Path(__file__).resolve().parents[1]
OUT = REPO / "reorganization_r1f"


def rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git(*args: str) -> str:
    result = subprocess.run(["git", *args], cwd=REPO, text=True, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE, check=False)
    if result.returncode:
        raise AssertionError(result.stderr)
    return result.stdout.strip()


def main() -> int:
    if git("rev-parse", "HEAD")[:7] != PREREG_COMMIT:
        raise AssertionError("migration verifier must run before the migration commit")
    batch = rows(OUT / "PREREGISTERED_BATCH.tsv")
    index = git("ls-files", "-s").splitlines()
    paths_by_oid = {}
    for line in index:
        fields = line.split(None, 3)
        paths_by_oid.setdefault(fields[1], []).append(fields[3])
    for row in batch:
        old, destination = row["current_path"], row["destination"]
        if (REPO / old).exists() or not (REPO / destination).is_file():
            raise AssertionError(f"path state failed: {old}")
        if git("hash-object", "--no-filters", destination) != row["git_blob_oid"]:
            raise AssertionError(f"blob changed: {destination}")
        if sha(REPO / destination) != row["sha256"]:
            raise AssertionError(f"SHA changed: {destination}")
        if paths_by_oid[row["git_blob_oid"]] != [destination]:
            raise AssertionError(f"duplicate blob copy: {old}: {paths_by_oid[row['git_blob_oid']]}")

    changes = git("diff", "--name-status", "--find-renames=100%", PREREG_COMMIT).splitlines()
    expected_renames = {f"R100\t{row['current_path']}\t{row['destination']}" for row in batch}
    actual_renames = {line for line in changes if line.startswith("R")}
    if actual_renames != expected_renames:
        raise AssertionError({"expected_R100": sorted(expected_renames), "actual": sorted(actual_renames)})
    for line in changes:
        fields = line.split("\t")
        status = fields[0]
        target = fields[-1]
        if line in expected_renames:
            continue
        if status == "M" and target in {
            "research/_registry/CURRENT_ARTIFACT_PATHS.tsv", "research/macro/ROOT_INVENTORY.tsv"}:
            continue
        if status == "A" and target.startswith("reorganization_r1f/"):
            continue
        raise AssertionError(f"unauthorized migration diff: {line}")

    if git("diff", "--name-only", BASE, "--", "reorganization_r0", "reorganization_r1a",
           "reorganization_r1b", "reorganization_r1c", "reorganization_r1d", "reorganization_r1e"):
        raise AssertionError("fixed R0-R1E record changed")

    current = rows(REPO / "research/_registry/CURRENT_ARTIFACT_PATHS.tsv")
    if len(current) != 1114 or len({row["original_path"] for row in current}) != 1114 or len({row["current_path"] for row in current}) != 1114:
        raise AssertionError("current map uniqueness failed")
    counts = Counter(row["path_status"] for row in current)
    if counts != Counter({"ROOT_RETAINED": 1109, "MIGRATED_R1D": 1, "MIGRATED_R1F": 4}):
        raise AssertionError(f"current map totals: {counts}")
    current_by_original = {row["original_path"]: row for row in current}
    macro = {row["current_path"]: row for row in rows(REPO / "research/macro/ROOT_INVENTORY.tsv")}
    for item in batch:
        mapped = current_by_original[item["current_path"]]
        if mapped["current_path"] != item["destination"] or mapped["path_status"] != "MIGRATED_R1F":
            raise AssertionError(f"current map mismatch: {item['current_path']}")
        if item["destination"] not in macro or item["current_path"] in macro:
            raise AssertionError(f"macro inventory mismatch: {item['current_path']}")
    if not all((REPO / row["current_path"]).exists() for row in current):
        raise AssertionError("current map missing target")

    pre = {row["original_path"]: row for row in rows(OUT / "pre_move/BEHAVIOR_RUNS.tsv")}
    post = {row["original_path"]: row for row in rows(OUT / "post_move/BEHAVIOR_RUNS.tsv")}
    if set(pre) != set(post) or set(pre) != {row["current_path"] for row in batch}:
        raise AssertionError("behavior coverage mismatch")
    for path in pre:
        for field in ("exit_code", "stdout_size", "stdout_sha256", "stderr_size", "stderr_sha256",
                      "python_version", "python_executable", "sympy_version"):
            if pre[path][field] != post[path][field]:
                raise AssertionError(f"behavior mismatch: {path}:{field}")
        if (REPO / pre[path]["stdout_path"]).read_bytes() != (REPO / post[path]["stdout_path"]).read_bytes():
            raise AssertionError(f"stdout bytes mismatch: {path}")
        if (REPO / pre[path]["stderr_path"]).read_bytes() != (REPO / post[path]["stderr_path"]).read_bytes():
            raise AssertionError(f"stderr bytes mismatch: {path}")
    dependency = json.loads((OUT / "PREMOVE_DEPENDENCY_AUDIT.json").read_text())
    if dependency["result"] != "PASS" or dependency["candidates"] != 4:
        raise AssertionError("dependency audit failed")
    occurrences = rows(OUT / "OLD_PATH_OCCURRENCE_CLASSIFICATION.tsv")
    if not occurrences or any(row["classification"] == "STALE_CURRENT_POINTER" for row in occurrences):
        raise AssertionError("stale current pointer")

    result = {
        "result": "PASS", "mode": "R1F_PRECOMMIT_MIGRATION_VERIFY",
        "base": BASE, "preregistration_commit": git("rev-parse", "HEAD"),
        "r100_renames": 4, "identical_blobs": 4, "identical_sha256": 4,
        "duplicate_copies": 0, "behaviorally_identical": 4,
        "current_map_rows": 1114, "unique_original_paths": 1114, "unique_current_paths": 1114,
        "status_counts": dict(counts), "stale_current_navigation_pointers": 0,
        "fixed_r0_r1e_changes": 0,
    }
    (OUT / "MIGRATION_VERIFY_RESULT.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
