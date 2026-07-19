#!/usr/bin/env python3
"""Exact CPU algebra for the preregistered Xmax-reciprocity audit."""

from __future__ import annotations

import json
import platform
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent
OUT = HERE / "DERIVATION_RESULT.json"


def require_zero(name: str, value, checks: dict[str, str]) -> None:
    if isinstance(value, sp.MatrixBase):
        reduced = value.applyfunc(lambda entry: sp.simplify(sp.trigsimp(entry.rewrite(sp.exp))))
        if any(sp.simplify(entry) != 0 for entry in reduced):
            raise AssertionError(f"{name}: {reduced}")
    else:
        reduced = sp.simplify(sp.trigsimp(value.rewrite(sp.exp)))
        if reduced != 0:
            raise AssertionError(f"{name}: {reduced}")
    checks[name] = "PASS"


def bounded_composition_tile(checks: dict[str, str]) -> dict:
    xi, eta, zeta = sp.symbols("xi eta zeta", real=True)

    def compose(left, right):
        return sp.cancel((left + right) / (1 + left * right))

    require_zero("XR1_identity_right", compose(xi, 0) - xi, checks)
    require_zero("XR1_identity_left", compose(0, xi) - xi, checks)
    require_zero("XR1_inverse", compose(xi, -xi), checks)
    require_zero("XR1_associative_1D", compose(compose(xi, eta), zeta) - compose(xi, compose(eta, zeta)), checks)
    require_zero("XR1_commutative_1D", compose(xi, eta) - compose(eta, xi), checks)
    require_zero("XR1_endpoint_plus_absorbing_limit_formula", compose(1, eta) - 1, checks)
    require_zero("XR1_endpoint_minus_absorbing_limit_formula", compose(-1, eta) + 1, checks)

    p, q = sp.symbols("p q", real=True)
    require_zero(
        "XR1_additive_rapidity",
        sp.tanh(p + q) - compose(sp.tanh(p), sp.tanh(q)),
        checks,
    )

    A = lambda value: sp.cancel((1 - value) / (1 + value))
    require_zero("XR1_A_reversal_inverse", A(-xi) * A(xi) - 1, checks)
    require_zero("XR1_A_composition_multiplicative", A(compose(xi, eta)) - A(xi) * A(eta), checks)
    require_zero("XR1_A_exponential", A(sp.tanh(p)) - sp.exp(-2 * p), checks)

    alpha = sp.symbols("alpha", real=True)
    recentered = compose(xi, -alpha)
    require_zero("XR1_recenter_formula", recentered - (xi - alpha) / (1 - alpha * xi), checks)
    require_zero("XR1_recenter_A_ratio", A(recentered) - A(xi) / A(alpha), checks)

    return {
        "domain": "xi=x/X_max in (-1,1)",
        "composition": "(xi+eta)/(1+xi*eta)",
        "identity": "0",
        "inverse": "-xi",
        "endpoint_scope": "+-1 are not group elements; they are absorbing one-sided limits; (+1) composed (-1) is undefined 0/0",
        "additive_coordinate": "phi=atanh(xi)",
        "metric_factor": "A=(1-xi)/(1+xi)=exp(-2 phi)",
        "multiplicative_character": "A(xi composed eta)=A(xi)A(eta)",
        "reversal_character": "A(-xi)=1/A(xi)",
        "classification": "EXACT_WITHIN_WORKING_XMAX_PLUS_CHOSEN_FRACTIONAL_LINEAR_XR1_LAW_SIGNED_ORIENTED_DOMAIN_AND_ADDITIVE_COORDINATE_TO_METRIC_PHI_IDENTIFICATION",
    }


