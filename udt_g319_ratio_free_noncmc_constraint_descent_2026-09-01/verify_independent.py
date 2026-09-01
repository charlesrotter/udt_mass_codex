#!/usr/bin/env python3
"""Implementation-distinct direct-tensor verification for G319.

This script imports no production code and reads no production result.
"""

from fractions import Fraction as F
import json
import math
from pathlib import Path


HERE = Path(__file__).resolve().parent
CHECKS = []


def check(label, condition):
    if not condition:
        raise AssertionError(label)
    CHECKS.append(label)


def delta(i, j):
    return 1 if i == j else 0


def connection(psi, psi_prime):
    u = (2 * psi_prime / psi, F(0), F(0))
    gamma = [[[F(0) for _ in range(3)] for _ in range(3)] for _ in range(3)]
    for upper in range(3):
        for left in range(3):
            for right in range(3):
                gamma[upper][left][right] = (
                    delta(upper, left) * u[right]
                    + delta(upper, right) * u[left]
                    - delta(left, right) * u[upper]
                )
    return gamma


def ricci_scalar(psi, psi_prime, psi_second):
    h_value = psi_prime / psi
    h_prime = psi_second / psi - h_value ** 2
    u = (2 * h_value, F(0), F(0))
    ux = (2 * h_prime, F(0), F(0))
    gamma = connection(psi, psi_prime)
    dgamma = [[[F(0) for _ in range(3)] for _ in range(3)] for _ in range(3)]
    for upper in range(3):
        for left in range(3):
            for right in range(3):
                dgamma[upper][left][right] = (
                    delta(upper, left) * ux[right]
                    + delta(upper, right) * ux[left]
                    - delta(left, right) * ux[upper]
                )
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
    return sum(ricci_cov[i][i] * psi ** -4 for i in range(3))


def momentum_from_connection(psi, psi_prime, kdiag, kdiag_prime, tau, tau_prime):
    gamma = connection(psi, psi_prime)
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


# Direct tensor replay on unconstrained A' and fully variable A/B jets.
for psi in (F(1, 2), F(4, 5), F(1), F(3, 2), F(5, 2)):
    for psi_prime in (F(-7, 8), F(-1, 10), F(3, 11), F(5, 4)):
        h_value = psi_prime / psi
        for a_value in (F(-9, 5), F(-2, 9), F(4, 7), F(13, 6)):
            for b_value in (F(-11, 7), F(-1, 3), F(5, 8), F(7, 3)):
                for a_prime in (F(-5, 3), F(1, 12), F(8, 7)):
                    for d_value in (F(0), F(-4, 7), F(9, 5)):
                        for lam in (F(-8, 5), F(0), F(7, 6)):
                            psi_second = psi ** 5 * (
                                a_value * b_value
                                - 3 * d_value ** 2 * psi ** -12
                                - 3 * lam
                            ) / 12
                            b_prime = 3 * h_value * (a_value - b_value)
                            tau = (a_value + b_value) / 2
                            mu = (a_value - b_value) / 2
                            tau_prime = (a_prime + b_prime) / 2
                            mu_prime = (a_prime - b_prime) / 2
                            q_value = d_value * psi ** -6
                            q_prime = -6 * h_value * q_value
                            kdiag = (
                                (tau + 2 * mu) / 3,
                                (tau - mu) / 3 + q_value,
                                (tau - mu) / 3 - q_value,
                            )
                            kdiag_prime = (
                                (tau_prime + 2 * mu_prime) / 3,
                                (tau_prime - mu_prime) / 3 + q_prime,
                                (tau_prime - mu_prime) / 3 - q_prime,
                            )
                            scalar_3 = ricci_scalar(psi, psi_prime, psi_second)
                            hamiltonian = scalar_3 + tau ** 2 - sum(item * item for item in kdiag) - 2 * lam
                            momentum = momentum_from_connection(
                                psi, psi_prime, kdiag, kdiag_prime, tau, tau_prime
                            )
                            j_prime = (
                                6 * psi ** 5 * psi_prime * b_value ** 2
                                + 2 * psi ** 6 * b_value * b_prime
                                - 72 * psi_prime * psi_second
                                - 18 * d_value ** 2 * psi ** -7 * psi_prime
                                - 18 * lam * psi ** 5 * psi_prime
                            )
                            prefix = f"psi={psi} A={a_value} B={b_value} d={d_value} L={lam}"
                            check(f"independent Ricci scalar {prefix}", scalar_3 == -8 * psi ** -5 * psi_second)
                            check(f"independent Hamiltonian {prefix}", hamiltonian == 0)
                            check(f"independent momentum {prefix}", momentum == (0, 0, 0))
                            check(f"independent J conservation {prefix}", j_prime == 0)


