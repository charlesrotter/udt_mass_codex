#!/usr/bin/env python3
"""Deterministically discover and hash the fixed-base branch/screen source universe."""

from __future__ import annotations

import csv
import hashlib
import re
import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
BASE = "bd8649ae31aab31435fbe986427d7f4e84d58e6d"
EXTENSIONS = {".md", ".tsv", ".json", ".py"}
NAME_RE = re.compile(r"finite.?cell|completion|complete.?branch|global.?metric|nonultrastatic|coframe|screen", re.I)
COMPLETION_RE = re.compile(r"finite[ -]?cell|completion|complete|globally? regular", re.I)
GEOMETRY_RE = re.compile(r"metric|coframe|screen|branch", re.I)
CONTEXT_RE = re.compile(r"branch|metric|coframe|screen|completion|path|holonomy|curvature|finite", re.I)
REFERENCE_RE = re.compile(r"[A-Za-z0-9_./-]+\.(?:md|tsv|json|py|npz|txt|csv|log)")
EXCLUDED_PREFIXES = ("archive/", "rescued_workspaces/", "reorganization_r", HERE.name + "/")


def git(*args: str, binary: bool = False):
    result = subprocess.run(
        ["git", *args], cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        text=not binary, check=False,
    )
    if result.returncode:
        message = result.stderr if not binary else result.stderr.decode("utf-8", "replace")
        raise RuntimeError(message)
    return result.stdout


def sha(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def write_tsv(name: str, records: list[dict[str, object]]) -> None:
    with (HERE / name).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(records[0]), delimiter="\t", lineterminator="\n")
        writer.writeheader(); writer.writerows(records)


def main() -> None:
    tree_lines = str(git("ls-tree", "-r", BASE)).splitlines()
    blobs = {line.split("\t", 1)[1]: line.split()[2] for line in tree_lines}
    paths = sorted(blobs)
    path_set = set(paths)
    by_name: dict[str, list[str]] = {}
    for path in paths:
        by_name.setdefault(Path(path).name, []).append(path)
    payloads: dict[str, bytes] = {}

    history = str(git("log", "--diff-filter=A", "--format=@@DATE@@%cs", "--name-only", BASE)).splitlines()
    introduced_dates: dict[str, str] = {}
    active_date = "UNKNOWN"
    for line in history:
        if line.startswith("@@DATE@@"):
            active_date = line.removeprefix("@@DATE@@")
        elif line:
            introduced_dates[line] = active_date

    completion_hits = {
        line.split(":", 1)[1]
        for line in str(git(
            "grep", "-I", "-l", "-E", r"finite[ -]?cell|completion|complete|globally? regular",
            BASE, "--", "*.md", "*.tsv", "*.json", "*.py",
        )).splitlines()
    }
    geometry_hits = {
        line.split(":", 1)[1]
        for line in str(git(
            "grep", "-I", "-l", "-E", r"metric|coframe|screen|branch",
            BASE, "--", "*.md", "*.tsv", "*.json", "*.py",
        )).splitlines()
    }
    content_hits = completion_hits & geometry_hits

    def payload(path: str) -> bytes:
        if path not in payloads:
            payloads[path] = git("show", f"{BASE}:{path}", binary=True)
        return payloads[path]

    candidates: dict[str, set[str]] = {}
    excluded = []
    for path in paths:
        if Path(path).suffix.lower() not in EXTENSIONS:
            continue
        if path.startswith(EXCLUDED_PREFIXES):
            continue
        filename_hit = bool(NAME_RE.search(Path(path).name))
        content_hit = path in content_hits
        if not (filename_hit or content_hit):
            continue
        introduced = introduced_dates.get(path, "UNKNOWN")
        if introduced != "UNKNOWN" and introduced < "2026-07-01":
            excluded.append({
                "path": path, "first_commit_date": introduced,
                "reason": "PRE_JULY_SEED_EXCLUDED_UNLESS_TRANSITIVELY_NAMED_BY_CURRENT_SOURCE",
            })
            continue
        reasons = candidates.setdefault(path, set())
        if filename_hit:
            reasons.add("FILENAME_SEED")
        if content_hit:
            reasons.add("CONTENT_CONJUNCTION_SEED")

    frontier = list(candidates)
    scanned: set[str] = set()
    while frontier:
        source = frontier.pop()
        if source in scanned:
            continue
        scanned.add(source)
        text = payload(source).decode("utf-8", "replace")
        for line in text.splitlines():
            if not CONTEXT_RE.search(line):
                continue
            for literal in REFERENCE_RE.findall(line):
                if literal in path_set:
                    resolved = literal
                else:
                    matches = by_name.get(Path(literal).name, [])
                    resolved = matches[0] if len(matches) == 1 else ""
                if not resolved or resolved.startswith((HERE.name + "/", "reorganization_r")):
                    continue
                if Path(resolved).suffix.lower() not in {".md", ".tsv", ".json", ".py", ".npz", ".txt", ".csv", ".log"}:
                    continue
                is_new = resolved not in candidates
                candidates.setdefault(resolved, set()).add(f"TRANSITIVE_FROM:{source}")
                if is_new and Path(resolved).suffix.lower() in EXTENSIONS:
                    frontier.append(resolved)

    records = []
    for path in sorted(candidates):
        data = payload(path)
        records.append({
            "path": path,
            "blob": blobs[path],
            "sha256": sha(data),
            "size_bytes": len(data),
            "first_commit_date": introduced_dates.get(path, "UNKNOWN"),
            "discovery_reason": ";".join(sorted(candidates[path])),
            "adjudication": "UNADJUDICATED",
        })
    write_tsv("DISCOVERED_SOURCE_CENSUS.tsv", records)
    if excluded:
        write_tsv("EXCLUDED_SEED_CENSUS.tsv", sorted(excluded, key=lambda row: row["path"]))
    print(f"discovered_sources={len(records)} excluded_pre_july_seeds={len(excluded)}")


if __name__ == "__main__":
    main()
