#!/usr/bin/env python3
"""Verify G79 artifacts, numerical gates, repository gates, and protected dirt."""

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
BASE = "26f90fc22271c682fe00ef350eac01b3113a5b9e"
PREREG = "4bea21b7"
MANIFESTS = (
    "native_action_stage1_2026-07-18/arm_A/SHA256SUMS.txt",
    "native_action_stage1_2026-07-18/arm_B/SHA256SUMS.txt",
    "native_action_stage2_2026-07-18/arm_A/SHA256SUMS.txt",
    "native_action_stage2_2026-07-18/arm_B/SHA256SUMS.txt",
    "native_action_arm_c_2026-07-18/SHA256SUMS.txt",
    "native_action_final_adjudication_2026-07-18/SHA256SUMS.txt",
)
PROTECTED_PREFIX = "udt_native_onshell_timelive_reset_owner_audit_2026-08-10/"


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
    assert len(manifest) == len({row["path"] for row in manifest}) == 16
    for row in manifest:
        data = subprocess.check_output(["git", "show", f"{BASE}:{row['path']}"], cwd=ROOT)
        assert hashlib.sha256(data).hexdigest() == row["sha256"]

    expected = {
        "AUDIT_REPORT.md", "CATCH_PROOF_RESULTS.json", "DERIVATION_RESULT.json",
        "EXACT_DERIVATION.md", "INDEPENDENT_VERIFICATION.json", "LAY_REPORT.md",
        "PATH_EVIDENCE.npz", "PREMISE_LEDGER.tsv", "PREREGISTRATION.md",
        "REFINEMENT_ATLAS.tsv", "SOURCE_MANIFEST.tsv", "THERMAL_READOUT_LEDGER.tsv",
        "TYPE_LEDGER.tsv", "derive_same_geometry_sne_query.py", "run_catch_proofs.py",
        "verify_package.py", "verify_same_geometry_sne_independent.py",
    }
    assert expected <= {path.name for path in HERE.iterdir() if path.is_file()}

    result = json.loads((HERE / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    independent = json.loads((HERE / "INDEPENDENT_VERIFICATION.json").read_text(encoding="utf-8"))
    catches = json.loads((HERE / "CATCH_PROOF_RESULTS.json").read_text(encoding="utf-8"))
    assert result["status"] == independent["status"] == catches["status"] == "PASS"
    assert result["source_rows"] == 16
    assert result["selected_profile"]["profile_id"] == independent["profile_id"] == "G75_AM_S01_E05"
    assert result["redshift"]["absolute_direct_analytic_difference"] < 1.0e-10
    assert independent["fine_production_relative"] < 2.0e-4
    assert independent["redshift_absolute_difference"] < 1.0e-10
    assert independent["max_endpoint_null_absolute"] < 1.0e-9
    assert catches["catch_count"] == 12 and all(catches["catches"].values())
    assert len(table(HERE / "REFINEMENT_ATLAS.tsv")) == 3
    assert len(table(HERE / "PREMISE_LEDGER.tsv")) == 12
    assert len(table(HERE / "TYPE_LEDGER.tsv")) == 7
    assert len(table(HERE / "THERMAL_READOUT_LEDGER.tsv")) == 5

    evidence = np.load(HERE / "PATH_EVIDENCE.npz", allow_pickle=False)
    assert evidence["affine"].shape == (501,)
    assert evidence["state"].shape == (32, 501)
    assert evidence["endpoint_D"].shape == (2, 2)
    assert np.allclose(evidence["endpoint_D"], np.asarray(result["endpoint"]["D"]), rtol=0.0, atol=0.0)

    combined = (HERE / "EXACT_DERIVATION.md").read_text(encoding="utf-8") + (HERE / "AUDIT_REPORT.md").read_text(encoding="utf-8")
    for token in (
        "DERIVED_CONDITIONAL_ON_ONE_FROZEN_GEOMETRY_AND_ONE_CHOSEN_STATIONARY_QUERY",
        "The mixing profile is not set to zero",
        "Neither endpoint is last scattering or `X_max`",
        "T_observed(n) = T_source(F_sky(n)) / [1+z(n)]",
        "No CMB temperature or spectrum is predicted",
    ):
        assert token in combined

    premise = run(["python3", "verify_current_scientific_premises.py"], 60)
    assert premise.returncode == 0
    premise_match = re.search(r"PASS: (\d+) premise guards", premise.stdout)
    assert premise_match
    tests = run(["python3", "-m", "pytest", "-q", "tests/"], 300)
    assert tests.returncode == 0
    test_match = re.search(r"(\d+) passed, 1 xfailed", tests.stdout)
    assert test_match

    frozen_members = 0
    for relative in MANIFESTS:
        manifest_path = ROOT / relative
        for line in manifest_path.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            expected_hash, member = line.split(None, 1)
            assert digest(manifest_path.parent / member.strip()) == expected_hash
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
            continue
        unexpected.append(line)
    assert len(protected) == 7 and not unexpected, unexpected

    output = {
        "schema": "udt-cmb-g79-package-verification-v1",
        "status": "PASS",
        "preregistration_commit": PREREG,
        "source_rows": len(manifest),
        "profile_id": result["selected_profile"]["profile_id"],
        "one_plus_z": result["redshift"]["one_plus_z_direct"],
        "dA_over_R": result["distance"]["dA_over_R"],
        "independent_D_relative": independent["fine_production_relative"],
        "catch_proofs": catches["catch_count"],
        "premise_guards": int(premise_match.group(1)),
        "pytest": f"{test_match.group(1)} passed, 1 xfailed",
        "frozen_manifests": len(MANIFESTS),
        "frozen_package_paths": frozen_members + len(MANIFESTS),
        "current_paths": len(current_paths),
        "protected_untracked_paths": len(protected),
        "protected_contents_read": False,
        "unexpected_dirty_paths": unexpected,
    }
    (HERE / "PACKAGE_VERIFICATION.json").write_text(
        json.dumps(output, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

