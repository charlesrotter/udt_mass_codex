#!/usr/bin/env python3
"""Semantic and algebraic mutation catches for G179."""

from __future__ import annotations

import ast
import json
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent
ETA4 = sp.diag(-1, 1, 1, 1)


def block_e(b: sp.Matrix, q: sp.Matrix, s: sp.Matrix) -> sp.Matrix:
    return b.row_join(sp.zeros(2)).col_join((q * s).row_join(q))


def pullback(e: sp.Matrix, j: sp.Matrix) -> sp.Matrix:
    return sp.simplify(j.T * e.T * ETA4 * e * j)


def main() -> None:
    derivation = json.loads((HERE / "DERIVATION_RESULT.json").read_text())
    independent = json.loads((HERE / "INDEPENDENT_VERIFICATION.json").read_text())
    tree = ast.parse((HERE / "derive_complete_coframe_extension.py").read_text())
    names = {node.id for node in ast.walk(tree) if isinstance(node, ast.Name)}

    b = sp.Matrix([[2, -2], [2, 1]])
    q = sp.Matrix([[1, 2], [2, 3]])
    s = sp.Matrix([[-1, 1], [-1, -1]])
    y = sp.Matrix([[3, 2], [-3, 1]])
    z = sp.Matrix([[1, -2], [2, -3]])
    j = y.col_join(z)
    h = pullback(block_e(b, q, s), j)
    determinant = h.det()
    m2 = -determinant

    h_no_q = pullback(block_e(b, sp.eye(2), s), j)
    h_no_s = pullback(block_e(b, q, sp.zeros(2)), j)
    scalar_s = sp.eye(2) * sp.trace(s) / 2
    h_scalar_s = pullback(block_e(b, q, scalar_s), j)
    h_no_z = pullback(block_e(b, q, s), y.col_join(sp.zeros(2)))
    h_frozen_y = pullback(block_e(b, q, s), sp.eye(2).col_join(z))
    h_shift_erased = sp.diag(h[0, 0], h[1, 1])

    arbitrary_phi = sp.log((-determinant) / h[0, 0] ** 2) / 4
    completed_phi = -sp.log(-h[0, 0]) / 2
    arclength_m2 = h[1, 1]

    forbidden_executable = {
        "X_max",
        "path",
        "holonomy",
        "jacobi",
        "source",
        "matter",
        "action",
        "fit",
        "bootstrap",
        "mu",
    }
    catches = {
        "production_and_independent_pass": derivation["status"] == "PASS"
        and independent["status"] == "PASS",
        "independent_target_reached": independent["exact_fraction_regular_trials"] >= 20_000,
        "delete_Q_changes_pullback": h_no_q != h,
        "delete_S_changes_pullback": h_no_s != h,
        "scalarize_S_changes_pullback": h_scalar_s != h,
        "delete_Z_changes_pullback": h_no_z != h,
        "freeze_Y_changes_pullback": h_frozen_y != h,
        "erase_shift_changes_density": -h_shift_erased.det() != m2,
        "arclength_is_not_completed_density": arclength_m2 != m2,
        "arbitrary_calibration_phi_is_not_completed_phi": sp.simplify(
            arbitrary_phi - completed_phi
        ) != 0,
        "wrong_determinant_sign_is_negative": determinant < 0 and determinant != m2,
        "full_four_component_S_witness": all(value != 0 for value in s),
        "nonspherical_Q_witness": q.T * q != sp.eye(2) * (q.T * q)[0, 0],
        "nonzero_shift_witness": h[0, 1] != 0,
        "singular_Y_regular_witness": derivation["checks"]["singular_Y_retained"]
        and derivation["checks"]["singular_Y_full_J_rank_two"]
        and derivation["checks"]["singular_Y_pair_regular"],
        "nonblock_coframe_control": derivation["checks"][
            "nonblock_coordinate_coframe_exercised"
        ],
        "lorentz_gauge_control": derivation["checks"]["lorentz_gauge_pullback_invariant"],
        "ambient_coordinate_control": derivation["checks"][
            "ambient_coordinate_pullback_invariant"
        ],
        "positive_density_reparameterization": derivation["checks"][
            "positive_pair_scale_determinant_density"
        ],
        "orientation_reversal_not_pair_reversal": derivation["checks"][
            "orientation_reversal_shift_sign"
        ],
        "time_live_is_product_rule_only": derivation["checks"]["query_live_product_rule"],
        "all_five_live_sectors_retained": derivation["checks"]["all_BQSYZ_sectors_live"]
        and set(derivation["sector_effects"]) == {"B", "Q", "S", "Y", "Z"},
        "no_Xmax_executable_dependency": "X_max" not in names,
        "no_path_or_transport_executable_dependency": not (
            {"path", "holonomy", "jacobi"} & names
        ),
        "no_source_matter_action_executable_dependency": not (
            {"source", "matter", "action"} & names
        ),
        "no_fit_bootstrap_mu_executable_dependency": not (
            {"fit", "bootstrap", "mu"} & names
        ),
        "forbidden_dependency_census_complete": len(forbidden_executable & names) == 0,
        "event_germ_selection_remains_open": "event_and_germ_realization" in derivation["open"],
        "global_completion_remains_open": "history_completion_and_X_max" in derivation["open"],
        "non_scalar_transport_remains_open": "non_scalar_transport" in derivation["open"],
    }
    failed = [name for name, passed in catches.items() if not passed]
    result = {
        "audit": "G179",
        "status": "PASS" if not failed and len(catches) >= 20 else "FAIL",
        "catch_count": len(catches),
        "failed": failed,
        "catches": catches,
    }
    (HERE / "CATCH_PROOF_RESULT.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n"
    )
    if result["status"] != "PASS":
        raise SystemExit(f"FAIL: {failed}")
    print(f"PASS: {len(catches)} semantic and algebraic mutation catches")


if __name__ == "__main__":
    main()
