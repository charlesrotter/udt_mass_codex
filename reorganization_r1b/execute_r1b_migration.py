#!/usr/bin/env python3
"""Execute exactly the frozen two-file R1B migration and one pointer edit."""

from __future__ import annotations

import argparse
import csv
import hashlib
import subprocess
from pathlib import Path
from typing import Any


def load(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def write(path: Path, rows: list[dict[str, Any]], fields: tuple[str, ...]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows({field: row.get(field, "-") for field in fields} for row in rows)


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def git_blob_oid(data: bytes) -> str:
    return hashlib.sha1(f"blob {len(data)}\0".encode("ascii") + data).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--mutation-base", required=True)
    parser.add_argument("--move-plan", type=Path, required=True)
    parser.add_argument("--pointer-plan", type=Path, required=True)
    parser.add_argument("--colocated-plan", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()

    repo = args.repo.resolve()
    output = args.output_dir.resolve()
    output.mkdir(parents=True, exist_ok=True)
    head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=repo, text=True).strip()
    assert head == args.mutation_base
    assert not subprocess.check_output(
        ["git", "status", "--porcelain", "--untracked-files=no"], cwd=repo, text=True
    )
    moves = load(args.move_plan)
    pointers = load(args.pointer_plan)
    colocated = load(args.colocated_plan)
    assert len(moves) == 2 and len(pointers) == 1 and len(colocated) == 1

    move_payloads = {}
    for move in moves:
        old = repo / move["old_path"]
        new = repo / move["new_path"]
        assert old.is_file() and not new.exists()
        payload = old.read_bytes()
        assert sha256(payload) == move["sha256_before"]
        assert git_blob_oid(payload) == move["git_blob_oid_before"]
        assert len(payload) == int(move["size_bytes"])
        move_payloads[move["old_path"]] = payload

    pointer_payloads = {}
    pointer_results = []
    for pointer in pointers:
        path = repo / pointer["source"]
        before = path.read_bytes()
        text = before.decode("utf-8")
        old, new = pointer["old_target"], pointer["new_target"]
        assert pointer["rewrite_mode"] == "EXACT_PATH_TOKEN_ONLY"
        assert pointer["source_immutability"] in {
            "MUTABLE_NAVIGATION_SOURCE", "SOFT_EVIDENCE_PATH_ONLY_SOURCE"
        }
        assert text.count(old) == 1 and new not in text
        after = text.replace(old, new, 1).encode("utf-8")
        pointer_payloads[pointer["source"]] = after
        pointer_results.append(
            {
                "source": pointer["source"],
                "old_target": old,
                "new_target": new,
                "replacement_count": 1,
                "before_sha256": sha256(before),
                "after_sha256": sha256(after),
                "change_scope": "EXACT_PATH_TOKEN_ONLY",
            }
        )

    for move in moves:
        subprocess.run(
            ["git", "mv", "--", move["old_path"], move["new_path"]],
            cwd=repo,
            check=True,
        )
    for source, payload in pointer_payloads.items():
        (repo / source).write_bytes(payload)

    move_results = []
    for move in moves:
        old, new = repo / move["old_path"], repo / move["new_path"]
        assert not old.exists() and new.is_file()
        payload = new.read_bytes()
        assert payload == move_payloads[move["old_path"]]
        move_results.append(
            {
                **move,
                "sha256_after": sha256(payload),
                "git_blob_oid_after": git_blob_oid(payload),
                "content_identical": "YES",
            }
        )

    colocated_result = []
    for row in colocated:
        source = repo / row["source"]
        target = repo / "archive/pre_2026-07-01" / row["target"]
        assert source.is_file() and target.is_file()
        assert row["target"] in source.read_text(encoding="utf-8")
        assert source.parent == target.parent
        colocated_result.append({**row, "postmove_resolves": "YES"})

    write(
        output / "MIGRATION_RESULT.tsv",
        move_results,
        (
            "old_path", "new_path", "git_blob_oid_before", "git_blob_oid_after",
            "sha256_before", "sha256_after", "size_bytes", "content_identical",
        ),
    )
    write(
        output / "POINTER_SUBSTITUTION_RESULT.tsv",
        pointer_results,
        (
            "source", "old_target", "new_target", "replacement_count",
            "before_sha256", "after_sha256", "change_scope",
        ),
    )
    write(
        output / "COLOCATED_REFERENCE_RESULT.tsv",
        colocated_result,
        ("source", "target", "line", "column", "reason", "rewrite", "postmove_resolves"),
    )
    print("PASS: migrated 2 byte-identical files, rewrote 1 exact pointer, preserved 1 co-located reference")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
