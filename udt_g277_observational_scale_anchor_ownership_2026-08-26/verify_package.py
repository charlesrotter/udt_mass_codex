#!/usr/bin/env python3
"""Package and no-write replay verification for G277."""

from __future__ import annotations

import csv
import hashlib
import json
import subprocess
import sys
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
OUT = HERE / "PACKAGE_VERIFICATION.json"


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def verify_sources() -> int:
    count = 0
    with (HERE / "SOURCE_MANIFEST.tsv").open(newline="") as stream:
        for row in csv.DictReader(stream, delimiter="\t"):
            path = Path(row["path"])
            if not path.is_absolute():
                path = ROOT / path
            assert digest(path) == row["sha256"]
            assert "udt_native_onshell_timelive_reset" not in str(path)
            assert "udt_pair_regime_flow" not in str(path)
            assert "udt_sne_xmax_G88" not in str(path)
            assert "udt_kernel_plane_global_curvature" not in str(path)
            count += 1
    return count


def no_write_replays() -> dict[str, str]:
    artifacts = [
        HERE / "DERIVATION_RESULT.json",
        HERE / "ANCHOR_CLASSIFICATION.tsv",
        HERE / "DATA_SCHEMA_AUDIT.tsv",
        HERE / "COVARIANCE_RANK_AUDIT.tsv",
        HERE / "INDEPENDENT_VERIFICATION.json",
        HERE / "CATCH_PROOF_RESULT.json",
    ]
    before = {path.name: digest(path) for path in artifacts}
    commands = [
        [sys.executable, str(HERE / "derive_anchor_ownership.py"), "--no-write"],
        [sys.executable, str(HERE / "verify_anchor_ownership_independent.py"), "--no-write"],
        [sys.executable, str(HERE / "run_catch_proofs.py"), "--no-write"],
    ]
    for command in commands:
        completed = subprocess.run(command, cwd=ROOT, check=False, capture_output=True, text=True)
        assert completed.returncode == 0, completed.stderr
    after = {path.name: digest(path) for path in artifacts}
    assert before == after
    return after


def main() -> None:
    source_count = verify_sources()
    production = json.loads((HERE / "DERIVATION_RESULT.json").read_text())
    independent = json.loads((HERE / "INDEPENDENT_VERIFICATION.json").read_text())
    catches = json.loads((HERE / "CATCH_PROOF_RESULT.json").read_text())
    assert production["status"] == "PASS"
    assert independent["status"] == "VERIFIED_WITH_CAVEATS"
    assert catches["status"] == "PASS" and catches["rejected_overclaims"] == 11
    required_catch_criteria = {
        "independent",
        "nonzero_weight",
        "zero_point_closed",
        "same_object",
        "bridge_owned",
        "source_owned",
        "dimensional_type",
        "populated_boundary",
        "global_completion",
    }
    assert required_catch_criteria.issubset(
        set(catches["failed_criterion_by_overclaim"].values())
    )
    assert catches["unconditional_true_controls"] == 0
    assert catches["phrase_anywhere_controls"] == 0
    assert catches["literal_missing_column_semantic_controls"] == 0
    assert not production["observational_fit_performed"]
    assert not production["numerical_scale_computed"]
    assert not production["metric_or_kernel_changed"]
    assert not production["xmax_selected"]
    covariance_rank = production["actual_covariance_weighted_rank"]
    assert not covariance_rank["raw_symmetry_gate_pass"]
    assert covariance_rank["raw_symmetry_defect"] > covariance_rank["raw_symmetry_threshold"]
    assert covariance_rank["actual_design_rank"] == 2
    assert all(route["weighted_rank"] == 2 for route in covariance_rank["symmetric_routes"].values())
    assert all(route["condition_ratio"] > 1e-12 for route in covariance_rank["symmetric_routes"].values())
    assert covariance_rank["max_fisher_relative_difference"] < 1e-4
    assert covariance_rank["max_eigen_relative_difference"] < 1e-4
    assert independent["classification_derived_from_explicit_predicate"]
    assert independent["classification_facts_derived_from_sources_and_computation"]
    with (HERE / "ANCHOR_CLASSIFICATION.tsv").open(newline="") as stream:
        classes = {row["candidate"]: row["classification"] for row in csv.DictReader(stream, delimiter="\t")}
    assert classes["PantheonPlus_CEPH_DIST_calibrators"] == "CONDITIONAL_TRANSFER_OR_DISTANCE_ANCHOR"
    assert classes["DES_Dovekie_alone"] == "RELATIVE_ONLY"
    assert classes["PantheonPlus_relative_plus_DES_relative"] == "RELATIVE_ONLY"
    assert classes["cmb_temp"] == "NOT_CURRENTLY_SCALE_TYPED"
    assert classes["G276_same_segment_proper_clock"] == "DIRECT_NONZERO_WEIGHT_ANCHOR"
    artifact_hashes = no_write_replays()
    result = {
        "status": "PASS",
        "source_hashes_verified": source_count,
        "classification_rows": len(classes),
        "hostile_overclaims_rejected": catches["rejected_overclaims"],
        "no_write_artifact_hashes": artifact_hashes,
        "fit_performed": False,
        "scale_computed": False,
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
