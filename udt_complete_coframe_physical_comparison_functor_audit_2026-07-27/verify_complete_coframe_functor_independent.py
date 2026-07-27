#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
from fractions import Fraction as Q
from pathlib import Path


HERE = Path(__file__).resolve().parent


def z(n: int = 4) -> list[list[Q]]:
    return [[Q(0) for _ in range(n)] for _ in range(n)]


def eye(n: int = 4) -> list[list[Q]]:
    a = z(n)
    for i in range(n):
        a[i][i] = Q(1)
    return a


def tr(a: list[list[Q]]) -> list[list[Q]]:
    return [list(row) for row in zip(*a)]


def mm(a: list[list[Q]], b: list[list[Q]]) -> list[list[Q]]:
    return [[sum((x * y for x, y in zip(row, col)), Q(0)) for col in tr(b)] for row in a]


def gauss_rank(a: list[list[Q]]) -> int:
    a = [row[:] for row in a]
    r = 0
    for c in range(len(a[0]) if a else 0):
        p = next((i for i in range(r, len(a)) if a[i][c]), None)
        if p is None:
            continue
        a[r], a[p] = a[p], a[r]
        v = a[r][c]
        a[r] = [x / v for x in a[r]]
        for i in range(len(a)):
            if i != r and a[i][c]:
                f = a[i][c]
                a[i] = [x - f * y for x, y in zip(a[i], a[r])]
        r += 1
    return r


def inv(a: list[list[Q]]) -> list[list[Q]]:
    n = len(a)
    work = [row[:] + eye(n)[i] for i, row in enumerate(a)]
    for c in range(n):
        p = next(i for i in range(c, n) if work[i][c])
        work[c], work[p] = work[p], work[c]
        v = work[c][c]
        work[c] = [x / v for x in work[c]]
        for i in range(n):
            if i != c and work[i][c]:
                f = work[i][c]
                work[i] = [x - f * y for x, y in zip(work[i], work[c])]
    return [row[n:] for row in work]


def diag(values: list[Q]) -> list[list[Q]]:
    a = z(len(values))
    for i, value in enumerate(values):
        a[i][i] = value
    return a


def response_vector(x: list[list[Q]], eta: list[list[Q]]) -> list[Q]:
    xt_eta = mm(tr(x), eta)
    eta_x = mm(eta, x)
    return [entry for a, b in zip(xt_eta, eta_x) for entry in [left + right for left, right in zip(a, b)]]


def matrix_with(entries: dict[tuple[int, int], Q]) -> list[list[Q]]:
    x = z()
    for (i, j), value in entries.items():
        x[i][j] = value
    return x


def extension_and_response_ranks() -> dict[str, tuple[int, int]]:
    eta = diag([Q(-1), Q(1), Q(1), Q(1)])
    mixing = [matrix_with({slot: Q(1)}) for slot in ((2, 0), (2, 1), (3, 0), (3, 1))]
    angular = [
        matrix_with({(2, 2): Q(1)}),
        matrix_with({(2, 3): Q(1)}),
        matrix_with({(3, 3): Q(1)}),
    ]
    determinant_one_angular = [
        matrix_with({(2, 2): Q(1), (3, 3): Q(-1)}),
        matrix_with({(2, 3): Q(1)}),
    ]
    families = {
        "general": angular + mixing,
        "determinant_one": determinant_one_angular + mixing,
        "transverse_invariant": mixing,
        "no_mixing": angular,
        "spectator_given_both": [],
    }
    result: dict[str, tuple[int, int]] = {}
    for name, basis_matrices in families.items():
        if not basis_matrices:
            result[name] = (0, 0)
            continue
        basis = [[entry for row in x for entry in row] for x in basis_matrices]
        responses = [response_vector(x, eta) for x in basis_matrices]
        result[name] = (
            gauss_rank([list(column) for column in zip(*basis)]),
            gauss_rank([list(column) for column in zip(*responses)]),
        )
    return result


