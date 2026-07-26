#!/usr/bin/env python3
"""Fail-closed semantic and algebra replay for the covariant-lift atlas."""

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


def keyed(values: list[dict[str, str]], key: str) -> dict[str, dict[str, str]]:
    output = {value[key]: value for value in values}
    if len(output) != len(values):
        raise AssertionError(f"duplicate {key}")
    return output


def run_json(script: str) -> dict[str, object]:
    result = subprocess.run(
        [sys.executable, str(HERE / script)], cwd=ROOT, text=True,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
    )
    if result.returncode:
        raise AssertionError(f"{script}: {result.stderr}")
    return json.loads(result.stdout)


def validate_sources(values: list[dict[str, str]], corrupt: bool = False) -> None:
    if len(values) != 16:
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
        if (
            blob.returncode
            or blob.stdout.strip() != row["git_blob"]
            or digest != row["sha256"]
            or source.stat().st_size != int(row["size_bytes"])
        ):
            raise AssertionError(f"source identity {path}")


def validate_source_scope(scope: list[dict[str, str]], manifest: list[dict[str, str]]) -> None:
    scope_map = {row["path"]: row["role"] for row in scope}
    manifest_map = {row["path"]: row["role"] for row in manifest}
    if len(scope_map) != len(scope) or scope_map != manifest_map:
        raise AssertionError("source scope mismatch")


EXPECTED_DATA = {
    "D00": "NO_COVARIANT_LIFT_FROM_DATA",
    "D01": "COVARIANT_LINE_SPLIT_NOT_ORDERED_PAIR",
    "D02": "SINGULAR_OR_DEGENERATE_STRATUM",
    "D03": "NO_COVARIANT_LIFT_FROM_DATA",
    "D04": "COVARIANT_LINE_SPLIT_NOT_ORDERED_PAIR",
    "D05": "CONDITIONAL_ORDERED_PAIR_WITH_PHYSICAL_MODULI",
    "D06": "CONDITIONAL_ORDERED_PAIR_WITH_PHYSICAL_MODULI",
    "D07": "NO_FOUNDED_PHYSICAL_LIFT_FROM_PLANE_ALONE",
    "D08": "CHOICE_DEPENDENT_DERIVATIVE_LIFT",
    "D09": "GLOBAL_OR_TRANSPORT_INPUT_REQUIRED",
    "D10": "GLOBAL_OR_TRANSPORT_INPUT_REQUIRED",
    "D11": "NO_COVARIANT_LIFT_FROM_DATA",
    "D12": "NO_DIRECTIONAL_RANK_CHANGE",
    "D13": "NO_DIRECTIONAL_RANK_CHANGE",
    "D14": "EXPLICIT_UNBOUNDED_REMAINDER",
}


def validate_data_universe(universe: list[dict[str, str]], outcomes: list[dict[str, str]]) -> None:
    universe_ids = [row["id"] for row in universe]
    if universe_ids != [f"D{index:02d}" for index in range(15)] or len(set(universe_ids)) != 15:
        raise AssertionError("data universe")
    table = keyed(outcomes, "id")
    if {key: row["outcome"] for key, row in table.items()} != EXPECTED_DATA:
        raise AssertionError("data outcomes")
    if table["D13"]["physical_moduli_or_obstruction"] != "action_scalar_leaves_every_stabilizer_unchanged":
        raise AssertionError("hbar promotion")


EXPECTED_STRATA = {
    "T01": "NO_LIFT",
    "T02": "LOCAL_CONDITIONAL",
    "T03": "LOCAL_CONDITIONAL_NOT_CLEAN_PAIR_CODOMAIN",
    "T04": "DEGENERATE",
    "T05": "NO_LIFT",
    "T06": "NO_REGULAR_UNIVERSAL_CONTINUATION",
    "T07": "RELATIONAL_CONDITIONAL",
    "T08": "RELATIONAL_CONDITIONAL",
    "T09": "FALLS_BACK_TO_T07",
    "T10": "CONDITIONAL_D05",
    "T11": "DEGENERATE_OR_WRONG_TYPE",
    "T12": "CHOICE_DEPENDENT",
    "T13": "NO_REGULAR_UNIVERSAL_CONTINUATION",
    "T14": "NO_COMPLETE_LIFT",
    "T15": "NO_BACK_SELECTION",
    "T16": "OPEN_GLOBAL",
}


