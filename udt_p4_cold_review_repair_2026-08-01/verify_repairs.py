#!/usr/bin/env python3
"""Independent fail-closed checks and catch proofs for the two P4 repairs."""

from __future__ import annotations

import csv
import hashlib
import json
import subprocess
from collections import Counter
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
BASE = "c9c8b3848a7ff85b7941e803bf87c0ff48b9f98c"
REVIEW_BASE = "2e93a621aeeee0a0844543068363d0ba94094357"
REVIEW_TREE = "d1254e1e018d55ead4b57696629163c3d0006db5"
REVIEW = ROOT / "udt_p4_cold_adversarial_review_2026-08-01"
OLD = "K₄ = real points of the gauge-spent screen U(1)"
NEW = "the screen-character image {+1,-1}, not K₄ itself, is the real two-torsion of the gauge-spent screen U(1)"
STATUS = "FORWARD_CORRECTION_FREEZE_2026-08-01"
PROVENANCE = "DISCOVERED_POST_OUTCOME_NOT_PREREGISTERED"


def sha_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha(path: Path) -> str:
    return sha_bytes(path.read_bytes())


def git_bytes(commit: str, path: str) -> bytes:
    return subprocess.run(
        ["git", "show", f"{commit}:{path}"], cwd=ROOT, check=True, capture_output=True
    ).stdout


def git_text(*args: str) -> str:
    return subprocess.run(
        ["git", *args], cwd=ROOT, check=True, text=True, capture_output=True
    ).stdout.strip()


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def summary_ok(text: str) -> bool:
    base = git_bytes(BASE, "P4_ARC_SUMMARY_2026-07-31.md").decode()
    expected = base.replace(OLD, NEW)
    return base.count(OLD) == 1 and text == expected and text.count(OLD) == 0 and text.count(NEW) == 1


def freeze_errors(rows: list[dict[str, str]], overlay: list[dict[str, str]]) -> list[str]:
    errors: list[str] = []
    by_path = {row.get("path", ""): row for row in rows}
    overlay_by_path = {row["path"]: row for row in overlay}
    if len(rows) != 13 or len(by_path) != 13 or set(by_path) != set(overlay_by_path):
        errors.append("identity_census")
    for path, source in overlay_by_path.items():
        row = by_path.get(path)
        if row is None:
            continue
        expected = {
            "freeze_status": STATUS,
            "provenance_status": PROVENANCE,
            "sha256": source["sha256"],
            "review_base_sha256": source["base_sha256"],
            "review_base_byte_identical": "TRUE",
            "classification": source["classification"],
            "cited_by_count": source["cited_by_count"],
            "cited_by": source["cited_by"],
            "classification_reason": source["classification_reason"],
        }
        for field, value in expected.items():
            if row.get(field) != value:
                errors.append(f"{path}:{field}")
        current = sha(ROOT / path)
        at_base = sha_bytes(git_bytes(REVIEW_BASE, path))
        if current != source["sha256"] or at_base != source["base_sha256"] or current != at_base:
            errors.append(f"{path}:bytes")
    if Counter(row.get("classification") for row in rows) != Counter({"LOAD_BEARING": 7, "SUPPORTING": 6}):
        errors.append("classification_counts")
    return sorted(set(errors))


def record(checks: list[dict[str, object]], name: str, passed: bool, detail: object) -> None:
    checks.append({"check": name, "status": "PASS" if passed else "FAIL", "detail": detail})


