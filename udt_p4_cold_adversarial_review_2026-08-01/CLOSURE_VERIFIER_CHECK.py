#!/usr/bin/env python3
"""Independent same-second-verifier closure check for the amended cold review.

This checker does not import the primary builder or verifier.  It parses emitted
artifacts, recomputes hashes from repository bytes, invokes saved entry points as
black boxes, and writes only its own two records beside this script.
"""

from __future__ import annotations

import csv
import hashlib
import json
import re
import subprocess
from collections import Counter
from pathlib import Path


OUT = Path(__file__).resolve().parent
ROOT = OUT.parent
BASE = "2e93a621aeeee0a0844543068363d0ba94094357"
RAW_PATH = OUT / "CLOSURE_VERIFIER_RAW.jsonl"
RESULT_PATH = OUT / "CLOSURE_VERIFIER_RESULTS.json"

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
CONDITION_CATEGORIES = (
    "SIGN",
    "POSITIVITY",
    "NORMALIZATION",
    "BRANCH",
    "BOUNDARY_GERM",
    "PAIRING",
    "POSTURE",
    "TOPOLOGY",
)
PARSER_IDS = {"IR03", "IR06", "IR10", "IR15", "IR19", "IR20"}
ACTION_EXPECTED = {
    "P4-07": "no native action selected; reduced conditional action/ODE and integrated response pairing are explicitly used",
    "P4-08": "no native action selected; cell-energy first integral and conditional action-derived mass definitions are explicitly used",
    "P4-16": "no global action or posture selected; seam functional B and its N=2 first variation are explicitly active",
    "P4-18": "no complete action selected; reduced second variation/Hessian and wall-germ Hessian sectors are explicitly tested",
    "P4-20": "no coupling or action selected; IF-ADOPTED theta coupling classes and coupling terms are explicitly tested",
}
ACTION_COUNTS = {"P4-07": 4, "P4-08": 5, "P4-16": 5, "P4-18": 5, "P4-20": 7}
SECOND_HASHES = {
    "SECOND_VERIFIER_CHECK.py": "170bd495f1f908ee9a155906d6822ed29fe827850f68aea5eae5fa5ceeffd2c0",
    "SECOND_VERIFIER_RAW.jsonl": "2027bc7d01b6494714e4f8a4755c8ce067cfd77e221d93655715f6e12275affb",
    "SECOND_VERIFIER_RESULTS.json": "0cfcd7c621e120cde2b89d75a5d47f514bdd5a43549ef4053daad9e84001e4d7",
    "SECOND_VERIFIER_PREMISE_RAW.txt": "67548c2f45b0ac85fedbd95705493469aab88780e747382953fa0dc515a346b2",
    "SECOND_VERIFIER_MANIFEST.sha256": "c8ecc256f8ef41707e22856e168334ceb32a0ee2ea06e2f7b71b703ebae8ea0a",
}
SECOND_SECTION_HASH = "899fc7793bfe661fd8f0f8c1e30696e4af110116d6af23d655b79d914cd38bae"
CAP_PATH = "udt_higher_isometry_plane_ownership_audit_2026-07-28/TORIC_CAP_ENUMERATION.tsv"
CAP_HASH = "ceecb5837ff8652c83c0ba72c67645182b1fd30f6e437026bd735c4d813bdfdf"
JOINT_PATH = "udt_joint_selector_provenance_audit_2026-07-28/JOINT_OPERATION_OBLIGATIONS.tsv"
JOINT_HASH = "52bc430e16227cc60d73e312a916666e0d206c54dc90a0d7ca8914d6c01336e9"


raw: list[dict[str, object]] = []
failures: list[str] = []


def digest_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def digest(path: Path) -> str:
    return digest_bytes(path.read_bytes())


def rows(name: str) -> list[dict[str, str]]:
    with (OUT / name).open(newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def run(*args: str, cwd: Path = OUT) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, cwd=cwd, text=True, capture_output=True, check=False)


def check(name: str, ok: bool, **detail: object) -> None:
    record = {"check": name, "status": "PASS" if ok else "FAIL", **detail}
    raw.append(record)
    if not ok:
        failures.append(name)