def validate_strata(universe: list[dict[str, str]], ledger: list[dict[str, str]]) -> None:
    ids = [row["id"] for row in universe]
    if ids != [f"T{index:02d}" for index in range(1, 17)] or len(set(ids)) != 16:
        raise AssertionError("stratum universe")
    table = keyed(ledger, "id")
    if {key: row["continuation_status"] for key, row in table.items()} != EXPECTED_STRATA:
        raise AssertionError("stratum outcomes")


EXPECTED_DIRECTION = {
    "L_GENERIC": ("real_not_equal_1", "6", "3", "9", "UNSELECTED_FAMILY"),
    "L_CLOCK_DEMOCRATIC": ("1", "1", "0", "1", "UNIQUE_ONLY_AFTER_DEMOCRATIC_1PLUS3_CODOMAIN_CHOICE"),
    "L_SPECTATOR": ("0", "6", "3", "9", "UNIQUE_ONLY_IF_COMPLETE_DETERMINANT_OR_SCREEN_AREA_INVARIANCE_ADDED"),
    "L_RULER_DEMOCRATIC": ("-1", "6", "3", "9", "not_selected_and_depends_on_direction"),
    "L_TRACE_EMBEDDING_SPECIAL": ("-1/2", "6", "3", "9", "ALGEBRAIC_SPECIAL_NOT_SELECTOR"),
    "L_SCREEN_ROTATION_GAUGE": ("omega", "-", "-", "-", "GAUGE_ONLY_POINTWISE_GLOBAL_CONNECTION_OPEN"),
}


def validate_direction(values: list[dict[str, str]]) -> None:
    table = keyed(values, "case")
    actual = {
        key: (
            row["lambda"], row["generator_span"], row["rotation_commutator_span"],
            row["Lie_span"], row["selection_status"],
        )
        for key, row in table.items()
    }
    if actual != EXPECTED_DIRECTION:
        raise AssertionError("direction family")


EXPECTED_STATUS = {
    "S01": "DERIVED_RETAINED",
    "S02": "NOT_DERIVED_RETAINED",
    "S03": "NO_COVARIANT_NONTRIVIAL_LIFT",
    "S04": "DERIVED_DIMENSION_TWO",
    "S05": "UNIQUE_CONDITIONAL_LOCAL",
    "S06": "ALGEBRAIC_CONDITIONAL",
    "S07": "OBSTRUCTED_IN_BOUNDED_CLASS",
    "S08": "CONDITIONAL_ONE_PHYSICAL_MODULUS",
    "S09": "DERIVED_NINE_DIMENSIONAL_LOCAL_ALGEBRA",
    "S10": "DERIVED_COLLAPSE_TO_1PLUS3",
    "S11": "CONDITIONAL_NOT_SELECTED",
    "S12": "PLANE_WITHOUT_FOUNDED_AXES",
    "S13": "CHOICE_DEPENDENT_AND_DEGENERACY_SENSITIVE",
    "S14": "SCALAR_CALIBRATION_ONLY",
    "S15": "OPEN_TWO_CODOMAINS",
    "S16": "OPEN_UNCHANGED",
    "S17": "VERIFIED_WITH_CAVEATS_BOUNDED_LOCAL_LIFT_ATLAS",
    "S18": "OBSERVER_PAIR_FAMILY_CONSISTENCY_OR_CODOMAIN_ADJUDICATION",
}


def validate_status(values: list[dict[str, str]]) -> None:
    table = keyed(values, "id")
    if {key: row["status"] for key, row in table.items()} != EXPECTED_STATUS:
        raise AssertionError("status")


