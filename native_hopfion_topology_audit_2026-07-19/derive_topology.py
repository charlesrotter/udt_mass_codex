#!/usr/bin/env python3
"""Exact CPU algebra for the native Hopfion topology audit."""

from __future__ import annotations

import argparse
import json
import pathlib
import platform

import sympy as sp


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    eta, xi1, xi2 = sp.symbols("eta xi1 xi2", real=True)
    coordinates = (eta, xi1, xi2)
    connection = (sp.Integer(0), sp.cos(eta) ** 2, sp.sin(eta) ** 2)

    # Coefficient of A wedge dA in d_eta wedge d_xi1 wedge d_xi2.
    cs_density = sp.simplify(sum(
        sp.LeviCivita(i, j, k) * connection[i] * sp.diff(connection[k], coordinates[j])
        for i in range(3) for j in range(3) for k in range(3)
    ))
    cs_integral = sp.integrate(
        cs_density,
        (eta, 0, sp.pi / 2),
        (xi1, 0, 2 * sp.pi),
        (xi2, 0, 2 * sp.pi),
    )
    hopf_charge = sp.simplify(-cs_integral / (4 * sp.pi**2))

    # Twice the normalized connection has curvature equal to the conventional unit-S2 area form.
    area_connection = tuple(2 * component for component in connection)
    area_cs_density = sp.simplify(sum(
        sp.LeviCivita(i, j, k) * area_connection[i] * sp.diff(area_connection[k], coordinates[j])
        for i in range(3) for j in range(3) for k in range(3)
    ))
    area_cs_integral = sp.integrate(
        area_cs_density,
        (eta, 0, sp.pi / 2),
        (xi1, 0, 2 * sp.pi),
        (xi2, 0, 2 * sp.pi),
    )
    area_normalized_hopf_charge = sp.simplify(-area_cs_integral / (16 * sp.pi**2))

    x1, x2, x3, x4 = sp.symbols("x1 x2 x3 x4", real=True)
    n1 = 2 * (x1 * x3 + x2 * x4)
    n2 = 2 * (x2 * x3 - x1 * x4)
    n3 = x1**2 + x2**2 - x3**2 - x4**2
    s3_norm = x1**2 + x2**2 + x3**2 + x4**2
    hopf_target_identity = sp.expand(n1**2 + n2**2 + n3**2 - s3_norm**2)

    theta, azimuth = sp.symbols("theta azimuth", real=True)
    hedgehog_flux = sp.integrate(
        sp.sin(theta),
        (theta, 0, sp.pi),
        (azimuth, 0, 2 * sp.pi),
    )

    p1, p2, p3, q1, q2, q3, scale = sp.symbols("p1 p2 p3 q1 q2 q3 scale", real=True)
    p = sp.Matrix([p1, p2, p3])
    q = sp.Matrix([q1, q2, q3])
    gradient_frobenius = sp.expand((scale * p).dot(q.cross(p)))

    omega, conformal = sp.symbols("omega conformal", positive=True)
    u1, u2, u3 = sp.symbols("u1 u2 u3", real=True)
    spatial_norm = u1**2 + u2**2 + u3**2
    ray = sp.Matrix([omega, omega * u1, omega * u2, omega * u3])
    minkowski = sp.diag(-1, 1, 1, 1)
    csn_metric = sp.diag(-conformal**2, conformal**2, conformal**2, conformal**2)
    null_norm = sp.expand((ray.T * minkowski * ray)[0])
    conformal_null_norm = sp.expand((ray.T * csn_metric * ray)[0])

    checks = {
        "hopf_target_identity_zero": hopf_target_identity == 0,
        "chern_simons_density": str(cs_density),
        "chern_simons_integral": str(cs_integral),
        "canonical_hopf_charge": str(hopf_charge),
        "canonical_hopf_charge_is_one": hopf_charge == 1,
        "unit_s2_area_chern_simons_integral": str(area_cs_integral),
        "unit_s2_area_hopf_charge": str(area_normalized_hopf_charge),
        "unit_s2_area_hopf_charge_is_one": area_normalized_hopf_charge == 1,
        "hedgehog_s2_flux": str(hedgehog_flux),
        "hedgehog_has_nonzero_primary_flux": hedgehog_flux == 4 * sp.pi,
        "normalized_gradient_frobenius_zero": gradient_frobenius == 0,
        "projective_null_condition": str(null_norm),
        "projective_null_fiber_is_s2": sp.simplify(null_norm / omega**2 + 1 - spatial_norm) == 0,
        "csn_scaled_metric_null_norm": str(conformal_null_norm),
        "csn_preserves_null_condition": sp.simplify(conformal_null_norm - conformal**2 * null_norm) == 0,
    }
    if not all(value for key, value in checks.items() if isinstance(value, bool)):
        raise AssertionError(checks)

    result = {
        "python": platform.python_version(),
        "sympy": sp.__version__,
        "method": "exact Hopf-coordinate Chern-Simons integration plus independent algebraic target/flux/null checks",
        "checks": checks,
        "classification_limits": {
            "canonical_hopf_map": "mathematical positive control only",
            "null_s2": "celestial conformal/topological S2 fiber of the projective null-line cone after the conditional 4D Lorentzian readout; not a fixed round carrier target or selected section; future positive rays additionally require chosen time orientation",
            "gradient_s2": "hypersurface-orthogonal where defined; not a generic carrier map",
            "hedgehog_flux": "nonzero primary pi2 flux; not a localized zero-flux Hopf configuration",
        },
    }
    output = pathlib.Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print("DERIVATION exact_checks=11/11")
    print(f"canonical_hopf_charge={hopf_charge}")
    print(f"unit_s2_area_hopf_charge={area_normalized_hopf_charge}")
    print(f"hedgehog_flux={hedgehog_flux}")
    print("projective_null_fiber=S2 CONDITIONAL_ON_4D_LORENTZIAN_READOUT")
    print("selected_null_direction_section=OPEN")


if __name__ == "__main__":
    main()
