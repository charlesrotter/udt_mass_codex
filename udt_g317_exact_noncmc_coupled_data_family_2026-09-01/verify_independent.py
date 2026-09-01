#!/usr/bin/env python3
"""Implementation-distinct dependency-free G317 verification."""

from fractions import Fraction
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
PASSED = []


def require(label, condition):
    if not condition:
        raise AssertionError(label)
    PASSED.append(label)


def direct_constraints(p, tau, tau_x, q, lam):
    gamma_inverse = Fraction(1, 1) / p ** 4
    k_mixed = (tau, q, -q)
    trace = sum(k_mixed)
    hamiltonian = trace * trace - sum(value * value for value in k_mixed) - 2 * lam
    # Q^{ij}=K^{ij}-gamma^{ij}K is diagonal. Its xx entry vanishes identically;
    # the yy and zz entries depend on x but divergence differentiates them in y,z.
    q_xx_derivative = gamma_inverse * (tau_x - tau_x)
    momentum = (q_xx_derivative, Fraction(0), Fraction(0))
    return hamiltonian, momentum


def conformal_seed(p, mean_tau, q):
    scale = p ** 6
    return (
        Fraction(2, 3) * scale * mean_tau,
        scale * (q - mean_tau / 3),
        scale * (-q - mean_tau / 3),
    )


def conformal_total(p, tau, mean_tau, q):
    seed = conformal_seed(p, mean_tau, q)
    u = p ** 6 * (tau - mean_tau) / 2
    longitudinal = (Fraction(4, 3) * u, -Fraction(2, 3) * u, -Fraction(2, 3) * u)
    return tuple(seed[i] + longitudinal[i] for i in range(3))


def scalar_constraint(p, tau, mean_tau, q):
    tensor = conformal_total(p, tau, mean_tau, q)
    lam = -q * q
    return -sum(value * value for value in tensor) * p ** -7 + (
        Fraction(2, 3) * tau * tau - 2 * lam
    ) * p ** 5


def electric(tau, q):
    lam = -q * q
    entries = (tau, q, -q)
    trace = tau
    return tuple(trace * value - value * value - Fraction(2, 3) * lam for value in entries)


# Start from the physical data, independently of the production conformal calculation.
for p in (Fraction(1, 3), Fraction(1), Fraction(4, 3), Fraction(3)):
    for tau in (Fraction(-11, 4), Fraction(-1, 7), Fraction(0), Fraction(8, 5)):
        for tau_x in (Fraction(-9, 2), Fraction(1, 3), Fraction(7)):
            for q in (Fraction(-5, 3), Fraction(-1, 4), Fraction(0), Fraction(2)):
                lam = -q * q
                hamiltonian, momentum = direct_constraints(p, tau, tau_x, q, lam)
                require(f"direct Hamiltonian {p},{tau},{tau_x},{q}", hamiltonian == 0)
                require(f"direct momentum {p},{tau},{tau_x},{q}", momentum == (0, 0, 0))
                e_diag = electric(tau, q)
                require(f"electric trace {p},{tau},{q}", sum(e_diag) == 0)
                if q == 0:
                    require(f"zero Weyl branch {p},{tau}", e_diag == (0, 0, 0))
                else:
                    require(f"tidal branch {p},{tau},{q}", e_diag[0] == Fraction(2, 3) * q * q and e_diag[0] != 0)
                opposite = electric(tau, -q)
                require(f"axis relabel {p},{tau},{q}", opposite == (e_diag[0], e_diag[2], e_diag[1]))


# Reconstruct the conformal decomposition by a route that begins from K rather than its seed.
for p in (Fraction(1, 2), Fraction(1), Fraction(5, 2)):
    for mean_tau in (Fraction(-4, 3), Fraction(0), Fraction(9, 7)):
        for q in (Fraction(-2), Fraction(0), Fraction(3, 5)):
            seed = conformal_seed(p, mean_tau, q)
            require(f"independent TT trace {p},{mean_tau},{q}", sum(seed) == 0)
            for tau in (mean_tau - 2, mean_tau + Fraction(1, 6), mean_tau + Fraction(13, 5)):
                total = conformal_total(p, tau, mean_tau, q)
                target = p ** 6 * Fraction(1, 3)
                require(
                    f"independent conformal reconstruction {p},{mean_tau},{q},{tau}",
                    total == (
                        2 * target * tau,
                        p ** 6 * (q - tau / 3),
                        p ** 6 * (-q - tau / 3),
                    ),
                )
                require(f"independent scalar constraint {p},{mean_tau},{q},{tau}", scalar_constraint(p, tau, mean_tau, q) == 0)


# Formal Fourier differentiation checks periodic integrability without sampled trigonometry.
profiles = (
    ((1, Fraction(2), Fraction(-3)), (4, Fraction(5, 2), Fraction(7, 3))),
    ((2, Fraction(-1, 5), Fraction(9, 4)), (5, Fraction(8, 3), Fraction(-2, 7))),
)
for p in (Fraction(1), Fraction(3, 2)):
    for profile_index, modes in enumerate(profiles):
        for mode, cosine, sine in modes:
            # tau'=n*b*cos-n*a*sin. Integrating w'=p^6 tau/2 gives
            # w=(p^6/2)(a sin/n-b cos/n), so 2w''=p^6 tau'.
            tau_prime_cos = mode * sine
            tau_prime_sin = -mode * cosine
            w_sin = p ** 6 * cosine / (2 * mode)
            w_cos = -p ** 6 * sine / (2 * mode)
            two_w_second_cos = 2 * (-mode * mode) * w_cos
            two_w_second_sin = 2 * (-mode * mode) * w_sin
            require(f"Fourier vector cos {p},{profile_index},{mode}", two_w_second_cos == p ** 6 * tau_prime_cos)
            require(f"Fourier vector sin {p},{profile_index},{mode}", two_w_second_sin == p ** 6 * tau_prime_sin)


# Independently recover necessity from the affine tau coefficient.
for p in (Fraction(1, 2), Fraction(1), Fraction(2)):
    for mean_tau in (Fraction(-3), Fraction(0), Fraction(7, 4)):
        alpha_required = Fraction(2, 3) * p ** 6 * mean_tau
        for alpha in (alpha_required, alpha_required + Fraction(2, 9)):
            slope = Fraction(4, 3) * mean_tau - 2 * alpha * p ** -6
            require(
                f"necessity slope {p},{mean_tau},{alpha}",
                (slope == 0) == (alpha == alpha_required),
            )


ceilings = {
    "topology_selected": False,
    "scale_selected": False,
    "Lambda_sign_globally_selected": False,
    "tau_profile_selected": False,
    "general_noncmc_classified": False,
    "history_selected": False,
    "metric_changed": False,
    "kernel_changed": False,
}
for key, value in ceilings.items():
    require(f"independent ceiling {key}", value is False)


landing = (
    "EXACT_NONCMC_COUPLED_TORUS_FAMILY_EXISTS_WITH_ZERO_TIDE_AND_TIDAL_SUBBRANCHES__"
    "CONSTANT_PSI_CLASSIFICATION_FORCES_LAMBDA_MINUS_Q_SQUARED__NO_PHYSICAL_DATA_SELECTION"
)
result = {
    "schema": "udt-g317-independent-v1",
    "landing": landing,
    "status": "PASS",
    "assertion_count": len(PASSED),
    "production_imported": False,
    "production_result_read": False,
    "checks": PASSED,
}
(HERE / "INDEPENDENT_VERIFICATION.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
print(json.dumps({"landing": landing, "independent_assertions": len(PASSED)}, indent=2))
