#!/usr/bin/env python3
"""Independent standard-library verifier for the conceptual object-type audit."""

from __future__ import annotations

import copy
import csv
import hashlib
import json
import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
BASE = "c6ca30cba1bbe8e68a37a1ecbad9cddae8dae405"
ALLOWED_TYPES = {
    "FOUNDING_POSTULATE",
    "DERIVED_RELATION",
    "REPRESENTATION_COORDINATE_OR_POTENTIAL",
    "OBSERVATIONAL_ANCHOR",
    "DEFINED_CONFIGURATION_ARCHITECTURE",
    "SELECTED_SOLUTION_PROPERTY",
    "GLOBAL_OUTPUT_OR_LIMIT",
    "WORKING_POSIT",
    "CONDITIONAL_MODEL_INGREDIENT",
    "OPEN_PHYSICAL_LAW_OR_OBJECT",
    "HISTORICAL_AID_INACTIVE",
}
AUTHORIZED_OUTPUT_INPUTS = {"S02", "S03"}


def rows(name: str) -> list[dict[str, str]]:
    with (HERE / name).open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def root_rows(name: str) -> list[dict[str, str]]:
    with (ROOT / name).open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def indexed(items: list[dict[str, str]], key: str) -> dict[str, dict[str, str]]:
    out = {item[key]: item for item in items}
    require(len(out) == len(items), f"duplicate {key}")
    return out


def semantic_check(
    objects: list[dict[str, str]],
    chain: list[dict[str, str]],
    impacts: list[dict[str, str]],
    premise: list[dict[str, str]],
) -> None:
    obj = indexed(objects, "object_id")
    csn = indexed(chain, "step_id")
    dep = indexed(impacts, "family_id")
    reg = indexed(premise, "premise_id")

    require(len(obj) == 30, "object universe must contain 30 rows")
    require(all(row["primary_type"] in ALLOWED_TYPES for row in obj.values()), "unknown primary type")
    require(obj["O02"]["primary_type"] == "OBSERVATIONAL_ANCHOR", "c_E anchor lost")
    require("foundational_metric" in obj["O02"]["active_role"], "c_E removed from founding metric")
    require("absolute_length" in obj["O02"]["forbidden_merge"], "c_E absolute-length guard lost")
    require(obj["O05"]["primary_type"] == "REPRESENTATION_COORDINATE_OR_POTENTIAL", "phi mistyped")
    require("independent_native_scalar" in obj["O05"]["forbidden_merge"], "phi field guard lost")
    require(obj["O09"]["primary_type"] == "HISTORICAL_AID_INACTIVE", "strong CSN reactivated")
    require(obj["O09"]["epistemic_status"] == "CHALLENGED_OWNER_POSTULATE_NOT_DERIVED", "CSN status")
    require(obj["O10"]["primary_type"] == "GLOBAL_OUTPUT_OR_LIMIT", "Xmax limit role lost")
    require("variational_boundary" in obj["O10"]["forbidden_merge"], "Xmax boundary guard lost")
    require(obj["O11"]["epistemic_status"] == "DEFINED_CONFIGURATION_ARCHITECTURE", "coframe promoted")
    require(obj["O15"]["epistemic_status"] == "POSIT", "S2 carrier promoted")
    require(obj["O19"]["primary_type"] == "WORKING_POSIT", "bootstrap mistyped")
    require("density_optimizer" in obj["O19"]["forbidden_merge"], "bootstrap optimizer guard lost")
    require(obj["O20"]["epistemic_status"] == "OPEN", "action promoted")
    require(obj["O21"]["epistemic_status"] == "OPEN_NATIVE_VARIATION_DOMAIN", "variation ownership promoted")
    require("standalone_field" in obj["O21"]["forbidden_merge"], "variation ownership guard lost")
    require(obj["O22"]["epistemic_status"] == "OPEN", "source promoted")
    require("preexisting_substance" in obj["O22"]["forbidden_merge"], "source/substance guard lost")
    require(obj["O23"]["epistemic_status"] == "OPEN", "mass promoted")
    require("mass_like" in obj["O23"]["forbidden_merge"], "mass readout guard lost")
    require(obj["O26"]["active_role"] == "co_membership_of_events_in_one_complete_solution_domain", "copresence role")
    require("instantaneous_signal" in obj["O26"]["forbidden_merge"], "copresence signal guard lost")

    require(len(csn) == 11, "CSN provenance chain must contain 11 rows")
    require(csn["C01"]["record_status"] == "OPEN_CANDIDATE_NOT_USER_ADOPTED", "CSN began adopted")
    require("C2_Bach" in csn["C02"]["what_record_establishes"], "motivating validation omitted")
    require(csn["C07"]["record_status"] == "CHALLENGED_OWNER_POSTULATE_NOT_DERIVED", "CSN correction lost")
    require(csn["C10"]["current_ruling"] == "motive_testimony_supported_but_not_textually_proven", "motive overstated")
    require(csn["C11"]["current_ruling"] == "retired_as_active_selector_not_deleted_or_mathematically_refuted", "validation lifecycle")

    require(len(dep) == 16, "dependency universe must contain 16 rows")
    require(dep["D01"]["physical_authority"] == "INACTIVE_WITHOUT_EXPLICIT_STRONG_CSN", "C2 reactivated")
    require(dep["D02"]["physical_authority"] == "CONDITIONAL_NOT_SELECTED", "EH promoted")
    require(dep["D05"]["immediate_rederivation"] == "ZERO_CURRENT_LOAD_BEARING_ROWS", "phi rerun inflated")
    require(all(row["immediate_rederivation"] in {"NONE", "ZERO_CURRENT_LOAD_BEARING_ROWS"} for row in dep.values()), "unregistered rerun")

    require(len(reg) == 27, "current registry must contain 27 rows")
    require(reg["G04"]["active_use"] == "INACTIVE_UNLESS_CHARLES_EXPLICITLY_REAUTHORIZES", "registry CSN active")
    require(reg["G06"]["active_use"] == "ACTIVE_CALIBRATION", "registry c/G anchors inactive")
    require(reg["G19"]["active_use"] == "CONFIGURATION_ARENA_ONLY", "registry coframe promoted")
    require(reg["G20"]["active_use"] == "NO_UNIVERSAL_VARIATION_DOMAIN_SELECTED", "registry variation promoted")
    require(reg["G21"]["current_status"] == "OPEN_RESPONSE_OR_CURRENT_ROLE_NOT_SUBSTANCE", "registry source type")
    require(reg["G22"]["active_use"] == "NO_UNCONDITIONAL_MASS_CLAIM", "registry mass promoted")
    require(reg["G23"]["active_use"] == "SEMANTIC_FRAME_ONLY", "registry copresence promoted")
    require(reg["G24"]["active_use"] == "GEOMETRIC_REACHABILITY_ONLY", "registry causality promoted")
    require(reg["G25"]["active_use"] == "TYPE_GUARD_ONLY", "registry boundary types merged")
    require(reg["G26"]["active_use"] == "NO_CARRIER_EMERGENCE_CLAIM", "registry carrier promoted")
    require(reg["G27"]["active_use"] == "NO_ORDER_SELECTED", "registry action order selected")


