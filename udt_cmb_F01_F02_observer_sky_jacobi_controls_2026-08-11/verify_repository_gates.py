#!/usr/bin/env python3
"""Read-only repository gates for the F01/F02 observer-sky Jacobi controls."""

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
    "CURRENT_RESEARCH_PROGRAM.md", "INFLIGHT_STATE.md", "research/README.md",
    "research/_registry/README.md",
)
PROTECTED_UNTRACKED = {
    "udt_native_onshell_timelive_reset_owner_audit_2026-08-10/CANDIDATE_LAW_MAP.tsv",
    "udt_native_onshell_timelive_reset_owner_audit_2026-08-10/DERIVATION_RESULT.json",
    "udt_native_onshell_timelive_reset_owner_audit_2026-08-10/EQUATION_OWNERSHIP_ATLAS.tsv",
    "udt_native_onshell_timelive_reset_owner_audit_2026-08-10/SOURCE_SCOPE_CLARIFICATION.md",
    "udt_native_onshell_timelive_reset_owner_audit_2026-08-10/derive_owner_atlas.py",
    "udt_native_onshell_timelive_reset_owner_audit_2026-08-10/run_catch_proofs.py",
    "udt_native_onshell_timelive_reset_owner_audit_2026-08-10/verify_owner_independent.py",
}
AUTHORIZED_CONTROL_CHANGES = {
    "CURRENT_RESEARCH_PROGRAM.md", "CURRENT_SCIENTIFIC_PREMISES.md",
    "CURRENT_SCIENTIFIC_PREMISES.tsv", "HANDOFF.md", "INDEX.md", "INFLIGHT_STATE.md",
    "LIVE.md", "MEMORY.md", "README.md", "research/README.md",
    "research/_registry/README.md", "tests/test_startup_surface.py",
    "verify_current_scientific_premises.py",
}


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def tsv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream, delimiter="\t"))


def run(command: list[str], timeout: int = 300) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, cwd=ROOT, text=True, capture_output=True, check=False, timeout=timeout)


def main() -> None:
    frozen_members = 0
    frozen_hashes = {}
    for relative in MANIFESTS:
        manifest = ROOT / relative
        frozen_hashes[relative] = digest(manifest)
        for line in manifest.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            expected, member = line.split(None, 1)
            target = manifest.parent / member.strip()
            assert target.is_file() and digest(target) == expected, target
            frozen_members += 1
    assert frozen_members == 127

    premise = run(["python3", "verify_current_scientific_premises.py"], 60)
    assert premise.returncode == 0 and "PASS: 66 premise guards" in premise.stdout, premise.stdout

    current = tsv(ROOT / "research/_registry/CURRENT_ARTIFACT_PATHS.tsv")
    current_paths = [row["current_path"] for row in current]
    assert len(current_paths) == len(set(current_paths)) == 1114
    assert all((ROOT / path).exists() for path in current_paths)
    current_map = {row["original_path"]: row["current_path"] for row in current}

    frontier = tsv(ROOT / "research/_registry/CURRENT_FRONTIER_TARGETS.tsv")
    targets = {row["target_path"].rstrip("/") for row in frontier}
    resolved = {current_map.get(target, target) for target in targets}
    assert len(frontier) == 306 and len(targets) == len(resolved) == 101
    assert all((ROOT / target).exists() for target in resolved)

    link_pattern = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
    link_count = 0
    package_docs = [p for p in HERE.glob("*.md") if p.name != "EXTERNAL_REVIEW_RAW.md"]
    for source in [*(ROOT / path for path in STARTUP), *package_docs]:
        assert source.is_file(), source
        for raw in link_pattern.findall(source.read_text(encoding="utf-8")):
            target = raw.strip().strip("<>")
            if target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            relative = unquote(target.split("#", 1)[0])
            if not relative:
                continue
            resolved_link = Path(re.sub(r":\d+$", "", relative)) if Path(relative).is_absolute() else (source.parent / relative).resolve()
            assert resolved_link.exists(), (source, relative)
            link_count += 1

    tests = run(["python3", "-m", "pytest", "-q", "tests/"], 300)
    assert tests.returncode == 0 and "98 passed, 1 xfailed" in tests.stdout, tests.stdout + tests.stderr

    status = run(["git", "status", "--porcelain=v1", "--untracked-files=all"], 60)
    assert status.returncode == 0
    outside = []
    protected_seen = set()
    authorized_controls_seen = []
    for line in status.stdout.splitlines():
        path = line[3:]
        if path.startswith(HERE.name + "/"):
            continue
        if path in AUTHORIZED_CONTROL_CHANGES and not line.startswith("?? "):
            authorized_controls_seen.append(line)
            continue
        if path in PROTECTED_UNTRACKED and line.startswith("?? "):
            protected_seen.add(path)
            continue
        outside.append(line)
    assert protected_seen == PROTECTED_UNTRACKED
    assert not outside, outside

    result = {
        "schema": "udt-f01-f02-jacobi-repository-gates-v1",
        "status": "PASS", "premise_guards": 66, "startup_controls": len(STARTUP),
        "checked_markdown_links": link_count, "frozen_manifests": len(MANIFESTS),
        "frozen_manifest_members": frozen_members, "frozen_package_paths": frozen_members + len(MANIFESTS),
        "frozen_manifest_hashes": frozen_hashes, "current_paths": len(current_paths),
        "frontier_rows": len(frontier), "frontier_targets": len(targets),
        "pytest": "98 passed, 1 xfailed", "protected_untracked_path_count": len(protected_seen),
        "protected_untracked_contents_read": False, "authorized_control_changes": authorized_controls_seen,
        "unexpected_dirty_paths": outside,
    }
    (HERE / "REPOSITORY_GATES.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
