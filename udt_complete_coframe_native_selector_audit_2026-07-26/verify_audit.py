#!/usr/bin/env python3
"""Fail-closed verification for the complete-coframe selector audit."""

from __future__ import annotations

import copy
import csv
import hashlib
import json
from pathlib import Path
import subprocess
import sys


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def rows(name: str) -> list[dict[str, str]]:
    with (HERE / name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def keyed(values: list[dict[str, str]], key: str = "id") -> dict[str, dict[str, str]]:
    result = {row[key]: row for row in values}
    if len(result) != len(values):
        raise AssertionError(f"duplicate {key}")
    return result


def run_json(script: str) -> dict[str, object]:
    result = subprocess.run(
        [sys.executable, str(HERE / script)],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if result.returncode:
        raise AssertionError(f"{script}: {result.stderr}")
    return json.loads(result.stdout)


def validate_sources(values: list[dict[str, str]], corrupt: bool = False) -> None:
    if len(values) != 21:
        raise AssertionError("source count")
    seen: set[str] = set()
    for index, row in enumerate(values):
        path = row["path"]
        if path in seen:
            raise AssertionError("duplicate source")
        seen.add(path)
        source = ROOT / path
        if not source.is_file():
            raise AssertionError(f"missing source {path}")
        digest = hashlib.sha256(source.read_bytes()).hexdigest()
        if corrupt and index == 0:
            digest = "0" * 64
        blob = subprocess.run(
            ["git", "hash-object", path], cwd=ROOT, text=True,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
        )
        if blob.returncode or digest != row["sha256"] or blob.stdout.strip() != row["git_blob"]:
            raise AssertionError(f"source identity {path}")


def validate_premise_universe(values: list[dict[str, str]]) -> None:
    ids = [row["id"] for row in values]
    if ids != [f"P{index:02d}" for index in range(1, 19)] or len(set(ids)) != 18:
        raise AssertionError("premise universe")


def validate_extension_universe(values: list[dict[str, str]]) -> None:
    ids = [row["id"] for row in values]
    if ids != [f"E{index:02d}" for index in range(1, 8)] or len(set(ids)) != 7:
        raise AssertionError("extension universe")
    if values[0]["free_parameters"] != "7":
        raise AssertionError("extension parameter count")


EXPECTED_CAPABILITY = {
    "P01": ("0", "PAIR_PROJECTION_DOES_NOT_RESTRICT_K_OR_C"),
    "P02": ("0", "NO_COMPLETE_4D_PAIRING_EXTENSION_IS_REGISTERED"),
    "P03": ("0", "SATISFIED_BY_EVERY_GENERATOR_IN_BOUNDED_CLASS"),
    "P04": ("0", "SATISFIED_BY_EVERY_GENERATOR_IN_BOUNDED_CLASS"),
    "P05": ("0", "FIXED_INVARIANCE_IS_INCOMPATIBLE_AND_EQUIVARIANCE_DOES_NOT_SELECT_A_SLOT"),
    "P06": ("0", "COVARIANCE_IS_TRANSFORMATION_LAW_NOT_COMPONENT_SELECTOR"),
    "P07": ("0", "INTERSECTION_WITH_SEVEN_DIMENSIONAL_TRIANGULAR_EXTENSION_TANGENT_IS_ZERO"),
    "P08": ("0", "NO_REGISTERED_EQUATION_FOR_DIMENSIONLESS_K_OR_C"),
    "P09": ("0", "NATIVE_PLACEMENT_REMAINS_OPEN"),
    "P10": ("-", "BLOCKED_UNTYPED_SELECTOR_FOR_POINTWISE_EXTENSION"),
    "P11": ("0", "SCALAR_SEAL_VALUE_HAS_ZERO_EXTENSION_RANK_AND_FULL_LIFT_REMAINS_OPEN"),
    "P12": ("0", "ALGEBRAIC_IDENTITY_NOT_LOCAL_SCALE_GAUGE_OR_EXTENSION_EQUATION"),
    "P13": ("-", "CHALLENGED_NOT_DERIVED_AND_EXCLUDED_FROM_ACTIVE_RANK"),
    "P14": ("-", "DOMAIN_MISMATCH_NOT_OFFSHELL_LOCAL_SELECTOR"),
    "P15": ("-", "NO_POINTWISE_EXTENSION_OPERATION"),
    "P16": ("-", "CONDITIONAL_DOWNSTREAM_AND_EXCLUDED_AS_SELECTOR"),
    "P17": ("-", "EXCLUDED_NO_CARRIER_PROMOTION"),
    "P18": ("-", "OPEN_AND_EXCLUDED_NO_ACTION_BACKFILL"),
}


def validate_capability(values: list[dict[str, str]]) -> None:
    table = keyed(values)
    if set(table) != set(EXPECTED_CAPABILITY):
        raise AssertionError("capability coverage")
    rank = 0
    for premise, expected in EXPECTED_CAPABILITY.items():
        actual = (table[premise]["active_selector_rank"], table[premise]["ruling"])
        if actual != expected:
            raise AssertionError(f"capability {premise}")
        if actual[0] != "-":
            rank += int(actual[0])
    if rank != 0:
        raise AssertionError("active rank")


EXPECTED_STATUS = {
    "S01": "DERIVED_RETAINED",
    "S02": "DERIVED_CLASSIFICATION_RETAINED",
    "S03": "DERIVED_RANK_SEVEN",
    "S04": "DERIVED_ZERO_DIMENSIONAL_INTERSECTION",
    "S05": "ZERO",
    "S06": "DERIVED_EXACT_WITNESSES",
    "S07": "INCOMPATIBLE_WITH_FOUNDED_NONTRIVIAL_GENERATOR",
    "S08": "REQUIRED_OPEN_LIFT",
    "S09": "BLOCKED_UNTYPED_OR_NONUNIQUE",
    "S10": "NO_REGISTERED_RANK",
    "S11": "INACTIVE_CHALLENGED_NOT_DERIVED",
    "S12": "BLOCKED_DOMAIN_MISMATCH",
    "S13": "BLOCKED_OPEN_GLOBAL_SCHEMA",
    "S14": "OPEN_NOT_SELECTED",
    "S15": "OPEN",
    "S16": "VERIFIED_WITH_CAVEATS_BOUNDED_POINTWISE_SELECTOR_RANK",
    "S17": "OPEN_COVARIANT_COMPLETE_COFRAME_LIFT_OR_SECTION_RULE",
}


def validate_status(values: list[dict[str, str]]) -> None:
    table = keyed(values)
    if {key: row["status"] for key, row in table.items()} != EXPECTED_STATUS:
        raise AssertionError("status ledger")


def validate_conditional(values: list[dict[str, str]]) -> None:
    table = keyed(values)
    expected = {
        "C01": ("1", "6"),
        "C02": ("3", "4"),
        "C03": ("4", "3"),
        "C04": ("7", "0"),
        "C05": ("1", "6"),
        "C06": ("-", "-"),
        "C07": ("INCOMPATIBLE", "-"),
        "C08": ("0", "7"),
        "C09": ("-", "-"),
    }
    actual = {key: (row["constraint_rank"], row["physical_survivor_dimension"]) for key, row in table.items()}
    if actual != expected:
        raise AssertionError("conditional rank ledger")


def validate_results(derivation: dict[str, object], independent: dict[str, object]) -> None:
    counts = derivation["counts"]
    expected = {
        "active_physical_survivor_dimension": 7,
        "active_selector_rank": 0,
        "extension_intersection_with_Lorentz_kernel": 0,
        "extension_parameters": 7,
        "full_Lorentz_centralizer_dimension": 1,
        "local_Lorentz_presentation_kernel_dimension": 6,
        "physical_metric_tangent_rank": 7,
    }
    if derivation["result"] != "PASS" or counts != expected:
        raise AssertionError("derivation counts")
    rulings = derivation["rulings"]
    if rulings["bounded_active_outcome"] != "UNREDUCED_ACTIVE_FAMILY":
        raise AssertionError("false unique outcome")
    if rulings["variation_domain"] != "NOT_SELECTED_BY_POINTWISE_EXTENSION_KINEMATICS":
        raise AssertionError("variation promotion")
    if rulings["global_completion"] != "OPEN":
        raise AssertionError("global promotion")
    independent_counts = independent["counts"]
    if independent["result"] != "PASS" or independent_counts != {
        "Lorentz_kernel_dimension": 6,
        "active_selector_rank": 0,
        "extension_rank": 7,
        "full_frame_centralizer_dimension": 1,
        "physical_tangent_rank": 7,
        "survivor_dimension": 7,
    }:
        raise AssertionError("independent counts")


def expect_failure(callback) -> str:
    try:
        callback()
    except AssertionError:
        return "PASS"
    raise AssertionError("catch accepted corruption")


def main() -> None:
    source_rows = rows("SOURCE_MANIFEST.tsv")
    premise_rows = rows("PREMISE_SELECTOR_UNIVERSE.tsv")
    extension_rows = rows("EXTENSION_FAMILY_UNIVERSE.tsv")
    capability_rows = rows("SELECTOR_CAPABILITY_LEDGER.tsv")
    conditional_rows = rows("CONDITIONAL_RESTRICTION_LEDGER.tsv")
    status_rows = rows("STATUS_LEDGER.tsv")
    stored_derivation = json.loads((HERE / "DERIVATION_RESULT.json").read_text())
    stored_independent = json.loads((HERE / "INDEPENDENT_RESULT.json").read_text())

    validate_sources(source_rows)
    validate_premise_universe(premise_rows)
    validate_extension_universe(extension_rows)
    validate_capability(capability_rows)
    validate_conditional(conditional_rows)
    validate_status(status_rows)
    validate_results(stored_derivation, stored_independent)

    replay_derivation = run_json("derive_selector_rank.py")
    replay_independent = run_json("verify_selector_rank_independent.py")
    # Stored records intentionally omit the verbose check dictionaries.
    validate_results(replay_derivation, replay_independent)
    if replay_derivation["check_count"] != 39 or replay_independent["check_count"] != 11:
        raise AssertionError("replay check count")

    catches: dict[str, str] = {}
    for name, premise, rank, ruling in (
        ("strong_CSN_promotion", "P13", "1", "ACTIVE_LOCAL_SCALE_GAUGE"),
        ("common_factor_gauge_promotion", "P12", "0", "LOCAL_SCALE_GAUGE"),
        ("c_anchor_fake_selector", "P08", "1", EXPECTED_CAPABILITY["P08"][1]),
        ("bootstrap_offshell_promotion", "P14", "1", "OFFSHELL_LOCAL_SELECTOR"),
        ("finite_cell_fake_selector", "P10", "1", "SELECTS_SPECTATOR"),
        ("Lorentz_quotient_fake_reduction", "P07", "1", EXPECTED_CAPABILITY["P07"][1]),
    ):
        altered = copy.deepcopy(capability_rows)
        row = next(value for value in altered if value["id"] == premise)
        row["active_selector_rank"] = rank
        row["ruling"] = ruling
        catches[name] = expect_failure(lambda altered=altered: validate_capability(altered))

    missing_premise = copy.deepcopy(premise_rows[:-1])
    catches["missing_premise"] = expect_failure(lambda: validate_premise_universe(missing_premise))
    duplicate_premise = copy.deepcopy(premise_rows)
    duplicate_premise[-1]["id"] = "P17"
    catches["duplicate_premise"] = expect_failure(lambda: validate_premise_universe(duplicate_premise))
    missing_extension = copy.deepcopy(extension_rows[:-1])
    catches["missing_extension_family"] = expect_failure(lambda: validate_extension_universe(missing_extension))

    altered_derivation = copy.deepcopy(stored_derivation)
    altered_derivation["counts"]["physical_metric_tangent_rank"] = 6
    catches["physical_direction_lost"] = expect_failure(lambda: validate_results(altered_derivation, stored_independent))
    altered_derivation = copy.deepcopy(stored_derivation)
    altered_derivation["rulings"]["bounded_active_outcome"] = "UNIQUE_ACTIVE_SELECTION"
    catches["spectator_false_uniqueness"] = expect_failure(lambda: validate_results(altered_derivation, stored_independent))
    altered_derivation = copy.deepcopy(stored_derivation)
    altered_derivation["rulings"]["variation_domain"] = "SELECTED"
    catches["variation_domain_promotion"] = expect_failure(lambda: validate_results(altered_derivation, stored_independent))
    altered_derivation = copy.deepcopy(stored_derivation)
    altered_derivation["rulings"]["global_completion"] = "SELECTED"
    catches["global_completion_promotion"] = expect_failure(lambda: validate_results(altered_derivation, stored_independent))

    altered_conditional = copy.deepcopy(conditional_rows)
    next(value for value in altered_conditional if value["id"] == "C04")["constraint_rank"] = "6"
    catches["spectator_rank_corruption"] = expect_failure(lambda: validate_conditional(altered_conditional))
    catches["source_identity_corruption"] = expect_failure(lambda: validate_sources(source_rows, corrupt=True))

    if len(catches) != 15 or set(catches.values()) != {"PASS"}:
        raise AssertionError("catch proofs")
    output = {
        "schema": "udt-complete-coframe-native-selector-verification-1.0",
        "result": "PASS",
        "source_count": len(source_rows),
        "premise_count": len(premise_rows),
        "extension_family_count": len(extension_rows),
        "production_checks": replay_derivation["check_count"],
        "independent_checks": replay_independent["check_count"],
        "catch_proofs": catches,
        "ruling": "ACTIVE_SELECTOR_RANK_ZERO_SEVEN_PHYSICAL_DIRECTIONS_SURVIVE_IN_BOUNDED_CLASS",
    }
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
