#!/usr/bin/env python3
"""Replay frozen manifests, current premise guards, and repository tests."""

from __future__ import annotations

import hashlib
import csv
import json
import re
import subprocess
from pathlib import Path
from urllib.parse import unquote


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
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(command: list[str], timeout: int):
    return subprocess.run(command, cwd=ROOT, text=True, capture_output=True, timeout=timeout, check=False)


def rows(path: Path):
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def navigation() -> dict[str, int]:
    current = rows(ROOT / "research/_registry/CURRENT_ARTIFACT_PATHS.tsv")
    current_paths = [row["current_path"] for row in current]
    assert len(current) == 1114 and len(set(current_paths)) == 1114
    assert all((ROOT / path).exists() for path in current_paths)

    frontier = rows(ROOT / "research/_registry/CURRENT_FRONTIER_TARGETS.tsv")
    targets = {row["target_path"].rstrip("/") for row in frontier}
    assert len(frontier) == 306 and len(targets) == 101
    assert all((ROOT / path).exists() for path in targets)

    link_pattern = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
    links = []
    for source in PKG.glob("*.md"):
        if source.name == "EXTERNAL_ADVERSARIAL_REVIEW.md":
            continue
        for raw in link_pattern.findall(source.read_text(encoding="utf-8")):
            target = raw.strip().strip("<>")
            if target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            target = unquote(target.split("#", 1)[0])
            links.append(source.parent.joinpath(target).resolve())
    assert all(path.exists() for path in links)
    raw_review = (PKG / "EXTERNAL_ADVERSARIAL_REVIEW.md").read_text(encoding="utf-8")
    raw_review_links = link_pattern.findall(raw_review)
    assert raw_review_links and all(link.startswith("/tmp/udt_reciprocal_closure_review.") for link in raw_review_links)
    return {
        "current_paths": len(current),
        "frontier_rows": len(frontier),
        "frontier_targets": len(targets),
        "package_links": len(links),
        "raw_external_review_ephemeral_links_classified": len(raw_review_links),
    }


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
            assert target.is_file() and digest(target) == expected
            members += 1
        manifest_lines.append(f"{digest(manifest)}  {relative}")
    manifest_lines.append(f"PASS six frozen manifests; members={members}; package_paths={members + 6}")
    (PKG / "FROZEN_MANIFEST_STDOUT.txt").write_text("\n".join(manifest_lines) + "\n", encoding="utf-8")

    premise = run(["python3", "verify_current_scientific_premises.py"], 60)
    (PKG / "PREMISE_VERIFIER_STDOUT.txt").write_text(premise.stdout + premise.stderr, encoding="utf-8")
    assert premise.returncode == 0 and "PASS: 18 premise guards, 9 startup controls, 754 candidate dispositions" in premise.stdout

    tests = run(["python3", "-m", "pytest", "-q", "tests"], 300)
    (PKG / "REPOSITORY_TEST_STDOUT.txt").write_text(tests.stdout + tests.stderr, encoding="utf-8")
    assert tests.returncode == 0 and "70 passed, 1 xfailed" in tests.stdout

    nav = navigation()

    result = {
        "status": "PASS",
        "frozen_manifests": 6,
        "frozen_manifest_members": members,
        "frozen_package_paths": members + 6,
        "premise_verifier": "18 premise guards; 9 startup controls; 754 candidate dispositions",
        "tests": "70 passed, 1 xfailed",
        "navigation": nav,
    }
    (PKG / "REPOSITORY_GATES.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
