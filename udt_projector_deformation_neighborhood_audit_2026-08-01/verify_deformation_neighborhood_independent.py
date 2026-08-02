#!/usr/bin/env python3
"""Independent no-SymPy replay of the projector-neighborhood algebra."""

from __future__ import annotations

import csv
import json
from fractions import Fraction as F
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def add_exterior(
    exterior: dict[tuple[int, int, int], F],
    upper: int,
    left: int,
    right: int,
    value: F,
) -> None:
    if left == right:
        return
    if left > right:
        left, right, value = right, left, -value
    exterior[(upper, left, right)] = exterior.get((upper, left, right), F(0)) + value


def cartan_vectors(data: dict[str, F]) -> dict[int, tuple[F, F]]:
    """Build the connection from exterior forms, not from production formulas."""

    exterior: dict[tuple[int, int, int], F] = {}
    p1, p2, p3 = data["p1"], data["p2"], data["p3"]
    add_exterior(exterior, 0, 1, 0, -p1)
    add_exterior(exterior, 0, 2, 0, -p2)
    add_exterior(exterior, 0, 3, 0, -p3)
    add_exterior(exterior, 0, 2, 3, data["t0"])
    add_exterior(exterior, 1, 1, 1, p1)
    add_exterior(exterior, 1, 2, 1, p2)
    add_exterior(exterior, 1, 3, 1, p3)
    add_exterior(exterior, 1, 2, 3, data["t1"])
    for out in range(2):
        for direction in (1, 2, 3):
            for column in range(2):
                add_exterior(
                    exterior,
                    out + 2,
                    direction,
                    column + 2,
                    data[f"L{direction}{out + 1}{column + 1}"],
                )
        for column in range(2):
            add_exterior(
                exterior,
                out + 2,
                1,
                column + 2,
                data["m"] * data[f"c{out + 1}{column + 1}"],
            )

    structure: dict[tuple[int, int, int], F] = {}
    for (upper, left, right), coefficient in exterior.items():
        structure[(upper, left, right)] = -coefficient
        structure[(upper, right, left)] = coefficient
    signs = (F(-1), F(1), F(1), F(1))

    def lower(out: int, left: int, right: int) -> F:
        return signs[out] * structure.get((out, left, right), F(0))

    def gamma(direction: int, acted: int, out: int) -> F:
        return (
            lower(out, direction, acted)
            - lower(direction, acted, out)
            + lower(acted, out, direction)
        ) / 2

    return {
        direction: (gamma(direction, 1, 2), gamma(direction, 1, 3))
        for direction in range(4)
    }


def wedge(left: tuple[F, F], right: tuple[F, F]) -> F:
    return left[0] * right[1] - left[1] * right[0]


def formula_response(data: dict[str, F]) -> tuple[F, F, F]:
    a = data["L111"] + data["c11"] * data["m"]
    b = (
        data["L112"]
        + data["L121"]
        + (data["c12"] + data["c21"]) * data["m"]
    ) / 2
    d = data["L122"] + data["c22"] * data["m"]
    w12 = data["p3"] * a - data["p2"] * (b + data["t1"] / 2)
    w13 = data["p3"] * (b - data["t1"] / 2) - data["p2"] * d
    w23 = a * d - b * b + data["t1"] * data["t1"] / 4
    return w12, w13, w23


def symmetric_data(lam: F, mu: F, nu: F) -> dict[str, F]:
    data = {
        "p1": F(3, 50),
        "p2": F(1, 50),
        "p3": F(2, 50),
        "t0": F(-1, 32),
        "t1": F(-2),
        "m": F(-2),
        "c11": F(0),
        "c12": F(-1),
        "c21": F(1),
        "c22": F(0),
    }
    matrix = ((lam + mu, nu), (nu, lam - mu))
    for direction, derivative in ((1, F(3, 50)), (2, F(1, 50)), (3, F(2, 50))):
        for row in range(2):
            for column in range(2):
                data[f"L{direction}{row + 1}{column + 1}"] = derivative * matrix[row][column]
    return data


