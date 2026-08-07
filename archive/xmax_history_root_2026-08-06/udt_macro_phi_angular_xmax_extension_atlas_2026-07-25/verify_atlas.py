#!/usr/bin/env python3
"""Fail-closed verifier and exercised catches for the macro extension atlas."""

from __future__ import annotations

import copy
import csv
import hashlib
import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = Path(__file__).resolve().parent
BASE = "3ff555b4a48a70067313afef0cf10eba2e17fd49"
EXPECTED_DIRECTIONS = {
    "D01_ANGULAR_TRACE": ("POSSIBLE_IF_DPHI_HAS_ANGULAR_COMPONENT", "POSSIBLE_IF_GLOBAL_EXTENSION_DESCENDS"),
    "D02_ANGULAR_RECIPROCAL": ("POSSIBLE_IF_DPHI_HAS_ANGULAR_COMPONENT", "POSSIBLE_IF_GLOBAL_EXTENSION_DESCENDS"),
    "D03_ANGULAR_SHEAR": ("POSSIBLE_IF_DPHI_HAS_ANGULAR_COMPONENT", "POSSIBLE_IF_GLOBAL_EXTENSION_DESCENDS"),
    "D04_MIX_CLOCK_TO_ANGULAR_2": ("NONE_IN_FIXED_FOUNDED_REST_SLICE", "NO_EFFECT_IN_FIXED_FOUNDED_REST_SLICE__OTHER_OBSERVER_COMPARISON_OPEN"),
    "D05_MIX_DEPTH_TO_ANGULAR_2": ("POSSIBLE_IF_DPHI_HAS_ANGULAR_COMPONENT", "POSSIBLE_IF_GLOBAL_EXTENSION_DESCENDS"),
    "D06_MIX_CLOCK_TO_ANGULAR_3": ("NONE_IN_FIXED_FOUNDED_REST_SLICE", "NO_EFFECT_IN_FIXED_FOUNDED_REST_SLICE__OTHER_OBSERVER_COMPARISON_OPEN"),
    "D07_MIX_DEPTH_TO_ANGULAR_3": ("POSSIBLE_IF_DPHI_HAS_ANGULAR_COMPONENT", "POSSIBLE_IF_GLOBAL_EXTENSION_DESCENDS"),
}


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def write_tsv(path: Path, rows: list[dict[str, str]], fields: list[str]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def expected_completions() -> set[str]:
    rows = read_tsv(ROOT / "udt_angular_generator_branch_census_2026-07-23/BRANCH_UNIVERSE.tsv")
    values = {row["completion_id"] for row in rows}
    if len(rows) != 12 or len(values) != 12:
        raise AssertionError("source completion count")
    return values


def validate_atlas(rows: list[dict[str, str]]) -> None:
    completions = expected_completions()
    keys = [(row["completion_id"], row["direction_id"]) for row in rows]
    expected_keys = {(completion, direction) for completion in completions for direction in EXPECTED_DIRECTIONS}
    if len(rows) != 84 or len(set(keys)) != 84 or set(keys) != expected_keys:
        raise AssertionError("atlas must be exact 12x7 cross product")
    for row in rows:
        direction = row["direction_id"]
        nonaligned, global_effect = EXPECTED_DIRECTIONS[direction]
        if row["aligned_local_B_effect"] != "NONE_EXACT":
            raise AssertionError("aligned B promotion")
        if row["nonaligned_local_B_effect"] != nonaligned:
            raise AssertionError("nonaligned channel mismatch")
        if row["global_observer_rest_distance_effect"] != global_effect:
            raise AssertionError("local/global channel conflation")
        if row["selection_status"] != "NOT_SELECTED":
            raise AssertionError("selection promotion")
        if row["xmax_consequence"] != "DOES_NOT_SELECT_FINITE_OR_NUMERICAL_XMAX":
            raise AssertionError("Xmax promotion")
        if row["global_descent_status"] in {"GLOBAL_COMPATIBLE", "DERIVED", "FORCED"}:
            raise AssertionError("unproved global descent")
        if not row["unresolved_requirement"]:
            raise AssertionError("missing global requirement")
        if row["completion_id"] not in row["evidence"]:
            raise AssertionError("missing row evidence")


def validate_directions(rows: list[dict[str, str]]) -> None:
    if len(rows) != 7 or {row["direction_id"] for row in rows} != set(EXPECTED_DIRECTIONS):
        raise AssertionError("direction ledger")
    if any(row["founded_pair_effect"] != "NONE" for row in rows):
        raise AssertionError("founded pair altered")
    if any(row["aligned_local_B_effect"] != "NONE_EXACT" for row in rows):
        raise AssertionError("aligned identity altered")


def validate_channels(rows: list[dict[str, str]]) -> None:
    expected = {
        "M01_ALIGNED_LOCAL_DEPTH": ("DERIVED_EXACT_BOUNDED", "NO_LOCAL_B_MODULATION"),
        "M02_NONALIGNED_LOCAL_DEPTH": ("DERIVED_POSSIBILITY_WITH_EXACT_COUNTERWITNESSES", "CAN_MODULATE_B_AND_BREAK_TRANSNORMALITY"),
        "M03_TRANSVERSE_GLOBAL_DISTANCE": ("DERIVED_CONDITIONAL_WITNESS", "CAN_MODULATE_GLOBAL_OBSERVER_PAIR_DISTANCE"),
        "M04_CLOCK_ANGULAR_FOUR_D_MIX": ("DERIVED_EXACT_BOUNDED", "FOUR_D_CROSS_TERM_ONLY_IN_THIS_FRAME"),
        "M05_SCALAR_FEEDBACK": ("OPEN", "NO_NATIVE_FEEDBACK_LAW_DERIVED"),
    }
    if len(rows) != 5 or {row["channel_id"] for row in rows} != set(expected):
        raise AssertionError("modulation channel set")
    for row in rows:
        status, angular_role = expected[row["channel_id"]]
        if (row["status"], row["angular_role"]) != (status, angular_role):
            raise AssertionError("modulation channel promotion")


def validate_algebra(value: dict[str, object]) -> None:
    if value.get("result") != "PASS" or value.get("sympy_version") != "1.14.0":
        raise AssertionError("production algebra environment/result")
    checks = value["checks"]
    if checks["aligned_B"] != "p**2/w**2":
        raise AssertionError("aligned symbolic result")
    if checks["angular_fixed_level_difference"] != "1/25":
        raise AssertionError("angular witness")
    if checks["shift_fixed_level_difference"] != "-3/80":
        raise AssertionError("shift witness")
    if value["rulings"]["xmax"] != "NOT_DERIVED":
        raise AssertionError("algebra Xmax promotion")


def validate_independent(value: dict[str, object]) -> None:
    if value.get("result") != "PASS":
        raise AssertionError("independent result")
    checks = value["checks"]
    if checks["aligned_exact_samples"] != 6 or checks["general_B_exact_samples"] != 6:
        raise AssertionError("independent exact sample counts")
    if checks["angular_fixed_level_difference"] != "1/25" or checks["shift_fixed_level_difference"] != "-3/80":
        raise AssertionError("independent witnesses")


def validate_manifest(rows: list[dict[str, str]]) -> None:
    if len(rows) != 11 or len({row["path"] for row in rows}) != 11:
        raise AssertionError("source manifest cardinality")
    for row in rows:
        data = (ROOT / row["path"]).read_bytes()
        sha = hashlib.sha256(data).hexdigest()
        blob = subprocess.check_output(
            ["git", "rev-parse", f"{BASE}:{row['path']}"], cwd=ROOT, text=True
        ).strip()
        if sha != row["sha256"] or blob != row["git_blob_at_base"] or len(data) != int(row["size_bytes"]):
            raise AssertionError("source manifest mismatch")


def expect_failure(name: str, function, catches: list[dict[str, str]]) -> None:
    try:
        function()
    except (AssertionError, KeyError, ValueError, FileNotFoundError):
        catches.append({"catch_id": name, "result": "PASS", "meaning": "registered_corruption_rejected"})
        return
    raise AssertionError(f"catch did not fire: {name}")


def main() -> None:
    atlas = read_tsv(OUT / "BRANCH_EXTENSION_ATLAS.tsv")
    directions = read_tsv(OUT / "EXTENSION_DIRECTION_LEDGER.tsv")
    channels = read_tsv(OUT / "MODULATION_CHANNEL_LEDGER.tsv")
    manifest = read_tsv(OUT / "INPUT_SOURCE_MANIFEST.tsv")
    algebra = json.loads((OUT / "ALGEBRA_RESULT.json").read_text(encoding="utf-8"))
    independent = json.loads((OUT / "INDEPENDENT_RESULT.json").read_text(encoding="utf-8"))

    validate_atlas(atlas)
    validate_directions(directions)
    validate_channels(channels)
    validate_manifest(manifest)
    validate_algebra(algebra)
    validate_independent(independent)

    catches: list[dict[str, str]] = []
    expect_failure("C01_MISSING_CROSS_ROW", lambda: validate_atlas(atlas[:-1]), catches)
    expect_failure("C02_DUPLICATE_CROSS_ROW", lambda: validate_atlas(atlas + [copy.deepcopy(atlas[0])]), catches)

    promoted = copy.deepcopy(atlas)
    promoted[0]["selection_status"] = "DERIVED"
    expect_failure("C03_SELECTION_PROMOTION", lambda: validate_atlas(promoted), catches)

    modulated = copy.deepcopy(atlas)
    modulated[0]["aligned_local_B_effect"] = "ANGULARLY_MODULATED"
    expect_failure("C04_ALIGNED_B_FALSE_MODULATION", lambda: validate_atlas(modulated), catches)

    conflated = copy.deepcopy(atlas)
    clock_row = next(row for row in conflated if row["direction_id"] == "D04_MIX_CLOCK_TO_ANGULAR_2")
    clock_row["global_observer_rest_distance_effect"] = "POSSIBLE_IF_GLOBAL_EXTENSION_DESCENDS"
    expect_failure("C05_LOCAL_GLOBAL_CHANNEL_CONFLATION", lambda: validate_atlas(conflated), catches)

    descended = copy.deepcopy(atlas)
    descended[0]["global_descent_status"] = "GLOBAL_COMPATIBLE"
    expect_failure("C06_UNPROVED_GLOBAL_DESCENT", lambda: validate_atlas(descended), catches)

    xmax = copy.deepcopy(atlas)
    xmax[0]["xmax_consequence"] = "XMAX=1"
    expect_failure("C07_NUMERICAL_XMAX_PROMOTION", lambda: validate_atlas(xmax), catches)

    corrupt_manifest = copy.deepcopy(manifest)
    corrupt_manifest[0]["sha256"] = "0" * 64
    expect_failure("C08_SOURCE_HASH_CORRUPTION", lambda: validate_manifest(corrupt_manifest), catches)

    expect_failure("C09_MISSING_MODULATION_CHANNEL", lambda: validate_channels(channels[:-1]), catches)
    feedback = copy.deepcopy(channels)
    next(row for row in feedback if row["channel_id"] == "M05_SCALAR_FEEDBACK")["status"] = "DERIVED"
    expect_failure("C10_SCALAR_FEEDBACK_PROMOTION", lambda: validate_channels(feedback), catches)

    bad_independent = copy.deepcopy(independent)
    bad_independent["result"] = "FAIL"
    expect_failure("C11_INDEPENDENT_FAILURE", lambda: validate_independent(bad_independent), catches)

    bad_algebra = copy.deepcopy(algebra)
    bad_algebra["sympy_version"] = "unpinned"
    expect_failure("C12_UNPINNED_ALGEBRA", lambda: validate_algebra(bad_algebra), catches)

    write_tsv(OUT / "CATCH_PROOFS.tsv", catches, ["catch_id", "result", "meaning"])
    result = {
        "schema": "udt-macro-phi-angular-xmax-verification-1.0",
        "result": "PASS",
        "counts": {
            "completions": 12,
            "directions": 7,
            "atlas_rows": 84,
            "modulation_channels": 5,
            "source_files": 11,
            "catch_proofs": len(catches),
        },
        "checks": {
            "exact_cross_product": "PASS",
            "aligned_depth_identity": "PASS",
            "channel_separation": "PASS",
            "no_selection_promotion": "PASS",
            "no_xmax_promotion": "PASS",
            "source_manifest": "PASS",
            "pinned_sympy": algebra["sympy_version"],
            "independent_fraction_replay": "PASS",
        },
    }
    (OUT / "VERIFICATION_RESULT.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
