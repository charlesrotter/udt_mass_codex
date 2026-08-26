#!/usr/bin/env python3
"""Exact G265 static-radial closure checks. Writes no files."""

import json
import sympy as sp


def main() -> None:
    checks = 0
    c, f = sp.symbols("c f", positive=True)
    g = sp.diag(-f * c**2, 1 / f)
    k = sp.Matrix([1 / (c * f), 1])
    assert sp.simplify((k.T * g * k)[0]) == 0
    checks += 1

    # The three radial densities are different typed objects.
    null_time_density = 1 / (c * f)
    optical_density = 1 / f
    proper_density = 1 / sp.sqrt(f)
    lapse = sp.sqrt(f)
    assert sp.simplify(c * null_time_density - optical_density) == 0
    checks += 1
    assert sp.simplify(proper_density / (lapse * null_time_density) - c) == 0
    checks += 1

    # Literal global F1 equality between null time and slice distance is selective only by
    # adding that equality: positivity then forces f=1 pointwise.
    literal_residual = sp.factor(optical_density - proper_density)
    assert sp.solve(sp.Eq(literal_residual, 0), f) == [1]
    checks += 1

    kap = sp.symbols("kap", positive=True)
    calibrated = sp.solve(sp.Eq(optical_density, kap * proper_density), f)
    assert calibrated == [kap**(-2)]
    checks += 1

    # Current signed null arrow and relative coordinate-null speed are evaluator identities.
    phi_a, phi_b = sp.symbols("phi_a phi_b", real=True)
    f_a = sp.exp(-2 * phi_a)
    f_b = sp.exp(-2 * phi_b)
    delta = phi_b - phi_a
    arrow_ab = sp.sqrt(f_b / f_a)
    arrow_ba = sp.sqrt(f_a / f_b)
    assert sp.simplify(arrow_ab - sp.exp(-delta)) == 0
    checks += 1
    assert sp.simplify(arrow_ab * arrow_ba - 1) == 0
    checks += 1
    assert sp.simplify(f_b / f_a - sp.exp(-2 * delta)) == 0
    checks += 1

    # Equal same-correspondence slowdown in both directions trivializes the signed arrow.
    n_a, n_b = sp.symbols("n_a n_b", positive=True)
    mutual_solution = sp.solve(sp.Eq(n_b / n_a, n_a / n_b), n_b)
    assert mutual_solution == [n_a]
    checks += 1

    # Reversal-even group invariant and the optional SR-like projection are separate from the
    # signed character. The latter agrees with exp(-delta) only at delta=0.
    d = sp.symbols("d", real=True)
    D = sp.diag(sp.exp(-d), sp.exp(d))
    assert sp.simplify(sp.trace(D) / 2 - sp.cosh(d)) == 0
    checks += 1
    assert sp.simplify(D.subs(d, -d) - D.inv()) == sp.zeros(2)
    checks += 1
    signed_even_difference = sp.factor(sp.exp(-d) - 1 / sp.cosh(d))
    assert sp.solve(sp.Eq(signed_even_difference, 0), d) == [0]
    checks += 1

    # A symmetric two-endpoint speed can be formed by geometric-mean clock normalization,
    # but identifying it with sech(delta) is an additional functional equation. Its local
    # expansion first admits a nonconstant candidate which fails at fourth order.
    h = sp.symbols("h", real=True)
    n0, n1, n2, n3 = sp.symbols("n0 n1 n2 n3", positive=True)
    x = sp.symbols("x", real=True)
    N = n0 + n1 * x + n2 * x**2 / 2 + n3 * x**3 / 6
    i_half = sp.integrate(sp.series(1 / N, x, 0, 4).removeO(), (x, 0, h))
    i_opt = sp.integrate(sp.series(1 / N**2, x, 0, 4).removeO(), (x, 0, h))
    n_h = N.subs(x, h)
    m_geo = sp.series(i_half / (sp.sqrt(n0 * n_h) * i_opt), h, 0, 4).removeO()
    even_rate = sp.series(1 / sp.cosh(sp.log(n0 / n_h)), h, 0, 4).removeO()
    local_difference = sp.expand(m_geo - even_rate)
    coeff2 = sp.factor(local_difference.coeff(h, 2))
    expected2 = -n2 / (12 * n0) + 11 * n1**2 / (24 * n0**2)
    assert sp.simplify(coeff2 - expected2) == 0
    checks += 1

    p, z = sp.symbols("p z", real=True)
    p_nonconstant = sp.solve(sp.Eq(2 * p * (p - 1), 11 * p**2), p)
    assert p_nonconstant == [sp.Rational(-2, 9), 0]
    checks += 1

    pcrit = sp.Rational(-2, 9)
    xx = 1 + z
    m_power = (
        (1 - 2 * pcrit)
        / (1 - pcrit)
        * (xx ** (1 - pcrit) - 1)
        / (xx ** (pcrit / 2) * (xx ** (1 - 2 * pcrit) - 1))
    )
    r_power = 1 / sp.cosh(pcrit * sp.log(1 / xx))
    power_difference = sp.series(m_power - r_power, z, 0, 6).removeO()
    assert sp.simplify(sp.expand(power_difference).coeff(z, 4) - sp.Rational(7, 13122)) == 0
    checks += 1

    # Separating exact profile samples.
    rr, eps, ell = sp.symbols("rr eps ell", positive=True)
    bump = 1 + eps * (rr / ell) ** 2 * sp.exp(-(rr / ell) ** 2)
    assert sp.simplify(bump - 1) != 0
    checks += 1
    assert sp.simplify((1 / bump) - (1 / sp.sqrt(bump))) != 0
    checks += 1
    alpha2 = 1 + eps * (rr / ell) ** 2
    assert sp.simplify((1 / alpha2) - (1 / sp.sqrt(alpha2))) != 0
    checks += 1

    result = {
        "status": "PASS",
        "exact_checks": checks,
        "landing": (
            "INFINITE_BARE_C_METRIC_NULL_READING_IS_IDENTITY__LITERAL_DISTANCE_TIME_CLOSURE_"
            "TRIVIALIZES_THE_STATIC_PROFILE__SAME_CORRESPONDENCE_MUTUAL_SLOWDOWN_IS_NOT_THE_"
            "SIGNED_NULL_ARROW__THE_RECIPROCAL_KERNEL_ALREADY_CONTAINS_DISTINCT_EVEN_AND_"
            "DIRECTIONAL_CHANNELS__DISTANCE_OWNERSHIP_STILL_REQUIRES_A_TIMELIVE_OR_TWO_POINT_"
            "VALUE_LAW"
        ),
        "optical_closure": "identity for every positive f",
        "proper_distance_closure": "f=1, or constant before smooth-center calibration",
        "signed_arrow": "exp(-delta), inverse under same-correspondence reversal",
        "even_invariant": "cosh(delta)",
        "candidate_mutual_clock_rate": "sech(delta), proposed physical projection",
        "symmetric_all_interval_closure": "constant lapse only",
        "qualification": "static radial classification; not a full time-live no-go or canonization",
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