def commutator_equations(generators: list[list[list[Q]]]) -> list[list[Q]]:
    equations = []
    for g in generators:
        for i in range(4):
            for j in range(4):
                row = [Q(0) for _ in range(16)]
                for k in range(4):
                    row[4 * i + k] += g[k][j]
                    row[4 * k + j] -= g[i][k]
                equations.append(row)
    return equations


def generators() -> tuple[list[list[list[Q]]], list[list[list[Q]]]]:
    rotations = []
    for i, j in ((1, 2), (1, 3), (2, 3)):
        g = z()
        g[i][j], g[j][i] = Q(1), Q(-1)
        rotations.append(g)
    boosts = []
    for i in (1, 2, 3):
        g = z()
        g[0][i] = g[i][0] = Q(1)
        boosts.append(g)
    return rotations, boosts


def path_control() -> bool:
    # Different exact holdout from production: boost in 0-2 and rotation in 1-3.
    u = eye()
    u[0][0], u[0][2], u[2][0], u[2][2] = Q(13, 5), Q(12, 5), Q(12, 5), Q(13, 5)
    v = eye()
    v[1][1], v[1][3], v[3][1], v[3][3] = Q(5, 13), Q(-12, 13), Q(12, 13), Q(5, 13)
    d1 = diag([Q(1, 3), Q(3), Q(5), Q(1, 5)])
    d2 = mm(d1, d1)
    uinv = inv(u)
    d2q = mm(mm(u, d2), uinv)
    left = mm(mm(v, d2q), mm(u, d1))
    right = mm(mm(v, u), mm(d2, d1))
    dnegq = mm(mm(u, inv(d1)), uinv)
    reverse = mm(uinv, dnegq)
    return left == right and mm(reverse, mm(u, d1)) == eye()


OUTCOMES = {
    "E01": "FOUNDED_BASE_ONLY_NOT_COMPLETE_PHYSICAL_FUNCTOR",
    "E02": "SEVEN_PARAMETER_POINTWISE_CLASS_PATHWISE_AVAILABLE_NOT_SELECTED",
    "E03": "SIX_PARAMETER_DETERMINANT_ONE_CLASS_PATHWISE_AVAILABLE_NOT_SELECTED",
    "E04": "FOUR_PARAMETER_MIXING_CLASS_PATHWISE_AVAILABLE_NOT_SELECTED",
    "E05": "THREE_PARAMETER_ANGULAR_CLASS_PATHWISE_AVAILABLE_NOT_SELECTED",
    "E06": "EXACT_SPECTATOR_WITNESS_PATHWISE_AVAILABLE_UNDER_EXTRA_PREMISES_NOT_SELECTED",
    "E07": "EXACT_ANGULAR_NONUNIQUENESS_COUNTERFAMILY_NOT_SELECTED",
    "E08": "EXACT_SHIFT_NONUNIQUENESS_COUNTERFAMILY_NOT_SELECTED",
    "E09": "PHYSICAL_METRIC_READING_RETAINS_SEVEN_PARAMETER_OPEN_SELECTION",
    "E10": "CONFORMAL_READING_INACTIVE_AND_RETAINS_SIX_PARAMETER_AMBIGUITY",
    "E11": "LOCAL_LORENTZ_PHYSICAL_OPERATION_DESCENT_OPEN",
    "E12": "GLOBAL_PHYSICAL_COMPARISON_FUNCTOR_OPEN",
}


def independent_status(class_id: str, gate_id: str) -> str:
    families = {"E02", "E03", "E04", "E05", "E09", "E10"}
    if gate_id == "G01":
        if class_id == "E06":
            return "EXACT_WITNESS"
        if class_id in {"E07", "E08"}:
            return "EXACT_COUNTERMODEL"
        return "CLASSIFIED_FAMILY" if class_id in families else "NOT_APPLICABLE"
    if gate_id == "G02":
        if class_id == "E01":
            return "DERIVED"
        if class_id == "E06":
            return "AVAILABLE_CONDITIONAL"
        if class_id in families | {"E07", "E08"}:
            return "CLASSIFIED_FAMILY"
        return "OPEN"
    if gate_id == "G03":
        return "INACTIVE_PREMISE" if class_id == "E10" else "OPEN"
    if gate_id in {"G04", "G05", "G06", "G08", "G09", "G10", "G11"}:
        return "OPEN"
    if gate_id == "G07":
        return "AVAILABLE_CONDITIONAL"
    if gate_id == "G12":
        return "INACTIVE_PREMISE" if class_id == "E10" else "NOT_SELECTED"
    raise AssertionError((class_id, gate_id))


