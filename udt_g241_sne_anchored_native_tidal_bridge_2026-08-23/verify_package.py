#!/usr/bin/env python3
"""Verify G241 sources and compare production with the independent replay."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path


PACKAGE = Path(__file__).resolve().parent
REPO = PACKAGE.parent


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def preregistration_registry_digest(path: Path) -> str:
    lines = path.read_bytes().splitlines(keepends=True)
    g241_rows = [line for line in lines if line.startswith(b"G241\t")]
    assert len(g241_rows) == 1, "live registry must contain exactly one banked G241 row"
    historical = b"".join(line for line in lines if not line.startswith(b"G241\t"))
    return hashlib.sha256(historical).hexdigest()


def compare_float(left, right, tolerance, label, relative_tolerance=0.0):
    difference = abs(float(left) - float(right))
    scale = max(abs(float(left)), abs(float(right)))
    assert difference <= tolerance + relative_tolerance * scale, f"{label} mismatch: {left} vs {right}"


def verify() -> dict:
    with (PACKAGE / "SOURCE_MANIFEST.tsv").open(newline="") as stream:
        rows = list(csv.DictReader(stream, delimiter="\t"))
    assert len(rows) == 6
    for row in rows:
        source = REPO / row["path"]
        if row["path"] == "CURRENT_SCIENTIFIC_PREMISES.tsv":
            assert preregistration_registry_digest(source) == row["sha256"], "preregistration registry lineage mismatch"
        else:
            assert digest(source) == row["sha256"], f"source hash mismatch: {row['path']}"

    production = json.loads((PACKAGE / "DERIVATION_RESULT.json").read_text())
    independent = json.loads((PACKAGE / "INDEPENDENT_VERIFICATION.json").read_text())
    assert production["boss_outcomes_opened"] is False
    assert production["angular_fit_coefficient"] is None
    assert production["landing"] == independent["landing"]
    assert production["selected_degree"] == independent["selected_degree"]
    assert [row["degree"] for row in production["candidates"]] == [2, 3, 4]
    assert [row["degree"] for row in independent["candidates"]] == [2, 3, 4]

    maximum_difference = 0.0
    for prod, indep in zip(production["candidates"], independent["candidates"]):
        for key, tolerance in (
            ("chi2", 1.0e-8),
            ("chi2_ceiling", 1.0e-10),
            ("minimum_s_prime", 1.0e-9),
            ("minimum_s_prime_phi", 1.0e-9),
        ):
            compare_float(prod[key], indep[key], tolerance, f"d{prod['degree']} {key}")
            maximum_difference = max(maximum_difference, abs(float(prod[key]) - float(indep[key])))
        for key in ("dense_tidal_J_min", "dense_tidal_J_max"):
            compare_float(prod[key], indep[key], 1.0e-7, f"d{prod['degree']} {key}", 5.0e-10)
            maximum_difference = max(maximum_difference, abs(float(prod[key]) - float(indep[key])))
        assert prod["passed"] == indep["passed"]
        assert prod["adequate"] == indep["adequate"]
        assert prod["monotone_invertible"] == indep["monotone_invertible"]
        assert prod["finite_dense_grid"] == indep["finite_dense_grid"]
        for key in ("coefficients_theta_units", "knot_s_prime", "knot_s_second", "knot_p", "knot_q", "knot_tidal_J"):
            assert len(prod[key]) == len(indep[key])
            for index, (left, right) in enumerate(zip(prod[key], indep[key])):
                compare_float(left, right, 1.0e-7, f"d{prod['degree']} {key}[{index}]")
                maximum_difference = max(maximum_difference, abs(float(left) - float(right)))
        tidal_scale = max(1.0, abs(float(prod["dense_tidal_J_min"])), abs(float(prod["dense_tidal_J_max"])))
        assert prod["scale_invariance_max_abs_residual"] <= 1.0e-12 * tidal_scale
        assert indep["scale_invariance_max_abs_residual"] <= 1.0e-50

    return {
        "status": "PASS",
        "source_hashes": len(rows),
        "landing": production["landing"],
        "selected_degree": production["selected_degree"],
        "maximum_compared_absolute_difference": maximum_difference,
        "boss_outcomes_opened": False,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--no-write", action="store_true")
    args = parser.parse_args()
    result = verify()
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.no_write:
        assert rendered == (PACKAGE / "VERIFICATION_RESULT.json").read_text()
    else:
        (PACKAGE / "VERIFICATION_RESULT.json").write_text(rendered)
    print(f"PASS: G241 {result['landing']}")


if __name__ == "__main__":
    main()
