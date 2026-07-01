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


def trace(a):
    return sum(a[i][i] for i in range(3))


def commutator(a, b):
    return mat_sub(mat_mul(a, b), mat_mul(b, a))


def omega(a, b, c):
    return trace(mat_mul(a, commutator(b, c)))


def basis_antisymmetric():
    return [mat_sub(mat_unit(i, j), mat_unit(j, i)) for i, j in combinations(range(3), 2)]


def basis_symmetric_traceless():
    offdiag = [mat_add(mat_unit(i, j), mat_unit(j, i)) for i, j in combinations(range(3), 2)]
    diag1 = mat_sub(mat_unit(0, 0), mat_unit(1, 1))
    diag2 = mat_sub(mat_unit(1, 1), mat_unit(2, 2))
    return offdiag + [diag1, diag2]


def count_nonzero_form_values(basis):
    values = [omega(basis[i], basis[j], basis[k]) for i, j, k in combinations(range(len(basis)), 3)]
    return {
        "domain_dim": len(values),
        "nonzero_values": sum(1 for value in values if value != 0),
        "rank_as_scalar_functional": 1 if any(value != 0 for value in values) else 0,
        "sample_nonzero_values": sorted({value for value in values if value != 0})[:10],
    }


def count_block_values(blocks):
    values = []
    for a in blocks[0]:
        for b in blocks[1]:
            for c in blocks[2]:
                values.append(omega(a, b, c))
    return {
        "domain_dim": len(values),
        "nonzero_values": sum(1 for value in values if value != 0),
        "rank_as_scalar_functional": 1 if any(value != 0 for value in values) else 0,
        "sample_nonzero_values": sorted({value for value in values if value != 0})[:10],
    }


def count_lambda2_left_wedge_one(left, right):
    values = [
        omega(left[i], left[j], c)
        for i, j in combinations(range(len(left)), 2)
        for c in right
    ]
    return {
        "domain_dim": len(values),
        "nonzero_values": sum(1 for value in values if value != 0),
        "rank_as_scalar_functional": 1 if any(value != 0 for value in values) else 0,
        "sample_nonzero_values": sorted({value for value in values if value != 0})[:10],
    }


def count_one_wedge_lambda2_right(left, right):
    values = [
        omega(a, right[i], right[j])
        for a in left
        for i, j in combinations(range(len(right)), 2)
    ]
    return {
        "domain_dim": len(values),
        "nonzero_values": sum(1 for value in values if value != 0),
        "rank_as_scalar_functional": 1 if any(value != 0 for value in values) else 0,
        "sample_nonzero_values": sorted({value for value in values if value != 0})[:10],
    }


def main():
    trace_basis = [mat_add(mat_add(mat_unit(0, 0), mat_unit(1, 1)), mat_unit(2, 2))]
    a3 = basis_antisymmetric()
    s5 = basis_symmetric_traceless()
    t8 = a3 + s5
    end_h1 = trace_basis + t8

    trace_wedge_t8_pairs = [
        omega(trace_basis[0], t8[i], t8[j])
        for i, j in combinations(range(len(t8)), 2)
    ]

    report = {
        "full_Lambda3_EndH1": count_nonzero_form_values(end_h1),
        "trace_wedge_Lambda2_T8": {
            "domain_dim": len(trace_wedge_t8_pairs),
            "all_zero": all(value == 0 for value in trace_wedge_t8_pairs),
        },
        "active_Lambda3_T8": count_nonzero_form_values(t8),
        "A3_only": count_nonzero_form_values(a3),
        "S5_only": count_nonzero_form_values(s5),
        "block_contributions": {
            "Lambda3_A3": count_nonzero_form_values(a3),
            "Lambda2_A3_wedge_S5": count_lambda2_left_wedge_one(a3, s5),
            "A3_wedge_Lambda2_S5": count_one_wedge_lambda2_right(a3, s5),
            "Lambda3_S5": count_nonzero_form_values(s5),
        },
        "mixed_domain_dimensions": {
            "Lambda3_EndH1": 84,
            "trace_wedge_Lambda2_T8": 28,
            "Lambda3_T8": 56,
            "Lambda3_A3": 1,
            "Lambda2_A3_wedge_S5": 15,
            "A3_wedge_Lambda2_S5": 30,
            "Lambda3_S5": 10,
        },
        "interpretation": {
            "native_threeform": "Tr(A[B,C]) is a canonical alternating 3-form built from the native commutator and trace pairing.",
            "full_84_domain": "Its natural full domain is Lambda^3 End(H1), dimension 84.",
            "trace_kernel": "Any trace argument kills the form, so trace wedge Lambda^2 T8 is a 28D kernel.",
            "active_domain": "The active three-form domain is Lambda^3 T8, dimension 56.",
            "not_closed": "This gives 84 a native functional domain, but the active nonzero form is not the full 84-dimensional space.",
        },
    }

    for key, value in report.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    main()
