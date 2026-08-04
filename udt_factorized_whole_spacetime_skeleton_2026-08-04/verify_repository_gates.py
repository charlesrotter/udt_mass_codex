#!/usr/bin/env python3
"""Replay repository preservation gates for the Phase-A skeleton audit."""

from __future__ import annotations

import csv
import hashlib
import json
import os
import re
import subprocess
from pathlib import Path
from urllib.parse import unquote


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
MANIFESTS = (
    "native_action_stage1_2026-07-18/arm_A/SHA256SUMS.txt",
    "native_action_stage1_2026-07-18/arm_B/SHA256SUMS.txt",
    "native_action_stage2_2026-07-18/arm_A/SHA256SUMS.txt",
    "native_action_stage2_2026-07-18/arm_B/SHA256SUMS.txt",
    "native_action_arm_c_2026-07-18/SHA256SUMS.txt",
    "native_action_final_adjudication_2026-07-18/SHA256SUMS.txt",
)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def table(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def run(command: list[str], timeout: int) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, cwd=ROOT, text=True, capture_output=True, timeout=timeout, check=False)


members = 0
for relative in MANIFESTS:
    manifest = ROOT / relative
    for line in manifest.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        expected, member = line.split(None, 1)
        target = manifest.parent / member.strip()
        assert target.is_file() and digest(target) == expected
        members += 1
assert members == 127

premise = run(["python3", "verify_current_scientific_premises.py"], 60)
assert premise.returncode == 0
assert "PASS: 18 premise guards, 9 startup controls, 754 candidate dispositions" in premise.stdout

current = table(ROOT / "research/_registry/CURRENT_ARTIFACT_PATHS.tsv")
current_paths = [row["current_path"] for row in current]
assert len(current) == len(set(current_paths)) == 1114
assert all((ROOT / path).exists() for path in current_paths)

frontier = table(ROOT / "research/_registry/CURRENT_FRONTIER_TARGETS.tsv")
targets = {row["target_path"].rstrip("/") for row in frontier}
assert len(frontier) == 306 and len(targets) == 101
assert all((ROOT / target).exists() for target in targets)

pattern = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
links = 0
for source in HERE.glob("*.md"):
    for raw in pattern.findall(source.read_text(encoding="utf-8")):
        target = raw.strip().strip("<>")
        if target.startswith(("http://", "https://", "mailto:", "#")):
            continue
        relative = unquote(target.split("#", 1)[0])
        assert source.parent.joinpath(relative).resolve().exists(), (source, relative)
        links += 1

# Preserve unrelated untracked artifacts by metadata only; never open their contents.
status = subprocess.check_output(["git", "status", "--porcelain=v1", "-z", "--untracked-files=all"], cwd=ROOT)
unrelated = []
for raw in status.split(b"\0"):
    if not raw.startswith(b"?? "):
        continue
    relative = os.fsdecode(raw[3:])
    if relative.startswith(HERE.name + "/"):
        continue
    stat = (ROOT / relative).stat()
    unrelated.append((relative, str(stat.st_size), str(stat.st_mtime_ns)))
assert len(unrelated) == 83
assert all(path.startswith("udt_kernel_plane_global_curvature_holonomy_atlas_2026-08-02/") for path, _, _ in unrelated)
metadata_path = HERE / "UNRELATED_UNTRACKED_METADATA.tsv"
if metadata_path.exists():
    frozen_metadata = table(metadata_path)
    current_metadata = [
        {"path": path, "bytes": size, "mtime_ns": mtime}
        for path, size, mtime in sorted(unrelated)
    ]
    assert frozen_metadata == current_metadata
else:
    with metadata_path.open("w", newline="") as handle:
        writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
        writer.writerow(("path", "bytes", "mtime_ns"))
        writer.writerows(sorted(unrelated))

tests = run(["python3", "-m", "pytest", "-q", "tests"], 300)
assert tests.returncode == 0 and "70 passed, 1 xfailed" in tests.stdout
capture = re.sub(r"in \d+(?:\.\d+)?s(?=\n?$)", "in <elapsed>s", tests.stdout + tests.stderr)
(HERE / "REPOSITORY_TEST_STDOUT.txt").write_text(capture, encoding="utf-8")

result = {
    "status": "PASS",
    "frozen_manifests": 6,
    "frozen_manifest_members": members,
    "frozen_package_paths": members + 6,
    "premise_guards": 18,
    "startup_controls": 9,
    "candidate_dispositions": 754,
    "current_paths": len(current),
    "frontier_rows": len(frontier),
    "frontier_targets": len(targets),
    "audit_links": links,
    "unrelated_untracked_metadata_rows": len(unrelated),
    "tests": "70 passed, 1 xfailed",
}
(HERE / "REPOSITORY_GATES.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
print(json.dumps(result, sort_keys=True))
