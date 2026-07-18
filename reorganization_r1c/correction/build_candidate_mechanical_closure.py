#!/usr/bin/env python3
"""Build the preregistered, non-judgmental mechanical closure for all 13 candidates."""

from __future__ import annotations

import argparse
import ast
import csv
import hashlib
import json
import subprocess
from collections import defaultdict
from pathlib import Path
from typing import Any


BASE = "204f3637f134811f05df12aa7494ef41289ee3b4"
ACTIVE_LANES = {"FOUNDATIONS", "NATIVE_ACTION", "PARTICLE_MASS", "MACRO"}
LEFT_CONTINUATION = frozenset(
    "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_.-"
)
RIGHT_CONTINUATION = frozenset(
    "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_-"
)
FILE_SUFFIXES = (".md", ".py", ".json", ".npz", ".txt", ".log", ".tsv", ".csv", ".sh")
FROZEN_PACKAGE_PREFIXES = (
    "native_action_stage1_2026-07-18/",
    "native_action_stage2_2026-07-18/",
    "native_action_arm_c_2026-07-18/",
    "native_action_final_adjudication_2026-07-18/",
)


def command(repo: Path, args: list[str], *, check: bool = True) -> subprocess.CompletedProcess[bytes]:
    completed = subprocess.run(
        args, cwd=repo, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False
    )
    if check and completed.returncode:
        raise AssertionError(
            f"command failed: {' '.join(args)}\n{completed.stderr.decode('utf-8', 'replace')}"
        )
    return completed


def load_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def git_paths(repo: Path) -> list[str]:
    payload = command(repo, ["git", "ls-tree", "-r", "-z", "--name-only", BASE]).stdout
    return [part.decode("utf-8") for part in payload.split(b"\0") if part]


def git_blob(repo: Path, path: str) -> bytes:
    return command(repo, ["git", "show", f"{BASE}:{path}"]).stdout


def is_reference_at(text: str, start: int, token: str) -> bool:
    if not text.startswith(token, start):
        return False
    if start and text[start - 1] in LEFT_CONTINUATION:
        return False
    end = start + len(token)
    if end == len(text):
        return True
    following = text[end]
    if following in RIGHT_CONTINUATION:
        return False
    if following == "." and end + 1 < len(text):
        return text[end + 1] not in RIGHT_CONTINUATION
    return True


def occurrences(text: str, token: str) -> list[int]:
    found: list[int] = []
    offset = 0
    while True:
        offset = text.find(token, offset)
        if offset < 0:
            return found
        if is_reference_at(text, offset, token):
            found.append(offset)
        offset += len(token)


def dependency_indexes(rows: list[dict[str, str]]) -> tuple[dict[str, list[dict[str, str]]], dict[str, list[dict[str, str]]]]:
    inbound: dict[str, list[dict[str, str]]] = defaultdict(list)
    outbound: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        outbound[row["source"]].append(row)
        for target in filter(None, row["resolved_target"].split("|")):
            if row["source"] != target:
                inbound[target].append(row)
    return inbound, outbound


def compact_edge(row: dict[str, str]) -> dict[str, str]:
    return {
        "source": row["source"],
        "line": row["line"],
        "category": row["category"],
        "kind": row["kind"],
        "raw_target": row["raw_target"],
        "resolved_target": row["resolved_target"],
        "status": row["status"],
        "detail": row["detail"],
    }


