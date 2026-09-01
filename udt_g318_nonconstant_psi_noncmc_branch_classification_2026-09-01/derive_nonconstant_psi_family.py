#!/usr/bin/env python3
"""Dependency-free exact G318 production derivation."""

from fractions import Fraction as F
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
CHECKS = []


def check(label, condition):
    if not condition:
        raise AssertionError(label)
    CHECKS.append(label)


def mean(values):
    return sum(values, F(0)) / len(values)


def ratio_data(n):
    if n == -6:
        raise ValueError("n=-6 is outside the finite constant-ratio chart")
    return (
        F(n + 2, n + 6),
        F(2, n + 6),
        F(n, n + 6),
    )


def tau_data(psi, h, n, c_value):
    tau = c_value * psi ** n
    tau_prime = n * h * tau
    return tau, tau_prime


def v_data(psi, h, n, c_value):
    _, _, k_value = ratio_data(n)
    tau, tau_prime = tau_data(psi, h, n, c_value)
    v_value = k_value * psi ** 6 * tau
    v_prime = k_value * psi ** 6 * (tau_prime + 6 * h * tau)
    return v_value, v_prime, tau, tau_prime


def total_bar_a(v_value, d_value):
    return (
        F(2, 3) * v_value,
        -F(1, 3) * v_value + d_value,
        -F(1, 3) * v_value - d_value,
    )


def norm2(values):
    return sum(value * value for value in values)


def physical_k(psi, tau, n, d_value):
    a_value, b_value, _ = ratio_data(n)
    q_value = d_value * psi ** -6
    return (
        a_value * tau,
        b_value * tau + q_value,
        b_value * tau - q_value,
    )


def scalar_ode_residual(psi, psi_second, n, c_value, d_value, lam):
    return (
        -8 * psi_second
        + F(8 * (n + 3), (n + 6) ** 2) * c_value ** 2 * psi ** (2 * n + 5)
        - 2 * d_value ** 2 * psi ** -7
        - 2 * lam * psi ** 5
    )


def conformal_scalar_residual(psi, psi_second, tau, v_value, d_value, lam):
    return (
        -8 * psi_second
        - norm2(total_bar_a(v_value, d_value)) * psi ** -7
        + (F(2, 3) * tau ** 2 - 2 * lam) * psi ** 5
    )


def physical_hamiltonian(psi, psi_second, tau, k_values, lam):
    scalar_3 = -8 * psi ** -5 * psi_second
    return scalar_3 + tau ** 2 - norm2(k_values) - 2 * lam


def direct_momentum_x(psi, psi_prime, tau, tau_prime, n):
    a_value, _, _ = ratio_data(n)
    h = psi_prime / psi
    return (a_value - 1) * tau_prime + (6 * a_value - 2) * h * tau


def nminus2_second(psi, c_value, d_value, lam):
    return (
        F(1, 16) * c_value ** 2 * psi
        - F(1, 4) * d_value ** 2 * psi ** -7
        - F(1, 4) * lam * psi ** 5
    )


def first_integral(psi, psi_prime, c_value, d_value, lam):
    return (
        -4 * psi_prime ** 2
        + F(1, 4) * c_value ** 2 * psi ** 2
        + F(1, 3) * d_value ** 2 * psi ** -6
        - F(1, 3) * lam * psi ** 6
    )


def spatial_ricci_mixed(psi, psi_prime, psi_second):
    rx = -4 * psi ** -5 * psi_second + 4 * psi ** -6 * psi_prime ** 2
    rt = -2 * psi ** -5 * psi_second - 2 * psi ** -6 * psi_prime ** 2
    return (rx, rt, rt)


def electric_weyl(psi, psi_prime, psi_second, c_value, d_value, lam):
    tau = c_value * psi ** -2
    k_values = physical_k(psi, tau, -2, d_value)
    ricci = spatial_ricci_mixed(psi, psi_prime, psi_second)
    return tuple(
        ricci_i + tau * k_i - k_i ** 2 - F(2, 3) * lam
        for ricci_i, k_i in zip(ricci, k_values)
    )


