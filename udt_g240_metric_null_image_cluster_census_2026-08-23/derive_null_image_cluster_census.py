#!/usr/bin/env python3
"""Exact finite controls for the G240 all-regular-null-image census theorem."""

from __future__ import annotations

import argparse
import json
from fractions import Fraction
from pathlib import Path
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "DERIVATION_RESULT.json"
LANDING = (
    "ALL_REGULAR_NULL_IMAGE_QUERY_REMOVES_ARBITRARY_BRANCH_WEIGHTS_CONDITIONALLY"
    "__METRIC_RELATION_INDUCES_IMAGE_INTENSITY_AND_SIBLING_PAIR_MEASURE_ON_A_SUPPLIED_HISTORY"
    "__PHYSICAL_HISTORY_SOURCE_MEASURE_TRANSFER_CRITICAL_STRATA_AND_OBSERVATIONAL_ANCHOR_OPEN"
)


def q(value: Fraction) -> dict[str, Any]:
    return {
        "numerator": value.numerator,
        "denominator": value.denominator,
        "exact": f"{value.numerator}/{value.denominator}",
        "decimal": float(value),
    }


def q_vector(values: Iterable[Fraction]) -> list[dict[str, Any]]:
    return [q(value) for value in values]


def q_matrix(values: list[list[Fraction]]) -> list[list[dict[str, Any]]]:
    return [q_vector(row) for row in values]


def count_vector(images: list[int], cells: int) -> list[int]:
    counts = [0] * cells
    for image in images:
        if not 0 <= image < cells:
            raise ValueError("image cell outside observed space")
        counts[image] += 1
    return counts


def cluster_moments(parents: list[dict[str, Any]], cells: int) -> dict[str, Any]:
    """Return exact first and ordered-distinct second factorial image moments."""
    nu1 = [Fraction(0) for _ in range(cells)]
    sibling = [[Fraction(0) for _ in range(cells)] for _ in range(cells)]
    multiplicities: list[int] = []

    for parent in parents:
        intensity = parent["intensity"]
        if not isinstance(intensity, Fraction) or intensity <= 0:
            raise ValueError("parent intensity must be a positive Fraction")
        counts = count_vector(parent["images"], cells)
        multiplicities.append(sum(counts))
        for i in range(cells):
            nu1[i] += intensity * counts[i]
            for j in range(cells):
                ordered_distinct = counts[i] * counts[j] - (counts[i] if i == j else 0)
                sibling[i][j] += intensity * ordered_distinct

    total_intensity = sum(nu1, Fraction(0))
    if total_intensity <= 0:
        raise ValueError("image intensity must be positive")
    sibling_mass = sum((sum(row, Fraction(0)) for row in sibling), Fraction(0))
    product = [[nu1[i] * nu1[j] for j in range(cells)] for i in range(cells)]
    nu2 = [[product[i][j] + sibling[i][j] for j in range(cells)] for i in range(cells)]
    pair_mass = total_intensity * total_intensity + sibling_mass
    p = [value / total_intensity for value in nu1]
    normalized_pair = [[value / pair_mass for value in row] for row in nu2]
    gamma = [
        [normalized_pair[i][j] - p[i] * p[j] for j in range(cells)]
        for i in range(cells)
    ]
    predicted_sibling_mass = sum(
        parent["intensity"] * len(parent["images"]) * (len(parent["images"]) - 1)
        for parent in parents
    )

    assert sibling_mass == predicted_sibling_mass
    assert sum(p, Fraction(0)) == 1
    assert sum((sum(row, Fraction(0)) for row in normalized_pair), Fraction(0)) == 1
    assert sum((sum(row, Fraction(0)) for row in gamma), Fraction(0)) == 0

    return {
        "nu_1": nu1,
        "distinct_parent_product": product,
        "sigma_sibling": sibling,
        "nu_2": nu2,
        "N": total_intensity,
        "S": sibling_mass,
        "pair_mass": pair_mass,
        "P": p,
        "normalized_pair": normalized_pair,
        "Gamma": gamma,
        "multiplicities": multiplicities,
        "decomposition_exact": all(
            nu2[i][j] == product[i][j] + sibling[i][j]
            for i in range(cells)
            for j in range(cells)
        ),
        "normalization_exact": True,
        "ordered_distinct_images": True,
    }