def imports_from(payload: bytes) -> list[str]:
    if not payload:
        return []
    tree = ast.parse(payload.decode("utf-8"))
    found: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            found.extend(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            found.append(node.module or "")
    return sorted(set(filter(None, found)))


def test_globs(repo: Path) -> list[str]:
    tree = ast.parse((repo / "tests/test_hygiene_header.py").read_text(encoding="utf-8"))
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(
            isinstance(target, ast.Name) and target.id == "HYGIENE_COVERED_GLOBS"
            for target in node.targets
        ):
            value = ast.literal_eval(node.value)
            assert isinstance(value, list)
            return [str(item) for item in value]
    raise AssertionError("HYGIENE_COVERED_GLOBS not found")


def file_tokens(payload: str) -> list[str]:
    allowed = set("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_./-+")
    tokens = []
    for word in payload.replace("`", " ").replace("'", " ").replace('"', " ").split():
        candidate = word.strip("()[]{}<>,;:")
        if all(char in allowed for char in candidate) and candidate.endswith(FILE_SUFFIXES):
            tokens.append(candidate)
    return sorted(set(tokens))


def git_grep_sources(repo: Path, token: str) -> list[str]:
    completed = command(
        repo, ["git", "grep", "-I", "-l", "-F", token, BASE, "--"], check=False
    )
    assert completed.returncode in (0, 1)
    prefix = f"{BASE}:"
    result = []
    for line in completed.stdout.decode("utf-8").splitlines():
        assert line.startswith(prefix), line
        result.append(line[len(prefix):])
    return sorted(result)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--candidates", type=Path, required=True)
    parser.add_argument("--ownership", type=Path, required=True)
    parser.add_argument("--readiness", type=Path, required=True)
    parser.add_argument("--operational", type=Path, required=True)
    parser.add_argument("--forensic", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    repo = args.repo.resolve()
    assert command(repo, ["git", "rev-parse", BASE]).stdout.decode().strip() == BASE

    candidates = load_tsv(args.candidates)
    ownership = {row["current_path"]: row for row in load_tsv(args.ownership)}
    readiness = {row["current_path"]: row for row in load_tsv(args.readiness)}
    operational_in, operational_out = dependency_indexes(load_tsv(args.operational))
    forensic_in, _ = dependency_indexes(load_tsv(args.forensic))
    paths = git_paths(repo)
    text_blobs: dict[str, str] = {}
    for path in paths:
        payload = git_blob(repo, path)
        if b"\0" not in payload:
            text_blobs[path] = payload.decode("utf-8", "replace")
    globs = test_globs(repo)

    records: list[dict[str, Any]] = []
    for row in candidates:
        path = row["current_path"]
        payload = git_blob(repo, path)
        assert (repo / path).read_bytes() == payload
        literal_sources = sorted(source for source, text in text_blobs.items() if path in text)
        assert literal_sources == git_grep_sources(repo, path)
        boundary_map = {
            source: occurrences(text, path)
            for source, text in text_blobs.items()
            if occurrences(text, path)
        }
        owner = ownership[path]
        ready = readiness[path]
        assert owner["primary_owner"] in ACTIVE_LANES
        assert ready["migration_readiness"] == "MOVE_READY"
        assert ready["recommended_destination_if_migrated"] == row["recommended_destination_if_migrated"]
        source_text = payload.decode("utf-8")
        tokens = file_tokens(source_text)
        token_status = {
            token: {
                "tracked_at_base": token in paths,
                "readiness": readiness[token]["migration_readiness"] if token in readiness else "NOT_REGISTERED_ROOT_PATH",
                "frozen_manifest_status": ownership[token]["frozen_manifest_status"] if token in ownership else "NOT_REGISTERED_ROOT_PATH",
            }
            for token in tokens
        }
        imports = imports_from(payload) if path.endswith(".py") else []
        internal_imports = {
            module: (
                f"{module.split('.')[0]}.py"
                if f"{module.split('.')[0]}.py" in paths
                else "NOT_ROOT_MODULE"
            )
            for module in imports
        }
        forensic_edges = forensic_in.get(path, [])
        records.append(
            {
                "current_path": path,
                "primary_owner": owner["primary_owner"],
                "migration_readiness": ready["migration_readiness"],
                "destination": ready["recommended_destination_if_migrated"],
                "destination_collision": (repo / ready["recommended_destination_if_migrated"]).exists(),
                "git_blob_oid": command(repo, ["git", "rev-parse", f"{BASE}:{path}"]).stdout.decode().strip(),
                "sha256": hashlib.sha256(payload).hexdigest(),
                "size_bytes": len(payload),
                "candidate_frozen_manifest_status": owner["frozen_manifest_status"],
                "operational_inbound_edges": [compact_edge(edge) for edge in operational_in.get(path, [])],
                "operational_outbound_edges": [compact_edge(edge) for edge in operational_out.get(path, [])],
                "forensic_inbound_edges": [compact_edge(edge) for edge in forensic_edges],
                "forensic_reorganization_sources": sorted(
                    {edge["source"] for edge in forensic_edges if edge["source"].startswith("reorganization_r")}
                ),
                "frozen_package_inbound_sources": sorted(
                    {edge["source"] for edge in forensic_edges if edge["source"].startswith(FROZEN_PACKAGE_PREFIXES)}
                ),
                "literal_git_grep_sources": literal_sources,
                "corrected_boundary_sources": sorted(boundary_map),
                "corrected_boundary_occurrences": sum(len(value) for value in boundary_map.values()),
                "literal_git_grep_crosscheck": "PASS",
                "file_like_tokens": tokens,
                "file_like_token_status": token_status,
                "python_imports": imports,
                "root_internal_import_resolution": internal_imports,
                "hygiene_test_glob_matches": [pattern for pattern in globs if Path(path).match(pattern)],
                "registered_unresolved_dynamic_touches": int(ready["unresolved_dynamic_touches"]),
            }
        )

    assert len(records) == 13 and len({record["current_path"] for record in records}) == 13
    assert occurrences("See file.md.", "file.md")
    assert occurrences("See file.md)", "file.md")
    assert not occurrences("See file.md.bak", "file.md")
    result = {
        "result": "PASS",
        "mode": "R1C_CORRECTION_MECHANICAL_CLOSURE_NO_ADJUDICATION",
        "base": BASE,
        "candidate_count": len(records),
        "literal_git_grep_crosschecks": 13,
        "catchproof": {
            "file_md_period_detected": "PASS",
            "file_md_parenthesis_detected": "PASS",
            "file_md_bak_rejected": "PASS",
        },
        "candidates": records,
    }
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "result": result["result"],
        "candidate_count": result["candidate_count"],
        "literal_git_grep_crosschecks": result["literal_git_grep_crosschecks"],
        "catchproof": result["catchproof"],
    }, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
