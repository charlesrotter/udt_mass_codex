#!/usr/bin/env python3
"""Build the frozen pre-move R1A candidate and inbound-reference adjudication."""

from __future__ import annotations

import argparse
import csv
import fnmatch
import hashlib
import json
import re
import subprocess
from collections import Counter, defaultdict
from pathlib import Path, PurePosixPath
from typing import Any


REVIEW_CLASSES = {"ARCHIVE_CANDIDATE", "UNKNOWN/BLOCKED"}
PROHIBITED_EDGE_CATEGORIES = {"PYTHON_IMPORT", "FILE_PATH", "TEST", "STARTUP", "MANIFEST"}
UNRESOLVED_STATUSES = {
    "DYNAMIC",
    "DYNAMIC_OR_GLOB",
    "AMBIGUOUS_BASENAME",
    "MISSING_OR_GENERATED",
}
FROZEN_PREFIXES = (
    "native_action_stage1_2026-07-18/",
    "native_action_stage2_2026-07-18/",
    "native_action_arm_c_2026-07-18/",
    "native_action_final_adjudication_2026-07-18/",
)
R0_SNAPSHOT_PREFIX = "reorganization_r0/"
ARCHIVE_TARGET_PREFIX = "archive/pre_2026-07-01/"
CUTOFF = "2026-07-01"