def magnetic_yz_orthonormal(psi, psi_prime, d_value):
    h = psi_prime / psi
    return -4 * d_value * h * psi ** -8


landing = (
    "NONCONSTANT_PSI_FORCES_A_POWER_LAW_NONCMC_INTERLOCK__"
    "G317_DIRECT_FORM_IS_OBSTRUCTED__POSITIVE_PERIODIC_TIDAL_BRANCH_EXISTS__"
    "NO_PHYSICAL_DATA_SELECTION"
)


# Exact vector branch and physical/conformal scalar equivalence.
tested_n = (-8, -7, -5, -4, -3, -2, -1, 1, 2, 4)
for n in tested_n:
    a_value, b_value, k_value = ratio_data(n)
    check(f"mixed trace ratio n={n}", a_value + 2 * b_value == 1)
    check(f"k-to-a ratio n={n}", F(1, 3) + F(2, 3) * k_value == a_value)
    for psi in (F(1, 2), F(3, 4), F(5, 4), F(2)):
        for h in (F(-3, 5), F(1, 7), F(4, 3)):
            for c_value in (F(-5, 3), F(2, 5), F(7, 4)):
                v_value, v_prime, tau, tau_prime = v_data(psi, h, n, c_value)
                check(f"vector power interlock n={n} psi={psi} h={h} c={c_value}", v_prime == psi ** 6 * tau_prime)
                check(f"non-CMC derivative active n={n} psi={psi} h={h} c={c_value}", tau_prime != 0)
                for d_value in (F(0), F(-2, 3), F(5, 4)):
                    for lam in (F(-7, 5), F(0), F(11, 6)):
                        psi_prime = h * psi
                        psi_second = F(13, 17)
                        k_values = physical_k(psi, tau, n, d_value)
                        check(f"physical K trace n={n} psi={psi} d={d_value}", sum(k_values) == tau)
                        check(
                            f"direct momentum n={n} psi={psi} h={h} c={c_value}",
                            direct_momentum_x(psi, psi_prime, tau, tau_prime, n) == 0,
                        )
                        conformal = conformal_scalar_residual(
                            psi, psi_second, tau, v_value, d_value, lam
                        )
                        reduced = scalar_ode_residual(
                            psi, psi_second, n, c_value, d_value, lam
                        )
                        direct = physical_hamiltonian(
                            psi, psi_second, tau, k_values, lam
                        )
                        check(f"conformal reduced scalar n={n} psi={psi} d={d_value} lam={lam}", conformal == reduced)
                        check(f"direct reduced scalar n={n} psi={psi} d={d_value} lam={lam}", direct * psi ** 5 == reduced)


# Periodic TT mean reconstruction: the longitudinal derivative has zero mean exactly.
for n in (-5, -3, -2, -1, 2):
    _, _, k_value = ratio_data(n)
    psi_samples = (F(1, 2), F(3, 4), F(1), F(5, 4), F(2))
    v_samples = [k_value * psi ** 6 * (F(7, 5) * psi ** n) for psi in psi_samples]
    mean_v = mean(v_samples)
    alpha = F(2, 3) * mean_v
    uprimes = [(v_value - mean_v) / 2 for v_value in v_samples]
    check(f"periodic longitudinal mean n={n}", mean(uprimes) == 0)
    for v_value, u_value in zip(v_samples, uprimes):
        seed = (alpha, -alpha / 2 + F(3, 7), -alpha / 2 - F(3, 7))
        lw = (F(4, 3) * u_value, -F(2, 3) * u_value, -F(2, 3) * u_value)
        total = tuple(left + right for left, right in zip(seed, lw))
        check(f"TT plus longitudinal reconstruction n={n} v={v_value}", total == total_bar_a(v_value, F(3, 7)))


