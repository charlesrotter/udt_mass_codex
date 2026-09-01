#!/usr/bin/env python3
"""Dependency-free exact and bounded numerical derivation for G319."""

import csv
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


def mean(values):
    return sum(values) / len(values)


def f_value(psi, psi_second, d_value, lam):
    return 12 * psi_second * psi ** -5 + 3 * d_value ** 2 * psi ** -12 + 3 * lam


def total_bar_a(v_value, d_value):
    return (
        F(2, 3) * v_value,
        -F(1, 3) * v_value + d_value,
        -F(1, 3) * v_value - d_value,
    )


def conformal_scalar(psi, psi_second, tau, v_value, d_value, lam):
    norm2 = sum(item * item for item in total_bar_a(v_value, d_value))
    return (
        -8 * psi_second
        - norm2 * psi ** -7
        + (F(2, 3) * tau ** 2 - 2 * lam) * psi ** 5
    )


def physical_k(psi, tau, lambda_value, d_value):
    q_value = d_value * psi ** -6
    return (
        (tau + 2 * lambda_value) / 3,
        (tau - lambda_value) / 3 + q_value,
        (tau - lambda_value) / 3 - q_value,
    )


def physical_hamiltonian(psi, psi_second, tau, kdiag, lam):
    scalar_3 = -8 * psi ** -5 * psi_second
    return scalar_3 + tau ** 2 - sum(item * item for item in kdiag) - 2 * lam


def direct_momentum_x(psi, psi_prime, tau, tau_prime, lambda_value, lambda_prime):
    h_value = psi_prime / psi
    kx = (tau + 2 * lambda_value) / 3
    kx_prime = (tau_prime + 2 * lambda_prime) / 3
    return kx_prime - tau_prime + 6 * h_value * kx - 2 * h_value * tau


def conserved_j(psi, psi_prime, b_value, d_value, lam):
    return (
        psi ** 6 * b_value ** 2
        - 36 * psi_prime ** 2
        + 3 * d_value ** 2 * psi ** -6
        - 3 * lam * psi ** 6
    )


def conserved_j_prime(
    psi, psi_prime, psi_second, b_value, b_prime, d_value, lam
):
    return (
        6 * psi ** 5 * psi_prime * b_value ** 2
        + 2 * psi ** 6 * b_value * b_prime
        - 72 * psi_prime * psi_second
        - 18 * d_value ** 2 * psi ** -7 * psi_prime
        - 18 * lam * psi ** 5 * psi_prime
    )


LANDING = (
    "RATIO_FREE_REGULAR_STRATUM_HAS_EXACT_QUADRATURE_AND_ARBITRARY_"
    "POSITIVE_PERIODIC_PSI__B_ZERO_REMAINS_A_COMPATIBILITY_STRATUM__"
    "G318_POWER_OBSTRUCTIONS_ARE_ANSATZ_SCOPED__NO_PHYSICAL_DATA_SELECTION"
)


# Exact local-jet equivalence: no ratio between lambda and tau is assumed.
for psi in (F(1, 2), F(3, 4), F(1), F(5, 4), F(2), F(7, 3)):
    for psi_prime in (F(-5, 7), F(-1, 9), F(2, 11), F(4, 3)):
        h_value = psi_prime / psi
        for a_value in (F(-7, 5), F(-1, 4), F(2, 3), F(9, 4)):
            for b_value in (F(-8, 5), F(-2, 7), F(3, 5), F(11, 6)):
                for a_prime in (F(-13, 8), F(1, 10), F(7, 6)):
                    for d_value in (F(0), F(-3, 5), F(7, 4)):
                        for lam in (F(-5, 3), F(0), F(13, 7)):
                            # Choose psi'' so the scalar constraint AB=F holds exactly.
                            psi_second = psi ** 5 * (
                                a_value * b_value
                                - 3 * d_value ** 2 * psi ** -12
                                - 3 * lam
                            ) / 12
                            f_local = f_value(psi, psi_second, d_value, lam)
                            b_prime = 3 * h_value * (a_value - b_value)
                            tau = (a_value + b_value) / 2
                            lambda_value = (a_value - b_value) / 2
                            tau_prime = (a_prime + b_prime) / 2
                            lambda_prime = (a_prime - b_prime) / 2
                            v_value = psi ** 6 * lambda_value
                            v_prime = psi ** 6 * (
                                lambda_prime + 6 * h_value * lambda_value
                            )
                            kdiag = physical_k(
                                psi, tau, lambda_value, d_value
                            )

                            prefix = (
                                f"psi={psi} psip={psi_prime} A={a_value} "
                                f"B={b_value} d={d_value} L={lam}"
                            )
                            check(f"scalar factorization {prefix}", f_local == a_value * b_value)
                            check(f"vector B equation {prefix}", b_prime == 3 * h_value * (a_value - b_value))
                            check(f"vector original equation {prefix}", v_prime == psi ** 6 * tau_prime)
                            check(f"physical K trace {prefix}", sum(kdiag) == tau)
                            check(f"conformal scalar {prefix}", conformal_scalar(psi, psi_second, tau, v_value, d_value, lam) == 0)
                            check(f"physical Hamiltonian {prefix}", physical_hamiltonian(psi, psi_second, tau, kdiag, lam) == 0)
                            check(f"physical momentum {prefix}", direct_momentum_x(psi, psi_prime, tau, tau_prime, lambda_value, lambda_prime) == 0)
                            check(f"conserved J derivative {prefix}", conserved_j_prime(psi, psi_prime, psi_second, b_value, b_prime, d_value, lam) == 0)


