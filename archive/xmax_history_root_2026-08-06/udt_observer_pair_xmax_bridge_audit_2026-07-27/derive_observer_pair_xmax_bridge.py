#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
from fractions import Fraction
from pathlib import Path


HERE = Path(__file__).resolve().parent


CANDIDATES = [
    {
        "candidate_id": "C01",
        "candidate_family": "quotient_geodesic_diameter",
        "domain": "stationary_K_orbits_with_positive_complete_q",
        "domain_selected": "CONDITIONAL_BRANCH_ONLY",
        "covariance": "INTRINSIC_ON_ORBIT_SPACE",
        "composition_reversal": "SYMMETRIC_DISTANCE_TRIANGLE_NOT_ADDITIVE_COCYCLE",
        "angular_cut_locus": "ANGULAR_GEOMETRY_INCLUDED_SCALAR_DISTANCE_SINGLE_VALUED_VARIATION_MAY_BE_NONSMOOTH",
        "limit_type": "FINITE_ATTAINED_ON_SMOOTH_COMPACT_S3",
        "variation_type": "RIGHT_DERIVATIVE_MAX_OVER_ACTIVE_DIAMETER_PAIRS_MIN_OVER_ACTIVE_MINIMIZING_GEODESICS",
        "xmax_compatibility": "EXECUTABLE_MAXIMUM_SEPARATION_SCHEMA_BUT_NO_PHYSICAL_IDENTIFICATION_AND_DOES_NOT_REALIZE_SEPARATE_WORKING_UNATTAINABILITY_READING",
        "return_equation": "NONE_WITHOUT_NATIVE_TARGET_OR_STATIONARITY_RULE",
        "outcome": "DERIVED_EXECUTABLE_BRANCHWISE_GEOMETRIC_DIAMETER_NOT_OPERATIONAL_PHYSICAL_XMAX_BRIDGE",
    },
    {
        "candidate_id": "C02",
        "candidate_family": "Killing_norm_clock_depth",
        "domain": "normalized_stationary_K_endpoints_with_global_comparison_phi",
        "domain_selected": "CONDITIONAL_BRANCH_AND_ASSIGNMENT",
        "covariance": "K_RESCALING_INVARIANT_AS_ENDPOINT_RATIO",
        "composition_reversal": "SIGNED_ADDITIVE_COCYCLE_AND_OPERATOR_INVERSE_NOT_SYMMETRIC_DISTANCE",
        "angular_cut_locus": "PATH_INDEPENDENT_ENDPOINT_SCALAR_BUT_CANNOT_ENCODE_FULL_ANGULAR_PAIR_GEOMETRY",
        "limit_type": "BOUNDED_AND_ATTAINED_FOR_SMOOTH_PHI_ON_COMPACT_S3",
        "variation_type": "ENDPOINT_DISTRIBUTION;_RANGE_RIGHT_DERIVATIVE_MAX_ARGMAX_H_MINUS_MIN_ARGMIN_H",
        "xmax_compatibility": "NO_NATIVE_MAP_FROM_SIGNED_DEPTH_RANGE_TO_NONNEGATIVE_PAIR_SEPARATION",
        "return_equation": "NONE;_ENDPOINT_RESPONSE_IS_NOT_A_FIELD_EQUATION",
        "outcome": "DERIVED_BRANCHWISE_CLOCK_COCYCLE_NOT_COMPLETE_DISTANCE_OR_XMAX_BRIDGE",
    },
    {
        "candidate_id": "C03",
        "candidate_family": "optical_or_connection_weighted_path_depth",
        "domain": "future_metric_null_lifts_over_stationary_orbit_paths_under_STRICT_SLICE_POSITIVITY",
        "domain_selected": "CONDITIONAL_STATIONARY_BRANCH",
        "covariance": "DIRECTED_FUNCTIONAL_MODULO_ENDPOINT_TIME_SECTION_SHIFT;_ROUND_TRIP_AND_LOOP_DATA_INVARIANT",
        "composition_reversal": "PATH_CONCATENATION;_TWIST_MAKES_DIRECTED_REVERSAL_ASYMMETRIC",
        "angular_cut_locus": "FULL_Q_AND_CONNECTION_INCLUDED;_MULTIPLE_EXTREMAL_PATHS_GIVE_NONSMOOTH_ENVELOPE",
        "limit_type": "FINITE_ATTAINED_DISTANCE_ON_SMOOTH_COMPACT_STRONGLY_CONVEX_BRANCH",
        "variation_type": "PATH_SUPPORTED_INTEGRAL;_RIGHT_DERIVATIVE_MIN_OVER_ACTIVE_MINIMIZING_PATHS_AND_MAX_OVER_ACTIVE_DIAMETER_PAIRS",
        "xmax_compatibility": "STRONGEST_BRANCHWISE_PATH_OBJECT_BUT_NOT_UNATTAINED_AND_SIGNAL_ROLE_OPEN_UNDER_COPRESENCE",
        "return_equation": "NONE_WITHOUT_SELECTED_ALL_PAIR_SOLDER_TARGET_OR_VARIATIONAL_PRINCIPLE",
        "outcome": "DERIVED_BRANCHWISE_DIRECTED_NULL_PATH_GEOMETRY_NOT_PHYSICAL_XMAX_OR_BOOTSTRAP_BRIDGE",
    },
    {
        "candidate_id": "C04",
        "candidate_family": "projective_reciprocal_display",
        "domain": "supplied_oriented_one_dimensional_additive_depth_and_positive_scale_L",
        "domain_selected": "NOT_SELECTED",
        "covariance": "EXACT_ONLY_IN_REGISTERED_1D_PROJECTIVE_CLASS",
        "composition_reversal": "FRACTIONAL_SIGNED_COMPOSITION_AND_ODD_REVERSAL",
        "angular_cut_locus": "NO_GENERAL_NONCOLLINEAR_OR_CUT_LOCUS_COMPLETION",
        "limit_type": "UNATTAINED_PLUS_MINUS_L_ONLY_IF_INPUT_DEPTH_IS_UNBOUNDED",
        "variation_type": "ALGEBRAIC_SCALAR_DELTA_D_TANH_RHO_DELTA_L_PLUS_L_SECH2_RHO_DELTA_RHO",
        "xmax_compatibility": "CIRCULAR_IF_L_IS_INSERTED_AS_XMAX",
        "return_equation": "NONE;_REPARAMETERIZATION_NOT_SELECTION",
        "outcome": "UNIQUE_CONDITIONAL_1D_DISPLAY_NOT_METRIC_DERIVATION_OF_XMAX",
    },
    {
        "candidate_id": "C05",
        "candidate_family": "supremum_over_ordered_observer_pair_arrows",
        "domain": "supplied_observer_set_pairing_relation_and_arrow_functional",
        "domain_selected": "MISSING",
        "covariance": "SCHEMA_ONLY_UNTIL_ARROW_DATA_EXIST",
        "composition_reversal": "INHERITS_UNSUPPLIED_ARROW_LAW",
        "angular_cut_locus": "INHERITS_UNSUPPLIED_ARROW_AND_PATH_FAMILY",
        "limit_type": "ATTAINED_OR_UNATTAINED_DEPENDS_ON_DOMAIN_CONTINUITY_AND_COMPLETION",
        "variation_type": "UNDEFINED_BEFORE_FUNCTIONAL;_ENVELOPE_AFTER_SUPPLY",
        "xmax_compatibility": "EXACT_WORKING_OWNER_TYPE_BUT_NOT_YET_AN_EXECUTABLE_FUNCTIONAL",
        "return_equation": "NONE;_SUPREMUM_IS_AN_OUTPUT_NOT_A_RETURN_ARROW",
        "outcome": "WORKING_SCHEMA_MISSING_OPERATIONAL_ARROW_FUNCTIONAL",
    },
]