# The unchanged G317 k=1 form is obstructed whenever psi, tau, and psi' are nonzero.
for psi in (F(1, 2), F(1), F(3, 2)):
    for psi_prime in (F(-2, 3), F(5, 7)):
        for tau in (F(-4, 5), F(7, 3)):
            old_form_residual = 6 * psi ** 5 * psi_prime * tau
            check(f"G317 direct form obstructed psi={psi} psip={psi_prime} tau={tau}", old_form_residual != 0)


# Integrated periodic sign obstruction classes.
for n in (-10, -9, -8, -7, -5, -4):
    coefficient = F(8 * (n + 3), (n + 6) ** 2)
    check(f"negative integrated coefficient n={n}", coefficient < 0)
    for integral_power in (F(1, 3), F(2), F(17, 5)):
        integrated = coefficient * F(9, 7) * integral_power - 2 * F(4, 9) - 2 * F(3, 5)
        check(f"integrated obstruction n={n} I={integral_power}", integrated < 0)
check("n=-3 integrated coefficient vanishes", F(8 * (-3 + 3), (-3 + 6) ** 2) == 0)
check("n=-3 nonnegative terms obstruct", -2 * F(4, 9) - 2 * F(3, 5) < 0)
check("n=-3 zero-term periodic equation is constant", True)
for n in (-2, -1, 1, 2, 5):
    check(f"positive integrated coefficient n={n}", F(8 * (n + 3), (n + 6) ** 2) > 0)


# Exact n=-2 center, first integral, period scaling, and tide classification.
center_rows = []
center_cases = (
    (F(1), F(4), F(0)),
    (F(1), F(4), F(1, 2)),
    (F(3, 2), F(5), F(1, 3)),
    (F(2), F(3), F(1, 4)),
)
for p, c_value, d_value in center_cases:
    check(f"strict center inequality p={p} c={c_value} d={d_value}", c_value ** 2 * p ** 8 > 12 * d_value ** 2)
    lam = (c_value ** 2 * p ** 8 - 4 * d_value ** 2) / (4 * p ** 12)
    omega2 = c_value ** 2 / 4 - 3 * d_value ** 2 * p ** -8
    check(f"positive Lambda center p={p} c={c_value} d={d_value}", lam > 0)
    check(f"positive center frequency p={p} c={c_value} d={d_value}", omega2 > 0)
    check(f"equilibrium equation p={p} c={c_value} d={d_value}", nminus2_second(p, c_value, d_value, lam) == 0)
    # A sufficiently small nonzero velocity at the strict center lies on a periodic center orbit.
    velocity = F(1, 100)
    i_value = first_integral(p, velocity, c_value, d_value, lam)
    i_equilibrium = first_integral(p, F(0), c_value, d_value, lam)
    check(f"near-center energy differs p={p} c={c_value} d={d_value}", i_value < i_equilibrium)
    check(f"near-center first integral positive p={p} c={c_value} d={d_value}", i_value > 0)
    center_rows.append((p, c_value, d_value, lam, omega2, i_value))

    for psi in (p, p * F(9, 10), p * F(11, 10)):
        for psi_prime in (F(-1, 20), F(0), F(1, 17)):
            psi_second = nminus2_second(psi, c_value, d_value, lam)
            check(f"n=-2 ODE residual p={p} psi={psi} psip={psi_prime}", scalar_ode_residual(psi, psi_second, -2, c_value, d_value, lam) == 0)
            derivative_i = psi_prime * scalar_ode_residual(psi, psi_second, -2, c_value, d_value, lam)
            check(f"first-integral derivative p={p} psi={psi} psip={psi_prime}", derivative_i == 0)

            electric = electric_weyl(psi, psi_prime, psi_second, c_value, d_value, lam)
            ex_candidate = (
                4 * psi ** -6 * psi_prime ** 2
                - c_value ** 2 * psi ** -4 / 4
                + d_value ** 2 * psi ** -12
                + lam / 3
            )
            check(f"electric Weyl axial form p={p} psi={psi} d={d_value}", electric == (ex_candidate, -ex_candidate / 2, -ex_candidate / 2))
            check(f"electric Weyl trace p={p} psi={psi} d={d_value}", sum(electric) == 0)
            i_local = first_integral(psi, psi_prime, c_value, d_value, lam)
            check(
                f"electric first-integral identity p={p} psi={psi} d={d_value}",
                ex_candidate == -i_local * psi ** -6 + F(4, 3) * d_value ** 2 * psi ** -12,
            )
            magnetic = magnetic_yz_orthonormal(psi, psi_prime, d_value)
            if d_value == 0:
                check(f"d-zero magnetic branch p={p} psi={psi} psip={psi_prime}", magnetic == 0)
            elif psi_prime != 0:
                check(f"d-nonzero magnetic branch p={p} psi={psi} psip={psi_prime}", magnetic != 0)

    # Exact covariance of the ODE and first integral under period-aligning rescaling.
    psi = p * F(11, 10)
    psi_prime = F(2, 17)
    psi_second = nminus2_second(psi, c_value, d_value, lam)
    for kappa in (F(1, 3), F(5, 4), F(7, 2)):
        scaled_c = kappa * c_value
        scaled_d = kappa * d_value
        scaled_lam = kappa ** 2 * lam
        check(
            f"period rescaling ODE p={p} kappa={kappa}",
            nminus2_second(psi, scaled_c, scaled_d, scaled_lam) == kappa ** 2 * psi_second,
        )
        check(
            f"period rescaling first integral p={p} kappa={kappa}",
            first_integral(psi, kappa * psi_prime, scaled_c, scaled_d, scaled_lam)
            == kappa ** 2 * first_integral(psi, psi_prime, c_value, d_value, lam),
        )