# The B=0 stratum is compatible at F=0, but the regular reconstruction cannot divide through it.
zero_rows = []
for psi in (F(2, 3), F(1), F(5, 3), F(9, 4)):
    for psi_prime in (F(-3, 5), F(0), F(4, 7)):
        h_value = psi_prime / psi
        for a_value in (F(-5, 4), F(0), F(7, 6)):
            for d_value in (F(0), F(2, 5), F(7, 3)):
                for lam in (F(-4, 3), F(0), F(5, 6)):
                    psi_second = -psi ** 5 * (
                        3 * d_value ** 2 * psi ** -12 + 3 * lam
                    ) / 12
                    b_value = F(0)
                    b_prime = 3 * h_value * a_value
                    check("B-zero scalar compatibility", f_value(psi, psi_second, d_value, lam) == 0)
                    check("B-zero vector compatibility", b_prime == 3 * h_value * a_value)
                    check("B-zero conserved derivative", conserved_j_prime(psi, psi_prime, psi_second, b_value, b_prime, d_value, lam) == 0)
                    zero_rows.append((psi, psi_prime, a_value, d_value, lam, b_prime))


# Exact periodic mean reconstruction for freely varying v samples.
for values in (
    (F(1), F(3), F(-2), F(5), F(7)),
    (F(-4, 3), F(2, 7), F(9, 5), F(-3, 2), F(8, 9)),
    (F(0), F(1, 11), F(2, 11), F(3, 11), F(4, 11)),
):
    mean_v = sum(values, F(0)) / len(values)
    alpha = F(2, 3) * mean_v
    w_primes = tuple((value - mean_v) / 2 for value in values)
    check("periodic mean subtraction", sum(w_primes, F(0)) == 0)
    for value, w_prime in zip(values, w_primes):
        seed = (alpha, -alpha / 2 + F(5, 8), -alpha / 2 - F(5, 8))
        long_part = (F(4, 3) * w_prime, -F(2, 3) * w_prime, -F(2, 3) * w_prime)
        combined = tuple(left + right for left, right in zip(seed, long_part))
        check("periodic TT-longitudinal reconstruction", combined == total_bar_a(value, F(5, 8)))


# G318 embeds exactly whenever its scalar ODE is imposed.
for n in (-9, -8, -7, -5, -4, -3, -2, -1, 1, 3, 5):
    if n == -6:
        continue
    for psi in (F(2, 3), F(1), F(7, 4)):
        for psi_prime in (F(-2, 5), F(1, 7), F(5, 6)):
            for c_value in (F(-7, 5), F(3, 4), F(11, 6)):
                tau = c_value * psi ** n
                lambda_value = F(n, n + 6) * tau
                a_value = tau + lambda_value
                b_value = tau - lambda_value
                for d_value in (F(0), F(2, 3)):
                    for lam in (F(-1, 2), F(0), F(9, 7)):
                        psi_second = (
                            F(n + 3, (n + 6) ** 2) * c_value ** 2 * psi ** (2 * n + 5)
                            - F(1, 4) * d_value ** 2 * psi ** -7
                            - F(1, 4) * lam * psi ** 5
                        )
                        f_local = f_value(psi, psi_second, d_value, lam)
                        h_value = psi_prime / psi
                        b_prime = 3 * h_value * (a_value - b_value)
                        check(f"G318 scalar embedding n={n}", a_value * b_value == f_local)
                        check(f"G318 J conservation n={n}", conserved_j_prime(psi, psi_prime, psi_second, b_value, b_prime, d_value, lam) == 0)


