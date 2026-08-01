#!/usr/bin/env python3
"""Independent same-verifier audit of the forward P4 cold-review repairs."""

from __future__ import annotations

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
PREREG = "9089c0fcfd3bd8cfaa0121afb42d343593d7bca6"
BASE = "c9c8b3848a7ff85b7941e803bf87c0ff48b9f98c"
REVIEW_BASE = "2e93a621aeeee0a0844543068363d0ba94094357"
REVIEW_TREE = "d1254e1e018d55ead4b57696629163c3d0006db5"
REVIEW = ROOT / "udt_p4_cold_adversarial_review_2026-08-01"
SUMMARY_REL = "P4_ARC_SUMMARY_2026-07-31.md"
SUMMARY = ROOT / SUMMARY_REL
OLD = "K₄ = real points of the gauge-spent screen U(1)"
NEW = "the screen-character image {+1,-1}, not K₄ itself, is the real two-torsion of the gauge-spent screen U(1)"
OVERLAY_HASH = "217b3146488b82d0135fa7bd5d4d7cf45063ac4a7d2f7e44796352b2ece55f90"
INVENTORY_HASH = "a7032b94d91218e64ebfb40d0d31375cdfd75cc297aafabcf33d6617f12a199e"
SOURCE_MANIFEST_HASH = "f150650c940e2d942a455234726ad3e3ce72b20bd175573a65ca0aeea34e8d85"
FORWARD = "FORWARD_CORRECTION_FREEZE_2026-08-01"
POST_OUTCOME = "DISCOVERED_POST_OUTCOME_NOT_PREREGISTERED"
RAW_PATH = HERE / "SECOND_VERIFIER_RAW.jsonl"
RESULTS_PATH = HERE / "SECOND_VERIFIER_RESULTS.json"

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
        ["git", "status", "--porcelain=v1"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
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


def validate_sha_manifest(path: Path, relative_to: Path) -> tuple[int, list[str]]:
    bad: list[str] = []
    count = 0
    for line in path.read_text().splitlines():
        if not line.strip():
            continue
        count += 1
        digest, rel = line.split("  ", 1)
        target = (relative_to / rel).resolve()
        if not target.is_file() or sha(target) != digest:
            bad.append(rel)
    return count, bad


def validate_source_manifest_at_review_base() -> tuple[int, list[str]]:
    bad: list[str] = []
    count = 0
    for line in (REVIEW / "SOURCE_MANIFEST.sha256").read_text().splitlines():
        if not line.strip():
            continue
        count += 1
        expected, rel = line.split("  ", 1)
        root_relative = str((Path(REVIEW.name) / rel).resolve()).split(str(ROOT.resolve()) + "/", 1)[-1]
        # SOURCE_MANIFEST paths are relative to the review package and normally
        # begin with ../, so normalize them to repository-relative paths.
        root_relative = str((REVIEW / rel).resolve().relative_to(ROOT.resolve()))
        if sha_bytes(git_bytes(REVIEW_BASE, root_relative)) != expected:
            bad.append(rel)
    return count, bad


def freeze_errors(
    rows: list[dict[str, str]], overlay: list[dict[str, str]], verify_bytes: bool = True
) -> list[str]:
    bad: list[str] = []
    by_path = {row.get("path", ""): row for row in rows}
    source = {row["path"]: row for row in overlay}
    if len(rows) != len(by_path) or set(by_path) != set(source):
        bad.append("identity_census")
    for path, overlay_row in source.items():
        row = by_path.get(path)
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
            at_review_base = sha_bytes(git_bytes(REVIEW_BASE, path))
            if not (
                current
                == at_review_base
                == row["sha256"]
                == row["review_base_sha256"]
            ):
                bad.append(f"{path}:bytes")
    if Counter(row.get("classification") for row in rows) != Counter(
        {"LOAD_BEARING": 7, "SUPPORTING": 6}
    ):
        bad.append("classification_counts")
    return sorted(set(bad))


def main() -> None:
    overlay = read_tsv(REVIEW / "TRANSITIVE_DEPENDENCY_OVERLAY.tsv")
    freeze = read_tsv(HERE / "TRANSITIVE_DEPENDENCY_FREEZE.tsv")

    # The preregistration commit contains only the repair contract and retains
    # the unmodified target bytes; the mutations are forward worktree changes.
    head = git_text("rev-parse", "HEAD")
    parent = git_text("rev-parse", f"{PREREG}^")
    commit_paths = git_text("diff-tree", "--no-commit-id", "--name-only", "-r", PREREG).splitlines()
    expected_prereg_paths = {
        f"{HERE.name}/PREREGISTRATION.md",
        f"{HERE.name}/PREREG_SNAPSHOT.json",
        f"{HERE.name}/REPAIR_SCOPE.tsv",
        f"{HERE.name}/verify_preregistration.py",
    }
    base_summary = git_bytes(BASE, SUMMARY_REL)
    prereg_summary = git_bytes(PREREG, SUMMARY_REL)
    record(
        "preregistration_commit_precedes_mutation",
        head == PREREG
        and parent == BASE
        and set(commit_paths) == expected_prereg_paths
        and prereg_summary == base_summary
        and SUMMARY.read_bytes() != prereg_summary,
        head=head,
        parent=parent,
        commit_paths=commit_paths,
        prereg_summary_sha256=sha_bytes(prereg_summary),
        current_summary_sha256=sha(SUMMARY),
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
        "mutation_scope_summary_plus_repair_package_only",
        not outside and not diff_outside,
        status_paths=status_paths,
        outside=outside,
        diff_paths=diff_paths,
        diff_outside=diff_outside,
    )

    base_text = base_summary.decode()
    current_text = SUMMARY.read_text()
    expected_summary = base_text.replace(OLD, NEW)
    record(
        "summary_exact_single_phrase_replacement",
        base_text.count(OLD) == 1
        and base_text.count(NEW) == 0
        and current_text == expected_summary
        and current_text.count(OLD) == 0
        and current_text.count(NEW) == 1,
        base_sha256=sha_bytes(base_summary),
        current_sha256=sha(SUMMARY),
        old_count_base=base_text.count(OLD),
        old_count_current=current_text.count(OLD),
        new_count_current=current_text.count(NEW),
    )

    freeze_bad = freeze_errors(freeze, overlay)
    freeze_manifest_count, freeze_manifest_bad = validate_sha_manifest(
        HERE / "TRANSITIVE_DEPENDENCY_MANIFEST.sha256", HERE
    )
    record(
        "forward_freeze_13_exact_fields_current_and_review_base_bytes",
        len(freeze) == 13
        and not freeze_bad
        and freeze_manifest_count == 13
        and not freeze_manifest_bad,
        rows=len(freeze),
        classifications=dict(Counter(row["classification"] for row in freeze)),
        errors=freeze_bad,
        manifest_rows=freeze_manifest_count,
        manifest_bad=freeze_manifest_bad,
        freeze_sha256=sha(HERE / "TRANSITIVE_DEPENDENCY_FREEZE.tsv"),
        dependency_manifest_sha256=sha(HERE / "TRANSITIVE_DEPENDENCY_MANIFEST.sha256"),
    )

    repair_text = "\n".join(
        (HERE / name).read_text()
        for name in ("REPAIR_REPORT.md", "REPAIR_RESULTS.json", "TRANSITIVE_DEPENDENCY_FREEZE.tsv")
    )
    retro_bad = [
        row["path"]
        for row in freeze
        if row["provenance_status"] != POST_OUTCOME
        or row["freeze_status"] != FORWARD
        or row["review_base_byte_identical"] != "TRUE"
    ]
    record(
        "nonretroactive_provenance_explicit",
        not retro_bad
        and "DISCOVERED_POST_OUTCOME_NOT_PREREGISTERED" in repair_text
        and re.search(r"does not rewrite the original 311-path\s+preregistration", repair_text)
        and "PREREGISTERED_SOURCE_INVENTORY" not in (HERE / "TRANSITIVE_DEPENDENCY_FREEZE.tsv").read_text(),
        bad=retro_bad,
    )

    review_tree_head = git_text("rev-parse", f"HEAD:{REVIEW.name}")
    review_tree_base = git_text("rev-parse", f"{BASE}:{REVIEW.name}")
    review_status = git_text("status", "--porcelain=v1", "--", REVIEW.name).splitlines()
    inventory_sha = sha(REVIEW / "SOURCE_INVENTORY.tsv")
    source_manifest_sha = sha(REVIEW / "SOURCE_MANIFEST.sha256")
    source_manifest_count, source_manifest_bad = validate_source_manifest_at_review_base()
    record(
        "cold_review_tree_and_original_311_freeze_immutable",
        review_tree_head == review_tree_base == REVIEW_TREE
        and not review_status
        and inventory_sha == INVENTORY_HASH
        and source_manifest_sha == SOURCE_MANIFEST_HASH
        and source_manifest_count == 311
        and not source_manifest_bad,
        head_tree=review_tree_head,
        base_tree=review_tree_base,
        review_status=review_status,
        inventory_sha256=inventory_sha,
        source_manifest_sha256=source_manifest_sha,
        source_manifest_rows=source_manifest_count,
        source_manifest_bad=source_manifest_bad,
    )

    overlay_sha = sha(REVIEW / "TRANSITIVE_DEPENDENCY_OVERLAY.tsv")
    record(
        "original_overlay_immutable",
        overlay_sha == OVERLAY_HASH
        and len(overlay) == 13
        and Counter(row["classification"] for row in overlay)
        == Counter({"LOAD_BEARING": 7, "SUPPORTING": 6})
        and all(
            row["overlay_status"] == "NON_RETROACTIVE_POST_OUTCOME_DEPENDENCY_RECORD"
            for row in overlay
        ),
        overlay_sha256=overlay_sha,
    )

    primary_manifest_count, primary_manifest_bad = validate_sha_manifest(
        HERE / "REPAIR_MANIFEST.sha256", HERE
    )
    primary_raw = [
        json.loads(line) for line in (HERE / "REPAIR_VERIFIER_RAW.jsonl").read_text().splitlines()
    ]
    primary_checks = [row for row in primary_raw if "check" in row]
    primary_summary = primary_raw[-1]
    record(
        "primary_records_12_pass_and_manifest_current",
        primary_manifest_count == 12
        and not primary_manifest_bad
        and len(primary_checks) == 12
        and all(row["status"] == "PASS" for row in primary_checks)
        and primary_summary.get("checks") == primary_summary.get("passed") == 12
        and primary_summary.get("failed") == [],
        manifest_rows=primary_manifest_count,
        manifest_bad=primary_manifest_bad,
        saved_checks=len(primary_checks),
        saved_summary=primary_summary,
    )

    # Independently exercise the first four primary mutations through the same
    # predicates.  These four are real and fail as intended.
    old_headline_caught = not (
        git_bytes(BASE, SUMMARY_REL).decode() == expected_summary
    )
    missing_caught = bool(freeze_errors([dict(row) for row in freeze[:-1]], overlay, False))
    changed_hash = [dict(row) for row in freeze]
    changed_hash[0]["sha256"] = "0" * 64
    changed_hash_caught = bool(freeze_errors(changed_hash, overlay, False))
    retroactive = [dict(row) for row in freeze]
    retroactive[0]["provenance_status"] = "PREREGISTERED_SOURCE_INVENTORY"
    retroactive_caught = bool(freeze_errors(retroactive, overlay, False))
    record(
        "primary_first_four_catch_proofs_real",
        old_headline_caught and missing_caught and changed_hash_caught and retroactive_caught,
        old_headline=old_headline_caught,
        missing_dependency=missing_caught,
        changed_hash=changed_hash_caught,
        retroactive_promotion=retroactive_caught,
    )

    verifier_source = (HERE / "verify_repairs.py").read_text()
    tautology = 'record(checks, "catch_changed_review_tree", "0" * 40 != REVIEW_TREE' in verifier_source
    has_candidate_gate = bool(
        re.search(r"def\s+review_tree_ok\s*\(", verifier_source)
        or re.search(r"catch_changed_review_tree.*(?:git_text|rev-parse|candidate)", verifier_source)
    )
    independent_wrong_tree_rejected = ("0" * 40) != review_tree_head
    record(
        "primary_changed_review_tree_catch_is_genuine",
        not tautology and has_candidate_gate,
        tautological_constant_comparison_found=tautology,
        production_candidate_gate_found=has_candidate_gate,
        independent_wrong_tree_would_be_rejected=independent_wrong_tree_rejected,
        source_expression='record(..., "0" * 40 != REVIEW_TREE, ...)',
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
        "premise_gates_and_test_baseline",
        premise.returncode == 0
        and "PASS: 18 premise guards, 9 startup controls, 754 candidate dispositions" in premise.stdout
        and tests.returncode == 0
        and "70 passed, 1 xfailed" in tests.stdout,
        premise_returncode=premise.returncode,
        premise_stdout=premise.stdout,
        premise_stderr=premise.stderr,
        tests_returncode=tests.returncode,
        tests_stdout=tests.stdout,
        tests_stderr=tests.stderr,
    )

    post_status = git_status()
    post_outside = []
    for line in post_status:
        path = line[3:].split(" -> ")[-1]
        if path != SUMMARY_REL and not path.startswith(HERE.name + "/"):
            post_outside.append(path)
    record(
        "no_outside_mutations_after_checks",
        not post_outside,
        status=post_status,
        outside=post_outside,
    )

    verdict = "CLOSED-PASS" if not failures else "AMENDMENT-REQUIRED"
    result = {
        "verdict": verdict,
        "checks": len(checks),
        "passed": len(checks) - len(failures),
        "failed": failures,
        "preregistration_commit": PREREG,
        "base": BASE,
        "counts": {
            "dependencies": len(freeze),
            "load_bearing": Counter(row["classification"] for row in freeze)["LOAD_BEARING"],
            "supporting": Counter(row["classification"] for row in freeze)["SUPPORTING"],
            "primary_checks_saved_pass": len(primary_checks),
            "primary_catches_genuine": 4,
            "primary_catches_tautological": 1,
            "tests_passed": 70,
            "tests_xfailed": 1,
        },
        "hashes": {
            "summary": sha(SUMMARY),
            "freeze": sha(HERE / "TRANSITIVE_DEPENDENCY_FREEZE.tsv"),
            "dependency_manifest": sha(HERE / "TRANSITIVE_DEPENDENCY_MANIFEST.sha256"),
            "review_overlay": overlay_sha,
            "cold_review_tree": review_tree_head,
            "source_inventory": inventory_sha,
            "source_manifest": source_manifest_sha,
            "primary_repair_manifest": sha(HERE / "REPAIR_MANIFEST.sha256"),
        },
        "required_amendment": (
            "Replace the constant '0'*40 != REVIEW_TREE assertion with an in-memory changed-tree "
            "candidate passed through the same exact tree-equality predicate used by the production gate; "
            "rerun the primary verifier and rebuild its manifest without changing the two repair outputs."
        ),
        "maximum_conclusion": (
            "repair data match the preregistered contract, but primary catch-proof closure is incomplete; "
            "no T4, stability, adoption, physics, GPU, navigation, git, or canon conclusion"
        ),
    }
    RAW_PATH.write_text("".join(json.dumps(row, sort_keys=True) + "\n" for row in checks))
    RESULTS_PATH.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))
    raise SystemExit(0 if not failures else 1)


if __name__ == "__main__":
    main()
