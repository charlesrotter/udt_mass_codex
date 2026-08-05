#!/usr/bin/env python3
"""Repository preservation gates for the law-order architecture audit."""

from __future__ import annotations

import csv
import hashlib
import json
import os
import re
import subprocess
import tempfile
from pathlib import Path
from urllib.parse import unquote


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
BASE = "c2aa6de2"
MANIFESTS = (
    "native_action_stage1_2026-07-18/arm_A/SHA256SUMS.txt",
    "native_action_stage1_2026-07-18/arm_B/SHA256SUMS.txt",
    "native_action_stage2_2026-07-18/arm_A/SHA256SUMS.txt",
    "native_action_stage2_2026-07-18/arm_B/SHA256SUMS.txt",
    "native_action_arm_c_2026-07-18/SHA256SUMS.txt",
    "native_action_final_adjudication_2026-07-18/SHA256SUMS.txt",
)
CONTROLS = (
    "LIVE.md", "HANDOFF.md", "INDEX.md", "README.md", "MEMORY.md",
    "CURRENT_RESEARCH_PROGRAM.md", "CURRENT_SCIENTIFIC_PREMISES.md",
    "UDT_SCIENTIFIC_FRONTIER_2026-07-19.md", "research/README.md",
)
AUTHORIZED_TRACKED = {"LIVE.md", "HANDOFF.md", "INDEX.md", "README.md", "MEMORY.md"}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def table(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def protected_untracked_metadata() -> list[dict[str, str]]:
    raw = subprocess.check_output(
        ["git", "status", "--porcelain=v1", "-z", "--untracked-files=all"], cwd=ROOT
    )
    found = []
    for item in raw.split(b"\0"):
        if not item.startswith(b"?? "):
            continue
        relative = os.fsdecode(item[3:])
        if relative == "CURRENT_RESEARCH_PROGRAM.md" or relative.startswith(HERE.name + "/"):
            continue
        stat = os.lstat(ROOT / relative)
        found.append({
            "path": relative,
            "bytes": str(stat.st_size),
            "mtime_ns": str(stat.st_mtime_ns),
            "mode": oct(stat.st_mode),
            "inode": str(stat.st_ino),
        })
    return sorted(found, key=lambda row: row["path"])


def main() -> None:
    audit = subprocess.run(
        ["python3", str(HERE / "verify_architecture_audit.py")], cwd=ROOT, text=True,
        capture_output=True, timeout=60, check=False,
    )
    assert audit.returncode == 0 and '"status": "PASS"' in audit.stdout, audit.stdout + audit.stderr

    changed = set(subprocess.check_output(
        ["git", "diff", "--name-only", BASE, "--"], cwd=ROOT, text=True
    ).splitlines())
    assert AUTHORIZED_TRACKED < changed
    assert "CURRENT_RESEARCH_PROGRAM.md" in changed
    assert all(
        path in AUTHORIZED_TRACKED
        or path == "CURRENT_RESEARCH_PROGRAM.md"
        or path.startswith(HERE.name + "/")
        for path in changed
    ), changed

    pattern = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
    links = 0
    sources = [ROOT / name for name in CONTROLS]
    sources.extend(HERE.glob("*.md"))
    for source in sources:
        for raw in pattern.findall(source.read_text(encoding="utf-8")):
            target = raw.strip().strip("<>")
            if target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            relative = unquote(target.split("#", 1)[0])
            resolved = (
                Path(re.sub(r":\d+$", "", relative))
                if Path(relative).is_absolute()
                else source.parent.joinpath(relative).resolve()
            )
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

    baseline = sorted(
        table(ROOT / "udt_relational_phi_dependency_regrade_2026-08-05/UNRELATED_UNTRACKED_METADATA.tsv"),
        key=lambda row: row["path"],
    )
    protected = protected_untracked_metadata()
    assert len(baseline) == len(protected) == 83 and baseline == protected

    base_canon = subprocess.check_output(["git", "show", f"{BASE}:CANON.md"], cwd=ROOT)
    assert hashlib.sha256(base_canon).hexdigest() == digest(ROOT / "CANON.md")

    with tempfile.TemporaryDirectory(prefix="udt-law-order-") as tmp:
        env = dict(os.environ)
        env["TMPDIR"] = tmp
        tests = subprocess.run(
            ["python3", "-m", "pytest", "-q", "tests"], cwd=ROOT, text=True,
            capture_output=True, timeout=300, check=False, env=env,
        )
    assert tests.returncode == 0 and "70 passed, 1 xfailed" in tests.stdout, tests.stdout + tests.stderr

    result = {
        "schema": "udt.native_law_order_architecture.repository_gates.v1",
        "status": "PASS",
        "authorized_navigation_mutations": sorted(AUTHORIZED_TRACKED),
        "active_spine_added": True,
        "audit_package_changed_paths": sum(path.startswith(HERE.name + "/") for path in changed),
        "total_authorized_changed_paths": len(changed),
        "checked_links": links,
        "frozen_manifests": len(MANIFESTS),
        "frozen_manifest_members": members,
        "frozen_package_paths": members + len(MANIFESTS),
        "current_paths": len(current_paths),
        "frontier_rows": len(frontier),
        "frontier_targets": len(targets),
        "protected_untracked_metadata_rows": len(protected),
        "canon_unchanged_from_preregistered_base": True,
        "tests": "70 passed, 1 xfailed",
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
