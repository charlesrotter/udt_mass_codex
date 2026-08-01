#!/usr/bin/env python3
"""Same-second-verifier closure for the amended P4 cold-review repair."""

from __future__ import annotations

import ast
import csv
import hashlib
import json
import os
import re
import subprocess
from collections import Counter
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
BASE = "c9c8b3848a7ff85b7941e803bf87c0ff48b9f98c"
REVIEW_BASE = "2e93a621aeeee0a0844543068363d0ba94094357"
REVIEW_TREE = "d1254e1e018d55ead4b57696629163c3d0006db5"
REVIEW = ROOT / "udt_p4_cold_adversarial_review_2026-08-01"
SUMMARY_REL = "P4_ARC_SUMMARY_2026-07-31.md"
SUMMARY = ROOT / SUMMARY_REL
OLD = "K₄ = real points of the gauge-spent screen U(1)"
NEW = "the screen-character image {+1,-1}, not K₄ itself, is the real two-torsion of the gauge-spent screen U(1)"
FORWARD = "FORWARD_CORRECTION_FREEZE_2026-08-01"
POST_OUTCOME = "DISCOVERED_POST_OUTCOME_NOT_PREREGISTERED"
OVERLAY_HASH = "217b3146488b82d0135fa7bd5d4d7cf45063ac4a7d2f7e44796352b2ece55f90"
INVENTORY_HASH = "a7032b94d91218e64ebfb40d0d31375cdfd75cc297aafabcf33d6617f12a199e"
SOURCE_MANIFEST_HASH = "f150650c940e2d942a455234726ad3e3ce72b20bd175573a65ca0aeea34e8d85"
RAW_PATH = HERE / "CLOSURE_VERIFIER_RAW.jsonl"
RESULTS_PATH = HERE / "CLOSURE_VERIFIER_RESULTS.json"

checks: list[dict[str, object]] = []
failures: list[str] = []


def sha_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha(path: Path) -> str:
    return sha_bytes(path.read_bytes())


def git_bytes(commit: str, path: str) -> bytes:
    proc = subprocess.run(
        ["git", "show", f"{commit}:{path}"], cwd=ROOT, capture_output=True, check=False
    )
    if proc.returncode:
        raise RuntimeError(proc.stderr.decode(errors="replace"))
    return proc.stdout


def git_text(*args: str) -> str:
    proc = subprocess.run(["git", *args], cwd=ROOT, text=True, capture_output=True, check=False)
    if proc.returncode:
        raise RuntimeError(proc.stderr)
    return proc.stdout.strip()


def git_status() -> list[str]:
    proc = subprocess.run(
        ["git", "status", "--porcelain=v1"], cwd=ROOT, text=True, capture_output=True, check=False
    )
    if proc.returncode:
        raise RuntimeError(proc.stderr)
    return proc.stdout.splitlines()


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def record(name: str, ok: bool, **detail: object) -> None:
    checks.append({"check": name, "status": "PASS" if ok else "FAIL", **detail})
    if not ok:
        failures.append(name)


def validate_manifest(path: Path, relative_to: Path) -> tuple[int, list[str]]:
    bad: list[str] = []
    count = 0
    for line in path.read_text().splitlines():
        if not line.strip():
            continue
        count += 1
        expected, rel = line.split("  ", 1)
        target = (relative_to / rel).resolve()
        if not target.is_file() or sha(target) != expected:
            bad.append(rel)
    return count, bad


def freeze_errors(
    freeze: list[dict[str, str]], overlay: list[dict[str, str]], verify_bytes: bool = True
) -> list[str]:
    bad: list[str] = []
    rows = {row.get("path", ""): row for row in freeze}
    source = {row["path"]: row for row in overlay}
    if len(freeze) != 13 or len(rows) != 13 or set(rows) != set(source):
        bad.append("identity_census")
    for path, overlay_row in source.items():
        row = rows.get(path)
        if row is None:
            continue
        expected = {
            "freeze_date": "2026-08-01",
            "freeze_status": FORWARD,
            "provenance_status": POST_OUTCOME,
            "sha256": overlay_row["sha256"],
            "review_base_sha256": overlay_row["base_sha256"],
            "review_base_byte_identical": overlay_row["base_byte_identical"],
            "classification": overlay_row["classification"],
            "cited_by_count": overlay_row["cited_by_count"],
            "cited_by": overlay_row["cited_by"],
            "classification_reason": overlay_row["classification_reason"],
        }
        for field, value in expected.items():
            if row.get(field) != value:
                bad.append(f"{path}:{field}")
        if verify_bytes:
            current = sha(ROOT / path)
            review_base = sha_bytes(git_bytes(REVIEW_BASE, path))
            if not current == review_base == row["sha256"] == row["review_base_sha256"]:
                bad.append(f"{path}:bytes")
    if Counter(row["classification"] for row in freeze) != Counter(
        {"LOAD_BEARING": 7, "SUPPORTING": 6}
    ):
        bad.append("classification_counts")
    return sorted(set(bad))


