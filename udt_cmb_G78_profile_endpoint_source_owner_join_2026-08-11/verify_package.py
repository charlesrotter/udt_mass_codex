#!/usr/bin/env python3
"""Verify G78 artifacts, preregistration, repository gates, and protected dirt."""

from __future__ import annotations

import csv
import hashlib
import json
import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
BASE = "9a78af889321d84914ae5eb2c066da56bc957719"
PREREG = "bd500a09"
MANIFESTS = (
    "native_action_stage1_2026-07-18/arm_A/SHA256SUMS.txt",
    "native_action_stage1_2026-07-18/arm_B/SHA256SUMS.txt",
    "native_action_stage2_2026-07-18/arm_A/SHA256SUMS.txt",
    "native_action_stage2_2026-07-18/arm_B/SHA256SUMS.txt",
    "native_action_arm_c_2026-07-18/SHA256SUMS.txt",
    "native_action_final_adjudication_2026-07-18/SHA256SUMS.txt",
)
PROTECTED_PREFIX = "udt_native_onshell_timelive_reset_owner_audit_2026-08-10/"
PROTECTED_COUNT = 7


def table(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream, delimiter="\t"))


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(command: list[str], timeout: int = 300) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, cwd=ROOT, text=True, capture_output=True, timeout=timeout, check=False)


def main() -> None:
    assert run(["git", "merge-base", "--is-ancestor", PREREG, "HEAD"]).returncode == 0
    prereg_paths = run(["git", "diff-tree", "--no-commit-id", "--name-only", "-r", PREREG])
    assert set(prereg_paths.stdout.splitlines()) == {
        f"{HERE.name}/PREREGISTRATION.md", f"{HERE.name}/SOURCE_MANIFEST.tsv"
    }

    manifest = table(HERE / "SOURCE_MANIFEST.tsv")
    assert len(manifest) == len({row["path"] for row in manifest}) == 20
    for row in manifest:
        data = subprocess.check_output(["git", "show", f"{BASE}:{row['path']}"], cwd=ROOT)
        assert hashlib.sha256(data).hexdigest() == row["sha256"]

    expected_files = {
        "AUDIT_REPORT.md", "CATCH_PROOF_RESULTS.json", "DEPENDENCY_GRAPH.tsv",
        "DERIVATION_RESULT.json", "EXACT_DERIVATION.md", "INDEPENDENT_VERIFICATION.json",
        "OWNER_ROUTE_LEDGER.tsv", "PREMISE_LEDGER.tsv", "PREREGISTRATION.md",
        "SOURCE_ADJUDICATION.tsv", "SOURCE_MANIFEST.tsv", "derive_owner_join.py",
        "run_catch_proofs.py", "verify_owner_join_independent.py", "verify_package.py",
    }
    assert expected_files <= {path.name for path in HERE.iterdir() if path.is_file()}
    assert len(table(HERE / "OWNER_ROUTE_LEDGER.tsv")) == 7
    assert len(table(HERE / "SOURCE_ADJUDICATION.tsv")) == 20
    assert len(table(HERE / "PREMISE_LEDGER.tsv")) == 12

    result = json.loads((HERE / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    independent = json.loads((HERE / "INDEPENDENT_VERIFICATION.json").read_text(encoding="utf-8"))
    catches = json.loads((HERE / "CATCH_PROOF_RESULTS.json").read_text(encoding="utf-8"))
    assert result["status"] == independent["status"] == catches["status"] == "PASS"
    assert result["owned_native_routes"] == independent["owned_native_routes"] == 0
    assert result["family"]["profiles"] == independent["profile_rows"] == 591
    assert catches["catch_count"] == 10 and all(catches["catches"].values())

    report = (HERE / "AUDIT_REPORT.md").read_text(encoding="utf-8")
    exact = (HERE / "EXACT_DERIVATION.md").read_text(encoding="utf-8")
    for token in (
        "PROVISIONAL_INTERNALLY_VERIFIED__FRESH_ADVERSARIAL_REVIEW_REQUIRED",
        "NO_PHYSICAL_PROFILE_ENDPOINT_SCALE_OR_SOURCE_OWNER_IN_FROZEN_G78_UNIVERSE",
        "This does **not** mean UDT is scale-free",
        "The control sphere `x=1` is not `X_max`",
        "COMPATIBILITY_ANCHOR_ONLY",
    ):
        assert token in report + exact

    premise = run(["python3", "verify_current_scientific_premises.py"], 60)
    assert premise.returncode == 0 and "PASS: 70 premise guards" in premise.stdout
    tests = run(["python3", "-m", "pytest", "-q", "tests/"], 300)
    assert tests.returncode == 0 and "98 passed, 1 xfailed" in tests.stdout

    frozen_members = 0
    for relative in MANIFESTS:
        manifest_path = ROOT / relative
        for line in manifest_path.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            expected, member = line.split(None, 1)
            assert digest(manifest_path.parent / member.strip()) == expected
            frozen_members += 1
    assert frozen_members == 127

    current = table(ROOT / "research/_registry/CURRENT_ARTIFACT_PATHS.tsv")
    current_paths = [row["current_path"] for row in current]
    assert len(current_paths) == len(set(current_paths)) == 1114
    assert all((ROOT / path).exists() for path in current_paths)

    status = run(["git", "status", "--porcelain=v1", "--untracked-files=all"], 60)
    protected = []
    unexpected = []
    for line in status.stdout.splitlines():
        path = line[3:]
        if path.startswith(f"{HERE.name}/"):
            continue
        if line.startswith("?? ") and path.startswith(PROTECTED_PREFIX):
            protected.append(path)
            continue
        unexpected.append(line)
    assert len(protected) == PROTECTED_COUNT and not unexpected, unexpected

    output = {
        "schema": "udt-cmb-g78-package-verification-v1",
        "status": "PASS",
        "preregistration_commit": PREREG,
        "source_rows": len(manifest),
        "owner_routes": 7,
        "owned_native_routes": 0,
        "profile_rows": 591,
        "catch_proofs": 10,
        "premise_guards": 70,
        "pytest": "98 passed, 1 xfailed",
        "frozen_manifests": len(MANIFESTS),
        "frozen_package_paths": frozen_members + len(MANIFESTS),
        "current_paths": len(current_paths),
        "protected_untracked_paths": len(protected),
        "protected_contents_read": False,
        "unexpected_dirty_paths": unexpected,
    }
    (HERE / "PACKAGE_VERIFICATION.json").write_text(json.dumps(output, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
