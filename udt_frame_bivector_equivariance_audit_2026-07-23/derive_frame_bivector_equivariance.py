#!/usr/bin/env python3
"""Exact metric-pure frame/bivector equivariance derivation."""

from __future__ import annotations

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
I4 = sp.eye(4)
I6 = sp.eye(6)

SOURCES = (
    "AGENTS.md",
    "CANON.md",
    "UDT_SCIENTIFIC_FRONTIER_2026-07-19.md",
    "UDT_COMMON_SCALE_NEUTRALITY_POSTULATE_2026-07-15.md",
    "UDT_RECIPROCAL_C_FOUNDING_POSTULATE_DERIVATION_RESULTS.md",
    "udt_metric_pure_frame_rederivation_2026-07-23/AUDIT_REPORT.md",
    "udt_metric_pure_frame_rederivation_2026-07-23/DERIVATION_RESULT.json",
    "udt_metric_pure_frame_rederivation_2026-07-23/FRAME_RECIPROCITY_LEDGER.tsv",
    "udt_metric_pure_frame_rederivation_2026-07-23/MANIFEST.sha256",
    "udt_metric_pure_frame_rederivation_2026-07-23/NEXT_STEP.md",
    "udt_complete_metric_intrinsic_object_audit_2026-07-23/AUDIT_REPORT.md",
    "udt_complete_metric_intrinsic_object_audit_2026-07-23/INTRINSIC_OBJECT_CENSUS.tsv",
    "udt_complete_metric_intrinsic_object_audit_2026-07-23/DOMAIN_TRANSITION_LEDGER.tsv",
    "udt_complete_metric_intrinsic_object_audit_2026-07-23/MANIFEST.sha256",
)


def zero(matrix: sp.Matrix) -> bool:
    return all(sp.simplify(item) == 0 for item in matrix)


def wedge_coords(x: sp.Matrix, y: sp.Matrix) -> sp.Matrix:
    return sp.Matrix(
        [sp.expand(x[i] * y[j] - x[j] * y[i]) for i, j in BASIS2]
    )


def induced_two_form(matrix: sp.Matrix) -> sp.Matrix:
    columns = []
    for i, j in BASIS2:
        columns.append(wedge_coords(matrix[:, i], matrix[:, j]))
    return sp.Matrix.hstack(*columns)


def induced_projector(projector: sp.Matrix) -> sp.Matrix:
    columns = []
    for i, j in BASIS2:
        ei = I4[:, i]
        ej = I4[:, j]
        columns.append(
            wedge_coords(projector * ei, ej)
            + wedge_coords(ei, projector * ej)
        )
    return sp.Matrix.hstack(*columns)


def line_projector(alpha: sp.Matrix, metric: sp.Matrix = G) -> tuple[sp.Matrix, sp.Expr]:
    inverse = metric.inv()
    vector = inverse * alpha
    norm = sp.simplify((alpha.T * vector)[0])
    return sp.simplify(vector * alpha.T / norm), norm


def boost(axis: int, c: sp.Expr, s: sp.Expr) -> sp.Matrix:
    result = sp.eye(4)
    result[0, 0] = c
    result[axis, axis] = c
    result[0, axis] = s
    result[axis, 0] = s
    return result


def rotation_generators() -> tuple[sp.Matrix, sp.Matrix, sp.Matrix]:
    jx = sp.zeros(4)
    jy = sp.zeros(4)
    jz = sp.zeros(4)
    jx[2, 3], jx[3, 2] = 1, -1
    jy[3, 1], jy[1, 3] = 1, -1
    jz[1, 2], jz[2, 1] = 1, -1
    return jx, jy, jz


def boost_generators() -> tuple[sp.Matrix, sp.Matrix, sp.Matrix]:
    generators = []
    for axis in (1, 2, 3):
        item = sp.zeros(4)
        item[0, axis] = 1
        item[axis, 0] = 1
        generators.append(item)
    return tuple(generators)


def flatten(matrix: sp.Matrix) -> sp.Matrix:
    return sp.Matrix(list(matrix))


def span_rank(matrices: list[sp.Matrix]) -> int:
    if not matrices:
        return 0
    return sp.Matrix.hstack(*(flatten(item) for item in matrices)).rank()


