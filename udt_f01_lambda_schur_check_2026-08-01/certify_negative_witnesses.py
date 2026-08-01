#!/usr/bin/env python3
"""Validated R06 joint-negative witnesses for both owned p-trace variants.

This script is primary only for existence of an added negative joint direction.
It does not certify the R05 positive Schur sign or any global stability claim.
"""

from __future__ import annotations

import json
import platform
from fractions import Fraction
from pathlib import Path

import mpmath as mp
from mpmath import iv
import sympy as sp


OUT = Path(__file__).resolve().parent
iv.dps = 60
mp.mp.dps = 100
S_LO = "1.68102"
S_HI = "1.68103"
COARSE_SUBINTERVALS = 4096
FINE_SUBINTERVALS = 8192

# Exact decimal rationals, preregistered diagnostic N=4 minimizers rounded to
# nine decimal places.  The rounded vectors are evaluated anew; the diagnostic
# Schur values are not imported into the certificate.
WITNESSES = {
    "DIRICHLET": {
        "p": ["-0.435716777", "1.012907172", "0.127514598", "-0.771628348"],
        "f": ["0.548985835", "0.229527242", "-0.858813847", "0.294862992"],
    },
    "FREE": {
        "p": ["-0.730867811", "0.870467687", "-0.211945617", "-0.177970088"],
        "f": ["0.231682354", "0.443879735", "-0.576342529", "0.042284085"],
    },
}


def root_equation(s):
    """Closed form of s^-1 integral_0^(2s) log(1-z+z^2/2) dz."""
    u = 2 * s - 1
    return (
        u * iv.log((u * u + 1) / 2)
        - 2 * u
        + 2 * iv.atan2(u, iv.mpf(1))
        - 2
        + iv.pi / 2
    ) / s


def poly(coefficients, x):
    value = iv.mpf(0)
    for coefficient in reversed(coefficients):
        value = value * x + iv.mpf(str(coefficient.numerator)) / coefficient.denominator
    return value


def poly_derivative(coefficients, x):
    return poly([Fraction(k) * coefficients[k] for k in range(1, len(coefficients))], x)


def witness_fields(label: str, x):
    p_coeff = [Fraction(v) for v in WITNESSES[label]["p"]]
    f_coeff = [Fraction(v) for v in WITNESSES[label]["f"]]
    p0 = poly(p_coeff, x)
    dp0 = poly_derivative(p_coeff, x)
    f0 = poly(f_coeff, x)
    df0 = poly_derivative(f_coeff, x)
    if label == "DIRICHLET":
        factor = 1 - x * x
        factor_prime = -2 * x
    else:
        factor = 1 + x
        factor_prime = iv.mpf(1)
    p = factor * p0
    dp = factor_prime * p0 + factor * dp0
    # f' is the derivative of (1-x^2) times a polynomial.  Hence its
    # integral is exactly zero and both angular endpoint values may be pinned.
    fp = -2 * x * f0 + (1 - x * x) * df0
    return p, dp, fp


def density(label: str, s, x):
    p, dp, fp = witness_fields(label, x)
    w = (s * s / 2) * x * x + (s * s - s) * x + 1 + s * s / 2 - s
    wp = s * s * x + s * s - s
    logw = iv.log(w)
    # Representative a_F=a_F'=2.  Direct algebra gives k=a_F'/a_F^2=1/2.
    # With mu=1 the full form is Q_field + 2*k*L + k^2*C.
    field = w * (dp * dp + fp * fp) + 2 * p * (wp * dp + s * fp) + s * s * p * p
    cross = s * s * p * (1 + logw) + logw * (wp * dp + s * fp)
    diagonal = (s * s * logw * logw) / 4
    return field + cross + diagonal


def interval_integral(label: str, subintervals: int):
    s = iv.mpf([S_LO, S_HI])
    total = iv.mpf(0)
    width = mp.mpf(2) / subintervals
    for index in range(subintervals):
        lo = mp.mpf(-1) + index * width
        hi = lo + width
        x = iv.mpf([lo, hi])
        total += density(label, s, x) * iv.mpf(width)
    return total


def endpoints(value) -> list[str]:
    lower = iv.nstr(value.a, 70).lstrip("[").split(",", 1)[0]
    upper = iv.nstr(value.b, 70).lstrip("[").split(",", 1)[0]
    return [lower, upper]


def main() -> None:
    root_left = root_equation(iv.mpf(S_LO))
    root_right = root_equation(iv.mpf(S_HI))
    assert float(root_left.b) < 0
    assert float(root_right.a) > 0

    witnesses = {}
    for label in ("DIRICHLET", "FREE"):
        iv.dps = 80
        coarse = interval_integral(label, COARSE_SUBINTERVALS)
        iv.dps = 100
        enclosure = interval_integral(label, FINE_SUBINTERVALS)
        assert float(coarse.b) < 0 and float(enclosure.b) < 0
        assert float(enclosure.a) >= float(coarse.a)
        assert float(enclosure.b) <= float(coarse.b)
        witnesses[label] = {
            "p_coefficients_exact_decimal_rationals": WITNESSES[label]["p"],
            "f_primitive_coefficients_exact_decimal_rationals": WITNESSES[label]["f"],
            "mu": 1,
            "joint_quadratic_form_interval": endpoints(enclosure),
            "coarse_refinement_control_interval": endpoints(coarse),
            "certified_negative": True,
        }

    report = {
        "status": "CERTIFIED_R06_ADDED_NEGATIVE_DIRECTION_BOTH_P_TRACE_VARIANTS",
        "scope": "conditional F01 local crease cell; R06 odd zero f/h traces only",
        "root_uniqueness": {
            "proof": (
                "q(z)=1-z+z^2/2; log(q)<0 on (0,2), >0 on (2,infinity). "
                "Its primitive I therefore strictly increases for U>2; I(2)<0, while "
                "I(6)>=-2*log(2)+2*log(5)>0. Thus exactly one root occurs for s in (1,3)."
            ),
            "s_bracket": [S_LO, S_HI],
            "F_at_left_interval": endpoints(root_left),
            "F_at_right_interval": endpoints(root_right),
        },
        "positive_scale_separation": {
            "k": "a_Fprime/a_F^2",
            "identity": "Q=Q_field+2*(k*mu)*L+(k*mu)^2*C",
            "consequence": "for finite nonzero a_F and a_Fprime=2, the Schur sign is independent of the representative a_F",
            "representative": "a_F=a_Fprime=2; k=1/2",
        },
        "validated_integration": {
            "method": "outward interval range enclosure on a uniform partition",
            "x_interval": [-1, 1],
            "coarse_run": {"subintervals": COARSE_SUBINTERVALS, "interval_decimal_digits": 80},
            "fine_run": {"subintervals": FINE_SUBINTERVALS, "interval_decimal_digits": 100},
            "fine_interval_nested_in_coarse": True,
        },
        "witnesses": witnesses,
        "versions": {
            "python": platform.python_version(),
            "sympy": sp.__version__,
            "mpmath": mp.__version__,
        },
        "conclusion_ceiling": (
            "R06 has an added negative joint direction for each owned p trace at the unique root; "
            "R05 sign, wall-germ curvature, full chain, native stability, matter, and bootstrap remain open"
        ),
    }
    path = OUT / "NEGATIVE_WITNESS_CERTIFICATE.json"
    path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