EXPECTED_PRODUCTION_COUNTS = {
    "fixed_observer_directional_Lie_span_generic": 9,
    "fixed_observer_directional_Lie_span_lambda_one": 1,
    "fixed_observer_directional_generator_span_generic": 6,
    "fixed_observer_directional_rotation_span_generic": 3,
    "full_Lorentz_commutant_dimension": 1,
    "nonnull_one_line_commutant_dimension": 2,
    "nonnull_one_line_invariant_projector_ranks": [0, 1, 3, 4],
    "null_line_commutant_dimension": 2,
    "null_nontrivial_idempotents": 0,
    "ordered_pair_commutant_dimension": 6,
    "ordered_pair_fixed_base_lift_parameters": 2,
    "ordered_pair_physical_screen_moduli": 1,
    "oriented_plane_commutant_dimension": 4,
    "simple_spectrum_Lorentzian_pair_choices": 3,
}


def validate_results(production: dict[str, object], independent: dict[str, object]) -> None:
    if production["result"] != "PASS" or production["counts"] != EXPECTED_PRODUCTION_COUNTS:
        raise AssertionError("production result")
    rulings = production["rulings"]
    if rulings["universal_lift"] != "OPEN_NOT_SELECTED":
        raise AssertionError("universal promotion")
    if "NINE_DIMENSIONAL" not in rulings["directional_family"] or "LAMBDA_ONE_COLLAPSES" not in rulings["directional_family"]:
        raise AssertionError("directional ruling")
    if independent["result"] != "PASS" or independent["counts"] != {
        "full_Lorentz_commutant_dimension": 1,
        "generic_directional_Lie_span": 9,
        "lambda_one_directional_Lie_span": 1,
        "nonnull_one_line_commutant_dimension": 2,
        "null_line_commutant_dimension": 2,
        "ordered_pair_commutant_dimension": 6,
        "ordered_pair_physical_screen_moduli": 1,
        "oriented_plane_commutant_dimension": 4,
        "simple_spectrum_pair_choices": 3,
    }:
        raise AssertionError("independent result")


def expect_failure(callback) -> str:
    try:
        callback()
    except AssertionError:
        return "PASS"
    raise AssertionError("catch accepted corruption")


