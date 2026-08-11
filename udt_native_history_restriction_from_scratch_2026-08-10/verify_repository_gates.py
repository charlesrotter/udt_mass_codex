#!/usr/bin/env python3
"""Repository and preservation gates for G61."""

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
PREREG_COMMIT = "e7b1beb4"
BASE_COMMIT = "3897ef1152af9ef79fc24aee8fe91403a22e4119"
PROTECTED = "udt_kernel_plane_global_curvature_holonomy_atlas_2026-08-02/"
STOPPED = frozenset({
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
MUTABLE = frozenset({
    *STARTUP, "CURRENT_SCIENTIFIC_PREMISES.tsv", "verify_current_scientific_premises.py",
    "tests/test_startup_surface.py",
})
PREREG_FILES = (
    "PREREGISTRATION.md", "PONDER_MAP.md", "PREMISE_LEDGER.tsv",
    "CANDIDATE_OWNER_CLASSES.tsv", "FALSIFICATION_CONTRACT.tsv", "SOURCE_MANIFEST.tsv",
    "verify_preregistration.py",
)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def table(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream, delimiter="\t"))


def run(script: str, *args: str, timeout: int = 120) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["python3", script, *args], cwd=ROOT, text=True, capture_output=True,
        check=False, timeout=timeout,
    )


def main() -> None:
    assert subprocess.run(
        ["git", "merge-base", "--is-ancestor", PREREG_COMMIT, "HEAD"], cwd=ROOT
    ).returncode == 0
    for name in PREREG_FILES:
        frozen = subprocess.check_output(
            ["git", "show", f"{PREREG_COMMIT}:{HERE.name}/{name}"], cwd=ROOT
        )
        assert (HERE / name).read_bytes() == frozen, name

    premise = run("verify_current_scientific_premises.py", timeout=60)
    match = re.search(r"PASS: (\d+) premise guards", premise.stdout)
    assert premise.returncode == 0 and match and int(match.group(1)) == 61

    sources = table(HERE / "SOURCE_MANIFEST.tsv")
    assert len(sources) == len({row["path"] for row in sources}) == 10
    for row in sources:
        frozen = subprocess.check_output(["git", "show", f"{BASE_COMMIT}:{row['path']}"], cwd=ROOT)
        assert hashlib.sha256(frozen).hexdigest() == row["sha256"], row["path"]
        assert PROTECTED.rstrip("/") not in row["path"]
        assert "udt_native_onshell_timelive_reset_owner_audit_2026-08-10" not in row["path"]

    runs = {
        "production": run(f"{HERE.name}/derive_history_restriction.py", "--read-only"),
        "independent": run(f"{HERE.name}/verify_history_restriction_independent.py", "--read-only"),
        "catches": run(f"{HERE.name}/run_catch_proofs.py", "--read-only"),
        "fixed_base": run(f"{HERE.name}/verify_fixed_base_sources.py"),
    }
    assert all(item.returncode == 0 for item in runs.values()), {
        key: item.stdout + item.stderr for key, item in runs.items()
    }
    production = json.loads((HERE / "DERIVATION_RESULT.json").read_text())
    independent = json.loads((HERE / "INDEPENDENT_VERIFICATION_RESULT.json").read_text())
    catches = json.loads((HERE / "CATCH_PROOF_RESULT.json").read_text())
    assert production["exact_check_count"] == 14 and production["candidate_owner_classes"] == 5
    assert production["genuine_owned_history_restrictions"] == 0
    assert independent["total_exact_trials"] == 900 and independent["status"] == "PASS"
    assert catches["catch_count"] == catches["caught_count"] == 16 and not catches["failed"]
    raw_hash = digest(HERE / "EXTERNAL_REVIEW_RAW.md")
    assert raw_hash == "568f4388a3e903aecad16567dac40beb9b6ef7c1e90608e71932abe1865c87c0"

    checked_links = 0
    pattern = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
    for source in [*(ROOT / name for name in STARTUP), *HERE.glob("*.md")]:
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
    assert len(paths) == len(set(paths)) == 1114 and all((ROOT / path).exists() for path in paths)
    current_map = {row["original_path"]: row["current_path"] for row in current}
    frontier = table(ROOT / "research/_registry/CURRENT_FRONTIER_TARGETS.tsv")
    targets = {row["target_path"].rstrip("/") for row in frontier}
    resolved = {current_map.get(target, target) for target in targets}
    assert len(frontier) == 306 and len(targets) == 101
    assert all((ROOT / target).exists() for target in resolved)

    tests = subprocess.run(
        ["python3", "-m", "pytest", "-q", "tests/"], cwd=ROOT, text=True,
        capture_output=True, check=False, timeout=300,
    )
    assert tests.returncode == 0 and "97 passed, 1 xfailed" in tests.stdout, tests.stdout + tests.stderr

    unexpected = []
    for line in subprocess.check_output(
        ["git", "status", "--porcelain=v1", "--untracked-files=all"], cwd=ROOT, text=True
    ).splitlines():
        path = line[3:]
        if not (path.startswith((HERE.name + "/", PROTECTED)) or path in MUTABLE or path in STOPPED):
            unexpected.append(line)
    assert not unexpected, unexpected

    result = {
        "schema": "udt-native-history-restriction-repository-gates-v1",
        "status": "PASS",
        "base_commit": BASE_COMMIT,
        "preregistration_commit": PREREG_COMMIT,
        "preregistration_files_unchanged": len(PREREG_FILES),
        "premise_guards": int(match.group(1)),
        "source_manifest_rows": len(sources),
        "exact_checks": production["exact_check_count"],
        "candidate_owner_classes": production["candidate_owner_classes"],
        "selected_history_restrictions": production["genuine_owned_history_restrictions"],
        "independent_exact_trials": independent["total_exact_trials"],
        "scope_guards": catches["catch_count"],
        "external_verdict": "VERIFIED_WITH_CORRECTIONS",
        "external_review_banked_sha256": raw_hash,
        "external_review_transient_sha256": "76f1e09c40f923875aae7025371863acf83a3ff3bf1296edabd6567e6c5c1cff",
        "startup_controls_checked": len(STARTUP),
        "checked_markdown_links": checked_links,
        "frozen_manifests": len(MANIFESTS),
        "frozen_manifest_members": members,
        "frozen_package_paths": members + len(MANIFESTS),
        "current_paths": len(paths),
        "frontier_rows": len(frontier),
        "frontier_targets": len(targets),
        "pytest": "97 passed, 1 xfailed",
        "protected_atlas_contents_read": False,
        "stopped_historical_drafts_preserved_unbanked": len(STOPPED),
        "unexpected_dirty_paths": unexpected,
    }
    (HERE / "REPOSITORY_GATES.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
