#!/usr/bin/env python3
"""Exact controller for the reciprocal-transport naturality audit."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parents[1]
PACKAGE = Path(__file__).resolve().parent


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_tsv(path: Path, key: str) -> dict[str, dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return {row[key]: row for row in csv.DictReader(handle, delimiter="\t")}


def verify_sources() -> tuple[bool, list[dict[str, object]]]:
    rows: list[dict[str, object]] = []
    with (PACKAGE / "SOURCE_MANIFEST.tsv").open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle, delimiter="\t"):
            path = ROOT / row["path"]
            actual = sha256(path)
            rows.append(
                {
                    "path": row["path"],
                    "expected_sha256": row["sha256"],
                    "actual_sha256": actual,
                    "match": actual == row["sha256"],
                }
            )
    return all(bool(row["match"]) for row in rows), rows


def connection_difference(a_cov: sp.Matrix, metric: sp.Matrix) -> list[list[list[sp.Expr]]]:
    """C(A)^a_bc = delta^a_b A_c + delta^a_c A_b - g_bc A^a."""
    n = metric.rows
    inverse = metric.inv()
    a_up = inverse * a_cov
    return [
        [
            [
                sp.simplify(
                    int(i == j) * a_cov[k]
                    + int(i == k) * a_cov[j]
                    - metric[j, k] * a_up[i]
                )
                for k in range(n)
            ]
            for j in range(n)
        ]
        for i in range(n)
    ]


def tensor_add(*tensors: list[list[list[sp.Expr]]]) -> list[list[list[sp.Expr]]]:
    n = len(tensors[0])
    return [
        [
            [sp.simplify(sum(tensor[i][j][k] for tensor in tensors)) for k in range(n)]
            for j in range(n)
        ]
        for i in range(n)
    ]


def tensor_scale(
    scalar: sp.Expr, tensor: list[list[list[sp.Expr]]]
) -> list[list[list[sp.Expr]]]:
    return [
        [[sp.simplify(scalar * entry) for entry in row] for row in plane]
        for plane in tensor
    ]


def tensor_zero(tensor: list[list[list[sp.Expr]]]) -> bool:
    return all(entry == 0 for plane in tensor for row in plane for entry in row)


def tensor_nonzero_count(tensor: list[list[list[sp.Expr]]]) -> int:
    return sum(entry != 0 for plane in tensor for row in plane for entry in row)


def mixed_projector(alpha_cov: sp.Matrix, metric: sp.Matrix) -> sp.Matrix:
    alpha_up = metric.inv() * alpha_cov
    norm = (alpha_cov.T * alpha_up)[0]
    return sp.simplify(alpha_up * alpha_cov.T / norm)


def solve_polynomial_conditions() -> dict[str, object]:
    p, a, x, y = sp.symbols("p a x y")
    coeffs = sp.symbols("a0:6")
    f = sum(coeffs[i] * p**i for i in range(len(coeffs)))
    fp = sp.diff(f, p)

    reversal_expr = sp.expand(-fp.subs(p, -p) - fp)
    reversal_solution = sp.solve(
        sp.Poly(reversal_expr, p).all_coeffs(), coeffs, dict=True
    )

    shift_expr = sp.expand(fp.subs(p, p + a) - fp)
    shift_poly = sp.Poly(shift_expr, p, a)
    shift_solution = sp.solve(shift_poly.coeffs(), coeffs, dict=True)

    f_x = f.subs(p, x)
    f_y = f.subs(p, y)
    f_xy = f.subs(p, x + y)
    character_expr = sp.expand(f_xy - f_x - f_y + coeffs[0])
    character_solution = sp.solve(
        sp.Poly(character_expr, x, y).coeffs(), coeffs, dict=True
    )

    combined_equations = (
        sp.Poly(reversal_expr, p).all_coeffs() + shift_poly.coeffs()
    )
    combined_solution = sp.solve(combined_equations, coeffs, dict=True)

    return {
        "degree": 5,
        "strict_reversal_solution": [str(item) for item in reversal_solution],
        "strict_reversal_free_coefficients": ["a0", "a2", "a4"],
        "local_shift_solution": [str(item) for item in shift_solution],
        "local_shift_free_coefficients": ["a0", "a1"],
        "regular_character_solution": [str(item) for item in character_solution],
        "regular_character_free_coefficients": ["a0", "a1"],
        "shift_plus_strict_reversal_solution": [
            str(item) for item in combined_solution
        ],
        "shift_plus_strict_reversal_connection": "Gamma0",
        "checks": {
            "strict_reversal_leaves_only_even_nonconstant_terms": reversal_solution
            == [{coeffs[1]: 0, coeffs[3]: 0, coeffs[5]: 0}],
            "local_shift_leaves_only_affine_f": shift_solution
            == [
                {
                    coeffs[2]: 0,
                    coeffs[3]: 0,
                    coeffs[4]: 0,
                    coeffs[5]: 0,
                }
            ],
            "regular_character_leaves_only_affine_f": character_solution
            == [
                {
                    coeffs[2]: 0,
                    coeffs[3]: 0,
                    coeffs[4]: 0,
                    coeffs[5]: 0,
                }
            ],
            "shift_and_reversal_leave_constant_f": combined_solution
            == [
                {
                    coeffs[1]: 0,
                    coeffs[2]: 0,
                    coeffs[3]: 0,
                    coeffs[4]: 0,
                    coeffs[5]: 0,
                }
            ],
        },
    }


def source_authority() -> dict[str, object]:
    ontology = read_tsv(
        ROOT / "udt_phi_metric_ontology_audit_2026-07-22/PHI_ONTOLOGY_LEDGER.tsv",
        "id",
    )
    conflicts = read_tsv(
        ROOT
        / "udt_phi_metric_ontology_audit_2026-07-22/SEMANTIC_CONFLICT_LEDGER.tsv",
        "conflict_id",
    )
    parent = read_tsv(
        ROOT / "udt_csn_dphi_transport_selector_audit_2026-07-23/STATUS_LEDGER.tsv",
        "id",
    )
    cold = (ROOT / "UDT_NATIVE_ACTION_COLD_PACKET.md").read_text(encoding="utf-8")
    cold_words = " ".join(cold.split())

    checks = {
        "universal_phi_transformation_not_derived": ontology["O05"]["ruling"]
        == "NOT_DERIVED",
        "local_phi_shift_not_CSN_gauge": "not derived as CSN gauge"
        in conflicts["C03"]["provenance_disposition"],
        "group_depth_local_field_map_open": conflicts["C02"]["controlling_ruling"].endswith(
            "OPEN"
        ),
        "static_seal_scope_only": ontology["O15"]["ruling"]
        == "CANONIZED_BINDING_STATIC_SCOPE",
        "static_seal_no_eom": ontology["O16"]["ruling"] == "NOT_DERIVED",
        "bootstrap_no_realization_operator": ontology["O17"]["ruling"]
        == "NOT_PRESENT_IN_CURRENT_FOUNDATION",
        "complete_native_equation_open": ontology["O18"]["ruling"]
        == "OPEN_NOT_DERIVED",
        "reversal_and_seal_counterfamily_parent_verified": parent["S07"]["status"]
        == "REFUTED",
        "split_connection_uniqueness_parent_refuted": parent["S14"]["status"].startswith(
            "REFUTED"
        ),
        "physical_connection_selector_parent_open": parent["S21"]["status"] == "OPEN",
        "bootstrap_explicitly_not_local_equation": (
            "This principle is a global selection requirement, not a ready-made local field equation, action, or carrier."
            in cold_words
        ),
    }

    return {
        "checks": checks,
        "all_checks_pass": all(checks.values()),
        "registered": {
            "CSN": True,
            "relative_composition": True,
            "reciprocal_group_reversal": True,
            "static_seal_phi_zero": True,
        },
        "not_registered_as_local_selector": {
            "local_phi_shift_gauge": True,
            "strict_affine_connection_invariance_under_reversal": True,
            "torsion_free_transport": True,
            "zero_stabilizer_addition": True,
            "bootstrap_local_connection_operator": True,
            "seal_bulk_connection_rule": True,
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    sources_ok, sources = verify_sources()

    p, dp, lam, kappa, sigma = sp.symbols("phi dphi lambda kappa sigma")
    s, gscale, omega = sp.symbols("s gscale omega", positive=True)

    h0 = sp.simplify(s * gscale)
    s_bar = sp.exp(-2 * sigma) * s
    g_bar = sp.exp(2 * sigma) * gscale
    h0_bar = sp.simplify(s_bar * g_bar)

    metric = sp.diag(-2, 3, 5, 7)
    metric_bar = 11 * metric
    a_cov = sp.Matrix([2, -3, 4, 1])
    dsigma_cov = sp.Matrix([1, 2, -1, 3])
    csn_connection_residual = tensor_add(
        connection_difference(dsigma_cov, metric),
        connection_difference(a_cov - dsigma_cov, metric_bar),
        tensor_scale(-1, connection_difference(a_cov, metric)),
    )

    f_even = lam * p**2 + sp.Symbol("mu") * p**4
    b_even = sp.diff(f_even, p) * dp
    b_even_reversed = -sp.diff(f_even, p).subs(p, -p) * dp
    b_even_seal = sp.simplify(b_even.subs(p, 0))

    witness_phi = sp.Rational(2, 3)
    witness_lambda = sp.Rational(5, 7)
    witness_dphi = sp.Matrix([1, -2, 3, 1])
    witness_b = 2 * witness_lambda * witness_phi * witness_dphi
    witness_connection_difference = connection_difference(witness_b, metric)

    derivative_b = lam * dp
    derivative_b_reversed = -lam * dp

    alpha_cov = sp.Matrix([1, 2, -1, 3])
    q = sp.symbols("q", nonzero=True)
    projector = mixed_projector(alpha_cov, metric)
    projector_rescaled = mixed_projector(q * alpha_cov, metric)
    projector_difference = sp.simplify(projector_rescaled - projector)

    polynomial = solve_polynomial_conditions()
    authority = source_authority()

    checks = {
        "source_manifest_matches": sources_ok,
        "source_authority_checks_pass": authority["all_checks_pass"],
        "CSN_h0_invariant": sp.simplify(h0_bar - h0) == 0,
        "CSN_Weyl_connection_invariant": tensor_zero(csn_connection_residual),
        "even_f_strict_reversal_invariant": sp.simplify(
            b_even_reversed - b_even
        )
        == 0,
        "even_f_matches_Gamma0_at_static_seal": b_even_seal == 0,
        "even_f_bulk_connection_distinct": tensor_nonzero_count(
            witness_connection_difference
        )
        > 0,
        "derivative_family_reversal_is_covariant_lambda_flip": sp.simplify(
            derivative_b_reversed - derivative_b.subs(lam, -lam)
        )
        == 0,
        "derivative_family_strict_reversal_selects_lambda_zero": sp.solve(
            sp.Eq(derivative_b_reversed, derivative_b), lam
        )
        == [0],
        "same_projector_under_nonzero_rescaling": projector_difference
        == sp.zeros(4),
        "nonlinear_reparameterization_changes_A0_by_kappa_dphi": sp.simplify(
            sp.diff(sp.log(sp.exp(kappa * p)), p) * dp - kappa * dp
        )
        == 0,
        "linear_group_coordinate_rescaling_leaves_A0": sp.diff(
            sp.log(sp.Symbol("a", positive=True)), p
        )
        == 0,
        **polynomial["checks"],
    }

    result = {
        "schema": "udt-reciprocal-transport-naturality-v1",
        "sympy_version": sp.__version__,
        "source_manifest": sources,
        "source_authority": authority,
        "checks": checks,
        "all_checks_pass": all(checks.values()),
        "csn": {
            "s_transformation": "sbar=Omega^-2 s",
            "h0_transformation": "h0bar=h0",
            "A0_transformation": "A0bar=A0-dlogOmega",
            "Gamma_f_invariant_for_every_smooth_f": True,
        },
        "full_phi_family": {
            "family": "Gamma_f=LC(exp(2f(phi))*h0)",
            "strict_reversal_condition": "f'(-phi)=-f'(phi), equivalently f even up to a constant",
            "counterfamily": "f(phi)=lambda*phi^2+mu*phi^4",
            "counterfamily_matches_Gamma0_at_static_seal": True,
            "bulk_witness_nonzero_connection_components": tensor_nonzero_count(
                witness_connection_difference
            ),
        },
        "polynomial_classification": polynomial,
        "derivative_only_family": {
            "family": "A_lambda=A0+lambda*dphi",
            "under_reversal_covariance": "lambda maps to -lambda",
            "strict_reversal_invariance": "lambda=0",
            "current_authority_for_strict_invariance": "NOT_DERIVED",
        },
        "projector_only": {
            "P_under_dphi_to_q_dphi": "unchanged",
            "reparameterization": "F'(phi)=exp(kappa*phi)>0",
            "A0_change": "A0bar-A0=kappa*dphi",
            "conclusion": "the oriented or unoriented line/projector alone does not determine A0",
        },
        "group_coordinate": {
            "additive_automorphism": "phibar=a*phi with constant nonzero a",
            "A0_change": "zero",
            "nonlinear_monotone_reparameterization_preserves_group_law": False,
            "composition_is_not_local_shift_gauge": True,
        },
        "conditional_theorem": {
            "scope": "Gamma_f Levi-Civita/Weyl counterfamily only",
            "extra_assumptions": [
                "local phi-shift invariance",
                "strict affine-connection invariance under reciprocal reversal",
            ],
            "result": "Gamma_f=Gamma0",
            "status": "UNIQUE_CONDITIONAL",
            "does_not_remove_independent_stabilizer_connection_data": True,
        },
        "selector_adjudication": {
            "registered_sources_select_Gamma0": False,
            "registered_sources_select_projected_connection": False,
            "exact_surviving_counterfamily": "all smooth even f with f'(0)=0, including lambda*phi^2",
            "status": "OPEN_SELECTOR",
            "remaining_smallest_datum": "a typed native transport/naturality law specifying which phi data and which reversal action are physical",
        },
        "scope_exclusions": [
            "null dphi",
            "zero dphi",
            "global branch continuation",
            "action",
            "carrier or Hopfion",
            "source",
            "boundary charge",
            "physical time evolution",
        ],
    }

    if not result["all_checks_pass"]:
        failed = [name for name, passed in checks.items() if not passed]
        raise SystemExit(f"one or more exact controller checks failed: {failed}")
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")


if __name__ == "__main__":
    main()
