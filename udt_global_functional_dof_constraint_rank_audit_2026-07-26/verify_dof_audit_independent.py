#!/usr/bin/env python3
"""Independent stdlib reconstruction of the load-bearing local ranks."""

from __future__ import annotations

import csv
import hashlib
import json
from fractions import Fraction
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def matrix_rank(rows: list[list[int]]) -> int:
    a = [[Fraction(value) for value in row] for row in rows if any(row)]
    if not a:
        return 0
    rank = 0
    columns = len(a[0])
    for col in range(columns):
        pivot = next((i for i in range(rank, len(a)) if a[i][col]), None)
        if pivot is None:
            continue
        a[rank], a[pivot] = a[pivot], a[rank]
        scale = a[rank][col]
        a[rank] = [value / scale for value in a[rank]]
        for i in range(len(a)):
            if i != rank and a[i][col]:
                factor = a[i][col]
                a[i] = [x - factor * y for x, y in zip(a[i], a[rank])]
        rank += 1
        if rank == len(a):
            break
    return rank


def unit_equation(coefficients: dict[int, int], width: int = 16) -> list[int]:
    row = [0] * width
    for index, value in coefficients.items():
        row[index] += value
    return row


def idx(i: int, j: int) -> int:
    return 4 * i + j


def symmetric_matrix_nullity() -> int:
    equations = []
    for i in range(4):
        for j in range(i + 1, 4):
            equations.append(unit_equation({idx(i, j): 1, idx(j, i): -1}))
    return 16 - matrix_rank(equations)


def lorentz_lie_algebra_nullity() -> int:
    eta = [-1, 1, 1, 1]
    equations = []
    # (eta X + X^T eta)_ij = eta_i X_ij + eta_j X_ji.
    for i in range(4):
        for j in range(4):
            equations.append(unit_equation({idx(i, j): eta[i], idx(j, i): eta[j]}))
    return 16 - matrix_rank(equations)


def projector_tangent_nullity() -> int:
    # At P=diag(1,1,0,0), impose X=X^T and P X + X P = X.
    p = [1, 1, 0, 0]
    equations = []
    for i in range(4):
        for j in range(i + 1, 4):
            equations.append(unit_equation({idx(i, j): 1, idx(j, i): -1}))
    for i in range(4):
        for j in range(4):
            equations.append(unit_equation({idx(i, j): p[i] + p[j] - 1}))
    return 16 - matrix_rank(equations)


