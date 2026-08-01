#!/usr/bin/env python3
"""Independently reconstruct ontology classes and load-bearing relations from raw sources."""

from __future__ import annotations

import copy
import csv
import hashlib
import json
from pathlib import Path
from typing import Callable


ROOT = Path(__file__).resolve().parents[1]
PKG = Path(__file__).resolve().parent


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def local(name: str) -> list[dict[str, str]]:
    return read_tsv(PKG / name)


def expand_basis(value: str) -> set[str]:
    found: set[str] = set()
    for part in value.split(";"):
        if "-" in part:
            left, right = part.split("-", 1)
            start, stop = int(left[1:]), int(right[1:])
            found.update(f"A{index:02d}" for index in range(start, stop + 1))
        else:
            found.add(part)
    return found


def source_classification(atlas_row: dict[str, str]) -> str:
    blob = "\t".join(atlas_row.values())
    upper_blob = blob.upper()
    if atlas_row["stability_test"] == "NOT_APPLICABLE_EMPTY_DOMAIN" and "EMPTY" in atlas_row["existence"]:
        return "EXACT_EMPTY_SCOPE"
    if atlas_row["stability_test"] == "NONE" and "STRUCTURAL" in atlas_row["hypothesis_role"]:
        return "STRUCTURAL_COMPLETION_CLASS"
    if "FORMAL" in atlas_row["configuration_type"].upper() and "FORMAL" in atlas_row["overall_grade"].upper():
        return "FORMAL_MODULE_CLASS"
    if "CONTROL" in atlas_row["hypothesis_role"] and "CONTROL" in atlas_row["overall_grade"]:
        return "CONTROL_STRATUM"
    if "CONDITIONAL" in upper_blob and any(token in atlas_row["existence"].lower() for token in ("witness", "landing class", "observed")):
        return "CONDITIONAL_REALIZED_SOLUTION_FAMILY"
    return "OPEN_IDENTITY_OR_RELATION"


