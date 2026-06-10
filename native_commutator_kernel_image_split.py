from fractions import Fraction
from itertools import combinations


def mat_zero():
    return [[Fraction(0) for _ in range(3)] for _ in range(3)]


def mat_unit(i, j):
    m = mat_zero()
    m[i][j] = Fraction(1)
    return m


def mat_add(a, b):
    return [[a[i][j] + b[i][j] for j in range(3)] for i in range(3)]


def mat_sub(a, b):
    return [[a[i][j] - b[i][j] for j in range(3)] for i in range(3)]


def mat_mul(a, b):
    return [
        [sum(a[i][k] * b[k][j] for k in range(3)) for j in range(3)]
        for i in range(3)
    ]


def commutator(a, b):
    return mat_sub(mat_mul(a, b), mat_mul(b, a))


def flatten(a):
    return [a[i][j] for i in range(3) for j in range(3)]


def rank(rows):
    if not rows:
        return 0
    a = [row[:] for row in rows]
    n_rows = len(a)
    n_cols = len(a[0])
    r = 0
    for c in range(n_cols):
        pivot = None
        for i in range(r, n_rows):
            if a[i][c] != 0:
                pivot = i
                break
        if pivot is None:
            continue
        a[r], a[pivot] = a[pivot], a[r]
        inv = 1 / a[r][c]
        a[r] = [inv * x for x in a[r]]
        for i in range(n_rows):
            if i != r and a[i][c] != 0:
                factor = a[i][c]
                a[i] = [a[i][j] - factor * a[r][j] for j in range(n_cols)]
        r += 1
        if r == n_rows:
            break
    return r


def basis_antisymmetric():
    return [mat_sub(mat_unit(i, j), mat_unit(j, i)) for i, j in combinations(range(3), 2)]


def basis_symmetric_traceless():
    offdiag = [mat_add(mat_unit(i, j), mat_unit(j, i)) for i, j in combinations(range(3), 2)]
    diag1 = mat_sub(mat_unit(0, 0), mat_unit(1, 1))
    diag2 = mat_sub(mat_unit(1, 1), mat_unit(2, 2))
    return offdiag + [diag1, diag2]


def commutator_rows(left, right, same_space=False):
    pairs = combinations(range(len(left)), 2) if same_space else (
        (i, j) for i in range(len(left)) for j in range(len(right))
    )
    if same_space:
        return [flatten(commutator(left[i], left[j])) for i, j in pairs]
    return [flatten(commutator(left[i], right[j])) for i, j in pairs]


def main():
    a3 = basis_antisymmetric()
    s5 = basis_symmetric_traceless()
    t8 = a3 + s5
    trace = [mat_add(mat_add(mat_unit(0, 0), mat_unit(1, 1)), mat_unit(2, 2))]

    blocks = {
        "trace_wedge_T8": (8, commutator_rows(trace, t8)),
        "Lambda2_A3": (3, commutator_rows(a3, a3, same_space=True)),
        "A3_wedge_S5": (15, commutator_rows(a3, s5)),
        "Lambda2_S5": (10, commutator_rows(s5, s5, same_space=True)),
    }

    block_report = {}
    for name, (domain_dim, rows) in blocks.items():
        image_rank = rank(rows)
        block_report[name] = {
            "domain_dim": domain_dim,
            "image_rank": image_rank,
            "kernel_dim_within_block": domain_dim - image_rank,
        }

    active_rows = (
        blocks["Lambda2_A3"][1]
        + blocks["A3_wedge_S5"][1]
        + blocks["Lambda2_S5"][1]
    )
    full_rows = blocks["trace_wedge_T8"][1] + active_rows
    a_output_rows = blocks["Lambda2_A3"][1] + blocks["Lambda2_S5"][1]

    combined = {
        "active_Lambda2_T8": {
            "domain_dim": 28,
            "image_rank": rank(active_rows),
            "kernel_dim": 28 - rank(active_rows),
        },
        "full_Lambda2_EndH1": {
            "domain_dim": 36,
            "image_rank": rank(full_rows),
            "kernel_dim": 36 - rank(full_rows),
        },
        "A_output_blocks_Lambda2_A3_plus_Lambda2_S5": {
            "domain_dim": 13,
            "image_rank": rank(a_output_rows),
            "kernel_dim": 13 - rank(a_output_rows),
        },
    }

    interpretation = {
        "central_kernel": "trace wedge T8 contributes an 8D central kernel.",
        "active_kernel": "Lambda^2 T8 has a 20D internal kernel and an 8D image.",
        "tensor_rules": "[A3,A3] and [S5,S5] land in A3; [A3,S5] lands in S5.",
        "orchestra_hint": "The active image preserves the 3+5 split, while the two-form domain contains larger inactive/cancelling sectors.",
        "not_claimed": "No particle assignments or mass values follow from this kernel/image split alone.",
    }

    print(f"block_report: {block_report}")
    print(f"combined: {combined}")
    print(f"interpretation: {interpretation}")


if __name__ == "__main__":
    main()
