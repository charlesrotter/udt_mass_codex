#!/usr/bin/env python3
"""G189 algebraic mutation and scope catches."""

from __future__ import annotations

import json
import math
import os
from pathlib import Path

import numpy as np


HERE = Path(__file__).resolve().parent


def main() -> None:
    production = json.loads((HERE / "PRODUCTION_RESULT.json").read_text(encoding="utf-8"))
    z = np.geomspace(1.0001, 4.0, 2048)
    chi = np.tanh(np.log(z))
    candidate = z**2 * chi
    deleted_screen = z**2
    alternate_transfer = z**1.5 * chi
    p1 = 1.0559332414320268 * z**2 * (
        1.0 - z ** (-2.0 / 1.0559332414320268)
    )
    fitted_power = z**2 * np.tanh(0.9 * np.log(z))

    algebraic = {
        "screen_deletion_changes_curve": float(np.max(np.abs(candidate - deleted_screen))) > 0.5,
        "transfer_exponent_change_changes_curve": float(
            np.max(np.abs(candidate - alternate_transfer))
        ) > 0.1,
        "p1_injection_changes_curve": float(np.max(np.abs(candidate - p1))) > 0.1,
        "fitted_shape_power_changes_curve": float(
            np.max(np.abs(candidate - fitted_power))
        ) > 0.01,
        "chi_is_positive_on_outgoing_domain": bool(np.all(chi > 0.0)),
        "coincidence_limit_zero": abs(math.tanh(math.log(1.0))) == 0.0,
        "reversal_is_odd": max(
            abs(math.tanh(math.log(value)) + math.tanh(math.log(1.0 / value)))
            for value in (1.01, 1.3, 2.0, 5.0)
        ) <= 2e-16,
        "production_classification_is_preregistered_negative": production.get("landing")
        == "R_PROPORTIONAL_CHI_JOIN_REJECTED_IN_DECLARED_SNE_INTERFACE",
        "regular_center_type_failure_retained": production.get("type_landing")
        == "R_PROPORTIONAL_CHI_NOT_A_SMOOTH_REGULAR_CENTER_STATIC_HISTORY",
    }
    source = (HERE / "derive_p1_free_flux_interface.py").read_text(encoding="utf-8")
    report_source = (HERE / "PREREGISTRATION.md").read_text(encoding="utf-8")
    scope = {
        "candidate_function_contains_no_frozen_n": (
            "def model_chi" in source
            and "return 5.0 * np.log10(scale**2 * chi_radius_shape(z))" in source
        ),
        "shape_optimizer_forbidden": "No shape parameter" in report_source,
        "xmax_forbidden": "`X_max`" in report_source,
        "transfer_is_imported": "IMPORTED_CONDITIONAL" in report_source,
        "join_is_provisional": "CHOSE/PROVISIONAL_CONTROL" in report_source,
        "kernel_negative_forbidden": "They cannot\nreject the reciprocal kernel" in report_source,
        "p1_reference_only": "FROZEN_REFERENCE_ONLY" in report_source,
        "globalization_forbidden": "general cosmology" in report_source,
        "scope_correction_present": (HERE / "SCOPE_CORRECTION_PREREGISTRATION.md").is_file(),
    }
    result = {
        "audit": "G189_CATCH_PROOFS",
        "status": "PASS" if all(algebraic.values()) and all(scope.values()) else "FAIL",
        "algebraic_mutation_catches": algebraic,
        "scope_guards": scope,
        "algebraic_mutation_count": len(algebraic),
        "scope_guard_count": len(scope),
    }
    if os.environ.get("UDT_WRITE_G189_CATCHES") == "1":
        (HERE / "CATCH_PROOF_RESULT.json").write_text(
            json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
    print(json.dumps(result, sort_keys=True))
    raise SystemExit(0 if result["status"] == "PASS" else 1)


if __name__ == "__main__":
    main()
