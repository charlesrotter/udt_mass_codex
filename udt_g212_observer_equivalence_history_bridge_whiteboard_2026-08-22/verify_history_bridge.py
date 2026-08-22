#!/usr/bin/env python3
"""Exact finite-dimensional checks for the G212 whiteboard landing."""

from __future__ import annotations

import json
import os
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parent
OUT = ROOT / "VERIFICATION_RESULT.json"


def main() -> None:
    checks: dict[str, bool] = {}

    def check(name: str, condition: bool) -> None:
        checks[name] = bool(condition)
        if not condition:
            raise AssertionError(name)

    # T1: exact endpoint-potential classification on a finite connected pair groupoid.
    observer_count = 5
    potentials = sp.symbols(f"p0:{observer_count}")
    edges = [(i, j) for i in range(observer_count) for j in range(i + 1, observer_count)]
    incidence = sp.zeros(len(edges), observer_count)
    for row, (i, j) in enumerate(edges):
        incidence[row, i] = -1
        incidence[row, j] = 1
    check("connected_pair_potential_rank", incidence.rank() == observer_count - 1)

    triangle_rows = []
    edge_index = {edge: index for index, edge in enumerate(edges)}
    for i in range(observer_count):
        for j in range(i + 1, observer_count):
            for k in range(j + 1, observer_count):
                row = [0] * len(edges)
                row[edge_index[(i, j)]] = 1
                row[edge_index[(j, k)]] = 1
                row[edge_index[(i, k)]] = -1
                triangle_rows.append(row)
    triangle = sp.Matrix(triangle_rows)
    check("potential_edges_satisfy_all_triangles", triangle * incidence == sp.zeros(len(triangle_rows), observer_count))
    check("triangle_kernel_is_potential_space", len(edges) - triangle.rank() == observer_count - 1)
    for i, j, k in ((0, 1, 2), (0, 2, 4), (1, 3, 4)):
        delta_ij = potentials[j] - potentials[i]
        delta_jk = potentials[k] - potentials[j]
        delta_ik = potentials[k] - potentials[i]
        check(f"triangle_{i}{j}{k}", sp.expand(delta_ij + delta_jk - delta_ik) == 0)

    # T2 / G211: two generic completed clocks reconstruct the two scalar modes.
    C1, C2, S1, S2, R1, R2 = sp.symbols("C1 C2 S1 S2 R1 R2", nonzero=True)
    matrix = sp.Matrix([[C1, -S1], [C2, -S2]])
    delta = C2 * S1 - C1 * S2
    check("tomography_determinant", sp.expand(matrix.det() - delta) == 0)
    x = (-S2 * R1 + S1 * R2) / delta
    y = (-C2 * R1 + C1 * R2) / delta
    check("tomography_inverse", sp.simplify(matrix * sp.Matrix([x, y]) - sp.Matrix([R1, R2])) == sp.zeros(2, 1))
    check("static_clock_rank_deficient", sp.Matrix([[C1, 0], [C2, 0]]).rank() == 1)

    # T4: full curvature isotropy inside the primary spherical chart.
    r, K, C = sp.symbols("r K C", nonzero=True)
    f = sp.Function("f")(r)
    k_tr = -sp.diff(f, r, 2) / 2
    k_mixed = -sp.diff(f, r) / (2 * r)
    k_angular = (1 - f) / r**2
    isotropy_ode = sp.simplify(r * sp.diff(f, r) - 2 * (f - 1))
    f_general = 1 + C * r**2
    check("space_form_ode_solution", sp.simplify(isotropy_ode.subs(f, f_general).doit()) == 0)
    f_space_form = 1 - K * r**2
    substitutions = {f: f_space_form}
    check("space_form_tr", sp.simplify(k_tr.subs(substitutions).doit() - K) == 0)
    check("space_form_mixed", sp.simplify(k_mixed.subs(substitutions).doit() - K) == 0)
    check("space_form_angular", sp.simplify(k_angular.subs(substitutions) - K) == 0)

    scalar = -sp.diff(f, r, 2) - 4 * sp.diff(f, r) / r + 2 * (1 - f) / r**2
    kretschmann = sp.diff(f, r, 2) ** 2 + 4 * (sp.diff(f, r) / r) ** 2 + 4 * ((1 - f) / r**2) ** 2
    check("space_form_scalar", sp.simplify(scalar.subs(substitutions).doit() - 12 * K) == 0)
    check("space_form_kretschmann", sp.simplify(kretschmann.subs(substitutions).doit() - 24 * K**2) == 0)

    # Schur step: the contracted-Bianchi coefficient is nonzero for n=4.
    n = sp.Integer(4)
    schur_coefficient = (n - 1) - n * (n - 1) / 2
    check("schur_coefficient_nonzero", schur_coefficient != 0)

    # Finite anchor values do not remove a smooth functional direction.
    epsilon = sp.symbols("epsilon", nonzero=True)
    anchors = (sp.Integer(1), sp.Integer(2), sp.Integer(3))
    omega = epsilon * sp.prod((r - anchor) ** 4 for anchor in anchors)
    for index, anchor in enumerate(anchors):
        for derivative_order in range(4):
            check(
                f"anchor_{index}_jet_{derivative_order}",
                sp.diff(omega, r, derivative_order).subs(r, anchor) == 0,
            )
    check("anchor_deformation_nontrivial", sp.expand(omega) != 0)

    result = {
        "status": "PASS",
        "check_count": len(checks),
        "observer_count": observer_count,
        "pair_edge_count": len(edges),
        "pair_potential_rank": incidence.rank(),
        "triangle_rank": triangle.rank(),
        "tomography_rank_generic": 2,
        "tomography_rank_static": 1,
        "space_form_local_moduli": 1,
        "finite_anchor_jet_order_preserved": 3,
        "checks": checks,
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    if os.environ.get("UDT_NO_WRITE") != "1":
        OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
