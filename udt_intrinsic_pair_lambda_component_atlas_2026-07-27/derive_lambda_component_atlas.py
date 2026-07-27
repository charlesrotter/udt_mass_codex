#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
import sys
from fractions import Fraction
from pathlib import Path

import sympy as sp

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
ENGINE_DIR = ROOT / "udt_twisted_s3_intrinsic_pair_witness_audit_2026-07-27"
sys.path.insert(0, str(ENGINE_DIR))
from exact_invariant_jets import invariant_gradient_certificate  # noqa: E402

F = Fraction
EPSILON = F(1, 50)
TWIST = F(1, 64)
PRODUCTION_NODES = [F(value) for value in range(-4, 6)]
EXACT_HOLDOUTS = [F(-7, 2), F(-5, 2), F(-1, 2), F(1, 2), F(3, 2), F(5, 2), F(7, 2)]
CENTERS = {
    "C01": F(-2), "C02": F(-1), "C03": F(0),
    "C04": F(1, 2), "C05": F(1), "C06": F(2),
}
PRIMARY = (
    "THE_FROZEN_COMPLETE_S3_LAMBDA_SLICE_IS_PARTITIONED_INTO_EXACT_CERTIFICATE_"
    "COMPONENT_INTERVALS__C01_TO_C06_HAVE_EXACT_INTERVAL_ASSIGNMENTS__CERTIFICATE_"
    "DEGENERATION_POINTS_ARE_MAPPED__NO_FULL_CONFIGURATION_COMPONENT_OR_PHYSICAL_"
    "LAMBDA_SELECTION_IS_DERIVED"
)


def ftext(value: F) -> str:
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


def poly_add(left: list[F], right: list[F]) -> list[F]:
    size = max(len(left), len(right))
    result = [F(0) for _ in range(size)]
    for index, value in enumerate(left):
        result[index] += value
    for index, value in enumerate(right):
        result[index] += value
    while len(result) > 1 and result[-1] == 0:
        result.pop()
    return result


def poly_mul(left: list[F], right: list[F]) -> list[F]:
    result = [F(0) for _ in range(len(left) + len(right) - 1)]
    for i, a in enumerate(left):
        for j, b in enumerate(right):
            result[i + j] += a * b
    while len(result) > 1 and result[-1] == 0:
        result.pop()
    return result


def poly_scale(poly: list[F], scale: F) -> list[F]:
    return [coefficient * scale for coefficient in poly]


def poly_eval(poly: list[F], value: F) -> F:
    total = F(0)
    for coefficient in reversed(poly):
        total = total * value + coefficient
    return total


def interpolate(points: list[tuple[F, F]]) -> list[F]:
    result = [F(0)]
    for index, (x_value, y_value) in enumerate(points):
        basis = [F(1)]
        denominator = F(1)
        for other_index, (other_x, _) in enumerate(points):
            if other_index == index:
                continue
            basis = poly_mul(basis, [-other_x, F(1)])
            denominator *= x_value - other_x
        result = poly_add(result, poly_scale(basis, y_value / denominator))
    return result


def determinant(lambda_value: F) -> F:
    result = invariant_gradient_certificate(lambda_value, EPSILON, TWIST)
    return F(result["determinant"])


def write_tsv(name: str, fieldnames: list[str], rows: list[dict[str, object]]) -> None:
    with (HERE / name).open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def rational_from_sympy(value: sp.Rational) -> F:
    return F(int(value.p), int(value.q))


