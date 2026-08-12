#!/usr/bin/env python3
"""Fail-closed verification of the G81 package and frozen inputs."""

from __future__ import annotations

import csv
import hashlib
import json
import subprocess
from pathlib import Path

import numpy as np


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
BASE = "f112a32e4fbc5319de4e964e869f9024e9bdb1b9"
IDS = ["C0_RADIAL_ROTATED", "C1_FULL_ANGULAR"]
MAXIMUM = "DERIVED_CONDITIONAL_SCREEN_COVARIANCE_ON_TWO_FIXED_CONTROLS"


def validate_contract(contract: dict) -> None:
    assert contract["control_ids"] == IDS
    assert len(contract["control_ids"]) == len(set(contract["control_ids"])) == 2
    np.testing.assert_allclose(contract["directions"][IDS[0]], [1.0, 0.0, 0.0], rtol=0.0, atol=0.0)
    np.testing.assert_allclose(contract["directions"][IDS[1]], [12 / 13, 3 / 13, 4 / 13], rtol=0.0, atol=1e-16)
    np.testing.assert_allclose(contract["reverse_source_rotation"], [[0.6, -0.8], [0.8, 0.6]], rtol=0.0, atol=0.0)
    np.testing.assert_allclose(
        contract["receiver_projection_rotation"], [[5 / 13, -12 / 13], [12 / 13, 5 / 13]], rtol=0.0, atol=1e-16
    )
    assert contract["tangent_reversal"] == "FULL_K_REVERSE_EQUALS_MINUS_K_SOURCE_OVER_Z"
    assert contract["unrotated_matrix_law"] == "D_REVERSE_EQUALS_Z_TIMES_TRANSPOSE_D_FORWARD"
    assert contract["rotated_matrix_law"] == "D_REVERSE_AB_EQUALS_Z_TIMES_B_TIMES_TRANSPOSE_D_FORWARD_TIMES_TRANSPOSE_A"
    assert contract["diagonalization_permitted"] is False
    assert contract["retuning_permitted"] is False
    for field in (
        "future_signal_derived", "physical_profile_selected", "physical_endpoint_selected",
        "Xmax_identified", "physical_source_selected", "cmb_observable_derived",
    ):
        assert contract[field] is False


def validate_outcomes(production: dict, independent: dict) -> None:
    assert production["status"] == independent["status"] == "PASS"
    assert production["control_count"] == 2
    assert [row["control_id"] for row in production["controls"]] == IDS
    assert [row["control_id"] for row in independent["controls"]] == IDS
    assert len({row["control_id"] for row in production["controls"]}) == 2
    assert production["authority"]["maximum_conclusion"] == MAXIMUM
    assert production["authority"]["future_signal_derived"] is False
    assert production["authority"]["physical_profile_endpoint_scale_source_or_observable_selected"] is False
    assert production["authority"]["Xmax_identified"] is False
    assert production["authority"]["cmb_temp_activated"] is False
    for row, check in zip(production["controls"], independent["controls"], strict=True):
        assert row["status"] == check["status"] == "PASS"
        assert all(row["gates"].values()) and all(check["gates"].values())
        assert row["reverse_unrotated"]["D_relative"] < 1e-8
        assert row["reverse_rotated"]["D_relative"] < 1e-8
        assert row["reverse_unrotated"]["area_ratio_minus_Z"] < 1e-8
        assert check["independent_unrotated_reciprocity_relative"] < 2e-4
        assert check["independent_rotated_covariance_relative"] < 2e-4
        assert check["independent_area_ratio_minus_Z"] < 2e-4
        assert check["forward_production_relative"] < 2e-4
        assert check["reverse_production_relative"] < 2e-4
        assert check["rotated_production_relative"] < 2e-4
    c1 = production["controls"][1]
    assert c1["forward"]["offdiagonal_norm"] > 1e-5
    endpoint = c1["forward"]["endpoint"]
    assert abs(endpoint[2] - np.pi / 2) > 1e-3 and abs(endpoint[3]) > 1e-3


def validate_sources() -> int:
    with (HERE / "SOURCE_MANIFEST.tsv").open(newline="", encoding="utf-8") as stream:
        rows = list(csv.DictReader(stream, delimiter="\t"))
    assert len(rows) == len({row["path"] for row in rows}) == 9
    for row in rows:
        assert row["base_commit"] == BASE
        data = subprocess.check_output(["git", "show", f"{BASE}:{row['path']}"], cwd=ROOT)
        assert hashlib.sha256(data).hexdigest() == row["sha256"]
    return len(rows)


def main() -> None:
    contract = json.loads((HERE / "SEMANTIC_CONTRACT.json").read_text(encoding="utf-8"))
    production = json.loads((HERE / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    independent = json.loads((HERE / "INDEPENDENT_VERIFICATION.json").read_text(encoding="utf-8"))
    validate_contract(contract)
    validate_outcomes(production, independent)
    sources = validate_sources()
    output = {
        "schema": "udt-cmb-g81-package-verification-v1",
        "status": "PASS",
        "source_rows_verified": sources,
        "controls_verified": 2,
        "production_and_independent_gates": True,
        "nonradial_angular_activation": True,
        "authority_boundary_verified": True,
    }
    rendered = json.dumps(output, indent=2, sort_keys=True) + "\n"
    (HERE / "PACKAGE_VERIFICATION.json").write_text(rendered, encoding="utf-8")
    print(rendered, end="")


if __name__ == "__main__":
    main()
