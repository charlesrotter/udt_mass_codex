#!/usr/bin/env python3
"""Exact symbolic production derivation for G131."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent

EXPECTED_SOURCES = {
    "CURRENT_SCIENTIFIC_PREMISES.tsv",
    "UDT_RECIPROCAL_C_FOUNDING_POSTULATE_DERIVATION_RESULTS.md",
    "udt_uncompressed_pair_kernel_reconstruction_2026-08-14/EXACT_DERIVATION.md",
    "udt_g129_copresent_relational_network_faithfulness_2026-08-16/EXACT_DERIVATION.md",
    "udt_g130_copresence_rank_complete_network_ownership_2026-08-16/AUDIT_REPORT.md",
    "udt_g130_copresence_rank_complete_network_ownership_2026-08-16/EXACT_DERIVATION.md",
}


def source_hashes_match() -> bool:
    with (HERE / "SOURCE_MANIFEST.tsv").open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
    paths = [row["path"] for row in rows]
    return (
        len(rows) == 6
        and len(set(paths)) == 6
        and set(paths) == EXPECTED_SOURCES
        and all(
            hashlib.sha256((ROOT / row["path"]).read_bytes()).hexdigest() == row["sha256"]
            for row in rows
        )
    )


def q(metric: sp.Matrix, clock: sp.Matrix, ruler: sp.Matrix) -> sp.Expr:
    aa = (clock.T * metric * clock)[0]
    ab = (clock.T * metric * ruler)[0]
    bb = (ruler.T * metric * ruler)[0]
    return sp.factor((ab**2 - aa * bb) / aa**2)


def scalar_curvature(metric: sp.Matrix, coords: tuple[sp.Symbol, ...]) -> sp.Expr:
    n = len(coords)
    inverse = sp.simplify(metric.inv())
    gamma = [[[
        sp.simplify(
            sp.Rational(1, 2)
            * sum(
                inverse[k, ell]
                * (
                    sp.diff(metric[ell, j], coords[i])
                    + sp.diff(metric[ell, i], coords[j])
                    - sp.diff(metric[i, j], coords[ell])
                )
                for ell in range(n)
            )
        )
        for j in range(n)] for i in range(n)] for k in range(n)]
    ricci = sp.MutableDenseMatrix.zeros(n, n)
    for i in range(n):
        for j in range(n):
            ricci[i, j] = sp.simplify(
                sum(
                    sp.diff(gamma[k][i][j], coords[k])
                    - sp.diff(gamma[k][i][k], coords[j])
                    + sum(
                        gamma[k][k][ell] * gamma[ell][i][j]
                        - gamma[k][j][ell] * gamma[ell][i][k]
                        for ell in range(n)
                    )
                    for k in range(n)
                )
            )
    return sp.factor(
        sum(inverse[i, j] * ricci[i, j] for i in range(n) for j in range(n))
    )


def main() -> None:
    a, epsilon, lam = sp.symbols("a epsilon lambda", real=True, nonzero=True)
    b1, b2, b3 = sp.symbols("b1 b2 b3", real=True)
    x1, x2, x3 = sp.symbols("x1 x2 x3", real=True)
    b = sp.Matrix([b1, b2, b3])
    xvec = sp.Matrix([x1, x2, x3])
    norm2 = (xvec.T * xvec)[0]
    eta = sp.diag(-1, 1, 1, 1)
    e0 = sp.Matrix([1, 0, 0, 0])
    ruler = sp.Matrix([0, x1, x2, x3])

    # Equality for the fixed common clock e0 forces this exact Schur-complement family.
    C = b * b.T / a - a * sp.eye(3)
    candidate = sp.Matrix.vstack(
        sp.Matrix.hstack(sp.Matrix([[a]]), b.T),
        sp.Matrix.hstack(b, C),
    )
    fixed_clock_q = sp.factor(q(candidate, e0, ruler))
    eta_fixed_clock_q = sp.factor(q(eta, e0, ruler))

    # Tilt the clock in the same spatial direction. All-plane equality kills b exactly.
    tilted_clock = sp.Matrix([1, epsilon * x1, epsilon * x2, epsilon * x3])
    tilted_derivative = sp.factor(
        sp.diff(q(candidate, tilted_clock, ruler), epsilon).subs(epsilon, 0)
    )
    expected_derivative = sp.factor(-4 * norm2 * (b.dot(xvec)) / a)
    basis_derivatives = [
        sp.factor(tilted_derivative.subs({x1: int(i == 0), x2: int(i == 1), x3: int(i == 2)}))
        for i in range(3)
    ]
    expected_basis = [-4 * b1 / a, -4 * b2 / a, -4 * b3 / a]

    conformal_candidate = sp.simplify(candidate.subs({b1: 0, b2: 0, b3: 0}))
    conformal_factor = -a
    generic_clock = sp.Matrix(sp.symbols("t0:4"))
    generic_ruler = sp.Matrix(sp.symbols("r0:4"))
    generic_conformal_invariance = sp.factor(
        q(lam * eta, generic_clock, generic_ruler)
        - q(eta, generic_clock, generic_ruler)
    )

    # One-clock data alone has a larger shift family; a tilted clock detects it.
    shifted = candidate.subs({a: -2, b1: 1, b2: 0, b3: 0})
    one_clock_match = sp.simplify(
        q(shifted, e0, sp.Matrix([0, 2, 1, -1]))
        - q(eta, e0, sp.Matrix([0, 2, 1, -1]))
    )
    tilted_mismatch = sp.simplify(
        q(shifted, sp.Matrix([1, sp.Rational(1, 10), 0, 0]), sp.Matrix([0, 1, 0, 0]))
        - q(eta, sp.Matrix([1, sp.Rational(1, 10), 0, 0]), sp.Matrix([0, 1, 0, 0]))
    )

    # Smooth positive conformal witness: same Phi everywhere, different curvature.
    time, xpos, ypos, zpos = sp.symbols("time xpos ypos zpos", real=True)
    omega = 1 + xpos**2
    curved_conformal = omega**2 * eta
    curvature = scalar_curvature(curved_conformal, (time, xpos, ypos, zpos))

    founding = (ROOT / "UDT_RECIPROCAL_C_FOUNDING_POSTULATE_DERIVATION_RESULTS.md").read_text()
    kernel = (ROOT / "udt_uncompressed_pair_kernel_reconstruction_2026-08-14/EXACT_DERIVATION.md").read_text()
    g130 = (ROOT / "udt_g130_copresence_rank_complete_network_ownership_2026-08-16/AUDIT_REPORT.md").read_text()

    checks = {
        "source_hashes_match": source_hashes_match(),
        "lexical_foundation_cE_is_conversion_anchor": "reversible identity between temporal and spatial measure" in founding,
        "lexical_foundation_profile_remains_open": "does not yet derive a unique action, the profile" in founding,
        "lexical_terminal_formula_present": "phi_pair" in kernel and "(-det h)/h00^2" in kernel,
        "lexical_G130_scalar_depths_not_faithful": "Reciprocal depths alone are not faithful" in g130,
        "fixed_clock_family_matches_eta_exactly": sp.simplify(fixed_clock_q - eta_fixed_clock_q) == 0,
        "fixed_clock_q_is_spatial_norm": sp.simplify(fixed_clock_q - norm2) == 0,
        "tilted_derivative_exact": sp.simplify(tilted_derivative - expected_derivative) == 0,
        "three_basis_tilts_force_b_zero": all(
            sp.simplify(got - expected) == 0
            for got, expected in zip(basis_derivatives, expected_basis)
        ),
        "zero_b_candidate_is_positive_conformal_eta_when_a_negative": (
            sp.simplify(conformal_candidate - conformal_factor * eta) == sp.zeros(4)
        ),
        "positive_conformal_invariance_generic": generic_conformal_invariance == 0,
        "single_clock_nonconformal_shift_survives": one_clock_match == 0,
        "tilted_clock_detects_nonconformal_shift": tilted_mismatch != 0,
        "nonconstant_conformal_metric_differs_off_origin": sp.simplify(curved_conformal.subs(xpos, 1) - eta) != sp.zeros(4),
        "conformal_curvature_formula": sp.simplify(curvature + 12 / (1 + xpos**2) ** 3) == 0,
        "conformal_curvature_nonzero_at_origin": curvature.subs(xpos, 0) == -12,
        "common_scale_hidden_even_with_fixed_cE_symbol": sp.simplify(q(7 * eta, generic_clock, generic_ruler) - q(eta, generic_clock, generic_ruler)) == 0,
        "all_plane_result_is_certification_not_value_ownership": "certification domain" in g130 and "values open" in g130.lower(),
    }
    checks = {key: bool(value) for key, value in checks.items()}
    if not all(checks.values()):
        raise SystemExit(f"failed checks: {[key for key, value in checks.items() if not value]}")

    classification_rows = [
        {
            "datum": "one_fixed_clock_all_rulers",
            "kernel": "a_and_three_shift_components",
            "status": "NONCONFORMAL_KERNEL_SURVIVES",
        },
        {
            "datum": "shared_open_all_clock_ruler_planes",
            "kernel": "positive_common_conformal_factor",
            "status": "CONFORMAL_CLASS_FAITHFUL",
        },
        {
            "datum": "all_plane_Phi_plus_c_E_unit_anchor_only",
            "kernel": "positive_common_conformal_factor",
            "status": "COMMON_SCALE_NOT_REMOVED",
        },
        {
            "datum": "rank_complete_full_pullbacks_with_overlap",
            "kernel": "none_on_regular_covered_region",
            "status": "METRIC_FAITHFUL_BY_G129",
        },
    ]
    with (HERE / "KERNEL_CLASSIFICATION.tsv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=classification_rows[0].keys(), delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(classification_rows)

    result = {
        "status": "PASS",
        "landing": "ALL_PLANE_TERMINAL_SCALAR_CONFORMAL_FAITHFUL_ONLY__COMMON_SCALE_OPEN",
        "production_check_count": len(checks),
        "checks": checks,
        "fixed_clock_tilt_derivative": str(tilted_derivative),
        "tilted_shift_witness_mismatch": str(tilted_mismatch),
        "conformal_curvature": str(curvature),
        "maximum_conclusion": (
            "On a shared open regular all-plane certification domain, equality of terminal "
            "reciprocal scalars forces two Lorentz forms to differ by one positive pointwise "
            "conformal factor. The scalar is exactly blind to that common scale. Observed c_E "
            "calibrates clock-ruler units but does not supply the missing pointwise conformal datum."
        ),
    }
    (HERE / "DERIVATION_RESULT.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