def exact_control() -> dict[str, object]:
    # An exact rational null-path control.  Choose exp(phi)=2, c=3, a=1,
    # q(v,v)=9 and sigma_3(v)=2.  No floating-point tolerance is involved.
    exp_phi = Fraction(2)
    c_e = Fraction(3)
    a = Fraction(1)
    sqrt_q = Fraction(3)
    sigma3_v = Fraction(2)
    f_forward = (exp_phi * sqrt_q - a * sigma3_v) / c_e
    f_reverse = (exp_phi * sqrt_q + a * sigma3_v) / c_e
    assert f_forward == Fraction(4, 3)
    assert f_reverse == Fraction(8, 3)
    assert f_forward + f_reverse == 2 * exp_phi * sqrt_q / c_e
    assert f_forward - f_reverse == -2 * a * sigma3_v / c_e
    # Substitution back into g(v+tdot K,v+tdot K)=0.
    assert -(c_e * f_forward + a * sigma3_v) ** 2 / exp_phi**2 + sqrt_q**2 == 0
    assert -(c_e * f_reverse - a * sigma3_v) ** 2 / exp_phi**2 + sqrt_q**2 == 0

    # Slice/Randers positivity equivalence in the registered sigma_3 direction.
    # C=R^2 exp(2phi), so e^phi sqrt(C)=R exp(2phi).
    r = Fraction(5)
    exp_phi_2 = Fraction(4)
    a_control = Fraction(7)
    strict_slice = a_control**2 < r**2 * exp_phi_2**2
    randers = abs(a_control) < r * exp_phi_2
    assert strict_slice and strict_slice == randers

    # Lapse ratio and signed reciprocal depth are independent of constant K rescaling.
    n_a = Fraction(12)
    n_b = Fraction(3)
    alpha = Fraction(7, 2)
    assert n_b / n_a == (alpha * n_b) / (alpha * n_a) == Fraction(1, 4)

    # One-dimensional projective composition is exact but scale-dependent.
    x = Fraction(1, 3)
    y = Fraction(1, 4)
    length = Fraction(2)
    composed = (x + y) / (1 + x * y / length**2)
    assert composed == Fraction(28, 49)

    # A nonzero vector tangent to a phi level has zero clock-depth rate but
    # strictly positive reversible optical length.  This is the local angular
    # obstruction to a universal scalar solder.
    dphi_v = Fraction(0)
    q_vv = Fraction(9)
    reversible_optical_rate = exp_phi * sqrt_q / c_e
    assert dphi_v == 0 and q_vv > 0 and reversible_optical_rate == Fraction(2)

    return {
        "forward": str(f_forward),
        "reverse": str(f_reverse),
        "round_trip_sum": str(f_forward + f_reverse),
        "twist_antisymmetry": str(f_forward - f_reverse),
        "null_substitution_exact": True,
        "randers_slice_positivity_equivalent": True,
        "lapse_ratio_K_rescaling_invariant": True,
        "projective_1d_identity_exact": True,
        "phi_level_tangent_obstruction_exact": True,
    }