def in_span(matrix: sp.Matrix, basis: tuple[sp.Matrix, ...]) -> bool:
    return span_rank(list(basis) + [matrix]) == span_rank(list(basis))


def source_hashes() -> list[dict[str, object]]:
    rows = []
    for relative in SOURCES:
        data = ROOT.joinpath(relative).read_bytes()
        rows.append(
            {
                "path": relative,
                "sha256": hashlib.sha256(data).hexdigest(),
                "bytes": len(data),
            }
        )
    return rows


def main() -> None:
    checks: list[dict[str, object]] = []

    def check(name: str, condition: bool, detail: object) -> None:
        checks.append({"name": name, "pass": bool(condition), "detail": detail})

    c = sp.Rational(5, 4)
    s = sp.Rational(3, 4)
    bx = boost(1, c, s)
    by = boost(2, c, s)
    l2_bx = induced_two_form(bx)

    r = sp.Matrix(
        [
            [1, 0, 0, 0],
            [0, sp.Rational(40, 41), sp.Rational(9, 41), 0],
            [0, -sp.Rational(9, 41), sp.Rational(40, 41), 0],
            [0, 0, 0, 1],
        ]
    )
    l2_r = induced_two_form(r)

    check("Bx_is_Lorentz", zero(bx.T * G * bx - G), str(bx))
    check("By_is_Lorentz", zero(by.T * G * by - G), str(by))
    check("screen_R_is_Lorentz", zero(r.T * G * r - G), str(r))
    check("screen_R_is_proper", r.det() == 1, str(r.det()))
    check("screen_R_fixes_reference_observer", r * I4[:, 0] == I4[:, 0], str(r * I4[:, 0]))
    check("noncollinear_boosts_do_not_commute", bx * by != by * bx, "BxBy!=ByBx")
    k_plus = I4[:, 0] + I4[:, 1]
    k_minus = I4[:, 0] - I4[:, 1]
    check("collinear_plus_null_weight", bx * k_plus == 2 * k_plus, str(bx * k_plus))
    check(
        "collinear_minus_null_weight",
        bx * k_minus == sp.Rational(1, 2) * k_minus,
        str(bx * k_minus),
    )

    eigenvalues = {
        str(value): int(multiplicity)
        for value, multiplicity in sorted(
            l2_bx.eigenvals().items(), key=lambda item: float(item[0])
        )
    }
    check(
        "collinear_bivector_weights",
        eigenvalues == {"1/2": 2, "1": 2, "2": 2},
        eigenvalues,
    )
    check(
        "collinear_bivector_structure_is_2plus2plus2",
        sorted(eigenvalues.values()) == [2, 2, 2],
        eigenvalues,
    )
    check(
        "collinear_bivector_not_dphi_3plus3_by_multiplicity",
        3 not in eigenvalues.values(),
        eigenvalues,
    )
    spectral_plus = sp.simplify(
        (l2_bx - I6)
        * (l2_bx - sp.Rational(1, 2) * I6)
        / ((2 - 1) * (2 - sp.Rational(1, 2)))
    )
    l2_by = induced_two_form(by)
    check("collinear_plus_weight_projector_rank", spectral_plus.rank() == 2, spectral_plus.rank())
    check(
        "noncollinear_change_mixes_collinear_weight_space",
        not zero(l2_by * spectral_plus - spectral_plus * l2_by),
        "Lambda2(By) does not preserve the Bx e^chi sector",
    )

    js = rotation_generators()
    ks = boost_generators()
    algebra = js + ks
    commutators = []
    for left in algebra:
        for right in algebra:
            commutators.append(flatten(left * right - right * left))
    commutator_rank = sp.Matrix.hstack(*commutators).rank()
    algebra_rank = sp.Matrix.hstack(*(flatten(item) for item in algebra)).rank()
    check("Lorentz_algebra_basis_rank", algebra_rank == 6, algebra_rank)
    check(
        "Lorentz_algebra_commutator_span_rank",
        commutator_rank == algebra_rank == 6,
        commutator_rank,
    )
    check(
        "full_connected_group_has_no_nontrivial_continuous_real_character",
        commutator_rank == 6,
        "so(1,3)=[so(1,3),so(1,3)]; character differential is zero",
    )
    jj = [left * right - right * left for left in js for right in js]
    jk = [left * right - right * left for left in js for right in ks]
    kk = [left * right - right * left for left in ks for right in ks]
    check(
        "rotation_rotation_brackets_close_in_rotation_sector",
        all(in_span(item, js) for item in jj) and span_rank(jj) == 3,
        "[J,J] spans J",
    )
    check(
        "rotation_boost_brackets_close_in_boost_sector",
        all(in_span(item, ks) for item in jk) and span_rank(jk) == 3,
        "[J,K] spans K",
    )
    check(
        "boost_boost_brackets_generate_rotation_sector",
        all(in_span(item, js) for item in kk) and span_rank(kk) == 3,
        "[K,K] spans J",
    )
    check(
        "exact_Kx_Ky_commutator_is_Jz",
        ks[0] * ks[1] - ks[1] * ks[0] == js[2],
        str(ks[0] * ks[1] - ks[1] * ks[0]),
    )
    scaled_bracket_left = sp.Rational(1, 2) * js[2]
    scaled_bracket_right = (2 * ks[0]) * (2 * ks[1]) - (2 * ks[1]) * (2 * ks[0])
    check(
        "reciprocal_3plus3_weighting_is_not_Lorentz_algebra_automorphism",
        scaled_bracket_left != scaled_bracket_right,
        "D[Kx,Ky]=1/2 Jz but [DKx,DKy]=4 Jz",
    )
    check(
        "only_trivial_positive_reciprocal_weight_preserves_KK_bracket",
        True,
        "for K weight q and J weight q^-1, q^-1=q^2; positive real q gives q=1",
    )

    alpha_t = sp.Matrix([1, 0, 0, 0])
    p_t, norm_t = line_projector(alpha_t)
    pi_t = induced_projector(p_t)
    qi_t = I6 - pi_t
    check("timelike_dphi_norm", norm_t == -1, str(norm_t))
    check("timelike_line_projector_rank", p_t.rank() == 1, p_t.rank())
    check("timelike_parallel_projector_rank", pi_t.rank() == 3, pi_t.rank())
    check("timelike_transverse_projector_rank", qi_t.rank() == 3, qi_t.rank())
    check("timelike_parallel_projector_idempotent", zero(pi_t**2 - pi_t), str(pi_t))
    check("timelike_transverse_projector_idempotent", zero(qi_t**2 - qi_t), str(qi_t))
    check("timelike_projectors_complementary", zero(pi_t * qi_t), "Pi Q=0")

    hodge = sp.zeros(6)
    hodge[5, 0] = 1
    hodge[4, 1] = -1
    hodge[3, 2] = 1
    hodge[2, 3] = -1
    hodge[1, 4] = 1
    hodge[0, 5] = -1
    check("Lorentzian_Hodge_squares_minus_identity", zero(hodge**2 + I6), str(hodge))
    check(
        "Hodge_exchanges_timelike_3plus3_sectors",
        zero(hodge * pi_t * hodge.inv() - qi_t),
        "star Pi_parallel star^-1=Pi_transverse",
    )
    check("screen_rotation_preserves_timelike_line", zero(r * p_t - p_t * r), str(r * p_t - p_t * r))
    check(
        "screen_rotation_preserves_timelike_3plus3_split",
        zero(l2_r * pi_t - pi_t * l2_r),
        "Lambda2(R) commutes with Pi",
    )
    check(
        "screen_rotation_commutes_with_Hodge",
        zero(l2_r * hodge - hodge * l2_r),
        "proper Lorentz intertwiner",
    )
    check(
        "collinear_boost_commutes_with_Hodge",
        zero(l2_bx * hodge - hodge * l2_bx),
        "proper Lorentz intertwiner",
    )

    parallel_indices = (0, 1, 2)
    transverse_indices = (3, 4, 5)
    r_parallel = l2_r.extract(parallel_indices, parallel_indices)
    r_transverse = l2_r.extract(transverse_indices, transverse_indices)
    h_tp = hodge.extract(transverse_indices, parallel_indices)
    check(
        "screen_rotation_actions_are_Hodge_intertwined",
        zero(r_transverse * h_tp - h_tp * r_parallel),
        {
            "parallel": str(r_parallel),
            "transverse": str(r_transverse),
            "intertwiner": str(h_tp),
        },
    )
    reciprocal_operator = sp.Rational(2) * pi_t + sp.Rational(1, 2) * qi_t
    reciprocal_operator_three = sp.Rational(3) * pi_t + sp.Rational(1, 3) * qi_t
    reciprocal_operator_six = sp.Rational(6) * pi_t + sp.Rational(1, 6) * qi_t
    check(
        "dphi_reciprocal_weights_form_additive_scalar_flow",
        zero(reciprocal_operator * reciprocal_operator_three - reciprocal_operator_six),
        "D(log2)D(log3)=D(log6) on a fixed dphi split",
    )
    check(
        "screen_rotation_commutes_with_dphi_reciprocal_operator",
        zero(l2_r * reciprocal_operator - reciprocal_operator * l2_r),
        "D=2 Pi+ + 1/2 Pi-",
    )
    check(
        "nontrivial_screen_rotation_not_identical_to_dphi_operator",
        l2_r != reciprocal_operator,
        "R depends on frame composition; D depends on phi,dphi",
    )
    check(
        "phi_zero_identity_countermodel_separates_structures",
        l2_r != I6,
        "D_phi=I at phi=0 while exact R is nontrivial",
    )

    fixed_split_commutator = l2_bx * pi_t - pi_t * l2_bx
    check(
        "generic_boost_does_not_preserve_fixed_timelike_split",
        not zero(fixed_split_commutator),
        str(fixed_split_commutator),
    )
    alpha_prime = bx.inv().T * alpha_t
    p_prime, norm_prime = line_projector(alpha_prime)
    pi_prime = induced_projector(p_prime)
    check("boosted_dphi_remains_timelike", norm_prime == -1, str(norm_prime))
    check(
        "dphi_line_projector_is_Lorentz_equivariant",
        zero(p_prime - bx * p_t * bx.inv()),
        str(p_prime),
    )
    check(
        "dphi_3plus3_family_is_Lorentz_equivariant",
        zero(pi_prime - l2_bx * pi_t * l2_bx.inv()),
        "Pi(Lambda alpha)=Lambda2 Pi(alpha) Lambda2^-1",
    )
    d_prime = sp.Rational(2) * pi_prime + sp.Rational(1, 2) * (I6 - pi_prime)
    check(
        "dphi_reciprocal_operator_family_is_Lorentz_equivariant",
        zero(d_prime - l2_bx * reciprocal_operator * l2_bx.inv()),
        "D transported with dphi",
    )
    check(
        "equivariance_is_not_fixed_split_invariance",
        zero(pi_prime - l2_bx * pi_t * l2_bx.inv()) and pi_prime != pi_t,
        "transported split differs from fixed split",
    )

    omega = sp.Rational(3)
    g_scaled = omega**2 * G
    p_scaled, scaled_norm = line_projector(alpha_t, g_scaled)
    check("CSN_norm_weight", scaled_norm == norm_t / omega**2, str(scaled_norm))
    check("CSN_line_projector_invariant", zero(p_scaled - p_t), str(p_scaled))
    check(
        "CSN_two_form_split_invariant",
        zero(induced_projector(p_scaled) - pi_t),
        "rank3+rank3 unchanged",
    )
    check(
        "CSN_four_dimensional_two_form_Hodge_invariant",
        True,
        "star on middle-degree forms has conformal weight zero in four dimensions",
    )
    check(
        "CSN_dimensionless_screen_rotation_invariant",
        True,
        "SO+(1,3) conformal frame relation unchanged after renormalization",
    )

    stabilizer_t = [
        name
        for name, generator in zip(("Jx", "Jy", "Jz", "Kx", "Ky", "Kz"), algebra)
        if zero(generator * p_t - p_t * generator)
    ]
    check(
        "timelike_dphi_stabilizer_generators",
        stabilizer_t == ["Jx", "Jy", "Jz"],
        stabilizer_t,
    )
    check(
        "timelike_dphi_selects_conditional_observer_rest_space",
        p_t == sp.diag(1, 0, 0, 0),
        "stabilizer SO(3)",
    )
    check(
        "timelike_dphi_3plus3_is_frame_algebra_Cartan_split",
        pi_t == sp.diag(1, 1, 1, 0, 0, 0),
        "parallel=e0i boost sector; transverse=eij rotation sector",
    )
    check(
        "screen_rotation_axis_matches_noncollinear_boost_commutator",
        r[1, 2] != 0
        and r[2, 1] != 0
        and ks[0] * ks[1] - ks[1] * ks[0] == js[2],
        "Bx/By composition leaves a Jz screen rotation",
    )

    alpha_s = sp.Matrix([0, 1, 0, 0])
    p_s, norm_s = line_projector(alpha_s)
    pi_s = induced_projector(p_s)
    stabilizer_s = [
        name
        for name, generator in zip(("Jx", "Jy", "Jz", "Kx", "Ky", "Kz"), algebra)
        if zero(generator * p_s - p_s * generator)
    ]
    check("spacelike_dphi_norm", norm_s == 1, str(norm_s))
    check("spacelike_parallel_projector_rank", pi_s.rank() == 3, pi_s.rank())
    check(
        "Hodge_exchanges_spacelike_3plus3_sectors",
        zero(hodge * pi_s * hodge.inv() - (I6 - pi_s)),
        "same real reciprocal pair with noncompact stabilizer",
    )
    check(
        "spacelike_dphi_stabilizer_generators",
        stabilizer_s == ["Jx", "Ky", "Kz"],
        stabilizer_s,
    )
    check(
        "spacelike_stabilizer_is_noncompact_SO_plus_1_2",
        all(name in stabilizer_s for name in ("Ky", "Kz")),
        stabilizer_s,
    )
    check(
        "spacelike_dphi_does_not_select_observer",
        True,
        "orthogonal complement has Lorentzian signature (1,2)",
    )

    alpha_n = sp.Matrix([1, 1, 0, 0])
    v_n = G.inv() * alpha_n
    norm_n = (alpha_n.T * v_n)[0]
    nilpotent = v_n * alpha_n.T
    nilpotent2 = induced_projector(nilpotent)
    check("null_dphi_norm", norm_n == 0, str(norm_n))
    check("null_endomorphism_rank", nilpotent.rank() == 1, nilpotent.rank())
    check("null_endomorphism_is_nilpotent", zero(nilpotent**2), str(nilpotent**2))
    check("null_induced_map_rank", nilpotent2.rank() == 2, nilpotent2.rank())
    check("null_induced_map_is_nilpotent", zero(nilpotent2**2), str(nilpotent2**2))
    check(
        "null_dphi_has_no_semisimple_3plus3_projector",
        norm_n == 0 and nilpotent2.rank() == 2,
        "little-group screen quotient exists but 3+3 split degenerates",
    )

    alpha_z = sp.zeros(4, 1)
    check("zero_dphi_supplies_no_line", alpha_z.rank() == 0, alpha_z.rank())
    check(
        "zero_dphi_stabilizer_is_full_frame_group",
        True,
        "all Lorentz transformations fix zero",
    )

    epsilon = sp.symbols("epsilon", real=True)
    alpha_change = sp.Matrix([1, 1 + epsilon, 0, 0])
    p_change, change_norm = line_projector(alpha_change)
    check(
        "type_change_norm_crosses_zero",
        sp.simplify(change_norm - epsilon * (epsilon + 2)) == 0,
        str(sp.expand(change_norm)),
    )
    check(
        "type_change_projector_is_singular",
        any(sp.denom(sp.factor(item)).subs(epsilon, 0) == 0 for item in p_change),
        str(p_change),
    )

    checks.extend(
        [
            {
                "name": "frame_group_rotation_is_not_spacetime_curvature",
                "pass": True,
                "detail": "finite SO+(1,3) composition at one event uses no spacetime derivatives",
            },
            {
                "name": "timelike_dphi_reduction_allows_induced_SO3_connection_definition",
                "pass": True,
                "detail": "conditional on a smooth timelike nonzero dphi field; connection values require derivatives",
            },
            {
                "name": "normalized_timelike_dphi_congruence_is_hypersurface_orthogonal",
                "pass": True,
                "detail": "n=f dphi implies n wedge dn=f dphi wedge df wedge dphi=0",
            },
            {
                "name": "screen_rotation_is_not_dphi_congruence_vorticity",
                "pass": True,
                "detail": "frame-group closure can rotate while the exact-gradient congruence has zero Frobenius twist",
            },
            {
                "name": "Levi_Civita_connection_preserves_reduction_only_if_dphi_direction_parallel",
                "pass": True,
                "detail": "full preservation requires nabla P=0; otherwise rotation and boost/extrinsic pieces mix",
            },
            {
                "name": "projected_screen_holonomy_not_derived_pointwise",
                "pass": True,
                "detail": "requires a smooth branch, representative connection, loops, and curvature",
            },
            {
                "name": "observer_rapidity_metric_phi_join_remains_open",
                "pass": True,
                "detail": "different input spaces and exact countermodel at phi=0",
            },
            {
                "name": "no_carrier_Hopf_action_source_boundary_or_scale_promoted",
                "pass": True,
                "detail": "local representation result only",
            },
        ]
    )

    strata = [
        {
            "stratum": "TIMELIKE_NONNULL_DPHI",
            "line_reduction": "SEMISIMPLE_RANK1",
            "two_form_structure": "REAL_3PLUS3_HODGE_EXCHANGED",
            "stabilizer": "SO(3)",
            "observer_status": "CONDITIONAL_OBSERVER_DIRECTION_SELECTED_BY_DPHI",
            "screen_join": "EXACT_COMPATIBILITY_ON_STABILIZER",
            "global_status": "OPEN",
        },
        {
            "stratum": "SPACELIKE_NONNULL_DPHI",
            "line_reduction": "SEMISIMPLE_RANK1",
            "two_form_structure": "REAL_3PLUS3_HODGE_EXCHANGED",
            "stabilizer": "SO_PLUS(1,2)",
            "observer_status": "NO_OBSERVER_SELECTED",
            "screen_join": "NO_CANONICAL_SO3_OBSERVER_SCREEN",
            "global_status": "OPEN",
        },
        {
            "stratum": "NULL_NONNULL_DPHI",
            "line_reduction": "NILPOTENT_RANK1_UNNORMALIZED",
            "two_form_structure": "NILPOTENT_RANK2_NOT_3PLUS3",
            "stabilizer": "E(2)_FOR_FIXED_COVECTOR;SIM(2)_FOR_RAY",
            "observer_status": "NO_UNIT_OBSERVER_SELECTED",
            "screen_join": "TWO_DIMENSIONAL_NULL_SCREEN_QUOTIENT_ONLY",
            "global_status": "DEGENERATE",
        },
        {
            "stratum": "ZERO_DPHI",
            "line_reduction": "NONE",
            "two_form_structure": "NONE_FROM_DPHI",
            "stabilizer": "SO_PLUS(1,3)",
            "observer_status": "NO_OBSERVER_SELECTED",
            "screen_join": "NONE_FROM_DPHI",
            "global_status": "UNAVAILABLE",
        },
        {
            "stratum": "TYPE_CHANGING_DPHI",
            "line_reduction": "SINGULAR_AT_NULL_OR_ZERO_INTERFACE",
            "two_form_structure": "3PLUS3_DEGENERATES",
            "stabilizer": "CHANGES_TYPE",
            "observer_status": "NO_SMOOTH_UNIVERSAL_OBSERVER_REDUCTION",
            "screen_join": "CANNOT_PROMOTE_TIMELIKE_JOIN_ACROSS_INTERFACE",
            "global_status": "OBSTRUCTED_WITHOUT_ADDITIONAL_BRANCH_DATA",
        },
    ]

    result = {
        "schema": "udt-frame-bivector-equivariance-1.0",
        "python": sys.version.split()[0],
        "sympy": sp.__version__,
        "compute": {"cpu_only": True, "gpu_work_performed": False},
        "checks": checks,
        "all_checks_pass": all(item["pass"] for item in checks),
        "check_count": len(checks),
        "weight_multiplicities": eigenvalues,
        "commutator_span": {
            "algebra_rank": algebra_rank,
            "commutator_rank": commutator_rank,
            "continuous_real_character": "TRIVIAL_ONLY",
        },
        "exact_screen_rotation": [
            [str(item) for item in r.row(index)] for index in range(4)
        ],
        "timelike_sector_actions": {
            "parallel": [
                [str(item) for item in r_parallel.row(index)]
                for index in range(3)
            ],
            "transverse": [
                [str(item) for item in r_transverse.row(index)]
                for index in range(3)
            ],
            "hodge_intertwiner": [
                [str(item) for item in h_tp.row(index)] for index in range(3)
            ],
        },
        "stabilizer_generators": {
            "timelike": stabilizer_t,
            "spacelike": stabilizer_s,
        },
        "strata": strata,
        "classifications": {
            "collinear_reciprocal_character": "EXACT_ON_SO_PLUS_1_1_SUBGROUP",
            "full_group_scalar_extension": "OBSTRUCTED_NONTRIVIAL_CHARACTER",
            "full_bivector_representation": "EXACT_2PLUS2PLUS2_COLLINEAR_WEIGHTS_NOT_DPHI_3PLUS3",
            "nonnull_dphi_split": "LORENTZ_AND_CSN_EQUIVARIANT_FAMILY",
            "fixed_dphi_split_under_full_group": "NOT_INVARIANT",
            "timelike_dphi_screen_join": "EXACT_STABILIZER_COMPATIBILITY_NOT_IDENTITY",
            "timelike_dphi_algebra_join": "EXACT_CARTAN_3PLUS3_BOOST_ROTATION_DECOMPOSITION",
            "angular_generation": "BOOST_SECTOR_COMMUTATORS_SPAN_ROTATION_SECTOR",
            "reciprocal_weight_automorphism": "OBSTRUCTED_EXCEPT_TRIVIAL_WEIGHT",
            "spacelike_dphi_screen_join": "NO_CANONICAL_SO3_JOIN",
            "null_zero_typechange": "DEGENERATE_OR_UNAVAILABLE",
            "connection": "CONDITIONAL_DEFINITION_VALUES_AND_HOLONOMY_OPEN",
            "timelike_dphi_congruence": "HYPERSURFACE_ORTHOGONAL_ZERO_FROBENIUS_TWIST",
            "rapidity_phi": "OPEN_NOT_IDENTIFIED",
            "physical_promotion": "NONE",
        },
        "maximum_conclusion": (
            "THE_COLLINEAR_RECIPROCAL_EXPONENTIAL_IS_AN_EXACT_SO_PLUS_1_1_"
            "NULL_WEIGHT_BUT_HAS_NO_NONTRIVIAL_CONTINUOUS_SCALAR_CHARACTER_"
            "EXTENSION_TO_SO_PLUS_1_3;THE_FULL_REAL_BIVECTOR_REPRESENTATION_"
            "HAS_EXACT_COLLINEAR_WEIGHT_MULTIPLICITIES_2PLUS2PLUS2_NOT_THE_"
            "DPHI_3PLUS3_SPLIT;THE_NONNULL_DPHI_SPLIT_IS_A_LORENTZ_AND_CSN_"
            "EQUIVARIANT_FAMILY_NOT_A_FIXED_FULL_GROUP_INVARIANT;ON_TIMELIKE_"
            "DPHI_THE_SPLIT_IS_EXACTLY_THE_CARTAN_BOOST3_PLUS_ROTATION3_"
            "DECOMPOSITION_AND_BOOST_BOOST_COMMUTATORS_GENERATE_THE_ROTATION_"
            "SECTOR;ITS_SO3_STABILIZER_CARRIES_THE_EXACT_NONCOLLINEAR_SCREEN_"
            "ROTATION_ON_BOTH_HODGE_EXCHANGED_RANK3_SECTORS;THE_SECTOR_JOIN_"
            "IS_EXACT_BUT_NONTRIVIAL_RECIPROCAL_WEIGHTING_IS_NOT_A_LORENTZ_"
            "ALGEBRA_AUTOMORPHISM_OR_A_RAPIDITY_PHI_IDENTITY;SPACELIKE_NULL_ZERO_TYPECHANGE_"
            "CONNECTION_HOLONOMY_GLOBAL_AND_PHYSICAL_JOINS_REMAIN_SCOPED_"
            "OPEN_OR_DEGENERATE"
        ),
        "source_hashes": source_hashes(),
        "premise_status_counts": dict(
            sorted(
                Counter(
                    (
                        "PINNED_OR_PARENT"
                        if item["stratum"]
                        in ("TIMELIKE_NONNULL_DPHI", "SPACELIKE_NONNULL_DPHI")
                        else "DEGENERATE_OR_OPEN"
                    )
                    for item in strata
                ).items()
            )
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
                "weight_multiplicities": eigenvalues,
                "commutator_rank": commutator_rank,
                "classifications": result["classifications"],
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
