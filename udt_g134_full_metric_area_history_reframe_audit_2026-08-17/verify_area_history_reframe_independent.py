#!/usr/bin/env python3
"""Independent Fraction-only checks for G134; does not import production code."""

from __future__ import annotations

import json
from fractions import Fraction as F
from pathlib import Path


PAIR_BASIS = ((0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3))
COMPONENTS = ((0, 0), (0, 1), (0, 2), (0, 3), (1, 1), (1, 2), (1, 3), (2, 2), (2, 3), (3, 3))
OUT = Path(__file__).with_name("INDEPENDENT_VERIFICATION.json")


def zeros(rows: int, cols: int) -> list[list[F]]:
    return [[F(0) for _ in range(cols)] for _ in range(rows)]


def transpose(a: list[list[F]]) -> list[list[F]]:
    return [list(row) for row in zip(*a)]


def matmul(a: list[list[F]], b: list[list[F]]) -> list[list[F]]:
    bt = transpose(b)
    return [[sum(x * y for x, y in zip(row, col)) for col in bt] for row in a]


def rank(a: list[list[F]]) -> int:
    m = [row[:] for row in a]
    rows = len(m)
    cols = len(m[0]) if rows else 0
    r = 0
    for c in range(cols):
        pivot = next((i for i in range(r, rows) if m[i][c]), None)
        if pivot is None:
            continue
        m[r], m[pivot] = m[pivot], m[r]
        scale = m[r][c]
        m[r] = [x / scale for x in m[r]]
        for i in range(rows):
            if i != r and m[i][c]:
                factor = m[i][c]
                m[i] = [x - factor * y for x, y in zip(m[i], m[r])]
        r += 1
        if r == rows:
            break
    return r


def determinant(a: list[list[F]]) -> F:
    m = [row[:] for row in a]
    n = len(m)
    det = F(1)
    for c in range(n):
        pivot = next((i for i in range(c, n) if m[i][c]), None)
        if pivot is None:
            return F(0)
        if pivot != c:
            m[c], m[pivot] = m[pivot], m[c]
            det = -det
        p = m[c][c]
        det *= p
        for i in range(c + 1, n):
            factor = m[i][c] / p
            for j in range(c + 1, n):
                m[i][j] -= factor * m[c][j]
    return det


def area_matrix(g: list[list[F]]) -> list[list[F]]:
    return [
        [g[i][k] * g[j][l] - g[i][l] * g[j][k] for k, l in PAIR_BASIS]
        for i, j in PAIR_BASIS
    ]


def dg(component: tuple[int, int], i: int, j: int) -> F:
    return F(int(tuple(sorted((i, j))) == component))


def area_jacobian(g: list[list[F]]) -> list[list[F]]:
    rows: list[list[F]] = []
    for p, (i, j) in enumerate(PAIR_BASIS):
        for q in range(p, len(PAIR_BASIS)):
            k, l = PAIR_BASIS[q]
            row = []
            for component in COMPONENTS:
                value = (
                    dg(component, i, k) * g[j][l]
                    + g[i][k] * dg(component, j, l)
                    - dg(component, i, l) * g[j][k]
                    - g[i][l] * dg(component, j, k)
                )
                row.append(value)
            rows.append(row)
    return rows


def scale(a: list[list[F]], c: F) -> list[list[F]]:
    return [[c * x for x in row] for row in a]


def main() -> None:
    eta = [[F(-1), F(0), F(0), F(0)], [F(0), F(1), F(0), F(0)], [F(0), F(0), F(1), F(0)], [F(0), F(0), F(0), F(1)]]
    L = [[F(1), F(0), F(0), F(0)], [F(1), F(1), F(0), F(0)], [F(2), F(-1), F(1), F(0)], [F(1), F(2), F(1), F(1)]]
    generic = matmul(transpose(L), matmul(eta, L))
    area_eta = area_matrix(eta)
    area_generic = area_matrix(generic)

    plus = [[F(-1), F(1, 2), F(0), F(0)], [F(1, 2), F(1), F(0), F(0)], [F(0), F(0), F(1), F(0)], [F(0), F(0), F(0), F(1)]]
    minus = [[F(-1), F(-1, 2), F(0), F(0)], [F(-1, 2), F(1), F(0), F(0)], [F(0), F(0), F(1), F(0)], [F(0), F(0), F(0), F(1)]]
    area_plus = area_matrix(plus)
    area_minus = area_matrix(minus)

    K = [[F(0), F(1)], [F(1), F(0)]]
    D = [[F(2), F(0)], [F(0), F(1, 2)]]
    U = [[F(1), F(1)], [F(0), F(1)]]

    s1, s2 = F(1, 4), F(4)
    sph1 = [[-s1, F(0), F(0), F(0)], [F(0), 1 / s1, F(0), F(0)], [F(0), F(0), F(1), F(0)], [F(0), F(0), F(0), F(1)]]
    sph2 = [[-s2, F(0), F(0), F(0)], [F(0), 1 / s2, F(0), F(0)], [F(0), F(0), F(1), F(0)], [F(0), F(0), F(0), F(1)]]

    checks = {
        "eta_jacobian_rank_10": rank(area_jacobian(eta)) == 10,
        "generic_jacobian_rank_10": rank(area_jacobian(generic)) == 10,
        "ambient_area_dimension_21": len(area_jacobian(eta)) == 21,
        "local_codimension_11": 21 - rank(area_jacobian(eta)) == 11,
        "eta_determinant_identity": determinant(area_eta) == determinant(eta) ** 3,
        "generic_determinant_identity": determinant(area_generic) == determinant(generic) ** 3,
        "scale_weight_two": area_matrix(scale(generic, F(3))) == scale(area_generic, F(9)),
        "global_sign_kernel": area_matrix(scale(generic, F(-1))) == area_generic,
        "nonunit_common_scale_detected": area_matrix(scale(generic, F(2))) != area_generic,
        "D_preserves_K": matmul(transpose(D), matmul(K, D)) == K,
        "D_determinant_one": determinant(D) == 1,
        "U_determinant_one": determinant(U) == 1,
        "U_not_K_orthogonal": matmul(transpose(U), matmul(K, U)) != K,
        "self_areas_match": [area_plus[i][i] for i in range(6)] == [area_minus[i][i] for i in range(6)],
        "cross_areas_separate": area_plus[1][3] == F(1, 2) and area_minus[1][3] == F(-1, 2),
        "full_area_separates": area_plus != area_minus,
        "spherical_reciprocal_base_determinants_match": determinant([row[:2] for row in sph1[:2]]) == -1 and determinant([row[:2] for row in sph2[:2]]) == -1,
        "spherical_full_areas_differ": area_matrix(sph1) != area_matrix(sph2),
        "spherical_curvature_witnesses": 2 * (1 - s1) == F(3, 2) and 2 * (1 - s2) == F(-6),
    }
    result = {
        "status": "PASS" if all(checks.values()) else "FAIL",
        "check_count": len(checks),
        "passed": sum(checks.values()),
        "method": "stdlib Fraction matrices and independent Gaussian elimination",
        "checks": checks,
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"{result['status']}: {result['passed']}/{result['check_count']} independent G134 checks")


if __name__ == "__main__":
    main()
