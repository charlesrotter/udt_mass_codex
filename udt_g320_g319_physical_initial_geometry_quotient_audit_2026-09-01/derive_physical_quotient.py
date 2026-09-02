#!/usr/bin/env python3
"""G320 production derivation: quotient G319 representation freedom physically."""

import csv
from fractions import Fraction
import json
import math
from pathlib import Path


HERE = Path(__file__).resolve().parent
CHECKS = []
P = Fraction(3, 2)  # CHOSE_CATEGORY_A_DIAGNOSTIC_CONTROL
A = Fraction(1, 5)  # CHOSE_CATEGORY_A_DIAGNOSTIC_CONTROL
D_VALUE = 0.0  # CHOSE_CATEGORY_A_DIAGNOSTIC_CONTROL
LAMBDA = 0.0  # CHOSE_CATEGORY_A_DIAGNOSTIC_CONTROL
J0 = 100.0  # CHOSE_CATEGORY_A_DIAGNOSTIC_CONTROL
MODES = (1, 2, 3, 4)  # FREE_AND_EXPLORED_CONTROL_FAMILY
SAMPLES = 16384  # CATEGORY_A_NUMERICAL_QUADRATURE
TWO_PI = 2.0 * math.pi

LANDING = (
    "G319_FREEDOM_NOT_PURE_REPRESENTATION__SCALE_FREE_INTRINSIC_CURVATURE_"
    "SEPARATES_LAWFUL_PROFILES__DECLARED_GAUGE_DUPLICATES_QUOTIENTED__"
    "NO_COMPLETE_MODULI_OR_PHYSICAL_DATA_SELECTION"
)


def check(label, condition):
    if not condition:
        raise AssertionError(label)
    CHECKS.append(label)


def mean(values):
    return math.fsum(values) / len(values)


def profile_jet(x_value, mode, phase=0.0, reflected=False, p=float(P), amplitude=float(A)):
    argument_x = -x_value if reflected else x_value
    argument = mode * (argument_x - phase)
    orientation = -1.0 if reflected else 1.0
    psi = p + amplitude * math.cos(argument)
    psi_prime = -amplitude * mode * math.sin(argument) * orientation
    psi_second = -amplitude * mode * mode * math.cos(argument)
    psi_third = amplitude * mode ** 3 * math.sin(argument) * orientation
    return psi, psi_prime, psi_second, psi_third


def reconstruct(psi, psi_prime, psi_second, psi_third, sign):
    f_value = 12.0 * psi_second * psi ** -5
    f_prime = 12.0 * (
        psi_third * psi ** -5 - 5.0 * psi_second * psi ** -6 * psi_prime
    )
    g_value = 36.0 * psi_prime ** 2
    g_prime = 72.0 * psi_prime * psi_second
    z_value = g_value + J0
    b_value = sign * psi ** -3 * math.sqrt(z_value)
    b_prime = b_value * (-3.0 * psi_prime / psi + g_prime / (2.0 * z_value))
    a_value = f_value / b_value
    a_prime = f_prime / b_value - f_value * b_prime / b_value ** 2
    tau = 0.5 * (a_value + b_value)
    lambda_value = 0.5 * (a_value - b_value)
    tau_prime = 0.5 * (a_prime + b_prime)
    lambda_prime = 0.5 * (a_prime - b_prime)
    kdiag = (
        (tau + 2.0 * lambda_value) / 3.0,
        (tau - lambda_value) / 3.0,
        (tau - lambda_value) / 3.0,
        )
    kdiag_prime = (
        (tau_prime + 2.0 * lambda_prime) / 3.0,
        (tau_prime - lambda_prime) / 3.0,
        (tau_prime - lambda_prime) / 3.0,
    )
    scalar_3 = -8.0 * psi ** -5 * psi_second
    hamiltonian = scalar_3 + tau ** 2 - math.fsum(item * item for item in kdiag)
    h_value = psi_prime / psi
    momentum = (
        kdiag_prime[0] - tau_prime + 6.0 * h_value * kdiag[0]
        - 2.0 * h_value * tau
    )
    j_value = psi ** 6 * b_value ** 2 - 36.0 * psi_prime ** 2
    return {
        "R3": scalar_3,
        "tau": tau,
        "K2": math.fsum(item * item for item in kdiag),
        "K3": math.fsum(item ** 3 for item in kdiag),
        "hamiltonian": hamiltonian,
        "momentum": momentum,
        "J": j_value,
        "B2": b_value ** 2,
        "B2_plus_F": b_value ** 2 + f_value,
    }