def rotate(vector: tuple[F, F], rotation: tuple[tuple[F, F], tuple[F, F]]) -> tuple[F, F]:
    return (
        rotation[0][0] * vector[0] + rotation[0][1] * vector[1],
        rotation[1][0] * vector[0] + rotation[1][1] * vector[1],
    )


def main() -> int:
    checks: list[bool] = []
    center_table = {
        row["center"]: row for row in read_tsv(HERE / "CENTER_NEIGHBORHOOD_ATLAS.tsv")
    }
    centers = {
        "C01": F(-2),
        "C02": F(-1),
        "C03": F(0),
        "C04": F(1, 2),
        "C05": F(1),
        "C06": F(2),
    }
    exact_lines: list[str] = []
    for center, lam in centers.items():
        data = symmetric_data(lam, F(0), F(0))
        vectors = cartan_vectors(data)
        reconstructed = (
            wedge(vectors[1], vectors[2]),
            wedge(vectors[1], vectors[3]),
            wedge(vectors[2], vectors[3]),
        )
        direct = formula_response(data)
        expected_w23 = F(center_table[center]["relative_curvature_W23"])
        determinant = F(center_table[center]["clock_certificate_determinant"])
        checks.extend(
            (
                reconstructed == direct,
                direct[2] == expected_w23,
                direct[2] == 1 + F(9, 2500) * lam * lam,
                direct[2] != 0,
                determinant != 0,
            )
        )
        exact_lines.append(f"{center}:{direct[0]},{direct[1]},{direct[2]}")

    # The one-shear intersections and the full affine zero line are exact.
    zero_points = (
        (F(25, 2), F(-125, 6), F(0)),
        (F(-200, 9), F(0), F(-250, 9)),
    )
    for point in zero_points:
        data = symmetric_data(*point)
        vectors = cartan_vectors(data)
        response = (
            wedge(vectors[1], vectors[2]),
            wedge(vectors[1], vectors[3]),
            wedge(vectors[2], vectors[3]),
        )
        checks.extend((response == formula_response(data), response == (F(0), F(0), F(0))))
    for nu in (F(-7, 3), F(-1), F(0), F(2), F(11, 4)):
        lam = F(5, 4) * nu + F(25, 2)
        mu = -F(3, 4) * nu - F(125, 6)
        data = symmetric_data(lam, mu, nu)
        checks.append(formula_response(data) == (F(0), F(0), F(0)))

    # Independent arbitrary rational first-jet probes exercise the general formula.
    general_probes = (
        (F(2), F(1), F(-3)),
        (F(-4, 3), F(5, 2), F(7, 5)),
        (F(0), F(2), F(-1, 7)),
        (F(11, 9), F(-13, 8), F(17, 6)),
    )
    for lam, mu, nu in general_probes:
        data = symmetric_data(lam, mu, nu)
        vectors = cartan_vectors(data)
        reconstructed = (
            wedge(vectors[1], vectors[2]),
            wedge(vectors[1], vectors[3]),
            wedge(vectors[2], vectors[3]),
        )
        checks.append(reconstructed == formula_response(data))

    # SO(2) screen-frame changes preserve every oriented response scalar.
    data = symmetric_data(F(7, 5), F(-2, 3), F(4, 7))
    vectors = cartan_vectors(data)
    for rotation in (
        ((F(0), F(-1)), (F(1), F(0))),
        ((F(3, 5), F(-4, 5)), (F(4, 5), F(3, 5))),
    ):
        transformed = {key: rotate(value, rotation) for key, value in vectors.items()}
        for left, right in ((1, 2), (1, 3), (2, 3)):
            checks.append(wedge(transformed[left], transformed[right]) == wedge(vectors[left], vectors[right]))

    if not all(checks):
        raise AssertionError("independent rational replay failed")
    result = {
        "schema": "udt.projector_deformation_neighborhood.independent.v1",
        "status": "PASS",
        "implementation": "stdlib_Fraction_full_exterior_to_Cartan_no_SymPy_no_production_import",
        "check_count": len(checks),
        "center_count": len(centers),
        "general_probe_count": len(general_probes),
        "zero_line_samples": 5,
        "gauge_rotation_samples": 2,
        "exact_center_responses": exact_lines,
    }
    (HERE / "INDEPENDENT_RESULT.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
