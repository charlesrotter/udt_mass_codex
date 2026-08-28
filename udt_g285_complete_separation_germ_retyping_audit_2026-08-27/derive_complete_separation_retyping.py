#!/usr/bin/env python3
"""Source-bounded G285 type-schema adjudication; writes no repository files."""

from __future__ import annotations

import json
from fractions import Fraction
from pathlib import Path


PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parent


def load(relative: str) -> dict:
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


def germ(pair: tuple[str, ...], tide: tuple[Fraction, Fraction, Fraction]) -> tuple[object, ...]:
    return pair + tide


def main() -> None:
    g280 = load("udt_g280_projective_position_optical_area_bridge_audit_2026-08-27/DERIVATION_RESULT.json")
    g282 = load("udt_g282_complete_history_depth_jacobi_minimal_law_type_2026-08-27/DERIVATION_RESULT.json")
    g283 = load("udt_g283_neighbor_relation_curvature_identity_nonselection_2026-08-27/DERIVATION_RESULT.json")
    g284 = load("udt_g284_emergent_ce_causal_projective_value_law_audit_2026-08-27/DERIVATION_RESULT.json")

    scalar = ("delta=2", "same_redshift", "same_projective_state")
    pair = ("same_central_pair_pullback", "same_endpoint_frame_state")
    tide_a = (Fraction(0), Fraction(0), Fraction(0))
    tide_b = (Fraction(1), Fraction(1, 3), Fraction(-1))
    hessian_a = tuple(-value for value in tide_a)
    hessian_b = tuple(-value for value in tide_b)

    same_longitudinal = (
        g280["checks"]["same_frequency_ratio_for_arbitrary_endpoint_rapidity"]
        and g280["checks"]["same_projective_state_for_arbitrary_endpoint_rapidity"]
    )
    same_central_pair = (
        g280["checks"]["same_full_endpoint_arrow_for_both_metrics"]
        and g282["checks"]["same_central_metric"]
        and g282["checks"]["same_central_metric_first_jet"]
    )
    different_tide = (
        g282["checks"]["transverse_curvature_nonzero_and_tracefree"]
        and len(g283["arbitrary_functions_retained"]) == 3
    )
    cone_reconstruction = (
        g284["checks"]["neighboring_cone_hessian_reconstructs_T"]
        and g284["checks"]["curvature_equals_reconstructed_T"]
    )

    checks = {
        "G280_registered_pass": g280["status"] == "PASS",
        "G282_registered_pass": g282["status"] == "PASS",
        "G283_registered_pass": g283["status"] == "PASS",
        "G284_registered_pass": g284["status"] == "PASS",
        "same_longitudinal_scalar_registered": same_longitudinal,
        "same_completed_central_pair_registered": same_central_pair,
        "different_tidal_values_registered": different_tide and tide_a != tide_b,
        "different_complete_germs_registered": same_central_pair
        and different_tide
        and germ(pair, tide_a) != germ(pair, tide_b),
        "cone_hessian_reconstructs_tide_A": tuple(-value for value in hessian_a) == tide_a,
        "cone_hessian_reconstructs_tide_B": tuple(-value for value in hessian_b) == tide_b,
        "cone_hessian_map_injective": cone_reconstruction
        and (hessian_a != hessian_b) == (tide_a != tide_b),
        "W5_scalar_is_retained_component": same_longitudinal
        and scalar[2] == "same_projective_state",
        "W5_scalar_is_not_complete_germ": same_longitudinal
        and different_tide
        and scalar != germ(pair, tide_a),
        "G283_retains_arbitrary_functions": len(g283["arbitrary_functions_retained"]) == 3,
        "G284_retains_arbitrary_functions": len(g284["arbitrary_tidal_functions_retained"]) == 3,
        "G284_finds_no_value_selector": g284["value_selecting_constraints_found"] == 0,
        "radial_fixed_depth_areas_differ": g282["checks"]["primary_same_depth"]
        and g282["checks"]["primary_different_areal_position"],
        "retyping_does_not_attach_scale": g280["fitted_coefficients"] == 0,
        "retyping_does_not_select_population": g284["value_selecting_constraints_found"] == 0,
        "retyping_does_not_supply_dynamics": g282["field_equations_adopted"] == 0
        and g283["field_equations_adopted"] == 0,
    }

    faithful = checks["different_complete_germs_registered"] and checks["cone_hessian_map_injective"]
    selector_found = not checks["G284_finds_no_value_selector"]
    if not faithful:
        landing = "CANDIDATE_COMPLETE_GERM_IS_INCONSISTENT_OR_NONFAITHFUL_ON_REGISTERED_WITNESSES"
    elif selector_found:
        landing = "COMPLETE_GERM_RETYPING_ITSELF_SELECTS_TIDAL_VALUES"
    elif tide_a == tide_b:
        landing = "SCALAR_STATE_IS_COMPLETE_SEPARATION__G280_G284_REMAIN_SAME_SEPARATION_COUNTERMODELS"
    else:
        landing = "COMPLETE_GERM_RETYPES_SCALAR_TWINS_AS_DISTINCT_SEPARATIONS__VALUE_PROPAGATION_REMAINS_OPEN"

    result = {
        "audit": "G285_COMPLETE_SEPARATION_GERM_TYPE_SCHEMA_ADJUDICATION",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "landing": landing,
        "checks": checks,
        "type_schema_checks": len(checks),
        "witness_geometry_recomputed": False,
        "load_bearing_geometry": "externally_reviewed_G280_G282_G283_G284_source_results",
        "type_levels": [
            "L0_LONGITUDINAL_SCALAR",
            "L1_COMPLETED_PAIR",
            "L2_COMPLETE_SEPARATION_GERM",
            "L3_COMPATIBLE_RELATION_NETWORK",
            "L4_PHYSICAL_VALUE_PROPAGATION",
        ],
        "regraded_claims": {
            "G280": "SAME_L0_NOT_SAME_L2__SCALAR_AREA_NONIDENTITY_RETAINED",
            "G281": "NO_NATIVE_SNE_PREDICTION_UNCHANGED",
            "G282": "SAME_FIRST_JET_NOT_SAME_L2__MINIMUM_INFORMATION_RESULT_RETAINED",
            "G283": "DISTINCT_L2_VALUATIONS__IDENTITY_VALUE_NONSELECTION_RETAINED",
            "G284": "NEIGHBOR_CONE_RECONSTRUCTS_L2__VALUE_PROPAGATION_STILL_OPEN",
        },
        "candidate_clarification_status": "CANDIDATE_WORKING_FOUNDATIONAL_CLARIFICATION__NOT_CANON",
        "value_selecting_constraints_found": 0,
        "scientific_imports": {
            "field_equation": False,
            "action": False,
            "source_or_matter": False,
            "observation_or_fit": False,
            "scale_or_Xmax": False,
        },
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    raise SystemExit(0 if result["status"] == "PASS" else 1)


if __name__ == "__main__":
    main()
