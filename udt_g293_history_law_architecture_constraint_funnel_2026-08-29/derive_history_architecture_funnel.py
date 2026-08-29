#!/usr/bin/env python3
"""Exact symbolic checks for the preregistered G293 architecture funnel."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import sympy as sp


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=Path("DERIVATION_RESULT.json"))
    args = parser.parse_args()

    checks: list[dict[str, object]] = []

    def check(name: str, expression: sp.Expr | sp.MatrixBase, expected: object = 0) -> None:
        if isinstance(expression, sp.MatrixBase):
            simplified = expression.applyfunc(sp.simplify)
            passed = simplified == sp.zeros(*simplified.shape)
            rendered = str(simplified)
        else:
            simplified = sp.simplify(expression)
            passed = simplified == expected
            rendered = str(simplified)
        if not passed:
            raise AssertionError(f"{name}: got {rendered}, expected {expected}")
        checks.append({"name": name, "value": rendered, "expected": str(expected), "pass": True})

    s, t, k = sp.symbols("s t k", real=True)
    alpha = sp.symbols("alpha", positive=True)

    gamma = lambda z: k * z
    check("additive_depth_homomorphism", gamma(s + t) - gamma(s) - gamma(t))

    D = lambda z: sp.diag(sp.exp(-gamma(z)), sp.exp(gamma(z)))
    check("reciprocal_character_composition", D(s + t) - D(s) * D(t))
    check("reciprocal_character_determinant", D(s).det() - 1)

    chi = lambda z: sp.tanh(gamma(z))
    mobius = (chi(s) + chi(t)) / (1 + chi(s) * chi(t))
    check("projective_mobius_composition", sp.trigsimp(mobius - chi(s + t)))
    check("projective_reversal", chi(-s) + chi(s))
    check("projective_generator_jacobian", sp.diff(chi(s), s) - k * (1 - chi(s) ** 2))
    check("trivial_scalar_branch", chi(s).subs(k, 0))

    # Endpoint composition and reversal do not themselves supply translation homogeneity.
    endpoint_a, endpoint_b, endpoint_c = sp.symbols("endpoint_a endpoint_b endpoint_c", real=True)
    V = lambda z: z + z**3
    endpoint_delta = lambda left, right: V(right) - V(left)
    check(
        "endpoint_cocycle_composition_without_homogeneity",
        endpoint_delta(endpoint_a, endpoint_c)
        - endpoint_delta(endpoint_a, endpoint_b)
        - endpoint_delta(endpoint_b, endpoint_c),
    )
    check("endpoint_cocycle_reversal", endpoint_delta(endpoint_a, endpoint_b) + endpoint_delta(endpoint_b, endpoint_a))
    homogeneity_defect = sp.expand(
        endpoint_delta(endpoint_a, endpoint_b) - endpoint_delta(0, endpoint_b - endpoint_a)
    )
    if homogeneity_defect == 0:
        raise AssertionError("nonhomogeneous endpoint potential unexpectedly became homogeneous")
    checks.append(
        {
            "name": "endpoint_composition_does_not_imply_homogeneity",
            "value": str(homogeneity_defect),
            "expected": "nonzero polynomial",
            "pass": True,
        }
    )

    delta0, depth_shift = sp.symbols("delta0 depth_shift", real=True)
    flow = lambda initial, z: initial + k * z
    check(
        "constant_generator_commutes_with_depth_translation",
        flow(delta0 + depth_shift, s) - flow(delta0, s) - depth_shift,
    )
    check("constant_generator_semigroup", flow(flow(delta0, s), t) - flow(delta0, s + t))

    # Flow composition alone also does not imply translation equivariance.
    nonlinear_flow = lambda initial, z: sp.exp(z) * initial
    check(
        "nonconstant_autonomous_flow_composes",
        nonlinear_flow(nonlinear_flow(delta0, s), t) - nonlinear_flow(delta0, s + t),
    )
    nonlinear_translation_defect = sp.expand(
        nonlinear_flow(delta0 + depth_shift, s) - nonlinear_flow(delta0, s) - depth_shift
    )
    if sp.simplify(nonlinear_translation_defect) == 0:
        raise AssertionError("nonconstant composing flow unexpectedly translation equivariant")
    checks.append(
        {
            "name": "flow_composition_does_not_imply_translation_equivariance",
            "value": str(nonlinear_translation_defect),
            "expected": "nonzero for generic s and shift",
            "pass": True,
        }
    )

    # On an augmented state, depth-translation equivariance still permits dependence on other state.
    y0 = sp.symbols("y0", real=True)
    augmented_y = lambda initial_y, z: initial_y + z
    augmented_delta = lambda initial_delta, initial_y, z: initial_delta + initial_y * z + z**2 / 2
    check(
        "augmented_state_depth_translation_equivariance",
        augmented_delta(delta0 + depth_shift, y0, s)
        - augmented_delta(delta0, y0, s)
        - depth_shift,
    )
    check(
        "augmented_state_semigroup_y",
        augmented_y(augmented_y(y0, s), t) - augmented_y(y0, s + t),
    )
    check(
        "augmented_state_semigroup_delta",
        augmented_delta(augmented_delta(delta0, y0, s), augmented_y(y0, s), t)
        - augmented_delta(delta0, y0, s + t),
    )

    # A nonconstant autonomous vector field is not equivariant under all depth translations.
    X = lambda depth: 1 + depth**2
    nonconstant_defect = sp.expand(X(delta0 + depth_shift) - X(delta0))
    expected_defect = 2 * delta0 * depth_shift + depth_shift**2
    check("nonconstant_generator_translation_defect", nonconstant_defect - expected_defect)
    if sp.simplify(nonconstant_defect) == 0:
        raise AssertionError("nonconstant generator unexpectedly translation equivariant")
    checks.append(
        {
            "name": "nonconstant_generator_rejected",
            "value": str(nonconstant_defect),
            "expected": "nonzero polynomial",
            "pass": True,
        }
    )

    sprime = alpha * s
    kprime = k / alpha
    check("parameter_rescaling_degeneracy", kprime * sprime - k * s)

    # Fixed Euler period with an arbitrary zero-mean quadrupole amplitude.
    x, amplitude = sp.symbols("x amplitude", real=True)
    P2 = (3 * x**2 - 1) / 2
    check("P2_zero_mean", sp.integrate(P2, (x, -1, 1)))
    q = 1 + amplitude * P2
    check("fixed_total_euler_flux", 2 * sp.pi * sp.integrate(q, (x, -1, 1)) - 4 * sp.pi)
    check("north_flux_value", q.subs(x, 1) - (1 + amplitude))
    check("equator_flux_value", q.subs(x, 0) - (1 - amplitude / 2))
    local_separator = sp.simplify(q.subs(x, 1) - q.subs(x, 0))
    check("local_flux_separator_formula", local_separator - 3 * amplitude / 2)
    if sp.simplify(local_separator.subs(amplitude, 1)) == 0:
        raise AssertionError("local Euler-sector separator vanished")
    checks.append(
        {
            "name": "same_total_different_local_flux",
            "value": str(local_separator),
            "expected": "nonzero when amplitude != 0",
            "pass": True,
        }
    )
    c = sp.symbols("c", real=True)
    cap_integral = 2 * sp.pi * sp.integrate(amplitude * P2, (x, c, 1))
    check("cap_flux_difference", cap_integral - sp.pi * amplitude * (c - c**3))

    # Lawful time-live connection family: the mixed curvature term is mandatory.
    theta = sp.symbols("theta", real=True)
    live_amplitude = sp.Function("live_amplitude")(s)
    P2_theta = (3 * sp.cos(theta) ** 2 - 1) / 2
    b_phi = sp.cos(theta) * sp.sin(theta) ** 2 / 2
    check("global_difference_form_derivative", sp.diff(b_phi, theta) - P2_theta * sp.sin(theta))
    F_theta_phi = sp.sin(theta) * (1 + live_amplitude * P2_theta)
    F_s_phi = sp.diff(live_amplitude, s) * b_phi
    check(
        "time_live_curvature_Bianchi_closure",
        sp.diff(F_theta_phi, s) - sp.diff(F_s_phi, theta),
    )
    missing_mixed_defect = sp.simplify(sp.diff(F_theta_phi, s))
    if missing_mixed_defect == 0:
        raise AssertionError("slice-only time-live curvature unexpectedly closed")
    checks.append(
        {
            "name": "slice_only_time_live_curvature_rejected",
            "value": str(missing_mixed_defect),
            "expected": "nonzero when amplitude varies",
            "pass": True,
        }
    )

    # Inherited G257/G259 primary formulas, recomputed as regression checks only.
    r, C = sp.symbols("r C", positive=True, nonzero=True)
    f = sp.Function("f")(r)
    E0 = r * sp.diff(f, r) + f - 1
    E1 = r * sp.diff(f, r) + r**2 * sp.diff(f, r, 2) / 2
    check("primary_residual_dependence", r * sp.diff(E0, r) - 2 * E1)

    f_gr = 1 + C / r
    check("GR_branch_E0", E0.subs(f, f_gr).doit())
    check("GR_branch_E1", E1.subs(f, f_gr).doit())

    phi = -sp.log(f) / 2
    p = r * sp.diff(phi, r)
    zeta = r**2 * sp.diff(phi, r, 2)
    apar = f * (2 * p**2 + p - zeta)
    aperp = 1 - f * (1 + p)
    check("angular_trace_residual_identity", apar + aperp - (E1 - E0))
    apar_gr = sp.simplify(apar.subs(f, f_gr).doit())
    aperp_gr = sp.simplify(aperp.subs(f, f_gr).doit())
    check("GR_active_angular_cancellation", apar_gr + aperp_gr)
    if apar_gr == 0 or aperp_gr == 0:
        raise AssertionError("GR angular modes were incorrectly discarded")
    checks.extend(
        [
            {"name": "GR_A_parallel_nonzero", "value": str(apar_gr), "expected": "nonzero", "pass": True},
            {"name": "GR_A_perp_nonzero", "value": str(aperp_gr), "expected": "nonzero", "pass": True},
        ]
    )

    # Geometric mass-aspect rewrite inherited from G259.
    mu = sp.Function("mu")(r)
    f_mu = 1 - 2 * mu / r
    check("mass_aspect_E0", E0.subs(f, f_mu).doit() + 2 * sp.diff(mu, r))
    check("mass_aspect_E1", E1.subs(f, f_mu).doit() + r * sp.diff(mu, r, 2))

    # R[g]=0 is a local metric two-jet scalar residual outside the G259 rank-two class.
    Q = sp.symbols("Q", nonzero=True, real=True)
    f_scalar = 1 + C / r + Q / r**2
    E0_scalar = sp.simplify(E0.subs(f, f_scalar).doit())
    E1_scalar = sp.simplify(E1.subs(f, f_scalar).doit())
    scalar_curvature = sp.simplify(-2 * (E0_scalar + E1_scalar) / r**2)
    check("scalar_residual_R_zero_family", scalar_curvature)
    check("scalar_residual_non_Einstein_separator", E0_scalar + Q / r**2)
    if E0_scalar == 0 or E1_scalar == 0:
        raise AssertionError("R=0 comparison family unexpectedly collapsed to Einstein vacuum")
    checks.append(
        {
            "name": "G259_class_not_all_local_metric_two_jet_laws",
            "value": f"E0={E0_scalar}, E1={E1_scalar}",
            "expected": "both nonzero while R=0",
            "pass": True,
        }
    )

    result = {
        "landing_candidate": (
            "SCALAR_RECIPROCAL_GENERATOR_IS_PARAMETERIZATION_ONLY__"
            "EULER_SECTOR_LEAVES_CONTINUOUS_FLUX_FREE__"
            "PRIMITIVE_STATE_AND_DATA_DEPENDENCE_PARTITION_REMAINS__"
            "UDT_HISTORY_LAW_ARCHITECTURE_NARROWED_NOT_SELECTED"
        ),
        "assertion_count": len(checks),
        "all_pass": all(bool(item["pass"]) for item in checks),
        "checks": checks,
        "scope": {
            "observations": 0,
            "fit_coefficients": 0,
            "physical_scales_selected": 0,
            "field_equations_adopted": 0,
            "protected_inputs": 0,
            "gpu": False,
        },
    }
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"all_pass": result["all_pass"], "assertions": len(checks)}))


if __name__ == "__main__":
    main()
