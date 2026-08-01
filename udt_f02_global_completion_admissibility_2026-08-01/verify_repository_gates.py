#!/usr/bin/env python3
"""Replay frozen manifests, premise guards, and repository tests."""

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
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def run(command: list[str], timeout: int) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, cwd=ROOT, text=True, capture_output=True, timeout=timeout, check=False)


def main() -> None:
    members = 0
    lines = []
    for relative in MANIFESTS:
        manifest = ROOT / relative
        for line in manifest.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            expected, member = line.split(None, 1)
            target = manifest.parent / member.strip()
            assert target.is_file() and digest(target) == expected
            members += 1
        lines.append(f"{digest(manifest)}  {relative}")
    lines.append(f"PASS six frozen manifests; members={members}; package_paths={members + 6}")
    (PKG / "FROZEN_MANIFEST_STDOUT.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")

    premise = run(["python3", "verify_current_scientific_premises.py"], 60)
    (PKG / "PREMISE_VERIFIER_STDOUT.txt").write_text(premise.stdout + premise.stderr, encoding="utf-8")
    assert premise.returncode == 0
    assert "PASS: 18 premise guards, 9 startup controls, 754 candidate dispositions" in premise.stdout

    tests = run(["python3", "-m", "pytest", "-q", "tests"], 300)
    (PKG / "REPOSITORY_TEST_STDOUT.txt").write_text(tests.stdout + tests.stderr, encoding="utf-8")
    assert tests.returncode == 0 and "70 passed, 1 xfailed" in tests.stdout
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
