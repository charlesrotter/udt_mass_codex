#!/usr/bin/env python3
"""Exact finite type classification for G314 using only the Python standard library."""

from __future__ import annotations

import csv
import json
from dataclasses import asdict, dataclass
from pathlib import Path


PACKAGE = Path(__file__).resolve().parent
LANDING = (
    "GLOBAL_ADMISSIBILITY_AND_ACTUALIZATION_ARE_DISTINCT_MISSING_TYPES"
    "__CURRENT_STRUCTURE_SUPPLIES_NEITHER"
)


@dataclass(frozen=True)
class Witness:
    name: str
    grade: str
    complete_history: bool
    regular: bool
    globally_hyperbolic: bool
    compact_cauchy: bool
    lambda_sign: int
    weyl_zero: bool
    topology: str
    positive_round_s3: bool
    scale_label: str
    reciprocal: bool
    network_reconstructible: bool


@dataclass(frozen=True)
class Candidate:
    candidate_id: str
    candidate_type: str
    ownership: str
    accepts: tuple[str, ...]
    extra_burden: str
    note: str


class Checks:
    def __init__(self) -> None:
        self.count = 0

    def require(self, condition: bool, message: str) -> None:
        self.count += 1
        if not condition:
            raise AssertionError(message)


def main() -> None:
    checks = Checks()
    witnesses = (
        Witness(
            "round_dS_X1", "EXACT_COMPLETE_HISTORY", True, True, True, True,
            1, True, "S3", True, "X1", True, True,
        ),
        Witness(
            "round_dS_X2", "EXACT_COMPLETE_HISTORY_HOMOTHETIC", True, True, True, True,
            1, True, "S3", True, "X2", True, True,
        ),
        Witness(
            "positive_dS2_x_S2", "EXACT_COMPLETE_HISTORY", True, True, True, True,
            1, False, "S1xS2", False, "X1", True, True,
        ),
        Witness(
            "minkowski", "EXACT_COMPLETE_HISTORY", True, True, True, False,
            0, True, "R3", False, "UNSCALED", True, True,
        ),
        Witness(
            "berger_S3_data", "EXACT_CONSTRAINT_DATA_CONDITIONAL_LOCAL_DEVELOPMENT", False,
            True, False, True, 1, False, "S3", False, "X1", True, True,
        ),
        Witness(
            "ricci_flat_plane_wave", "EXACT_LOCAL_SOLUTION_GLOBAL_SCOPE_UNCLASSIFIED", False,
            True, False, False, 0, False, "R3", False, "UNSCALED", True, True,
        ),
    )
    by_name = {w.name: w for w in witnesses}
    checks.require(len(by_name) == len(witnesses), "duplicate witness")
    complete = tuple(w.name for w in witnesses if w.complete_history)
    complete_set = frozenset(complete)
    checks.require(len(complete) == 4, "complete witness family changed")
    checks.require("berger_S3_data" not in complete_set, "Berger data promoted to complete history")
    checks.require("ricci_flat_plane_wave" not in complete_set, "plane wave global scope promoted")

    def accepted(predicate) -> tuple[str, ...]:
        return tuple(sorted(w.name for w in witnesses if w.complete_history and predicate(w)))

    all_complete = tuple(sorted(complete))
    candidate_specs = (
        Candidate(
            "C01_ACTIVE_EQUATION", "equation_identity", "ACTIVE_BOUNDED_DERIVED",
            all_complete, "none inside the admitted arena",
            "Defines the arena and therefore accepts every registered complete solution.",
        ),
        Candidate(
            "C02_RECIPROCITY", "owned_response_compatibility", "OWNER_ADOPTED_PROVISIONAL",
            all_complete, "none inside the admitted arena",
            "Constrains response shape; G313 witnesses all remain reciprocal.",
        ),
        Candidate(
            "C03_NETWORK_RECONSTRUCTION", "reconstruction_identity", "DERIVED_CONDITIONAL",
            all_complete, "none",
            "The complete network reconstructs each supplied metric; it does not reject one.",
        ),
        Candidate(
            "C04_LOCAL_METRIC_SUFFICIENCY", "response_constitution", "OWNER_ADOPTED_PROVISIONAL",
            all_complete, "none",
            "Allows global metric selection but forbids hidden history-dependent local response.",
        ),
        Candidate(
            "C05_POSITIVE_LAMBDA", "curvature_sign_predicate", "NOT_OWNED_CANDIDATE_CONTROL",
            accepted(lambda w: w.lambda_sign > 0), "one sign premise",
            "Rejects Minkowski but leaves round scales and the product history.",
        ),
        Candidate(
            "C06_COMPACT_CAUCHY", "global_causal_topology_predicate", "NOT_OWNED_CANDIDATE_CONTROL",
            accepted(lambda w: w.compact_cauchy), "one global compactness premise",
            "Leaves both round scales and the S1xS2 product.",
        ),
        Candidate(
            "C07_WEYL_ZERO", "curvature_predicate", "NOT_OWNED_CANDIDATE_CONTROL",
            accepted(lambda w: w.weyl_zero), "one conformal-flatness premise",
            "Leaves both round scales and Minkowski.",
        ),
        Candidate(
            "C08_S3_TOPOLOGY", "topology_predicate", "NOT_OWNED_CANDIDATE_CONTROL",
            accepted(lambda w: w.topology == "S3"), "one topology premise",
            "Leaves both homothetic round histories; Berger data are not a complete-history row.",
        ),
        Candidate(
            "C09_FIXED_SCALE_X1", "scale_predicate", "NOT_OWNED_CANDIDATE_CONTROL",
            accepted(lambda w: w.scale_label == "X1"), "one numerical scale attachment",
            "Leaves the round and product histories at the registered scale.",
        ),
        Candidate(
            "C10_POSITIVE_ROUND_S3", "conjoined_branch_predicate", "NOT_OWNED_CANDIDATE_CONTROL",
            accepted(lambda w: w.positive_round_s3),
            "positive sign plus conformal flatness plus round-S3 global branch",
            "Leaves the two homothetic positive round histories; this is not maximal symmetry alone.",
        ),
        Candidate(
            "C11_ROUND_AND_SCALE", "conjoined_selector_control", "NOT_OWNED_CANDIDATE_CONTROL",
            accepted(lambda w: w.positive_round_s3 and w.scale_label == "X1"),
            "positive round-S3 branch plus a numerical scale",
            "Singleton only on the finite registered witnesses; not a full-arena uniqueness theorem.",
        ),
        Candidate(
            "C12_EXTREMAL_ACTION", "variational_or_order_predicate", "MISSING_NEW_STRUCTURE",
            (), "functional plus comparison order plus extremum rule",
            "No active UDT functional or order is supplied, so no acceptance set is evaluated.",
        ),
        Candidate(
            "C13_OBSERVATIONAL_MATCH", "downstream_discrimination", "OBSERVED_INTERFACE_ONLY",
            (), "observation map data likelihood and decision rule",
            "May discriminate a derived finite family; it is not a native admissibility law.",
        ),
        Candidate(
            "C14_POPULATION_MEASURE", "actualization_or_population", "MISSING_NEW_STRUCTURE",
            (), "choice map or normalized measure on accepted classes",
            "Not an admissibility predicate and not supplied by current premises.",
        ),
    )

    candidate_rows: list[dict[str, object]] = []
    for candidate in candidate_specs:
        accepted_set = frozenset(candidate.accepts)
        if accepted_set:
            checks.require(accepted_set <= complete_set, f"{candidate.candidate_id} accepts nonhistory")
        identity = accepted_set == complete_set
        nonidentity = bool(accepted_set) and accepted_set != complete_set
        singleton = len(accepted_set) == 1
        if candidate.ownership in {
            "ACTIVE_BOUNDED_DERIVED", "OWNER_ADOPTED_PROVISIONAL", "DERIVED_CONDITIONAL"
        }:
            checks.require(identity, f"owned candidate became selective: {candidate.candidate_id}")
        candidate_rows.append(
            {
                **asdict(candidate),
                "accepts": ",".join(candidate.accepts) if candidate.accepts else "NOT_EVALUATED",
                "accepted_count": len(accepted_set),
                "identity_on_registered_complete_family": identity,
                "nonidentity_on_registered_complete_family": nonidentity,
                "singleton_on_registered_complete_family": singleton,
            }
        )

    # Exact finite logic: nonidentity admissibility need not uniquely actualize a history.
    positive = frozenset(next(c.accepts for c in candidate_specs if c.candidate_id == "C05_POSITIVE_LAMBDA"))
    compact = frozenset(next(c.accepts for c in candidate_specs if c.candidate_id == "C06_COMPACT_CAUCHY"))
    round_only = frozenset(next(
        c.accepts for c in candidate_specs if c.candidate_id == "C10_POSITIVE_ROUND_S3"
    ))
    round_scale = frozenset(next(c.accepts for c in candidate_specs if c.candidate_id == "C11_ROUND_AND_SCALE"))
    checks.require(0 < len(positive) < len(complete_set), "positive predicate not nonidentity")
    checks.require(len(positive) == 3, "positive predicate unexpectedly unique")
    checks.require(positive == compact, "registered positive/compact independence control changed")
    checks.require(len(round_only) == 2, "roundness incorrectly sets scale")
    checks.require(len(round_scale) == 1, "finite singleton control changed")
    checks.require(
        next(c for c in candidate_specs if c.candidate_id == "C11_ROUND_AND_SCALE").ownership
        == "NOT_OWNED_CANDIDATE_CONTROL",
        "finite singleton control promoted to owned",
    )

    # A population is extra information whenever more than one class survives.
    delta_populations = {name: {member: int(member == name) for member in sorted(positive)} for name in positive}
    checks.require(len(delta_populations) == len(positive), "population multiplicity changed")
    for name, measure in delta_populations.items():
        checks.require(sum(measure.values()) == 1, f"population not normalized: {name}")
        checks.require(measure[name] == 1, f"delta population support changed: {name}")

    # Complete-network reconstruction is the identity fixed-point map on the supplied history set.
    network = {name: f"network::{name}" for name in sorted(complete_set)}
    reconstruct = {value: key for key, value in network.items()}
    reconstruction_composite = {name: reconstruct[network[name]] for name in sorted(complete_set)}
    checks.require(all(name == image for name, image in reconstruction_composite.items()),
                   "network reconstruction stopped being identity")
    identity_fixed = tuple(sorted(name for name, image in reconstruction_composite.items() if name == image))
    checks.require(frozenset(identity_fixed) == complete_set, "reconstruction became selective")

    # The fixed-point syntax is neutral until a nonidentity map B is supplied.
    target = "round_dS_X1"
    target_map = {name: target for name in sorted(complete_set)}
    target_fixed = tuple(sorted(name for name, image in target_map.items() if name == image))
    checks.require(target_fixed == (target,), "target map fixed-point control changed")
    checks.require(target_map != reconstruction_composite, "nonidentity map collapsed to reconstruction")

    swap_map = {
        "round_dS_X1": "round_dS_X2",
        "round_dS_X2": "round_dS_X1",
        "positive_dS2_x_S2": "positive_dS2_x_S2",
        "minkowski": "minkowski",
    }
    swap_fixed = tuple(sorted(name for name, image in swap_map.items() if name == image))
    checks.require(swap_fixed == ("minkowski", "positive_dS2_x_S2"),
                   "alternative nonidentity fixed points changed")
    checks.require(target_fixed != swap_fixed, "different bootstrap maps lost distinct selections")

    # Global selection of a metric is compatible with local response sufficiency.
    equal_jet_histories = ("history_left", "history_right")
    jet = {name: "same_local_metric_jet" for name in equal_jet_histories}
    local_response = {name: f"response::{jet[name]}" for name in equal_jet_histories}
    checks.require(len(set(local_response.values())) == 1, "local response not jet-factored")
    global_acceptance = {"history_left": True, "history_right": False}
    checks.require(len({name for name, value in global_acceptance.items() if value}) == 1,
                   "global selector control changed")
    hidden_response = {"history_left": "response::left", "history_right": "response::right"}
    checks.require(len(set(hidden_response.values())) == 2, "hidden response control failed")

    owned_candidates = [row for row in candidate_rows if row["ownership"] in {
        "ACTIVE_BOUNDED_DERIVED", "OWNER_ADOPTED_PROVISIONAL", "DERIVED_CONDITIONAL"
    }]
    checks.require(all(row["identity_on_registered_complete_family"] for row in owned_candidates),
                   "an owned nonidentity selector appeared")
    checks.require(not any(row["singleton_on_registered_complete_family"] for row in owned_candidates),
                   "an owned unique selector appeared")

    result = {
        "status": "PASS",
        "landing": LANDING,
        "assertions": checks.count,
        "scope": "BOUNDED_G312_G313_REGISTERED_CANDIDATE_TYPES_AND_WITNESSES_ONLY",
        "complete_moduli_witness_count": len(complete_set),
        "control_nonhistory_count": len(witnesses) - len(complete_set),
        "witnesses": [asdict(w) for w in witnesses],
        "candidate_rows": candidate_rows,
        "admissibility_actualization": {
            "positive_acceptance_count": len(positive),
            "positive_delta_population_count": len(delta_populations),
            "nonidentity_does_not_imply_unique": len(positive) > 1,
            "singleton_can_collapse_actualization_type": len(round_scale) == 1,
            "singleton_control_owned": False,
        },
        "bootstrap_fixed_points": {
            "reconstruction_fixed": list(identity_fixed),
            "target_map_fixed": list(target_fixed),
            "swap_map_fixed": list(swap_fixed),
            "fixed_point_syntax_selects_without_B": False,
        },
        "locality_compatibility": {
            "global_metric_selection_allowed": True,
            "jet_factored_local_response_preserved": True,
            "hidden_history_local_response_forbidden": True,
        },
        "minimum_missing_type": {
            "first": "NONIDENTITY_DIFF_INVARIANT_ADMISSIBILITY_PREDICATE_OR_EQUIVALENTLY_SPECIFIED_NONIDENTITY_BOOTSTRAP_MAP",
            "second_if_nonsingleton": "ACTUALIZATION_CHOICE_OR_POPULATION_MEASURE",
            "two_premises_logically_forced": False,
        },
        "interpretive_boundary": {
            "conditional_field_theory_requires_unique_universe_selector": False,
            "initial_or_boundary_data_may_label_a_conditional_history": True,
            "bootstrap_from_no_supplied_data_requires_extra_structure": True,
            "g303_cauchy_method_remains_conditional": True,
        },
        "nonpromotion": {
            "candidate_adopted": False,
            "full_solution_space_enumerated": False,
            "metric_or_kernel_changed": False,
            "observation_or_xmax_used": False,
        },
    }

    (PACKAGE / "DERIVATION_RESULT.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    with (PACKAGE / "ADMISSIBILITY_TYPE_ATLAS.tsv").open("w", encoding="utf-8", newline="") as stream:
        fields = (
            "candidate_id", "candidate_type", "ownership", "accepts", "accepted_count",
            "identity_on_registered_complete_family", "nonidentity_on_registered_complete_family",
            "singleton_on_registered_complete_family", "extra_burden", "note",
        )
        writer = csv.DictWriter(stream, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows({field: row[field] for field in fields} for row in candidate_rows)
    with (PACKAGE / "WITNESS_SIGNATURES.tsv").open("w", encoding="utf-8", newline="") as stream:
        fields = tuple(asdict(witnesses[0]).keys())
        writer = csv.DictWriter(stream, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(asdict(witness) for witness in witnesses)
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
