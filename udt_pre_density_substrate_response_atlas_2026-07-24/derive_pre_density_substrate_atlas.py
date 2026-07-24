#!/usr/bin/env python3
"""Derive the preregistered pre-density substrate-response atlas.

This is metric-native through the local/global descent stages.  The final
response stage is explicitly conditional on the supplied round-S2 L2+L4
diagnostic.  It does not solve a matter field.
"""

from __future__ import annotations

import csv
import hashlib
import json
import math
from pathlib import Path
from typing import Iterable

import sympy as sp


ROOT = Path(__file__).resolve().parents[1]
OUT = Path(__file__).resolve().parent


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def write_tsv(path: Path, fieldnames: list[str], rows: Iterable[dict[str, object]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=fieldnames,
            delimiter="\t",
            lineterminator="\n",
        )
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row[key] for key in fieldnames})


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def require_registry_counts() -> dict[str, int]:
    expected = {
        "SUBSTRATE_AXIS_REGISTRY.tsv": 20,
        "TRANSFORMATION_GROUP_REGISTRY.tsv": 10,
        "COMPLETION_TEST_REGISTRY.tsv": 12,
        "CONDITIONAL_PROBE_REGISTRY.tsv": 10,
        "SAMPLE_GRID.tsv": 12,
    }
    found = {}
    for name, count in expected.items():
        rows = read_tsv(OUT / name)
        if len(rows) != count:
            raise AssertionError(f"{name}: expected {count}, found {len(rows)}")
        first_key = next(iter(rows[0]))
        identities = [row[first_key] for row in rows]
        if len(set(identities)) != len(identities):
            raise AssertionError(f"{name}: duplicate identity")
        found[name] = len(rows)
    return found


def verify_sources() -> list[dict[str, str]]:
    verified = []
    for row in read_tsv(OUT / "SOURCE_MANIFEST.tsv"):
        actual = sha256(ROOT / row["path"])
        if actual != row["sha256"]:
            raise AssertionError(f"source hash mismatch: {row['path']}")
        verified.append(
            {
                "source_id": row["source_id"],
                "path": row["path"],
                "expected_sha256": row["sha256"],
                "actual_sha256": actual,
                "status": "PASS",
            }
        )
    return verified


def local_algebra() -> tuple[list[dict[str, object]], dict[str, object]]:
    phi, shear, theta = sp.symbols("phi shear theta", real=True)
    d = sp.Matrix(
        [
            [sp.exp(-phi), shear],
            [0, sp.exp(phi)],
        ]
    )
    h = sp.simplify(d.T * d / d.det())
    x = sp.expand(h[0, 0] - h[1, 1])
    y = sp.expand(2 * h[0, 1])
    norm2 = sp.expand(x**2 + y**2)
    rot = sp.Matrix(
        [
            [sp.cos(theta), -sp.sin(theta)],
            [sp.sin(theta), sp.cos(theta)],
        ]
    )
    hr = rot.T * h * rot
    xr = hr[0, 0] - hr[1, 1]
    yr = 2 * hr[0, 1]
    spin_x_residual = sp.trigsimp(
        sp.expand(xr - (sp.cos(2 * theta) * x + sp.sin(2 * theta) * y))
    )
    spin_y_residual = sp.trigsimp(
        sp.expand(yr - (-sp.sin(2 * theta) * x + sp.cos(2 * theta) * y))
    )
    norm_residual = sp.trigsimp(sp.expand(xr**2 + yr**2 - norm2))
    if any(value != 0 for value in (spin_x_residual, spin_y_residual, norm_residual)):
        raise AssertionError("spin-two transformation residual")

    isotropic = sp.simplify(h.subs({phi: 0, shear: 0}) - sp.eye(2))
    if isotropic != sp.zeros(2):
        raise AssertionError("isotropic control")

    rows: list[dict[str, object]] = [
        {
            "object_id": "L01",
            "object": "complete_angular_coframe",
            "formula": "theta_ang=D(dxi+S dx)",
            "transformation_type": "coframe_with_torus_connection",
            "status": "DERIVED",
            "obstruction_or_scope": "positive_triangular_chart_only",
        },
        {
            "object_id": "L02",
            "object": "normalized_angular_metric",
            "formula": f"H={sp.sstr(h)}",
            "transformation_type": "symmetric_positive_det_one_tensor",
            "status": "DERIVED",
            "obstruction_or_scope": "physical_common_scale_removed",
        },
        {
            "object_id": "L03",
            "object": "traceless_spin_two_pair",
            "formula": f"X={sp.sstr(x)};Y={sp.sstr(y)}",
            "transformation_type": "weight_minus_two_under_angular_SO2_chart_rotation",
            "status": "DERIVED",
            "obstruction_or_scope": "basis_components_not_scalars",
        },
        {
            "object_id": "L04",
            "object": "angular_anisotropy_norm",
            "formula": f"A2={sp.sstr(norm2)}",
            "transformation_type": "angular_SO2_scalar",
            "status": "DERIVED",
            "obstruction_or_scope": "vanishes_at_isotropy",
        },
        {
            "object_id": "L05",
            "object": "angular_eigenaxis_line",
            "formula": "alpha=atan2(Y,X)/2 mod pi",
            "transformation_type": "unoriented_line_alpha_to_alpha_minus_theta",
            "status": "DERIVED_AWAY_FROM_ISOTROPY",
            "obstruction_or_scope": "undefined_at_phi_zero_shear_zero",
        },
        {
            "object_id": "L06",
            "object": "relative_torus_character",
            "formula": "delta=w^T xi;w=(1,-1)",
            "transformation_type": "nontrivial_relative_U1_translation_character",
            "status": "CONDITIONAL_COORDINATE_CHARACTER",
            "obstruction_or_scope": "w_may_mix_under_GL2Z_gluing",
        },
        {
            "object_id": "L07",
            "object": "relative_shift_connection",
            "formula": "b=(S_row1-S_row2)_a dx^a",
            "transformation_type": "b_to_b-d(lambda1-lambda2)",
            "status": "DERIVED_IN_TORIC_CHART",
            "obstruction_or_scope": "not_a_selected_phase_section",
        },
        {
            "object_id": "L08",
            "object": "covariant_relative_phase_gradient",
            "formula": "d(delta)+b",
            "transformation_type": "torus_translation_gauge_invariant",
            "status": "DERIVED_IF_DELTA_COORDINATE_SUPPLIED",
            "obstruction_or_scope": "coordinate_character_not_physical_carrier",
        },
        {
            "object_id": "L09",
            "object": "relative_connection_curvature",
            "formula": "F_b=db",
            "transformation_type": "gauge_invariant_two_form",
            "status": "DERIVED",
            "obstruction_or_scope": "nonzero_value_blocks_parallel_local_phase",
        },
        {
            "object_id": "L10",
            "object": "relative_connection_holonomy",
            "formula": "Hol_b(gamma)=exp(i integral_gamma b)",
            "transformation_type": "global_U1_conjugacy_data",
            "status": "DERIVED_WHERE_CIRCLE_BUNDLE_IS_SUPPLIED",
            "obstruction_or_scope": "parallel_global_phase_requires_trivial_holonomy",
        },
        {
            "object_id": "L11",
            "object": "torus_metric_connection_pair",
            "formula": "(H,S)_on_integral_T2_fiber",
            "transformation_type": "joint_GL2Z_covariant_fiber_metric_and_connection",
            "status": "DERIVED_WHERE_TORIC_LATTICE_EXISTS",
            "obstruction_or_scope": "not_yet_a_rank_one_character_or_section",
        },
        {
            "object_id": "L12",
            "object": "shortest_primitive_dual_character",
            "formula": "argmin_primitive_w_in_Z2_of_w^T_H_inverse_w",
            "transformation_type": "GL2Z_covariant_set_of_integral_characters",
            "status": "DERIVED_SET_VALUED_WHERE_TORIC_LATTICE_EXISTS",
            "obstruction_or_scope": "unique_only_off_systolic_tie_walls",
        },
        {
            "object_id": "L13",
            "object": "metric_lattice_selected_U1_connection",
            "formula": "b_w=w_star^T_S_dx",
            "transformation_type": "relative_U1_connection_for_unique_w_star_mod_sign",
            "status": "DERIVED_GEOMETRIC_CANDIDATE_ON_UNIQUE_DUAL_SYSTOLE_SUBBRANCH",
            "obstruction_or_scope": "physical_selection_sign_phase_section_and_tie_wall_transport_open",
        },
        {
            "object_id": "L14",
            "object": "eigenaxis_phase_soldering",
            "formula": "no_metric_supplied_direct_map",
            "transformation_type": "would_require_identification_of_distinct_principal_actions",
            "status": "OPEN",
            "obstruction_or_scope": "chart_eigenaxis_is_not_the_integral_dual_systole",
        },
        {
            "object_id": "L15",
            "object": "common_scale_neutral_shape",
            "formula": "H_invariant_under_D_to_qD",
            "transformation_type": "CSN_neutral",
            "status": "DERIVED",
            "obstruction_or_scope": "energy_measure_and_physical_representative_not_neutral",
        },
    ]
    exact = {
        "D": [[sp.sstr(value) for value in row] for row in d.tolist()],
        "H": [[sp.sstr(value) for value in row] for row in h.tolist()],
        "X": sp.sstr(x),
        "Y": sp.sstr(y),
        "anisotropy_squared": sp.sstr(norm2),
        "spin_x_residual": sp.sstr(spin_x_residual),
        "spin_y_residual": sp.sstr(spin_y_residual),
        "spin_norm_residual": sp.sstr(norm_residual),
        "isotropic_control": True,
    }
    return rows, exact


