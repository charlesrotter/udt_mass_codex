#!/usr/bin/env python3
"""Exact production derivation for reciprocal readout descent through screen gauge."""

from __future__ import annotations

import csv
import json
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
ETA = sp.diag(-1, 1, 1, 1)
LAMBDAS = [sp.Rational(-2), sp.Rational(-1), sp.Rational(0), sp.Rational(1, 2), sp.Rational(1), sp.Rational(2)]


def boost(i: int, j: int) -> sp.Matrix:
    out = sp.eye(4)
    out[i, i] = out[j, j] = sp.Rational(5, 4)
    out[i, j] = out[j, i] = sp.Rational(3, 4)
    return out


def screen_rotation(theta: sp.Symbol) -> sp.Matrix:
    out = sp.eye(4)
    out[2, 2] = out[3, 3] = sp.cos(theta)
    out[2, 3] = -sp.sin(theta)
    out[3, 2] = sp.sin(theta)
    return out


def gram(columns: sp.Matrix) -> sp.Matrix:
    return sp.simplify(columns.T * ETA * columns)


def positive_ratio(value: sp.Expr) -> sp.Expr:
    return sp.simplify(sp.Abs(value))


def density_arguments(arrow: sp.Matrix, flag: sp.Matrix) -> tuple[sp.Expr, sp.Expr, sp.Expr]:
    source = gram(flag)
    target = gram(sp.simplify(arrow * flag))
    line_ratio = sp.simplify(positive_ratio(target[0, 0]) / positive_ratio(source[0, 0]))
    area_ratio = sp.simplify(positive_ratio(target.det()) / positive_ratio(source.det()))
    reciprocal_argument = sp.simplify(area_ratio / line_ratio**2)
    return line_ratio, area_ratio, reciprocal_argument


