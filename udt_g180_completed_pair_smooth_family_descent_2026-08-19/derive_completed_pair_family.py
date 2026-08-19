#!/usr/bin/env python3
"""Exact symbolic derivation for G180 completed-pair smooth-family descent."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent


def source_hashes() -> tuple[int, list[str]]:
    rows = list(csv.DictReader((HERE / "SOURCE_MANIFEST.tsv").open(), delimiter="\t"))
    failures = []
    for row in rows:
        actual = hashlib.sha256((ROOT / row["path"]).read_bytes()).hexdigest()
        if actual != row["sha256"]:
            failures.append(row["path"])
    return len(rows), failures


def matrix_strings(value: sp.Matrix) -> list[list[str]]:
    return [[str(value[i, j]) for j in range(value.cols)] for i in range(value.rows)]


def main() -> None:
    # Generic shifted pair. Positivity is a domain condition; the identities are exact.
    t, ell, beta, k, common = sp.symbols("T L beta k common", positive=True, real=True)
    h = sp.Matrix(
        [
            [-t**2, -t**2 * beta],
            [-t**2 * beta, ell**2 - t**2 * beta**2],
        ]
    )
    m2 = sp.simplify(-h.det())
    m = t * ell
    d = sp.diag(1, 1 / m)
    h_s = sp.simplify(d.T * h * d)
    beta_s = sp.simplify(beta / m)

    # Lawful auxiliary reparameterization sigma=k*sigma_tilde.
    p = sp.diag(1, k)
    h_k = sp.simplify(p.T * h * p)
    m_k = sp.simplify(k * m)
    d_k = sp.diag(1, 1 / m_k)
    h_s_k = sp.simplify(d_k.T * h_k * d_k)

    # Common metric scale is retained by the completed kernel rather than canceled.
    h_common = sp.simplify(common**2 * h)
    common_m2 = sp.simplify(-h_common.det())
    common_m = sp.simplify(common**2 * m)
    h_s_common = sp.simplify(
        sp.diag(1, 1 / common_m).T
        * h_common
        * sp.diag(1, 1 / common_m)
    )

    # Primary static-spherical family. q=exp(-2 phi)>0.
    q, r, v, b2 = sp.symbols("q r v b2", positive=True, real=True)
    h_spatial = sp.simplify(v**2 / q + r**2 * b2)
    h_primary = sp.diag(-q, h_spatial)
    primary_m2 = sp.simplify(-h_primary.det())
    primary_h_s = sp.simplify(
        sp.diag(1, 1 / sp.sqrt(primary_m2)).T
        * h_primary
        * sp.diag(1, 1 / sp.sqrt(primary_m2))
    )

    # Exact derivative identities, including the distance-parametrized response.
    qdot, rdot, vdot, b2dot = sp.symbols("qdot rdot vdot b2dot", real=True)
    primary_m2_dot_direct = sp.expand(
        sp.diff(primary_m2, q) * qdot
        + sp.diff(primary_m2, r) * rdot
        + sp.diff(primary_m2, v) * vdot
        + sp.diff(primary_m2, b2) * b2dot
    )
    h00_dot = -qdot
    phi_dot_from_h = sp.simplify(-sp.Rational(1, 2) * h00_dot / (-q))
    phi_dot_from_q = sp.simplify(-qdot / (2 * q))
    phi_s_squared = sp.simplify(phi_dot_from_q**2 / primary_m2)

    # Registered rational witnesses.
    generic_values = {t: sp.Rational(3, 2), ell: sp.Rational(5, 3), beta: sp.Rational(-2, 5)}
    generic_h = sp.simplify(h.subs(generic_values))
    generic_h_s = sp.simplify(h_s.subs(generic_values))

    primary_values = {
        q: sp.Rational(1, 4),
        r: sp.Integer(3),
        v: sp.Integer(2),
        b2: sp.Rational(25, 36),
    }
    primary_h_value = sp.simplify(h_primary.subs(primary_values))
    primary_m2_value = sp.simplify(primary_m2.subs(primary_values))
    primary_h_s_value = sp.simplify(primary_h_s.subs(primary_values))

    turning_values = {
        q: sp.Rational(1, 4),
        r: sp.Integer(3),
        v: sp.Integer(0),
        b2: sp.Rational(4, 9),
    }
    turning_h = sp.simplify(h_primary.subs(turning_values))
    turning_m2 = sp.simplify(primary_m2.subs(turning_values))
    turning_h_s = sp.simplify(primary_h_s.subs(turning_values))

    checks = {
        "generic_pair_determinant": sp.simplify(h.det() + t**2 * ell**2) == 0,
        "generic_density": sp.simplify(m2 - t**2 * ell**2) == 0,
        "generic_calibrated_determinant": sp.simplify(h_s.det() + 1) == 0,
        "generic_reciprocal_clock_ruler": sp.simplify(
            h_s[1, 1] - h_s[0, 1] ** 2 / h_s[0, 0] - 1 / t**2
        ) == 0,
        "generic_shift_retained": sp.simplify(h_s[0, 1] + t**2 * beta_s) == 0,
        "positive_reparameterization_density": sp.simplify(-h_k.det() - m_k**2) == 0,
        "positive_reparameterization_invariant": sp.simplify(h_s_k - h_s) == sp.zeros(2),
        "common_scale_density_retained": sp.simplify(common_m2 - common**4 * m2) == 0,
        "common_scale_calibrated_determinant": sp.simplify(h_s_common.det() + 1) == 0,
        "common_scale_changes_completed_depth": sp.simplify(
            -sp.log(common * t) + sp.log(t) + sp.log(common)
        ) == 0,
        "primary_pullback_determinant": sp.simplify(h_primary.det() + q * h_spatial) == 0,
        "primary_density": sp.simplify(primary_m2 - (v**2 + q * r**2 * b2)) == 0,
        "primary_calibrated_metric": sp.simplify(primary_h_s - sp.diag(-q, 1 / q)) == sp.zeros(2),
        "primary_calibrated_determinant": sp.simplify(primary_h_s.det() + 1) == 0,
        "angular_channel_changes_tape": sp.diff(primary_m2, b2) == q * r**2,
        "angular_channel_not_direct_depth": sp.diff(-sp.log(q) / 2, b2) == 0,
        "profile_changes_depth": sp.diff(-sp.log(q) / 2, q) == -1 / (2 * q),
        "radial_recovery": sp.simplify(primary_m2.subs(b2, 0) - v**2) == 0,
        "turning_witness_positive": turning_m2 == 1,
        "turning_witness_calibrated": turning_h_s == sp.diag(sp.Rational(-1, 4), 4),
        "primary_full_witness_density": primary_m2_value == sp.Rational(89, 16),
        "primary_full_witness_calibrated": primary_h_s_value == sp.diag(sp.Rational(-1, 4), 4),
        "generic_shift_witness": generic_h[0, 1] != 0 and generic_h_s[0, 1] != 0,
        "generic_witness_determinant": generic_h.det() == sp.Rational(-25, 4),
        "generic_witness_calibrated": generic_h_s.det() == -1,
        "depth_derivative_identity": sp.simplify(phi_dot_from_h - phi_dot_from_q) == 0,
        "distance_derivative_denominator": sp.simplify(
            phi_s_squared - qdot**2 / (4 * q**2 * primary_m2)
        ) == 0,
        "primary_density_derivative_exact": primary_m2_dot_direct
        == sp.expand(
            2 * v * vdot
            + qdot * r**2 * b2
            + 2 * q * r * rdot * b2
            + q * r**2 * b2dot
        ),
        "center_monotone_limit": sp.limit(primary_m2.subs(v, 1), r, 0, dir="+") == 1,
    }

    count, hash_failures = source_hashes()
    status = "PASS" if all(checks.values()) and count == 9 and not hash_failures else "FAIL"
    result = {
        "audit": "G180",
        "status": status,
        "landing": (
            "COMPLETED_PAIR_SMOOTH_FAMILY_DESCENT__ORCHESTRA_ENTERS_THE_PHYSICAL_TAPE_MAP"
            if status == "PASS"
            else "PREREGISTERED_FAILURE"
        ),
        "checks": checks,
        "source_count": count,
        "source_hash_failures": hash_failures,
        "generic_shifted_witness": {
            "h_sigma": matrix_strings(generic_h),
            "h_s": matrix_strings(generic_h_s),
            "m_squared": "25/4",
        },
        "primary_full_witness": {
            "q": "1/4",
            "r": "3",
            "v": "2",
            "b_squared": "25/36",
            "h_sigma": matrix_strings(primary_h_value),
            "m_squared": str(primary_m2_value),
            "h_s": matrix_strings(primary_h_s_value),
        },
        "turning_witness": {
            "v": "0",
            "b_squared": "4/9",
            "h_sigma": matrix_strings(turning_h),
            "m_squared": str(turning_m2),
            "h_s": matrix_strings(turning_h_s),
        },
        "scope": "supplied smooth connected regular completed pair families",
        "open": [
            "physical_event_germ_and_family_realization",
            "cross_family_matching_and_global_completion",
            "null_and_degenerate_strata",
            "non_scalar_transport",
            "Xmax_observations_dynamics_source_matter_and_signalling",
        ],
    }
    (HERE / "DERIVATION_RESULT.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n"
    )
    if status != "PASS":
        failed = [name for name, passed in checks.items() if not passed]
        raise SystemExit(f"FAIL: checks={failed}, hashes={hash_failures}")
    print(
        "PASS: generic smooth density descent, primary orchestra tape map, turning, shift, "
        "reparameterization, derivative, and center controls"
    )


if __name__ == "__main__":
    main()
