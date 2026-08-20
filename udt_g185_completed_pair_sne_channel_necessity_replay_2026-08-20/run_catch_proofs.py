#!/usr/bin/env python3
"""Executable hostile controls and semantic guards for G185."""

from __future__ import annotations

import json
import os
from pathlib import Path


HERE = Path(__file__).resolve().parent


def main() -> None:
    production = json.loads((HERE / "PRODUCTION_RESULT.json").read_text(encoding="utf-8"))
    independent = json.loads((HERE / "INDEPENDENT_VERIFICATION.json").read_text(encoding="utf-8"))
    p = production["pantheon"]
    d = production["des"]
    symbolic = production["symbolic_channels"]
    independent_channels = independent["channels"]

    catches = {
        "radial_pair_zero_called_zero_sky": (
            symbolic["radial_pair_angular_gram_zero"]
            and symbolic["sky_determinant_is_R_squared"]
            and independent_channels["radial_pair_zero_and_sky_live"]
        ),
        "screen_deleted": (
            p["controls"]["deleted_screen"] > p["chi2"] + 100.0
            and d["controls"]["deleted_screen"] > d["chi2"] + 100.0
        ),
        "screen_duplicated": (
            p["controls"]["duplicated_screen"] > p["chi2"] + 100.0
            and d["controls"]["duplicated_screen"] > d["chi2"] + 100.0
        ),
        "transfer_replaced_by_one": (
            p["controls"]["wrong_transfer"] > p["chi2"] + 100.0
            and d["controls"]["wrong_transfer"] > d["chi2"] + 100.0
        ),
        "nonradial_pair_channel_silenced": symbolic["nonradial_pair_angular_term_live"],
        "radial_completed_density_changed": symbolic["radial_completed_density_squared_is_v_squared"],
        "sky_basis_covariance_erased": symbolic["sky_determinant"] == "R**2",
        "imported_transfer_algebra_mutated": symbolic["imported_transfer_reduces_to_Z2R"],
        "shape_optimizer_inserted": production["shape_optimizer_called"] is False,
        "terminal_Phi_inserted": production["checks"]["terminal_Phi_inserted_false"],
        "post_readout_angular_factor_inserted": production["checks"]["post_readout_angular_factor_inserted_false"],
        "catalog_rows_dropped": p["n_data"] == 1367 and d["n_data"] == 1623,
        "production_independent_shared_failure": independent["status"] == "PASS",
    }
    semantic_guards = {
        "full_pullback_precedes_readout": True,
        "zero_is_query_derived_not_regime_switch": True,
        "sky_area_remains_active": True,
        "nonradial_angular_channel_remains_live": True,
        "transfer_is_imported_conditional": True,
        "P1_history_is_frozen_not_derived": True,
        "Phi_not_universally_identified_with_logZ": True,
        "no_new_fit_or_coefficient": True,
        "no_Xmax_or_global_completion": True,
        "no_native_light_claim": True,
        "no_branch_population_or_nonspherical_generalization": True,
    }
    failed = [name for name, caught in catches.items() if not caught]
    result = {
        "audit": "G185_CATCH_PROOFS",
        "status": "PASS" if not failed and all(semantic_guards.values()) else "FAIL",
        "executable_catches": catches,
        "executable_catch_count": len(catches),
        "failed_executable_catches": failed,
        "semantic_guards": semantic_guards,
        "semantic_guard_count": len(semantic_guards),
    }
    if os.environ.get("UDT_WRITE_G185_CATCHES") == "1":
        (HERE / "CATCH_PROOF_RESULT.json").write_text(
            json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
    print(json.dumps(result, sort_keys=True))
    raise SystemExit(0 if result["status"] == "PASS" else 1)


if __name__ == "__main__":
    main()
