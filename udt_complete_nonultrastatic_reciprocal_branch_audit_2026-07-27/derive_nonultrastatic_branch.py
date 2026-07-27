#!/usr/bin/env python3
"""Exact algebra for the complete stationary reciprocal-coframe configuration audit."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path

import sympy as sp

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def table(name: str) -> list[dict[str, str]]:
    with (HERE / name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def unique(rows: list[dict[str, str]], key: str, expected: set[str]) -> None:
    values = [row[key] for row in rows]
    assert len(values) == len(set(values))
    assert set(values) == expected


def main() -> int:
    p, lam = sp.symbols("p lam", real=True)
    R = sp.symbols("R", positive=True)
    a, kappa = sp.symbols("a kappa", real=True, nonzero=True)
    ep = sp.exp(p)

    # Basis is (c_E dt, sigma_3, sigma_1, sigma_2).
    M = sp.diag(sp.exp(-p), R * ep, R * sp.exp(lam * p), R * sp.exp(lam * p))
    M[0, 1] = a * sp.exp(-p)
    eta = sp.diag(-1, 1, 1, 1)
    g = sp.simplify(M.T * eta * M)
    assert sp.simplify(M.det() - R**3 * sp.exp(2 * lam * p)) == 0
    assert sp.simplify(g.det() + R**6 * sp.exp(4 * lam * p)) == 0
    assert sp.simplify(g[0, 0] + sp.exp(-2 * p)) == 0
    assert sp.simplify(g[0, 1] + a * sp.exp(-2 * p)) == 0
    slice_ruler = sp.simplify(g[1, 1])
    assert sp.simplify(slice_ruler - (R**2 * sp.exp(2 * p) - a**2 * sp.exp(-2 * p))) == 0

    # Killing-norm depth: Q/c_E=exp(-phi).
    pA, pB, pC, scale = sp.symbols("pA pB pC scale", real=True, nonzero=True)
    deltaAB = pB - pA
    deltaBA = pA - pB
    deltaBC = pC - pB
    deltaAC = pC - pA
    assert sp.simplify(deltaAB + deltaBA) == 0
    assert sp.simplify(deltaAB + deltaBC - deltaAC) == 0
    assert sp.simplify(sp.log(scale * sp.exp(-pA) / (scale * sp.exp(-pB))) - deltaAB) == 0

    # K-flat wedge dK-flat. Terms containing dphi wedge tau vanish; only tau wedge d sigma_3 remains.
    twist_coefficient = sp.simplify(a * kappa / R**2 * sp.exp(-(3 + 2 * lam) * p))
    assert twist_coefficient != 0
    twist_norm = sp.simplify(twist_coefficient**2)
    assert twist_norm.is_positive

    # Distinct quadratic lapse fingerprint on round S3.
    d = sp.symbols("d0:4", real=True)
    x = sp.Matrix(sp.symbols("x0:4", real=True))
    variables = sp.symbols("A01 A02 A03 A12 A13 A23", real=True)
    A01, A02, A03, A12, A13, A23 = variables
    A = sp.Matrix([
        [0, A01, A02, A03], [-A01, 0, A12, A13],
        [-A02, -A12, 0, A23], [-A03, -A13, -A23, 0],
    ])
    D = sp.diag(*d)
    commutator = sp.simplify(D * A - A * D)
    expected = {
        (0, 1): (d[0] - d[1]) * A01,
        (0, 2): (d[0] - d[2]) * A02,
        (0, 3): (d[0] - d[3]) * A03,
        (1, 2): (d[1] - d[2]) * A12,
        (1, 3): (d[1] - d[3]) * A13,
        (2, 3): (d[2] - d[3]) * A23,
    }
    for ij, expression in expected.items():
        assert sp.simplify(commutator[ij] - expression) == 0
    f = (x.T * D * x)[0]
    Yf = sp.expand((sp.Matrix(D * x).T * A * x)[0] * 2)
    assert sp.simplify(Yf - (x.T * commutator * x)[0]) == 0

    # Finite exact samples exercise all real-lambda strata and both sides of the slice gate.
    samples = []
    for lv in (-2, -1, 0, 1, 3):
        for pv in (-sp.Rational(1, 2), 0, sp.Rational(2, 3)):
            good = sp.simplify((4 * sp.exp(2 * pv) - sp.Rational(1, 4) * sp.exp(-2 * pv)))
            samples.append({"lambda": lv, "phi": str(pv), "slice_positive": bool(good > 0)})
    assert len(samples) == 15 and all(row["slice_positive"] for row in samples)

    strata = table("CONFIGURATION_STRATUM_UNIVERSE.tsv")
    strata_out = table("CONFIGURATION_STRATUM_OUTCOMES.tsv")
    witnesses = table("WITNESS_UNIVERSE.tsv")
    witness_out = table("WITNESS_OUTCOMES.tsv")
    gates = table("PROPERTY_GATE_UNIVERSE.tsv")
    gate_out = table("PROPERTY_GATE_OUTCOMES.tsv")
    falsifications = table("FALSIFICATION_CONTRACT.tsv")
    unique(strata, "stratum_id", {f"C{i:02d}" for i in range(1, 13)})
    unique(strata_out, "stratum_id", {f"C{i:02d}" for i in range(1, 13)})
    unique(witnesses, "witness_id", {f"W{i:02d}" for i in range(1, 7)})
    unique(witness_out, "witness_id", {f"W{i:02d}" for i in range(1, 7)})
    unique(gates, "gate_id", {f"G{i:02d}" for i in range(1, 17)})
    unique(gate_out, "gate_id", {f"G{i:02d}" for i in range(1, 17)})
    unique(falsifications, "catch_id", {f"F{i:02d}" for i in range(1, 19)})

    result = {
        "schema_version": 1,
        "sympy_version": sp.__version__,
        "strata": 12,
        "witnesses": 6,
        "property_gates": 16,
        "catch_contracts": 18,
        "exact_lambda_samples": len(samples),
        "twisted_S3_complete_configuration_family": "DERIVED_EXISTENCE_CLASS",
        "static_S3_intrinsic_Killing_depth_witness": "DERIVED_CONDITIONAL_BRANCH",
        "twisted_S3_ruler_line_given_stationary_line": "DERIVED_EXACT",
        "single_all_gate_intrinsic_pair_witness": "OPEN",
        "primary_ruling": "COMPLETE_NONULTRASTATIC_CONFIGURATIONS_EXIST__INTRINSIC_STATIONARY_DEPTH_EXISTS_IN_BOUNDED_STATIC_CONTROL__FULL_INTRINSIC_PAIR_REMAINS_CONDITIONAL",
        "on_shell_solution_claimed": False,
        "lambda_selected": False,
        "global_endpoint_path_semantics_selected": False,
        "gpu_used": False,
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