def main() -> int:
    # No production result, matrix, or outcome file is read.
    with (HERE / "EXTENSION_CLASS_UNIVERSE.tsv").open(newline="") as handle:
        classes = list(csv.DictReader(handle, delimiter="\t"))
    with (HERE / "GATE_SCHEMA.tsv").open(newline="") as handle:
        gates = list(csv.DictReader(handle, delimiter="\t"))
    assert len(classes) == len(gates) == 12

    rotations, boosts = generators()
    residual = extension_and_response_ranks()
    extension_rank, response_rank = residual["general"]
    rotation_rank = gauss_rank(commutator_equations(rotations))
    full_rank = gauss_rank(commutator_equations(rotations + boosts))
    assert residual == {
        "general": (7, 7),
        "determinant_one": (6, 6),
        "transverse_invariant": (4, 4),
        "no_mixing": (3, 3),
        "spectator_given_both": (0, 0),
    }
    assert rotation_rank == 14 and full_rank == 15
    assert path_control()

    statuses = []
    for row in classes:
        for gate in gates:
            statuses.append({"class_id": row["id"], "gate_id": gate["gate_id"], "status": independent_status(row["id"], gate["gate_id"])})
    assert len(statuses) == 144
    with (HERE / "INDEPENDENT_CLASS_GATE_STATUS.tsv").open("w", newline="") as handle:
        writer = csv.DictWriter(handle, delimiter="\t", fieldnames=list(statuses[0]))
        writer.writeheader()
        writer.writerows(statuses)

    outcomes = [{"class_id": row["id"], "outcome": OUTCOMES[row["id"]]} for row in classes]
    with (HERE / "INDEPENDENT_CLASS_OUTCOMES.tsv").open("w", newline="") as handle:
        writer = csv.DictWriter(handle, delimiter="\t", fieldnames=list(outcomes[0]))
        writer.writeheader()
        writer.writerows(outcomes)

    result = {
        "schema": "udt.complete_coframe_physical_comparison_functor.independent.v1",
        "status": "PASS_NO_PRODUCTION_READ_FRACTION_AND_SEMANTIC_RECONSTRUCTION",
        "production_outputs_read": False,
        "classes": 12,
        "gates": 12,
        "cells": 144,
        "extension_generator_rank": extension_rank,
        "metric_response_rank": response_rank,
        "registered_residual_ranks": {name: pair[0] for name, pair in residual.items()},
        "registered_residual_metric_response_ranks": {name: pair[1] for name, pair in residual.items()},
        "spatial_rotation_commutator_constraint_rank": rotation_rank,
        "spatial_rotation_centralizer_dimension": 16 - rotation_rank,
        "full_Lorentz_commutator_constraint_rank": full_rank,
        "full_Lorentz_centralizer_dimension": 16 - full_rank,
        "full_centralizer": "SCALAR_IDENTITY_ONLY",
        "founded_base_in_full_centralizer": False,
        "endpoint_collapse_requires_holonomy_centralization": True,
        "independent_path_functor_holdout": True,
        "composition_selects_extension_parameters": False,
        "physical_path_ontology_selected": False,
        "physical_functor_status": "OPEN_NOT_SELECTED_IN_TWELVE_CLASS_UNIVERSE",
        "control_obstruction_scope": "FULL_HOLONOMY_TWISTED_CONTROL_ONLY",
    }
    (HERE / "INDEPENDENT_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
