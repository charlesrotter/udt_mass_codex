#!/usr/bin/env python3
"""Independent exact-rational founded-pair first-jet verification."""

from __future__ import annotations

from fractions import Fraction as Q
import json


IDS = [f"W{i:02d}" for i in range(1, 7)] + [f"U{i:02d}" for i in range(1, 9)] + [f"N{i:02d}" for i in range(1, 9)]
ETA = [[Q(-1), Q(0), Q(0), Q(0)], [Q(0), Q(1), Q(0), Q(0)], [Q(0), Q(0), Q(1), Q(0)], [Q(0), Q(0), Q(0), Q(1)]]


def check(name, condition, checks):
    if not condition:
        raise AssertionError(name)
    checks[name] = "PASS"


def zeros(rows, columns):
    return [[Q(0) for _ in range(columns)] for _ in range(rows)]


def transpose(a):
    return [list(row) for row in zip(*a)]


def matmul(a, b):
    return [[sum((a[i][k] * b[k][j] for k in range(len(b))), Q(0)) for j in range(len(b[0]))] for i in range(len(a))]


def matvec(a, v):
    return [sum((a[i][j] * v[j] for j in range(len(v))), Q(0)) for i in range(len(a))]


def matadd(a, b):
    return [[a[i][j] + b[i][j] for j in range(len(a[0]))] for i in range(len(a))]


def matscale(value, a):
    return [[value * entry for entry in row] for row in a]


def rank_fraction(matrix):
    data = [row[:] for row in matrix]
    if not data:
        return 0
    rows, columns = len(data), len(data[0])
    pivot_row = 0
    for column in range(columns):
        pivot = next((row for row in range(pivot_row, rows) if data[row][column]), None)
        if pivot is None:
            continue
        data[pivot_row], data[pivot] = data[pivot], data[pivot_row]
        scale = data[pivot_row][column]
        data[pivot_row] = [entry / scale for entry in data[pivot_row]]
        for row in range(rows):
            if row == pivot_row or not data[row][column]:
                continue
            factor = data[row][column]
            data[row] = [data[row][j] - factor * data[pivot_row][j] for j in range(columns)]
        pivot_row += 1
        if pivot_row == rows:
            break
    return pivot_row


def screen(v2, v3):
    return [Q(0), Q(0), v2, v3]


def star(v2, v3):
    return [Q(0), Q(0), -v3, v2]


def scaled(vector, scalar):
    return [entry * scalar for entry in vector]


def canonical_values(data, transformed=False):
    w = data[:4]
    U = [[data[4 + 2 * b + A] for A in range(2)] for b in range(4)]
    N = [[data[12 + 2 * b + A] for A in range(2)] for b in range(4)]
    uflat, nflat = [Q(-1), Q(0), Q(0), Q(0)], [Q(0), Q(1), Q(0), Q(0)]
    tu, zu = U[2][0] + U[3][1], U[2][1] - U[3][0]
    tn, zn = N[2][0] + N[3][1], N[2][1] - N[3][0]
    if not transformed:
        return [
            scaled(uflat, w[0]), scaled(nflat, w[0]), scaled(uflat, w[1]), scaled(nflat, w[1]), screen(w[2], w[3]), star(w[2], w[3]),
            screen(*U[0]), star(*U[0]), screen(*U[1]), star(*U[1]), scaled(uflat, tu), scaled(nflat, tu), scaled(uflat, zu), scaled(nflat, zu),
            screen(*N[0]), star(*N[0]), screen(*N[1]), star(*N[1]), scaled(uflat, tn), scaled(nflat, tn), scaled(uflat, zn), scaled(nflat, zn),
        ]
    minus_n = scaled(nflat, Q(-1))
    return [
        scaled(uflat, -w[0]), scaled(minus_n, -w[0]), scaled(uflat, w[1]), scaled(minus_n, w[1]), screen(-w[2], -w[3]), scaled(star(-w[2], -w[3]), Q(-1)),
        screen(*U[0]), scaled(star(*U[0]), Q(-1)), screen(-U[1][0], -U[1][1]), scaled(star(-U[1][0], -U[1][1]), Q(-1)),
        scaled(uflat, tu), scaled(minus_n, tu), scaled(uflat, -zu), scaled(minus_n, -zu),
        screen(-N[0][0], -N[0][1]), scaled(star(-N[0][0], -N[0][1]), Q(-1)), screen(*N[1]), scaled(star(*N[1]), Q(-1)),
        scaled(uflat, -tn), scaled(minus_n, -tn), scaled(uflat, zn), scaled(minus_n, zn),
    ]


