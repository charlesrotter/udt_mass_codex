#!/usr/bin/env python3
"""Repository preservation gates for the R17 normal-holonomy audit."""

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
PROTECTED = "udt_kernel_plane_global_curvature_holonomy_atlas_2026-08-02/"
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
    "CURRENT_SCIENTIFIC_PREMISES.md",
    "CURRENT_RESEARCH_PROGRAM.md",
    "INFLIGHT_STATE.md",
    "research/README.md",
    "research/_registry/README.md",
)
CURRENT_MUTABLE = frozenset(
    {
        *STARTUP,
        "CURRENT_SCIENTIFIC_PREMISES.tsv",
        "verify_current_scientific_premises.py",
        "tests/test_startup_surface.py",
    }
)


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def table(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream, delimiter="\t"))


def main() -> None:
    premise = subprocess.run(
        ["python3", "verify_current_scientific_premises.py"], cwd=ROOT,
        text=True, capture_output=True, check=False, timeout=60,
    )
    match = re.search(r"PASS: (\d+) premise guards", premise.stdout)
    assert premise.returncode == 0 and match and int(match.group(1)) == 48, premise.stdout + premise.stderr

    source_rows = table(HERE / "SOURCE_MANIFEST.tsv")
    assert len(source_rows) == 12
    for row in source_rows:
        data = subprocess.check_output(["git", "show", row["source_ref"]], cwd=ROOT)
        assert len(data) == int(row["size"]), row["path"]
        assert hashlib.sha256(data).hexdigest() == row["sha256"], row["path"]
        blob = subprocess.check_output(["git", "rev-parse", row["source_ref"]], cwd=ROOT, text=True).strip()
        assert blob == row["git_blob"], row["path"]

    checked_links = 0
    pattern = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
    for source in [*(ROOT / path for path in STARTUP), *HERE.glob("*.md")]:
        assert source.is_file(), source
        for raw in pattern.findall(source.read_text(encoding="utf-8")):
            target = raw.strip().strip("<>")
            if target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            relative = unquote(target.split("#", 1)[0])
            resolved = (
                Path(re.sub(r":\d+$", "", relative))
                if Path(relative).is_absolute()
                else (source.parent / relative).resolve()
            )
            assert resolved.exists(), (source, relative)
            checked_links += 1

    members = 0
    for relative in MANIFESTS:
        manifest = ROOT / relative
        for line in manifest.read_text(encoding="utf-8").splitlines():
            if line.strip():
                expected, member = line.split(None, 1)
                target = manifest.parent / member.strip()
                assert target.is_file() and digest(target) == expected, target
                members += 1
    assert members == 127

    current = table(ROOT / "research/_registry/CURRENT_ARTIFACT_PATHS.tsv")
    paths = [row["current_path"] for row in current]
    assert len(paths) == len(set(paths)) == 1114
    assert all((ROOT / path).exists() for path in paths)
    current_map = {row["original_path"]: row["current_path"] for row in current}
    frontier = table(ROOT / "research/_registry/CURRENT_FRONTIER_TARGETS.tsv")
    targets = {row["target_path"].rstrip("/") for row in frontier}
    resolved = {current_map.get(target, target) for target in targets}
    assert len(frontier) == 306 and len(targets) == 101
    assert all((ROOT / target).exists() for target in resolved)

    tests = subprocess.run(
        ["python3", "-m", "pytest", "-q", "tests/"], cwd=ROOT,
        text=True, capture_output=True, check=False, timeout=300,
    )
    assert tests.returncode == 0 and "88 passed, 1 xfailed" in tests.stdout, tests.stdout + tests.stderr

    status = subprocess.check_output(
        ["git", "status", "--porcelain=v1", "--untracked-files=all"], cwd=ROOT, text=True
    ).splitlines()
    unexpected = []
    for line in status:
        path = line[3:]
        allowed = path.startswith((HERE.name + "/", PROTECTED)) or path in CURRENT_MUTABLE
        if not allowed:
            unexpected.append(line)
    assert not unexpected, unexpected

    result = {
        "schema": "udt-r17-normal-holonomy-repository-gates-v1",
        "status": "PASS",
        "premise_guards": int(match.group(1)),
        "source_manifest_rows": len(source_rows),
        "startup_controls_checked": len(STARTUP),
        "checked_markdown_links": checked_links,
        "frozen_manifests": len(MANIFESTS),
        "frozen_manifest_members": members,
        "frozen_package_paths": members + len(MANIFESTS),
        "current_paths": len(paths),
        "frontier_rows": len(frontier),
        "frontier_targets": len(targets),
        "frontier_resolved_targets": len(resolved),
        "pytest": "88 passed, 1 xfailed",
        "protected_atlas_contents_read": False,
        "unexpected_dirty_paths": unexpected,
    }
    (HERE / "REPOSITORY_GATES.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