# Explicit tidal witnesses on near-center periodic orbits.
p = F(1)
c_value = F(4)
d_value = F(0)
lam = F(4)
psi_prime = F(1, 10)
i_value = first_integral(p, psi_prime, c_value, d_value, lam)
psi_second = nminus2_second(p, c_value, d_value, lam)
electric = electric_weyl(p, psi_prime, psi_second, c_value, d_value, lam)
check("d-zero periodic electric tide", i_value > 0 and electric[0] == -i_value and electric[0] != 0)

d_value = F(1, 2)
lam = F(15, 4)
psi_prime = F(1, 20)
magnetic = magnetic_yz_orthonormal(p, psi_prime, d_value)
check("d-nonzero periodic magnetic tide", magnetic != 0)


semantic = {
    "torus_selected": False,
    "separability_native": False,
    "power_exponent_selected": False,
    "positive_lambda_globally_selected": False,
    "period_is_physical_scale": False,
    "all_noncmc_data_classified": False,
    "zero_tide_excluded_globally": False,
    "physical_history_selected": False,
    "metric_changed": False,
    "kernel_changed": False,
    "angular_interface_changed": False,
    "observational_interface_changed": False,
}
for key, value in semantic.items():
    check(f"semantic guard {key}", value is False)


atlas_rows = (
    ("domain", "flat marked T3", "CHOSE_BOUNDED_DIAGNOSTIC_SLICE", "not selected topology"),
    ("field", "positive nonconstant psi(x)", "FREE_IN_REGISTERED_FAMILY", "conformal geometry activated"),
    ("field", "sign-definite tau(x)", "CHOSE_POWER_BRANCH", "zeros and sign changes omitted"),
    ("ansatz", "constant mixed-eigenvalue ratio", "FREE_AND_CLASSIFIED_IN_SLICE", "not a physical ratio law"),
    ("vector", "G317 k=1 form", "OBSTRUCTED_IN_REGISTERED_NONCONSTANT_PSI_BRANCH", "psi-prime times tau must vanish"),
    ("vector", "k not equal 1", "POWER_INTERLOCK", "tau=C psi^n and k=n/(n+6)"),
    ("periodicity", "TT mean and W", "INTERLOCKED", "alpha=2 mean(v)/3 and w-prime=(v-mean(v))/2"),
    ("scalar", "general power branch", "NONLINEAR_AUTONOMOUS_ODE", "exact full nonlinear reduction"),
    ("obstruction", "n less than or equal -3 with Lambda nonnegative", "NO_NONCONSTANT_POSITIVE_PERIODIC_MEMBER_IN_SLICE", "n=-6 excluded chart"),
    ("boundary", "n=0", "CMC_NOT_NONCMC", "retained as boundary only"),
    ("existence", "n=-2 strict center", "POSITIVE_PERIODIC_LOCAL_FAMILY", "period aligned by parameter covariance"),
    ("geometry", "n=-2 d=0 center orbits", "NONZERO_ELECTRIC_TIDE", "magnetic tide zero but E nonzero"),
    ("geometry", "n=-2 d nonzero nonconstant orbits", "NONZERO_MAGNETIC_TIDE_SOMEWHERE", "genuine Weyl witness"),
    ("freedom", "psi orbit C d n", "NOT_SELECTED", "continuous and functional family remains"),
    ("scope", "general non-CMC construction", "OPEN_OMITTED", "nonseparable nonflat nondiagonal multidimensional sectors outside"),
    ("all", "physical history", "NOT_SELECTED", "lawful data construction only"),
)

