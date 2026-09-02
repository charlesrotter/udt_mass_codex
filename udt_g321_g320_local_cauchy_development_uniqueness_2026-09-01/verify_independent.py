#!/usr/bin/env python3
"""Implementation-distinct G321 verification using connection/index loops."""

import json
import math
from pathlib import Path


HERE = Path(__file__).resolve().parent
CHECKS = []
P = 1.7  # CHOSE_CATEGORY_A_INDEPENDENT_CONTROL
AMPLITUDE = 0.12  # CHOSE_CATEGORY_A_INDEPENDENT_CONTROL
J0 = 300.0  # CHOSE_CATEGORY_A_INDEPENDENT_CONTROL
MODES = (1, 3, 5)  # FREE_AND_EXPLORED_INDEPENDENT_CONTROLS
SIGNS = (-1, 1)  # FREE_AND_EXPLORED_BRANCHES
SAMPLES = 3072  # CATEGORY_A_NUMERICAL_QUADRATURE


def check(label, condition):
    if not condition:
        raise AssertionError(label)
    CHECKS.append(label)


def jet(x_value, mode):
    angle = mode * x_value
    return (
        P + AMPLITUDE * math.cos(angle),
        -AMPLITUDE * mode * math.sin(angle),
        -AMPLITUDE * mode ** 2 * math.cos(angle),
        AMPLITUDE * mode ** 3 * math.sin(angle),
    )


def geometry(psi, psi_1, psi_2):
    scale = psi ** 4
    scale_1 = 4.0 * psi ** 3 * psi_1
    scale_2 = 12.0 * psi ** 2 * psi_1 ** 2 + 4.0 * psi ** 3 * psi_2
    g = [[scale * float(i == j) for j in range(3)] for i in range(3)]
    g_inv = [[float(i == j) / scale for j in range(3)] for i in range(3)]
    dg = [[[0.0 for _ in range(3)] for _ in range(3)] for _ in range(3)]
    ddg = [[[[0.0 for _ in range(3)] for _ in range(3)] for _ in range(3)] for _ in range(3)]
    for i in range(3):
        dg[0][i][i] = scale_1
        ddg[0][0][i][i] = scale_2
    dg_inv = [[[0.0 for _ in range(3)] for _ in range(3)] for _ in range(3)]
    for i in range(3):
        dg_inv[0][i][i] = -scale_1 / scale ** 2

    gamma = [[[0.0 for _ in range(3)] for _ in range(3)] for _ in range(3)]
    dgamma = [[[[0.0 for _ in range(3)] for _ in range(3)] for _ in range(3)] for _ in range(3)]
    for upper in range(3):
        for i in range(3):
            for j in range(3):
                for lower in range(3):
                    bracket = dg[i][j][lower] + dg[j][i][lower] - dg[lower][i][j]
                    gamma[upper][i][j] += 0.5 * g_inv[upper][lower] * bracket
                    for derivative in range(3):
                        dbracket = (
                            ddg[derivative][i][j][lower]
                            + ddg[derivative][j][i][lower]
                            - ddg[derivative][lower][i][j]
                        )
                        dgamma[derivative][upper][i][j] += 0.5 * (
                            dg_inv[derivative][upper][lower] * bracket
                            + g_inv[upper][lower] * dbracket
                        )

    ricci = [[0.0 for _ in range(3)] for _ in range(3)]
    for i in range(3):
        for j in range(3):
            for k in range(3):
                ricci[i][j] += dgamma[k][k][i][j] - dgamma[j][k][i][k]
                for lower in range(3):
                    ricci[i][j] += (
                        gamma[k][i][j] * gamma[lower][k][lower]
                        - gamma[lower][i][k] * gamma[k][j][lower]
                    )
    scalar = sum(g_inv[i][j] * ricci[i][j] for i in range(3) for j in range(3))
    return g, g_inv, gamma, ricci, scalar


