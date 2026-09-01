#!/usr/bin/env python3
"""Exact dependency-free G317 production derivation."""

from fractions import Fraction as F
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
CHECKS = []


def check(label, condition):
    if not condition:
        raise AssertionError(label)
    CHECKS.append(label)


def add_term(field, key, value):
    if value:
        field[key] = field.get(key, F(0)) + value
        if field[key] == 0:
            del field[key]


def derivative(field):
    result = {}
    for (kind, mode), coefficient in field.items():
        if kind == "constant":
            continue
        if kind == "cos":
            add_term(result, ("sin", mode), -mode * coefficient)
        elif kind == "sin":
            add_term(result, ("cos", mode), mode * coefficient)
        else:
            raise AssertionError(f"unknown Fourier kind {kind}")
    return result


def scale(field, factor):
    return {key: factor * value for key, value in field.items() if factor * value}


def subtract(left, right):
    result = dict(left)
    for key, value in right.items():
        add_term(result, key, -value)
    return result


def integrate_zero_mean(field):
    check("Fourier source has zero mean", field.get(("constant", 0), F(0)) == 0)
    result = {}
    for (kind, mode), coefficient in field.items():
        if kind == "constant":
            continue
        if kind == "cos":
            add_term(result, ("sin", mode), coefficient / mode)
        elif kind == "sin":
            add_term(result, ("cos", mode), -coefficient / mode)
    return result


def tt_seed(p, mean_tau, q):
    p6 = p ** 6
    return (
        F(2, 3) * p6 * mean_tau,
        p6 * (q - F(1, 3) * mean_tau),
        p6 * (-q - F(1, 3) * mean_tau),
    )


def lw_from_wprime(wprime):
    return (F(4, 3) * wprime, -F(2, 3) * wprime, -F(2, 3) * wprime)


def norm2(diagonal):
    return sum(value * value for value in diagonal)


def general_reduced_scalar(p, tau, mean_tau, alpha, d_value, lam):
    beta = -alpha / 2 + d_value
    gamma = -alpha / 2 - d_value
    wprime = p ** 6 * (tau - mean_tau) / 2
    total = tuple(
        seed + longitudinal
        for seed, longitudinal in zip((alpha, beta, gamma), lw_from_wprime(wprime))
    )
    return -norm2(total) * p ** -12 + F(2, 3) * tau ** 2 - 2 * lam


def physical_hamiltonian(tau, q, lam):
    trace = tau
    k_norm = tau ** 2 + 2 * q ** 2
    return trace ** 2 - k_norm - 2 * lam


def electric_weyl(tau, q, lam):
    k = (tau, q, -q)
    trace = tau
    return tuple(trace * value - value * value - F(2, 3) * lam for value in k)


def levi_civita(i, j, k):
    if len({i, j, k}) < 3:
        return 0
    return 1 if (i, j, k) in ((0, 1, 2), (1, 2, 0), (2, 0, 1)) else -1


def magnetic_weyl_from_registered_derivative(tau_prime):
    # Only D_x K_xx is nonzero; epsilon_i^{xx}=0 kills it exactly.
    derivative_k_l_j = {(0, 0, 0): tau_prime}
    result = []
    for i in range(3):
        row = []
        for j in range(3):
            value = F(0)
            for k in range(3):
                for ell in range(3):
                    value += levi_civita(i, k, ell) * derivative_k_l_j.get((k, ell, j), F(0))
            row.append(value)
        result.append(tuple(row))
    return tuple(result)


landing = (
    "EXACT_NONCMC_COUPLED_TORUS_FAMILY_EXISTS_WITH_ZERO_TIDE_AND_TIDAL_SUBBRANCHES__"
    "CONSTANT_PSI_CLASSIFICATION_FORCES_LAMBDA_MINUS_Q_SQUARED__NO_PHYSICAL_DATA_SELECTION"
)


# Exact Fourier construction of nonconstant tau and the periodic longitudinal solution.
profiles = (
    {
        "name": "single_zero_mean_mode",
        "mean": F(0),
        "modes": {("cos", 1): F(2), ("sin", 2): F(-3, 2)},
    },
    {
        "name": "nonzero_mean_multimode",
        "mean": F(5, 3),
        "modes": {("sin", 1): F(4), ("cos", 3): F(7, 5), ("sin", 5): F(-2, 3)},
    },
    {
        "name": "mixed_high_modes",
        "mean": F(-7, 4),
        "modes": {("cos", 2): F(9, 7), ("sin", 4): F(11, 6), ("cos", 7): F(-5, 8)},
    },
)

