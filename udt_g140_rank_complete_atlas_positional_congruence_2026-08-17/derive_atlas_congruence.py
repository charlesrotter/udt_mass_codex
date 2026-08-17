#!/usr/bin/env python3
"""Exact production derivation for G140."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from itertools import product

import sympy as sp


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
NAMES = ("A", "B", "C", "D")
EDGES = ((0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3))
FACES = ((0, 1, 2), (0, 1, 3), (0, 2, 3), (1, 2, 3))
ETA = sp.diag(-1, 1, 1, 1)


def require(condition: bool, label: str, checks: list[str]) -> None:
    if not condition:
        raise AssertionError(label)
    checks.append(label)


def pair_embedding(r: sp.Matrix) -> sp.Matrix:
    return sp.Matrix([[1, 0], [0, r[0]], [0, r[1]], [0, r[2]]])


def restriction_design(embeddings: dict[tuple[int, int], sp.Matrix]) -> sp.Matrix:
    # Metric component order: 00,01,02,03,11,12,13,22,23,33.
    symbols = sp.symbols("g00 g01 g02 g03 g11 g12 g13 g22 g23 g33")
    g00, g01, g02, g03, g11, g12, g13, g22, g23, g33 = symbols
    g = sp.Matrix([
        [g00, g01, g02, g03],
        [g01, g11, g12, g13],
        [g02, g12, g22, g23],
        [g03, g13, g23, g33],
    ])
    rows = []
    zero = {s: 0 for s in symbols}
    for edge in EDGES:
        h = sp.expand(embeddings[edge].T * g * embeddings[edge])
        for value in (h[0, 0], h[0, 1], h[1, 1]):
            rows.append([sp.expand(value).coeff(s) for s in symbols])
            require_zero = sp.expand(value - sum(rows[-1][k] * symbols[k] for k in range(10)))
            if require_zero.subs(zero) != 0 or require_zero != 0:
                raise AssertionError("design coefficient extraction")
    return sp.Matrix(rows)


def network(vertices: tuple[sp.Matrix, ...]) -> dict:
    embeddings = {}
    pullbacks = {}
    lengths2 = {}
    terminal_magnitudes = {}
    oriented_cochain = {}
    observations = []
    for i, j in EDGES:
        r = sp.simplify(vertices[j] - vertices[i])
        jmap = pair_embedding(r)
        h = sp.simplify(jmap.T * ETA * jmap)
        ell2 = sp.simplify((r.T * r)[0])
        bar_phi = sp.simplify(sp.log(ell2) / 4)
        embeddings[(i, j)] = jmap
        pullbacks[(i, j)] = h
        lengths2[(i, j)] = ell2
        terminal_magnitudes[(i, j)] = bar_phi
        # This increasing-label sign is a supplied ordered-cochain lift.  It is
        # not produced by reversing the affine strip parameter, because the
        # pullback and its terminal magnitude are unchanged by that reversal.
        oriented_cochain[(i, j)] = bar_phi
        observations.extend([h[0, 0], h[0, 1], h[1, 1]])

    design = restriction_design(embeddings)
    metric_vector = sp.Matrix([-1, 0, 0, 0, 1, 0, 0, 1, 0, 1])
    reconstructed = sp.linsolve((design, sp.Matrix(observations)))
    cycles = {}
    for i, j, k in FACES:
        residual = sp.simplify(
            oriented_cochain[(i, j)]
            + oriented_cochain[(j, k)]
            - oriented_cochain[(i, k)]
        )
        cycles[f"{NAMES[i]}{NAMES[j]}{NAMES[k]}"] = residual
    return {
        "embeddings": embeddings,
        "pullbacks": pullbacks,
        "lengths2": lengths2,
        "terminal_magnitudes": terminal_magnitudes,
        "oriented_cochain": oriented_cochain,
        "design": design,
        "rank": design.rank(),
        "reconstructed": reconstructed,
        "metric_vector": metric_vector,
        "cycles": cycles,
    }


def main() -> None:
    checks: list[str] = []
    right = (
        sp.Matrix([0, 0, 0]),
        sp.Matrix([1, 0, 0]),
        sp.Matrix([0, 1, 0]),
        sp.Matrix([0, 0, 1]),
    )
    regular = (
        sp.Matrix([0, 0, 0]),
        sp.Matrix([1, 0, 0]),
        sp.Matrix([sp.Rational(1, 2), sp.sqrt(3) / 2, 0]),
        sp.Matrix([sp.Rational(1, 2), sp.sqrt(3) / 6, sp.sqrt(sp.Rational(2, 3))]),
    )
    nclose = network(right)
    close = network(regular)

    require(nclose["rank"] == 10, "nonclosing_design_rank_ten", checks)
    require(close["rank"] == 10, "closing_design_rank_ten", checks)
    require(nclose["reconstructed"] == sp.FiniteSet(tuple(nclose["metric_vector"])),
            "nonclosing_reconstructs_same_metric", checks)
    require(close["reconstructed"] == sp.FiniteSet(tuple(close["metric_vector"])),
            "closing_reconstructs_same_metric", checks)

    for edge in EDGES:
        require(nclose["pullbacks"][edge] == sp.diag(-1, nclose["lengths2"][edge]),
                f"nonclosing_pullback_{edge}", checks)
        require(close["pullbacks"][edge] == sp.diag(-1, close["lengths2"][edge]),
                f"closing_pullback_{edge}", checks)
        require(nclose["pullbacks"][edge][0, 0] < 0 and nclose["pullbacks"][edge].det() < 0,
                f"nonclosing_regular_{edge}", checks)
        require(close["pullbacks"][edge][0, 0] < 0 and close["pullbacks"][edge].det() < 0,
                f"closing_regular_{edge}", checks)

    expected_right_lengths = {
        (0, 1): 1, (0, 2): 1, (0, 3): 1,
        (1, 2): 2, (1, 3): 2, (2, 3): 2,
    }
    require(nclose["lengths2"] == expected_right_lengths, "right_tetrahedron_lengths", checks)
    require(all(v == 1 for v in close["lengths2"].values()), "regular_tetrahedron_unit_lengths", checks)

    a = sp.log(2) / 4
    require(all(sp.simplify(v - a) == 0 for v in nclose["cycles"].values()),
            "nonclosing_face_residuals_log2_over4", checks)
    require(all(v == 0 for v in close["cycles"].values()), "closing_face_residuals_zero", checks)
    nonzero_edges = ((1, 2), (1, 3), (2, 3))
    closing_sign_assignments = 0
    for signs in product((-1, 1), repeat=len(nonzero_edges)):
        signed = dict(nclose["oriented_cochain"])
        for edge, sign in zip(nonzero_edges, signs):
            signed[edge] = sign * signed[edge]
        residuals = [sp.simplify(signed[(i, j)] + signed[(j, k)] - signed[(i, k)])
                     for i, j, k in FACES]
        closing_sign_assignments += int(all(value == 0 for value in residuals))
    require(closing_sign_assignments == 0, "no_inverse_sign_assignment_closes_nonclosing_data", checks)
    require(sp.simplify(sp.tanh(a)) != 0, "nonclosing_mobius_residual", checks)
    require(sp.simplify(sp.exp(-2 * a) - 1 / sp.sqrt(2)) == 0,
            "nonclosing_q_cycle_product", checks)

    # The same metric has zero curvature invariants in both constructions; only query embeddings differ.
    require(nclose["metric_vector"] == close["metric_vector"], "identical_metric_history", checks)
    require(
        nclose["terminal_magnitudes"] != close["terminal_magnitudes"],
        "different_terminal_magnitude_networks_same_metric",
        checks,
    )

    lines = (HERE / "SOURCE_MANIFEST.tsv").read_text(encoding="utf-8").splitlines()[1:]
    hashes = {}
    for line in lines:
        expected, rel, _role = line.split("\t")
        actual = hashlib.sha256((ROOT / rel).read_bytes()).hexdigest()
        require(actual == expected, f"source_hash_{Path(rel).parent.name}", checks)
        hashes[rel] = actual

    result = {
        "status": "PASS",
        "checks_passed": len(checks),
        "checks_total": len(checks),
        "checks": checks,
        "nonclosing": {
            "design_rank": nclose["rank"],
            "squared_lengths": {f"{NAMES[i]}{NAMES[j]}": str(v) for (i, j), v in nclose["lengths2"].items()},
            "face_residuals": {k: str(v) for k, v in nclose["cycles"].items()},
            "mobius_residual": str(sp.simplify(sp.tanh(a))),
            "q_cycle_product": str(1 / sp.sqrt(2)),
            "inverse_sign_assignments_tested": 8,
            "closing_sign_assignments": closing_sign_assignments,
        },
        "closing": {
            "design_rank": close["rank"],
            "all_squared_lengths": "1",
            "all_face_residuals": "0",
        },
        "ambient_metric": "diag(-1,1,1,1)",
        "calibration": {
            "length_unit": "ell_0>0",
            "clock_unit": "tau_0=ell_0/c_E",
            "coordinates": "dimensionless hatted variables",
        },
        "typing": {
            "terminal_readout": "unoriented bar_phi_{ij}=log(|Delta p_hat_ij|^2)/4",
            "cycle_input": "separately supplied antisymmetric ordered cochain delta",
            "rank_scope": "pooled constant-metric coefficient reconstruction",
        },
        "source_hashes": hashes,
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
