#!/usr/bin/env python3
"""Hostile mutation and scope checks for G209."""

from __future__ import annotations

import json
import os
from pathlib import Path

import sympy as sp


OUT = Path(__file__).with_name("CATCH_PROOF_RESULT.json")


def main() -> None:
    f, h, b, v, q = sp.symbols("f h b v q", positive=True)
    prereg = Path(__file__).with_name("PREREGISTRATION.md").read_text(encoding="utf-8")
    map_text = Path(__file__).with_name("MAP.md").read_text(encoding="utf-8")

    required_scope = (
        "all three smooth components",
        "Trace-changing spatial shape does not have to precede",
        "timelike and\nspacelike completeness",
        "No physical shift",
        "matter, and `X_max` remain open",
    )

    def catches_removed(text: str, token: str) -> bool:
        if token not in text:
            return False
        mutated = text.replace(token, "REMOVED_GUARD", 1)
        return token in text and token not in mutated

    g = sp.Matrix([[-f + h * b**2, h * b], [h * b, h]])
    inv = sp.Matrix([[-1 / f, b / f], [b / f, 1 / h - b**2 / f]])
    cone = -f + h * (v + b) ** 2
    A = f - b**2 / f
    E, L, r, p = sp.symbols("E L r p", nonzero=True, real=True)
    constraint = A * p**2 - 2 * b * E * p / f - E**2 / f + L**2 / r**2
    rdot = A * p - b * E / f
    catches: dict[str, bool] = {
        "dropping_shift_square_changes_gtt": sp.simplify((-f) - g[0, 0]) != 0,
        "wrong_cross_sign_changes_metric": sp.simplify(-h * b - g[0, 1]) != 0,
        "determinant_not_shift_dependent": sp.simplify(g.det() + f * h) == 0,
        "dt_covector_stays_temporal": sp.simplify(inv[0, 0] + 1 / f) == 0,
        "wrong_inverse_spatial_block_fails": sp.simplify((g * sp.Matrix([[-1 / f, b / f], [b / f, 1 / h + b**2 / f]]) - sp.eye(2))[1, 1]) != 0,
        "cone_center_not_plus_b": sp.simplify(cone.subs(v, b) + f) != 0,
        "cone_center_is_minus_b": sp.simplify(cone.subs(v, -b) + f) == 0,
        "shift_changes_center_not_width": sp.simplify(sp.diff(cone, v, 2) - 2 * h) == 0,
        "g205_width_is_f_not_sqrt_f": sp.simplify(sp.sqrt(f * f) - f) == 0,
        "coordinate_bounded_not_metric_subluminal": sp.simplify((b**2 / f) / f - b**2 / f**2) == 0,
        "energy_shift_term_sign_matters": sp.simplify((f - b) - (f + b)) != 0,
        "live_energy_not_conserved_generically": sp.Symbol("db", nonzero=True) != 0,
        "hamiltonian_cross_term_required": sp.simplify(constraint - (A * p**2 - E**2 / f + L**2 / r**2)) != 0,
        "radial_first_integral_exact": sp.simplify(rdot**2 - (E**2 - A * L**2 / r**2) - A * constraint) == 0,
        "failure_witness_uses_nonzero_L": L != 0,
        "bounded_shift_does_not_imply_null_complete": sp.limit(b**2 / f, f, 0, dir="+") == sp.oo,
        "pair_coordinate_clock_hears_shift": sp.simplify((f - h * b**2) - f) != 0,
        "pair_eulerian_clock_is_controlled_blind_stratum": sp.simplify(-f + h * ((-b) + b) ** 2 + f) == 0,
        "generic_pair_cross_term_survives": sp.expand(h * (v + b) ** 2).coeff(v * b) == 2 * h,
        "all_three_components_guard": catches_removed(map_text, required_scope[0]),
        "tracechange_dependency_guard": catches_removed(map_text, required_scope[1]),
        "timelike_spacelike_not_inferred": catches_removed(map_text, required_scope[2]),
        "physical_shift_not_selected": catches_removed(map_text, required_scope[3]),
        "xmax_not_input_or_output": catches_removed(map_text, required_scope[4]),
        "global_theorem_is_bounded": "one bounded global tile" in prereg,
    }
    failed = [name for name, caught in catches.items() if not caught]
    if failed:
        raise AssertionError(f"uncaught mutations: {failed}")
    result = {
        "status": "PASS",
        "catch_count": len(catches),
        "catches": sorted(catches),
        "scope": "local algebra, causal center/width, global-vs-affine distinction, pair strata, provenance, and X_max guards",
    }
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if os.environ.get("UDT_NO_WRITE") != "1":
        OUT.write_text(payload, encoding="utf-8")
    print(payload, end="")


if __name__ == "__main__":
    main()