def profile_reconstruction(p_value, amplitude, mode, d_value, lam, sign, samples=2048):
    raw = []
    lower_bound = -float("inf")
    for index in range(samples):
        x_value = 2 * math.pi * index / samples
        cosine = math.cos(mode * x_value)
        sine = math.sin(mode * x_value)
        psi = p_value + amplitude * cosine
        psi_prime = -amplitude * mode * sine
        psi_second = -amplitude * mode ** 2 * cosine
        psi_third = amplitude * mode ** 3 * sine
        f_local = 12 * psi_second * psi ** -5 + 3 * d_value ** 2 * psi ** -12 + 3 * lam
        f_prime = (
            12 * (psi_third * psi ** -5 - 5 * psi_second * psi ** -6 * psi_prime)
            - 36 * d_value ** 2 * psi ** -13 * psi_prime
        )
        g_local = 36 * psi_prime ** 2 - 3 * d_value ** 2 * psi ** -6 + 3 * lam * psi ** 6
        g_prime = (
            72 * psi_prime * psi_second
            + 18 * d_value ** 2 * psi ** -7 * psi_prime
            + 18 * lam * psi ** 5 * psi_prime
        )
        lower_bound = max(lower_bound, -g_local, -g_local - psi ** 6 * f_local)
        raw.append((x_value, psi, psi_prime, psi_second, f_local, f_prime, g_local, g_prime))

    j_zero = lower_bound + 5.0
    rows = []
    for x_value, psi, psi_prime, psi_second, f_local, f_prime, g_local, g_prime in raw:
        z_value = g_local + j_zero
        b_value = sign * psi ** -3 * math.sqrt(z_value)
        h_value = psi_prime / psi
        b_prime = b_value * (-3 * h_value + g_prime / (2 * z_value))
        a_value = f_local / b_value
        a_prime = f_prime / b_value - f_local * b_prime / b_value ** 2
        tau = (a_value + b_value) / 2
        lambda_value = (a_value - b_value) / 2
        tau_prime = (a_prime + b_prime) / 2
        lambda_prime = (a_prime - b_prime) / 2
        v_value = psi ** 6 * lambda_value
        v_prime = psi ** 6 * (lambda_prime + 6 * h_value * lambda_value)
        q_value = d_value * psi ** -6
        kdiag = (
            (tau + 2 * lambda_value) / 3,
            (tau - lambda_value) / 3 + q_value,
            (tau - lambda_value) / 3 - q_value,
        )
        ham = -8 * psi ** -5 * psi_second + tau ** 2 - sum(item * item for item in kdiag) - 2 * lam
        momentum = (
            (tau_prime + 2 * lambda_prime) / 3
            - tau_prime
            + 6 * h_value * kdiag[0]
            - 2 * h_value * tau
        )
        vector = v_prime - psi ** 6 * tau_prime
        scalar = -8 * psi_second - (F(2, 3) * v_value ** 2 + 2 * d_value ** 2) * psi ** -7 + (F(2, 3) * tau ** 2 - 2 * lam) * psi ** 5
        j_local = psi ** 6 * b_value ** 2 - 36 * psi_prime ** 2 + 3 * d_value ** 2 * psi ** -6 - 3 * lam * psi ** 6
        rows.append({
            "x": x_value,
            "psi": psi,
            "tau": tau,
            "lambda": lambda_value,
            "ratio": lambda_value / tau,
            "v": v_value,
            "B2": b_value ** 2,
            "B2_plus_F": b_value ** 2 + f_local,
            "ham": ham,
            "momentum": momentum,
            "vector": vector,
            "scalar": float(scalar),
            "J": j_local,
        })
    return j_zero, rows


