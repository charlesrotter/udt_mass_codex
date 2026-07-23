#!/usr/bin/env python3
"""Fail-closed package verifier for the temporal-soldering atlas."""

from __future__ import annotations

import copy
import csv
import gzip
import hashlib
import json
import subprocess
from collections import Counter
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
BASE = "d7a2469ae3a76a099e78656c9357710bf8645843"


def digest(path):
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(131072), b""): h.update(block)
    return h.hexdigest()


def rows(path):
    opener = gzip.open if path.suffix == ".gz" else open
    with opener(path, "rt", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def require(condition, message):
    if not condition: raise AssertionError(message)


def validate_mutation_state(state):
    """Fail closed on the registered package-level evidence invariants."""
    require(state["path_count"] == 95_232, "path count")
    require(state["path_unique"] == 95_232, "path uniqueness")
    require(state["path_census"] == {
        "LORENTZ_TWO_PLANE_ONLY": 7_845,
        "NO_PROPER_INTRINSIC_TEMPORAL_SUBSPACE": 82_140,
        "RANK_ONE_LINE_SPACELIKE__LORENTZ_COMPLEMENT": 2_160,
        "TRANSITION_OR_NUMERICALLY_UNCERTAIN": 1_312,
        "UNIQUE_LOCAL_UNORIENTED_TIMELIKE_LINE": 1_775,
    }, "path census")
    require(state["complement_count"] == 30_175, "complement count")
    require(state["complement_unique"] == 30_175, "complement uniqueness")
    require(state["refinement_count"] == 2, "refinement count")
    require(state["line_count"] == 1_775, "line count")
    require(state["line_census"] == {
        "FOUR_LINES|NONINTEGRABILITY_OBSERVED_AT_ONE_OR_MORE_NODES": 1_055,
        "LINE_PLUS_THREE|ALL_17_NODES_CONSOLIDATED_INTEGRABLE": 720,
    }, "line census")
    require(state["timelike_nodes"] == 12_240, "timelike node count")
    require(state["timelike_contains_D"] is True, "timelike D family")
    require(state["timelike_future"] is False, "timelike future")
    require(state["timelike_global_time"] is False, "timelike global time")
    require(state["spacelike_nodes"] == 36_720, "spacelike node count")
    require(state["spacelike_contains_D"] is True, "spacelike D family")
    require(state["spacelike_physical"] is False, "spacelike branch")
    require(state["spacelike_intraleaf_time"] is False, "spacelike intraleaf time")
    require(state["full_connectors"] == 0, "full connector")
    require(state["actions_loaded"] == 0, "action")
    require(state["carriers_loaded"] == 0, "carrier")
    require(state["sne_fits"] == 0, "SNe fit")
    require(state["source_integrity"] is True, "source integrity")
    require(state["production_builder_imported"] is False, "independence")


def exercised_mutation_catches(paths, path_census, consolidated, refined, lines, timelike, spacelike, production_result, source, independent):
    state = {
        "path_count": len(paths),
        "path_unique": len({(r["identity_id"], r["family_id"]) for r in paths}),
        "path_census": dict(sorted(path_census.items())),
        "complement_count": len(consolidated),
        "complement_unique": len({(r["identity_id"], r["family_id"], r["path_node"]) for r in consolidated}),
        "refinement_count": len(refined),
        "line_count": len(lines),
        "line_census": dict(sorted(("|".join(key), value) for key, value in Counter((r["motif"], r["consolidated_path_status"]) for r in lines).items())),
        "timelike_nodes": timelike["node_presentations"],
        "timelike_contains_D": timelike["all_families_contain_D"],
        "timelike_future": timelike["physical_future_selected"],
        "timelike_global_time": timelike["global_time_function_derived"],
        "spacelike_nodes": spacelike["node_presentations"],
        "spacelike_contains_D": spacelike["all_families_contain_D"],
        "spacelike_physical": spacelike["physical_branch_selected"],
        "spacelike_intraleaf_time": spacelike["timelike_line_within_leaf_derived"],
        "full_connectors": production_result["full_optical_connectors_derived"],
        "actions_loaded": production_result["actions_loaded"],
        "carriers_loaded": production_result["carriers_loaded"],
        "sne_fits": production_result["sne_fits"],
        "source_integrity": all(digest(ROOT / r["path"]) == r["sha256"] for r in source),
        "production_builder_imported": independent["production_builder_imported"],
    }
    validate_mutation_state(state)
    mutations = [
        ("P01_MISSING_PATH", "path_count -= 1", lambda s: s.__setitem__("path_count", s["path_count"] - 1)),
        ("P02_DUPLICATE_PATH", "path_unique -= 1", lambda s: s.__setitem__("path_unique", s["path_unique"] - 1)),
        ("P03_PROMOTE_TWO_PLANE", "two-plane -1; timelike-line +1", lambda s: (s["path_census"].__setitem__("LORENTZ_TWO_PLANE_ONLY", s["path_census"]["LORENTZ_TWO_PLANE_ONLY"] - 1), s["path_census"].__setitem__("UNIQUE_LOCAL_UNORIENTED_TIMELIKE_LINE", s["path_census"]["UNIQUE_LOCAL_UNORIENTED_TIMELIKE_LINE"] + 1))),
        ("P04_MISSING_COMPLEMENT_NODE", "complement_count -= 1", lambda s: s.__setitem__("complement_count", s["complement_count"] - 1)),
        ("P05_DUPLICATE_COMPLEMENT_KEY", "complement_unique -= 1", lambda s: s.__setitem__("complement_unique", s["complement_unique"] - 1)),
        ("P06_WRONG_REFINEMENT_COUNT", "refinement_count = 3", lambda s: s.__setitem__("refinement_count", 3)),
        ("P07_MISSING_LINE_PATH", "line_count -= 1", lambda s: s.__setitem__("line_count", s["line_count"] - 1)),
        ("P08_ERASE_FOUR_LINE_TWIST", "four-line status count = 0", lambda s: s["line_census"].__setitem__("FOUR_LINES|NONINTEGRABILITY_OBSERVED_AT_ONE_OR_MORE_NODES", 0)),
        ("P09_IMPORT_CARRIER", "carriers_loaded = 1", lambda s: s.__setitem__("carriers_loaded", 1)),
        ("P10_DROP_D_FROM_TIMELIKE_FAMILY", "timelike_contains_D = false", lambda s: s.__setitem__("timelike_contains_D", False)),
        ("P11_SELECT_TIMELIKE_FUTURE", "timelike_future = true", lambda s: s.__setitem__("timelike_future", True)),
        ("P12_FALSE_GLOBAL_TIME", "timelike_global_time = true", lambda s: s.__setitem__("timelike_global_time", True)),
        ("P13_FALSE_SNE_FIT", "sne_fits = 1", lambda s: s.__setitem__("sne_fits", 1)),
        ("P14_DROP_D_FROM_SPACELIKE_FAMILY", "spacelike_contains_D = false", lambda s: s.__setitem__("spacelike_contains_D", False)),
        ("P15_SELECT_SPACELIKE_BRANCH", "spacelike_physical = true", lambda s: s.__setitem__("spacelike_physical", True)),
        ("P16_FALSE_INTRALEAF_TIME", "spacelike_intraleaf_time = true", lambda s: s.__setitem__("spacelike_intraleaf_time", True)),
        ("P17_FALSE_FULL_CONNECTOR", "full_connectors = 1", lambda s: s.__setitem__("full_connectors", 1)),
        ("P18_IMPORT_ACTION", "actions_loaded = 1", lambda s: s.__setitem__("actions_loaded", 1)),
        ("P19_SOURCE_MUTATION", "source_integrity = false", lambda s: s.__setitem__("source_integrity", False)),
        ("P20_INDEPENDENCE_FALSE", "production_builder_imported = true", lambda s: s.__setitem__("production_builder_imported", True)),
    ]
    catches = []
    for identity, mutation, mutate in mutations:
        corrupted = copy.deepcopy(state)
        mutate(corrupted)
        try:
            validate_mutation_state(corrupted)
        except AssertionError as exc:
            catches.append({"catch_id": identity, "mutation": mutation, "validator": "validate_mutation_state", "rejection": str(exc), "result": "MUTATION_REJECTED_AS_REQUIRED"})
        else:
            raise AssertionError(f"corruption mutation accepted {identity}")
    return catches


def main():
    source = rows(HERE / "FROZEN_SOURCE_LEDGER.tsv"); require(len(source) == 44, "source count")
    for row in source:
        path = ROOT / row["path"]; require(path.exists(), f"source exists {path}")
        require(digest(path) == row["sha256"], f"source sha {path}")
        blob = subprocess.check_output(["git", "rev-parse", f"{BASE}:{row['path']}"], cwd=ROOT, text=True).strip()
        require(blob == row["base_blob"], f"source blob {path}")

    paths = rows(HERE / "PATH_TEMPORAL_CLASSIFICATION.tsv.gz")
    require(len(paths) == 95_232 and len({(r["identity_id"], r["family_id"]) for r in paths}) == 95_232, "path coverage")
    path_census = Counter(r["local_temporal_class"] for r in paths)
    require(path_census == Counter({
        "NO_PROPER_INTRINSIC_TEMPORAL_SUBSPACE": 82_140,
        "LORENTZ_TWO_PLANE_ONLY": 7_845,
        "RANK_ONE_LINE_SPACELIKE__LORENTZ_COMPLEMENT": 2_160,
        "UNIQUE_LOCAL_UNORIENTED_TIMELIKE_LINE": 1_775,
        "TRANSITION_OR_NUMERICALLY_UNCERTAIN": 1_312,
    }), "path class census")

    production = rows(HERE / "ORTHOGONAL_COMPLEMENT_ATLAS.tsv.gz")
    require(len(production) == 30_175, "production node count")
    consolidated = rows(HERE / "CROSS_IMPLEMENTATION_COMPLEMENT_CLASSIFICATION.tsv.gz")
    require(len(consolidated) == 30_175 and len({(r["identity_id"], r["family_id"], r["path_node"]) for r in consolidated}) == 30_175, "consolidated node coverage")
    refined = [r for r in consolidated if r["adjudication_source"] == "CROSS_IMPLEMENTATION_THRESHOLD_REFINEMENT"]
    require(len(refined) == 2 and all(r["consolidated_class"] == "NUMERICALLY_INTEGRABLE_LOCAL__REFINED_TWO_ROUTE" for r in refined), "refinement rows")
    require(Counter(r["consolidated_class"] for r in consolidated) == Counter({
        "NUMERICALLY_INTEGRABLE_LOCAL": 12_238,
        "NUMERICALLY_INTEGRABLE_LOCAL__REFINED_TWO_ROUTE": 2,
        "NUMERICALLY_NONINTEGRABLE_LOCAL": 17_925,
        "NUMERIC_UNCERTAIN_DERIVATIVE": 10,
    }), "consolidated node census")

    lines = rows(HERE / "CROSS_IMPLEMENTATION_LINE_COMPLETION.tsv")
    require(len(lines) == 1_775, "line count")
    require(Counter((r["motif"], r["consolidated_path_status"]) for r in lines) == Counter({
        ("LINE_PLUS_THREE", "ALL_17_NODES_CONSOLIDATED_INTEGRABLE"): 720,
        ("FOUR_LINES", "NONINTEGRABILITY_OBSERVED_AT_ONE_OR_MORE_NODES"): 1_055,
    }), "line status census")

    independent = json.loads((HERE / "INDEPENDENT_VERIFICATION_RESULT.json").read_text())
    require(independent["status"] == "PASS_WITH_REGISTERED_SCOPE", "independent status")
    require(independent["orthogonal_complement_nodes_independently_recomputed"] == 30_175, "independent node count")
    require(independent["initial_threshold_class_conflicts"] == 2, "conflict count")
    require(independent["catch_proofs_passed"] == 20, "independent catches")
    require(independent["production_builder_imported"] is False, "independent route")

    conflict = json.loads((HERE / "THRESHOLD_CONFLICT_REFINEMENT_RESULT.json").read_text())
    require(conflict["candidate_rows"] == 2 and conflict["retuning_outside_frozen_candidates"] == 0, "refinement scope")
    require(all(r["consolidated_class"] == "REFINED_INTEGRABLE" for r in conflict["cases"]), "refinement result")

    timelike = json.loads((HERE / "PHI_GRADIENT_SOLDERING_RESULT.json").read_text())
    require(timelike["path_presentations"] == 720 and timelike["node_presentations"] == 12_240, "timelike phi coverage")
    require(timelike["all_families_contain_D"] and timelike["all_nodes_s_negative"], "timelike phi gates")
    require(max(timelike["max_residuals"].values()) <= 1.0e-9, "timelike phi residual")
    require(not timelike["physical_future_selected"] and not timelike["global_time_function_derived"], "timelike phi overclaim")

    spacelike = json.loads((HERE / "PHI_GRADIENT_SPACELIKE_BRANCH_RESULT.json").read_text())
    require(spacelike["path_presentations"] == 2_160 and spacelike["node_presentations"] == 36_720, "spacelike phi coverage")
    require(spacelike["all_families_contain_D"] and spacelike["all_nodes_s_positive"], "spacelike phi gates")
    require(max(spacelike["max_residuals"].values()) <= 1.0e-9, "spacelike phi residual")
    require(not spacelike["physical_branch_selected"] and not spacelike["timelike_line_within_leaf_derived"], "spacelike phi overclaim")

    chart = rows(HERE / "CHART_COFRAME_TEMPORAL_INVARIANCE.tsv")
    require(len(chart) == 60 and sum(int(r["path_presentations"]) for r in chart) == 1_142_784, "chart census")
    require(all(r["status"] == "EXACT_CLASS_INVARIANCE_FOR_ALL_RETAINED_PRESENTATIONS" for r in chart), "chart statuses")
    require(independent["chart_coframe_numeric_anchor_comparisons"] == 48, "chart anchors")

    selectors = {r["selector"]: r for r in rows(HERE / "SELECTOR_STATUS.tsv")}
    require(selectors["RECIPROCITY"]["line_selection"] == "CONSTRAINS_NOT_SELECTS", "reciprocity status")
    require(selectors["COMMON_SCALE_NEUTRALITY"]["line_selection"] == "SILENT", "CSN status")
    require(selectors["BOOTSTRAP"]["line_selection"] == "OPEN", "bootstrap status")
    ladder = rows(HERE / "CONSOLIDATED_COMPLETION_LADDER.tsv")
    require(len(ladder) == 7 and all(r["global_status"] == "OPEN" for r in ladder[1:]), "completion ladder")

    status = rows(HERE / "STATUS_LEDGER.tsv"); premise = rows(HERE / "PREMISE_STATUS_LEDGER.tsv")
    require(len(status) == 17 and len(premise) == 20, "ledger coverage")
    report = (HERE / "AUDIT_REPORT.md").read_text()
    for phrase in (
        "does **not** supply one preferred clock direction everywhere",
        "Neither sign branch is selected as the physical universe",
        "zero global line bundles",
        "No action, carrier, source",
        "not canonization",
    ):
        require(phrase in report, f"report guard {phrase}")

    production_result = json.loads((HERE / "VERIFICATION_RESULT.json").read_text())
    require(production_result["gpu_runs"] == 0 and production_result["actions_loaded"] == 0 and production_result["carriers_loaded"] == 0 and production_result["sne_fits"] == 0, "scope guards")

    catches = exercised_mutation_catches(paths, path_census, consolidated, refined, lines, timelike, spacelike, production_result, source, independent)
    with (HERE / "PACKAGE_CATCH_PROOFS.tsv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=("catch_id", "mutation", "validator", "rejection", "result"), delimiter="\t", lineterminator="\n")
        writer.writeheader(); writer.writerows(catches)
    result = {
        "status": "PASS_WITH_REGISTERED_SCOPE",
        "frozen_source_files_verified": len(source),
        "path_presentations_verified": len(paths),
        "path_nodes_accounted": len(paths) * 17,
        "complement_nodes_verified": len(consolidated),
        "line_paths_verified": len(lines),
        "timelike_phi_nodes_verified": timelike["node_presentations"],
        "spacelike_phi_nodes_verified": spacelike["node_presentations"],
        "independent_catches": independent["catch_proofs_passed"],
        "package_catches": len(catches),
        "global_connectors_derived": 0,
        "maximum_conclusion": "CORRECTED_BOUNDED_TEMPORAL_SOLDERING_ATLAS_VERIFIED__GLOBAL_PHYSICAL_THREADING_OPEN",
    }
    (HERE / "PACKAGE_VERIFICATION_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__": main()
