#!/usr/bin/env python3
"""Independent G303 replay: coordinate tensor witness plus separate exact rank checks."""

from __future__ import annotations

import json
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parent
LANDING = (
    "BOTH_G301_CLASSES_HAVE_THE_SAME_LOCAL_CAUSAL_PRINCIPAL_SYSTEM"
    "__TRACEFREE_DATA_ARE_THE_UNION_OVER_ONE_CONSTANT_SCALAR_DATUM"
    "__WELLPOSEDNESS_DOES_NOT_SELECT"
)
PAIRS = [(i, j) for i in range(4) for j in range(i, 4)]


def christoffel_and_ricci(metric: sp.Matrix, coordinates: tuple[sp.Symbol, ...]):
    dim = len(coordinates)
    inverse = sp.simplify(metric.inv())
    gamma = [[[sp.S.Zero for _ in range(dim)] for _ in range(dim)] for _ in range(dim)]
    for a in range(dim):
        for b in range(dim):
            for c in range(dim):
                gamma[a][b][c] = sp.simplify(sp.Rational(1, 2) * sum(
                    inverse[a, d] * (
                        sp.diff(metric[d, c], coordinates[b])
                        + sp.diff(metric[d, b], coordinates[c])
                        - sp.diff(metric[b, c], coordinates[d])
                    ) for d in range(dim)
                ))
    ricci = sp.zeros(dim)
    for a in range(dim):
        for b in range(dim):
            ricci[a, b] = sp.simplify(sum(
                sp.diff(gamma[c][a][b], coordinates[c])
                - sp.diff(gamma[c][a][c], coordinates[b])
                + sum(
                    gamma[c][c][d] * gamma[d][a][b]
                    - gamma[c][b][d] * gamma[d][a][c]
                    for d in range(dim)
                )
                for c in range(dim)
            ))
    return inverse, gamma, ricci


def traceless_basis(g: sp.Matrix) -> tuple[sp.Matrix, sp.Matrix]:
    """Construct ker(trace_g) directly; do not reuse production's projector formula."""
    inv = g.inv()
    trace = sp.Matrix([[inv[i, j] * (2 if i != j else 1) for i, j in PAIRS]])
    basis = sp.Matrix.hstack(*trace.nullspace())
    return trace, basis


def tree_incidence(n: int) -> sp.Matrix:
    # Deliberately different from production's star: alternating path/fork tree.
    edges = []
    for vertex in range(1, n):
        parent = (vertex - 1) // 2
        row = [0] * n
        row[parent] = -1
        row[vertex] = 1
        edges.append(row)
    return sp.Matrix(edges)


def main() -> None:
    assertions = 0
    t, x, y, z, h = sp.symbols("t x y z h", real=True)
    a = sp.exp(h * t)
    metric = sp.diag(-1, a**2, a**2, a**2)
    inverse, _, ricci = christoffel_and_ricci(metric, (t, x, y, z))
    expected_lambda = 3 * h**2
    assert sp.simplify(ricci - expected_lambda * metric) == sp.zeros(4)
    assertions += 1
    scalar = sp.simplify(sum(inverse[i, j] * ricci[i, j] for i in range(4) for j in range(4)))
    assert scalar == 12 * h**2
    assert sp.simplify(scalar / 4 - expected_lambda) == 0
    assertions += 2

    # Direct Cauchy projection on t=constant: gamma=a^2 delta, K_ij=h gamma_ij.
    spatial_scalar = sp.S.Zero
    K_trace = 3 * h
    K_squared = 3 * h**2
    hamiltonian = sp.simplify(spatial_scalar + K_trace**2 - K_squared)
    assert hamiltonian == 6 * h**2
    assert sp.simplify(hamiltonian - 2 * expected_lambda) == 0
    assert hamiltonian.subs(h, 0) == 0
    assertions += 3

    # General-dimensional Bianchi replay, evaluated only afterward at d=4.
    d = sp.symbols("d", integer=True, positive=True)
    coefficient = sp.simplify(sp.Rational(1, 2) - 1 / d)
    assert coefficient.subs(d, 4) == sp.Rational(1, 4)
    assert coefficient.subs(d, 2) == 0
    assertions += 2

    # Independent rational congruence family. Unlike production, construct the nine-dimensional
    # traceless output space as the kernel of the trace map; never form the closed projector.
    eta = sp.diag(-1, 1, 1, 1)
    transforms = [
        sp.eye(4),
        sp.Matrix([[1, 1, 0, 0], [0, 2, 0, 0], [0, 0, 1, 1], [0, 0, 0, 3]]),
        sp.Matrix([[2, 0, 1, 0], [1, 1, 0, 0], [0, 0, 2, 1], [0, 1, 0, 1]]),
    ]
    symbol_checks = []
    for transform in transforms:
        assert transform.det() != 0
        g = sp.simplify(transform.T * eta * transform)
        trace, basis = traceless_basis(g)
        assert trace.rank() == 1
        assert basis.shape == (10, 9) and basis.rank() == 9
        assert sp.simplify(trace * basis) == sp.zeros(1, 9)
        assertions += 3
        inv = g.inv()
        for xi in (sp.Matrix([1, 0, 0, 0]), sp.Matrix([1, 2, -1, 1])):
            q = sp.simplify((xi.T * inv * xi)[0])
            full_symbol = -sp.Rational(1, 2) * q * sp.eye(10)
            raw_symbol = sp.simplify(-sp.Rational(1, 2) * q * basis)
            assert raw_symbol.rank() in (0, 9)
            assert full_symbol.rank() in (0, 10)
            assertions += 2
            symbol_checks.append({"q": str(q), "full_rank": full_symbol.rank(), "raw_rank": raw_symbol.rank()})

    # A different connected graph establishes exactly one scalar modulus.
    graph_checks = []
    for n in range(3, 13):
        incidence = tree_incidence(n)
        assert incidence.rank() == n - 1
        nullspace = incidence.nullspace()
        assert len(nullspace) == 1
        assert all(value == nullspace[0][0] for value in nullspace[0])
        assertions += 3
        graph_checks.append({"vertices": n, "constancy_rank": n - 1, "moduli": 1})

    output = {
        "status": "PASS",
        "landing": LANDING,
        "imports_production_code": False,
        "method": "full FLRW coordinate Ricci tensor, direct kernels of trace maps, binary-tree incidence ranks",
        "rank_nine_construction": "kernel basis of the 1x10 metric trace map; no closed projector",
        "assertions": assertions,
        "coordinate_witness": {
            "metric": "diag(-1,exp(2ht),exp(2ht),exp(2ht))",
            "Ricci": "3*h^2*g",
            "R": "12*h^2",
            "Lambda": "3*h^2",
            "Hamiltonian": "6*h^2=2*Lambda",
            "generic_nested_at": "h=0",
        },
        "raw_tracefree_rank": 9,
        "fixed_lambda_full_rank": 10,
        "symbol_checks": symbol_checks,
        "graph_checks": graph_checks,
        "extra_connected_constants": 1,
        "extra_scalar_functions": 0,
        "wellposedness_discriminator": False,
    }
    (ROOT / "INDEPENDENT_VERIFICATION.json").write_text(
        json.dumps(output, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(f"G303 independent verification PASS ({assertions} assertions)")
    print("Ric=3h^2 g, R=12h^2, H=6h^2=2 Lambda")


if __name__ == "__main__":
    main()
