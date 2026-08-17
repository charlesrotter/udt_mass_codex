#!/usr/bin/env python3
"""Independent stdlib/Fraction replay of the load-bearing G147 identities."""

from __future__ import annotations

import hashlib
import json
from fractions import Fraction as F
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
Matrix = list[list[F]]


def transpose(a: Matrix) -> Matrix:
    return [list(row) for row in zip(*a)]


def matmul(a: Matrix, b: Matrix) -> Matrix:
    return [[sum(a[i][k] * b[k][j] for k in range(len(b))) for j in range(len(b[0]))]
            for i in range(len(a))]


def add(a: Matrix, b: Matrix) -> Matrix:
    return [[a[i][j] + b[i][j] for j in range(len(a[0]))] for i in range(len(a))]


def sub(a: Matrix, b: Matrix) -> Matrix:
    return [[a[i][j] - b[i][j] for j in range(len(a[0]))] for i in range(len(a))]


def scale(a: Matrix, factor: F) -> Matrix:
    return [[factor * value for value in row] for row in a]


def eye(n: int) -> Matrix:
    return [[F(int(i == j)) for j in range(n)] for i in range(n)]


def inverse(a: Matrix) -> Matrix:
    n = len(a)
    work = [a[i][:] + eye(n)[i] for i in range(n)]
    for col in range(n):
        pivot = next(row for row in range(col, n) if work[row][col] != 0)
        work[col], work[pivot] = work[pivot], work[col]
        factor = work[col][col]
        work[col] = [value / factor for value in work[col]]
        for row in range(n):
            if row == col:
                continue
            factor = work[row][col]
            work[row] = [work[row][j] - factor * work[col][j] for j in range(2 * n)]
    return [row[n:] for row in work]


def rref(a: Matrix) -> tuple[Matrix, list[int]]:
    out = [row[:] for row in a]
    rows, cols = len(out), len(out[0])
    pivots: list[int] = []
    row = 0
    for col in range(cols):
        pivot = next((i for i in range(row, rows) if out[i][col] != 0), None)
        if pivot is None:
            continue
        out[row], out[pivot] = out[pivot], out[row]
        factor = out[row][col]
        out[row] = [value / factor for value in out[row]]
        for i in range(rows):
            if i == row:
                continue
            factor = out[i][col]
            out[i] = [out[i][j] - factor * out[row][j] for j in range(cols)]
        pivots.append(col)
        row += 1
        if row == rows:
            break
    return out, pivots


def rank(a: Matrix) -> int:
    return len(rref(a)[1])


def nullspace(a: Matrix) -> Matrix:
    reduced, pivots = rref(a)
    free = [col for col in range(len(a[0])) if col not in pivots]
    vectors: list[list[F]] = []
    for free_col in free:
        vector = [F(0) for _ in range(len(a[0]))]
        vector[free_col] = F(1)
        for row, pivot_col in enumerate(pivots):
            vector[pivot_col] = -reduced[row][free_col]
        vectors.append(vector)
    return transpose(vectors)


def column(a: Matrix, index: int) -> Matrix:
    return [[row[index]] for row in a]


def hstack(a: Matrix, b: Matrix) -> Matrix:
    return [a[i] + b[i] for i in range(len(a))]


def vstack(a: Matrix, b: Matrix) -> Matrix:
    return a + b


def block(a: Matrix, b: Matrix, c: Matrix, d: Matrix) -> Matrix:
    return [a[i] + b[i] for i in range(len(a))] + [c[i] + d[i] for i in range(len(c))]


def equal(a: Matrix, b: Matrix) -> bool:
    return a == b


def determinant_2(a: Matrix) -> F:
    return a[0][0] * a[1][1] - a[0][1] * a[1][0]


def strings(a: Matrix) -> list[list[str]]:
    return [[str(value) for value in row] for row in a]


def projector(g: Matrix, k: Matrix) -> Matrix:
    gram = matmul(transpose(k), matmul(g, k))
    return sub(eye(len(g)), matmul(k, matmul(inverse(gram), matmul(transpose(k), g))))


