#!/usr/bin/env python3
"""Exact G264 metric-native classification of negative-phi selectivity."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import sympy as sp


LANDING = (
    "NEGATIVE_PHI_SIGN_ALONE_DOES_NOT_SELECT"
    "__FINITE_ARBITRARILY_DEEP_SMOOTH_ASYMPTOTICALLY_FLAT_SLICE_COMPLETE_COUNTERFAMILY_EXISTS"
    "__UNBOUNDED_NEGATIVE_ENDS_HAVE_AN_ALPHA_TWO_CURVATURE_ACCELERATION_AND_SLICE_COMPLETENESS_THRESHOLD"
    "__THE_ALPHA_TWO_CRITICAL_REPRESENTATIVE_IS_THE_G201_ZERO_TIDE_FAMILY"
)


def derive() -> dict[str, object]:
    r, theta = sp.symbols("r theta", positive=True, real=True)
    t, varphi = sp.symbols("t varphi", real=True)
    f = sp.Function("f")(r)
    coordinates = (t, r, theta, varphi)
    metric = sp.diag(-f, 1 / f, r**2, r**2 * sp.sin(theta) ** 2)
    inverse = sp.simplify(metric.inv())
    n = 4
    checks: list[str] = []

    def exact(name: str, expression: sp.Expr) -> None:
        if sp.simplify(expression) != 0:
            raise AssertionError(name)
        checks.append(name)

    exact("metric_determinant_f_independent", metric.det() + r**4 * sp.sin(theta) ** 2)

    christoffel = [
        [
            [
                sp.simplify(
                    sum(
                        inverse[a, d]
                        * (
                            sp.diff(metric[d, c], coordinates[b])
                            + sp.diff(metric[d, b], coordinates[c])
                            - sp.diff(metric[b, c], coordinates[d])
                        )
                        for d in range(n)
                    )
                    / 2
                )
                for c in range(n)
            ]
            for b in range(n)
        ]
        for a in range(n)
    ]

    ricci = sp.MutableDenseNDimArray.zeros(n, n)
    for a in range(n):
        for b in range(n):
            ricci[a, b] = sp.simplify(
                sum(
                    sp.diff(christoffel[c][a][b], coordinates[c])
                    - sp.diff(christoffel[c][a][c], coordinates[b])
                    + sum(
                        christoffel[c][c][d] * christoffel[d][a][b]
                        - christoffel[c][b][d] * christoffel[d][a][c]
                        for d in range(n)
                    )
                    for c in range(n)
                )
            )
    scalar = sp.simplify(sum(inverse[a, b] * ricci[a, b] for a in range(n) for b in range(n)))
    scalar_target = -sp.diff(f, r, 2) - 4 * sp.diff(f, r) / r - 2 * (f - 1) / r**2
    exact("scalar_curvature_direct", scalar - scalar_target)

    einstein = sp.MutableDenseNDimArray.zeros(n, n)
    for a in range(n):
        for b in range(n):
            einstein[a, b] = sp.simplify(ricci[a, b] - metric[a, b] * scalar / 2)
    g_t = sp.simplify(inverse[0, 0] * einstein[0, 0])
    g_theta = sp.simplify(inverse[2, 2] * einstein[2, 2])
    exact("einstein_radial_channel", g_t - (r * sp.diff(f, r) + f - 1) / r**2)
    exact("einstein_angular_channel", g_theta - (sp.diff(f, r, 2) / 2 + sp.diff(f, r) / r))
    exact("scalar_from_channel_trace", scalar + 2 * g_t + 2 * g_theta)

    riemann_up = sp.MutableDenseNDimArray.zeros(n, n, n, n)
    for a in range(n):
        for b in range(n):
            for c in range(n):
                for d in range(n):
                    riemann_up[a, b, c, d] = sp.simplify(
                        sp.diff(christoffel[a][b][d], coordinates[c])
                        - sp.diff(christoffel[a][b][c], coordinates[d])
                        + sum(
                            christoffel[a][c][e] * christoffel[e][b][d]
                            - christoffel[a][d][e] * christoffel[e][b][c]
                            for e in range(n)
                        )
                    )
    riemann_down = sp.MutableDenseNDimArray.zeros(n, n, n, n)
    for a in range(n):
        for b in range(n):
            for c in range(n):
                for d in range(n):
                    riemann_down[a, b, c, d] = sp.simplify(
                        sum(metric[a, e] * riemann_up[e, b, c, d] for e in range(n))
                    )
    kretschmann = 0
    for a in range(n):
        for b in range(n):
            for c in range(n):
                for d in range(n):
                    if riemann_down[a, b, c, d] == 0:
                        continue
                    for aa in range(n):
                        if inverse[a, aa] == 0:
                            continue
                        for bb in range(n):
                            if inverse[b, bb] == 0:
                                continue
                            for cc in range(n):
                                if inverse[c, cc] == 0:
                                    continue
                                for dd in range(n):
                                    if inverse[d, dd] == 0:
                                        continue
                                    kretschmann += (
                                        inverse[a, aa]
                                        * inverse[b, bb]
                                        * inverse[c, cc]
                                        * inverse[d, dd]
                                        * riemann_down[a, b, c, d]
                                        * riemann_down[aa, bb, cc, dd]
                                    )
    kretschmann = sp.simplify(kretschmann)
    kretschmann_target = (
        sp.diff(f, r, 2) ** 2
        + 4 * (sp.diff(f, r) / r) ** 2
        + 4 * ((f - 1) / r**2) ** 2
    )
    exact("kretschmann_direct", kretschmann - kretschmann_target)

    epsilon, length = sp.symbols("epsilon length", positive=True, real=True)
    x = r**2 / length**2
    bump = 1 + epsilon * x * sp.exp(-x)
    bump_prime = 2 * epsilon * r * sp.exp(-x) * (1 - x) / length**2
    bump_second = 2 * epsilon * sp.exp(-x) * (1 - 5 * x + 2 * x**2) / length**2
    exact("bump_first_derivative", sp.diff(bump, r) - bump_prime)
    exact("bump_second_derivative", sp.diff(bump, r, 2) - bump_second)
    bump_scalar = sp.simplify(scalar_target.subs(f, bump).doit())
    bump_scalar_target = -2 * epsilon * sp.exp(-x) * (2 * x**2 - 9 * x + 6) / length**2
    exact("bump_scalar_curvature", bump_scalar - bump_scalar_target)
    bump_k = sp.simplify(kretschmann_target.subs(f, bump).doit())
    bump_k_target = (
        4
        * epsilon**2
        * sp.exp(-2 * x)
        * ((1 - 5 * x + 2 * x**2) ** 2 + 4 * (1 - x) ** 2 + 1)
        / length**4
    )
    exact("bump_kretschmann", bump_k - bump_k_target)
    exact("bump_center_f", sp.limit(bump, r, 0) - 1)
    exact("bump_center_first_derivative", sp.limit(sp.diff(bump, r), r, 0))
    exact("bump_center_scalar", sp.limit(bump_scalar, r, 0) + 12 * epsilon / length**2)
    exact("bump_center_kretschmann", sp.limit(bump_k, r, 0) - 24 * epsilon**2 / length**4)
    exact("bump_asymptotic_f", sp.limit(bump, r, sp.oo) - 1)
    exact("bump_asymptotic_scalar", sp.limit(bump_scalar, r, sp.oo))
    exact("bump_asymptotic_kretschmann", sp.limit(bump_k, r, sp.oo))
    phi_bump = -sp.log(bump) / 2
    exact(
        "bump_center_phi_coefficient",
        sp.limit(phi_bump / r**2, r, 0) + epsilon / (2 * length**2),
    )
    exact("bump_maximum_value", bump.subs(r, length) - 1 - epsilon / sp.E)

    rho, coefficient, alpha = sp.symbols("rho coefficient alpha", positive=True, real=True)
    power = coefficient * rho**alpha
    power_scalar = -sp.diff(power, rho, 2) - 4 * sp.diff(power, rho) / rho - 2 * power / rho**2
    power_scalar_target = -coefficient * (alpha + 1) * (alpha + 2) * rho ** (alpha - 2)
    exact("power_scalar_leading", power_scalar - power_scalar_target)
    power_k = (
        sp.diff(power, rho, 2) ** 2
        + 4 * (sp.diff(power, rho) / rho) ** 2
        + 4 * (power / rho**2) ** 2
    )
    power_k_target = (
        coefficient**2
        * (alpha**2 * (alpha - 1) ** 2 + 4 * alpha**2 + 4)
        * rho ** (2 * alpha - 4)
    )
    exact("power_kretschmann_leading", power_k - power_k_target)
    power_accel = sp.diff(sp.sqrt(power), rho)
    exact(
        "power_acceleration_leading",
        power_accel - sp.sqrt(coefficient) * alpha * rho ** (alpha / 2 - 1) / 2,
    )

    critical_c = sp.symbols("critical_c", positive=True, real=True)
    critical = 1 + critical_c * r**2 / length**2
    critical_scalar = sp.simplify(scalar_target.subs(f, critical).doit())
    critical_k = sp.simplify(kretschmann_target.subs(f, critical).doit())
    critical_aparallel = sp.simplify((r**2 * sp.diff(critical, r, 2) - r * sp.diff(critical, r)) / 2)
    critical_aperp = sp.simplify(1 - critical + r * sp.diff(critical, r) / 2)
    critical_accel = sp.diff(sp.sqrt(critical), r)
    exact("critical_scalar_constant", critical_scalar + 12 * critical_c / length**2)
    exact("critical_kretschmann_constant", critical_k - 24 * critical_c**2 / length**4)
    exact("critical_Aparallel_zero", critical_aparallel)
    exact("critical_Aperp_zero", critical_aperp)
    exact(
        "critical_acceleration_limit",
        sp.limit(critical_accel, r, sp.oo) - sp.sqrt(critical_c) / length,
    )

    return {
        "status": "PASS",
        "landing": LANDING,
        "classification": "SIGN_ONLY_NONSELECTION_WITH_GROWTH_THRESHOLDS",
        "scope": "primary_static_spherical_real_phi_positive_f_local_and_power_asymptotic",
        "symbolic_check_count": len(checks),
        "symbolic_checks": checks,
        "invariants": {
            "determinant": "-c_E^2 r^4 sin(theta)^2 independent of f",
            "scalar_curvature": "-f_second-4 f_first/r-2(f-1)/r^2",
            "kretschmann": "f_second^2+4(f_first/r)^2+4((f-1)/r^2)^2",
        },
        "negative_bump": {
            "family": "f=1+epsilon rho^2 exp(-rho^2), epsilon>0",
            "properties": [
                "phi<0 for every finite r>0",
                "smooth areal center",
                "asymptotically flat",
                "bounded scalar and Kretschmann curvature for each finite epsilon and length",
                "complete static spatial slice",
                "arbitrarily negative finite minimum as epsilon increases",
            ],
            "ownership": "counterfamily_not_selected_physical_history",
        },
        "power_end": {
            "assumption": "f~C(r/L)^alpha with C>0 alpha>0",
            "alpha_less_than_2": "radial slice length infinite; R,K,normalized acceleration tend zero",
            "alpha_equal_2": "radial slice length logarithmically infinite; R,K finite nonzero; normalized acceleration finite nonzero",
            "alpha_greater_than_2": "radial slice length finite; R,K and normalized acceleration diverge",
            "spatial_volume": "infinite for alpha<=6 and finite for alpha>6",
        },
        "alpha_two_critical": {
            "family": "f=1+C(r/L)^2 with C>0",
            "G201_angular_channels": "Aparallel=Aperp=0 exactly",
            "scalar_curvature": "-12C/L^2",
            "kretschmann": "24C^2/L^4",
            "static_slice": "complete with logarithmically divergent radial proper length",
            "normalized_acceleration": "tends sqrt(C)/L",
            "phi": "tends negative infinity",
            "ownership": "derived_conditional_intersection_not_physical_selection",
        },
        "conditional_monotone_quiet_end_theorem": (
            "f(0)=1, f>=1 nondecreasing, and f->1 imply f identically 1; monotonicity and outer quietness are not founded"
        ),
        "ownership": {
            "sign_only_selection": "NOT_DERIVED_COUNTERFAMILY",
            "growth_thresholds": "DERIVED_CONDITIONAL_ASYMPTOTIC_CLASSIFICATION",
            "spatial_completeness": "CONDITIONAL_GEOMETRIC_CLASSIFIER",
            "physical_mass_or_energy_positivity": "NOT_USED_NOT_DERIVED",
            "history_source_dynamics_xmax": "OPEN",
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = derive()
    encoded = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(encoded, encoding="utf-8")
    else:
        print(encoded, end="")


if __name__ == "__main__":
    main()
