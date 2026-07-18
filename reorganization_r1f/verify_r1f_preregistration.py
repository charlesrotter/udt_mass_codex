#!/usr/bin/env python3
"""Fail-closed verifier for the pre-mutation R1F freeze."""

from __future__ import annotations

import csv
import hashlib
import json
import subprocess
from pathlib import Path


BASE = "14ba31a77aed1553c5df8ecd59b0f7a000c10e20"
BATCH = "B01_ACTIVE_MACRO_SYMPY_QUARTET"
EXPECTED = {
    "verify_center_escape.py": ("research/macro/verify_center_escape.py", "867cddbad61287219658912e3523c9dbbe2cc7e9", "ef0a29e58d7132d908ac94869d0c94ee1d65caceea13c42bdf9e7019eb998aa5"),
    "verify_center_nogo.py": ("research/macro/verify_center_nogo.py", "a86c2554959ccb5478fd2043a0030d8a9caa2530", "206d51e2d7a44ea567a49ae8da114e5a9e801e970a96b21b4e6393376abf88d0"),
    "verify_eos_dS_window.py": ("research/macro/verify_eos_dS_window.py", "9cb1f6917debc40700d99eaebb1f4c927d1b8293", "719fd2f4f70fc72dee2d129d57515957adf82a0ed962986453500ac5752ac58d"),
    "verify_wrl_canon.py": ("research/macro/verify_wrl_canon.py", "e5f2b5760326b7eefa7f7dc0339118b8bd327deb", "b5e6b5b79a1f743962d94820d9e5e14e0315fec0873962158bc5bdc5190877fc"),
}
REPO = Path(__file__).resolve().parents[1]
OUT = REPO / "reorganization_r1f"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git(*args: str) -> str:
    result = subprocess.run(["git", *args], cwd=REPO, text=True, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE, check=False)
    if result.returncode:
        raise AssertionError(result.stderr)
    return result.stdout.strip()


def rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def main() -> int:
    if git("rev-parse", "HEAD") != BASE:
        raise AssertionError("preregistration verification must precede its commit")
    frozen = rows(OUT / "PREREGISTERED_BATCH.tsv")
    if len(frozen) != 4 or {row["current_path"] for row in frozen} != set(EXPECTED):
        raise AssertionError("candidate coverage mismatch")
    for row in frozen:
        old = row["current_path"]
        destination, blob, digest = EXPECTED[old]
        if row["batch_id"] != BATCH or row["destination"] != destination:
            raise AssertionError(f"wrong batch/destination: {old}")
        if row["git_blob_oid"] != blob or row["sha256"] != digest:
            raise AssertionError(f"registered hash mismatch: {old}")
        if not (REPO / old).is_file() or (REPO / destination).exists():
            raise AssertionError(f"pre-move state mismatch: {old}")
        if git("hash-object", "--no-filters", old) != blob or sha(REPO / old) != digest:
            raise AssertionError(f"working artifact mismatch: {old}")
    plan = [row for row in rows(REPO / "reorganization_r1e/PROPOSED_BATCH_FILE_PLAN.tsv")
            if row["batch_id"] == BATCH]
    if frozen != plan:
        raise AssertionError("frozen rows are not an exact R1E plan extraction")
    current = {row["original_path"]: row for row in rows(REPO / "research/_registry/CURRENT_ARTIFACT_PATHS.tsv")}
    macro = {row["current_path"]: row for row in rows(REPO / "research/macro/ROOT_INVENTORY.tsv")}
    for old in EXPECTED:
        if current[old]["current_path"] != old or current[old]["path_status"] != "ROOT_RETAINED":
            raise AssertionError(f"current map not pre-move: {old}")
        if old not in macro:
            raise AssertionError(f"macro inventory missing: {old}")
    diff = git("diff", "--name-status", BASE).splitlines()
    for line in diff:
        status, path = line.split("\t", 1)
        if status != "A" or not path.startswith("reorganization_r1f/"):
            raise AssertionError(f"unauthorized preregistration diff: {line}")
    payload = json.loads((OUT / "PREREGISTERED_INPUTS.json").read_text())
    if payload["base"] != BASE or payload["candidate_rows"] != 4 or payload["artifact_mutations"] != 0:
        raise AssertionError("preregistered inputs mismatch")
    result = {
        "result": "PASS", "mode": "R1F_PREREGISTRATION_VERIFY", "base": BASE,
        "batch_id": BATCH, "candidate_rows": 4,
        "preregistered_batch_sha256": sha(OUT / "PREREGISTERED_BATCH.tsv"),
        "artifact_mutations": 0,
    }
    (OUT / "PREREG_VERIFY_RESULT.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
