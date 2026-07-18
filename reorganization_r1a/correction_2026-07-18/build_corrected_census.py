#!/usr/bin/env python3
"""Build corrected, additive R1A reference and adjudication tables."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import subprocess
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

from reference_boundary import catchproof, occurrences


FROZEN_PREFIXES = (
    "native_action_stage1_2026-07-18/",
    "native_action_stage2_2026-07-18/",
    "native_action_arm_c_2026-07-18/",
    "native_action_final_adjudication_2026-07-18/",
)
EXPECTED_LIVE_REWRITES = {
    ("HANDOFF_ARCHIVE.md", "PROVENANCE_AUDIT_2026-06-30.md"),
    ("FOUNDATIONAL_ASSUMPTIONS_LEDGER.md", "STEP2_timelive_matter_results.md"),
    ("HANDOFF_ARCHIVE.md", "coupled_timelive_VERIFIER.md"),
    ("archive/tier_d_round3_contract.md", "lepton_ladder_test_results.md"),
    ("NEGATIVES_REGISTRY.md", "weld_discriminator_results.md"),
}
COLOCATED_REFERENCE = (
    "archive/pre_native_coupled/timelive_nonround_native_solve_results.md",
    "timelive_nonround_VERIFIER.md",
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
        raise RuntimeError(f"command failed: {' '.join(command)}\n{stderr}")
    return completed.stdout


def load_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


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
        for row in rows:
            writer.writerow(
                {
                    field: str(row.get(field, "-")).replace("\t", "\\t").replace("\n", "\\n")
                    for field in fields
                }
            )


def source_frozen(source: str, classes: dict[str, str]) -> bool:
    return classes.get(source) == "FROZEN_EVIDENCE" or source.startswith(FROZEN_PREFIXES)


def snapshot_paths(repo: Path, revision: str) -> list[str]:
    raw = str(execute(repo, ["git", "ls-tree", "-r", "-z", "--name-only", revision]))
    return [path for path in raw.split("\0") if path]


def blob(repo: Path, revision: str, path: str) -> bytes:
    return bytes(execute(repo, ["git", "show", f"{revision}:{path}"], binary=True))


def text_snapshot(repo: Path, revision: str) -> dict[str, str]:
    result: dict[str, str] = {}
    for path in snapshot_paths(repo, revision):
        payload = blob(repo, revision, path)
        if b"\x00" in payload[:8192]:
            continue
        try:
            result[path] = payload.decode("utf-8")
        except UnicodeDecodeError:
            continue
    return result


def line_details(text: str, offset: int) -> tuple[int, int, str]:
    line = text.count("\n", 0, offset) + 1
    line_start = text.rfind("\n", 0, offset) + 1
    line_end = text.find("\n", offset)
    if line_end < 0:
        line_end = len(text)
    return line, offset - line_start + 1, text[line_start:line_end].strip()[:500]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--base", required=True)
    parser.add_argument("--r0-inventory", type=Path, required=True)
    parser.add_argument("--original-adjudication", type=Path, required=True)
    parser.add_argument("--original-references", type=Path, required=True)
    parser.add_argument("--original-rewrite-plan", type=Path, required=True)
    parser.add_argument("--move-map", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()

    repo = args.repo.resolve()
    output = args.output_dir.resolve()
    output.mkdir(parents=True, exist_ok=True)
    inventory = load_tsv(args.r0_inventory)
    original_adjudication = load_tsv(args.original_adjudication)
    original_references = load_tsv(args.original_references)
    original_rewrite_plan = load_tsv(args.original_rewrite_plan)
    move_map = load_tsv(args.move_map)
    classes = {row["path"]: row["classification"] for row in inventory}
    candidates = {row["path"] for row in original_adjudication}
    moved = {row["old_path"]: row["new_path"] for row in move_map}
    texts = text_snapshot(repo, args.base)

    corrected: list[dict[str, Any]] = []
    for source, text in sorted(texts.items()):
        for target in sorted(candidates):
            for offset in occurrences(text, target):
                line, column, excerpt = line_details(text, offset)
                corrected.append(
                    {
                        "target": target,
                        "source": source,
                        "line": line,
                        "column": column,
                        "source_frozen": "YES" if source_frozen(source, classes) else "NO",
                        "source_r0_classification": classes.get(source, "NON_ROOT"),
                        "line_excerpt": excerpt,
                    }
                )
    corrected.sort(key=lambda row: (row["target"], row["source"], row["line"], row["column"]))

    original_keys = {
        (row["target"], row["source"], int(row["line"]), int(row["column"]))
        for row in original_references
    }
    corrected_keys = {
        (row["target"], row["source"], int(row["line"]), int(row["column"]))
        for row in corrected
    }
    if not original_keys < corrected_keys:
        raise AssertionError("original reference keys are not a strict subset")
    omitted_keys = corrected_keys - original_keys
    if len(omitted_keys) != 14:
        raise AssertionError(f"expected 14 omissions, found {len(omitted_keys)}")

    omissions: list[dict[str, Any]] = []
    for row in corrected:
        key = (row["target"], row["source"], int(row["line"]), int(row["column"]))
        if key not in omitted_keys:
            continue
        pair = (row["source"], row["target"])
        if pair in EXPECTED_LIVE_REWRITES:
            disposition = "REWRITE_LIVE_POINTER"
            new_target = moved[row["target"]]
        elif pair == COLOCATED_REFERENCE:
            disposition = "INTENTIONAL_COLOCATED_ARCHIVE_REFERENCE"
            new_target = "UNCHANGED_COLOCATED_BASENAME"
        elif row["target"] not in moved:
            disposition = "RETAINED_TARGET_NO_REWRITE"
            new_target = "RETAINED_AT_ROOT"
        else:
            raise AssertionError(f"unclassified omission: {pair}")
        omissions.append(
            {
                **row,
                "disposition": disposition,
                "new_target_or_reason": new_target,
            }
        )

    disposition_counts = Counter(row["disposition"] for row in omissions)
    expected_dispositions = Counter(
        {
            "REWRITE_LIVE_POINTER": 5,
            "INTENTIONAL_COLOCATED_ARCHIVE_REFERENCE": 1,
            "RETAINED_TARGET_NO_REWRITE": 8,
        }
    )
    if disposition_counts != expected_dispositions:
        raise AssertionError(f"wrong omission dispositions: {disposition_counts}")

    inbound_by_target: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in corrected:
        inbound_by_target[row["target"]].append(row)
    consolidated = []
    for original in original_adjudication:
        inbound = inbound_by_target[original["path"]]
        frozen_sources = sorted({row["source"] for row in inbound if row["source_frozen"] == "YES"})
        eligible_recheck = (
            "PASS_UNCHANGED"
            if original["disposition"] == "MOVE_BATCH_1" and not frozen_sources
            else "RETAIN_UNCHANGED"
        )
        consolidated.append(
            {
                **original,
                "corrected_inbound_occurrences": len(inbound),
                "corrected_inbound_sources": len({row["source"] for row in inbound}),
                "corrected_frozen_inbound_sources": ";".join(frozen_sources) or "-",
                "corrected_eligibility_recheck": eligible_recheck,
            }
        )
    if sum(row["corrected_eligibility_recheck"] == "PASS_UNCHANGED" for row in consolidated) != 17:
        raise AssertionError("corrected census changed the 17-file eligible set")

    corrected_rewrite_plan = [dict(row, correction_layer="ORIGINAL_R1A") for row in original_rewrite_plan]
    for row in omissions:
        if row["disposition"] != "REWRITE_LIVE_POINTER":
            continue
        corrected_rewrite_plan.append(
            {
                "source": row["source"],
                "old_target": row["target"],
                "new_target": moved[row["target"]],
                "occurrences": 1,
                "lines": row["line"],
                "source_frozen": row["source_frozen"],
                "rewrite_mode": "EXACT_PATH_TOKEN_ONLY",
                "correction_layer": "BOUNDARY_CORRECTION_2026-07-18",
            }
        )
    corrected_rewrite_plan.sort(key=lambda row: (row["source"], row["old_target"]))

    write_tsv(
        output / "CORRECTED_INBOUND_REFERENCES.tsv",
        corrected,
        [
            "target",
            "source",
            "line",
            "column",
            "source_frozen",
            "source_r0_classification",
            "line_excerpt",
        ],
    )
    write_tsv(
        output / "OMISSION_LEDGER.tsv",
        omissions,
        [
            "target",
            "source",
            "line",
            "column",
            "source_frozen",
            "source_r0_classification",
            "disposition",
            "new_target_or_reason",
            "line_excerpt",
        ],
    )
    fields = list(original_adjudication[0]) + [
        "corrected_inbound_occurrences",
        "corrected_inbound_sources",
        "corrected_frozen_inbound_sources",
        "corrected_eligibility_recheck",
    ]
    write_tsv(output / "CORRECTED_CONSOLIDATED_ADJUDICATION.tsv", consolidated, fields)
    write_tsv(
        output / "CORRECTED_CONSOLIDATED_POINTER_PLAN.tsv",
        corrected_rewrite_plan,
        [
            "source",
            "old_target",
            "new_target",
            "occurrences",
            "lines",
            "source_frozen",
            "rewrite_mode",
            "correction_layer",
        ],
    )

    summary = {
        "result": "CORRECTED_CENSUS_BUILT",
        "base": str(execute(repo, ["git", "rev-parse", args.base])).strip(),
        "corrected_occurrences": len(corrected),
        "corrected_sources": len({row["source"] for row in corrected}),
        "corrected_frozen_source_occurrences": sum(
            row["source_frozen"] == "YES" for row in corrected
        ),
        "omitted_occurrences_recovered": len(omissions),
        "omission_dispositions": dict(sorted(disposition_counts.items())),
        "moved_files_still_eligible": 17,
        "consolidated_pointer_occurrences": sum(
            int(row["occurrences"]) for row in corrected_rewrite_plan
        ),
        "boundary_catchproof": catchproof(),
        "historical_tables_modified": False,
    }
    if (
        summary["corrected_occurrences"],
        summary["corrected_sources"],
        summary["corrected_frozen_source_occurrences"],
    ) != (815, 92, 16):
        raise AssertionError(f"corrected totals mismatch: {summary}")
    (output / "CORRECTED_SUMMARY.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
