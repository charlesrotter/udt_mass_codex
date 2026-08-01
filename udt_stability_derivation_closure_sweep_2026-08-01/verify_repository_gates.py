#!/usr/bin/env python3
"""Repository preservation gates for the derivation-closure sweep."""

from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path


PKG = Path(__file__).resolve().parent
ROOT = PKG.parent
PRIMARY = Path("/home/udt-admin/udt_mass_codex")
MANIFESTS = [
    "native_action_stage1_2026-07-18/arm_A/SHA256SUMS.txt",
    "native_action_stage1_2026-07-18/arm_B/SHA256SUMS.txt",
    "native_action_stage2_2026-07-18/arm_A/SHA256SUMS.txt",
    "native_action_stage2_2026-07-18/arm_B/SHA256SUMS.txt",
    "native_action_arm_c_2026-07-18/SHA256SUMS.txt",
    "native_action_final_adjudication_2026-07-18/SHA256SUMS.txt",
]


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def main() -> None:
    lines, members = [], 0
    for rel in MANIFESTS:
        manifest = ROOT / rel
        for line in manifest.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            expected, member = line.split(None, 1)
            target = manifest.parent / member.strip()
            if not target.is_file() or sha256(target) != expected:
                raise RuntimeError(f"frozen manifest failure: {target}")
            members += 1
        lines.append(f"{sha256(manifest)}  {rel}")
    lines.append(f"PASS six frozen manifests; members={members}; package_paths={members + 6}")
    (PKG / "FROZEN_MANIFEST_STDOUT.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")

    premise = subprocess.run(["python3", "verify_current_scientific_premises.py"], cwd=ROOT, text=True, capture_output=True, timeout=60, check=False)
    (PKG / "PREMISE_VERIFIER_STDOUT.txt").write_text(premise.stdout + premise.stderr, encoding="utf-8")
    if premise.returncode != 0 or "PASS: 18 premise guards, 9 startup controls, 754 candidate dispositions" not in premise.stdout:
        raise RuntimeError("scientific premise verifier failed")

    tests = subprocess.run(["pytest", "-q"], cwd=ROOT, text=True, capture_output=True, timeout=300, check=False)
    (PKG / "REPOSITORY_TEST_STDOUT.txt").write_text(tests.stdout + tests.stderr, encoding="utf-8")
    if tests.returncode != 0 or "70 passed, 1 xfailed" not in tests.stdout:
        raise RuntimeError("test baseline changed")

    primary = subprocess.check_output(["git", "status", "--short", "--branch"], cwd=PRIMARY, text=True).strip()
    primary_head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=PRIMARY, text=True).strip()
    if primary != "## grok...origin/grok" or primary_head != "5adeb59dde063770c0619d37b76b03f735d82038":
        raise RuntimeError(f"primary checkout changed: {primary} {primary_head}")

    result = {
        "status": "PASS",
        "frozen_manifests": 6,
        "frozen_manifest_members": members,
        "frozen_package_paths": members + 6,
        "premise_verifier": "18 premise guards; 9 startup controls; 754 candidate dispositions",
        "tests": "70 passed, 1 xfailed",
        "primary_checkout": primary,
        "primary_head": primary_head,
    }
    (PKG / "REPOSITORY_GATES.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"PASS repository gates: manifests=6 package_paths={members + 6} tests=70 passed, 1 xfailed primary={primary}")


if __name__ == "__main__":
    main()