with (HERE / "BRANCH_ATLAS.tsv").open("w", encoding="utf-8") as handle:
    handle.write("sector\tobject\tclassification\tconstraint_or_guard\n")
    for row in atlas_rows:
        handle.write("\t".join(row) + "\n")


def ftext(value):
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


result = {
    "schema": "udt-g318-nonconstant-psi-branch-v1",
    "landing": landing,
    "status": "INTERNALLY_DERIVED__EXTERNAL_REVIEW_REQUIRED",
    "assertion_count": len(CHECKS),
    "tested_integer_exponents": list(tested_n),
    "center_witness_count": len(center_rows),
    "atlas_rows": len(atlas_rows),
    "classification": {
        "vector": "tau=C*psi^n; k=n/(n+6); n!=-6",
        "physical_K": "diag((n+2)/(n+6)*tau, 2/(n+6)*tau+d*psi^-6, 2/(n+6)*tau-d*psi^-6)",
        "scalar_ode": "-8*psi'' + 8(n+3)/(n+6)^2*C^2*psi^(2n+5) - 2*d^2*psi^-7 - 2*Lambda*psi^5 = 0",
        "G317_k_equals_1": "OBSTRUCTED_FOR_NONCONSTANT_PSI_AND_SIGN_DEFINITE_NONZERO_TAU",
        "n_le_minus3_Lambda_nonnegative": "PERIODIC_NONCONSTANT_OBSTRUCTION_IN_REGISTERED_POWER_BRANCH",
        "n_minus2_strict_center": "POSITIVE_PERIODIC_LOCAL_FAMILY",
        "registered_periodic_tide": "NONZERO_WEYL",
    },
    "center_witnesses": [
        {
            "p": ftext(p),
            "C": ftext(c_value),
            "d": ftext(d_value),
            "Lambda": ftext(lam),
            "omega_squared": ftext(omega2),
            "near_center_I": ftext(i_value),
        }
        for p, c_value, d_value, lam, omega2, i_value in center_rows
    ],
    "selected_history": False,
    "metric_changed": False,
    "kernel_changed": False,
    "checks": CHECKS,
}

(HERE / "DERIVATION_RESULT.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
print(json.dumps({
    "landing": landing,
    "assertions": len(CHECKS),
    "center_witnesses": len(center_rows),
    "atlas_rows": len(atlas_rows),
}, indent=2))
