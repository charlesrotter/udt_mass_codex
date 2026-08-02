#!/usr/bin/env python3
"""Replay repository gates when banking the external-review closure."""

from __future__ import annotations

import csv
import hashlib
import json
import subprocess
from pathlib import Path


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


def table(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def main() -> int:
    members = 0
    identities: list[str] = []
    for relative in MANIFESTS:
        manifest = ROOT / relative
        for line in manifest.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            expected, member = line.split(None, 1)
            target = manifest.parent / member.strip()
            assert target.is_file() and digest(target) == expected
            members += 1
        identities.append(f"{digest(manifest)}  {relative}")
    assert members == 127
    (HERE / "FROZEN_MANIFEST_STDOUT.txt").write_text(
        "\n".join(identities + [f"PASS six frozen manifests; members={members}; package_paths={members + 6}"]) + "\n",
        encoding="utf-8",
    )

    premise = subprocess.run(
        ["python3", "verify_current_scientific_premises.py"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        timeout=60,
        check=False,
    )
    (HERE / "PREMISE_VERIFIER_STDOUT.txt").write_text(
        premise.stdout + premise.stderr, encoding="utf-8"
    )
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

    tests = subprocess.run(
        ["python3", "-m", "pytest", "-q", "tests"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        timeout=300,
        check=False,
    )
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
        "tests": "70 passed, 1 xfailed",
    }
    (HERE / "REPOSITORY_GATES.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
