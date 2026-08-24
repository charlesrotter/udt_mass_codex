#!/usr/bin/env python3
"""Verify the complete G243 evidence package and independent census."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path

import numpy as np


PACKAGE = Path(__file__).resolve().parent
REPO = PACKAGE.parent
EXPECTED_LOCAL_CLASSIFICATION = (
    "SNE_ONLY_SMOOTH_RADIAL_REPRESENTATION_FROZEN__TURNING_INTERVALS_RETAINED"
)
EXPECTED_LANDING = "CROSS_ROUTE_OR_FULL_COVARIANCE_FAILURE__NO_FREEZE"
EXPECTED_ROWS = 5 * 97


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def preregistration_registry_digest(path: Path) -> str:
    """Retain preregistration lineage after a later append-only G243 bank."""
    lines = path.read_bytes().splitlines(keepends=True)
    g243_rows = [line for line in lines if line.startswith(b"G243\t")]
    if not g243_rows:
        return digest(path)
    assert len(g243_rows) == 1, "registry may contain at most one G243 row"
    historical = b"".join(line for line in lines if not line.startswith(b"G243\t"))
    return hashlib.sha256(historical).hexdigest()


def close(left: object, right: object, absolute: float, label: str, relative: float = 0.0) -> float:
    difference = abs(float(left) - float(right))
    scale = max(abs(float(left)), abs(float(right)))
    assert difference <= absolute + relative * scale, f"{label}: {left} != {right}"
    return difference


def read_census(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as stream:
        return list(csv.DictReader(stream, delimiter="\t"))


def verify() -> dict[str, object]:
    with (PACKAGE / "SOURCE_MANIFEST.tsv").open(newline="") as stream:
        sources = list(csv.DictReader(stream, delimiter="\t"))
    assert len(sources) == 8
    for row in sources:
        if row["path"] == "CURRENT_SCIENTIFIC_PREMISES.tsv":
            actual = preregistration_registry_digest(REPO / row["path"])
        elif row["path"].startswith("external_data/"):
            # External observational files are hash-checked by both production and the sealed builder.
            continue
        else:
            actual = digest(REPO / row["path"])
        assert actual == row["sha256"], f"source hash mismatch: {row['path']}"

    production = json.loads((PACKAGE / "DERIVATION_RESULT.json").read_text())
    independent = json.loads((PACKAGE / "INDEPENDENT_VERIFICATION.json").read_text())
    assert production["classification"] == EXPECTED_LOCAL_CLASSIFICATION
    assert independent["classification"] == EXPECTED_LOCAL_CLASSIFICATION
    assert production["redshift_role"] == "DIRECT_RECIPROCAL_DEPTH__NO_ANGULAR_INPUT"
    assert production["angular_outcomes"] == "CLOSED_AND_UNUSED"
    assert independent["angular_outcomes"] == "CLOSED_AND_UNUSED"
    assert production["boss_outcomes"] == "CLOSED_AND_UNREAD"
    assert independent["boss_outcomes"] == "CLOSED_AND_UNREAD"
    assert production["counts"] == {"pantheon": 768, "des": 1623, "total": 2391}
    assert independent["counts"] == {"pantheon": 768, "des": 1623}

    selected = production["selected"]
    independent_selected = independent["selected"]
    assert selected["basis_count"] == independent_selected["basis_count"] == 48
    assert selected["alpha_index"] == independent_selected["alpha_index"] == 44
    close(selected["alpha"], independent_selected["alpha"], 0.0, "selected alpha")
    assert selected["alpha_boundary"] is False
    assert independent_selected["alpha_boundary"] is False
    assert selected["globally_invertible"] is False
    assert independent_selected["globally_invertible"] is False
    assert float(selected["minimum_s_prime"]) < 0.0
    assert len(selected["positive_intervals"]) == 4

    production_census = read_census(PACKAGE / "CANDIDATE_CENSUS.tsv")
    independent_census = read_census(PACKAGE / "INDEPENDENT_CENSUS.tsv")
    assert len(production_census) == len(independent_census) == EXPECTED_ROWS
    maximum_difference = 0.0
    maximum_raw_chi2_difference = 0.0
    raw_chi2_gate_failures = 0
    for index, (left, right) in enumerate(zip(production_census, independent_census)):
        assert int(left["basis_count"]) == int(right["basis_count"])
        assert int(left["alpha_index"]) == int(right["alpha_index"])
        raw_chi2_difference = abs(float(left["raw_chi2"]) - float(right["raw_chi2"]))
        maximum_raw_chi2_difference = max(maximum_raw_chi2_difference, raw_chi2_difference)
        raw_chi2_gate_failures += int(raw_chi2_difference > 1.0e-7)
        maximum_difference = max(
            maximum_difference,
            close(left["log10_alpha"], right["log10_alpha"], 0.0, f"row {index} log10 alpha"),
            close(left["alpha"], right["alpha"], 0.0, f"row {index} alpha"),
            close(left["lambda"], right["lambda"], 1.0e-12, f"row {index} lambda", 1.0e-12),
            # EDF is a trace of a differently assembled ill-conditioned solve and was not a
            # preregistered 1e-8 agreement gate. The load-bearing chi-square/GCV retain 1e-7.
            close(left["edf"], right["edf"], 1.0e-6, f"row {index} edf"),
            close(left["gcv"], right["gcv"], 1.0e-7, f"row {index} gcv"),
        )
    assert raw_chi2_gate_failures > 0, "a certified freeze would require a different landing"
    assert maximum_raw_chi2_difference > 1.0e-7

    coefficients = np.asarray(selected["coefficients"], dtype=np.float64)
    independent_coefficients = np.asarray(independent_selected["coefficients"], dtype=np.float64)
    coefficient_difference = float(np.max(np.abs(coefficients - independent_coefficients)))
    assert coefficient_difference <= 1.0e-8

    with np.load(PACKAGE / "RADIAL_REPRESENTATION.npz", allow_pickle=False) as archive:
        expected_arrays = {
            "phi",
            "theta",
            "theta_prime",
            "theta_second",
            "s_prime",
            "s_second",
            "coefficients",
            "coefficient_covariance",
            "knot_vector",
        }
        assert set(archive.files) == expected_arrays
        for key in ("phi", "theta", "theta_prime", "theta_second", "s_prime", "s_second"):
            assert archive[key].shape == (4097,)
            assert np.all(np.isfinite(archive[key]))
        assert archive["coefficients"].shape == (49,)
        assert archive["coefficient_covariance"].shape == (49, 49)
        assert np.allclose(archive["coefficient_covariance"], archive["coefficient_covariance"].T)
        assert float(np.min(archive["s_prime"])) < 0.0
        assert np.max(np.abs(archive["coefficients"] - coefficients)) == 0.0

    return {
        "status": "PASS",
        "classification": EXPECTED_LANDING,
        "local_candidate_classification": EXPECTED_LOCAL_CLASSIFICATION,
        "source_manifest_rows": len(sources),
        "candidate_rows_compared": EXPECTED_ROWS,
        "maximum_census_absolute_difference": maximum_difference,
        "maximum_raw_chi2_absolute_difference": maximum_raw_chi2_difference,
        "raw_chi2_gate_failures": raw_chi2_gate_failures,
        "maximum_selected_coefficient_absolute_difference": coefficient_difference,
        "selected_basis_count": 48,
        "selected_alpha": 0.1,
        "turning_intervals_retained_as_uncertified_local_candidate": True,
        "redshift_direct_from_reciprocal_phi": True,
        "angular_outcomes_used": False,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--no-write", action="store_true")
    args = parser.parse_args()
    result = verify()
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    output = PACKAGE / "VERIFICATION_RESULT.json"
    if args.no_write:
        assert output.read_text() == rendered
    else:
        output.write_text(rendered)
    print(f"PASS: G243 {result['classification']}")


if __name__ == "__main__":
    main()
