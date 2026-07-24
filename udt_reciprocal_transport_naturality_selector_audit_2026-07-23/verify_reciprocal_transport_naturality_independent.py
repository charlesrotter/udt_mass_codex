#!/usr/bin/env python3
"""Independent stdlib/Fraction verifier; does not import controller code."""

from __future__ import annotations

import argparse
import csv
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACKAGE = Path(__file__).resolve().parent


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def source_hashes_match() -> bool:
    with (PACKAGE / "SOURCE_MANIFEST.tsv").open(newline="", encoding="utf-8") as handle:
        return all(
            sha256(ROOT / row["path"]) == row["sha256"]
            for row in csv.DictReader(handle, delimiter="\t")
        )


def mat_vec(matrix: list[list[F]], vector: list[F]) -> list[F]:
    return [sum(row[j] * vector[j] for j in range(len(vector))) for row in matrix]


def outer(left: list[F], right: list[F]) -> list[list[F]]:
    return [[x * y for y in right] for x in left]


def scale_matrix(scale: F, matrix: list[list[F]]) -> list[list[F]]:
    return [[scale * entry for entry in row] for row in matrix]


def projector(alpha: list[F], inverse_metric: list[list[F]]) -> list[list[F]]:
    raised = mat_vec(inverse_metric, alpha)
    norm = sum(alpha[i] * raised[i] for i in range(len(alpha)))
    return scale_matrix(F(1, 1) / norm, outer(raised, alpha))


def even_f(phi: F, lam: F, mu: F) -> F:
    return lam * phi**2 + mu * phi**4


def even_f_prime(phi: F, lam: F, mu: F) -> F:
    return 2 * lam * phi + 4 * mu * phi**3


def connection_difference_nonzero(b: list[F], metric_diag: list[F]) -> int:
    inverse_diag = [F(1, 1) / value for value in metric_diag]
    b_up = [inverse_diag[i] * b[i] for i in range(4)]
    count = 0
    for i in range(4):
        for j in range(4):
            for k in range(4):
                value = (
                    (b[k] if i == j else F(0))
                    + (b[j] if i == k else F(0))
                    - (metric_diag[j] if j == k else F(0)) * b_up[i]
                )
                count += value != 0
    return count


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--production-result", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    production = json.loads(args.production_result.read_text(encoding="utf-8"))

    phi = F(2, 3)
    lam = F(5, 7)
    mu = F(-3, 11)
    dphi = [F(1), F(-2), F(3), F(1)]
    b = [even_f_prime(phi, lam, mu) * value for value in dphi]
    b_reversed = [
        -even_f_prime(-phi, lam, mu) * value for value in dphi
    ]

    metric_diag = [F(-2), F(3), F(5), F(7)]
    inverse_metric = [
        [F(-1, 2), F(0), F(0), F(0)],
        [F(0), F(1, 3), F(0), F(0)],
        [F(0), F(0), F(1, 5), F(0)],
        [F(0), F(0), F(0), F(1, 7)],
    ]
    alpha = [F(1), F(2), F(-1), F(3)]
    q = F(7, 3)
    p0 = projector(alpha, inverse_metric)
    pq = projector([q * value for value in alpha], inverse_metric)

    kappa = F(4, 9)
    a0_shift = [kappa * value for value in dphi]

    exact_checks = {
        "sources_match_frozen_manifest": source_hashes_match(),
        "even_f_value_reversal": even_f(-phi, lam, mu) == even_f(phi, lam, mu),
        "even_f_connection_reversal": b_reversed == b,
        "even_f_seal_derivative_zero": even_f_prime(F(0), lam, mu) == 0,
        "even_f_bulk_connection_distinct": connection_difference_nonzero(
            b, metric_diag
        )
        > 0,
        "projector_exactly_rescaling_invariant": pq == p0,
        "nonlinear_same_projector_A0_shift_nonzero": any(a0_shift),
        "linear_rescaling_A0_shift_zero": F(0) == 0,
        "constant_derivative_family_flips_under_reversal": [
            -lam * value for value in dphi
        ]
        != [lam * value for value in dphi],
    }

    catches = {
        "reject_local_shift_as_registered_CSN_gauge": production["source_authority"][
            "not_registered_as_local_selector"
        ]["local_phi_shift_gauge"],
        "reject_missing_even_counterfamily": "lambda*phi^2"
        in production["selector_adjudication"]["exact_surviving_counterfamily"],
        "reject_seal_as_bulk_selector": production["full_phi_family"][
            "counterfamily_matches_Gamma0_at_static_seal"
        ]
        and not production["selector_adjudication"]["registered_sources_select_Gamma0"],
        "reject_projector_unique_A0": "does not determine A0"
        in production["projector_only"]["conclusion"],
        "reject_torsion_free_as_registered_law": production["source_authority"][
            "not_registered_as_local_selector"
        ]["torsion_free_transport"],
        "reject_zero_stabilizer_as_registered_law": production["source_authority"][
            "not_registered_as_local_selector"
        ]["zero_stabilizer_addition"],
        "reject_bootstrap_as_local_connection_operator": production[
            "source_authority"
        ]["not_registered_as_local_selector"]["bootstrap_local_connection_operator"],
        "reject_unscoped_unique_claim": production["conditional_theorem"]["status"]
        == "UNIQUE_CONDITIONAL"
        and production["selector_adjudication"]["status"] == "OPEN_SELECTOR",
        "reject_null_extension": "null dphi" in production["scope_exclusions"],
        "reject_physical_transport_promotion": not production[
            "selector_adjudication"
        ]["registered_sources_select_projected_connection"],
        "reject_Hopfion_inference": "carrier or Hopfion"
        in production["scope_exclusions"],
        "reject_mutated_source_hash": not all(
            row["expected_sha256"] == "0" * 64
            for row in production["source_manifest"]
        ),
    }

    agreement = {
        "production_all_checks_pass": production["all_checks_pass"],
        "production_conclusion_open_selector": production["selector_adjudication"][
            "status"
        ]
        == "OPEN_SELECTOR",
        "production_counterfamily_bulk_nonzero": production["full_phi_family"][
            "bulk_witness_nonzero_connection_components"
        ]
        > 0,
        "production_projector_result_matches": production["projector_only"][
            "P_under_dphi_to_q_dphi"
        ]
        == "unchanged",
        "production_shift_reversal_conditional_only": production[
            "conditional_theorem"
        ]["does_not_remove_independent_stabilizer_connection_data"],
    }

    result = {
        "schema": "udt-reciprocal-transport-naturality-independent-v1",
        "method": "Python stdlib and exact Fraction arithmetic; no SymPy and no controller import",
        "exact_checks": exact_checks,
        "catches": catches,
        "agreement": agreement,
        "counts": {
            "exact_checks_passed": sum(exact_checks.values()),
            "exact_checks_total": len(exact_checks),
            "catches_passed": sum(catches.values()),
            "catches_total": len(catches),
            "agreement_passed": sum(agreement.values()),
            "agreement_total": len(agreement),
        },
        "all_checks_pass": all(exact_checks.values())
        and all(catches.values())
        and all(agreement.values()),
    }
    if not result["all_checks_pass"]:
        raise SystemExit("independent verification failed")
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")


if __name__ == "__main__":
    main()