def canonical_map(transformed=False):
    matrix = zeros(80, 22)
    for variable in range(20):
        data = [Q(0)] * 20
        data[variable] = Q(1)
        values = canonical_values(data, transformed)
        for candidate in range(22):
            for component in range(4):
                matrix[component * 20 + variable][candidate] = values[candidate][component]
    return matrix


class Dual:
    __slots__ = ("value", "gradient")

    def __init__(self, value=0, gradient=None):
        self.value = Q(value)
        self.gradient = tuple(Q(0) for _ in range(4)) if gradient is None else tuple(Q(item) for item in gradient)

    def __add__(self, other):
        other = dual(other)
        return Dual(self.value + other.value, [self.gradient[i] + other.gradient[i] for i in range(4)])

    __radd__ = __add__

    def __neg__(self):
        return Dual(-self.value, [-entry for entry in self.gradient])

    def __sub__(self, other):
        return self + (-dual(other))

    def __rsub__(self, other):
        return dual(other) - self

    def __mul__(self, other):
        other = dual(other)
        return Dual(self.value * other.value, [self.gradient[i] * other.value + self.value * other.gradient[i] for i in range(4)])

    __rmul__ = __mul__


def dual(value):
    return value if isinstance(value, Dual) else Dual(value)


def dsum(values):
    result = Dual(0)
    for value in values:
        result = result + value
    return result


def lower_dual(vector):
    return [dsum(ETA[a][b] * vector[b] for b in range(4)) for a in range(4)]


def epsilon4(a, b, c, d):
    values = [a, b, c, d]
    if len(set(values)) != 4:
        return 0
    inversions = sum(values[i] > values[j] for i in range(4) for j in range(i + 1, 4))
    return -1 if inversions % 2 else 1


def pair_candidates(u, n, du, dn):
    uf, nf = lower_dual(u), lower_dual(n)
    S = [[dual(int(a == b)) + uf[a] * u[b] - nf[a] * n[b] for b in range(4)] for a in range(4)]
    ecov = [[dsum(epsilon4(a, b, c, d) * u[c] * n[d] for c in range(4) for d in range(4)) for b in range(4)] for a in range(4)]
    emix = [[dsum(ecov[a][c] * ETA[c][b] for c in range(4)) for b in range(4)] for a in range(4)]
    Scontra = [[dsum(ETA[b][a] * S[a][c] for a in range(4)) for c in range(4)] for b in range(4)]
    econtra = [[dsum(ETA[b][a] * ETA[c][d] * ecov[a][d] for a in range(4) for d in range(4)) for c in range(4)] for b in range(4)]

    def project(v):
        return [dsum(S[a][b] * v[b] for b in range(4)) for a in range(4)]

    def hodge(v):
        return [dsum(emix[a][b] * v[b] for b in range(4)) for a in range(4)]

    def along(derivative, direction):
        return project([dsum(direction[b] * derivative[b][c] for b in range(4)) for c in range(4)])

    def scale(v, scalar):
        return [entry * scalar for entry in v]

    omega = [dsum(n[c] * du[b][c] for c in range(4)) for b in range(4)]
    wu, wn = dsum(u[b] * omega[b] for b in range(4)), dsum(n[b] * omega[b] for b in range(4))
    ws = project(omega)
    Uu, Un, Nu, Nn = along(du, u), along(du, n), along(dn, u), along(dn, n)
    tu = dsum(Scontra[b][c] * du[b][c] for b in range(4) for c in range(4))
    zu = dsum(econtra[b][c] * du[b][c] for b in range(4) for c in range(4))
    tn = dsum(Scontra[b][c] * dn[b][c] for b in range(4) for c in range(4))
    zn = dsum(econtra[b][c] * dn[b][c] for b in range(4) for c in range(4))
    return [
        scale(uf, wu), scale(nf, wu), scale(uf, wn), scale(nf, wn), ws, hodge(ws),
        Uu, hodge(Uu), Un, hodge(Un), scale(uf, tu), scale(nf, tu), scale(uf, zu), scale(nf, zu),
        Nu, hodge(Nu), Nn, hodge(Nn), scale(uf, tn), scale(nf, tn), scale(uf, zn), scale(nf, zn),
    ]


