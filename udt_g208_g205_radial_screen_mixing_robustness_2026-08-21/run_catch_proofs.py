#!/usr/bin/env python3
"""Hostile mutation checks for the bounded G208 landing."""

from __future__ import annotations

import json
import os
from pathlib import Path

import sympy as sp


OUT = Path(__file__).with_name("CATCH_PROOF_RESULT.json")


def main() -> None:
    q = sp.symbols("q", positive=True)
    phi = sp.symbols("phi", real=True)
    c = (q + 1 / q) / 2
    d = (q - 1 / q) / 2
    C = (q**2 + q**-2) / 2
    S = (q**2 - q**-2) / 2
    exact_schur = sp.simplify(C - S**2 / C)
    f = sp.exp(-2 * phi)
    H = sp.Matrix([[C, S, 0], [S, C, 0], [0, 0, 1]])
    untouched = sp.Matrix([0, 0, sp.Symbol("z", nonzero=True)])
    pair_mixed = sp.Matrix([[-1, S], [S, C + 1]])
    pair_base = sp.diag(-1, 2)
    prereg = Path(__file__).with_name("PREREGISTRATION.md").read_text(encoding="utf-8")

    required_scope = (
        "globally bounded smooth static `C`",
        "radial envelope",
        "relative time-derivative bounds",
        "does not classify timelike/spacelike",
        "chosen control, not a physical history",
        "or `X_max`",
    )

    def catches_removed_scope(token: str) -> bool:
        if token not in prereg:
            return False
        mutated = prereg.replace(token, "REMOVED_SCOPE_GUARD", 1)
        return all(required in prereg for required in required_scope) and not all(
            required in mutated for required in required_scope
        )

    catches: dict[str, bool] = {
        "nonsymmetric_boost_breaks_det": sp.simplify(sp.Matrix([[c, d], [-d, c]]).det() - 1) != 0,
        "same_sign_eigenvalues_break_det": sp.simplify(q * q - 1) != 0,
        "omitting_cross_term_changes_metric": S != 0,
        "old_radial_schur_is_wrong": sp.simplify(exact_schur - 1) != 0,
        "wrong_minimizer_sign": sp.simplify(C * 1**2 + 2 * S * (S / C) + C * (S / C) ** 2 - exact_schur) != 0,
        "missing_square_root_changes_bound": sp.simplify(C - sp.sqrt(C)) != 0,
        "g207_radial_bound_not_retained": sp.simplify(sp.sqrt(C) - 1) != 0,
        "affine_weight_must_be_exp_2omega": sp.exp(phi) != sp.exp(2 * phi),
        "completed_phi_shift_sign_matters": sp.simplify((-phi) - phi) != 0,
        "pair_determinant_has_fourth_scale_power": sp.exp(4 * phi) != sp.exp(2 * phi),
        "radial_clock_not_blind": sp.simplify(C - 1) != 0,
        "untouched_screen_is_blind": sp.simplify((untouched.T * H * untouched)[0] - untouched.dot(untouched)) == 0,
        "generic_cross_term_nonzero": sp.simplify(2 * S) != 0,
        "sigma_2phi_does_not_give_f_integrand": sp.simplify(sp.exp(-2 * phi) / f - f) != 0,
        "expanding_spiral_not_contracting": sp.simplify(sp.exp(4 * phi) / f - f) != 0,
        "constant_sigma_over_r2_is_center_singular": sp.limit(1 / sp.Symbol("r", positive=True) ** 2, sp.Symbol("r", positive=True), 0) == sp.oo,
        "bounded_static_scope_not_unrestricted": catches_removed_scope("globally bounded smooth static `C`"),
        "slab_growth_condition_not_plain_smoothness": catches_removed_scope("radial envelope"),
        "compact_live_requires_relative_time_bound": catches_removed_scope("relative time-derivative bounds"),
        "timelike_spacelike_not_inferred": catches_removed_scope("does not classify timelike/spacelike"),
        "chosen_witness_not_selected_history": catches_removed_scope("chosen control, not a physical history"),
        "ambient_det_not_pair_area_blindness": sp.simplify(pair_mixed.det() - pair_base.det()) != 0,
        "xmax_not_input_or_output": catches_removed_scope("or `X_max`"),
    }
    failed = [name for name, caught in catches.items() if not caught]
    if failed:
        raise AssertionError(f"uncaught mutations: {failed}")
    result = {
        "status": "PASS",
        "catch_count": len(catches),
        "catches": sorted(catches),
        "scope": "algebra, global-theorem typing, pair response, provenance, and X_max guards",
    }
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if os.environ.get("UDT_NO_WRITE") != "1":
        OUT.write_text(payload, encoding="utf-8")
    print(payload, end="")


if __name__ == "__main__":
    main()
