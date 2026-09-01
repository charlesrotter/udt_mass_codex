#!/usr/bin/env python3
"""Implementation-distinct tensor replay for G318; imports no production code."""

from fractions import Fraction as F
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
CHECKS = []


def check(label, condition):
    if not condition:
        raise AssertionError(label)
    CHECKS.append(label)


def delta(i, j):
    return 1 if i == j else 0


def permutation_sign(i, j, k):
    if len({i, j, k}) < 3:
        return 0
    return 1 if (i, j, k) in ((0, 1, 2), (1, 2, 0), (2, 0, 1)) else -1


def connection_and_xderivative(psi, psi_prime, psi_second):
    h = psi_prime / psi
    h_prime = psi_second / psi - h ** 2
    u = (2 * h, F(0), F(0))
    ux = (2 * h_prime, F(0), F(0))
    gamma = [[[F(0) for _ in range(3)] for _ in range(3)] for _ in range(3)]
    dgamma = [[[F(0) for _ in range(3)] for _ in range(3)] for _ in range(3)]
    for upper in range(3):
        for left in range(3):
            for right in range(3):
                gamma[upper][left][right] = (
                    delta(upper, left) * u[right]
                    + delta(upper, right) * u[left]
                    - delta(left, right) * u[upper]
                )
                dgamma[upper][left][right] = (
                    delta(upper, left) * ux[right]
                    + delta(upper, right) * ux[left]
                    - delta(left, right) * ux[upper]
                )
    return gamma, dgamma


def ricci_mixed_from_connection(psi, psi_prime, psi_second):
    gamma, dgamma = connection_and_xderivative(psi, psi_prime, psi_second)
    ricci_cov = [[F(0) for _ in range(3)] for _ in range(3)]
    for i in range(3):
        for j in range(3):
            value = dgamma[0][i][j]
            if j == 0:
                value -= sum(dgamma[k][i][k] for k in range(3))
            for k in range(3):
                for ell in range(3):
                    value += gamma[k][i][j] * gamma[ell][k][ell]
                    value -= gamma[ell][i][k] * gamma[k][j][ell]
            ricci_cov[i][j] = value
    inverse_factor = psi ** -4
    return tuple(ricci_cov[i][i] * inverse_factor for i in range(3)), ricci_cov


def direct_momentum_from_connection(psi, psi_prime, kdiag, kdiag_prime, tau, tau_prime):
    gamma, _ = connection_and_xderivative(psi, psi_prime, F(0))
    pmat = [[F(0) for _ in range(3)] for _ in range(3)]
    pprime = [[F(0) for _ in range(3)] for _ in range(3)]
    for i in range(3):
        pmat[i][i] = kdiag[i] - tau
        pprime[i][i] = kdiag_prime[i] - tau_prime
    result = []
    for i in range(3):
        value = pprime[0][i]
        for j in range(3):
            for m in range(3):
                value += gamma[j][j][m] * pmat[m][i]
                value -= gamma[m][j][i] * pmat[j][m]
        result.append(value)
    return tuple(result)


def magnetic_from_connection(psi, psi_prime, psi_second, kdiag, kdiag_prime):
    gamma, _ = connection_and_xderivative(psi, psi_prime, psi_second)
    gfactor = psi ** 4
    h = psi_prime / psi
    kcov = [[F(0) for _ in range(3)] for _ in range(3)]
    kcov_prime = [[F(0) for _ in range(3)] for _ in range(3)]
    for i in range(3):
        kcov[i][i] = gfactor * kdiag[i]
        kcov_prime[i][i] = gfactor * (kdiag_prime[i] + 4 * h * kdiag[i])

    def covariant_derivative(k, ell, j):
        value = kcov_prime[ell][j] if k == 0 else F(0)
        for m in range(3):
            value -= gamma[m][k][ell] * kcov[m][j]
            value -= gamma[m][k][j] * kcov[ell][m]
        return value

    bcov = [[F(0) for _ in range(3)] for _ in range(3)]
    epsilon_factor = psi ** -2
    for i in range(3):
        for j in range(3):
            value = F(0)
            for k in range(3):
                for ell in range(3):
                    value += epsilon_factor * permutation_sign(i, k, ell) * covariant_derivative(k, ell, j)
            bcov[i][j] = value
    orthonormal_factor = psi ** -4
    return tuple(tuple(bcov[i][j] * orthonormal_factor for j in range(3)) for i in range(3))


