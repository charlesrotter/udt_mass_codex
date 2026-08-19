#!/usr/bin/env python3
"""Independent stdlib exact-rational replay for G179; no production imports."""

from __future__ import annotations

import csv
import hashlib
import json
import random
from fractions import Fraction as F
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent


def transpose(a: list[list[F]]) -> list[list[F]]:
    return [list(row) for row in zip(*a)]


def matmul(a: list[list[F]], b: list[list[F]]) -> list[list[F]]:
    return [
        [sum((a[i][k] * b[k][j] for k in range(len(b))), F(0)) for j in range(len(b[0]))]
        for i in range(len(a))
    ]


def add(a: list[list[F]], b: list[list[F]]) -> list[list[F]]:
    return [[a[i][j] + b[i][j] for j in range(len(a[0]))] for i in range(len(a))]


def scale(a: list[list[F]], c: F) -> list[list[F]]:
    return [[c * value for value in row] for row in a]


def det2(a: list[list[F]]) -> F:
    return a[0][0] * a[1][1] - a[0][1] * a[1][0]


def inverse2(a: list[list[F]]) -> list[list[F]]:
    determinant = det2(a)
    return [
        [a[1][1] / determinant, -a[0][1] / determinant],
        [-a[1][0] / determinant, a[0][0] / determinant],
    ]


def block_e(
    b: list[list[F]], q: list[list[F]], s: list[list[F]]
) -> list[list[F]]:
    qs = matmul(q, s)
    return [
        [b[0][0], b[0][1], F(0), F(0)],
        [b[1][0], b[1][1], F(0), F(0)],
        [qs[0][0], qs[0][1], q[0][0], q[0][1]],
        [qs[1][0], qs[1][1], q[1][0], q[1][1]],
    ]


def pullback(e: list[list[F]], j: list[list[F]]) -> list[list[F]]:
    v = matmul(e, j)
    signs = [F(-1), F(1), F(1), F(1)]
    return [
        [
            sum((signs[a] * v[a][i] * v[a][k] for a in range(4)), F(0))
            for k in range(2)
        ]
        for i in range(2)
    ]


def block_pullback(
    b: list[list[F]],
    q: list[list[F]],
    s: list[list[F]],
    y: list[list[F]],
    z: list[list[F]],
) -> list[list[F]]:
    u = matmul(b, y)
    r = add(matmul(s, y), z)
    a = matmul(q, r)
    return [
        [
            -u[0][i] * u[0][k]
            + u[1][i] * u[1][k]
            + a[0][i] * a[0][k]
            + a[1][i] * a[1][k]
            for k in range(2)
        ]
        for i in range(2)
    ]


def rank_two(j: list[list[F]]) -> bool:
    for a in range(4):
        for b in range(a + 1, 4):
            if j[a][0] * j[b][1] - j[a][1] * j[b][0] != 0:
                return True
    return False


def random_invertible_2(rng: random.Random) -> list[list[F]]:
    while True:
        value = [[F(rng.randint(-4, 4)) for _ in range(2)] for _ in range(2)]
        if det2(value) != 0:
            return value


def random_matrix(rng: random.Random, rows: int, cols: int, nonzero: bool = False) -> list[list[F]]:
    choices = [-4, -3, -2, -1, 1, 2, 3, 4] if nonzero else list(range(-4, 5))
    return [[F(rng.choice(choices)) for _ in range(cols)] for _ in range(rows)]


def source_hashes() -> tuple[int, list[str]]:
    rows = list(csv.DictReader((HERE / "SOURCE_MANIFEST.tsv").open(), delimiter="\t"))
    failures = []
    for row in rows:
        actual = hashlib.sha256((ROOT / row["path"]).read_bytes()).hexdigest()
        if actual != row["sha256"]:
            failures.append(row["path"])
    return len(rows), failures


