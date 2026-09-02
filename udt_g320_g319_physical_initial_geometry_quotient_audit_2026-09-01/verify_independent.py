#!/usr/bin/env python3
"""Implementation-distinct G320 verification from physical tensors.

This file imports no production code and reads no production output.
"""

import json
import math
from pathlib import Path


HERE = Path(__file__).resolve().parent
CHECKS = []
TWO_PI = 2.0 * math.pi
SAMPLES = 3072  # CATEGORY_A_NUMERICAL_QUADRATURE


def check(label, condition):
    if not condition:
        raise AssertionError(label)
    CHECKS.append(label)


def delta(left, right):
    return 1.0 if left == right else 0.0


def ricci_scalar_by_index_loops(psi, psi_prime, psi_second):
    h_value = psi_prime / psi
    h_prime = psi_second / psi - h_value ** 2
    u = (2.0 * h_value, 0.0, 0.0)
    u_prime = (2.0 * h_prime, 0.0, 0.0)
    gamma = [[[0.0 for _ in range(3)] for _ in range(3)] for _ in range(3)]
    dgamma_x = [[[0.0 for _ in range(3)] for _ in range(3)] for _ in range(3)]
    for upper in range(3):
        for left in range(3):
            for right in range(3):
                gamma[upper][left][right] = (
                    delta(upper, left) * u[right]
                    + delta(upper, right) * u[left]
                    - delta(left, right) * u[upper]
                )
                dgamma_x[upper][left][right] = (
                    delta(upper, left) * u_prime[right]
                    + delta(upper, right) * u_prime[left]
                    - delta(left, right) * u_prime[upper]
                )
    ricci = [[0.0 for _ in range(3)] for _ in range(3)]
    for i in range(3):
        for j in range(3):
            value = dgamma_x[0][i][j]
            if j == 0:
                value -= sum(dgamma_x[k][i][k] for k in range(3))
            for k in range(3):
                for ell in range(3):
                    value += gamma[k][i][j] * gamma[ell][k][ell]
                    value -= gamma[ell][i][k] * gamma[k][j][ell]
            ricci[i][j] = value
    return psi ** -4 * sum(ricci[i][i] for i in range(3)), gamma


def momentum_by_index_loops(gamma, kdiag, kdiag_prime, tau, tau_prime):
    pmat = [[0.0 for _ in range(3)] for _ in range(3)]
    pprime = [[0.0 for _ in range(3)] for _ in range(3)]
    for i in range(3):
        pmat[i][i] = kdiag[i] - tau
        pprime[i][i] = kdiag_prime[i] - tau_prime
    answer = []
    for i in range(3):
        value = pprime[0][i]
        for j in range(3):
            for m in range(3):
                value += gamma[j][j][m] * pmat[m][i]
                value -= gamma[m][j][i] * pmat[j][m]
        answer.append(value)
    return tuple(answer)


def profile(x_value, mode, phase, reflected, p_value, amplitude):
    coordinate = -x_value if reflected else x_value
    orientation = -1.0 if reflected else 1.0
    argument = mode * (coordinate - phase)
    psi = p_value + amplitude * math.cos(argument)
    psi_prime = -amplitude * mode * math.sin(argument) * orientation
    psi_second = -amplitude * mode ** 2 * math.cos(argument)
    psi_third = amplitude * mode ** 3 * math.sin(argument) * orientation
    return psi, psi_prime, psi_second, psi_third


def evaluate(mode, sign, phase=0.0, reflected=False, p_value=4.0 / 3.0, amplitude=1.0 / 7.0):
    volume_terms = []
    scalar_terms = []
    tau_terms = []
    k2_terms = []
    max_ricci_formula_error = 0.0
    max_hamiltonian = 0.0
    max_momentum = 0.0
    min_signed_tau = float("inf")
    j0 = 200.0
    for index in range(SAMPLES):
        x_value = TWO_PI * index / SAMPLES
        psi, psi_prime, psi_second, psi_third = profile(
            x_value, mode, phase, reflected, p_value, amplitude
        )
        scalar_loop, gamma = ricci_scalar_by_index_loops(psi, psi_prime, psi_second)
        scalar_closed = -8.0 * psi ** -5 * psi_second
        max_ricci_formula_error = max(max_ricci_formula_error, abs(scalar_loop - scalar_closed))

        f_value = 12.0 * psi_second * psi ** -5
        f_prime = 12.0 * (
            psi_third * psi ** -5 - 5.0 * psi_second * psi ** -6 * psi_prime
        )
        z_value = 36.0 * psi_prime ** 2 + j0
        z_prime = 72.0 * psi_prime * psi_second
        b_value = sign * psi ** -3 * math.sqrt(z_value)
        b_prime = b_value * (-3.0 * psi_prime / psi + z_prime / (2.0 * z_value))
        a_value = f_value / b_value
        a_prime = f_prime / b_value - f_value * b_prime / b_value ** 2
        tau = 0.5 * (a_value + b_value)
        mu = 0.5 * (a_value - b_value)
        tau_prime = 0.5 * (a_prime + b_prime)
        mu_prime = 0.5 * (a_prime - b_prime)
        kdiag = (
            (tau + 2.0 * mu) / 3.0,
            (tau - mu) / 3.0,
            (tau - mu) / 3.0,
        )
        kdiag_prime = (
            (tau_prime + 2.0 * mu_prime) / 3.0,
            (tau_prime - mu_prime) / 3.0,
            (tau_prime - mu_prime) / 3.0,
        )
        hamiltonian = scalar_loop + tau ** 2 - sum(item * item for item in kdiag)
        momentum = momentum_by_index_loops(
            gamma, kdiag, kdiag_prime, tau, tau_prime
        )
        max_hamiltonian = max(max_hamiltonian, abs(hamiltonian))
        max_momentum = max(max_momentum, *(abs(item) for item in momentum))
        min_signed_tau = min(min_signed_tau, sign * tau)
        weight = psi ** 6
        volume_terms.append(weight)
        scalar_terms.append(weight * scalar_loop)
        tau_terms.append(weight * tau)
        k2_terms.append(weight * sum(item * item for item in kdiag))
    volume = TWO_PI ** 3 * math.fsum(volume_terms) / SAMPLES
    total_scalar = TWO_PI ** 3 * math.fsum(scalar_terms) / SAMPLES
    return {
        "volume": volume,
        "total_scalar": total_scalar,
        "Q_R": total_scalar / volume ** (1.0 / 3.0),
        "weighted_tau": math.fsum(tau_terms) / math.fsum(volume_terms),
        "weighted_K2": math.fsum(k2_terms) / math.fsum(volume_terms),
        "max_ricci_formula_error": max_ricci_formula_error,
        "max_hamiltonian": max_hamiltonian,
        "max_momentum": max_momentum,
        "min_signed_tau": min_signed_tau,
    }