def validate(state: dict[str, object]) -> None:
    output_families = state["families"]
    output_axes = state["axes"]
    output_pairs = state["pairs"]
    output_pair_axes = state["pair_axes"]
    output_premises = state["premises"]
    output_crosswalk = state["crosswalk"]
    output_result = state["result"]
    assert isinstance(output_families, list) and isinstance(output_axes, list) and isinstance(output_pairs, list)
    assert isinstance(output_pair_axes, list) and isinstance(output_premises, list)
    assert isinstance(output_crosswalk, list) and isinstance(output_result, dict)

    atlas = read_tsv(ROOT / "udt_stability_hypothesis_cross_family_atlas_2026-08-01/FAMILY_ATLAS.tsv")
    if [row["family_id"] for row in atlas] != [f"F{i:02d}" for i in range(1, 8)]:
        raise AssertionError("raw family atlas changed")
    independently_derived = {row["family_id"]: source_classification(row) for row in atlas}
    emitted = {row["family_id"]: row["primary_ontology"] for row in output_families}
    if emitted != independently_derived:
        raise AssertionError(f"source-derived ontology mismatch: {emitted} != {independently_derived}")

    # The decisive F01/F02 sources establish a formal domain/one-form pullback and explicitly
    # leave the census choice open; this is not a shared realized solution-set theorem.
    forcing = (ROOT / "udt_p4_bookkeeping_forcing_2026-07-29/EXACT_DERIVATION.md").read_text(encoding="utf-8")
    registration = (ROOT / "udt_p4_routeD_field_registration_2026-07-29/AUDIT_REPORT.md").read_text(encoding="utf-8")
    for needle in ("PULLBACK of the field-fork one-form", "Census-fork verdict: OPEN", "pullback-vanishing is strictly weaker"):
        if needle not in forcing:
            raise AssertionError(f"missing raw census relation: {needle}")
    for needle in ("fork is real", "PURE domain-definition choice", "response space is defined + typed, NOT exhausted"):
        if needle not in registration:
            raise AssertionError(f"missing raw registration relation: {needle}")
    pair_map = {(row["left_family"], row["right_family"]): row for row in output_pairs}
    if pair_map[("F01", "F02")]["relation"] != "FORMAL_EMBEDDING_ONLY":
        raise AssertionError("raw constant-section pullback misclassified")
    if any(token in pair_map[("F01", "F02")]["finding"] for token in ("same parent solution", "same object")):
        raise AssertionError("open census fork collapsed")

    # The closure sweep explicitly owns a formal F02/F07 relation and owns no corresponding
    # F01/F07 or F03/F07 row. The output must not manufacture those relations.
    closure = read_tsv(ROOT / "udt_stability_derivation_closure_sweep_2026-08-01/OBJECT_STATUS_LEDGER.tsv")
    closure_families = {row["family"] for row in closure}
    if "F02;F07" not in closure_families:
        raise AssertionError("raw F02/F07 closure rows missing")
    if pair_map[("F02", "F07")]["relation"] != "FORMAL_EMBEDDING_ONLY":
        raise AssertionError("raw F02/F07 formal relation lost")
    if pair_map[("F01", "F07")]["relation"] != "NO_DERIVED_RELATION" or pair_map[("F03", "F07")]["relation"] != "NO_DERIVED_RELATION":
        raise AssertionError("unsupported formal embedding invented")

    axis_map = {(row["family_id"], row["axis_id"]): row for row in output_axes}
    f05_relation = axis_map[("F05", "A10")]
    if f05_relation["axis_status"] != "CONSTRAINT_ON_REGISTERED_BRANCHES" or "no whole-label F03 map" not in f05_relation["finding"]:
        raise AssertionError("F05 family-axis relation contradicts F03/F05 pair ruling")
    if pair_map[("F03", "F05")]["relation"] != "NO_DERIVED_RELATION":
        raise AssertionError("F03/F05 whole-label relation invented")

    pair_axis_map = {(row["pair_id"], row["axis_id"]): row for row in output_pair_axes}
    for pair_id in ("P06", "P07", "P12", "P16", "P18", "P25", "P27"):
        row = pair_axis_map[(pair_id, "A09")]
        if row["comparison_status"] != "RELATED_P4_LINEAGES_NO_OBJECT_MAP" or "related P4 audit lineages" not in row["finding"]:
            raise AssertionError("same-P4 source lineage mislabeled as distinct")

    # F03 and F06 are operational unions. Componentwise facts cannot become whole-label
    # containment relations.
    family_map = {row["family_id"]: row for row in output_families}
    if "UNION" not in family_map["F03"]["realization_status"] or "UNION" not in family_map["F06"]["realization_status"]:
        raise AssertionError("union-valued family status erased")
    forbidden_containment = {"CONTROL_STRATUM_OF", "EMPTY_SUBSCOPE_OF"}
    for key in (("F01", "F03"), ("F02", "F03"), ("F01", "F06"), ("F02", "F06")):
        if pair_map[key]["relation"] in forbidden_containment:
            raise AssertionError("component relation promoted to whole-label containment")

    # Every emitted source basis must resolve to one of the 18 source authorities.
    authority_ids = {row["anchor_id"] for row in local("SOURCE_AUTHORITY_LEDGER.tsv")}
    if authority_ids != {f"A{i:02d}" for i in range(1, 19)}:
        raise AssertionError("source authority universe changed")
    for collection in (output_families, output_axes, output_pairs, output_pair_axes, output_premises, output_crosswalk):
        for row in collection:
            basis = row.get("source_basis", "")
            if not basis or not expand_basis(basis) <= authority_ids:
                raise AssertionError(f"invalid source basis: {basis}")
            if any(not value for value in row.values()):
                raise AssertionError("empty adjudication cell")

    if len(output_pair_axes) != 210:
        raise AssertionError("pair-axis coverage lost")
    if len(output_premises) != 29:
        raise AssertionError("branch-level premise census lost")
    premise = {row["premise_id"]: row for row in output_premises}
    required = {
        "L04": "OPEN_DOMAIN_DEFINITION_CHOICE",
        "L08": "BOUNDED_OPEN",
        "L10": "CHOSE_SIGN_INVARIANT_SCOPE",
        "L13": "CONDITIONALITIES_TRAVEL",
        "L17": "EXACT_EMPTY_SCOPED",
        "L18": "EXACT_EMPTY_SCOPED",
        "L20": "OPEN",
        "L22": "POSIT",
        "L24": "CHOSE_COMPUTATIONAL",
        "L25": "OPEN",
        "L27": "OPEN",
    }
    if any(premise[key]["status"] != value for key, value in required.items()):
        raise AssertionError("load-bearing premise promoted or erased")

    registry = (ROOT / "NEGATIVES_REGISTRY.md").read_text(encoding="utf-8")
    if "#61." not in registry or "CONDITIONS-CHANGED" not in registry:
        raise AssertionError("negative registry control missing")
    if len(output_crosswalk) != 8 or {row["crosswalk_id"] for row in output_crosswalk} != {f"X{i:02d}" for i in range(1, 9)}:
        raise AssertionError("negative-registry crosswalk incomplete")
    if next(row for row in output_crosswalk if row["crosswalk_id"] == "X04")["registry_match"] != "RELATED_HISTORICAL_ENTRY_61":
        raise AssertionError("Hopfion historical premise distinction lost")

    # Necessary set-theoretic condition: four raw-source-derived labels are not
    # solution-family sets. Therefore the seven labels cannot be a seven-way solution
    # partition regardless of the still-open exact F01/F02 solution-set relation.
    non_solution = {"CONTROL_STRATUM", "STRUCTURAL_COMPLETION_CLASS", "FORMAL_MODULE_CLASS", "EXACT_EMPTY_SCOPE"}
    if sum(value in non_solution for value in independently_derived.values()) != 4:
        raise AssertionError("source-derived heterogeneous-type obstruction disappeared")
    if output_result.get("outcome") != "OPERATIONAL_EVIDENCE_MAP_NOT_SOLUTION_PARTITION":
        raise AssertionError("source-derived maximum outcome changed")
    if output_result.get("native_realized_family_count") != 0 or output_result.get("readiness_promotions") != 0:
        raise AssertionError("native family/readiness promotion")

    effective = local("EFFECTIVE_SOURCE_INVENTORY.tsv")
    if len(effective) != 1608:
        raise AssertionError("effective source census changed")
    for row in effective:
        path = ROOT / row["path"]
        if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != row["sha256"]:
            raise AssertionError("effective source byte mismatch")