# Explicit regular periodic controls with genuinely nonconstant lambda/tau.
profiles = (
    (1.40, 0.21, 1, 0.30, 0.40),
    (1.10, 0.08, 2, 0.00, -0.15),
    (1.75, 0.33, 3, 0.45, 0.00),
    (0.95, 0.11, 4, 0.20, 0.70),
)
profile_rows = []
for profile_index, parameters in enumerate(profiles, start=1):
    for sign in (1, -1):
        j_zero, rows = profile_reconstruction(*parameters, sign)
        taus = [row["tau"] for row in rows]
        ratios = [row["ratio"] for row in rows]
        check(f"profile {profile_index} psi positive", parameters[0] > abs(parameters[1]))
        check(f"profile {profile_index} B2 positive sign={sign}", min(row["B2"] for row in rows) > 0)
        check(f"profile {profile_index} B2+F positive sign={sign}", min(row["B2_plus_F"] for row in rows) > 0)
        check(f"profile {profile_index} tau sign sign={sign}", min(sign * value for value in taus) > 0)
        check(f"profile {profile_index} variable ratio sign={sign}", max(ratios) - min(ratios) > 1e-5)
        check(f"profile {profile_index} Hamiltonian sign={sign}", max(abs(row["ham"]) for row in rows) < 2e-10)
        check(f"profile {profile_index} momentum sign={sign}", max(abs(row["momentum"]) for row in rows) < 2e-10)
        check(f"profile {profile_index} vector sign={sign}", max(abs(row["vector"]) for row in rows) < 2e-9)
        check(f"profile {profile_index} scalar sign={sign}", max(abs(row["scalar"]) for row in rows) < 2e-9)
        check(f"profile {profile_index} J constant sign={sign}", max(abs(row["J"] - j_zero) for row in rows) < 2e-9)
        v_values = [row["v"] for row in rows]
        mean_v = mean(v_values)
        w_primes = [(value - mean_v) / 2 for value in v_values]
        check(f"profile {profile_index} periodic mean sign={sign}", abs(mean(w_primes)) < 2e-13)
        profile_rows.append({
            "profile": profile_index,
            "sign": sign,
            "p": parameters[0],
            "amplitude": parameters[1],
            "mode": parameters[2],
            "d": parameters[3],
            "Lambda": parameters[4],
            "J0": j_zero,
            "min_psi": min(row["psi"] for row in rows),
            "min_abs_tau": min(abs(value) for value in taus),
            "ratio_range": max(ratios) - min(ratios),
            "max_hamiltonian": max(abs(row["ham"]) for row in rows),
            "max_momentum": max(abs(row["momentum"]) for row in rows),
            "max_J_drift": max(abs(row["J"] - j_zero) for row in rows),
        })


with (HERE / "PROFILE_ATLAS.tsv").open("w", encoding="utf-8", newline="") as handle:
    writer = csv.DictWriter(handle, fieldnames=profile_rows[0].keys(), delimiter="\t")
    writer.writeheader()
    writer.writerows(profile_rows)


classification = {
    "ratio_free_equations": "B_PRIME_EQUALS_3H_A_MINUS_B__AB_EQUALS_F",
    "regular_stratum": "EXACT_ONE_CONSTANT_QUADRATURE",
    "positive_periodic_psi": "ARBITRARY_WITH_SUFFICIENTLY_LARGE_FREE_J0",
    "B_zero": "COMPATIBILITY_GLUE_STRATUM_NOT_GLOBALLY_PARAMETERIZED",
    "G318_power_family": "EXACT_EMBEDDED_SUBFAMILY",
    "G318_n_le_minus3_obstruction": "CONSTANT_RATIO_ANSATZ_SCOPED",
    "G318_periodic_tidal_family": "SURVIVES_AS_EMBEDDED_SUBFAMILY",
    "physical_data_selection": "NOT_SELECTED",
}

result = {
    "schema": "udt-g319-ratio-free-constraint-descent-v1",
    "status": "PASS_PENDING_EXTERNAL_REVIEW",
    "landing": LANDING,
    "assertion_count": len(CHECKS),
    "exact_zero_stratum_instances": len(zero_rows),
    "periodic_profile_witnesses": len(profile_rows),
    "classification": classification,
    "metric_changed": False,
    "kernel_changed": False,
    "selected_history": False,
    "selected_scale": False,
    "selected_Xmax": False,
    "checks": CHECKS,
}
(HERE / "DERIVATION_RESULT.json").write_text(
    json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
)
print(json.dumps({
    "status": result["status"],
    "landing": LANDING,
    "assertions": len(CHECKS),
    "zero_stratum_instances": len(zero_rows),
    "periodic_profile_witnesses": len(profile_rows),
}, indent=2))
