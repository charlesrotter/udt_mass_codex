#!/usr/bin/env python3
"""Exact algebra for the regular-branch flux ownership factorization."""

from __future__ import annotations

import json
from pathlib import Path

import sympy as sp


def matrix_is_zero(matrix: sp.Matrix) -> bool:
    return all(sp.simplify(value) == 0 for value in matrix)


def main() -> None:
    # Positive physical readouts. These are symbolic; no numerical history is selected.
    Z, d_A, luminosity_omega = sp.symbols(
        "Z d_A luminosity_omega", positive=True
    )
    survival, energy_ratio = sp.symbols(
        "survival energy_ratio", positive=True
    )

    # Screen reciprocity on a two-dimensional screen.
    a, b, c, d = sp.symbols("a b c d", real=True)
    D_forward = sp.Matrix([[a, b], [c, d]])
    D_reverse = Z * D_forward.T
    det_scaling = sp.simplify(D_reverse.det() / D_forward.det())
    assert det_scaling == Z**2

    # Differential bolometric flux. d_G is the source-angle -> receiver-area distance.
    d_G = Z * d_A
    clock_rate_ratio = 1 / Z  # d_tau_source / d_tau_observer
    flux = sp.simplify(
        luminosity_omega
        * survival
        * energy_ratio
        * clock_rate_ratio
        / d_G**2
    )
    expected_flux = luminosity_omega * survival * energy_ratio / (Z**3 * d_A**2)
    assert sp.simplify(flux - expected_flux) == 0

    # Isotropic-equivalent luminosity distance is a definition after source isotropy is supplied.
    luminosity = 4 * sp.pi * luminosity_omega
    d_L_squared = sp.simplify(luminosity / (4 * sp.pi * flux))
    expected_d_L_squared = Z**3 * d_A**2 / (survival * energy_ratio)
    assert sp.simplify(d_L_squared - expected_d_L_squared) == 0

    # The historical relation follows only after two extra transfer assignments.
    standard_flux = sp.simplify(flux.subs({survival: 1, energy_ratio: 1 / Z}))
    assert standard_flux == luminosity_omega / (Z**4 * d_A**2)
    standard_d_L_squared = sp.simplify(
        d_L_squared.subs({survival: 1, energy_ratio: 1 / Z})
    )
    assert standard_d_L_squared == Z**4 * d_A**2

    # Composition and reversal leave an infinite regular character family.
    # Under continuity/measurability/local boundedness, positive multiplicative
    # characters of R_{>0} are exactly powers. Without regularity, additive
    # Cauchy functions after log-coordinate conversion permit a larger class.
    p, q = sp.symbols("p q", real=True)
    Z_1, Z_2 = sp.symbols("Z_1 Z_2", positive=True)
    energy_character = lambda value: value ** (-p)
    survival_character = lambda value: value ** (-q)
    energy_composition = sp.simplify(
        energy_character(Z_1 * Z_2)
        / (energy_character(Z_1) * energy_character(Z_2))
    )
    survival_composition = sp.simplify(
        survival_character(Z_1 * Z_2)
        / (survival_character(Z_1) * survival_character(Z_2))
    )
    energy_reversal = sp.simplify(
        energy_character(1 / Z_1) * energy_character(Z_1)
    )
    survival_reversal = sp.simplify(
        survival_character(1 / Z_1) * survival_character(Z_1)
    )
    assert energy_composition == 1
    assert survival_composition == 1
    assert energy_reversal == 1
    assert survival_reversal == 1

    # Local covariant carried-density laws also remain nonunique. If A is a
    # finite beam cross-section and n obeys d(log n)=-a d(log A), then n*A
    # is conserved only for a=1, while every a composes across cross-sections.
    area_1, area_2, area_3 = sp.symbols(
        "area_1 area_2 area_3", positive=True
    )
    transport_a = sp.symbols("transport_a", real=True)
    amount_ratio = lambda area_end, area_start: (
        area_end / area_start
    ) ** (1 - transport_a)
    local_composition = sp.simplify(
        amount_ratio(area_3, area_1)
        / (amount_ratio(area_3, area_2) * amount_ratio(area_2, area_1))
    )
    assert local_composition == 1
    assert sp.simplify(amount_ratio(area_2, area_1).subs(transport_a, 1)) == 1

    exponent_family = sp.simplify((3 + p + q) / 2)
    assert exponent_family.subs({p: 1, q: 0}) == 2
    assert exponent_family.subs({p: 0, q: 0}) == sp.Rational(3, 2)
    assert exponent_family.subs({p: -1, q: 0}) == 1

    # Wronskian identity for a symmetric two-screen optical tidal matrix.
    t11, t12, t22 = sp.symbols("t11 t12 t22", real=True)
    T = sp.Matrix([[t11, t12], [t12, t22]])
    f11, f12, f21, f22 = sp.symbols("f11 f12 f21 f22", real=True)
    r11, r12, r21, r22 = sp.symbols("r11 r12 r21 r22", real=True)
    pf11, pf12, pf21, pf22 = sp.symbols("pf11 pf12 pf21 pf22", real=True)
    pr11, pr12, pr21, pr22 = sp.symbols("pr11 pr12 pr21 pr22", real=True)
    D_f = sp.Matrix([[f11, f12], [f21, f22]])
    D_r = sp.Matrix([[r11, r12], [r21, r22]])
    P_f = sp.Matrix([[pf11, pf12], [pf21, pf22]])
    P_r = sp.Matrix([[pr11, pr12], [pr21, pr22]])
    # W = D_r^T P_f - P_r^T D_f; substitute D'=P and P'=T D.
    W_prime = (
        P_r.T * P_f
        + D_r.T * T * D_f
        - (T * D_r).T * D_f
        - P_r.T * P_f
    )
    assert matrix_is_zero(W_prime)

    result = {
        "screen_dimension": 2,
        "reverse_determinant_factor": str(det_scaling),
        "reverse_area_distance_relation": "d_G = Z*d_A",
        "clock_rate_relation": "d_tau_source/d_tau_observer = 1/Z",
        "general_flux": "F_o = L_Omega*survival*energy_ratio/(Z^3*d_A^2)",
        "general_luminosity_distance_squared": (
            "d_L^2 = Z^3*d_A^2/(survival*energy_ratio)"
        ),
        "conditional_historical_relation": (
            "survival=1 and energy_ratio=1/Z imply d_L=Z^2*d_A"
        ),
        "character_family": (
            "regular: energy_ratio=Z^(-p), survival=Z^(-q), "
            "d_L=Z^((3+p+q)/2)*d_A"
        ),
        "character_scope": (
            "powers exhaust continuous/measurable/locally-bounded positive characters; "
            "composition alone permits pathological Cauchy characters"
        ),
        "composition_selects_p_or_q": False,
        "local_density_transport_family": (
            "d(log n)=-a*d(log area); carried n*area is conserved only at a=1"
        ),
        "local_transport_composes_for_all_a": True,
        "wronskian_derivative_zero": True,
        "scope": "regular single null branch with supplied metric and typed query",
    }
    output = Path(__file__).with_name("DERIVATION_RESULT.json")
    output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