def main() -> None:
    checks: dict[str, bool] = {}

    B = [[F(2), F(1, 2)], [F(0), F(3)]]
    Q = [[F(1), F(1, 3)], [F(0), F(2)]]
    S = [[F(1, 5), -F(1, 7)], [F(1, 4), F(1, 6)]]
    Y = eye(2)
    Z = [[F(1, 10), -F(1, 8)], [-F(1, 12), F(1, 9)]]
    zero = [[F(0), F(0)], [F(0), F(0)]]
    E = block(B, zero, matmul(Q, S), Q)
    eta = [[F(-1), F(0), F(0), F(0)], [F(0), F(1), F(0), F(0)],
           [F(0), F(0), F(1), F(0)], [F(0), F(0), F(0), F(1)]]
    g = matmul(transpose(E), matmul(eta, E))
    J = Y + Z
    h = matmul(transpose(J), matmul(g, J))
    J0, J1 = column(J, 0), column(J, 1)
    beta = h[0][1] / h[0][0]
    r = sub(J1, scale(J0, beta))
    K = hstack(J0, r)
    rho = F(2, 5)

    checks["registered_clock_timelike"] = h[0][0] < 0
    checks["registered_pair_lorentzian"] = determinant_2(h) < 0
    checks["rho_nonzero_inside_ball"] = rho != 0 and abs(rho) < 1
    checks["clock_ruler_orthogonal"] = matmul(transpose(J0), matmul(g, r))[0][0] == 0
    checks["ruler_positive"] = matmul(transpose(r), matmul(g, r))[0][0] > 0
    checks["flag_and_pair_span_equal"] = rank(hstack(J, K)) == 2

    P_pair = projector(g, J)
    P_flag = projector(g, K)
    checks["projectors_equal"] = equal(P_pair, P_flag)
    checks["projector_idempotent"] = equal(matmul(P_pair, P_pair), P_pair)
    checks["projector_metric_self_adjoint"] = equal(matmul(transpose(P_pair), g), matmul(g, P_pair))
    checks["projector_rank_two"] = rank(P_pair) == 2
    checks["projector_kills_clock"] = all(value[0] == 0 for value in matmul(P_pair, J0))
    checks["projector_kills_ruler"] = all(value[0] == 0 for value in matmul(P_pair, r))

    constraints_pair = matmul(transpose(J), g)
    constraints_directional = matmul(transpose(K), g)
    checks["constraint_rowspaces_equal"] = (
        rank(constraints_pair) == 2
        and rank(constraints_directional) == 2
        and rank(vstack(constraints_pair, constraints_directional)) == 2
    )
    H = nullspace(constraints_pair)
    H_gram = matmul(transpose(H), matmul(g, H))
    checks["screen_nullspace_rank_two"] = len(H[0]) == 2
    checks["screen_positive_first_minor"] = H_gram[0][0] > 0
    checks["screen_positive_determinant"] = determinant_2(H_gram) > 0

    def witness_metric_and_projector(
        bx: Matrix, qx: Matrix, sx: Matrix, yx: Matrix, zx: Matrix
    ) -> tuple[Matrix, Matrix]:
        ex = block(bx, zero, matmul(qx, sx), qx)
        gx = matmul(transpose(ex), matmul(eta, ex))
        jx = yx + zx
        hx = matmul(transpose(jx), matmul(gx, jx))
        return hx, projector(gx, jx)

    perturbations = {
        "B": (scale(B, F(2)), Q, S, Y, Z),
        "Q": (B, scale(Q, F(2)), S, Y, Z),
        "S": (B, Q, scale(S, F(2)), Y, Z),
        "Y": (B, Q, S, scale(Y, F(2)), Z),
        "Z": (B, Q, S, Y, scale(Z, F(2))),
    }
    for name, values in perturbations.items():
        h_changed, p_changed = witness_metric_and_projector(*values)
        checks[f"{name}_sensitivity_changes_h"] = not equal(h_changed, h)
        checks[f"{name}_sensitivity_changes_screen_projector"] = not equal(p_changed, P_pair)

    A = [[F(1), F(1, 3), F(0), F(0)], [F(0), F(1), F(1, 5), F(0)],
         [F(0), F(0), F(1), F(1, 7)], [F(0), F(0), F(0), F(1)]]
    A_inv = inverse(A)
    g_new = matmul(transpose(A), matmul(g, A))
    J_new = matmul(A_inv, J)
    h_new = matmul(transpose(J_new), matmul(g_new, J_new))
    P_new = projector(g_new, J_new)
    checks["ambient_basis_pair_metric_invariant"] = equal(h_new, h)
    checks["ambient_basis_projector_covariant"] = equal(P_new, matmul(A_inv, matmul(P_pair, A)))

    R = [[F(2), F(1, 3)], [F(0), F(3, 2)]]
    J_R = matmul(J, R)
    h_R = matmul(transpose(J_R), matmul(g, J_R))
    beta_R = h_R[0][1] / h_R[0][0]
    r_R = sub(column(J_R, 1), scale(column(J_R, 0), beta_R))
    checks["flag_domain_clock_line_same"] = rank(hstack(J0, column(J_R, 0))) == 1
    checks["flag_domain_ruler_line_mod_clock_same"] = rank(hstack(J0, hstack(r, r_R))) == 2
    checks["flag_domain_projector_same"] = equal(projector(g, J_R), P_pair)

    nonflag = [[F(1), F(1, 2)], [F(1, 3), F(1)]]
    J_changed = matmul(J, nonflag)
    checks["nonflag_change_changes_clock_line"] = rank(hstack(J0, column(J_changed, 0))) == 2

    with (HERE / "SOURCE_MANIFEST.tsv").open(encoding="utf-8") as handle:
        header = handle.readline().rstrip("\n").split("\t")
        rows = [dict(zip(header, line.rstrip("\n").split("\t"))) for line in handle]
    for index, row in enumerate(rows, start=1):
        digest = hashlib.sha256((ROOT / row["path"]).read_bytes()).hexdigest()
        checks[f"source_{index}_hash"] = digest == row["sha256"]

    failures = [name for name, passed in checks.items() if not passed]
    result = {
        "method": "independent Python stdlib Fraction matrix and row-space replay; no production imports",
        "landing": "INDEPENDENT_PASS" if not failures else "INDEPENDENT_FAILURE",
        "checks": checks,
        "passed": sum(checks.values()),
        "total": len(checks),
        "failures": failures,
        "witness": {
            "h": strings(h),
            "screen_gram": strings(H_gram),
            "screen_projector": strings(P_pair),
        },
    }
    (HERE / "INDEPENDENT_RESULT.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    if failures:
        raise SystemExit(f"FAIL: {failures}")
    print(f"PASS: {result['passed']}/{result['total']} independent G147 checks")


if __name__ == "__main__":
    main()
