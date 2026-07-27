#!/usr/bin/env python3
"""Fail-closed verifier for the CMB-polarization observable-typing audit."""

from __future__ import annotations

import copy
import csv
import hashlib
import json
import subprocess
import sys
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
OBS_IDS = {f"O{i:02d}" for i in range(1, 13)}
EXT_IDS = {f"E{i:02d}" for i in range(1, 13)}
GATE_IDS = {f"G{i:02d}" for i in range(1, 15)}
CATCH_IDS = {f"F{i:02d}" for i in range(1, 25)}


def table(name: str) -> list[dict[str, str]]:
    with (HERE / name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def run(script: str) -> tuple[int, str, str]:
    result = subprocess.run(
        [sys.executable, str(HERE / script)], cwd=ROOT, text=True,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
    )
    return result.returncode, result.stdout, result.stderr


def review_fields(text: str) -> dict[str, str]:
    fields: dict[str, str] = {}
    active = False
    for line in text.splitlines():
        if line == "```text REVIEW_FIELDS":
            active = True
            continue
        if active and line == "```":
            break
        if active and "=" in line:
            key, value = line.split("=", 1)
            fields[key.strip()] = value.strip()
    return fields


def load_state() -> dict[str, object]:
    return {
        "observables": table("OBSERVABLE_UNIVERSE.tsv"),
        "extensions": table("EXTENSION_ROW_UNIVERSE.tsv"),
        "gates": table("GATE_SCHEMA.tsv"),
        "observable_matrix": table("OBSERVABLE_GATE_MATRIX.tsv"),
        "capability_matrix": table("EXTENSION_OBSERVABLE_CAPABILITY.tsv"),
        "independent_observable": table("INDEPENDENT_OBSERVABLE_GATE_STATUS.tsv"),
        "independent_capability": table("INDEPENDENT_EXTENSION_CAPABILITY.tsv"),
        "dependency": table("DEPENDENCY_CHAIN.tsv"),
        "ranking": table("DISCRIMINATOR_RANKING.tsv"),
        "external": table("EXTERNAL_SOURCE_REGISTRY.tsv"),
        "derived": json.loads((HERE / "DERIVATION_RESULT.json").read_text(encoding="utf-8")),
        "independent": json.loads((HERE / "INDEPENDENT_RESULT.json").read_text(encoding="utf-8")),
        "review": review_fields((HERE / "FRESH_ADVERSARIAL_REVIEW.md").read_text(encoding="utf-8")),
    }


def unique(rows: list[dict[str, str]], key: str, expected: set[str]) -> None:
    values = [row[key] for row in rows]
    assert len(values) == len(set(values))
    assert set(values) == expected


def validate(state: dict[str, object]) -> None:
    observables = state["observables"]
    extensions = state["extensions"]
    gates = state["gates"]
    observable_matrix = state["observable_matrix"]
    capability_matrix = state["capability_matrix"]
    independent_observable = state["independent_observable"]
    independent_capability = state["independent_capability"]
    dependency = state["dependency"]
    ranking = state["ranking"]
    external = state["external"]
    derived = state["derived"]
    independent = state["independent"]
    review = state["review"]
    assert all(isinstance(x, list) for x in (
        observables, extensions, gates, observable_matrix, capability_matrix,
        independent_observable, independent_capability, dependency, ranking, external,
    ))
    assert isinstance(derived, dict) and isinstance(independent, dict) and isinstance(review, dict)

    unique(observables, "observable_id", OBS_IDS)
    unique(extensions, "extension_id", EXT_IDS)
    unique(gates, "gate_id", GATE_IDS)
    assert len(observable_matrix) == 168
    observable_keys = [(row["observable_id"], row["gate_id"]) for row in observable_matrix]
    assert len(observable_keys) == len(set(observable_keys))
    assert set(observable_keys) == {(o, g) for o in OBS_IDS for g in GATE_IDS}
    independent_observable_map = {
        (row["observable_id"], row["gate_id"]): row["status"] for row in independent_observable
    }
    assert len(independent_observable_map) == 168
    assert all(independent_observable_map[key] == row["status"] for key, row in zip(observable_keys, observable_matrix))

    assert len(capability_matrix) == 144
    capability_keys = [(row["extension_id"], row["observable_id"]) for row in capability_matrix]
    assert len(capability_keys) == len(set(capability_keys))
    assert set(capability_keys) == {(e, o) for e in EXT_IDS for o in OBS_IDS}
    independent_capability_map = {
        (row["extension_id"], row["observable_id"]): row["status"] for row in independent_capability
    }
    assert len(independent_capability_map) == 144
    assert all(independent_capability_map[key] == row["status"] for key, row in zip(capability_keys, capability_matrix))

    unique(dependency, "link_id", {f"D{i:02d}" for i in range(1, 11)})
    assert {row["status"] for row in dependency if row["link_id"] in {"D01", "D02"}} == {
        "DERIVED_CLASSIFICATION_OPEN_SELECTION", "OPEN",
    }
    assert next(row for row in dependency if row["link_id"] == "D04")["status"] == "OPEN"
    assert next(row for row in dependency if row["link_id"] == "D05")["status"] == "OPEN"
    assert next(row for row in dependency if row["link_id"] == "D06")["layer"] == "L3"
    assert next(row for row in dependency if row["link_id"] == "D07")["layer"] == "L2"
    assert next(row for row in dependency if row["link_id"] == "D08")["layer"] == "L0"
    assert next(row for row in dependency if row["link_id"] == "D09")["layer"] == "L3"
    assert len(ranking) == 4 and [row["rank"] for row in ranking] == ["1", "2", "3", "4"]
    assert ranking[0]["observable_ids"] == "O09;O10;O11"
    assert ranking[0]["current_use"] == "TYPE_AND_FALSIFICATION_CONTRACT_ONLY"
    unique(external, "external_id", {f"X{i:02d}" for i in range(1, 11)})
    assert all(row["admissible_use"] and row["prohibited_promotion"] for row in external)

    assert derived["observable_types"] == independent["observables"] == 12
    assert derived["observable_gates"] == independent["gates"] == 14
    assert derived["observable_gate_cells"] == independent["observable_gate_cells"] == 168
    assert derived["extension_rows"] == independent["extensions"] == 12
    assert derived["extension_observable_cells"] == independent["extension_observable_cells"] == 144
    assert derived["observable_gate_status_counts"] == independent["observable_gate_status_counts"]
    assert derived["capability_status_counts"] == independent["capability_status_counts"]
    assert derived["highest_priority_future_guideposts"] == independent["highest_priority_future_guideposts"] == ["O09", "O10", "O11"]
    assert derived["CMB_polarization_guidepost_status"] == independent["CMB_polarization_guidepost_status"] == "PROMISING_FUTURE_GUIDEPOST_ONLY_AFTER_NATIVE_EXTENSION_DOMAIN_CARRIER_SOURCE_PROPAGATION_GLOBAL_SKY_STATISTICAL_RULE_AND_EXTERNAL_CALIBRATION_FOREGROUND_CONTROLS"
    assert derived["power_spectra_alone_for_directional_holonomy"] == independent["power_spectra_alone_for_directional_holonomy"] == "INSUFFICIENT_NONINJECTIVE_COMPRESSION"
    assert derived["current_UDT_CMB_prediction"] == independent["current_UDT_CMB_prediction"] == "ABSENT_OPEN_CHAIN"
    assert derived["exact_controls"]["spin2_rotation_composition_exact"] is True
    assert derived["exact_controls"]["spin2_rotation_reversal_exact"] is True
    assert derived["exact_controls"]["power_spectrum_noninjective_witness"] is True
    assert derived["exact_controls"]["calibration_rotation_degeneracy_witness"] is True
    assert derived["exact_controls"]["schematic_B_component_sum_nonuniqueness_sanity_check"] is True
    assert independent["controls"]["spin2_composition_holdout"] is True
    assert independent["controls"]["spin2_reversal_holdout"] is True
    assert independent["controls"]["isotropic_power_noninjective_holdout"] is True
    assert independent["production_outputs_read"] is False
    for key in (
        "unique_extension_selected", "physical_path_selected", "physical_polarization_carrier_derived",
        "native_polarization_source_derived", "E_B_are_local_basis_components",
        "zero_TB_EB_metric_only_prediction", "BB_unique_holonomy_signature",
        "rotation_unique_without_calibration_control", "source_peak_phase_amplitude_derived_from_metric_only",
        "statistical_isotropy_UDT_theorem", "map_level_anomaly_equated_to_power_spectrum",
        "Maxwell_Thomson_imported_as_native", "standard_cosmology_imported_as_UDT", "fit_performed",
        "strong_local_CSN_activated", "cross_branch_splice_used",
        "Xmax_bootstrap_action_source_boundary_mass_changed",
    ):
        assert derived[key] is False
    for key in (
        "unique_extension_selected", "physical_path_selected", "native_carrier_or_source_derived",
        "E_B_are_local_basis_components", "power_spectra_directionally_complete",
        "rotation_unique_without_calibration_control", "BB_unique_holonomy_signature",
        "statistical_isotropy_UDT_theorem", "Maxwell_Thomson_imported_as_native", "external_model_promoted",
    ):
        assert independent[key] is False

    assert review == {
        "verdict": "VERIFIED_WITH_CAVEATS",
        "source_first": "TRUE",
        "production_outputs_read_before_independent_verdict": "FALSE",
        "physical_polarization_promoted": "FALSE",
        "extension_selected": "FALSE",
        "required_corrections_applied": "TRUE",
    }


def rejected(mutator) -> str:
    state = load_state()
    mutator(state)
    try:
        validate(state)
    except (AssertionError, KeyError, TypeError):
        return "PASS"
    raise AssertionError("structured mutation accepted")


def catch_proofs() -> list[dict[str, str]]:
    def duplicate_extension(state):
        state["extensions"][1] = copy.deepcopy(state["extensions"][0])

    def remove_directional_guidepost(state):
        state["ranking"][0]["observable_ids"] = "O09;O11"

    mutations = {
        "F01": lambda s: s["observables"].pop(),
        "F02": duplicate_extension,
        "F03": lambda s: s["observable_matrix"].pop(),
        "F04": lambda s: s["derived"].__setitem__("physical_polarization_carrier_derived", True),
        "F05": lambda s: s["derived"].__setitem__("Maxwell_Thomson_imported_as_native", True),
        "F06": lambda s: s["derived"].__setitem__("E_B_are_local_basis_components", True),
        "F07": lambda s: s["derived"].__setitem__("power_spectra_alone_for_directional_holonomy", "SUFFICIENT"),
        "F08": lambda s: s["derived"].__setitem__("zero_TB_EB_metric_only_prediction", True),
        "F09": lambda s: s["derived"].__setitem__("BB_unique_holonomy_signature", True),
        "F10": lambda s: s["derived"].__setitem__("rotation_unique_without_calibration_control", True),
        "F11": lambda s: s["derived"].__setitem__("physical_path_selected", True),
        "F12": lambda s: s["derived"].__setitem__("unique_extension_selected", True),
        "F13": lambda s: s["derived"].__setitem__("strong_local_CSN_activated", True),
        "F14": lambda s: s["derived"].__setitem__("cross_branch_splice_used", True),
        "F15": lambda s: s["derived"].__setitem__("source_peak_phase_amplitude_derived_from_metric_only", True),
        "F16": lambda s: s["derived"].__setitem__("fit_performed", True),
        "F17": lambda s: s["derived"].__setitem__("statistical_isotropy_UDT_theorem", True),
        "F18": remove_directional_guidepost,
        "F19": lambda s: s["derived"].__setitem__("map_level_anomaly_equated_to_power_spectrum", True),
        "F20": lambda s: s["derived"].__setitem__("standard_cosmology_imported_as_UDT", True),
        "F21": lambda s: s["derived"].__setitem__("Xmax_bootstrap_action_source_boundary_mass_changed", True),
        "F22": lambda s: s["derived"].__setitem__("current_UDT_CMB_prediction", "VALIDATED"),
        "F23": lambda s: s["independent"].__setitem__("production_outputs_read", True),
        "F24": lambda s: s["review"].__setitem__("source_first", "FALSE"),
    }
    contract = {row["catch_id"]: row["false_promotion_or_corruption"] for row in table("FALSIFICATION_CONTRACT.tsv")}
    assert set(contract) == set(mutations) == CATCH_IDS
    return [
        {"catch_id": catch_id, "mutation": contract[catch_id], "status": rejected(mutations[catch_id])}
        for catch_id in sorted(CATCH_IDS)
    ]


def main() -> int:
    validate(load_state())
    for script, expected in (
        ("verify_local_source_manifest.py", {"result": "PASS", "sources": 10}),
        ("verify_external_source_registry.py", {"result": "PASS", "primary_or_official_sources": 10}),
    ):
        code, stdout, stderr = run(script)
        assert code == 0 and stderr == "" and json.loads(stdout) == expected

    code, stdout, stderr = run("derive_cmb_observable_typing.py")
    assert code == 0 and stderr == ""
    assert json.loads(stdout) == json.loads((HERE / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    assert stdout == (HERE / "DERIVATION_STDOUT.txt").read_text(encoding="utf-8")
    assert stderr == (HERE / "DERIVATION_STDERR.txt").read_text(encoding="utf-8")

    code, independent_stdout, independent_stderr = run("verify_cmb_typing_independent.py")
    assert code == 0 and independent_stderr == ""
    assert json.loads(independent_stdout) == json.loads((HERE / "INDEPENDENT_RESULT.json").read_text(encoding="utf-8"))
    assert independent_stdout == (HERE / "INDEPENDENT_STDOUT.txt").read_text(encoding="utf-8")
    assert independent_stderr == (HERE / "INDEPENDENT_STDERR.txt").read_text(encoding="utf-8")
    independent_code = (HERE / "verify_cmb_typing_independent.py").read_text(encoding="utf-8")
    for forbidden in ("derive_cmb_observable_typing", "DERIVATION_RESULT.json", "OBSERVABLE_GATE_MATRIX.tsv", "EXTENSION_OBSERVABLE_CAPABILITY.tsv", "DISCRIMINATOR_RANKING.tsv"):
        assert forbidden not in independent_code

    catches = catch_proofs()
    with (HERE / "CATCH_PROOFS.tsv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, delimiter="\t", fieldnames=("catch_id", "mutation", "status"))
        writer.writeheader()
        writer.writerows(catches)
    assert len(catches) == 24 and all(row["status"] == "PASS" for row in catches)

    report = (HERE / "AUDIT_REPORT.md").read_text(encoding="utf-8")
    exact = (HERE / "EXACT_DERIVATION.md").read_text(encoding="utf-8")
    ledger = (HERE / "STATUS_LEDGER.tsv").read_text(encoding="utf-8")
    for token in (
        "CMB_POLARIZATION_IS_A_PROMISING_FUTURE_GUIDEPOST",
        "NO_CURRENT_NATIVE_UDT_CMB_PREDICTION",
        "POWER_SPECTRA_ALONE_ARE_DIRECTIONALLY_INSUFFICIENT",
        "No extension was selected",
    ):
        assert token in report
    for token in ("Metric screen geometry is not physical polarization", "Exact spin-two readout algebra", "Exact information loss", "Ranked future discriminator types"):
        assert token in exact
    assert "CMB_polarization_as_current_UDT_prediction\tABSENT_OPEN_CHAIN" in ledger

    result = {
        "schema": "udt.cmb_polarization_observable_typing.verification.v1",
        "status": "PASS_VERIFIED_WITH_CAVEATS",
        "local_sources": 10,
        "external_primary_or_official_sources": 10,
        "observables": 12,
        "observable_gates": 14,
        "observable_gate_cells": 168,
        "extension_observable_cells": 144,
        "catch_proofs": 24,
        "production_replay": "PASS",
        "independent_no_production_read_replay": "PASS",
        "fresh_adversarial_review": "VERIFIED_WITH_CAVEATS",
        "current_UDT_CMB_prediction": "ABSENT_OPEN_CHAIN",
        "audit_report_sha256": hashlib.sha256((HERE / "AUDIT_REPORT.md").read_bytes()).hexdigest(),
        "status_ledger_sha256": hashlib.sha256((HERE / "STATUS_LEDGER.tsv").read_bytes()).hexdigest(),
        "observable_matrix_sha256": hashlib.sha256((HERE / "OBSERVABLE_GATE_MATRIX.tsv").read_bytes()).hexdigest(),
        "capability_matrix_sha256": hashlib.sha256((HERE / "EXTENSION_OBSERVABLE_CAPABILITY.tsv").read_bytes()).hexdigest(),
    }
    (HERE / "VERIFICATION_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