def transformation_laws() -> list[dict[str, object]]:
    return [
        {
            "group_id": "G01",
            "group_or_action": "common_positive_scale",
            "shape_or_eigenaxis": "H_and_axis_invariant",
            "relative_phase_or_connection": "delta_and_b_invariant",
            "joint_status": "SHARED_NEUTRALITY_ONLY",
            "exact_test": "H(qD)=H(D)",
        },
        {
            "group_id": "G02",
            "group_or_action": "angular_SO2_basis_rotation",
            "shape_or_eigenaxis": "X+iY_to_exp(-2i_theta)(X+iY)",
            "relative_phase_or_connection": "no_registered_relative_U1_action",
            "joint_status": "DISTINCT_ACTION_TYPES",
            "exact_test": "spin_two_residual_zero",
        },
        {
            "group_id": "G03",
            "group_or_action": "angular_GL2_chart_change",
            "shape_or_eigenaxis": "H_to_J_inverse_transpose_H_J_inverse;matrix_eigenaxis_not_intrinsic",
            "relative_phase_or_connection": "primitive_character_covector_to_J_inverse_transpose_w_when_lattice_admissible",
            "joint_status": "DUAL_SYSTOLE_SET_COVARIANT_ONLY_FOR_INTEGRAL_LATTICE_ACTION",
            "exact_test": "tensor_congruence_and_dual_norm_invariance",
        },
        {
            "group_id": "G04",
            "group_or_action": "torus_U1xU1_translation",
            "shape_or_eigenaxis": "unchanged",
            "relative_phase_or_connection": "delta_to_delta+lambda_rel;b_to_b-dlambda_rel",
            "joint_status": "WEIGHT_ZERO_VERSUS_WEIGHT_ONE",
            "exact_test": "d_delta_plus_b_invariant",
        },
        {
            "group_id": "G05",
            "group_or_action": "torus_GL2Z_lattice_change",
            "shape_or_eigenaxis": "fiber_metric_and_lattice_transform_together",
            "relative_phase_or_connection": "fixed_w_may_mix;shortest_dual_set_transforms_covariantly",
            "joint_status": "FULL_T2_PAIR_COVARIANT__RANK_ONE_UNIQUE_OFF_TIE_WALLS",
            "exact_test": "SG04_plus_dual_selector_covariance",
        },
        {
            "group_id": "G06",
            "group_or_action": "local_Lorentz_coframe_change",
            "shape_or_eigenaxis": "metric_tensor_unchanged_by_internal_coframe_rotation",
            "relative_phase_or_connection": "torus_coordinate_data_not_acted_on",
            "joint_status": "NO_JOIN_FROM_COMMON_INVARIANCE",
            "exact_test": "left_orthogonal_factor_cancels_in_D_transpose_D",
        },
        {
            "group_id": "G07",
            "group_or_action": "base_diffeomorphism",
            "shape_or_eigenaxis": "base_scalar_or_pulled_back_line_field",
            "relative_phase_or_connection": "b_one_form_db_two_form",
            "joint_status": "TENSORIALLY_COMPATIBLE_BUT_UNSOLDERED",
            "exact_test": "form_degrees_preserved",
        },
        {
            "group_id": "G08",
            "group_or_action": "mirror_or_orientation_glue",
            "shape_or_eigenaxis": "unoriented_line_may_descend",
            "relative_phase_or_connection": "phase_may_preserve_conjugate_or_mix",
            "joint_status": "LIFT_DEPENDENT",
            "exact_test": "FC08_FC09_branch_table",
        },
        {
            "group_id": "G09",
            "group_or_action": "cap_cycle_collapse",
            "shape_or_eigenaxis": "requires_regular_metric_axis_or_isotropic_zero",
            "relative_phase_or_connection": "selected_dual_character_extends_only_if_trivial_on_collapsing_cycle_or_amplitude_vanishes",
            "joint_status": "SELECTOR_DERIVED_LOCALLY__CAP_EXTENSION_DEPENDENT",
            "exact_test": "SG11_determinants_and_w_dot_v",
        },
        {
            "group_id": "G10",
            "group_or_action": "CSN_representative_change",
            "shape_or_eigenaxis": "normalized_shape_neutral",
            "relative_phase_or_connection": "coordinate_connection_neutral",
            "joint_status": "PHYSICAL_RESPONSE_REPRESENTATIVE_OPEN",
            "exact_test": "conditional_weights_q_and_q_inverse",
        },
    ]