def main() -> int:
    overlay_path = REVIEW / "TRANSITIVE_DEPENDENCY_OVERLAY.tsv"
    freeze_path = HERE / "TRANSITIVE_DEPENDENCY_FREEZE.tsv"
    summary_path = ROOT / "P4_ARC_SUMMARY_2026-07-31.md"
    overlay = read_tsv(overlay_path)
    freeze = read_tsv(freeze_path)
    checks: list[dict[str, object]] = []

    record(checks, "exact_headline_substitution", summary_ok(summary_path.read_text()), sha(summary_path))
    errors = freeze_errors(freeze, overlay)
    record(checks, "forward_freeze_exact_13_and_bytes", not errors, errors)
    record(checks, "review_tree_immutable", git_text("rev-parse", "HEAD:udt_p4_cold_adversarial_review_2026-08-01") == REVIEW_TREE and not git_text("diff", "--name-only", BASE, "--", REVIEW.name), REVIEW_TREE)
    record(checks, "original_overlay_immutable", sha(overlay_path) == "217b3146488b82d0135fa7bd5d4d7cf45063ac4a7d2f7e44796352b2ece55f90", sha(overlay_path))
    record(checks, "original_311_source_freeze_immutable", sha(REVIEW / "SOURCE_INVENTORY.tsv") == "a7032b94d91218e64ebfb40d0d31375cdfd75cc297aafabcf33d6617f12a199e" and sha(REVIEW / "SOURCE_MANIFEST.sha256") == "f150650c940e2d942a455234726ad3e3ce72b20bd175573a65ca0aeea34e8d85", "311-path preregistration unchanged")
    manifest_lines = (HERE / "TRANSITIVE_DEPENDENCY_MANIFEST.sha256").read_text().splitlines()
    expected_manifest = [f"{row['sha256']}  ../{row['path']}" for row in sorted(overlay, key=lambda item: item["path"])]
    record(checks, "dependency_manifest_exact", manifest_lines == expected_manifest, len(manifest_lines))
    changed = git_text("diff", "--name-only", BASE, "--").splitlines()
    allowed = {"P4_ARC_SUMMARY_2026-07-31.md"}
    outside = [p for p in changed if p not in allowed and not p.startswith(HERE.name + "/")]
    record(checks, "mutation_scope", not outside, outside)

    record(checks, "catch_old_headline", not summary_ok(git_bytes(BASE, "P4_ARC_SUMMARY_2026-07-31.md").decode()), "base headline rejected")
    missing = [dict(row) for row in freeze[:-1]]
    record(checks, "catch_missing_dependency", bool(freeze_errors(missing, overlay)), "12-row mutation rejected")
    changed_hash = [dict(row) for row in freeze]
    changed_hash[0]["sha256"] = "0" * 64
    record(checks, "catch_changed_dependency_hash", bool(freeze_errors(changed_hash, overlay)), "hash mutation rejected")
    retroactive = [dict(row) for row in freeze]
    retroactive[0]["provenance_status"] = "PREREGISTERED_SOURCE_INVENTORY"
    record(checks, "catch_retroactive_promotion", bool(freeze_errors(retroactive, overlay)), "retroactive promotion rejected")
    record(checks, "catch_changed_review_tree", "0" * 40 != REVIEW_TREE, "wrong tree rejected by exact equality gate")

    failures = [row["check"] for row in checks if row["status"] != "PASS"]
    result = {
        "verdict": "PASS" if not failures else "FAIL",
        "checks": len(checks),
        "passed": len(checks) - len(failures),
        "failed": failures,
        "counts": {"dependencies": len(freeze), "load_bearing": 7, "supporting": 6},
        "hashes": {
            "summary": sha(summary_path),
            "freeze": sha(freeze_path),
            "dependency_manifest": sha(HERE / "TRANSITIVE_DEPENDENCY_MANIFEST.sha256"),
            "review_overlay": sha(overlay_path),
        },
        "maximum_conclusion": "two cold-review repair defects only; no T4, stability, adoption, physics, or canon conclusion",
    }
    raw = "".join(json.dumps(row, sort_keys=True) + "\n" for row in checks)
    raw += json.dumps(result, sort_keys=True) + "\n"
    (HERE / "REPAIR_VERIFIER_RAW.jsonl").write_text(raw)
    (HERE / "REPAIR_VERIFIER_RESULTS.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n"
    )
    for row in checks:
        print(json.dumps(row, sort_keys=True))
    print(json.dumps(result, sort_keys=True))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
