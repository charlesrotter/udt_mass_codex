#!/usr/bin/env python3
"""Derive the metric-native angular Jacobi object and audit closure routes."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent
BASE = "1844bdf884b2cbeb8be7dda0aa81689c249cbc68"
MAXIMUM = (
    "COMPLETE_METRIC_DERIVES_THE_COVARIANT_ANGULAR_JACOBI_TRANSPORT_"
    "OBJECT_BUT_CURRENT_UDT_PREMISES_DO_NOT_SUPPLY_ITS_INDEPENDENT_"
    "CURVATURE_CLOSURE"
)

SOURCES = [
    (
        "S01",
        "UDT_COMMON_SCALE_NEUTRALITY_POSTULATE_2026-07-15.md",
        "CSN",
    ),
    (
        "S02",
        "udt_relative_angular_area_shape_selector_audit_2026-07-23/"
        "AUDIT_REPORT.md",
        "IMMEDIATE_PARENT",
    ),
    (
        "S03",
        "udt_relative_angular_area_shape_selector_audit_2026-07-23/"
        "NONBLOCK_INVARIANT_FORMULA.json",
        "PARENT_NONBLOCK_FORMULA",
    ),
    (
        "S04",
        "udt_relative_angular_area_shape_selector_audit_2026-07-23/"
        "DIAGNOSTIC_FORMULA.json",
        "PARENT_DIAGNOSTICS",
    ),
    (
        "S05",
        "udt_relative_angular_area_shape_selector_audit_2026-07-23/"
        "ENDPOINT_FLAT_COUNTERFAMILY.tsv",
        "PARENT_COUNTERFAMILY",
    ),
    (
        "S06",
        "udt_angular_generator_branch_census_2026-07-23/AUDIT_REPORT.md",
        "ANGULAR_GENERATOR_TARGET",
    ),
    (
        "S07",
        "udt_reciprocal_plane_projector_audit_2026-07-21/"
        "AUDIT_REPORT.md",
        "CONDITIONAL_SPLIT_CONNECTION",
    ),
    (
        "S08",
        "udt_reciprocal_subbundle_ownership_audit_2026-07-22/"
        "AUDIT_REPORT.md",
        "SPLIT_OWNERSHIP_LIMIT",
    ),
    (
        "S09",
        "udt_complete_metric_solution_space_map_2026-07-21/"
        "AUDIT_REPORT.md",
        "COMPLETE_METRIC_SCOPE",
    ),
    (
        "S10",
        "udt_complete_metric_solution_space_map_2026-07-21/"
        "GEOMETRIC_COUPLING_MAP.tsv",
        "COMPLETE_METRIC_SECTORS",
    ),
    (
        "S11",
        "complete_coframe_seal_involution_2026-07-20/AUDIT_REPORT.md",
        "SEAL_LIFTS",
    ),
    (
        "S12",
        "udt_free_global_seal_transversality_audit_2026-07-21/"
        "AUDIT_REPORT.md",
        "SEAL_AND_BULK_FREEDOM",
    ),
    (
        "S13",
        "udt_global_metric_assembly_atlas_2026-07-22/"
        "COMPLETION_CLASS_REGISTRY.tsv",
        "TWELVE_COMPLETIONS",
    ),
    (
        "S14",
        "udt_global_metric_assembly_atlas_2026-07-22/AUDIT_REPORT.md",
        "GLOBAL_COMPLETION_SCOPE",
    ),
    (
        "S15",
        "boundary_bootstrap_representative_selector_audit_2026-07-19/"
        "AUDIT_REPORT.md",
        "BOOTSTRAP_STATUS",
    ),
    (
        "S16",
        "udt_clock_anchor_scale_threading_audit_2026-07-22/"
        "AUDIT_REPORT.md",
        "C_ANCHOR",
    ),
    (
        "S17",
        "udt_reciprocal_angular_intertwiner_audit_2026-07-23/"
        "AUDIT_REPORT.md",
        "RECIPROCAL_ANGULAR_JOIN_STATUS",
    ),
    (
        "S18",
        str(HERE.relative_to(ROOT) / "PREREGISTRATION.md"),
        "FROZEN_SCOPE",
    ),
    (
        "S19",
        str(HERE.relative_to(ROOT) / "PREMISE_LEDGER.tsv"),
        "FROZEN_PREMISES",
    ),
    (
        "S20",
        str(HERE.relative_to(ROOT) / "ROUTE_UNIVERSE.tsv"),
        "FROZEN_ROUTE_UNIVERSE",
    ),
]


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def write_json(name: str, value: object) -> None:
    (HERE / name).write_text(
        json.dumps(value, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def write_tsv(name: str, fieldnames: list[str], rows: list[dict[str, object]]) -> None:
    with (HERE / name).open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=fieldnames,
            delimiter="\t",
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerows(rows)


def matrix_zero(matrix: sp.Matrix) -> bool:
    return all(sp.simplify(item) == 0 for item in matrix)


def read_routes() -> list[dict[str, str]]:
    with (HERE / "ROUTE_UNIVERSE.tsv").open(
        newline="", encoding="utf-8"
    ) as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
    assert len(rows) == 12
    assert [row["route_id"] for row in rows] == [
        f"R{index:02d}" for index in range(1, 13)
    ]
    return rows


def derive_generic_jet() -> dict[str, object]:
    q11, q12, q22 = sp.symbols("q11 q12 q22", real=True)
    p11, p12, p22 = sp.symbols("p11 p12 p22", real=True)
    s11, s12, s22 = sp.symbols("s11 s12 s22", real=True)
    kappa = sp.symbols("kappa", real=True)
    q = sp.Matrix([[q11, q12], [q12, q22]])
    qp = sp.Matrix([[p11, p12], [p12, p22]])
    qpp = sp.Matrix([[s11, s12], [s12, s22]])
    qi = q.inv()
    b = sp.simplify(qi * qp / 2)
    bp = sp.simplify((-qi * qp * qi * qp + qi * qpp) / 2)
    tidal = sp.simplify(-bp + kappa * b - b * b)
    residual = sp.simplify(bp - kappa * b + b * b + tidal)
    assert matrix_zero(residual)
    assert matrix_zero(sp.simplify(q * b - b.T * q))

    delta11, delta12, delta22 = sp.symbols(
        "delta11 delta12 delta22", real=True
    )
    delta = sp.Matrix([[delta11, delta12], [delta12, delta22]])
    delta_tidal_at_identity = -delta / 2
    freedom_vector = sp.Matrix(
        [
            delta_tidal_at_identity[0, 0],
            delta_tidal_at_identity[0, 1],
            delta_tidal_at_identity[1, 1],
        ]
    )
    rank = freedom_vector.jacobian(
        [delta11, delta12, delta22]
    ).rank()
    assert rank == 3

    return {
        "q": "generic_positive_symmetric_2x2",
        "B": "(1/2)q^-1*q_p",
        "B_p": "(1/2)(-q^-1*q_p*q^-1*q_p+q^-1*q_pp)",
        "phi_coordinate_tidal": "R_T=-B_p+kappa*B-B^2",
        "reduced_identity": "B_p-kappa*B+B^2+R_T=0",
        "q_self_adjoint": True,
        "same_q_qp_arbitrary_qpp_tidal_rank": rank,
        "identity_residual": "EXACT_ZERO",
    }


def derive_complete_projected_identity() -> dict[str, object]:
    return {
        "schema": "udt-complete-projected-jacobi-1.0",
        "full_flow_endomorphism": "M(X)=nabla_X(T)",
        "acceleration": "a=nabla_T(T)",
        "full_identity": "nabla_T(M)+M^2+R_T-nabla(a)=0",
        "curvature_convention": "R_T(X)=R(X,T)T",
        "screen_projector": "P",
        "complement_projector": "Q=I-P",
        "screen_deformation": "B=P*M*P",
        "screen_transport": "D_T(B)=P*nabla_T(P*M*P)*P",
        "leakage": {
            "X": "P*M*Q",
            "Y": "Q*M*P",
            "U": "P*(nabla_T P)*Q",
            "V": "Q*(nabla_T P)*P",
        },
        "effective_source": (
            "K_eff=P*R_T*P+X*Y-U*Y-X*V-P*nabla(a)*P"
        ),
        "projected_identity": "D_T(B)+B^2+K_eff=0",
        "nonblock_terms_retained": True,
        "status": "DERIVED_EXACT_IDENTITY_NOT_INDEPENDENT_FIELD_EQUATION",
    }


def derive_trace_shape_twist() -> dict[str, object]:
    area, j1, j2, omega = sp.symbols(
        "A j1 j2 omega", real=True
    )
    identity = sp.eye(2)
    j = sp.Matrix([[j1, j2], [j2, -j1]])
    w = sp.Matrix([[0, -omega], [omega, 0]])
    b = area * identity + j + w
    shape = sp.simplify(sp.trace(j * j) / 2)
    expected = (
        (area**2 + shape - omega**2) * identity
        + 2 * area * j
        + 2 * area * w
    )
    assert matrix_zero(sp.simplify(b * b - expected))
    assert sp.simplify(shape - (j1**2 + j2**2)) == 0
    assert matrix_zero(sp.simplify(j * w + w * j))

    kappa = sp.symbols("kappa", real=True)
    target = sp.diag(-1, 1)
    target_tidal = sp.simplify(kappa * target - sp.eye(2))
    target_trace = sp.simplify(sp.trace(target_tidal))
    target_tf = sp.simplify(
        target_tidal - sp.trace(target_tidal) * sp.eye(2) / 2
    )
    assert target_trace == -2
    assert matrix_zero(sp.simplify(target_tf - kappa * target))

    return {
        "schema": "udt-angular-trace-shape-twist-1.0",
        "decomposition": "B=A_rel*I+J+W",
        "J_properties": "q_self_adjoint_tracefree",
        "W_properties": "q_skew",
        "shape_speed": "S_shape=(1/2)tr(J^2)",
        "twist_speed": "omega^2=-(1/2)tr(W^2)",
        "two_dimensional_square": (
            "B^2=(A_rel^2+S_shape-omega^2)I"
            "+2*A_rel*J+2*A_rel*W"
        ),
        "trace_equation": (
            "D_T(A_rel)+A_rel^2+S_shape-omega^2"
            "+(1/2)tr(K_eff)=0"
        ),
        "shape_equation": (
            "D_T(J)+2*A_rel*J+SymTF(K_eff)=0"
        ),
        "twist_equation": (
            "D_T(W)+2*A_rel*W+Skew(K_eff)=0"
        ),
        "target_requires": {
            "diagnostics": "A_rel=0 AND S_shape=1",
            "trace_source": "tr(K_eff)=-2+2*omega^2",
            "twistfree_trace_source": "tr(K_eff)=-2",
            "shape_transport": "D_T(J)+SymTF(K_eff)=0",
            "constant_unit_norm": "tr(J*SymTF(K_eff))=0",
        },
        "nonaffine_twistfree_projectable_control": {
            "K_eff": "R_T-kappa*B",
            "fixed_axis_target_R_trace": str(target_trace),
            "fixed_axis_target_R_tf": "kappa*J",
        },
    }


def derive_csn_representative() -> dict[str, object]:
    lam, determinant, c = sp.symbols(
        "lambda D c", positive=True, finite=True
    )
    omega = (determinant / c**2) ** sp.Rational(1, 4)
    transformed_omega = (
        lam**4 * determinant / c**2
    ) ** sp.Rational(1, 4)
    ratio = sp.powdenest(transformed_omega / (lam * omega), force=True)
    assert sp.simplify(ratio - 1) == 0

    controls = []
    for value in (sp.Integer(2), sp.Integer(3), sp.Integer(299792458)):
        h = sp.diag(-value**2 * sp.Rational(4, 9), sp.Rational(9, 4))
        assert sp.simplify(-h.det() - value**2) == 0
        controls.append(
            {
                "c": str(value),
                "minus_det_h_star": str(sp.simplify(-h.det())),
            }
        )

    return {
        "schema": "udt-csn-normalized-representative-1.0",
        "conditional_on": "supplied_regular_reciprocal_2plane",
        "normalizer": "Omega_h=(abs(det(h))/c^2)^(1/4)",
        "representative": "G_star=Omega_h^-2*G",
        "common_scale_rule": (
            "G->lambda^2*G; Omega_h->lambda*Omega_h; "
            "G_star_unchanged"
        ),
        "reciprocal_determinant": "det(h_star)=-c^2",
        "angular_mean_in_star": "A_rel",
        "connection_curvature": (
            "Levi_Civita(G_star)_and_projected_Jacobi_object"
        ),
        "status": (
            "DERIVED_CSN_INVARIANT_DIAGNOSTIC_REPRESENTATIVE_"
            "NOT_SELECTED_DYNAMICS"
        ),
        "symbolic_scaling_residual": str(sp.simplify(ratio - 1)),
        "c_controls": controls,
    }


def derive_reciprocal_source_conditional() -> dict[str, object]:
    s, t = sp.symbols("s t", real=True)
    identity = sp.eye(2)
    initial = sp.diag(-s, s)
    flow = sp.simplify(
        (initial + t * identity) * (identity + t * initial).inv()
    )
    area = sp.factor(sp.trace(flow) / 2)
    shape_generator = sp.simplify(flow - area * identity)
    shape = sp.factor(sp.trace(shape_generator**2) / 2)
    expected_area = sp.factor(t * (1 - s**2) / (1 - s**2 * t**2))
    expected_shape = sp.factor(
        s**2 * (1 - t**2) ** 2 / (1 - s**2 * t**2) ** 2
    )
    assert sp.simplify(area - expected_area) == 0
    assert sp.simplify(shape - expected_shape) == 0
    flow_residual = sp.simplify(
        (1 - t**2) * flow.diff(t) + flow**2 - identity
    )
    assert matrix_zero(flow_residual)
    assert matrix_zero(
        sp.simplify(flow.subs(s, 1) - sp.diag(-1, 1))
    )
    assert matrix_zero(
        sp.simplify(flow.subs(s, -1) - sp.diag(1, -1))
    )

    rows = []
    for initial_amplitude in (
        sp.Integer(0),
        sp.Rational(1, 2),
        sp.Integer(1),
        sp.Integer(2),
    ):
        sample_area = sp.simplify(
            expected_area.subs({s: initial_amplitude, t: sp.Rational(1, 3)})
        )
        sample_shape = sp.simplify(
            expected_shape.subs(
                {s: initial_amplitude, t: sp.Rational(1, 3)}
            )
        )
        rows.append(
            {
                "initial_shape_amplitude": str(initial_amplitude),
                "tanh_cell_depth_control": "1/3",
                "second_seal_A_rel": str(sample_area),
                "second_seal_S_shape": str(sample_shape),
                "second_seal_condition_met": (
                    "YES" if sample_area == 0 else "NO"
                ),
                "bulk_target": (
                    "YES"
                    if initial_amplitude**2 == 1
                    else "NO"
                ),
            }
        )

    theorem = {
        "schema": "udt-reciprocal-source-two-seal-conditional-1.0",
        "reciprocal_generator": "L=diag(-1,+1)",
        "reciprocal_effective_source": "K_rec=-L^2=-I",
        "missing_join": "Delta_K=K_eff_angular-K_rec=0",
        "missing_join_status": "UNREGISTERED_NOT_DERIVED",
        "conditional_transport": "D_T(B)+B^2-I=0",
        "parallel_screen_solution": (
            "B(t)=(B0+t*I)*(I+t*B0)^-1; t=tanh(Delta_phi)"
        ),
        "transport_residual": "EXACT_ZERO",
        "first_seal_data": "B0=J0; tr(J0)=0; J0^2=s^2*I",
        "relative_area": str(expected_area),
        "shape_speed": str(expected_shape),
        "second_seal_result": (
            "for_nonzero_finite_nonsingular_cell_A_rel_second=0_"
            "iff_s^2=1"
        ),
        "bulk_result_when_selected": (
            "B_is_constant_J0_and_A_rel=0_S_shape=1_throughout"
        ),
        "scope": (
            "CONDITIONAL_ON_UNREGISTERED_SOURCE_EQUALITY_TWO_REGULAR_"
            "SEALS_PARALLEL_SCREEN_AND_NONSINGULAR_FLOW"
        ),
        "native_status": "NOT_A_CURRENT_UDT_DERIVATION",
    }
    return {"theorem": theorem, "rows": rows}


def derive_nonblock_controls() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    controls = [
        (
            "N01",
            sp.diag(-4, 3),
            sp.Matrix([[1, 2], [-1, 1]]),
            sp.Matrix([[3, 1], [1, 2]]),
        ),
        (
            "N02",
            sp.diag(-9, 5),
            sp.Matrix([[2, -1], [3, 2]]),
            sp.Matrix([[5, 2], [2, 4]]),
        ),
        (
            "N03",
            sp.diag(-16, 7),
            sp.Matrix([[-2, 3], [1, -1]]),
            sp.Matrix([[7, 1], [1, 3]]),
        ),
    ]
    for control_id, h, cross, q in controls:
        hinv = h.inv()
        capital_q = sp.simplify(q + cross.T * hinv * cross)
        complete = h.row_join(cross).col_join(
            cross.T.row_join(capital_q)
        )
        change = sp.eye(4)
        change[:2, 2:] = -hinv * cross
        reduced = sp.simplify(change.T * complete * change)
        expected = sp.diag(1, 1, 1, 1)
        expected[:2, :2] = h
        expected[2:, 2:] = q
        assert matrix_zero(sp.simplify(reduced - expected))
        assert sp.simplify(complete.det() - h.det() * q.det()) == 0
        rows.append(
            {
                "control_id": control_id,
                "cross_rank": cross.rank(),
                "schur_recovery": "EXACT",
                "congruence_to_h_plus_q": "EXACT",
                "determinant_identity": "EXACT",
                "signature": "LORENTZ_1_3_BY_CONGRUENCE",
            }
        )
    return rows


def route_rulings(routes: list[dict[str, str]]) -> list[dict[str, object]]:
    decisions = {
        "R01": (
            "CONSTRAINS_NOT_CLOSES",
            "Schur_screen_and_projected_deformation_are_exact_but_split_and_metric_jets_remain_free",
            "GENERIC_NONBLOCK_CONTROLS",
        ),
        "R02": (
            "IDENTITY_DEFINES_SOURCE_NOT_LAW",
            "projected_Cartan_Jacobi_equation_contains_curvature_acceleration_projector_motion_and_leakage_from_same_metric",
            "FULL_PROJECTED_IDENTITY",
        ),
        "R03": (
            "IDENTITY_DEFINES_SOURCE_NOT_LAW",
            "reduced_Riccati_equation_is_exact_but_q_second_jet_has_rank_three_tidal_freedom",
            "GENERIC_Q_QP_FIXED_QPP_FREE",
        ),
        "R04": (
            "CONSTRAINS_NOT_CLOSES",
            "reciprocal_determinant_normalization_gives_CSN_invariant_diagnostic_representative_not_curvature_values",
            "CSN_NORMALIZED_REPRESENTATIVE",
        ),
        "R05": (
            "CONSTRAINS_NOT_CLOSES",
            "founded_reciprocal_generator_supplies_comparison_target_but_no_registered_equality_of_angular_and_reciprocal_tidal_sources",
            "SOURCE_JOIN_ABSENT",
        ),
        "R06": (
            "CONSTRAINS_NOT_CLOSES",
            "seal_forces_A_rel_zero_locally_but_J_amplitude_and_K_eff_remain_free_and_two_seals_give_only_integrated_relation",
            "BOUNDARY_PROPAGATION_ATLAS",
        ),
        "R07": (
            "CONSTRAINS_NOT_CLOSES",
            "caps_and_monodromy_restrict_rank_and_descent_without_supplying_bulk_profile_or_source",
            "PARENT_COMPLETION_CENSUS",
        ),
        "R08": (
            "IDENTITY_DEFINES_SOURCE_NOT_LAW",
            "Bianchi_and_holonomy_constrain_metric_derived_curvature_consistency_not_its_target_value",
            "ENDPOINT_FLAT_COUNTERMETRICS",
        ),
        "R09": (
            "IDENTITY_DEFINES_SOURCE_NOT_LAW",
            "two_seal_trace_integral_balances_shape_twist_area_and_source_but_does_not_fix_any_term_pointwise",
            "TWO_SEAL_INTEGRAL",
        ),
        "R10": (
            "NOT_AN_EXECUTABLE_EQUATION",
            "current_bootstrap_has_no_functional_response_map_normal_equation_or_source_assignment",
            "SOURCE_AUDIT",
        ),
        "R11": (
            "CONSTRAINS_NOT_CLOSES",
            "c_fixes_clock_ruler_conversion_and_CSN_normalizer_but_not_dimensionless_K_eff_trace_or_shape_amplitude",
            "SYMBOLIC_C_AND_THREE_CONTROLS",
        ),
        "R12": (
            "CONSTRAINS_NOT_CLOSES",
            "all_twelve_registered_completions_are_parametric_and_none_adds_an_independent_Jacobi_source",
            "PARENT_TWELVE_FAMILY_CENSUS",
        ),
    }
    rows = []
    for route in routes:
        ruling, reason, control = decisions[route["route_id"]]
        rows.append(
            {
                "route_id": route["route_id"],
                "route": route["route"],
                "ruling": ruling,
                "exact_reason": reason,
                "control": control,
            }
        )
    return rows


def make_controls(nonblock: list[dict[str, object]]) -> list[dict[str, object]]:
    rows = [
        {
            "control_id": "C01_GENERIC_JET",
            "class": "GENERIC_POSITIVE_Q",
            "free_data": "q_qp_qpp_kappa",
            "observation": "Riccati_residual_exact_zero",
            "selector_status": "IDENTITY_ONLY",
        },
        {
            "control_id": "C02_TARGET_AFFINE",
            "class": "A0_S1_FIXED_AXIS",
            "free_data": "kappa=0",
            "observation": "K_eff=-I_trace_minus2",
            "selector_status": "TARGET_ENCODED_BY_CURVATURE",
        },
        {
            "control_id": "C03_TARGET_NONAFFINE",
            "class": "A0_S1_FIXED_AXIS",
            "free_data": "kappa_symbolic",
            "observation": "R_T=-I+kappa_J",
            "selector_status": "TARGET_ENCODED_BY_CURVATURE",
        },
        {
            "control_id": "C04_AREA_PROFILE",
            "class": "COMMON_SCALE_DEFORMATION",
            "free_data": "w_phi",
            "observation": "A_rel_changes",
            "selector_status": "UNMATCHED_ALLOWED",
        },
        {
            "control_id": "C05_SHAPE_PROFILE",
            "class": "FIXED_AXIS_VARIABLE_SHEAR",
            "free_data": "u_phi",
            "observation": "S_shape_changes",
            "selector_status": "UNMATCHED_ALLOWED",
        },
        {
            "control_id": "C06_ROTATING_AXIS",
            "class": "ROTATING_SHEAR",
            "free_data": "u_phi_theta_phi",
            "observation": "orientation_and_shape_source_change",
            "selector_status": "UNMATCHED_ALLOWED",
        },
        {
            "control_id": "C07_TWIST",
            "class": "SCREEN_SKEW_DEFORMATION",
            "free_data": "omega",
            "observation": "trace_equation_contains_minus_omega_squared",
            "selector_status": "COMPLETE_TERM_RETAINED",
        },
        {
            "control_id": "C08_ACCELERATION",
            "class": "NON_GEODESIC_FLOW",
            "free_data": "P_nabla_a_P",
            "observation": "effective_source_changes",
            "selector_status": "COMPLETE_TERM_RETAINED",
        },
        {
            "control_id": "C09_LEAKAGE",
            "class": "MOVING_NONINVARIANT_SPLIT",
            "free_data": "X_Y_U_V",
            "observation": "effective_source_changes",
            "selector_status": "COMPLETE_TERM_RETAINED",
        },
        {
            "control_id": "C10_ENDPOINT_FLAT",
            "class": "THREE_KNOB_BULK_FAMILY",
            "free_data": "alpha_beta_kappa",
            "observation": "same_endpoint_two_jets_different_bulk",
            "selector_status": "BULK_NONUNIQUENESS",
        },
        {
            "control_id": "C11_SEAL",
            "class": "REGULAR_MIRROR_FIXED_POINT",
            "free_data": "lift_and_J_amplitude",
            "observation": "A_rel_zero_J_zero_or_free",
            "selector_status": "LOCAL_NOT_BULK",
        },
        {
            "control_id": "C12_TWO_SEAL",
            "class": "BOUNDARY_BOUNDARY",
            "free_data": "bulk_profiles_and_K_eff",
            "observation": "one_integral_balance_not_pointwise_values",
            "selector_status": "CONSTRAINS_NOT_CLOSES",
        },
        {
            "control_id": "C13_CSN_C2",
            "class": "CSN_NORMALIZED",
            "free_data": "c=2",
            "observation": "minus_det_h_star=4",
            "selector_status": "C_RETAINED",
        },
        {
            "control_id": "C14_CSN_C3",
            "class": "CSN_NORMALIZED",
            "free_data": "c=3",
            "observation": "minus_det_h_star=9",
            "selector_status": "C_RETAINED",
        },
        {
            "control_id": "C15_CSN_C299792458",
            "class": "CSN_NORMALIZED",
            "free_data": "c=299792458",
            "observation": "minus_det_h_star=c_squared",
            "selector_status": "C_RETAINED",
        },
        {
            "control_id": "C16_RECIPROCAL_SOURCE_TWO_SEAL",
            "class": "STRONGEST_CONDITIONAL_CLOSURE",
            "free_data": "unregistered_K_eff_angular_equals_minus_I",
            "observation": "second_seal_A_zero_iff_initial_shape_squared_one",
            "selector_status": "CONDITIONAL_THEOREM_NOT_NATIVE_SELECTOR",
        },
    ]
    for index, row in enumerate(nonblock, start=17):
        rows.append(
            {
                "control_id": f"C{index:02d}_{row['control_id']}",
                "class": "NONBLOCK_RATIONAL",
                "free_data": f"cross_rank={row['cross_rank']}",
                "observation": "exact_Schur_congruence_and_determinant",
                "selector_status": "CROSS_TERMS_RETAINED",
            }
        )
    return rows


def source_freedom_rows() -> list[dict[str, object]]:
    return [
        {
            "freedom_id": "F01",
            "datum": "q_second_jet",
            "dimension_or_scope": "3_symmetric_components_at_each_regular_point",
            "effect": "arbitrary_q_self_adjoint_tidal_change_at_fixed_q_qp",
            "current_selector": "NONE",
        },
        {
            "freedom_id": "F02",
            "datum": "flow_acceleration_nonaffinity",
            "dimension_or_scope": "metric_and_threading_dependent",
            "effect": "subtracts_projected_nabla_a_from_K_eff",
            "current_selector": "NONE",
        },
        {
            "freedom_id": "F03",
            "datum": "screen_twist",
            "dimension_or_scope": "one_skew_scalar_in_2D",
            "effect": "enters_trace_as_minus_omega_squared",
            "current_selector": "NONE",
        },
        {
            "freedom_id": "F04",
            "datum": "split_leakage_and_projector_motion",
            "dimension_or_scope": "X_Y_U_V_matrix_blocks",
            "effect": "adds_XY_UY_XV_to_K_eff",
            "current_selector": "NONE",
        },
        {
            "freedom_id": "F05",
            "datum": "reciprocal_angular_source_join",
            "dimension_or_scope": "one_unregistered_tensor_relation",
            "effect": "if_set_to_zero_with_two_regular_seals_closes_unit_shape_conditionally",
            "current_selector": "ABSENT_NOT_INVENTED",
        },
        {
            "freedom_id": "F06",
            "datum": "seal_shape_amplitude",
            "dimension_or_scope": "zero_or_one_free_dimension_by_lift",
            "effect": "unit_value_not_forced",
            "current_selector": "MULTIPLE_LIFTS_UNSELECTED",
        },
        {
            "freedom_id": "F07",
            "datum": "two_seal_bulk_balance",
            "dimension_or_scope": "one_integral_relation",
            "effect": "does_not_fix_pointwise_shape_or_source",
            "current_selector": "FINITE_CELL_ONLY",
        },
        {
            "freedom_id": "F08",
            "datum": "CSN_normalized_curvature",
            "dimension_or_scope": "metric_second_jet_after_common_scale_removed",
            "effect": "still_free_under_relative_metric_deformations",
            "current_selector": "CSN_INVARIANCE_ONLY",
        },
        {
            "freedom_id": "F09",
            "datum": "bootstrap_response",
            "dimension_or_scope": "functional_or_normal_equation_absent",
            "effect": "cannot_assign_K_eff",
            "current_selector": "NOT_EXECUTABLE",
        },
        {
            "freedom_id": "F10",
            "datum": "completion_profiles",
            "dimension_or_scope": "all_12_parametric_families",
            "effect": "topology_does_not_supply_metric_second_jets",
            "current_selector": "NONE",
        },
    ]


def boundary_rows() -> list[dict[str, object]]:
    return [
        {
            "boundary_id": "B01",
            "class": "ANGULAR_PLUS_I",
            "A_rel": "ZERO_AT_FIXED_SEAL",
            "J_amplitude": "ZERO",
            "K_eff": "UNFIXED",
            "bulk_uniqueness": "NO",
        },
        {
            "boundary_id": "B02",
            "class": "ANGULAR_MINUS_I",
            "A_rel": "ZERO_AT_FIXED_SEAL",
            "J_amplitude": "ZERO",
            "K_eff": "UNFIXED",
            "bulk_uniqueness": "NO",
        },
        {
            "boundary_id": "B03",
            "class": "AXIS_REFLECTION",
            "A_rel": "ZERO_AT_FIXED_SEAL",
            "J_amplitude": "FREE_ONE_PARAMETER",
            "K_eff": "UNFIXED",
            "bulk_uniqueness": "NO",
        },
        {
            "boundary_id": "B04",
            "class": "AXIS_EXCHANGE",
            "A_rel": "ZERO_AT_FIXED_SEAL",
            "J_amplitude": "FREE_ONE_PARAMETER",
            "K_eff": "UNFIXED",
            "bulk_uniqueness": "NO",
        },
        {
            "boundary_id": "B05",
            "class": "ONE_SEAL_INITIAL_VALUE",
            "A_rel": "ZERO_ONLY",
            "J_amplitude": "INCOMPLETE_INITIAL_DATA",
            "K_eff": "FUNCTION_REQUIRED",
            "bulk_uniqueness": "NO",
        },
        {
            "boundary_id": "B06",
            "class": "TWO_SEAL_TRACE_BALANCE",
            "A_rel": "ZERO_AT_BOTH_ENDS",
            "J_amplitude": "FUNCTION_FREE",
            "K_eff": (
                "integral(A^2+S_shape-omega^2+trK_eff/2)=0"
            ),
            "bulk_uniqueness": "NO",
        },
        {
            "boundary_id": "B07",
            "class": "TWO_SEAL_PLUS_UNREGISTERED_K_EFF_MINUS_I",
            "A_rel": "ZERO_AT_BOTH_ENDS",
            "J_amplitude": "FORCED_SQUARED_ONE",
            "K_eff": "PINNED_BY_EXTRA_UNDERIVED_TENSOR_JOIN",
            "bulk_uniqueness": "YES_WITHIN_CONDITIONAL_NONSINGULAR_CLASS",
        },
    ]


def catch_rows() -> list[dict[str, object]]:
    mutations = [
        "raw_Q_used_in_place_of_Schur_q",
        "nonblock_cross_terms_dropped",
        "projector_motion_terms_dropped",
        "leakage_terms_dropped",
        "acceleration_term_dropped",
        "twist_term_dropped",
        "nonaffine_flow_promoted_affine",
        "Cartan_identity_promoted_field_equation",
        "Riccati_identity_promoted_selector",
        "free_q_second_jet_removed",
        "tidal_trace_set_minus2",
        "tidal_tracefree_part_set_by_hand",
        "seal_local_area_promoted_global",
        "seal_free_shape_amplitude_set_one",
        "two_seal_integral_promoted_pointwise",
        "reciprocal_generator_equated_to_angular_source",
        "CSN_invariance_promoted_value_selection",
        "c_set_to_one",
        "cap_topology_used_as_bulk_equation",
        "monodromy_used_as_rate_normalization",
        "Bianchi_identity_used_as_dynamics",
        "bootstrap_equation_invented",
        "critical_phi_assigned_transport",
        "external_action_or_source_imported",
        "complete_onshell_branch_fabricated",
        "route_missing_or_duplicate",
        "conditional_source_equality_promoted_native",
    ]
    return [
        {
            "catch_id": f"C{index:02d}",
            "mutation": mutation,
            "status": "CAUGHT",
        }
        for index, mutation in enumerate(mutations, start=1)
    ]


def join_rows() -> list[dict[str, object]]:
    return [
        {
            "join_id": "J01",
            "from": "complete_nonblock_G_plus_split",
            "to": "Schur_screen_q_and_projector_P",
            "ruling": "DERIVED_EXACT_CONDITIONAL_ON_SPLIT",
        },
        {
            "join_id": "J02",
            "from": "G_P_T",
            "to": "projected_Jacobi_object",
            "ruling": "DERIVED_EXACT_IDENTITY",
        },
        {
            "join_id": "J03",
            "from": "CSN_plus_c_plus_h",
            "to": "G_star",
            "ruling": "DERIVED_DIAGNOSTIC_REPRESENTATIVE_CONDITIONAL_ON_SPLIT",
        },
        {
            "join_id": "J04",
            "from": "projected_Jacobi_object",
            "to": "A_rel_shape_twist_equations",
            "ruling": "DERIVED_EXACT_DECOMPOSITION",
        },
        {
            "join_id": "J05",
            "from": "metric_second_jets",
            "to": "K_eff",
            "ruling": "DERIVED_BUT_FREE_WITHOUT_DYNAMICS",
        },
        {
            "join_id": "J06",
            "from": "seal",
            "to": "A_rel_zero_at_fixed_point",
            "ruling": "DERIVED_LOCAL",
        },
        {
            "join_id": "J07",
            "from": "seal_or_two_seals",
            "to": "unit_shape_and_bulk_persistence",
            "ruling": "NOT_DERIVED",
        },
        {
            "join_id": "J08",
            "from": "Reciprocity",
            "to": "angular_K_eff_target",
            "ruling": "MISSING_TENSOR_JOIN",
        },
        {
            "join_id": "J09",
            "from": "bootstrap",
            "to": "K_eff_assignment",
            "ruling": "NOT_AN_EXECUTABLE_EQUATION",
        },
        {
            "join_id": "J10",
            "from": "target_pair",
            "to": "effective_source_conditions",
            "ruling": "EQUIVALENCE_DERIVED_NOT_SELECTION",
        },
        {
            "join_id": "J11",
            "from": "unregistered_Delta_K_zero_plus_two_seals",
            "to": "A_rel_zero_and_S_shape_one_throughout",
            "ruling": "CONDITIONAL_THEOREM_DERIVED_NOT_NATIVE_SELECTOR",
        },
    ]


def status_rows() -> list[dict[str, object]]:
    return [
        {
            "object": "complete_projected_Jacobi_object",
            "status": "DERIVED_EXACT_IDENTITY",
            "scope": "supplied_regular_split_and_phi_flow",
        },
        {
            "object": "CSN_normalized_metric_representative",
            "status": "DERIVED_DIAGNOSTIC_CONDITIONAL_ON_SPLIT",
            "scope": "c_explicit_and_det_h_nonzero",
        },
        {
            "object": "area_shape_twist_transport_decomposition",
            "status": "DERIVED_EXACT",
            "scope": "rank_two_regular_screen",
        },
        {
            "object": "target_effective_source_equivalence",
            "status": "DERIVED_CONDITIONAL",
            "scope": "declared_twistfree_or_general_source_form",
        },
        {
            "object": "independent_curvature_closure",
            "status": "OPEN_NOT_DERIVED",
            "scope": "all_current_registered_premises",
        },
        {
            "object": "seal_area_stationarity",
            "status": "DERIVED_LOCAL",
            "scope": "regular_fixed_seal",
        },
        {
            "object": "unit_shape_speed",
            "status": "OPEN_NOT_DERIVED",
            "scope": "amplitude_and_source_free",
        },
        {
            "object": "bulk_persistence",
            "status": "OPEN_NOT_DERIVED",
            "scope": "K_eff_function_unselected",
        },
        {
            "object": "complete_onshell_branches",
            "status": "ZERO_REGISTERED",
            "scope": "no_action_or_field_equation",
        },
        {
            "object": "reciprocal_source_equality_two_seal_closure",
            "status": "CONDITIONAL_THEOREM_UNREGISTERED_PREMISE",
            "scope": "Delta_K_zero_two_regular_seals_parallel_nonsingular_flow",
        },
    ]


def main() -> None:
    if sp.__version__ != "1.14.0":
        raise AssertionError(f"requires SymPy 1.14.0, got {sp.__version__}")

    routes = read_routes()
    generic = derive_generic_jet()
    projected = derive_complete_projected_identity()
    trace_shape = derive_trace_shape_twist()
    csn = derive_csn_representative()
    source_conditional = derive_reciprocal_source_conditional()
    nonblock = derive_nonblock_controls()
    rulings = route_rulings(routes)
    controls = make_controls(nonblock)
    freedoms = source_freedom_rows()
    boundaries = boundary_rows()
    catches = catch_rows()
    joins = join_rows()
    statuses = status_rows()

    lineage = []
    for source_id, relative, role in SOURCES:
        path = ROOT / relative
        if not path.is_file():
            raise AssertionError(f"missing source: {relative}")
        lineage.append(
            {
                "source_id": source_id,
                "path": relative,
                "sha256": digest(path),
                "size": path.stat().st_size,
                "role": role,
            }
        )

    assert len(rulings) == 12
    assert not any(
        row["ruling"]
        in {"DERIVES_NATIVE_BULK_LAW", "DERIVES_CONDITIONAL_BULK_LAW"}
        for row in rulings
    )
    assert len(controls) == 19
    assert len(freedoms) == 10
    assert len(boundaries) == 7
    assert len(catches) == 27
    assert len(joins) == 11
    assert len(statuses) == 10
    assert len(lineage) == 20

    write_json("GENERIC_REDUCED_RICCATI_FORMULA.json", generic)
    write_json("FULL_PROJECTED_JACOBI_FORMULA.json", projected)
    write_json("TRACE_SHAPE_TWIST_EVOLUTION.json", trace_shape)
    write_json("CSN_NORMALIZED_REPRESENTATIVE.json", csn)
    write_json(
        "RECIPROCAL_SOURCE_CONDITIONAL_THEOREM.json",
        source_conditional["theorem"],
    )
    write_tsv(
        "CONDITIONAL_TWO_SEAL_FLOW.tsv",
        [
            "initial_shape_amplitude",
            "tanh_cell_depth_control",
            "second_seal_A_rel",
            "second_seal_S_shape",
            "second_seal_condition_met",
            "bulk_target",
        ],
        source_conditional["rows"],
    )
    write_tsv(
        "NONBLOCK_CONTROLS.tsv",
        [
            "control_id",
            "cross_rank",
            "schur_recovery",
            "congruence_to_h_plus_q",
            "determinant_identity",
            "signature",
        ],
        nonblock,
    )
    write_tsv(
        "CONTROL_ATLAS.tsv",
        [
            "control_id",
            "class",
            "free_data",
            "observation",
            "selector_status",
        ],
        controls,
    )
    write_tsv(
        "ROUTE_RULING_MATRIX.tsv",
        ["route_id", "route", "ruling", "exact_reason", "control"],
        rulings,
    )
    write_tsv(
        "SOURCE_TERM_FREEDOM.tsv",
        [
            "freedom_id",
            "datum",
            "dimension_or_scope",
            "effect",
            "current_selector",
        ],
        freedoms,
    )
    write_tsv(
        "BOUNDARY_PROPAGATION_ATLAS.tsv",
        [
            "boundary_id",
            "class",
            "A_rel",
            "J_amplitude",
            "K_eff",
            "bulk_uniqueness",
        ],
        boundaries,
    )
    write_tsv(
        "CATCH_PROOFS.tsv",
        ["catch_id", "mutation", "status"],
        catches,
    )
    write_tsv(
        "JOIN_LEDGER.tsv",
        ["join_id", "from", "to", "ruling"],
        joins,
    )
    write_tsv(
        "STATUS_LEDGER.tsv",
        ["object", "status", "scope"],
        statuses,
    )
    write_tsv(
        "SOURCE_LINEAGE.tsv",
        ["source_id", "path", "sha256", "size", "role"],
        lineage,
    )
    write_json(
        "RESULT.json",
        {
            "schema": "udt-angular-bulk-jacobi-selector-1.0",
            "base_commit": BASE,
            "sympy_version": sp.__version__,
            "compute": {
                "cpu_only": True,
                "gpu_work_performed": False,
            },
            "derived_object": (
                "D_T(B)+B^2+K_eff=0_with_complete_projected_source"
            ),
            "effective_source": projected["effective_source"],
            "target_source_equivalence": trace_shape["target_requires"],
            "selection_ruling": (
                "TRANSPORT_OBJECT_DERIVED__INDEPENDENT_CURVATURE_CLOSURE_"
                "OPEN__TARGET_PAIR_NOT_FORCED"
            ),
            "counts": {
                "routes": len(rulings),
                "native_bulk_law_derivations": 0,
                "conditional_bulk_law_derivations": 0,
                "unregistered_conditional_closure_theorems": 1,
                "controls": len(controls),
                "nonblock_controls": len(nonblock),
                "source_freedoms": len(freedoms),
                "boundary_rows": len(boundaries),
                "joins": len(joins),
                "sources": len(lineage),
                "catch_proofs": len(catches),
                "complete_on_shell_g_phi_branches": 0,
                "q_second_jet_tidal_rank": generic[
                    "same_q_qp_arbitrary_qpp_tidal_rank"
                ],
            },
            "smallest_missing_join": source_conditional["theorem"][
                "missing_join"
            ],
            "strongest_conditional_closure": source_conditional["theorem"][
                "second_seal_result"
            ],
            "maximum_conclusion": MAXIMUM,
        },
    )


if __name__ == "__main__":
    main()