def alternative_bounded_group_tile(checks: dict[str, str]) -> dict:
    """Smooth countermodel: generic bounded group axioms do not force XR1."""
    u = sp.symbols("u", real=True)
    compactify = u / sp.sqrt(1 + u**2)
    derivative = sp.simplify(sp.diff(compactify, u))
    require_zero("alternative_compactification_derivative", derivative - (1 + u**2) ** sp.Rational(-3, 2), checks)
    require_zero("alternative_compactification_origin", compactify.subs(u, 0), checks)
    require_zero("alternative_compactification_odd", compactify.subs(u, -u) + compactify, checks)
    if sp.limit(compactify, u, sp.oo) != 1 or sp.limit(compactify, u, -sp.oo) != -1:
        raise AssertionError("alternative compactification lost finite endpoints")
    checks["alternative_compactification_finite_endpoints"] = "PASS"

    xi_value = 1 / sp.sqrt(2)
    # f^{-1}(1/sqrt(2))=1, so composing two equal elements through
    # additive u gives f(2)=2/sqrt(5).
    alternative_composed = 2 / sp.sqrt(5)
    A = lambda value: sp.simplify((1 - value) / (1 + value))
    A_composed = sp.radsimp(A(alternative_composed))
    A_product = sp.expand(sp.radsimp(A(xi_value) ** 2))
    require_zero("alternative_A_composed_witness", A_composed - (9 - 4 * sp.sqrt(5)), checks)
    require_zero("alternative_A_product_witness", A_product - (17 - 12 * sp.sqrt(2)), checks)
    if sp.simplify(A_composed - A_product) == 0:
        raise AssertionError("alternative bounded group unexpectedly preserves A character")
    checks["alternative_bounded_group_breaks_A_character"] = "PASS"

    return {
        "compactification": "xi=f(u)=u/sqrt(1+u^2), u in R",
        "inverse_coordinate": "u=xi/sqrt(1-xi^2)",
        "composition": "xi boxplus eta=f(f_inverse(xi)+f_inverse(eta))",
        "properties": "smooth ordered associative commutative group by conjugation of additive R; identity 0; inverse -xi; endpoints +-1",
        "witness": {
            "xi": "1/sqrt(2)",
            "xi_boxplus_xi": "2/sqrt(5)",
            "A_of_composition": str(A_composed),
            "A_product": str(A_product),
        },
        "classification": "EXACT_COUNTERMODEL_FINITE_BOUND_COMPOSITION_REVERSAL_AND_REGULARITY_DO_NOT_FORCE_FRACTIONAL_LINEAR_XR1_OR_MULTIPLICATIVE_A",
    }


def involution_tile(checks: dict[str, str]) -> dict:
    xi, sigma, X = sp.symbols("xi sigma X", positive=True)
    arithmetic = 1 / xi
    require_zero("XR2_involution", 1 / arithmetic - xi, checks)
    arithmetic_witness = arithmetic.subs(xi, sp.Rational(1, 2))
    require_zero("XR2_inside_maps_outside_witness", arithmetic_witness - 2, checks)

    complement = 1 - xi
    require_zero("XR3_involution", 1 - complement - xi, checks)
    complement_identity_image = complement.subs(xi, 0)
    require_zero("XR3_identity_not_preserved", complement_identity_image - 1, checks)
    # A homomorphism would satisfy C(xi composed eta)=C(xi) composed C(eta).
    compose = lambda left, right: sp.cancel((left + right) / (1 + left * right))
    complement_defect = sp.factor((1 - compose(xi, sp.Rational(1, 3))) - compose(1 - xi, sp.Rational(2, 3)))
    if complement_defect == 0:
        raise AssertionError("XR3 complement unexpectedly became a homomorphism")
    checks["XR3_not_composition_homomorphism"] = "PASS"

    scale_dual = X**2 / sigma
    require_zero("XR4_scale_involution", X**2 / scale_dual - sigma, checks)
    require_zero("XR4_scale_fixed_point", scale_dual.subs(sigma, X) - X, checks)
    scale_witness = scale_dual.subs(sigma, X / 2)
    require_zero("XR4_below_X_maps_above_X", scale_witness - 2 * X, checks)

    return {
        "arithmetic_x_to_X2_over_x": {
            "dimensionless_map": "xi -> 1/xi",
            "witness": "xi=1/2 -> 2 outside (-1,1)",
            "classification": "VALID_INVOLUTION_ON_NONZERO_EXTENDED_DOMAIN_NOT_INTERNAL_MAXIMUM_REACH_RECIPROCITY",
        },
        "boundary_complement": {
            "map": "xi -> 1-xi on [0,1]",
            "identity_image": "0 -> 1",
            "composition_defect": str(complement_defect),
            "classification": "INVOLUTION_BUT_NOT_POSITIONAL_REVERSAL_OR_COMPOSITION_AUTOMORPHISM",
        },
        "scale_dual": {
            "map": "sigma -> X_max^2/sigma",
            "fixed_point": "sigma=X_max",
            "witness": "sigma=X_max/2 -> 2 X_max",
            "classification": "VALID_POSITIVE_SCALE_INVOLUTION_BUT_NOT_SELF_MAP_OF_SUBMAXIMAL_REACH_DOMAIN",
        },
    }