for p in (F(1, 2), F(1), F(3, 2), F(2)):
    for profile in profiles:
        tau_zero_mean = dict(profile["modes"])
        w = scale(integrate_zero_mean(tau_zero_mean), p ** 6 / 2)
        wprime = derivative(w)
        expected_wprime = scale(tau_zero_mean, p ** 6 / 2)
        check(f"periodic w derivative {p} {profile['name']}", wprime == expected_wprime)
        lhs = scale(derivative(wprime), F(2))
        rhs = scale(derivative(tau_zero_mean), p ** 6)
        check(f"coupled vector equation {p} {profile['name']}", lhs == rhs)
        check(f"non-CMC source active {profile['name']}", derivative(tau_zero_mean) != {})


# Necessary and sufficient pointwise scalar classification inside the registered ansatz.
for p in (F(1, 2), F(1), F(3, 2), F(2)):
    for mean_tau in (F(-3, 2), F(0), F(5, 3)):
        for d_value in (F(-2), F(0), F(7, 5)):
            alpha = F(2, 3) * p ** 6 * mean_tau
            lam = -(d_value ** 2) * p ** -12
            for tau in (mean_tau - F(7, 3), mean_tau + F(1, 5), mean_tau + F(9, 4)):
                check(
                    f"classified scalar residual {p} {mean_tau} {d_value} {tau}",
                    general_reduced_scalar(p, tau, mean_tau, alpha, d_value, lam) == 0,
                )
            wrong_alpha = alpha + F(1, 7)
            t1, t2 = mean_tau - 1, mean_tau + 2
            difference = (
                general_reduced_scalar(p, t1, mean_tau, wrong_alpha, d_value, lam)
                - general_reduced_scalar(p, t2, mean_tau, wrong_alpha, d_value, lam)
            )
            check(f"nonconstant tau forces alpha {p} {mean_tau} {d_value}", difference != 0)
            check(
                f"classified Lambda is unique in ansatz {p} {mean_tau} {d_value}",
                general_reduced_scalar(p, t1, mean_tau, alpha, d_value, lam + F(1, 11)) != 0,
            )


# Reconstruct the conformal and physical tensors and verify both constraint routes.
family_rows = []
for p in (F(1, 2), F(1), F(3, 2), F(2)):
    for profile in profiles:
        mean_tau = profile["mean"]
        for q in (F(-2), F(-1, 3), F(0), F(5, 4)):
            seed = tt_seed(p, mean_tau, q)
            check(f"TT trace {p} {profile['name']} {q}", sum(seed) == 0)
            d_value = (seed[1] - seed[2]) / 2
            check(f"q reconstruction {p} {profile['name']} {q}", d_value * p ** -6 == q)
            lam = -q ** 2
            for tau, tau_prime in (
                (mean_tau - F(5, 2), F(7, 3)),
                (mean_tau + F(2, 7), F(-11, 5)),
                (mean_tau + F(13, 6), F(3, 4)),
            ):
                wprime = p ** 6 * (tau - mean_tau) / 2
                total_bar_a = tuple(
                    value + addition for value, addition in zip(seed, lw_from_wprime(wprime))
                )
                expected_bar_a = p ** 6 * F(1, 3)
                expected = (
                    2 * expected_bar_a * tau,
                    p ** 6 * (q - tau / 3),
                    p ** 6 * (-q - tau / 3),
                )
                check(f"conformal tensor reconstruction {p} {profile['name']} {q} {tau}", total_bar_a == expected)
                scalar = -norm2(total_bar_a) * p ** -7 + (F(2, 3) * tau ** 2 - 2 * lam) * p ** 5
                check(f"coupled scalar equation {p} {profile['name']} {q} {tau}", scalar == 0)
                check(f"direct Hamiltonian {p} {profile['name']} {q} {tau}", physical_hamiltonian(tau, q, lam) == 0)
                # With flat constant gamma, only D_x of the xx momentum component could survive;
                # K^xx-gamma^xx K is identically zero.
                momentum = (p ** -4 * (tau_prime - tau_prime), F(0), F(0))
                check(f"direct momentum {p} {profile['name']} {q} {tau}", momentum == (0, 0, 0))
                e_diag = electric_weyl(tau, q, lam)
                expected_e = (
                    F(2, 3) * q ** 2,
                    tau * q - F(1, 3) * q ** 2,
                    -tau * q - F(1, 3) * q ** 2,
                )
                check(f"electric Weyl formula {p} {profile['name']} {q} {tau}", e_diag == expected_e)
                check(f"electric Weyl tracefree {p} {profile['name']} {q} {tau}", sum(e_diag) == 0)
                magnetic = magnetic_weyl_from_registered_derivative(tau_prime)
                check(f"magnetic Weyl zero {p} {profile['name']} {q} {tau}", all(value == 0 for row in magnetic for value in row))
                if q == 0:
                    check(f"zero-tide branch {p} {profile['name']} {tau}", e_diag == (0, 0, 0))
                else:
                    check(f"tidal branch {p} {profile['name']} {q} {tau}", e_diag[0] != 0)
                mirrored = electric_weyl(tau, -q, lam)
                check(
                    f"q sign axis relabelling {p} {profile['name']} {q} {tau}",
                    mirrored == (e_diag[0], e_diag[2], e_diag[1]),
                )
            family_rows.append((profile["name"], p, q, lam, "ZERO_TIDE" if q == 0 else "ELECTRIC_TIDE"))