# Independent zero-stratum germs: no division by B is used.
for psi in (F(3, 5), F(1), F(8, 5)):
    for psi_prime in (F(-2, 3), F(0), F(5, 9)):
        h_value = psi_prime / psi
        for a_value in (F(-4, 3), F(0), F(6, 5)):
            for d_value in (F(0), F(5, 11)):
                for lam in (F(-7, 9), F(0), F(3, 4)):
                    psi_second = -psi ** 5 * (3 * d_value ** 2 * psi ** -12 + 3 * lam) / 12
                    b_value = F(0)
                    b_prime = 3 * h_value * a_value
                    f_local = 12 * psi_second * psi ** -5 + 3 * d_value ** 2 * psi ** -12 + 3 * lam
                    j_prime = (
                        2 * psi ** 6 * b_value * b_prime
                        - 72 * psi_prime * psi_second
                        - 18 * d_value ** 2 * psi ** -7 * psi_prime
                        - 18 * lam * psi ** 5 * psi_prime
                    )
                    check("independent B-zero F condition", f_local == 0)
                    check("independent B-zero derivative", b_prime == 3 * h_value * a_value)
                    check("independent B-zero J conservation", j_prime == 0)


# Independently construct several periodic variable-ratio families and check direct constraints.
profile_parameters = (
    (1.25, 0.13, 1, 0.15, 0.20),
    (1.60, 0.19, 2, 0.35, -0.10),
    (0.90, 0.06, 3, 0.00, 0.55),
)
periodic_instances = 0
max_direct_residual = 0.0
for p_value, amplitude, mode, d_value, lam in profile_parameters:
    samples = 1536
    jets = []
    lower = -float("inf")
    for index in range(samples):
        x_value = 2 * math.pi * index / samples
        psi = p_value + amplitude * math.cos(mode * x_value)
        psi_prime = -amplitude * mode * math.sin(mode * x_value)
        psi_second = -amplitude * mode ** 2 * math.cos(mode * x_value)
        psi_third = amplitude * mode ** 3 * math.sin(mode * x_value)
        f_local = 12 * psi_second * psi ** -5 + 3 * d_value ** 2 * psi ** -12 + 3 * lam
        f_prime = 12 * (psi_third * psi ** -5 - 5 * psi_second * psi ** -6 * psi_prime) - 36 * d_value ** 2 * psi ** -13 * psi_prime
        g_local = 36 * psi_prime ** 2 - 3 * d_value ** 2 * psi ** -6 + 3 * lam * psi ** 6
        g_prime = 72 * psi_prime * psi_second + 18 * d_value ** 2 * psi ** -7 * psi_prime + 18 * lam * psi ** 5 * psi_prime
        lower = max(lower, -g_local, -g_local - psi ** 6 * f_local)
        jets.append((psi, psi_prime, psi_second, f_local, f_prime, g_local, g_prime))
    j_zero = lower + 7.0
    for sign in (-1, 1):
        ratios = []
        taus = []
        for psi, psi_prime, psi_second, f_local, f_prime, g_local, g_prime in jets:
            z_value = g_local + j_zero
            b_value = sign * psi ** -3 * math.sqrt(z_value)
            b_prime = b_value * (-3 * psi_prime / psi + g_prime / (2 * z_value))
            a_value = f_local / b_value
            a_prime = f_prime / b_value - f_local * b_prime / b_value ** 2
            tau = (a_value + b_value) / 2
            mu = (a_value - b_value) / 2
            tau_prime = (a_prime + b_prime) / 2
            mu_prime = (a_prime - b_prime) / 2
            q_value = d_value * psi ** -6
            q_prime = -6 * psi_prime / psi * q_value
            kdiag = (
                (tau + 2 * mu) / 3,
                (tau - mu) / 3 + q_value,
                (tau - mu) / 3 - q_value,
            )
            kdiag_prime = (
                (tau_prime + 2 * mu_prime) / 3,
                (tau_prime - mu_prime) / 3 + q_prime,
                (tau_prime - mu_prime) / 3 - q_prime,
            )
            # This is the closed direct Ricci result obtained above from index loops.
            scalar_3 = -8 * psi ** -5 * psi_second
            hamiltonian = scalar_3 + tau ** 2 - sum(item * item for item in kdiag) - 2 * lam
            h_value = psi_prime / psi
            momentum_x = kdiag_prime[0] - tau_prime + 6 * h_value * kdiag[0] - 2 * h_value * tau
            max_direct_residual = max(max_direct_residual, abs(hamiltonian), abs(momentum_x))
            ratios.append(mu / tau)
            taus.append(tau)
        check("independent periodic tau sign", min(sign * item for item in taus) > 0)
        check("independent periodic variable ratio", max(ratios) - min(ratios) > 1e-5)
        periodic_instances += 1
check("independent periodic direct residual", max_direct_residual < 2e-10)


result = {
    "schema": "udt-g319-independent-direct-tensor-v1",
    "status": "PASS",
    "assertion_count": len(CHECKS),
    "method": "independent Christoffel-Ricci and physical constraint index loops",
    "production_imported": False,
    "production_result_read": False,
    "periodic_variable_ratio_instances": periodic_instances,
    "max_periodic_direct_residual": max_direct_residual,
    "landing_upheld": True,
    "checks": CHECKS,
}
(HERE / "INDEPENDENT_VERIFICATION.json").write_text(
    json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
)
print(json.dumps({
    "status": "PASS",
    "assertions": len(CHECKS),
    "periodic_variable_ratio_instances": periodic_instances,
    "max_direct_residual": max_direct_residual,
}, indent=2))