# Different controls from production: distinct p, amplitude, modes, sample count, and J0.
modes = (1, 3, 5)
for sign in (-1, 1):
    baseline = evaluate(1, sign)
    check(f"independent baseline lawful sign={sign}", baseline["max_hamiltonian"] < 2e-12 and baseline["max_momentum"] < 2e-12)
    check(f"independent baseline tau sign={sign}", baseline["min_signed_tau"] > 0)
    check(f"independent direct Ricci sign={sign}", baseline["max_ricci_formula_error"] < 2e-14)
    for mode in modes[1:]:
        current = evaluate(mode, sign)
        check(f"independent same volume n={mode} sign={sign}", abs(current["volume"] - baseline["volume"]) < 2e-11)
        check(f"independent Q ratio n={mode} sign={sign}", abs(current["Q_R"] / baseline["Q_R"] - mode ** 2) < 3e-12)
        check(f"independent lawful n={mode} sign={sign}", current["max_hamiltonian"] < 3e-12 and current["max_momentum"] < 3e-12)
        check(f"independent tau sign n={mode} sign={sign}", current["min_signed_tau"] > 0)
        check(f"independent direct Ricci n={mode} sign={sign}", current["max_ricci_formula_error"] < 3e-13)


# Independent isometry controls on a mode absent from the production family.
for sign in (-1, 1):
    baseline = evaluate(5, sign)
    for phase, reflected in ((0.223, False), (0.817, False), (0.0, True)):
        control = evaluate(5, sign, phase=phase, reflected=reflected)
        for key in ("volume", "total_scalar", "Q_R", "weighted_tau", "weighted_K2"):
            tolerance = 5e-11 * max(1.0, abs(baseline[key]))
            check(f"independent isometry {key} sign={sign} phase={phase} reflect={reflected}", abs(control[key] - baseline[key]) < tolerance)


# Independent conformal-seed identity with a different nonconstant seed factor.
max_seed_metric_error = 0.0
max_seed_physical_a_error = 0.0
max_raw_seed_difference = 0.0
for index in range(SAMPLES):
    x_value = TWO_PI * index / SAMPLES
    psi = profile(x_value, 3, 0.0, False, 4.0 / 3.0, 1.0 / 7.0)[0]
    theta = math.exp(0.07 * math.cos(2.0 * x_value))
    reconstructed = (psi / theta) ** 4 * theta ** 4
    max_seed_metric_error = max(max_seed_metric_error, abs(reconstructed - psi ** 4))
    max_raw_seed_difference = max(max_raw_seed_difference, abs(psi / theta - psi))
    for bar_a in (1.75, -0.5, -1.25):
        original_physical_a = psi ** -10 * bar_a
        transformed_physical_a = (psi / theta) ** -10 * theta ** -10 * bar_a
        max_seed_physical_a_error = max(
            max_seed_physical_a_error,
            abs(transformed_physical_a - original_physical_a),
        )
check("independent seed fields differ", max_raw_seed_difference > 0.05)
check("independent seed metric identical", max_seed_metric_error < 4e-15)
check("independent seed physical A identical", max_seed_physical_a_error < 4e-15)


result = {
    "schema": "udt-g320-independent-physical-tensor-v1",
    "status": "PASS",
    "assertion_count": len(CHECKS),
    "method": "direct Christoffel-Ricci index loops plus physical constraint reconstruction",
    "production_imported": False,
    "production_result_read": False,
    "control_modes": list(modes),
    "branches": [-1, 1],
    "Q_R_mode_scaling": "n^2",
    "intrinsic_inequivalence_upheld": True,
    "isometry_controls_pass": True,
    "seed_duplicate_control_pass": True,
    "max_seed_metric_error": max_seed_metric_error,
    "max_seed_physical_A_error": max_seed_physical_a_error,
    "checks": CHECKS,
}
(HERE / "INDEPENDENT_VERIFICATION.json").write_text(
    json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
)
print(json.dumps({
    "status": "PASS",
    "assertions": len(CHECKS),
    "control_modes": list(modes),
    "max_seed_metric_error": max_seed_metric_error,
    "max_seed_physical_A_error": max_seed_physical_a_error,
}, indent=2))
