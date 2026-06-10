from fractions import Fraction
from itertools import combinations


def unit_vector(k, n=9):
    return [Fraction(1 if i == k else 0) for i in range(n)]


def mat_zero():
    return [[Fraction(0) for _ in range(3)] for _ in range(3)]


def mat_unit(i, j):
    m = mat_zero()
    m[i][j] = Fraction(1)
    return m


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


def outer(u, v):
    return [[u[i] * v[j] for j in range(len(v))] for i in range(len(u))]


def mat_add(a, b):
    return [[a[i][j] + b[i][j] for j in range(len(a[0]))] for i in range(len(a))]


def mat_scale(c, a):
    return [[c * a[i][j] for j in range(len(a[0]))] for i in range(len(a))]


def identity(n):
    return [[Fraction(1 if i == j else 0) for j in range(n)] for i in range(n)]


def trace_matrix(a):
    return sum(a[i][i] for i in range(len(a)))


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


def main():
    end_basis = [mat_unit(i, j) for i in range(3) for j in range(3)]
    commutator_columns = [
        flatten(commutator(end_basis[a], end_basis[b]))
        for a, b in combinations(range(9), 2)
    ]

    bb_t = [[Fraction(0) for _ in range(9)] for _ in range(9)]
    for col in commutator_columns:
        bb_t = mat_add(bb_t, outer(col, col))

    identity_vector = flatten(
        [
            [Fraction(1 if i == j else 0) for j in range(3)]
            for i in range(3)
        ]
    )
    trace_projection = mat_scale(Fraction(1, 3), outer(identity_vector, identity_vector))
    traceless_projection = mat_add(identity(9), mat_scale(Fraction(-1), trace_projection))
    expected = mat_scale(Fraction(3), traceless_projection)

    domain_dim = len(commutator_columns)
    image_rank = rank(commutator_columns)
    c1_side_action = Fraction(1, domain_dim)

    checks = {
        "BBt_equals_3P_T8": bb_t == expected,
        "trace_BBt": trace_matrix(bb_t),
        "rank_image": image_rank,
        "domain_dim_Lambda2_EndH1": domain_dim,
        "kernel_dim": domain_dim - image_rank,
        "C1_side_action": c1_side_action,
        "total_uniform_domain_weight": domain_dim * c1_side_action,
        "image_singular_square": Fraction(3),
        "normalized_map_factor_squared": Fraction(1, 3),
    }

    interpretation = {
        "isotropy": "The commutator two-form is isotropic onto T8: B B^T = 3 P_T8.",
        "normalization": "Multiplying the commutator by 1/sqrt(3) gives a coisometry onto T8.",
        "C1_weight": "eta/2=1/36 is the uniform side-action weight per Lambda^2 End(H1) basis cell.",
        "remaining_gap": "This links C1 weighting to the commutator domain measure, but still does not prove a physical particle mass operator.",
    }

    print(f"checks: {checks}")
    print(f"interpretation: {interpretation}")


if __name__ == "__main__":
    main()
