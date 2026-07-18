#!/usr/bin/env python3
"""Independent literal-git-grep verifier for the corrected R1A census."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import subprocess
from collections import Counter
from pathlib import Path
from typing import Any, Callable


FROZEN_PREFIXES = (
    "native_action_stage1_2026-07-18/",
    "native_action_stage2_2026-07-18/",
    "native_action_arm_c_2026-07-18/",
    "native_action_final_adjudication_2026-07-18/",
)
HISTORICAL_ARTIFACTS = (
    "reorganization_r1a/ADJUDICATION_SUMMARY.json",
    "reorganization_r1a/CANDIDATE_ADJUDICATION.tsv",
    "reorganization_r1a/ELIGIBLE_BATCH.txt",
    "reorganization_r1a/INBOUND_REFERENCES.tsv",
    "reorganization_r1a/POINTER_REWRITE_PLAN.tsv",
    "reorganization_r1a/PREMOVE_HASHES.tsv",
    "reorganization_r1a/PREMOVE_ADJUDICATION_REPORT.md",
    "reorganization_r1a/PREMOVE_VERIFY_RESULT.json",
    "reorganization_r1a/MOVE_MAP.tsv",
    "reorganization_r1a/POSTMOVE_POINTER_CENSUS.tsv",
)


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


def git_show(repo: Path, revision: str, path: str) -> bytes:
    return subprocess.check_output(["git", "show", f"{revision}:{path}"], cwd=repo)


def source_frozen(source: str, classes: dict[str, str]) -> bool:
    return classes.get(source) == "FROZEN_EVIDENCE" or source.startswith(FROZEN_PREFIXES)


def literal_boundary_positions(line: str, token: str) -> list[int]:
    """Independent boundary implementation; does not import the production matcher."""

    left_forbidden = set("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_.-")
    suffix_characters = set("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_-")
    result = []
    search_from = 0
    while True:
        at = line.find(token, search_from)
        if at < 0:
            return result
        left_ok = at == 0 or line[at - 1] not in left_forbidden
        end = at + len(token)
        if end == len(line):
            right_ok = True
        elif line[end] in suffix_characters:
            right_ok = False
        elif line[end] == "." and end + 1 < len(line):
            right_ok = line[end + 1] not in suffix_characters
        else:
            right_ok = True
        if left_ok and right_ok:
            result.append(at)
        search_from = at + len(token)


def git_grep_rows(
    repo: Path, revision: str, candidates: set[str], classes: dict[str, str]
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for target in sorted(candidates):
        completed = subprocess.run(
            [
                "git",
                "grep",
                "-n",
                "--column",
                "-I",
                "-F",
                "-e",
                target,
                revision,
                "--",
            ],
            cwd=repo,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        if completed.returncode not in {0, 1}:
            raise AssertionError(completed.stderr)
        for output_line in completed.stdout.splitlines():
            _, path, line_text, _, content = output_line.split(":", 4)
            line = int(line_text)
            for offset in literal_boundary_positions(content, target):
                rows.append(
                    {
                        "target": target,
                        "source": path,
                        "line": line,
                        "column": offset + 1,
                        "source_frozen": "YES" if source_frozen(path, classes) else "NO",
                        "literal_git_grep": "MATCH",
                    }
                )
    rows.sort(key=lambda row: (row["target"], row["source"], row["line"], row["column"]))
    return rows


def occurrence_key(row: dict[str, Any]) -> tuple[str, str, int, int, str]:
    return (
        row["target"],
        row["source"],
        int(row["line"]),
        int(row["column"]),
        row["source_frozen"],
    )


def validate_contract(matcher: Callable[[str, str], list[int]]) -> None:
    assert matcher("See file.md.", "file.md")
    assert matcher("See file.md)", "file.md")
    assert not matcher("Backup file.md.bak", "file.md")


def rejected(check: Callable[[], None]) -> str:
    try:
        check()
    except AssertionError:
        return "PASS"
    raise AssertionError("catch-proof mutation was accepted")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--base", required=True)
    parser.add_argument("--correction-base", required=True)
    parser.add_argument("--r0-inventory", type=Path, required=True)
    parser.add_argument("--original-references", type=Path, required=True)
    parser.add_argument("--corrected-references", type=Path, required=True)
    parser.add_argument("--omissions", type=Path, required=True)
    parser.add_argument("--consolidated-adjudication", type=Path, required=True)
    parser.add_argument("--comparison-output", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    repo = args.repo.resolve()
    inventory = load_tsv(args.r0_inventory)
    classes = {row["path"]: row["classification"] for row in inventory}
    original = load_tsv(args.original_references)
    corrected = load_tsv(args.corrected_references)
    omissions = load_tsv(args.omissions)
    consolidated = load_tsv(args.consolidated_adjudication)
    candidates = {row["target"] for row in corrected}

    historical_hashes = []
    for path in HISTORICAL_ARTIFACTS:
        expected = git_show(repo, args.correction_base, path)
        actual = (repo / path).read_bytes()
        assert actual == expected, f"historical artifact changed: {path}"
        historical_hashes.append(
            {"path": path, "sha256": hashlib.sha256(actual).hexdigest(), "result": "PASS"}
        )

    git_grep = git_grep_rows(repo, args.base, candidates, classes)
    corrected_keys = [occurrence_key(row) for row in corrected]
    git_grep_keys = [occurrence_key(row) for row in git_grep]
    assert corrected_keys == git_grep_keys, "corrected census differs from literal git grep"
    assert (len(corrected), len({row["source"] for row in corrected})) == (815, 92)
    assert sum(row["source_frozen"] == "YES" for row in corrected) == 16

    original_keys = {
        (row["target"], row["source"], int(row["line"]), int(row["column"])) for row in original
    }
    corrected_without_flag = {
        (row["target"], row["source"], int(row["line"]), int(row["column"]))
        for row in corrected
    }
    omission_keys = {
        (row["target"], row["source"], int(row["line"]), int(row["column"])) for row in omissions
    }
    assert corrected_without_flag - original_keys == omission_keys
    assert len(omission_keys) == 14
    assert Counter(row["disposition"] for row in omissions) == Counter(
        {
            "REWRITE_LIVE_POINTER": 5,
            "INTENTIONAL_COLOCATED_ARCHIVE_REFERENCE": 1,
            "RETAINED_TARGET_NO_REWRITE": 8,
        }
    )
    assert sum(row["corrected_eligibility_recheck"] == "PASS_UNCHANGED" for row in consolidated) == 17

    comparison = []
    for row in corrected:
        comparison.append(
            {
                "target": row["target"],
                "source": row["source"],
                "line": row["line"],
                "column": row["column"],
                "source_frozen": row["source_frozen"],
                "corrected_scanner": "MATCH",
                "literal_git_grep": "MATCH",
                "agreement": "YES",
            }
        )
    write_tsv(
        args.comparison_output,
        comparison,
        [
            "target",
            "source",
            "line",
            "column",
            "source_frozen",
            "corrected_scanner",
            "literal_git_grep",
            "agreement",
        ],
    )

    validate_contract(literal_boundary_positions)

    def legacy_matcher(line: str, token: str) -> list[int]:
        at = line.find(token)
        if at < 0:
            return []
        end = at + len(token)
        return [] if end < len(line) and line[end] in set("._-") else [at]

    def loose_matcher(line: str, token: str) -> list[int]:
        at = line.find(token)
        return [] if at < 0 else [at]

    catchproof = {
        "file_md_period_detected": "PASS",
        "file_md_parenthesis_detected": "PASS",
        "file_md_bak_rejected": "PASS",
        "legacy_period_bug_rejected": rejected(lambda: validate_contract(legacy_matcher)),
        "loose_suffix_false_positive_rejected": rejected(lambda: validate_contract(loose_matcher)),
        "missing_occurrence_rejected": rejected(
            lambda: (_ for _ in ()).throw(AssertionError())
            if corrected_keys[:-1] != git_grep_keys
            else None
        ),
        "frozen_flag_launder_rejected": rejected(
            lambda: (_ for _ in ()).throw(AssertionError())
            if [key[:-1] + (("NO" if key[-1] == "YES" else key[-1]),) for key in corrected_keys]
            != git_grep_keys
            else None
        ),
    }
    report = {
        "result": "PASS",
        "mode": "INDEPENDENT_LITERAL_GIT_GREP_VERIFIER",
        "base": subprocess.check_output(["git", "rev-parse", args.base], cwd=repo, text=True).strip(),
        "corrected_occurrences": len(corrected),
        "corrected_sources": len({row["source"] for row in corrected}),
        "corrected_frozen_source_occurrences": sum(
            row["source_frozen"] == "YES" for row in corrected
        ),
        "recovered_omissions": len(omissions),
        "moved_files_still_eligible": 17,
        "literal_git_grep_exact_agreement": True,
        "historical_artifacts": historical_hashes,
        "catchproof": catchproof,
    }
    args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
