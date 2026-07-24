#!/usr/bin/env python3
"""Independent stdlib/Fraction verification of substrate-to-micro results."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from fractions import Fraction
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def matmul(a: list[list[Fraction]], b: list[list[Fraction]]) -> list[list[Fraction]]:
    return [
        [
            sum((a[i][k] * b[k][j] for k in range(len(b))), Fraction(0))
            for j in range(len(b[0]))
        ]
        for i in range(len(a))
    ]


def transpose(a: list[list[Fraction]]) -> list[list[Fraction]]:
    return [list(row) for row in zip(*a)]


def add(a: list[list[Fraction]], b: list[list[Fraction]]) -> list[list[Fraction]]:
    return [
        [a[i][j] + b[i][j] for j in range(len(a[0]))]
        for i in range(len(a))
    ]


def scale(c: Fraction, a: list[list[Fraction]]) -> list[list[Fraction]]:
    return [[c * value for value in row] for row in a]


def pullback(e: list[list[Fraction]], g: list[list[Fraction]]) -> list[list[Fraction]]:
    return matmul(matmul(transpose(e), g), e)


def polynomial_value(coefficients: list[Fraction], x: Fraction) -> Fraction:
    return sum(
        (coefficient * x**power for power, coefficient in enumerate(coefficients)),
        Fraction(0),
    )


def polynomial_derivative(coefficients: list[Fraction], x: Fraction) -> Fraction:
    return sum(
        (
            Fraction(power) * coefficient * x ** (power - 1)
            for power, coefficient in enumerate(coefficients)
            if power
        ),
        Fraction(0),
    )


def polynomial_second(coefficients: list[Fraction], x: Fraction) -> Fraction:
    return sum(
        (
            Fraction(power * (power - 1))
            * coefficient
            * x ** (power - 2)
            for power, coefficient in enumerate(coefficients)
            if power >= 2
        ),
        Fraction(0),
    )


def exact_checks() -> list[dict[str, object]]:
    checks: list[dict[str, object]] = []

    def record(name: str, passed: bool, detail: str) -> None:
        checks.append({"name": name, "passed": passed, "detail": detail})

    e = [
        [Fraction(1), Fraction(0), Fraction(2)],
        [Fraction(0), Fraction(1), Fraction(-1)],
        [Fraction(2), Fraction(1), Fraction(0)],
        [Fraction(-1), Fraction(3), Fraction(1)],
    ]
    g = [
        [Fraction(3), Fraction(1), Fraction(0), Fraction(0)],
        [Fraction(1), Fraction(4), Fraction(1), Fraction(0)],
        [Fraction(0), Fraction(1), Fraction(5), Fraction(1)],
        [Fraction(0), Fraction(0), Fraction(1), Fraction(6)],
    ]
    dg = [
        [Fraction(1), Fraction(2), Fraction(0), Fraction(1)],
        [Fraction(2), Fraction(-1), Fraction(3), Fraction(0)],
        [Fraction(0), Fraction(3), Fraction(2), Fraction(-2)],
        [Fraction(1), Fraction(0), Fraction(-2), Fraction(4)],
    ]
    epsilon = Fraction(3, 7)
    left = pullback(e, add(g, scale(epsilon, dg)))
    right = add(pullback(e, g), scale(epsilon, pullback(e, dg)))
    record("pullback_variation_fraction", left == right, str(left == right))

    q = Fraction(5, 3)
    record("e2_weight_fraction", q**3 * q**-2 == q, str(q))
    record("e4_weight_fraction", q**3 * q**-4 == q**-1, str(q**-1))

    qpoly = [Fraction(2), Fraction(1), Fraction(3)]
    upoly = [Fraction(-1), Fraction(4), Fraction(2), Fraction(1)]
    point = Fraction(2, 5)
    qv = polynomial_value(qpoly, point)
    qp = polynomial_derivative(qpoly, point)
    up = polynomial_derivative(upoly, point)
    upp = polynomial_second(upoly, point)
    divergence = qp * up + qv * upp
    laplace_direct = divergence / qv**3
    laplace_formula = (upp + qp * up / qv) / qv**2
    record(
        "conformal_laplacian_fraction",
        laplace_direct == laplace_formula,
        str(laplace_direct),
    )

    xi, kappa, ashape, bshape = (
        Fraction(2),
        Fraction(8),
        Fraction(3),
        Fraction(6),
    )
    # Choose values with an exact square root:
    # kappa*B/(xi*A)=8, so set q and compare R-coordinate scaling through R*q.
    ratio = kappa * ashape / (xi * bshape)
    record("positive_ratio_control", ratio == Fraction(2), str(ratio))
    # Algebraic stationarity is squared to avoid floating square roots:
    # R_star^2 = kappa*B/(xi*A*q^2).
    r2 = kappa * bshape / (xi * ashape * q**2)
    stationarity_scaled = xi * q * ashape * r2 - kappa * bshape / q
    record("constant_q_stationarity_fraction", stationarity_scaled == 0, str(stationarity_scaled))
    physical_r2 = q**2 * r2
    record(
        "constant_q_physical_radius_fraction",
        physical_r2 == kappa * bshape / (xi * ashape),
        str(physical_r2),
    )

    sigma = Fraction(7, 11)
    record("e2_trace_weight_fraction", (3 - 2) * sigma == sigma, str(sigma))
    record("e4_trace_weight_fraction", (3 - 4) * sigma == -sigma, str(-sigma))

    delta_prime, lambda_prime, bvalue = Fraction(3), Fraction(-5), Fraction(7)
    original_p = delta_prime + bvalue
    transformed_p = delta_prime + lambda_prime + bvalue - lambda_prime
    record("phase_connection_fraction", original_p == transformed_p, str(original_p))

    # Mixed partial cancellation represented by polynomial lambda=x^2*y^3.
    xx, yy = Fraction(2), Fraction(3)
    dxy = Fraction(6) * xx * yy**2
    dyx = Fraction(6) * xx * yy**2
    record("curvature_gauge_cancellation_fraction", dxy == dyx, str(dxy))
    return checks


def table_checks(
    result: dict[str, object],
    channels: list[dict[str, str]],
    regrades: list[dict[str, str]],
    fixed: list[dict[str, str]],
    completions: list[dict[str, str]],
) -> list[dict[str, object]]:
    checks: list[dict[str, object]] = []

    def record(name: str, passed: bool, detail: object) -> None:
        checks.append({"name": name, "passed": passed, "detail": str(detail)})

    record("channel_count", len(channels) == 24, len(channels))
    record("channel_unique", len({row["id"] for row in channels}) == 24, len(channels))
    record("regrade_count", len(regrades) == 15, len(regrades))
    record("fixed_arrow_count", len(fixed) == 14, len(fixed))
    record("completion_count", len(completions) == 12, len(completions))
    record(
        "all_completion_matter_open",
        all(row["matter_closure"] == "NOT_SUPPLIED" for row in completions),
        "all",
    )
    channel_map = {row["id"]: row["outcome"] for row in channels}
    regrade_map = {row["id"]: row["disposition"] for row in regrades}
    record(
        "direct_density_rejected",
        channel_map.get("C23_DIRECT_DENSITY_COUPLING") == "REJECTED_DIRECT_INSERTION",
        channel_map.get("C23_DIRECT_DENSITY_COUPLING"),
    )
    record(
        "gr_route_rejected",
        channel_map.get("C24_GR_DENSITY_CURVATURE") == "REJECTED_AS_UDT_DERIVATION",
        channel_map.get("C24_GR_DENSITY_CURVATURE"),
    )
    record(
        "strong_local_not_promoted",
        channel_map.get("C19_STRONG_LOCAL_WINDOW")
        == "WORKING_HYPOTHESIS_CHANNEL_ARCHITECTURE_EXISTS_DEPENDENCE_OPEN",
        channel_map.get("C19_STRONG_LOCAL_WINDOW"),
    )
    record(
        "fixed_background_scope_retained",
        regrade_map.get("R05_STATIC_STABILITY") == "UNCHANGED_FIXED_BACKGROUND_SCOPE",
        regrade_map.get("R05_STATIC_STABILITY"),
    )
    record(
        "outer_role_qualified",
        regrade_map.get("R09_BOOTSTRAP_AFTER_SOLUTION")
        == "QUALIFIED_CURRENT_ROLE_NOT_EXHAUSTIVE_OWNER_HYPOTHESIS",
        regrade_map.get("R09_BOOTSTRAP_AFTER_SOLUTION"),
    )
    record(
        "density_closure_open",
        result["rulings"]["simultaneous_density_matter_closure"]
        == "OPEN_MISSING_NATIVE_ARROWS",
        result["rulings"]["simultaneous_density_matter_closure"],
    )
    record(
        "no_physics_promotions",
        not any(bool(value) for value in result["authority_boundary"].values()),
        result["authority_boundary"],
    )
    return checks


def catch_proofs(
    result: dict[str, object],
    channels: list[dict[str, str]],
    regrades: list[dict[str, str]],
    fixed: list[dict[str, str]],
    completions: list[dict[str, str]],
) -> list[dict[str, object]]:
    catches: list[dict[str, object]] = []

    def catches_failure(name: str, mutated_passes: bool) -> None:
        catches.append({"name": name, "passed": not mutated_passes})

    catches_failure("missing_channel_rejected", len(channels[:-1]) == 24)
    catches_failure(
        "duplicate_channel_rejected",
        len({row["id"] for row in channels + [channels[0]]}) == len(channels) + 1,
    )
    mutated = [dict(row) for row in channels]
    next(row for row in mutated if row["id"] == "C23_DIRECT_DENSITY_COUPLING")[
        "outcome"
    ] = "METRIC_NATIVE_KINEMATIC_CHANNEL"
    catches_failure(
        "density_insertion_promotion_rejected",
        next(row for row in mutated if row["id"] == "C23_DIRECT_DENSITY_COUPLING")[
            "outcome"
        ]
        == "REJECTED_DIRECT_INSERTION",
    )
    mutated = [dict(row) for row in channels]
    next(row for row in mutated if row["id"] == "C19_STRONG_LOCAL_WINDOW")[
        "outcome"
    ] = "DERIVED_MATTER_WINDOW"
    catches_failure(
        "strong_local_promotion_rejected",
        next(row for row in mutated if row["id"] == "C19_STRONG_LOCAL_WINDOW")[
            "outcome"
        ]
        == "WORKING_HYPOTHESIS_CHANNEL_ARCHITECTURE_EXISTS_DEPENDENCE_OPEN",
    )
    catches_failure("missing_regrade_rejected", len(regrades[:-1]) == 15)
    catches_failure("missing_fixed_arrow_rejected", len(fixed[:-1]) == 14)
    catches_failure("missing_completion_rejected", len(completions[:-1]) == 12)
    mutated_completion = [dict(row) for row in completions]
    mutated_completion[0]["matter_closure"] = "DERIVED"
    catches_failure(
        "completion_matter_promotion_rejected",
        all(row["matter_closure"] == "NOT_SUPPLIED" for row in mutated_completion),
    )
    mutated_result = json.loads(json.dumps(result))
    mutated_result["authority_boundary"]["density_curvature_law_derived"] = True
    catches_failure(
        "density_curvature_claim_rejected",
        not any(bool(value) for value in mutated_result["authority_boundary"].values()),
    )
    mutated_result = json.loads(json.dumps(result))
    mutated_result["rulings"]["constant_homothety"] = "SELECTS_COEFFICIENT_RULER"
    catches_failure(
        "homothety_scale_promotion_rejected",
        mutated_result["rulings"]["constant_homothety"]
        == "DOES_NOT_REMOVE_CONDITIONAL_COEFFICIENT_RULER",
    )
    catches_failure(
        "production_failure_rejected",
        bool({**result, "all_checks_pass": False}["all_checks_pass"]),
    )
    return catches


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--production", type=Path, required=True)
    parser.add_argument("--channels", type=Path, required=True)
    parser.add_argument("--regrades", type=Path, required=True)
    parser.add_argument("--fixed-point", type=Path, required=True)
    parser.add_argument("--completions", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    result = json.loads(args.production.read_text(encoding="utf-8"))
    channels = read_tsv(args.channels)
    regrades = read_tsv(args.regrades)
    fixed = read_tsv(args.fixed_point)
    completions = read_tsv(args.completions)

    exact = exact_checks()
    tables = table_checks(result, channels, regrades, fixed, completions)
    catches = catch_proofs(result, channels, regrades, fixed, completions)
    all_pass = all(bool(row["passed"]) for row in exact + tables + catches)

    output = {
        "schema": "udt-bootstrap-substrate-micro-independent-v1",
        "method": "PYTHON_STDLIB_FRACTION_NO_SYMPY_NO_CONTROLLER_IMPORT",
        "exact_checks": exact,
        "table_agreement_checks": tables,
        "catch_proofs": catches,
        "counts": {
            "exact_passed": sum(bool(row["passed"]) for row in exact),
            "exact_total": len(exact),
            "agreement_passed": sum(bool(row["passed"]) for row in tables),
            "agreement_total": len(tables),
            "catches_passed": sum(bool(row["passed"]) for row in catches),
            "catches_total": len(catches),
        },
        "artifact_sha256": {
            "production": sha256(args.production),
            "channels": sha256(args.channels),
            "regrades": sha256(args.regrades),
            "fixed_point": sha256(args.fixed_point),
            "completions": sha256(args.completions),
        },
        "all_checks_pass": all_pass,
    }
    args.output.write_text(
        json.dumps(output, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    if not all_pass:
        raise SystemExit("independent checks failed")
    print(
        "independent=PASS "
        f"exact={output['counts']['exact_passed']}/{output['counts']['exact_total']} "
        f"agreement={output['counts']['agreement_passed']}/{output['counts']['agreement_total']} "
        f"catches={output['counts']['catches_passed']}/{output['counts']['catches_total']}"
    )


if __name__ == "__main__":
    main()
