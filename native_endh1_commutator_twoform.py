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


def transpose(a):
    return [[a[j][i] for j in range(3)] for i in range(3)]


def trace(a):
    return sum(a[i][i] for i in range(3))


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


def main():
    end_basis = [mat_unit(i, j) for i in range(3) for j in range(3)]
    trace_identity = [mat_add(mat_add(mat_unit(0, 0), mat_unit(1, 1)), mat_unit(2, 2))]
    a3 = basis_antisymmetric()
    s5 = basis_symmetric_traceless()
    t8 = a3 + s5

    comm_end = [commutator(a, b) for a, b in combinations(end_basis, 2)]
    comm_t8 = [commutator(a, b) for a, b in combinations(t8, 2)]
    comm_a3_a3 = [commutator(a, b) for a, b in combinations(a3, 2)]
    comm_a3_s5 = [commutator(a, b) for a in a3 for b in s5]
    comm_s5_s5 = [commutator(a, b) for a, b in combinations(s5, 2)]
    comm_trace_t8 = [commutator(trace_identity[0], b) for b in t8]

    result = {
        "domain_dimensions": {
            "Lambda^2 End(H1)": 36,
            "trace_wedge_T8": 8,
            "Lambda^2 T8": 28,
            "Lambda^2 A3": 3,
            "A3_wedge_S5": 15,
            "Lambda^2 S5": 10,
        },
        "image_ranks": {
            "[End,End]": rank([flatten(m) for m in comm_end]),
            "[T8,T8]": rank([flatten(m) for m in comm_t8]),
            "[A3,A3]": rank([flatten(m) for m in comm_a3_a3]),
            "[A3,S5]": rank([flatten(m) for m in comm_a3_s5]),
            "[S5,S5]": rank([flatten(m) for m in comm_s5_s5]),
            "[trace,T8]": rank([flatten(m) for m in comm_trace_t8]),
        },
        "trace_of_all_commutators_zero": all(trace(m) == 0 for m in comm_end),
        "kernel_dimensions": {
            "Lambda^2 End_to_T8": 36 - rank([flatten(m) for m in comm_end]),
            "Lambda^2 T8_to_T8": 28 - rank([flatten(m) for m in comm_t8]),
        },
        "interpretation": {
            "functional_twoform": "The commutator is a native alternating map Lambda^2 End(H1) -> T8.",
            "trace_role": "Trace-wedge-traceless pairs are central under the commutator and lie in the kernel.",
            "active_twoform": "The active bracket domain is Lambda^2 T8, dimension 28, with image T8 dimension 8.",
            "not_gauge_import": "This is operator algebra on the native H1 carrier, not a local gauge principle or particle label.",
        },
    }

    for key, value in result.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    main()
