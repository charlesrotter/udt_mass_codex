#!/usr/bin/env python3
"""Verify the R5 covariance-subspace correction is frozen before rerun."""

from __future__ import annotations

import ast
from pathlib import Path


HERE = Path(__file__).resolve().parent
CORRECTED_OUTPUTS = (
    "R5_VIEW_SPECTRA.tsv",
    "R5_RANKED_SUBSPACE_OVERLAPS.tsv",
    "R5_COVARIANCE_SUBSPACE_ATLAS.tsv",
    "R5_COVARIANCE_SUBSPACE_SUMMARY.tsv",
    "R5_RESULT.json",
    "R5_OUTPUT_MANIFEST.tsv",
)


def main():
    for name in CORRECTED_OUTPUTS:
        assert not (HERE / name).exists(), f"corrected R5 output already exists: {name}"
    failure = (HERE / "R5_FIRST_ASSEMBLY_METHOD_FAILURE.json").read_text()
    correction = (HERE / "R5_COVARIANCE_SUBSPACE_CORRECTION_PREREGISTRATION.md").read_text()
    source = (HERE / "run_r5_common_subspace_atlas.py").read_text()
    ast.parse(source)
    assert "INDIVIDUAL_MODE_COVARIANCE_ANNOTATION_NOT_INVARIANT" in failure
    for token in (
        "cumulative top-`k` subspace quantities",
        "275,868",
        "2,850",
        "No gap threshold",
        "No individual SVD-vector sign",
    ):
        assert token in correction, token
    for token in (
        "R5_COVARIANCE_SUBSPACE_ATLAS.tsv",
        "subspace_covariance_trace",
        "subspace_range_overlap",
        "difference_projection_norm",
        "global_boundary_absolute_gap",
    ):
        assert token in source, token
    for forbidden in (
        "R5_COVARIANCE_MODE_ATLAS.tsv",
        "signed_difference_projection",
        "mode_standard_deviation",
    ):
        assert forbidden not in source, forbidden
    print("PASS: R5 covariance-subspace correction frozen before rerun")


if __name__ == "__main__":
    main()