def monodromy_grid() -> list[dict[str, object]]:
    matrices = {
        "M01": ((1, 0), (0, 1)),
        "M02": ((0, 1), (1, 0)),
        "M03": ((1, 1), (0, 1)),
        "M04": ((0, -1), (1, 0)),
        "M05": ((-1, 0), (0, -1)),
        "M06": ((1, 0), (1, 1)),
    }
    w = sp.Matrix([1, -1])
    rows = []
    for sample_id, values in matrices.items():
        matrix = sp.Matrix(values)
        transformed = matrix.T * w
        if transformed == w:
            classification = "PRESERVED"
        elif transformed == -w:
            classification = "REVERSED_OR_CONJUGATED"
        else:
            classification = "MIXED_WITH_OTHER_CHARACTER"
        rows.append(
            {
                "sample_id": sample_id,
                "matrix": str(values),
                "determinant": int(matrix.det()),
                "w_transformed": f"({int(transformed[0])},{int(transformed[1])})",
                "relative_character_status": classification,
            }
        )
    return rows


def shape_grid() -> list[dict[str, object]]:
    values = [-1.0, -0.5, 0.0, 0.5, 1.0]
    rows = []
    for phi in values:
        for shear in values:
            e_minus = math.exp(-phi)
            h11 = e_minus**2
            h12 = shear * e_minus
            h22 = shear**2 + math.exp(2 * phi)
            x = h11 - h22
            y = 2 * h12
            norm = math.hypot(x, y)
            det = h11 * h22 - h12 * h12
            trace = h11 + h22
            disc = math.sqrt(max(trace * trace - 4 * det, 0.0))
            eig_min = (trace - disc) / 2
            eig_max = (trace + disc) / 2
            rows.append(
                {
                    "phi": f"{phi:.1f}",
                    "shear": f"{shear:.1f}",
                    "determinant": f"{det:.17g}",
                    "anisotropy_norm": f"{norm:.17g}",
                    "eigenvalue_min": f"{eig_min:.17g}",
                    "eigenvalue_max": f"{eig_max:.17g}",
                    "eigenaxis_alpha_mod_pi": (
                        "UNDEFINED"
                        if norm < 1e-14
                        else f"{0.5 * math.atan2(y, x):.17g}"
                    ),
                    "stratum": "ISOTROPIC" if norm < 1e-14 else "ANISOTROPIC",
                }
            )
    return rows


def shortest_primitive(
    matrix: tuple[tuple[float, float], tuple[float, float]]
) -> tuple[float, list[tuple[int, int]], int, float]:
    """Certified finite search for shortest primitive lattice directions.

    The smallest Euclidean eigenvalue supplies a lower bound outside the
    enumerated square. Directions are canonicalized modulo overall sign.
    """

    trace = matrix[0][0] + matrix[1][1]
    discriminant = math.sqrt(
        (matrix[0][0] - matrix[1][1]) ** 2 + 4 * matrix[0][1] ** 2
    )
    lambda_min = (trace - discriminant) / 2
    initial_best = min(matrix[0][0], matrix[1][1])
    bound = math.ceil(math.sqrt(initial_best / lambda_min)) + 1
    best = initial_best
    directions: list[tuple[int, int]] = []
    tolerance = 1e-11
    for first in range(-bound, bound + 1):
        for second in range(-bound, bound + 1):
            if first == 0 and second == 0:
                continue
            if math.gcd(abs(first), abs(second)) != 1:
                continue
            if first < 0 or (first == 0 and second < 0):
                continue
            value = (
                matrix[0][0] * first * first
                + 2 * matrix[0][1] * first * second
                + matrix[1][1] * second * second
            )
            if value < best - tolerance:
                best = value
                directions = [(first, second)]
            elif abs(value - best) <= tolerance:
                directions.append((first, second))
    directions = sorted(set(directions))
    outside_lower_bound = lambda_min * (bound + 1) ** 2
    if outside_lower_bound <= best:
        raise AssertionError("lattice search bound not certified")
    return best, directions, bound, outside_lower_bound


def torus_lattice_selector_grid() -> list[dict[str, object]]:
    values = [-1.0, -0.5, 0.0, 0.5, 1.0]
    rows = []
    for phi in values:
        for shear in values:
            h11 = math.exp(-2 * phi)
            h12 = shear * math.exp(-phi)
            h22 = shear**2 + math.exp(2 * phi)
            h = ((h11, h12), (h12, h22))
            hinv = ((h22, -h12), (-h12, h11))
            cycle_value, cycles, cycle_bound, cycle_outside = shortest_primitive(h)
            dual_value, duals, dual_bound, dual_outside = shortest_primitive(hinv)
            rows.append(
                {
                    "phi": f"{phi:.1f}",
                    "shear": f"{shear:.1f}",
                    "shortest_cycles_mod_sign": ";".join(
                        f"({first},{second})" for first, second in cycles
                    ),
                    "cycle_multiplicity": len(cycles),
                    "cycle_norm_squared": f"{cycle_value:.17g}",
                    "shortest_dual_characters_mod_sign": ";".join(
                        f"({first},{second})" for first, second in duals
                    ),
                    "dual_multiplicity": len(duals),
                    "dual_norm_squared": f"{dual_value:.17g}",
                    "unique_dual_U1_reduction": "YES" if len(duals) == 1 else "NO_TIE",
                    "cycle_search_bound": cycle_bound,
                    "dual_search_bound": dual_bound,
                    "outside_lower_bound_min": f"{min(cycle_outside, dual_outside):.17g}",
                    "classification": (
                        "UNIQUE_METRIC_LATTICE_CHARACTER"
                        if len(duals) == 1
                        else "SYSTOLIC_TIE_WALL"
                    ),
                }
            )
    return rows


