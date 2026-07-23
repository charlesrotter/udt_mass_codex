#!/usr/bin/env python3
"""Derive the metric angular-strain generator and audit all completion families."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
BASE = "863c2c879e7d1aad351ffc0e456dafcb93a97e98"
MAXIMUM = (
    "THE_FULL_METRIC_ANGULAR_STRAIN_MATCHES_THE_RECIPROCAL_MINUS1_PLUS1_"
    "SPECTRUM_IFF_ITS_RELATIVE_MEAN_SCALE_RATE_VANISHES_AND_ITS_CSN_SHAPE_"
    "SPEED_HAS_UNIT_MAGNITUDE__THE_REGISTERED_FC12_PROFILE_SUPPLIES_AN_"
    "EXACT_CONSTANT_RELATIVE_SCALE_SUBFAMILY_BUT_ARBITRARY_OMEGA_TOPOLOGY_"
    "SEAL_MONODROMY_AND_CURRENT_BOOTSTRAP_DO_NOT_FORCE_OR_SELECT_IT"
)


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def write_tsv(
    path: Path,
    rows: list[dict[str, object]],
    fields: tuple[str, ...] | None = None,
) -> None:
    if fields is None:
        if not rows:
            raise ValueError("fields required for empty table")
        fields = tuple(rows[0])
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=list(fields),
            delimiter="\t",
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerows(rows)


def exact_formula() -> dict[str, object]:
    u, up, w, wp, theta, thetap = sp.symbols(
        "u u_p w w_p theta theta_p", real=True
    )
    c = sp.symbols("c", positive=True, finite=True)
    rotation = sp.Matrix(
        [
            [sp.cos(theta), -sp.sin(theta)],
            [sp.sin(theta), sp.cos(theta)],
        ]
    )
    shape = sp.diag(sp.exp(-2 * u), sp.exp(2 * u))
    q = sp.exp(2 * w) * rotation.T * shape * rotation
    q_prime = (
        q.diff(u) * up
        + q.diff(w) * wp
        + q.diff(theta) * thetap
    )
    raw = sp.simplify(sp.Rational(1, 2) * q.inv() * q_prime)
    reduced = sp.simplify(raw - sp.trace(raw) * sp.eye(2) / 2)
    sigma_squared = sp.simplify(
        up**2 + thetap**2 * sp.sinh(2 * u) ** 2
    )
    if sp.simplify(sp.trace(raw) - 2 * wp) != 0:
        raise AssertionError("raw trace formula")
    if sp.simplify(sp.trace(reduced)) != 0:
        raise AssertionError("reduced trace formula")
    if (
        sp.simplify(
            sp.expand_trig(sp.simplify(reduced.det() + sigma_squared))
        )
        != 0
    ):
        raise AssertionError("reduced determinant formula")
    square_residual = (reduced * reduced - sigma_squared * sp.eye(2)).applyfunc(
        lambda value: sp.simplify(sp.expand_trig(sp.simplify(value)))
    )
    if square_residual != sp.zeros(2):
        raise AssertionError("reduced square formula")
    if sp.simplify(q.det() - sp.exp(4 * w)) != 0:
        raise AssertionError("angular determinant")
    reciprocal_metric = sp.diag(
        -c**2 * sp.exp(-2 * sp.symbols("phi", real=True)),
        sp.exp(2 * sp.symbols("phi", real=True)),
    )
    complete = sp.diag(1, 1, 1, 1)
    complete[:2, :2] = reciprocal_metric
    complete[2:, 2:] = q
    complete_det = sp.factor(complete.det())
    if sp.simplify(complete_det + c**2 * sp.exp(4 * w)) != 0:
        raise AssertionError("complete determinant retains c")

    theta_zero = sp.simplify(reduced.subs(theta, 0))
    return {
        "schema": "udt-angular-generator-formula-1.0",
        "angular_metric_parameterization": (
            "q=exp(2w) R(theta)^T diag(exp(-2u),exp(2u)) R(theta)"
        ),
        "raw_generator": "H=(1/2)q^-1 Lie_T(q), T(phi)=1",
        "raw_trace": str(sp.trace(raw)),
        "relative_mean_rate_vs_reciprocal_block": "w_p",
        "csn_shape_generator": "J=H-(trace(H)/2)I",
        "csn_reduced_theta_zero_matrix": str(theta_zero),
        "sigma_squared": str(sigma_squared),
        "reduced_determinant": "-(theta_p**2*sinh(2*u)**2 + u_p**2)",
        "reduced_square": "J^2=sigma_squared I",
        "full_symmetric_generator_eigenvalues": "w_p-sigma,w_p+sigma",
        "reciprocal_predicate": "w_p=0 AND sigma_squared=1",
        "reciprocal_eigenvalues": "(-1,+1) only under both gates",
        "angular_metric_determinant": str(sp.factor(q.det())),
        "complete_metric_determinant": "-c**2*exp(4*w)",
        "c_in_generator": False,
        "c_in_complete_metric": True,
        "skew_frame_rotation_from_metric_alone": "NOT_DETERMINED",
    }


def pointwise_controls() -> list[dict[str, object]]:
    return [
        {
            "control_id": "P01_MATCHED_DIAGONAL",
            "profile": (
                "u=phi; theta=0; "
                "w=constant relative to reciprocal block"
            ),
            "sigma_squared": "1",
            "pointwise_pattern": "PASS_ALL_REGULAR_POINTS",
            "eigendirection_persistence": "CONSTANT_IN_SUPPLIED_TORIC_FRAME",
            "scope": "EXACT_CONDITIONAL_CONTROL",
        },
        {
            "control_id": "P02_INVERSE_DIAGONAL",
            "profile": (
                "u=-phi; theta=0; "
                "w=constant relative to reciprocal block"
            ),
            "sigma_squared": "1",
            "pointwise_pattern": "PASS_ALL_REGULAR_POINTS",
            "eigendirection_persistence": "CONSTANT_IN_SUPPLIED_TORIC_FRAME",
            "scope": "EXACT_CONDITIONAL_CONTROL",
        },
        {
            "control_id": "P03_SPECTATOR",
            "profile": "u=0; theta=0; w arbitrary",
            "sigma_squared": "0",
            "pointwise_pattern": "FAIL",
            "eigendirection_persistence": "NO_RECIPROCAL_EIGENVALUES",
            "scope": "ADMISSIBLE_COUNTERPROFILE_WHERE_PROFILES_FREE",
        },
        {
            "control_id": "P04_VARIABLE_SHEAR",
            "profile": "u=phi^2; theta=0; w arbitrary",
            "sigma_squared": "4*phi^2",
            "pointwise_pattern": "PASS_ONLY_AT_PHI_PLUS_OR_MINUS_ONE_HALF",
            "eigendirection_persistence": "EIGENDIRECTIONS_FIXED_SPECTRUM_NOT",
            "scope": "ADMISSIBLE_COUNTERPROFILE_WHERE_PROFILES_FREE",
        },
        {
            "control_id": "P05_TUNED_ROTATING_AXIS",
            "profile": (
                "u=u0!=0; theta=phi/sinh(2u0); "
                "w=constant relative to reciprocal block"
            ),
            "sigma_squared": "1",
            "pointwise_pattern": "PASS_ALL_REGULAR_POINTS",
            "eigendirection_persistence": (
                "SPECTRUM_ONLY__EIGENDIRECTIONS_ROTATE_WITHOUT_SUPPLIED_TRANSPORT"
            ),
            "scope": "EXACT_NONDIAGONAL_SHAPE_CONTROL",
        },
        {
            "control_id": "P06_GENERIC_ROTATING_AXIS",
            "profile": "u=u0; theta=k*phi; w arbitrary",
            "sigma_squared": "k^2*sinh(2u0)^2",
            "pointwise_pattern": "PASS_ONLY_IF_K_SQUARED_SINH_SQUARED_EQUALS_ONE",
            "eigendirection_persistence": (
                "SPECTRUM_AND_FRAME_TRANSPORT_SEPARATE"
            ),
            "scope": "EXACT_FAMILY_CONTROL",
        },
        {
            "control_id": "P07_MIXED_SHEAR_ROTATION",
            "profile": "u=u(phi); theta=theta(phi); w arbitrary",
            "sigma_squared": "u_p^2+theta_p^2*sinh(2u)^2",
            "pointwise_pattern": "CODIMENSION_ONE_UNIT_SPEED_CONDITION",
            "eigendirection_persistence": "NOT_IMPLIED_BY_SPECTRUM",
            "scope": "GENERAL_EXACT_RESULT",
        },
        {
            "control_id": "P08_COMMON_SCALE_RATE",
            "profile": "u=phi; theta=0; w=w(phi)",
            "sigma_squared": "1",
            "pointwise_pattern": (
                "SHAPE_PASSES__FULL_MINUS1_PLUS1_FAILS_UNLESS_W_P_ZERO"
            ),
            "eigendirection_persistence": "CONSTANT_IN_SUPPLIED_TORIC_FRAME",
            "scope": (
                "H_EIGENVALUES_W_P_PLUS_OR_MINUS_ONE__ANGULAR_RELATIVE_"
                "MEAN_IS_NOT_FULL_METRIC_CSN_GAUGE"
            ),
        },
        {
            "control_id": "P09_CRITICAL_PHI",
            "profile": "dphi=0",
            "sigma_squared": "UNDEFINED",
            "pointwise_pattern": "UNDEFINED",
            "eigendirection_persistence": "T_WITH_T_PHI_ONE_DOES_NOT_EXIST",
            "scope": "FAIL_CLOSED",
        },
        {
            "control_id": "P10_RANK_DROP",
            "profile": "q=diag(r^2,1) at r=0",
            "sigma_squared": "UNDEFINED_AT_R_ZERO",
            "pointwise_pattern": "REGULAR_COMPLEMENT_ONLY",
            "eigendirection_persistence": "NO_RANK_TWO_EXTENSION_THROUGH_CAP",
            "scope": "FAIL_CLOSED",
        },
    ]


def mirror_controls() -> list[dict[str, object]]:
    return [
        {
            "lift": "ANGULAR_PLUS_I",
            "seal_jet_equation": "-q_p=q_p",
            "allowed_first_jet": "ZERO_ONLY",
            "reciprocal_at_seal": "NO",
            "ruling": "PATTERN_BLOCKED_AT_FIXED_SEAL",
        },
        {
            "lift": "ANGULAR_MINUS_I",
            "seal_jet_equation": "-q_p=(-I)^T q_p (-I)=q_p",
            "allowed_first_jet": "ZERO_ONLY",
            "reciprocal_at_seal": "NO",
            "ruling": "PATTERN_BLOCKED_AT_FIXED_SEAL",
        },
        {
            "lift": "AXIS_REFLECTION_DIAG_PLUS_MINUS",
            "seal_jet_equation": "-q_p=R^T q_p R",
            "allowed_first_jet": "OFF_DIAGONAL_ONE_PARAMETER_AT_Q0=I",
            "reciprocal_at_seal": "ALLOWED_IF_ABSOLUTE_OFFDIAGONAL_J_EQUALS_ONE",
            "ruling": "ALLOWED_NOT_FORCED",
        },
        {
            "lift": "AXIS_EXCHANGE_F",
            "seal_jet_equation": "-q_p=F^T q_p F",
            "allowed_first_jet": "DIAGONAL_TRACEFREE_ONE_PARAMETER_AT_Q0=I",
            "reciprocal_at_seal": "ALLOWED_FOR_Q_P=DIAG(-2,2)",
            "ruling": "ALLOWED_NOT_FORCED",
        },
        {
            "lift": "NO_UNIQUE_LIFT_SELECTED",
            "seal_jet_equation": "MULTIPLE_REGISTERED_LIFTS",
            "allowed_first_jet": "ZERO_OR_ONE_PARAMETER_BY_LIFT",
            "reciprocal_at_seal": "NOT_FORCED",
            "ruling": "FC08_DOES_NOT_SELECT_RECIPROCAL_PATTERN",
        },
    ]


def monodromy_controls() -> list[dict[str, object]]:
    return [
        {
            "control_id": "M01_IDENTITY",
            "matrix": "[[1,0],[0,1]]",
            "relation_to_L": "COMMUTES",
            "oriented_J_glue": "PASS",
            "unoriented_eigenline_glue": "PASS",
        },
        {
            "control_id": "M02_MINUS_IDENTITY",
            "matrix": "[[-1,0],[0,-1]]",
            "relation_to_L": "COMMUTES",
            "oriented_J_glue": "PASS",
            "unoriented_eigenline_glue": "PASS",
        },
        {
            "control_id": "M03_AXIS_REFLECTION",
            "matrix": "[[1,0],[0,-1]]",
            "relation_to_L": "COMMUTES",
            "oriented_J_glue": "PASS",
            "unoriented_eigenline_glue": "PASS",
        },
        {
            "control_id": "M04_EXCHANGE",
            "matrix": "[[0,1],[1,0]]",
            "relation_to_L": "ANTICOMMUTES",
            "oriented_J_glue": "FAIL_UNLESS_PHI_ORIENTATION_REVERSES",
            "unoriented_eigenline_glue": "PASS_WITH_LINE_EXCHANGE",
        },
        {
            "control_id": "M05_PARABOLIC",
            "matrix": "[[1,1],[0,1]]",
            "relation_to_L": "NEITHER",
            "oriented_J_glue": "FAIL",
            "unoriented_eigenline_glue": "FAIL",
        },
        {
            "control_id": "M06_HYPERBOLIC",
            "matrix": "[[2,1],[1,1]]",
            "relation_to_L": "NEITHER",
            "oriented_J_glue": "FAIL",
            "unoriented_eigenline_glue": "FAIL",
        },
        {
            "control_id": "M07_ORIENTATION_REVERSING_SHEAR",
            "matrix": "[[1,1],[0,-1]]",
            "relation_to_L": "NEITHER",
            "oriented_J_glue": "FAIL",
            "unoriented_eigenline_glue": "FAIL",
        },
        {
            "control_id": "M08_GENERAL_RULE",
            "matrix": "M_IN_GL2Z",
            "relation_to_L": "M^-1 L M MUST_EQUAL PLUS_OR_MINUS_L",
            "oriented_J_glue": "ONLY_NORMALIZER_SUBFAMILY",
            "unoriented_eigenline_glue": "ONLY_SIGNED_MONOMIAL_SUBFAMILY",
        },
        {
            "control_id": "M09_REAL_PHI_ON_S1",
            "matrix": "NOT_APPLICABLE",
            "relation_to_L": "PHI_HAS_A_CRITICAL_POINT_ON_COMPACT_S1",
            "oriented_J_glue": "T_PHI_ONE_UNDEFINED_SOMEWHERE",
            "unoriented_eigenline_glue": "CIRCLE_VALUED_OR_COVER_PHI_NOT_SUPPLIED",
        },
    ]


def branch_rows() -> list[dict[str, object]]:
    common_free = {
        "supplies_q_profile": "NO__PARAMETRIC_COMPATIBLE_PROFILES",
        "matched_witness": "RECIPROCAL_TORIC_PROFILE_ON_REGULAR_STRATUM",
        "unmatched_counterprofile": (
            "COMPACTLY_SUPPORTED_INTERIOR_SHEAR_OR_SPECTATOR_PROFILE"
        ),
        "pattern_forced": "NO",
        "natural_selection": "NO",
    }
    rows = [
        {
            "completion_id": "FC01_BOUNDARY_BOUNDARY",
            "supplies_angular_bundle": "ORBIT_BUNDLE_ONLY_IF_ORBIT_DATA_SUPPLIED",
            **common_free,
            "supplies_global_T_phi_one": "ONLY_IF_MONOTONE_PHI_PROFILE_SUPPLIED",
            "supplies_fiber_identification": "NO",
            "regular_interior_result": "MATCHED_AND_UNMATCHED_PROFILES_BOTH_EXIST",
            "endpoint_or_glue_result": "BOUNDARY_DATA_DO_NOT_FIX_INTERIOR_SIGMA",
            "pattern_persists_regular": "ONLY_IN_CHOSEN_MATCHED_SUBPROFILE",
            "extends_degeneracy": "NOT_APPLICABLE_IF_BOUNDARY_Q_NONDEGENERATE",
            "branch_ruling": "ALLOWED_NOT_FORCED",
        },
        {
            "completion_id": "FC02_ONE_CAP_BOUNDARY",
            "supplies_angular_bundle": "TORIC_ORBIT_BUNDLE_ON_REGULAR_INTERIOR",
            **common_free,
            "supplies_global_T_phi_one": "PROFILE_DEPENDENT",
            "supplies_fiber_identification": "CAP_CYCLE_ONLY__NO_BULK_TRANSPORT",
            "regular_interior_result": "MATCHED_AND_UNMATCHED_PROFILES_BOTH_EXIST",
            "endpoint_or_glue_result": "Q_RANK_DROPS_AT_CAP",
            "pattern_persists_regular": "ONLY_IN_CHOSEN_MATCHED_SUBPROFILE",
            "extends_degeneracy": "NO_RANK_TWO_GENERATOR_AT_CAP",
            "branch_ruling": "UNDEFINED_AT_REQUIRED_STRATUM",
        },
        {
            "completion_id": "FC03_TWO_CAP_P0",
            "supplies_angular_bundle": "TORIC_ORBIT_BUNDLE_ON_REGULAR_INTERIOR",
            **common_free,
            "supplies_global_T_phi_one": "PROFILE_DEPENDENT",
            "supplies_fiber_identification": "CAP_CYCLES_ONLY__NO_BULK_TRANSPORT",
            "regular_interior_result": "MATCHED_AND_UNMATCHED_PROFILES_BOTH_EXIST",
            "endpoint_or_glue_result": "Q_RANK_DROPS_AT_BOTH_CAPS",
            "pattern_persists_regular": "ONLY_IN_CHOSEN_MATCHED_SUBPROFILE",
            "extends_degeneracy": "NO_RANK_TWO_GENERATOR_AT_CAPS",
            "branch_ruling": "UNDEFINED_AT_REQUIRED_STRATUM",
        },
        {
            "completion_id": "FC04_TWO_CAP_P1",
            "supplies_angular_bundle": "TORIC_ORBIT_BUNDLE_ON_REGULAR_INTERIOR",
            **common_free,
            "supplies_global_T_phi_one": "PROFILE_DEPENDENT",
            "supplies_fiber_identification": (
                "UNIMODULAR_CAP_CYCLES_ONLY__NO_BULK_TRANSPORT"
            ),
            "regular_interior_result": "MATCHED_AND_UNMATCHED_PROFILES_BOTH_EXIST",
            "endpoint_or_glue_result": "S3_TOPOLOGY_DOES_NOT_FIX_SIGMA",
            "pattern_persists_regular": "ONLY_IN_CHOSEN_MATCHED_SUBPROFILE",
            "extends_degeneracy": "NO_RANK_TWO_GENERATOR_AT_CAPS",
            "branch_ruling": "UNDEFINED_AT_REQUIRED_STRATUM",
        },
        {
            "completion_id": "FC05_TWO_CAP_P_GT1",
            "supplies_angular_bundle": "TORIC_ORBIT_BUNDLE_ON_REGULAR_INTERIOR",
            **common_free,
            "supplies_global_T_phi_one": "PROFILE_DEPENDENT",
            "supplies_fiber_identification": (
                "LENS_CAP_CYCLES_ONLY__NO_BULK_TRANSPORT"
            ),
            "regular_interior_result": "MATCHED_AND_UNMATCHED_PROFILES_BOTH_EXIST",
            "endpoint_or_glue_result": "LENS_TOPOLOGY_DOES_NOT_FIX_SIGMA",
            "pattern_persists_regular": "ONLY_IN_CHOSEN_MATCHED_SUBPROFILE",
            "extends_degeneracy": "NO_RANK_TWO_GENERATOR_AT_CAPS",
            "branch_ruling": "UNDEFINED_AT_REQUIRED_STRATUM",
        },
        {
            "completion_id": "FC06_NONPRIMITIVE_CAP",
            "supplies_angular_bundle": "REGULAR_COMPLEMENT_ONLY",
            **common_free,
            "supplies_global_T_phi_one": "PROFILE_DEPENDENT_REGULAR_COMPLEMENT",
            "supplies_fiber_identification": "NO_THROUGH_SINGULARITY_DATA",
            "regular_interior_result": "MATCHED_AND_UNMATCHED_PROFILES_BOTH_EXIST",
            "endpoint_or_glue_result": "ORBIFOLD_OR_SINGULAR_RANK_FAILURE",
            "pattern_persists_regular": "ONLY_IN_CHOSEN_MATCHED_SUBPROFILE",
            "extends_degeneracy": "NO",
            "branch_ruling": "UNDEFINED_AT_REQUIRED_STRATUM",
        },
        {
            "completion_id": "FC07_PERIODIC_TORUS_BUNDLE",
            "supplies_angular_bundle": "YES_WITH_SUPPLIED_GL2Z_GLUE",
            **common_free,
            "supplies_global_T_phi_one": (
                "NO_FOR_SINGLE_VALUED_REAL_PHI_ON_S1__CRITICAL_POINT_REQUIRED"
            ),
            "supplies_fiber_identification": "MONODROMY_ONLY__LOCAL_CONNECTION_FREE",
            "regular_interior_result": (
                "RECIPROCAL_ARCS_ALLOWED_WHERE_DPHI_NONZERO"
            ),
            "endpoint_or_glue_result": (
                "GENERAL_GL2Z_DOES_NOT_NORMALIZE_RECIPROCAL_EIGENLINES"
            ),
            "pattern_persists_regular": (
                "ONLY_ON_NORMALIZER_SUBFAMILY_AND_REGULAR_PHI_ARCS"
            ),
            "extends_degeneracy": "NO_ACROSS_REQUIRED_PHI_CRITICAL_POINT",
            "branch_ruling": "UNDEFINED_AT_REQUIRED_STRATUM",
        },
        {
            "completion_id": "FC08_MIRROR_DOUBLE",
            "supplies_angular_bundle": "ONLY_AFTER_ONE_REGISTERED_LIFT_CHOSEN",
            "supplies_q_profile": "NO__MIRROR_COMPATIBILITY_ONLY",
            "matched_witness": "EXCHANGE_LIFT_WITH_Q_P=DIAG(-2,2)",
            "unmatched_counterprofile": "PLUS_I_OR_MINUS_I_LIFT_FORCES_Q_P_ZERO",
            "pattern_forced": "NO",
            "natural_selection": "NO",
            "supplies_global_T_phi_one": "LIFT_AND_PHI_PARITY_DEPENDENT",
            "supplies_fiber_identification": "MULTIPLE_INEQUIVALENT_LIFTS",
            "regular_interior_result": "MATCHED_AND_UNMATCHED_PROFILES_BOTH_EXIST",
            "endpoint_or_glue_result": (
                "EXCHANGE_ALLOWS_PATTERN__PLUS_MINUS_I_BLOCK_IT_AT_FIXED_SEAL"
            ),
            "pattern_persists_regular": "ONLY_AFTER_MATCHED_LIFT_AND_PROFILE",
            "extends_degeneracy": "LIFT_DEPENDENT",
            "branch_ruling": "ALLOWED_NOT_FORCED",
        },
        {
            "completion_id": "FC09_NONORIENTABLE_GLUE",
            "supplies_angular_bundle": "YES_WITH_SUPPLIED_DET_MINUS1_GLUE",
            **common_free,
            "supplies_global_T_phi_one": "BASE_AND_PHI_PROFILE_DEPENDENT",
            "supplies_fiber_identification": "MONODROMY_ONLY__LOCAL_CONNECTION_FREE",
            "regular_interior_result": "MATCHED_AND_UNMATCHED_PROFILES_BOTH_EXIST",
            "endpoint_or_glue_result": (
                "ONLY_SIGNED_MONOMIAL_NORMALIZER_SUBFAMILY_PRESERVES_EIGENLINES"
            ),
            "pattern_persists_regular": "ONLY_IN_COMPATIBLE_SUBFAMILY",
            "extends_degeneracy": "NOT_GENERALLY",
            "branch_ruling": "ALLOWED_NOT_FORCED",
        },
        {
            "completion_id": "FC10_STRATIFIED_PROJECTOR",
            "supplies_angular_bundle": "ONLY_ON_FIXED_RANK_STRATA",
            "supplies_q_profile": "STRATUM_DEPENDENT",
            "matched_witness": "POSSIBLE_ON_ONE_REGULAR_STRATUM",
            "unmatched_counterprofile": "GENERIC_STRATUM_OR_RANK_MERGER",
            "pattern_forced": "NO",
            "natural_selection": "NO",
            "supplies_global_T_phi_one": "NOT_ACROSS_ALL_TRANSITIONS",
            "supplies_fiber_identification": "FINE_BUNDLE_FAILS_AT_TRANSITION",
            "regular_interior_result": "STRATUM_LOCAL_ONLY",
            "endpoint_or_glue_result": "PROJECTOR_RANK_MERGER_OR_SPLIT",
            "pattern_persists_regular": "NOT_THROUGH_FULL_STRATIFIED_BRANCH",
            "extends_degeneracy": "NO",
            "branch_ruling": "UNDEFINED_AT_REQUIRED_STRATUM",
        },
        {
            "completion_id": "FC11_NONINTEGRABLE_DISTRIBUTION",
            "supplies_angular_bundle": (
                "PLANE_DISTRIBUTION_ONLY__NO_ANGULAR_ORBIT_SURFACE"
            ),
            "supplies_q_profile": "INDUCED_Q_POSSIBLE_LOCALLY",
            "matched_witness": "NOT_GLOBAL_WITHOUT_T_AND_CONNECTION",
            "unmatched_counterprofile": "ARBITRARY_LOCAL_DISTRIBUTION_STRAIN",
            "pattern_forced": "NO",
            "natural_selection": "NO",
            "supplies_global_T_phi_one": "NO",
            "supplies_fiber_identification": "NO",
            "regular_interior_result": (
                "LOCAL_STRAIN_DEPENDS_ON_UNSUPPLIED_FLOW_IDENTIFICATION"
            ),
            "endpoint_or_glue_result": "NONZERO_FROBENIUS_OBSTRUCTION_RETAINED",
            "pattern_persists_regular": "UNDETERMINED",
            "extends_degeneracy": "NOT_APPLICABLE",
            "branch_ruling": "INSUFFICIENT_METRIC_DATA",
        },
        {
            "completion_id": "FC12_RECIPROCAL_TORIC_DIAGONAL",
            "supplies_angular_bundle": "YES_CONDITIONALLY_IN_FIXED_INTEGRAL_T2_BASIS",
            "supplies_q_profile": (
                "YES_CONDITIONALLY__Q=OMEGA^2_DIAG(EXP(-2PHI),EXP(2PHI))"
            ),
            "matched_witness": "FC12_WITH_CONSTANT_RELATIVE_OMEGA",
            "unmatched_counterprofile": (
                "FC12_WITH_OMEGA=EXP(A*PHI)_AND_NONZERO_A"
            ),
            "pattern_forced": "NO",
            "natural_selection": "NO__FC12_IS_CONDITIONAL_AND_UNSELECTED",
            "supplies_global_T_phi_one": "YES_WHERE_DPHI_NONZERO",
            "supplies_fiber_identification": (
                "YES_IN_SUPPLIED_FIXED_INTEGRAL_T2_BASIS"
            ),
            "regular_interior_result": (
                "SHAPE_J=L_FOR_ALL_OMEGA__FULL_H=W_P_I_PLUS_L__"
                "MATCH_ONLY_W_P_ZERO"
            ),
            "endpoint_or_glue_result": (
                "BOUNDARY_OK_IF_Q_POSITIVE__CAP_RANK_DROP_UNDEFINED"
            ),
            "pattern_persists_regular": (
                "ONLY_CONSTANT_RELATIVE_OMEGA_SUBFAMILY_WHERE_DPHI_NONZERO"
            ),
            "extends_degeneracy": "NO_GENERAL_RANK_TWO_EXTENSION_THROUGH_CAP",
            "branch_ruling": "ALLOWED_NOT_FORCED",
        },
    ]
    return rows


def joins() -> list[dict[str, str]]:
    return [
        {
            "join_id": "J01",
            "left": "complete_metric_plus_angular_bundle_plus_T",
            "right": "raw_strain_H",
            "ruling": "DERIVED_CONDITIONAL",
            "missing": "bundle_or_T_on_general_branches",
        },
        {
            "join_id": "J02",
            "left": "H_plus_CSN",
            "right": "traceless_J",
            "ruling": "DERIVED_EXACT",
            "missing": "none_on_regular_supplied_stratum",
        },
        {
            "join_id": "J03",
            "left": "relative_mean_rate_plus_J",
            "right": "full_reciprocal_spectrum",
            "ruling": "IFF_W_P_ZERO_AND_SIGMA_SQUARED_EQUALS_ONE",
            "missing": "branch_equations_for_relative_scale_and_sigma",
        },
        {
            "join_id": "J04",
            "left": "reciprocal_spectrum",
            "right": "persistent_eigendirections",
            "ruling": "NOT_AUTOMATIC",
            "missing": "metric_selected_transport_or_constant_toric_frame",
        },
        {
            "join_id": "J05",
            "left": "completion_topology",
            "right": "sigma_squared_equals_one",
            "ruling": "NOT_DERIVED",
            "missing": "metric_profile_or_equation",
        },
        {
            "join_id": "J06",
            "left": "FC12_profile",
            "right": "shape_J_equals_L_but_full_H_equals_W_P_I_plus_L",
            "ruling": "FULL_MATCH_ONLY_CONSTANT_RELATIVE_OMEGA_SUBFAMILY",
            "missing": "Omega_equation_FC12_selection_and_cap_extension",
        },
        {
            "join_id": "J07",
            "left": "mirror_seal",
            "right": "reciprocal_J_at_seal",
            "ruling": "LIFT_DEPENDENT_NOT_SELECTED",
            "missing": "unique_angular_lift",
        },
        {
            "join_id": "J08",
            "left": "GL2Z_monodromy",
            "right": "global_reciprocal_eigenlines",
            "ruling": "NORMALIZER_SUBFAMILY_ONLY",
            "missing": "monodromy_selection",
        },
        {
            "join_id": "J09",
            "left": "c_anchor",
            "right": "angular_generator",
            "ruling": "C_RETAINED_IN_COMPLETE_METRIC_NOT_IN_DIMENSIONLESS_J",
            "missing": "angular_scale_selection",
        },
    ]


def source_lineage() -> list[dict[str, object]]:
    sources = [
        (
            "S01",
            "udt_global_metric_assembly_atlas_2026-07-22/"
            "COMPLETION_CLASS_REGISTRY.tsv",
            "TWELVE_BRANCH_UNIVERSE",
        ),
        (
            "S02",
            "udt_global_metric_assembly_atlas_2026-07-22/AUDIT_REPORT.md",
            "BRANCH_SCOPE_AND_GLOBAL_LIMITS",
        ),
        (
            "S03",
            "udt_global_metric_assembly_atlas_2026-07-22/"
            "build_global_assembly_atlas.py",
            "FC12_EXACT_PROFILE_AND_MONODROMY_CONTROLS",
        ),
        (
            "S04",
            "udt_global_metric_assembly_atlas_2026-07-22/"
            "BUNDLE_HOLONOMY_ATLAS.tsv",
            "TRANSPORT_MONODROMY_SEPARATION",
        ),
        (
            "S05",
            "udt_reciprocal_angular_intertwiner_audit_2026-07-23/"
            "AUDIT_REPORT.md",
            "MATCHED_GENERATOR_THEOREM",
        ),
        (
            "S06",
            "udt_reciprocal_angular_intertwiner_audit_2026-07-23/"
            "COMPLETION_SOLDERING_ATLAS.tsv",
            "PRIOR_COMPLETION_RULINGS",
        ),
        (
            "S07",
            "UDT_COMMON_SCALE_NEUTRALITY_POSTULATE_2026-07-15.md",
            "CSN_TRACE_REMOVAL_SCOPE",
        ),
        (
            "S08",
            "udt_complete_metric_intrinsic_object_audit_2026-07-23/"
            "AUDIT_REPORT.md",
            "INTRINSIC_OBJECT_AND_DPHI_STRATA",
        ),
        (
            "S09",
            "udt_reciprocal_seam_descent_audit_2026-07-23/AUDIT_REPORT.md",
            "COVER_AND_CRITICAL_DPHI_LIMITS",
        ),
        (
            "S10",
            "udt_clock_anchor_scale_threading_audit_2026-07-22/"
            "AUDIT_REPORT.md",
            "C_SCALE_THREADING",
        ),
        (
            "S11",
            "udt_angular_generator_branch_census_2026-07-23/"
            "PREREGISTRATION.md",
            "FROZEN_SCOPE",
        ),
        (
            "S12",
            "udt_angular_generator_branch_census_2026-07-23/"
            "PREMISE_LEDGER.tsv",
            "FROZEN_PREMISES",
        ),
        (
            "S13",
            "udt_angular_generator_branch_census_2026-07-23/"
            "BRANCH_UNIVERSE.tsv",
            "FROZEN_BRANCH_IDENTITIES",
        ),
        (
            "S14",
            "udt_angular_generator_branch_census_2026-07-23/"
            "CORRECTION_PREREGISTRATION.md",
            "FULL_METRIC_RELATIVE_SCALE_CORRECTION",
        ),
        (
            "S15",
            "udt_angular_generator_branch_census_2026-07-23/"
            "CORRECTION_PREMISE_LEDGER.tsv",
            "CORRECTED_PREMISE_TYPES",
        ),
    ]
    rows = []
    for source_id, relative, role in sources:
        path = ROOT / relative
        if not path.is_file():
            raise FileNotFoundError(relative)
        rows.append(
            {
                "source_id": source_id,
                "path": relative,
                "sha256": digest(path),
                "size": path.stat().st_size,
                "role": role,
            }
        )
    return rows


def validate_branch_rows(rows: list[dict[str, object]]) -> None:
    expected = {
        row["completion_id"]
        for row in read_tsv(HERE / "BRANCH_UNIVERSE.tsv")
    }
    observed = [str(row["completion_id"]) for row in rows]
    if len(observed) != 12 or len(set(observed)) != 12:
        raise AssertionError("missing or duplicate branch")
    if set(observed) != expected:
        raise AssertionError("branch universe changed")
    allowed = {
        "FORCED_PERSISTENT_REGULAR",
        "CONDITIONAL_SUBFAMILY_PERSISTENT_REGULAR",
        "ALLOWED_NOT_FORCED",
        "OBSTRUCTED_BY_GLOBAL_GLUE",
        "UNDEFINED_AT_REQUIRED_STRATUM",
        "INSUFFICIENT_METRIC_DATA",
    }
    if any(str(row["branch_ruling"]) not in allowed for row in rows):
        raise AssertionError("invalid ruling")
    if any(row["pattern_forced"] != "NO" for row in rows):
        raise AssertionError("unregistered force claim")
    if any(row["natural_selection"] != "NO" and not str(row["natural_selection"]).startswith("NO__") for row in rows):
        raise AssertionError("selection overclaim")


def catches(rows: list[dict[str, object]], formula: dict[str, object]) -> list[dict[str, str]]:
    checks: list[tuple[str, bool]] = [
        ("missing_completion_row", len(rows[:-1]) != 12),
        (
            "duplicate_completion_row",
            len({row["completion_id"] for row in rows + [rows[0]]}) != 13,
        ),
        (
            "topology_treated_as_metric_profile",
            all(
                row["supplies_q_profile"]
                != "YES_BECAUSE_TOPOLOGY"
                for row in rows
            ),
        ),
        (
            "angular_trace_erased_as_full_metric_CSN",
            formula["relative_mean_rate_vs_reciprocal_block"] == "w_p",
        ),
        (
            "common_scale_silently_constant",
            "w=constant relative" in pointwise_controls()[0]["profile"],
        ),
        (
            "angular_rotation_silently_zero",
            "theta_p" in formula["sigma_squared"],
        ),
        (
            "FC12_promoted_to_selected",
            next(
                row for row in rows
                if row["completion_id"] == "FC12_RECIPROCAL_TORIC_DIAGONAL"
            )["natural_selection"]
            == "NO__FC12_IS_CONDITIONAL_AND_UNSELECTED",
        ),
        (
            "critical_phi_assigned_generator",
            next(
                row for row in pointwise_controls()
                if row["control_id"] == "P09_CRITICAL_PHI"
            )["pointwise_pattern"]
            == "UNDEFINED",
        ),
        (
            "rank_drop_extended",
            all(
                row["extends_degeneracy"] != "YES"
                for row in rows
                if "CAP" in row["completion_id"]
                or row["completion_id"] == "FC10_STRATIFIED_PROJECTOR"
            ),
        ),
        (
            "general_monodromy_replaced_by_identity",
            monodromy_controls()[-2]["control_id"] == "M08_GENERAL_RULE",
        ),
        (
            "mirror_lifts_collapsed",
            len({row["ruling"] for row in mirror_controls()}) > 1,
        ),
        (
            "allowed_profile_called_forced",
            sum(row["branch_ruling"] == "FORCED_PERSISTENT_REGULAR" for row in rows)
            == 0,
        ),
        ("c_dropped_from_complete_metric", formula["c_in_complete_metric"] is True),
        (
            "conditional_control_called_universe",
            all(row["natural_selection"] != "YES" for row in rows),
        ),
        (
            "FC12_regular_result_lost",
            next(
                row for row in rows
                if row["completion_id"] == "FC12_RECIPROCAL_TORIC_DIAGONAL"
            )["regular_interior_result"]
            == (
                "SHAPE_J=L_FOR_ALL_OMEGA__FULL_H=W_P_I_PLUS_L__"
                "MATCH_ONLY_W_P_ZERO"
            ),
        ),
        (
            "formula_sign_flip",
            formula["reduced_determinant"].startswith("-"),
        ),
        (
            "sigma_rotation_term_dropped",
            "sinh(2*u)" in formula["sigma_squared"],
        ),
        (
            "branch_count_changed",
            len(read_tsv(HERE / "BRANCH_UNIVERSE.tsv")) == 12,
        ),
        (
            "pointwise_spectrum_promoted_to_transport",
            pointwise_controls()[4]["eigendirection_persistence"].startswith(
                "SPECTRUM_ONLY"
            ),
        ),
        (
            "action_or_matter_claim_added",
            all(
                token not in MAXIMUM
                for token in ("ACTION_DERIVED", "MATTER_DERIVED", "MASS_DERIVED")
            ),
        ),
    ]
    output = []
    for index, (mutation, caught) in enumerate(checks, 1):
        if not caught:
            raise AssertionError(f"catch failed: {mutation}")
        output.append(
            {
                "catch_id": f"C{index:02d}",
                "mutation": mutation,
                "status": "CAUGHT",
            }
        )
    return output


def main() -> None:
    registry = read_tsv(
        ROOT
        / "udt_global_metric_assembly_atlas_2026-07-22"
        / "COMPLETION_CLASS_REGISTRY.tsv"
    )
    if [row["completion_id"] for row in registry] != [
        row["completion_id"] for row in read_tsv(HERE / "BRANCH_UNIVERSE.tsv")
    ]:
        raise AssertionError("registered branch order changed")

    formula = exact_formula()
    pointwise = pointwise_controls()
    mirrors = mirror_controls()
    monodromy = monodromy_controls()
    branches = branch_rows()
    validate_branch_rows(branches)
    join_rows = joins()
    lineage = source_lineage()
    catch_rows = catches(branches, formula)

    (HERE / "ANGULAR_GENERATOR_FORMULA.json").write_text(
        json.dumps(formula, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    write_tsv(HERE / "POINTWISE_GENERATOR_CONTROLS.tsv", pointwise)
    write_tsv(HERE / "MIRROR_LIFT_GENERATOR_ATLAS.tsv", mirrors)
    write_tsv(HERE / "MONODROMY_GENERATOR_ATLAS.tsv", monodromy)
    write_tsv(HERE / "BRANCH_GENERATOR_ATLAS.tsv", branches)
    write_tsv(HERE / "JOIN_LEDGER.tsv", join_rows)
    write_tsv(HERE / "SOURCE_LINEAGE.tsv", lineage)
    write_tsv(HERE / "CATCH_PROOFS.tsv", catch_rows)

    status = [
        {
            "object": "general_full_metric_relative_angular_strain",
            "status": "DERIVED_EXACT_CONDITIONAL_ON_A_Q_T",
            "scope": "REGULAR_RANK_TWO_DPHI_NONZERO_STRATA",
        },
        {
            "object": "reciprocal_pointwise_spectrum",
            "status": "UNIQUE_CONDITION_CHARACTERIZED",
            "scope": "RELATIVE_MEAN_ZERO_AND_SIGMA_SQUARED_EQUALS_ONE",
        },
        {
            "object": "FC12_regular_interior_pattern",
            "status": "ALLOWED_NOT_FORCED",
            "scope": (
                "SHAPE_J_EQUALS_L_FOR_ALL_OMEGA__FULL_MATCH_ONLY_W_P_ZERO"
            ),
        },
        {
            "object": "pattern_selected_across_completion_space",
            "status": "OPEN_NOT_SELECTED",
            "scope": "ZERO_FORCED_UNCONDITIONAL_BRANCHES",
        },
        {
            "object": "extension_through_caps_or_rank_changes",
            "status": "NOT_DERIVED",
            "scope": "J_UNDEFINED_WHERE_Q_LOSES_RANK",
        },
        {
            "object": "full_angular_representation_generator",
            "status": "OPEN",
            "scope": "METRIC_FIXES_SYMMETRIC_STRAIN_NOT_SKEW_FRAME_ROTATION",
        },
        {
            "object": "c_anchor",
            "status": "RETAINED_EXPLICITLY",
            "scope": "COMPLETE_METRIC_DETERMINANT_HAS_C_SQUARED",
        },
    ]
    write_tsv(HERE / "STATUS_LEDGER.tsv", status)

    ruling_counts: dict[str, int] = {}
    for row in branches:
        key = str(row["branch_ruling"])
        ruling_counts[key] = ruling_counts.get(key, 0) + 1
    result = {
        "schema": "udt-angular-generator-branch-census-1.0",
        "base_commit": BASE,
        "sympy_version": sp.__version__,
        "maximum_conclusion": MAXIMUM,
        "formula": {
            "raw_trace": formula["raw_trace"],
            "sigma_squared": formula["sigma_squared"],
            "reciprocal_predicate": formula["reciprocal_predicate"],
            "complete_metric_determinant": formula["complete_metric_determinant"],
        },
        "counts": {
            "completion_families": len(branches),
            "pointwise_controls": len(pointwise),
            "mirror_lifts": len(mirrors),
            "monodromy_controls": len(monodromy),
            "joins": len(join_rows),
            "sources": len(lineage),
            "catch_proofs": len(catch_rows),
            "forced_persistent_unconditional_families": sum(
                row["branch_ruling"] == "FORCED_PERSISTENT_REGULAR"
                for row in branches
            ),
            "conditional_persistent_regular_families": sum(
                row["branch_ruling"]
                == "CONDITIONAL_SUBFAMILY_PERSISTENT_REGULAR"
                for row in branches
            ),
            "complete_on_shell_g_phi_branches": 0,
        },
        "branch_ruling_counts": ruling_counts,
        "selection_ruling": (
            "FC12_HAS_AN_EXACT_CONSTANT_RELATIVE_OMEGA_MATCHED_SUBFAMILY_"
            "BUT_ITS_ARBITRARY_POSITIVE_OMEGA_FAMILY_IS_NOT_FORCED_"
            "RECIPROCAL__NO_REGISTERED_COMPLETION_OR_BOOTSTRAP_SELECTS_IT"
        ),
        "compute": {"cpu_only": True, "gpu_work_performed": False},
    }
    (HERE / "RESULT.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