def main() -> None:
    theta_p, theta_q = sp.symbols("theta_p theta_q", real=True)
    depth = sp.symbols("depth", real=True)
    rotation_p = screen_rotation(theta_p)
    rotation_q = screen_rotation(theta_q)
    assert sp.trigsimp(rotation_p.T * ETA * rotation_p - ETA) == sp.zeros(4)
    assert sp.trigsimp(rotation_q.T * ETA * rotation_q - ETA) == sp.zeros(4)

    flag = sp.Matrix.hstack(sp.eye(4)[:, 0], sp.eye(4)[:, 1])
    pu = sp.diag(1, 0, 0, 0)
    pn = sp.diag(0, 1, 0, 0)
    hs = sp.diag(0, 0, 1, 1)
    assert all(sp.simplify(rotation_p * projector - projector * rotation_p) == sp.zeros(4) for projector in (pu, pn, hs))
    assert all(sp.simplify(rotation_q * projector - projector * rotation_q) == sp.zeros(4) for projector in (pu, pn, hs))

    # Complete mixed-arrow witness from the prior reciprocal-flag challenge.
    arrow = sp.Matrix(
        [
            [sp.Rational(1, 2), 0, 0, 0],
            [0, 2, 0, 0],
            [sp.Rational(1, 4), 0, 1, 0],
            [0, 0, 0, 1],
        ]
    )
    pair_metric = gram(arrow * flag)
    line_ratio, area_ratio, reciprocal_argument = density_arguments(arrow, flag)
    assert line_ratio == sp.Rational(3, 16)
    assert area_ratio == sp.Rational(3, 4)
    assert reciprocal_argument == sp.Rational(64, 3)
    source_metric = gram(flag)
    source_normalization = sp.simplify(
        positive_ratio(source_metric.det()) / positive_ratio(source_metric[0, 0]) ** 2
    )
    assert source_normalization == 1
    terminal_argument = sp.simplify(-pair_metric.det() / pair_metric[0, 0] ** 2)
    assert terminal_argument == reciprocal_argument * source_normalization

    # The terminal bracket equals Q only in normalized source calibration.  An unnormalized
    # source flag exposes the otherwise hidden source factor exactly.
    unnormalized_flag = flag * sp.diag(2, 3)
    unnormalized_source = gram(unnormalized_flag)
    unnormalized_target = gram(arrow * unnormalized_flag)
    _, _, unnormalized_q = density_arguments(arrow, unnormalized_flag)
    unnormalized_source_factor = sp.simplify(
        positive_ratio(unnormalized_source.det()) / positive_ratio(unnormalized_source[0, 0]) ** 2
    )
    unnormalized_terminal = sp.simplify(
        -unnormalized_target.det() / unnormalized_target[0, 0] ** 2
    )
    assert unnormalized_source_factor == sp.Rational(9, 4)
    assert unnormalized_terminal != unnormalized_q
    assert unnormalized_terminal == unnormalized_q * unnormalized_source_factor

    # Arbitrary continuous endpoint screen rotation leaves all four readouts unchanged.
    rotated_arrow = sp.simplify(rotation_q * arrow * rotation_p.inv())
    rotated_pair_metric = sp.trigsimp(gram(rotated_arrow * flag))
    assert rotated_pair_metric == pair_metric
    assert all(
        sp.trigsimp(a - b) == 0
        for a, b in zip(density_arguments(rotated_arrow, flag), (line_ratio, area_ratio, reciprocal_argument))
    )

    # The conditional R17 reciprocal exponent commutes with the complete screen stabilizer.
    rows = []
    for index, lam in enumerate(LAMBDAS, start=1):
        grading = -pu + pn + lam * hs
        exponential = sp.diag(sp.exp(-depth), sp.exp(depth), sp.exp(lam * depth), sp.exp(lam * depth))
        assert sp.trigsimp(rotation_p * grading - grading * rotation_p) == sp.zeros(4)
        assert sp.trigsimp(rotation_q * grading - grading * rotation_q) == sp.zeros(4)
        assert sp.trigsimp(rotation_p * exponential - exponential * rotation_p) == sp.zeros(4)
        assert sp.trigsimp(rotation_q * exponential - exponential * rotation_q) == sp.zeros(4)
        _, _, r17_argument = density_arguments(exponential, flag)
        assert sp.simplify(r17_argument - sp.exp(4 * depth)) == 0
        rows.append(
            {
                "branch_id": f"C{index:02d}",
                "lambda": str(lam),
                "full_screen_gauge": "SO2_CONTINUOUS",
                "delta_RF_descent": "DERIVED_ON_SUPPLIED_REGULAR_FLAG_ARROW",
                "terminal_pair_readout_descent": "DERIVED_ON_SUPPLIED_REGULAR_PAIR_METRIC",
                "conditional_R17_scalar_descent": "DERIVED_WITHOUT_BRANCH_OWNERSHIP_PROMOTION",
                "alignment_generated_calibration": "NO_ISOMETRIC_ALIGNMENT_HAS_NONZERO_LOG_DENSITIES",
                "path_label": "RETAINED",
            }
        )

    # An isometric carried-to-intrinsic alignment has exactly zero calibration densities.
    carried_frame = boost(0, 1)
    alignment = carried_frame.inv()
    carried_flag = carried_frame * flag
    alignment_line, alignment_area, alignment_reciprocal = density_arguments(alignment, carried_flag)
    assert alignment_line == alignment_area == alignment_reciprocal == 1

    # Exact telescoping and balanced middle-gauge composition on a noncommuting three-arrow witness.
    dilation = sp.diag(sp.Rational(2, 3), sp.Rational(3, 2), 1, 1)
    arrow_12 = arrow
    arrow_23 = boost(0, 2) * dilation
    flag_2 = arrow_12 * flag
    total = sp.simplify(arrow_23 * arrow_12)
    d12 = density_arguments(arrow_12, flag)
    d23 = density_arguments(arrow_23, flag_2)
    d13 = density_arguments(total, flag)
    assert sp.simplify(d12[0] * d23[0] - d13[0]) == 0
    assert sp.simplify(d12[1] * d23[1] - d13[1]) == 0
    assert sp.simplify(d12[2] * d23[2] - d13[2]) == 0

    quarter_turn = screen_rotation(sp.pi / 2)
    arrow_12_gauge = sp.simplify(quarter_turn * arrow_12)
    arrow_23_gauge = sp.simplify(arrow_23 * quarter_turn.inv())
    assert sp.simplify(arrow_23_gauge * arrow_12_gauge - total) == sp.zeros(4)
    gauge_d12 = density_arguments(arrow_12_gauge, flag)
    gauge_d23 = density_arguments(arrow_23_gauge, arrow_12_gauge * flag)
    assert all(sp.simplify(a - b) == 0 for a, b in zip(gauge_d12, d12))
    assert all(sp.simplify(a - b) == 0 for a, b in zip(gauge_d23, d23))

    with (ROOT / "udt_intrinsic_reciprocal_holonomy_audit_2026-07-27/LOOP_HOLONOMY.tsv").open() as stream:
        loops = list(csv.DictReader(stream, delimiter="\t"))
    assert len(loops) == 36
    assert all(float(row["ordinary_closure_residual"]) > 1e-10 for row in loops)

    with (HERE / "DESCENT_ATLAS.tsv").open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]), delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

    result = {
        "primary_landing": "RECIPROCAL_READOUT_DESCENT_DERIVED__CALIBRATION_MAGNITUDE_NOT_GENERATED",
        "scope": "C01-C06 regular full-projector strata; supplied flags/arrows/pair metrics; path labels retained",
        "lambda_rows": len(rows),
        "continuous_screen_gauge_checked_symbolically": True,
        "mixed_arrow_clock_line_ratio": str(line_ratio),
        "mixed_arrow_plane_area_ratio": str(area_ratio),
        "delta_RF_and_terminal_argument": str(reciprocal_argument),
        "delta_RF_value": "log(64/3)/4",
        "terminal_pair_readout_matches_delta_RF": True,
        "terminal_pair_readout_requires_normalized_source_calibration": True,
        "unnormalized_source_factor_witness": str(unnormalized_source_factor),
        "conditional_R17_exponent_descends": True,
        "balanced_composition_and_density_telescoping_exact": True,
        "isometric_alignment_line_ratio": str(alignment_line),
        "isometric_alignment_area_ratio": str(alignment_area),
        "isometric_alignment_reciprocal_argument": str(alignment_reciprocal),
        "alignment_generates_nonzero_calibration": False,
        "path_loop_rows_retained": len(loops),
        "owned": [
            "screen-gauge descent of supplied clock-line and clock/ruler-plane densities",
            "screen-gauge descent of conditional delta_RF",
            "screen-gauge descent of the terminal supplied pair-metric log imbalance",
            "screen-gauge descent of the conditional R17 reciprocal exponent",
            "exact density telescoping under balanced middle-gauge composition",
        ],
        "open": [
            "physical non-isometric calibration magnitude and its owner",
            "physical pair relation or pair surface",
            "selection of delta_RF or R17 as the physical law",
            "null/degenerate strata and global cut-locus continuation",
            "universal mixed-geometry c_eff",
        ],
    }
    (HERE / "DERIVATION_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
