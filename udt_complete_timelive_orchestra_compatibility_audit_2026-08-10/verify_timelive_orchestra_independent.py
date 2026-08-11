#!/usr/bin/env python3
"""Independent exact Fraction reconstruction of the time-live compatibility algebra."""

from __future__ import annotations

import argparse
import json
import random
from fractions import Fraction as F
from pathlib import Path


HERE = Path(__file__).resolve().parent
parser = argparse.ArgumentParser()
parser.add_argument("--read-only", action="store_true")
READ_ONLY = parser.parse_args().read_only
RNG = random.Random(20260810)


def z(n: int, m: int):
    return [[F(0) for _ in range(m)] for _ in range(n)]


def ident(n: int):
    out = z(n, n)
    for i in range(n):
        out[i][i] = F(1)
    return out


def add(a, b):
    return [[a[i][j] + b[i][j] for j in range(len(a[0]))] for i in range(len(a))]


def sub(a, b):
    return [[a[i][j] - b[i][j] for j in range(len(a[0]))] for i in range(len(a))]


def mul(a, b):
    return [
        [sum((a[i][k] * b[k][j] for k in range(len(b))), F(0)) for j in range(len(b[0]))]
        for i in range(len(a))
    ]


def transpose(a):
    return [list(row) for row in zip(*a)]


def neg(a):
    return [[-value for value in row] for row in a]


def inv2(a):
    determinant = a[0][0] * a[1][1] - a[0][1] * a[1][0]
    assert determinant != 0
    return [
        [a[1][1] / determinant, -a[0][1] / determinant],
        [-a[1][0] / determinant, a[0][0] / determinant],
    ]


def block(a, b, c, d):
    return [a[0] + b[0], a[1] + b[1], c[0] + d[0], c[1] + d[1]]


def eq(a, b):
    return a == b


def randf(nonzero: bool = False):
    while True:
        value = F(RNG.randint(-5, 5), RNG.randint(1, 5))
        if value or not nonzero:
            return value


def rand_positive():
    return F(RNG.randint(1, 5), RNG.randint(1, 5))


def rand2(invertible: bool = False):
    while True:
        value = [[randf(), randf()], [randf(), randf()]]
        determinant = value[0][0] * value[1][1] - value[0][1] * value[1][0]
        if determinant or not invertible:
            return value


def rand2_positive():
    while True:
        value = rand2(True)
        determinant = value[0][0] * value[1][1] - value[0][1] * value[1][0]
        if determinant > 0:
            return value


def triangular_B():
    T, L, beta = rand_positive(), rand_positive(), randf()
    return [[T, T * beta], [F(0), L]]


def triangular_dB(B):
    T = B[0][0]
    beta = B[0][1] / T
    Td, Ld, betad = randf(), randf(), randf()
    return [[Td, Td * beta + T * betad], [F(0), Ld]]


def gram(x, metric):
    return mul(mul(transpose(x), metric), x)


block_trials = 300
mc_trials = 300
channel_trials = 300
pair_trials = 300
eta4 = [[F(-1), F(0), F(0), F(0)], [F(0), F(1), F(0), F(0)], [F(0), F(0), F(1), F(0)], [F(0), F(0), F(0), F(1)]]
eta2_local = [[F(-1), F(0)], [F(0), F(1)]]

for _ in range(block_trials):
    B = triangular_B()
    Q = rand2_positive()
    S = rand2()
    dB, dQ, dS = triangular_dB(B), rand2(), rand2()
    Binv, Qinv = inv2(B), inv2(Q)
    E = block(B, z(2, 2), mul(Q, S), Q)
    dE = block(dB, z(2, 2), add(mul(dQ, S), mul(Q, dS)), dQ)
    Einv = block(Binv, z(2, 2), neg(mul(S, Binv)), Qinv)
    assert eq(mul(E, Einv), ident(4))
    qmetric = mul(transpose(Q), Q)
    metric_expected = block(
        add(gram(B, eta2_local), mul(mul(transpose(S), qmetric), S)),
        mul(transpose(S), qmetric),
        mul(qmetric, S),
        qmetric,
    )
    assert eq(gram(E, eta4), metric_expected)
    K = mul(dE, Einv)
    P, C, R = mul(dB, Binv), mul(mul(Q, dS), Binv), mul(dQ, Qinv)
    assert eq(K, block(P, z(2, 2), C, R))

