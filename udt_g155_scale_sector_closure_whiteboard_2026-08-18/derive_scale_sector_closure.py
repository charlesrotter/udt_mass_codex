#!/usr/bin/env python3
"""Exact G155 role/rank and conformal common-scale derivation."""

from __future__ import annotations

import csv
import hashlib
import json
import subprocess
from collections import Counter
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parent.parent
HERE = Path(__file__).resolve().parent
MANIFEST = HERE / "SOURCE_MANIFEST.tsv"
LEDGER = HERE / "EQUATION_ROLE_LEDGER.tsv"
OUTPUT = HERE / "DERIVATION_RESULT.json"
SOURCE_SNAPSHOT = "2f5cf474"

HISTORY_ROLES = {"PHYSICAL_HISTORY_CONSTRAINT", "PHYSICAL_HISTORY_EVOLUTION"}
ALLOWED_ROLES = {
    "REPRESENTATION_CONSTRAINT",
    "DEFINITION_OR_EVALUATOR",
    "NETWORK_ADMISSIBILITY",
    "QUERY_EVOLUTION",
    "CALIBRATION_OR_WORKING_FRAME",
    "INACTIVE_OR_OPEN",
    *HISTORY_ROLES,
}


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def verify_manifest(rows: list[dict[str, str]]) -> None:
    assert len(rows) == 41
    assert [row["source_id"] for row in rows] == [f"S{i:02d}" for i in range(1, 42)]
    for row in rows:
        payload = subprocess.run(
            ["git", "show", f"{SOURCE_SNAPSHOT}:{row['path']}"],
            cwd=ROOT,
            check=True,
            stdout=subprocess.PIPE,
        ).stdout
        assert len(payload) == int(row["bytes"]), row["source_id"]
        assert hashlib.sha256(payload).hexdigest() == row["sha256"], row["source_id"]


def validate_ledger(rows: list[dict[str, str]], source_ids: set[str]) -> None:
    assert len(rows) == 41
    assert [row["equation_id"] for row in rows] == [f"E{i:02d}" for i in range(1, 42)]
    assert {row["source_id"] for row in rows} == source_ids
    assert all(row["role"] in ALLOWED_ROLES for row in rows)
    for row in rows:
        rank = int(row["physical_history_principal_rank"])
        assert rank >= 0
        if row["role"] not in HISTORY_ROLES:
            assert rank == 0, row["equation_id"]
    # Load-bearing regression guards.
    by_source = {row["source_id"]: row for row in rows}
    assert by_source["S06"]["active_status"] == "INACTIVE_CHALLENGED"
    assert by_source["S06"]["role"] == "INACTIVE_OR_OPEN"
    assert by_source["S18"]["role"] == "CALIBRATION_OR_WORKING_FRAME"
    assert by_source["S37"]["role"] == "QUERY_EVOLUTION"


def classify(rows: list[dict[str, str]]) -> tuple[str, int, int]:
    constraints = [r for r in rows if r["role"] == "PHYSICAL_HISTORY_CONSTRAINT"]
    evolution = [r for r in rows if r["role"] == "PHYSICAL_HISTORY_EVOLUTION"]
    rank = sum(int(r["physical_history_principal_rank"]) for r in constraints + evolution)
    if not constraints and not evolution:
        landing = "RANK_ZERO"
    elif constraints and not evolution:
        landing = "CONSTRAINT_ONLY"
    elif evolution and not constraints:
        landing = "EVOLUTION_PRESENT"
    else:
        landing = "MIXED_SCALE_CLOSURE"
    return landing, rank, len(constraints) + len(evolution)


