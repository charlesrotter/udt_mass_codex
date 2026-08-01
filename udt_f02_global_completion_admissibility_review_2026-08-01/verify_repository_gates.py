#!/usr/bin/env python3
"""Replay repository gates without mutating the frozen parent package."""

from __future__ import annotations

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


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def run(command: list[str], timeout: int) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command, cwd=ROOT, text=True, capture_output=True, timeout=timeout, check=False
    )


members = 0
manifest_hashes: dict[str, str] = {}
for relative in MANIFESTS:
    manifest = ROOT / relative
    manifest_hashes[relative] = sha256(manifest)
    for line in manifest.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        expected, member = line.split(None, 1)
        target = manifest.parent / member.strip()
        assert target.is_file() and sha256(target) == expected
        members += 1

premise = run(["python3", "verify_current_scientific_premises.py"], 60)
assert premise.returncode == 0
assert "PASS: 18 premise guards, 9 startup controls, 754 candidate dispositions" in premise.stdout

tests = run(["python3", "-m", "pytest", "-q", "tests"], 300)
assert tests.returncode == 0
assert "70 passed, 1 xfailed" in tests.stdout

result = {
    "status": "PASS",
    "frozen_manifests": len(MANIFESTS),
    "frozen_manifest_members": members,
    "frozen_package_paths": members + len(MANIFESTS),
    "manifest_hashes": manifest_hashes,
    "premise_verifier": "18 premise guards; 9 startup controls; 754 candidate dispositions",
    "tests": "70 passed, 1 xfailed",
    "test_stdout_sha256": hashlib.sha256(tests.stdout.encode()).hexdigest(),
    "test_stderr_sha256": hashlib.sha256(tests.stderr.encode()).hexdigest(),
}
(HERE / "REPOSITORY_GATES.json").write_text(
    json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
)
print(json.dumps(result, indent=2, sort_keys=True))