def serialize_moments(result: dict[str, Any]) -> dict[str, Any]:
    serialized: dict[str, Any] = {}
    matrix_keys = {
        "distinct_parent_product",
        "sigma_sibling",
        "nu_2",
        "normalized_pair",
        "Gamma",
    }
    vector_keys = {"nu_1", "P"}
    scalar_keys = {"N", "S", "pair_mass"}
    for key, value in result.items():
        if key in matrix_keys:
            serialized[key] = q_matrix(value)
        elif key in vector_keys:
            serialized[key] = q_vector(value)
        elif key in scalar_keys:
            serialized[key] = q(value)
        else:
            serialized[key] = value
    return serialized


def permute_parents(parents: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {"id": parent["id"], "intensity": parent["intensity"], "images": list(reversed(parent["images"]))}
        for parent in reversed(parents)
    ]


def permute_sky(parents: list[dict[str, Any]], permutation: list[int]) -> list[dict[str, Any]]:
    return [
        {
            "id": parent["id"],
            "intensity": parent["intensity"],
            "images": [permutation[image] for image in parent["images"]],
        }
        for parent in parents
    ]


def matrix_permute(matrix: list[list[Fraction]], permutation: list[int]) -> list[list[Fraction]]:
    inverse = [0] * len(permutation)
    for old, new in enumerate(permutation):
        inverse[new] = old
    return [[matrix[inverse[i]][inverse[j]] for j in range(len(permutation))] for i in range(len(permutation))]


def vector_permute(vector: list[Fraction], permutation: list[int]) -> list[Fraction]:
    result = [Fraction(0)] * len(permutation)
    for old, new in enumerate(permutation):
        result[new] = vector[old]
    return result


def build_result() -> dict[str, Any]:
    parents = [
        {"id": "A", "intensity": Fraction(1, 2), "images": [0, 1]},
        {"id": "B", "intensity": Fraction(2, 3), "images": [1]},
        {"id": "C", "intensity": Fraction(3, 4), "images": [0, 2, 2]},
    ]
    witness_raw = cluster_moments(parents, 3)

    one_image_parents = [
        {"id": "U", "intensity": Fraction(1, 3), "images": [0]},
        {"id": "V", "intensity": Fraction(2, 5), "images": [1]},
        {"id": "W", "intensity": Fraction(3, 7), "images": [2]},
    ]
    one_image_raw = cluster_moments(one_image_parents, 3)

    g239_parents = [{"id": "P", "intensity": Fraction(1), "images": [0, 1]}]
    g239_raw = cluster_moments(g239_parents, 2)

    relabeled_raw = cluster_moments(permute_parents(parents), 3)
    branch_relabel_invariant = all(
        witness_raw[key] == relabeled_raw[key]
        for key in ("nu_1", "sigma_sibling", "nu_2", "P", "Gamma")
    )

    sky_permutation = [2, 0, 1]
    sky_raw = cluster_moments(permute_sky(parents, sky_permutation), 3)
    sky_covariant = (
        sky_raw["nu_1"] == vector_permute(witness_raw["nu_1"], sky_permutation)
        and sky_raw["sigma_sibling"] == matrix_permute(witness_raw["sigma_sibling"], sky_permutation)
        and sky_raw["Gamma"] == matrix_permute(witness_raw["Gamma"], sky_permutation)
    )

    result = {
        "audit": "G240_METRIC_NULL_IMAGE_CLUSTER_CENSUS",
        "landing": LANDING,
        "query": "ALL_REGULAR_NULL_IMAGES_COUNTED_ONCE",
        "query_status": "CHOSE_QUERY_PROTOCOL__NOT_UNIVERSAL_DETECTION_LAW",
        "metric_status": "DERIVED_CONDITIONAL_NULL_RELATION_ON_SUPPLIED_HISTORY_AND_INCIDENCE",
        "parent_status": "CHOSE_POISSON_CONTROL__NOT_UDT_SOURCE_LAW",
        "uses_arbitrary_branch_weights": False,
        "unit_multiplicity_source": "COUNTING_MEASURE_AFTER_ALL_IMAGE_QUERY",
        "physical_history_selected": False,
        "observational_anchor_used": False,
        "boss_outcomes_opened": False,
        "formula": {
            "intensity": "nu1(A)=integral C_x(A) mu(dx)",
            "second_factorial": "nu2=nu1 tensor nu1+Sigma_sib",
            "sibling": "Sigma_sib(A,B)=integral sum_{y!=z in R_x} 1_A(y)1_B(z) mu(dx)",
            "total_sibling_mass": "S=integral m(x)(m(x)-1) mu(dx)",
            "normalized_gamma": "Gamma=Sigma_sib/(N^2+S)-[S/(N^2+S)] P tensor P",
        },
        "general_theorem_scope": "MEASURABLE_LOCALLY_FINITE_PROPER_REGULAR_IMAGE_RELATION",
        "witness": serialize_moments(witness_raw),
        "one_image_control": serialize_moments(one_image_raw),
        "g239_two_cell_control": serialize_moments(g239_raw),
        "invariance_controls": {
            "source_parent_reordering": branch_relabel_invariant,
            "branch_relabeling": branch_relabel_invariant,
            "sky_reparameterization_covariance": sky_covariant,
        },
        "critical_strata": {
            "caustic_density_formula": "OPEN__PUSHFORWARD_MEASURE_MAY_SURVIVE_WHILE_REGULAR_DENSITY_FORM_FAILS",
            "nonproper_or_infinite_images": "OPEN__NOT_REJECTED",
            "coherent_wave_interference": "OPEN__NOT_IN_POINT_IMAGE_CENSUS",
        },
        "omitted": [
            "physical metric-history selection",
            "physical source measure or evolution",
            "radiative transfer and detector selection",
            "caustic and infinite-image completion",
            "non-Poisson source correlations",
            "observational anchor",
            "BOSS outcomes",
        ],
        "forbidden_inputs_absent": [
            "P1",
            "G116/G189 transfer",
            "X_max",
            "Lambda-CDM distance",
            "BOSS curve value",
            "feature scale",
            "fitted coefficient",
            "post-readout orchestra",
            "protected package",
        ],
    }
    validate_result(result)
    return result


