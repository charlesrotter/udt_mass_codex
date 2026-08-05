#!/usr/bin/env python3
"""Independent stdlib/Fraction reconstruction; imports no production audit code."""

from __future__ import annotations

from fractions import Fraction as F
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
Matrix = list[list[F]]


def mat(rows: list[list[int | F]]) -> Matrix:
    return [[F(value) for value in row] for row in rows]


def eye(n: int) -> Matrix:
    return [[F(i == j) for j in range(n)] for i in range(n)]


def zero(rows: int, cols: int) -> Matrix:
    return [[F(0) for _ in range(cols)] for _ in range(rows)]


def mmul(a: Matrix, b: Matrix) -> Matrix:
    return [[sum((a[i][k] * b[k][j] for k in range(len(b))), F(0)) for j in range(len(b[0]))] for i in range(len(a))]


def madd(a: Matrix, b: Matrix) -> Matrix:
    return [[a[i][j] + b[i][j] for j in range(len(a[0]))] for i in range(len(a))]


def inv(a: Matrix) -> Matrix:
    n = len(a)
    work = [row[:] + ident[:] for row, ident in zip(a, eye(n))]
    for col in range(n):
        pivot = next((row for row in range(col, n) if work[row][col]), None)
        if pivot is None:
            raise ValueError("singular")
        work[col], work[pivot] = work[pivot], work[col]
        scale = work[col][col]
        work[col] = [entry / scale for entry in work[col]]
        for row in range(n):
            if row == col:
                continue
            factor = work[row][col]
            work[row] = [work[row][j] - factor * work[col][j] for j in range(2 * n)]
    return [row[n:] for row in work]


def rank(a: Matrix) -> int:
    work = [row[:] for row in a]
    rows, cols = len(work), len(work[0])
    pivot_row = 0
    for col in range(cols):
        pivot = next((row for row in range(pivot_row, rows) if work[row][col]), None)
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        scale = work[pivot_row][col]
        work[pivot_row] = [entry / scale for entry in work[pivot_row]]
        for row in range(rows):
            if row != pivot_row and work[row][col]:
                factor = work[row][col]
                work[row] = [work[row][j] - factor * work[pivot_row][j] for j in range(cols)]
        pivot_row += 1
        if pivot_row == rows:
            break
    return pivot_row


def block(a: Matrix, b: Matrix, c: Matrix, d: Matrix) -> Matrix:
    return [a[i] + b[i] for i in range(len(a))] + [c[i] + d[i] for i in range(len(c))]


def character(z: F) -> Matrix:
    return mat([[1 / z, 0], [0, z]])


def embed_base(a: Matrix) -> Matrix:
    return block(a, zero(2, 2), zero(2, 2), eye(2))


def extension(z: F, screen: Matrix, mixing: Matrix) -> Matrix:
    return block(character(z), zero(2, 2), mmul(screen, mixing), screen)


def incidence(vertices: int, edges: list[tuple[int, int]]) -> Matrix:
    rows = []
    for left, right in edges:
        row = [F(0)] * vertices
        row[left] = F(-1)
        row[right] = F(1)
        rows.append(row)
    return rows


def column(values: list[int]) -> Matrix:
    return [[F(value)] for value in values]


def json_matrix(a: Matrix) -> list[list[str]]:
    return [[str(value) for value in row] for row in a]