def main() -> None:
    state: dict[str, object] = {
        "families": local("FAMILY_ONTOLOGY_LEDGER.tsv"),
        "axes": local("FAMILY_AXIS_MATRIX.tsv"),
        "pairs": local("PAIRWISE_RELATION_ATLAS.tsv"),
        "pair_axes": local("PAIR_AXIS_MATRIX.tsv"),
        "premises": local("PREMISE_LEDGER.tsv"),
        "crosswalk": local("NEGATIVE_REGISTRY_CROSSWALK.tsv"),
        "result": json.loads((PKG / "AUDIT_RESULT.json").read_text(encoding="utf-8")),
    }
    validate(state)
    mutations: list[tuple[str, Callable[[dict[str, object]], None]]] = [
        ("raw_classification_disagrees", lambda s: s["families"][0].update(primary_ontology="SHARED_PARENT_SOLUTION_SECTOR")),
        ("census_parent_identity_invented", lambda s: s["pairs"][1].update(relation="SAME_OBJECT_DIFFERENT_SECTOR")),
        ("F03_component_containment_promoted", lambda s: s["pairs"][2].update(relation="CONTROL_STRATUM_OF")),
        ("F06_component_containment_promoted", lambda s: s["pairs"][5].update(relation="EMPTY_SUBSCOPE_OF")),
        ("unsupported_F01_F07_embedding", lambda s: s["pairs"][6].update(relation="FORMAL_EMBEDDING_ONLY")),
        ("F05_F03_crosscut_restored", lambda s: next(row for row in s["axes"] if row["family_id"] == "F05" and row["axis_id"] == "A10").update(axis_status="CONSTRAINT_ON_PARENT", finding="cross-cuts F01/F02/F03")),
        ("same_P4_lineage_called_distinct", lambda s: next(row for row in s["pair_axes"] if row["pair_id"] == "P16" and row["axis_id"] == "A09").update(comparison_status="DISTINCT_SOURCE_LINEAGES")),
        ("missing_pair_axis", lambda s: s["pair_axes"].pop()),
        ("census_fork_selected", lambda s: s["premises"][3].update(status="DERIVED_CONSTANTS")),
        ("wall_germ_closed", lambda s: s["premises"][7].update(status="DERIVED_COMPLETE")),
        ("carrier_promoted", lambda s: s["premises"][21].update(status="DERIVED")),
        ("time_promoted", lambda s: s["premises"][24].update(status="DERIVED")),
        ("missing_negative_crosswalk", lambda s: s["crosswalk"].pop()),
        ("native_family_promoted", lambda s: s["result"].update(native_realized_family_count=1)),
    ]
    catches = []
    for name, mutation in mutations:
        candidate = copy.deepcopy(state)
        mutation(candidate)
        rejected = False
        try:
            validate(candidate)
        except (AssertionError, FileNotFoundError):
            rejected = True
        if not rejected:
            raise RuntimeError(f"source-derived mutation escaped: {name}")
        catches.append({"catch_id": f"S{len(catches)+1:02d}", "mutation": name, "result": "REJECTED", "exercised": "YES"})
    with (PKG / "SOURCE_DERIVED_CATCH_PROOFS.tsv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(catches[0]), delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(catches)
    result = {
        "verdict": "PASS",
        "route": "raw-source field classification plus exact census-pullback and joint-realization anchors",
        "source_artifacts": 1608,
        "source_derived_family_classes": 7,
        "non_solution_classes": 4,
        "branch_level_premises": 29,
        "negative_crosswalk_rows": 8,
        "catch_proofs_passed": len(catches),
        "catch_proofs_total": len(catches),
    }
    (PKG / "SOURCE_DERIVED_VERIFICATION_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    stdout = f"PASS source-derived ontology verification: sources=1608 classes=7 nonsolution=4 premises=29 crosswalk=8 catches={len(catches)}/{len(catches)}\n"
    (PKG / "SOURCE_DERIVED_VERIFICATION_STDOUT.txt").write_text(stdout, encoding="utf-8")
    print(stdout, end="")


if __name__ == "__main__":
    main()