def validate_result(result: dict[str, Any]) -> None:
    if result["landing"] != LANDING:
        raise AssertionError("landing changed")
    if result["query"] != "ALL_REGULAR_NULL_IMAGES_COUNTED_ONCE":
        raise AssertionError("branch-selection shortcut inserted")
    if result["uses_arbitrary_branch_weights"] is not False:
        raise AssertionError("arbitrary branch weights inserted")
    if result["unit_multiplicity_source"] != "COUNTING_MEASURE_AFTER_ALL_IMAGE_QUERY":
        raise AssertionError("unit multiplicity provenance changed")
    if result["parent_status"] != "CHOSE_POISSON_CONTROL__NOT_UDT_SOURCE_LAW":
        raise AssertionError("Poisson control promoted")
    if result["general_theorem_scope"] != "MEASURABLE_LOCALLY_FINITE_PROPER_REGULAR_IMAGE_RELATION":
        raise AssertionError("regular-stratum scope widened")
    if result["physical_history_selected"] is not False or result["observational_anchor_used"] is not False:
        raise AssertionError("unowned physical input promoted")
    if result["boss_outcomes_opened"] is not False:
        raise AssertionError("BOSS outcome gate opened")
    if result["one_image_control"]["S"]["exact"] != "0/1":
        raise AssertionError("one-image sibling cancellation lost")
    if result["g239_two_cell_control"]["Gamma"][0][1]["exact"] != "1/12":
        raise AssertionError("G239 sibling control changed")
    if result["g239_two_cell_control"]["Gamma"][0][0]["exact"] != "-1/12":
        raise AssertionError("G239 normalization compensation lost")
    if result["witness"]["ordered_distinct_images"] is not True:
        raise AssertionError("image self-pairs inserted")
    if result["formula"]["normalized_gamma"] != "Gamma=Sigma_sib/(N^2+S)-[S/(N^2+S)] P tensor P":
        raise AssertionError("sibling normalization changed")
    if not all(result["invariance_controls"].values()):
        raise AssertionError("relabeling/covariance control failed")
    forbidden = set(result["forbidden_inputs_absent"])
    required = {"P1", "X_max", "BOSS curve value", "fitted coefficient", "protected package"}
    if not required.issubset(forbidden):
        raise AssertionError("forbidden-input guard removed")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--no-write", action="store_true")
    args = parser.parse_args()
    result = build_result()
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.no_write:
        print(payload, end="")
    else:
        OUTPUT.write_text(payload, encoding="utf-8")
        print(payload, end="")


if __name__ == "__main__":
    main()