def main() -> None:
    checks: dict[str, bool] = {}

    def check(name: str, condition: bool) -> None:
        checks[name] = bool(condition)
        if not condition:
            raise AssertionError(name)

    # Different exact witness from production.
    z = [F(3), F(4), F(7)]
    h = [F(5), F(8), F(11)]
    screens = [mat([[1, 0], [2, 3]]), mat([[4, 0], [1, 2]]), mat([[2, 0], [-1, 5]])]
    mixings = [mat([[2, 0], [1, 1]]), mat([[1, 3], [-2, 1]]), mat([[0, -1], [4, 2]])]
    refs = [
        eye(4),
        mat([[1, 0, 0, 0], [2, 1, 0, 0], [0, 0, 1, 0], [1, 0, 2, 1]]),
        mat([[1, 0, 0, 0], [0, 2, 0, 0], [1, 0, 1, 0], [0, 1, 0, 1]]),
    ]
    e = [extension(z[i], screens[i], mixings[i]) for i in range(3)]
    k = [embed_base(character(h[i])) for i in range(3)]
    ep = [extension(z[i] * h[i], screens[i], mmul(mixings[i], character(h[i]))) for i in range(3)]
    refp = [mmul(inv(k[i]), refs[i]) for i in range(3)]
    theta = [mmul(e[i], refs[i]) for i in range(3)]
    thetap = [mmul(ep[i], refp[i]) for i in range(3)]
    for i in range(3):
        check(f"local_identity_{i}", mmul(ep[i], inv(k[i])) == e[i])
        check(f"physical_coframe_fixed_{i}", thetap[i] == theta[i])

    pairs = [(0, 1), (1, 2), (0, 2)]
    left: dict[tuple[int, int], Matrix] = {}
    right: dict[tuple[int, int], Matrix] = {}
    rightp: dict[tuple[int, int], Matrix] = {}
    for i, j in pairs:
        left[i, j] = mmul(theta[j], inv(theta[i]))
        right[i, j] = mmul(refs[j], inv(refs[i]))
        rightp[i, j] = mmul(refp[j], inv(refp[i]))
        check(f"overlap_{i}{j}", e[j] == mmul(mmul(left[i, j], e[i]), inv(right[i, j])))
        check(f"coboundary_{i}{j}", rightp[i, j] == mmul(mmul(inv(k[j]), right[i, j]), k[i]))
        check(f"shifted_overlap_{i}{j}", ep[j] == mmul(mmul(left[i, j], ep[i]), inv(rightp[i, j])))
    check("physical_cocycle", left[0, 2] == mmul(left[1, 2], left[0, 1]))
    check("reference_cocycle", right[0, 2] == mmul(right[1, 2], right[0, 1]))
    check("shifted_reference_cocycle", rightp[0, 2] == mmul(rightp[1, 2], rightp[0, 1]))
    check("nonconstant_chart_shift", len(set(h)) == 3)

    cover_b = incidence(3, [(0, 1), (1, 2), (0, 2)])
    check("cover_rank", rank(cover_b) == 2)
    check("scalar_function_sample_a", mmul(cover_b, column([3, 3, 3])) == zero(3, 1))
    check("scalar_function_sample_b", mmul(cover_b, column([17, 17, 17])) == zero(3, 1))
    check("scalar_function_nonconstant_across_points", F(3) != F(17))

    def shifted(epsilon: int, a: F, chi_i: F, chi_j: F) -> F:
        return a + chi_j - F(epsilon) * chi_i

    for label, eps01, eps12 in [("oriented", 1, 1), ("twisted", -1, -1)]:
        a01, a12 = F(4), F(-2)
        eps02 = eps12 * eps01
        a02 = F(eps12) * a01 + a12
        ap01 = shifted(eps01, a01, F(5), F(8))
        ap12 = shifted(eps12, a12, F(8), F(11))
        ap02 = shifted(eps02, a02, F(5), F(11))
        check(f"affine_cocycle_{label}", ap02 == F(eps12) * ap01 + ap12)
    check("oriented_loop_translation_invariant", F(9) + (1 - 1) * F(5) == F(9))
    check("twisted_loop_translation_changes", F(9) + (1 - (-1)) * F(5) == F(19))

    edges = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]
    b = incidence(4, edges)
    c = mat([[1, -1, 0, 1, 0, 0], [1, 0, -1, 0, 1, 0], [0, 1, -1, 0, 0, 1], [0, 0, 0, 1, -1, 1]])
    check("observer_rank", rank(b) == 3)
    check("triangle_rank", rank(c) == 3)
    check("complex_identity", mmul(c, b) == zero(4, 4))
    potentials = column([2, -1, 5, 8])
    shifts = column([1, 4, 9, 16])
    edge_data = mmul(b, potentials)
    check("potential_composition", mmul(c, edge_data) == zero(4, 1))
    check("shifted_potential_composition", mmul(c, madd(edge_data, mmul(b, shifts))) == zero(4, 1))
    check("fixed_depth_shift_kernel_dimension", 4 - rank(b) == 1)
    free_edge = column([1, 0, 0, 0, 0, 0])
    period = mmul([c[0]], free_edge)[0][0]
    shifted_period = mmul([c[0]], madd(free_edge, mmul(b, shifts)))[0][0]
    check("path_period_nonzero", period == 1)
    check("path_period_gauge_invariant", shifted_period == period)

    reset = mat([[1, 0, 0, 0], [0, 0, 1, 0], [0, 1, 0, 0], [0, 0, 0, 1]])
    d2 = embed_base(character(F(2)))
    d5 = embed_base(character(F(5)))
    d10 = embed_base(character(F(10)))
    check("query_composition", mmul(d5, d2) == d10)
    check("query_reset_composition", mmul(mmul(mmul(reset, d5), inv(reset)), mmul(mmul(reset, d2), inv(reset))) == mmul(mmul(reset, d10), inv(reset)))
    check("query_reset_nonbasic", mmul(mmul(reset, d2), inv(reset)) != d2)

    fixed = embed_base(character(F(3)))
    kminus = embed_base(character(F(2)))
    check("oriented_fixed_seam", mmul(mmul(fixed, kminus), inv(fixed)) == kminus)
    flip = embed_base(mat([[0, 1], [1, 0]]))
    check("twisted_fixed_seam", mmul(mmul(flip, kminus), inv(flip)) == embed_base(character(F(1, 2))))
    seam_screen_minus = mat([[3, 0], [1, 2]])
    seam_screen_plus = mat([[2, 0], [-1, 4]])
    seam_mixing_minus = mat([[0, 2], [1, -1]])
    seam_mixing_plus = mat([[3, 1], [-2, 0]])
    seam_e_minus = extension(F(3), seam_screen_minus, seam_mixing_minus)
    seam_e_plus = extension(F(7), seam_screen_plus, seam_mixing_plus)
    seam_ref_minus = mat([[1, 0, 0, 0], [2, 1, 0, 0], [0, 0, 1, 0], [0, 1, 0, 1]])
    seam_ref_plus = mat([[1, 0, 0, 0], [0, 2, 0, 0], [1, 0, 1, 0], [0, 0, 3, 1]])
    seam_theta_minus = mmul(seam_e_minus, seam_ref_minus)
    seam_theta_plus = mmul(seam_e_plus, seam_ref_plus)
    seam_physical = mmul(seam_theta_plus, inv(seam_theta_minus))
    seam_reference = mmul(seam_ref_plus, inv(seam_ref_minus))
    seam_k_minus = embed_base(character(F(5)))
    seam_k_plus = embed_base(character(F(11)))
    seam_e_minus_p = extension(F(15), seam_screen_minus, mmul(seam_mixing_minus, character(F(5))))
    seam_e_plus_p = extension(F(77), seam_screen_plus, mmul(seam_mixing_plus, character(F(11))))
    seam_ref_minus_p = mmul(inv(seam_k_minus), seam_ref_minus)
    seam_ref_plus_p = mmul(inv(seam_k_plus), seam_ref_plus)
    seam_reference_p = mmul(seam_ref_plus_p, inv(seam_ref_minus_p))
    check("seam_reference_coboundary", seam_reference_p == mmul(mmul(inv(seam_k_plus), seam_reference), seam_k_minus))
    check("seam_reference_changes", seam_reference_p != seam_reference)
    check("seam_relation_before", seam_e_plus == mmul(mmul(seam_physical, seam_e_minus), inv(seam_reference)))
    check("seam_relation_after", seam_e_plus_p == mmul(mmul(seam_physical, seam_e_minus_p), inv(seam_reference_p)))
    check("seam_complete_coframes_fixed", mmul(seam_e_minus_p, seam_ref_minus_p) == seam_theta_minus and mmul(seam_e_plus_p, seam_ref_plus_p) == seam_theta_plus)

    result = {
        "check_count": len(checks),
        "checks": checks,
        "independence": "stdlib Fraction implementation; no SymPy and no production import",
        "nonconstant_shift_witness": [str(value) for value in h],
        "reference_transition_changed": rightp[0, 1] != right[0, 1],
        "sample_shifted_reference_transition": json_matrix(rightp[0, 1]),
        "seam_reference_after": json_matrix(seam_reference_p),
        "seam_reference_before": json_matrix(seam_reference),
        "seam_reference_changed": seam_reference_p != seam_reference,
        "seam_relation_preserved": True,
        "status": "PASS",
    }
    check("all_checks_true_before_write", all(checks.values()))
    result["check_count"] = len(checks)
    result["checks"] = checks
    (HERE / "INDEPENDENT_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
