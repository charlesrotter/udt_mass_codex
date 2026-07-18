#!/usr/bin/env python3
"""Freeze the base-derived R1B candidate and frontier inputs before adjudication."""

from __future__ import annotations

import argparse
import csv
import hashlib
import importlib.util
import json
import subprocess
from pathlib import Path
from typing import Any


PERMANENT_ROOTS = {
    "AGENTS.md": "mandatory operating instructions",
    "CANON.md": "canon ledger",
    "CLAUDE.md": "binding working charter",
    "COGNITIVE_CORRAL_TRIGGERS_SETUP.md": "governance control",
    "CROSS_MODEL_VERIFY.md": "verification control",
    "FOUNDATIONAL_ASSUMPTIONS_LEDGER.md": "foundation status ledger",
    "HANDOFF.md": "startup handoff",
    "HYGIENE_HEADER_TEMPLATE.md": "test-governed evidence template",
    "INDEX.md": "repository navigation control",
    "LIVE.md": "authoritative current-state control",
    "MEMORY.md": "startup pointer ledger",
    "NEGATIVES_REGISTRY.md": "premise-scoped negative ledger",
    "PROBLEM_STATEMENT.md": "repository problem control",
    "PROVENANCE.md": "provenance ledger",
    "README.md": "root public navigation",
    "STRUCTURE_HYGIENE.md": "test-governed structure control",
}


def execute(repo: Path, command: list[str], *, binary: bool = False) -> str | bytes:
    completed = subprocess.run(
        command,
        cwd=repo,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=not binary,
        check=False,
    )
    if completed.returncode:
        error = completed.stderr if not binary else completed.stderr.decode("utf-8", "replace")
        raise RuntimeError(f"command failed: {' '.join(command)}\n{error}")
    return completed.stdout


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def write_tsv(path: Path, rows: list[dict[str, Any]], fields: tuple[str, ...]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=fields,
            delimiter="\t",
            lineterminator="\n",
            extrasaction="ignore",
        )
        writer.writeheader()
        for row in rows:
            writer.writerow(
                {
                    field: str(row.get(field, "-")).replace("\t", "\\t").replace("\n", "\\n")
                    for field in fields
                }
            )


