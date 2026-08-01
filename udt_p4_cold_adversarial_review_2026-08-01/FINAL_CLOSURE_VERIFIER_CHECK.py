#!/usr/bin/env python3
"""Final independent source-anchor closure verifier.

The checker imports neither the review generator nor the production verifier.  It
reconstructs every emitted source excerpt from bytes, rechecks the earlier gates,
and writes only FINAL_CLOSURE_VERIFIER_RAW.jsonl and RESULTS.json in this package.
"""

from __future__ import annotations

import csv
import hashlib
import json
import re
import subprocess
from collections import Counter, defaultdict
from pathlib import Path


OUT = Path(__file__).resolve().parent
ROOT = OUT.parent
BASE = "2e93a621aeeee0a0844543068363d0ba94094357"
RAW_PATH = OUT / "FINAL_CLOSURE_VERIFIER_RAW.jsonl"
RESULT_PATH = OUT / "FINAL_CLOSURE_VERIFIER_RESULTS.json"

COMPLETENESS = (
    "fields_covered_or_dropped",
    "action_terms_covered_or_dropped",
    "equations_covered_or_dropped",
    "domain_covered_or_dropped",
    "boundary_covered_or_dropped",
    "topology_covered_or_dropped",
    "dynamical_character_covered_or_dropped",
    "branches_covered_or_dropped",
    "stability_covered_or_dropped",
    "regime_and_limits",
)
ACTION_EXPECTED = {
    "P4-07": "reduced conditional action/ODE and integrated response pairing are explicitly used",
    "P4-08": "cell-energy first integral and conditional action-derived mass definitions are explicitly used",
    "P4-16": "seam functional B and its N=2 first variation are explicitly active",
    "P4-18": "reduced second variation/Hessian and wall-germ Hessian sectors are explicitly tested",
    "P4-20": "IF-ADOPTED theta coupling classes and coupling terms are explicitly tested",
}
ACTION_COUNTS = {"P4-07": 4, "P4-08": 5, "P4-16": 5, "P4-18": 5, "P4-20": 7}
PARSER_IDS = {"IR03", "IR06", "IR10", "IR15", "IR19", "IR20"}
CAP_PATH = "udt_higher_isometry_plane_ownership_audit_2026-07-28/TORIC_CAP_ENUMERATION.tsv"
CAP_HASH = "ceecb5837ff8652c83c0ba72c67645182b1fd30f6e437026bd735c4d813bdfdf"
JOINT_PATH = "udt_joint_selector_provenance_audit_2026-07-28/JOINT_OPERATION_OBLIGATIONS.tsv"
JOINT_HASH = "52bc430e16227cc60d73e312a916666e0d206c54dc90a0d7ca8914d6c01336e9"
REVIEW_OVERLAY = OUT.name + "/TRANSITIVE_DEPENDENCY_OVERLAY.tsv"

IMMUTABLE = {
    "SECOND_VERIFIER_CHECK.py": "170bd495f1f908ee9a155906d6822ed29fe827850f68aea5eae5fa5ceeffd2c0",
    "SECOND_VERIFIER_RAW.jsonl": "2027bc7d01b6494714e4f8a4755c8ce067cfd77e221d93655715f6e12275affb",
    "SECOND_VERIFIER_RESULTS.json": "0cfcd7c621e120cde2b89d75a5d47f514bdd5a43549ef4053daad9e84001e4d7",
    "SECOND_VERIFIER_PREMISE_RAW.txt": "67548c2f45b0ac85fedbd95705493469aab88780e747382953fa0dc515a346b2",
    "SECOND_VERIFIER_MANIFEST.sha256": "c8ecc256f8ef41707e22856e168334ceb32a0ee2ea06e2f7b71b703ebae8ea0a",
    "CLOSURE_VERIFIER_CHECK.py": "9e1341b9250cd2ab2b63e86ac1df18a31752d906fffd476f64db71ed2c58e8c0",
    "CLOSURE_VERIFIER_RAW.jsonl": "2a455041f1420faab5c735a14012923466195dc835875d00379ef1190fb6564c",
    "CLOSURE_VERIFIER_RESULTS.json": "dc4b299eb5db41bf3f93005dd13815a959e42d936741905d8ceb594edc48cba8",
    "CLOSURE_VERIFIER_MANIFEST.sha256": "f4b47972102ddeff04dcb4e83ad415326c57673111a2dac95b56b84333f471cf",
}
SECOND_SECTION_HASH = "899fc7793bfe661fd8f0f8c1e30696e4af110116d6af23d655b79d914cd38bae"
CLOSURE_SECTION_HASH = "db4b97c8a7e4f05aa446b996367405021ab1e60de82b2dc9b2c68636f344d330"

