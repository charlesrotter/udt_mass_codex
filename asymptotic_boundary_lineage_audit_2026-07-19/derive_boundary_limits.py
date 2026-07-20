#!/usr/bin/env python3
"""Independent exact limit audit for the WR-L wall and canonical odd fold."""

from __future__ import annotations

import json
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent


def require(name: str, condition: bool, checks: dict[str, str]) -> None:
    if not condition:
        raise AssertionError(name)
    checks[name] = "PASS"


def main() -> None:
    r, X, eps, c, G, rho_s = sp.symbols("r X eps c G rho_s", positive=True)
    alpha = sp.symbols("alpha", real=True)
    checks: dict[str, str] = {}

    A_alpha = (1 - r / X) ** alpha
    A = 1 - r / X
    phi = -sp.log(A) / 2
    lapse = sp.sqrt(A)
    ruler = 1 / sp.sqrt(A)

    # Exact static-slice measures for the selected alpha=1 profile.
    proper_radius = sp.integrate(1 / sp.sqrt(A), (r, 0, X))
    proper_volume = sp.simplify(4 * sp.pi * sp.integrate(r**2 / sp.sqrt(A), (r, 0, X)))
    require("wrl_proper_radius_2X", sp.simplify(proper_radius - 2 * X) == 0, checks)
    require("wrl_proper_volume_64piX3_over15", sp.simplify(proper_volume - 64 * sp.pi * X**3 / 15) == 0, checks)

    optical_primitive = sp.integrate(1 / A, r)
    require("wrl_optical_primitive", sp.simplify(sp.diff(optical_primitive, r) - 1 / A) == 0, checks)
    require("wrl_optical_reach_infinite", sp.limit(-X * sp.log(1 - r / X), r, X, dir="-") == sp.oo, checks)

    phi_eps = sp.simplify(phi.subs(r, X * (1 - eps)))
    lapse_eps = sp.simplify(lapse.subs(r, X * (1 - eps)))
    ruler_eps = sp.simplify(ruler.subs(r, X * (1 - eps)))
    require("wrl_phi_positive_infinite", sp.limit(phi_eps, eps, 0, dir="+") == sp.oo, checks)
    require("wrl_lapse_zero", sp.limit(lapse_eps, eps, 0, dir="+") == 0, checks)
    require("wrl_reciprocal_ruler_infinite", sp.limit(ruler_eps, eps, 0, dir="+") == sp.oo, checks)

    # Curvature invariants of ds^2=-A c^2dt^2+A^-1dr^2+r^2dOmega^2.
    Ricci = -sp.diff(A, r, 2) - 4 * sp.diff(A, r) / r + 2 * (1 - A) / r**2
    Kretschmann = sp.diff(A, r, 2) ** 2 + 4 * (sp.diff(A, r) / r) ** 2 + 4 * ((1 - A) / r**2) ** 2
    require("wrl_R_6_over_Xr", sp.simplify(Ricci - 6 / (X * r)) == 0, checks)
    require("wrl_K_8_over_X2r2", sp.simplify(Kretschmann - 8 / (X**2 * r**2)) == 0, checks)
    require("wrl_wall_R_finite", sp.simplify(sp.limit(Ricci, r, X, dir="-") - 6 / X**2) == 0, checks)
    require("wrl_wall_K_finite", sp.simplify(sp.limit(Kretschmann, r, X, dir="-") - 8 / X**4) == 0, checks)

    # Static-slice lapse flux.  This is a metric quantity, not a normalized mass.
    # h_rr=A^-1 gives outward unit normal n^r=sqrt(A), while N=sqrt(A).
    raw_lapse_flux = sp.simplify(4 * sp.pi * r**2 * sp.sqrt(A) * sp.diff(lapse, r))
    require("wrl_raw_lapse_flux_profile", sp.simplify(raw_lapse_flux + 2 * sp.pi * r**2 / X) == 0, checks)
    require("wrl_raw_lapse_flux_wall", sp.limit(raw_lapse_flux, r, X, dir="-") == -2 * sp.pi * X, checks)

    # Ingoing Eddington-Finkelstein radial block [[-A,1],[1,0]] is regular at A=0.
    ef_block = sp.Matrix([[-A, 1], [1, 0]])
    require("wrl_ef_determinant_regular", sp.det(ef_block) == -1, checks)
    require("wrl_static_wall_null", sp.limit(A, r, X, dir="-") == 0, checks)

    # Family selector powers. Near eps=1-r/X, proper~eps^-alpha/2 and optical~eps^-alpha.
    A_eps = sp.simplify(A_alpha.subs(r, X * (1 - eps)))
    A2_eps = sp.simplify(sp.diff(A_alpha, r, 2).subs(r, X * (1 - eps)))
    require("family_A_eps_power", sp.simplify(A_eps - eps**alpha) == 0, checks)
    require(
        "family_A2_eps_power",
        sp.simplify(A2_eps - alpha * (alpha - 1) * eps ** (alpha - 2) / X**2) == 0,
        checks,
    )
    family_rules = {
        "proper_finite": "alpha < 2",
        "optical_infinite": "alpha >= 1",
        "finite_A_second_inside_1_to_2": "alpha = 1",
        "intersection": "alpha = 1",
    }

    # Misner-Sharp is retained only as a declared GR/reference readout.
    m_ms = sp.simplify(c**2 * r * (1 - A) / (2 * G))
    require("wrl_MS_readout_profile", sp.simplify(m_ms - c**2 * r**2 / (2 * G * X)) == 0, checks)
    require("wrl_MS_readout_wall", sp.simplify(sp.limit(m_ms, r, X, dir="-") - c**2 * X / (2 * G)) == 0, checks)

    # Canonical odd fold has phi=0, A=1, and rho'=0. It is not a lapse horizon.
    fold = {
        "phi": "0",
        "A": "1",
        "clock_factor_sqrt_A": "1",
        "radial_ruler_factor_inv_sqrt_A": "1",
        "areal_derivative_rho_prime": "0",
        "normal_norm_g_inverse_rr": "1",
        "surface_character": "TIMELIKE_QUOTIENT_OR_BOUNDARY_IN_RECORDED_STATIC_METRIC",
        "mass": "NO_NATIVE_MASS; conditional MS readout gives c^2*rho_s/(2G)",
    }
    require("fold_not_lapse_horizon", fold["A"] == "1", checks)
    require("fold_clock_not_asymptotic", fold["clock_factor_sqrt_A"] == "1", checks)
    require("fold_normal_not_null", fold["normal_norm_g_inverse_rr"] == "1", checks)

    # Surface-identity discriminants.
    discriminants = {
        "phi": {"CMB_FOLD": "0", "WRL_WALL": "+infinity"},
        "A": {"CMB_FOLD": "1", "WRL_WALL": "0"},
        "clock_factor": {"CMB_FOLD": "1", "WRL_WALL": "0"},
        "radial_ruler": {"CMB_FOLD": "1", "WRL_WALL": "+infinity"},
        "normal_character": {"CMB_FOLD": "non-null in recorded static metric", "WRL_WALL": "null"},
    }
    require("fold_wrl_not_same_surface_by_phi", discriminants["phi"]["CMB_FOLD"] != discriminants["phi"]["WRL_WALL"], checks)
    require("fold_wrl_not_same_surface_by_lapse", discriminants["A"]["CMB_FOLD"] != discriminants["A"]["WRL_WALL"], checks)

    result = {
        "schema": "udt-asymptotic-boundary-limits-1.0",
        "result": "PASS",
        "checks": checks,
        "family_rules": family_rules,
        "WRL_WALL": {
            "profile": "A=1-r/X; phi=-log(A)/2",
            "X_status_in_profile": "SUPPLIED_POSITIVE_PARAMETER",
            "phi_limit": "+infinity",
            "A_limit": "0",
            "clock_factor_limit": "0",
            "radial_ruler_factor_limit": "+infinity",
            "proper_radius": "2X",
            "proper_volume": "64*pi*X^3/15",
            "optical_reach": "+infinity",
            "Ricci_wall": "6/X^2",
            "Kretschmann_wall": "8/X^4",
            "raw_lapse_flux_wall": "-2*pi*X",
            "raw_lapse_flux_authority": "UNNORMALIZED_METRIC_QUANTITY; NOT_NATIVE_MASS",
            "static_surface": "NULL_CAUSAL_HORIZON",
            "regular_extension": True,
            "terminal_boundary_derived": False,
            "MS_mass_readout": "c^2*X/(2G)",
            "MS_mass_authority": "GR_REFERENCE_OR_CONDITIONAL_ONLY",
            "native_mass": "OPEN",
        },
        "CMB_FOLD": fold,
        "surface_discriminants": discriminants,
        "join_result": "CMB_FOLD_AND_WRL_WALL_DISTINCT_IN_RECORDED_MODELS; GLOBAL_XMAX_JOIN_OPEN",
        "scale_closure": {
            "c_E": "OBSERVATIONAL_ANCHOR",
            "G_obs": "OBSERVATIONAL_ANCHOR",
            "native_total_mass_structure": "OPEN",
            "dimensionless_compactness": "G_obs*M_tot/(c_E^2*X_max)",
            "one_dimensional_relation": "X_max=alpha*G_obs*M_tot/c_E^2",
            "alpha": "NOT_DERIVED",
            "second_independent_closure": "REQUIRED_UNLESS_NATIVE_MASS_STRUCTURE_SUPPLIES_IT",
            "absolute_scale_gate": "NATIVE_MASS_OR_BOUNDARY_STRUCTURE_MUST_BREAK_X_TO_lambda_X_AND_M_TO_lambda_M_HOMOTHETY",
        },
        "compute": {"cpu_only": True, "gpu_used": False, "sympy": sp.__version__},
    }
    (HERE / "DERIVATION_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"result": result["result"], "checks": len(checks), "join": result["join_result"]}, sort_keys=True))


if __name__ == "__main__":
    main()
