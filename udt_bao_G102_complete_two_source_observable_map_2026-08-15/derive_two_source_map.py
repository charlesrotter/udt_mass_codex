#!/usr/bin/env python3
"""Exact symbolic/synthetic derivation for the preregistered G102 map.

No repository outcome artifact or observational curve is read.
"""

from __future__ import annotations

import json
from fractions import Fraction

import sympy as sp


ETA = sp.diag(-1, 1, 1, 1)


def inner(a: sp.Matrix, b: sp.Matrix) -> sp.Expr:
    return sp.expand((a.T * ETA * b)[0])


def pair_readout(V: sp.Matrix) -> dict[str, sp.Expr | sp.Matrix]:
    h = sp.simplify(V.T * ETA * V)
    v0 = V[:, 0]
    v1 = V[:, 1]
    T2 = sp.simplify(-h[0, 0])
    ruler = sp.simplify(v1 - (h[0, 1] / h[0, 0]) * v0)
    L2 = sp.simplify(h[1, 1] - h[0, 1] ** 2 / h[0, 0])
    u = sp.simplify(v0 / sp.sqrt(T2))
    n = sp.simplify(ruler / sp.sqrt(L2))
    phi_argument = sp.simplify((-h.det()) / h[0, 0] ** 2)
    return {
        "h": h,
        "T2": T2,
        "L2": L2,
        "u": u,
        "ruler": ruler,
        "n": n,
        "phi_argument": phi_argument,
    }


def exact_angle_bin(cosine: Fraction) -> int:
    if cosine > Fraction(1, 2):
        return 0
    if cosine > Fraction(-1, 2):
        return 1
    return 2


def dot_fraction(a: tuple[Fraction, ...], b: tuple[Fraction, ...]) -> Fraction:
    return sum((x * y for x, y in zip(a, b)), Fraction(0))


def auto_counts(
    points: list[tuple[Fraction, ...]], weights: list[Fraction]
) -> tuple[list[Fraction], Fraction]:
    bins = [Fraction(0), Fraction(0), Fraction(0)]
    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            bins[exact_angle_bin(dot_fraction(points[i], points[j]))] += weights[i] * weights[j]
    total = (sum(weights) ** 2 - sum((w * w for w in weights), Fraction(0))) / 2
    return bins, total


def cross_counts(
    left: list[tuple[Fraction, ...]],
    left_weights: list[Fraction],
    right: list[tuple[Fraction, ...]],
    right_weights: list[Fraction],
) -> tuple[list[Fraction], Fraction]:
    bins = [Fraction(0), Fraction(0), Fraction(0)]
    for i, p in enumerate(left):
        for j, q in enumerate(right):
            bins[exact_angle_bin(dot_fraction(p, q))] += left_weights[i] * right_weights[j]
    return bins, sum(left_weights) * sum(right_weights)


def frac_strings(values: list[Fraction]) -> list[str]:
    return [str(value) for value in values]