def generators():
    output = []
    for i in range(1, 4):
        m = zeros(4, 4)
        m[0][i] = m[i][0] = Q(1)
        output.append(m)
    for i, j in ((1, 2), (1, 3), (2, 3)):
        m = zeros(4, 4)
        m[i][j], m[j][i] = Q(1), Q(-1)
        output.append(m)
    return output


GEN = generators()


def deterministic_lie(seed, slot):
    coefficients = [((seed * 17 + slot * 23 + k * 11 + slot * k * 3) % 7) - 3 for k in range(6)]
    if not any(coefficients):
        coefficients[slot % 6] = 1
    result = zeros(4, 4)
    for coefficient, generator in zip(coefficients, GEN):
        result = matadd(result, matscale(Q(coefficient), generator))
    return result


def sample(seed):
    A = [deterministic_lie(seed, 10 + a) for a in range(4)]
    B = [[zeros(4, 4) for _ in range(4)] for _ in range(4)]
    slot = 30
    for a in range(4):
        for b in range(a, 4):
            B[a][b] = B[b][a] = deterministic_lie(seed, slot)
            slot += 1
    e0, e1 = [Q(1), Q(0), Q(0), Q(0)], [Q(0), Q(1), Q(0), Q(0)]
    first_u, first_n = [matvec(A[a], e0) for a in range(4)], [matvec(A[a], e1) for a in range(4)]
    second_u, second_n = [[None] * 4 for _ in range(4)], [[None] * 4 for _ in range(4)]
    for a in range(4):
        for b in range(4):
            second_matrix = matadd(B[a][b], matscale(Q(1, 2), matadd(matmul(A[a], A[b]), matmul(A[b], A[a]))))
            second_u[a][b], second_n[a][b] = matvec(second_matrix, e0), matvec(second_matrix, e1)
    u = [Dual(e0[c], [first_u[a][c] for a in range(4)]) for c in range(4)]
    n = [Dual(e1[c], [first_n[a][c] for a in range(4)]) for c in range(4)]
    du = [[Dual(matvec(ETA, first_u[b])[c], [matvec(ETA, second_u[a][b])[c] for a in range(4)]) for c in range(4)] for b in range(4)]
    dn = [[Dual(matvec(ETA, first_n[b])[c], [matvec(ETA, second_n[a][b])[c] for a in range(4)]) for c in range(4)] for b in range(4)]
    return A, first_u, first_n, second_u, second_n, pair_candidates(u, n, du, dn)


def dot(v, w):
    return sum((v[i] * ETA[i][i] * w[i] for i in range(4)), Q(0))


