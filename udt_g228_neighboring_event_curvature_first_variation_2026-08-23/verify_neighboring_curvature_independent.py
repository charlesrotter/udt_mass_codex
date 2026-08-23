#!/usr/bin/env python3
"""Independent standard-library exact replay for G228.

This file intentionally does not import the production implementation or SymPy.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from fractions import Fraction as F
from pathlib import Path


BIVECTORS = ((0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3))
PAIR_INDEX = {pair: i for i, pair in enumerate(BIVECTORS)}
SLOTS = tuple((i, j) for i in range(6) for j in range(i, 6) if (i, j) != (2, 3))
DIRECTIONS = {
    "k": (F(1), F(0), F(0), F(1)),
    "l": (F(1, 2), F(0), F(0), F(-1, 2)),
    "s1": (F(0), F(1), F(0), F(0)),
    "s2": (F(0), F(0), F(1), F(0)),
}
ORDER = ("k", "l", "s1", "s2")


def q_bases():
    answer = []
    for i, j in SLOTS:
        q = [[F(0) for _ in range(6)] for _ in range(6)]
        q[i][j] = F(1)
        q[j][i] = F(1)
        q[2][3] = -q[0][5] + q[1][4]
        q[3][2] = q[2][3]
        answer.append(q)
    return answer


QB = q_bases()


def opair(a, b):
    if a == b:
        return 0, -1
    if a < b:
        return 1, PAIR_INDEX[(a, b)]
    return -1, PAIR_INDEX[(b, a)]


def rcomp(j, a, b, c, d):
    s1, i = opair(a, b)
    s2, k = opair(c, d)
    if not s1 or not s2:
        return F(0)
    return F(s1 * s2) * QB[j][i][k]


def bianchi_matrix():
    rows = []
    for e, a, b in itertools.combinations(range(4), 3):
        for c, d in BIVECTORS:
            row = [F(0)] * 80
            for j in range(20):
                row[e * 20 + j] += rcomp(j, a, b, c, d)
                row[a * 20 + j] += rcomp(j, b, e, c, d)
                row[b * 20 + j] += rcomp(j, e, a, c, d)
            rows.append(row)
    return rows


def rref(matrix):
    a = [row[:] for row in matrix]
    if not a:
        return a, []
    rows, cols = len(a), len(a[0])
    pivots = []
    r = 0
    for c in range(cols):
        pivot = next((i for i in range(r, rows) if a[i][c]), None)
        if pivot is None:
            continue
        a[r], a[pivot] = a[pivot], a[r]
        scale = a[r][c]
        a[r] = [value / scale for value in a[r]]
        for i in range(rows):
            if i == r or not a[i][c]:
                continue
            factor = a[i][c]
            a[i] = [a[i][j] - factor * a[r][j] for j in range(cols)]
        pivots.append(c)
        r += 1
        if r == rows:
            break
    return a, pivots


def nullspace(matrix):
    reduced, pivots = rref(matrix)
    cols = len(matrix[0])
    free = [j for j in range(cols) if j not in pivots]
    basis = []
    for free_col in free:
        vector = [F(0)] * cols
        vector[free_col] = F(1)
        for row_index, pivot_col in enumerate(pivots):
            vector[pivot_col] = -reduced[row_index][free_col]
        basis.append(vector)
    return basis


def rank(matrix):
    return len(rref(matrix)[1])


def transpose(matrix):
    return [list(col) for col in zip(*matrix)]


def matmul(a, b):
    bt = transpose(b)
    return [[sum((x * y for x, y in zip(row, col)), F(0)) for col in bt] for row in a]


def projection(names):
    rows = []
    for name in names:
        direction = DIRECTIONS[name]
        for component in range(20):
            row = [F(0)] * 80
            for mu, coefficient in enumerate(direction):
                row[mu * 20 + component] = coefficient
            rows.append(row)
    return rows


def matrix_hash(matrix):
    payload = "\n".join(",".join(str(x) for x in row) for row in matrix)
    return hashlib.sha256(payload.encode()).hexdigest()


def mm2(a, b):
    return [[sum((a[i][k] * b[k][j] for k in range(len(b))), F(0)) for j in range(len(b[0]))] for i in range(len(a))]


def madd(a, b):
    return [[a[i][j] + b[i][j] for j in range(len(a[0]))] for i in range(len(a))]


def msub(a, b):
    return [[a[i][j] - b[i][j] for j in range(len(a[0]))] for i in range(len(a))]


def mtranspose(a):
    return [list(x) for x in zip(*a)]


def diag2(a, b):
    z = F(0)
    return [a[0] + [z, z], a[1] + [z, z], [z, z] + b[0], [z, z] + b[1]]


def screen_checks():
    C = [[F(3, 5), F(-4, 5)], [F(4, 5), F(3, 5)]]
    J = [[F(0), F(-1)], [F(1), F(0)]]
    Omega = [[F(7, 3) * x for x in row] for row in J]
    Cp = mm2(C, Omega)
    T = [[F(2), F(3)], [F(3), F(5)]]
    Tp = [[F(7), F(11)], [F(11), F(13)]]
    Ct = mtranspose(C)
    TE = mm2(mm2(Ct, T), C)
    TEp = madd(madd(mm2(mm2(mtranspose(Cp), T), C), mm2(mm2(Ct, Tp), C)), mm2(mm2(Ct, T), Cp))
    cov = msub(madd(TEp, msub(mm2(Omega, TE), mm2(TE, Omega))), mm2(mm2(Ct, Tp), C))

    I = [[F(1), F(0)], [F(0), F(1)]]
    Z = [[F(0), F(0)], [F(0), F(0)]]
    Apar = [Z[0] + I[0], Z[1] + I[1], [-x for x in T[0]] + Z[0], [-x for x in T[1]] + Z[1]]
    H = diag2(C, C)
    Hp = diag2(Cp, Cp)
    Ht = mtranspose(H)
    changed = msub(mm2(mm2(Ht, Apar), H), mm2(Ht, Hp))
    expected = [
        [-x for x in Omega[0]] + I[0],
        [-x for x in Omega[1]] + I[1],
        [-x for x in TE[0]] + [-x for x in Omega[0]],
        [-x for x in TE[1]] + [-x for x in Omega[1]],
    ]
    J4 = [Z[0] + I[0], Z[1] + I[1], [-x for x in I[0]] + Z[0], [-x for x in I[1]] + Z[1]]
    ham = madd(mm2(mtranspose(expected), J4), mm2(J4, expected))
    zero2 = [[F(0), F(0)], [F(0), F(0)]]
    zero4 = [[F(0)] * 4 for _ in range(4)]
    omitted = msub(TEp, mm2(mm2(Ct, Tp), C))
    return {
        "covariant_tide_identity": cov == zero2,
        "phase_change_identity": changed == expected,
        "hamiltonian_generator": ham == zero4,
        "omitted_commutator_detected": omitted != zero2,
    }


def derive():
    b = bianchi_matrix()
    brank = rank(b)
    ker_columns = nullspace(b)
    kernel = transpose(ker_columns)
    census = []
    for size in range(1, 5):
        for names in itertools.combinations(ORDER, size):
            image = matmul(projection(names), kernel)
            image_rank = rank(image)
            target = 20 * size
            census.append({
                "key": "+".join(names),
                "size": size,
                "target_dimension": target,
                "image_rank": image_rank,
                "codimension": target - image_rank,
                "image_sha256": matrix_hash(image),
            })
    restricted = [row["size"] for row in census if row["codimension"]]
    result = {
        "differential_bianchi_generated_rows": len(b),
        "differential_bianchi_independent_rank": brank,
        "compatible_module_dimension": 80 - brank,
        "bianchi_matrix_sha256": matrix_hash(b),
        "kernel_matrix_sha256": matrix_hash(kernel),
        "first_restricted_subset_size": min(restricted) if restricted else None,
        "subset_census": census,
        "screen_and_phase": screen_checks(),
    }
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=Path(__file__).resolve().parent / "INDEPENDENT_VERIFICATION.json")
    parser.add_argument("--no-write", action="store_true")
    args = parser.parse_args()
    result = derive()
    if not args.no_write:
        args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