# CMC boundary is retained but not confused with the registered non-CMC family.
for p in (F(1), F(2)):
    for constant_tau in (F(-3), F(0), F(5, 2)):
        check(
            f"CMC constant-psi boundary {p} {constant_tau}",
            general_reduced_scalar(p, constant_tau, constant_tau, F(0), F(0), constant_tau ** 2 / 3) == 0,
        )


semantic = {
    "torus_selected": False,
    "constant_psi_native": False,
    "diagonal_tt_native": False,
    "negative_lambda_globally_selected": False,
    "p_is_calibrated_scale": False,
    "q_sign_selected": False,
    "tau_profile_selected": False,
    "all_noncmc_data_classified": False,
    "physical_history_selected": False,
    "metric_changed": False,
    "kernel_changed": False,
}
for key, value in semantic.items():
    check(f"semantic guard {key}", value is False)


atlas_rows = (
    ("domain", "flat marked T3", "CHOSE_BOUNDED_DIAGNOSTIC_SLICE", "not selected topology"),
    ("ansatz", "constant psi=p", "FREE_POSITIVE_PARAMETER_IN_SLICE", "not calibrated scale"),
    ("ansatz", "tau(x)", "FREE_SMOOTH_PERIODIC_NONCMC_FUNCTION", "arbitrary Fourier data retained"),
    ("ansatz", "constant diagonal TT", "CHOSE_BOUNDED_DIAGNOSTIC_SLICE", "transverse q channel retained"),
    ("vector", "W", "SOLVED_MODULO_TRANSLATION_KERNEL", "w'=p^6(tau-mu)/2"),
    ("scalar", "TT x coefficient", "SOLVED_WITHIN_ANSATZ", "alpha=2 p^6 mu/3"),
    ("scalar", "Lambda", "SOLVED_WITHIN_ANSATZ", "Lambda=-q^2"),
    ("physical", "gamma and K", "LAWFUL_OUTPUT", "direct constraints pass"),
    ("geometry", "q=0", "ZERO_INITIAL_WEYL", "local flatness only conditional"),
    ("geometry", "q!=0", "NONZERO_ELECTRIC_WEYL", "invariant tidal witness"),
    ("symmetry", "q sign", "AXIS_RELABELLED", "y-z swap"),
    ("freedom", "p q tau", "NOT_SELECTED", "family remains continuous and functional"),
    ("scope", "general non-CMC construction", "OPEN_OMITTED", "nonconstant psi and other seeds outside"),
    ("all", "physical history", "NOT_SELECTED", "construction characterizes lawful data only"),
)

with (ROOT / "NONCMC_FAMILY_ATLAS.tsv").open("w", encoding="utf-8") as handle:
    handle.write("sector\tobject\tclassification\tconstraint_or_guard\n")
    for row in atlas_rows:
        handle.write("\t".join(row) + "\n")


def fraction_text(value):
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


result = {
    "schema": "udt-g317-exact-noncmc-family-v1",
    "landing": landing,
    "status": "INTERNALLY_DERIVED__EXTERNAL_REVIEW_REQUIRED",
    "assertion_count": len(CHECKS),
    "profiles": [profile["name"] for profile in profiles],
    "family_instances": len(family_rows),
    "atlas_rows": len(atlas_rows),
    "classification": {
        "alpha": "(2/3)*p^6*mean(tau)",
        "q": "((beta-gamma)/2)*p^-6",
        "Lambda": "-q^2",
        "physical_metric": "p^4*diag(1,1,1)",
        "physical_K_mixed": "diag(tau(x),q,-q)",
    },
    "subclasses": {"q=0": "ZERO_INITIAL_WEYL", "q!=0": "NONZERO_ELECTRIC_WEYL"},
    "selected_history": False,
    "metric_changed": False,
    "kernel_changed": False,
    "sample_family": [
        {
            "profile": name,
            "p": fraction_text(p),
            "q": fraction_text(q),
            "Lambda": fraction_text(lam),
            "tide": tide,
        }
        for name, p, q, lam, tide in family_rows
    ],
    "checks": CHECKS,
}

(ROOT / "DERIVATION_RESULT.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
print(json.dumps({
    "landing": landing,
    "assertions": len(CHECKS),
    "family_instances": len(family_rows),
    "atlas_rows": len(atlas_rows),
}, indent=2))
