#!/usr/bin/env python3
"""Build the fixed-base R1B inbound, immutability, and dependency evidence."""

from __future__ import annotations

import argparse
import csv
import fnmatch
import hashlib
import importlib.util
import json
import re
import subprocess
from collections import Counter, defaultdict
from pathlib import Path, PurePosixPath
from typing import Any


FROZEN_PREFIXES = (
    "native_action_stage1_2026-07-18/",
    "native_action_stage2_2026-07-18/",
    "native_action_arm_c_2026-07-18/",
    "native_action_final_adjudication_2026-07-18/",
)
REORGANIZATION_PREFIXES = ("reorganization_r0/", "reorganization_r1a/", "reorganization_r1b/")
PROHIBITED_CATEGORIES = {"PYTHON_IMPORT", "FILE_PATH", "TEST", "STARTUP", "MANIFEST"}
UNRESOLVED_STATUSES = {"DYNAMIC", "DYNAMIC_OR_GLOB", "AMBIGUOUS_BASENAME", "MISSING_OR_GENERATED"}
NAVIGATION_SOURCES = {
    "AGENTS.md",
    "CLAUDE.md",
    "COGNITIVE_CORRAL_TRIGGERS_SETUP.md",
    "CROSS_MODEL_VERIFY.md",
    "FOUNDATIONAL_ASSUMPTIONS_LEDGER.md",
    "HANDOFF.md",
    "HANDOFF_ARCHIVE.md",
    "HYGIENE_HEADER_TEMPLATE.md",
    "INDEX.md",
    "LIVE.md",
    "MEMORY.md",
    "NEGATIVES_REGISTRY.md",
    "PROBLEM_STATEMENT.md",
    "PROVENANCE.md",
    "README.md",
    "STATE.md",
    "STRUCTURE_HYGIENE.md",
}
RUNTIME_SUFFIXES = {
    ".py", ".pyi", ".sh", ".bash", ".toml", ".yaml", ".yml", ".ini", ".cfg",
    ".json", ".csv", ".tsv", ".txt", ".log", ".npz", ".npy", ".pt", ".pth",
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


def load_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


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
    spec = importlib.util.spec_from_file_location("r1a_corrected_boundary_for_r1b", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def base_paths(repo: Path, base: str) -> list[str]:
    raw = str(execute(repo, ["git", "ls-tree", "-r", "-z", "--name-only", base]))
    return sorted(filter(None, raw.split("\0")))


def base_blob(repo: Path, base: str, path: str) -> bytes:
    return bytes(execute(repo, ["git", "show", f"{base}:{path}"], binary=True))


def text_snapshot(repo: Path, base: str) -> dict[str, str]:
    result = {}
    for path in base_paths(repo, base):
        payload = base_blob(repo, base, path)
        if b"\0" in payload[:8192]:
            continue
        try:
            result[path] = payload.decode("utf-8")
        except UnicodeDecodeError:
            continue
    return result


def line_details(text: str, offset: int) -> tuple[int, int, str]:
    line = text.count("\n", 0, offset) + 1
    start = text.rfind("\n", 0, offset) + 1
    end = text.find("\n", offset)
    if end < 0:
        end = len(text)
    return line, offset - start + 1, text[start:end].strip()[:500].rstrip()


def source_class(source: str, root_classes: dict[str, str]) -> str:
    basename = PurePosixPath(source).name
    suffix = PurePosixPath(source).suffix.lower()
    if source == "CANON.md" or source.startswith(FROZEN_PREFIXES):
        return "HARD_FROZEN_SOURCE"
    if root_classes.get(source) == "FROZEN_EVIDENCE":
        return "HARD_FROZEN_SOURCE"
    if source.startswith(REORGANIZATION_PREFIXES):
        return "HISTORICAL_SNAPSHOT_SOURCE"
    if (
        source.startswith("tests/")
        or suffix in RUNTIME_SUFFIXES
        or "manifest" in basename.lower()
        or "SHA256SUMS" in basename
    ):
        return "RUNTIME_OR_MANIFEST_IMMUTABLE"
    if source in NAVIGATION_SOURCES:
        return "MUTABLE_NAVIGATION_SOURCE"
    if suffix in {".md", ".rst"}:
        return "SOFT_EVIDENCE_PATH_ONLY_SOURCE"
    return "UNKNOWN_BLOCKING_SOURCE"


def operational_source(source: str) -> bool:
    return not source.startswith(REORGANIZATION_PREFIXES)


def expand_braces(pattern: str) -> list[str]:
    match = re.search(r"\{([^{}]+)\}", pattern)
    if not match:
        return [pattern]
    result = []
    for value in match.group(1).split(","):
        result.extend(expand_braces(pattern[: match.start()] + value + pattern[match.end() :]))
    return result


def unresolved_matches(candidate: str, edge: dict[str, str], repo: Path) -> bool:
    raw = edge["raw_target"].replace("\\n", "\n").strip().strip("'\"")
    resolved = edge["resolved_target"].replace("\\n", "\n").strip().strip("'\"")
    basename = PurePosixPath(candidate).name
    if raw in {candidate, basename} or resolved in {candidate, basename}:
        return True
    prefix = str(repo).rstrip("/") + "/"
    if raw.startswith(prefix):
        raw = raw[len(prefix):]
    if not any(character in raw for character in "*?{") or raw == "*":
        return False
    for pattern in expand_braces(raw):
        if "/" in pattern and fnmatch.fnmatch(candidate, pattern):
            return True
        if "/" not in pattern and fnmatch.fnmatch(basename, pattern):
            return True
    return False


def supersession_excerpt(text: str) -> str:
    expressions = (
        r"(?im)^.{0,80}\bSUPERSEDED\b.{0,240}$",
        r"(?im)^.{0,80}\bCONDITIONS-CHANGED\b.{0,240}$",
        r"(?im)^.{0,80}\b(?:ARCHIVED|RETIRED|PRE-NATIVE|IMPORT-ERA)\b.{0,240}$",
    )
    for expression in expressions:
        match = re.search(expression, text[:5000])
        if match:
            return match.group(0).strip()[:400]
    return "-"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--base", required=True)
    parser.add_argument("--candidate-table", type=Path, required=True)
    parser.add_argument("--frontier-registry", type=Path, required=True)
    parser.add_argument("--root-inventory", type=Path, required=True)
    parser.add_argument("--dependency-map", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()

    repo = args.repo.resolve()
    output = args.output_dir.resolve()
    output.mkdir(parents=True, exist_ok=True)
    matcher = load_matcher(repo)
    assert set(matcher.catchproof().values()) == {"PASS"}
    candidate_rows = load_tsv(args.candidate_table)
    candidates = [row["path"] for row in candidate_rows]
    candidate_set = set(candidates)
    assert len(candidates) == len(candidate_set) == 99
    inventory = load_tsv(args.root_inventory)
    root_classes = {row["path"]: row["classification"] for row in inventory}
    dependencies = load_tsv(args.dependency_map)
    frontier = {row["target"] for row in load_tsv(args.frontier_registry) if row["candidate_universe"] == "YES"}
    texts = text_snapshot(repo, args.base)

    references: list[dict[str, Any]] = []
    for source, text in sorted(texts.items()):
        immutable = source_class(source, root_classes)
        operational = operational_source(source)
        for target in candidates:
            for offset in matcher.occurrences(text, target):
                line, column, excerpt = line_details(text, offset)
                qualified = offset > 0 and text[offset - 1] == "/"
                references.append(
                    {
                        "target": target,
                        "source": source,
                        "line": line,
                        "column": column,
                        "source_immutability": immutable,
                        "source_formally_frozen": "YES" if immutable == "HARD_FROZEN_SOURCE" else "NO",
                        "forensic_scope": "YES",
                        "operational_scope": "YES" if operational else "NO",
                        "reference_role": "QUALIFIED_PATH_SUFFIX" if qualified else "ROOT_BASENAME_REFERENCE",
                        "line_excerpt": excerpt,
                    }
                )
    references.sort(key=lambda row: (row["target"], row["source"], row["line"], row["column"]))
    operational_references = [row for row in references if row["operational_scope"] == "YES"]

    sources: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in references:
        sources[row["source"]].append(row)
    source_rows = []
    for source, rows in sorted(sources.items()):
        source_rows.append(
            {
                "source": source,
                "immutability_class": rows[0]["source_immutability"],
                "forensic_occurrences": len(rows),
                "operational_occurrences": sum(row["operational_scope"] == "YES" for row in rows),
                "candidate_targets": ";".join(sorted({row["target"] for row in rows})),
                "root_basename_occurrences": sum(row["reference_role"] == "ROOT_BASENAME_REFERENCE" for row in rows),
                "qualified_suffix_occurrences": sum(row["reference_role"] == "QUALIFIED_PATH_SUFFIX" for row in rows),
                "source_sha256_at_base": sha256(base_blob(repo, args.base, source)),
            }
        )

    inbound_edges: dict[str, list[dict[str, str]]] = defaultdict(list)
    outbound_edges: dict[str, list[dict[str, str]]] = defaultdict(list)
    unresolved_edges: dict[str, list[dict[str, str]]] = defaultdict(list)
    for edge in dependencies:
        if not operational_source(edge["source"]):
            continue
        resolved = set(filter(None, edge["resolved_target"].split("|")))
        for candidate in candidate_set & resolved:
            inbound_edges[candidate].append(edge)
        if edge["source"] in candidate_set:
            outbound_edges[edge["source"]].append(edge)
        if edge["status"] in UNRESOLVED_STATUSES:
            for candidate in candidates:
                if unresolved_matches(candidate, edge, repo):
                    unresolved_edges[candidate].append(edge)

    refs_by_target: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in operational_references:
        refs_by_target[row["target"]].append(row)
    evidence_rows = []
    for registered in candidate_rows:
        path = registered["path"]
        inbound = refs_by_target[path]
        root_refs = [row for row in inbound if row["reference_role"] == "ROOT_BASENAME_REFERENCE"]
        hard = sorted({row["source"] for row in root_refs if row["source_immutability"] == "HARD_FROZEN_SOURCE"})
        runtime = sorted(
            {row["source"] for row in root_refs if row["source_immutability"] in {"RUNTIME_OR_MANIFEST_IMMUTABLE", "UNKNOWN_BLOCKING_SOURCE"}}
        )
        editable = sorted(
            {row["source"] for row in root_refs if row["source_immutability"] in {"MUTABLE_NAVIGATION_SOURCE", "SOFT_EVIDENCE_PATH_ONLY_SOURCE"}}
        )
        prohibited = [
            edge for edge in inbound_edges[path] + outbound_edges[path]
            if edge["category"] in PROHIBITED_CATEGORIES
        ]
        text = texts[path]
        evidence_rows.append(
            {
                **registered,
                "r0_classification": root_classes.get(path, "-"),
                "current_frontier_target": "YES" if path in frontier else "NO",
                "forensic_occurrences": sum(row["target"] == path for row in references),
                "operational_occurrences": len(inbound),
                "operational_root_references": len(root_refs),
                "hard_frozen_root_sources": ";".join(hard) or "-",
                "runtime_or_unknown_root_sources": ";".join(runtime) or "-",
                "editable_root_sources": ";".join(editable) or "-",
                "prohibited_dependency_edges": len(prohibited),
                "prohibited_dependency_categories": ";".join(sorted({edge["category"] for edge in prohibited})) or "-",
                "unresolved_dynamic_touches": len(unresolved_edges[path]),
                "destination": "archive/pre_2026-07-01/" + path,
                "destination_collision_at_base": "YES" if "archive/pre_2026-07-01/" + path in texts else "NO",
                "supersession_excerpt": supersession_excerpt(text),
            }
        )

    write_tsv(
        output / "BASE_INBOUND_REFERENCES_FORENSIC.tsv",
        references,
        (
            "target", "source", "line", "column", "source_immutability",
            "source_formally_frozen", "forensic_scope", "operational_scope",
            "reference_role", "line_excerpt",
        ),
    )
    write_tsv(
        output / "BASE_INBOUND_REFERENCES_OPERATIONAL.tsv",
        operational_references,
        (
            "target", "source", "line", "column", "source_immutability",
            "source_formally_frozen", "forensic_scope", "operational_scope",
            "reference_role", "line_excerpt",
        ),
    )
    write_tsv(
        output / "INBOUND_SOURCE_IMMUTABILITY_REGISTRY.tsv",
        source_rows,
        (
            "source", "immutability_class", "forensic_occurrences", "operational_occurrences",
            "candidate_targets", "root_basename_occurrences", "qualified_suffix_occurrences",
            "source_sha256_at_base",
        ),
    )
    evidence_fields = tuple(evidence_rows[0])
    write_tsv(output / "CANDIDATE_EVIDENCE.tsv", evidence_rows, evidence_fields)

    full_dependency_counts = Counter(edge["category"] for edge in dependencies)
    operational_dependencies = [edge for edge in dependencies if operational_source(edge["source"])]
    operational_dependency_counts = Counter(edge["category"] for edge in operational_dependencies)
    report = {
        "result": "PASS",
        "mode": "R1B_FIXED_BASE_FORENSIC_AND_OPERATIONAL_CENSUS",
        "base": args.base,
        "candidates": len(candidates),
        "corrected_matcher_catchproof": matcher.catchproof(),
        "forensic_inbound_occurrences": len(references),
        "forensic_inbound_sources": len(sources),
        "operational_inbound_occurrences": len(operational_references),
        "operational_inbound_sources": len({row["source"] for row in operational_references}),
        "source_immutability_counts": dict(sorted(Counter(row["immutability_class"] for row in source_rows).items())),
        "full_forensic_dependency_edges": len(dependencies),
        "full_forensic_dependency_category_counts": dict(sorted(full_dependency_counts.items())),
        "operational_dependency_edges": len(operational_dependencies),
        "operational_dependency_category_counts": dict(sorted(operational_dependency_counts.items())),
        "operational_exclusion_prefixes": list(REORGANIZATION_PREFIXES),
        "generated_records_influence_candidate_selection": False,
    }
    (output / "BASE_CENSUS_SUMMARY.json").write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