def ratios(n):
    if n == -6:
        raise ValueError("singular ratio chart")
    return F(n + 2, n + 6), F(2, n + 6)


def ode_second_nminus2(psi, c_value, d_value, lam):
    return c_value ** 2 * psi / 16 - d_value ** 2 * psi ** -7 / 4 - lam * psi ** 5 / 4


def first_integral(psi, psi_prime, c_value, d_value, lam):
    return -4 * psi_prime ** 2 + c_value ** 2 * psi ** 2 / 4 + d_value ** 2 * psi ** -6 / 3 - lam * psi ** 6 / 3


# Reconstruct spatial curvature from connection rather than importing the closed formula.
for psi in (F(1, 2), F(3, 4), F(1), F(7, 4), F(2)):
    for psi_prime in (F(-5, 7), F(0), F(3, 8)):
        for psi_second in (F(-11, 9), F(2, 5), F(13, 6)):
            ricci, cov = ricci_mixed_from_connection(psi, psi_prime, psi_second)
            expected = (
                -4 * psi ** -5 * psi_second + 4 * psi ** -6 * psi_prime ** 2,
                -2 * psi ** -5 * psi_second - 2 * psi ** -6 * psi_prime ** 2,
                -2 * psi ** -5 * psi_second - 2 * psi ** -6 * psi_prime ** 2,
            )
            check(f"connection Ricci psi={psi} psip={psi_prime} psipp={psi_second}", ricci == expected)
            check(f"Ricci offdiagonal psi={psi} psip={psi_prime} psipp={psi_second}", all(cov[i][j] == 0 for i in range(3) for j in range(3) if i != j))
            check(f"Ricci scalar psi={psi} psip={psi_prime} psipp={psi_second}", sum(ricci) == -8 * psi ** -5 * psi_second)


# Direct physical constraints across independently assembled power branches.
for n in (-9, -8, -7, -5, -4, -3, -2, -1, 1, 3, 5):
    a_value, b_value = ratios(n)
    for psi in (F(2, 3), F(1), F(5, 3)):
        for h in (F(-4, 7), F(1, 5), F(9, 8)):
            psi_prime = h * psi
            for c_value in (F(-7, 5), F(3, 4)):
                tau = c_value * psi ** n
                tau_prime = n * h * tau
                for d_value in (F(0), F(-5, 6), F(7, 4)):
                    q_value = d_value * psi ** -6
                    q_prime = -6 * h * q_value
                    kdiag = (a_value * tau, b_value * tau + q_value, b_value * tau - q_value)
                    kdiag_prime = (a_value * tau_prime, b_value * tau_prime + q_prime, b_value * tau_prime - q_prime)
                    momentum = direct_momentum_from_connection(
                        psi, psi_prime, kdiag, kdiag_prime, tau, tau_prime
                    )
                    check(f"direct tensor momentum n={n} psi={psi} h={h} c={c_value} d={d_value}", momentum == (0, 0, 0))
                    for lam in (F(-3, 2), F(0), F(8, 5)):
                        for psi_second in (F(-2, 3), F(11, 10)):
                            ricci, _ = ricci_mixed_from_connection(psi, psi_prime, psi_second)
                            direct_h = sum(ricci) + tau ** 2 - sum(value * value for value in kdiag) - 2 * lam
                            reduced = (
                                -8 * psi_second
                                + F(8 * (n + 3), (n + 6) ** 2) * c_value ** 2 * psi ** (2 * n + 5)
                                - 2 * d_value ** 2 * psi ** -7
                                - 2 * lam * psi ** 5
                            )
                            check(f"direct tensor Hamiltonian n={n} psi={psi} d={d_value} lam={lam}", direct_h * psi ** 5 == reduced)


