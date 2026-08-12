#!/usr/bin/env python3
"""Verify the banked BAO data-suitability package without running a UDT fit."""

from __future__ import annotations

import csv
import hashlib
import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parent
DATA = Path("/media/udt-admin/ScratchDisk/Data/BAO/CobayaSampler_bao_data")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def main() -> None:
    result = json.loads((ROOT / "OFFICIAL_DR2_AUDIT_RESULT.json").read_text())
    independent = json.loads((ROOT / "INDEPENDENT_GAUSSIAN_REPLAY.json").read_text())

    mean = DATA / "desi_bao_dr2/desi_gaussian_bao_ALL_GCcomb_mean.txt"
    cov = DATA / "desi_bao_dr2/desi_gaussian_bao_ALL_GCcomb_cov.txt"
    assert sha256(mean) == result["mean_sha256"]
    assert sha256(cov) == result["cov_sha256"] == independent["cov_sha256"]
    assert result["status"] == independent["status"] == "PASS"
    assert result["n_measurements"] == 13
    assert result["quantity_counts"] == {
        "DH_over_rs": 6,
        "DM_over_rs": 6,
        "DV_over_rs": 1,
    }
    assert result["covariance"]["rank"] == 13
    assert result["covariance"]["symmetry_max_abs"] == 0.0
    assert result["covariance"]["eigenvalue_min"] > 0.0
    assert result["gaussian_replay"]["abs_delta"] < 1e-12
    assert float(independent["abs_delta"]) < 1e-12
    assert result["classification"]["origin_interpretation"] == (
        "NONE__OBSERVED_CORRELATION_PATTERN_ONLY"
    )
    assert result["classification"]["full_vector_operational_meaning"] == (
        "FULL_PATTERN_VECTOR_READY_ONLY_WITH_PUBLISHED_NORMALIZATION_NUISANCE"
    )

    with (ROOT / "OFFICIAL_DR2_AP_SHAPE.tsv").open(newline="") as stream:
        rows = list(csv.DictReader(stream, delimiter="\t"))
    assert len(rows) == 6
    assert [float(row["z"]) for row in rows] == [0.510, 0.706, 0.934, 1.321, 1.484, 2.330]
    assert all(float(row["DM_over_DH"]) > 0.0 for row in rows)

    ontology = (ROOT / "ONTOLOGY_CORRECTION.md").read_text()
    for forbidden_import in ("standard ruler", "Lambda-CDM", "acoustic-origin"):
        assert forbidden_import in ontology

    with (ROOT / "LINEAGE_SUITABILITY_ATLAS.tsv").open(newline="") as stream:
        lineages = list(csv.DictReader(stream, delimiter="\t"))
    assert len(lineages) == 6
    assert {row["candidate"] for row in lineages} == {
        "LOCAL_ANGULAR_M2_M3",
        "LOCAL_LYA_SELF_FIT",
        "PUBLISHED_DR1_AP",
        "OFFICIAL_DR2_GAUSSIAN",
        "DR1_FULL_SHAPE_BAO_LIKELIHOOD",
        "RAW_REDUCTION_ROUTE",
    }

    proof = (ROOT / "PREREGISTRATION_COMMIT_PROOF.md").read_text()
    prereg_commit = "1ed1a3a0001ac9fa99ced02bd422b53c86ef6460"
    assert prereg_commit in proof
    assert "f55f3364821ea9b932b095628a43acae8a5c96e6" in proof
    assert subprocess.check_output(
        ["git", "cat-file", "-t", prereg_commit], cwd=ROOT.parent, text=True
    ).strip() == "commit"
    assert subprocess.check_output(
        ["git", "rev-parse", f"{prereg_commit}^{{tree}}"], cwd=ROOT.parent, text=True
    ).strip() == "f55f3364821ea9b932b095628a43acae8a5c96e6"
    subprocess.run(
        ["git", "merge-base", "--is-ancestor", prereg_commit, "origin/grok"],
        cwd=ROOT.parent,
        check=True,
    )
    representation = (ROOT / "TABLE4_REPRESENTATION_NOTE.md").read_text()
    assert "not required to equal" in representation
    review = (ROOT / "EXTERNAL_REVIEW.md").read_text()
    assert "SUSTAINED_VERIFIED_WITH_CAVEATS" in review
    raw_review = (ROOT / "EXTERNAL_REVIEW_RAW.md").read_text()
    assert "019ff7d4-545c-7c21-8448-f711c714b12c" in raw_review
    assert "f04c5bb33c18030b611b9f810439cd8b9b4a812ba5c1b925c6b818c2be2590b7" in raw_review
    adjudication = (ROOT / "EXTERNAL_REVIEW_ADJUDICATION.md").read_text()
    assert "VERIFIED_WITH_CAVEATS__OBSERVED_PATTERN_DATA_SUITABILITY_ONLY" in adjudication

    print("BAO data-suitability package: PASS (13-vector, 6 shape bins, 6 lineages)")


if __name__ == "__main__":
    main()
