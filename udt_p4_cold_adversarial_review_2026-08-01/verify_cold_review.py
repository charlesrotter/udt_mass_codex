#!/usr/bin/env python3
"""Fail-closed verifier and production-path mutation proofs for the cold review."""

from __future__ import annotations

import csv
import hashlib
import json
import subprocess
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = Path(__file__).resolve().parent
PREFIX = OUT.name + "/"

COMPLETENESS_FIELDS = (
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

PARSER_OR_REGRESSION_IDS = {"IR03", "IR06", "IR10", "IR15", "IR19", "IR20"}

IMMUTABLE_SECOND = {
    "SECOND_VERIFIER_CHECK.py": "170bd495f1f908ee9a155906d6822ed29fe827850f68aea5eae5fa5ceeffd2c0",
    "SECOND_VERIFIER_MANIFEST.sha256": "c8ecc256f8ef41707e22856e168334ceb32a0ee2ea06e2f7b71b703ebae8ea0a",
    "SECOND_VERIFIER_PREMISE_RAW.txt": "67548c2f45b0ac85fedbd95705493469aab88780e747382953fa0dc515a346b2",
    "SECOND_VERIFIER_RAW.jsonl": "2027bc7d01b6494714e4f8a4755c8ce067cfd77e221d93655715f6e12275affb",
    "SECOND_VERIFIER_RESULTS.json": "0cfcd7c621e120cde2b89d75a5d47f514bdd5a43549ef4053daad9e84001e4d7",
}
IMMUTABLE_CLOSURE = {
    "CLOSURE_VERIFIER_CHECK.py": "9e1341b9250cd2ab2b63e86ac1df18a31752d906fffd476f64db71ed2c58e8c0",
    "CLOSURE_VERIFIER_MANIFEST.sha256": "f4b47972102ddeff04dcb4e83ad415326c57673111a2dac95b56b84333f471cf",
    "CLOSURE_VERIFIER_RAW.jsonl": "2a455041f1420faab5c735a14012923466195dc835875d00379ef1190fb6564c",
    "CLOSURE_VERIFIER_RESULTS.json": "dc4b299eb5db41bf3f93005dd13815a959e42d936741905d8ceb594edc48cba8",
}
SECOND_SECTION_MARKER = b"## Required second fresh adversarial verifier \xe2\x80\x94 2026-08-01\n"
AMENDMENT_MARKER = b"\n## Primary amendment closure \xe2\x80\x94 2026-08-01\n"
SECOND_SECTION_SHA256 = "899fc7793bfe661fd8f0f8c1e30696e4af110116d6af23d655b79d914cd38bae"
CLOSURE_SECTION_MARKER = b"## Same-second-verifier closure \xe2\x80\x94 2026-08-01\n"
ANCHOR_RESPONSE_MARKER = b"\n## Source-local anchor blocker response \xe2\x80\x94 2026-08-01\n"
CLOSURE_SECTION_SHA256 = "db4b97c8a7e4f05aa446b996367405021ab1e60de82b2dc9b2c68636f344d330"


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def duplicate_values(values: list[str]) -> list[str]:
    counts = Counter(values)
    return sorted(value for value, count in counts.items() if count != 1)


def check_frozen_units(rows: list[dict[str, str]]) -> list[str]:
    bad = duplicate_values([r.get("unit_id", "") for r in rows])
    expected = {f"P4-{i:02d}" for i in range(29)} | {f"Q{i}" for i in range(1, 9)}
    got = {r.get("unit_id", "") for r in rows}
    bad.extend(f"missing:{uid}" for uid in sorted(expected - got))
    bad.extend(f"unexpected:{uid}" for uid in sorted(got - expected))
    return sorted(set(bad))


def check_units(rows: list[dict[str, str]], required: set[str]) -> list[str]:
    got = {r["unit_id"] for r in rows}
    return sorted(required - got)


def check_duplicates(rows: list[dict[str, str]]) -> list[str]:
    return duplicate_values([r.get("claim_id", "") for r in rows])


def check_quantifiers(rows: list[dict[str, str]]) -> list[str]:
    bad = []
    for r in rows:
        q = r.get("quantifier_guard", "").strip()
        replacement = r.get("replacement_sentence", "").strip()
        if not q or not replacement:
            bad.append(r.get("claim_id", "?"))
            continue
        if r.get("unit_kind") == "PACKAGE_HEADLINE_CLAUSE" and r.get("regrade") != "CONTRADICTED":
            if "Within " not in replacement and "only within " not in replacement:
                bad.append(r["claim_id"])
        low = replacement.lower()
        if any(promotion in low for promotion in (
            "no common solution exists in every domain",
            "has no common solution in every domain",
            "universally selected physical action",
            "fixed realized on-shell embedding is proved",
        )):
            bad.append(r["claim_id"])
        if r.get("unit_id") == "P4-02" and "shares no exact static equation sector" in r.get("source_clause", ""):
            if "EQUATION_SET_INEQUIVALENCE" not in q or "absence of all common solutions" not in replacement:
                bad.append(r["claim_id"])
        if r.get("unit_id") == "Q2":
            required = ("banked package controls", "cold parser regression", "not a cold different-method proof", "solution-level embedding remains open")
            if any(token not in replacement for token in required):
                bad.append(r["claim_id"])
    return sorted(set(bad))


def check_semantic_premises(rows: list[dict[str, str]]) -> list[str]:
    bad = []
    package_rows = [r for r in rows if r.get("unit_kind") == "PACKAGE_HEADLINE_CLAUSE"]
    if len(package_rows) != 172:
        bad.append("PACKAGE_PREMISE_CENSUS")
    for r in package_rows:
        stack = r.get("premise_stack", "")
        tokens = [token for token in r.get("required_premise_tokens", "").split("||") if token]
        semantic_id = "SEM:" + sha256_bytes(stack.encode("utf-8"))[:16]
        if any(token not in stack for token in tokens) or r.get("semantic_premise_id") != semantic_id:
            bad.append(r["claim_id"])
        if any(forbidden in stack for forbidden in ("PACKAGE_SCOPED_NAMED_CONDITION_RETAINED", "DEFAULT", "TBD", "TRIGGER_FALLBACK")):
            bad.append(r["claim_id"])
    return sorted(set(bad))


def check_source_anchors(
    rows: list[dict[str, str]], inventory_paths: set[str], overlay_paths: set[str]
) -> list[str]:
    bad = []
    required_fields = (
        "source_path", "source_start_line", "source_end_line", "source_anchor_token",
        "source_excerpt_sha256", "shared_source_premise_id", "source_stamp_id",
        "source_provenance_class",
    )
    group_shapes: dict[str, tuple[str, ...]] = {}
    shape_groups: dict[tuple[str, ...], str] = {}
    package_count = 0
    for r in rows:
        cid = r.get("claim_id", "?")
        if any(not r.get(field, "").strip() for field in required_fields):
            bad.append(cid)
            continue
        if r.get("unit_kind") == "PACKAGE_HEADLINE_CLAUSE":
            package_count += 1
        path_text = r["source_path"]
        provenance = r["source_provenance_class"]
        admitted = (
            provenance == "PREREGISTERED_SOURCE_INVENTORY" and path_text in inventory_paths
        ) or (
            provenance == "NON_RETROACTIVE_DEPENDENCY_OVERLAY" and path_text in overlay_paths
        ) or (
            provenance == "NON_RETROACTIVE_REVIEW_OVERLAY"
            and path_text == PREFIX + "TRANSITIVE_DEPENDENCY_OVERLAY.tsv"
        )
        if not admitted:
            bad.append(cid)
        path = ROOT / path_text
        try:
            start = int(r["source_start_line"])
            end = int(r["source_end_line"])
        except ValueError:
            bad.append(cid)
            continue
        if not path.is_file():
            bad.append(cid)
            continue
        lines = path.read_bytes().splitlines(keepends=True)
        if start < 1 or end < start or end > len(lines):
            bad.append(cid)
            continue
        excerpt = b"".join(lines[start - 1:end])
        token = r["source_anchor_token"]
        if (
            token.encode("utf-8") not in excerpt
            or sha256_bytes(excerpt) != r["source_excerpt_sha256"]
            or len(token.strip()) < 10
            or any(x in token.upper() for x in ("DEFAULT", "TBD", "FALLBACK", "PACKAGE_TRIGGER"))
        ):
            bad.append(cid)
        substantive_lines = [
            line for line in excerpt.decode("utf-8").splitlines()
            if line.strip() and not line.lstrip().startswith("#")
        ]
        if not substantive_lines:
            bad.append(r["claim_id"])
        group = r["shared_source_premise_id"]
        shape = (path_text, str(start), str(end), token, r["source_excerpt_sha256"], provenance, r["source_stamp_id"])
        if group in group_shapes and group_shapes[group] != shape:
            bad.append(cid)
        if shape in shape_groups and shape_groups[shape] != group:
            bad.append(cid)
        group_shapes[group] = shape
        shape_groups[shape] = group
    if package_count != 172:
        bad.append(f"PACKAGE_ANCHOR_CENSUS:{package_count}")
    return sorted(set(bad))


def check_completeness(rows: list[dict[str, str]]) -> list[str]:
    bad = []
    action_rows = 0
    for r in rows:
        if any(not r.get(field, "").strip() for field in COMPLETENESS_FIELDS):
            bad.append(r.get("claim_id", "?"))
        uid = r.get("unit_id")
        if uid in ACTION_EXPECTED:
            action_rows += 1
            action = r.get("action_terms_covered_or_dropped", "")
            if ACTION_EXPECTED[uid] not in action or "response/geometry only" in action:
                bad.append(r.get("claim_id", "?"))
    if action_rows != 26:
        bad.append(f"ACTION_ROW_CENSUS:{action_rows}")
    return sorted(set(bad))


def check_false_independence(rows: list[dict[str, str]]) -> list[str]:
    bad = []
    got_ids = {r.get("record_id", "") for r in rows}
    for r in rows:
        rid = r["record_id"]
        label = r["independence_label"]
        expected = "INDEPENDENT_PARSER_OR_REGRESSION" if rid in PARSER_OR_REGRESSION_IDS else "GENUINELY_DIFFERENT_METHOD"
        if label != expected:
            bad.append(rid)
        if label not in {"GENUINELY_DIFFERENT_METHOD", "INDEPENDENT_PARSER_OR_REGRESSION"}:
            bad.append(rid)
    if len(rows) != 21 or not PARSER_OR_REGRESSION_IDS <= got_ids:
        bad.append("INDEPENDENCE_CENSUS")
    return sorted(set(bad))


def check_outside(paths: list[str]) -> list[str]:
    return sorted(p for p in paths if p and not p.startswith(PREFIX))


def source_manifest(overrides: dict[str, bytes] | None = None) -> tuple[int, list[str]]:
    """Production manifest checker; overrides support in-memory mutation proofs."""
    overrides = overrides or {}
    bad = []
    lines = (OUT / "SOURCE_MANIFEST.sha256").read_text().splitlines()
    for line in lines:
        digest, rel = line.split("  ", 1)
        path = (OUT / rel).resolve()
        if not path.is_file():
            bad.append(rel)
            continue
        data = overrides.get(rel, path.read_bytes())
        if sha256_bytes(data) != digest:
            bad.append(rel)
    return len(lines), bad


def check_overlay(rows: list[dict[str, str]]) -> list[str]:
    bad = []
    if len(rows) != 13 or duplicate_values([r.get("path", "") for r in rows]):
        bad.append("OVERLAY_CENSUS")
    if Counter(r.get("classification", "") for r in rows) != Counter({"LOAD_BEARING": 7, "SUPPORTING": 6}):
        bad.append("OVERLAY_CLASSIFICATION_CENSUS")
    for r in rows:
        path = ROOT / r["path"]
        if r.get("overlay_date") != "2026-08-01" or r.get("overlay_status") != "NON_RETROACTIVE_POST_OUTCOME_DEPENDENCY_RECORD":
            bad.append(r.get("path", "?"))
        if not path.is_file() or sha256(path) != r.get("sha256") or r.get("sha256") != r.get("base_sha256") or r.get("base_byte_identical") != "TRUE":
            bad.append(r.get("path", "?"))
        cited = [x for x in r.get("cited_by", "").split("|") if x]
        if len(cited) != int(r.get("cited_by_count", "-1")):
            bad.append(r.get("path", "?"))
    expected = {
        "udt_higher_isometry_plane_ownership_audit_2026-07-28/TORIC_CAP_ENUMERATION.tsv": "ceecb5837ff8652c83c0ba72c67645182b1fd30f6e437026bd735c4d813bdfdf",
        "udt_joint_selector_provenance_audit_2026-07-28/JOINT_OPERATION_OBLIGATIONS.tsv": "52bc430e16227cc60d73e312a916666e0d206c54dc90a0d7ca8914d6c01336e9",
    }
    by_path = {r["path"]: r for r in rows}
    for path, digest in expected.items():
        if by_path.get(path, {}).get("sha256") != digest:
            bad.append(path)
    return sorted(set(bad))


def check_immutable_second_verifier() -> list[str]:
    bad = [name for name, digest in IMMUTABLE_SECOND.items() if not (OUT / name).is_file() or sha256(OUT / name) != digest]
    report = (OUT / "AUDIT_REPORT.md").read_bytes()
    try:
        start = report.index(SECOND_SECTION_MARKER)
    except ValueError:
        return sorted(bad + ["AUDIT_REPORT:SECOND_SECTION_MISSING"])
    end = report.find(AMENDMENT_MARKER, start)
    section = report[start:] if end < 0 else report[start:end]
    if sha256_bytes(section) != SECOND_SECTION_SHA256:
        bad.append("AUDIT_REPORT:SECOND_SECTION_MUTATED")
    return sorted(bad)


def check_immutable_closure_verifier() -> list[str]:
    bad = [name for name, digest in IMMUTABLE_CLOSURE.items() if not (OUT / name).is_file() or sha256(OUT / name) != digest]
    report = (OUT / "AUDIT_REPORT.md").read_bytes()
    try:
        start = report.index(CLOSURE_SECTION_MARKER)
    except ValueError:
        return sorted(bad + ["AUDIT_REPORT:CLOSURE_SECTION_MISSING"])
    end = report.find(ANCHOR_RESPONSE_MARKER, start)
    section = report[start:] if end < 0 else report[start:end]
    if sha256_bytes(section) != CLOSURE_SECTION_SHA256:
        bad.append("AUDIT_REPORT:CLOSURE_SECTION_MUTATED")
    return sorted(bad)


def git_changed_paths() -> list[str]:
    raw = subprocess.check_output(["git", "status", "--porcelain", "-z"], cwd=ROOT)
    return [item[3:] for item in raw.decode().split("\0") if item]


def main() -> int:
    frozen = list(csv.DictReader((OUT / "FROZEN_REVIEW_UNITS.tsv").open(), delimiter="\t"))
    required = {r["unit_id"] for r in frozen}
    claims = list(csv.DictReader((OUT / "MECHANICAL_CLAIM_REGRADES.tsv").open(), delimiter="\t"))
    recompute = list(csv.DictReader((OUT / "INDEPENDENT_RECOMPUTATION_LEDGER.tsv").open(), delimiter="\t"))
    overlay = list(csv.DictReader((OUT / "TRANSITIVE_DEPENDENCY_OVERLAY.tsv").open(), delimiter="\t"))
    inventory = list(csv.DictReader((OUT / "SOURCE_INVENTORY.tsv").open(), delimiter="\t"))
    inventory_paths = {r["path"] for r in inventory}
    overlay_paths = {r["path"] for r in overlay}
    results = json.loads((OUT / "REVIEW_RESULTS.json").read_text())

    checks: list[tuple[str, bool, str]] = []
    frozen_bad = check_frozen_units(frozen)
    checks.append(("frozen_unit_identity_and_uniqueness", len(frozen) == 37 and not frozen_bad, f"rows={len(frozen)},bad={frozen_bad}"))
    checks.append(("package_and_cross_cutting_counts", sum(r["unit_id"].startswith("P4-") for r in frozen) == 29 and sum(r["unit_id"].startswith("Q") for r in frozen) == 8, "29+8"))
    checks.append(("claim_row_count", len(claims) == results["mechanical_claim_rows"] == 182, f"{len(claims)}"))
    checks.append(("all_units_covered", not check_units(claims, required), str(check_units(claims, required))))
    checks.append(("claim_ids_unique", not check_duplicates(claims), str(check_duplicates(claims))))
    quant_bad = check_quantifiers(claims)
    checks.append(("claim_specific_quantifier_guards", not quant_bad, str(quant_bad)))
    premise_bad = check_semantic_premises(claims)
    checks.append(("semantic_premise_profiles_no_row_id_uniqueness", not premise_bad, str(premise_bad)))
    anchor_bad = check_source_anchors(claims, inventory_paths, overlay_paths)
    package_claims = [r for r in claims if r["unit_kind"] == "PACKAGE_HEADLINE_CLAUSE"]
    anchor_sizes = Counter(r["shared_source_premise_id"] for r in package_claims)
    anchor_result = results.get("source_local_premise_anchors", {})
    anchor_counts_ok = (
        anchor_result.get("package_clause_rows") == 172
        and anchor_result.get("anchored_package_clause_rows") == 172
        and anchor_result.get("source_anchor_groups") == len(anchor_sizes)
        and anchor_result.get("legitimate_shared_anchor_groups") == sum(size > 1 for size in anchor_sizes.values())
        and anchor_result.get("single_clause_anchor_groups") == sum(size == 1 for size in anchor_sizes.values())
        and anchor_result.get("semantic_premise_profiles") == len({r["semantic_premise_id"] for r in package_claims})
    )
    checks.append(("source_local_anchor_ranges_hashes_tokens_and_admission", not anchor_bad and anchor_counts_ok, f"bad={anchor_bad},groups={len(anchor_sizes)},semantic={len({r['semantic_premise_id'] for r in package_claims})}"))
    complete_bad = check_completeness(claims)
    checks.append(("all_ten_completeness_cells_and_action_content", not complete_bad, str(complete_bad)))
    checks.append(("regrades_and_k4_correction", Counter(r["regrade"] for r in claims) == Counter({"RETAINED": 32, "NARROWED": 148, "CONTRADICTED": 1, "OPEN": 1}) and sum("order-four K4 group itself does not embed" in r["replacement_sentence"] for r in claims) == 1, str(Counter(r["regrade"] for r in claims))))
    independence_bad = check_false_independence(recompute)
    checks.append(("recompute_status_and_independence_classes", len(recompute) == 21 and all(r["status"] == "PASS" for r in recompute) and not independence_bad and Counter(r["independence_label"] for r in recompute) == Counter({"GENUINELY_DIFFERENT_METHOD": 15, "INDEPENDENT_PARSER_OR_REGRESSION": 6}), str(independence_bad)))
    n_manifest, bad_manifest = source_manifest()
    checks.append(("frozen_source_manifest", n_manifest == 311 and not bad_manifest, f"rows={n_manifest},bad={bad_manifest}"))
    overlay_bad = check_overlay(overlay)
    checks.append(("nonretroactive_dependency_overlay", not overlay_bad, str(overlay_bad)))
    immutable_bad = check_immutable_second_verifier()
    checks.append(("immutable_second_verifier_artifacts_and_report_section", not immutable_bad, str(immutable_bad)))
    closure_immutable_bad = check_immutable_closure_verifier()
    checks.append(("immutable_closure_verifier_artifacts_and_report_section", not closure_immutable_bad, str(closure_immutable_bad)))
    changed = git_changed_paths()
    outside = check_outside(changed)
    checks.append(("no_edit_outside_package", not outside, str(outside)))
    base_ok = subprocess.run(["git", "merge-base", "--is-ancestor", "2e93a621aeeee0a0844543068363d0ba94094357", "HEAD"], cwd=ROOT).returncode == 0
    checks.append(("base_is_ancestor", base_ok, "2e93a621..."))
    checks.append(("stop_repair_first_preserved", results.get("smallest_next_step", "").startswith("STOP_REPAIR_FIRST"), results.get("smallest_next_step", "")))

    # Seven production-path catch-proofs.  Every mutation is in memory and is
    # passed to the same checker used above; no source or evidence byte is edited.
    missing_rows = [dict(r) for r in claims if r["unit_id"] != "P4-00"]
    checks.append(("catch_missing_unit", "P4-00" in check_units(missing_rows, required), "production unit-coverage checker"))
    duplicate_frozen = [dict(r) for r in frozen] + [dict(frozen[0])]
    checks.append(("catch_duplicate_frozen_unit", "P4-00" in check_frozen_units(duplicate_frozen), "production frozen-unit identity checker"))
    manifest_line = (OUT / "SOURCE_MANIFEST.sha256").read_text().splitlines()[0]
    _, rel = manifest_line.split("  ", 1)
    _, mutated_bad = source_manifest({rel: (OUT / rel).read_bytes() + b"synthetic production-manifest mutation"})
    checks.append(("catch_production_source_manifest_mutation", rel in mutated_bad, "production source_manifest override"))
    promoted_rows = [dict(r) for r in claims]
    promoted = next(r for r in promoted_rows if r["unit_id"] == "P4-02" and "shares no exact static equation sector" in r["source_clause"])
    promoted["replacement_sentence"] = "The action pair has no common solution in every domain."
    checks.append(("catch_concrete_quantifier_promotion", promoted["claim_id"] in check_quantifiers(promoted_rows), "equation-set inequivalence promoted to universal empty intersection"))
    parser_rows = [dict(r) for r in recompute]
    parser = next(r for r in parser_rows if r["record_id"] == "IR10")
    parser["independence_label"] = "GENUINELY_DIFFERENT_METHOD"
    checks.append(("catch_actual_parser_false_independence", "IR10" in check_false_independence(parser_rows), "IR10 parser mislabeled different-method"))
    incomplete_rows = [dict(r) for r in claims]
    incomplete_rows[0]["topology_covered_or_dropped"] = ""
    checks.append(("catch_missing_completeness_cell", incomplete_rows[0]["claim_id"] in check_completeness(incomplete_rows), "production ten-cell checker"))
    stamped_rows = [dict(r) for r in claims]
    stamped = next(r for r in stamped_rows if r["unit_kind"] == "PACKAGE_HEADLINE_CLAUSE")
    stamped["source_excerpt_sha256"] = "0" * 64
    checks.append(("catch_mutated_source_excerpt_hash", stamped["claim_id"] in check_source_anchors(stamped_rows, inventory_paths, overlay_paths), "production source-anchor checker"))
    token_rows = [dict(r) for r in claims]
    token_row = next(r for r in token_rows if r["unit_kind"] == "PACKAGE_HEADLINE_CLAUSE")
    token_row["source_anchor_token"] = "TBD_PACKAGE_TRIGGER_FALLBACK"
    checks.append(("catch_default_or_fallback_anchor_token", token_row["claim_id"] in check_source_anchors(token_rows, inventory_paths, overlay_paths), "production source-anchor checker"))
    semantic_rows = [dict(r) for r in claims]
    semantic = next(r for r in semantic_rows if r["unit_kind"] == "PACKAGE_HEADLINE_CLAUSE")
    semantic["premise_stack"] += "; TRIGGER_FALLBACK"
    checks.append(("catch_semantic_package_trigger_fallback", semantic["claim_id"] in check_semantic_premises(semantic_rows), "production semantic-premise checker"))

    for name, passed, detail in checks:
        print(json.dumps({"check": name, "status": "PASS" if passed else "FAIL", "detail": detail}, sort_keys=True))
    passed = sum(ok for _, ok, _ in checks)
    print(json.dumps({"summary": {"checks": len(checks), "passed": passed, "failed": len(checks) - passed}}, sort_keys=True))
    return 0 if passed == len(checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