def summarize(mode, sign, phase=0.0, reflected=False):
    rows = []
    for index in range(SAMPLES):
        x_value = TWO_PI * index / SAMPLES
        jet = profile_jet(x_value, mode, phase=phase, reflected=reflected)
        psi = jet[0]
        physical = reconstruct(*jet, sign)
        weight = psi ** 6
        rows.append((psi, weight, physical))

    volume = TWO_PI ** 3 * mean([row[1] for row in rows])
    total_scalar = TWO_PI ** 3 * mean(
        [row[1] * row[2]["R3"] for row in rows]
    )
    q_scalar = total_scalar / volume ** (1.0 / 3.0)

    def weighted_average(key):
        numerator = mean([row[1] * row[2][key] for row in rows])
        denominator = mean([row[1] for row in rows])
        return numerator / denominator

    return {
        "mode": mode,
        "sign": sign,
        "phase": phase,
        "reflected": reflected,
        "volume": volume,
        "total_scalar": total_scalar,
        "Q_R": q_scalar,
        "weighted_tau": weighted_average("tau"),
        "weighted_K2": weighted_average("K2"),
        "weighted_K3": weighted_average("K3"),
        "min_psi": min(row[0] for row in rows),
        "min_signed_tau": min(sign * row[2]["tau"] for row in rows),
        "min_B2": min(row[2]["B2"] for row in rows),
        "min_B2_plus_F": min(row[2]["B2_plus_F"] for row in rows),
        "max_hamiltonian": max(abs(row[2]["hamiltonian"]) for row in rows),
        "max_momentum": max(abs(row[2]["momentum"]) for row in rows),
        "max_J_drift": max(abs(row[2]["J"] - J0) for row in rows),
    }


# Exact coefficient identities: no outcome sampling is used for the separator theorem.
p = P
a = A
average_psi6 = (
    p ** 6
    + Fraction(15, 2) * p ** 4 * a ** 2
    + Fraction(45, 8) * p ** 2 * a ** 4
    + Fraction(5, 16) * a ** 6
)
check("positive profile exact", p > abs(a))
check("positive volume coefficient exact", average_psi6 > 0)
for mode in MODES:
    integral_gradient_coefficient = Fraction(1, 2) * a ** 2 * mode ** 2
    check(f"gradient coefficient positive n={mode}", integral_gradient_coefficient > 0)
    check(
        f"mode-square scaling exact n={mode}",
        integral_gradient_coefficient
        == mode ** 2 * Fraction(1, 2) * a ** 2,
    )
    positivity_margin = Fraction(100) - 12 * a * mode ** 2 * (p + a)
    check(f"regular reconstruction bound n={mode}", positivity_margin > 0)


atlas = []
base_by_sign = {}
for mode in MODES:
    for sign in (-1, 1):
        summary = summarize(mode, sign)
        expected_volume = TWO_PI ** 3 * float(average_psi6)
        expected_scalar = 32.0 * math.pi ** 3 * float(a ** 2) * mode ** 2
        check(f"volume analytic n={mode} sign={sign}", abs(summary["volume"] - expected_volume) < 2e-11)
        check(f"scalar analytic n={mode} sign={sign}", abs(summary["total_scalar"] - expected_scalar) < 2e-10)
        check(f"psi positive n={mode} sign={sign}", summary["min_psi"] > 0)
        check(f"tau sign n={mode} sign={sign}", summary["min_signed_tau"] > 0)
        check(f"B2 positive n={mode} sign={sign}", summary["min_B2"] > 0)
        check(f"B2 plus F positive n={mode} sign={sign}", summary["min_B2_plus_F"] > 0)
        check(f"Hamiltonian n={mode} sign={sign}", summary["max_hamiltonian"] < 2e-12)
        check(f"momentum n={mode} sign={sign}", summary["max_momentum"] < 2e-12)
        check(f"J constant n={mode} sign={sign}", summary["max_J_drift"] < 2e-12)
        if mode == 1:
            base_by_sign[sign] = summary
        else:
            q_ratio = summary["Q_R"] / base_by_sign[sign]["Q_R"]
            check(f"Q mode-square ratio n={mode} sign={sign}", abs(q_ratio - mode ** 2) < 2e-12)
        atlas.append(summary)


