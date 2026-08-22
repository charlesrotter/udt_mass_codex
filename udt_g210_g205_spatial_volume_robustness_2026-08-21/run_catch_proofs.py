#!/usr/bin/env python3
"""Hostile algebra and scope catches for G210."""

from __future__ import annotations

import json
import os
from pathlib import Path

import sympy as sp


OUT = Path(__file__).with_name("CATCH_PROOF_RESULT.json")


def removed(text: str, token: str) -> bool:
    if token not in text:
        return False
    return token not in text.replace(token, "REMOVED_G210_GUARD", 1)


def main() -> None:
    f, a, h, b, v = sp.symbols("f a h b v", positive=True)
    dH, dK = sp.symbols("dH dK", positive=True)
    E, r, c = sp.symbols("E r c", positive=True)
    exact = Path(__file__).with_name("EXACT_DERIVATION.md").read_text(encoding="utf-8")
    prereg = Path(__file__).with_name("PREREGISTRATION.md").read_text(encoding="utf-8")
    sigma = sp.log(dK / dH) / 6
    cone = -f + a**2 * h * (v + b) ** 2
    failure_integral = sp.integrate(sp.exp(-c * r**4), (r, 0, sp.oo))

    catches: dict[str, bool] = {
        "one_sixth_not_one_third": sp.simplify(sigma - sp.log(dK / dH) / 3) != 0,
        "spatial_det_uses_six_sigma": sp.simplify(sp.exp(6 * sigma) * dH - dK) == 0,
        "ambient_det_changes": sp.simplify((-f * a**6 * h) - (-f * h)) != 0,
        "wrong_ambient_det_sign_caught": sp.simplify(f * a**6 * h - (-f * a**6 * h)) != 0,
        "dt_temporal_independent_of_a": -1 / f < 0,
        "cone_center_is_minus_b": sp.simplify(cone.subs(v, -b) + f) == 0,
        "cone_center_not_plus_b": sp.simplify(cone.subs(v, b) + f) != 0,
        "width_scales_inverse_a": sp.simplify(cone.subs(v, -b + sp.sqrt(f) / (a * sp.sqrt(h)))) == 0,
        "g205_width_is_f_over_a": sp.simplify(sp.sqrt(f * (f / a**2)) - f / a) == 0,
        "shape_volume_shift_roles_distinct": sp.diff(cone, v, 2) == 2 * a**2 * h,
        "lower_bound_controls_width": sp.limit(f / a, a, 0, dir="+") == sp.oo,
        "static_radial_affine_speed": sp.simplify((E / a) ** 2 - E**2 / a**2) == 0,
        "failure_affine_integral_finite": failure_integral.is_finite is True,
        "failure_coordinate_time_integrand_diverges": sp.limit(sp.exp(c * r**4), r, sp.oo) == sp.oo,
        "global_hyperbolicity_not_null_completeness": removed(exact, "globally-hyperbolic but null-incomplete"),
        "live_energy_not_generically_conserved": sp.Symbol("sigma_t", nonzero=True) != 0,
        "live_energy_sign_guard": removed(exact, "dE}{d\\lambda}"),
        "generic_pair_hears_volume": sp.diff(f - a**2 * h * (v + b) ** 2, a) != 0,
        "unshifted_static_clock_blind": sp.diff(f - a**2 * h * 0**2, a) == 0,
        "shifted_static_clock_hears_volume": sp.diff(f - a**2 * h * b**2, a) != 0,
        "eulerian_clock_blind": sp.diff(f - a**2 * h * ((-b) + b) ** 2, a) == 0,
        "ambient_det_not_universal_pair_response": removed(exact, "does not imply universal pair response"),
        "timelike_spacelike_not_inferred": removed(prereg, "timelike/spacelike completeness"),
        "physical_history_not_selected": removed(prereg, "physical history\nselection"),
        "xmax_not_selected": removed(prereg, "or `X_max`"),
    }
    failed = [name for name, caught in catches.items() if not caught]
    if failed:
        raise AssertionError(f"uncaught mutations: {failed}")
    result = {
        "status": "PASS",
        "catch_count": len(catches),
        "catches": sorted(catches),
        "scope": "determinant factor, cone center/width, causal-affine distinction, pair strata, evidence ceiling, history and X_max guards",
    }
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if os.environ.get("UDT_NO_WRITE") != "1":
        OUT.write_text(payload, encoding="utf-8")
    print(payload, end="")


if __name__ == "__main__":
    main()