def validate_sample(A, fu, fn, su, sn):
    e0, e1 = [Q(1), Q(0), Q(0), Q(0)], [Q(0), Q(1), Q(0), Q(0)]
    total = 0
    for matrix in A:
        condition = matadd(matmul(transpose(matrix), ETA), matmul(ETA, matrix))
        if any(condition[i][j] for i in range(4) for j in range(4)):
            raise AssertionError("Lie generator")
    for a in range(4):
        if 2 * dot(e0, fu[a]) or 2 * dot(e1, fn[a]) or dot(fu[a], e1) + dot(e0, fn[a]):
            raise AssertionError("first pair jet")
        total += 3
        for b in range(a, 4):
            if 2 * dot(fu[a], fu[b]) + 2 * dot(e0, su[a][b]):
                raise AssertionError("second u norm")
            if 2 * dot(fn[a], fn[b]) + 2 * dot(e1, sn[a][b]):
                raise AssertionError("second n norm")
            if dot(su[a][b], e1) + dot(fu[a], fn[b]) + dot(fu[b], fn[a]) + dot(e0, sn[a][b]):
                raise AssertionError("second orthogonality")
            total += 3
    return total


def exterior_block(candidates):
    matrix = zeros(6, 22)
    for candidate in range(22):
        row = 0
        for a in range(4):
            for b in range(a + 1, 4):
                matrix[row][candidate] = candidates[candidate][b].gradient[a] - candidates[candidate][a].gradient[b]
                row += 1
    return matrix


def main():
    checks = {}
    base_map = canonical_map(False)
    flipped_map = canonical_map(True)
    check("independent_basis_rank_22", rank_fraction(base_map) == 22, checks)
    orientation_ids = {"W06", "U02", "U04", "U07", "U08", "N02", "N04", "N07", "N08"}
    o2 = [i for i, identity in enumerate(IDS) if identity not in orientation_ids]
    check("independent_O2_rank_13", rank_fraction([[row[i] for i in o2] for row in base_map]) == 13, checks)
    parity = {
        "W01": "ODD", "W02": "EVEN", "W03": "EVEN", "W04": "ODD", "W05": "ODD", "W06": "EVEN",
        "U01": "EVEN", "U02": "ODD", "U03": "ODD", "U04": "EVEN", "U05": "EVEN", "U06": "ODD", "U07": "ODD", "U08": "EVEN",
        "N01": "ODD", "N02": "EVEN", "N03": "EVEN", "N04": "ODD", "N05": "ODD", "N06": "EVEN", "N07": "EVEN", "N08": "ODD",
    }
    for column, identity in enumerate(IDS):
        sign = Q(1) if parity[identity] == "EVEN" else Q(-1)
        check(f"independent_parity_{identity}", all(flipped_map[row][column] == sign * base_map[row][column] for row in range(80)), checks)
    even = [i for i, identity in enumerate(IDS) if parity[identity] == "EVEN"]
    both = [i for i in o2 if parity[IDS[i]] == "EVEN"]
    check("independent_even_rank_11", rank_fraction([[row[i] for i in even] for row in base_map]) == 11, checks)
    check("independent_O2_even_rank_6", rank_fraction([[row[i] for i in both] for row in base_map]) == 6, checks)

    stacked = []
    constraint_checks = 0
    for seed in (71, 83, 97, 109, 127, 149):
        A, fu, fn, su, sn, candidates = sample(seed)
        constraint_checks += validate_sample(A, fu, fn, su, sn)
        stacked.extend(exterior_block(candidates))
    closure_rank = rank_fraction(stacked)
    check("independent_closure_rank_22", closure_rank == 22, checks)
    check("independent_closure_nullity_zero", 22 - closure_rank == 0, checks)
    check("independent_constraints_252", constraint_checks == 252, checks)

    summary = {
        "schema": "udt-founded-pair-first-jet-independent-1.0",
        "result": "PASS",
        "summary_check_count": len(checks),
        "checks": checks,
        "counts": {
            "basis_rank": rank_fraction(base_map),
            "O2_rank": rank_fraction([[row[i] for i in o2] for row in base_map]),
            "n_flip_even_rank": rank_fraction([[row[i] for i in even] for row in base_map]),
            "O2_n_flip_even_rank": rank_fraction([[row[i] for i in both] for row in base_map]),
            "parity_checks": 22,
            "closure_samples": 6,
            "closure_rows": len(stacked),
            "closure_rank": closure_rank,
            "Taylor_constraint_checks": constraint_checks,
        },
    }
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
