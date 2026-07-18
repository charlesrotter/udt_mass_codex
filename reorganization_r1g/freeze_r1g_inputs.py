#!/usr/bin/env python3
"""Freeze the R1G candidate and blast-radius universes after preregistration."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import subprocess
from pathlib import Path


BASE = "8015342a81b2d27cc310dde95ab7f386c6441a77"
BATCHES = {"B02_LEGACY_STANDALONE_ALGEBRA_A", "B03_LEGACY_STANDALONE_ALGEBRA_B"}
INPUTS = [
    "reorganization_r1c/build_r1c_lane_overlay.py",
    "research/_registry/ROOT_OWNERSHIP.tsv",
    "research/_registry/MIGRATION_READINESS.tsv",
    "research/_registry/CURRENT_ARTIFACT_PATHS.tsv",
    "reorganization_r1e/PROPOSED_BATCH_FILE_PLAN.tsv",
    "reorganization_r1e/COMPLETE_CANDIDATE_LEDGER.tsv",
    "reorganization_r1e/BATCH_RANKING.tsv",
    "reorganization_r1e/ATOMIC_FAMILY_GRAPH.json",
    "native_field_equations_constrained_two_player_results.md",
    "PURSUIT_CHARTER_2026-07-04.md",
    "branch_operator_contamination_ledger.md",
]


def run(repo: Path, *args: str) -> str:
    result = subprocess.run(["git", *args], cwd=repo, text=True, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE, check=False)
    if result.returncode:
        raise AssertionError(f"git {' '.join(args)} failed: {result.stderr}")
    return result.stdout


def rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def write_rows(path: Path, data: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(data[0]), delimiter="\t", lineterminator="\n")
        writer.writeheader(); writer.writerows(data)


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def bulk_history(repo: Path, paths: set[str]) -> dict[str, dict[str, str]]:
    marker = "__R1G_COMMIT__"
    output = run(repo, "log", f"--format={marker}%H%x09%aI%x09%cI%x09%s", "--name-status", "--", *sorted(paths))
    newest: dict[str, list[str]] = {}; oldest: dict[str, list[str]] = {}; introduced: dict[str, list[str]] = {}
    commit: list[str] | None = None
    for line in output.splitlines():
        if line.startswith(marker):
            commit = line[len(marker):].split("\t", 3)
            continue
        if not line or commit is None or "\t" not in line:
            continue
        fields = line.split("\t")
        status, path = fields[0], fields[-1]
        if path not in paths:
            continue
        newest.setdefault(path, commit); oldest[path] = commit
        if status.startswith("A"):
            introduced[path] = commit
    missing = paths - set(newest)
    if missing:
        raise AssertionError(f"no Git history for: {sorted(missing)}")
    result = {}
    for path in paths:
        intro = introduced.get(path, oldest[path])
        result[path] = {
            "introducing_commit": intro[0], "introducing_author_date": intro[1],
            "introducing_commit_date": intro[2], "introducing_subject": intro[3],
            "first_commit": oldest[path][0], "first_commit_date": oldest[path][2],
            "last_commit": newest[path][0], "last_commit_date": newest[path][2],
        }
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args(); repo = args.repo.resolve(); output = args.output_dir.resolve()
    output.mkdir(parents=True, exist_ok=True)
    if run(repo, "rev-parse", "HEAD").strip() != run(repo, "rev-parse", "HEAD").strip():
        raise AssertionError("unreachable")
    if run(repo, "merge-base", "--is-ancestor", BASE, "HEAD") is None:
        raise AssertionError("base is not an ancestor")

    current = {row["original_path"]: row for row in rows(repo / "research/_registry/CURRENT_ARTIFACT_PATHS.tsv")}
    plan = [row for row in rows(repo / "reorganization_r1e/PROPOSED_BATCH_FILE_PLAN.tsv")
            if row["batch_id"] in BATCHES]
    if len(plan) != 32 or {row["batch_id"] for row in plan} != BATCHES:
        raise AssertionError(f"unexpected B02/B03 universe: {len(plan)}")
    ownership = rows(repo / "research/_registry/ROOT_OWNERSHIP.tsv")
    affected_source = [row for row in ownership
                       if (Path(row["current_path"]).name.startswith("cascade_")
                           and row["primary_owner"] == "LEGACY_FROZEN"
                           and row["ownership_evidence"] == "PRE_NATIVE_FAMILY+R0_HISTORICAL_EVIDENCE")]
    if len(affected_source) != 121:
        raise AssertionError(f"expected 121 affected cascades, got {len(affected_source)}")
    histories = bulk_history(repo, {row["current_path"] for row in plan}
                             | {row["current_path"] for row in affected_source})

    candidates = []
    for row in plan:
        mapped = current[row["current_path"]]
        if mapped["current_path"] != row["current_path"]:
            raise AssertionError(f"candidate moved since R1E: {row['current_path']}")
        record = {
            "batch_id": row["batch_id"], "original_path": row["current_path"],
            "current_path": mapped["current_path"], "path_status": mapped["path_status"],
            "proposed_destination": row["destination"], "r1e_atomic_family_id": row["atomic_family_id"],
            "git_blob_oid": row["git_blob_oid"], "sha256": row["sha256"],
        }
        record.update(histories[row["current_path"]]); candidates.append(record)
    write_rows(output / "PREREGISTERED_B02_B03_UNIVERSE.tsv", candidates)

    affected = []
    for row in affected_source:
        record = {
            "current_path": row["current_path"], "artifact_type": row["artifact_type"],
            "r1c_first_commit_date": row["first_commit_date"],
            "r1c_last_commit_date": row["last_commit_date"],
            "r1c_primary_owner": row["primary_owner"],
            "r1c_ownership_evidence": row["ownership_evidence"],
        }
        record.update(histories[row["current_path"]]); affected.append(record)
    if len(affected) != 121:
        raise AssertionError(f"expected 121 affected cascades, got {len(affected)}")
    write_rows(output / "PREREGISTERED_AFFECTED_CASCADE_UNIVERSE.tsv", affected)

    hashes = [{"path": path, "git_blob_oid": run(repo, "rev-parse", f"{BASE}:{path}").strip(),
               "sha256": sha(repo / path), "size_bytes": str((repo / path).stat().st_size)}
              for path in INPUTS]
    write_rows(output / "PREREGISTERED_INPUT_HASHES.tsv", hashes)
    result = {
        "result": "PASS", "base": BASE,
        "preregistration_commit": run(repo, "rev-parse", "HEAD").strip(),
        "candidate_rows": len(candidates),
        "batch_counts": {batch: sum(row["batch_id"] == batch for row in candidates) for batch in sorted(BATCHES)},
        "affected_cascade_rows": len(affected),
        "affected_cascade_introduction_dates": {
            date: sum(row["introducing_commit_date"][:10] == date for row in affected)
            for date in sorted({row["introducing_commit_date"][:10] for row in affected})
        },
        "input_hash_rows": len(hashes), "candidate_contents_opened_by_freezer": False,
    }
    (output / "PREREGISTERED_INPUTS.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
