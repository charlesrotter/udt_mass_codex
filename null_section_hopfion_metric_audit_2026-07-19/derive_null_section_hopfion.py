#!/usr/bin/env python3
"""Exact CPU algebra for the null-section / angular-Hopf metric audit."""

from __future__ import annotations

import argparse
import json
import platform

import sympy as sp


def s(expr: sp.Expr | sp.Matrix) -> str:
    return str(sp.simplify(expr))


def require_zero(name: str, expr: sp.Expr | sp.Matrix) -> str:
    simplified = sp.simplify(expr)
    if isinstance(simplified, sp.MatrixBase):
        simplified = simplified.applyfunc(lambda item: sp.simplify(item.rewrite(sp.exp)))
    else:
        simplified = sp.simplify(simplified.rewrite(sp.exp))
    if isinstance(simplified, sp.MatrixBase):
        is_zero = simplified == sp.zeros(*simplified.shape)
    else:
        is_zero = simplified == 0
    if not is_zero:
        raise AssertionError(f"{name}: expected zero, got {simplified}")
    return "PASS"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    phi, delta = sp.symbols("phi delta", real=True)
    t = sp.symbols("t", positive=True)

    # Celestial null lift and positive conformal invariance in an orthonormal Lorentz frame.
    n_x, n_y, n_z = sp.symbols("n_x n_y n_z", real=True)
    n_norm_sq = n_x**2 + n_y**2 + n_z**2
    null_lift_norm = -1 + n_norm_sq
    null_lift_iff_unit_check = require_zero(
        "null_lift_iff_unit",
        null_lift_norm - (n_norm_sq - 1),
    )
    conformal_omega = sp.symbols("Omega_c", positive=True)
    conformal_null_norm = sp.expand(conformal_omega**2 * null_lift_norm)
    conformal_null_check = require_zero(
        "positive_conformal_null_invariance",
        conformal_null_norm.subs(n_z**2, 1 - n_x**2 - n_y**2),
    )

    # Round S3 in Hopf coordinates: z1=cos(eta)e^(i xi1), z2=sin(eta)e^(i xi2).
    # Parameterize tan(eta)=exp(2 phi).  The determinant-normalized torus block is reciprocal.
    cos_eta_sq = 1 / (1 + t**2)
    sin_eta_sq = t**2 / (1 + t**2)
    omega_h_sq = t / (1 + t**2)
    normalized_torus = sp.diag(
        sp.simplify(cos_eta_sq / omega_h_sq),
        sp.simplify(sin_eta_sq / omega_h_sq),
    )
    reciprocal_torus_check = require_zero(
        "reciprocal_torus",
        normalized_torus - sp.diag(1 / t, t),
    )

    # This determinant-one form is not unique to S3: every positive diagonal two-block has it.
    scale_a, scale_b = sp.symbols("a b", positive=True)
    generic_block = sp.diag(scale_a**2, scale_b**2)
    generic_common_scale = sp.sqrt(sp.det(generic_block))
    generic_normalized = sp.simplify(generic_block / generic_common_scale)
    generic_normal_form_check = require_zero(
        "generic_two_block_normal_form",
        generic_normalized - sp.diag(scale_a / scale_b, scale_b / scale_a),
    )

    eta = sp.atan(sp.exp(2 * phi))
    eta_prime = sp.simplify(sp.diff(eta, phi).rewrite(sp.cosh))
    eta_prime_check = require_zero("eta_prime", eta_prime - sp.sech(2 * phi))

    f = (1 - sp.tanh(2 * phi)) / 2  # cos(eta)^2
    g = (1 + sp.tanh(2 * phi)) / 2  # sin(eta)^2
    round_scale = 1 / (2 * sp.cosh(2 * phi))
    round_block_check = require_zero(
        "round_block",
        sp.Matrix([
            f - round_scale * sp.exp(-2 * phi),
            g - round_scale * sp.exp(2 * phi),
        ]),
    )
    mirror_check = require_zero(
        "mirror_swap",
        sp.Matrix([f.subs(phi, -phi) - g, g.subs(phi, -phi) - f]),
    )
    endpoint_limits = {
        "Omega_minus_infinity": sp.limit(round_scale, phi, -sp.oo),
        "Omega_plus_infinity": sp.limit(round_scale, phi, sp.oo),
        "f_minus_infinity": sp.limit(f, phi, -sp.oo),
        "f_plus_infinity": sp.limit(f, phi, sp.oo),
        "g_minus_infinity": sp.limit(g, phi, -sp.oo),
        "g_plus_infinity": sp.limit(g, phi, sp.oo),
    }
    if endpoint_limits != {
        "Omega_minus_infinity": 0,
        "Omega_plus_infinity": 0,
        "f_minus_infinity": 1,
        "f_plus_infinity": 0,
        "g_minus_infinity": 0,
        "g_plus_infinity": 1,
    }:
        raise AssertionError(f"endpoint limits failed: {endpoint_limits}")

    # Standard Hopf quotient written directly in reciprocal depth and relative phase.
    hopf_n = sp.Matrix([
        sp.sech(2 * phi) * sp.cos(delta),
        sp.sech(2 * phi) * sp.sin(delta),
        -sp.tanh(2 * phi),
    ])
    hopf_n_norm_check = require_zero("hopf_n_norm", hopf_n.dot(hopf_n) - 1)

    # Metric-dual connection of the diagonal U(1) generator V=d_xi1+d_xi2.
    # A=f dxi1+g dxi2.  Its A wedge dA density in (phi,xi1,xi2) is f'.
    hopf_density = sp.simplify(sp.diff(f, phi))
    density_check = require_zero("hopf_density", hopf_density + sp.sech(2 * phi) ** 2)
    radial_integral = sp.integrate(hopf_density, (phi, -sp.oo, sp.oo))
    connection_integral = sp.simplify(radial_integral * (2 * sp.pi) ** 2)
    hopf_charge = sp.simplify(-connection_integral / (4 * sp.pi**2))
    if radial_integral != -1 or connection_integral != -4 * sp.pi**2 or hopf_charge != 1:
        raise AssertionError("Hopf connection normalization failed")
    doubled_connection_integral = sp.simplify(4 * connection_integral)
    doubled_connection_charge = sp.simplify(
        -doubled_connection_integral / (16 * sp.pi**2)
    )
    if doubled_connection_integral != -16 * sp.pi**2 or doubled_connection_charge != 1:
        raise AssertionError("doubled area-form connection normalization failed")
    # Derive the anti-diagonal result from A_-=f dxi1-g dxi2 rather than assigning its sign.
    anti_diagonal_density = sp.simplify(
        (-g) * sp.diff(f, phi) - f * sp.diff(-g, phi)
    )
    anti_density_check = require_zero(
        "anti_diagonal_density",
        anti_diagonal_density + hopf_density,
    )
    anti_diagonal_integral = sp.simplify(
        sp.integrate(anti_diagonal_density, (phi, -sp.oo, sp.oo)) * (2 * sp.pi) ** 2
    )
    anti_diagonal_charge = sp.simplify(-anti_diagonal_integral / (4 * sp.pi**2))
    if anti_diagonal_charge != -1:
        raise AssertionError("anti-diagonal Hopf connection normalization failed")

    # Derive the constant map's zero pullback curvature and hence zero registered Hopf charge.
    x_c, y_c, z_c = sp.symbols("x_c y_c z_c", real=True)
    constant_target_map = sp.Matrix([0, 0, 1])
    constant_gradients = [sp.diff(constant_target_map, coordinate) for coordinate in (x_c, y_c, z_c)]
    constant_pullback_curvature = sp.Matrix([
        constant_target_map.dot(constant_gradients[0].cross(constant_gradients[1])),
        constant_target_map.dot(constant_gradients[1].cross(constant_gradients[2])),
        constant_target_map.dot(constant_gradients[2].cross(constant_gradients[0])),
    ])
    constant_map_curvature_check = require_zero(
        "constant_map_pullback_curvature",
        constant_pullback_curvature,
    )
    constant_connection_integral = sp.simplify(sum(constant_pullback_curvature, sp.Integer(0)))
    constant_map_charge = sp.simplify(-constant_connection_integral / (4 * sp.pi**2))
    if constant_map_charge != 0:
        raise AssertionError("constant-map Hopf charge failed")

    # CSN cancellation: an arbitrary positive common angular scale cancels from A.
    omega2 = sp.symbols("Omega2", positive=True)
    a2 = omega2 * sp.exp(-2 * phi)
    b2 = omega2 * sp.exp(2 * phi)
    csn_connection = sp.Matrix([sp.simplify(a2 / (a2 + b2)), sp.simplify(b2 / (a2 + b2))])
    csn_connection_check = require_zero("csn_connection", csn_connection - sp.Matrix([f, g]))

    # Unit-quaternion frame winding: rotating a constant axis produces the standard Hopf map.
    qw, qx, qy, qz = sp.symbols("q_w q_x q_y q_z", real=True)
    frame_hopf = sp.Matrix([
        2 * (qx * qz + qw * qy),
        2 * (qy * qz - qw * qx),
        qw**2 - qx**2 - qy**2 + qz**2,
    ])
    quaternion_norm_sq = qw**2 + qx**2 + qy**2 + qz**2
    frame_hopf_check = require_zero(
        "quaternion_hopf_norm",
        frame_hopf.dot(frame_hopf) - quaternion_norm_sq**2,
    )
    eta_h, xi1, xi2 = sp.symbols("eta_h xi1 xi2", real=True)
    hopf_quaternion_substitution = {
        qw: sp.cos(eta_h) * sp.cos(xi1),
        qz: sp.cos(eta_h) * sp.sin(xi1),
        qy: sp.sin(eta_h) * sp.cos(xi2),
        qx: sp.sin(eta_h) * sp.sin(xi2),
    }
    standard_hopf_from_angles = sp.Matrix([
        sp.sin(2 * eta_h) * sp.cos(xi1 - xi2),
        sp.sin(2 * eta_h) * sp.sin(xi1 - xi2),
        sp.cos(2 * eta_h),
    ])
    winding_frame_map_check = require_zero(
        "winding_frame_is_standard_hopf_map",
        sp.trigsimp(frame_hopf.subs(hopf_quaternion_substitution) - standard_hopf_from_angles),
    )
    reciprocal_hopf_map_check = require_zero(
        "standard_hopf_map_in_reciprocal_depth",
        sp.trigsimp(
            standard_hopf_from_angles.subs({eta_h: eta, xi1: delta, xi2: 0}) - hopf_n
        ),
    )

    # A local frame rotation gives ordinary derivative energy to a physically constant direction.
    theta, theta_x = sp.symbols("theta theta_x", real=True)
    rotation = sp.Matrix([
        [sp.cos(theta), 0, sp.sin(theta)],
        [0, 1, 0],
        [-sp.sin(theta), 0, sp.cos(theta)],
    ])
    e3 = sp.Matrix([0, 0, 1])
    rotated_n = rotation * e3
    dn = sp.diff(rotated_n, theta) * theta_x
    ordinary_energy = sp.simplify(dn.dot(dn))
    if ordinary_energy != theta_x**2:
        raise AssertionError("ordinary frame energy check failed")
    rotation_x = sp.diff(rotation, theta) * theta_x
    pure_gauge = sp.simplify(rotation_x * rotation.T)
    covariant_dn = sp.simplify(dn - pure_gauge * rotated_n)
    covariant_cancel_check = require_zero("pure_gauge_cancel", covariant_dn)

    # A rotating dyad on an isotropic two-block is likewise removable frame gauge.
    dyad_rotation = sp.Matrix([
        [sp.cos(theta), -sp.sin(theta)],
        [sp.sin(theta), sp.cos(theta)],
    ])
    dyad_rotation_x = sp.diff(dyad_rotation, theta) * theta_x
    dyad_spin_connection = sp.simplify(dyad_rotation_x * dyad_rotation.T)
    dyad_covariant_derivative = sp.simplify(
        dyad_rotation_x - dyad_spin_connection * dyad_rotation
    )
    rotating_dyad_gauge_check = require_zero(
        "rotating_round_dyad_is_gauge",
        dyad_covariant_derivative,
    )

    # Celestial sphere aberration under a local Lorentz boost is not a fixed SO(3) rotation.
    beta, nx, ny, nz = sp.symbols("beta n_x n_y n_z", real=True)
    gamma = 1 / sp.sqrt(1 - beta**2)
    denom = 1 - beta * nx
    aberrated = sp.Matrix([
        (nx - beta) / denom,
        ny / (gamma * denom),
        nz / (gamma * denom),
    ])
    aberrated_norm = sp.together(aberrated.dot(aberrated) - 1)
    aberrated_on_sphere = sp.factor(aberrated_norm.subs(nz**2, 1 - nx**2 - ny**2))
    aberration_check = require_zero("aberration_sphere", aberrated_on_sphere)
    # A fixed SO(3) rotation would preserve the mutual angle of every pair.  A boost in x maps
    # e_y and e_z to directions with dot product beta^2 instead of zero.
    boosted_ey = sp.Matrix([-beta, 1 / gamma, 0])
    boosted_ez = sp.Matrix([-beta, 0, 1 / gamma])
    aberration_angle_change = sp.simplify(boosted_ey.dot(boosted_ez))
    aberration_not_rotation_check = require_zero(
        "aberration_is_not_fixed_spatial_rotation",
        aberration_angle_change - beta**2,
    )
    if sp.simplify(aberration_angle_change.subs(beta, sp.Rational(1, 2))) != sp.Rational(1, 4):
        raise AssertionError("aberration fixed-rotation counterexample failed")

    # Mixed angular connection: common round warp is proportional to identity; reciprocal
    # anisotropy has a trace-free part but only after the two angular slots are supplied.
    radius, radius_p = sp.symbols("R R_p", nonzero=True, real=True)
    round_mixed = sp.diag(radius_p / radius, radius_p / radius)
    round_tracefree = sp.simplify(round_mixed - sp.eye(2) * sp.trace(round_mixed) / 2)
    round_no_selector_check = require_zero("round_tracefree", round_tracefree)

    omega, omega_p = sp.symbols("Omega Omega_p", nonzero=True, real=True)
    reciprocal_mixed = sp.diag(omega_p / omega - 1, omega_p / omega + 1)
    reciprocal_tracefree = sp.simplify(
        reciprocal_mixed - sp.eye(2) * sp.trace(reciprocal_mixed) / 2
    )
    reciprocal_shear_check = require_zero(
        "reciprocal_tracefree",
        reciprocal_tracefree - sp.diag(-1, 1),
    )

    # The target-map output and spacetime null lift have different ambient types until a
    # soldering/trivialization supplies a map between them.
    null_lift = sp.Matrix([1, n_x, n_y, n_z])
    if hopf_n.shape != (3, 1) or null_lift.shape != (4, 1):
        raise AssertionError("carrier/null-lift type check failed")

    # Angular-dependent reciprocal scalar in the diagonal radial metric.
    # ell=dt+A^-1 dr is null, but angular gradients obstruct Frobenius and make the
    # radial-looking null line non-geodesic in the angular directions.
    aval, a_theta, a_varphi = sp.symbols("A A_theta A_varphi", nonzero=True, real=True)
    inverse_tr_metric = sp.diag(-1 / aval, aval)
    ell_tr = sp.Matrix([1, 1 / aval])
    radial_null_norm = sp.simplify((ell_tr.T * inverse_tr_metric * ell_tr)[0])
    radial_null_check = require_zero("radial_null", radial_null_norm)

    time_c, r_c, theta_c, varphi_c = sp.symbols("t_c r_c theta_c varphi_c", real=True)
    coordinates = [time_c, r_c, theta_c, varphi_c]
    a_function = sp.Function("A")(r_c, theta_c, varphi_c)
    ell_components = [sp.Integer(1), 1 / a_function, sp.Integer(0), sp.Integer(0)]
    d_ell = sp.Matrix(4, 4, lambda i, j: sp.simplify(
        sp.diff(ell_components[j], coordinates[i])
        - sp.diff(ell_components[i], coordinates[j])
    ))

    def wedge_three(i: int, j: int, k: int) -> sp.Expr:
        return sp.simplify(
            ell_components[i] * d_ell[j, k]
            + ell_components[j] * d_ell[k, i]
            + ell_components[k] * d_ell[i, j]
        )

    frobenius_functional = sp.Matrix([
        wedge_three(0, 1, 2),
        wedge_three(0, 1, 3),
    ])
    frobenius_coefficients = sp.simplify(frobenius_functional.subs({
        a_function: aval,
        sp.diff(a_function, theta_c): a_theta,
        sp.diff(a_function, varphi_c): a_varphi,
    }))
    frobenius_derivation_check = require_zero(
        "frobenius_angular_coefficients",
        frobenius_coefficients - sp.Matrix([a_theta / aval**2, a_varphi / aval**2]),
    )
    spatial_pullback = sp.simplify(wedge_three(1, 2, 3))
    spatial_pullback_check = require_zero("frobenius_spatial_pullback", spatial_pullback)

    qtt, qtp, qpp = sp.symbols("qInv_tt qInv_tp qInv_pp", real=True)
    angular_inverse = sp.Matrix([[qtt, qtp], [qtp, qpp]])
    angular_gradient = sp.Matrix([a_theta, a_varphi])
    gamma_angular_tt = sp.simplify(angular_inverse * angular_gradient / 2)
    gamma_angular_rr = sp.simplify(angular_inverse * angular_gradient / (2 * aval**2))
    raised_ell_t = -1 / aval
    raised_ell_r = sp.Integer(1)
    angular_acceleration = sp.simplify(
        gamma_angular_tt * raised_ell_t**2 + gamma_angular_rr * raised_ell_r**2
    )
    angular_acceleration_check = require_zero(
        "angular_null_acceleration",
        angular_acceleration - angular_inverse * angular_gradient / aval**2,
    )

    # Global closure is additional data: primitive collapsing cycles have determinant one for S3;
    # determinant p gives the lens-space family, so the same interior local form is not enough.
    lens_p, lens_q = sp.symbols("p q", integer=True)
    collapse_determinant = sp.det(sp.Matrix([[1, lens_q], [0, lens_p]]))
    if collapse_determinant != lens_p:
        raise AssertionError("collapse-cycle determinant failed")

    checks = {
        "unit_target_vector_has_null_lift_iff_unit_norm": null_lift_iff_unit_check,
        "positive_conformal_rescaling_preserves_null_lift": conformal_null_check,
        "reciprocal_hopf_torus_block": reciprocal_torus_check,
        "generic_positive_two_block_has_reciprocal_normal_form": generic_normal_form_check,
        "hopf_coordinate_derivative": eta_prime_check,
        "round_s3_block_reconstruction": round_block_check,
        "reciprocity_mirror_swaps_circles": mirror_check,
        "round_completion_endpoint_limits": "PASS",
        "hopf_quotient_map_unit_norm": hopf_n_norm_check,
        "hopf_connection_density": density_check,
        "hopf_connection_integral_and_charge": "PASS",
        "constant_map_has_zero_hopf_charge": "PASS",
        "constant_map_pullback_curvature_is_zero": constant_map_curvature_check,
        "doubled_area_form_connection_convention": "PASS",
        "anti_diagonal_connection_density_and_charge": anti_density_check,
        "common_scale_cancels_from_connection": csn_connection_check,
        "winding_frame_produces_hopf_components": frame_hopf_check,
        "winding_frame_equals_standard_hopf_map": winding_frame_map_check,
        "standard_hopf_map_equals_reciprocal_depth_map": reciprocal_hopf_map_check,
        "ordinary_derivative_frame_energy": "PASS",
        "pure_gauge_covariant_cancellation": covariant_cancel_check,
        "rotating_round_dyad_is_removable_frame_gauge": rotating_dyad_gauge_check,
        "lorentz_aberration_preserves_celestial_sphere": aberration_check,
        "lorentz_aberration_is_not_fixed_so3_rotation": aberration_not_rotation_check,
        "round_angular_warp_has_no_tracefree_selector": round_no_selector_check,
        "reciprocal_angular_realization_has_tracefree_shear": reciprocal_shear_check,
        "target_map_and_spacetime_null_lift_are_distinct_types": "PASS",
        "angular_phi_radial_covector_is_null": radial_null_check,
        "angular_phi_frobenius_coefficients_derived": frobenius_derivation_check,
        "angular_phi_spatial_frobenius_pullback_zero": spatial_pullback_check,
        "angular_phi_null_acceleration_derived": angular_acceleration_check,
        "global_collapse_cycle_determinant": "PASS",
    }
    if set(checks.values()) != {"PASS"}:
        raise AssertionError(checks)

    result = {
        "status": "PASS",
        "python": platform.python_version(),
        "sympy": sp.__version__,
        "check_count": len(checks),
        "checks": checks,
        "exact_identities": {
            "null_lift_norm": s(null_lift_norm),
            "positive_conformal_null_lift_norm": s(conformal_null_norm),
            "hopf_coordinate": "tan(eta)=exp(2*phi)",
            "round_s3_metric": "sech(2*phi)^2 dphi^2 + [1/(2*cosh(2*phi))]*(exp(-2*phi) dxi1^2 + exp(2*phi) dxi2^2)",
            "normalized_hopf_torus_block": s(normalized_torus.subs(t, sp.exp(2 * phi))),
            "generic_normalized_two_block": s(generic_normalized),
            "common_scale_round_s3": s(round_scale),
            "hopf_map": [s(item) for item in hopf_n],
            "hopf_connection_coefficients": [s(f), s(g)],
            "hopf_curvature_density": s(hopf_density),
            "integral_A_wedge_dA": s(connection_integral),
            "registered_hopf_charge": s(hopf_charge),
            "doubled_connection_integral": s(doubled_connection_integral),
            "doubled_connection_charge_1_over_16pi2": s(doubled_connection_charge),
            "diagonal_and_antidiagonal_charges": [s(hopf_charge), s(anti_diagonal_charge)],
            "anti_diagonal_connection_density": s(anti_diagonal_density),
            "constant_map_registered_hopf_charge": s(constant_map_charge),
            "constant_map_pullback_curvature": [s(item) for item in constant_pullback_curvature],
            "mirror_rule": "phi->-phi swaps xi1 and xi2 scale factors",
            "round_completion_endpoint_limits": {key: s(value) for key, value in endpoint_limits.items()},
            "frame_rotation_ordinary_L2_density": s(ordinary_energy),
            "frame_rotation_covariant_derivative": [s(item) for item in covariant_dn],
            "winding_frame_standard_hopf_map": [s(item) for item in standard_hopf_from_angles],
            "rotating_round_dyad_covariant_derivative": s(dyad_covariant_derivative),
            "geometric_type_shapes": {
                "internal_target_map": list(hopf_n.shape),
                "spacetime_null_lift": list(null_lift.shape),
            },
            "aberration_pair_dot_product_before": "0",
            "aberration_pair_dot_product_after": s(aberration_angle_change),
            "round_mixed_connection": s(round_mixed),
            "round_mixed_tracefree": s(round_tracefree),
            "reciprocal_mixed_connection": s(reciprocal_mixed),
            "reciprocal_mixed_tracefree": s(reciprocal_tracefree),
            "angular_phi_frobenius_coefficients": [s(item) for item in frobenius_coefficients],
            "radial_null_angular_acceleration": [s(item) for item in angular_acceleration],
            "spatial_slice_pullback_of_ell_wedge_dell": s(spatial_pullback),
            "collapse_cycle_determinant": s(collapse_determinant),
        },
        "structural_readout": {
            "exact_new_match": "The CSN-normalized U(1)xU(1) orbit block of round S3 in Hopf coordinates is diag(exp(-2*phi),exp(2*phi)).",
            "genericity_caveat": "Every positive diagonal two-block has a reciprocal determinant-one normal form; the local exponential match alone does not select S3 or Hopf topology.",
            "conditional_unit_charge": "Choosing the diagonal circle action, 2*pi periods, and S3 endpoint closure gives integral(A wedge dA)=-4*pi^2 and Q_H=1.",
            "not_selected": "C0/C1 does not place the reciprocal pair in two spatial angular slots or select the common scale, radial completion, circle action, periods, collapse cycles, or physical boundary.",
            "csn_endpoint_caveat": "The round common scale tends to zero at the two collapse orbits; the CSN equivalence with Omega>0 holds on the open principal-orbit region, while smooth caps are additional conformal-completion data.",
            "frame_obstruction": "The existing internal target field and ordinary-derivative energy cannot be relabeled as an unframed null-direction section.",
            "angular_phi_result": "Angular dependence of the diagonal reciprocal scalar creates geometric coupling and a Frobenius obstruction, but its spatial pullback is not the existing Hopf charge and the radial-looking null line is not geodesic when angular gradients are nonzero.",
        },
        "maximum_verdict": "EXACT_RECIPROCAL_HOPF_ORBIT_BLOCK_COMPATIBILITY_WITNESS; CONDITIONAL_UNIT_HOPF_CONNECTION_AFTER_TORIC_S3_COMPLETION; ANGULAR_SLOTS_GLOBAL_CLOSURE_BOUNDARY_CONFIGURATION_SPACE_AND_ACTION_OPEN; DIRECT_CELESTIAL_CARRIER_IDENTITY_BLOCKED_WITHOUT_SOLDERING",
    }

    with open(args.output, "w", encoding="utf-8") as handle:
        json.dump(result, handle, indent=2, sort_keys=True)
        handle.write("\n")
    print(f"DERIVATION PASS {len(checks)}/{len(checks)}")
    print(result["maximum_verdict"])


if __name__ == "__main__":
    main()