def mutation_catches(
    objects: list[dict[str, str]],
    chain: list[dict[str, str]],
    impacts: list[dict[str, str]],
    premise: list[dict[str, str]],
) -> list[str]:
    mutations = [
        ("strong_CSN_reactivated", "objects", "O09", "primary_type", "FOUNDING_POSTULATE"),
        ("c_anchor_dropped", "objects", "O02", "primary_type", "HISTORICAL_AID_INACTIVE"),
        ("c_promoted_to_absolute_length", "objects", "O02", "forbidden_merge", "none"),
        ("Xmax_boundary_guard_deleted", "objects", "O10", "forbidden_merge", "wall_only"),
        ("phi_field_guard_deleted", "objects", "O05", "forbidden_merge", "none"),
        ("coframe_promoted_on_shell", "objects", "O11", "epistemic_status", "SELECTED_ON_SHELL"),
        ("S2_carrier_promoted", "objects", "O15", "epistemic_status", "DERIVED"),
        ("bootstrap_optimizer_inserted", "objects", "O19", "forbidden_merge", "local_equation"),
        ("action_promoted", "objects", "O20", "epistemic_status", "DERIVED"),
        ("variation_promoted", "objects", "O21", "epistemic_status", "DERIVED"),
        ("source_promoted", "objects", "O22", "epistemic_status", "DERIVED"),
        ("mass_promoted", "objects", "O23", "epistemic_status", "DERIVED"),
        ("copresence_signal_guard_deleted", "objects", "O26", "forbidden_merge", "zero_time_only"),
        ("C2_reactivated", "impacts", "D01", "physical_authority", "ACTIVE_NATIVE_PRIORITY"),
        ("historical_validation_reactivated", "chain", "C11", "current_ruling", "active_selector"),
        ("action_order_selected", "premise", "G27", "active_use", "ACTION_FIRST"),
    ]
    caught = []
    for name, target, identity, field, value in mutations:
        o, c, d, p = map(copy.deepcopy, (objects, chain, impacts, premise))
        selected, key = {
            "objects": (o, "object_id"),
            "chain": (c, "step_id"),
            "impacts": (d, "family_id"),
            "premise": (p, "premise_id"),
        }[target]
        indexed(selected, key)[identity][field] = value
        try:
            semantic_check(o, c, d, p)
        except AssertionError:
            caught.append(name)
        else:
            raise AssertionError(f"mutation escaped: {name}")
    return caught


