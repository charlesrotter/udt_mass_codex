#!/usr/bin/env python3
"""Independent fail-closed verification of the preregistered R1B inputs."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import subprocess
from pathlib import Path


def command(repo: Path, arguments: list[str], *, binary: bool = False) -> str | bytes:
    completed = subprocess.run(
        arguments,
        cwd=repo,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=not binary,
        check=False,
    )
    if completed.returncode:
        error = completed.stderr if not binary else completed.stderr.decode("utf-8", "replace")
        raise AssertionError(f"command failed: {' '.join(arguments)}\n{error}")
    return completed.stdout


def tsv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def digest(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def blob(repo: Path, base: str, path: str) -> bytes:
    return bytes(command(repo, ["git", "show", f"{base}:{path}"], binary=True))


def independent_positions(text: str, token: str) -> list[int]:
    left = set("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_.-")
    suffix = set("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_-")
    result = []
    start = 0
    while True:
        at = text.find(token, start)
        if at < 0:
            return result
        left_ok = at == 0 or text[at - 1] not in left
        end = at + len(token)
        if end == len(text):
            right_ok = True
        elif text[end] in suffix:
            right_ok = False
        elif text[end] == "." and end + 1 < len(text):
            right_ok = text[end + 1] not in suffix
        else:
            right_ok = True
        if left_ok and right_ok:
            result.append(at)
        start = at + len(token)


def current_span(source: str, text: str) -> str:
    if source == "LIVE.md":
        end = text.index("**[prior layer of the same arc")
        return text[:end]
    start = text.index("## CURRENT")
    end = text.index("## [ARCHIVED]", start)
    return text[start:end]


def coordinates(text: str, offset: int) -> tuple[int, int]:
    line = text.count("\n", 0, offset) + 1
    start = text.rfind("\n", 0, offset) + 1
    return line, offset - start + 1


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--base", required=True)
    parser.add_argument("--cutoff", default="2026-07-01")
    parser.add_argument("--input-dir", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    repo = args.repo.resolve()
    inputs = args.input_dir.resolve()
    summary = json.loads((inputs / "PREREGISTERED_INPUTS.json").read_text(encoding="utf-8"))
    assert summary["base"] == args.base and summary["cutoff"] == args.cutoff
    for name, expected in summary["generated_artifacts"].items():
        assert digest((inputs / name).read_bytes()) == expected, name

    base_paths = sorted(
        filter(
            None,
            str(command(repo, ["git", "ls-tree", "-r", "-z", "--name-only", args.base])).split("\0"),
        )
    )
    assert not any(path.startswith("reorganization_r1b/") for path in base_paths)
    root_markdown = [path for path in base_paths if "/" not in path and path.endswith(".md")]
    registered_all = tsv(inputs / "BASE_ROOT_MARKDOWN.tsv")
    registered_candidates = tsv(inputs / "PREREGISTERED_CANDIDATES.tsv")
    assert [row["path"] for row in registered_all] == root_markdown

    independently_selected = []
    for row in registered_all:
        path = row["path"]
        additions = str(
            command(
                repo,
                [
                    "git",
                    "log",
                    "--follow",
                    "--diff-filter=A",
                    "--format=%cs%x09%H",
                    args.base,
                    "--",
                    path,
                ],
            )
        ).splitlines()
        assert additions, path
        first_date, first_commit = additions[-1].split("\t", 1)
        payload = blob(repo, args.base, path)
        tree = str(command(repo, ["git", "ls-tree", args.base, "--", path])).strip().split()
        assert row["first_commit_date"] == first_date
        assert row["first_commit"] == first_commit, (
            path,
            row["first_commit_date"],
            row["first_commit"],
            first_date,
            first_commit,
        )
        assert row["git_blob_oid_at_base"] == tree[2]
        assert row["sha256_at_base"] == digest(payload)
        assert int(row["size_bytes_at_base"]) == len(payload)
        assert row["pre_cutoff"] == ("YES" if first_date < args.cutoff else "NO")
        if first_date < args.cutoff:
            independently_selected.append(path)
    assert [row["path"] for row in registered_candidates] == independently_selected
    assert len(independently_selected) == 99

    assert independent_positions("See file.md.", "file.md")
    assert independent_positions("See file.md)", "file.md")
    assert not independent_positions("See file.md.bak", "file.md")
    frontier_expected = []
    for source in ("LIVE.md", "HANDOFF.md"):
        span = current_span(source, blob(repo, args.base, source).decode("utf-8"))
        for target in root_markdown:
            for offset in independent_positions(span, target):
                if offset and span[offset - 1] == "/":
                    continue
                line, column = coordinates(span, offset)
                frontier_expected.append((target, source, line, column))
    frontier_expected.sort()
    frontier_actual = sorted(
        (row["target"], row["source"], int(row["line"]), int(row["column"]))
        for row in tsv(inputs / "CURRENT_FRONTIER_REFERENCE_REGISTRY.tsv")
    )
    assert frontier_actual == frontier_expected
    assert len(frontier_actual) == 28

    permanent = tsv(inputs / "PERMANENT_ROOT_REGISTRY.tsv")
    assert len(permanent) == 16
    assert len({row["path"] for row in permanent}) == len(permanent)
    assert all(row["phase_status"] == "PERMANENT_ROOT" for row in permanent)

    report = {
        "result": "PASS",
        "mode": "INDEPENDENT_R1B_PREREGISTERED_INPUT_VERIFIER",
        "base": args.base,
        "base_tracked_paths": len(base_paths),
        "base_root_markdown": len(root_markdown),
        "preregistered_candidates": len(independently_selected),
        "frontier_occurrences": len(frontier_actual),
        "frontier_candidate_targets": len(
            {target for target, _, _, _ in frontier_actual if target in independently_selected}
        ),
        "permanent_root_rows": len(permanent),
        "generated_records_absent_from_selection_base": True,
        "catchproof": {
            "file_md_period_detected": "PASS",
            "file_md_parenthesis_detected": "PASS",
            "file_md_bak_rejected": "PASS",
        },
    }
    args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
