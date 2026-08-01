#!/usr/bin/env python3
"""Independent fail-closed verification for the stability-family ontology audit."""

from __future__ import annotations

import copy
import csv
import hashlib
import json
from pathlib import Path
from typing import Callable


ROOT = Path(__file__).resolve().parents[1]
PKG = Path(__file__).resolve().parent


def read_tsv(name: str) -> list[dict[str, str]]:
    with (PKG / name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def validate(state: dict[str, object]) -> None:
    families = state["families"]
    axes = state["axes"]
    pairs = state["pairs"]
    pair_axes = state["pair_axes"]
    gates = state["gates"]
    taxonomy = state["taxonomy"]
    regrades = state["regrades"]
    readiness = state["readiness"]
    premises = state["premises"]
    authorities = state["authorities"]
    result = state["result"]
    source = state["source"]
    assert isinstance(families, list) and isinstance(axes, list) and isinstance(pairs, list) and isinstance(pair_axes, list)
    assert isinstance(gates, list) and isinstance(taxonomy, list) and isinstance(regrades, list)
    assert isinstance(readiness, list) and isinstance(premises, list) and isinstance(authorities, list)
    assert isinstance(result, dict) and isinstance(source, list)

    family_ids = [row["family_id"] for row in families]
    if family_ids != [f"F{i:02d}" for i in range(1, 8)] or len(family_ids) != len(set(family_ids)):
        raise AssertionError("missing or duplicate family")
    exact_ontology = {
        "F01": "CONDITIONAL_REALIZED_SOLUTION_FAMILY",
        "F02": "CONDITIONAL_REALIZED_SOLUTION_FAMILY",
        "F03": "CONTROL_STRATUM",
        "F04": "CONDITIONAL_REALIZED_SOLUTION_FAMILY",
        "F05": "STRUCTURAL_COMPLETION_CLASS",
        "F06": "EXACT_EMPTY_SCOPE",
        "F07": "FORMAL_MODULE_CLASS",
    }
    by_family = {row["family_id"]: row for row in families}
    if any(by_family[key]["primary_ontology"] != value for key, value in exact_ontology.items()):
        raise AssertionError("ontology promotion or regression")
    if by_family["F01"]["parent_object"] == by_family["F02"]["parent_object"]:
        raise AssertionError("open census fork collapsed to one parent solution object")
    if {by_family["F01"]["independence_status"], by_family["F02"]["independence_status"]} != {"CENSUS_FORK_OPEN_NO_COMMON_SOLUTION_SET"}:
        raise AssertionError("open census solution-set relation lost")
    if by_family["F04"]["parent_object"] == by_family["F01"]["parent_object"]:
        raise AssertionError("conditional Hopfion silently merged with P4")
    if "conditional" not in by_family["F04"]["maximum_claim"]:
        raise AssertionError("Hopfion premise stamp lost")

    expected_axis_keys = {(f"F{i:02d}", f"A{j:02d}") for i in range(1, 8) for j in range(1, 11)}
    axis_keys = [(row["family_id"], row["axis_id"]) for row in axes]
    if len(axes) != 70 or set(axis_keys) != expected_axis_keys or len(axis_keys) != len(set(axis_keys)):
        raise AssertionError("axis coverage failure")
    axis_by_key = {(row["family_id"], row["axis_id"]): row for row in axes}
    required_axis = {
        ("F01", "A10"): "CENSUS_FORK_RELATION",
        ("F02", "A10"): "CENSUS_FORK_RELATION",
        ("F04", "A06"): "CARRIER_POSIT",
        ("F04", "A07"): "STATIC_ONLY",
        ("F05", "A02"): "STRUCTURAL_ONLY",
        ("F05", "A10"): "CONSTRAINT_ON_REGISTERED_BRANCHES",
        ("F06", "A05"): "NOT_APPLICABLE",
        ("F07", "A01"): "PARTIAL_FORMAL_MODULES",
        ("F07", "A02"): "WHOLE_EQUATION_OPEN",
    }
    if any(axis_by_key[key]["axis_status"] != value for key, value in required_axis.items()):
        raise AssertionError("load-bearing axis status changed")

    prereg_pairs = read_tsv("PAIRWISE_UNIVERSE.tsv")
    expected_pairs = {(row["pair_id"], row["left_family"], row["right_family"]) for row in prereg_pairs}
    actual_pairs = [(row["pair_id"], row["left_family"], row["right_family"]) for row in pairs]
    if len(pairs) != 28 or set(actual_pairs) != expected_pairs or len(actual_pairs) != len(set(actual_pairs)):
        raise AssertionError("pair coverage failure")
    relation_by_pair = {(row["left_family"], row["right_family"]): row["relation"] for row in pairs}
    expected_relations = {
        ("F01", "F02"): "FORMAL_EMBEDDING_ONLY",
        ("F01", "F03"): "CONDITIONAL_ANALOGY_ONLY",
        ("F01", "F04"): "NO_DERIVED_RELATION",
        ("F01", "F05"): "STRUCTURAL_CONSTRAINT_ON",
        ("F01", "F06"): "NO_DERIVED_RELATION",
        ("F01", "F07"): "NO_DERIVED_RELATION",
        ("F04", "F07"): "NO_DERIVED_RELATION",
        ("F05", "F06"): "STRUCTURAL_CONSTRAINT_ON",
    }
    if any(relation_by_pair.get(key) != value for key, value in expected_relations.items()):
        raise AssertionError("load-bearing pair relation changed")
    if sum(row["relation"] == "SELF" for row in pairs) != 7:
        raise AssertionError("diagonal relation failure")
    expected_pair_axis_keys = {
        (row["pair_id"], f"A{axis:02d}")
        for row in prereg_pairs if row["left_family"] != row["right_family"]
        for axis in range(1, 11)
    }
    pair_axis_keys = [(row["pair_id"], row["axis_id"]) for row in pair_axes]
    if len(pair_axes) != 210 or set(pair_axis_keys) != expected_pair_axis_keys or len(pair_axis_keys) != len(set(pair_axis_keys)):
        raise AssertionError("pair-axis coverage failure")
    pair_axis_by_key = {(row["pair_id"], row["axis_id"]): row for row in pair_axes}
    if pair_axis_by_key[("P02", "A10")]["comparison_status"] != "NO_SOLUTION_SET_RELATION":
        raise AssertionError("F01/F02 formal relation promoted or erased")
    if pair_axis_by_key[("P20", "A10")]["comparison_status"] != "RELATION_OPEN":
        raise AssertionError("P4/Hopfion no-relation promoted to disjointness")
    for pair_id in ("P06", "P07", "P12", "P16", "P18", "P25", "P27"):
        if pair_axis_by_key[(pair_id, "A09")]["comparison_status"] != "RELATED_P4_LINEAGES_NO_OBJECT_MAP":
            raise AssertionError("related P4 lineage mislabeled as distinct")

    gate_by_id = {row["gate_id"]: row for row in gates}
    if set(gate_by_id) != {f"G{i:02d}" for i in range(1, 8)}:
        raise AssertionError("partition gate coverage failure")
    if any(gate_by_id[key]["status"] != "FAIL" for key in ("G01", "G02", "G03", "G04", "G05", "G07")):
        raise AssertionError("failed partition gate promoted")
    if gate_by_id["G06"]["status"] != "PASS_AFTER_CORRECTION":
        raise AssertionError("type-separation correction missing")

    if [row["taxonomy_id"] for row in taxonomy] != [f"T{i:02d}" for i in range(1, 7)]:
        raise AssertionError("taxonomy coverage failure")
    taxonomy_by_id = {row["taxonomy_id"]: row for row in taxonomy}
    if taxonomy_by_id["T05"]["members_or_components"] != "none established":
        raise AssertionError("native family invented")
    if taxonomy_by_id["T06"]["status"] != "TWO_RESEARCH_PROGRAMS_NO_DERIVED_JOIN":
        raise AssertionError("conditional streams silently joined")

    if [row["regrade_id"] for row in regrades] != [f"N{i:02d}" for i in range(1, 9)]:
        raise AssertionError("claim regrade coverage failure")
    if "WITHDRAWN_AS_PHYSICAL_COUNT" not in {row["status"] for row in regrades}:
        raise AssertionError("physical family count not withdrawn")
    if [row["family_id"] for row in readiness] != family_ids:
        raise AssertionError("readiness coverage failure")
    if any(row["promotion"] != "NO" for row in readiness):
        raise AssertionError("readiness promotion")
    if "GPU_READY" in "\n".join(str(value) for row in readiness for value in row.values()):
        raise AssertionError("GPU readiness invented")
    if [row["premise_id"] for row in premises] != [f"L{i:02d}" for i in range(1, 30)]:
        raise AssertionError("premise coverage failure")
    premise_by_id = {row["premise_id"]: row for row in premises}
    if premise_by_id["L04"]["status"] != "OPEN_DOMAIN_DEFINITION_CHOICE":
        raise AssertionError("census fork promoted")
    if premise_by_id["L20"]["status"] != "OPEN" or premise_by_id["L25"]["status"] != "OPEN" or premise_by_id["L27"]["status"] != "OPEN":
        raise AssertionError("realization time or native matter premise promoted")

    if result.get("outcome") != "OPERATIONAL_EVIDENCE_MAP_NOT_SOLUTION_PARTITION":
        raise AssertionError("overall outcome promoted")
    exact_result = {
        "source_artifact_count": 1608,
        "authority_count": 18,
        "inherited_label_count": 7,
        "axis_cell_count": 70,
        "pair_count": 28,
        "pair_axis_cell_count": 210,
        "native_realized_family_count": 0,
        "conditional_realized_family_count": 3,
        "conditional_research_program_count": 2,
        "readiness_promotions": 0,
        "solves_run": 0,
        "gpu_runs": 0,
    }
    if any(result.get(key) != value for key, value in exact_result.items()):
        raise AssertionError("result census or authority boundary changed")

    paths = [row["path"] for row in source]
    if len(paths) != 1608 or paths != sorted(paths) or len(paths) != len(set(paths)):
        raise AssertionError("source freeze changed")
    if any(not (ROOT / row["path"]).is_file() or sha256(ROOT / row["path"]) != row["sha256"] for row in source):
        raise AssertionError("source byte mismatch")
    source_set = set(paths)
    if len(authorities) != 18 or len({row["anchor_id"] for row in authorities}) != 18:
        raise AssertionError("authority census failure")
    for row in authorities:
        if row["path"] not in source_set:
            raise AssertionError("authority outside source freeze")
        if sha256(ROOT / row["path"]) != row["sha256"]:
            raise AssertionError("authority hash mismatch")

    # Independent set-theoretic check: a proposed partition must consist solely
    # of configuration-bearing classes. Control, structural, formal, and empty
    # labels fail this necessary condition before any physics interpretation.
    non_solution_types = {"CONTROL_STRATUM", "STRUCTURAL_COMPLETION_CLASS", "FORMAL_MODULE_CLASS", "EXACT_EMPTY_SCOPE"}
    if len({row["primary_ontology"] for row in families} & non_solution_types) != 4:
        raise AssertionError("heterogeneous ontology evidence erased")


def main() -> None:
    state: dict[str, object] = {
        "families": read_tsv("FAMILY_ONTOLOGY_LEDGER.tsv"),
        "axes": read_tsv("FAMILY_AXIS_MATRIX.tsv"),
        "pairs": read_tsv("PAIRWISE_RELATION_ATLAS.tsv"),
        "pair_axes": read_tsv("PAIR_AXIS_MATRIX.tsv"),
        "gates": read_tsv("PARTITION_GATE_LEDGER.tsv"),
        "taxonomy": read_tsv("CORRECTED_STABILITY_TAXONOMY.tsv"),
        "regrades": read_tsv("NEGATIVE_AND_CLAIM_REGRADE.tsv"),
        "readiness": read_tsv("READINESS_REGRADE.tsv"),
        "premises": read_tsv("PREMISE_LEDGER.tsv"),
        "authorities": read_tsv("SOURCE_AUTHORITY_LEDGER.tsv"),
        "result": json.loads((PKG / "AUDIT_RESULT.json").read_text(encoding="utf-8")),
        "source": read_tsv("EFFECTIVE_SOURCE_INVENTORY.tsv"),
    }
    validate(state)

    mutations: list[tuple[str, Callable[[dict[str, object]], None]]] = []
    mutations.append(("missing_family", lambda s: s["families"].pop()))
    mutations.append(("duplicate_family", lambda s: s["families"].append(copy.deepcopy(s["families"][0]))))
    mutations.append(("census_fork_collapsed", lambda s: s["families"][1].update(parent_object=s["families"][0]["parent_object"])))
    mutations.append(("F03_promoted_to_family", lambda s: s["families"][2].update(primary_ontology="NATIVE_REALIZED_SOLUTION_FAMILY")))
    mutations.append(("Hopfion_promoted_native", lambda s: s["families"][3].update(primary_ontology="NATIVE_REALIZED_SOLUTION_FAMILY")))
    mutations.append(("F05_promoted_to_family", lambda s: s["families"][4].update(primary_ontology="NATIVE_REALIZED_SOLUTION_FAMILY")))
    mutations.append(("F06_empty_promoted", lambda s: s["families"][5].update(primary_ontology="NATIVE_REALIZED_SOLUTION_FAMILY")))
    mutations.append(("F07_formal_promoted", lambda s: s["families"][6].update(primary_ontology="NATIVE_REALIZED_SOLUTION_FAMILY")))
    mutations.append(("missing_axis_cell", lambda s: s["axes"].pop()))
    mutations.append(("carrier_posit_lost", lambda s: next(row for row in s["axes"] if row["family_id"] == "F04" and row["axis_id"] == "A06").update(axis_status="DERIVED")))
    mutations.append(("missing_pair", lambda s: s["pairs"].pop()))
    mutations.append(("missing_pair_axis_cell", lambda s: s["pair_axes"].pop()))
    mutations.append(("P4_Hopfion_join_invented", lambda s: next(row for row in s["pairs"] if row["left_family"] == "F01" and row["right_family"] == "F04").update(relation="OVERLAPPING_CONFIGURATION_SETS")))
    mutations.append(("partition_gate_promoted", lambda s: s["gates"][0].update(status="PASS")))
    mutations.append(("native_family_invented", lambda s: s["taxonomy"][4].update(members_or_components="F04")))
    mutations.append(("conditional_streams_joined", lambda s: s["taxonomy"][5].update(status="NATIVE_FAMILY_PARTITION_DERIVED")))
    mutations.append(("physical_count_restored", lambda s: s["regrades"][7].update(status="RETAINED")))
    mutations.append(("readiness_promoted", lambda s: s["readiness"][1].update(promotion="YES", ontology_corrected_readiness="GPU_READY")))
    mutations.append(("native_time_promoted", lambda s: s["premises"][24].update(status="DERIVED")))
    mutations.append(("result_promoted", lambda s: s["result"].update(outcome="NATIVE_FAMILY_PARTITION_DERIVED")))
    mutations.append(("native_family_count_promoted", lambda s: s["result"].update(native_realized_family_count=1)))
    mutations.append(("gpu_run_hidden", lambda s: s["result"].update(gpu_runs=1)))
    mutations.append(("authority_outside_freeze", lambda s: s["authorities"][0].update(path="outside-freeze.md")))

    catches = []
    for name, mutate in mutations:
        candidate = copy.deepcopy(state)
        mutate(candidate)
        rejected = False
        try:
            validate(candidate)
        except (AssertionError, FileNotFoundError):
            rejected = True
        if not rejected:
            raise RuntimeError(f"mutation escaped: {name}")
        catches.append({"catch_id": f"C{len(catches)+1:02d}", "mutation": name, "result": "REJECTED", "exercised": "YES"})

    with (PKG / "CATCH_PROOFS.tsv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(catches[0]), delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(catches)
    verification = {
        "verdict": "PASS",
        "families": 7,
        "axis_cells": 70,
        "pairs": 28,
        "pair_axis_cells": 210,
        "partition_gates": 7,
        "source_authorities": 18,
        "source_artifacts": 1608,
        "native_realized_families": 0,
        "readiness_promotions": 0,
        "catch_proofs_passed": len(catches),
        "catch_proofs_total": len(catches),
        "independent_route": "set-theoretic necessary condition separating solution-bearing from control, structural, empty, and formal classes",
    }
    (PKG / "VERIFICATION_RESULT.json").write_text(json.dumps(verification, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    stdout = f"PASS ontology verification: families=7 axes=70 pair_axes=210 pairs=28 gates=7 authorities=18 catches={len(catches)}/{len(catches)} sources=1608 native=0 promotions=0\n"
    (PKG / "VERIFICATION_STDOUT.txt").write_text(stdout, encoding="utf-8")
    print(stdout, end="")


if __name__ == "__main__":
    main()