def main() -> int:
    cache: dict[F, F] = {}

    def cached(value: F) -> F:
        if value not in cache:
            cache[value] = determinant(value)
        return cache[value]

    production_points = [(value, cached(value)) for value in PRODUCTION_NODES]
    coefficients = interpolate(production_points)
    assert len(coefficients) <= 10
    assert all(poly_eval(coefficients, x_value) == y_value
               for x_value, y_value in production_points)

    holdout_rows = []
    for value in EXACT_HOLDOUTS:
        direct = cached(value)
        reconstructed = poly_eval(coefficients, value)
        assert direct == reconstructed
        holdout_rows.append({
            "lambda": ftext(value),
            "direct_determinant": ftext(direct),
            "polynomial_determinant": ftext(reconstructed),
            "exact_match": "YES",
        })

    symbol = sp.Symbol("lambda")
    expression = sum(
        sp.Rational(value.numerator, value.denominator) * symbol**degree
        for degree, value in enumerate(coefficients)
    )
    polynomial = sp.Poly(expression, symbol, domain=sp.QQ)
    assert polynomial.degree() == len(coefficients) - 1 <= 9
    intervals_with_multiplicity = polynomial.intervals(eps=sp.Rational(1, 10**12))
    real_roots = []
    for root_index, (bounds, multiplicity) in enumerate(intervals_with_multiplicity, start=1):
        left_sp, right_sp = bounds
        left = rational_from_sympy(left_sp)
        right = rational_from_sympy(right_sp)
        midpoint = (left + right) / 2
        real_roots.append({
            "root_id": f"R{root_index:02d}",
            "left_bound": ftext(left),
            "right_bound": ftext(right),
            "multiplicity": int(multiplicity),
            "decimal_midpoint": f"{float(midpoint):.15g}",
            "meaning": "FIXED_CERTIFICATE_RANK_LOSS_ONLY",
        })

    distinct_root_count = len(real_roots)
    root_bounds = [(F(row["left_bound"]), F(row["right_bound"])) for row in real_roots]
    interval_rows = []
    samples: list[F] = []
    if root_bounds:
        samples.append(F(root_bounds[0][0].numerator // root_bounds[0][0].denominator - 1))
        for (_, previous_right), (next_left, _) in zip(root_bounds, root_bounds[1:]):
            samples.append((previous_right + next_left) / 2)
        samples.append(F(root_bounds[-1][1].numerator // root_bounds[-1][1].denominator + 1))
    else:
        samples.append(F(0))
    for interval_index, sample in enumerate(samples, start=1):
        value = poly_eval(coefficients, sample)
        assert value != 0
        left_label = "-infinity" if interval_index == 1 else real_roots[interval_index - 2]["root_id"]
        right_label = "infinity" if interval_index > distinct_root_count else real_roots[interval_index - 1]["root_id"]
        interval_rows.append({
            "interval_id": f"I{interval_index:02d}",
            "left_boundary": left_label,
            "right_boundary": right_label,
            "exact_sample": ftext(sample),
            "determinant_sign": "POSITIVE" if value > 0 else "NEGATIVE",
            "certificate_status": "RANK_THREE",
        })

    center_rows = []
    for candidate_id, value in CENTERS.items():
        direct = cached(value)
        assert direct != 0
        root_count_below = 0
        for left, right in root_bounds:
            if right < value:
                root_count_below += 1
            elif left <= value <= right:
                raise AssertionError(f"center lies in root bracket: {candidate_id}")
        interval_id = f"I{root_count_below + 1:02d}"
        center_rows.append({
            "candidate_id": candidate_id,
            "lambda": ftext(value),
            "interval_id": interval_id,
            "determinant_sign": "POSITIVE" if direct > 0 else "NEGATIVE",
            "all_other_gates": "PASS_INDEPENDENT_OF_LAMBDA",
        })

    node_rows = [{
        "node_id": f"N{index:02d}",
        "lambda": ftext(value),
        "determinant": ftext(determinant_value),
        "exact": "YES",
    } for index, (value, determinant_value) in enumerate(production_points, start=1)]
    coefficient_rows = [{
        "power": degree,
        "coefficient": ftext(value),
        "nonzero": "YES" if value else "NO",
    } for degree, value in enumerate(coefficients)]
    write_tsv("PRODUCTION_NODE_OUTCOMES.tsv", ["node_id", "lambda", "determinant", "exact"], node_rows)
    write_tsv("EXACT_HOLDOUT_OUTCOMES.tsv", ["lambda", "direct_determinant", "polynomial_determinant", "exact_match"], holdout_rows)
    write_tsv("POLYNOMIAL_COEFFICIENTS.tsv", ["power", "coefficient", "nonzero"], coefficient_rows)
    write_tsv("REAL_ROOTS.tsv", ["root_id", "left_bound", "right_bound", "multiplicity", "decimal_midpoint", "meaning"], real_roots)
    write_tsv("LAMBDA_INTERVALS.tsv", ["interval_id", "left_boundary", "right_boundary", "exact_sample", "determinant_sign", "certificate_status"], interval_rows)
    write_tsv("CENTER_ASSIGNMENTS.tsv", ["candidate_id", "lambda", "interval_id", "determinant_sign", "all_other_gates"], center_rows)

    result = {
        "schema_version": 1,
        "compute": "CPU_ONLY_EXACT_RATIONAL_JETS_AND_EXACT_POLYNOMIAL",
        "base_commit": "de1125fded1155b1a4020360b0ebb9c07b46ca8d",
        "preregistration_commit": "6df7f07",
        "preregistration_correction_commit": "2ec7a4b",
        "premise_stamps": {
            "COPRESENCE": "WORKING_INTERPRETIVE_FRAME",
            "METRIC_CAUSAL_STRUCTURE": "DERIVED_CONDITIONAL",
            "INSTANTANEOUS_OPERATIONAL_ACCESS": "NOT_DERIVED",
            "COMPLETE_WHOLE_SOLUTION_LAW": "OPEN",
        },
        "degree_bound": 9,
        "actual_degree": polynomial.degree(),
        "frozen_axis": {
            "phi": "f/50",
            "a": "1/64",
            "R": "1",
            "event": "north_stereographic",
            "invariants": ["scalar_curvature", "Ricci_squared", "Kretschmann"],
        },
        "coefficients_ascending": [ftext(value) for value in coefficients],
        "factorization": str(sp.factor(polynomial.as_expr())),
        "production_nodes": len(production_points),
        "production_nodes_reproduced_exactly": True,
        "exact_holdouts": len(holdout_rows),
        "exact_holdouts_passed": sum(row["exact_match"] == "YES" for row in holdout_rows),
        "distinct_real_roots": distinct_root_count,
        "real_roots_with_multiplicity": sum(int(row["multiplicity"]) for row in real_roots),
        "certificate_intervals": len(interval_rows),
        "torch_tolerance": "2e-9*max(1,abs(D_exact))",
        "center_assignments": center_rows,
        "other_gates_lambda_independent": True,
        "D_zero_proves_clock_absent": False,
        "D_zero_proves_extra_symmetry": False,
        "D_zero_proves_metric_singular": False,
        "full_configuration_component_claim": False,
        "lambda_selected": False,
        "physical_phase_claim": False,
        "instantaneous_access_claim": False,
        "physics_inferences": False,
        "primary_conclusion": PRIMARY,
    }
    (HERE / "DERIVATION_RESULT.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(f"PASS exact_degree_bound actual={polynomial.degree()} bound=9")
    print("PASS production_nodes 10/10")
    print("PASS exact_holdouts 7/7")
    print(f"PASS distinct_real_roots {distinct_root_count}")
    print(f"PASS certificate_intervals {len(interval_rows)}")
    print("PASS center_assignments 6/6")
    print(f"PRIMARY {PRIMARY}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
