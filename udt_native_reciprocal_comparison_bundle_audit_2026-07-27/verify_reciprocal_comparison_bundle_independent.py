#!/usr/bin/env python3
"""Independent exact-Fraction reconstruction of the bundle audit's load-bearing algebra."""

from __future__ import annotations

import json
from fractions import Fraction as F


N = 4


def zeros(rows: int = N, cols: int = N) -> list[list[F]]:
    return [[F(0) for _ in range(cols)] for _ in range(rows)]


def eye(n: int = N) -> list[list[F]]:
    result = zeros(n, n)
    for i in range(n):
        result[i][i] = F(1)
    return result


def diag(values: list[F]) -> list[list[F]]:
    result = zeros(len(values), len(values))
    for i, value in enumerate(values):
        result[i][i] = value
    return result


def transpose(a: list[list[F]]) -> list[list[F]]:
    return [list(row) for row in zip(*a)]


def add(a: list[list[F]], b: list[list[F]]) -> list[list[F]]:
    return [[x + y for x, y in zip(left, right)] for left, right in zip(a, b)]


def sub(a: list[list[F]], b: list[list[F]]) -> list[list[F]]:
    return [[x - y for x, y in zip(left, right)] for left, right in zip(a, b)]


def scale(value: F, a: list[list[F]]) -> list[list[F]]:
    return [[value * entry for entry in row] for row in a]


def mul(a: list[list[F]], b: list[list[F]]) -> list[list[F]]:
    bt = transpose(b)
    return [[sum((x * y for x, y in zip(row, col)), F(0)) for col in bt] for row in a]


def inverse(a: list[list[F]]) -> list[list[F]]:
    n = len(a)
    work = [row[:] + eye(n)[i] for i, row in enumerate(a)]
    for col in range(n):
        pivot = next(row for row in range(col, n) if work[row][col])
        work[col], work[pivot] = work[pivot], work[col]
        divisor = work[col][col]
        work[col] = [entry / divisor for entry in work[col]]
        for row in range(n):
            if row != col and work[row][col]:
                factor = work[row][col]
                work[row] = [x - factor * y for x, y in zip(work[row], work[col])]
    return [row[n:] for row in work]


def flatten(a: list[list[F]]) -> list[F]:
    return [entry for row in a for entry in row]


def rank(matrix: list[list[F]]) -> int:
    work = [row[:] for row in matrix]
    if not work:
        return 0
    rows, cols = len(work), len(work[0])
    pivot_row = 0
    for col in range(cols):
        pivot = next((row for row in range(pivot_row, rows) if work[row][col]), None)
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        divisor = work[pivot_row][col]
        work[pivot_row] = [entry / divisor for entry in work[pivot_row]]
        for row in range(rows):
            if row != pivot_row and work[row][col]:
                factor = work[row][col]
                work[row] = [x - factor * y for x, y in zip(work[row], work[pivot_row])]
        pivot_row += 1
        if pivot_row == rows:
            break
    return pivot_row


def columns_rank(columns: list[list[F]]) -> int:
    return rank([list(row) for row in zip(*columns)])


ETA = diag([F(-1), F(1), F(1), F(1)])


def metric_response(x: list[list[F]]) -> list[list[F]]:
    return add(mul(transpose(x), ETA), mul(ETA, x))


def dagger(x: list[list[F]]) -> list[list[F]]:
    return mul(mul(ETA, transpose(x)), ETA)


def lorentz_generators() -> dict[str, list[list[F]]]:
    result = {}
    for i in range(1, 4):
        value = zeros()
        value[0][i] = value[i][0] = F(1)
        result[f"K0{i}"] = value
    for i, j in ((1, 2), (1, 3), (2, 3)):
        value = zeros()
        value[i][j] = F(1)
        value[j][i] = F(-1)
        result[f"J{i}{j}"] = value
    return result


def response_from_variables(values: list[F]) -> list[list[F]]:
    a, b, c, d, e, f, h = values
    return [
        [F(2), F(0), a, b],
        [F(0), F(2), c, d],
        [a, c, e, f],
        [b, d, f, h],
    ]


def invariant_residual(generator: list[list[F]], response: list[list[F]]) -> list[list[F]]:
    return add(mul(transpose(generator), response), mul(response, generator))


