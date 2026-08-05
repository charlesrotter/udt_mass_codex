#!/usr/bin/env python3
"""Read-only repository preservation gates for the stratified first-jet atlas."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import re
import subprocess
from pathlib import Path
from urllib.parse import unquote


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
OUTPUT = HERE / "REPOSITORY_GATES.json"
MANIFESTS = (
    "native_action_stage1_2026-07-18/arm_A/SHA256SUMS.txt",
    "native_action_stage1_2026-07-18/arm_B/SHA256SUMS.txt",
    "native_action_stage2_2026-07-18/arm_A/SHA256SUMS.txt",
    "native_action_stage2_2026-07-18/arm_B/SHA256SUMS.txt",
    "native_action_arm_c_2026-07-18/SHA256SUMS.txt",
    "native_action_final_adjudication_2026-07-18/SHA256SUMS.txt",
)
STARTUP = (
    "LIVE.md",
    "HANDOFF.md",
    "README.md",
    "INDEX.md",
    "AGENTS.md",
    "MEMORY.md",
    "UDT_SCIENTIFIC_FRONTIER_2026-07-19.md",
    "CURRENT_SCIENTIFIC_PREMISES.md",
    "research/README.md",
    "research/_registry/README.md",
)
UNTRACKED_BASELINE = ROOT / (
    "udt_reciprocal_path_composition_residual_audit_2026-08-04/"
    "UNRELATED_UNTRACKED_METADATA.tsv"
)
OUTCOME = (
    "DERIVED_FULL_METRIC_FIRST_JET_SURJECTION__"
    "DERIVED_JOINT_RECIPROCAL_ANGULAR_CAUSAL_STRATA__"
    "NORMALIZED_REDUCTION_HAS_NO_UNIVERSAL_STRATIFIED_EXTENSION__"
    "NO_KINEMATIC_EVOLUTION_RETURN"
)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def table(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def current_unrelated() -> list[dict[str, str]]:
    raw = subprocess.check_output(
        ["git", "status", "--porcelain=v1", "-z", "--untracked-files=all"], cwd=ROOT
    )
    rows = []
    for item in raw.split(b"\0"):
        if not item.startswith(b"?? "):
            continue
        relative = os.fsdecode(item[3:])
        if relative.startswith(HERE.name + "/"):
            continue
        stat = (ROOT / relative).stat()
        rows.append({"path": relative, "bytes": str(stat.st_size), "mtime_ns": str(stat.st_mtime_ns)})
    return sorted(rows, key=lambda row: row["path"])


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--no-write", action="store_true")
    args = parser.parse_args()

    premise = subprocess.run(
        ["python3", "verify_current_scientific_premises.py"], cwd=ROOT, text=True,
        capture_output=True, check=False, timeout=60,
    )
    assert premise.returncode == 0 and "PASS: 18 premise guards" in premise.stdout

    for name in ("LIVE.md", "HANDOFF.md"):
        content = (ROOT / name).read_text(encoding="utf-8")
        assert content.count("<!-- STARTUP_CURRENT_BEGIN -->") == 1
        assert content.count("<!-- STARTUP_CURRENT_END -->") == 1
        current = content.split("<!-- STARTUP_CURRENT_BEGIN -->", 1)[1].split(
            "<!-- STARTUP_CURRENT_END -->", 1
        )[0]
        assert HERE.name in current and OUTCOME in current
    for name in STARTUP:
        content = (ROOT / name).read_text(encoding="utf-8")
        assert HERE.name in content
        assert "CURRENT_SCIENTIFIC_PREMISES.tsv" in content

    link_pattern = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
    links = 0
    link_sources = [ROOT / name for name in STARTUP]
    link_sources.extend(HERE.glob("*.md"))
    for source in link_sources:
        for raw in link_pattern.findall(source.read_text(encoding="utf-8")):
            target = raw.strip().strip("<>")
            if target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            relative = unquote(target.split("#", 1)[0])
            if Path(relative).is_absolute():
                resolved = Path(re.sub(r":\d+$", "", relative))
            else:
                resolved = source.parent.joinpath(relative).resolve()
            assert resolved.exists(), (source, relative)
            links += 1

    members = 0
    for relative in MANIFESTS:
        manifest = ROOT / relative
        for line in manifest.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            expected, member = line.split(None, 1)
            target = manifest.parent / member.strip()
            assert target.is_file() and digest(target) == expected
            members += 1
    assert members == 127

    current_paths = [row["current_path"] for row in table(ROOT / "research/_registry/CURRENT_ARTIFACT_PATHS.tsv")]
    assert len(current_paths) == len(set(current_paths)) == 1114
    assert all((ROOT / path).exists() for path in current_paths)

    frontier = table(ROOT / "research/_registry/CURRENT_FRONTIER_TARGETS.tsv")
    targets = {row["target_path"].rstrip("/") for row in frontier}
    assert len(frontier) == 306 and len(targets) == 101
    assert all((ROOT / target).exists() for target in targets)

    baseline = table(UNTRACKED_BASELINE)
    unrelated = current_unrelated()
    assert len(baseline) == len(unrelated) == 83
    assert baseline == unrelated

    tests = subprocess.run(
        ["python3", "-m", "pytest", "-q", "tests"], cwd=ROOT, text=True,
        capture_output=True, check=False, timeout=300,
    )
    assert tests.returncode == 0 and "70 passed, 1 xfailed" in tests.stdout

    result = {
        "schema": "udt.full_coframe_first_jet_stratified_transition.repository_gates.v1",
        "status": "PASS",
        "premise_guards": 18,
        "startup_controls": len(STARTUP),
        "checked_links": links,
        "frozen_manifests": len(MANIFESTS),
        "frozen_manifest_members": members,
        "frozen_package_paths": members + len(MANIFESTS),
        "current_paths": len(current_paths),
        "frontier_rows": len(frontier),
        "frontier_targets": len(targets),
        "unrelated_untracked_metadata_rows": len(unrelated),
        "tests": "70 passed, 1 xfailed",
    }
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if not args.no_write:
        OUTPUT.write_text(rendered, encoding="utf-8")
    print(rendered, end="")


if __name__ == "__main__":
    main()