def same_tree_predicate(candidate_tree: str, changed_paths: list[str]) -> bool:
    return candidate_tree == REVIEW_TREE and not changed_paths


def validate_source_manifest_at_review_base() -> tuple[int, list[str]]:
    bad: list[str] = []
    count = 0
    for line in (REVIEW / "SOURCE_MANIFEST.sha256").read_text().splitlines():
        if not line.strip():
            continue
        count += 1
        expected, rel = line.split("  ", 1)
        repo_path = str((REVIEW / rel).resolve().relative_to(ROOT.resolve()))
        if sha_bytes(git_bytes(REVIEW_BASE, repo_path)) != expected:
            bad.append(rel)
    return count, bad


def main() -> None:
    overlay = read_tsv(REVIEW / "TRANSITIVE_DEPENDENCY_OVERLAY.tsv")
    freeze = read_tsv(HERE / "TRANSITIVE_DEPENDENCY_FREEZE.tsv")

    amended_source = (HERE / "verify_repairs_amended.py").read_text()
    tree = ast.parse(amended_source)
    functions = {
        node.name: node for node in tree.body if isinstance(node, ast.FunctionDef)
    }
    predicate = functions.get("review_tree_ok")
    predicate_return = next(
        (node for node in predicate.body if isinstance(node, ast.Return)), None
    ) if predicate else None
    predicate_body = ast.unparse(predicate_return.value) if predicate_return else ""
    calls = [
        node
        for node in ast.walk(tree)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
        and node.func.id == "review_tree_ok"
    ]
    call_args = [[ast.unparse(arg) for arg in call.args] for call in calls]
    actual_tree = git_text("rev-parse", f"HEAD:{REVIEW.name}")
    changed_review_paths = git_text(
        "diff", "--name-only", BASE, "--", REVIEW.name
    ).splitlines()
    review_status = git_text("status", "--porcelain=v1", "--", REVIEW.name).splitlines()
    wrong_tree = "0" * 40
    record(
        "shared_review_tree_predicate_actual_and_mutation",
        predicate_body
        in {
            "candidate_tree == REVIEW_TREE and not changed_review_paths",
            "candidate_tree == REVIEW_TREE and (not changed_review_paths)",
        }
        and ["actual_tree", "changed_review_paths"] in call_args
        and ["wrong_tree", "[]"] in call_args
        and same_tree_predicate(actual_tree, changed_review_paths)
        and not same_tree_predicate(wrong_tree, [])
        and not review_status,
        predicate_body=predicate_body,
        call_arguments=call_args,
        actual_tree=actual_tree,
        changed_review_paths=changed_review_paths,
        review_status=review_status,
        wrong_tree=wrong_tree,
        wrong_tree_rejected=not same_tree_predicate(wrong_tree, []),
    )

    amended_raw = [
        json.loads(line)
        for line in (HERE / "AMENDED_REPAIR_VERIFIER_RAW.jsonl").read_text().splitlines()
    ]
    amended_checks = [row for row in amended_raw if "check" in row]
    amended_summary = amended_raw[-1]
    tree_production = next(
        (row for row in amended_checks if row["check"] == "review_tree_immutable"), {}
    )
    tree_catch = next(
        (row for row in amended_checks if row["check"] == "catch_changed_review_tree"), {}
    )
    record(
        "amended_emissions_12_of_12_and_real_tree_catch",
        len(amended_checks) == 12
        and all(row["status"] == "PASS" for row in amended_checks)
        and amended_summary.get("checks") == amended_summary.get("passed") == 12
        and amended_summary.get("failed") == []
        and tree_production.get("detail")
        == {"tree": actual_tree, "changed_paths": changed_review_paths}
        and tree_catch.get("detail")
        == {
            "candidate_tree": wrong_tree,
            "production_predicate": "review_tree_ok",
            "rejected": True,
        },
        saved_checks=len(amended_checks),
        saved_summary=amended_summary,
        production_tree_record=tree_production,
        mutation_tree_record=tree_catch,
    )

    base_text = git_bytes(BASE, SUMMARY_REL).decode()
    current_text = SUMMARY.read_text()
    record(
        "exact_headline_repair_unchanged",
        base_text.count(OLD) == 1
        and base_text.count(NEW) == 0
        and current_text == base_text.replace(OLD, NEW)
        and current_text.count(OLD) == 0
        and current_text.count(NEW) == 1,
        base_sha256=sha_bytes(base_text.encode()),
        current_sha256=sha(SUMMARY),
    )

    freeze_bad = freeze_errors(freeze, overlay)
    dep_count, dep_bad = validate_manifest(
        HERE / "TRANSITIVE_DEPENDENCY_MANIFEST.sha256", HERE
    )
    record(
        "dependency_freeze_13_7_plus_6_bytes_unchanged",
        len(freeze) == 13 and not freeze_bad and dep_count == 13 and not dep_bad,
        rows=len(freeze),
        classifications=dict(Counter(row["classification"] for row in freeze)),
        errors=freeze_bad,
        manifest_rows=dep_count,
        manifest_bad=dep_bad,
        freeze_sha256=sha(HERE / "TRANSITIVE_DEPENDENCY_FREEZE.tsv"),
        dependency_manifest_sha256=sha(HERE / "TRANSITIVE_DEPENDENCY_MANIFEST.sha256"),
    )

    source_count, source_bad = validate_source_manifest_at_review_base()
    inventory_sha = sha(REVIEW / "SOURCE_INVENTORY.tsv")
    source_manifest_sha = sha(REVIEW / "SOURCE_MANIFEST.sha256")
    record(
        "review_tree_and_original_311_freeze_unchanged",
        actual_tree == REVIEW_TREE
        and not changed_review_paths
        and not review_status
        and inventory_sha == INVENTORY_HASH
        and source_manifest_sha == SOURCE_MANIFEST_HASH
        and source_count == 311
        and not source_bad,
        review_tree=actual_tree,
        inventory_sha256=inventory_sha,
        source_manifest_sha256=source_manifest_sha,
        source_rows=source_count,
        source_bad=source_bad,
    )

    manifest_results: dict[str, object] = {}
    all_manifests_ok = True
    for name in (
        "REPAIR_MANIFEST.sha256",
        "SECOND_VERIFIER_MANIFEST.sha256",
        "AMENDED_REPAIR_MANIFEST.sha256",
        "TRANSITIVE_DEPENDENCY_MANIFEST.sha256",
    ):
        count, bad = validate_manifest(HERE / name, HERE)
        manifest_results[name] = {
            "rows": count,
            "bad": bad,
            "sha256": sha(HERE / name),
        }
        all_manifests_ok = all_manifests_ok and not bad
    record(
        "all_four_preclosure_manifests_valid_and_prior_records_preserved",
        all_manifests_ok,
        manifests=manifest_results,
    )

    # Exercise all five mutations independently.  The fifth uses the same
    # predicate already proven to receive the actual production inputs above.
    expected_summary = base_text.replace(OLD, NEW)
    old_headline_caught = git_bytes(BASE, SUMMARY_REL).decode() != expected_summary
    missing_caught = bool(freeze_errors([dict(row) for row in freeze[:-1]], overlay, False))
    changed_hash = [dict(row) for row in freeze]
    changed_hash[0]["sha256"] = "0" * 64
    changed_hash_caught = bool(freeze_errors(changed_hash, overlay, False))
    retroactive = [dict(row) for row in freeze]
    retroactive[0]["provenance_status"] = "PREREGISTERED_SOURCE_INVENTORY"
    retroactive_caught = bool(freeze_errors(retroactive, overlay, False))
    wrong_tree_caught = not same_tree_predicate(wrong_tree, [])
    record(
        "all_five_catch_proofs_genuine",
        all(
            (
                old_headline_caught,
                missing_caught,
                changed_hash_caught,
                retroactive_caught,
                wrong_tree_caught,
            )
        ),
        old_headline=old_headline_caught,
        missing_dependency=missing_caught,
        changed_dependency_hash=changed_hash_caught,
        retroactive_promotion=retroactive_caught,
        changed_review_tree=wrong_tree_caught,
    )

    status = git_status()
    status_paths: list[str] = []
    outside: list[str] = []
    for line in status:
        path = line[3:].split(" -> ")[-1]
        status_paths.append(path)
        if path != SUMMARY_REL and not path.startswith(HERE.name + "/"):
            outside.append(path)
    diff_paths = git_text("diff", "--name-only", BASE, "--").splitlines()
    diff_outside = [
        path
        for path in diff_paths
        if path != SUMMARY_REL and not path.startswith(HERE.name + "/")
    ]
    record(
        "authorized_path_scope_only",
        not outside and not diff_outside,
        status_paths=status_paths,
        outside=outside,
        diff_paths=diff_paths,
        diff_outside=diff_outside,
    )

    amendment = (HERE / "PRIMARY_AMENDMENT.md").read_text()
    record(
        "nonretroactive_ceiling_and_no_new_science",
        re.search(
            r"without changing the\s+headline, dependency freeze, review evidence, or any scientific result",
            amendment,
        )
        and re.search(
            r"authorizes no T4, stability work, adoption, physics, canonization, GPU work, navigation edit",
            amendment,
        )
        and all(row["provenance_status"] == POST_OUTCOME for row in freeze),
        provenance_counts=dict(Counter(row["provenance_status"] for row in freeze)),
    )

    env = dict(os.environ)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    premise = subprocess.run(
        ["python3", "verify_current_scientific_premises.py"],
        cwd=ROOT,
        env=env,
        text=True,
        capture_output=True,
        check=False,
    )
    tests = subprocess.run(
        ["pytest", "-q", "-p", "no:cacheprovider"],
        cwd=ROOT,
        env=env,
        text=True,
        capture_output=True,
        check=False,
    )
    record(
        "premise_gates_and_tests",
        premise.returncode == 0
        and "PASS: 18 premise guards, 9 startup controls, 754 candidate dispositions"
        in premise.stdout
        and tests.returncode == 0
        and "70 passed, 1 xfailed" in tests.stdout,
        premise_returncode=premise.returncode,
        premise_stdout=premise.stdout,
        premise_stderr=premise.stderr,
        test_returncode=tests.returncode,
        test_stdout=tests.stdout,
        test_stderr=tests.stderr,
    )

    post_status = git_status()
    post_outside: list[str] = []
    for line in post_status:
        path = line[3:].split(" -> ")[-1]
        if path != SUMMARY_REL and not path.startswith(HERE.name + "/"):
            post_outside.append(path)
    record(
        "no_outside_mutations_after_closure_checks",
        not post_outside,
        status=post_status,
        outside=post_outside,
    )

    verdict = "CLOSED-PASS" if not failures else "FURTHER-AMENDMENT"
    result = {
        "verdict": verdict,
        "checks": len(checks),
        "passed": len(checks) - len(failures),
        "failed": failures,
        "counts": {
            "amended_primary_checks": len(amended_checks),
            "genuine_catches": 5,
            "dependencies": len(freeze),
            "load_bearing": Counter(row["classification"] for row in freeze)["LOAD_BEARING"],
            "supporting": Counter(row["classification"] for row in freeze)["SUPPORTING"],
            "source_manifest_rows": source_count,
            "tests_passed": 70,
            "tests_xfailed": 1,
        },
        "hashes": {
            "amended_verifier": sha(HERE / "verify_repairs_amended.py"),
            "amended_raw": sha(HERE / "AMENDED_REPAIR_VERIFIER_RAW.jsonl"),
            "amended_results": sha(HERE / "AMENDED_REPAIR_VERIFIER_RESULTS.json"),
            "amended_manifest": sha(HERE / "AMENDED_REPAIR_MANIFEST.sha256"),
            "summary": sha(SUMMARY),
            "freeze": sha(HERE / "TRANSITIVE_DEPENDENCY_FREEZE.tsv"),
            "dependency_manifest": sha(HERE / "TRANSITIVE_DEPENDENCY_MANIFEST.sha256"),
            "review_tree": actual_tree,
            "source_inventory": inventory_sha,
            "source_manifest": source_manifest_sha,
        },
        "maximum_conclusion": (
            "the two preregistered cold-review presentation/provenance repairs are second-verifier closed; "
            "no T4, stability, science, GPU, adoption, navigation, git, physics, or canon conclusion"
        ),
    }
    RAW_PATH.write_text("".join(json.dumps(row, sort_keys=True) + "\n" for row in checks))
    RESULTS_PATH.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))
    raise SystemExit(0 if not failures else 1)


if __name__ == "__main__":
    main()
