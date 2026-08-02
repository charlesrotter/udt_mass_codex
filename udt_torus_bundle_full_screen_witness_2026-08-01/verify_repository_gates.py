#!/usr/bin/env python3
"""Replay frozen packages, current navigation, premise guards, links, and tests."""

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


def table(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def run(command: list[str], timeout: int) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, cwd=ROOT, text=True, capture_output=True, timeout=timeout, check=False)


def main() -> int:
    members = 0; identities = []
    for relative in MANIFESTS:
        manifest = ROOT / relative
        for line in manifest.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            expected, member = line.split(None, 1); target = manifest.parent / member.strip()
            assert target.is_file() and digest(target) == expected; members += 1
        identities.append(f"{digest(manifest)}  {relative}")
    assert members == 127
    (HERE / "FROZEN_MANIFEST_STDOUT.txt").write_text("\n".join(identities + [f"PASS six frozen manifests; members={members}; package_paths={members + 6}"]) + "\n", encoding="utf-8")

    premise = run(["python3", "verify_current_scientific_premises.py"], 60)
    (HERE / "PREMISE_VERIFIER_STDOUT.txt").write_text(premise.stdout + premise.stderr, encoding="utf-8")
    assert premise.returncode == 0 and "PASS: 18 premise guards, 9 startup controls, 754 candidate dispositions" in premise.stdout

    current = table(ROOT / "research/_registry/CURRENT_ARTIFACT_PATHS.tsv")
    current_paths = [row["current_path"] for row in current]
    assert len(current) == len(set(current_paths)) == 1114 and all((ROOT / path).exists() for path in current_paths)
    frontier = table(ROOT / "research/_registry/CURRENT_FRONTIER_TARGETS.tsv")
    targets = {row["target_path"].rstrip("/") for row in frontier}
    assert len(frontier) == 306 and len(targets) == 101 and all((ROOT / target).exists() for target in targets)

    pattern = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
    links = 0
    for source in HERE.glob("*.md"):
        for raw in pattern.findall(source.read_text(encoding="utf-8")):
            target = raw.strip().strip("<>")
            if target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            relative = unquote(target.split("#", 1)[0])
            assert source.parent.joinpath(relative).resolve().exists(), (source, relative); links += 1

    tests = run(["python3", "-m", "pytest", "-q", "tests"], 300)
    assert tests.returncode == 0 and "70 passed, 1 xfailed" in tests.stdout
    # Pytest's elapsed wall time is nondeterministic evidence noise. Preserve every
    # semantic line while normalizing only that terminal duration before hashing.
    test_capture = re.sub(
        r"in \d+(?:\.\d+)?s(?=\n?$)",
        "in <elapsed>s",
        tests.stdout + tests.stderr,
    )
    (HERE / "REPOSITORY_TEST_STDOUT.txt").write_text(test_capture, encoding="utf-8")
    output = {"status": "PASS", "frozen_manifests": 6, "frozen_manifest_members": members, "frozen_package_paths": members + 6, "premise_verifier": "18 premise guards; 9 startup controls; 754 candidate dispositions", "current_paths": len(current), "frontier_rows": len(frontier), "frontier_targets": len(targets), "package_links": links, "tests": "70 passed, 1 xfailed"}
    (HERE / "REPOSITORY_GATES.json").write_text(json.dumps(output, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(output, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