def metric_symmetry_tile(checks: dict[str, str]) -> dict:
    xi, alpha, k = sp.symbols("xi alpha k", real=True, finite=True)
    A = lambda value: sp.cancel((1 - value) / (1 + value))
    transformed = sp.cancel((xi - alpha) / (1 - alpha * xi))
    derivative = sp.factor(sp.diff(transformed, xi))
    expected_derivative = (1 - alpha**2) / (1 - alpha * xi) ** 2
    require_zero("metric_recenter_derivative", derivative - expected_derivative, checks)

    time_ratio = sp.factor(A(transformed) / A(xi))
    spatial_ratio = sp.factor(A(xi) * derivative**2 / A(transformed))
    require_zero("metric_time_ratio", time_ratio - (1 + alpha) / (1 - alpha), checks)

    witness = {alpha: sp.Rational(1, 3)}
    spatial_0 = sp.simplify(spatial_ratio.subs(witness | {xi: 0}))
    spatial_half = sp.simplify(spatial_ratio.subs(witness | {xi: sp.Rational(1, 2)}))
    require_zero("metric_spatial_ratio_at_zero", spatial_0 - sp.Rational(32, 81), checks)
    require_zero("metric_spatial_ratio_at_half", spatial_half - sp.Rational(512, 625), checks)
    if spatial_0 == spatial_half:
        raise AssertionError("position-dependent spatial ratio unexpectedly constant")
    checks["metric_no_constant_time_rescaling_can_restore_conformal_ratio"] = "PASS"

    invariant_h = 1 / (1 - xi**2) ** 2
    require_zero(
        "XR1_invariant_spatial_metric",
        invariant_h.subs(xi, transformed) * derivative**2 - invariant_h,
        checks,
    )
    current_h = 1 / A(xi)
    ratio_current_to_invariant = sp.factor(current_h / invariant_h)
    require_zero(
        "current_vs_invariant_spatial_ratio",
        ratio_current_to_invariant - (1 - xi) * (1 + xi) ** 3,
        checks,
    )
    if sp.diff(ratio_current_to_invariant, xi) == 0:
        raise AssertionError("current radial metric unexpectedly XR1 invariant")
    checks["current_radial_metric_not_XR1_invariant"] = "PASS"

    # Exact endpoint distances: current proper radial length is finite, while
    # XR1-invariant rapidity distance and current optical distance diverge.
    theta = sp.symbols("theta", real=True)
    # With xi=cos(theta), the endpoint integral becomes
    # integral_0^(pi/2) (1+cos(theta)) dtheta.
    current_proper = sp.integrate(1 + sp.cos(theta), (theta, 0, sp.pi / 2))
    require_zero("current_proper_endpoint_integral", current_proper - (1 + sp.pi / 2), checks)
    optical_primitive = -xi - 2 * sp.log(1 - xi)
    require_zero("current_optical_primitive", sp.diff(optical_primitive, xi) - (1 + xi) / (1 - xi), checks)
    invariant_primitive = sp.atanh(xi)

    return {
        "recenter": "xi'=(xi-alpha)/(1-alpha*xi)",
        "time_component_ratio_t_unchanged": str(time_ratio),
        "spatial_component_ratio": str(spatial_ratio),
        "spatial_ratio_witnesses_alpha_one_third": {"xi_0": str(spatial_0), "xi_half": str(spatial_half)},
        "constant_time_rescaling": "cannot remove xi dependence of the spatial ratio",
        "XR1_invariant_spatial_line": "dell^2 proportional dxi^2/(1-xi^2)^2 = dphi^2",
        "current_reciprocal_spatial_line": "dell^2 proportional ((1+xi)/(1-xi)) dxi^2",
        "current_to_invariant_coefficient_ratio": str(ratio_current_to_invariant),
        "current_proper_distance_0_to_X_over_X": str(current_proper),
        "current_optical_primitive_over_X": str(optical_primitive),
        "XR1_invariant_distance_primitive": str(invariant_primitive),
        "endpoint_classification": "CURRENT_PROPER_DISTANCE_FINITE; CURRENT_OPTICAL_AND_XR1_RAPIDITY_DISTANCES_DIVERGE",
        "classification": "XR1_RECENTERING_NOT_ISOMETRY_OR_CSN_EQUIVALENCE_OF_PINNED_RECIPROCAL_METRIC_WITH_UNCHANGED_OR_CONSTANTLY_RESCALED_TIME",
        "scope": "declared static diagonal transformation class; a new field/frame action remains open",
    }


