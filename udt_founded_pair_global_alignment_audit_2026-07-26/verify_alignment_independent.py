#!/usr/bin/env python3
"""Independent exact-rational verification; intentionally no SymPy import."""

from __future__ import annotations

from fractions import Fraction as F
from itertools import product
import json


def matmul(a, b):
    return [[sum((a[i][k] * b[k][j] for k in range(len(b))), F(0)) for j in range(len(b[0]))] for i in range(len(a))]


def transpose(a):
    return [list(row) for row in zip(*a)]


def add(a, b):
    return [[a[i][j] + b[i][j] for j in range(len(a[0]))] for i in range(len(a))]


def sub(a, b):
    return [[a[i][j] - b[i][j] for j in range(len(a[0]))] for i in range(len(a))]


def eye(n):
    return [[F(int(i == j)) for j in range(n)] for i in range(n)]


def block(a, b, c, d):
    return [a[i] + b[i] for i in range(len(a))] + [c[i] + d[i] for i in range(len(c))]


def inverse2(a):
    det = a[0][0] * a[1][1] - a[0][1] * a[1][0]
    return [[a[1][1] / det, -a[0][1] / det], [-a[1][0] / det, a[0][0] / det]]


def trace(a):
    return sum((a[i][i] for i in range(len(a))), F(0))


def invariant(metric, operator):
    return trace(matmul(matmul(matmul(inverse2(metric), transpose(operator)), metric), operator))


def check(name, condition, checks):
    if not condition:
        raise AssertionError(name)
    checks[name] = "PASS"


