#!/usr/bin/env python3
"""Repository preservation gates for the branch reconciliation."""

from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path


PKG = Path(__file__).resolve().parent
ROOT = PKG.parent
MANIFESTS = [
    "native_action_stage1_2026-07-18/arm_A/SHA256SUMS.txt",
    "native_action_stage1_2026-07-18/arm_B/SHA256SUMS.txt",
    "native_action_stage2_2026-07-18/arm_A/SHA256SUMS.txt",
    "native_action_stage2_2026-07-18/arm_B/SHA256SUMS.txt",
    "native_action_arm_c_2026-07-18/SHA256SUMS.txt",
    "native_action_final_adjudication_2026-07-18/SHA256SUMS.txt",
]


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            value.update(block)
    return value.hexdigest()


def main() -> None:
    members = 0
    manifest_lines = []
    for relative in MANIFESTS:
        manifest = ROOT / relative
        for line in manifest.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            expected, member = line.split(None, 1)
            target = manifest.parent / member.strip()
            if not target.is_file() or digest(target) != expected:
                raise AssertionError(target)
            members += 1
        manifest_lines.append(f"{digest(manifest)}  {relative}")
    manifest_lines.append(f"PASS six frozen manifests; members={members}; package_paths={members + 6}")
    (PKG / "FROZEN_MANIFEST_STDOUT.txt").write_text("\n".join(manifest_lines) + "\n", encoding="utf-8")

    premise = subprocess.run(
        ["python3", "verify_current_scientific_premises.py"], cwd=ROOT, text=True,
        capture_output=True, timeout=60, check=False,
    )
    (PKG / "PREMISE_VERIFIER_STDOUT.txt").write_text(premise.stdout + premise.stderr, encoding="utf-8")
    if premise.returncode != 0 or "PASS: 18 premise guards, 9 startup controls, 754 candidate dispositions" not in premise.stdout:
        raise AssertionError("premise verifier")

    tests = subprocess.run(
        ["python3", "-m", "pytest", "-q", "tests"], cwd=ROOT, text=True,
        capture_output=True, timeout=300, check=False,
    )
    (PKG / "REPOSITORY_TEST_STDOUT.txt").write_text(tests.stdout + tests.stderr, encoding="utf-8")
    if tests.returncode != 0 or "70 passed, 1 xfailed" not in tests.stdout:
        raise AssertionError("repository tests")

    result = {
        "status": "PASS",
        "frozen_manifests": 6,
        "frozen_manifest_members": members,
        "frozen_package_paths": members + 6,
        "premise_verifier": "18 premise guards; 9 startup controls; 754 candidate dispositions",
        "tests": "70 passed, 1 xfailed",
    }
    (PKG / "REPOSITORY_GATES.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
