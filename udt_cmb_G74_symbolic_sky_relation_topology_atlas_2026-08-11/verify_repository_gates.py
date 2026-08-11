#!/usr/bin/env python3
"""Live repository gates for the G74 internal review package."""

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
AUTHORIZED_CONTROLS = {
    "CURRENT_RESEARCH_PROGRAM.md", "CURRENT_SCIENTIFIC_PREMISES.md", "HANDOFF.md", "INDEX.md",
    "INFLIGHT_STATE.md", "LIVE.md", "MEMORY.md", "README.md", "research/README.md",
    "research/_registry/README.md",
}
PROTECTED = {
    "udt_native_onshell_timelive_reset_owner_audit_2026-08-10/CANDIDATE_LAW_MAP.tsv",
    "udt_native_onshell_timelive_reset_owner_audit_2026-08-10/DERIVATION_RESULT.json",
    "udt_native_onshell_timelive_reset_owner_audit_2026-08-10/EQUATION_OWNERSHIP_ATLAS.tsv",
    "udt_native_onshell_timelive_reset_owner_audit_2026-08-10/SOURCE_SCOPE_CLARIFICATION.md",
    "udt_native_onshell_timelive_reset_owner_audit_2026-08-10/derive_owner_atlas.py",
    "udt_native_onshell_timelive_reset_owner_audit_2026-08-10/run_catch_proofs.py",
    "udt_native_onshell_timelive_reset_owner_audit_2026-08-10/verify_owner_independent.py",
}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def table(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream, delimiter="\t"))


def run(command: list[str], timeout: int = 300) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, cwd=ROOT, text=True, capture_output=True, timeout=timeout, check=False)


def main() -> None:
    replays = {}
    for name, command, timeout in (
        ("production", ["python3", str(HERE / "derive_topology_atlas.py")], 120),
        ("independent", ["python3", str(HERE / "verify_topology_independent.py")], 420),
        ("catches", ["python3", str(HERE / "run_catch_proofs.py")], 60),
        ("package", ["python3", str(HERE / "verify_package.py")], 60),
    ):
        completed = run(command, timeout)
        assert completed.returncode == 0, completed.stdout + completed.stderr
        replays[name] = hashlib.sha256((completed.stdout + completed.stderr).encode()).hexdigest()

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
            assert target.is_file() and digest(target) == expected
            frozen_members += 1
    assert frozen_members == 127

    premise = run(["python3", "verify_current_scientific_premises.py"], 60)
    assert premise.returncode == 0 and "PASS: 66 premise guards" in premise.stdout

    current = table(ROOT / "research/_registry/CURRENT_ARTIFACT_PATHS.tsv")
    paths = [row["current_path"] for row in current]
    assert len(paths) == len(set(paths)) == 1114 and all((ROOT / path).exists() for path in paths)
    mapping = {row["original_path"]: row["current_path"] for row in current}
    frontier = table(ROOT / "research/_registry/CURRENT_FRONTIER_TARGETS.tsv")
    targets = {row["target_path"].rstrip("/") for row in frontier}
    resolved = {mapping.get(path, path) for path in targets}
    assert len(frontier) == 306 and len(targets) == len(resolved) == 101
    assert all((ROOT / path).exists() for path in resolved)

    link_re = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
    link_count = 0
    docs = [HERE / "AUDIT_REPORT.md", HERE / "EXACT_DERIVATION.md", HERE / "PREREGISTRATION.md"]
    for source in [*(ROOT / path for path in STARTUP), *docs]:
        assert source.is_file()
        for raw in link_re.findall(source.read_text(encoding="utf-8", errors="replace")):
            target = raw.strip().strip("<>")
            if target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            relative = unquote(target.split("#", 1)[0])
            if not relative:
                continue
            target_path = Path(re.sub(r":\d+$", "", relative)) if Path(relative).is_absolute() else (source.parent / relative).resolve()
            assert target_path.exists(), (source, relative)
            link_count += 1

    tests = run(["python3", "-m", "pytest", "-q", "tests/"], 300)
    assert tests.returncode == 0 and "98 passed, 1 xfailed" in tests.stdout, tests.stdout + tests.stderr

    status = run(["git", "status", "--porcelain=v1", "--untracked-files=all"], 60)
    outside = []
    protected_seen = set()
    controls_seen = []
    for line in status.stdout.splitlines():
        path = line[3:]
        if path.startswith(HERE.name + "/"):
            continue
        if path in AUTHORIZED_CONTROLS and not line.startswith("?? "):
            controls_seen.append(line)
            continue
        if path in PROTECTED and line.startswith("?? "):
            protected_seen.add(path)
            continue
        outside.append(line)
    assert protected_seen == PROTECTED and not outside, outside

    payload = {
        "schema": "udt-cmb-g74-repository-gates-v1",
        "status": "PASS",
        "replay_stdout_stderr_sha256": replays,
        "frozen_manifests": 6,
        "frozen_manifest_members": frozen_members,
        "frozen_package_paths": frozen_members + 6,
        "frozen_manifest_hashes": frozen_hashes,
        "premise_guards": 66,
        "current_paths": len(paths),
        "frontier_rows": len(frontier),
        "frontier_targets": len(targets),
        "checked_markdown_links": link_count,
        "pytest": "98 passed, 1 xfailed",
        "authorized_control_changes": controls_seen,
        "protected_untracked_path_count": len(protected_seen),
        "protected_untracked_contents_read": False,
        "unexpected_dirty_paths": outside,
    }
    (HERE / "REPOSITORY_GATES.json").write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