def run(repo: Path, arguments: list[str]) -> str:
    completed = subprocess.run(
        arguments,
        cwd=repo,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if completed.returncode:
        raise RuntimeError(
            f"command failed ({completed.returncode}): {' '.join(arguments)}\n{completed.stderr}"
        )
    return completed.stdout


def load_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


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


def sha256(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def is_text(payload: bytes) -> bool:
    if b"\x00" in payload[:8192]:
        return False
    try:
        payload.decode("utf-8")
    except UnicodeDecodeError:
        return False
    return True


def git_history(repo: Path, path: str) -> tuple[str, str, str, str]:
    lines = run(
        repo,
        ["git", "log", "--follow", "--format=%cs%x09%H%x09%s", "--", path],
    ).splitlines()
    if not lines:
        return "-", "-", "-", "-"
    newest = lines[0].split("\t", 2)
    oldest = lines[-1].split("\t", 2)
    return oldest[0], newest[0], newest[1], newest[2]


def source_is_frozen(source: str, root_classes: dict[str, str]) -> bool:
    return root_classes.get(source) == "FROZEN_EVIDENCE" or source.startswith(FROZEN_PREFIXES)


def expand_one_brace(pattern: str) -> list[str]:
    match = re.search(r"\{([^{}]+)\}", pattern)
    if not match:
        return [pattern]
    values = match.group(1).split(",")
    expanded: list[str] = []
    for value in values:
        expanded.extend(
            expand_one_brace(pattern[: match.start()] + value + pattern[match.end() :])
        )
    return expanded


def unresolved_matches(candidate: str, edge: dict[str, str], repo: Path) -> bool:
    raw = edge["raw_target"].replace("\\n", "\n").strip().strip("'\"")
    resolved = edge["resolved_target"].replace("\\n", "\n").strip().strip("'\"")
    basename = PurePosixPath(candidate).name
    if raw in {candidate, basename} or resolved in {candidate, basename}:
        return True
    repo_prefix = str(repo).rstrip("/") + "/"
    if raw.startswith(repo_prefix):
        raw = raw[len(repo_prefix) :]
    if not any(character in raw for character in "*?{") or raw == "*":
        return False
    for pattern in expand_one_brace(raw):
        if "/" in pattern:
            if fnmatch.fnmatch(candidate, pattern):
                return True
        elif fnmatch.fnmatch(basename, pattern):
            return True
    return False


def unknown_role(path: str) -> str:
    if path.endswith(".pt"):
        return "OPAQUE_TORCH_ARTIFACT"
    if path.endswith(".png"):
        return "PROVENANCE_IMAGE"
    if path.endswith(".txt"):
        return "NUMERICAL_LOG"
    if path.endswith(".out"):
        return "RUNTIME_OUTPUT"
    if path.endswith(".json"):
        if path.startswith("noNull_"):
            return "PARTICLE_MASS_NUMERICAL_JSON"
        if path.startswith("simple_metric_"):
            return "MACRO_NUMERICAL_JSON"
        if path.startswith("cascade_"):
            return "CASCADE_NUMERICAL_JSON"
        if path.startswith("u_plat_"):
            return "PLATEAU_NUMERICAL_JSON"
        return "NUMERICAL_JSON"
    return "OPAQUE_OR_UNRESOLVED"


def title_of(path: str, payload: bytes) -> str:
    if not path.endswith(".md"):
        return unknown_role(path)
    text = payload.decode("utf-8", "replace")
    for line in text.splitlines()[:80]:
        stripped = line.strip().lstrip("> ").strip()
        if stripped.startswith("#"):
            return stripped.lstrip("# ")[:240]
    for line in text.splitlines()[:20]:
        if line.strip():
            return line.strip()[:240]
    return "UNTITLED_MARKDOWN"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--r0-inventory", type=Path, required=True)
    parser.add_argument("--r0-dependencies", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    arguments = parser.parse_args()

    repo = arguments.repo.resolve()
    output_dir = arguments.output_dir.resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    inventory = load_tsv(arguments.r0_inventory)
    dependency_rows = load_tsv(arguments.r0_dependencies)
    root_classes = {row["path"]: row["classification"] for row in inventory}
    candidates = {
        row["path"]: row for row in inventory if row["classification"] in REVIEW_CLASSES
    }
    if Counter(row["classification"] for row in candidates.values()) != Counter(
        {"ARCHIVE_CANDIDATE": 26, "UNKNOWN/BLOCKED": 37}
    ):
        raise AssertionError("R0 review set is not exactly 26 archive + 37 unknown")

    tracked = run(repo, ["git", "ls-files", "-z"]).split("\0")
    tracked = [path for path in tracked if path]
    payloads = {path: (repo / path).read_bytes() for path in tracked}
    candidate_pattern = re.compile(
        r"(?<![A-Za-z0-9_.-])(?P<target>"
        + "|".join(re.escape(path) for path in sorted(candidates, key=len, reverse=True))
        + r")(?![A-Za-z0-9_.-])"
    )

    references: list[dict[str, Any]] = []
    for source in sorted(tracked):
        payload = payloads[source]
        if not is_text(payload):
            continue
        text = payload.decode("utf-8")
        starts = [0]
        starts.extend(match.end() for match in re.finditer("\n", text))
        for match in candidate_pattern.finditer(text):
            line = text.count("\n", 0, match.start()) + 1
            line_start = starts[line - 1]
            line_end = text.find("\n", match.end())
            if line_end < 0:
                line_end = len(text)
            excerpt = text[line_start:line_end].strip()[:500]
            target = match.group("target")
            matching_edges = [
                edge
                for edge in dependency_rows
                if edge["source"] == source
                and edge["resolved_target"] == target
                and str(edge["line"]) == str(line)
            ]
            categories = ";".join(sorted({edge["category"] for edge in matching_edges})) or "TEXT_SCAN"
            kinds = ";".join(sorted({edge["kind"] for edge in matching_edges})) or "EXACT_TEXT"
            statuses = ";".join(sorted({edge["status"] for edge in matching_edges})) or "RESOLVED_EXACT"
            references.append(
                {
                    "target": target,
                    "source": source,
                    "line": line,
                    "column": match.start() - line_start + 1,
                    "categories": categories,
                    "kinds": kinds,
                    "statuses": statuses,
                    "source_frozen": "YES" if source_is_frozen(source, root_classes) else "NO",
                    "source_r0_classification": root_classes.get(source, "NON_ROOT"),
                    "line_excerpt": excerpt,
                }
            )

    inbound_by_target: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in references:
        inbound_by_target[row["target"]].append(row)

    prohibited_by_target: dict[str, list[dict[str, str]]] = defaultdict(list)
    unresolved_by_target: dict[str, list[dict[str, str]]] = defaultdict(list)
    outbound_by_source: dict[str, list[dict[str, str]]] = defaultdict(list)
    for edge in dependency_rows:
        if edge["resolved_target"] in candidates and edge["category"] in PROHIBITED_EDGE_CATEGORIES:
            prohibited_by_target[edge["resolved_target"]].append(edge)
        if edge["source"] in candidates and edge["category"] in PROHIBITED_EDGE_CATEGORIES:
            outbound_by_source[edge["source"]].append(edge)
        if edge["status"] in UNRESOLVED_STATUSES:
            for candidate in candidates:
                if unresolved_matches(candidate, edge, repo):
                    unresolved_by_target[candidate].append(edge)

    decisions: dict[str, str] = {}
    rows: list[dict[str, Any]] = []
    premove_hashes: list[dict[str, Any]] = []
    for path in sorted(candidates):
        r0 = candidates[path]
        payload = payloads[path]
        first_date, last_date, last_hash, last_subject = git_history(repo, path)
        inbound = inbound_by_target[path]
        frozen_sources = sorted({row["source"] for row in inbound if row["source_frozen"] == "YES"})
        prohibited = prohibited_by_target[path] + outbound_by_source[path]
        unresolved = unresolved_by_target[path]
        destination = ARCHIVE_TARGET_PREFIX + path
        collision = destination in payloads or (repo / destination).exists()
        blockers: list[str] = []
        role = title_of(path, payload)
        if r0["classification"] == "UNKNOWN/BLOCKED":
            blockers.append(f"R0_UNKNOWN:{unknown_role(path)}")
        if not path.endswith(".md"):
            blockers.append("NOT_MARKDOWN_TEXT_RECORD")
        if first_date >= CUTOFF:
            blockers.append(f"FIRST_COMMIT_NOT_PRE_CUTOFF:{first_date}")
        if prohibited:
            blockers.append(
                "PROHIBITED_DEPENDENCY:"
                + ",".join(
                    sorted({f"{edge['category']}:{edge['source']}" for edge in prohibited})
                )
            )
        if frozen_sources:
            blockers.append("FROZEN_INBOUND:" + ",".join(frozen_sources))
        if unresolved:
            blockers.append(
                "UNRESOLVED_PATH_TOUCH:"
                + ",".join(sorted({f"{edge['source']}:{edge['line']}" for edge in unresolved}))
            )
        if collision:
            blockers.append("DESTINATION_COLLISION")

        if not blockers and r0["classification"] == "ARCHIVE_CANDIDATE":
            disposition = "MOVE_BATCH_1"
            rationale = (
                f"Pre-cutoff superseded text record ({role}); no runtime, manifest, frozen-source, "
                "or unresolved-path dependency; non-frozen pointers are atomically rewritable."
            )
        else:
            disposition = "RETAIN_R1A"
            rationale = f"Retain {role}; " + "; ".join(blockers)
        decisions[path] = disposition
        rows.append(
            {
                "path": path,
                "r0_classification": r0["classification"],
                "artifact_role_or_title": role,
                "size_bytes": len(payload),
                "git_blob_oid": r0["git_blob_oid"],
                "sha256": sha256(payload),
                "first_commit_date": first_date,
                "last_commit_date": last_date,
                "last_commit": last_hash,
                "last_commit_subject": last_subject,
                "inbound_occurrences": len(inbound),
                "inbound_sources": len({row["source"] for row in inbound}),
                "frozen_inbound_sources": ";".join(frozen_sources) or "-",
                "prohibited_dependency_edges": len(prohibited),
                "unresolved_path_touches": len(unresolved),
                "destination": destination if disposition == "MOVE_BATCH_1" else "-",
                "disposition": disposition,
                "rationale": rationale,
            }
        )
        if disposition == "MOVE_BATCH_1":
            premove_hashes.append(
                {
                    "old_path": path,
                    "new_path": destination,
                    "git_blob_oid": r0["git_blob_oid"],
                    "sha256_before": sha256(payload),
                    "size_bytes": len(payload),
                }
            )

    eligible = {path for path, decision in decisions.items() if decision == "MOVE_BATCH_1"}
    for row in references:
        source = row["source"]
        target = row["target"]
        if row["source_frozen"] == "YES":
            role = "FROZEN_SOURCE"
            rewrite = "NO"
        elif source.startswith(R0_SNAPSHOT_PREFIX):
            role = "R0_HISTORICAL_SNAPSHOT"
            rewrite = "NO"
        elif source == target:
            role = "SELF_PROVENANCE_REFERENCE"
            rewrite = "NO"
        elif source in eligible and target in eligible:
            role = "SAME_BATCH_COLOCATED_REFERENCE"
            rewrite = "NO"
        elif target in eligible:
            role = "NON_FROZEN_LIVE_POINTER"
            rewrite = "YES"
        else:
            role = "RETAINED_TARGET_REFERENCE"
            rewrite = "NO"
        row["reference_role"] = role
        row["rewrite_required"] = rewrite
        row["new_target"] = ARCHIVE_TARGET_PREFIX + target if target in eligible else "-"

    rewrite_groups: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    for row in references:
        if row["rewrite_required"] == "YES":
            rewrite_groups[(row["source"], row["target"])].append(row)
    rewrite_plan = []
    for (source, target), group in sorted(rewrite_groups.items()):
        rewrite_plan.append(
            {
                "source": source,
                "old_target": target,
                "new_target": ARCHIVE_TARGET_PREFIX + target,
                "occurrences": len(group),
                "lines": ";".join(str(row["line"]) for row in group),
                "source_frozen": "NO",
                "rewrite_mode": "EXACT_PATH_TOKEN_ONLY",
            }
        )

    write_tsv(
        output_dir / "CANDIDATE_ADJUDICATION.tsv",
        rows,
        [
            "path",
            "r0_classification",
            "artifact_role_or_title",
            "size_bytes",
            "git_blob_oid",
            "sha256",
            "first_commit_date",
            "last_commit_date",
            "last_commit",
            "last_commit_subject",
            "inbound_occurrences",
            "inbound_sources",
            "frozen_inbound_sources",
            "prohibited_dependency_edges",
            "unresolved_path_touches",
            "destination",
            "disposition",
            "rationale",
        ],
    )
    write_tsv(
        output_dir / "INBOUND_REFERENCES.tsv",
        sorted(references, key=lambda row: (row["target"], row["source"], row["line"], row["column"])),
        [
            "target",
            "source",
            "line",
            "column",
            "categories",
            "kinds",
            "statuses",
            "source_frozen",
            "source_r0_classification",
            "reference_role",
            "rewrite_required",
            "new_target",
            "line_excerpt",
        ],
    )
    write_tsv(
        output_dir / "PREMOVE_HASHES.tsv",
        premove_hashes,
        ["old_path", "new_path", "git_blob_oid", "sha256_before", "size_bytes"],
    )
    write_tsv(
        output_dir / "POINTER_REWRITE_PLAN.tsv",
        rewrite_plan,
        [
            "source",
            "old_target",
            "new_target",
            "occurrences",
            "lines",
            "source_frozen",
            "rewrite_mode",
        ],
    )
    (output_dir / "ELIGIBLE_BATCH.txt").write_text(
        "".join(path + "\n" for path in sorted(eligible)), encoding="utf-8"
    )

    summary = {
        "base_commit": run(repo, ["git", "rev-parse", "HEAD"]).strip(),
        "candidate_rows": len(rows),
        "r0_classification_counts": dict(sorted(Counter(row["r0_classification"] for row in rows).items())),
        "disposition_counts": dict(sorted(Counter(row["disposition"] for row in rows).items())),
        "inbound_reference_occurrences": len(references),
        "inbound_reference_sources": len({row["source"] for row in references}),
        "frozen_reference_occurrences": sum(row["source_frozen"] == "YES" for row in references),
        "pointer_rewrite_groups": len(rewrite_plan),
        "pointer_rewrite_occurrences": sum(int(row["occurrences"]) for row in rewrite_plan),
        "eligible_batch": sorted(eligible),
        "result": "PREMOVE_ADJUDICATION_FROZEN",
    }
    (output_dir / "ADJUDICATION_SUMMARY.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    archive_rows = [row for row in rows if row["r0_classification"] == "ARCHIVE_CANDIDATE"]
    unknown_rows = [row for row in rows if row["r0_classification"] == "UNKNOWN/BLOCKED"]
    report = [
        "# R1A pre-move candidate adjudication",
        "",
        f"Snapshot: `{summary['base_commit']}`. This is the frozen first adjudicator run.",
        "",
        "Every one of the 26 R0 archive candidates and 37 R0 unknown/blocked paths is",
        "listed below. `INBOUND_REFERENCES.tsv` records every exact occurrence and",
        "states whether its source is frozen. `POINTER_REWRITE_PLAN.tsv` is the complete",
        "non-frozen live-pointer rewrite set for the first batch.",
        "",
        "## Outcome",
        "",
        f"- First safe batch: {len(eligible)} files.",
        f"- Retained in R1A: {len(rows) - len(eligible)} files.",
        f"- Exact inbound occurrences: {len(references)} across "
        f"{len({row['source'] for row in references})} sources.",
        f"- Frozen-source occurrences: {sum(row['source_frozen'] == 'YES' for row in references)}.",
        f"- Required pointer substitutions: {sum(int(row['occurrences']) for row in rewrite_plan)} "
        f"occurrences in {len(rewrite_plan)} source/target groups.",
        "",
        "## All 26 archive candidates",
        "",
        "| Path | First commit | Inbound occurrences | Frozen sources | Disposition | Individual ruling |",
        "|---|---|---:|---|---|---|",
    ]
    for row in archive_rows:
        report.append(
            "| `{}` | `{}` | {} | {} | `{}` | {} |".format(
                row["path"],
                row["first_commit_date"],
                row["inbound_occurrences"],
                row["frozen_inbound_sources"],
                row["disposition"],
                row["rationale"].replace("|", "\\|"),
            )
        )
    report.extend(
        [
            "",
            "## All 37 unknown/blocked paths",
            "",
            "No unknown/blocked path is moved in R1A. Opaque artifacts are not",
            "deserialized and numerical outputs are not reinterpreted as archival merely",
            "because they have no exact inbound reference.",
            "",
            "| Path | Artifact role | Inbound occurrences | Disposition | Individual ruling |",
            "|---|---|---:|---|---|",
        ]
    )
    for row in unknown_rows:
        report.append(
            "| `{}` | `{}` | {} | `{}` | {} |".format(
                row["path"],
                row["artifact_role_or_title"],
                row["inbound_occurrences"],
                row["disposition"],
                row["rationale"].replace("|", "\\|"),
            )
        )
    report.extend(
        [
            "",
            "## Interpretation boundary",
            "",
            "A `MOVE_BATCH_1` ruling means only that the path satisfies the",
            "preregistered topology predicate. It does not alter or endorse the record's",
            "physics. A `RETAIN_R1A` ruling is a conservative location decision, not a",
            "claim that the file is active or canonical.",
            "",
        ]
    )
    (output_dir / "PREMOVE_ADJUDICATION_REPORT.md").write_text(
        "\n".join(report), encoding="utf-8"
    )
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
