#!/usr/bin/env python3
"""Independent Fraction replay of the uncompressed complete-pair evaluator.

This script intentionally does not import SymPy or the production derivation.
"""

from __future__ import annotations

from fractions import Fraction as F
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
OUT = HERE / "INDEPENDENT_VERIFICATION.json"


def mat(rows):
    return [[F(x) for x in row] for row in rows]


def zeros(r, c):
    return [[F(0) for _ in range(c)] for _ in range(r)]


def add(a, b):
    return [[a[i][j] + b[i][j] for j in range(len(a[0]))] for i in range(len(a))]


def sub(a, b):
    return [[a[i][j] - b[i][j] for j in range(len(a[0]))] for i in range(len(a))]


def scale(c, a):
    return [[c * a[i][j] for j in range(len(a[0]))] for i in range(len(a))]


def transpose(a):
    return [list(row) for row in zip(*a)]


def mul(a, b):
    return [
        [sum((a[i][k] * b[k][j] for k in range(len(b))), F(0)) for j in range(len(b[0]))]
        for i in range(len(a))
    ]


def vstack(a, b):
    return [row[:] for row in a] + [row[:] for row in b]


def hstack(a, b):
    return [a[i][:] + b[i][:] for i in range(len(a))]


def det2(a):
    return a[0][0] * a[1][1] - a[0][1] * a[1][0]


def inv2(a):
    d = det2(a)
    return [[a[1][1] / d, -a[0][1] / d], [-a[1][0] / d, a[0][0] / d]]


def trace2(a):
    return a[0][0] + a[1][1]