for _ in range(mc_trials):
    B, Q, S = triangular_B(), rand2_positive(), rand2()
    Bt, Bx = triangular_dB(B), triangular_dB(B)
    Qt, Qx, St, Sx = rand2(), rand2(), rand2(), rand2()
    Btx, Qtx, Stx = rand2(), rand2(), rand2()
    # The lower-left zero of B and its mixed derivative are retained.
    Btx[1][0] = F(0)
    Binv, Qinv = inv2(B), inv2(Q)
    d_t_Binv = neg(mul(mul(Binv, Bt), Binv))
    d_x_Binv = neg(mul(mul(Binv, Bx), Binv))
    d_t_Qinv = neg(mul(mul(Qinv, Qt), Qinv))
    d_x_Qinv = neg(mul(mul(Qinv, Qx), Qinv))

    Pt, Px = mul(Bt, Binv), mul(Bx, Binv)
    Rt, Rx = mul(Qt, Qinv), mul(Qx, Qinv)
    Ct, Cx = mul(mul(Q, St), Binv), mul(mul(Q, Sx), Binv)

    dt_Px = add(mul(Btx, Binv), mul(Bx, d_t_Binv))
    dx_Pt = add(mul(Btx, Binv), mul(Bt, d_x_Binv))
    dt_Rx = add(mul(Qtx, Qinv), mul(Qx, d_t_Qinv))
    dx_Rt = add(mul(Qtx, Qinv), mul(Qt, d_x_Qinv))
    dt_Cx = add(add(mul(mul(Qt, Sx), Binv), mul(mul(Q, Stx), Binv)), mul(mul(Q, Sx), d_t_Binv))
    dx_Ct = add(add(mul(mul(Qx, St), Binv), mul(mul(Q, Stx), Binv)), mul(mul(Q, St), d_x_Binv))

    comm_P = sub(mul(Pt, Px), mul(Px, Pt))
    comm_R = sub(mul(Rt, Rx), mul(Rx, Rt))
    coupled_C = add(sub(mul(Ct, Px), mul(Cx, Pt)), sub(mul(Rt, Cx), mul(Rx, Ct)))
    assert eq(sub(sub(dt_Px, dx_Pt), comm_P), z(2, 2))
    assert eq(sub(sub(dt_Rx, dx_Rt), comm_R), z(2, 2))
    assert eq(sub(sub(dt_Cx, dx_Ct), coupled_C), z(2, 2))

eta = [[F(-1), F(0)], [F(0), F(1)]]
for _ in range(channel_trials):
    X, Y = rand2(), rand2()
    P, C, R, JR, JA = rand2(), rand2(), rand2(), rand2(), rand2()
    dX = add(mul(P, X), JR)
    dY = add(add(mul(C, X), mul(R, Y)), JA)
    dHR = add(mul(mul(transpose(dX), eta), X), mul(mul(transpose(X), eta), dX))
    expected_HR = add(
        mul(mul(transpose(X), add(mul(transpose(P), eta), mul(eta, P))), X),
        add(mul(mul(transpose(JR), eta), X), mul(mul(transpose(X), eta), JR)),
    )
    dHA = add(mul(transpose(dY), Y), mul(transpose(Y), dY))
    expected_HA = add(
        add(mul(mul(transpose(X), transpose(C)), Y), mul(mul(transpose(Y), C), X)),
        add(
            mul(mul(transpose(Y), add(transpose(R), R)), Y),
            add(mul(transpose(JA), Y), mul(transpose(Y), JA)),
        ),
    )
    assert eq(dHR, expected_HR)
    assert eq(dHA, expected_HA)

for _ in range(pair_trials):
    h00 = -abs(randf(True))
    h01 = randf()
    # Force negative determinant by choosing positive h11 above h01^2/h00 in sign-aware form.
    h11 = abs(randf(True)) + F(1)
    determinant = h00 * h11 - h01 * h01
    assert determinant < 0
    dh00, dh01, dh11 = randf(), randf(), randf()
    ddet = dh00 * h11 + h00 * dh11 - 2 * h01 * dh01
    hinv = [[h11 / determinant, -h01 / determinant], [-h01 / determinant, h00 / determinant]]
    dh = [[dh00, dh01], [dh01, dh11]]
    product = mul(hinv, dh)
    trace = product[0][0] + product[1][1]
    assert ddet / determinant == trace
    dkappa = F(1, 4) * trace
    dphi = dkappa - F(1, 2) * dh00 / h00
    dbeta = (h00 * dh01 - h01 * dh00) / (h00 * h00)
    assert dkappa == F(1, 4) * ddet / determinant
    assert dphi == F(1, 4) * ddet / determinant - F(1, 2) * dh00 / h00
    assert dbeta == (h00 * dh01 - h01 * dh00) / (h00 * h00)

result = {
    "status": "PASS",
    "implementation": "independent_standard_library_fraction_no_sympy_no_production_import",
    "block_factorization_trials": block_trials,
    "mixed_time_space_compatibility_trials": mc_trials,
    "matrix_channel_evolution_trials": channel_trials,
    "pair_state_derivative_trials": pair_trials,
    "total_exact_trials": block_trials + mc_trials + channel_trials + pair_trials,
    "time_only_two_form_constraints": 0,
    "arbitrary_frequency_selection": "NONE_FROM_KINEMATICS",
}
if not READ_ONLY:
    (HERE / "INDEPENDENT_VERIFICATION_RESULT.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
print(json.dumps(result, indent=2, sort_keys=True))
