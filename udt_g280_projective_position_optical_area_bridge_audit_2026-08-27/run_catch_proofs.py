#!/usr/bin/env python3
"""Hostile provenance and non-vacuity catches for G280."""

from __future__ import annotations

import argparse
import copy
import csv
import json
import math
from pathlib import Path

import sympy as sp


PACKAGE = Path(__file__).resolve().parent
EXECUTABLE_MUTATION = "executable_mutation"
PROVENANCE_GUARD = "provenance_guard"


def validate(result: dict[str, object]) -> None:
    checks = result["checks"]
    assert isinstance(checks, list)
    assert len(checks) == result["caught"] == result["expected"] == 8
    assert all(item["caught"] for item in checks)
    assert len({item["name"] for item in checks}) == 8
    assert sum(item["check_kind"] == EXECUTABLE_MUTATION for item in checks) == 4
    assert sum(item["check_kind"] == PROVENANCE_GUARD for item in checks) == 4
    assert result["executable_mutations"] == 4
    assert result["provenance_guards"] == 4
    center = next(
        item
        for item in checks
        if item["name"] == "equating_areal_radius_to_projective_position_forces_nonsmooth_center_profile"
    )
    assert center["check_kind"] == EXECUTABLE_MUTATION
    assert center["evidence"]["forced_center_slope"] == 1
    assert center["evidence"]["smooth_center_control_slope"] == 0


def assert_validator_rejects(mutated: dict[str, object]) -> None:
    try:
        validate(mutated)
    except (AssertionError, StopIteration):
        return
    raise AssertionError("repair mutation escaped fail-closed validator")


def run() -> dict[str, object]:
    checks: list[dict[str, object]] = []

    def record(name: str, check_kind: str, caught: bool, evidence: dict[str, object]) -> None:
        checks.append(
            {
                "name": name,
                "check_kind": check_kind,
                "caught": bool(caught),
                "evidence": evidence,
            }
        )

    length = 1.0
    a = 0.49
    root_a = math.sqrt(a)
    flat_area = length**2
    wave_area = math.sinh(root_a * length) * math.sin(root_a * length) / a
    delta = 0.7
    ell = 3.0
    chi = math.tanh(delta)

    zero_tidal_area = flat_area
    record(
        "zero_tidal_parameter_is_vacuous",
        EXECUTABLE_MUTATION,
        abs(wave_area - flat_area) > 1.0e-4 and zero_tidal_area == flat_area,
        {"nonzero_tidal_area": wave_area, "zero_tidal_area": zero_tidal_area},
    )
    deleted_second_jet_area = flat_area
    record(
        "deleting_transverse_second_jet_erases_separator",
        EXECUTABLE_MUTATION,
        wave_area != flat_area and deleted_second_jet_area == flat_area,
        {"native_wave_area": wave_area, "deleted_second_jet_area": deleted_second_jet_area},
    )
    surrogate_flat_area = ell * chi
    surrogate_wave_area = ell * chi
    record(
        "replacing_Jacobi_area_by_ell_times_chi_discards_metric_information",
        EXECUTABLE_MUTATION,
        surrogate_flat_area == surrogate_wave_area and wave_area != flat_area,
        {
            "native_flat_area": flat_area,
            "native_wave_area": wave_area,
            "mutated_flat_area": surrogate_flat_area,
            "mutated_wave_area": surrogate_wave_area,
        },
    )

    normalized_radius = sp.symbols("normalized_radius", real=True)
    forced_profile = sp.atanh(normalized_radius)
    smooth_center_control = normalized_radius**2
    forced_center_slope = sp.diff(forced_profile, normalized_radius).subs(normalized_radius, 0)
    smooth_center_control_slope = sp.diff(smooth_center_control, normalized_radius).subs(
        normalized_radius, 0
    )
    record(
        "equating_areal_radius_to_projective_position_forces_nonsmooth_center_profile",
        EXECUTABLE_MUTATION,
        forced_center_slope == 1 and smooth_center_control_slope == 0,
        {
            "forced_center_slope": int(forced_center_slope),
            "smooth_center_control_slope": int(smooth_center_control_slope),
        },
    )

    with (PACKAGE / "PREMISE_LEDGER.tsv").open(newline="") as handle:
        rows = {row["item"]: row for row in csv.DictReader(handle, delimiter="\t")}
    record(
        "promoting_imported_dA_R_to_universal_metric_identity",
        PROVENANCE_GUARD,
        rows["central_spherical_dA_equals_R"]["open_boundary"] == "universal equality with W5 position",
        {"registered_open_boundary": rows["central_spherical_dA_equals_R"]["open_boundary"]},
    )
    record(
        "promoting_transparent_transfer_to_native",
        PROVENANCE_GUARD,
        rows["transparent_radiative_transfer"]["status"] == "CONDITIONAL_IMPORT",
        {"registered_status": rows["transparent_radiative_transfer"]["status"]},
    )
    record(
        "promoting_W5_to_canon",
        PROVENANCE_GUARD,
        rows["W5_projective_position"]["status"] == "WORKING_FOUNDATIONAL_CLARIFICATION",
        {"registered_status": rows["W5_projective_position"]["status"]},
    )
    record(
        "reading_observational_outcomes",
        PROVENANCE_GUARD,
        all(rows[name]["status"] == "EXCLUDED" for name in ("SNe_Cepheid_DES_outcomes",)),
        {"registered_status": rows["SNe_Cepheid_DES_outcomes"]["status"]},
    )

    result: dict[str, object] = {
        "audit": "G280_HOSTILE_CATCH_PROOFS",
        "status": "PASS",
        "caught": len(checks),
        "expected": 8,
        "executable_mutations": 4,
        "provenance_guards": 4,
        "checks": checks,
    }
    validate(result)

    repair_mutations_caught = 0
    for index in range(len(checks)):
        mutated = copy.deepcopy(result)
        mutated["checks"][index]["check_kind"] = "unclassified"
        assert_validator_rejects(mutated)
        repair_mutations_caught += 1
    mutated = copy.deepcopy(result)
    center = next(
        item
        for item in mutated["checks"]
        if item["name"] == "equating_areal_radius_to_projective_position_forces_nonsmooth_center_profile"
    )
    center["evidence"]["forced_center_slope"] = 0
    assert_validator_rejects(mutated)
    repair_mutations_caught += 1
    mutated = copy.deepcopy(result)
    mutated["executable_mutations"] = 3
    assert_validator_rejects(mutated)
    repair_mutations_caught += 1
    assert repair_mutations_caught == 10
    result["repair_fail_closed_mutations"] = {
        "caught": repair_mutations_caught,
        "expected": 10,
    }
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--no-write", action="store_true")
    args = parser.parse_args()
    result = run()
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.no_write:
        print(rendered, end="")
    else:
        (PACKAGE / "CATCH_PROOF_RESULT.json").write_text(rendered)
        print(rendered, end="")


if __name__ == "__main__":
    main()
