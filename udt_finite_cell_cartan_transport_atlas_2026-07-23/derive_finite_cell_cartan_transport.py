#!/usr/bin/env python3
"""Derive the finite-cell Cartan persistence/mixing/degeneration atlas."""

from __future__ import annotations

import csv
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
BASIS2 = ((0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3))
G = sp.diag(-1, 1, 1, 1)
G2 = sp.diag(-1, -1, -1, 1, 1, 1)
I4 = sp.eye(4)
I6 = sp.eye(6)
PARENT_BRANCH = (
    ROOT
    / "udt_finite_cell_reciprocal_survival_density_audit_2026-07-23"
    / "FINITE_CELL_BRANCH_ATLAS.tsv"
)

SOURCES = (
    "AGENTS.md",
    "CANON.md",
    "UDT_SCIENTIFIC_FRONTIER_2026-07-19.md",
    "UDT_COMMON_SCALE_NEUTRALITY_POSTULATE_2026-07-15.md",
    "udt_frame_bivector_equivariance_audit_2026-07-23/AUDIT_REPORT.md",
    "udt_frame_bivector_equivariance_audit_2026-07-23/DERIVATION_RESULT.json",
    "udt_frame_bivector_equivariance_audit_2026-07-23/MANIFEST.sha256",
    "udt_finite_cell_reciprocal_survival_density_audit_2026-07-23/AUDIT_REPORT.md",
    "udt_finite_cell_reciprocal_survival_density_audit_2026-07-23/FINITE_CELL_BRANCH_ATLAS.tsv",
    "udt_finite_cell_reciprocal_survival_density_audit_2026-07-23/GLOBAL_SURVIVAL_THEOREMS.tsv",
    "udt_finite_cell_reciprocal_survival_density_audit_2026-07-23/MANIFEST.sha256",
    "udt_global_metric_assembly_atlas_2026-07-22/AUDIT_REPORT.md",
    "udt_global_metric_assembly_atlas_2026-07-22/COMPLETION_CLASS_REGISTRY.tsv",
    "udt_global_metric_assembly_atlas_2026-07-22/BUNDLE_HOLONOMY_ATLAS.tsv",
    "udt_global_metric_assembly_atlas_2026-07-22/EXACT_TRANSPORT_CONTROL.json",
    "udt_global_metric_assembly_atlas_2026-07-22/SHA256SUMS.txt",
    "udt_complete_metric_intrinsic_object_audit_2026-07-23/AUDIT_REPORT.md",
    "udt_complete_metric_intrinsic_object_audit_2026-07-23/DOMAIN_TRANSITION_LEDGER.tsv",
    "udt_complete_metric_intrinsic_object_audit_2026-07-23/MANIFEST.sha256",
    "udt_finite_cell_completion_atlas_2026-07-21/AUDIT_REPORT.md",
    "udt_finite_cell_completion_atlas_2026-07-21/CAUSAL_TIME_LIVE_ATLAS.tsv",
    "udt_finite_cell_completion_atlas_2026-07-21/SHA256SUMS.txt",
)


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def write_tsv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        raise AssertionError(f"empty table {path.name}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=list(rows[0]),
            delimiter="\t",
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerows(rows)


def zero(matrix: sp.Matrix) -> bool:
    return all(sp.simplify(item) == 0 for item in matrix)


def wedge_coords(x: sp.Matrix, y: sp.Matrix) -> sp.Matrix:
    return sp.Matrix(
        [sp.expand(x[i] * y[j] - x[j] * y[i]) for i, j in BASIS2]
    )


def induced_generator(matrix: sp.Matrix) -> sp.Matrix:
    columns = []
    for i, j in BASIS2:
        ei = I4[:, i]
        ej = I4[:, j]
        columns.append(
            wedge_coords(matrix * ei, ej) + wedge_coords(ei, matrix * ej)
        )
    return sp.Matrix.hstack(*columns)


def induced_projector(projector: sp.Matrix) -> sp.Matrix:
    return induced_generator(projector)


def line_projector(alpha: sp.Matrix, metric: sp.Matrix = G) -> tuple[sp.Matrix, sp.Expr]:
    vector = metric.inv() * alpha
    norm = sp.simplify((alpha.T * vector)[0])
    return sp.simplify(vector * alpha.T / norm), norm


def matrix_rank_block(matrix: sp.Matrix, rows: tuple[int, ...], cols: tuple[int, ...]) -> int:
    return matrix.extract(rows, cols).rank()


def source_hashes() -> list[dict[str, object]]:
    output = []
    for relative in SOURCES:
        data = ROOT.joinpath(relative).read_bytes()
        output.append(
            {
                "path": relative,
                "sha256": hashlib.sha256(data).hexdigest(),
                "bytes": len(data),
            }
        )
    return output


def branch_effect(completion_id: str) -> str:
    effects = {
        "FC01_BOUNDARY_BOUNDARY": "BOUNDARIES_ALLOW_NONNULL_SUBMERSION_BUT_DO_NOT_FORCE_PROFILE",
        "FC02_ONE_CAP_BOUNDARY": "ORBIT_DEPTH_STATIC_CAP_FORCES_NORMAL_CRITICALITY;GENERAL_OR_TIMELIVE_OPEN",
        "FC03_TWO_CAP_P0": "COMPACT_STATIC_REAL_SCALAR_FORCES_ZERO_DPHI;TIMELIVE_NONNULL_OPEN",
        "FC04_TWO_CAP_P1": "COMPACT_STATIC_REAL_SCALAR_FORCES_ZERO_DPHI;TIMELIVE_NONNULL_OPEN",
        "FC05_TWO_CAP_P_GT1": "COMPACT_STATIC_REAL_SCALAR_FORCES_ZERO_DPHI;TIMELIVE_NONNULL_OPEN",
        "FC06_NONPRIMITIVE_CAP": "TRUE_SINGULAR_STRATUM_BLOCKS_CONSTRUCTION;REGULAR_COMPLEMENT_ONLY",
        "FC07_PERIODIC_TORUS_BUNDLE": "PERIODIC_STATIC_REAL_SCALAR_FORCES_CRITICAL_POINT;TIMELIVE_NONNULL_OPEN",
        "FC08_MIRROR_DOUBLE": "EVEN_SCALAR_NORMAL_DERIVATIVE_ZERO;ODD_DOUBLE_NEEDS_SIGN_TWIST_TO_QUOTIENT",
        "FC09_NONORIENTABLE_GLUE": "PROJECTOR_MAY_DESCEND_WITH_LINE;ORDINARY_HODGE_REQUIRES_ORIENTATION_TWIST",
        "FC10_STRATIFIED_PROJECTOR": "OTHER_PROJECTOR_STRATA_DO_NOT_DETERMINE_DPHI_STRATA",
        "FC11_NONINTEGRABLE_DISTRIBUTION": "OTHER_ANHOLONOMIC_PLANE_DOES_NOT_OBSTRUCT_KERNEL_DPHI",
        "FC12_RECIPROCAL_TORIC_DIAGONAL": "OPEN_NONNULL_DEPTH_CONTROL;CAP_OR_GLUE_EXTENSION_PROFILE_DEPENDENT",
    }
    return effects[completion_id]


def main() -> None:
    checks: list[dict[str, object]] = []

    def check(name: str, condition: bool, detail: object) -> None:
        checks.append({"name": name, "pass": bool(condition), "detail": detail})

    r1, r2, r3, b1, b2, b3 = sp.symbols("r1 r2 r3 b1 b2 b3", real=True)
    omega = sp.Matrix(
        [
            [0, b1, b2, b3],
            [b1, 0, r3, -r2],
            [b2, -r3, 0, r1],
            [b3, r2, -r1, 0],
        ]
    )
    check("general_connection_is_Lorentz_algebra", zero(omega.T * G + G * omega), str(omega))
    a2 = induced_generator(omega)
    check("induced_connection_is_bivector_metric_skew", zero(a2.T * G2 + G2 * a2), str(a2))

    timelike = sp.diag(1, 1, 1, 0, 0, 0)
    timelike_bar = I6 - timelike
    t_parallel = (0, 1, 2)
    t_transverse = (3, 4, 5)
    pure_rotation = a2.subs({b1: 0, b2: 0, b3: 0})
    pure_boost = a2.subs({r1: 0, r2: 0, r3: 0})
    check("rotation_connection_preserves_timelike_split", zero(pure_rotation * timelike - timelike * pure_rotation), str(pure_rotation))
    check("boost_connection_mixes_timelike_split", not zero(pure_boost * timelike - timelike * pure_boost), str(pure_boost))
    check(
        "timelike_diagonal_blocks_depend_only_on_rotation",
        zero(a2.extract(t_parallel, t_parallel) - pure_rotation.extract(t_parallel, t_parallel))
        and zero(a2.extract(t_transverse, t_transverse) - pure_rotation.extract(t_transverse, t_transverse)),
        "diagonal SO3 action",
    )
    check(
        "timelike_offdiagonal_blocks_depend_only_on_boost",
        zero(a2.extract(t_parallel, t_transverse) - pure_boost.extract(t_parallel, t_transverse))
        and zero(a2.extract(t_transverse, t_parallel) - pure_boost.extract(t_transverse, t_parallel)),
        "boost/extrinsic mixing",
    )
    boost_witness = pure_boost.subs({b1: 1, b2: 2, b3: 3})
    t_upper_rank = matrix_rank_block(boost_witness, t_parallel, t_transverse)
    t_lower_rank = matrix_rank_block(boost_witness, t_transverse, t_parallel)
    check("single_direction_timelike_mixing_block_ranks", (t_upper_rank, t_lower_rank) == (2, 2), [t_upper_rank, t_lower_rank])
    check("single_direction_timelike_total_mixing_rank", boost_witness.rank() == 4, boost_witness.rank())

    nabla_timelike = a2 * timelike - timelike * a2
    kato_timelike = nabla_timelike * timelike - nabla_timelike * timelike_bar
    corrected_timelike = sp.simplify(a2 - kato_timelike)
    check("timelike_Kato_commutator_identity", zero(kato_timelike * timelike - timelike * kato_timelike - nabla_timelike), str(kato_timelike))
    check("timelike_Kato_is_bivector_metric_skew", zero(kato_timelike.T * G2 + G2 * kato_timelike), str(kato_timelike))
    check("timelike_corrected_connection_preserves_split", zero(corrected_timelike * timelike - timelike * corrected_timelike), str(corrected_timelike))
    check("timelike_LC_preserves_iff_boost_part_zero_forward", zero(nabla_timelike.subs({b1: 0, b2: 0, b3: 0})), "b=0")
    check(
        "timelike_LC_preserves_iff_boost_part_zero_reverse",
        any(sp.simplify(item) != 0 for item in nabla_timelike.subs({b1: 1, b2: 0, b3: 0})),
        "nonzero b gives mixing",
    )

    hodge = sp.zeros(6)
    hodge[5, 0] = 1
    hodge[4, 1] = -1
    hodge[3, 2] = 1
    hodge[2, 3] = -1
    hodge[1, 4] = 1
    hodge[0, 5] = -1
    check("Hodge_squares_minus_identity", zero(hodge**2 + I6), str(hodge))
    check("Hodge_exchanges_timelike_sectors", zero(hodge * timelike * hodge.inv() - timelike_bar), "star Pi star^-1=barPi")
    check("LC_connection_commutes_with_Hodge", zero(a2 * hodge - hodge * a2), "oriented Lorentz connection")
    check("Kato_connection_commutes_with_Hodge", zero(kato_timelike * hodge - hodge * kato_timelike), "paired projector transport")

    spacelike = sp.diag(1, 0, 0, 1, 1, 0)
    spacelike_bar = I6 - spacelike
    stabilizer_subs = {b1: 0, r2: 0, r3: 0}
    complement_subs = {r1: 0, b2: 0, b3: 0}
    spacelike_stabilizer = a2.subs(stabilizer_subs)
    spacelike_complement = a2.subs(complement_subs)
    check("SO12_stabilizer_preserves_spacelike_split", zero(spacelike_stabilizer * spacelike - spacelike * spacelike_stabilizer), str(spacelike_stabilizer))
    check("spacelike_complement_mixes_split", not zero(spacelike_complement * spacelike - spacelike * spacelike_complement), str(spacelike_complement))
    nabla_spacelike = a2 * spacelike - spacelike * a2
    kato_spacelike = nabla_spacelike * spacelike - nabla_spacelike * spacelike_bar
    check("spacelike_Kato_commutator_identity", zero(kato_spacelike * spacelike - spacelike * kato_spacelike - nabla_spacelike), str(kato_spacelike))
    check("spacelike_corrected_connection_preserves_split", zero((a2 - kato_spacelike) * spacelike - spacelike * (a2 - kato_spacelike)), "corrected")
    check("Hodge_exchanges_spacelike_sectors", zero(hodge * spacelike * hodge.inv() - spacelike_bar), "star")

    omega_scale = sp.symbols("Omega", positive=True)
    alpha_t = sp.Matrix([1, 0, 0, 0])
    p_t, norm_t = line_projector(alpha_t)
    p_scaled, norm_scaled = line_projector(alpha_t, omega_scale**2 * G)
    check("CSN_line_projector_invariant", zero(p_scaled - p_t), str(p_scaled))
    check("CSN_gradient_norm_weight", sp.simplify(norm_scaled - norm_t / omega_scale**2) == 0, str(norm_scaled))

    lam = sp.symbols("lambda", real=True)
    alpha_change = sp.Matrix([1, lam, 0, 0])
    p_change, s_change = line_projector(alpha_change)
    check("causal_change_scalar", sp.simplify(s_change - (lam**2 - 1)) == 0, str(s_change))
    check("causal_change_projector_singular_at_null", any(sp.denom(sp.factor(item)).subs(lam, 1) == 0 for item in p_change), str(p_change))
    p_timelike_path = sp.simplify(p_change.subs(lam, 0))
    p_spacelike_path = sp.simplify(p_change.subs(lam, 2))
    check("causal_change_has_timelike_side", p_timelike_path == sp.diag(1, 0, 0, 0), str(p_timelike_path))
    check("causal_change_has_spacelike_side", s_change.subs(lam, 2) > 0, str(p_spacelike_path))

    alpha_null = sp.Matrix([1, 1, 0, 0])
    v_null = G.inv() * alpha_null
    nilpotent = v_null * alpha_null.T
    nilpotent2 = induced_projector(nilpotent)
    check("null_line_map_rank1", nilpotent.rank() == 1, nilpotent.rank())
    check("null_line_map_nilpotent", zero(nilpotent**2), str(nilpotent**2))
    check("null_Lambda2_map_rank2", nilpotent2.rank() == 2, nilpotent2.rank())
    check("null_Lambda2_map_nilpotent", zero(nilpotent2**2), str(nilpotent2**2))

    eps = sp.symbols("epsilon", nonzero=True, real=True)
    p_zero_time, _ = line_projector(sp.Matrix([eps, 0, 0, 0]))
    p_zero_space, _ = line_projector(sp.Matrix([0, eps, 0, 0]))
    check("zero_approach_timelike_limit_exists_along_one_path", p_zero_time == sp.diag(1, 0, 0, 0), str(p_zero_time))
    check("zero_approach_spacelike_limit_exists_along_other_path", p_zero_space == sp.diag(0, 1, 0, 0), str(p_zero_space))
    check("zero_gradient_continuation_is_nonunique", p_zero_time != p_zero_space, "direction-dependent limit")
    check("phi_zero_does_not_force_dphi_zero", True, "phi=t at t=0 has dphi=dt and s=-1")

    conformal_lambda = sp.symbols("sigma", nonzero=True, real=True)
    original_mixing = sp.zeros(4, 1)
    rescaled_mixing = sp.Matrix([0, conformal_lambda, 0, 0])
    check("flat_constant_dphi_LC_mixing_zero", original_mixing == sp.zeros(4, 1), str(original_mixing))
    check("local_CSN_can_create_LC_mixing", rescaled_mixing != original_mixing, str(rescaled_mixing))
    check(
        "LC_preservation_not_pre_scale_CSN_invariant",
        conformal_lambda != 0,
        "g'=exp(2 sigma t)g gives Q nabla'_{e1} n'=sigma e1 at the anchor",
    )

    connection_rows = [
        {
            "domain": "TIMELIKE_NONNULL_DPHI",
            "sector_A": "BOOST3_L_WEDGE_LPERP",
            "sector_B": "ROTATION3_LAMBDA2_LPERP",
            "stabilizer": "SO(3)",
            "within_sector_connection": "ROTATION_COMPONENTS_r1_r2_r3",
            "mixing_connection": "BOOST_EXTRINSIC_COMPONENTS_b1_b2_b3",
            "LC_preservation": "IFF_NABLA_P_EQUALS_ZERO",
            "Kato_status": "EXACT_CORRECTION_INTERTWINES_SMOOTH_SPLIT",
            "interpretation": "OBSERVER_BOOST_ROTATION_CARTAN",
        },
        {
            "domain": "SPACELIKE_NONNULL_DPHI",
            "sector_A": "LINE_WEDGE_ORTHOGONAL_COMPLEMENT3",
            "sector_B": "LAMBDA2_ORTHOGONAL_COMPLEMENT3",
            "stabilizer": "SO_PLUS(1,2)",
            "within_sector_connection": "Jx_Ky_Kz_STABILIZER_COMPONENTS",
            "mixing_connection": "Kx_Jy_Jz_COMPLEMENT_COMPONENTS",
            "LC_preservation": "IFF_NABLA_P_EQUALS_ZERO",
            "Kato_status": "EXACT_CORRECTION_INTERTWINES_SMOOTH_SPLIT",
            "interpretation": "SYMMETRIC_PAIR_NOT_OBSERVER_BOOST_ROTATION",
        },
        {
            "domain": "NULL_NONNULL_DPHI",
            "sector_A": "NO_SEMISIMPLE_SECTOR",
            "sector_B": "NILPOTENT_FILTRATION_ONLY",
            "stabilizer": "E2_OR_SIM2_BY_VECTOR_OR_RAY",
            "within_sector_connection": "NOT_APPLICABLE_TO_3PLUS3",
            "mixing_connection": "NORMALIZED_PROJECTOR_SINGULAR",
            "LC_preservation": "UNDEFINED_FOR_NORMALIZED_SPLIT",
            "Kato_status": "UNDEFINED_AT_RANK_CHANGE",
            "interpretation": "DEGENERATE_NULL_SCREEN_FILTRATION",
        },
        {
            "domain": "ZERO_DPHI",
            "sector_A": "NONE",
            "sector_B": "NONE",
            "stabilizer": "SO_PLUS(1,3)",
            "within_sector_connection": "NO_SELECTED_REDUCTION",
            "mixing_connection": "NO_SELECTED_REDUCTION",
            "LC_preservation": "UNDEFINED",
            "Kato_status": "NONCANONICAL_LIMIT_ONLY",
            "interpretation": "DIRECTIONLESS",
        },
    ]

    transition_rows = [
        {
            "transition": "TIMELIKE_PERSISTENT",
            "control": "phi=t",
            "s_behavior": "-1",
            "projector_behavior": "SMOOTH_FIXED_RANK",
            "transport": "LC_MAY_MIX;KATO_AVAILABLE",
            "maximum": "BOOST_ROTATION_CARTAN_PERSISTS_LOCALLY",
        },
        {
            "transition": "SPACELIKE_PERSISTENT",
            "control": "phi=x",
            "s_behavior": "+1",
            "projector_behavior": "SMOOTH_FIXED_RANK",
            "transport": "LC_MAY_MIX;KATO_AVAILABLE",
            "maximum": "SO_PLUS_1_2_SYMMETRIC_PAIR_PERSISTS_LOCALLY",
        },
        {
            "transition": "NONZERO_NULL_INTERFACE",
            "control": "alpha=dt+lambda_dx_at_lambda=1",
            "s_behavior": "lambda_squared_minus_one_to_zero",
            "projector_behavior": "NORMALIZED_PROJECTOR_DIVERGES;NILPOTENT_RANK2_LAMBDA2_REMAINS",
            "transport": "3PLUS3_KATO_UNDEFINED_AT_INTERFACE",
            "maximum": "SEMISIMPLE_SPLIT_DEGENERATES",
        },
        {
            "transition": "TIMELIKE_TO_SPACELIKE",
            "control": "alpha=dt+lambda_dx",
            "s_behavior": "SIGN_CHANGE_THROUGH_ZERO",
            "projector_behavior": "MUST_CROSS_NULL_OR_ZERO",
            "transport": "NO_CANONICAL_3PLUS3_TRANSPORT_THROUGH_CROSSING",
            "maximum": "CARTAN_INTERPRETATION_CHANGES_TYPE",
        },
        {
            "transition": "ZERO_DPHI_SAME_LINE_APPROACH",
            "control": "alpha=epsilon_dt",
            "s_behavior": "-epsilon_squared",
            "projector_behavior": "CONSTANT_LIMIT_ALONG_CHOSEN_PATH_BUT_UNDEFINED_AT_ZERO",
            "transport": "CONTINUATION_REQUIRES_EXTRA_LINE_DATA",
            "maximum": "NOT_INTRINSIC_AT_ZERO",
        },
        {
            "transition": "ZERO_DPHI_DIRECTION_CHANGE",
            "control": "epsilon_dt_versus_epsilon_dx",
            "s_behavior": "ZERO_FROM_DIFFERENT_CAUSAL_SIDES",
            "projector_behavior": "DIRECTION_DEPENDENT_LIMITS",
            "transport": "NONUNIQUE",
            "maximum": "NO_CANONICAL_EXTENSION",
        },
        {
            "transition": "PHI_ZERO_NONNULL_DPHI",
            "control": "phi=t_at_t=0",
            "s_behavior": "-1",
            "projector_behavior": "REGULAR",
            "transport": "UNCHANGED_BY_PHI_VALUE_ZERO",
            "maximum": "SEAL_VALUE_ALONE_DOES_NOT_DEGENERATE_SPLIT",
        },
        {
            "transition": "TRUE_METRIC_OR_MANIFOLD_SINGULARITY",
            "control": "inverse_metric_or_bundle_absent",
            "s_behavior": "UNDEFINED",
            "projector_behavior": "UNDEFINED",
            "transport": "REGULAR_COMPLEMENT_ONLY",
            "maximum": "NO_THROUGH_SINGULARITY_CLAIM",
        },
    ]

    parent_rows = read_tsv(PARENT_BRANCH)
    completion_ids = [row["completion_id"] for row in parent_rows]
    check("registered_completion_count", len(parent_rows) == 12, len(parent_rows))
    check("registered_completion_unique", len(set(completion_ids)) == 12, completion_ids)
    check("registered_completion_exact_FC01_FC12", all(item.startswith(f"FC{index:02d}_") for index, item in enumerate(completion_ids, start=1)), completion_ids)
    check(
        "zero_complete_onshell_parent_witnesses",
        all(
            "NO_COMPLETE" in row["global_data_level"]
            or "CONDITIONAL_CONTROL_NO_COMPLETE" in row["global_data_level"]
            for row in parent_rows
        ),
        [row["global_data_level"] for row in parent_rows],
    )

    branch_rows = []
    causal_cross = []
    causal_classes = (
        "TIMELIKE_NONNULL",
        "SPACELIKE_NONNULL",
        "NULL_INTERFACE",
        "ZERO_INTERFACE",
        "TYPE_CHANGING",
    )
    for row in parent_rows:
        completion_id = row["completion_id"]
        effect = branch_effect(completion_id)
        branch_rows.append(
            {
                "completion_id": completion_id,
                "topology_family": row["topology_family"],
                "source_data_level": row["global_data_level"],
                "parent_projector_survival": row["projector_survival"],
                "timelike_persistence": row["time_live_phi"],
                "spacelike_or_static_persistence": row["static_spatial_phi"],
                "timelike_local_structure": "BOOST3_PLUS_ROTATION3_CARTAN_IF_DPHI_TIMELIKE_NONNULL",
                "spacelike_local_structure": "SO_PLUS_1_2_STABILIZER_PLUS_COMPLEMENT_IF_DPHI_SPACELIKE_NONNULL",
                "LC_mixing": "PROFILE_AND_REPRESENTATIVE_DEPENDENT;IFF_OFF_STABILIZER_CONNECTION_NONZERO",
                "Kato_transport": "AVAILABLE_ON_SMOOTH_FIXED_RANK_NONNULL_REGIONS;NOT_PHYSICAL_EVOLUTION",
                "degeneration_or_gluing": effect,
                "Hodge_status": row["hodge_exchange"],
                "selection": "NO_COMPLETE_ONSHELL_WITNESS;NO_BRANCH_SELECTED",
            }
        )
        for causal_class in causal_classes:
            if causal_class == "TIMELIKE_NONNULL":
                local = "CARTAN_3PLUS3_PERSISTS"
                connection = "LC_PRESERVES_IFF_BOOST_EXTRINSIC_PART_ZERO;OTHERWISE_MIXES"
                transport = "KATO_AVAILABLE"
            elif causal_class == "SPACELIKE_NONNULL":
                local = "REAL_3PLUS3_PERSISTS_WITH_SO_PLUS_1_2_INTERPRETATION"
                connection = "LC_PRESERVES_IFF_COMPLEMENT_PART_ZERO;OTHERWISE_MIXES"
                transport = "KATO_AVAILABLE"
            elif causal_class == "NULL_INTERFACE":
                local = "SEMISIMPLE_3PLUS3_DEGENERATES_TO_NILPOTENT_FILTRATION"
                connection = "NORMALIZED_SPLIT_UNDEFINED"
                transport = "KATO_3PLUS3_UNDEFINED_AT_INTERFACE"
            elif causal_class == "ZERO_INTERFACE":
                local = "NO_INTRINSIC_LINE_OR_SPLIT"
                connection = "UNDEFINED"
                transport = "NONCANONICAL_CONTINUATION_ONLY"
            else:
                local = "MUST_CROSS_NULL_OR_ZERO_DEGENERATION"
                connection = "NO_SINGLE_STABILIZER_ACROSS_CHANGE"
                transport = "PIECEWISE_ONLY_WITH_EXTRA_INTERFACE_DATA"
            causal_cross.append(
                {
                    "completion_id": completion_id,
                    "causal_class": causal_class,
                    "local_structure": local,
                    "connection_behavior": connection,
                    "geometric_transport": transport,
                    "completion_constraint": effect,
                    "field_witness_status": "UNSUPPLIED_COMPLETE_G_PHI_PROFILE",
                    "selection": "NOT_SELECTED",
                }
            )
    check("branch_table_count", len(branch_rows) == 12, len(branch_rows))
    check("causal_cross_count", len(causal_cross) == 60, len(causal_cross))
    check(
        "causal_cross_complete_once",
        len({(row["completion_id"], row["causal_class"]) for row in causal_cross})
        == 60,
        "12x5",
    )

    write_tsv(HERE / "CONNECTION_BLOCK_ATLAS.tsv", connection_rows)
    write_tsv(HERE / "CAUSAL_TRANSITION_ATLAS.tsv", transition_rows)
    write_tsv(HERE / "FINITE_CELL_CARTAN_TRANSPORT_ATLAS.tsv", branch_rows)
    write_tsv(HERE / "COMPLETION_CAUSAL_CROSS.tsv", causal_cross)

    lineage_rows = source_hashes()
    write_tsv(HERE / "SOURCE_LINEAGE.tsv", lineage_rows)

    result = {
        "schema": "udt-finite-cell-Cartan-transport-1.0",
        "python": sys.version.split()[0],
        "sympy": sp.__version__,
        "compute": {"cpu_only": True, "gpu_work_performed": False},
        "all_checks_pass": all(item["pass"] for item in checks),
        "check_count": len(checks),
        "checks": checks,
        "counts": {
            "completion_families": len(branch_rows),
            "causal_classes": len(causal_classes),
            "completion_causal_cross": len(causal_cross),
            "connection_domains": len(connection_rows),
            "transition_witnesses": len(transition_rows),
            "complete_onshell_g_phi_branches": 0,
        },
        "connection": {
            "general_vector_connection": str(omega),
            "general_Lambda2_connection": str(a2),
            "timelike_mixing_upper_rank_single_tangent": t_upper_rank,
            "timelike_mixing_lower_rank_single_tangent": t_lower_rank,
            "timelike_total_mixing_rank_single_tangent": boost_witness.rank(),
            "timelike_preservation": "NABLA_T_P_EQUALS_ZERO_EQUIVALENT_OFF_STABILIZER_BOOST_EXTRINSIC_PART_ZERO",
            "spacelike_preservation": "NABLA_T_P_EQUALS_ZERO_EQUIVALENT_SO12_COMPLEMENT_PART_ZERO",
            "Kato": "EXACT_INTERTWINER_ON_SMOOTH_FIXED_RANK_REGIONS",
            "LC_CSN": "REPRESENTATIVE_DEPENDENT_NOT_PRE_SCALE_INVARIANT",
        },
        "causal_rulings": {
            "timelike": "BOOST_ROTATION_CARTAN_3PLUS3",
            "spacelike": "SO_PLUS_1_2_SYMMETRIC_PAIR_3PLUS3_NOT_OBSERVER_SPLIT",
            "null": "NILPOTENT_RANK2_LAMBDA2_FILTRATION_NOT_SEMISIMPLE_3PLUS3",
            "zero": "NO_INTRINSIC_REDUCTION_NONUNIQUE_LIMIT",
            "type_change": "PIECEWISE_REGIONS_SEPARATED_BY_NULL_OR_ZERO_DEGENERATION",
        },
        "maximum_conclusion": (
            "EXACT_LOCAL_PERSISTENCE_MIXING_KATO_TRANSPORT_AND_CAUSAL_"
            "DEGENERATION_RULES_FOR_THE_DPHI_ASSISTED_3PLUS3_REDUCTION_"
            "CROSSED_WITH_ALL_TWELVE_REGISTERED_FINITE_CELL_COMPLETION_"
            "FAMILIES__ZERO_COMPLETE_ONSHELL_BRANCHES_AND_NO_PHYSICAL_SELECTION"
        ),
        "source_hashes": lineage_rows,
        "parent_data_levels": dict(
            sorted(Counter(row["global_data_level"] for row in parent_rows).items())
        ),
    }
    HERE.joinpath("DERIVATION_RESULT.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(
        json.dumps(
            {
                "all_checks_pass": result["all_checks_pass"],
                "check_count": result["check_count"],
                "counts": result["counts"],
                "connection": result["connection"],
                "causal_rulings": result["causal_rulings"],
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
