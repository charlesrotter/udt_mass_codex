#!/usr/bin/env python3
"""Exact G129 production derivation for observer-pair network faithfulness."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
COMPONENTS = (
    (0, 0), (0, 1), (0, 2), (0, 3), (1, 1),
    (1, 2), (1, 3), (2, 2), (2, 3), (3, 3),
)


def symmetric_matrix(values: list[sp.Rational]) -> sp.Matrix:
    matrix = sp.zeros(4)
    for value, (i, j) in zip(values, COMPONENTS, strict=True):
        matrix[i, j] = value
        matrix[j, i] = value
    return matrix


def restriction_rows(u: sp.Matrix, v: sp.Matrix) -> list[list[sp.Expr]]:
    rows: list[list[sp.Expr]] = []
    for left, right in ((u, u), (u, v), (v, v)):
        row = []
        for i, j in COMPONENTS:
            coefficient = left[i] * right[j]
            if i != j:
                coefficient += left[j] * right[i]
            row.append(sp.expand(coefficient))
        rows.append(row)
    return rows


def design_matrix(directions: list[sp.Matrix]) -> sp.Matrix:
    e0 = sp.Matrix([1, 0, 0, 0])
    return sp.Matrix([row for v in directions for row in restriction_rows(e0, v)])


def pullback(g: sp.Matrix, u: sp.Matrix, v: sp.Matrix) -> sp.Matrix:
    a = sp.Matrix.hstack(u, v)
    return sp.simplify(a.T * g * a)


def q(value: int, denominator: int = 1) -> sp.Rational:
    return sp.Rational(value, denominator)


def source_hashes_match() -> bool:
    with (HERE / "SOURCE_MANIFEST.tsv").open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
    for row in rows:
        payload = (ROOT / row["path"]).read_bytes()
        if hashlib.sha256(payload).hexdigest() != row["sha256"]:
            return False
    return True


def main() -> None:
    e1 = sp.Matrix([0, 1, 0, 0])
    e2 = sp.Matrix([0, 0, 1, 0])
    e3 = sp.Matrix([0, 0, 0, 1])
    axial = [e1, e2, e3]
    faithful = axial + [e1 + e2, e1 + e3, e2 + e3]

    families = {
        "one_axial_plane": [e1],
        "two_axial_planes": [e1, e2],
        "three_axial_planes": axial,
        "axial_plus_e1e2": axial + [e1 + e2],
        "axial_plus_e1e2_e1e3": axial + [e1 + e2, e1 + e3],
        "six_clock_ruler_planes": faithful,
    }
    atlas = []
    for name, directions in families.items():
        matrix = design_matrix(directions)
        atlas.append(
            {
                "family": name,
                "plane_count": len(directions),
                "row_count": matrix.rows,
                "rank": matrix.rank(),
                "kernel_dimension": 10 - matrix.rank(),
                "faithful": matrix.rank() == 10,
            }
        )

    g_values = [
        q(-4), q(1, 3), q(-1, 5), q(1, 7), q(3),
        q(1, 11), q(-1, 13), q(5), q(1, 17), q(7),
    ]
    g = symmetric_matrix(g_values)
    leading = [sp.factor(g[:i, :i].det()) for i in range(1, 5)]
    pivots = [leading[0]] + [sp.factor(leading[i] / leading[i - 1]) for i in range(1, 4)]
    lorentz_pivots = pivots[0] < 0 and all(value > 0 for value in pivots[1:])
    pair_metrics = [
        pullback(g, sp.Matrix([1, 0, 0, 0]), v) for v in faithful
    ]
    pair_metrics_regular = all(
        h[0, 0] < 0 and sp.factor(h.det()) < 0 for h in pair_metrics
    )

    full_design = design_matrix(faithful)
    measurements = full_design * sp.Matrix(g_values)
    reconstructed = sp.simplify(
        (full_design.T * full_design).inv() * full_design.T * measurements
    )
    reconstruction_exact = reconstructed == sp.Matrix(g_values)

    axial_design = design_matrix(axial)
    axial_nullspace = axial_design.nullspace()
    expected_invisible_positions = {5, 6, 8}
    null_support = {
        next(i for i, value in enumerate(vector) if value != 0)
        for vector in axial_nullspace
    }
    axial_kernel_exact = (
        axial_design.rank() == 7
        and len(axial_nullspace) == 3
        and null_support == expected_invisible_positions
    )

    invisible_values = [q(0)] * 10
    invisible_values[5] = q(1)
    invisible = symmetric_matrix(invisible_values)
    epsilon = q(1, 2)
    g_epsilon = g + epsilon * invisible
    axial_equal = all(
        pullback(g, sp.Matrix([1, 0, 0, 0]), v)
        == pullback(g_epsilon, sp.Matrix([1, 0, 0, 0]), v)
        for v in axial
    )
    leading_epsilon = [sp.factor(g_epsilon[:i, :i].det()) for i in range(1, 5)]
    pivots_epsilon = [leading_epsilon[0]] + [
        sp.factor(leading_epsilon[i] / leading_epsilon[i - 1]) for i in range(1, 4)
    ]
    epsilon_lorentz = pivots_epsilon[0] < 0 and all(value > 0 for value in pivots_epsilon[1:])
    faithful_detects = full_design * sp.Matrix(invisible_values) != sp.zeros(full_design.rows, 1)

    frame = sp.Matrix(
        [
            [1, q(1, 3), 0, 0],
            [0, 1, q(1, 5), 0],
            [0, 0, 1, q(1, 7)],
            [0, 0, 0, 1],
        ]
    )
    frame_inverse = frame.inv()
    g_new = sp.simplify(frame.T * g * frame)
    frame_covariant = True
    for v in faithful:
        a_old = sp.Matrix.hstack(sp.Matrix([1, 0, 0, 0]), v)
        a_new = frame_inverse * a_old
        frame_covariant &= sp.simplify(a_new.T * g_new * a_new - a_old.T * g * a_old) == sp.zeros(2)
    transformed_design = sp.Matrix(
        [
            row
            for v in faithful
            for row in restriction_rows(
                frame_inverse * sp.Matrix([1, 0, 0, 0]), frame_inverse * v
            )
        ]
    )
    frame_rank_preserved = transformed_design.rank() == full_design.rank() == 10

    c2 = sp.Matrix(
        [
            [1, q(1, 4), 0, 0],
            [0, 1, 0, q(1, 6)],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ]
    )
    c3 = sp.Matrix(
        [
            [1, 0, q(-1, 5), 0],
            [0, 1, 0, 0],
            [0, q(1, 8), 1, 0],
            [0, 0, 0, 1],
        ]
    )
    c1 = sp.eye(4)
    h1, h2, h3 = (sp.simplify(c.T * g * c) for c in (c1, c2, c3))
    d21 = c2.inv() * c1
    d32 = c3.inv() * c2
    d31 = c3.inv() * c1
    overlap_cocycle = sp.simplify(d32 * d21 - d31) == sp.zeros(4)
    overlap_metric_descent = all(
        residual == sp.zeros(4)
        for residual in (
            sp.simplify(d21.T * h2 * d21 - h1),
            sp.simplify(d32.T * h3 * d32 - h2),
            sp.simplify(d31.T * h3 * d31 - h1),
        )
    )
    corrupted_h2 = sp.MutableDenseMatrix(h2)
    corrupted_h2[0, 0] += q(1, 7)
    overlap_corruption_detected = (
        sp.simplify(d21.T * corrupted_h2 * d21 - h1) != sp.zeros(4)
    )

    h_terminal_1 = sp.Matrix([[-1, 0], [0, 1]])
    h_terminal_2 = sp.Matrix([[-1, q(1, 2)], [q(1, 2), q(3, 4)]])
    terminal_ratio_1 = sp.factor(-h_terminal_1.det() / h_terminal_1[0, 0] ** 2)
    terminal_ratio_2 = sp.factor(-h_terminal_2.det() / h_terminal_2[0, 0] ** 2)
    terminal_scalar_nonfaithful = (
        h_terminal_1 != h_terminal_2 and terminal_ratio_1 == terminal_ratio_2 == 1
    )

    x = sp.symbols("x", real=True)
    compact_bump = sp.exp(-1 / ((x - 1) * (2 - x)))
    bump_profile = sp.Piecewise((compact_bump, (x > 1) & (x < 2)), (0, True))
    bump_quiet_samples = all(
        bump_profile.subs(x, value) == 0
        for value in (q(-3), q(-1), q(0), q(1), q(2), q(3))
    )
    bump_nonzero = bump_profile.subs(x, q(3, 2)) == sp.exp(-4)
    continuation_nonrigid = bump_quiet_samples and bump_nonzero

    # Curved germ invisible to the three axial clock-ruler planes:
    # g_xy=a z^2 changes Ricci^2 at z=0 while every axial pair pullback is unchanged.
    t, x_coord, y_coord, z = sp.symbols("t x y z", real=True)
    coordinates = (t, x_coord, y_coord, z)
    a = sp.symbols("a", nonzero=True, real=True)
    curved = sp.Matrix(
        [
            [-1, 0, 0, 0],
            [0, 1, a * z**2, 0],
            [0, a * z**2, 1, 0],
            [0, 0, 0, 1],
        ]
    )
    curved_axial_equal = all(
        pullback(curved, sp.Matrix([1, 0, 0, 0]), v)
        == pullback(sp.diag(-1, 1, 1, 1), sp.Matrix([1, 0, 0, 0]), v)
        for v in axial
    )
    curved_inverse = sp.simplify(curved.inv())
    gamma = [
        [
            [
                sp.simplify(
                    sum(
                        curved_inverse[k, ell]
                        * (
                            sp.diff(curved[ell, j], coordinates[i])
                            + sp.diff(curved[ell, i], coordinates[j])
                            - sp.diff(curved[i, j], coordinates[ell])
                        )
                        for ell in range(4)
                    )
                    / 2
                )
                for j in range(4)
            ]
            for i in range(4)
        ]
        for k in range(4)
    ]
    ricci = sp.MutableDenseMatrix.zeros(4, 4)
    for i in range(4):
        for j in range(4):
            ricci[i, j] = sp.simplify(
                sum(
                    sp.diff(gamma[k][i][j], coordinates[k])
                    - sp.diff(gamma[k][i][k], coordinates[j])
                    + sum(
                        gamma[k][k][ell] * gamma[ell][i][j]
                        - gamma[k][j][ell] * gamma[ell][i][k]
                        for ell in range(4)
                    )
                    for k in range(4)
                )
            )
    ricci_squared = sp.simplify(
        sum(
            curved_inverse[i, k]
            * curved_inverse[j, ell]
            * ricci[i, j]
            * ricci[k, ell]
            for i in range(4)
            for j in range(4)
            for k in range(4)
            for ell in range(4)
        )
    )
    curved_ricci_squared_at_origin = sp.factor(ricci_squared.subs(z, 0))
    curved_nonisometric = (
        curved_axial_equal and curved_ricci_squared_at_origin == 2 * a**2
    )

    checks = {
        "source_hashes_match": source_hashes_match(),
        "generic_metric_lorentz": bool(lorentz_pivots),
        "all_six_pair_metrics_regular_lorentzian": bool(pair_metrics_regular),
        "six_plane_rank_ten": full_design.rank() == 10,
        "exact_metric_reconstruction": bool(reconstruction_exact),
        "frame_pullbacks_covariant": bool(frame_covariant),
        "frame_rank_preserved": bool(frame_rank_preserved),
        "three_axial_rank_seven": axial_design.rank() == 7,
        "axial_kernel_exactly_spatial_cross_terms": bool(axial_kernel_exact),
        "invisible_perturbation_preserves_axial_pullbacks": bool(axial_equal),
        "invisible_perturbation_retains_lorentz_signature": bool(epsilon_lorentz),
        "faithful_network_detects_perturbation": bool(faithful_detects),
        "overlap_transition_cocycle": bool(overlap_cocycle),
        "overlap_metric_descent": bool(overlap_metric_descent),
        "overlap_corruption_detected": bool(overlap_corruption_detected),
        "terminal_phi_scalar_nonfaithful": bool(terminal_scalar_nonfaithful),
        "quiet_endpoint_bump_sample_regression": bool(continuation_nonrigid),
        "rank_deficient_network_hides_curved_nonisometric_germ": bool(curved_nonisometric),
    }

    with (HERE / "NETWORK_RANK_ATLAS.tsv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle, fieldnames=atlas[0].keys(), delimiter="\t", lineterminator="\n"
        )
        writer.writeheader()
        writer.writerows(atlas)

    result = {
        "status": "PASS" if all(checks.values()) else "FAIL",
        "landing": "FAITHFUL_IFF_PAIR_PLANE_SPAN_HAS_RANK_TEN",
        "checks": checks,
        "production_check_count": len(checks),
        "rank_atlas": atlas,
        "generic_metric_leading_pivots": [str(value) for value in pivots],
        "perturbed_metric_leading_pivots": [str(value) for value in pivots_epsilon],
        "axial_kernel_basis": [
            [str(value) for value in vector] for vector in axial_nullspace
        ],
        "curved_counterexample_ricci_squared_at_origin": str(curved_ricci_squared_at_origin),
        "maximum_conclusion": (
            "On the declared regular pointwise arena, full calibrated pair pullbacks reconstruct "
            "the Lorentz metric exactly iff their restriction design has rank ten. Compatible "
            "full-rank local reconstructions descend uniquely up to chart isometry on the declared "
            "regular cover. Rank-deficient query networks retain exact invisible metric and curved "
            "germ fibers. Terminal reciprocal depth, quiet-middle agreement, and endpoint behavior "
            "alone are not faithful and do not select a physical universe."
        ),
    }
    (HERE / "DERIVATION_RESULT.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    if result["status"] != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