def write_outcomes() -> None:
    fieldnames = list(CANDIDATES[0])
    with (HERE / "CANDIDATE_OUTCOMES.tsv").open("w", newline="") as handle:
        writer = csv.DictWriter(handle, delimiter="\t", fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(CANDIDATES)


def main() -> int:
    with (HERE / "CANDIDATE_UNIVERSE.tsv").open(newline="") as handle:
        universe = list(csv.DictReader(handle, delimiter="\t"))
    assert [row["candidate_id"] for row in universe] == [row["candidate_id"] for row in CANDIDATES]
    write_outcomes()
    result = {
        "schema": "udt.observer_pair_xmax_bridge.derivation.v1",
        "status": "PASS_CLASSIFIED_NO_COMPLETE_BRIDGE",
        "candidate_count": 5,
        "candidate_outcomes": {row["candidate_id"]: row["outcome"] for row in CANDIDATES},
        "exact_control": exact_control(),
        "derived_relations": {
            "orbit_metric": "q=R^2 exp(2 lambda phi)(sigma1^2+sigma2^2)+R^2 exp(2 phi)sigma3^2",
            "lapse": "N=sqrt(-g(K,K))=c_E exp(-phi) for registered K=partial_t",
            "clock_ratio": "N_B/N_A=exp[-(phi_B-phi_A)]",
            "future_null_path": "c_E dt=exp(phi) ds_q-a sigma3",
            "reverse_null_path": "c_E dt_reverse=exp(phi) ds_q+a sigma3",
            "reversible_optical_element": "(F(v)+F(-v))/2=exp(phi) ds_q/c_E",
            "twist_odd_element": "(F(v)-F(-v))/2=-a sigma3/c_E",
            "strong_convexity": "a^2<R^2 exp(4phi), pointwise",
            "conditional_phi_from_q_anisotropy": "phi=log(C/A)/(2(1-lambda)), if lambda!=1 and the registered eigenvalue slots are identified",
            "diameter_first_variation": "D'_q[h]=max_(p,r in ArgDiam) min_(gamma in Min(p,r)) (1/2) integral_gamma h(v,v) ds for the right derivative",
            "clock_first_variation": "delta rho_AB=delta phi(B)-delta phi(A)",
            "clock_range_first_variation": "Range(phi)'[h]=max_(Argmax phi) h-min_(Argmin phi) h for the right derivative",
            "projective_first_variation": "delta d=tanh(rho) delta L+L sech^2(rho) delta rho",
        },
        "compact_smooth_stationary_ruling": {
            "q_diameter": "FINITE_ATTAINED",
            "clock_depth_range": "FINITE_ATTAINED",
            "strongly_convex_optical_distance": "FINITE_ATTAINED",
            "unattained_finite_limit_requires": [
                "noncompact_or_open_observer_domain",
                "excluded_limit_points",
                "singular_or_unbounded_profile_or_weight",
                "projective_display_with_independently_supplied_scale",
                "or_an_unregistered_noncontinuous_functional",
            ],
        },
        "positive_nondegenerate_scalar_distance_equal_to_signed_clock_cocycle": "OBSTRUCTED_ON_FULL_ANGULAR_SPACE_BY_NONZERO_TANGENTS_IN_KERNEL_OF_DPHI",
        "all_pair_clock_cocycle_linearization": "INFINITE_DIMENSIONAL_MOD_CONSTANTS_IF_A_PHYSICAL_PAIR_DOMAIN_IS_SUPPLIED",
        "physical_null_signal_interpretation": "OPEN_UNDER_COPRESENCE",
        "operational_Xmax_bridge_status": "NOT_SELECTED_IN_FROZEN_FIVE_CANDIDATES",
        "field_valued_global_to_local_return_equation_status": "NOT_SELECTED_IN_FROZEN_FIVE_CANDIDATES",
        "bootstrap_status": "WORKING_ON_SHELL_ADMISSIBILITY_ONLY_UNCHANGED",
        "complete_4D_extension_status": "OPEN_UNCHANGED",
        "strong_local_CSN_status": "CHALLENGED_OWNER_POSTULATE_NOT_DERIVED_INACTIVE",
        "phi_native_field_ownership": "FOUNDED_PAIR_DEPTH_NOT_SELECTED_INDEPENDENT_NATIVE_SCALAR",
        "c_E_G_obs_scale_closure": "NOT_DERIVED_SUFFICIENT_FOR_LENGTH_OR_DENSITY",
        "cross_branch_splice_used": False,
        "scope_beyond_frozen_five": "OPEN_NOT_CLASSIFIED",
        "maximum_conclusion": "BRANCHWISE_DIRECTED_NULL_PATH_GEOMETRY_DERIVED;_FIVE_TYPES_CLASSIFIED;_NO_OPERATIONAL_XMAX_OR_FIELD_VALUED_RETURN_SELECTED",
    }
    (HERE / "DERIVATION_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
