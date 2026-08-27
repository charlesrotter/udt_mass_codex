#!/usr/bin/env python3
"""Read-only replay of saved load-bearing SNe lineage outputs."""

from __future__ import annotations

import json
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent


def load(relative: str) -> dict:
    return json.loads((ROOT / relative).read_text())


def main() -> None:
    m3 = load("udt_xmax_scale_observational_M3_runs_2026-08-07/sne_results.json")
    g236 = load("udt_g236_dual_sne_relational_state_reconstruction_2026-08-23/PRODUCTION_RESULT.json")
    g237 = load("udt_g237_dual_sne_joint_relational_state_freeze_2026-08-23/JOINT_STATE_RESULT.json")
    g278 = load("udt_g278_cepheid_scale_attachment_des_holdout_2026-08-27/DERIVATION_RESULT.json")
    g279 = load("udt_g279_native_kernel_observational_interface_provenance_audit_2026-08-27/DERIVATION_RESULT.json")
    g280 = load("udt_g280_projective_position_optical_area_bridge_audit_2026-08-27/DERIVATION_RESULT.json")

    p1 = m3["fits"]["A:zCMB:P1"]
    p2 = m3["fits"]["A:zCMB:P2"]
    checks = {
        "m3_has_18_registered_fits": len(m3["fits"]) == 18,
        "m3_P1_score_exact": math.isclose(p1["chi2"], 1260.8480887040496, abs_tol=1e-12),
        "m3_P1_has_fitted_shape": p1["shape_name"] == "inv_n" and p1["shape"] is not None,
        "m3_P1_beats_P2_only_inside_menu": p1["chi2"] < p2["chi2"],
        "g236_pass": g236["status"] == "PASS",
        "g236_landing_exact": g236["landing"] == "DUAL_SNE_RELATIONAL_STATE_CONCORDANCE_LEAD",
        "g236_no_P1": g236["checks"]["p1_not_used"] is True,
        "g236_processed_caveat": g236["checks"]["processed_release_caveat_retained"] is True,
        "g236_no_profile_optimizer": g236["checks"]["no_profile_optimizer"] is True,
        "g237_pass": g237["status"] == "PASS",
        "g237_landing_exact": g237["landing"] == "JOINT_DUAL_SNE_RELATIVE_STATE_FROZEN_WITH_CAVEATS",
        "g237_primary_K12": g237["primary_resolution"] == 12,
        "g237_state_rows_56": g237["state_rows"] == 56,
        "g278_resolution_sensitive": g278["landing"] == "SCALE_ATTACHMENT_RESOLUTION_OR_SUBSET_SENSITIVE",
        "g278_DES_is_holdout": g278["frozen"]["DES_parameters_fitted"] == 0,
        "g278_kernel_not_retuned": g278["frozen"]["kernel_retuned"] is False,
        "g278_shape_not_retuned": g278["frozen"]["state_shape_retuned_by_calibrators"] is False,
        "g278_no_P1": g278["frozen"]["P1_used"] is False,
        "g278_no_Xmax": g278["frozen"]["Xmax_used"] is False,
        "g278_transfer_is_imported": g278["conditionality"]["transparent_radiative_transfer"] == "CONDITIONAL_IMPORT",
        "g279_pass": g279["status"] == "PASS",
        "g279_kernel_not_fitted": g279["key_findings"]["kernel_function_fitted"] is False,
        "g279_empirical_attachment_explicit": g279["key_findings"]["processed_release_and_transfer_imports_are_declared"] is True,
        "g280_pass": g280["status"] == "PASS",
        "g280_zero_fitted_coefficients": g280["fitted_coefficients"] == 0,
        "g280_no_observations": g280["observational_outcomes_used"] == 0,
        "g280_native_area_separator": g280["checks"]["distinct_regular_native_Jacobi_area_at_fixed_projective_state"] is True,
    }
    if not all(checks.values()):
        raise AssertionError(
            json.dumps(
                {
                    "checks": checks,
                    "failed": [name for name, passed in checks.items() if not passed],
                },
                indent=2,
                sort_keys=True,
            )
        )
    print(
        json.dumps(
            {
                "audit": "G281_SAVED_LINEAGE_OUTPUT_REPLAY",
                "status": "PASS",
                "checks": checks,
                "control_values": {
                    "M3_P1_chi2": p1["chi2"],
                    "M3_P1_ndof": p1["ndof"],
                    "M3_P1_shape": p1["shape"],
                    "G278_resolution_chi2": g278["gates"]["resolution_chi2"],
                    "G278_resolution_ceiling": g278["gates"]["resolution_ceiling"],
                },
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
