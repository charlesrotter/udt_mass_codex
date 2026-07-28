#!/usr/bin/env python3
"""Replay determinism and final internal consistency for the bounded atlas."""

from __future__ import annotations

import csv
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent

REPLAY_GROUPS = [
    ("discover_and_freeze_sources.py", ["DISCOVERED_SOURCE_CENSUS.tsv", "EXCLUDED_SEED_CENSUS.tsv"]),
    ("extract_branch_universe.py", [
        "SOURCE_ROLE_CENSUS.tsv", "LOAD_BEARING_SOURCE_MANIFEST.tsv",
        "COMPLETION_CLASS_UNIVERSE.tsv", "CONCRETE_REPRESENTATIVE_UNIVERSE.tsv",
        "NONULTRASTATIC_WITNESS_UNIVERSE.tsv", "TWISTED_PARAMETER_STRATA.tsv",
        "BRANCH_IDENTITY_ALIAS_LEDGER.tsv", "SOURCE_EXTRACTION_RESULT.json",
    ]),
    ("derive_screen_response_atlas.py", [
        "BRANCH_PATH_RESPONSE_ATLAS.tsv", "INTRINSIC_INVARIANT_ATLAS.tsv",
        "COFRAME_GAUGE_ATLAS.tsv", "ROTATION_OWNERSHIP_ATLAS.tsv",
        "GENERATED_ALGEBRA_ATLAS.tsv", "FROZEN_DOF_DIAGNOSTIC.tsv",
        "PAIR_SCREEN_MIXING_ATLAS.tsv", "DEGENERACY_ATLAS.tsv",
        "HOLONOMY_DESCENT_ATLAS.tsv", "SCREEN_COMPONENT_COVERAGE.tsv",
        "COMMON_INTERSECTION_AUDIT.tsv", "BRANCH_PATH_COVERAGE.tsv",
        "TEN_CRITERION_COVERAGE.tsv", "DERIVATION_RESULT.json",
    ]),
    ("verify_screen_response_independent.py", ["CATCH_PROOFS.tsv", "INDEPENDENT_RESULT.json"]),
]


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rows(name: str) -> list[dict[str, str]]:
    with (HERE / name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def main() -> int:
    replay = []
    environment = dict(os.environ)
    environment.update({"CUDA_VISIBLE_DEVICES": "", "PYTHONDONTWRITEBYTECODE": "1"})
    for script, outputs in REPLAY_GROUPS:
        before = {name: sha(HERE / name) for name in outputs}
        process = subprocess.run(
            [sys.executable, str(HERE / script)], cwd=ROOT, env=environment,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=False,
        )
        if process.returncode:
            raise AssertionError(f"{script}: {process.stderr}")
        after = {name: sha(HERE / name) for name in outputs}
        if before != after:
            raise AssertionError(f"nondeterministic replay: {script}")
        replay.append({
            "script": script, "outputs": len(outputs), "result": "BYTE_IDENTICAL",
            "stdout_sha256": hashlib.sha256(process.stdout.encode()).hexdigest(),
            "stderr_sha256": hashlib.sha256(process.stderr.encode()).hexdigest(),
        })

    derivation = json.loads((HERE / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    independent = json.loads((HERE / "INDEPENDENT_RESULT.json").read_text(encoding="utf-8"))
    assert derivation["status"] == "PASS"
    assert derivation["branch_path_rows"] == derivation["unique_record_ids"] == 52
    assert derivation["completion_taxonomy_rows"] == 12
    assert derivation["pair_screen_mixing_rows"] == 7
    assert derivation["mixing_or_mismatch_rows"] == 8
    assert derivation["outcome_class"] == "MIXED_MULTIPLE_OUTCOMES"
    assert independent["catch_proofs"] == 28
    assert independent["allowed_grade"] == "VERIFIED_WITH_CAVEATS"
    assert independent["physical_selection"] is False
    assert independent["fresh_adversarial_model"] is False
    assert len(rows("TEN_CRITERION_COVERAGE.tsv")) == 10
    assert len(rows("CATCH_PROOFS.tsv")) == 28
    status = {r["claim_id"]: r for r in rows("STATUS_LEDGER.tsv")}
    assert len(status) == 14
    assert status["S08"]["status"] == "OBSERVED"
    assert status["S11"]["status"] == "OPEN"
    assert status["S14"]["status"] == "VERIFIED-WITH-CAVEATS"

    result = {
        "schema": "udt-complete-screen-response-audit-verification-1.0",
        "status": "PASS_VERIFIED_WITH_CAVEATS",
        "replay_groups": replay,
        "branch_path_rows": 52,
        "exact_pair_screen_mixing_rows": 7,
        "mixing_or_mismatch_rows": 8,
        "exact_zero_shear_rows": 30,
        "open_generic_jacobi_shear_rows": 3,
        "completion_taxonomy_rows": 12,
        "ten_completeness_stamps": 10,
        "catch_proofs": 28,
        "fresh_adversarial_model": False,
        "maximum_grade": "VERIFIED_WITH_CAVEATS",
        "authority_boundary": {
            "physical_selection": False,
            "action_source_carrier_density_bootstrap_boundary_scale": False,
            "GPU_ODE_PDE_time_live": False,
            "CANON_changed": False,
            "repository_reorganization": False,
        },
    }
    (HERE / "VERIFICATION_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
