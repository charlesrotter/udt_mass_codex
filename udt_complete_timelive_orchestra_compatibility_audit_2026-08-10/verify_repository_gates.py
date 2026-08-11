#!/usr/bin/env python3
"""Repository and evidence-preservation gates for the G60 time-live orchestra audit."""

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
PREREG_COMMIT = "c86094e1"
BASE_COMMIT = "78f925459eb7ee8a4251dcc86460d3c581634bc8"
PROTECTED = "udt_kernel_plane_global_curvature_holonomy_atlas_2026-08-02/"
STOPPED_DRAFTS = frozenset({
    "udt_native_onshell_timelive_reset_owner_audit_2026-08-10/CANDIDATE_LAW_MAP.tsv",
    "udt_native_onshell_timelive_reset_owner_audit_2026-08-10/DERIVATION_RESULT.json",
    "udt_native_onshell_timelive_reset_owner_audit_2026-08-10/EQUATION_OWNERSHIP_ATLAS.tsv",
    "udt_native_onshell_timelive_reset_owner_audit_2026-08-10/SOURCE_SCOPE_CLARIFICATION.md",
    "udt_native_onshell_timelive_reset_owner_audit_2026-08-10/derive_owner_atlas.py",
    "udt_native_onshell_timelive_reset_owner_audit_2026-08-10/run_catch_proofs.py",
    "udt_native_onshell_timelive_reset_owner_audit_2026-08-10/verify_owner_independent.py",
})
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
    "CURRENT_SCIENTIFIC_PREMISES.md", "CURRENT_RESEARCH_PROGRAM.md", "INFLIGHT_STATE.md",
    "research/README.md", "research/_registry/README.md",
)
CURRENT_MUTABLE = frozenset({
    *STARTUP, "CURRENT_SCIENTIFIC_PREMISES.tsv", "verify_current_scientific_premises.py",
    "tests/test_startup_surface.py",
})
PREREG_FILES = (
    "PREREGISTRATION.md", "PONDER_MAP.md", "PREMISE_LEDGER.tsv", "TIMELIVE_AXES.tsv",
    "FALSIFICATION_CONTRACT.tsv", "COMPLETENESS_MAP.md", "SOURCE_MANIFEST.tsv",
    "verify_preregistration.py",
)


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            value.update(block)
    return value.hexdigest()


def table(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream, delimiter="\t"))


def run(script: str, *args: str, timeout: int = 120) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["python3", script, *args], cwd=ROOT, text=True, capture_output=True, check=False,
        timeout=timeout,
    )


