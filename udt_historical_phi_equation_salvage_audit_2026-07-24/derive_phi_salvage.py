#!/usr/bin/env python3
"""Exact bounded algebra for the historical phi-equation salvage audit."""

from __future__ import annotations

import json
import platform
from pathlib import Path

import sympy as sp


def exact_zero(expr: sp.Expr) -> bool:
    return sp.simplify(sp.together(expr)) == 0


def main() -> None:
    r, mu, X, C = sp.symbols("r mu X C", positive=True, finite=True)
    phi = sp.Function("phi")(r)
    psi = sp.Function("psi")(r)
    background = sp.Function("background")(r)
    source = sp.Function("S")(r)

    warp = sp.exp(-2 * phi)
    phi_r = sp.diff(phi, r)

    radial_box = sp.diff(r**2 * warp * phi_r, r) / r**2
    radial_box_expanded = warp * (
        sp.diff(phi, r, 2) + 2 * phi_r / r - 2 * phi_r**2
    )
    gtheta_mixed = warp * (
        2 * phi_r**2 - sp.diff(phi, r, 2) - 2 * phi_r / r
    )

    # The probe scalar psi is varied while the metric background is held fixed.
    background_warp = sp.exp(-2 * background)
    lag_probe = (
        r**2
        * (
            background_warp * sp.diff(psi, r) ** 2
            + mu**2 * psi**2
            - 2 * source * psi
        )
        / 2
    )
    el_probe = sp.diff(lag_probe, psi) - sp.diff(
        sp.diff(lag_probe, sp.diff(psi, r)), r
    )
    probe_lhs = (
        sp.diff(r**2 * background_warp * sp.diff(psi, r), r) / r**2
        - mu**2 * psi
    )

    # The metric-determining phi is varied everywhere it occurs, including g[phi].
    lag_self = (
        r**2
        * (warp * phi_r**2 + mu**2 * phi**2 - 2 * source * phi)
        / 2
    )
    el_self = sp.diff(lag_self, phi) - sp.diff(
        sp.diff(lag_self, phi_r), r
    )
    self_lhs = warp * (
        sp.diff(phi, r, 2) + 2 * phi_r / r - phi_r**2
    ) - mu**2 * phi
    probe_phi_lhs = radial_box - mu**2 * phi

    sinh_profile = C * sp.sinh(mu * r) / (mu * r)
    sinh_residual = (
        sp.diff(sinh_profile, r, 2)
        + 2 * sp.diff(sinh_profile, r) / r
        - mu**2 * sinh_profile
    )

    wrl_phi = -sp.log(1 - r / X) / 2
    wrl_warp = sp.exp(-2 * wrl_phi)
    wrl_box = sp.simplify(
        sp.diff(r**2 * wrl_warp * sp.diff(wrl_phi, r), r) / r**2
    )
    wrl_screened_residual = sp.simplify(wrl_box - mu**2 * wrl_phi)

    checks = {
        "radial_box_expansion": exact_zero(radial_box - radial_box_expanded),
        "box_phi_equals_minus_Gtheta": exact_zero(radial_box + gtheta_mixed),
        "probe_EL_matches_fixed_background_screened_equation": exact_zero(
            el_probe + r**2 * (probe_lhs + source)
        ),
        "self_EL_matches_self_consistent_equation": exact_zero(
            el_self + r**2 * (self_lhs + source)
        ),
        "self_minus_probe_operator": exact_zero(
            self_lhs - probe_phi_lhs - warp * phi_r**2
        ),
        "linear_vacuum_sinh_solution": exact_zero(sinh_residual),
        "WRL_box_exact": exact_zero(wrl_box - 1 / (X * r)),
        "WRL_not_zero_source_screened_for_finite_constant_mu": (
            sp.limit(wrl_screened_residual, r, 0, dir="+") is sp.oo
            and sp.limit(wrl_screened_residual, r, X, dir="-") is -sp.oo
        ),
    }

    result = {
        "environment": {
            "python": platform.python_version(),
            "sympy": sp.__version__,
        },
        "scope": "static_spherical_diagonal_areal_radius_control",
        "expressions": {
            "sqrt_minus_g_without_angular_factor": "c*r**2",
            "box_phi": str(sp.simplify(radial_box_expanded)),
            "Gtheta_mixed": str(sp.simplify(gtheta_mixed)),
            "probe_phi_lhs": str(sp.simplify(probe_phi_lhs)),
            "self_phi_lhs": str(sp.simplify(self_lhs)),
            "self_minus_probe": str(sp.simplify(self_lhs - probe_phi_lhs)),
            "linear_vacuum_solution": str(sinh_profile),
            "WRL_box_phi": str(wrl_box),
            "WRL_screened_zero_source_residual": str(wrl_screened_residual),
        },
        "checks": checks,
        "check_count": len(checks),
        "pass_count": sum(bool(value) for value in checks.values()),
        "all_pass": all(checks.values()),
        "maximum_conclusion": (
            "exact metric identities plus conditional fixed-background probe "
            "mathematics only; no native action, source, screening scale, "
            "universal phi law, or bilocal observer transition is derived"
        ),
    }

    output = Path(__file__).with_name("DERIVATION_RESULT.json")
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))
    if not result["all_pass"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()

