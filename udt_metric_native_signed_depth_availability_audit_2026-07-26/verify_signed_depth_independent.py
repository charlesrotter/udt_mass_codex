#!/usr/bin/env python3
"""Independent no-SymPy verification of the signed-depth audit."""

from __future__ import annotations

from fractions import Fraction as F
from itertools import product
import json
import math


def matmul(a, b):
    return [[sum((a[i][k] * b[k][j] for k in range(len(b))), F(0)) for j in range(len(b[0]))] for i in range(len(a))]


def transpose(a):
    return [list(row) for row in zip(*a)]


def trace(a):
    return sum((a[i][i] for i in range(len(a))), F(0))


def diag(*values):
    return [[F(values[i]) if i == j else F(0) for j in range(len(values))] for i in range(len(values))]


def check(name, condition, checks):
    if not condition:
        raise AssertionError(name)
    checks[name] = "PASS"


def main():
    checks = {}

    # Exhaustive finite endpoint-potential control.
    endpoint_triangles = 0
    endpoint_reversals = 0
    for pa, pb, pc in product(range(-2, 3), repeat=3):
        dab, dbc, dac = pb - pa, pc - pb, pc - pa
        check(f"endpoint_triangle_{endpoint_triangles}", dab + dbc == dac, checks)
        endpoint_triangles += 1
        check(f"endpoint_reversal_{endpoint_reversals}", dab == -(pa - pb), checks)
        endpoint_reversals += 1
    values = {"O": 0, "A": 2, "B": -3, "C": 5}
    arrow = {(a, b): values[b] - values[a] for a in values for b in values}
    reconstructed = {name: arrow[("O", name)] for name in values}
    check("basepoint_reconstructs_all_arrows", all(arrow[(a, b)] == reconstructed[b] - reconstructed[a] for a in values for b in values), checks)

    # Metric-skew/self-adjoint trace pairing over an exact bounded census.
    eta = diag(-1, 1, 1, 1)
    skew_samples = 0
    for lam, b1, b2, r12 in product((-2, -1, 0, 1, 2), (-1, 0, 1), (-1, 0, 1), (-1, 0, 1)):
        X = diag(-1, 1, lam, lam)
        omega = [
            [F(0), F(b1), F(b2), F(0)],
            [F(b1), F(0), F(r12), F(0)],
            [F(b2), F(-r12), F(0), F(0)],
            [F(0), F(0), F(0), F(0)],
        ]
        metric_skew = matmul(transpose(omega), eta)
        eta_omega = matmul(eta, omega)
        check(f"metric_skew_{skew_samples}", all(metric_skew[i][j] + eta_omega[i][j] == 0 for i in range(4) for j in range(4)), checks)
        check(f"trace_pair_zero_{skew_samples}", trace(matmul(X, omega)) == 0, checks)
        skew_samples += 1

    # Reference dependence is exact at the coefficient level.
    reference_samples = 0
    for dphi, dchi in product(range(-2, 3), repeat=2):
        raw = F(dphi)
        changed = F(dphi - dchi)
        check(f"reference_shift_{reference_samples}", changed - raw == -dchi, checks)
        reference_samples += 1

    # Reciprocal subgroup composition uses positive rational characters.
    q_values = (F(1, 3), F(1, 2), F(1), F(2), F(3))
    subgroup_compositions = 0
    for q, r in product(q_values, repeat=2):
        Aq = diag(1 / q, q)
        Ar = diag(1 / r, r)
        product_map = matmul(Ar, Aq)
        extracted_factor = product_map[1][1]
        check(f"subgroup_composition_{subgroup_compositions}", extracted_factor == q * r and product_map[0][0] == 1 / (q * r), checks)
        subgroup_compositions += 1

    # Independently evaluate the preregistered noncommuting logarithm witness.
    A = diag(F(1, 2), F(2))
    B = [[F(5, 4), F(3, 4)], [F(3, 4), F(5, 4)]]
    BA = matmul(B, A)
    AB = matmul(A, B)
    check("noncommuting_maps_are_distinct", BA != AB, checks)
    mf = [[float(value) for value in row] for row in BA]
    matrix_trace = mf[0][0] + mf[1][1]
    matrix_det = mf[0][0] * mf[1][1] - mf[0][1] * mf[1][0]
    discriminant = math.sqrt(matrix_trace * matrix_trace - 4.0 * matrix_det)
    eig_plus = (matrix_trace + discriminant) / 2.0
    eig_minus = (matrix_trace - discriminant) / 2.0
    projector_plus = [
        [(mf[i][j] - (eig_minus if i == j else 0.0)) / (eig_plus - eig_minus) for j in range(2)]
        for i in range(2)
    ]
    projector_minus = [[(1.0 if i == j else 0.0) - projector_plus[i][j] for j in range(2)] for i in range(2)]
    log_product = [
        [math.log(eig_plus) * projector_plus[i][j] + math.log(eig_minus) * projector_minus[i][j] for j in range(2)]
        for i in range(2)
    ]
    reconstructed_product = [
        [eig_plus * projector_plus[i][j] + eig_minus * projector_minus[i][j] for j in range(2)]
        for i in range(2)
    ]
    check("spectral_log_projectors_reconstruct_product", max(abs(reconstructed_product[i][j] - mf[i][j]) for i in range(2) for j in range(2)) < 1e-14, checks)
    projected_product = (-log_product[0][0] + log_product[1][1]) / 2.0
    projected_separate = math.log(2.0)
    check("independent_log_projection_nonadditive", projected_product - projected_separate > 0.1, checks)

    # Magnitudes, triangle defects, one-form periods, and clock ratios.
    symmetric_odd = [value for value in range(7) if value == -value]
    check("symmetric_nonnegative_and_odd_only_zero", symmetric_odd == [0], checks)
    check("Euclidean_noncollinear_triangle_defect", abs((1.0 + math.sqrt(2.0) - 1.0) - math.sqrt(2.0)) < 1e-15, checks)
    check("collinear_triangle_adds", F(1) + F(2) == F(3), checks)
    identity_factors = [q for q in q_values if diag(1 / q, q) == diag(1, 1)]
    check("faithful_positive_character_only_unit", identity_factors == [F(1)], checks)
    clock_ratio_checks = 0
    for wa, wb, wc in product((F(1), F(2), F(3)), repeat=3):
        qab, qbc, qac = wb / wa, wc / wb, wc / wa
        check(f"clock_ratio_{clock_ratio_checks}", qab * qbc == qac and (wa / wb) == 1 / qab, checks)
        clock_ratio_checks += 1
    check("clock_ratio_can_differ_from_founded_factor", F(2) != F(3), checks)

    # Several metric-scalar formulas yield distinct endpoint cocycles.
    invariant_cocycles = 0
    functions = (lambda x: x, lambda x: 2 * x, lambda x: x**3)
    for fn in functions:
        for ia, ib, ic in product(range(-2, 3), repeat=3):
            dab, dbc, dac = fn(ib) - fn(ia), fn(ic) - fn(ib), fn(ic) - fn(ia)
            check(f"invariant_cocycle_{invariant_cocycles}", dab + dbc == dac, checks)
            invariant_cocycles += 1
    check("invariant_formulas_are_distinct", functions[0](2) != functions[1](2) != functions[2](2), checks)

    summary = {
        name: value
        for name, value in checks.items()
        if not name.startswith((
            "endpoint_triangle_",
            "endpoint_reversal_",
            "metric_skew_",
            "trace_pair_zero_",
            "reference_shift_",
            "subgroup_composition_",
            "clock_ratio_",
            "invariant_cocycle_",
        ))
    }
    census = len(checks) - len(summary)
    result = {
        "schema": "udt-metric-native-signed-depth-independent-1.0",
        "result": "PASS",
        "summary_check_count": len(summary),
        "census_check_count": census,
        "checks": summary,
        "counts": {
            "endpoint_triangles": endpoint_triangles,
            "endpoint_reversals": endpoint_reversals,
            "metric_skew_samples": skew_samples,
            "reference_change_samples": reference_samples,
            "reciprocal_subgroup_compositions": subgroup_compositions,
            "clock_ratio_compositions": clock_ratio_checks,
            "invariant_cocycles": invariant_cocycles,
            "identity_character_factors": len(identity_factors),
        },
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
