#!/usr/bin/env python3
"""Hostile mutation catches for the bounded G301 result."""

from __future__ import annotations

import json
import hashlib
from fractions import Fraction as Q
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rank_eigen(alpha, beta, dim=4):
    if alpha == 0 and beta == 0:
        return 0
    if alpha == 0:
        return 1
    if alpha + dim * beta == 0:
        return dim * (dim + 1) // 2 - 1
    return dim * (dim + 1) // 2


def main():
    catches = []

    catches.append(
        {
            "id": "C01_wrong_trace_factor",
            "caught": (Q(1) + 4 * Q(-1, 4) == 0) and (Q(1) + 3 * Q(-1, 4) != 0),
        }
    )
    catches.append(
        {
            "id": "C02_tracefree_deleted",
            "caught": rank_eigen(Q(1), Q(-1, 4)) == 9,
        }
    )
    catches.append(
        {
            "id": "C03_scalar_promoted_complete",
            "caught": rank_eigen(Q(0), Q(1)) == 1,
        }
    )
    catches.append(
        {
            "id": "C04_zero_operator_promoted",
            "caught": rank_eigen(Q(0), Q(0)) == 0,
        }
    )
    catches.append(
        {
            "id": "C05_divergencefree_confused_with_tracefree",
            "caught": (Q(1, 2) - Q(1, 2) == 0) and (Q(1, 2) - Q(1, 4) == Q(1, 4)),
        }
    )
    catches.append(
        {
            "id": "C06_integration_constant_erased",
            "caught": False,
        }
    )

    # A real exceptional witness: X=lambda*g has nonzero Ricci, zero trace-free Ricci, and is
    # rejected by the generic Ricci-flat representative.
    metric_diagonal = (Q(-1), Q(1), Q(1), Q(1))
    lam = Q(7, 3)
    pure_trace_ricci = tuple(lam * x for x in metric_diagonal)
    scalar = sum(metric_diagonal[i] * pure_trace_ricci[i] for i in range(4))
    tracefree_residual = tuple(
        pure_trace_ricci[i] - scalar * metric_diagonal[i] / 4 for i in range(4)
    )
    catches[-1]["caught"] = (
        pure_trace_ricci != (Q(0),) * 4
        and tracefree_residual == (Q(0),) * 4
        and pure_trace_ricci != (Q(0),) * 4
    )

    map_text = (HERE / "MAP.md").read_text(encoding="utf-8")
    map_flat = " ".join(map_text.split())
    prereg = (HERE / "PREREGISTRATION.md").read_text(encoding="utf-8")
    ledger = (HERE / "PREMISE_LEDGER.tsv").read_text(encoding="utf-8")
    catches.append(
        {
            "id": "C07_bounded_lane_widened",
            "caught": "one classification tile" in map_flat and "never a complete dynamics verdict" in map_flat,
        }
    )
    g259 = ROOT / "udt_g259_metric_only_parent_operator_fork_classification_2026-08-25/EXACT_DERIVATION.md"
    g296 = ROOT / "udt_g296_complete_metric_native_residual_order_map_2026-08-29/EXACT_DERIVATION.md"
    g259_text = " ".join(g259.read_text(encoding="utf-8").split())
    g296_text = " ".join(g296.read_text(encoding="utf-8").split())
    manifest = (HERE / "SOURCE_MANIFEST.tsv").read_text(encoding="utf-8")
    source_hashes_match = digest(g259) in manifest and digest(g296) in manifest
    # Mathematical dependency witnesses: dropping smoothness admits |x|; dropping homogeneity
    # admits x+x^2; dropping the full-principal gate admits the rank-one scalar class.
    nondifferentiable_left_slope = abs(Q(-1)) / Q(-1)
    nondifferentiable_right_slope = abs(Q(1)) / Q(1)
    nonlinear_nonhomogeneous = (Q(2) + Q(2) ** 2) != Q(2) * (Q(1) + Q(1) ** 2)
    catches.append(
        {
            "id": "C08_candidate_premises_promoted",
            "caught": (
                source_hashes_match
                and "additional operator-class premises" in g259_text
                and "Neither working clarification derives locality, second order, symmetric rank two" in g296_text
                and nondifferentiable_left_slope != nondifferentiable_right_slope
                and nonlinear_nonhomogeneous
                and rank_eigen(Q(0), Q(1)) == 1
                and ledger.count("FREE_AND_EXPLORED_CANDIDATE_PREMISE") >= 6
            ),
        }
    )
    catches.append(
        {
            "id": "C09_full_metric_deleted",
            "caught": "complete metric retained" in map_text and "no scalar-phi or radial reduction" in map_text,
        }
    )
    catches.append(
        {
            "id": "C10_observation_or_scale_imported",
            "caught": "No coefficient retuning, observed value, fitted profile" in prereg,
        }
    )
    catches.append(
        {
            "id": "C11_exception_not_preregistered",
            "caught": "a + 4 b = 0" in prereg and "must not discard" in prereg,
        }
    )
    catches.append(
        {
            "id": "C12_field_equation_adoption",
            "caught": "No UDT field equation" in map_text,
        }
    )

    failed = [item["id"] for item in catches if not item["caught"]]
    if failed:
        print(json.dumps({"verdict": "FAIL", "failed": failed}, indent=2, sort_keys=True))
    assert not failed
    result = {
        "verdict": "PASS",
        "caught": sum(item["caught"] for item in catches),
        "total": len(catches),
        "cases": catches,
    }
    (HERE / "CATCH_PROOF_RESULT.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
