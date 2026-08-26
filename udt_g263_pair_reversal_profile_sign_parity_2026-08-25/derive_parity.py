#!/usr/bin/env python3
"""Exact G263 parity classification on the bounded primary metric."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import sympy as sp


LANDING = (
    "PAIR_ARROW_REVERSAL_IS_EXACT_RECIPROCAL_INVOLUTION"
    "__WHOLE_PROFILE_SIGN_CONJUGATION_IS_A_DISTINCT_METRIC_INVOLUTION"
    "__SCALAR_DEPTH_INVERSION_SHARED_BUT_COMPLETE_CHANNEL_PARITIES_MIXED"
)


def derive() -> dict[str, object]:
    delta, phi, p, z, r, c = sp.symbols("delta phi p z r c", real=True)
    u, s = sp.symbols("u s", positive=True)
    checks: list[str] = []

    def exact(name: str, expression: sp.Expr) -> None:
        if sp.simplify(expression) != 0:
            raise AssertionError(name)
        checks.append(name)

    # R_pair: endpoint reversal at fixed ambient metric.
    dmat = sp.diag(sp.exp(-delta), sp.exp(delta))
    dmat_r = dmat.subs(delta, -delta)
    exact("pair_reversal_inverse", (dmat_r * dmat - sp.eye(2)).norm())
    d_even = sp.cosh(delta) * sp.eye(2)
    d_odd = sp.diag(-sp.sinh(delta), sp.sinh(delta))
    exact("pair_D_even", (d_even - (dmat + dmat_r) / 2).norm())
    exact("pair_D_odd", (d_odd - (dmat - dmat_r) / 2).norm())
    exact("pair_D_reconstruction", (dmat - d_even - d_odd).norm())
    exact("pair_clock_even", (sp.exp(-delta) + sp.exp(delta)) / 2 - sp.cosh(delta))
    exact("pair_clock_odd", (sp.exp(-delta) - sp.exp(delta)) / 2 + sp.sinh(delta))
    exact("pair_chi_odd", sp.tanh(-delta) + sp.tanh(delta))
    exact(
        "pair_contrast_even",
        (sp.trace(dmat.T * dmat) / 2 - 1) - (sp.cosh(2 * delta) - 1),
    )

    # C_phi: whole-profile sign conjugation. s=exp(phi), so C sends s->1/s.
    f = s ** -2
    lapse = s ** -1
    f_c = s**2
    lapse_c = s
    cosh1 = (s + 1 / s) / 2
    sinh1 = (s - 1 / s) / 2
    cosh2 = (s**2 + s ** -2) / 2
    sinh2 = (s**2 - s ** -2) / 2
    exact("profile_f_inverse", f * f_c - 1)
    exact("profile_lapse_inverse", lapse * lapse_c - 1)
    exact("profile_lapse_even", (lapse + lapse_c) / 2 - cosh1)
    exact("profile_lapse_odd", (lapse - lapse_c) / 2 + sinh1)
    exact("profile_f_even", (f + f_c) / 2 - cosh2)
    exact("profile_f_odd", (f - f_c) / 2 + sinh2)

    mu = r * (1 - f) / 2
    mu_c = r * (1 - f_c) / 2
    mu_even = -r * sinh1**2
    mu_odd = r * sinh2 / 2
    exact("mass_aspect_even", (mu + mu_c) / 2 - mu_even)
    exact("mass_aspect_odd", (mu - mu_c) / 2 - mu_odd)
    exact("mass_aspect_reconstruction", mu - mu_even - mu_odd)

    accel = -p / (r * s)
    accel_c = p * s / r
    accel_even = p * sinh1 / r
    accel_odd = -p * cosh1 / r
    exact("acceleration_even", (accel + accel_c) / 2 - accel_even)
    exact("acceleration_odd", (accel - accel_c) / 2 - accel_odd)

    e0 = f * (1 - 2 * p) - 1
    e0_c = f_c * (1 + 2 * p) - 1
    e0_even = cosh2 + 2 * p * sinh2 - 1
    e0_odd = -sinh2 - 2 * p * cosh2
    exact("E0_even", (e0 + e0_c) / 2 - e0_even)
    exact("E0_odd", (e0 - e0_c) / 2 - e0_odd)

    e1 = f * (2 * p**2 - 2 * p - z)
    e1_c = f_c * (2 * p**2 + 2 * p + z)
    e1_even = 2 * p**2 * cosh2 + (2 * p + z) * sinh2
    e1_odd = -2 * p**2 * sinh2 - (2 * p + z) * cosh2
    exact("E1_even", (e1 + e1_c) / 2 - e1_even)
    exact("E1_odd", (e1 - e1_c) / 2 - e1_odd)

    apar = f * (2 * p**2 + p - z)
    apar_c = f_c * (2 * p**2 - p + z)
    apar_even = 2 * p**2 * cosh2 - (p - z) * sinh2
    apar_odd = -2 * p**2 * sinh2 + (p - z) * cosh2
    exact("Aparallel_even", (apar + apar_c) / 2 - apar_even)
    exact("Aparallel_odd", (apar - apar_c) / 2 - apar_odd)

    aperp = 1 - f * (1 + p)
    aperp_c = 1 - f_c * (1 - p)
    aperp_even = 1 - cosh2 + p * sinh2
    aperp_odd = sinh2 - p * cosh2
    exact("Aperp_even", (aperp + aperp_c) / 2 - aperp_even)
    exact("Aperp_odd", (aperp - aperp_c) / 2 - aperp_odd)
    exact("angular_residual_join", apar + aperp - (e1 - e0))
    exact("conjugate_angular_residual_join", apar_c + aperp_c - (e1_c - e0_c))

    # G201 zero-tide family is not invariant under C_phi.
    x = c * r**2
    conjugate_apar = 4 * x**2 / (1 + x) ** 3
    conjugate_aperp = x**2 / (1 + x) ** 2
    f_zero_c = 1 / (1 + x)
    exact(
        "zero_tide_conjugate_Aparallel",
        (r**2 * sp.diff(f_zero_c, r, 2) - r * sp.diff(f_zero_c, r)) / 2
        - conjugate_apar,
    )
    exact(
        "zero_tide_conjugate_Aperp",
        1 - f_zero_c + r * sp.diff(f_zero_c, r) / 2 - conjugate_aperp,
    )

    return {
        "status": "PASS",
        "landing": LANDING,
        "scope": "primary_static_spherical_real_phi_positive_f_local_second_jet",
        "symbolic_check_count": len(checks),
        "symbolic_checks": checks,
        "classification": "SCALAR_EQUIVALENCE_ONLY",
        "operations": {
            "R_pair": "endpoint swap at fixed ambient metric; delta->-delta",
            "C_phi": "whole profile and jets conjugated; (phi,p,z)->(-phi,-p,-z), f->1/f",
        },
        "separation": {
            "shared": "both can invert endpoint scalar depth when C_phi acts on both endpoint values",
            "distinct": "R_pair fixes g; C_phi changes g_phi to g_minus_phi and generally changes every hierarchy channel",
            "sphere_guard": "areal r^2 dOmega^2 is unchanged under C_phi, so clock/radial coefficient exchange is not a full coframe swap",
        },
        "asymptotic_constant_jet": {
            "phi_to_positive_infinity": "N->0; mu/r->1/2; Aparallel->0; Aperp->1",
            "phi_to_negative_infinity": "N->infinity; mu/r->-infinity; Aparallel->0; Aperp->-infinity",
        },
        "ownership": {
            "pair_reversal": "DERIVED_CONDITIONAL_G170",
            "profile_conjugation": "MATHEMATICAL_DIAGNOSTIC_NOT_PHYSICAL_SYMMETRY",
            "parity_decomposition": "DERIVED_BOUNDED",
            "history_selection": "NOT_DERIVED",
            "universal_angular_loudness": "NOT_DERIVED_G201_ZERO_TIDE_COUNTERFAMILY_RETAINED",
            "physical_mass_or_source": "NOT_DERIVED",
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = derive()
    encoded = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(encoded, encoding="utf-8")
    else:
        print(encoded, end="")


if __name__ == "__main__":
    main()
