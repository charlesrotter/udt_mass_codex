#!/usr/bin/env python3
"""Repository preservation gates for the JR_CERT_NATIVE package."""

from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
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
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


manifest_lines: list[str] = []
manifest_members = 0
for rel in MANIFESTS:
    manifest = ROOT / rel
    base = manifest.parent
    for line in manifest.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        expected, member = line.split(None, 1)
        member_path = base / member.strip()
        assert member_path.is_file(), f"missing frozen member {member_path}"
        assert sha256(member_path) == expected, f"frozen hash mismatch {member_path}"
        manifest_members += 1
    manifest_lines.append(f"{sha256(manifest)}  {rel}")
manifest_lines.append(f"PASS six frozen manifests; members={manifest_members}; package_paths={manifest_members + len(MANIFESTS)}")
(HERE / "FROZEN_MANIFEST_STDOUT.txt").write_text("\n".join(manifest_lines) + "\n", encoding="utf-8")

premise = subprocess.run(
    ["python3", "verify_current_scientific_premises.py"], cwd=ROOT, text=True, capture_output=True, check=False
)
(HERE / "PREMISE_VERIFIER_STDOUT.txt").write_text(premise.stdout + premise.stderr, encoding="utf-8")
assert premise.returncode == 0
assert "PASS: 18 premise guards, 9 startup controls, 754 candidate dispositions" in premise.stdout

tests = subprocess.run(["pytest", "-q"], cwd=ROOT, text=True, capture_output=True, check=False)
(HERE / "REPOSITORY_TEST_STDOUT.txt").write_text(tests.stdout + tests.stderr, encoding="utf-8")
assert tests.returncode == 0
assert "70 passed, 1 xfailed" in tests.stdout

primary_status = subprocess.check_output(["git", "status", "--short", "--branch"], cwd=PRIMARY, text=True)
assert primary_status.strip() == "## grok...origin/grok"

result = {
    "status": "PASS",
    "frozen_manifests": len(MANIFESTS),
    "frozen_manifest_members": manifest_members,
    "frozen_package_paths": manifest_members + len(MANIFESTS),
    "tests": "70 passed, 1 xfailed",
    "premise_verifier": "18 premise guards; 9 startup controls; 754 candidate dispositions",
    "primary_grok_checkout_status": primary_status.strip(),
}
(HERE / "REPOSITORY_GATES.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
print(
    "PASS repository gates: "
    f"manifests={len(MANIFESTS)} package_paths={result['frozen_package_paths']} "
    f"tests={result['tests']} primary={primary_status.strip()}"
)
