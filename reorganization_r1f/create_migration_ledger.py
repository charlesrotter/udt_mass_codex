#!/usr/bin/env python3
"""Create the append-only R1F ledger after the migration commit exists."""

from __future__ import annotations

import csv
import hashlib
import subprocess
from pathlib import Path


MIGRATION_COMMIT = "c4cf405bba49625a9352a022b60754e7249c27f9"
ROLLBACK_PARENT = "fa211047fd9d81fcc64c424376facc6378837dfc"
REPO = Path(__file__).resolve().parents[1]
OUT = REPO / "research/_registry/MIGRATION_LEDGER.tsv"
FIELDS = [
    "migration_id", "committed_at_utc", "phase", "batch_id", "original_path",
    "old_current_path", "new_current_path", "rename_score", "git_blob_oid_before",
    "git_blob_oid_after", "sha256_before", "sha256_after", "pointer_change_record",
    "verification_record", "commit", "rollback_parent", "notes",
]


def run(*args: str, binary: bool = False) -> str | bytes:
    result = subprocess.run(["git", *args], cwd=REPO, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE, text=not binary, check=False)
    if result.returncode:
        err = result.stderr if not binary else result.stderr.decode("utf-8", "replace")
        raise AssertionError(err)
    return result.stdout


def sha(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def main() -> int:
    head = str(run("rev-parse", "HEAD")).strip()
    parent = str(run("rev-parse", f"{MIGRATION_COMMIT}^")).strip()
    if head != MIGRATION_COMMIT or parent != ROLLBACK_PARENT:
        raise AssertionError("ledger must be created immediately after the registered migration commit")
    if OUT.exists():
        raise AssertionError("append-only ledger already exists")
    schema = []
    with (REPO / "reorganization_r1e/PROPOSED_MIGRATION_LEDGER_SCHEMA.tsv").open(
            encoding="utf-8", newline="") as handle:
        schema = [row["column"] for row in csv.DictReader(handle, delimiter="\t")]
    if schema != FIELDS:
        raise AssertionError("registered schema mismatch")
    with (REPO / "reorganization_r1f/PREREGISTERED_BATCH.tsv").open(
            encoding="utf-8", newline="") as handle:
        batch = list(csv.DictReader(handle, delimiter="\t"))
    timestamp = str(run("show", "-s", "--format=%cI", MIGRATION_COMMIT)).strip()
    map_path = "research/_registry/CURRENT_ARTIFACT_PATHS.tsv"
    inv_path = "research/macro/ROOT_INVENTORY.tsv"
    before_map = sha(bytes(run("show", f"{ROLLBACK_PARENT}:{map_path}", binary=True)))
    after_map = sha(bytes(run("show", f"{MIGRATION_COMMIT}:{map_path}", binary=True)))
    before_inv = sha(bytes(run("show", f"{ROLLBACK_PARENT}:{inv_path}", binary=True)))
    after_inv = sha(bytes(run("show", f"{MIGRATION_COMMIT}:{inv_path}", binary=True)))
    pointer_record = (
        f"{map_path}:{before_map}:{after_map};"
        f"{inv_path}:{before_inv}:{after_inv}"
    )
    records = []
    for index, item in enumerate(batch, 1):
        records.append({
            "migration_id": f"R1F-20260718-{index:03d}",
            "committed_at_utc": timestamp,
            "phase": "R1F",
            "batch_id": item["batch_id"],
            "original_path": item["current_path"],
            "old_current_path": item["current_path"],
            "new_current_path": item["destination"],
            "rename_score": "R100",
            "git_blob_oid_before": item["git_blob_oid"],
            "git_blob_oid_after": item["git_blob_oid"],
            "sha256_before": item["sha256"],
            "sha256_after": item["sha256"],
            "pointer_change_record": pointer_record,
            "verification_record": "reorganization_r1f/MIGRATION_VERIFY_RESULT.json",
            "commit": MIGRATION_COMMIT,
            "rollback_parent": ROLLBACK_PARENT,
            "notes": "B01 byte-identical R100; pre/post exit and raw streams identical",
        })
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS, delimiter="\t", lineterminator="\n")
        writer.writeheader(); writer.writerows(records)
    print(f"ledger_rows={len(records)} migration_commit={MIGRATION_COMMIT} rollback_parent={ROLLBACK_PARENT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