def angular_extension_tile(checks: dict[str, str]) -> dict:
    phi = sp.symbols("phi", positive=True)
    warps = {"flat": phi, "hyperbolic": sp.sinh(phi), "spherical_local": sp.sin(phi)}
    curvatures = {}
    expected = {"flat": (0, 0), "hyperbolic": (-1, -1), "spherical_local": (1, 1)}
    for name, warp in warps.items():
        radial = sp.simplify(-sp.diff(warp, phi, 2) / warp)
        tangential = sp.simplify((1 - sp.diff(warp, phi) ** 2) / warp**2)
        require_zero(f"angular_{name}_radial_curvature", radial - expected[name][0], checks)
        require_zero(f"angular_{name}_tangential_curvature", tangential - expected[name][1], checks)
        curvatures[name] = {"f(phi)": str(warp), "K_radial": str(radial), "K_tangential": str(tangential)}

    # Conditional isotropic Lorentz-like extension: non-collinear boost-like
    # generators close into a spatial rotation.  This is comparison group
    # algebra, not an adoption of SR dynamics or of physical position boosts.
    Kx = sp.zeros(4); Kx[0, 1] = 1; Kx[1, 0] = 1
    Ky = sp.zeros(4); Ky[0, 2] = 1; Ky[2, 0] = 1
    Jz = sp.zeros(4); Jz[1, 2] = -1; Jz[2, 1] = 1
    commutator = Kx * Ky - Ky * Kx
    require_zero("conditional_isotropic_noncollinear_commutator", commutator + Jz, checks)

    # Flat isotropic counterextension: use additive u in R^3 and compactify
    # radially by x=X tanh(|u|) u/|u|.  Collinear composition is XR1, while
    # the translation generators commute.  Homogeneous-coordinate matrices
    # encode the two independent affine translations.
    Tx = sp.zeros(4); Tx[1, 0] = 1
    Ty = sp.zeros(4); Ty[2, 0] = 1
    flat_commutator = Tx * Ty - Ty * Tx
    require_zero("flat_isotropic_extension_commuting_translations", flat_commutator, checks)

    return {
        "radial_data_counterfamily": curvatures,
        "counterfamily_result": "SAME_RADIAL_PHI_COORDINATE_ALLOWS_LOCAL_ANGULAR_SECTIONAL_CURVATURE_MINUS_ONE_ZERO_OR_PLUS_ONE",
        "conditional_isotropic_group": {
            "algebra": "[Kx,Ky]=-Jz",
            "commutator": str(commutator.tolist()),
            "meaning": "non-collinear recenterings conditionally generate angular rotation/local holonomy",
            "premises": "CHOSEN standard Lorentz/negative-curvature position-space embedding",
            "status": "CHOSE_CONDITIONAL_COMPARISON_NOT_DERIVED_FROM_1D_XR1_OR_ISOTROPY_HOMOGENEITY_ALONE",
        },
        "flat_isotropic_counterextension": {
            "map": "u in R^3 -> x=X tanh(|u|) u/|u|",
            "collinear_law": "XR1",
            "translation_algebra": "[Tx,Ty]=0",
            "meaning": "bounded isotropic homogeneous ball realization with no forced rotational commutator",
        },
        "classification": "RADIAL_XR1_DOES_NOT_SELECT_ANGULAR_WARP_OR_HOLONOMY; ROTATIONAL_COMMUTATOR_REQUIRES_CHOSEN_NEGATIVE_CURVATURE_GROUP_EMBEDDING",
    }


def scale_and_boundary_tile(checks: dict[str, str]) -> dict:
    epsilon, y = sp.symbols("epsilon y", real=True)
    omega = 1 + epsilon * sp.cos(2 * sp.pi * y)
    average = sp.integrate(omega, (y, 0, 1))
    require_zero("CSN_local_family_same_global_length", average - 1, checks)
    if sp.diff(omega, y) == 0:
        raise AssertionError("local conformal counterfamily became constant")
    checks["CSN_local_modes_not_fixed_by_one_length"] = "PASS"

    xi = sp.symbols("xi", real=True)
    phi = sp.atanh(xi)
    require_zero("Xmax_phi_neutral_at_x_zero", phi.subs(xi, 0), checks)
    # The divergent limit is represented exactly by the one-sided SymPy limit.
    limit_phi = sp.limit(phi, xi, 1, dir="-")
    if limit_phi != sp.oo:
        raise AssertionError(f"Xmax phi limit changed: {limit_phi}")
    checks["Xmax_phi_diverges_at_reach_boundary"] = "PASS"

    return {
        "constant_scale": {
            "law": "L_max[s^2 g]=s L_max[g] for a geometric length functional",
            "one_condition": "L_max[g_*]=X_max fixes at most one global constant normalization",
        },
        "local_CSN_counterfamily": {
            "Omega_epsilon": "1+epsilon cos(2 pi y), |epsilon|<1",
            "unit_interval_average": str(average),
            "result": "infinitely many nonconstant positive local conformal factors preserve the same one-dimensional total length",
        },
        "finite_cell_comparison": {
            "Xmax_reach_boundary": "xi->1 implies phi->+infinity and A->0",
            "current_static_phi_seal": "phi=0 with normal derivative free",
            "same_surface_test": "incompatible under xi=tanh(phi): phi=0 maps to xi=0, not xi=1",
            "classification": "DISTINCT_OBJECTS_UNLESS_A_NEW_GLOBAL_MAP_IS_DERIVED",
        },
        "classification": "XMAX_CAN_FIX_AT_MOST_A_GLOBAL_SCALE_NORMALIZATION_WITHOUT_LOCAL_REPRESENTATIVE_SELECTION; FINITE_CELL_SEAL_NOT_IDENTIFIED_WITH_XMAX_BOUNDARY",
    }