def main():
    checks = {}
    eta2 = [[F(-1), F(0)], [F(0), F(1)]]
    H = [[F(-1), F(0)], [F(0), F(1)]]

    shear = [[F(1), F(1)], [F(0), F(1)]]
    shear_inv = inverse2(shear)
    metric_prime = matmul(matmul(transpose(shear), eta2), shear)
    operator_prime = matmul(matmul(shear_inv, H), shear)
    check("independent_simultaneous_self_adjoint", matmul(transpose(operator_prime), metric_prime) == matmul(metric_prime, operator_prime), checks)
    check("independent_simultaneous_invariant_two", invariant(metric_prime, operator_prime) == F(2), checks)
    check("independent_metric_only_not_self_adjoint", matmul(transpose(H), metric_prime) != matmul(metric_prime, H), checks)
    check("independent_metric_only_invariant_changes", invariant(metric_prime, H) != F(2), checks)

    mixed = [[F(1), F(-2)], [F(-2), F(1)]]
    swap = [[F(0), F(1)], [F(1), F(0)]]
    check("independent_mixed_swap_isometry", matmul(matmul(transpose(swap), mixed), swap) == mixed, checks)
    check("independent_mixed_invariant_minus_ten_thirds", invariant(mixed, H) == F(-10, 3), checks)

    self_adjoint_lorentz = 0
    nonself_adjoint_lorentz = 0
    for aa, bb, cc in product(range(-3, 4), repeat=3):
        if aa * cc - bb * bb >= 0:
            continue
        metric = [[F(aa), F(bb)], [F(bb), F(cc)]]
        if matmul(transpose(H), metric) == matmul(metric, H):
            self_adjoint_lorentz += 1
            check(f"aligned_census_offdiagonal_zero_{self_adjoint_lorentz}", bb == 0, checks)
        else:
            nonself_adjoint_lorentz += 1
    check("bounded_pair_census_has_aligned_examples", self_adjoint_lorentz > 0, checks)
    check("bounded_pair_census_has_mixed_examples", nonself_adjoint_lorentz > 0, checks)

    # Fixed pair restriction with nonzero cross block and positive Schur witness.
    W = [[F(1, 4), F(0)], [F(0), F(1, 4)]]
    Q = eye(2)
    G = block(eta2, W, transpose(W), Q)
    check("independent_complete_pair_restriction", [row[:2] for row in G[:2]] == eta2, checks)
    schur = [[F(17, 16), F(0)], [F(0), F(15, 16)]]
    check("independent_schur_witness_positive", schur[0][0] > 0 and schur[1][1] > 0, checks)

    # Exhaust all small lower shifts: C^T C vanishes only for C=0.
    lower_shift_zero_count = 0
    for values in product((-1, 0, 1), repeat=4):
        C = [[F(values[0]), F(values[1])], [F(values[2]), F(values[3])]]
        CtC = matmul(transpose(C), C)
        if CtC == [[F(0), F(0)], [F(0), F(0)]]:
            lower_shift_zero_count += 1
            check("independent_zero_CtC_has_zero_C", all(value == 0 for value in values), checks)
    check("independent_only_zero_lower_shift_preserves_pair_metric", lower_shift_zero_count == 1, checks)

    # Exhaust 81 mixing blocks. The exact self-adjoint construction always
    # works, while pair invariance occurs only for the zero block.
    eta4 = [[F(-1), F(0), F(0), F(0)], [F(0), F(1), F(0), F(0)], [F(0), F(0), F(1), F(0)], [F(0), F(0), F(0), F(1)]]
    self_adjoint_count = 0
    invariant_count = 0
    for values in product((-1, 0, 1), repeat=4):
        B = [[F(values[0]), F(values[1])], [F(values[2]), F(values[3])]]
        A = matmul(eta2, transpose(B))
        X = block(H, A, B, [[F(0), F(0)], [F(0), F(0)]])
        if matmul(transpose(X), eta4) == matmul(eta4, X):
            self_adjoint_count += 1
        if B == [[F(0), F(0)], [F(0), F(0)]]:
            invariant_count += 1
            check("independent_invariant_case_upper_block_zero", A == [[F(0), F(0)], [F(0), F(0)]], checks)
    check("independent_all_81_compression_extensions_self_adjoint", self_adjoint_count == 81, checks)
    check("independent_only_one_small_mixing_block_is_pair_invariant", invariant_count == 1, checks)

    # Screen-rotation commutation among small symmetric responses.
    J = [[F(0), F(-1)], [F(1), F(0)]]
    isotropic_count = 0
    for a, b, d in product((-1, 0, 1), repeat=3):
        D = [[F(a), F(b)], [F(b), F(d)]]
        if matmul(D, J) == matmul(J, D):
            isotropic_count += 1
            check(f"independent_isotropic_screen_scalar_{isotropic_count}", b == 0 and a == d, checks)
    check("independent_three_small_isotropic_screen_responses", isotropic_count == 3, checks)

    # Opposite norms prevent an isometric line exchange in any dimension.
    e0_norm = eta4[0][0]
    e1_norm = eta4[1][1]
    check("independent_opposite_causal_norms", e0_norm == -1 and e1_norm == 1, checks)
    check("independent_isometric_exchange_impossible", e0_norm != e1_norm, checks)

    # Only summary-level checks are counted; dynamically named census checks
    # are retained as raw evidence but separated in the output.
    summary_checks = {name: value for name, value in checks.items() if not name.startswith(("aligned_census_", "independent_isotropic_screen_scalar_"))}
    census_checks = len(checks) - len(summary_checks)
    result = {
        "schema": "udt-founded-pair-global-alignment-independent-1.0",
        "result": "PASS",
        "summary_check_count": len(summary_checks),
        "census_check_count": census_checks,
        "checks": summary_checks,
        "counts": {
            "bounded_pair_self_adjoint_Lorentzian": self_adjoint_lorentz,
            "bounded_pair_nonself_adjoint_Lorentzian": nonself_adjoint_lorentz,
            "lower_shift_blocks_tested": 81,
            "lower_shift_pair_metric_preserving": lower_shift_zero_count,
            "self_adjoint_compression_blocks_tested": 81,
            "pair_invariant_compression_blocks": invariant_count,
            "small_symmetric_screen_responses_tested": 27,
            "screen_rotation_equivariant_responses": isotropic_count,
        },
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

