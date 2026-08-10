#!/usr/bin/env python3
"""Exercise fail-closed defects against the reciprocal descent result."""

from __future__ import annotations

import csv
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
ETA = sp.diag(-1, 1, 1, 1)


def gram(columns: sp.Matrix) -> sp.Matrix:
    return sp.simplify(columns.T * ETA * columns)


def rotation(theta: sp.Expr) -> sp.Matrix:
    out = sp.eye(4)
    out[2, 2] = out[3, 3] = sp.cos(theta)
    out[2, 3] = -sp.sin(theta)
    out[3, 2] = sp.sin(theta)
    return out


def main() -> None:
    flag = sp.Matrix.hstack(sp.eye(4)[:, 0], sp.eye(4)[:, 1])
    arrow = sp.Matrix(
        [[sp.Rational(1, 2), 0, 0, 0], [0, 2, 0, 0], [sp.Rational(1, 4), 0, 1, 0], [0, 0, 0, 1]]
    )
    quarter = rotation(sp.pi / 2)
    pu = sp.diag(1, 0, 0, 0)
    pn = sp.diag(0, 1, 0, 0)
    hs = sp.diag(0, 0, 1, 1)
    tests = []
    with (ROOT / "CURRENT_SCIENTIFIC_PREMISES.tsv").open(newline="", encoding="utf-8") as stream:
        premises = {row["premise_id"]: row for row in csv.DictReader(stream, delimiter="\t")}

    def record(test_id: str, defect: str, rejected: bool) -> None:
        assert rejected, test_id
        tests.append({"test_id": test_id, "injected_defect": defect, "expected": "REJECT", "observed": "REJECT"})

    base_metric = gram(arrow * flag)
    rotated_arrow = quarter * arrow
    record(
        "C01",
        "use one screen component as the scalar so a pure screen rotation changes the readout",
        rotated_arrow[2, 0] != arrow[2, 0] and gram(rotated_arrow * flag) == base_metric,
    )

    boost = sp.eye(4)
    boost[0, 0] = boost[1, 1] = sp.Rational(5, 4)
    boost[0, 1] = boost[1, 0] = sp.Rational(3, 4)
    alignment = boost.inv()
    carried_flag = boost * flag
    record(
        "C02",
        "claim an isometric middle alignment generates nonzero calibration",
        gram(alignment * carried_flag) == gram(carried_flag),
    )

    record(
        "C03",
        "call delta_RF the selected universal physical law after proving only gauge descent",
        "PHYSICAL_FLAG_ARROW_CALIBRATION_OPEN" in premises["G35"]["current_status"]
        and "delta_RF called selected physical law" in premises["G35"]["forbidden_regression"],
    )
    record(
        "C04",
        "zero the clock-to-screen mixing before testing descent",
        arrow[2, 0] == sp.Rational(1, 4) and gram(quarter * arrow * flag) == base_metric,
    )

    with (ROOT / "udt_intrinsic_reciprocal_holonomy_audit_2026-07-27/LOOP_HOLONOMY.tsv").open() as stream:
        loops = list(csv.DictReader(stream, delimiter="\t"))
    record(
        "C05",
        "erase path labels after screen-gauge descent",
        len(loops) == 36 and all(float(row["ordinary_closure_residual"]) > 1e-10 for row in loops),
    )

    null_flag = sp.Matrix.hstack(sp.Matrix([1, 1, 0, 0]), sp.eye(4)[:, 2])
    record(
        "C06",
        "extend the logarithmic density formula through a null clock line",
        gram(null_flag)[0, 0] == 0,
    )

    b02 = sp.eye(4)
    b02[0, 0] = b02[2, 2] = sp.Rational(5, 4)
    b02[0, 2] = b02[2, 0] = sp.Rational(3, 4)
    a12 = arrow
    a23 = b02 * sp.diag(sp.Rational(2, 3), sp.Rational(3, 2), 1, 1)
    original = sp.simplify(a23 * a12)
    one_sided = sp.simplify(a23 * quarter * a12)
    balanced = sp.simplify((a23 * quarter.inv()) * (quarter * a12))
    record(
        "C07",
        "change only one middle gauge leg and call composition representative independent",
        one_sided != original and balanced == original,
    )

    record(
        "C08",
        "promote one named screen axis despite a nontrivial stabilizer",
        quarter != sp.eye(4) and all(quarter * projector == projector * quarter for projector in (pu, pn, hs)),
    )
    record(
        "C09",
        "infer a universal c_eff without a physical pair map or calibration owner",
        "universal mixed-geometry c_eff identification" in premises["G37"]["open_scope"],
    )
    record(
        "C10",
        "promote conditional R17 to a branch-owned physical transition",
        "CONDITIONAL_ASSEMBLY_NOT_BRANCH_OWNED" in premises["G42"]["current_status"]
        and "R17 semidirect assembly called branch-owned" in premises["G42"]["forbidden_regression"],
    )
    source_rotation = rotation(sp.pi / 2)
    target_rotation = rotation(sp.pi)
    independently_rotated = target_rotation * arrow * source_rotation.inv()
    record(
        "C11",
        "require source and target screen gauges to use the same angle",
        source_rotation != target_rotation and gram(independently_rotated * flag) == base_metric,
    )
    record(
        "C12",
        "claim gauge descent equates distinct physical paths",
        any(float(row["nonidentity_max"]) > 1e-10 for row in loops),
    )

    unnormalized_flag = flag * sp.diag(2, 3)
    source_metric = gram(unnormalized_flag)
    target_metric = gram(arrow * unnormalized_flag)
    line_ratio = sp.Abs(target_metric[0, 0]) / sp.Abs(source_metric[0, 0])
    area_ratio = sp.Abs(target_metric.det()) / sp.Abs(source_metric.det())
    reciprocal_argument = sp.simplify(area_ratio / line_ratio**2)
    source_factor = sp.simplify(sp.Abs(source_metric.det()) / sp.Abs(source_metric[0, 0]) ** 2)
    terminal_bracket = sp.simplify(-target_metric.det() / target_metric[0, 0] ** 2)
    record(
        "C13",
        "omit the source-calibration normalization factor from the terminal determinant identity",
        source_factor == sp.Rational(9, 4)
        and terminal_bracket != reciprocal_argument
        and terminal_bracket == reciprocal_argument * source_factor,
    )

    with (HERE / "CATCH_PROOFS.tsv").open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(tests[0]), delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(tests)
    print(f"catch_proofs={len(tests)}/{len(tests)}")


if __name__ == "__main__":
    main()
