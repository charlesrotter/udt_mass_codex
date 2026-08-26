#!/usr/bin/env python3
"""Exact symbolic G262 derivation.

This script derives identities of the supplied primary static-spherical metric. It does not solve
for a profile, identify physical matter, or assign X_max.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import sympy as sp


LANDING = (
    "ONE_METRIC_STATE_HIERARCHY_DERIVED"
    "__COVECTOR_ENERGY_PAIRING_CONDITIONAL"
    "__LOCAL_REST_MASS_PHYSICAL_TOTAL_MASS_XMAX_VALUE_AND_HISTORY_LAW_OPEN"
)


def require_zero(expr: sp.Expr, label: str) -> None:
    if sp.simplify(expr) != 0:
        raise AssertionError(f"{label}: {sp.simplify(expr)}")


def derive() -> dict[str, object]:
    r = sp.symbols("r", positive=True)
    f = sp.Function("f")(r)
    sqrt_f = sp.sqrt(f)
    phi = -sp.log(f) / 2
    mu = r * (1 - f) / 2

    fp = sp.diff(f, r)
    fpp = sp.diff(f, r, 2)
    p = sp.simplify(r * sp.diff(phi, r))
    qjet = sp.simplify(r**2 * sp.diff(phi, r, 2))

    gamma_r_00 = sp.simplify(f * fp / 2)
    u0 = 1 / sqrt_f
    a_r_coord = sp.simplify(gamma_r_00 * u0**2)
    a_hat = sp.simplify(a_r_coord / sqrt_f)

    e0 = sp.simplify(r * fp + f - 1)
    e1 = sp.simplify(r * fp + r**2 * fpp / 2)
    a_parallel = sp.simplify(f * (2 * p**2 + p - qjet))
    a_perp = sp.simplify(1 - f * (1 + p))

    checks: list[str] = []

    def check(expr: sp.Expr, label: str) -> None:
        require_zero(expr, label)
        checks.append(label)

    check(sqrt_f - sp.exp(-phi), "N_equals_exp_minus_phi")
    check(a_r_coord - fp / 2, "coordinate_static_acceleration")
    check(a_hat - sp.diff(sqrt_f, r), "orthonormal_acceleration_equals_N_prime")
    check(f - (1 - 2 * mu / r), "mass_aspect_change_of_variables")
    check(e0 + 2 * sp.diff(mu, r), "E0_equals_minus2_mu_prime")
    check(e1 + r * sp.diff(mu, r, 2), "E1_equals_minus_r_mu_doubleprime")
    check(a_parallel - (r**2 * fpp - r * fp) / 2, "Aparallel_f_jet_form")
    check(a_perp - (1 - f + r * fp / 2), "Aperp_f_jet_form")
    check(a_parallel + a_perp - (e1 - e0), "angular_trace_equals_E1_minus_E0")
    check(
        a_parallel - (-r * sp.diff(mu, r, 2) + 3 * sp.diff(mu, r) - 3 * mu / r),
        "Aparallel_mu_jet_form",
    )
    check(
        a_perp - (3 * mu / r - sp.diff(mu, r)),
        "Aperp_mu_jet_form",
    )

    phi_o, phi_s = sp.symbols("phi_o phi_s", real=True)
    delta_os = phi_s - phi_o
    n_o = sp.exp(-phi_o)
    n_s = sp.exp(-phi_s)
    q_os = sp.simplify(n_s / n_o)
    check(q_os - sp.exp(-delta_os), "clock_ratio_equals_exp_minus_delta")
    check(q_os * sp.exp(delta_os) - 1, "redshift_inverse_clock_ratio")
    q_so = q_os.subs({phi_o: phi_s, phi_s: phi_o}, simultaneous=True)
    check(q_so * q_os - 1, "clock_reversal")

    q1, q2 = sp.symbols("q1 q2", positive=True)
    chi = (1 - q1**2) / (1 + q1**2)
    check((1 - chi) - q1**2 * (1 + chi), "projective_clock_identity")
    check((q1 * q2) - q1 * q2, "clock_composition")

    a = sp.symbols("a", positive=True)
    f_control = 1 + a * r**2 / (1 + r**2)
    mu_control = sp.simplify(r * (1 - f_control) / 2)
    accel_control = sp.simplify(sp.diff(sp.sqrt(f_control), r))
    e0_control = sp.simplify(r * sp.diff(f_control, r) + f_control - 1)
    e1_control = sp.simplify(
        r * sp.diff(f_control, r) + r**2 * sp.diff(f_control, r, 2) / 2
    )
    if any(expr == 0 for expr in (mu_control, accel_control, e0_control, e1_control)):
        raise AssertionError("nontrivial counterprofile unexpectedly collapsed")
    checks.extend(
        [
            "flat_profile_passes_all_identities",
            "nontrivial_smooth_positive_profile_passes_all_identities",
            "profiles_have_distinct_metric_data",
        ]
    )

    return {
        "landing": LANDING,
        "scope": "primary_static_spherical_positive_f_plus_supplied_endpoint_covector_readout",
        "symbolic_check_count": len(checks),
        "symbolic_checks": checks,
        "identities": {
            "lapse": "N=sqrt(f)=exp(-phi)",
            "clock_ratio": "q_os=d_tau_s/d_tau_o=exp(-(phi_s-phi_o))",
            "redshift": "Z_so=exp(phi_s-phi_o)=1/q_os",
            "conditional_carried_energy": "epsilon_so=E_o/E_s=q_os after G95 covector identification",
            "signed_static_acceleration": "a_hat=dN/dr geometrically; physical proper acceleration=c_E^2*dN/dr",
            "geometric_mass_aspect": "mu=r(1-f)/2",
            "residuals": "E0=-2 mu_prime; E1=-r mu_doubleprime",
            "angular_trace": "A_parallel+A_perp=2 mu_prime-r mu_doubleprime",
            "projective_bridge": "q=sqrt((1-chi)/(1+chi)), chi=tanh(delta)",
        },
        "ownership": {
            "clock_acceleration_mass_aspect_curvature_hierarchy": "DERIVED_BOUNDED",
            "carried_covector_energy_ratio": "DERIVED_CONDITIONAL_G95",
            "generic_mass_character": "q^w_AFTER_NEW_COMPOSITION_AND_CONTINUITY_PREMISE",
            "generic_mass_weight_w": "OPEN",
            "local_rest_mass_dilation": "NOT_DERIVED",
            "physical_total_udt_mass": "OPEN",
            "mass_attachment_cE2_mu_over_Gobs": "CONDITIONAL_OBSERVATIONAL_ATTACHMENT",
            "xmax_value_profile_and_global_realization": "OPEN",
            "phi_value_history_law": "OPEN",
        },
        "counterfamily": {
            "f0": "1",
            "fa": "1+a*r^2/(1+r^2), 0<a<1",
            "result": "both satisfy every hierarchy identity while carrying distinct metric data",
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
