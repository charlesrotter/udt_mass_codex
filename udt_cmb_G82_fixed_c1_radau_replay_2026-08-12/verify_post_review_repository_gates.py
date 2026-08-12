#!/usr/bin/env python3
"""Replay G82 external-review provenance and repository gates after navigation advances."""

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
REVIEW_BASE = "a9cffc66794707eb68042e372bdb47b1a182de63"
MANIFESTS = (
    "native_action_stage1_2026-07-18/arm_A/SHA256SUMS.txt",
    "native_action_stage1_2026-07-18/arm_B/SHA256SUMS.txt",
    "native_action_stage2_2026-07-18/arm_A/SHA256SUMS.txt",
    "native_action_stage2_2026-07-18/arm_B/SHA256SUMS.txt",
    "native_action_arm_c_2026-07-18/SHA256SUMS.txt",
    "native_action_final_adjudication_2026-07-18/SHA256SUMS.txt",
)
STARTUP = (
    "LIVE.md", "HANDOFF.md", "INDEX.md", "README.md", "MEMORY.md",
    "CURRENT_RESEARCH_PROGRAM.md", "CURRENT_SCIENTIFIC_PREMISES.md", "INFLIGHT_STATE.md",
    "research/README.md", "research/_registry/README.md",
)
AUTHORIZED = {
    "CURRENT_RESEARCH_PROGRAM.md", "CURRENT_SCIENTIFIC_PREMISES.md",
    "CURRENT_SCIENTIFIC_PREMISES.tsv", "HANDOFF.md", "INDEX.md", "INFLIGHT_STATE.md",
    "LIVE.md", "MEMORY.md", "README.md", "research/README.md",
    "research/_registry/README.md", "verify_current_scientific_premises.py",
    "tests/test_startup_surface.py",
    f"{HERE.name}/POST_REVIEW_REPOSITORY_GATES.json",
    f"{HERE.name}/verify_post_review_repository_gates.py",
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
    review_manifest = table(HERE / "REVIEW_MANIFEST.tsv")
    assert len(review_manifest) == 26
    historical_rows = live_rows = 0
    for row in review_manifest:
        if row["path"] == "CURRENT_SCIENTIFIC_PREMISES.tsv":
            shown = subprocess.run(
                ["git", "show", f"{REVIEW_BASE}:{row['path']}"], cwd=ROOT,
                capture_output=True, check=True,
            ).stdout
            assert digest_bytes(shown) == row["sha256"]
            historical_rows += 1
        else:
            assert digest(ROOT / row["path"]) == row["sha256"]
            live_rows += 1
    assert historical_rows == 1 and live_rows == 25
    assert digest(HERE / "REVIEW_MANIFEST.tsv") == "fe2a80592aa3236af5044f91675862be2989cc2209d5b9fefa66c87d6973ac5a"
    assert digest(HERE / "EXTERNAL_REVIEW_RAW.md") == "fb99a23e261e55ce1567a3118feac80a7b239f0e61007841dbfb9f69f0e21ada"
    assert digest(HERE / "EXTERNAL_REVIEW_TRANSCRIPT.txt") == "7944ace16025aaeafb682e7dcbbcd19e4c364e646121da22a80ff3def3b0df66"

    external = run(["python3", str(HERE / "verify_external_review_adjudication.py")], 60)
    assert external.returncode == 0 and '"status": "PASS"' in external.stdout
    premise = run(["python3", "verify_current_scientific_premises.py"], 60)
    assert premise.returncode == 0 and "PASS: 83 premise guards" in premise.stdout

    frozen_members = 0
    frozen_hashes: dict[str, str] = {}
    for relative in MANIFESTS:
        manifest = ROOT / relative
        frozen_hashes[relative] = digest(manifest)
        for line in manifest.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            expected, member = line.split(None, 1)
            assert digest(manifest.parent / member.strip()) == expected
            frozen_members += 1
    assert frozen_members == 127

    current = table(ROOT / "research/_registry/CURRENT_ARTIFACT_PATHS.tsv")
    paths = [row["current_path"] for row in current]
    assert len(paths) == len(set(paths)) == 1114
    assert all((ROOT / path).exists() for path in paths)
    mapping = {row["original_path"]: row["current_path"] for row in current}
    frontier = table(ROOT / "research/_registry/CURRENT_FRONTIER_TARGETS.tsv")
    targets = {row["target_path"].rstrip("/") for row in frontier}
    resolved = {mapping.get(path, path) for path in targets}
    assert len(frontier) == 306 and len(targets) == len(resolved) == 101
    assert all((ROOT / path).exists() for path in resolved)

    link_re = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
    link_count = 0
    for source in [*(ROOT / path for path in STARTUP), HERE / "EXTERNAL_REVIEW_ADJUDICATION.md"]:
        for raw in link_re.findall(source.read_text(encoding="utf-8", errors="replace")):
            target = raw.strip().strip("<>")
            if target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            relative = unquote(target.split("#", 1)[0])
            if not relative:
                continue
            candidate = Path(re.sub(r":\d+$", "", relative))
            target_path = candidate if candidate.is_absolute() else (source.parent / candidate).resolve()
            assert target_path.exists(), (source, relative)
            link_count += 1

    tests = run(["python3", "-m", "pytest", "-q", "tests/"], 300)
    assert tests.returncode == 0 and "103 passed, 1 xfailed" in tests.stdout, tests.stdout + tests.stderr

    status = run(["git", "status", "--porcelain=v1", "--untracked-files=all"], 60)
    protected_seen: set[str] = set()
    outside: list[str] = []
    for line in status.stdout.splitlines():
        path = line[3:]
        if path in AUTHORIZED:
            continue
        if path in PROTECTED and line.startswith("?? "):
            protected_seen.add(path)
            continue
        outside.append(line)
    assert protected_seen == PROTECTED and not outside, outside

    payload = {
        "schema": "udt-cmb-g82-post-review-repository-gates-v1",
        "status": "PASS",
        "sealed_intake_files": 27,
        "sealed_payload_rows": len(review_manifest),
        "review_payload_rows_verified_live": live_rows,
        "review_mutable_registry_row_verified_at_review_base": historical_rows,
        "review_base": REVIEW_BASE,
        "premise_guards": 83,
        "frozen_manifests": len(MANIFESTS),
        "frozen_manifest_members": frozen_members,
        "frozen_package_paths": frozen_members + len(MANIFESTS),
        "frozen_manifest_hashes": frozen_hashes,
        "current_paths": len(paths),
        "frontier_rows": len(frontier),
        "frontier_targets": len(targets),
        "checked_markdown_links": link_count,
        "pytest": "103 passed, 1 xfailed",
        "protected_untracked_path_count": len(protected_seen),
        "protected_untracked_contents_read": False,
        "unexpected_dirty_paths": outside,
    }
    rendered = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    (HERE / "POST_REVIEW_REPOSITORY_GATES.json").write_text(rendered, encoding="utf-8")
    print(rendered, end="")


if __name__ == "__main__":
    main()