def main() -> None:
    rng = random.Random(179)
    target = 20_000
    accepted = 0
    attempts = 0

    boost = [
        [F(5, 3), F(4, 3), F(0), F(0)],
        [F(4, 3), F(5, 3), F(0), F(0)],
        [F(0), F(0), F(0), F(-1)],
        [F(0), F(0), F(1), F(0)],
    ]
    coordinate = [
        [F(1), F(1), F(0), F(0)],
        [F(0), F(1), F(1), F(0)],
        [F(0), F(0), F(1), F(1)],
        [F(0), F(0), F(0), F(1)],
    ]
    coordinate_inverse = [
        [F(1), F(-1), F(1), F(-1)],
        [F(0), F(1), F(-1), F(1)],
        [F(0), F(0), F(1), F(-1)],
        [F(0), F(0), F(0), F(1)],
    ]

    while accepted < target:
        attempts += 1
        b = random_invertible_2(rng)
        q = random_invertible_2(rng)
        s = random_matrix(rng, 2, 2, nonzero=True)
        # Generate an exact Lorentzian two-plane in coframe components, then
        # solve the invertible block coframe for J. This avoids filtering the
        # overwhelming spacelike-plane majority without weakening the test.
        spatial0 = [F(rng.randint(-2, 2)) for _ in range(3)]
        spatial1 = [F(rng.randint(-4, 4)) for _ in range(3)]
        if spatial1 == [F(0), F(0), F(0)]:
            spatial1[0] = F(1)
        v = [
            [F(rng.randint(8, 12)), F(0)],
            [spatial0[0], spatial1[0]],
            [spatial0[1], spatial1[1]],
            [spatial0[2], spatial1[2]],
        ]
        u = v[:2]
        a = v[2:]
        y = matmul(inverse2(b), u)
        z = add(matmul(inverse2(q), a), scale(matmul(s, y), F(-1)))
        j = y + z
        if not rank_two(j):
            raise SystemExit("FAIL: constructed rank-two pair")
        e = block_e(b, q, s)
        h = pullback(e, j)
        determinant = det2(h)
        if not (h[0][0] < 0 and determinant < 0):
            raise SystemExit("FAIL: constructed Lorentzian pair")
        accepted += 1

        if h != block_pullback(b, q, s, y, z):
            raise SystemExit("FAIL: complete block pullback")

        t2 = -h[0][0]
        beta = h[0][1] / h[0][0]
        l2 = h[1][1] - h[0][1] ** 2 / h[0][0]
        m2 = -determinant
        if t2 * l2 != m2 or t2 <= 0 or l2 <= 0 or m2 <= 0:
            raise SystemExit("FAIL: reciprocal density identity")
        reconstructed = [
            [-t2, -t2 * beta],
            [-t2 * beta, l2 - t2 * beta**2],
        ]
        if reconstructed != h:
            raise SystemExit("FAIL: shifted reconstruction")

        if pullback(matmul(boost, e), j) != h:
            raise SystemExit("FAIL: Lorentz coframe gauge")
        e_prime = matmul(e, coordinate_inverse)
        j_prime = matmul(coordinate, j)
        if pullback(e_prime, j_prime) != h:
            raise SystemExit("FAIL: ambient coordinate covariance")

        k = F(rng.choice([-4, -3, -2, -1, 1, 2, 3, 4]))
        j_scaled = [[row[0], k * row[1]] for row in j]
        h_scaled = pullback(e, j_scaled)
        expected_scaled = [[h[0][0], k * h[0][1]], [k * h[1][0], k**2 * h[1][1]]]
        if h_scaled != expected_scaled or det2(h_scaled) != k**2 * determinant:
            raise SystemExit("FAIL: auxiliary ruler density covariance")

        # Independent time-live coefficient: d(EJ)=dE J+E dJ and
        # d(V^T eta V)=dV^T eta V+V^T eta dV.
        de = random_matrix(rng, 4, 4)
        dj = random_matrix(rng, 4, 2)
        v = matmul(e, j)
        dv = add(matmul(de, j), matmul(e, dj))
        signs = [F(-1), F(1), F(1), F(1)]
        dot_h = [
            [
                sum(
                    (
                        signs[a]
                        * (dv[a][i] * v[a][k] + v[a][i] * dv[a][k])
                        for a in range(4)
                    ),
                    F(0),
                )
                for k in range(2)
            ]
            for i in range(2)
        ]
        dot_g = add(
            matmul(matmul(transpose(de), [[F(-1), F(0), F(0), F(0)], [F(0), F(1), F(0), F(0)], [F(0), F(0), F(1), F(0)], [F(0), F(0), F(0), F(1)]]), e),
            matmul(matmul(transpose(e), [[F(-1), F(0), F(0), F(0)], [F(0), F(1), F(0), F(0)], [F(0), F(0), F(1), F(0)], [F(0), F(0), F(0), F(1)]]), de),
        )
        g = matmul(matmul(transpose(e), [[F(-1), F(0), F(0), F(0)], [F(0), F(1), F(0), F(0)], [F(0), F(0), F(1), F(0)], [F(0), F(0), F(0), F(1)]]), e)
        product_dot = add(
            add(matmul(matmul(transpose(dj), g), j), matmul(matmul(transpose(j), dot_g), j)),
            matmul(matmul(transpose(j), g), dj),
        )
        if dot_h != product_dot:
            raise SystemExit("FAIL: query-live product rule")

    # Independently replay the two exact registered witnesses.
    b0 = [[F(2), F(-2)], [F(2), F(1)]]
    q0 = [[F(1), F(2)], [F(2), F(3)]]
    s0 = [[F(-1), F(1)], [F(-1), F(-1)]]
    y0 = [[F(3), F(2)], [F(-3), F(1)]]
    z0 = [[F(1), F(-2)], [F(2), F(-3)]]
    exact_h = pullback(block_e(b0, q0, s0), y0 + z0)
    if exact_h != [[F(-118), F(102)], [F(102), F(822)]]:
        raise SystemExit(f"FAIL: exact full witness {exact_h}")
    singular_y = [[F(-8), F(0)], [F(2), F(0)]]
    singular_z = [[F(-6), F(3)], [F(-6), F(-6)]]
    singular_j = singular_y + singular_z
    singular_h = pullback(block_e(b0, q0, s0), singular_j)
    if det2(singular_y) != 0 or not rank_two(singular_j):
        raise SystemExit("FAIL: singular-Y typing")
    if not (singular_h[0][0] < 0 and det2(singular_h) < 0):
        raise SystemExit("FAIL: singular-Y regularity")

    source_count, failures = source_hashes()
    result = {
        "audit": "G179",
        "status": "PASS" if source_count == 10 and not failures else "FAIL",
        "exact_fraction_regular_trials": accepted,
        "attempts": attempts,
        "controls_per_trial": [
            "block_pullback",
            "shifted_reconstruction",
            "reciprocal_density",
            "lorentz_coframe_gauge",
            "ambient_coordinate_covariance",
            "auxiliary_ruler_reparameterization_and_orientation",
            "query_live_product_rule",
        ],
        "full_witness_h": [[str(v) for v in row] for row in exact_h],
        "singular_Y_h": [[str(v) for v in row] for row in singular_h],
        "source_count": source_count,
        "source_hash_failures": failures,
    }
    (HERE / "INDEPENDENT_VERIFICATION.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n"
    )
    if result["status"] != "PASS":
        raise SystemExit(f"FAIL: source hashes {failures}")
    print(
        f"PASS: {accepted} independent exact Fraction witnesses in {attempts} attempts; "
        "all covariance, density, block, and live controls"
    )


if __name__ == "__main__":
    main()