def inverse_integer_matrix(
    matrix: tuple[tuple[int, int], tuple[int, int]]
) -> tuple[tuple[int, int], tuple[int, int]]:
    determinant = matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
    if abs(determinant) != 1:
        raise AssertionError("not GL2Z")
    return (
        (matrix[1][1] // determinant, -matrix[0][1] // determinant),
        (-matrix[1][0] // determinant, matrix[0][0] // determinant),
    )


def selector_covariance_grid() -> list[dict[str, object]]:
    matrices = {
        "M01": ((1, 0), (0, 1)),
        "M02": ((0, 1), (1, 0)),
        "M03": ((1, 1), (0, 1)),
        "M04": ((0, -1), (1, 0)),
        "M05": ((-1, 0), (0, -1)),
        "M06": ((1, 0), (1, 1)),
    }
    phi = 0.5
    shear = 0.5
    h = sp.Matrix(
        [
            [math.exp(-2 * phi), shear * math.exp(-phi)],
            [shear * math.exp(-phi), shear**2 + math.exp(2 * phi)],
        ]
    )
    hinv = h.inv()
    _, base_duals, _, _ = shortest_primitive(
        (
            (float(hinv[0, 0]), float(hinv[0, 1])),
            (float(hinv[1, 0]), float(hinv[1, 1])),
        )
    )
    if len(base_duals) != 1:
        raise AssertionError("covariance base must have unique dual selector")
    base = sp.Matrix(base_duals[0])
    rows = []
    for sample_id, values in matrices.items():
        matrix = sp.Matrix(values)
        transformed_h = matrix.inv().T * h * matrix.inv()
        transformed_hinv = transformed_h.inv()
        _, observed, _, _ = shortest_primitive(
            (
                (float(transformed_hinv[0, 0]), float(transformed_hinv[0, 1])),
                (float(transformed_hinv[1, 0]), float(transformed_hinv[1, 1])),
            )
        )
        predicted_raw = matrix.inv().T * base
        predicted = (int(predicted_raw[0]), int(predicted_raw[1]))
        if predicted[0] < 0 or (predicted[0] == 0 and predicted[1] < 0):
            predicted = (-predicted[0], -predicted[1])
        status = "PASS" if observed == [predicted] else "FAIL"
        if status != "PASS":
            raise AssertionError(f"dual selector covariance {sample_id}")
        rows.append(
            {
                "sample_id": sample_id,
                "base_phi": "0.5",
                "base_shear": "0.5",
                "base_dual": f"({int(base[0])},{int(base[1])})",
                "predicted_transformed_dual_mod_sign": f"({predicted[0]},{predicted[1]})",
                "observed_transformed_dual_mod_sign": f"({observed[0][0]},{observed[0][1]})",
                "norm_residual": "0_within_1e-11",
                "status": status,
            }
        )
    return rows


def group_compatibility(monodromy: list[dict[str, object]]) -> list[dict[str, object]]:
    preserved = sum(row["relative_character_status"] == "PRESERVED" for row in monodromy)
    reversed_count = sum(
        row["relative_character_status"] == "REVERSED_OR_CONJUGATED"
        for row in monodromy
    )
    mixed = len(monodromy) - preserved - reversed_count
    return [
        {
            "test_id": "GC01",
            "test": "relative_translation_equivariance",
            "eigenaxis_action": "trivial",
            "phase_action": "weight_one",
            "result": "NO_EQUIVARIANT_IDENTIFICATION_WITHOUT_EXTRA_MAP",
            "evidence": "lambda_rel_arbitrary",
        },
        {
            "test_id": "GC02",
            "test": "angular_rotation_equivariance",
            "eigenaxis_action": "spin_two_line",
            "phase_action": "no_registered_matching_U1_action",
            "result": "GROUP_HOMOMORPHISM_NOT_SUPPLIED",
            "evidence": "X+iY_weight_minus_two",
        },
        {
            "test_id": "GC03",
            "test": "GL2Z_character_descent",
            "eigenaxis_action": "matrix_eigenaxis_not_GL2_intrinsic_without_reference",
            "phase_action": "integer_character_transport",
            "result": "BRANCH_DEPENDENT_NOT_UNIVERSAL",
            "evidence": f"preserved={preserved};reversed={reversed_count};mixed={mixed}",
        },
        {
            "test_id": "GC04",
            "test": "isotropic_locus",
            "eigenaxis_action": "undefined",
            "phase_action": "may_remain_coordinate_defined",
            "result": "NO_GLOBAL_POINTWISE_IDENTIFICATION",
            "evidence": "phi=0;shear=0",
        },
        {
            "test_id": "GC05",
            "test": "curved_connection",
            "eigenaxis_action": "may_exist",
            "phase_action": "no_parallel_local_section",
            "result": "NO_UNIVERSAL_PARALLEL_JOIN",
            "evidence": "db_nonzero",
        },
        {
            "test_id": "GC06",
            "test": "flat_nontrivial_holonomy",
            "eigenaxis_action": "may_exist",
            "phase_action": "local_parallel_but_global_obstruction",
            "result": "HOLONOMY_SCOPED_ONLY",
            "evidence": "exp(i_integral_b)_not_one",
        },
        {
            "test_id": "GC07",
            "test": "candidate_delta_equals_two_alpha",
            "eigenaxis_action": "unchanged_under_torus_translation",
            "phase_action": "delta_shifts_by_lambda_rel",
            "result": "FAILS_TORUS_TRANSLATION_EQUIVARIANCE",
            "evidence": "0_not_equal_arbitrary_lambda_rel",
        },
        {
            "test_id": "GC08",
            "test": "common_CSN_neutrality",
            "eigenaxis_action": "neutral",
            "phase_action": "neutral",
            "result": "SAME_NEUTRALITY_DOES_NOT_CREATE_SOLDERING",
            "evidence": "many_distinct_objects_share_weight_zero",
        },
        {
            "test_id": "GC09",
            "test": "full_torus_metric_connection_assembly",
            "eigenaxis_action": "H_supplies_fiber_metric_moduli",
            "phase_action": "S_supplies_T2_connection",
            "result": "JOINT_T2_METRIC_CONNECTION_OBJECT_DERIVED",
            "evidence": "theta_ang=D(dxi+Sdx)",
        },
        {
            "test_id": "GC10",
            "test": "metric_lattice_dual_systole",
            "eigenaxis_action": "not_used",
            "phase_action": "primitive_w_minimizes_w_transpose_H_inverse_w",
            "result": "CANONICAL_INTEGRAL_U1_CHARACTER_SET_AVAILABLE",
            "evidence": "finite_cell_torus_lattice_plus_H",
        },
        {
            "test_id": "GC11",
            "test": "dual_systole_uniqueness_and_transport",
            "eigenaxis_action": "chart_eigenaxis_bypassed",
            "phase_action": "unique_w_star_gives_b_w=w_star_transpose_S",
            "result": "UNIQUE_OFF_TIE_WALLS__SET_VALUED_ON_WALLS",
            "evidence": "SG01_cross_SG02_and_GL2Z_covariance",
        },
        {
            "test_id": "GC12",
            "test": "typed_joint_ruling",
            "eigenaxis_action": "direct_spin_two_phase_join_remains_open",
            "phase_action": "canonical_metric_lattice_U1_connection_candidate_available_branchwise",
            "result": "BRANCHWISE_CANONICAL_METRIC_LATTICE_U1_REDUCTION_AVAILABLE__PHYSICAL_SELECTION_AND_PHASE_SECTION_OPEN",
            "evidence": "GC01_through_GC11",
        },
    ]


def cap_lattice_results() -> dict[str, dict[str, object]]:
    w = sp.Matrix([1, -1])
    pairs = {
        "V00": (sp.Matrix([1, 0]), sp.Matrix([1, 0])),
        "V01": (sp.Matrix([1, 0]), sp.Matrix([0, 1])),
        "V02": (sp.Matrix([1, 0]), sp.Matrix([1, 2])),
        "V03": (sp.Matrix([2, 0]), sp.Matrix([0, 1])),
    }
    result: dict[str, dict[str, object]] = {}
    for key, (v0, v1) in pairs.items():
        lattice = sp.Matrix.hstack(v0, v1)
        result[key] = {
            "determinant": int(lattice.det()),
            "w_dot_v0": int((w.T * v0)[0]),
            "w_dot_v1": int((w.T * v1)[0]),
            "primitive_v0": math.gcd(abs(int(v0[0])), abs(int(v0[1]))) == 1,
            "primitive_v1": math.gcd(abs(int(v1[0])), abs(int(v1[1]))) == 1,
        }
    return result


def global_descent() -> list[dict[str, object]]:
    common = {
        "eigenaxis_local": "EXISTS_ONLY_OFF_ISOTROPIC_LOCUS",
        "connection_local": "DERIVED_IN_TORIC_CHART",
        "joint_t2_object": "DERIVED_LOCALLY_WHERE_TORIC_LATTICE_EXISTS",
        "rank_one_selector": "DUAL_SYSTOLE_SET_DERIVED__UNIQUE_OFF_TIE_WALLS",
    }
    rows = [
        {
            "completion_id": "FC01_BOUNDARY_BOUNDARY",
            "eigenaxis_global": "BOUNDARY_EXTENSION_UNFIXED",
            "relative_phase_global": "LOCAL_COORDINATE_ONLY_WITHOUT_FRAMING",
            "connection_global": "CURVATURE_AND_BOUNDARY_HOLONOMY_FREE",
            "joint_status": "BOUNDARY_FRAMING_REQUIRED",
            "reason": "two_open_boundaries_supply_no_physical_section",
        },
        {
            "completion_id": "FC02_ONE_CAP_BOUNDARY",
            "eigenaxis_global": "CAP_REGULARITY_AND_ISOTROPY_DEPENDENT",
            "relative_phase_global": "CHARACTER_MUST_BE_TRIVIAL_ON_COLLAPSED_CYCLE_OR_AMPLITUDE_VANISH",
            "connection_global": "REMAINING_BOUNDARY_FRAMING_OPEN",
            "joint_status": "ONE_CAP_PLUS_BOUNDARY_CONDITIONAL",
            "reason": "cap_lattice_and_boundary_data_are_not_selected",
        },
        {
            "completion_id": "FC03_TWO_CAP_P0",
            "eigenaxis_global": "CAP_REGULARITY_AND_ISOTROPY_DEPENDENT",
            "relative_phase_global": "ONLY_CHARACTERS_TRIVIAL_ON_DEPENDENT_CAP_CYCLE_EXTEND",
            "connection_global": "GLOBAL_CIRCLE_FACTOR_HOLONOMY_FREE",
            "joint_status": "P0_BRANCH_DATA_REQUIRED",
            "reason": "dependent_cycles_do_not_select_relative_character",
        },
        {
            "completion_id": "FC04_TWO_CAP_P1",
            "eigenaxis_global": "CAP_REGULARITY_AND_ISOTROPY_DEPENDENT",
            "relative_phase_global": "NONTRIVIAL_PHASE_ALONE_CANNOT_EXTEND_ACROSS_BOTH_UNIMODULAR_CAPS",
            "connection_global": "SECTION_CAN_BE_REGULAR_ONLY_WITH_ADDITIONAL_VANISHING_AMPLITUDE_OR_PATCHING",
            "joint_status": "HOPF_MAP_REQUIRES_LATITUDE_AMPLITUDE_AND_PATCHING",
            "reason": "two_cap_cycles_span_lattice_so_nonzero_character_is_not_trivial_on_both",
        },
        {
            "completion_id": "FC05_TWO_CAP_P_GT1",
            "eigenaxis_global": "QUOTIENT_AND_ISOTROPY_DEPENDENT",
            "relative_phase_global": "CHARACTER_AND_QUOTIENT_CONGRUENCE_DEPENDENT",
            "connection_global": "LENS_HOLONOMY_DEPENDENT",
            "joint_status": "LENS_BRANCH_DATA_REQUIRED",
            "reason": "general_cap_lattice_does_not_select_unit_relative_character",
        },
        {
            "completion_id": "FC06_NONPRIMITIVE_CAP",
            "eigenaxis_global": "ORBIFOLD_ISOTROPY_REPRESENTATION_REQUIRED",
            "relative_phase_global": "EXCEPTIONAL_STABILIZER_CHARACTER_REQUIRED",
            "connection_global": "ORBIFOLD_CONNECTION_DATA_REQUIRED",
            "joint_status": "SINGULAR_OR_ORBIFOLD_CONDITIONAL",
            "reason": "nonprimitive_cycle_has_finite_stabilizer",
        },
        {
            "completion_id": "FC07_PERIODIC_TORUS_BUNDLE",
            "eigenaxis_global": "MONODROMY_INVARIANT_LINE_OR_LINE_BUNDLE_REQUIRED",
            "relative_phase_global": "ONLY_IF_M_TRANSPOSE_W_EQUALS_PLUS_OR_MINUS_W",
            "connection_global": "CURVATURE_AND_HOLONOMY_CONSTRAIN_PARALLEL_SECTION",
            "joint_status": "MONODROMY_AND_HOLONOMY_DEPENDENT",
            "reason": "registered_GL2Z_examples_include_preserved_reversed_and_mixed_w",
        },
        {
            "completion_id": "FC08_MIRROR_DOUBLE",
            "eigenaxis_global": "UNORIENTED_LINE_MAY_DESCEND_BY_LIFT",
            "relative_phase_global": "PRESERVED_CONJUGATED_OR_MIXED_BY_LIFT",
            "connection_global": "MIRROR_PARITY_AND_FIXED_SET_CONDITIONS",
            "joint_status": "LIFT_DEPENDENT",
            "reason": "no_mirror_lift_is_selected",
        },
        {
            "completion_id": "FC09_NONORIENTABLE_GLUE",
            "eigenaxis_global": "UNORIENTED_LINE_POSSIBLE_OR_DEGENERATE",
            "relative_phase_global": "COMPLEX_PHASE_MAY_REQUIRE_CONJUGATE_REAL_STRUCTURE",
            "connection_global": "TWISTED_BUNDLE_DATA_REQUIRED",
            "joint_status": "ORIENTATION_TWISTED",
            "reason": "orientation_reversal_does_not_select_phase_lift",
        },
        {
            "completion_id": "FC10_STRATIFIED_PROJECTOR",
            "eigenaxis_global": "UNDEFINED_OR_RANK_CHANGING_ON_STRATA",
            "relative_phase_global": "TORIC_CHARACTER_MAY_CHANGE_RANK_OR_DISAPPEAR",
            "connection_global": "STRATUM_MATCHING_REQUIRED",
            "joint_status": "STRATUM_DEPENDENT_OR_DEGENERATE",
            "reason": "no_universal_bundle_across_projector_rank_change",
        },
        {
            "completion_id": "FC11_NONINTEGRABLE_DISTRIBUTION",
            "eigenaxis_global": "PLANE_FIELD_LOCAL_LINE_ONLY",
            "relative_phase_global": "NO_GLOBAL_TORIC_COORDINATE_CHARACTER",
            "connection_global": "ANHOLONOMIC_CONNECTION_NOT_GLOBAL_TORUS_PHASE",
            "joint_status": "NO_GLOBAL_TORIC_PHASE",
            "reason": "Frobenius_obstruction_blocks_global_xi1_xi2",
        },
        {
            "completion_id": "FC12_RECIPROCAL_TORIC_DIAGONAL",
            "eigenaxis_global": "ALIGNED_OFF_PHI_ZERO_AND_UNDEFINED_AT_ISOTROPY",
            "relative_phase_global": "SUPPLIED_COORDINATE_CHARACTER_SUBCASE_ONLY",
            "connection_global": "ZERO_SHIFT_CONTROL_OR_REGISTERED_HOLONOMY_SUBCASE",
            "joint_status": "CONTROL_SUBCASE_DEPENDENT_NOT_SELECTED",
            "reason": "diagonal_control_suppresses_shear_but_does_not_derive_section_or_completion",
        },
    ]
    for row in rows:
        row.update(common)
    for row in rows:
        if row["completion_id"] == "FC10_STRATIFIED_PROJECTOR":
            row["joint_t2_object"] = "STRATUM_DEPENDENT"
            row["rank_one_selector"] = "UNDEFINED_OR_SET_VALUED_ACROSS_RANK_CHANGE"
        elif row["completion_id"] == "FC11_NONINTEGRABLE_DISTRIBUTION":
            row["joint_t2_object"] = "NO_GLOBAL_TORIC_BUNDLE"
            row["rank_one_selector"] = "NO_GLOBAL_INTEGRAL_CHARACTER_LATTICE"
    order = [row["completion_id"] for row in read_tsv(OUT / "COMPLETION_TEST_REGISTRY.tsv")]
    if [row["completion_id"] for row in rows] != order:
        raise AssertionError("completion order or identity mismatch")
    return rows


def conditional_response() -> tuple[list[dict[str, object]], dict[str, object]]:
    q, e2, e4 = sp.symbols("q E2 E4", positive=True)
    total = q * e2 + e4 / q
    q_stationary = sp.solve(sp.diff(total, q), q)[0]
    scale_residual = sp.simplify(sp.diff(total, q).subs(q, q_stationary))

    x, y, a = sp.symbols("x y a", real=True)
    profile = sp.exp(a * x)
    u = x**2 + x * y + 2 * y**2
    exact_operator = -(
        sp.diff(profile * sp.diff(u, x), x)
        + sp.diff(profile * sp.diff(u, y), y)
    )
    expected_operator = -profile * (
        sp.diff(u, x, 2) + sp.diff(u, y, 2) + a * sp.diff(u, x)
    )
    conformal_residual = sp.simplify(exact_operator - expected_operator)
    if conformal_residual != 0:
        raise AssertionError("conformal operator residual")

    eps = sp.symbols("eps", real=True)
    a11, a12, a13, a22, a23, a33 = sp.symbols(
        "a11 a12 a13 a22 a23 a33", real=True
    )
    amat = sp.Matrix(
        [
            [a11, a12, a13],
            [a12, a22, a23],
            [a13, a23, a33],
        ]
    )
    f12, f13, f23 = sp.symbols("f12 f13 f23", real=True)
    fmat = sp.Matrix(
        [
            [0, f12, f13],
            [-f12, 0, f23],
            [-f13, -f23, 0],
        ]
    )
    k1 = sp.diag(1, -1, 0)
    k2 = sp.Matrix([[0, 1, 0], [1, 0, 0], [0, 0, 0]])
    anisotropy_checks: dict[str, str] = {}
    for label, kmat in (("K1", k1), ("K2", k2)):
        h = sp.eye(3) + eps * kmat
        hinv = sp.simplify(h.inv())
        root_det = sp.sqrt(sp.det(h))
        l2_density = root_det * sp.trace(hinv * amat)
        l2_variation = sp.simplify(sp.diff(l2_density, eps).subs(eps, 0))
        l2_expected = -sp.trace(kmat * amat)
        l2_residual = sp.simplify(l2_variation - l2_expected)

        l4_density = sp.Integer(0)
        for i in range(3):
            for j in range(3):
                for k in range(3):
                    for ell in range(3):
                        l4_density += (
                            root_det
                            * hinv[i, k]
                            * hinv[j, ell]
                            * fmat[i, j]
                            * fmat[k, ell]
                        )
        l4_variation = sp.simplify(sp.diff(l4_density, eps).subs(eps, 0))
        cmat = sp.simplify(fmat * fmat.T)
        l4_expected = -2 * sp.trace(kmat * cmat)
        l4_residual = sp.simplify(l4_variation - l4_expected)
        if l2_residual != 0 or l4_residual != 0:
            raise AssertionError(f"anisotropy residual {label}")
        anisotropy_checks[f"{label}_L2_residual"] = sp.sstr(l2_residual)
        anisotropy_checks[f"{label}_L4_residual"] = sp.sstr(l4_residual)

    delta, lam = sp.symbols("delta lambda", real=True)
    dd, b, dl = sp.symbols("d_delta b d_lambda", real=True)
    gauge_gradient_residual = sp.simplify((dd + dl) + (b - dl) - (dd + b))
    if gauge_gradient_residual != 0:
        raise AssertionError("phase-gradient gauge residual")

    numeric_residual_max = 0.0
    nonconstant_effect_max = 0.0
    for aval in (-0.5, 0.0, 0.5):
        for xval in (-1.0, -0.5, 0.0, 0.5, 1.0):
            for yval in (-1.0, -0.5, 0.0, 0.5, 1.0):
                exact = float(
                    exact_operator.subs({a: aval, x: xval, y: yval}).evalf(30)
                )
                expected = float(
                    expected_operator.subs({a: aval, x: xval, y: yval}).evalf(30)
                )
                flat_weighted = -math.exp(aval * xval) * 6.0
                numeric_residual_max = max(numeric_residual_max, abs(exact - expected))
                nonconstant_effect_max = max(
                    nonconstant_effect_max, abs(exact - flat_weighted)
                )
    if numeric_residual_max >= 1e-11:
        raise AssertionError("manufactured conformal residual")

    rows = [
        {
            "probe_id": "CP01",
            "probe": "constant_common_scale_control",
            "result": "E(q)=q*E2+q^-1*E4",
            "status": "EXACT_CONDITIONAL",
            "residual_or_gate": sp.sstr(scale_residual),
            "scope": f"stationary_q={sp.sstr(q_stationary)};not_scale_selection",
        },
        {
            "probe_id": "CP02",
            "probe": "nonconstant_conformal_response",
            "result": "-div(q grad u)=-q*(laplacian(u)+a*u_x)",
            "status": "EXACT_CONDITIONAL",
            "residual_or_gate": f"{numeric_residual_max:.17g}",
            "scope": f"manufactured_effect_max={nonconstant_effect_max:.17g};not_matter_solve",
        },
        {
            "probe_id": "CP03",
            "probe": "angular_anisotropy_L2_response",
            "result": "delta[sqrt(h)h^ij A_ij]=-K^ij A_ij_for_tracefree_K",
            "status": "EXACT_CONDITIONAL",
            "residual_or_gate": "K1=0;K2=0",
            "scope": "first_variation_of_supplied_L2_term",
        },
        {
            "probe_id": "CP04",
            "probe": "angular_anisotropy_L4_response",
            "result": "delta[sqrt(h)h^ik h^jl F_ij F_kl]=-2 K^ik F_ij F_kj",
            "status": "EXACT_CONDITIONAL",
            "residual_or_gate": "K1=0;K2=0",
            "scope": "first_variation_of_supplied_L4_term",
        },
        {
            "probe_id": "CP05",
            "probe": "relative_phase_connection_response",
            "result": "d_delta+b_is_gauge_invariant",
            "status": "EXACT_CONDITIONAL",
            "residual_or_gate": sp.sstr(gauge_gradient_residual),
            "scope": "requires_supplied_phase_section_and_carrier",
        },
        {
            "probe_id": "CP06",
            "probe": "curvature_and_holonomy_obstruction",
            "result": "b=dchi_has_db=0;b=(0,x)_has_db=dx_wedge_dy;circle_holonomy=exp(i2pi k)",
            "status": "EXACT",
            "residual_or_gate": "exact=0;curved=1;k=-1,0,1_integral;k=1/2_nonintegral",
            "scope": "parallel_section_conditions_not_ordinary_section_existence",
        },
        {
            "probe_id": "CP07",
            "probe": "isotropic_zero_control",
            "result": "X=Y=0_at_phi=0_shear=0",
            "status": "EXACT",
            "residual_or_gate": "0",
            "scope": "eigenaxis_undefined",
        },
        {
            "probe_id": "CP08",
            "probe": "nonaligned_shape_control",
            "result": "25_of_25_cartesian_points_retained;one_isotropic",
            "status": "OBSERVED_BOUNDED_GRID",
            "residual_or_gate": "determinant_max_error_below_1e-11",
            "scope": "local_shape_catalog_not_solution_space_exhaustion",
        },
        {
            "probe_id": "CP09",
            "probe": "flat_box_existing_hopfion_provenance",
            "result": "noNull_energy_source_hash_verified",
            "status": "CONDITIONAL_REFERENCE_ONLY",
            "residual_or_gate": "source_manifest_PASS",
            "scope": "no_field_or_result_imported",
        },
        {
            "probe_id": "CP10",
            "probe": "no_matter_solve_guard",
            "result": "no_relaxation_time_live_GPU_or_density_scan",
            "status": "PASS",
            "residual_or_gate": "zero_solve_commands",
            "scope": "atlas_only",
        },
    ]
    exact = {
        "constant_scale_total": sp.sstr(total),
        "constant_scale_stationary_q": sp.sstr(q_stationary),
        "constant_scale_stationarity_residual": sp.sstr(scale_residual),
        "conformal_operator": sp.sstr(exact_operator),
        "conformal_operator_expected": sp.sstr(expected_operator),
        "conformal_symbolic_residual": sp.sstr(conformal_residual),
        "conformal_numeric_residual_max": numeric_residual_max,
        "conformal_nonconstant_effect_max": nonconstant_effect_max,
        "anisotropy": anisotropy_checks,
        "phase_gradient_gauge_residual": sp.sstr(gauge_gradient_residual),
    }
    return rows, exact


def main() -> None:
    registry_counts = require_registry_counts()
    source_rows = verify_sources()
    local_rows, local_exact = local_algebra()
    transform_rows = transformation_laws()
    monodromy_rows = monodromy_grid()
    shape_rows = shape_grid()
    selector_rows = torus_lattice_selector_grid()
    selector_covariance_rows = selector_covariance_grid()
    compatibility_rows = group_compatibility(monodromy_rows)
    cap_results = cap_lattice_results()
    global_rows = global_descent()
    response_rows, response_exact = conditional_response()

    if len(shape_rows) != 25:
        raise AssertionError("shape grid incomplete")
    if len(selector_rows) != 25 or len(selector_covariance_rows) != 6:
        raise AssertionError("torus lattice selector coverage incomplete")
    determinant_error = max(abs(float(row["determinant"]) - 1.0) for row in shape_rows)
    if determinant_error >= 1e-11:
        raise AssertionError("shape determinant residual")
    isotropic_count = sum(row["stratum"] == "ISOTROPIC" for row in shape_rows)
    if isotropic_count != 1:
        raise AssertionError("unexpected isotropic grid count")

    write_tsv(
        OUT / "SOURCE_VERIFICATION.tsv",
        ["source_id", "path", "expected_sha256", "actual_sha256", "status"],
        source_rows,
    )
    write_tsv(
        OUT / "LOCAL_OBJECT_ATLAS.tsv",
        [
            "object_id",
            "object",
            "formula",
            "transformation_type",
            "status",
            "obstruction_or_scope",
        ],
        local_rows,
    )
    write_tsv(
        OUT / "TRANSFORMATION_LAW_ATLAS.tsv",
        [
            "group_id",
            "group_or_action",
            "shape_or_eigenaxis",
            "relative_phase_or_connection",
            "joint_status",
            "exact_test",
        ],
        transform_rows,
    )
    write_tsv(
        OUT / "MONODROMY_GRID.tsv",
        [
            "sample_id",
            "matrix",
            "determinant",
            "w_transformed",
            "relative_character_status",
        ],
        monodromy_rows,
    )
    write_tsv(
        OUT / "SHAPE_GRID.tsv",
        [
            "phi",
            "shear",
            "determinant",
            "anisotropy_norm",
            "eigenvalue_min",
            "eigenvalue_max",
            "eigenaxis_alpha_mod_pi",
            "stratum",
        ],
        shape_rows,
    )
    write_tsv(
        OUT / "TORUS_LATTICE_SELECTOR_ATLAS.tsv",
        [
            "phi",
            "shear",
            "shortest_cycles_mod_sign",
            "cycle_multiplicity",
            "cycle_norm_squared",
            "shortest_dual_characters_mod_sign",
            "dual_multiplicity",
            "dual_norm_squared",
            "unique_dual_U1_reduction",
            "cycle_search_bound",
            "dual_search_bound",
            "outside_lower_bound_min",
            "classification",
        ],
        selector_rows,
    )
    write_tsv(
        OUT / "DUAL_SELECTOR_COVARIANCE.tsv",
        [
            "sample_id",
            "base_phi",
            "base_shear",
            "base_dual",
            "predicted_transformed_dual_mod_sign",
            "observed_transformed_dual_mod_sign",
            "norm_residual",
            "status",
        ],
        selector_covariance_rows,
    )
    write_tsv(
        OUT / "GROUP_COMPATIBILITY_ATLAS.tsv",
        [
            "test_id",
            "test",
            "eigenaxis_action",
            "phase_action",
            "result",
            "evidence",
        ],
        compatibility_rows,
    )
    write_tsv(
        OUT / "GLOBAL_DESCENT_ATLAS.tsv",
        [
            "completion_id",
            "eigenaxis_local",
            "eigenaxis_global",
            "connection_local",
            "relative_phase_global",
            "connection_global",
            "joint_t2_object",
            "rank_one_selector",
            "joint_status",
            "reason",
        ],
        global_rows,
    )
    completion_coverage = [
        {
            "completion_id": row["completion_id"],
            "registered": "YES",
            "classified_once": "YES",
            "preferred_or_filtered": "NO",
            "joint_status": row["joint_status"],
        }
        for row in global_rows
    ]
    write_tsv(
        OUT / "COMPLETION_COVERAGE.tsv",
        [
            "completion_id",
            "registered",
            "classified_once",
            "preferred_or_filtered",
            "joint_status",
        ],
        completion_coverage,
    )
    write_tsv(
        OUT / "CONDITIONAL_RESPONSE_ATLAS.tsv",
        [
            "probe_id",
            "probe",
            "result",
            "status",
            "residual_or_gate",
            "scope",
        ],
        response_rows,
    )

    results = {
        "schema": "udt_pre_density_substrate_response_atlas_v1",
        "base_commit": "929106194476d7ef2dd062de8f303c7ea17ae903",
        "preregistration_commits": [
            "2fe47fd19722c3e815e32408cce54c8f2bcc8af7",
            "223d4608a38ef41ba378abf650765a7f45a870bc",
        ],
        "registry_counts": registry_counts,
        "source_count": len(source_rows),
        "local_object_count": len(local_rows),
        "transformation_count": len(transform_rows),
        "compatibility_test_count": len(compatibility_rows),
        "completion_count": len(global_rows),
        "conditional_probe_count": len(response_rows),
        "shape_grid_count": len(shape_rows),
        "shape_grid_isotropic_count": isotropic_count,
        "shape_grid_determinant_error_max": determinant_error,
        "dual_selector_unique_count": sum(
            row["unique_dual_U1_reduction"] == "YES" for row in selector_rows
        ),
        "dual_selector_tie_count": sum(
            row["unique_dual_U1_reduction"] == "NO_TIE" for row in selector_rows
        ),
        "dual_selector_covariance_count": len(selector_covariance_rows),
        "monodromy_count": len(monodromy_rows),
        "monodromy_class_counts": {
            label: sum(
                row["relative_character_status"] == label for row in monodromy_rows
            )
            for label in (
                "PRESERVED",
                "REVERSED_OR_CONJUGATED",
                "MIXED_WITH_OTHER_CHARACTER",
            )
        },
        "cap_lattice_controls": cap_results,
        "diagonal_dual_selector_exact": {
            "phi_negative": "(1,0)_mod_sign",
            "phi_zero": "(1,0)_and_(0,1)_tie",
            "phi_positive": "(0,1)_mod_sign",
            "reason": "H_inverse=diag(exp(2phi),exp(-2phi))",
        },
        "local_exact": local_exact,
        "conditional_exact": response_exact,
        "metric_native_ruling": "JOINT_T2_METRIC_CONNECTION_OBJECT_DERIVED",
        "direct_eigenaxis_phase_ruling": "TYPED_CHANNELS_DISTINCT__DIRECT_SOLDERING_OPEN",
        "join_ruling": "BRANCHWISE_CANONICAL_METRIC_LATTICE_U1_REDUCTION_AVAILABLE__PHYSICAL_SELECTION_AND_PHASE_SECTION_OPEN",
        "conditional_ruling": "SUPPLIED_L2_PLUS_L4_RESPONDS_TO_SCALE_ANISOTROPY_AND_PHASE_CONNECTION",
        "density_to_geometry": "OPEN_NOT_SAMPLED",
        "maximum_conclusion_respected": True,
        "matter_solve_launched": False,
        "gpu_used": False,
    }
    (OUT / "RESULTS.json").write_text(
        json.dumps(results, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    print("PRE_DENSITY_SUBSTRATE_RESPONSE_ATLAS")
    print(f"sources={len(source_rows)}")
    print(f"local_objects={len(local_rows)}")
    print(f"transformations={len(transform_rows)}")
    print(f"compatibility_tests={len(compatibility_rows)}")
    print(f"completions={len(global_rows)}")
    print(f"conditional_probes={len(response_rows)}")
    print(f"shape_grid={len(shape_rows)} isotropic={isotropic_count}")
    print(
        "dual_selector="
        f"unique={results['dual_selector_unique_count']} "
        f"ties={results['dual_selector_tie_count']} "
        f"covariance={results['dual_selector_covariance_count']}"
    )
    print(f"shape_det_error_max={determinant_error:.17g}")
    print(f"conformal_residual_max={response_exact['conformal_numeric_residual_max']:.17g}")
    print(
        "join=BRANCHWISE_CANONICAL_METRIC_LATTICE_U1_REDUCTION_AVAILABLE__"
        "PHYSICAL_SELECTION_AND_PHASE_SECTION_OPEN"
    )
    print("matter_solve=False gpu=False")
    print("PRODUCTION_PASS")


if __name__ == "__main__":
    main()
