#!/usr/bin/env python3
"""Deterministic fixed-base discovery for the general-screen dependency regrade."""

from __future__ import annotations

import csv
import hashlib
import json
import re
import subprocess
from collections import Counter
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
BASE = "e098338b2a24cc85796ea8ab651378925b825dfb"
TREE = "5ba94fc3115729a1f0a2e486027a8b94959e148c"
TEXT_SUFFIXES = {".md", ".tsv", ".json", ".txt"}
EXCLUDED_PREFIXES = (
    "archive/", "reorganization_", "native_action_stage1_2026-07-18/",
    "native_action_stage2_2026-07-18/", "native_action_arm_c_2026-07-18/",
    "native_action_final_adjudication_2026-07-18/",
    "udt_general_screen_dependency_regrade_2026-07-28/",
)
PRIMARY_NAMES = {
    "STATUS_LEDGER.tsv", "AUDIT_REPORT.md", "CORRECTION_LAYER.md", "FINAL_STATUS_LEDGER.tsv",
    "NEXT_STEP.md", "DERIVATION_RESULT.json", "CURRENT_SCIENTIFIC_PREMISES.tsv",
}
DEPENDENCIES = {
    "EQUAL_WEIGHT_OR_LAMBDA": re.compile(r"equal.{0,30}(?:screen|angular|weight)|\blambda\b", re.I | re.S),
    "SHEAR": re.compile(r"\bshear\b|trace[- ]?free", re.I),
    "PARALLEL_PAIR_SCREEN": re.compile(r"parallel.{0,40}(?:screen|pair|angular)|(?:screen|pair|angular).{0,40}parallel", re.I | re.S),
    "ROUND_OR_DIAGONAL_SCREEN": re.compile(r"round.{0,30}(?:screen|S2)|diagonal.{0,30}(?:screen|angular)|fixed[- ]axis", re.I | re.S),
    "TRANSVERSE_RESPONSE": re.compile(r"transverse.{0,35}(?:response|screen|coframe)|angular.{0,35}(?:screen|weight|response)", re.I | re.S),
    "BLOCK_SCREEN": re.compile(r"block[- ]?screen|screen block", re.I),
}
CLAIM = re.compile(
    r"\b(?:DERIVED|UNIQUE|SELECTED|SETTLED|OPEN|CONDITIONAL|POSIT|OBSERVED|WORKING|REFUTED|"
    r"selector|selection|no[- ]?go|closure|bootstrap|action|source|boundary|stability|mass|SNe)\b",
    re.I,
)


def git(*args: str) -> bytes:
    return subprocess.check_output(["git", *args], cwd=ROOT)


def batch_payloads(blob_by_path: dict[str, str], paths: list[str]):
    process = subprocess.Popen(["git", "cat-file", "--batch"], cwd=ROOT,
                               stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    assert process.stdin is not None and process.stdout is not None
    try:
        for path in paths:
            process.stdin.write((blob_by_path[path]+"\n").encode()); process.stdin.flush()
            header = process.stdout.readline().decode().strip().split()
            if len(header) != 3 or header[1] != "blob":
                raise RuntimeError(f"cat-file header for {path}: {header}")
            size = int(header[2])
            payload = process.stdout.read(size)
            if process.stdout.read(1) != b"\n":
                raise RuntimeError(f"cat-file framing for {path}")
            yield path, payload
    finally:
        process.stdin.close(); process.stdout.close(); process.wait()


def write_tsv(name: str, rows: list[dict[str, str]]) -> None:
    with (HERE / name).open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), delimiter="\t", lineterminator="\n")
        writer.writeheader(); writer.writerows(rows)


def main() -> int:
    if git("rev-parse", f"{BASE}^{{tree}}").decode().strip() != TREE:
        raise SystemExit("base tree mismatch")
    tree_rows = git("ls-tree", "-r", BASE).decode().splitlines()
    blob_by_path = {}
    for line in tree_rows:
        metadata, path = line.split("\t", 1)
        blob_by_path[path] = metadata.split()[2]
    paths = sorted(blob_by_path)
    broad_dependency = set(
        line.split(":", 1)[1] for line in
        git("grep", "-Il", "-E", r"lambda|shear|screen|transverse|angular|parallel|round|diagonal", BASE,
            "--", "*.md", "*.tsv", "*.json", "*.txt").decode().splitlines()
    )
    broad_claim = set(
        line.split(":", 1)[1] for line in
        git("grep", "-Il", "-E", r"DERIVED|UNIQUE|SELECTED|SETTLED|OPEN|CONDITIONAL|POSIT|OBSERVED|WORKING|REFUTED|selector|selection|no-go|closure|bootstrap|action|source|boundary|stability|mass|SNe", BASE,
            "--", "*.md", "*.tsv", "*.json", "*.txt").decode().splitlines()
    )
    candidate_paths = sorted(
        path for path in (broad_dependency & broad_claim)
        if not path.startswith(EXCLUDED_PREFIXES) and Path(path).suffix in TEXT_SUFFIXES
    )
    rows = []
    for path, payload in batch_payloads(blob_by_path, candidate_paths):
        try:
            text = payload.decode("utf-8")
        except UnicodeDecodeError:
            continue
        dependency_hits = [name for name, pattern in DEPENDENCIES.items() if pattern.search(text) or pattern.search(path)]
        if not dependency_hits or not CLAIM.search(text):
            continue
        blob = blob_by_path[path]
        basename = Path(path).name
        family = path.split("/", 1)[0] if "/" in path else "CONTROL_ROOT"
        rows.append({
            "path": path,
            "family": family,
            "role": "PRIMARY_CLAIM_SOURCE" if basename in PRIMARY_NAMES else "SUPPORTING_FORENSIC_SOURCE",
            "dependency_hits": ";".join(dependency_hits),
            "git_blob": blob,
            "sha256": hashlib.sha256(payload).hexdigest(),
            "bytes": str(len(payload)),
        })
    rows.sort(key=lambda row: row["path"])
    write_tsv("DISCOVERED_SOURCE_CENSUS.tsv", rows)
    primary = [row for row in rows if row["role"] == "PRIMARY_CLAIM_SOURCE"]
    write_tsv("PRIMARY_CLAIM_SOURCE_CENSUS.tsv", primary)
    counts = Counter(row["family"] for row in rows)
    primary_counts = Counter(row["family"] for row in primary)
    families = [{
        "family": family,
        "all_matching_sources": str(counts[family]),
        "primary_claim_sources": str(primary_counts[family]),
        "adjudication_status": "PENDING",
    } for family in sorted(counts)]
    write_tsv("DISCOVERED_FAMILY_CENSUS.tsv", families)
    identity = hashlib.sha256("".join(f"{r['path']}\t{r['sha256']}\n" for r in rows).encode()).hexdigest()
    result = {
        "schema": "udt-general-screen-dependency-discovery-1.0",
        "status": "PASS",
        "base": BASE,
        "tracked_text_sources_scanned": sum(
            1 for p in paths if not p.startswith(EXCLUDED_PREFIXES) and Path(p).suffix in TEXT_SUFFIXES
        ),
        "matching_sources": len(rows),
        "primary_claim_sources": len(primary),
        "families": len(families),
        "identity_sha256": identity,
    }
    (HERE / "DISCOVERY_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True)+"\n")
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
