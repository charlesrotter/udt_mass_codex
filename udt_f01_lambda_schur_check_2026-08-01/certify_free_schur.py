#!/usr/bin/env python3
"""Exact-response plus interval certificate for the R05 free-angular Schur sign."""

from __future__ import annotations

import json
import platform
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


def symbolic_controls() -> dict[str, bool]:
    x, s = sp.symbols("x s", real=True, nonzero=True)
    w = s**2 * x**2 / 2 + (s**2 - s) * x + 1 + s**2 / 2 - s
    wp = sp.diff(w, x)
    logw = sp.log(w)
    lop = lambda value: sp.factor(-sp.diff(w * sp.diff(value, x), x) - s**2 * value / w)
    v1 = wp / w
    v2 = 1 - 1 / w
    source = s**2 * (-1 + (1 - logw) / w)
    particular = 1 - logw
    t = lambda value: sp.factor(w * sp.diff(value, x) + wp * value)
    w_right = sp.factor(w.subs(x, 1))
    wp_right = sp.factor(wp.subs(x, 1))
    b_free = -1 / (2 * s - 1)
    response_free = particular + v1 / s + b_free * v2
    b_dirichlet = sp.factor(-(w_right * (1 - sp.log(w_right)) + 2 * s - 1) / (w_right - 1))
    response_dirichlet = particular + v1 / s + b_dirichlet * v2
    controls = {
        "quadratic_identity": sp.simplify(wp**2 + s**2 - 2 * s**2 * w) == 0,
        "v1_homogeneous": sp.simplify(lop(v1)) == 0,
        "v2_homogeneous": sp.simplify(lop(v2)) == 0,
        "particular_response": sp.simplify(lop(particular) + source) == 0,
        "free_left_dirichlet": sp.simplify(response_free.subs(x, -1)) == 0,
        "free_right_inhomogeneous_robin": sp.simplify((t(response_free) + logw * wp).subs(x, 1)) == 0,
        "dirichlet_left": sp.simplify(response_dirichlet.subs(x, -1)) == 0,
        "dirichlet_right": sp.simplify(response_dirichlet.subs(x, 1)) == 0,
        "free_homogeneous_kernel_excluded": sp.simplify(wp_right) != 0,
        "dirichlet_homogeneous_kernel_excluded": sp.simplify((1 - 1 / w_right)) != 0,
    }
    assert all(controls.values())
    return controls


def interval_response(label: str, s, x):
    w = (s * s / 2) * x * x + (s * s - s) * x + 1 + s * s / 2 - s
    wp = s * s * x + s * s - s
    logw = iv.log(w)
    v1 = wp / w
    v1p = s * s / w - wp * wp / (w * w)
    v2 = 1 - 1 / w
    v2p = wp / (w * w)
    if label == "FREE":
        coefficient = -1 / (2 * s - 1)
    else:
        w_right = 1 - 2 * s + 2 * s * s
        coefficient = -(w_right * (1 - iv.log(w_right)) + 2 * s - 1) / (w_right - 1)
    response = 1 - logw + v1 / s + coefficient * v2
    response_prime = -wp / w + v1p / s + coefficient * v2p
    return w, wp, logw, response, response_prime


def schur_integrand(label: str, s, x):
    w, wp, logw, response, response_prime = interval_response(label, s, x)
    ell = (
        s * s * response * (1 + logw * (1 - 1 / w))
        + logw * wp * response_prime
    )
    diagonal = s * s * logw * logw * (1 - 1 / w)
    return diagonal + ell


def interval_integral(label: str, subintervals: int):
    s = iv.mpf([S_LO, S_HI])
    total = iv.mpf(0)
    width = mp.mpf(2) / subintervals
    for index in range(subintervals):
        lo = mp.mpf(-1) + index * width
        hi = lo + width
        x = iv.mpf([lo, hi])
        total += schur_integrand(label, s, x) * iv.mpf(width)
    return total


def endpoints(value) -> list[str]:
    lower = iv.nstr(value.a, 70).lstrip("[").split(",", 1)[0]
    upper = iv.nstr(value.b, 70).lstrip("[").split(",", 1)[0]
    return [lower, upper]


def main() -> None:
    controls = symbolic_controls()
    branches = {}
    for label in ("DIRICHLET", "FREE"):
        iv.dps = 80
        coarse = interval_integral(label, COARSE_SUBINTERVALS)
        iv.dps = 100
        dimensionless = interval_integral(label, FINE_SUBINTERVALS)
        assert float(coarse.a) > 0 and float(dimensionless.a) > 0
        assert float(dimensionless.a) >= float(coarse.a)
        assert float(dimensionless.b) <= float(coarse.b)
        # For a_F=a_Fprime=2, k=a_Fprime/a_F^2=1/2 and S_mu=k^2*S_nu.
        representative = dimensionless / 4
        branches[label] = {
            "dimensionless_nu_schur_interval": endpoints(dimensionless),
            "coarse_refinement_control_interval": endpoints(coarse),
            "representative_mu_schur_interval": endpoints(representative),
            "certified_positive": True,
        }
    report = {
        "status": "CERTIFIED_R05_POSITIVE_SCHUR_BOTH_P_TRACE_VARIANTS",
        "scope": "conditional F01 local crease cell; R05 free f/h traces only",
        "root_bracket_imported_from_primary_root_certificate": [S_LO, S_HI],
        "exact_response": {
            "operator": "L[p]=-(w*p')'-s^2*p/w",
            "source": "s^2*(-1+(1-log(w))/w)",
            "particular": "1-log(w)",
            "homogeneous_basis": ["w'/w", "1-1/w"],
            "uniqueness": "left Dirichlet plus either right Dirichlet or the registered free-right Robin condition excludes both homogeneous constants for s>1",
        },
        "symbolic_controls": controls,
        "positive_scale_separation": {
            "k": "a_Fprime/a_F^2",
            "identity": "S_mu=k^2*S_nu",
            "consequence": "sign is independent of finite nonzero a_F when a_Fprime=2",
            "representative": "a_F=a_Fprime=2; k^2=1/4",
        },
        "validated_integration": {
            "method": "outward interval range enclosure on a uniform partition",
            "x_interval": [-1, 1],
            "s_interval": [S_LO, S_HI],
            "coarse_run": {"subintervals": COARSE_SUBINTERVALS, "interval_decimal_digits": 80},
            "fine_run": {"subintervals": FINE_SUBINTERVALS, "interval_decimal_digits": 100},
            "fine_interval_nested_in_coarse": True,
        },
        "branches": branches,
        "versions": {
            "python": platform.python_version(),
            "sympy": sp.__version__,
            "mpmath": mp.__version__,
        },
        "conclusion_ceiling": (
            "R05 lambda/mu adds no negative direction beyond the one exact reduced-field direction; "
            "wall-germ curvature, full chain, native stability, matter, and bootstrap remain open"
        ),
    }
    path = OUT / "FREE_SCHUR_CERTIFICATE.json"
    path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
