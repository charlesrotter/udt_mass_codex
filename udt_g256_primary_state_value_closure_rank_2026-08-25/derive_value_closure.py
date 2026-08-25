#!/usr/bin/env python3
"""Exact symbolic production derivation for the bounded G256 value-closure question."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path

import sympy as sp


PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parent
LANDING = (
    "FUNCTION_VALUED_PRIMARY_STATE_REMAINS__"
    "ANGULAR_INTERLOCK_IS_TOMOGRAPHIC_NOT_PROPAGATING__NO_ODE_GPU"
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def validate_sources_and_owners() -> dict[str, int]:
    manifest = read_tsv(PACKAGE / "SOURCE_MANIFEST.tsv")
    owners = read_tsv(PACKAGE / "OWNER_CENSUS.tsv")
    assert len(manifest) == len(owners) == 18
    manifest_paths = {row["path"] for row in manifest}
    assert manifest_paths == {row["source"] for row in owners}
    for row in manifest:
        source = ROOT / row["path"]
        assert source.is_file(), row["path"]
        assert sha256(source) == row["sha256"], row["path"]
    assert {row["owned_nonidentity_value_law"] for row in owners} == {"no"}
    return {
        "source_count": len(manifest),
        "owned_nonidentity_value_law_count": 0,
    }


def graph_edges(kind: str, n: int) -> list[tuple[int, int]]:
    assert n >= 2
    if kind == "path":
        return [(i, i + 1) for i in range(n - 1)]
    if kind == "star":
        return [(0, j) for j in range(1, n)]
    if kind == "cycle":
        assert n >= 3
        return [(i, i + 1) for i in range(n - 1)] + [(0, n - 1)]
    if kind == "complete":
        return [(i, j) for i in range(n) for j in range(i + 1, n)]
    raise ValueError(kind)


def incidence_matrix(n: int, edges: list[tuple[int, int]]) -> sp.Matrix:
    rows = []
    for source, target in edges:
        assert 0 <= source < target < n
        row = [0] * n
        row[source] = -1
        row[target] = 1
        rows.append(row)
    return sp.Matrix(rows)


def complete_cycle_matrix(n: int, edges: list[tuple[int, int]]) -> sp.Matrix:
    index = {edge: position for position, edge in enumerate(edges)}
    rows = []
    for i in range(1, n):
        for j in range(i + 1, n):
            row = [0] * len(edges)
            row[index[(0, i)]] = 1
            row[index[(i, j)]] = 1
            row[index[(0, j)]] = -1
            rows.append(row)
    return sp.Matrix(rows) if rows else sp.zeros(0, len(edges))


def validate_graph_record(record: dict[str, int | str]) -> None:
    n = int(record["N"])
    edges = int(record["edge_count"])
    rank = int(record["incidence_rank"])
    assert rank == n - 1
    assert int(record["anchored_state_dimension"]) == n - 1
    assert int(record["cycle_rank"]) == edges - n + 1
    if record["kind"] == "complete":
        assert edges == n * (n - 1) // 2
        assert int(record["cycle_annihilation_rank"]) == int(record["cycle_rank"])


def graph_census() -> list[dict[str, int | str]]:
    records: list[dict[str, int | str]] = []
    for n in range(2, 13):
        kinds = ["path", "star", "complete"]
        if n >= 3:
            kinds.insert(2, "cycle")
        for kind in kinds:
            edges = graph_edges(kind, n)
            matrix = incidence_matrix(n, edges)
            rank = int(matrix.rank())
            cycle_rank = len(edges) - rank
            cycle_annihilation_rank = cycle_rank
            if kind == "complete":
                cycles = complete_cycle_matrix(n, edges)
                assert cycles * matrix == sp.zeros(cycles.rows, n)
                cycle_annihilation_rank = int(cycles.rank())
            record: dict[str, int | str] = {
                "kind": kind,
                "N": n,
                "edge_count": len(edges),
                "incidence_rank": rank,
                "cycle_rank": cycle_rank,
                "cycle_annihilation_rank": cycle_annihilation_rank,
                "anchored_state_dimension": n - 1,
            }
            validate_graph_record(record)
            records.append(record)
    return records


def angular_interlock() -> dict[str, object]:
    phi, p, q, a_parallel, a_perp = sp.symbols(
        "phi p q A_parallel A_perp", real=True
    )
    scale = sp.exp(-2 * phi)
    forward_parallel = scale * (2 * p**2 + p - q)
    forward_perp = 1 - scale * (1 + p)
    recovered_p = sp.exp(2 * phi) * (1 - a_perp) - 1
    recovered_q = 2 * recovered_p**2 + recovered_p - sp.exp(2 * phi) * a_parallel
    assert sp.simplify(
        recovered_p.subs(a_perp, forward_perp) - p
    ) == 0
    assert sp.simplify(
        recovered_q.subs({a_perp: forward_perp, a_parallel: forward_parallel}) - q
    ) == 0
    jacobian = sp.Matrix([forward_parallel, forward_perp]).jacobian([p, q])
    determinant = sp.simplify(jacobian.det())
    assert determinant == -sp.exp(-4 * phi)
    record = {
        "forward_parallel": str(forward_parallel),
        "forward_perp": str(forward_perp),
        "recovered_p": str(recovered_p),
        "recovered_q": str(recovered_q),
        "jet_jacobian_determinant": str(determinant),
        "nonzero_for_finite_real_phi": True,
        "owned_residual_count": 0,
        "classification": "LOCAL_TOMOGRAPHIC_BIJECTION_NOT_VALUE_PROPAGATION",
    }
    validate_angular_record(record)
    return record


def validate_angular_record(record: dict[str, object]) -> None:
    assert record["nonzero_for_finite_real_phi"] is True
    assert int(record["owned_residual_count"]) == 0
    assert record["classification"] == "LOCAL_TOMOGRAPHIC_BIJECTION_NOT_VALUE_PROPAGATION"


def jet_targets(index: int) -> tuple[sp.Rational, sp.Rational, sp.Rational]:
    phi = sp.Rational(3 * index**2 - 2 * index + 5, index + 2)
    p = sp.Rational((-1) ** index * (2 * index + 1), index + 3)
    q = sp.Rational(index**2 - 4 * index + 7, 2 * index + 1)
    return phi, p, q


def hermite_matrix(nodes: list[sp.Rational]) -> sp.Matrix:
    degree_count = 3 * len(nodes)
    rows: list[list[sp.Expr]] = []
    for node in nodes:
        rows.append([node**power for power in range(degree_count)])
        rows.append([
            0 if power == 0 else power * node ** (power - 1)
            for power in range(degree_count)
        ])
        rows.append([
            0 if power < 2 else power * (power - 1) * node ** (power - 2)
            for power in range(degree_count)
        ])
    return sp.Matrix(rows)


def hermite_record(n: int, domain: str) -> dict[str, object]:
    x = sp.symbols("x", real=True)
    nodes = [sp.Rational(i) for i in range(1, n + 1)]
    targets: list[sp.Rational] = []
    triples: list[tuple[sp.Rational, sp.Rational, sp.Rational]] = []
    for i, node in enumerate(nodes, start=1):
        value, scaled_first, scaled_second = jet_targets(i)
        first = scaled_first / node
        second = scaled_second / node**2
        triples.append((value, first, second))
        targets.extend([value, first, second])
    matrix = hermite_matrix(nodes)
    assert matrix.rank() == 3 * n
    coefficients = matrix.inv() * sp.Matrix(targets)
    polynomial = sp.expand(sum(coefficients[k] * x**k for k in range(3 * n)))
    for node, (value, first, second) in zip(nodes, triples):
        assert sp.simplify(polynomial.subs(x, node) - value) == 0
        assert sp.simplify(sp.diff(polynomial, x).subs(x, node) - first) == 0
        assert sp.simplify(sp.diff(polynomial, x, 2).subs(x, node) - second) == 0

    null_deformation = sp.prod((x - node) ** 3 for node in nodes)
    deformed = sp.expand(polynomial + null_deformation)
    for node, (value, first, second) in zip(nodes, triples):
        assert sp.simplify(deformed.subs(x, node) - value) == 0
        assert sp.simplify(sp.diff(deformed, x).subs(x, node) - first) == 0
        assert sp.simplify(sp.diff(deformed, x, 2).subs(x, node) - second) == 0
    third_change = sp.simplify(sp.diff(null_deformation, x, 3).subs(x, nodes[0]))
    assert third_change != 0
    coefficient_text = ";".join(str(value) for value in coefficients)
    record = {
        "domain": domain,
        "N": n,
        "condition_count": 3 * n,
        "matrix_rank": int(matrix.rank()),
        "maximum_degree": 3 * n - 1,
        "all_jets_exact": True,
        "null_deformation_preserves_all_registered_jets": True,
        "third_germ_change_at_first_node": str(third_change),
        "coefficient_sha256": hashlib.sha256(coefficient_text.encode()).hexdigest(),
    }
    validate_hermite_record(record)
    return record


def validate_hermite_record(record: dict[str, object]) -> None:
    n = int(record["N"])
    assert int(record["condition_count"]) == 3 * n
    assert int(record["matrix_rank"]) == 3 * n
    assert record["all_jets_exact"] is True
    assert record["null_deformation_preserves_all_registered_jets"] is True
    assert sp.Rational(str(record["third_germ_change_at_first_node"])) != 0


def validate_solver_gate(record: dict[str, object]) -> None:
    assert int(record["owned_residual_count"]) == 0
    assert record["ode_status"] == "GATED_NOT_DEFINED"
    assert record["pde_status"] == "GATED_NOT_DEFINED"
    assert record["gpu_status"] == "GATED_NOT_DEFINED"


def derive() -> dict[str, object]:
    ownership = validate_sources_and_owners()
    graphs = graph_census()
    radial = [hermite_record(n, "radial") for n in range(2, 9)]
    timelive = [hermite_record(n, "timelive") for n in range(2, 9)]
    angular = angular_interlock()
    solver_gate = {
        "owned_residual_count": 0,
        "ode_status": "GATED_NOT_DEFINED",
        "pde_status": "GATED_NOT_DEFINED",
        "gpu_status": "GATED_NOT_DEFINED",
    }
    validate_solver_gate(solver_gate)
    complete_rows = [row for row in graphs if row["kind"] == "complete"]
    assert all(
        int(row["anchored_state_dimension"]) == int(row["N"]) - 1
        for row in complete_rows
    )
    return {
        "status": "PASS",
        "landing": LANDING,
        "ownership": ownership,
        "graph_sweep": {
            "N_min": 2,
            "N_max": 12,
            "record_count": len(graphs),
            "complete_graph_anchored_dimension_formula": "N-1",
            "arbitrary_N_proof": "connected_incidence_kernel_is_span_of_all_ones",
        },
        "angular_interlock": angular,
        "radial_hermite": {
            "N_min": 2,
            "N_max": 8,
            "records": radial,
            "arbitrary_N_proof": (
                "homogeneous_degree_below_3N_polynomial_with_triple_zeros_at_N_"
                "distinct_nodes_is_zero"
            ),
        },
        "timelive_carry": {
            "reversal": "delta_ji=-delta_ij",
            "actual_composition": "delta_ik=delta_ij+delta_jk",
            "anchored_event_state_dimension": "N-1",
            "records": timelive,
            "higher_germs": "free_via_product_of_cubed_node_factors",
        },
        "solver_gate": solver_gate,
        "conclusion_scope": (
            "bounded_primary_scalar_value_closure_only; no universal future-law no-go"
        ),
    }


def write_tsv(path: Path, rows: list[dict[str, object]]) -> None:
    assert rows
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    parser.add_argument("--rank-atlas", type=Path)
    parser.add_argument("--hermite-atlas", type=Path)
    arguments = parser.parse_args()
    result = derive()
    if arguments.rank_atlas:
        write_tsv(arguments.rank_atlas, graph_census())
    if arguments.hermite_atlas:
        rows = result["radial_hermite"]["records"] + result["timelive_carry"]["records"]
        write_tsv(arguments.hermite_atlas, rows)
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if arguments.output:
        arguments.output.write_text(payload, encoding="utf-8")
    else:
        print(payload, end="")


if __name__ == "__main__":
    main()
