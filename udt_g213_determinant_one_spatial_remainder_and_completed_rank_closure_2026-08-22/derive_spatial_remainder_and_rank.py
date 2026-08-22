#!/usr/bin/env python3
"""Dependency-free exact algebraic production replay for G213; writes no files."""

from fractions import Fraction as F
import json


checks = {}


def check(name, condition):
    value = bool(condition)
    checks[name] = value
    if not value:
        raise AssertionError(name)


def rank(matrix):
    work = [[F(value) for value in row] for row in matrix]
    pivot_row = 0
    for column in range(len(work[0])):
        pivot = next((row for row in range(pivot_row, len(work)) if work[row][column]), None)
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        lead = work[pivot_row][column]
        work[pivot_row] = [value / lead for value in work[pivot_row]]
        for row in range(len(work)):
            if row != pivot_row and work[row][column]:
                factor = work[row][column]
                work[row] = [left - factor * right for left, right in zip(work[row], work[pivot_row])]
        pivot_row += 1
    return pivot_row


def transpose(matrix):
    return [list(row) for row in zip(*matrix)]


def matmul(left, right):
    right_t = transpose(right)
    return [[sum((a * b for a, b in zip(row, column)), F(0)) for column in right_t] for row in left]


def det2(matrix):
    return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]


def det3(matrix):
    return (
        matrix[0][0] * (matrix[1][1] * matrix[2][2] - matrix[1][2] * matrix[2][1])
        - matrix[0][1] * (matrix[1][0] * matrix[2][2] - matrix[1][2] * matrix[2][0])
        + matrix[0][2] * (matrix[1][0] * matrix[2][1] - matrix[1][1] * matrix[2][0])
    )


# Unique logarithmic 1+2+2 decomposition of Sym_0(3).
grade = [[2, 0, 0], [0, -1, 0], [0, 0, -1]]
mix_1 = [[0, 1, 0], [1, 0, 0], [0, 0, 0]]
mix_2 = [[0, 0, 1], [0, 0, 0], [1, 0, 0]]
screen_1 = [[0, 0, 0], [0, 1, 0], [0, 0, -1]]
screen_2 = [[0, 0, 0], [0, 0, 1], [0, 1, 0]]
bases = [grade, mix_1, mix_2, screen_1, screen_2]

check("log_coordinate_symmetric", all(matrix == transpose(matrix) for matrix in bases))
check("log_coordinate_tracefree", all(sum(matrix[i][i] for i in range(3)) == 0 for matrix in bases))

# Rows are x00,x01,x02,x11,x12; columns are gamma,w1,w2,s1,s2.
coordinate_jacobian = [
    [2, 0, 0, 0, 0],
    [0, 1, 0, 0, 0],
    [0, 0, 1, 0, 0],
    [-1, 0, 0, 1, 0],
    [0, 0, 0, 0, 1],
]
check("grade_dimension_one", rank([[row[0]] for row in coordinate_jacobian]) == 1)
check("mix_dimension_two", rank([[row[1], row[2]] for row in coordinate_jacobian]) == 2)
check("screen_dimension_two", rank([[row[3], row[4]] for row in coordinate_jacobian]) == 2)
check("full_log_coordinate_rank_five", rank(coordinate_jacobian) == 5)
check("g207_g208_tangent_rank_four", rank([row[1:] for row in coordinate_jacobian]) == 4)
reordered = [[row[1], row[2], row[3], row[4], row[0]] for row in coordinate_jacobian]
check("grading_completes_rank_five", rank(reordered) == 5)

# Exact inverse: gamma=x00/2, w=(x01,x02), s=(x11+x00/2,x12).
coordinate_inverse = [
    [F(1, 2), 0, 0, 0, 0],
    [0, 1, 0, 0, 0],
    [0, 0, 1, 0, 0],
    [F(1, 2), 0, 0, 1, 0],
    [0, 0, 0, 0, 1],
]
identity_5 = [[F(int(row == column)) for column in range(5)] for row in range(5)]
check(
    "log_coordinate_inverse",
    matmul(coordinate_inverse, coordinate_jacobian) == identity_5
    and matmul(coordinate_jacobian, coordinate_inverse) == identity_5,
)


def schur_build(root_a, u1, u2, p, q):
    """Build the exact Schur chart with a=root_a**2 and det(B)=1."""
    a = root_a**2
    B = [[p, q], [q, (1 + q**2) / p]]
    middle = [
        [a, F(0), F(0)],
        [F(0), B[0][0] / root_a, B[0][1] / root_a],
        [F(0), B[1][0] / root_a, B[1][1] / root_a],
    ]
    lower = [[F(1), F(0), F(0)], [u1, F(1), F(0)], [u2, F(0), F(1)]]
    return B, matmul(matmul(lower, middle), transpose(lower))