def reconstruct(psi, psi_1, psi_2, psi_3, sign):
    f_value = 12.0 * psi_2 * psi ** -5
    f_prime = 12.0 * (psi_3 * psi ** -5 - 5.0 * psi_2 * psi ** -6 * psi_1)
    z_value = 36.0 * psi_1 ** 2 + J0
    z_prime = 72.0 * psi_1 * psi_2
    b_value = sign * psi ** -3 * math.sqrt(z_value)
    b_prime = b_value * (-3.0 * psi_1 / psi + z_prime / (2.0 * z_value))
    a_value = f_value / b_value
    a_prime = f_prime / b_value - f_value * b_prime / b_value ** 2
    tau = 0.5 * (a_value + b_value)
    anisotropy = 0.5 * (a_value - b_value)
    tau_prime = 0.5 * (a_prime + b_prime)
    anisotropy_prime = 0.5 * (a_prime - b_prime)
    mixed_k = [
        (tau + 2.0 * anisotropy) / 3.0,
        (tau - anisotropy) / 3.0,
        (tau - anisotropy) / 3.0,
    ]
    mixed_k_prime = [
        (tau_prime + 2.0 * anisotropy_prime) / 3.0,
        (tau_prime - anisotropy_prime) / 3.0,
        (tau_prime - anisotropy_prime) / 3.0,
    ]
    g, _, gamma, ricci, scalar = geometry(psi, psi_1, psi_2)
    hamiltonian = scalar + tau ** 2 - sum(value ** 2 for value in mixed_k)

    tensor = [[0.0 for _ in range(3)] for _ in range(3)]
    for index in range(3):
        tensor[index][index] = mixed_k[index] - tau
    momentum = []
    for i in range(3):
        value = mixed_k_prime[0] - tau_prime if i == 0 else 0.0
        for j in range(3):
            value += gamma[j][j][i] * tensor[i][i]
            value -= gamma[j][j][i] * tensor[j][j]
        momentum.append(value)

    k_cov = [g[index][index] * mixed_k[index] for index in range(3)]
    gamma_dot = [-2.0 * value for value in k_cov]
    k_dot = [
        ricci[index][index] + tau * k_cov[index]
        - 2.0 * g[index][index] * mixed_k[index] ** 2
        for index in range(3)
    ]
    return {
        "g": tuple(g[index][index] for index in range(3)),
        "K": tuple(k_cov),
        "gamma_dot": tuple(gamma_dot),
        "K_dot": tuple(k_dot),
        "hamiltonian": hamiltonian,
        "momentum": tuple(momentum),
        "scalar": scalar,
    }


max_hamiltonian = 0.0
max_momentum = 0.0
max_ricci_formula_error = 0.0
max_time_reversal_error = 0.0
q_values = {}
for mode in MODES:
    branch_rows = {}
    weighted_scalar = []
    weights = []
    for sign in SIGNS:
        rows = []
        for index in range(SAMPLES):
            x_value = 2.0 * math.pi * index / SAMPLES
            values = jet(x_value, mode)
            row = reconstruct(*values, sign)
            rows.append(row)
            psi, psi_1, psi_2, _ = values
            expected_scalar = -8.0 * psi ** -5 * psi_2
            max_ricci_formula_error = max(max_ricci_formula_error, abs(row["scalar"] - expected_scalar))
            max_hamiltonian = max(max_hamiltonian, abs(row["hamiltonian"]))
            max_momentum = max(max_momentum, *(abs(value) for value in row["momentum"]))
            if sign == 1:
                weights.append(psi ** 6)
                weighted_scalar.append(psi ** 6 * row["scalar"])
        branch_rows[sign] = rows

    volume = (2.0 * math.pi) ** 3 * math.fsum(weights) / SAMPLES
    total_scalar = (2.0 * math.pi) ** 3 * math.fsum(weighted_scalar) / SAMPLES
    q_values[mode] = total_scalar / volume ** (1.0 / 3.0)

    for minus, plus in zip(branch_rows[-1], branch_rows[1]):
        for axis in range(3):
            max_time_reversal_error = max(
                max_time_reversal_error,
                abs(minus["K"][axis] + plus["K"][axis]),
                abs(minus["gamma_dot"][axis] + plus["gamma_dot"][axis]),
                abs(minus["K_dot"][axis] - plus["K_dot"][axis]),
            )

check("direct loop Ricci agrees with scalar anchor", max_ricci_formula_error < 2e-13)
check("independent Hamiltonian", max_hamiltonian < 5e-12)
check("independent momentum", max_momentum < 5e-12)
check("independent time reversal", max_time_reversal_error < 5e-12)
for mode in MODES:
    check(f"independent Q mode square n={mode}", abs(q_values[mode] / q_values[1] - mode ** 2) < 5e-12)

result = {
    "schema": "udt-g321-independent-local-development-v1",
    "status": "PASS_INDEPENDENT",
    "assertion_count": len(CHECKS),
    "production_imported": False,
    "production_output_read": False,
    "connection_ricci_index_loop": True,
    "modes_checked": list(MODES),
    "branches_checked": list(SIGNS),
    "max_ricci_formula_error": max_ricci_formula_error,
    "max_hamiltonian_residual": max_hamiltonian,
    "max_momentum_residual": max_momentum,
    "max_time_reversal_error": max_time_reversal_error,
    "conditional_theorem_application_upheld": True,
    "global_or_occupancy_claim": False,
}
with (HERE / "INDEPENDENT_VERIFICATION.json").open("w", encoding="utf-8") as handle:
    json.dump(result, handle, indent=2, sort_keys=True)
    handle.write("\n")
print(json.dumps(result, indent=2, sort_keys=True))