def git_bytes(path: str) -> bytes:
    proc = subprocess.run(
        ("git", "show", f"{BASE}:{path}"), cwd=ROOT, capture_output=True, check=False
    )
    if proc.returncode:
        raise RuntimeError(f"git show failed for {path}: {proc.stderr.decode(errors='replace')}")
    return proc.stdout


def validate_manifest(name: str) -> tuple[int, list[str]]:
    bad: list[str] = []
    count = 0
    for line in (OUT / name).read_text().splitlines():
        if not line.strip():
            continue
        count += 1
        expected, rel = line.split("  ", 1)
        path = (OUT / rel).resolve()
        if not path.is_file() or digest(path) != expected:
            bad.append(rel)
    return count, bad


def original_second_section() -> str:
    report = (OUT / "AUDIT_REPORT.md").read_text()
    marker = "## Required second fresh adversarial verifier — 2026-08-01\n"
    end = "\n## Primary amendment closure — 2026-08-01"
    return marker + report.split(marker, 1)[1].split(end, 1)[0]


def main() -> None:
    frozen = rows("FROZEN_REVIEW_UNITS.tsv")
    inventory = rows("SOURCE_INVENTORY.tsv")
    claims = rows("MECHANICAL_CLAIM_REGRADES.tsv")
    independence = rows("INDEPENDENT_RECOMPUTATION_LEDGER.tsv")
    premise = rows("PREMISE_QUANTIFIER_AUDIT.tsv")
    overlay = rows("TRANSITIVE_DEPENDENCY_OVERLAY.tsv")

    frozen_ids = [r["unit_id"] for r in frozen]
    check(
        "frozen_units_37_29_plus_8",
        len(frozen) == len(set(frozen_ids)) == 37
        and Counter(r["unit_kind"] for r in frozen)
        == Counter({"PACKAGE_HEADLINE_BUNDLE": 29, "CROSS_CUTTING_QUESTION": 8}),
        rows=len(frozen),
        kinds=dict(Counter(r["unit_kind"] for r in frozen)),
    )

    source_manifest_count, source_manifest_bad = validate_manifest("SOURCE_MANIFEST.sha256")
    inventory_bad: list[str] = []
    inventory_base_bad: list[str] = []
    for row in inventory:
        path = ROOT / row["path"]
        if not path.is_file() or digest(path) != row["sha256"]:
            inventory_bad.append(row["path"])
        else:
            if digest_bytes(git_bytes(row["path"])) != row["sha256"]:
                inventory_base_bad.append(row["path"])
    check(
        "source_freeze_311_current_and_base",
        len(inventory) == 311
        and len({r["path"] for r in inventory}) == 311
        and source_manifest_count == 311
        and not source_manifest_bad
        and not inventory_bad
        and not inventory_base_bad,
        inventory_rows=len(inventory),
        manifest_rows=source_manifest_count,
        current_bad=inventory_bad,
        base_bad=inventory_base_bad,
        source_manifest_bad=source_manifest_bad,
        source_manifest_sha256=digest(OUT / "SOURCE_MANIFEST.sha256"),
    )

    kinds = Counter(r["unit_kind"] for r in claims)
    regrades = Counter(r["regrade"] for r in claims)
    claim_ids = [r["claim_id"] for r in claims]
    check(
        "claim_census_and_regrades",
        len(claims) == len(set(claim_ids)) == 182
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

    k4 = [r for r in claims if r["regrade"] == "CONTRADICTED"]
    k4_ok = (
        len(k4) == 1
        and k4[0]["unit_id"] == "P4-19"
        and "only that the screen-character image {+1,-1}" in k4[0]["replacement_sentence"]
        and "K4 group itself does not embed" in k4[0]["replacement_sentence"]
    )
    check("k4_single_correction_retained", k4_ok, contradicted=[r["claim_id"] for r in k4])

    q2 = [r for r in claims if r["unit_id"] == "Q2"]
    q2_tokens = (
        "banked package controls",
        "cold parser regression",
        "not a cold different-method proof",
        "solution-level embedding remains open",
    )
    check(
        "q2_bank_control_parser_only",
        len(q2) == 1
        and q2[0]["regrade"] == "OPEN"
        and all(token in q2[0]["replacement_sentence"] for token in q2_tokens)
        and "BANK_CONTROL_PLUS_COLD_PARSER_REGRESSION" in q2[0]["quantifier_guard"],
        replacement=q2[0]["replacement_sentence"] if q2 else None,
    )

    labels = Counter(r["independence_label"] for r in independence)
    parser_actual = {r["record_id"] for r in independence if r["independence_label"] == "INDEPENDENT_PARSER_OR_REGRESSION"}
    check(
        "independence_15_plus_6_all_pass",
        len(independence) == 21
        and all(r["status"] == "PASS" for r in independence)
        and labels
        == Counter({"GENUINELY_DIFFERENT_METHOD": 15, "INDEPENDENT_PARSER_OR_REGRESSION": 6})
        and parser_actual == PARSER_IDS,
        labels=dict(labels),
        parser_ids=sorted(parser_actual),
    )

    blank_cells = [
        f"{r['claim_id']}:{field}" for r in claims for field in COMPLETENESS if not r.get(field, "").strip()
    ]
    check(
        "all_ten_completeness_cells_182",
        set(COMPLETENESS).issubset(claims[0]) and not blank_cells,
        cells=len(COMPLETENESS),
        rows=len(claims),
        populated=len(claims) * len(COMPLETENESS) - len(blank_cells),
        blank=blank_cells,
    )

    action_rows = [r for r in claims if r["unit_id"] in ACTION_EXPECTED]
    action_counts = Counter(r["unit_id"] for r in action_rows)
    action_bad = [
        r["claim_id"]
        for r in action_rows
        if r["action_terms_covered_or_dropped"] != ACTION_EXPECTED[r["unit_id"]]
        or "response/geometry only" in r["action_terms_covered_or_dropped"]
    ]
    check(
        "action_cells_26_corrected",
        len(action_rows) == 26 and action_counts == Counter(ACTION_COUNTS) and not action_bad,
        count=len(action_rows),
        by_unit=dict(action_counts),
        bad=action_bad,
    )

    package_claims = [r for r in claims if r["unit_kind"] == "PACKAGE_HEADLINE_CLAUSE"]
    stamp_bad: list[str] = []
    source_located: list[str] = []
    semantic_stacks: list[str] = []
    active_category_rows = 0
    generic_active_rows = 0
    inventory_by_path = {r["path"]: r for r in inventory}
    for row in package_claims:
        stack = row["premise_stack"]
        source = ROOT / row["source_path"]
        source_hash = digest(source) if source.is_file() else ""
        source_text = source.read_text(errors="replace") if source.is_file() else ""
        match = re.fullmatch(rf"{re.escape(row['unit_id'])}:C(\d{{2}}):([0-9a-f]{{12}})", row["source_stamp_id"])
        required = (
            f"SOURCE_SHA256={source_hash}",
            f"SOURCE_PATH={row['source_path']}",
            f"EXPLODED_REVIEW_CLAUSE={row['source_clause']}",
            "SCOPE=",
            "ACTION_FIELD_ADOPTION_STATUS=",
            f"QUANTIFIER={row['quantifier_guard']}",
        ) + tuple(f"{category}=" for category in CONDITION_CATEGORIES)
        required_names = (
            "SOURCE_SHA256=",
            "SOURCE_PATH=",
            f"CLAUSE_INDEX={int(match.group(1))}" if match else "CLAUSE_INDEX=INVALID",
            f"EXPLODED_REVIEW_CLAUSE={row['source_clause']}",
            "SCOPE=",
            "ACTION_FIELD_ADOPTION_STATUS=",
            f"QUANTIFIER={row['quantifier_guard']}",
        ) + tuple(f"{category}=" for category in CONDITION_CATEGORIES)
        active = sum(f"{category}=NOT_LOAD_BEARING_FOR_THIS_CLAUSE" not in stack for category in CONDITION_CATEGORIES)
        active_category_rows += active > 0
        generic_active_rows += "PACKAGE_SCOPED_NAMED_CONDITION_RETAINED" in stack
        if row["source_clause"].casefold() in source_text.casefold() or "SOURCE_ANCHOR=" in stack or "SOURCE_EXCERPT_SHA256=" in stack:
            source_located.append(row["claim_id"])
        semantic_stacks.append(
            re.sub(
                r"^SOURCE_SHA256=[0-9a-f]+; SOURCE_PATH=[^;]+; CLAUSE_INDEX=\d+; EXPLODED_REVIEW_CLAUSE=[^;]+; ",
                "",
                stack,
            )
        )
        ok = (
            source_hash
            and row["source_path"] in inventory_by_path
            and inventory_by_path[row["source_path"]]["sha256"] == source_hash
            and match is not None
            and match.group(2) == source_hash[:12]
            and f"CLAUSE_INDEX={int(match.group(1))}" in stack
            and all(token in stack for token in required)
            and "all DERIVED/CHOSE/OPEN/CONDITIONAL/POSIT labels retained" in stack
            and "no action, field, carrier, mass, coupling, dynamics or physics adopted" in stack
            and all(token in row["required_premise_tokens"] for token in required_names)
        )
        if not ok:
            stamp_bad.append(row["claim_id"])
    premise_counts_ok = all(
        r["audit_result"] == "PASS_CLAUSE_SPECIFIC_WITH_SCOPE"
        and r["exploded_claim_count"] == r["clause_source_stamp_count"] == r["unique_clause_premise_stacks"]
        for r in premise
        if r["unit_id"].startswith("P4-")
    )
    check(
        "clause_specific_condition_rich_stamps_172",
        len(package_claims) == 172
        and len({r["source_stamp_id"] for r in package_claims}) == 172
        and len({r["premise_stack"] for r in package_claims}) == 172
        and not stamp_bad
        and premise_counts_ok,
        rows=len(package_claims),
        unique_stamps=len({r["source_stamp_id"] for r in package_claims}),
        unique_stacks=len({r["premise_stack"] for r in package_claims}),
        rows_with_at_least_one_active_condition=active_category_rows,
        rows_with_explicit_not_load_bearing_categories=len(package_claims) - active_category_rows,
        rows_with_package_scoped_fallback_for_a_trigger=generic_active_rows,
        source_located_clauses=len(source_located),
        source_unlocated_clauses=len(package_claims) - len(source_located),
        unique_semantic_stacks_after_removing_stamp_identity=len(set(semantic_stacks)),
        bad=stamp_bad,
    )
    # Structural uniqueness above is not enough for the requested source-level closure.
    # A source hash repeated for every claim in a package plus a reviewer-local index does
    # not locate the claim in that source.  Require either a literal source occurrence or
    # an explicit source anchor/excerpt hash for every exploded clause.
    if len(source_located) != len(package_claims):
        failures.append("clause_specific_source_location_1_of_172")
        raw.append(
            {
                "check": "clause_specific_source_location_172",
                "status": "FAIL",
                "located": len(source_located),
                "unlocated": len(package_claims) - len(source_located),
                "located_claim_ids": source_located,
                "unique_semantic_stacks_after_removing_stamp_identity": len(set(semantic_stacks)),
                "reason": "171 reviewer clauses have no literal source occurrence, SOURCE_ANCHOR, or SOURCE_EXCERPT_SHA256; local review indices therefore do not establish exact per-clause source provenance",
            }
        )

    production = run("python3", "verify_cold_review.py")
    production_records = [json.loads(line) for line in production.stdout.splitlines() if line.startswith("{")]
    production_passes = [
        record["check"] for record in production_records if record.get("status") == "PASS"
    ]
    catch_names = [name for name in production_passes if name.startswith("catch_")]
    check(
        "production_verifier_23_and_catches_7",
        production.returncode == 0
        and len(production_passes) == 23
        and len(catch_names) == 7
        and production_records[-1].get("summary") == {"checks": 23, "failed": 0, "passed": 23},
        returncode=production.returncode,
        passes=len(production_passes),
        catch_names=catch_names,
        stdout=production.stdout,
        stderr=production.stderr,
    )

    recompute = run("python3", "independent_recompute.py")
    replay_records = [json.loads(line) for line in recompute.stdout.splitlines() if line.strip().startswith("{")]
    check(
        "cold_recompute_21_replay",
        recompute.returncode == 0
        and len([r for r in replay_records if "record_id" in r]) == 21
        and all(r.get("status") == "PASS" for r in replay_records if "record_id" in r)
        and digest_bytes(recompute.stdout.encode()) == digest(OUT / "INDEPENDENT_RECOMPUTATION_RAW.jsonl"),
        returncode=recompute.returncode,
        records=len([r for r in replay_records if "record_id" in r]),
        replay_sha256=digest_bytes(recompute.stdout.encode()),
        saved_sha256=digest(OUT / "INDEPENDENT_RECOMPUTATION_RAW.jsonl"),
        stderr=recompute.stderr,
    )

    overlay_counts = Counter(r["classification"] for r in overlay)
    overlay_bad: list[str] = []
    for row in overlay:
        current = ROOT / row["path"]
        current_hash = digest(current) if current.is_file() else ""
        base_hash = digest_bytes(git_bytes(row["path"]))
        cited = [x for x in row["cited_by"].split("|") if x]
        if not (
            row["overlay_date"] == "2026-08-01"
            and row["overlay_status"] == "NON_RETROACTIVE_POST_OUTCOME_DEPENDENCY_RECORD"
            and current_hash == base_hash == row["sha256"] == row["base_sha256"]
            and row["base_byte_identical"] == "TRUE"
            and int(row["cited_by_count"]) == len(cited)
            and all((ROOT / path).is_file() for path in cited)
        ):
            overlay_bad.append(row["path"])
    overlay_map = {r["path"]: r for r in overlay}
    check(
        "nonretroactive_overlay_13_7_plus_6",
        len(overlay) == 13
        and len({r["path"] for r in overlay}) == 13
        and overlay_counts == Counter({"LOAD_BEARING": 7, "SUPPORTING": 6})
        and not overlay_bad
        and overlay_map.get(CAP_PATH, {}).get("sha256") == CAP_HASH
        and overlay_map.get(JOINT_PATH, {}).get("sha256") == JOINT_HASH,
        rows=len(overlay),
        classifications=dict(overlay_counts),
        bad=overlay_bad,
        cap_hash=overlay_map.get(CAP_PATH, {}).get("sha256"),
        joint_hash=overlay_map.get(JOINT_PATH, {}).get("sha256"),
        overlay_sha256=digest(OUT / "TRANSITIVE_DEPENDENCY_OVERLAY.tsv"),
    )

    second_actual = {name: digest(OUT / name) for name in SECOND_HASHES}
    section_hash = digest_bytes(original_second_section().encode())
    check(
        "original_second_verifier_preserved",
        second_actual == SECOND_HASHES and section_hash == SECOND_SECTION_HASH,
        artifact_hashes=second_actual,
        section_sha256=section_hash,
    )

    result = json.loads((OUT / "REVIEW_RESULTS.json").read_text())
    report = (OUT / "AUDIT_REPORT.md").read_text()
    check(
        "stop_repair_first_and_maximum_conclusion_retained",
        result.get("smallest_next_step", "").startswith("STOP_REPAIR_FIRST")
        and "premise-scoped formal response/census" in result.get("maximum_conclusion", "")
        and "**STOP_REPAIR_FIRST remains in force**" in report
        and all(term in report for term in ("no T4", "adoption", "new science", "GPU run", "canon change")),
        smallest_next_step=result.get("smallest_next_step"),
        maximum_conclusion=result.get("maximum_conclusion"),
    )

    prereg = run("python3", "verify_preregistration.py")
    check(
        "preregistration_recheck",
        prereg.returncode == 0
        and "37 units" in prereg.stdout
        and "311 source paths" in prereg.stdout
        and BASE in prereg.stdout,
        returncode=prereg.returncode,
        stdout=prereg.stdout,
        stderr=prereg.stderr,
    )

    premise_verify = run("python3", "verify_current_scientific_premises.py", cwd=ROOT)
    check(
        "current_scientific_premises_recheck",
        premise_verify.returncode == 0 and "PASS" in premise_verify.stdout,
        returncode=premise_verify.returncode,
        stdout=premise_verify.stdout,
        stderr=premise_verify.stderr,
    )

    review_manifest_count, review_manifest_bad = validate_manifest("REVIEW_MANIFEST.sha256")
    check(
        "primary_review_manifest_current_preclosure_append",
        review_manifest_count > 0 and not review_manifest_bad,
        entries=review_manifest_count,
        bad=review_manifest_bad,
        manifest_sha256=digest(OUT / "REVIEW_MANIFEST.sha256"),
    )

    status = run("git", "status", "--porcelain", cwd=ROOT)
    package_prefix = OUT.name + "/"
    status_paths: list[str] = []
    outside: list[str] = []
    for line in status.stdout.splitlines():
        path = line[3:]
        if " -> " in path:
            path = path.split(" -> ", 1)[1]
        status_paths.append(path)
        if not path.startswith(package_prefix):
            outside.append(path)
    check(
        "isolation_zero_outside_package",
        status.returncode == 0 and not outside,
        status_paths=status_paths,
        outside=outside,
        stderr=status.stderr,
    )

    status_name = "CLOSED-PASS" if not failures else "FURTHER-AMENDMENTS"
    summary = {
        "verdict": status_name,
        "review_base": BASE,
        "checks": len(raw),
        "passed": len(raw) - len(failures),
        "failed": failures,
        "exact_counts": {
            "frozen_units": len(frozen),
            "source_inventory": len(inventory),
            "claims": len(claims),
            "package_clauses": len(package_claims),
            "cross_cutting": kinds["CROSS_CUTTING_QUESTION"],
            "discoveries": kinds["DISCOVERED_LOAD_BEARING_CLAIM"],
            "different_method": labels["GENUINELY_DIFFERENT_METHOD"],
            "parser_or_regression": labels["INDEPENDENT_PARSER_OR_REGRESSION"],
            "completeness_cells": len(COMPLETENESS),
            "action_cells": len(action_rows),
            "production_checks": len(production_passes),
            "production_catches": len(catch_names),
            "overlay_rows": len(overlay),
            "overlay_load_bearing": overlay_counts["LOAD_BEARING"],
            "overlay_supporting": overlay_counts["SUPPORTING"],
        },
        "hashes": {
            "mechanical_claim_regrades": digest(OUT / "MECHANICAL_CLAIM_REGRADES.tsv"),
            "premise_quantifier_audit": digest(OUT / "PREMISE_QUANTIFIER_AUDIT.tsv"),
            "independence_ledger": digest(OUT / "INDEPENDENT_RECOMPUTATION_LEDGER.tsv"),
            "independent_raw": digest(OUT / "INDEPENDENT_RECOMPUTATION_RAW.jsonl"),
            "overlay": digest(OUT / "TRANSITIVE_DEPENDENCY_OVERLAY.tsv"),
            "review_results": digest(OUT / "REVIEW_RESULTS.json"),
            "production_verifier": digest(OUT / "verify_cold_review.py"),
            "production_raw": digest(OUT / "REVIEW_VERIFIER_RAW.jsonl"),
            "source_manifest": digest(OUT / "SOURCE_MANIFEST.sha256"),
            "review_manifest": digest(OUT / "REVIEW_MANIFEST.sha256"),
            "cap": CAP_HASH,
            "joint": JOINT_HASH,
        },
        "scope": "evidence-review closure only; no producer-headline repair, transitive preregistration, T4, adoption, science, GPU, physics, or canon action",
    }
    RAW_PATH.write_text("".join(json.dumps(record, sort_keys=True) + "\n" for record in raw))
    RESULT_PATH.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))
    raise SystemExit(0 if not failures else 1)


if __name__ == "__main__":
    main()