schur_controls = [
    (F(1), F(0), F(0), F(1), F(0)),
    (F(2), F(1, 3), F(-2, 5), F(3, 2), F(1, 4)),
    (F(3, 2), F(-4, 7), F(5, 6), F(5, 3), F(-2, 9)),
    (F(4, 3), F(7, 8), F(1, 5), F(9, 4), F(3, 7)),
]
screen_det_ok = True
relative_det_ok = True
extract_a_ok = True
extract_mixing_ok = True
extract_screen_ok = True
parameter_roundtrip_ok = True
for root_a, u1, u2, p, q in schur_controls:
    B, relative = schur_build(root_a, u1, u2, p, q)
    a = root_a**2
    c = [relative[1][0], relative[2][0]]
    schur = [
        [relative[1][1] - c[0] ** 2 / a, relative[1][2] - c[0] * c[1] / a],
        [relative[2][1] - c[1] * c[0] / a, relative[2][2] - c[1] ** 2 / a],
    ]
    extracted_B = [[root_a * value for value in row] for row in schur]
    screen_det_ok &= det2(B) == 1
    relative_det_ok &= det3(relative) == 1
    extract_a_ok &= relative[0][0] == a
    extract_mixing_ok &= [value / a for value in c] == [u1, u2]
    extract_screen_ok &= extracted_B == B
    parameter_roundtrip_ok &= (
        relative[0][0], c[0] / a, c[1] / a, extracted_B[0][0], extracted_B[0][1]
    ) == (a, u1, u2, p, q)

check("screen_B_det_one", screen_det_ok)
check("schur_R_det_one", relative_det_ok)
check("schur_extract_a", extract_a_ok)
check("schur_extract_mixing", extract_mixing_ok)
check("schur_extract_screen", extract_screen_ok)
check("schur_global_parameter_rank_five", parameter_roundtrip_ok)

# G176 completed tuple is exactly equivalent to the auxiliary pullback when m is retained.
pair_controls = [
    (F(1), F(0), F(1)),
    (F(2), F(1, 5), F(3)),
    (F(5, 3), F(-2, 7), F(7, 4)),
]
auxiliary_det_ok = True
completed_det_ok = True
roundtrip_ok = True
clock_ok = True
shift_ok = True
for T, beta, length in pair_controls:
    h00 = -T**2
    h01 = -T**2 * beta
    h11 = length**2 - T**2 * beta**2
    m = T * length
    hs00, hs01, hs11 = h00, h01 / m, h11 / m**2
    auxiliary_det_ok &= h00 * h11 - h01**2 == -m**2
    completed_det_ok &= hs00 * hs11 - hs01**2 == -1
    roundtrip_ok &= (hs00, m * hs01, m**2 * hs11) == (h00, h01, h11)
    clock_ok &= hs00 == -T**2
    shift_ok &= hs01 == -T * beta / length

check("auxiliary_determinant", auxiliary_det_ok)
check("completed_determinant_minus_one", completed_det_ok)
check("completed_tuple_roundtrip", roundtrip_ok)
check("completed_clock_retained", clock_ok)
check("completed_shift_retained", shift_ok)

# Exact G129 six-plane restriction design.
directions = [(1, 0, 0), (0, 1, 0), (0, 0, 1), (1, 1, 0), (1, 0, 1), (0, 1, 1)]
design = []
for v1, v2, v3 in directions:
    design.extend([
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, v1, v2, v3, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, v1**2, 2*v1*v2, 2*v1*v3, v2**2, 2*v2*v3, v3**2],
    ])
design_rank = rank(design)
check("g129_six_plane_rank_ten", design_rank == 10)

# Without m, a common positive spatial calibration rescaling is exactly invisible.
density_blind_equal = True
auxiliary_changes = True
for aa, bb, mm, scale in [
    (F(-1), F(1, 3), F(4, 3), F(3, 2)),
    (F(-2), F(-2, 5), F(7, 4), F(5, 3)),
]:
    cc = (bb**2 - mm**2) / aa
    completed = (aa, bb / mm, cc / mm**2)
    scaled = (aa, scale * bb / (scale * mm), scale**2 * cc / (scale * mm) ** 2)
    density_blind_equal &= scaled == completed
    auxiliary_changes &= (aa, scale * bb, scale**2 * cc) != (aa, bb, cc)

check("density_blind_completed_metric_equal", density_blind_equal)
check("density_blind_auxiliary_metric_changes", auxiliary_changes)

result = {
    "audit": "G213",
    "status": "PASS",
    "landing": "FIVE_MODE_REMAINDER__G207_G208_COVER_FOUR__DENSITY_COMPLETES_RANK_TEN",
    "method": "stdlib_fraction_exact_algebra_and_explicit_inverse_maps",
    "exact_algebra_checks": len(checks),
    "all_checks_pass": all(checks.values()),
    "checks": checks,
    "mode_count": {"grading": 1, "radial_screen_mixing": 2, "tracefree_screen_shape": 2, "total": 5},
    "prior_tile_tangent_coverage": {"G207": 2, "G208": 2, "union": 4, "missing_independent_mode": "radial_versus_screen_grading"},
    "g129_design_rank": design_rank,
    "maximum_conclusion": "local_metric_decomposition_and_rank_reconstruction_only",
}
print(json.dumps(result, sort_keys=True))
