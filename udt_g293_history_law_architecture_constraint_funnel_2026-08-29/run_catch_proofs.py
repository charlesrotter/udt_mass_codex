#!/usr/bin/env python3
"""Hostile claim catches for G293."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


REQUIRED_CHECKS = {
    "endpoint_composition_does_not_imply_homogeneity": "founded composition selects homogeneity",
    "flow_composition_does_not_imply_translation_equivariance": "flow composition selects constant generator",
    "augmented_state_depth_translation_equivariance": "scalar theorem widens to complete state",
    "projective_generator_jacobian": "projective generator forgets Jacobian",
    "trivial_scalar_branch": "k=0 silently excluded",
    "parameter_rescaling_degeneracy": "k called a derived physical scale",
    "P2_zero_mean": "Euler period fixes every local mode",
    "same_total_different_local_flux": "same Euler sector fixes local flux",
    "time_live_curvature_Bianchi_closure": "time-live mixed term omitted",
    "GR_active_angular_cancellation": "GR quiet branch deletes angular modes",
    "G259_class_not_all_local_metric_two_jet_laws": "G259 widened to every local two-jet law",
}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--package", type=Path, default=Path(__file__).resolve().parent)
    parser.add_argument("--output", type=Path, default=Path("CATCH_PROOF_RESULT.json"))
    args = parser.parse_args()

    production = json.loads((args.package / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    check_map = {row["name"]: row for row in production["checks"]}
    catches: list[dict[str, object]] = []

    for name, hostile_claim in REQUIRED_CHECKS.items():
        if name not in check_map or not check_map[name]["pass"]:
            raise AssertionError(f"missing hostile catch evidence: {name}")
        catches.append(
            {
                "hostile_claim": hostile_claim,
                "evidence_check": name,
                "caught": True,
            }
        )

    scope = production["scope"]
    scope_gate = (
        scope["observations"] == 0
        and scope["fit_coefficients"] == 0
        and scope["physical_scales_selected"] == 0
        and scope["field_equations_adopted"] == 0
        and scope["protected_inputs"] == 0
        and scope["gpu"] is False
    )
    if not scope_gate:
        raise AssertionError("forbidden input entered production scope")
    catches.append(
        {
            "hostile_claim": "observation fit scale equation protected work or GPU entered",
            "evidence_check": "production_scope_zero_gate",
            "caught": True,
        }
    )

    with (args.package / "STATUS_LEDGER.tsv").open(newline="", encoding="utf-8") as handle:
        status_rows = {row["statement"]: row for row in csv.DictReader(handle, delimiter="\t")}
    semantic_gates = {
        "architecture_lattice_is_exhaustive": "NOT_CLAIMED",
        "physical_history_law": "OPEN",
        "observational_calibration": "DEFERRED",
        "arbitrary_P2_amplitude_is_metric_realized": "NOT_DERIVED",
    }
    for statement, expected in semantic_gates.items():
        actual = status_rows[statement]["status"]
        if actual != expected:
            raise AssertionError(f"{statement}: {actual} != {expected}")

    result = {
        "all_pass": True,
        "catch_count": len(catches),
        "catches": catches,
        "semantic_gate_count": len(semantic_gates),
        "semantic_gates": semantic_gates,
    }
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"all_pass": True, "catches": len(catches), "semantic_gates": len(semantic_gates)}))


if __name__ == "__main__":
    main()