def main() -> None:
    sources = rows("SOURCE_MANIFEST.tsv")
    source_scope = rows("SOURCE_SCOPE.tsv")
    data_universe = rows("DATA_UNIVERSE.tsv")
    outcomes = rows("DATA_OUTCOME_ATLAS.tsv")
    stratum_universe = rows("STRATUM_UNIVERSE.tsv")
    strata = rows("CAUSAL_STRATUM_LEDGER.tsv")
    directions = rows("DIRECTIONAL_FAMILY_LEDGER.tsv")
    statuses = rows("STATUS_LEDGER.tsv")
    production = json.loads((HERE / "DERIVATION_RESULT.json").read_text())
    independent = json.loads((HERE / "INDEPENDENT_RESULT.json").read_text())

    validate_sources(sources)
    validate_source_scope(source_scope, sources)
    validate_data_universe(data_universe, outcomes)
    validate_strata(stratum_universe, strata)
    validate_direction(directions)
    validate_status(statuses)
    validate_results(production, independent)

    replay_production = run_json("derive_covariant_lift_atlas.py")
    replay_independent = run_json("verify_covariant_lift_independent.py")
    validate_results(replay_production, replay_independent)
    if replay_production["check_count"] != 62 or replay_independent["check_count"] != 35:
        raise AssertionError("check counts")

    catches: dict[str, str] = {}
    altered = copy.deepcopy(outcomes)
    next(row for row in altered if row["id"] == "D00")["outcome"] = "UNIQUE_COVARIANT_LIFT"
    catches["metric_only_fake_lift"] = expect_failure(lambda: validate_data_universe(data_universe, altered))
    altered = copy.deepcopy(outcomes)
    next(row for row in altered if row["id"] == "D01")["outcome"] = "UNIQUE_ORDERED_PAIR"
    catches["one_line_fake_pair"] = expect_failure(lambda: validate_data_universe(data_universe, altered))
    altered = copy.deepcopy(outcomes)
    next(row for row in altered if row["id"] == "D02")["outcome"] = "REGULAR_NULL_LIFT"
    catches["null_projector_promotion"] = expect_failure(lambda: validate_data_universe(data_universe, altered))
    altered = copy.deepcopy(outcomes)
    next(row for row in altered if row["id"] == "D13")["physical_moduli_or_obstruction"] = "hbar_selects_screen"
    catches["hbar_direction_promotion"] = expect_failure(lambda: validate_data_universe(data_universe, altered))
    catches["missing_data_row"] = expect_failure(lambda: validate_data_universe(data_universe[:-1], outcomes))
    duplicate_data = copy.deepcopy(data_universe)
    duplicate_data[-1]["id"] = "D13"
    catches["duplicate_data_row"] = expect_failure(lambda: validate_data_universe(duplicate_data, outcomes))
    catches["missing_stratum"] = expect_failure(lambda: validate_strata(stratum_universe[:-1], strata))

    altered = copy.deepcopy(directions)
    next(row for row in altered if row["case"] == "L_GENERIC")["Lie_span"] = "8"
    catches["generic_Lie_span_corruption"] = expect_failure(lambda: validate_direction(altered))
    altered = copy.deepcopy(directions)
    next(row for row in altered if row["case"] == "L_CLOCK_DEMOCRATIC")["Lie_span"] = "9"
    catches["lambda_one_collapse_corruption"] = expect_failure(lambda: validate_direction(altered))
    altered = copy.deepcopy(directions)
    next(row for row in altered if row["case"] == "L_SPECTATOR")["selection_status"] = "NATIVELY_SELECTED"
    catches["spectator_false_selection"] = expect_failure(lambda: validate_direction(altered))
    altered = copy.deepcopy(directions)
    next(row for row in altered if row["case"] == "L_SCREEN_ROTATION_GAUGE")["selection_status"] = "PHYSICAL_HOPF_FORCE"
    catches["rotation_physics_promotion"] = expect_failure(lambda: validate_direction(altered))

    altered = copy.deepcopy(statuses)
    next(row for row in altered if row["id"] == "S15")["status"] = "CODOMAIN_SELECTED"
    catches["ontology_fork_promotion"] = expect_failure(lambda: validate_status(altered))
    altered = copy.deepcopy(statuses)
    next(row for row in altered if row["id"] == "S16")["status"] = "ACTION_DERIVED"
    catches["action_promotion"] = expect_failure(lambda: validate_status(altered))

    altered_production = copy.deepcopy(production)
    altered_production["counts"]["ordered_pair_physical_screen_moduli"] = 0
    catches["screen_dilation_gauge_error"] = expect_failure(lambda: validate_results(altered_production, independent))
    altered_production = copy.deepcopy(production)
    altered_production["rulings"]["universal_lift"] = "SELECTED"
    catches["universal_lift_promotion"] = expect_failure(lambda: validate_results(altered_production, independent))
    catches["source_identity_corruption"] = expect_failure(lambda: validate_sources(sources, corrupt=True))

    if len(catches) != 16 or set(catches.values()) != {"PASS"}:
        raise AssertionError("catch proofs")
    output = {
        "schema": "udt-covariant-reciprocal-coframe-lift-verification-1.0",
        "result": "PASS",
        "source_count": len(sources),
        "data_type_count": len(data_universe),
        "stratum_count": len(stratum_universe),
        "production_checks": replay_production["check_count"],
        "independent_checks": replay_independent["check_count"],
        "catch_proofs": catches,
        "ruling": "LOCAL_LIFT_ATLAS_AND_DIRECTIONAL_ALGEBRA_VERIFIED_WITH_UNIVERSAL_CODOMAIN_OPEN",
    }
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
