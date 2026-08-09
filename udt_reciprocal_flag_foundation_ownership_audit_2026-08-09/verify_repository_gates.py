#!/usr/bin/env python3
"""Read-only repository gates for the reciprocal-flag ownership audit."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
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
STARTUP = (
    "LIVE.md", "HANDOFF.md", "README.md", "INDEX.md", "AGENTS.md", "MEMORY.md",
    "UDT_SCIENTIFIC_FRONTIER_2026-07-19.md", "CURRENT_SCIENTIFIC_PREMISES.md",
    "research/README.md", "research/_registry/README.md",
)
EXTERNAL_INPUTS = {
    "udt_cmb_N03_profile_role_regular_center_map_2026-08-09/udt_missing_rule_cold_review.md",
    "udt_cmb_N03_profile_role_regular_center_map_2026-08-09/verify_udt_missing_rule.py",
    "udt_cmb_N03_profile_role_regular_center_map_2026-08-09/reciprocal_flag_followup_audit.md",
    "udt_cmb_N03_profile_role_regular_center_map_2026-08-09/verify_reciprocal_flag_followup.py",
}


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def table(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream, delimiter="\t"))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=HERE / "REPOSITORY_GATES.json")
    args = parser.parse_args()

    premise = subprocess.run(
        ["python3", "verify_current_scientific_premises.py"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
        timeout=60,
    )
    assert premise.returncode == 0 and "PASS: 34 premise guards" in premise.stdout, premise.stdout + premise.stderr

    link_pattern = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
    link_sources = [ROOT / path for path in STARTUP]
    link_sources.extend(HERE.glob("*.md"))
    checked_links = 0
    for source in link_sources:
        assert source.is_file(), source
        for raw in link_pattern.findall(source.read_text(encoding="utf-8")):
            target = raw.strip().strip("<>")
            if target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            relative = unquote(target.split("#", 1)[0])
            resolved = Path(re.sub(r":\d+$", "", relative)) if Path(relative).is_absolute() else (source.parent / relative).resolve()
            assert resolved.exists(), (source, relative)
            checked_links += 1

    members = 0
    for relative in MANIFESTS:
        manifest = ROOT / relative
        for line in manifest.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            expected, member = line.split(None, 1)
            target = manifest.parent / member.strip()
            assert target.is_file() and digest(target) == expected, target
            members += 1
    assert members == 127

    current_rows = table(ROOT / "research/_registry/CURRENT_ARTIFACT_PATHS.tsv")
    paths = [row["current_path"] for row in current_rows]
    assert len(paths) == len(set(paths)) == 1114
    assert all((ROOT / path).exists() for path in paths)
    current_map = {row["original_path"]: row["current_path"] for row in current_rows}

    frontier = table(ROOT / "research/_registry/CURRENT_FRONTIER_TARGETS.tsv")
    targets = {row["target_path"].rstrip("/") for row in frontier}
    assert len(frontier) == 306 and len(targets) == 101
    resolved_targets = {current_map.get(target, target) for target in targets}
    assert all((ROOT / target).exists() for target in resolved_targets)

    with (HERE / "SOURCE_MANIFEST.tsv").open(newline="", encoding="utf-8") as stream:
        sources = list(csv.DictReader(stream, delimiter="\t"))
    assert len(sources) == 26 == len({row["path"] for row in sources})
    assert all((ROOT / row["path"]).is_file() and digest(ROOT / row["path"]) == row["sha256"] for row in sources)

    tests = subprocess.run(
        ["python3", "-m", "pytest", "-q", "tests/"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
        timeout=300,
    )
    assert tests.returncode == 0 and "83 passed, 1 xfailed" in tests.stdout, tests.stdout + tests.stderr

    status_raw = subprocess.check_output(
        ["git", "status", "--porcelain=v1", "--untracked-files=all"], cwd=ROOT, text=True
    ).splitlines()
    unexpected = []
    for line in status_raw:
        path = line[3:]
        if path.startswith(HERE.name + "/") or path in EXTERNAL_INPUTS:
            continue
        unexpected.append(line)
    assert not unexpected, unexpected

    result = {
        "schema": "udt-reciprocal-flag-foundation-ownership-repository-gates-v1",
        "status": "PASS",
        "premise_guards": 34,
        "startup_controls_checked": len(STARTUP),
        "checked_markdown_links": checked_links,
        "frozen_manifests": len(MANIFESTS),
        "frozen_manifest_members": members,
        "frozen_package_paths": members + len(MANIFESTS),
        "current_paths": len(paths),
        "frontier_rows": len(frontier),
        "frontier_targets": len(targets),
        "frontier_resolved_targets": len(resolved_targets),
        "source_manifest_rows": len(sources),
        "pytest": "83 passed, 1 xfailed",
        "unexpected_dirty_paths": unexpected,
    }
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