def main() -> int:
    ancestry = subprocess.run(
        ["git", "merge-base", "--is-ancestor", PREREG_COMMIT, "HEAD"], cwd=ROOT, check=False,
    )
    assert ancestry.returncode == 0, "preregistration commit is not an ancestor"
    for name in PREREG_FILES:
        frozen = subprocess.check_output(
            ["git", "show", f"{PREREG_COMMIT}:{HERE.name}/{name}"], cwd=ROOT
        )
        assert (HERE / name).read_bytes() == frozen, f"preregistration artifact changed: {name}"

    premise = run("verify_current_scientific_premises.py", timeout=60)
    match = re.search(r"PASS: (\d+) premise guards", premise.stdout)
    assert premise.returncode == 0 and match and int(match.group(1)) == 60, premise.stdout + premise.stderr

    sources = table(HERE / "SOURCE_MANIFEST.tsv")
    assert len(sources) == 13 and len({row["path"] for row in sources}) == 13
    for row in sources:
        frozen = subprocess.check_output(["git", "show", f"{BASE_COMMIT}:{row['path']}"], cwd=ROOT)
        assert hashlib.sha256(frozen).hexdigest() == row["sha256"], row["path"]
        assert PROTECTED.rstrip("/") not in row["path"]
        assert "udt_native_onshell_timelive_reset_owner_audit_2026-08-10" not in row["path"]

    runs = {
        "production": run(f"{HERE.name}/derive_timelive_orchestra.py", "--read-only"),
        "independent": run(f"{HERE.name}/verify_timelive_orchestra_independent.py", "--read-only"),
        "guards": run(f"{HERE.name}/run_catch_proofs.py", "--read-only"),
        "fixed_base": run(f"{HERE.name}/verify_fixed_base_sources.py"),
    }
    assert all(result.returncode == 0 for result in runs.values()), {
        key: result.stdout + result.stderr for key, result in runs.items()
    }
    production = json.loads((HERE / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    independent = json.loads((HERE / "INDEPENDENT_VERIFICATION_RESULT.json").read_text(encoding="utf-8"))
    guards = json.loads((HERE / "CATCH_PROOF_RESULT.json").read_text(encoding="utf-8"))
    assert production["exact_check_count"] == 15
    assert production["compatibility_blocks"] == 3
    assert production["trajectory_families"] == 4
    assert production["status"] == "EXACT_COMPATIBILITY_ORCHESTRA_BUT_NO_EVOLUTION_LAW"
    assert independent["total_exact_trials"] == 1200 and independent["status"] == "PASS"
    assert guards["catch_count"] == guards["caught_count"] == 20 and not guards["failed"]

    raw_hash = digest(HERE / "EXTERNAL_REVIEW_RAW.md")
    assert raw_hash == "1c4b23a660859993a6f68c71687bfc181db321d4619810343fcbecb067408e7b"
    assert "VERIFIED_WITH_CORRECTIONS" in (HERE / "EXTERNAL_REVIEW_RAW.md").read_text(encoding="utf-8")

    checked_links = 0
    pattern = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
    package_markdown = [path for path in HERE.glob("*.md") if path.name != "EXTERNAL_REVIEW_RAW.md"]
    for source in [*(ROOT / path for path in STARTUP), *package_markdown]:
        assert source.is_file(), source
        for raw in pattern.findall(source.read_text(encoding="utf-8")):
            target = raw.strip().strip("<>")
            if target.startswith(("http://", "https://", "mailto:", "#", "/tmp/")):
                continue
            relative = unquote(target.split("#", 1)[0])
            resolved = (
                Path(re.sub(r":\d+$", "", relative)) if Path(relative).is_absolute()
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
    assert tests.returncode == 0 and "96 passed, 1 xfailed" in tests.stdout, tests.stdout + tests.stderr

    status = subprocess.check_output(
        ["git", "status", "--porcelain=v1", "--untracked-files=all"], cwd=ROOT, text=True
    ).splitlines()
    unexpected = []
    for line in status:
        path = line[3:]
        allowed = (
            path.startswith((HERE.name + "/", PROTECTED))
            or path in CURRENT_MUTABLE
            or path in STOPPED_DRAFTS
        )
        if not allowed:
            unexpected.append(line)
    assert not unexpected, unexpected

    result = {
        "schema": "udt-complete-timelive-orchestra-repository-gates-v1",
        "status": "PASS",
        "base_commit": BASE_COMMIT,
        "preregistration_commit": PREREG_COMMIT,
        "preregistration_files_unchanged": len(PREREG_FILES),
        "premise_guards": int(match.group(1)),
        "source_manifest_rows": len(sources),
        "exact_checks": production["exact_check_count"],
        "compatibility_blocks": production["compatibility_blocks"],
        "trajectory_families": production["trajectory_families"],
        "independent_exact_trials": independent["total_exact_trials"],
        "scope_guards": guards["catch_count"],
        "external_verdict": "VERIFIED_WITH_CORRECTIONS",
        "external_review_banked_sha256": raw_hash,
        "external_review_posix_newline_sha256_before_whitespace_normalization": "0e42f81c7a8051bfe967c3f6c14a8202400fce3d6a432efc1e1c5f9c5060bfda",
        "external_review_transient_sha256_before_posix_newline": "992a9cabc69d578d61d39496b912e9664b8697fc86b2601c6816af4aa785d1be",
        "startup_controls_checked": len(STARTUP),
        "checked_markdown_links": checked_links,
        "frozen_manifests": len(MANIFESTS),
        "frozen_manifest_members": members,
        "frozen_package_paths": members + len(MANIFESTS),
        "current_paths": len(paths),
        "frontier_rows": len(frontier),
        "frontier_targets": len(targets),
        "frontier_resolved_targets": len(resolved),
        "pytest": "96 passed, 1 xfailed",
        "protected_atlas_contents_read": False,
        "stopped_historical_drafts_preserved_unbanked": len(STOPPED_DRAFTS),
        "unexpected_dirty_paths": unexpected,
    }
    (HERE / "REPOSITORY_GATES.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
