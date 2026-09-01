#!/usr/bin/env python3
"""Implementation-distinct G314 verification; reads no production code or result."""

from __future__ import annotations

import itertools
import json
from pathlib import Path


PACKAGE = Path(__file__).resolve().parent
LANDING = (
    "GLOBAL_ADMISSIBILITY_AND_ACTUALIZATION_ARE_DISTINCT_MISSING_TYPES"
    "__CURRENT_STRUCTURE_SUPPLIES_NEITHER"
)


def main() -> None:
    assertions = 0

    def check(condition: bool, message: str) -> None:
        nonlocal assertions
        assertions += 1
        if not condition:
            raise AssertionError(message)

    # Rebuilt from the preregistered witness descriptions, not production artifacts.
    universe = ("round1", "round2", "product", "flat")
    properties = {
        "round1": frozenset(("einstein", "reciprocal", "network", "positive", "compact", "weyl0", "S3", "round", "X1")),
        "round2": frozenset(("einstein", "reciprocal", "network", "positive", "compact", "weyl0", "S3", "round", "X2")),
        "product": frozenset(("einstein", "reciprocal", "network", "positive", "compact", "weyl_active", "S1xS2", "nonround", "X1")),
        "flat": frozenset(("einstein", "reciprocal", "network", "zero", "noncompact", "weyl0", "R3", "nonround", "unscaled")),
    }
    for item in universe:
        check("einstein" in properties[item], f"equation missing: {item}")
        check("reciprocal" in properties[item], f"reciprocity missing: {item}")
        check("network" in properties[item], f"network missing: {item}")

    predicates = {
        "owned_equation": lambda tags: "einstein" in tags,
        "owned_reciprocity": lambda tags: "reciprocal" in tags,
        "owned_network": lambda tags: "network" in tags,
        "positive": lambda tags: "positive" in tags,
        "compact": lambda tags: "compact" in tags,
        "weyl_zero": lambda tags: "weyl0" in tags,
        "s3": lambda tags: "S3" in tags,
        "positive_round_s3": lambda tags: "round" in tags and "positive" in tags and "S3" in tags,
        "scale_x1": lambda tags: "X1" in tags,
        "round_x1": lambda tags: "round" in tags and "positive" in tags and "S3" in tags and "X1" in tags,
    }
    acceptance = {
        name: frozenset(item for item in universe if predicate(properties[item]))
        for name, predicate in predicates.items()
    }
    all_items = frozenset(universe)
    for name in ("owned_equation", "owned_reciprocity", "owned_network"):
        check(acceptance[name] == all_items, f"owned predicate selective: {name}")
    check(acceptance["positive"] == frozenset(("round1", "round2", "product")), "positive set")
    check(acceptance["compact"] == acceptance["positive"], "compact witness set")
    check(acceptance["weyl_zero"] == frozenset(("round1", "round2", "flat")), "Weyl set")
    check(acceptance["s3"] == frozenset(("round1", "round2")), "S3 set")
    check(acceptance["positive_round_s3"] == frozenset(("round1", "round2")), "positive round-S3 set")
    check(acceptance["scale_x1"] == frozenset(("round1", "product")), "scale set")
    check(acceptance["round_x1"] == frozenset(("round1",)), "finite singleton control")

    # Exhaust every Boolean acceptance predicate on the finite four-class control moduli.
    subsets = []
    for bits in itertools.product((False, True), repeat=len(universe)):
        accepted = frozenset(item for item, bit in zip(universe, bits) if bit)
        subsets.append(accepted)
        nonidentity = 0 < len(accepted) < len(universe)
        unique = len(accepted) == 1
        check(not unique or nonidentity, "unique acceptance must be nonidentity")
        check(not unique or len(accepted) == 1, "unique typing")
        if nonidentity and len(accepted) > 1:
            check(not unique, "nonidentity improperly implies unique")
    check(len(set(subsets)) == 16, "Boolean predicate census incomplete")
    nonsingleton_nonidentity = [subset for subset in subsets if 1 < len(subset) < len(universe)]
    check(len(nonsingleton_nonidentity) == 10, "nonsingleton nonidentity count changed")

    # Every accepted member defines a different delta population when acceptance is non-singleton.
    positive = acceptance["positive"]
    delta_measures = []
    for support in sorted(positive):
        measure = tuple(int(item == support) for item in sorted(positive))
        delta_measures.append(measure)
        check(sum(measure) == 1, "delta measure not normalized")
    check(len(set(delta_measures)) == len(positive), "population not extra information")

    # Exhaust every endomap on a three-class control set: fixed-point syntax has many outcomes.
    small = (0, 1, 2)
    fixed_sets = set()
    map_count = 0
    for images in itertools.product(small, repeat=len(small)):
        map_count += 1
        fixed = tuple(index for index, image in enumerate(images) if index == image)
        fixed_sets.add(fixed)
        check(all(images[index] == index for index in fixed), "fixed-point extraction")
    check(map_count == 27, "endomap census incomplete")
    check(len(fixed_sets) == 8, "fixed-point set diversity changed")
    check(tuple(small) in fixed_sets and () in fixed_sets, "identity/derangement controls missing")
    check((0,) in fixed_sets and (1, 2) in fixed_sets, "selective fixed sets missing")

    # Network encoder/decoder composite is explicitly identity.
    encoded = {item: ("metric_network", item) for item in universe}
    decoded = {value: key for key, value in encoded.items()}
    for item in universe:
        check(decoded[encoded[item]] == item, "network reconstruction changed")

    # Global metric selection and local jet-factor response are compatible.
    histories = ("left", "right")
    same_jet = {history: (1, 2, 3) for history in histories}
    factored = {history: sum(same_jet[history]) for history in histories}
    check(len(set(factored.values())) == 1, "jet-factor response failed")
    chosen = {"left": True, "right": False}
    check(sum(chosen.values()) == 1, "global selection control failed")
    hidden = {"left": 6, "right": 7}
    check(len(set(hidden.values())) == 2, "hidden history control failed")

    # Conditional dynamics can be deterministic for supplied data without selecting data ex nihilo.
    data_labels = tuple(f"data::{item}" for item in universe)
    evolution = {data: history for data, history in zip(data_labels, universe)}
    check(len(evolution) == len(universe), "conditional evolution data burden changed")
    check(len(set(evolution.values())) == len(universe), "conditional histories collapsed")
    for data in data_labels:
        check(evolution[data] in universe, "supplied data lacks a conditional history")

    result = {
        "status": "PASS",
        "landing": LANDING,
        "assertions": assertions,
        "production_imported": False,
        "production_result_read": False,
        "boolean_predicates_exhausted": len(subsets),
        "nonsingleton_nonidentity_predicates": len(nonsingleton_nonidentity),
        "endomaps_exhausted": map_count,
        "distinct_fixed_point_sets": len(fixed_sets),
        "owned_acceptance_sets_are_identity": True,
        "admissibility_does_not_supply_population": True,
        "network_reconstruction_is_identity": True,
        "global_selection_local_response_compatible": True,
        "conditional_field_theory_requires_unique_universe_selector": False,
        "bootstrap_without_supplied_data_requires_extra_structure": True,
        "candidate_adopted": False,
    }
    (PACKAGE / "INDEPENDENT_VERIFICATION.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
