#!/usr/bin/env python3
"""Execute the frozen R1A git-move batch and exact non-frozen pointer rewrites."""

from __future__ import annotations

import argparse
import csv
import hashlib
import subprocess
from collections import defaultdict
from pathlib import Path
from typing import Any


def load_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def digest(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def clean(value: Any) -> Any:
    if isinstance(value, str):
        return value.replace("\t", "\\t").replace("\r", "\\r").replace("\n", "\\n")
    return value


def write_tsv(path: Path, rows: list[dict[str, Any]], fields: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=fields,
            delimiter="\t",
            lineterminator="\n",
            extrasaction="ignore",
        )
        writer.writeheader()
        writer.writerows(
            {field: clean(row.get(field, "-")) for field in fields} for row in rows
        )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--expected-head", required=True)
    parser.add_argument("--premove", type=Path, required=True)
    parser.add_argument("--rewrite-plan", type=Path, required=True)
    parser.add_argument("--move-output", type=Path, required=True)
    parser.add_argument("--rewrite-output", type=Path, required=True)
    args = parser.parse_args()

    repo = args.repo.resolve()
    head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=repo, text=True).strip()
    if head != args.expected_head:
        raise AssertionError(f"expected HEAD {args.expected_head}, found {head}")

    premove = load_tsv(args.premove)
    rewrite_plan = load_tsv(args.rewrite_plan)
    if len(premove) != 17:
        raise AssertionError("frozen move set is not 17 paths")
    if any(row["source_frozen"] != "NO" for row in rewrite_plan):
        raise AssertionError("rewrite plan contains frozen source")

    before_payloads: dict[str, bytes] = {}
    for row in premove:
        old = repo / row["old_path"]
        new = repo / row["new_path"]
        if not old.is_file() or new.exists():
            raise AssertionError(f"move precondition failed: {row['old_path']}")
        payload = old.read_bytes()
        if digest(payload) != row["sha256_before"] or len(payload) != int(row["size_bytes"]):
            raise AssertionError(f"pre-move hash mismatch: {row['old_path']}")
        before_payloads[row["old_path"]] = payload

    rewrite_groups: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rewrite_plan:
        rewrite_groups[row["source"]].append(row)
    rewrite_results: list[dict[str, Any]] = []
    for source, rows in sorted(rewrite_groups.items()):
        path = repo / source
        original = path.read_bytes()
        text = original.decode("utf-8")
        total = 0
        for row in rows:
            old_target = row["old_target"]
            expected = int(row["occurrences"])
            actual = text.count(old_target)
            if actual != expected:
                raise AssertionError(
                    f"pointer count mismatch {source}: {old_target} expected {expected}, got {actual}"
                )
            text = text.replace(old_target, row["new_target"])
            total += expected
        updated = text.encode("utf-8")
        path.write_bytes(updated)
        rewrite_results.append(
            {
                "source": source,
                "source_frozen": "NO",
                "path_only_substitutions": total,
                "sha256_before": digest(original),
                "sha256_after": digest(updated),
                "bytes_before": len(original),
                "bytes_after": len(updated),
            }
        )

    for row in premove:
        destination = repo / row["new_path"]
        destination.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run(
            ["git", "mv", "--", row["old_path"], row["new_path"]],
            cwd=repo,
            check=True,
        )

    move_results: list[dict[str, Any]] = []
    pointer_sources_by_target: dict[str, list[str]] = defaultdict(list)
    for row in rewrite_plan:
        pointer_sources_by_target[row["old_target"]].append(row["source"])
    for row in premove:
        old_path = row["old_path"]
        new_path = row["new_path"]
        after = (repo / new_path).read_bytes()
        before = before_payloads[old_path]
        if after != before:
            raise AssertionError(f"moved content changed: {old_path}")
        move_results.append(
            {
                "old_path": old_path,
                "new_path": new_path,
                "git_blob_oid_before": row["git_blob_oid"],
                "sha256_before": row["sha256_before"],
                "sha256_after": digest(after),
                "size_bytes": len(after),
                "content_identical": "YES",
                "rewritten_pointer_sources": ";".join(
                    sorted(set(pointer_sources_by_target[old_path]))
                )
                or "-",
            }
        )

    write_tsv(
        args.move_output,
        move_results,
        [
            "old_path",
            "new_path",
            "git_blob_oid_before",
            "sha256_before",
            "sha256_after",
            "size_bytes",
            "content_identical",
            "rewritten_pointer_sources",
        ],
    )
    write_tsv(
        args.rewrite_output,
        rewrite_results,
        [
            "source",
            "source_frozen",
            "path_only_substitutions",
            "sha256_before",
            "sha256_after",
            "bytes_before",
            "bytes_after",
        ],
    )
    print(f"moved={len(move_results)} pointer_sources={len(rewrite_results)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
