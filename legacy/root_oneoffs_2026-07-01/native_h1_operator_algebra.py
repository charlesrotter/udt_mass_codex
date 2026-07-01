from fractions import Fraction


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


def mat_scale(c, a):
    return [[c * a[i][j] for j in range(3)] for i in range(3)]


def transpose(a):
    return [[a[j][i] for j in range(3)] for i in range(3)]


def trace(a):
    return sum(a[i][i] for i in range(3))


def identity():
    return [[Fraction(1 if i == j else 0) for j in range(3)] for i in range(3)]


def trace_part(a):
    return mat_scale(trace(a) / 3, identity())


def traceless_part(a):
    return mat_sub(a, trace_part(a))


def antisymmetric_part(a):
    return mat_scale(Fraction(1, 2), mat_sub(a, transpose(a)))


def symmetric_part(a):
    return mat_scale(Fraction(1, 2), mat_add(a, transpose(a)))


def symmetric_traceless_part(a):
    return traceless_part(symmetric_part(a))


def flatten(a):
    return [a[i][j] for i in range(3) for j in range(3)]


def rank(mats):
    rows = [flatten(m) for m in mats]
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


def is_zero(a):
    return all(x == 0 for x in flatten(a))


def commutator(a, b):
    return mat_sub(mat_mul(a, b), mat_mul(b, a))


def main():
    basis = [mat_unit(i, j) for i in range(3) for j in range(3)]

    trace_basis = [trace_part(m) for m in basis if not is_zero(trace_part(m))]
    traceless_basis = [traceless_part(m) for m in basis if not is_zero(traceless_part(m))]
    antisym_basis = [
        antisymmetric_part(m) for m in basis if not is_zero(antisymmetric_part(m))
    ]
    sym_tr_basis = [
        symmetric_traceless_part(m)
        for m in basis
        if not is_zero(symmetric_traceless_part(m))
    ]

    projector_checks = {
        "trace_plus_traceless_reconstructs": all(
            mat_add(trace_part(m), traceless_part(m)) == m for m in basis
        ),
        "antisym_plus_symtr_plus_trace_reconstructs": all(
            mat_add(
                trace_part(m),
                mat_add(antisymmetric_part(m), symmetric_traceless_part(m)),
            )
            == m
            for m in basis
        ),
        "trace_projector_idempotent": all(trace_part(trace_part(m)) == trace_part(m) for m in basis),
        "traceless_projector_idempotent": all(
            traceless_part(traceless_part(m)) == traceless_part(m) for m in basis
        ),
        "antisym_projector_idempotent": all(
            antisymmetric_part(antisymmetric_part(m)) == antisymmetric_part(m)
            for m in basis
        ),
        "symtr_projector_idempotent": all(
            symmetric_traceless_part(symmetric_traceless_part(m))
            == symmetric_traceless_part(m)
            for m in basis
        ),
    }

    commutators_traceless = [
        commutator(a, b) for a in traceless_basis for b in traceless_basis
    ]

    result = {
        "input_carrier": "H1 real rank N=3",
        "End(H1)_dimension": rank(basis),
        "trace_scalar_dimension": rank(trace_basis),
        "traceless_dimension": rank(traceless_basis),
        "antisymmetric_dimension": rank(antisym_basis),
        "symmetric_traceless_dimension": rank(sym_tr_basis),
        "dimension_identities": {
            "End(H1)": "3*3=9",
            "trace_split": "9=1+8",
            "SO3_tensor_split": "8=3+5",
        },
        "projector_checks": projector_checks,
        "traceless_commutator_closes": all(trace(m) == 0 for m in commutators_traceless),
        "interpretation": {
            "native": "End(H1) has exact scalar plus traceless split, with traceless part decomposing as antisymmetric 3 plus symmetric-traceless 5.",
            "not_derived_here": "No particle labels, gauge principle, compact SU(3), kappa orbit, or mass formula.",
        },
    }

    for key, value in result.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    main()