def main() -> None:
    source = rows("SOURCE_INVENTORY.tsv")
    objects = rows("OBJECT_TYPE_LEDGER.tsv")
    chain = rows("CSN_PROVENANCE_CHAIN.tsv")
    impacts = rows("DEPENDENCY_IMPACT.tsv")
    census = rows("CSN_RAW_CENSUS.tsv")
    mutations = rows("AUTHORIZED_MUTATIONS.tsv")
    premise = root_rows("CURRENT_SCIENTIFIC_PREMISES.tsv")

    require(len(source) == 28, "source inventory must contain 28 rows")
    indexed(source, "source_id")
    require(len({row["path"] for row in source}) == 28, "duplicate source path")
    for row in source:
        path = ROOT / row["path"]
        require(path.is_file(), f"missing source: {row['path']}")
        if row["source_id"] not in AUTHORIZED_OUTPUT_INPUTS:
            require(digest(path) == row["sha256"], f"source SHA drift: {row['path']}")
            blob = subprocess.check_output(["git", "hash-object", row["path"]], cwd=ROOT, text=True).strip()
            require(blob == row["git_blob"], f"source blob drift: {row['path']}")

    require(len(mutations) == 3, "authorized mutation ledger must contain three rows")
    indexed(mutations, "path")
    for row in mutations:
        path = ROOT / row["path"]
        require(path.is_file(), f"missing authorized output: {row['path']}")
        require(digest(path) == row["after_sha256"], f"authorized output SHA drift: {row['path']}")
        blob = subprocess.check_output(["git", "hash-object", row["path"]], cwd=ROOT, text=True).strip()
        require(blob == row["after_blob"], f"authorized output blob drift: {row['path']}")
        before = subprocess.check_output(["git", "show", f"{BASE}:{row['path']}"], cwd=ROOT)
        require(hashlib.sha256(before).hexdigest() == row["before_sha256"], f"authorized input SHA drift: {row['path']}")
        before_blob = subprocess.check_output(["git", "rev-parse", f"{BASE}:{row['path']}"], cwd=ROOT, text=True).strip()
        require(before_blob == row["before_blob"], f"authorized input blob drift: {row['path']}")

    for row in objects:
        source_path = row["controlling_source"].split(":", 1)[0]
        require((ROOT / source_path).is_file(), f"missing object authority: {source_path}")

    semantic_check(objects, chain, impacts, premise)
    raw = indexed(census, "census_id")
    require((raw["R01"]["occurrences"], raw["R01"]["source_paths"]) == ("12194", "1207"), "raw CSN census")
    require((raw["R02"]["occurrences"], raw["R02"]["source_paths"]) == ("175", "149"), "stale-token census")
    require((raw["R03"]["occurrences"], raw["R03"]["source_paths"]) == ("103", "96"), "correction-token census")
    caught = mutation_catches(objects, chain, impacts, premise)

    founding = (ROOT / "UDT_RECIPROCAL_C_FOUNDING_POSTULATE_DERIVATION_RESULTS.md").read_text(encoding="utf-8")
    require("-e^{-2\\phi}c^2dt^2" in founding, "founding metric no longer contains dimensional c")
    csn_postulate = (ROOT / "UDT_COMMON_SCALE_NEUTRALITY_POSTULATE_2026-07-15.md").read_text(encoding="utf-8")
    require("Common-Scale Neutrality declares the first factor calibrational" in csn_postulate, "CSN declaration missing")
    map_text = (ROOT / "archive/native_action_chat_2026-07-14_15/UDT_RECIPROCAL_C_CONFORMAL_ACTION_MAP.md").read_text(encoding="utf-8")
    require("OPEN CANDIDATE / NOT YET USER-ADOPTED" in map_text, "CSN candidate provenance missing")

    result = {
        "schema": "udt.conceptual_object_type_dependency_audit.v1",
        "status": "PASS",
        "source_rows": len(source),
        "object_rows": len(objects),
        "primary_types": len({row["primary_type"] for row in objects}),
        "csn_chain_rows": len(chain),
        "dependency_rows": len(impacts),
        "authorized_mutation_rows": len(mutations),
        "current_premise_rows": len(premise),
        "mutation_catches": len(caught),
        "caught_mutations": caught,
        "external_semantic_review": "NOT_RUN_NOT_AUTHORIZED_FOR_THIS_PAYLOAD",
        "grade_ceiling": "VERIFIED_WITH_CAVEATS",
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
