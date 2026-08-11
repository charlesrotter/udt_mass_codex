#!/usr/bin/env python3
"""Verify the G74 sealed snapshot and the advanced live navigation without conflating them."""

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
BASE = "6cc3f29b5b873729f0f8561aefc64aa1a16771be"
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
    "CURRENT_RESEARCH_PROGRAM.md", "CURRENT_SCIENTIFIC_PREMISES.md", "INFLIGHT_STATE.md",
    "research/README.md", "research/_registry/README.md",
)
PROTECTED = {
    "udt_native_onshell_timelive_reset_owner_audit_2026-08-10/CANDIDATE_LAW_MAP.tsv",
    "udt_native_onshell_timelive_reset_owner_audit_2026-08-10/DERIVATION_RESULT.json",
    "udt_native_onshell_timelive_reset_owner_audit_2026-08-10/EQUATION_OWNERSHIP_ATLAS.tsv",
    "udt_native_onshell_timelive_reset_owner_audit_2026-08-10/SOURCE_SCOPE_CLARIFICATION.md",
    "udt_native_onshell_timelive_reset_owner_audit_2026-08-10/derive_owner_atlas.py",
    "udt_native_onshell_timelive_reset_owner_audit_2026-08-10/run_catch_proofs.py",
    "udt_native_onshell_timelive_reset_owner_audit_2026-08-10/verify_owner_independent.py",
}
AUTHORIZED = {
    "CURRENT_RESEARCH_PROGRAM.md", "CURRENT_SCIENTIFIC_PREMISES.md",
    "CURRENT_SCIENTIFIC_PREMISES.tsv", "HANDOFF.md", "INDEX.md", "INFLIGHT_STATE.md",
    "LIVE.md", "MEMORY.md", "README.md", "research/README.md",
    "research/_registry/README.md", "verify_current_scientific_premises.py",
    "tests/test_startup_surface.py",
}


def digest_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def digest(path: Path) -> str:
    return digest_bytes(path.read_bytes())


def table(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream, delimiter="\t"))


def run(command: list[str], timeout: int = 300) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, cwd=ROOT, text=True, capture_output=True, timeout=timeout, check=False)


def main() -> None:
    review_rows = table(HERE / "REVIEW_MANIFEST.tsv")
    assert len(review_rows) == 34
    reviewed = 0
    for row in review_rows:
        if row["path"] == "CURRENT_SCIENTIFIC_PREMISES.tsv":
            data = subprocess.check_output(
                ["git", "show", f"{BASE}:CURRENT_SCIENTIFIC_PREMISES.tsv"], cwd=ROOT
            )
            actual = digest_bytes(data)
        else:
            actual = digest(ROOT / row["path"])
        assert actual == row["sha256"], row["path"]
        reviewed += 1

    external = run(["python3", str(HERE / "verify_external_review_adjudication.py")], 60)
    assert external.returncode == 0 and '"passed": 7' in external.stdout

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
    assert premise.returncode == 0 and "PASS: 67 premise guards" in premise.stdout

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
    docs = [HERE / "EXTERNAL_REVIEW_ADJUDICATION.md", HERE / "EXACT_DERIVATION.md"]
    for source in [*(ROOT / path for path in STARTUP), *docs]:
        assert source.is_file()
        for raw in link_re.findall(source.read_text(encoding="utf-8", errors="replace")):
            target = raw.strip().strip("<>")
            if target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            relative = unquote(target.split("#", 1)[0])
            if not relative:
                continue
            target_path = (
                Path(re.sub(r":\d+$", "", relative))
                if Path(relative).is_absolute()
                else (source.parent / relative).resolve()
            )
            assert target_path.exists(), (source, relative)
            link_count += 1

    tests = run(["python3", "-m", "pytest", "-q", "tests/"], 300)
    assert tests.returncode == 0 and "98 passed, 1 xfailed" in tests.stdout, tests.stdout + tests.stderr

    status = run(["git", "status", "--porcelain=v1", "--untracked-files=all"], 60)
    outside = []
    protected_seen = set()
    for line in status.stdout.splitlines():
        path = line[3:]
        if path.startswith(HERE.name + "/"):
            continue
        if path in AUTHORIZED and not line.startswith("?? "):
            continue
        if path in PROTECTED and line.startswith("?? "):
            protected_seen.add(path)
            continue
        outside.append(line)
    assert protected_seen == PROTECTED and not outside, outside

    payload = {
        "schema": "udt-cmb-g74-post-review-gates-v1",
        "status": "PASS",
        "sealed_review_payloads": reviewed,
        "sealed_root_premise_source": f"{BASE}:CURRENT_SCIENTIFIC_PREMISES.tsv",
        "external_adjudication_checks": 7,
        "premise_guards": 67,
        "frozen_manifests": 6,
        "frozen_manifest_members": frozen_members,
        "frozen_package_paths": frozen_members + 6,
        "frozen_manifest_hashes": frozen_hashes,
        "current_paths": len(paths),
        "frontier_rows": len(frontier),
        "frontier_targets": len(targets),
        "checked_markdown_links": link_count,
        "pytest": "98 passed, 1 xfailed",
        "protected_untracked_path_count": len(protected_seen),
        "protected_untracked_contents_read": False,
        "unexpected_dirty_paths": outside,
    }
    (HERE / "POST_REVIEW_GATES.json").write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
