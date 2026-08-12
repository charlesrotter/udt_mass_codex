#!/usr/bin/env python3
"""Independent exact-Fraction replay of the pair-first matrix identities."""

from __future__ import annotations

from fractions import Fraction as F
import json
from pathlib import Path
import random


HERE = Path(__file__).resolve().parent


def tr(a):
    return [list(x) for x in zip(*a)]


def mm(a, b):
    bt = tr(b)
    return [[sum(x * y for x, y in zip(row, col)) for col in bt] for row in a]


def add(a, b):
    return [[x + y for x, y in zip(ra, rb)] for ra, rb in zip(a, b)]


def sub(a, b):
    return [[x - y for x, y in zip(ra, rb)] for ra, rb in zip(a, b)]


def block(a, b, c, d):
    return [ra + rb for ra, rb in zip(a, b)] + [rc + rd for rc, rd in zip(c, d)]


def eye(n):
    return [[F(int(i == j)) for j in range(n)] for i in range(n)]


def inv2(a):
    det = a[0][0] * a[1][1] - a[0][1] * a[1][0]
    if det == 0:
        raise ZeroDivisionError
    return [[a[1][1] / det, -a[0][1] / det],
            [-a[1][0] / det, a[0][0] / det]]


def eq(a, b):
    return a == b


def randmat(rng, n=2, m=2):
    return [[F(rng.randint(-3, 3), rng.randint(1, 4)) for _ in range(m)] for _ in range(n)]


def main():
    rng = random.Random(20260812)
    eta2 = [[F(-1), F(0)], [F(0), F(1)]]
    eta4 = [[F(-int(i == j and i == 0) + int(i == j and i != 0)) for j in range(4)] for i in range(4)]
    zero = [[F(0), F(0)], [F(0), F(0)]]
    O = [[F(3, 5), F(-4, 5)], [F(4, 5), F(3, 5)]]

    counts = {
        "direct_pullback": 0,
        "reduced_gram": 0,
        "coordinate_covariance": 0,
        "screen_covariance": 0,
        "terminal_reconstruction": 0,
    }
    samples = 160
    for _ in range(samples):
        T = F(rng.randint(1, 5), rng.randint(1, 4))
        L = F(rng.randint(1, 5), rng.randint(1, 4))
        beta = F(rng.randint(-3, 3), rng.randint(1, 4))
        B = [[T, T * beta], [F(0), L]]
        qa = F(rng.randint(1, 5), rng.randint(1, 4))
        qc = F(rng.randint(1, 5), rng.randint(1, 4))
        qb = F(rng.randint(-3, 3), rng.randint(1, 4))
        Q = [[qa, F(0)], [qb, qc]]
        S = randmat(rng)
        while True:
            Y = randmat(rng)
            try:
                Yinv = inv2(Y)
                break
            except ZeroDivisionError:
                pass
        Z = randmat(rng)
        while True:
            R = randmat(rng)
            try:
                inv2(R)
                break
            except ZeroDivisionError:
                pass

        E = block(B, zero, mm(Q, S), Q)
        J = [*Y, *Z]
        g = mm(mm(tr(E), eta4), E)
        h_direct = mm(mm(tr(J), g), J)
        q = mm(tr(Q), Q)
        SYZ = add(mm(S, Y), Z)
        h_formula = add(mm(mm(mm(tr(Y), tr(B)), eta2), mm(B, Y)), mm(mm(tr(SYZ), q), SYZ))
        assert eq(h_direct, h_formula)
        counts["direct_pullback"] += 1

        C = add(S, mm(Z, Yinv))
        reduced_direct = mm(mm(tr(Yinv), h_direct), Yinv)
        reduced_formula = add(mm(mm(tr(B), eta2), B), mm(mm(tr(C), q), C))
        assert eq(reduced_direct, reduced_formula)
        counts["reduced_gram"] += 1

        JR = mm(J, R)
        hR = mm(mm(tr(JR), g), JR)
        assert eq(hR, mm(mm(tr(R), h_direct), R))
        counts["coordinate_covariance"] += 1

        OQ = mm(O, Q)
        assert eq(mm(tr(OQ), OQ), q)
        counts["screen_covariance"] += 1

        # Independently reconstruct any regular 2x2 Lorentzian h met in the sample.
        h00, h01, h11 = h_direct[0][0], h_direct[0][1], h_direct[1][1]
        det = h00 * h11 - h01 * h01
        if h00 < 0 and det < 0:
            T2 = -h00
            beta_out = h01 / h00
            L2 = h11 - h01 * h01 / h00
            recon = [[-T2, -T2 * beta_out],
                     [-T2 * beta_out, -T2 * beta_out * beta_out + L2]]
            assert eq(recon, h_direct)
            counts["terminal_reconstruction"] += 1

    # Flat F_k family: exact for several independent offsets.
    flat_rows = 0
    for k in [F(-5, 4), F(-1, 3), F(0), F(2, 5), F(7, 3)]:
        ell = F(5, 2)
        Jk = [[F(1), k / ell], [F(0), F(1)]]
        hk = mm(mm(tr(Jk), eta2), Jk)
        det = hk[0][0] * hk[1][1] - hk[0][1] * hk[1][0]
        assert det == -1 and (-det) / (hk[0][0] ** 2) == 1
        flat_rows += 1

    # One exact tangent/normal witness in Minkowski space. The timelike pair plane is
    # span(e0,e1); its orthogonal complement span(e2,e3) is positive definite.
    Jpair = [[F(1), F(0)], [F(0), F(1)], [F(0), F(0)], [F(0), F(0)]]
    H = [[F(0), F(0)], [F(0), F(0)], [F(1), F(0)], [F(0), F(1)]]
    orth = mm(mm(tr(Jpair), eta4), H)
    normal_metric = mm(mm(tr(H), eta4), H)
    assert orth == [[F(0), F(0)], [F(0), F(0)]]
    assert normal_metric == eye(2)

    production = json.loads((HERE / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    assert production["status"] == "PASS"
    assert all(production["checks"].values())

    result = {
        "schema": "udt-pair-first-independent-v1",
        "status": "PASS",
        "seed": 20260812,
        "exact_fraction_samples": samples,
        "checks": counts,
        "flat_counterfamily_rows": flat_rows,
        "orthogonal_screen_witness": "PASS",
        "production_checks_reopened": len(production["checks"]),
    }
    (HERE / "INDEPENDENT_VERIFICATION.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
