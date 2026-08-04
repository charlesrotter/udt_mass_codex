#!/usr/bin/env python3
"""Fail-closed verifier for the query-bundle section/descent audit."""

from __future__ import annotations

import ast
import csv
import hashlib
import json
from copy import deepcopy
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def table(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def validate(
    law_rows: list[dict[str, str]],
    object_rows: list[dict[str, str]],
    premise_rows: list[dict[str, str]],
    source_rows: list[dict[str, str]],
) -> None:
    universe = table(HERE / "LAW_SLOT_UNIVERSE.tsv")
    expected_facets = {
        (row["slot_id"], facet)
        for row in universe
        for facet in row["facets_to_classify"].split(";")
    }
    actual_facets = [(row["slot_id"], row["facet"]) for row in law_rows]
    assert len(universe) == 8
    assert len(expected_facets) == len(actual_facets) == len(set(actual_facets)) == 36
    assert set(actual_facets) == expected_facets

    test_ids = [row["test_id"] for row in table(HERE / "DESCENT_TEST_UNIVERSE.tsv")]
    outcome_ids = [row["test_id"] for row in object_rows]
    assert len(test_ids) == len(outcome_ids) == len(set(outcome_ids)) == 18
    assert set(test_ids) == set(outcome_ids)

    by_test = {row["test_id"]: row for row in object_rows}
    assert by_test["D17"]["primary_class"] == "POSITIVE_BASIC_CONTROL"
    assert by_test["D18"]["primary_class"] == "NEGATIVE_BASIC_CONTROL"
    assert by_test["D03"]["spacetime_status"] == "NO_NATURAL_SECTION_OF_TM_FOLLOWS"
    assert by_test["D09"]["primary_class"] == "QUERY_CHANGE_NOT_FIELD_VARIATION"
    assert by_test["D12"]["primary_class"] == "STRATIFIED_RULE_REQUIRED"
    assert by_test["D15"]["primary_class"] == "FIBER_AGGREGATION_OPEN"
    assert "measure" in by_test["D15"]["caveat"]
    assert by_test["D02"]["primary_class"] == "QUERY_GROUPOID_LAW_NO_SECTION"
    assert "does_not_select_plane" in by_test["D05"]["caveat"]

    by_law = {(row["slot_id"], row["facet"]): row for row in law_rows}
    assert by_law[("L02", "query_variation")]["primary_class"] == "QUERY_CHANGE_NOT_FIELD_VARIATION"
    assert by_law[("L03", "ambient_metric_law")]["primary_class"] == "SPACETIME_BASIC_NO_SECTION"
    assert by_law[("L03", "query_bundle_law")]["primary_class"] == "QUERY_LAW_NO_SECTION"
    assert by_law[("L03", "projected_response")]["primary_class"] == "QUERY_EQUIVARIANT_NOT_BASIC"
    assert by_law[("L03", "fiber_aggregation")]["primary_class"] == "FIBER_AGGREGATION_OPEN"
    assert by_law[("L05", "base_boundary")]["primary_class"] == "SPACETIME_BOUNDARY_NO_SECTION"
    assert by_law[("L05", "pair_polarization")]["primary_class"] == "QUERY_EQUIVARIANT_NOT_BASIC"
    assert by_law[("L07", "typed_pair_path_law")]["primary_class"] == "QUERY_GROUPOID_LAW_NO_SECTION"
    assert by_law[("L08", "ambient_source")]["primary_class"] == "DOWNSTREAM_OPEN_MAY_NOT_REQUIRE_SECTION"
    assert not any("PHYSICAL_BRANCH_SELECTED" in row["primary_class"] for row in law_rows)

    classes = [row["primary_class"] for row in law_rows]
    assert classes.count("REALIZED_SECTION_REQUIRED") == 7
    assert classes.count("STRATIFIED_RULE_REQUIRED") == 4
    assert classes.count("FIBER_AGGREGATION_OPEN") == 2
    assert classes.count("SPACETIME_BASIC_NO_SECTION") == 4

    premise = {row["premise_id"]: row for row in premise_rows}
    assert len(premise) == 18
    assert premise["P17"]["status"] == "OPEN_NOT_SUPPLIED"
    assert premise["P08"]["status"] == "OPEN"
    assert premise["P15"]["status"] == "POSIT"

    assert len(source_rows) == 28
    assert len({row["path"] for row in source_rows}) == 28
    for row in source_rows:
        target = ROOT / row["path"]
        assert target.is_file()
        assert target.stat().st_size == int(row["bytes"])
        assert digest(target) == row["sha256"]


law = table(HERE / "LAW_SLOT_DESCENT_ATLAS.tsv")
objects = table(HERE / "OBJECT_DESCENT_ATLAS.tsv")
premises = table(HERE / "PREMISE_LEDGER.tsv")
sources = table(HERE / "SOURCE_MANIFEST.tsv")
validate(law, objects, premises, sources)

production = json.loads((HERE / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
independent = json.loads((HERE / "INDEPENDENT_RESULT.json").read_text(encoding="utf-8"))
assert production["status"] == independent["status"] == "PASS"
assert production["exact_checks"] == 26 and independent["exact_checks"] == 19
for key in ("vertical_projector_derivative", "projected_curvature_traces", "screen_readout_values", "pair_projector_ranks", "collision_projectors_distinct"):
    assert production[key] == independent[key]

tree = ast.parse((HERE / "verify_descent_independent.py").read_text(encoding="utf-8"))
imports = {
    alias.name.split(".")[0]
    for node in ast.walk(tree)
    if isinstance(node, ast.Import)
    for alias in node.names
} | {
    (node.module or "").split(".")[0]
    for node in ast.walk(tree)
    if isinstance(node, ast.ImportFrom)
}
assert imports <= {"__future__", "json", "fractions", "pathlib"}
assert "derive_descent_atlas" not in (HERE / "verify_descent_independent.py").read_text(encoding="utf-8")

review = json.loads((HERE / "FRESH_ADVERSARIAL_REVIEW_RESULT.json").read_text(encoding="utf-8"))
assert review["verdict"] == "PASS"
assert review["required_repairs"] == 0 and review["files_modified_by_reviewer"] == 0
assert digest(HERE / "FRESH_ADVERSARIAL_REVIEW.md") == review["review_output_sha256"]


def must_fail(catch_id: str, mutate) -> tuple[str, str, str]:
    l, o, p, s = deepcopy(law), deepcopy(objects), deepcopy(premises), deepcopy(sources)
    mutate(l, o, p, s)
    try:
        validate(l, o, p, s)
    except (AssertionError, KeyError):
        return catch_id, "REJECT", "PASS"
    raise AssertionError(f"catch did not fail: {catch_id}")


catches: list[tuple[str, str, str]] = []
catches.append(must_fail("C01_MISSING_LAW_FACET", lambda l, o, p, s: l.pop()))
catches.append(must_fail("C02_DUPLICATE_LAW_FACET", lambda l, o, p, s: l.append(deepcopy(l[0]))))
catches.append(must_fail("C03_PAIR_PROJECTOR_FALSE_BASIC", lambda l, o, p, s: o[17].update(primary_class="POSITIVE_BASIC_CONTROL")))
catches.append(must_fail("C04_QUERY_CHANGE_FALSE_FIELD_VARIATION", lambda l, o, p, s: next(row for row in l if row["slot_id"] == "L02" and row["facet"] == "query_variation").update(primary_class="REALIZED_SECTION_REQUIRED")))
catches.append(must_fail("C05_INVENTED_FIBER_AVERAGE", lambda l, o, p, s: next(row for row in l if row["slot_id"] == "L03" and row["facet"] == "fiber_aggregation").update(primary_class="SPACETIME_BASIC_NO_SECTION")))
catches.append(must_fail("C06_COLLISION_FALSE_SMOOTH", lambda l, o, p, s: next(row for row in o if row["test_id"] == "D12").update(primary_class="BRANCH_DERIVED_SECTION_REGULAR_ONLY")))
catches.append(must_fail("C07_SECTION_FALSE_INDEPENDENT", lambda l, o, p, s: next(row for row in o if row["test_id"] == "D03").update(spacetime_status="UNIQUE_SPACETIME_SECTION")))
catches.append(must_fail("C08_MISSING_OBJECT", lambda l, o, p, s: o.pop()))
catches.append(must_fail("C09_AMBIENT_LAW_FALSE_SECTION_REQUIRED", lambda l, o, p, s: next(row for row in l if row["slot_id"] == "L03" and row["facet"] == "ambient_metric_law").update(primary_class="REALIZED_SECTION_REQUIRED")))
catches.append(must_fail("C10_QUERY_COMPOSITION_FALSE_SECTION_REQUIRED", lambda l, o, p, s: next(row for row in o if row["test_id"] == "D02").update(primary_class="REALIZED_SECTION_REQUIRED")))
catches.append(must_fail("C11_BOUNDARY_POLARIZATION_FALSE_BASIC", lambda l, o, p, s: next(row for row in l if row["slot_id"] == "L05" and row["facet"] == "pair_polarization").update(primary_class="SPACETIME_BOUNDARY_NO_SECTION")))
catches.append(must_fail("C12_AMBIENT_SOURCE_FALSE_SECTION_REQUIRED", lambda l, o, p, s: next(row for row in l if row["slot_id"] == "L08" and row["facet"] == "ambient_source").update(primary_class="REALIZED_SECTION_REQUIRED")))
catches.append(must_fail("C13_ALL_LAWS_FALSE_SECTION_REQUIRED", lambda l, o, p, s: [row.update(primary_class="REALIZED_SECTION_REQUIRED") for row in l]))
catches.append(must_fail("C14_ZERO_MIXING_FALSE_SELECTOR", lambda l, o, p, s: next(row for row in o if row["test_id"] == "D05").update(caveat="zero_selects_plane")))
catches.append(must_fail("C15_MISSING_SOURCE", lambda l, o, p, s: s.pop()))
catches.append(must_fail("C16_PHYSICAL_SECTION_FALSE_DERIVED", lambda l, o, p, s: next(row for row in p if row["premise_id"] == "P08").update(status="DERIVED")))
catches.append(must_fail("C17_CARRIER_FALSE_DERIVED", lambda l, o, p, s: next(row for row in p if row["premise_id"] == "P15").update(status="DERIVED")))
catches.append(must_fail("C18_LOST_AGGREGATION_CAVEAT", lambda l, o, p, s: next(row for row in o if row["test_id"] == "D15").update(caveat="average_now")))

with (HERE / "CATCH_PROOFS.tsv").open("w", newline="", encoding="utf-8") as handle:
    writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
    writer.writerow(("catch_id", "expected", "observed"))
    writer.writerows(catches)

status = table(HERE / "STATUS_LEDGER.tsv")
overall = next(row for row in status if row["object"] == "overall_audit")["status"]
assert overall in {
    "PROVISIONAL_PENDING_FRESH_ADVERSARIAL_REVIEW",
    "VERIFIED_WITH_CAVEATS_BOUNDED_DESCENT_AND_SECTION_NECESSITY_ATLAS",
}
assert any(row["object"] == "native_law_home_and_ownership" and row["status"] == "OPEN_SMALLEST_TYPE_LEVEL_JOINT" for row in status)

result = {
    "status": "PASS" if overall.startswith("VERIFIED") else "PASS_PRE_REVIEW",
    "outcome": "TYPED_SPLIT_QUERY_AND_SPACETIME_LAWS",
    "law_slots": 8,
    "law_facets": len(law),
    "object_classes": len(objects),
    "variation_classes": len(table(HERE / "VARIATION_OWNERSHIP_ATLAS.tsv")),
    "boundary_classes": len(table(HERE / "BOUNDARY_DESCENT_ATLAS.tsv")),
    "stratified_classes": len(table(HERE / "STRATIFIED_SECTION_LEDGER.tsv")),
    "production_exact_checks": production["exact_checks"],
    "independent_exact_checks": independent["exact_checks"],
    "catch_proofs": len(catches),
    "frozen_sources": len(sources),
    "fresh_adversarial_review": review["verdict"],
    "required_repairs": review["required_repairs"],
    "smallest_open_joint": "NATIVE_LAW_HOME_CODOMAIN_AND_OWNERSHIP_RULE",
    "maximum_conclusion": "QUERY_KINEMATICS_AND_AMBIENT_GEOMETRY_DO_NOT_REQUIRE_UNIVERSAL_SECTION;PAIR_PROJECTED_PHYSICAL_RESPONSE_REQUIRES_QUERY_TYPING_OR_REALIZED_BRANCH_STRATIFIED_REDUCTION",
}
(HERE / "VERIFICATION_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
print(json.dumps(result, sort_keys=True))
