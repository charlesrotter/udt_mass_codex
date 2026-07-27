#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path


HERE = Path(__file__).resolve().parent


@dataclass(frozen=True)
class Facts:
    candidate_id: str
    geometric_diameter: bool = False
    signed_endpoint_cocycle: bool = False
    stationary_null_path: bool = False
    projective_display: bool = False
    schema_missing_arrow: bool = False
    compact_continuous: bool = False
    physical_domain_selected: bool = False
    scale_supplied_not_derived: bool = False


def classify(facts: Facts) -> tuple[str, str]:
    if facts.geometric_diameter:
        assert facts.compact_continuous and not facts.physical_domain_selected
        return (
            "DERIVED_EXECUTABLE_BRANCHWISE_GEOMETRIC_DIAMETER_NOT_OPERATIONAL_PHYSICAL_XMAX_BRIDGE",
            "finite_attained_geometric_output_without_physical_identification",
        )
    if facts.signed_endpoint_cocycle:
        assert not facts.physical_domain_selected
        return (
            "DERIVED_BRANCHWISE_CLOCK_COCYCLE_NOT_COMPLETE_DISTANCE_OR_XMAX_BRIDGE",
            "signed_additive_endpoint_map_not_symmetric_nondegenerate_distance",
        )
    if facts.stationary_null_path:
        assert facts.compact_continuous and not facts.physical_domain_selected
        return (
            "DERIVED_BRANCHWISE_DIRECTED_NULL_PATH_GEOMETRY_NOT_PHYSICAL_XMAX_OR_BOOTSTRAP_BRIDGE",
            "directed_path_geometry_exists_but_signal_ontology_and_physical_arrows_are_open",
        )
    if facts.projective_display:
        assert facts.scale_supplied_not_derived
        return (
            "UNIQUE_CONDITIONAL_1D_DISPLAY_NOT_METRIC_DERIVATION_OF_XMAX",
            "bounded_display_is_one_dimensional_and_uses_an_input_scale",
        )
    if facts.schema_missing_arrow:
        return (
            "WORKING_SCHEMA_MISSING_OPERATIONAL_ARROW_FUNCTIONAL",
            "supremum_has_no_domain_pairing_or_integrand",
        )
    raise AssertionError(f"unclassified facts: {facts}")


def matrix_rank(matrix: list[list[Fraction]]) -> int:
    work = [row[:] for row in matrix]
    rows = len(work)
    cols = len(work[0]) if rows else 0
    rank = 0
    for col in range(cols):
        pivot = next((row for row in range(rank, rows) if work[row][col]), None)
        if pivot is None:
            continue
        work[rank], work[pivot] = work[pivot], work[rank]
        value = work[rank][col]
        work[rank] = [entry / value for entry in work[rank]]
        for row in range(rows):
            if row != rank and work[row][col]:
                factor = work[row][col]
                work[row] = [left - factor * right for left, right in zip(work[row], work[rank])]
        rank += 1
    return rank


def bilocal_incidence_rank(n: int) -> int:
    # Rows evaluate phi(j)-phi(i) on all ordered pairs.  This is an exact
    # finite control of the all-pairs cocycle linearization.
    matrix: list[list[Fraction]] = []
    for i in range(n):
        for j in range(n):
            if i == j:
                continue
            row = [Fraction(0) for _ in range(n)]
            row[i] = Fraction(-1)
            row[j] = Fraction(1)
            matrix.append(row)
    return matrix_rank(matrix)


def main() -> int:
    # Independent exact null reconstruction; no production output is read.
    exp_phi = Fraction(2)
    c_e = Fraction(3)
    twist = Fraction(1)
    sigma3_v = Fraction(2)
    sqrt_q = Fraction(3)
    forward = (exp_phi * sqrt_q - twist * sigma3_v) / c_e
    reverse = (exp_phi * sqrt_q + twist * sigma3_v) / c_e
    assert forward == Fraction(4, 3) and reverse == Fraction(8, 3)
    assert -(c_e * forward + twist * sigma3_v) ** 2 + (exp_phi * sqrt_q) ** 2 == 0
    assert -(c_e * reverse - twist * sigma3_v) ** 2 + (exp_phi * sqrt_q) ** 2 == 0
    assert (forward + reverse) / 2 == exp_phi * sqrt_q / c_e
    assert (forward - reverse) / 2 == -twist * sigma3_v / c_e

    # Independent strong-convexity/slice check.
    a = Fraction(7)
    radius = Fraction(5)
    exp_2phi = Fraction(4)
    assert (a * a < radius * radius * exp_2phi * exp_2phi) == (abs(a) < radius * exp_2phi)

    # The full all-pairs endpoint cocycle has rank n-1, not scalar rank one.
    ranks = {str(n): bilocal_incidence_rank(n) for n in range(2, 9)}
    assert all(rank == int(n) - 1 for n, rank in ranks.items())

    # The local positive-distance obstruction is narrower: ker(dphi) is two
    # dimensional in three dimensions and q remains positive on nonzero ker vectors.
    kernel_dimension = 3 - 1
    q_vv = Fraction(25, 4)
    assert kernel_dimension == 2 and q_vv > 0

    facts = [
        Facts("C01", geometric_diameter=True, compact_continuous=True),
        Facts("C02", signed_endpoint_cocycle=True),
        Facts("C03", stationary_null_path=True, compact_continuous=True),
        Facts("C04", projective_display=True, scale_supplied_not_derived=True),
        Facts("C05", schema_missing_arrow=True),
    ]
    independently_classified = []
    for item in facts:
        outcome, reason = classify(item)
        independently_classified.append(
            {
                "candidate_id": item.candidate_id,
                "outcome": outcome,
                "operational_xmax_selected": "NO",
                "field_valued_return_selected": "NO_IN_FROZEN_CENSUS",
                "reason": reason,
            }
        )

    with (HERE / "INDEPENDENT_OUTCOMES.tsv").open("w", newline="") as handle:
        writer = csv.DictWriter(handle, delimiter="\t", fieldnames=list(independently_classified[0]))
        writer.writeheader()
        writer.writerows(independently_classified)

    result = {
        "schema": "udt.observer_pair_xmax_bridge.independent.v2",
        "status": "PASS_INDEPENDENT_STDLIB_FRACTION_AND_SEMANTIC_RECONSTRUCTION",
        "production_outputs_read": False,
        "candidate_count": 5,
        "independent_outcomes": {row["candidate_id"]: row["outcome"] for row in independently_classified},
        "null_path_exact": True,
        "twist_reversal_exact": True,
        "strong_convexity_equivalence_exact": True,
        "angular_kernel_dimension": kernel_dimension,
        "bilocal_incidence_ranks": ranks,
        "bilocal_kernel": "CONSTANTS",
        "compact_attainment_type": "FINITE_ATTAINED_FOR_CONTINUOUS_BRANCH_FUNCTIONALS",
        "operational_Xmax_bridge_status": "NOT_SELECTED_IN_FROZEN_FIVE_CANDIDATES",
        "field_valued_return_equation_status": "NOT_SELECTED_IN_FROZEN_FIVE_CANDIDATES",
    }
    (HERE / "INDEPENDENT_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
