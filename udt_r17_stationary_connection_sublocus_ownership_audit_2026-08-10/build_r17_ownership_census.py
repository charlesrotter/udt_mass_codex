#!/usr/bin/env python3
"""Census every tracked R17/W01 reference at the frozen preregistration base."""

from __future__ import annotations

import csv
import hashlib
import json
import re
import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent
BASE = "64b5319c1115589928317008548224600881b252"
PROTECTED = "udt_kernel_plane_global_curvature_holonomy_atlas_2026-08-02/"
PRIMARY_ALIAS = re.compile(r"(?<![A-Za-z0-9_])(?:R17|W01|F_GENERIC)(?![A-Za-z0-9_])")
ALL_ALIAS = re.compile(r"(?<![A-Za-z0-9_])(?:R17|W01|F_GENERIC|C0[1-6])(?![A-Za-z0-9_])")
OWNER_TERMS = re.compile(
    r"field equation|equation of motion|on[- ]shell|profile equation|whole[- ]solution law|"
    r"select(?:s|ed|ion)?[^\n]{0,50}(?:lambda|profile|branch)",
    re.IGNORECASE,
)
NONOWNER_TERMS = re.compile(
    r"off[- ]shell|not (?:an? )?equation|no field equation|on[- ]shell[^\n]{0,40}open|"
    r"profile_selected.{0,8}false|lambda_selected.{0,8}false|"
    r"complete_whole_solution_law.{0,8}open|does not select|no.*selection",
    re.IGNORECASE,
)


def git(*args: str) -> bytes:
    return subprocess.check_output(("git", *args), cwd=HERE.parent)


def artifact_class(path: str) -> str:
    if path in {
        "LIVE.md", "HANDOFF.md", "INDEX.md", "README.md", "AGENTS.md", "MEMORY.md",
        "CURRENT_RESEARCH_PROGRAM.md", "CURRENT_SCIENTIFIC_PREMISES.md",
        "CURRENT_SCIENTIFIC_PREMISES.tsv", "INFLIGHT_STATE.md",
    }:
        return "CURRENT_CONTROL_OR_ORIENTATION"
    if path.startswith(("archive/", "reorganization_r")) or "TRANSCRIPT" in path.upper():
        return "HISTORICAL_OR_REVIEW_RECORD"
    if path.endswith((".py", ".json", ".tsv", ".txt", ".log")):
        return "MACHINE_EVIDENCE_OR_IMPLEMENTATION"
    if path.endswith(".md"):
        return "RESEARCH_OR_EVIDENCE_PROSE"
    return "OTHER_TRACKED_REFERENCE"


def disposition(path: str, text: str, owner_hits: int, negative_hits: int) -> str:
    if path == "CURRENT_SCIENTIFIC_PREMISES.tsv":
        return "CURRENT_AUTHORITY_EXPLICITLY_LEAVES_R17_ONSHELL_AND_BRANCH_SELECTION_OPEN"
    if path.startswith("udt_r17_") or path.startswith("udt_twisted_s3_"):
        if negative_hits:
            return "PRIMARY_R17_EVIDENCE_EXPLICITLY_OFFSHELL_OR_NONSE﻿LECTING".replace("﻿", "")
        return "PRIMARY_R17_IMPLEMENTATION_OR_RECORD_NO_EQUATION_OWNER_CLAIM"
    if artifact_class(path) == "CURRENT_CONTROL_OR_ORIENTATION":
        return "CURRENT_POINTER_OR_GUARD_NOT_AN_EQUATION_OWNER"
    if artifact_class(path) == "HISTORICAL_OR_REVIEW_RECORD":
        return "HISTORICAL_OR_REVIEW_REFERENCE_NOT_CURRENT_OWNER"
    if owner_hits and negative_hits:
        return "MENTIONS_EQUATION_OR_SELECTION_BUT_EXPLICITLY_OPEN_NEGATIVE_OR_OTHER_SCOPE"
    if owner_hits:
        return "TERM_HIT_REQUIRES_CONTEXT__NOT_CURRENT_R17_AUTHORITY"
    return "REFERENCE_ONLY_NO_OWNERSHIP_TERM"


def main() -> int:
    paths = git("ls-tree", "-r", "--name-only", BASE).decode().splitlines()
    rows: list[dict[str, str | int]] = []
    for path in paths:
        if path.startswith(PROTECTED):
            continue
        raw = git("show", f"{BASE}:{path}")
        if b"\0" in raw:
            continue
        text = raw.decode("utf-8", errors="replace")
        primary_alias_hits = len(PRIMARY_ALIAS.findall(text))
        if not primary_alias_hits:
            continue
        alias_hits = len(ALL_ALIAS.findall(text))
        owner_hits = len(OWNER_TERMS.findall(text))
        negative_hits = len(NONOWNER_TERMS.findall(text))
        rows.append({
            "path": path,
            "artifact_class": artifact_class(path),
            "primary_alias_occurrences": primary_alias_hits,
            "alias_occurrences": alias_hits,
            "ownership_term_occurrences": owner_hits,
            "explicit_nonowner_occurrences": negative_hits,
            "disposition": disposition(path, text, owner_hits, negative_hits),
            "blob": git("rev-parse", f"{BASE}:{path}").decode().strip(),
            "sha256": hashlib.sha256(raw).hexdigest(),
        })

    rows.sort(key=lambda row: str(row["path"]))
    fieldnames = [
        "path", "artifact_class", "primary_alias_occurrences", "alias_occurrences", "ownership_term_occurrences",
        "explicit_nonowner_occurrences", "disposition", "blob", "sha256",
    ]
    with (HERE / "R17_TRACKED_REFERENCE_CENSUS.tsv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, delimiter="\t", fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

    disposition_counts: dict[str, int] = {}
    for row in rows:
        key = str(row["disposition"])
        disposition_counts[key] = disposition_counts.get(key, 0) + 1
    result = {
        "schema_version": 1,
        "base": BASE,
        "protected_prefix_excluded_unread": PROTECTED,
        "tracked_text_paths_with_r17_alias": len(rows),
        "primary_alias_occurrences": sum(int(row["primary_alias_occurrences"]) for row in rows),
        "alias_occurrences": sum(int(row["alias_occurrences"]) for row in rows),
        "ownership_term_occurrences": sum(int(row["ownership_term_occurrences"]) for row in rows),
        "explicit_nonowner_occurrences": sum(int(row["explicit_nonowner_occurrences"]) for row in rows),
        "disposition_counts": disposition_counts,
        "current_authoritative_owner": "NONE",
        "current_authoritative_status": "R17_ONSHELL_BRANCH_LAMBDA_PROFILE_SELECTION_OPEN",
        "census_sha256": hashlib.sha256((HERE / "R17_TRACKED_REFERENCE_CENSUS.tsv").read_bytes()).hexdigest(),
    }
    (HERE / "R17_OWNERSHIP_CENSUS_RESULT.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
