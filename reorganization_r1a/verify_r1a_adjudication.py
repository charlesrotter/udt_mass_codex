#!/usr/bin/env python3
"""Independent fail-closed verifier for the frozen R1A pre-move adjudication."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import subprocess
from collections import Counter
from pathlib import Path
from typing import Any


VALID_DISPOSITIONS = {"MOVE_BATCH_1", "RETAIN_R1A"}
FROZEN_PREFIXES = (
    "native_action_stage1_2026-07-18/",
    "native_action_stage2_2026-07-18/",
    "native_action_arm_c_2026-07-18/",
    "native_action_final_adjudication_2026-07-18/",
)


def execute(repo: Path, command: list[str], binary: bool = False) -> bytes | str:
    completed = subprocess.run(
        command,
        cwd=repo,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=not binary,
        check=False,
    )
    if completed.returncode:
        stderr = completed.stderr if not binary else completed.stderr.decode("utf-8", "replace")
        raise AssertionError(f"command failed: {' '.join(command)}\n{stderr}")
    return completed.stdout


def tsv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def source_frozen(source: str, classes: dict[str, str]) -> bool:
    return classes.get(source) == "FROZEN_EVIDENCE" or source.startswith(FROZEN_PREFIXES)


def boundary_ok(text: str, start: int, length: int) -> bool:
    word = set("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_.-")
    before = start == 0 or text[start - 1] not in word
    after_at = start + length
    after = after_at == len(text) or text[after_at] not in word
    return before and after


def snapshot_files(repo: Path, commit: str) -> dict[str, bytes]:
    listing = str(execute(repo, ["git", "ls-tree", "-r", "-z", "--name-only", commit]))
    paths = [path for path in listing.split("\0") if path]
    return {
        path: bytes(execute(repo, ["git", "show", f"{commit}:{path}"], binary=True))
        for path in paths
    }


def independent_references(
    files: dict[str, bytes], candidates: set[str], classes: dict[str, str]
) -> list[tuple[str, str, int, int, str]]:
    rows: list[tuple[str, str, int, int, str]] = []
    for source, payload in sorted(files.items()):
        if b"\x00" in payload[:8192]:
            continue
        try:
            text = payload.decode("utf-8")
        except UnicodeDecodeError:
            continue
        for target in sorted(candidates):
            position = 0
            while True:
                position = text.find(target, position)
                if position < 0:
                    break
                if boundary_ok(text, position, len(target)):
                    line = text.count("\n", 0, position) + 1
                    line_start = text.rfind("\n", 0, position) + 1
                    column = position - line_start + 1
                    rows.append(
                        (
                            target,
                            source,
                            line,
                            column,
                            "YES" if source_frozen(source, classes) else "NO",
                        )
                    )
                position += len(target)
    return sorted(rows)


def validate(
    repo: Path,
    r0_inventory: list[dict[str, str]],
    adjudication: list[dict[str, str]],
    references: list[dict[str, str]],
    premove: list[dict[str, str]],
    eligible_lines: list[str],
    summary: dict[str, Any],
) -> None:
    classes = {row["path"]: row["classification"] for row in r0_inventory}
    candidates = {
        row["path"]
        for row in r0_inventory
        if row["classification"] in {"ARCHIVE_CANDIDATE", "UNKNOWN/BLOCKED"}
    }
    paths = [row["path"] for row in adjudication]
    assert len(adjudication) == 63, "not 63 adjudication rows"
    assert len(paths) == len(set(paths)), "duplicate adjudication row"
    assert set(paths) == candidates, "missing or extra candidate"
    assert Counter(row["r0_classification"] for row in adjudication) == Counter(
        {"ARCHIVE_CANDIDATE": 26, "UNKNOWN/BLOCKED": 37}
    )
    assert all(row["disposition"] in VALID_DISPOSITIONS for row in adjudication)
    assert all(
        row["disposition"] == "RETAIN_R1A"
        for row in adjudication
        if row["r0_classification"] == "UNKNOWN/BLOCKED"
    ), "unknown path made movable"

    snapshot = snapshot_files(repo, summary["base_commit"])
    for row in adjudication:
        payload = snapshot[row["path"]]
        assert hashlib.sha256(payload).hexdigest() == row["sha256"], row["path"]
        assert len(payload) == int(row["size_bytes"]), row["path"]

    recorded_refs = sorted(
        (
            row["target"],
            row["source"],
            int(row["line"]),
            int(row["column"]),
            row["source_frozen"],
        )
        for row in references
    )
    expected_refs = independent_references(snapshot, candidates, classes)
    assert recorded_refs == expected_refs, "inbound reference census mismatch"

    eligible = {
        row["path"] for row in adjudication if row["disposition"] == "MOVE_BATCH_1"
    }
    assert eligible == set(eligible_lines), "eligible batch file mismatch"
    assert eligible == set(summary["eligible_batch"]), "eligible summary mismatch"
    assert {row["old_path"] for row in premove} == eligible, "pre-move hash set mismatch"
    for row in premove:
        assert row["new_path"] == "archive/pre_2026-07-01/" + row["old_path"]
        candidate = next(item for item in adjudication if item["path"] == row["old_path"])
        assert row["sha256_before"] == candidate["sha256"]
        assert row["git_blob_oid"] == candidate["git_blob_oid"]
    assert not any(
        row["source_frozen"] == "YES" and row["target"] in eligible for row in references
    ), "eligible target has frozen inbound reference"


def rejected(callable_check: Any) -> str:
    try:
        callable_check()
    except (AssertionError, KeyError):
        return "PASS"
    raise AssertionError("catch-proof mutation was accepted")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--r0-inventory", type=Path, required=True)
    parser.add_argument("--adjudication", type=Path, required=True)
    parser.add_argument("--references", type=Path, required=True)
    parser.add_argument("--premove", type=Path, required=True)
    parser.add_argument("--eligible", type=Path, required=True)
    parser.add_argument("--summary", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    repo = args.repo.resolve()
    inventory = tsv(args.r0_inventory)
    adjudication = tsv(args.adjudication)
    references = tsv(args.references)
    premove = tsv(args.premove)
    eligible = [line for line in args.eligible.read_text(encoding="utf-8").splitlines() if line]
    summary = json.loads(args.summary.read_text(encoding="utf-8"))
    validate(repo, inventory, adjudication, references, premove, eligible, summary)

    def check_with(rows: list[dict[str, str]], refs: list[dict[str, str]]) -> None:
        validate(repo, inventory, rows, refs, premove, eligible, summary)

    catchproof = {
        "missing_candidate_rejected": rejected(lambda: check_with(adjudication[:-1], references)),
        "duplicate_candidate_rejected": rejected(
            lambda: check_with(adjudication + [dict(adjudication[0])], references)
        ),
        "missing_reference_rejected": rejected(
            lambda: check_with(adjudication, references[:-1])
        ),
        "bad_hash_rejected": rejected(
            lambda: check_with(
                [dict(row, sha256="0" * 64) if index == 0 else row for index, row in enumerate(adjudication)],
                references,
            )
        ),
        "unknown_move_rejected": rejected(
            lambda: check_with(
                [
                    dict(row, disposition="MOVE_BATCH_1")
                    if row["r0_classification"] == "UNKNOWN/BLOCKED"
                    else row
                    for row in adjudication
                ],
                references,
            )
        ),
        "frozen_flag_launder_rejected": rejected(
            lambda: check_with(
                adjudication,
                [
                    dict(row, source_frozen="NO")
                    if row["source_frozen"] == "YES"
                    else row
                    for row in references
                ],
            )
        ),
    }
    report = {
        "result": "PASS",
        "mode": "INDEPENDENT_PREMOVE_STATIC_VERIFIER",
        "snapshot": summary["base_commit"],
        "candidate_rows": len(adjudication),
        "reference_occurrences": len(references),
        "eligible_batch_files": len(eligible),
        "catchproof": catchproof,
    }
    args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