def main() -> None:
    x = sp.symbols("x0:4", real=True)
    y = sp.symbols("y0:4", real=True)
    v0 = sp.Matrix(x)
    v1 = sp.Matrix(y)
    V = v0.row_join(v1)
    generic = pair_readout(V)

    type_checks = {
        "clock_unit": sp.simplify(inner(generic["u"], generic["u"]) + 1),
        "clock_ruler_orthogonal": sp.simplify(inner(v0, generic["ruler"])),
        "ruler_norm": sp.simplify(inner(generic["ruler"], generic["ruler"]) - generic["L2"]),
        "direction_unit": sp.simplify(inner(generic["n"], generic["n"]) - 1),
    }
    if any(value != 0 for value in type_checks.values()):
        raise AssertionError(type_checks)

    a, b, c = sp.symbols("a b c", positive=True)
    V_gauge = (a * v0).row_join(b * v1 + c * v0)
    transformed = pair_readout(V_gauge)
    gauge_checks = {
        "ruler_covariance": sp.simplify(transformed["ruler"] - b * generic["ruler"]),
        "L2_covariance": sp.simplify(transformed["L2"] - b**2 * generic["L2"]),
        "det_covariance": sp.simplify(transformed["h"].det() - (a * b) ** 2 * generic["h"].det()),
    }
    if gauge_checks["ruler_covariance"] != sp.zeros(4, 1):
        raise AssertionError(gauge_checks)
    if gauge_checks["L2_covariance"] != 0 or gauge_checks["det_covariance"] != 0:
        raise AssertionError(gauge_checks)

    V1 = sp.Matrix([[2, 1], [0, 3], [0, 0], [0, 0]])
    V2 = sp.Matrix([[3, -1], [0, 3], [0, 4], [0, 0]])
    pair1 = pair_readout(V1)
    pair2 = pair_readout(V2)
    if pair1["u"] != pair2["u"]:
        raise AssertionError("synthetic pairs do not share the observer clock")
    cosine = sp.simplify(inner(pair1["n"], pair2["n"]))
    if cosine != sp.Rational(3, 5):
        raise AssertionError(cosine)

    boost = sp.Matrix(
        [
            [sp.Rational(5, 4), sp.Rational(3, 4), 0, 0],
            [sp.Rational(3, 4), sp.Rational(5, 4), 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ]
    )
    if sp.simplify(boost.T * ETA * boost - ETA) != sp.zeros(4):
        raise AssertionError("boost is not Lorentz")
    pair1_boost = pair_readout(boost * V1)
    pair2_boost = pair_readout(boost * V2)
    frame_checks = {
        "observer_angle": sp.simplify(inner(pair1_boost["n"], pair2_boost["n"]) - cosine),
    }
    if any(value != 0 for value in frame_checks.values()):
        raise AssertionError(frame_checks)

    data_points = [
        (Fraction(1), Fraction(0)),
        (Fraction(3, 5), Fraction(4, 5)),
        (Fraction(0), Fraction(1)),
        (Fraction(-1), Fraction(0)),
    ]
    data_weights = [Fraction(1), Fraction(2), Fraction(3), Fraction(4)]
    random_points = [
        (Fraction(1), Fraction(0)),
        (Fraction(0), Fraction(-1)),
        (Fraction(-3, 5), Fraction(4, 5)),
        (Fraction(-1), Fraction(0)),
        (Fraction(0), Fraction(1)),
    ]
    random_weights = [Fraction(1)] * len(random_points)
    DD, DD_total = auto_counts(data_points, data_weights)
    DR, DR_total = cross_counts(data_points, data_weights, random_points, random_weights)
    RR, RR_total = auto_counts(random_points, random_weights)
    dd = [value / DD_total for value in DD]
    dr = [value / DR_total for value in DR]
    rr = [value / RR_total for value in RR]
    if any(value == 0 for value in rr):
        raise AssertionError("synthetic RR bin is empty")
    landy_szalay = [(dd[i] - 2 * dr[i] + rr[i]) / rr[i] for i in range(3)]

    observed_pair = sp.Matrix([[5, 1, 2], [1, 4, 3], [2, 3, 6]])
    permutation = sp.Matrix([[0, 1, 0], [0, 0, 1], [1, 0, 0]])
    pulled_source = sp.simplify(permutation.T * observed_pair * permutation)
    reconstructed = sp.simplify(permutation * pulled_source * permutation.T)
    if reconstructed != observed_pair:
        raise AssertionError("finite pushforward nonidentifiability witness failed")

    # Separately typed terminal endpoint carries on the same two relation labels.
    terminal_Z = [sp.Integer(2), sp.Integer(3)]
    terminal_depth = [sp.log(value) for value in terminal_Z]
    if [sp.simplify(sp.exp(value)) for value in terminal_depth] != terminal_Z:
        raise AssertionError("terminal depth-to-redshift carry failed")

    result = {
        "status": "PASS",
        "outcome_artifacts_read": 0,
        "symbolic_type_checks": {key: str(value) for key, value in type_checks.items()},
        "gauge_checks": {
            "ruler_covariance": str(gauge_checks["ruler_covariance"]),
            "L2_covariance": str(gauge_checks["L2_covariance"]),
            "det_covariance": str(gauge_checks["det_covariance"]),
        },
        "synthetic_pairs": {
            "common_observer": True,
            "cos_theta": str(cosine),
            "observer_local_h1": str(pair1["h"]),
            "observer_local_h2": str(pair2["h"]),
            "terminal_depths_separately_typed": [str(value) for value in terminal_depth],
            "terminal_Z": [str(value) for value in terminal_Z],
        },
        "frame_checks": {key: str(value) for key, value in frame_checks.items()},
        "synthetic_estimator": {
            "DD": frac_strings(DD),
            "DR": frac_strings(DR),
            "RR": frac_strings(RR),
            "DD_total": str(DD_total),
            "DR_total": str(DR_total),
            "RR_total": str(RR_total),
            "landy_szalay": frac_strings(landy_szalay),
        },
        "source_nonidentifiability": {
            "permutation_reconstruction": True,
            "meaning": "distinct invertible sky map plus pulled-back source pair measure gives the same observed pair measure",
        },
        "maximum_conclusion": "COMPLETE_TWO_SOURCE_OBSERVABLE_EVALUATOR_DERIVED__DIRECTION_IDENTIFICATION_QUERY_OWNED__ENDPOINT_DEPTH_CARRY_CONDITIONAL__PHYSICAL_HISTORY_AND_SOURCE_PAIR_MEASURE_OPEN",
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