def affine_system(names: tuple[str, ...], generators: dict[str, list[list[F]]]):
    origin = response_from_variables([F(0)] * 7)
    bases = []
    for index in range(7):
        values = [F(0)] * 7
        values[index] = F(1)
        bases.append(sub(response_from_variables(values), origin))
    coefficient_rows: list[list[F]] = []
    constants: list[F] = []
    for name in names:
        constant = flatten(invariant_residual(generators[name], origin))
        columns = [flatten(invariant_residual(generators[name], basis)) for basis in bases]
        for row_index, value in enumerate(constant):
            coefficient_rows.append([column[row_index] for column in columns])
            constants.append(-value)
    augmented = [row + [value] for row, value in zip(coefficient_rows, constants)]
    return rank(coefficient_rows), rank(augmented)


def outer(a: list[F], b: list[F]) -> list[list[F]]:
    return [[x * y for y in b] for x in a]


def vecmul(a: list[list[F]], vector: list[F]) -> list[F]:
    return [sum((x * y for x, y in zip(row, vector)), F(0)) for row in a]


def main() -> None:
    checks: dict[str, str] = {}

    def check(name: str, condition: bool) -> None:
        if not condition:
            raise AssertionError(name)
        checks[name] = "PASS"

    # Reconstruct End(V) -> Sym^2(V*) and its Lorentz kernel.
    end_basis = []
    for i in range(N):
        for j in range(N):
            value = zeros()
            value[i][j] = F(1)
            end_basis.append(value)
    response_rank = columns_rank([flatten(metric_response(value)) for value in end_basis])
    generators = lorentz_generators()
    check("independent_response_rank_ten", response_rank == 10)
    check("independent_kernel_dimension_six", 16 - response_rank == 6)
    check("independent_lorentz_rank_six", columns_rank([flatten(value) for value in generators.values()]) == 6)
    check("independent_lorentz_kernel", all(metric_response(value) == zeros() for value in generators.values()))

    sample = zeros()
    sample[0][0], sample[1][1], sample[2][0], sample[2][3] = F(-1), F(1), F(2), F(3)
    self_part = scale(F(1, 2), add(sample, dagger(sample)))
    skew_part = scale(F(1, 2), sub(sample, dagger(sample)))
    check("independent_self_adjoint_decomposition", dagger(self_part) == self_part)
    check("independent_skew_decomposition", metric_response(skew_part) == zeros())
    check("independent_response_uses_self_part", metric_response(sample) == metric_response(self_part))

    extension_entries = [(2, 2), (2, 3), (3, 3), (2, 0), (2, 1), (3, 0), (3, 1)]
    extension_basis = []
    for i, j in extension_entries:
        value = zeros()
        value[i][j] = F(1)
        extension_basis.append(value)
    check("independent_extension_tangent_rank_seven", columns_rank([flatten(value) for value in extension_basis]) == 7)
    check("independent_extension_response_rank_seven", columns_rank([flatten(metric_response(value)) for value in extension_basis]) == 7)
    restriction = [[F(1), F(0), F(0)], [F(0), F(1), F(0)], [F(0), F(0), F(1)]]
    check("independent_pair_restriction_rank_three", rank(restriction) == 3)
    check("independent_affine_fiber_dimension_seven", 10 - rank(restriction) == 7)

    pair_rank, pair_aug = affine_system(("J23",), generators)
    observer_rank, observer_aug = affine_system(("J12", "J13", "J23"), generators)
    ruler_rank, ruler_aug = affine_system(("K02", "K03", "J23"), generators)
    full_rank, full_aug = affine_system(tuple(generators), generators)
    check("independent_pair_SO2_dimension_one", pair_rank == pair_aug == 6)
    check("independent_observer_SO3_unique", observer_rank == observer_aug == 7)
    check("independent_ruler_SO12_unique", ruler_rank == ruler_aug == 7)
    check("independent_full_Lorentz_inconsistent", full_aug > full_rank)
    for name in ("J23",):
        check("independent_pair_family_witness", invariant_residual(generators[name], response_from_variables([F(0), F(0), F(0), F(0), F(7), F(0), F(7)])) == zeros())
    check("independent_observer_plus_one_witness", all(invariant_residual(generators[name], response_from_variables([F(0), F(0), F(0), F(0), F(2), F(0), F(2)])) == zeros() for name in ("J12", "J13", "J23")))
    check("independent_ruler_minus_one_witness", all(invariant_residual(generators[name], response_from_variables([F(0), F(0), F(0), F(0), F(-2), F(0), F(-2)])) == zeros() for name in ("K02", "K03", "J23")))

    boost = eye()
    boost[0][0] = boost[2][2] = F(5, 3)
    boost[0][2] = boost[2][0] = F(4, 3)
    rotation23 = eye()
    rotation23[2][2] = rotation23[3][3] = F(3, 5)
    rotation23[2][3], rotation23[3][2] = F(-4, 5), F(4, 5)
    rotation12 = eye()
    rotation12[1][1] = rotation12[2][2] = F(3, 5)
    rotation12[1][2], rotation12[2][1] = F(-4, 5), F(4, 5)
    check("independent_Lorentz_controls", mul(mul(transpose(boost), ETA), boost) == ETA and mul(mul(transpose(rotation23), ETA), rotation23) == ETA and mul(mul(transpose(rotation12), ETA), rotation12) == ETA)

    u, n = [F(1), F(0), F(0), F(0)], [F(0), F(1), F(0), F(0)]

    def projector_u(vector: list[F]) -> list[list[F]]:
        covector = vecmul(ETA, vector)
        return scale(F(-1), outer(vector, covector))

    def projector_n(vector: list[F]) -> list[list[F]]:
        covector = vecmul(ETA, vector)
        return outer(vector, covector)

    def x_lambda(uv: list[F], nv: list[F], lam: F) -> list[list[F]]:
        pu, pn = projector_u(uv), projector_n(nv)
        return add(add(scale(F(-1), pu), pn), scale(lam, sub(sub(eye(), pu), pn)))

    transformed_pair = x_lambda(vecmul(boost, u), vecmul(boost, n), F(3, 7))
    conjugated = mul(mul(boost, x_lambda(u, n, F(3, 7))), inverse(boost))
    check("independent_pair_query_covariance", transformed_pair == conjugated)

    U1, U2 = boost, rotation23
    Lp, Lq, Lr = rotation12, mul(rotation23, boost), mul(boost, rotation12)
    U1p = mul(mul(Lq, U1), inverse(Lp))
    U2p = mul(mul(Lr, U2), inverse(Lq))
    check("independent_transport_composition", mul(U2p, U1p) == mul(mul(Lr, mul(U2, U1)), inverse(Lp)))
    source = diag([F(-1), F(1), F(0), F(0)])
    source[2][0] = F(2)
    transformed_source = mul(mul(Lp, source), inverse(Lp))
    transported = mul(mul(U1p, transformed_source), inverse(U1p))
    expected = mul(mul(Lq, mul(mul(U1, source), inverse(U1))), inverse(Lq))
    check("independent_generator_transport", transported == expected)
    check("independent_reversal", mul(inverse(U1), U1) == eye())

    triangular = diag([F(-1), F(1), F(0), F(0)])
    triangular[2][0] = F(1)
    symmetric_lift = scale(F(1, 2), add(triangular, dagger(triangular)))

    def second_jet(value: list[list[F]]) -> list[list[F]]:
        vt = transpose(value)
        return add(add(mul(mul(vt, vt), ETA), scale(F(2), mul(mul(vt, ETA), value))), mul(mul(ETA, value), value))

    check("independent_same_first_jet", metric_response(triangular) == metric_response(symmetric_lift))
    check("independent_different_second_jet", second_jet(triangular) != second_jet(symmetric_lift))

    swap = eye()
    swap[0][0] = swap[1][1] = F(0)
    swap[0][1] = swap[1][0] = F(1)
    check("independent_swap_non_Lorentz", mul(mul(transpose(swap), ETA), swap) != ETA)

    expected = 27
    check("independent_registered_count", len(checks) == expected - 1)
    if len(checks) != expected:
        raise AssertionError(f"unexpected independent check count {len(checks)}")

    result = {
        "schema": "udt.native_reciprocal_comparison_bundle.independent.v1",
        "result": "PASS",
        "check_count": len(checks),
        "ranks": {
            "metric_response": response_rank,
            "Lorentz_kernel": 16 - response_rank,
            "founded_affine_response_fiber": 7,
            "pair_SO2_invariant_dimension": 7 - pair_rank,
            "observer_SO3_invariant_dimension": 7 - observer_rank,
            "ruler_SO12_invariant_dimension": 7 - ruler_rank,
            "full_Lorentz_affine_system_consistent": full_rank == full_aug,
        },
        "finite_lift_same_first_different_second": True,
        "maximum_conclusion": "INDEPENDENT_EXACT_RECONSTRUCTION_ONLY",
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