# Explicit spatial-isometry controls: phase translations and reflections preserve every integral.
for mode in MODES:
    for sign in (-1, 1):
        baseline = next(row for row in atlas if row["mode"] == mode and row["sign"] == sign)
        for phase in (0.137, 0.511, 1.203):
            shifted = summarize(mode, sign, phase=phase)
            for key in ("volume", "total_scalar", "Q_R", "weighted_tau", "weighted_K2", "weighted_K3"):
                tolerance = 3e-11 * max(1.0, abs(baseline[key]))
                check(f"phase invariant {key} n={mode} sign={sign} phase={phase}", abs(shifted[key] - baseline[key]) < tolerance)
        reflected = summarize(mode, sign, reflected=True)
        for key in ("volume", "total_scalar", "Q_R", "weighted_tau", "weighted_K2", "weighted_K3"):
            tolerance = 3e-11 * max(1.0, abs(baseline[key]))
            check(f"reflection invariant {key} n={mode} sign={sign}", abs(reflected[key] - baseline[key]) < tolerance)


# Conformal-seed representation control: a nonconstant seed rewrite reconstructs the same gamma.
seed_max_error = 0.0
seed_max_physical_a_error = 0.0
raw_seed_difference = 0.0
for index in range(SAMPLES):
    x_value = TWO_PI * index / SAMPLES
    psi = profile_jet(x_value, 2)[0]
    theta = 1.0 + 0.1 * math.sin(3.0 * x_value)
    psi_hat = psi / theta
    bar_gamma_hat_factor = theta ** 4
    gamma_factor = psi ** 4
    gamma_hat_factor = psi_hat ** 4 * bar_gamma_hat_factor
    seed_max_error = max(seed_max_error, abs(gamma_hat_factor - gamma_factor))
    raw_seed_difference = max(raw_seed_difference, abs(psi_hat - psi))
    for bar_a in (2.0, -0.75, -1.25):
        physical_a = psi ** -10 * bar_a
        bar_a_hat = theta ** -10 * bar_a
        physical_a_hat = psi_hat ** -10 * bar_a_hat
        seed_max_physical_a_error = max(
            seed_max_physical_a_error, abs(physical_a_hat - physical_a)
        )
check("nontrivial seed rewrite", raw_seed_difference > 0.01)
check("seed rewrite reconstructs same gamma", seed_max_error < 4e-15)
check("seed rewrite reconstructs same physical A", seed_max_physical_a_error < 4e-15)


# Homothety control: numerator and denominator scale together, leaving Q_R fixed.
reference = base_by_sign[1]
for length_scale in (0.3, 2.0, 7.5):
    scaled_total_scalar = length_scale * reference["total_scalar"]
    scaled_volume = length_scale ** 3 * reference["volume"]
    scaled_q = scaled_total_scalar / scaled_volume ** (1.0 / 3.0)
    check(f"homothety-neutral Q scale={length_scale}", abs(scaled_q - reference["Q_R"]) < 2e-13)


with (HERE / "INVARIANT_ATLAS.tsv").open("w", encoding="utf-8", newline="") as handle:
    fieldnames = tuple(atlas[0].keys())
    writer = csv.DictWriter(handle, fieldnames=fieldnames, delimiter="\t", lineterminator="\n")
    writer.writeheader()
    writer.writerows(atlas)


result = {
    "schema": "udt-g320-physical-initial-geometry-quotient-v1",
    "status": "PASS_PENDING_EXTERNAL_REVIEW",
    "landing": LANDING,
    "assertion_count": len(CHECKS),
    "analytic_family": "psi_n=3/2+(1/5)cos(nx)",
    "modes_checked": list(MODES),
    "branches_checked": [-1, 1],
    "same_volume_all_modes": True,
    "Q_R_mode_scaling": "n^2",
    "intrinsic_physical_inequivalence": True,
    "countably_infinite_physical_directions_in_registered_family": True,
    "every_distinct_profile_proven_inequivalent": False,
    "phase_reflection_controls_pass": True,
    "conformal_seed_full_data_duplicate_control_pass": True,
    "seed_rewrite_max_metric_error": seed_max_error,
    "seed_rewrite_max_physical_A_error": seed_max_physical_a_error,
    "complete_moduli_classification": False,
    "physical_data_selected": False,
    "history_selected": False,
    "scale_selected": False,
    "Xmax_selected": False,
    "metric_changed": False,
    "kernel_changed": False,
    "checks": CHECKS,
}
(HERE / "DERIVATION_RESULT.json").write_text(
    json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
)
print(json.dumps({
    "status": result["status"],
    "landing": LANDING,
    "assertions": len(CHECKS),
    "modes": list(MODES),
    "branches": [-1, 1],
    "seed_rewrite_max_metric_error": seed_max_error,
    "seed_rewrite_max_physical_A_error": seed_max_physical_a_error,
}, indent=2))