def main() -> None:
    checks: list[tuple[str, bool, str]] = []

    for manifest in ("SOURCE_MANIFEST.tsv", "SOURCE_MANIFEST_CORRECTION.tsv"):
        for row in read_tsv(HERE / manifest):
            path = ROOT / row["path"]
            checks.append(
                (
                    f"source_{row['source_id']}",
                    path.is_file() and str(path.stat().st_size) == row["bytes"] and sha256(path) == row["sha256"],
                    row["path"],
                )
            )

    symmetric = symmetric_matrix_nullity()
    lorentz = lorentz_lie_algebra_nullity()
    projector = projector_tangent_nullity()
    metric_quotient = symmetric - 4
    coframe_quotient = 16 - lorentz - 4
    split = 3 + 3 + 4

    checks.extend(
        [
            ("symmetric_metric_nullity", symmetric == 10, str(symmetric)),
            ("lorentz_lie_algebra_nullity", lorentz == 6, str(lorentz)),
            ("metric_quotient", metric_quotient == 6, str(metric_quotient)),
            ("coframe_quotient", coframe_quotient == 6, str(coframe_quotient)),
            ("two_plus_two_chart", split == 10, str(split)),
            ("chosen_comparison_scalar_total", metric_quotient + 1 == 7, str(metric_quotient + 1)),
            ("counterfactual_local_csn_arithmetic", metric_quotient - 1 == 5, str(metric_quotient - 1)),
            ("rank_two_projector_tangent", projector == 4, str(projector)),
        ]
    )

    presentations = {row["id"]: row for row in read_tsv(HERE / "LOCAL_PRESENTATION_RANK.tsv")}
    branches = read_tsv(HERE / "REALIZATION_BRANCH_RANK.tsv")
    completions = read_tsv(HERE / "COMPLETION_DOF_ATLAS.tsv")
    derived = read_tsv(HERE / "DERIVED_OBJECT_NO_DOUBLE_COUNT.tsv")
    status = {row["id"]: row for row in read_tsv(HERE / "STATUS_LEDGER.tsv")}

    checks.extend(
        [
            ("presentation_metric", presentations["P01"]["quotient_signature"] == "F4[6]", presentations["P01"]["quotient_signature"]),
            ("presentation_coframe", presentations["P02"]["quotient_signature"] == "F4[6]", presentations["P02"]["quotient_signature"]),
            ("comparison_scalar_count", presentations["P04"]["quotient_signature"] == "F4[7]", presentations["P04"]["quotient_signature"]),
            ("comparison_scalar_scope", presentations["P04"]["status"] == "CHOSE_COMPARISON_CONFIGURATION", presentations["P04"]["status"]),
            ("founded_phi_scope", presentations["P05"]["status"] == "DERIVED_FOUNDED_SUBGROUP__FULL_EXTENSION_OPEN", presentations["P05"]["status"]),
            ("csn_inactive", presentations["P06"]["status"] == "INACTIVE_COUNTERFACTUAL_REQUIRES_EXPLICIT_REAUTHORIZATION", presentations["P06"]["status"]),
            ("presentation_projector", presentations["P08"]["quotient_signature"] == "F4[10]", presentations["P08"]["quotient_signature"]),
            ("seven_branches", [row["branch_id"] for row in branches] == [f"C0{i}" for i in range(1, 8)], str(len(branches))),
            ("twelve_completions", len(completions) == 12 and len({row["completion_id"] for row in completions}) == 12, str(len(completions))),
            ("none_selected", all(row["selected"] == "NO" for row in branches + completions), "all NO"),
            ("derived_inventory", len(derived) == 14, str(len(derived))),
            ("maxwell_scoped", status["S12"]["status"] == "F_EQUALS_dS_AND_dF_EQUALS_ZERO_ONLY_CONDITIONAL_TORIC", status["S12"]["status"]),
            ("modes_not_evaluable", status["S14"]["status"] == "NOT_EVALUABLE", status["S14"]["status"]),
            ("closure_type", status["S13"]["status"] == "FOUNDED_COMPLETE_EXTENSION_AND_VARIATION_DOMAIN_THEN_RESPONSE_AND_GLOBAL_BOUNDARY", status["S13"]["status"]),
            ("native_rank_open", status["S15"]["status"] == "CORRECTED_GENERIC_ARENA_RANK_CHARACTERIZED__NATIVE_FOUNDED_EXTENSION_RANK_OPEN", status["S15"]["status"]),
        ]
    )

    failed = [name for name, ok, _ in checks if not ok]
    result = {
        "implementation": "independent_fraction_linear_constraints_no_production_import",
        "status": "PASS" if not failed else "FAIL",
        "checks": len(checks),
        "failed": failed,
        "reconstructed": {
            "symmetric_metric": symmetric,
            "local_lorentz": lorentz,
            "metric_quotient": metric_quotient,
            "coframe_quotient": coframe_quotient,
            "rank_two_projector": projector,
            "chosen_comparison_scalar_total": metric_quotient + 1,
            "counterfactual_local_csn_arithmetic": metric_quotient - 1,
        },
        "details": [{"check": name, "pass": ok, "detail": detail} for name, ok, detail in checks],
    }
    (HERE / "INDEPENDENT_VERIFICATION_RESULT.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    if failed:
        raise SystemExit("independent verification failed: " + ", ".join(failed))
    print(json.dumps({"status": "PASS", "checks": len(checks), "reconstructed": result["reconstructed"]}, sort_keys=True))


if __name__ == "__main__":
    main()
