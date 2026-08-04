#!/usr/bin/env python3
"""Fail-closed semantic and algebraic verifier for the selector atlas."""

from __future__ import annotations

import copy
import csv
import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def table(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def validate(
    universe: list[dict[str, str]],
    outcomes: list[dict[str, str]],
    production: dict[str, object],
    independent: dict[str, object],
) -> None:
    expected = [f"M{i:02d}" for i in range(18)]
    require([row["selector_id"] for row in universe] == expected, "selector universe changed")
    require([row["selector_id"] for row in outcomes] == expected, "missing duplicate or reordered outcome")
    by_id = {row["selector_id"]: row for row in outcomes}
    require(len(by_id) == 18, "duplicate outcome")
    require(by_id["M00"]["ruling"] == "UNIVERSAL_OBSTRUCTION_EXACT", "full isotropy softened")
    require(by_id["M00"]["certificate"] == "NO_RANK2_IDEMPOTENT_IN_SCALAR_COMMUTANT", "full certificate lost")
    require(by_id["M01"]["ruling"] == "CONDITIONAL_INPUT_NOT_METRIC_SELECTOR", "coframe presentation promoted")
    require(by_id["M02"]["ruling"] == "DERIVED_CONTAINER_NO_NATURAL_SECTION", "query bundle promoted to section")
    require(by_id["M03"]["ruling"] == "FIRST_JET_INSUFFICIENT_FOR_RANK2", "one phi line promoted")
    require(by_id["M04"]["ruling"] == "BRANCH_LOCAL_CONDITIONAL", "phi Hessian scope changed")
    require("COMPLEX_NULL_JORDAN_NULL_OR_ZERO_DPHI_TYPE_CHANGE" in by_id["M04"]["obstruction_domain"], "phi Hessian strata omitted")
    require(by_id["M05"]["ruling"] == "BRANCH_LOCAL_POSITIVE_COLLISION_OBSTRUCTED", "Ricci scope changed")
    require(by_id["M06"]["ruling"] == "CONDITIONAL_CAPABILITY_NO_FROZEN_WITNESS", "bivector witness invented")
    require(by_id["M07"]["ruling"] == "CONDITIONAL_CAPABILITY_NO_FROZEN_WITNESS", "gradient witness invented")
    require(by_id["M08"]["ruling"] == "BRANCH_LOCAL_CONDITIONAL", "Killing selector promoted")
    require(by_id["M09"]["ruling"] == "BRANCH_LOCAL_CONDITIONAL", "holonomy selector promoted")
    require(by_id["M10"]["ruling"] == "BRANCH_LOCAL_POSITIVE_DEFECT_OBSTRUCTED", "intrinsic defect discarded")
    require(by_id["M11"]["ruling"] == "NO_UNIQUE_RECIPROCAL_SPLIT", "round control discarded")
    require(by_id["M12"]["ruling"] == "BRANCH_LOCAL_POSITIVE_NOT_PHYSICAL", "squashed branch promoted")
    require(by_id["M13"]["ruling"] == "ROUND_CONTROL_OBSTRUCTED_OTHER_BRANCH_CAPABILITY_OPEN", "whole-solution scope wrong")
    require(by_id["M14"]["ruling"] == "OPEN_NO_TYPED_SELECTOR", "boundary selector promoted")
    require(by_id["M15"]["ruling"] == "NATURAL_SET_NOT_REALIZED_SPLIT", "set-valued/member conflated")
    require(by_id["M16"]["ruling"] == "NO_GLOBAL_SMOOTH_FIXED_RANK_FROM_CURRENT_DATA", "rank changes erased")
    require(by_id["M17"]["ruling"] == "EXCLUDED_NOT_TESTED_AS_METRIC_SELECTOR", "downstream selector imported")
    require(production["result"] == "BRANCH_LOCAL_SELECTORS_ONLY_UNIVERSAL_OBSTRUCTED", "outcome changed")
    checks = production["checks"]
    require(checks["full_commutant_rank"] == 15, "full commutant rank")
    require(checks["round_spatial_commutant_rank"] == 14, "round commutant rank")
    require(checks["round_invariant_projector_ranks"] == [0, 1, 3, 4], "round idempotents")
    require(checks["null_little_group_commutant_rank"] == 14, "null little-group rank")
    require(checks["null_little_group_idempotent_ranks"] == [0, 4], "null idempotents")
    require(checks["synthetic_operator_equals_2I_plus_2Ricci_q02"] is True, "Q02 Ricci linkage")
    require(checks["ricci_projector_rank"] == 2, "Ricci projector rank")
    require(checks["ricci_projector_equivariant_under_exact_boost"] is True, "Ricci equivariance")
    require(checks["collision_distinct_projector_limits"] is True, "collision lost")
    require(checks["collision_paths_related_by_round_axis_rotation"] is True, "collision source tie")
    require(checks["round_spatial_line_orbit_dimension"] == 2, "set orbit dimension")
    require(checks["intrinsic_positive_candidate_count"] == 6, "intrinsic positive count")
    require(independent["result"] == "PASS", "independent result")
    require(independent["method"] == "stdlib_Fraction_no_production_import", "independence method")
    require(independent["full_commutant_rank"] == 15, "independent full rank")
    require(independent["round_commutant_rank"] == 14, "independent round rank")
    require(independent["null_little_group_commutant_rank"] == 14, "independent null rank")
    require(independent["null_little_group_idempotent_ranks"] == [0, 4], "independent null idempotents")
    require(independent["ricci_projector_rank"] == 2, "independent Ricci rank")
    require(independent["selector_rows"] == 18, "independent candidate count")


universe = table(HERE / "SELECTOR_UNIVERSE.tsv")
outcomes = table(HERE / "SELECTOR_OUTCOMES.tsv")
production = json.loads((HERE / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
independent = json.loads((HERE / "INDEPENDENT_RESULT.json").read_text(encoding="utf-8"))
review = json.loads((HERE / "COLD_REVIEW_RESULT.json").read_text(encoding="utf-8"))

# Source packet replay.
sources = table(HERE / "SOURCE_MANIFEST.tsv")
require(len(sources) == 28, "source count")
for row in sources:
    target = ROOT / row["path"]
    require(target.is_file(), f"missing source {row['path']}")
    require(str(target.stat().st_size) == row["bytes"], f"source bytes {row['path']}")
    require(digest(target) == row["sha256"], f"source hash {row['path']}")
manifest_expected = (HERE / "SOURCE_MANIFEST.sha256").read_text(encoding="utf-8").split()[0]
require(digest(HERE / "SOURCE_MANIFEST.tsv") == manifest_expected, "manifest hash")

validate(universe, outcomes, production, independent)
require(review["verdict"] == "PASS_WITH_REQUIRED_REPAIRS", "review verdict")
require(review["repair_replay"] == "REPAIRS_ACCEPTED", "repair replay not accepted")
require(review["maximum_conclusion_survives"] is True, "maximum conclusion rejected")
require("derive_selector_atlas" not in (HERE / "verify_selector_independent.py").read_text(), "shared production import")

report = (HERE / "EXACT_DERIVATION.md").read_text(encoding="utf-8")
lay = (HERE / "LAY_REPORT.md").read_text(encoding="utf-8")
next_step = (HERE / "NEXT_STEP.md").read_text(encoding="utf-8")
report_flat = " ".join(report.lower().split())
require("future native law could change the domain" in report.lower(), "universal scope caveat")
require("does not derive a natural realized field" in report_flat, "query section caveat")
require("a = 2 i + 2 ric#_q02".replace(" ", "") in report_flat.replace(" ", ""), "Q02 linkage missing")
require("No option has been selected" in lay, "lay selection overclaim")
require("section-necessity and descent audit" in next_step, "next object drift")


def rejected(mutator) -> bool:
    u = copy.deepcopy(universe)
    o = copy.deepcopy(outcomes)
    p = copy.deepcopy(production)
    i = copy.deepcopy(independent)
    mutator(u, o, p, i)
    try:
        validate(u, o, p, i)
    except (AssertionError, KeyError):
        return True
    return False


def review_rejected(mutator) -> bool:
    candidate = copy.deepcopy(review)
    mutator(candidate)
    try:
        require(candidate["verdict"] == "PASS_WITH_REQUIRED_REPAIRS", "review verdict")
        require(candidate["repair_replay"] == "REPAIRS_ACCEPTED", "repair replay")
        require(candidate["maximum_conclusion_survives"] is True, "maximum conclusion")
    except (AssertionError, KeyError):
        return True
    return False


catches = [
    ("C01", "missing_selector", rejected(lambda u, o, p, i: o.pop(0))),
    ("C02", "duplicate_selector", rejected(lambda u, o, p, i: o.__setitem__(1, copy.deepcopy(o[0])))),
    ("C03", "discard_round_control", rejected(lambda u, o, p, i: o[11].__setitem__("ruling", "BRANCH_LOCAL_POSITIVE_NOT_PHYSICAL"))),
    ("C04", "promote_coframe_presentation", rejected(lambda u, o, p, i: o[1].__setitem__("ruling", "UNIVERSAL_METRIC_SELECTOR"))),
    ("C05", "query_bundle_becomes_section", rejected(lambda u, o, p, i: o[2].__setitem__("ruling", "DERIVED_SPACETIME_SECTION"))),
    ("C06", "promote_phi_first_jet", rejected(lambda u, o, p, i: o[3].__setitem__("ruling", "UNIVERSAL_RANK2_SPLIT"))),
    ("C07", "erase_Ricci_collision", rejected(lambda u, o, p, i: o[5].__setitem__("ruling", "UNIVERSAL_SMOOTH_POSITIVE"))),
    ("C08", "erase_intrinsic_defect", rejected(lambda u, o, p, i: o[10].__setitem__("ruling", "GLOBAL_SMOOTH_POSITIVE"))),
    ("C09", "promote_squashed_branch_physics", rejected(lambda u, o, p, i: o[12].__setitem__("ruling", "PHYSICAL_SPLIT_SELECTED"))),
    ("C10", "universalize_partial_nogo", rejected(lambda u, o, p, i: o[13].__setitem__("ruling", "IMPOSSIBLE_UNIVERSALLY"))),
    ("C11", "set_valued_equals_member", rejected(lambda u, o, p, i: o[15].__setitem__("ruling", "REALIZED_UNIQUE_SPLIT"))),
    ("C12", "erase_rank_change", rejected(lambda u, o, p, i: o[16].__setitem__("ruling", "GLOBAL_SMOOTH_FIXED_RANK"))),
    ("C13", "import_action_selector", rejected(lambda u, o, p, i: o[17].__setitem__("ruling", "ACTIVE_METRIC_SELECTOR"))),
    ("C14", "alter_full_commutant_rank", rejected(lambda u, o, p, i: p["checks"].__setitem__("full_commutant_rank", 14))),
    ("C15", "alter_round_projector_ranks", rejected(lambda u, o, p, i: p["checks"].__setitem__("round_invariant_projector_ranks", [0, 1, 2, 3, 4]))),
    ("C16", "lose_Ricci_equivariance", rejected(lambda u, o, p, i: p["checks"].__setitem__("ricci_projector_equivariant_under_exact_boost", False))),
    ("C17", "lose_independent_method", rejected(lambda u, o, p, i: i.__setitem__("method", "production_import"))),
    ("C18", "drop_universe_control", rejected(lambda u, o, p, i: u.pop(11))),
    ("C19", "erase_phi_second_jet_strata", rejected(lambda u, o, p, i: o[4].__setitem__("obstruction_domain", "EIGEN_COLLISION_ONLY"))),
    ("C20", "invent_bivector_witness", rejected(lambda u, o, p, i: o[6].__setitem__("ruling", "DERIVED_COMPLETE_WITNESS"))),
    ("C21", "invent_gradient_witness", rejected(lambda u, o, p, i: o[7].__setitem__("ruling", "DERIVED_COMPLETE_WITNESS"))),
    ("C22", "promote_Killing_generator", rejected(lambda u, o, p, i: o[8].__setitem__("ruling", "UNIVERSAL_SELECTOR"))),
    ("C23", "promote_holonomy_parallelism", rejected(lambda u, o, p, i: o[9].__setitem__("ruling", "UNIVERSAL_PARALLEL_SPLIT"))),
    ("C24", "promote_boundary_selector", rejected(lambda u, o, p, i: o[14].__setitem__("ruling", "DERIVED_GLOBAL_SECTION"))),
    ("C25", "incomplete_repair_replay", review_rejected(lambda r: r.__setitem__("repair_replay", "REPAIRS_INCOMPLETE"))),
]
require(all(item[2] for item in catches), "catch proof failure")
with (HERE / "CATCH_PROOFS.tsv").open("w", newline="", encoding="utf-8") as handle:
    writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
    writer.writerow(["catch_id", "mutation", "result"])
    writer.writerows([[item[0], item[1], "PASS_REJECTED"] for item in catches])

result = {
    "schema": "udt-metric-natural-reciprocal-split-selector-verification-1.0",
    "result": "PASS_REVIEW_ACCEPTED",
    "source_count": len(sources),
    "source_manifest_sha256": manifest_expected,
    "selector_count": len(outcomes),
    "catch_count": len(catches),
    "production_result": production["result"],
    "independent_result": independent["result"],
    "fresh_adversarial_review": "PASS_WITH_REQUIRED_REPAIRS__REPAIRS_ACCEPTED",
}
(HERE / "VERIFICATION_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
print(json.dumps(result, sort_keys=True))