def main() -> None:
    checks: dict[str, str] = {}
    bounded = bounded_composition_tile(checks)
    alternative = alternative_bounded_group_tile(checks)
    involutions = involution_tile(checks)
    metric = metric_symmetry_tile(checks)
    angular = angular_extension_tile(checks)
    scale_boundary = scale_and_boundary_tile(checks)

    result = {
        "schema": "udt-xmax-reciprocity-audit-1.0",
        "python": platform.python_version(),
        "sympy": sp.__version__,
        "checks": checks,
        "bounded_composition": bounded,
        "alternative_bounded_group_countermodel": alternative,
        "candidate_involutions": involutions,
        "metric_symmetry": metric,
        "angular_extension": angular,
        "scale_and_boundary": scale_boundary,
        "adjudication": {
            "Xmax_reciprocity": "EXACT_1D_MULTIPLICATIVE_RECIPROCITY_WITHIN_WORKING_XMAX_PLUS_CHOSEN_FRACTIONAL_LINEAR_XR1_AND_METRIC_PHI_JOIN; NOT_DERIVED_FROM_FINITE_BOUND_GENERIC_COMPOSITION_REVERSAL_ALONE",
            "full_metric_symmetry": "NOT_DERIVED_AND_REFUTED_FOR_NATURAL_MOBIUS_RECENTERING_IN_PINNED_STATIC_DIAGONAL_TRANSFORMATION_CLASS",
            "angular_selector": "NOT_DERIVED; CHOSEN_NEGATIVE_CURVATURE_GROUP_EXTENSION_GENERATES_ROTATIONAL_HOLONOMY_BUT_ARBITRARY_WARP_AND_FLAT_ISOTROPIC_COUNTEREXTENSIONS_SURVIVE",
            "CSN_representative": "ONE_GLOBAL_LENGTH_CAN_FIX_ONE_CONSTANT_SCALE_NOT_ARBITRARY_LOCAL_CONFORMAL_REPRESENTATIVE",
            "finite_cell": "XMAX_ASYMPTOTIC_REACH_BOUNDARY_AND_STATIC_PHI_ZERO_SEAL_ARE_DISTINCT_UNLESS_NEW_MAP_DERIVED",
            "action": "NOT_SELECTED; CURRENT_FIELD_LOCALITY_VARIATION_DERIVATIVE_SOURCE_AND_BOUNDARY_GATES_REMAIN",
            "copresence": "COMPATIBLE_WHOLE_SOLUTION_SEMANTICS_NOT_A_TRANSFORMATION_OR_ACTION_SELECTOR",
        },
        "maximum_conclusion": "THE_CHOSEN_FRACTIONAL_LINEAR_XR1_LAW_HAS_AN_EXACT_MULTIPLICATIVE_A_CHARACTER_AND_REVERSAL_A_TO_A_INVERSE_AFTER_IDENTIFYING_ITS_ADDITIVE_COORDINATE_WITH_METRIC_PHI; FINITE_XMAX_AND_GENERIC_GROUP_AXIOMS_DO_NOT_FORCE_XR1; XR1_IS_NOT_A_SYMMETRY_OF_THE_PINNED_RECIPROCAL_METRIC_UNDER_NATURAL_RECENTERING; ANGULAR_HOLONOMY_REQUIRES_A_CHOSEN_CURVED_GROUP_EMBEDDING; SCALE_ACTION_AND_FINITE_CELL_BRIDGES_REMAIN_OPEN",
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
