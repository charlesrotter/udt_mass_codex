#!/usr/bin/env python3
"""Replay frozen manifests, premises, navigation, links, and tests."""

from __future__ import annotations

import csv
import hashlib
import json
import re
import subprocess
from pathlib import Path
from urllib.parse import unquote


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
MANIFESTS = [
    "native_action_stage1_2026-07-18/arm_A/SHA256SUMS.txt",
    "native_action_stage1_2026-07-18/arm_B/SHA256SUMS.txt",
    "native_action_stage2_2026-07-18/arm_A/SHA256SUMS.txt",
    "native_action_stage2_2026-07-18/arm_B/SHA256SUMS.txt",
    "native_action_arm_c_2026-07-18/SHA256SUMS.txt",
    "native_action_final_adjudication_2026-07-18/SHA256SUMS.txt",
]


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def run(command: list[str], timeout: int) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command, cwd=ROOT, text=True, capture_output=True, timeout=timeout, check=False
    )


def main() -> int:
    members = 0
    manifest_lines = []
    for relative in MANIFESTS:
        manifest = ROOT / relative
        for line in manifest.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            expected, member = line.split(None, 1)
            target = manifest.parent / member.strip()
            assert target.is_file() and digest(target) == expected
            members += 1
        manifest_lines.append(f"{digest(manifest)}  {relative}")
    assert members == 127
    (HERE / "FROZEN_MANIFEST_STDOUT.txt").write_text(
        "\n".join(
            manifest_lines
            + [f"PASS six frozen manifests; members={members}; package_paths={members + 6}"]
        )
        + "\n",
        encoding="utf-8",
    )

    premise = run(["python3", "verify_current_scientific_premises.py"], 60)
    (HERE / "PREMISE_VERIFIER_STDOUT.txt").write_text(
        premise.stdout + premise.stderr, encoding="utf-8"
    )
    assert premise.returncode == 0
    assert "PASS: 18 premise guards, 9 startup controls, 754 candidate dispositions" in premise.stdout

    current = rows(ROOT / "research/_registry/CURRENT_ARTIFACT_PATHS.tsv")
    current_paths = [row["current_path"] for row in current]
    assert len(current) == len(set(current_paths)) == 1114
    assert all((ROOT / path).exists() for path in current_paths)
    frontier = rows(ROOT / "research/_registry/CURRENT_FRONTIER_TARGETS.tsv")
    targets = {row["target_path"].rstrip("/") for row in frontier}
    assert len(frontier) == 306 and len(targets) == 101
    assert all((ROOT / target).exists() for target in targets)

    link_pattern = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
    link_count = 0
    for source in HERE.glob("*.md"):
        for raw in link_pattern.findall(source.read_text(encoding="utf-8")):
            target = raw.strip().strip("<>")
            if target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            target = unquote(target.split("#", 1)[0])
            assert source.parent.joinpath(target).resolve().exists(), (source, target)
            link_count += 1

    tests = run(["python3", "-m", "pytest", "-q", "tests"], 300)
    (HERE / "REPOSITORY_TEST_STDOUT.txt").write_text(
        tests.stdout + tests.stderr, encoding="utf-8"
    )
    assert tests.returncode == 0 and "70 passed, 1 xfailed" in tests.stdout

    result = {
        "status": "PASS",
        "frozen_manifests": 6,
        "frozen_manifest_members": members,
        "frozen_package_paths": members + 6,
        "premise_verifier": "18 premise guards; 9 startup controls; 754 candidate dispositions",
        "current_paths": len(current),
        "frontier_rows": len(frontier),
        "frontier_targets": len(targets),
        "package_links": link_count,
        "tests": "70 passed, 1 xfailed",
    }
    (HERE / "REPOSITORY_GATES.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