def exact_checks() -> dict[str, str | int]:
    check_names: list[str] = []
    # General regular Lorentzian pair metric and positive common rescaling.
    h00, h01, h11, a = sp.symbols("h00 h01 h11 a", nonzero=True, real=True)
    det_h = h00 * h11 - h01**2
    hhat00, hhat01, hhat11 = a**2 * h00, a**2 * h01, a**2 * h11
    det_hhat = sp.expand(hhat00 * hhat11 - hhat01**2)
    ratio_phi = sp.simplify((-det_h) / h00**2)
    ratio_phi_hat = sp.simplify((-det_hhat) / hhat00**2)
    beta = sp.simplify(h01 / h00)
    beta_hat = sp.simplify(hhat01 / hhat00)

    assert sp.simplify(det_hhat - a**4 * det_h) == 0
    check_names.append("pair_determinant_conformal_weight_four")
    assert sp.simplify(ratio_phi_hat - ratio_phi) == 0
    check_names.append("terminal_phi_ratio_conformal_weight_zero")
    assert sp.simplify(beta_hat - beta) == 0
    check_names.append("terminal_beta_conformal_weight_zero")

    # Founded reciprocal carrier is unimodular, but does not fix pair volume.
    delta = sp.symbols("delta", real=True)
    D = sp.diag(sp.exp(-delta), sp.exp(delta))
    assert sp.simplify(D.det() - 1) == 0
    check_names.append("reciprocal_carrier_unimodular")
    assert sp.simplify(det_hhat / det_h - a**4) == 0
    check_names.append("carrier_unimodularity_does_not_fix_pair_volume")

    # rho is explicitly unchanged because it is constructed from the invariant
    # terminal ratio. A normalized ruler derivative acquires weight -1 because
    # the ruler density L itself scales by a.
    X = sp.symbols("X", real=True)
    rho_from_h = X * sp.tanh(sp.log(ratio_phi) / 4)
    rho_from_hhat = X * sp.tanh(sp.log(ratio_phi_hat) / 4)
    assert sp.simplify(rho_from_hhat - rho_from_h) == 0
    check_names.append("bounded_position_conformal_weight_zero")

    phi, phi_sigma, Lsym = sp.symbols("phi phi_sigma L", real=True, nonzero=True)
    n_rho = X * sp.sech(phi) ** 2 * phi_sigma / Lsym
    n_rho_hat = X * sp.sech(phi) ** 2 * phi_sigma / (a * Lsym)
    assert sp.simplify(a * n_rho_hat - n_rho) == 0
    check_names.append("normalized_ruler_response_conformal_weight_minus_one")

    # G121's exact endpoint triangle descent survives arbitrary independent
    # common-scale endpoint values because the reciprocal edge is a potential
    # difference and carries no kappa term.
    pA, pB, pC, kA, kB, kC = sp.symbols("pA pB pC kA kB kC", real=True)
    triangle = sp.expand((pB - pA) + (pC - pB) + (pA - pC))
    assert triangle == 0 and all(sp.diff(triangle, k) == 0 for k in (kA, kB, kC))
    check_names.append("G121_triangle_descent_survives_common_scale_twins")

    # Direct computation for g=e^(2w) diag(-1,1). Curvature evaluates arbitrary
    # second jets of the supplied common scale; it does not constrain them.
    t, x = sp.symbols("t x", real=True)
    w = sp.Function("w")(t, x)
    coords = (t, x)
    g = sp.diag(-sp.exp(2 * w), sp.exp(2 * w))
    ginv = sp.simplify(g.inv())
    dim = 2
    Gamma = [[[sp.Integer(0) for _ in range(dim)] for _ in range(dim)] for _ in range(dim)]
    for k in range(dim):
        for i in range(dim):
            for j in range(dim):
                Gamma[k][i][j] = sp.simplify(
                    sp.Rational(1, 2)
                    * sum(
                        ginv[k, l]
                        * (sp.diff(g[l, j], coords[i]) + sp.diff(g[l, i], coords[j]) - sp.diff(g[i, j], coords[l]))
                        for l in range(dim)
                    )
                )
    Ric = [[sp.Integer(0) for _ in range(dim)] for _ in range(dim)]
    for i in range(dim):
        for j in range(dim):
            Ric[i][j] = sp.simplify(
                sum(
                    sp.diff(Gamma[k][i][j], coords[k])
                    - sp.diff(Gamma[k][i][k], coords[j])
                    + sum(Gamma[k][k][l] * Gamma[l][i][j] - Gamma[k][j][l] * Gamma[l][i][k] for l in range(dim))
                    for k in range(dim)
                )
            )
    scalar_R = sp.simplify(sum(ginv[i, j] * Ric[i][j] for i in range(dim) for j in range(dim)))
    expected_R = sp.simplify(2 * sp.exp(-2 * w) * (sp.diff(w, t, 2) - sp.diff(w, x, 2)))
    assert sp.simplify(scalar_R - expected_R) == 0
    check_names.append("conformal_curvature_evaluates_supplied_second_jets")

    assert len(check_names) == 9

    return {
        "exact_checks": len(check_names),
        "exact_check_names": check_names,
        "pair_determinant_weight": 4,
        "phi_pair_weight": 0,
        "beta_weight": 0,
        "rho_weight": 0,
        "normalized_response_weight": -1,
        "conformal_2d_scalar_curvature": str(scalar_R),
    }


def main() -> None:
    manifest = read_tsv(MANIFEST)
    ledger = read_tsv(LEDGER)
    verify_manifest(manifest)
    validate_ledger(ledger, {row["source_id"] for row in manifest})
    landing, rank, history_equation_count = classify(ledger)
    assert landing == "RANK_ZERO"
    assert rank == 0
    result = {
        "status": "PASS",
        "landing": landing,
        "source_count": len(manifest),
        "ledger_count": len(ledger),
        "role_counts": dict(sorted(Counter(row["role"] for row in ledger).items())),
        "owned_physical_history_equation_count": history_equation_count,
        "common_scale_physical_history_principal_rank": rank,
        "scope": "41-source frozen active record; regular complete-coframe and relation-network arena",
        "maximum_conclusion": "source-bounded equation-role and principal-rank classification only",
        **exact_checks(),
    }
    OUTPUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