raw: list[dict[str, object]] = []
failures: list[str] = []


def sha_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha(path: Path) -> str:
    return sha_bytes(path.read_bytes())


def tsv(name: str) -> list[dict[str, str]]:
    with (OUT / name).open(newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def run(*args: str, cwd: Path = OUT) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, cwd=cwd, text=True, capture_output=True, check=False)


def record(name: str, ok: bool, **detail: object) -> None:
    raw.append({"check": name, "status": "PASS" if ok else "FAIL", **detail})
    if not ok:
        failures.append(name)


def validate_manifest(name: str) -> tuple[int, list[str]]:
    bad: list[str] = []
    count = 0
    for line in (OUT / name).read_text().splitlines():
        if not line.strip():
            continue
        count += 1
        expected, rel = line.split("  ", 1)
        path = (OUT / rel).resolve()
        if not path.is_file() or sha(path) != expected:
            bad.append(rel)
    return count, bad


def report_section(start_marker: str, end_marker: str) -> str:
    report = (OUT / "AUDIT_REPORT.md").read_text()
    return start_marker + report.split(start_marker, 1)[1].split(end_marker, 1)[0]


def main() -> None:
    frozen = tsv("FROZEN_REVIEW_UNITS.tsv")
    inventory = tsv("SOURCE_INVENTORY.tsv")
    claims = tsv("MECHANICAL_CLAIM_REGRADES.tsv")
    independence = tsv("INDEPENDENT_RECOMPUTATION_LEDGER.tsv")
    premise = tsv("PREMISE_QUANTIFIER_AUDIT.tsv")
    overlay = tsv("TRANSITIVE_DEPENDENCY_OVERLAY.tsv")
    review_results = json.loads((OUT / "REVIEW_RESULTS.json").read_text())
    inventory_map = {row["path"]: row for row in inventory}
    overlay_map = {row["path"]: row for row in overlay}

    frozen_kinds = Counter(row["unit_kind"] for row in frozen)
    record(
        "frozen_units_37_29_plus_8",
        len(frozen) == len({row["unit_id"] for row in frozen}) == 37
        and frozen_kinds == Counter({"PACKAGE_HEADLINE_BUNDLE": 29, "CROSS_CUTTING_QUESTION": 8}),
        rows=len(frozen),
        kinds=dict(frozen_kinds),
    )

    source_manifest_count, source_manifest_bad = validate_manifest("SOURCE_MANIFEST.sha256")
    inventory_bad: list[str] = []
    for row in inventory:
        path = ROOT / row["path"]
        if not path.is_file() or sha(path) != row["sha256"] or path.stat().st_size != int(row["size_bytes"]):
            inventory_bad.append(row["path"])
    record(
        "frozen_source_hashes_311",
        len(inventory) == len(inventory_map) == source_manifest_count == 311
        and not inventory_bad
        and not source_manifest_bad,
        inventory_rows=len(inventory),
        manifest_rows=source_manifest_count,
        inventory_bad=inventory_bad,
        manifest_bad=source_manifest_bad,
        manifest_sha256=sha(OUT / "SOURCE_MANIFEST.sha256"),
    )

    kinds = Counter(row["unit_kind"] for row in claims)
    regrades = Counter(row["regrade"] for row in claims)
    record(
        "claim_census_182_and_regrades",
        len(claims) == len({row["claim_id"] for row in claims}) == 182
        and kinds
        == Counter(
            {
                "PACKAGE_HEADLINE_CLAUSE": 172,
                "CROSS_CUTTING_QUESTION": 8,
                "DISCOVERED_LOAD_BEARING_CLAIM": 2,
            }
        )
        and regrades
        == Counter({"RETAINED": 32, "NARROWED": 148, "CONTRADICTED": 1, "OPEN": 1}),
        rows=len(claims),
        kinds=dict(kinds),
        regrades=dict(regrades),
    )

    # Reconstruct every exact line range and anchor from source bytes.
    anchor_bad: list[object] = []
    group_rows: dict[str, list[dict[str, str]]] = defaultdict(list)
    group_shape: dict[str, tuple[object, ...]] = {}
    shape_group: dict[tuple[object, ...], str] = {}
    provenance = Counter()
    excerpt_hashes: dict[str, str] = {}
    for row in claims:
        cid = row["claim_id"]
        provenance[row["source_provenance_class"]] += 1
        try:
            path = ROOT / row["source_path"]
            start = int(row["source_start_line"])
            end = int(row["source_end_line"])
            lines = path.read_bytes().splitlines(keepends=True)
            if start < 1 or end < start or end > len(lines):
                raise ValueError(f"range {start}-{end} outside 1-{len(lines)}")
            excerpt = b"".join(lines[start - 1 : end])
        except Exception as exc:
            anchor_bad.append((cid, "resolution", repr(exc)))
            continue
        actual_hash = sha_bytes(excerpt)
        excerpt_hashes[cid] = actual_hash
        token = row["source_anchor_token"]
        group = row["shared_source_premise_id"]
        expected_stamp = f"{group}:{actual_hash[:12]}"
        if (
            not token.strip()
            or token.encode("utf-8") not in excerpt
            or actual_hash != row["source_excerpt_sha256"]
            or row["source_stamp_id"] != expected_stamp
            or any(mark in token.upper() for mark in ("DEFAULT", "TBD", "FALLBACK", "PACKAGE_TRIGGER"))
        ):
            anchor_bad.append((cid, "token_hash_or_stamp"))
        provenance_class = row["source_provenance_class"]
        admitted = (
            provenance_class == "PREREGISTERED_SOURCE_INVENTORY" and row["source_path"] in inventory_map
        ) or (
            provenance_class == "NON_RETROACTIVE_REVIEW_OVERLAY" and row["source_path"] == REVIEW_OVERLAY
        )
        if not admitted:
            anchor_bad.append((cid, "admission", provenance_class, row["source_path"]))
        if provenance_class == "PREREGISTERED_SOURCE_INVENTORY":
            inv = inventory_map[row["source_path"]]
            source = ROOT / row["source_path"]
            if sha(source) != inv["sha256"]:
                anchor_bad.append((cid, "inventory_source_hash"))
        shape = (
            row["source_path"],
            start,
            end,
            token,
            actual_hash,
            provenance_class,
            row["source_stamp_id"],
        )
        if group in group_shape and group_shape[group] != shape:
            anchor_bad.append((cid, "one_group_multiple_shapes"))
        if shape in shape_group and shape_group[shape] != group:
            anchor_bad.append((cid, "one_shape_hidden_under_multiple_groups"))
        group_shape[group] = shape
        shape_group[shape] = group
        group_rows[group].append(row)

    package_claims = [row for row in claims if row["unit_kind"] == "PACKAGE_HEADLINE_CLAUSE"]
    package_groups = {
        group: rows for group, rows in group_rows.items() if all(row["unit_kind"] == "PACKAGE_HEADLINE_CLAUSE" for row in rows)
    }
    package_group_sizes = Counter(len(rows) for rows in package_groups.values())
    record(
        "all_182_exact_source_ranges_tokens_excerpt_hashes",
        len(excerpt_hashes) == 182 and not anchor_bad,
        resolved=len(excerpt_hashes),
        bad=anchor_bad,
        provenance=dict(provenance),
    )
    record(
        "package_anchor_groups_83_37_single_46_shared",
        len(package_claims) == 172
        and len(package_groups) == 83
        and sum(len(rows) == 1 for rows in package_groups.values()) == 37
        and sum(len(rows) > 1 for rows in package_groups.values()) == 46
        and len(group_shape) == len(shape_group) == 93,
        package_claims=len(package_claims),
        groups=len(package_groups),
        singles=sum(len(rows) == 1 for rows in package_groups.values()),
        shared=sum(len(rows) > 1 for rows in package_groups.values()),
        size_distribution=dict(sorted(package_group_sizes.items())),
        all_claim_groups=len(group_shape),
    )

    # Semantic profiles must remain exactly 100 after stripping every prohibited
    # identity channel, including the reviewer clause itself where it occurs naturally.
    semantic_bad: list[str] = []
    semantic_ids: set[str] = set()
    stripped_profiles: set[str] = set()
    for row in package_claims:
        stack = row["premise_stack"]
        expected = "SEM:" + sha_bytes(stack.encode("utf-8"))[:16]
        if row["semantic_premise_id"] != expected:
            semantic_bad.append(row["claim_id"])
        if re.search(r"MC-\d+|CLAUSE_INDEX=|EXPLODED_REVIEW_CLAUSE=|SOURCE_(?:PATH|SHA256|ANCHOR|EXCERPT)=", stack):
            semantic_bad.append(row["claim_id"])
        if any(mark in stack for mark in ("PACKAGE_SCOPED_NAMED_CONDITION_RETAINED", "TRIGGER_FALLBACK", "TBD", "DEFAULT")):
            semantic_bad.append(row["claim_id"])
        required = [token for token in row["required_premise_tokens"].split("||") if token]
        if any(token not in stack for token in required):
            semantic_bad.append(row["claim_id"])
        semantic_ids.add(row["semantic_premise_id"])
        stripped = stack.replace(row["claim_id"], "").replace(row["source_clause"], "")
        stripped = re.sub(
            r"MC-\d+|CLAUSE_INDEX=[^;]*;?|EXPLODED_REVIEW_CLAUSE=[^;]*;?|SOURCE_(?:PATH|SHA256|ANCHOR|EXCERPT)=[^;]*;?",
            "",
            stripped,
        )
        stripped_profiles.add(stripped)
    record(
        "semantic_profiles_100_without_pseudo_uniqueness",
        len(semantic_ids) == len({row["premise_stack"] for row in package_claims}) == len(stripped_profiles) == 100
        and not semantic_bad,
        semantic_ids=len(semantic_ids),
        raw_stacks=len({row["premise_stack"] for row in package_claims}),
        profiles_after_stripping_identity=len(stripped_profiles),
        bad=sorted(set(semantic_bad)),
    )

    record(
        "source_admission_181_inventory_plus_1_review_overlay",
        provenance
        == Counter({"PREREGISTERED_SOURCE_INVENTORY": 181, "NON_RETROACTIVE_REVIEW_OVERLAY": 1})
        and sum(row["source_path"] in inventory_map for row in claims) == 181
        and sum(
            row["source_provenance_class"] == "NON_RETROACTIVE_REVIEW_OVERLAY"
            and row["unit_id"] == "D-001"
            and row["source_path"] == REVIEW_OVERLAY
            for row in claims
        )
        == 1,
        provenance=dict(provenance),
        inventory_admitted=sum(row["source_path"] in inventory_map for row in claims),
        review_overlay_admitted=sum(row["source_provenance_class"] == "NON_RETROACTIVE_REVIEW_OVERLAY" for row in claims),
    )

    premise_by_unit = {row["unit_id"]: row for row in premise}
    premise_bad: list[str] = []
    for uid in (f"P4-{index:02d}" for index in range(29)):
        rows_for_unit = [row for row in package_claims if row["unit_id"] == uid]
        audit = premise_by_unit.get(uid, {})
        if not (
            audit.get("audit_result") == "PASS_SOURCE_LOCAL_ANCHORED_WITH_LEGITIMATE_SHARED_GROUPS"
            and int(audit.get("exploded_claim_count", "-1")) == len(rows_for_unit)
            and int(audit.get("clause_source_stamp_count", "-1")) == len(rows_for_unit)
            and int(audit.get("source_anchor_group_count", "-1"))
            == len({row["shared_source_premise_id"] for row in rows_for_unit})
            and int(audit.get("semantic_premise_profile_count", "-1"))
            == len({row["semantic_premise_id"] for row in rows_for_unit})
        ):
            premise_bad.append(uid)
    record("premise_audit_emission_matches_recomputed_counts", not premise_bad, bad=premise_bad)

    labels = Counter(row["independence_label"] for row in independence)
    parser_actual = {
        row["record_id"]
        for row in independence
        if row["independence_label"] == "INDEPENDENT_PARSER_OR_REGRESSION"
    }
    record(
        "independence_21_pass_15_plus_6",
        len(independence) == 21
        and all(row["status"] == "PASS" for row in independence)
        and labels
        == Counter({"GENUINELY_DIFFERENT_METHOD": 15, "INDEPENDENT_PARSER_OR_REGRESSION": 6})
        and parser_actual == PARSER_IDS,
        labels=dict(labels),
        parser_ids=sorted(parser_actual),
    )

    recompute = run("python3", "independent_recompute.py")
    recompute_records = [json.loads(line) for line in recompute.stdout.splitlines() if line.startswith("{")]
    recompute_checks = [row for row in recompute_records if "record_id" in row]
    record(
        "independent_recompute_21_byte_replay",
        recompute.returncode == 0
        and len(recompute_checks) == 21
        and all(row.get("status") == "PASS" for row in recompute_checks)
        and sha_bytes(recompute.stdout.encode()) == sha(OUT / "INDEPENDENT_RECOMPUTATION_RAW.jsonl"),
        returncode=recompute.returncode,
        checks=len(recompute_checks),
        replay_sha256=sha_bytes(recompute.stdout.encode()),
        saved_sha256=sha(OUT / "INDEPENDENT_RECOMPUTATION_RAW.jsonl"),
        stderr=recompute.stderr,
    )

    blank = [
        f"{row['claim_id']}:{field}"
        for row in claims
        for field in COMPLETENESS
        if not row.get(field, "").strip()
    ]
    record(
        "completeness_1820_cells",
        not blank,
        rows=len(claims),
        cells_per_row=len(COMPLETENESS),
        populated=len(claims) * len(COMPLETENESS) - len(blank),
        blank=blank,
    )

    action_rows = [row for row in claims if row["unit_id"] in ACTION_EXPECTED]
    action_counts = Counter(row["unit_id"] for row in action_rows)
    action_bad = [
        row["claim_id"]
        for row in action_rows
        if ACTION_EXPECTED[row["unit_id"]] not in row["action_terms_covered_or_dropped"]
        or "response/geometry only" in row["action_terms_covered_or_dropped"]
    ]
    record(
        "action_cells_26_corrected",
        len(action_rows) == 26 and action_counts == Counter(ACTION_COUNTS) and not action_bad,
        count=len(action_rows),
        by_unit=dict(action_counts),
        bad=action_bad,
    )

    q2 = [row for row in claims if row["unit_id"] == "Q2"]
    q2_tokens = (
        "banked package controls",
        "cold parser regression",
        "not a cold different-method proof",
        "solution-level embedding remains open",
    )
    record(
        "q2_parser_control_grade",
        len(q2) == 1
        and q2[0]["regrade"] == "OPEN"
        and all(token in q2[0]["replacement_sentence"] for token in q2_tokens)
        and "BANK_CONTROL_PLUS_COLD_PARSER_REGRESSION" in q2[0]["quantifier_guard"],
        replacement=q2[0]["replacement_sentence"] if q2 else None,
    )

    k4 = [row for row in claims if row["regrade"] == "CONTRADICTED"]
    record(
        "k4_single_contradiction_retained",
        len(k4) == 1
        and k4[0]["unit_id"] == "P4-19"
        and "screen-character image {+1,-1}" in k4[0]["replacement_sentence"]
        and "order-four K4 group itself does not embed" in k4[0]["replacement_sentence"],
        contradicted=[row["claim_id"] for row in k4],
    )

    overlay_counts = Counter(row["classification"] for row in overlay)
    overlay_bad: list[str] = []
    for row in overlay:
        path = ROOT / row["path"]
        cited = [item for item in row["cited_by"].split("|") if item]
        if not (
            row["overlay_date"] == "2026-08-01"
            and row["overlay_status"] == "NON_RETROACTIVE_POST_OUTCOME_DEPENDENCY_RECORD"
            and path.is_file()
            and sha(path) == row["sha256"] == row["base_sha256"]
            and row["base_byte_identical"] == "TRUE"
            and int(row["cited_by_count"]) == len(cited)
        ):
            overlay_bad.append(row["path"])
    record(
        "dependency_overlay_13_7_plus_6",
        len(overlay) == len(overlay_map) == 13
        and overlay_counts == Counter({"LOAD_BEARING": 7, "SUPPORTING": 6})
        and not overlay_bad
        and overlay_map.get(CAP_PATH, {}).get("sha256") == CAP_HASH
        and overlay_map.get(JOINT_PATH, {}).get("sha256") == JOINT_HASH,
        rows=len(overlay),
        classifications=dict(overlay_counts),
        bad=overlay_bad,
        cap_hash=overlay_map.get(CAP_PATH, {}).get("sha256"),
        joint_hash=overlay_map.get(JOINT_PATH, {}).get("sha256"),
    )

    production = run("python3", "verify_cold_review.py")
    production_records = [json.loads(line) for line in production.stdout.splitlines() if line.startswith("{")]
    production_passes = [row["check"] for row in production_records if row.get("status") == "PASS"]
    catch_names = [name for name in production_passes if name.startswith("catch_")]
    prior_failure_classes = {
        "catch_missing_unit",
        "catch_duplicate_frozen_unit",
        "catch_production_source_manifest_mutation",
        "catch_concrete_quantifier_promotion",
        "catch_actual_parser_false_independence",
        "catch_missing_completeness_cell",
        "catch_mutated_source_excerpt_hash",
    }
    record(
        "production_27_pass_and_prior_7_catches",
        production.returncode == 0
        and len(production_passes) == 27
        and len(catch_names) == 9
        and prior_failure_classes <= set(catch_names)
        and production_records[-1].get("summary") == {"checks": 27, "failed": 0, "passed": 27},
        returncode=production.returncode,
        passes=len(production_passes),
        catches=catch_names,
        prior_seven_present=sorted(prior_failure_classes & set(catch_names)),
        stdout=production.stdout,
        stderr=production.stderr,
    )

    immutable_actual = {name: sha(OUT / name) for name in IMMUTABLE}
    second_section = report_section(
        "## Required second fresh adversarial verifier — 2026-08-01\n",
        "\n## Primary amendment closure — 2026-08-01",
    )
    closure_section = report_section(
        "## Same-second-verifier closure — 2026-08-01\n",
        "\n## Source-local anchor blocker response — 2026-08-01",
    )
    record(
        "prior_second_and_closure_records_immutable",
        immutable_actual == IMMUTABLE
        and sha_bytes(second_section.encode()) == SECOND_SECTION_HASH
        and sha_bytes(closure_section.encode()) == CLOSURE_SECTION_HASH,
        artifact_hashes=immutable_actual,
        second_section_sha256=sha_bytes(second_section.encode()),
        closure_section_sha256=sha_bytes(closure_section.encode()),
    )

    stop = review_results.get("smallest_next_step", "")
    maximum = review_results.get("maximum_conclusion", "")
    report_text = (OUT / "AUDIT_REPORT.md").read_text()
    record(
        "stop_repair_first_and_maximum_ceiling",
        stop.startswith("STOP_REPAIR_FIRST")
        and "premise-scoped formal response/census chain" in maximum
        and "No T4, adoption, new science, GPU work, physics claim, or canon change" in report_text,
        smallest_next_step=stop,
        maximum_conclusion=maximum,
    )

    result_anchor = review_results.get("source_local_premise_anchors", {})
    record(
        "review_results_anchor_counts_match",
        result_anchor
        == {
            "anchored_package_clause_rows": 172,
            "legitimate_shared_anchor_groups": 46,
            "note": "Counts are semantic/source-anchor counts; no uniqueness claim is manufactured from claim IDs or row indices.",
            "package_clause_rows": 172,
            "semantic_premise_profiles": 100,
            "single_clause_anchor_groups": 37,
            "source_anchor_groups": 83,
        },
        emitted=result_anchor,
    )

    prereg = run("python3", "verify_preregistration.py")
    record(
        "preregistration_recheck",
        prereg.returncode == 0 and "37 units" in prereg.stdout and "311 source paths" in prereg.stdout and BASE in prereg.stdout,
        returncode=prereg.returncode,
        stdout=prereg.stdout,
        stderr=prereg.stderr,
    )
    premise_verify = run("python3", "verify_current_scientific_premises.py", cwd=ROOT)
    record(
        "current_scientific_premises_recheck",
        premise_verify.returncode == 0 and "PASS" in premise_verify.stdout,
        returncode=premise_verify.returncode,
        stdout=premise_verify.stdout,
        stderr=premise_verify.stderr,
    )

    review_manifest_count, review_manifest_bad = validate_manifest("REVIEW_MANIFEST.sha256")
    record(
        "current_review_manifest_pre_final_append",
        review_manifest_count > 0 and not review_manifest_bad,
        entries=review_manifest_count,
        bad=review_manifest_bad,
        manifest_sha256=sha(OUT / "REVIEW_MANIFEST.sha256"),
    )

    status = run("git", "status", "--porcelain", cwd=ROOT)
    prefix = OUT.name + "/"
    paths: list[str] = []
    outside: list[str] = []
    for line in status.stdout.splitlines():
        path = line[3:].split(" -> ")[-1]
        paths.append(path)
        if not path.startswith(prefix):
            outside.append(path)
    record(
        "isolation_zero_outside_package",
        status.returncode == 0 and not outside,
        paths=paths,
        outside=outside,
        stderr=status.stderr,
    )

    verdict = "CLOSED-PASS" if not failures else "FURTHER"
    result = {
        "verdict": verdict,
        "review_base": BASE,
        "checks": len(raw),
        "passed": len(raw) - len(failures),
        "failed": failures,
        "exact_counts": {
            "review_units": len(frozen),
            "frozen_sources": len(inventory),
            "claims": len(claims),
            "package_clauses": len(package_claims),
            "package_anchor_groups": len(package_groups),
            "single_anchor_groups": sum(len(rows) == 1 for rows in package_groups.values()),
            "shared_anchor_groups": sum(len(rows) > 1 for rows in package_groups.values()),
            "semantic_profiles": len(semantic_ids),
            "inventory_anchors": provenance["PREREGISTERED_SOURCE_INVENTORY"],
            "review_overlay_anchors": provenance["NON_RETROACTIVE_REVIEW_OVERLAY"],
            "different_method": labels["GENUINELY_DIFFERENT_METHOD"],
            "parser_or_regression": labels["INDEPENDENT_PARSER_OR_REGRESSION"],
            "recomputations": len(independence),
            "completeness_cells": len(claims) * len(COMPLETENESS),
            "action_cells": len(action_rows),
            "production_checks": len(production_passes),
            "production_catches": len(catch_names),
            "overlay_rows": len(overlay),
            "overlay_load_bearing": overlay_counts["LOAD_BEARING"],
            "overlay_supporting": overlay_counts["SUPPORTING"],
        },
        "hashes": {
            "mechanical_claim_regrades": sha(OUT / "MECHANICAL_CLAIM_REGRADES.tsv"),
            "premise_quantifier_audit": sha(OUT / "PREMISE_QUANTIFIER_AUDIT.tsv"),
            "independence_ledger": sha(OUT / "INDEPENDENT_RECOMPUTATION_LEDGER.tsv"),
            "independent_raw": sha(OUT / "INDEPENDENT_RECOMPUTATION_RAW.jsonl"),
            "overlay": sha(OUT / "TRANSITIVE_DEPENDENCY_OVERLAY.tsv"),
            "review_results": sha(OUT / "REVIEW_RESULTS.json"),
            "production_verifier": sha(OUT / "verify_cold_review.py"),
            "production_raw": sha(OUT / "REVIEW_VERIFIER_RAW.jsonl"),
            "source_manifest": sha(OUT / "SOURCE_MANIFEST.sha256"),
            "review_manifest": sha(OUT / "REVIEW_MANIFEST.sha256"),
            "cap": CAP_HASH,
            "joint": JOINT_HASH,
        },
        "scope": "evidence-review closure only; STOP_REPAIR_FIRST remains; no T4, adoption, new science, GPU, physics, canon, or git mutation",
    }
    RAW_PATH.write_text("".join(json.dumps(item, sort_keys=True) + "\n" for item in raw))
    RESULT_PATH.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))
    raise SystemExit(0 if not failures else 1)


if __name__ == "__main__":
    main()