# Independent n=-2 Weyl reconstruction, including covariant magnetic curl.
weyl_rows = []
for p, c_value, d_value in (
    (F(1), F(4), F(0)),
    (F(1), F(4), F(1, 2)),
    (F(3, 2), F(5), F(1, 3)),
):
    lam = (c_value ** 2 * p ** 8 - 4 * d_value ** 2) / (4 * p ** 12)
    omega2 = c_value ** 2 / 4 - 3 * d_value ** 2 * p ** -8
    check(f"independent center lambda p={p} c={c_value} d={d_value}", lam > 0)
    check(f"independent center stability p={p} c={c_value} d={d_value}", omega2 > 0)
    for psi in (p * F(9, 10), p, p * F(11, 10)):
        for psi_prime in (F(-1, 13), F(0), F(1, 19)):
            h = psi_prime / psi
            tau = c_value * psi ** -2
            tau_prime = -2 * h * tau
            q_value = d_value * psi ** -6
            q_prime = -6 * h * q_value
            kdiag = (F(0), tau / 2 + q_value, tau / 2 - q_value)
            kdiag_prime = (F(0), tau_prime / 2 + q_prime, tau_prime / 2 - q_prime)
            psi_second = ode_second_nminus2(psi, c_value, d_value, lam)
            ricci, _ = ricci_mixed_from_connection(psi, psi_prime, psi_second)
            electric = tuple(
                ricci[i] + tau * kdiag[i] - kdiag[i] ** 2 - F(2, 3) * lam
                for i in range(3)
            )
            ex = 4 * psi ** -6 * psi_prime ** 2 - c_value ** 2 * psi ** -4 / 4 + d_value ** 2 * psi ** -12 + lam / 3
            check(f"independent electric form p={p} psi={psi} psip={psi_prime} d={d_value}", electric == (ex, -ex / 2, -ex / 2))
            magnetic = magnetic_from_connection(
                psi, psi_prime, psi_second, kdiag, kdiag_prime
            )
            candidate = -4 * d_value * h * psi ** -8
            expected_magnetic = (
                (F(0), F(0), F(0)),
                (F(0), F(0), candidate),
                (F(0), candidate, F(0)),
            )
            check(f"independent magnetic form p={p} psi={psi} psip={psi_prime} d={d_value}", magnetic == expected_magnetic)
            check(f"independent magnetic symmetry p={p} psi={psi} psip={psi_prime} d={d_value}", magnetic[1][2] == magnetic[2][1])
            i_value = first_integral(psi, psi_prime, c_value, d_value, lam)
            check(f"independent E-I relation p={p} psi={psi} psip={psi_prime} d={d_value}", ex == -i_value * psi ** -6 + F(4, 3) * d_value ** 2 * psi ** -12)
            e_norm = sum(value * value for value in electric)
            b_norm = sum(value * value for row in magnetic for value in row)
            check(f"nonnegative Weyl norm p={p} psi={psi} psip={psi_prime} d={d_value}", e_norm + b_norm >= 0)
            weyl_rows.append((p, c_value, d_value, psi, psi_prime, e_norm, b_norm))


# Old G317 direct form has a nonzero physical momentum residual when psi varies.
for psi in (F(2, 3), F(1), F(7, 4)):
    for h in (F(-3, 5), F(2, 7)):
        tau = F(5, 4)
        q_value = F(2, 3) * psi ** -6
        kdiag = (tau, q_value, -q_value)
        kdiag_prime = (F(0), -6 * h * q_value, 6 * h * q_value)
        momentum = direct_momentum_from_connection(
            psi, h * psi, kdiag, kdiag_prime, tau, F(0)
        )
        check(f"independent old-form obstruction psi={psi} h={h}", momentum[0] == 4 * h * tau and momentum[0] != 0)


result = {
    "schema": "udt-g318-independent-tensor-replay-v1",
    "status": "PASS",
    "assertion_count": len(CHECKS),
    "method": "independent Christoffel-Ricci-constraint-and-Weyl index loops",
    "production_imported": False,
    "production_result_read": False,
    "weyl_instances": len(weyl_rows),
    "landing_upheld": True,
    "checks": CHECKS,
}
(HERE / "INDEPENDENT_VERIFICATION.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
print(json.dumps({
    "status": "PASS",
    "assertions": len(CHECKS),
    "weyl_instances": len(weyl_rows),
}, indent=2))
