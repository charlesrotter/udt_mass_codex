#!/usr/bin/env python3
"""Verify G80 artifacts, numerical gates, repository gates, and protected dirt."""

from __future__ import annotations

import csv
import hashlib
import json
import re
import subprocess
from pathlib import Path

import numpy as np


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
BASE = "e5a4a652a62c77d41bb26e7e0d662ebba97fdd41"
PREREG = "76683fa1"
PROTECTED_PREFIX = "udt_native_onshell_timelive_reset_owner_audit_2026-08-10/"
MANIFESTS = (
    "native_action_stage1_2026-07-18/arm_A/SHA256SUMS.txt",
    "native_action_stage1_2026-07-18/arm_B/SHA256SUMS.txt",
    "native_action_stage2_2026-07-18/arm_A/SHA256SUMS.txt",
    "native_action_stage2_2026-07-18/arm_B/SHA256SUMS.txt",
    "native_action_arm_c_2026-07-18/SHA256SUMS.txt",
    "native_action_final_adjudication_2026-07-18/SHA256SUMS.txt",
)


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
    sources = table(HERE / "SOURCE_MANIFEST.tsv")
    assert len(sources) == len({row["path"] for row in sources}) == 10
    for row in sources:
        frozen = subprocess.check_output(["git", "show", f"{BASE}:{row['path']}"], cwd=ROOT)
        assert hashlib.sha256(frozen).hexdigest() == row["sha256"]

    required = {
        "AUDIT_REPORT.md", "CATCH_PROOF_RESULTS.json", "DERIVATION_RESULT.json",
        "EXACT_DERIVATION.md", "INDEPENDENT_VERIFICATION.json", "LAY_REPORT.md",
        "PREMISE_LEDGER.tsv", "PREREGISTRATION.md", "REFINEMENT_ATLAS.tsv",
        "REVERSE_PATH_EVIDENCE.npz", "SOURCE_MANIFEST.tsv", "TYPE_LEDGER.tsv",
        "derive_reverse_pair_reciprocity.py", "run_catch_proofs.py",
        "verify_exact_algebra.py", "verify_package.py", "verify_reverse_pair_independent.py",
    }
    assert required <= {path.name for path in HERE.iterdir() if path.is_file()}
    result = json.loads((HERE / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    independent = json.loads((HERE / "INDEPENDENT_VERIFICATION.json").read_text(encoding="utf-8"))
    catches = json.loads((HERE / "CATCH_PROOF_RESULTS.json").read_text(encoding="utf-8"))
    assert result["status"] == independent["status"] == catches["status"] == "PASS"
    assert result["profile_id"] == "G75_AM_S01_E05"
    assert result["query_type"] == "past_directed_mathematical_reversal_of_same_null_curve_not_future_signal"
    assert all(result["gates"].values())
    assert result["reciprocity"]["D_relative"] < 1.0e-8
    assert result["reciprocity"]["dA_ratio_minus_Z"] < 1.0e-8
    assert independent["reverse_production_relative"] < 2.0e-4
    assert independent["independent_reciprocity_relative"] < 2.0e-4
    assert independent["independent_area_ratio_minus_Z"] < 2.0e-4
    assert catches["catch_count"] == 10 and all(catches["catches"].values())
    assert len(table(HERE / "PREMISE_LEDGER.tsv")) == 12
    assert len(table(HERE / "TYPE_LEDGER.tsv")) == 11
    assert len(table(HERE / "REFINEMENT_ATLAS.tsv")) == 3
    evidence = np.load(HERE / "REVERSE_PATH_EVIDENCE.npz", allow_pickle=False)
    assert evidence["affine"].shape == (501,)
    assert evidence["state"].shape == (32, 501)
    assert evidence["D_forward"].shape == evidence["D_reverse"].shape == (2, 2)

    exact = run(["python3", f"{HERE.name}/verify_exact_algebra.py"], 60)
    assert exact.returncode == 0 and "PASS" in exact.stdout
    premise = run(["python3", "verify_current_scientific_premises.py"], 60)
    assert premise.returncode == 0
    premise_count = int(re.search(r"PASS: (\d+) premise guards", premise.stdout).group(1))
    tests = run(["python3", "-m", "pytest", "-q", "tests/"], 300)
    assert tests.returncode == 0
    test_count = int(re.search(r"(\d+) passed, 1 xfailed", tests.stdout).group(1))

    frozen_members = 0
    for relative in MANIFESTS:
        manifest = ROOT / relative
        for line in manifest.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            expected, member = line.split(None, 1)
            assert digest(manifest.parent / member.strip()) == expected
            frozen_members += 1
    assert frozen_members == 127
    current = table(ROOT / "research/_registry/CURRENT_ARTIFACT_PATHS.tsv")
    current_paths = [row["current_path"] for row in current]
    assert len(current_paths) == len(set(current_paths)) == 1114
    assert all((ROOT / path).exists() for path in current_paths)

    status = run(["git", "status", "--porcelain=v1", "--untracked-files=all"], 60)
    protected, unexpected = [], []
    for line in status.stdout.splitlines():
        path = line[3:]
        if path.startswith(f"{HERE.name}/"):
            continue
        if line.startswith("?? ") and path.startswith(PROTECTED_PREFIX):
            protected.append(path)
        else:
            unexpected.append(line)
    assert len(protected) == 7 and not unexpected, unexpected
    output = {
        "schema": "udt-cmb-g80-package-verification-v1",
        "status": "PASS",
        "scientific_grade": "PROVISIONAL_INTERNALLY_VERIFIED__FRESH_ADVERSARIAL_REVIEW_REQUIRED",
        "preregistration_commit": PREREG,
        "source_rows": len(sources),
        "production_reciprocity_relative": result["reciprocity"]["D_relative"],
        "independent_reciprocity_relative": independent["independent_reciprocity_relative"],
        "catch_proofs": catches["catch_count"],
        "premise_guards": premise_count,
        "pytest": f"{test_count} passed, 1 xfailed",
        "frozen_manifests": len(MANIFESTS),
        "frozen_package_paths": frozen_members + len(MANIFESTS),
        "current_paths": len(current_paths),
        "protected_untracked_paths": len(protected),
        "protected_contents_read": False,
        "reverse_path_sha256": digest(HERE / "REVERSE_PATH_EVIDENCE.npz"),
        "unexpected_dirty_paths": unexpected,
    }
    (HERE / "PACKAGE_VERIFICATION.json").write_text(
        json.dumps(output, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