ETA2 = mat([[-1, 0], [0, 1]])
ETA4 = mat([[-1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])
I2 = mat([[1, 0], [0, 1]])
Z2 = zeros(2, 2)


def full_E(B, Q, S):
    return vstack(hstack(B, Z2), hstack(mul(Q, S), Q))


def direct_h(B, Q, S, Y, Z):
    E = full_E(B, Q, S)
    J = vstack(Y, Z)
    return mul(mul(mul(mul(transpose(J), transpose(E)), ETA4), E), J)


def factored_h(B, Q, S, Y, Z):
    U = mul(B, Y)
    R = add(mul(S, Y), Z)
    A = mul(Q, R)
    return add(mul(mul(transpose(U), ETA2), U), mul(transpose(A), A))


def evaluate_line(base, direction, t):
    args = [add(base[i], scale(t, direction[i])) for i in range(5)]
    return factored_h(*args)


def central_difference(base, direction, step):
    hp = evaluate_line(base, direction, step)
    hm = evaluate_line(base, direction, -step)
    return scale(F(1, 2) / step, sub(hp, hm))


def analytic_dh(base, direction):
    B, Q, S, Y, Z = base
    dB, dQ, dS, dY, dZ = direction
    U = mul(B, Y)
    R = add(mul(S, Y), Z)
    A = mul(Q, R)
    dU = add(mul(dB, Y), mul(B, dY))
    dR = add(add(mul(dS, Y), mul(S, dY)), dZ)
    dA = add(mul(dQ, R), mul(Q, dR))
    return add(
        add(mul(mul(transpose(dU), ETA2), U), mul(mul(transpose(U), ETA2), dU)),
        add(mul(transpose(dA), A), mul(transpose(A), dA)),
    )


def max_abs(a):
    return max(abs(x) for row in a for x in row)


def dphi(h, dh):
    return trace2(mul(inv2(h), dh)) / 4 - dh[0][0] / (2 * h[0][0])


def terminal_reconstruction(h):
    T2 = -h[0][0]
    beta = h[0][1] / h[0][0]
    L2 = h[1][1] - h[0][1] * h[0][1] / h[0][0]
    return [[-T2, -T2 * beta], [-T2 * beta, -T2 * beta * beta + L2]], T2, L2


def sfrac(x):
    return f"{x.numerator}/{x.denominator}" if x.denominator != 1 else str(x.numerator)


def smat(a):
    return [[sfrac(x) for x in row] for row in a]


def main():
    B = mat([[2, F(1, 3)], [0, F(3, 2)]])
    Q = mat([[F(3, 2), F(1, 5)], [0, F(4, 3)]])
    S = mat([[F(1, 5), -F(1, 7)], [F(2, 9), F(1, 6)]])
    Y = mat([[1, F(1, 10)], [-F(1, 8), 1]])
    Z = mat([[F(1, 12), -F(1, 11)], [F(1, 13), F(1, 14)]])
    base = (B, Q, S, Y, Z)

    dB = mat([[F(1, 7), F(1, 9)], [-F(1, 11), F(1, 13)]])
    dQ = mat([[F(1, 5), -F(1, 8)], [F(1, 12), F(1, 6)]])
    dS = mat([[-F(1, 4), F(1, 10)], [F(1, 14), F(1, 9)]])
    dY = mat([[F(1, 15), -F(1, 7)], [F(1, 16), F(1, 11)]])
    dZ = mat([[F(1, 18), F(1, 13)], [-F(1, 17), F(1, 19)]])
    direction = (dB, dQ, dS, dY, dZ)

    h_direct = direct_h(*base)
    h_factored = factored_h(*base)
    dh = analytic_dh(base, direction)
    reconstruction, T2, L2 = terminal_reconstruction(h_factored)

    # The full line is polynomial of degree up to six.  Symmetric errors must decrease quadratically.
    steps = [F(1, 10), F(1, 100), F(1, 1000), F(1, 10000)]
    derivative_errors = []
    dphi_errors = []
    for step in steps:
        dh_fd = central_difference(base, direction, step)
        derivative_errors.append(max_abs(sub(dh_fd, dh)))
        hp = evaluate_line(base, direction, step)
        hm = evaluate_line(base, direction, -step)
        # Central difference of phi is evaluated numerically only at the final comparison.  The
        # rational invariant r=(-det h)/h00^2 is converted to float for the logarithm.
        import math

        phi_p = 0.25 * math.log(float(-det2(hp) / (hp[0][0] * hp[0][0])))
        phi_m = 0.25 * math.log(float(-det2(hm) / (hm[0][0] * hm[0][0])))
        fd_phi = (phi_p - phi_m) / (2 * float(step))
        dphi_errors.append(abs(fd_phi - float(dphi(h_factored, dh))))

    # Five black-box, one-channel finite differences.  They do not use the analytic sensitivities.
    E00 = mat([[1, 0], [0, 0]])
    one_channel = {}
    for idx, name in enumerate(("B", "Q", "S", "Y", "Z")):
        direction_i = [Z2, Z2, Z2, Z2, Z2]
        direction_i[idx] = E00
        step = F(1, 100000)
        hp = evaluate_line(base, direction_i, step)
        hm = evaluate_line(base, direction_i, -step)
        import math

        value = (
            0.25 * math.log(float(-det2(hp) / hp[0][0] ** 2))
            - 0.25 * math.log(float(-det2(hm) / hm[0][0] ** 2))
        ) / (2 * float(step))
        one_channel[name] = value

    # Independent compression checks.
    Yf = mat([[1, F(1, 4)], [0, 1]])
    Sf = mat([[F(1, 3), F(1, 5)], [F(1, 7), -F(1, 4)]])
    Zf = mat([[F(1, 6), -F(1, 8)], [F(1, 9), F(1, 10)]])
    Df = mat([[F(2, 5), F(1, 11)], [-F(1, 13), F(3, 7)]])
    Wf = mul(Zf, inv2(Yf))
    C1 = add(Sf, Wf)
    S2 = add(Sf, Df)
    Z2f = mul(sub(Wf, Df), Yf)
    C2 = add(S2, mul(Z2f, inv2(Yf)))

    O = mat([[0, -1], [1, 0]])
    Qf = mat([[F(3, 2), F(1, 5)], [0, F(4, 3)]])
    q1 = mul(transpose(Qf), Qf)
    q2 = mul(transpose(mul(O, Qf)), mul(O, Qf))

    checks = {
        "direct_equals_factored": h_direct == h_factored,
        "regular_terminal_witness": h_factored[0][0] < 0 and det2(h_factored) < 0,
        "terminal_reconstruction": reconstruction == h_factored,
        "ratio_squared_identity": T2 / L2 == h_factored[0][0] ** 2 / (-det2(h_factored)),
        "matrix_derivative_converges_quadratically": all(
            derivative_errors[i + 1] * 50 < derivative_errors[i]
            for i in range(len(derivative_errors) - 1)
        ),
        "phi_derivative_converges": all(
            dphi_errors[i + 1] < dphi_errors[i] for i in range(len(dphi_errors) - 1)
        ),
        "all_five_blackbox_sensitivities_nonzero": all(abs(v) > 1e-8 for v in one_channel.values()),
        "S_embedding_fiber": C1 == C2,
        "screen_frame_fiber": q1 == q2,
    }
    passed = all(checks.values())
    result = {
        "schema": "udt.uncompressed_pair_evaluator.independent.v1",
        "method": "standalone stdlib Fraction matrices plus shrinking-step black-box replay",
        "imports_production_code": False,
        "imports_sympy": False,
        "checks": checks,
        "passed": passed,
        "h": smat(h_factored),
        "matrix_derivative_error_by_step": {
            sfrac(step): sfrac(error) for step, error in zip(steps, derivative_errors)
        },
        "phi_derivative_error_by_step": {
            sfrac(step): value for step, value in zip(steps, dphi_errors)
        },
        "blackbox_dphi_sensitivities": one_channel,
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))
    if not passed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()

