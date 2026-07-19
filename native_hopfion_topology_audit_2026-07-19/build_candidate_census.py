#!/usr/bin/env python3
"""Generate the preregistered repository-wide Hopf/topology candidate and exclusion census."""

from __future__ import annotations

import argparse
import csv
import pathlib
import re
import subprocess

from build_source_inventory import SOURCES


BASE = "28628be883dd37b0982dfb8ceeb41e46f1aa0d9b"
FILENAME_RE = re.compile(r"hopf|skyr|topolog|winding|charge|carrier|nonull|(^|[/_.-])s2([/_.-]|$)", re.I)
TEXT_RE = r"Hopf|pi_3|S\^3|S\^2|Skyrme|winding|topological charge|boundary|compactif|carrier"


def git(root: pathlib.Path, *args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(["git", *args], cwd=root, text=True, capture_output=True, check=check)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    package = pathlib.Path(__file__).resolve().parent
    root = package.parent

    tracked = git(root, "ls-tree", "-r", "--name-only", BASE).stdout.splitlines()
    filename_matches = {path for path in tracked if FILENAME_RE.search(path)}
    grep = git(root, "grep", "-Il", "-E", TEXT_RE, BASE, "--", check=False)
    if grep.returncode not in (0, 1):
        raise RuntimeError(grep.stderr)
    prefix = BASE + ":"
    text_matches = {
        row[len(prefix):] if row.startswith(prefix) else row
        for row in grep.stdout.splitlines() if row
    }
    candidates = sorted(filename_matches | text_matches)
    load_bearing = {path for path, _, _ in SOURCES}

    rows = []
    for path in candidates:
        basis = []
        if path in filename_matches:
            basis.append("FILENAME")
        if path in text_matches:
            basis.append("TEXT")
        if path in load_bearing:
            disposition = "LOAD_BEARING_SOURCE"
            reason = "opened and hash-bound in SOURCE_INVENTORY.tsv"
        elif path.startswith(("archive/", "legacy/", "rescued_workspaces/", "reorganization_r")):
            disposition = "EXCLUDED_HISTORICAL_OR_REORG"
            reason = "not current affirmative authority; retained only as non-load-bearing context"
        elif path.startswith(("native_action_stage1_", "native_action_stage2_", "native_action_arm_c_", "native_action_final_")):
            disposition = "EXCLUDED_FROZEN_PACKAGE_COMPANION"
            reason = "frozen package companion; controlling carrier status is represented by exact C0/C1 and final ledger"
        elif pathlib.PurePosixPath(path).suffix.lower() not in {".md", ".py", ".tsv", ".json", ".txt"}:
            disposition = "EXCLUDED_OPAQUE_OR_NON_TEXT_ROLE"
            reason = "not needed for the bounded documentary/algebra classification"
        else:
            disposition = "SUPPORTING_NOT_LOAD_BEARING"
            reason = "discovery hit but not required after current authority, exact field code, and banked result sources were selected"
        rows.append({
            "base": BASE,
            "path": path,
            "match_basis": ";".join(basis),
            "git_blob": git(root, "rev-parse", f"{BASE}:{path}").stdout.strip(),
            "disposition": disposition,
            "reason": reason,
        })

    output = pathlib.Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    counts: dict[str, int] = {}
    for row in rows:
        counts[row["disposition"]] = counts.get(row["disposition"], 0) + 1
    rendered = " ".join(f"{key}={counts[key]}" for key in sorted(counts))
    print(f"CANDIDATE_CENSUS rows={len(rows)} filename={len(filename_matches)} text={len(text_matches)} {rendered}")


if __name__ == "__main__":
    main()
