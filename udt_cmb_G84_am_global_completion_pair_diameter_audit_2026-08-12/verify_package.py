#!/usr/bin/env python3
"""Fail-closed package verifier for G84."""

from __future__ import annotations

import csv
import hashlib
import json
from collections import Counter
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
EXPECTED_COUNTS = {
    "ZERO_MIXING_CONSTANT_CURVATURE_GLOBAL_EXTENSION_EXISTS": 1,
    "NONZERO_BIFURCATION_MIXING__STANDARD_SMOOTH_SYMMETRY_EXTENSION_OBSTRUCTED": 196,
}
FORBIDDEN_PROMOTIONS = (
    "PHYSICAL_XMAX_SELECTED",
    "PHYSICAL_PROFILE_SELECTED",
    "PHYSICAL_R_SELECTED",
    "CMB_PREDICTION",
    "BOOTSTRAP_CLOSED",
)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream, delimiter="\t"))


def verify_sources() -> int:
    manifest = rows(HERE / "SOURCE_MANIFEST.tsv")
    assert len(manifest) == len({row["path"] for row in manifest}) == 14
    for row in manifest:
        assert digest(ROOT / row["path"]) == row["sha256"]
    return len(manifest)


def validate_profiles(records: list[dict[str, str]]) -> Counter[str]:
    assert len(records) == len({row["profile_id"] for row in records}) == 197
    counts = Counter(row["extension_class"] for row in records)
    assert counts == EXPECTED_COUNTS
    zero = [row for row in records if row["extension_class"] == "ZERO_MIXING_CONSTANT_CURVATURE_GLOBAL_EXTENSION_EXISTS"]
    assert len(zero) == 1 and zero[0]["profile_id"] == "G75_F01_AM"
    assert zero[0]["q_at_s_4_exact"] == zero[0]["h_at_x_2_exact"] == "0"
    for row in records:
        if row["profile_id"] != "G75_F01_AM":
            assert row["q_at_s_4_exact"] != "0"
            assert row["mixing_vanishes_at_candidate_surface"] == "false"
        assert row["physical_status"] == "CONTROL_CLASSIFICATION_NOT_SELECTED_PHYSICS"
    return counts


def validate_geometry(geometry: dict[str, object]) -> None:
    expected = {
        "coordinate_map": "x=2*sin(chi)",
        "spatial_radius_over_R": "2",
        "spatial_diameter_over_R": "2*pi",
        "spatial_injectivity_radius_over_R": "2*pi",
        "equator_x": "2",
        "north_pole_to_equator_over_R": "pi",
        "x_map_multiplicity": "TWO_TO_ONE_OFF_EQUATOR_ON_DOUBLED_S3",
        "zero_mix_recentered_static_limit_over_R": "pi",
        "zero_mix_candidate_Xmax": "pi*R",
        "zero_mix_frame_scope": "GLOBAL_ISOMETRY_ORBIT_OF_CENTRAL_GEODESIC_OBSERVERS",
    }
    for key, value in expected.items():
        assert geometry[key] == value, key


def validate_recenter(records: list[dict[str, str]]) -> None:
    assert len(records) == len({row["fixed_chart_receiver_x"] for row in records}) == 4
    assert len({row["fixed_chart_distance_to_original_horizon_over_R"] for row in records}) == 4
    assert {row["recentered_own_horizon_distance_over_R"] for row in records} == {"pi"}
    assert {row["recentered_candidate_Xmax_over_R"] for row in records} == {"pi"}
    assert {row["status"] for row in records} == {"DERIVED_CONDITIONAL_ZERO_MIXING_GEODESIC_OBSERVER_CLASS"}


def validate_counterexamples(records: list[dict[str, str]]) -> None:
    assert len(records) == len({row["case"] for row in records}) == 3
    by_case = {row["case"]: row for row in records}
    assert by_case["NORTH_POLE_TO_EQUATOR"]["spatial_distance_over_R"] == "pi"
    assert by_case["SAME_LATITUDE_NORTH_PATCH_GAMMA_RANGE"]["spatial_distance_over_R"] == "0_to_pi"
    assert by_case["SAME_LATITUDE_NORTH_PATCH_GAMMA_RANGE"]["stationary_depth"] == "0"
    assert by_case["EQUATOR_PAIR_VARIABLE_ANGLE"]["spatial_distance_over_R"] == "0_to_2*pi"


def validate_authority(text: str) -> None:
    for token in FORBIDDEN_PROMOTIONS:
        assert token not in text
    required = (
        "physical `X_max`",
        "time-live",
        "zero-mixing",
        "central geodesic",
        "not the global spatial diameter",
        "minimal doubled",
    )
    for token in required:
        assert token in text, token


def main() -> None:
    source_rows = verify_sources()
    result = json.loads((HERE / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    independent = json.loads((HERE / "INDEPENDENT_VERIFICATION.json").read_text(encoding="utf-8"))
    profiles = rows(HERE / "PROFILE_COMPLETION_ATLAS.tsv")
    recentered = rows(HERE / "RECENTERED_OBSERVER_LIMIT_ATLAS.tsv")
    counterexamples = rows(HERE / "PAIR_DISTANCE_COUNTEREXAMPLES.tsv")
    branches = rows(HERE / "COMPLETION_BRANCH_ATLAS.tsv")
    counts = validate_profiles(profiles)
    validate_geometry(result["geometry"])
    validate_recenter(recentered)
    validate_counterexamples(counterexamples)
    assert len(branches) == len({row["object"] for row in branches}) == 5
    assert result["extension_class_counts"] == dict(sorted(counts.items()))
    assert result["physical_X_max_status"] == "OPEN"
    assert independent["status"] == "PASS" and not independent["profile_mismatches"]
    validate_authority(
        (HERE / "EXACT_DERIVATION.md").read_text(encoding="utf-8")
        + (HERE / "AUDIT_REPORT.md").read_text(encoding="utf-8")
    )
    output = {
        "schema": "udt-cmb-g84-package-verification-v1",
        "all_passed": True,
        "source_rows": source_rows,
        "profile_rows": len(profiles),
        "extension_class_counts": dict(sorted(counts.items())),
        "recentered_rows": len(recentered),
        "pair_counterexamples": len(counterexamples),
        "branch_rows": len(branches),
        "physical_X_max_status": result["physical_X_max_status"],
    }
    print(json.dumps(output, sort_keys=True))


if __name__ == "__main__":
    main()