def load_matcher(repo: Path):
    path = repo / "reorganization_r1a/correction_2026-07-18/reference_boundary.py"
    spec = importlib.util.spec_from_file_location("r1a_corrected_boundary", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load matcher: {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module, path


def base_paths(repo: Path, base: str) -> list[str]:
    raw = str(execute(repo, ["git", "ls-tree", "-r", "-z", "--name-only", base]))
    return sorted(filter(None, raw.split("\0")))


def base_blob(repo: Path, base: str, path: str) -> bytes:
    return bytes(execute(repo, ["git", "show", f"{base}:{path}"], binary=True))


def base_blob_oid(repo: Path, base: str, path: str) -> str:
    output = str(execute(repo, ["git", "ls-tree", base, "--", path])).strip()
    if not output:
        raise AssertionError(f"missing base path: {path}")
    return output.split()[2]


def history(repo: Path, base: str, path: str) -> tuple[str, str, str, str, str]:
    lines = str(
        execute(
            repo,
            ["git", "log", "--follow", "--format=%cs%x09%H%x09%s", base, "--", path],
        )
    ).splitlines()
    if not lines:
        raise AssertionError(f"no history: {path}")
    newest = lines[0].split("\t", 2)
    oldest = lines[-1].split("\t", 2)
    return oldest[0], oldest[1], newest[0], newest[1], newest[2]


def current_frontier_span(source: str, text: str) -> str:
    if source == "LIVE.md":
        marker = "**[prior layer of the same arc"
        end = text.find(marker)
        assert end > 0, "LIVE current-layer boundary not found"
        return text[:end]
    if source == "HANDOFF.md":
        start = text.find("## CURRENT")
        end = text.find("## [ARCHIVED]", start)
        assert start >= 0 and end > start, "HANDOFF current block not found"
        return text[start:end]
    raise AssertionError(source)


def line_details(text: str, offset: int) -> tuple[int, int, str]:
    line = text.count("\n", 0, offset) + 1
    start = text.rfind("\n", 0, offset) + 1
    end = text.find("\n", offset)
    if end < 0:
        end = len(text)
    return line, offset - start + 1, text[start:end].strip()[:400]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--base", required=True)
    parser.add_argument("--cutoff", default="2026-07-01")
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()

    repo = args.repo.resolve()
    output = args.output_dir.resolve()
    output.mkdir(parents=True, exist_ok=True)
    matcher, matcher_path = load_matcher(repo)
    proofs = matcher.catchproof()
    assert set(proofs.values()) == {"PASS"}

    paths = base_paths(repo, args.base)
    root_markdown = [path for path in paths if "/" not in path and path.endswith(".md")]
    all_rows: list[dict[str, Any]] = []
    candidate_rows: list[dict[str, Any]] = []
    for path in root_markdown:
        payload = base_blob(repo, args.base, path)
        first_date, first_commit, last_date, last_commit, last_subject = history(repo, args.base, path)
        row = {
            "path": path,
            "first_commit_date": first_date,
            "first_commit": first_commit,
            "last_commit_date_at_base": last_date,
            "last_commit_at_base": last_commit,
            "last_commit_subject_at_base": last_subject,
            "git_blob_oid_at_base": base_blob_oid(repo, args.base, path),
            "sha256_at_base": sha256(payload),
            "size_bytes_at_base": len(payload),
            "pre_cutoff": "YES" if first_date < args.cutoff else "NO",
        }
        all_rows.append(row)
        if first_date < args.cutoff:
            candidate_rows.append(
                {
                    **row,
                    "selection_reason": "TRACKED_ROOT_MARKDOWN_FIRST_COMMITTED_BEFORE_2026-07-01",
                }
            )

    candidate_names = {row["path"] for row in candidate_rows}
    permanent_rows = []
    for path, reason in sorted(PERMANENT_ROOTS.items()):
        status = "IN_CANDIDATE_UNIVERSE" if path in candidate_names else "OUTSIDE_BY_BASE_DATE_OR_ABSENCE"
        permanent_rows.append(
            {
                "path": path,
                "phase_status": "PERMANENT_ROOT",
                "reason": reason,
                "candidate_universe_status": status,
            }
        )

    frontier_rows = []
    for source in ("LIVE.md", "HANDOFF.md"):
        full = base_blob(repo, args.base, source).decode("utf-8")
        span = current_frontier_span(source, full)
        for target in root_markdown:
            for offset in matcher.occurrences(span, target):
                if offset and span[offset - 1] == "/":
                    continue
                line, column, excerpt = line_details(span, offset)
                frontier_rows.append(
                    {
                        "target": target,
                        "source": source,
                        "line": line,
                        "column": column,
                        "candidate_universe": "YES" if target in candidate_names else "NO",
                        "line_excerpt": excerpt,
                    }
                )
    frontier_rows.sort(key=lambda row: (row["target"], row["source"], row["line"], row["column"]))

    write_tsv(
        output / "BASE_ROOT_MARKDOWN.tsv",
        all_rows,
        (
            "path",
            "first_commit_date",
            "first_commit",
            "last_commit_date_at_base",
            "last_commit_at_base",
            "last_commit_subject_at_base",
            "git_blob_oid_at_base",
            "sha256_at_base",
            "size_bytes_at_base",
            "pre_cutoff",
        ),
    )
    write_tsv(
        output / "PREREGISTERED_CANDIDATES.tsv",
        candidate_rows,
        (
            "path",
            "first_commit_date",
            "first_commit",
            "last_commit_date_at_base",
            "last_commit_at_base",
            "last_commit_subject_at_base",
            "git_blob_oid_at_base",
            "sha256_at_base",
            "size_bytes_at_base",
            "selection_reason",
        ),
    )
    write_tsv(
        output / "PERMANENT_ROOT_REGISTRY.tsv",
        permanent_rows,
        ("path", "phase_status", "reason", "candidate_universe_status"),
    )
    write_tsv(
        output / "CURRENT_FRONTIER_REFERENCE_REGISTRY.tsv",
        frontier_rows,
        ("target", "source", "line", "column", "candidate_universe", "line_excerpt"),
    )

    generated = (
        "BASE_ROOT_MARKDOWN.tsv",
        "PREREGISTERED_CANDIDATES.tsv",
        "PERMANENT_ROOT_REGISTRY.tsv",
        "CURRENT_FRONTIER_REFERENCE_REGISTRY.tsv",
    )
    result = {
        "result": "PASS",
        "mode": "R1B_PREREGISTERED_INPUT_FREEZE",
        "base": args.base,
        "cutoff": args.cutoff,
        "selection_uses_base_tree_only": True,
        "generated_audit_records_influence_selection": False,
        "base_tracked_paths": len(paths),
        "base_root_markdown": len(root_markdown),
        "preregistered_candidates": len(candidate_rows),
        "permanent_root_registry_rows": len(permanent_rows),
        "current_frontier_reference_occurrences": len(frontier_rows),
        "current_frontier_candidate_targets": len(
            {row["target"] for row in frontier_rows if row["candidate_universe"] == "YES"}
        ),
        "matcher": {
            "path": str(matcher_path.relative_to(repo)),
            "sha256": sha256(matcher_path.read_bytes()),
            "catchproof": proofs,
        },
        "generated_artifacts": {
            name: sha256((output / name).read_bytes()) for name in generated
        },
    }
    (output / "PREREGISTERED_INPUTS.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
