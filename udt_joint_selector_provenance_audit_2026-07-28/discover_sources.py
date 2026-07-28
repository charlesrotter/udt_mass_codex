#!/usr/bin/env python3
"""Mechanically discover joint-selector source groups from a fixed Git tree."""

from __future__ import annotations

import csv
import hashlib
import json
import re
import subprocess
from collections import defaultdict
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def git(*args: str, binary: bool = False, check: bool = True):
    result = subprocess.run(
        ["git", *args], cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        text=not binary, check=False,
    )
    if check and result.returncode:
        error = result.stderr if not binary else result.stderr.decode("utf-8", "replace")
        raise RuntimeError(error)
    return result


def write_tsv(path: Path, fields: list[str], rows: list[dict[str, object]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def group_for(path: str, historical: set[str]) -> str:
    parts = path.split("/")
    if len(parts) == 1:
        return "ROOT::" + path
    top = parts[0]
    if top in historical or top.startswith("reorganization_"):
        return "/".join(parts[:-1])
    return top


def main() -> None:
    rules = json.loads((HERE / "DISCOVERY_RULES.json").read_text(encoding="utf-8"))
    base = rules["base_commit"]
    observed_head = git("rev-parse", "HEAD").stdout.strip()
    observed_tree = git("rev-parse", f"{base}^{{tree}}").stdout.strip()
    if observed_tree != rules["base_tree"]:
        raise AssertionError("F01 base tree mismatch")
    if git("merge-base", "--is-ancestor", base, observed_head, check=False).returncode:
        raise AssertionError("F01 base is not an ancestor of HEAD")

    raw = git("ls-tree", "-r", "-z", "--long", base, binary=True).stdout
    records = [record for record in raw.split(b"\0") if record]
    entries: dict[str, dict[str, object]] = {}
    for record in records:
        metadata, raw_path = record.split(b"\t", 1)
        mode, kind, blob, size = metadata.decode().split()
        path = raw_path.decode("utf-8", "surrogateescape")
        entries[path] = {"mode": mode, "kind": kind, "blob": blob, "size": int(size)}
    if len(entries) != 9926:
        raise AssertionError(f"F02 tracked path count changed: {len(entries)}")

    suffixes = tuple(rules["text_suffixes"])
    text_paths = sorted(path for path in entries if path.lower().endswith(suffixes))
    historical = set(rules["historical_group_prefixes"])
    buckets: dict[str, set[str]] = {}
    for bucket, pattern in rules["bucket_patterns"].items():
        command = ["grep", "-I", "-l", "-E", "-i", pattern, base, "--"]
        command.extend(f"*{suffix}" for suffix in suffixes)
        result = git(*command, check=False)
        if result.returncode not in (0, 1):
            raise RuntimeError(result.stderr)
        hits = set()
        for line in result.stdout.splitlines():
            prefix = base + ":"
            path = line[len(prefix):] if line.startswith(prefix) else line
            if path in entries:
                hits.add(path)
        buckets[bucket] = hits

    file_buckets: dict[str, set[str]] = defaultdict(set)
    for bucket, paths in buckets.items():
        for path in paths:
            file_buckets[path].add(bucket)
    group_files: dict[str, list[str]] = defaultdict(list)
    group_buckets: dict[str, set[str]] = defaultdict(set)
    for path in text_paths:
        group = group_for(path, historical)
        group_files[group].append(path)
        group_buckets[group].update(file_buckets.get(path, set()))
    required = set(rules["bucket_patterns"])
    qualifying = {group for group, seen in group_buckets.items() if seen == required}

    companion = re.compile(rules["evidence_companion_pattern"], re.IGNORECASE)
    candidates = []
    for group in sorted(qualifying):
        for path in group_files[group]:
            if file_buckets.get(path) or companion.search(path):
                candidates.append(path)
    candidates = sorted(set(candidates))

    hit_rows = []
    for path in sorted(file_buckets):
        hit_rows.append({
            "path": path,
            "group": group_for(path, historical),
            "buckets": ";".join(sorted(file_buckets[path])),
            "bucket_count": len(file_buckets[path]),
            "qualifying_group": "YES" if group_for(path, historical) in qualifying else "NO",
        })
    write_tsv(
        HERE / "DISCOVERY_FILE_HITS.tsv",
        ["path", "group", "buckets", "bucket_count", "qualifying_group"], hit_rows,
    )

    group_rows = []
    for group in sorted(group_files):
        group_rows.append({
            "group": group,
            "text_files": len(group_files[group]),
            "hit_files": sum(path in file_buckets for path in group_files[group]),
            "buckets": ";".join(sorted(group_buckets[group])),
            "bucket_count": len(group_buckets[group]),
            "qualifies": "YES" if group in qualifying else "NO",
            "candidate_files": sum(path in candidates for path in group_files[group]),
        })
    write_tsv(
        HERE / "DISCOVERY_GROUP_OUTCOMES.tsv",
        ["group", "text_files", "hit_files", "buckets", "bucket_count", "qualifies", "candidate_files"],
        group_rows,
    )

    manifest_rows = []
    candidate_lines = []
    for number, path in enumerate(candidates, 1):
        blob = str(entries[path]["blob"])
        content = git("cat-file", "blob", blob, binary=True).stdout
        if len(content) != int(entries[path]["size"]):
            raise AssertionError(f"F10 size mismatch {path}")
        manifest_rows.append({
            "source_id": f"S{number:04d}",
            "path": path,
            "git_blob": blob,
            "size_bytes": len(content),
            "sha256": hashlib.sha256(content).hexdigest(),
            "group": group_for(path, historical),
            "hit_buckets": ";".join(sorted(file_buckets.get(path, set()))) or "EVIDENCE_COMPANION",
        })
        candidate_lines.append(path)
    write_tsv(
        HERE / "SOURCE_MANIFEST.tsv",
        ["source_id", "path", "git_blob", "size_bytes", "sha256", "group", "hit_buckets"],
        manifest_rows,
    )
    (HERE / "SOURCE_CANDIDATES.txt").write_text("\n".join(candidate_lines) + "\n", encoding="utf-8")

    snapshot = {
        "schema": "udt-joint-selector-source-discovery-1.0",
        "base_commit": base,
        "base_tree": observed_tree,
        "tracked_paths": len(entries),
        "text_paths": len(text_paths),
        "hit_files": len(file_buckets),
        "source_groups": len(group_files),
        "qualifying_groups": len(qualifying),
        "candidate_files": len(candidates),
        "bucket_file_counts": {bucket: len(paths) for bucket, paths in sorted(buckets.items())},
        "dirty_worktree_read": False,
        "generated_sources_eligible": False,
        "status": "PASS",
    }
    (HERE / "REPOSITORY_SNAPSHOT.json").write_text(json.dumps(snapshot, indent=2, sort_keys=True) + "\n")
    print(json.dumps(snapshot, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
