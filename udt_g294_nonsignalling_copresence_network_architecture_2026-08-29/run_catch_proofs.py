#!/usr/bin/env python3
"""Hostile promotion and scope catches for G294."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--package", type=Path, default=Path(__file__).resolve().parent)
    parser.add_argument("--output", type=Path, default=Path("CATCH_PROOF_RESULT.json"))
    args = parser.parse_args()

    production = json.loads((args.package / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    derivation = (args.package / "EXACT_DERIVATION.md").read_text(encoding="utf-8")
    ledger = (args.package / "STATUS_LEDGER.tsv").read_text(encoding="utf-8")
    architecture = (args.package / "ARCHITECTURE_LATTICE.tsv").read_text(encoding="utf-8")
    check_names = {item["name"] for item in production["checks"] if item["pass"]}

    catches = [
        ("nonpropagating connectedness called infinite signal speed", not production["scope"]["literal_infinite_signal_speed_adopted"]),
        ("positive distance said incompatible with pair reversal", "projective_reversal_odd" in check_names and "mutual_projection_reversal_even" in check_names),
        ("planar sech equality widened through active screen", "screen_aware_mutual_bound_factor" in check_names and "active_screen_strict_gap" in check_names),
        ("cE alone called an absolute length", "ce_power_cannot_be_pure_length" in check_names),
        ("R/cE called dimensionless dilation", "distance_over_ce_is_time_T" in check_names),
        ("symmetric co-presence graph called a global now", "symmetry_not_transitivity" in check_names),
        ("co-presence graph conflated with reciprocal groupoid", "not automatically the path-labelled reciprocal" in derivation),
        ("timelike direction called automatically integrable", "timelike_does_not_imply_integrable" in check_names),
        ("owned integrability called necessarily a new field", "does not prove that a new field is required" in derivation),
        ("correlation called controllable response", "correlated_no_response_control" in check_names),
        ("global constraint called automatically no-signalling", "constraint_nonsignalling_trilemma" in check_names),
        ("metric cones called a derived response operator", "UDT_response_operator\tOPEN" in ledger),
        ("co-presence slicing called history selection", "primary_metric_scalar_curvature" in check_names and "copresence_selects_history\tNOT_DERIVED" in ledger),
        ("candidate architecture called derived formula", "WELL_TYPED_MISSING_LAW_ARCHITECTURE_NOT_FORMULA" in json.dumps(production["architecture"])),
        ("received starlight called proven co-present readout", "distant_star_image_is_copresent_state\tOPEN" in ledger),
        ("literal instantaneous response retained", "REJECTED BY NO-SIGNALLING GATE" in architecture.upper()),
    ]

    rendered = [
        {"hostile_claim": claim, "caught": bool(caught)}
        for claim, caught in catches
    ]
    semantic_gates = {
        "copresence_adopted": production["scope"]["copresence_adopted"],
        "literal_infinite_signal_speed_adopted": production["scope"]["literal_infinite_signal_speed_adopted"],
        "history_selected": production["scope"]["history_selected"],
        "causal_response_operator_imported": production["scope"]["causal_response_operator_imported"],
        "observation_used": production["scope"]["observation_used"],
        "protected_input_used": production["scope"]["protected_input_used"],
    }
    all_pass = all(item["caught"] for item in rendered) and not any(semantic_gates.values())
    result = {
        "all_pass": all_pass,
        "catch_count": len(rendered),
        "catches": rendered,
        "semantic_gate_count": len(semantic_gates),
        "semantic_gates": semantic_gates,
    }
    if not all_pass:
        raise AssertionError(json.dumps(result, sort_keys=True))
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"all_pass": all_pass, "catch_count": len(rendered)}, sort_keys=True))


if __name__ == "__main__":
    main()
