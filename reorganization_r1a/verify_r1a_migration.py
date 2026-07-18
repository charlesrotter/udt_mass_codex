#!/usr/bin/env python3
"""Fail-closed post-move verifier for the bounded R1A archive migration."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import stat
import subprocess
from collections import defaultdict
from pathlib import Path
from typing import Any


FROZEN_PREFIXES = (
    "native_action_stage1_2026-07-18/",
    "native_action_stage2_2026-07-18/",
    "native_action_arm_c_2026-07-18/",
    "native_action_final_adjudication_2026-07-18/",
)
EXPECTED_MANIFESTS = {
    "native_action_stage1_2026-07-18/arm_A": "d72e8d6e1b4bc8682bd5518264a1a43a3b5f7b3b246b3d218ea6bfecc6927d19",
    "native_action_stage1_2026-07-18/arm_B": "a99937a8fbba57ac24f490c2974937718f7dfbc2f2f7dd7c960d57fc5e839b92",
    "native_action_stage2_2026-07-18/arm_A": "ad63ffacdd5282a35fe0aef62269464d987aa61b710a4d393d95836234fd670a",
    "native_action_stage2_2026-07-18/arm_B": "30b2a3863f1d16e3b3507b5d0bf10a6b5b59c1e54d769cacc53127cc676d6d45",
    "native_action_arm_c_2026-07-18": "99fc0d6c26aff24e43b8636d74f80e3486c56131590552308b47c1d107ed500f",
    "native_action_final_adjudication_2026-07-18": "57be0046432c27046e84eaafd1706959558f43170d0f1e23dc3047966e512f33",
}
PREMOVE_SNAPSHOT_FILES = {
    "reorganization_r1a/ADJUDICATION_SUMMARY.json",
    "reorganization_r1a/CANDIDATE_ADJUDICATION.tsv",
    "reorganization_r1a/ELIGIBLE_BATCH.txt",
    "reorganization_r1a/INBOUND_REFERENCES.tsv",
    "reorganization_r1a/POINTER_REWRITE_PLAN.tsv",
    "reorganization_r1a/PREMOVE_ADJUDICATION_REPORT.md",
    "reorganization_r1a/PREMOVE_HASHES.tsv",
    "reorganization_r1a/PREMOVE_VERIFY_RESULT.json",
}


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
        raise AssertionError(f"command failed: {' '.join(command)}\n{stderr}")
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


def sha256(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def source_frozen(source: str, classes: dict[str, str]) -> bool:
    return classes.get(source) == "FROZEN_EVIDENCE" or source.startswith(FROZEN_PREFIXES)


def git_blob(repo: Path, revision: str, path: str) -> bytes:
    return bytes(execute(repo, ["git", "show", f"{revision}:{path}"], binary=True))


def package_state(repo: Path, revision: str, package: str) -> tuple[str, int]:
    listing = str(execute(repo, ["git", "ls-tree", "-r", "--name-only", revision, "--", package]))
    paths = [line for line in listing.splitlines() if line]
    ledger = []
    for path in paths:
        ledger.append(f"{path}\0{sha256(git_blob(repo, revision, path))}\n")
    return sha256("".join(ledger).encode("utf-8")), len(paths)


def worktree_package_state(repo: Path, revision: str, package: str) -> tuple[str, int]:
    listing = str(execute(repo, ["git", "ls-tree", "-r", "--name-only", revision, "--", package]))
    base_paths = [line for line in listing.splitlines() if line]
    current = str(execute(repo, ["git", "ls-files", "--", package])).splitlines()
    assert base_paths == current, f"frozen package path set changed: {package}"
    ledger = []
    for path in current:
        ledger.append(f"{path}\0{sha256((repo / path).read_bytes())}\n")
    return sha256("".join(ledger).encode("utf-8")), len(current)


def manifest_path(package: str) -> str:
    if package.startswith("native_action_stage1_2026-07-18/"):
        return package + "/SHA256SUMS.txt"
    if package.startswith("native_action_stage2_2026-07-18/"):
        return package + "/SHA256SUMS.txt"
    return package + "/SHA256SUMS.txt"


def current_dirty_metadata(checkout: Path) -> dict[str, tuple[str, int, str]]:
    env = os.environ.copy()
    env["GIT_OPTIONAL_LOCKS"] = "0"
    raw = subprocess.check_output(
        [
            "git",
            "--no-optional-locks",
            "status",
            "--porcelain=v2",
            "-z",
            "--untracked-files=all",
        ],
        cwd=checkout,
        env=env,
    )
    entries = raw.split(b"\0")
    result: dict[str, tuple[str, int, str]] = {}
    index = 0
    while index < len(entries):
        entry = entries[index]
        index += 1
        if not entry:
            continue
        marker = entry[:1]
        if marker == b"1":
            fields = entry.split(b" ", 8)
            status_code = fields[1].decode("ascii", "replace")
            raw_path = fields[8]
        elif marker == b"2":
            fields = entry.split(b" ", 9)
            status_code = fields[1].decode("ascii", "replace")
            raw_path = fields[9]
            index += 1
        elif marker == b"u":
            fields = entry.split(b" ", 10)
            status_code = fields[1].decode("ascii", "replace")
            raw_path = fields[10]
        elif marker in {b"?", b"!"}:
            status_code = "??" if marker == b"?" else "!!"
            raw_path = entry[2:]
        else:
            raise AssertionError(f"unknown porcelain-v2 record: {entry[:80]!r}")
        path = raw_path.decode("utf-8", "surrogateescape")
        info = (checkout / path).lstat()
        if stat.S_ISREG(info.st_mode):
            object_type = "regular_file"
        elif stat.S_ISDIR(info.st_mode):
            object_type = "directory"
        elif stat.S_ISLNK(info.st_mode):
            object_type = "symlink"
        else:
            object_type = "other"
        result[path] = (status_code, info.st_size, object_type)
    return result


def tracked_texts(repo: Path) -> dict[str, str]:
    paths = str(execute(repo, ["git", "ls-files", "-z"])).split("\0")
    result: dict[str, str] = {}
    for path in (item for item in paths if item):
        payload = (repo / path).read_bytes()
        if b"\x00" in payload[:8192]:
            continue
        try:
            result[path] = payload.decode("utf-8")
        except UnicodeDecodeError:
            continue
    return result


def token_occurrences(text: str, token: str) -> list[tuple[int, int, int]]:
    word = set("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_.-")
    rows = []
    start = 0
    while True:
        start = text.find(token, start)
        if start < 0:
            break
        before = start == 0 or text[start - 1] not in word
        after_at = start + len(token)
        after = after_at == len(text) or text[after_at] not in word
        if before and after:
            line = text.count("\n", 0, start) + 1
            line_start = text.rfind("\n", 0, start) + 1
            rows.append((start, line, start - line_start + 1))
        start += len(token)
    return rows


def validate_move_map(repo: Path, premove: list[dict[str, str]], move_map: list[dict[str, str]]) -> None:
    assert len(premove) == len(move_map) == 17
    expected = {row["old_path"]: row for row in premove}
    assert {row["old_path"] for row in move_map} == set(expected)
    for row in move_map:
        before = expected[row["old_path"]]
        assert row["new_path"] == before["new_path"]
        assert not (repo / row["old_path"]).exists()
        payload = (repo / row["new_path"]).read_bytes()
        assert sha256(payload) == before["sha256_before"] == row["sha256_after"]
        assert row["sha256_before"] == row["sha256_after"]
        assert row["content_identical"] == "YES"


def rejected(check: Any) -> str:
    try:
        check()
    except (AssertionError, KeyError, FileNotFoundError):
        return "PASS"
    raise AssertionError("catch-proof mutation was accepted")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--base", required=True)
    parser.add_argument("--r0-commit", required=True)
    parser.add_argument("--r0-inventory", type=Path, required=True)
    parser.add_argument("--dirty-inventory", type=Path, required=True)
    parser.add_argument("--dirty-checkout", type=Path, required=True)
    parser.add_argument("--premove", type=Path, required=True)
    parser.add_argument("--rewrite-plan", type=Path, required=True)
    parser.add_argument("--move-map", type=Path, required=True)
    parser.add_argument("--pointer-output", type=Path, required=True)
    parser.add_argument("--test-baseline", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    repo = args.repo.resolve()
    inventory = load_tsv(args.r0_inventory)
    classes = {row["path"]: row["classification"] for row in inventory}
    dirty_inventory = load_tsv(args.dirty_inventory)
    premove = load_tsv(args.premove)
    rewrite_plan = load_tsv(args.rewrite_plan)
    move_map = load_tsv(args.move_map)
    validate_move_map(repo, premove, move_map)

    plan_by_source: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rewrite_plan:
        assert row["source_frozen"] == "NO"
        plan_by_source[row["source"]].append(row)
    for source, rows in plan_by_source.items():
        original = git_blob(repo, args.base, source).decode("utf-8")
        expected = original
        for row in rows:
            assert expected.count(row["old_target"]) == int(row["occurrences"])
            expected = expected.replace(row["old_target"], row["new_target"])
        assert (repo / source).read_text(encoding="utf-8") == expected, source

    texts = tracked_texts(repo)
    for generated in (args.pointer_output, args.output):
        try:
            texts.pop(str(generated.resolve().relative_to(repo)), None)
        except ValueError:
            pass
    moved_destinations = {row["new_path"] for row in move_map}
    pointer_rows: list[dict[str, Any]] = []
    stale = []
    for move in move_map:
        old = move["old_path"]
        new = move["new_path"]
        for source, text in texts.items():
            for _, line, column in token_occurrences(text, new):
                pointer_rows.append(
                    {
                        "moved_path": old,
                        "token": new,
                        "token_kind": "NEW_PATH",
                        "source": source,
                        "line": line,
                        "column": column,
                        "source_frozen": "YES" if source_frozen(source, classes) else "NO",
                        "role": "UPDATED_OR_MIGRATION_RECORD",
                    }
                )
            for offset, line, column in token_occurrences(text, old):
                prefix = text[max(0, offset - 80) : offset]
                if prefix.endswith("archive/pre_2026-07-01/"):
                    role = "NEW_PATH_SUFFIX"
                elif offset and text[offset - 1] == "/":
                    role = "QUALIFIED_OTHER_PATH"
                elif source.startswith("reorganization_r0/"):
                    role = "R0_HISTORICAL_SNAPSHOT"
                elif source in PREMOVE_SNAPSHOT_FILES:
                    role = "R1A_PREMOVE_SNAPSHOT"
                elif source.startswith("reorganization_r1a/"):
                    role = "R1A_AUDIT_RECORD"
                elif source in moved_destinations:
                    role = "BYTE_PRESERVED_MOVED_RECORD"
                elif source_frozen(source, classes):
                    role = "FROZEN_SOURCE"
                elif source in {"reorganization_r1a/MOVE_MAP.tsv"}:
                    role = "MIGRATION_RECORD"
                else:
                    role = "STALE_NON_FROZEN_POINTER"
                    stale.append((source, line, old))
                pointer_rows.append(
                    {
                        "moved_path": old,
                        "token": old,
                        "token_kind": "OLD_BASENAME",
                        "source": source,
                        "line": line,
                        "column": column,
                        "source_frozen": "YES" if source_frozen(source, classes) else "NO",
                        "role": role,
                    }
                )
    assert not stale, f"stale non-frozen pointers: {stale[:20]}"
    write_tsv(
        args.pointer_output,
        sorted(pointer_rows, key=lambda row: (row["moved_path"], row["source"], row["line"], row["token_kind"])),
        [
            "moved_path",
            "token",
            "token_kind",
            "source",
            "line",
            "column",
            "source_frozen",
            "role",
        ],
    )

    frozen_results = []
    for package, expected_manifest in EXPECTED_MANIFESTS.items():
        manifest = repo / manifest_path(package)
        assert sha256(manifest.read_bytes()) == expected_manifest, package
        base_digest, base_count = package_state(repo, args.r0_commit, package)
        current_digest, current_count = worktree_package_state(repo, args.r0_commit, package)
        assert base_digest == current_digest and base_count == current_count, package
        frozen_results.append(
            {
                "package": package,
                "manifest_sha256": expected_manifest,
                "tracked_files": current_count,
                "complete_state_sha256": current_digest,
                "result": "PASS",
            }
        )

    current_dirty = current_dirty_metadata(args.dirty_checkout.resolve())
    recorded_dirty = {row["path"]: row for row in dirty_inventory}
    assert set(current_dirty) == set(recorded_dirty)
    for path, (status_code, size, object_type) in current_dirty.items():
        row = recorded_dirty[path]
        assert row["status"] == status_code
        assert int(row["size_bytes_lstat"]) == size
        assert row["object_type"] == object_type
        assert row["content_sha256"] == "NOT_READ"

    readme = (repo / "README.md").read_text(encoding="utf-8")
    assert readme.index("[`LIVE.md`](LIVE.md)") < readme.index("[`HANDOFF.md`](HANDOFF.md)")
    assert readme.index("[`HANDOFF.md`](HANDOFF.md)") < readme.index(
        "[`stability_branch_follow_256_DECISION.md`](stability_branch_follow_256_DECISION.md)"
    )
    assert "cannot overrule the topmost current-state block in `LIVE.md`" in readme

    changed = str(execute(repo, ["git", "diff", "--name-only", args.base])).splitlines()
    assert not any(source_frozen(path, classes) for path in changed), "frozen source changed"
    status_lines = str(
        execute(repo, ["git", "diff", "--name-status", "--find-renames=100%", args.base])
    ).splitlines()
    seen_modified: set[str] = set()
    seen_renames: set[tuple[str, str]] = set()
    for line in status_lines:
        fields = line.split("\t")
        status_code = fields[0]
        if status_code == "M":
            path = fields[1]
            assert path == "README.md" or path in plan_by_source, f"unauthorized modification: {path}"
            seen_modified.add(path)
        elif status_code.startswith("R"):
            assert len(fields) == 3 and status_code == "R100", line
            seen_renames.add((fields[1], fields[2]))
        elif status_code == "A":
            assert fields[1].startswith("reorganization_r1a/"), f"unauthorized addition: {fields[1]}"
        else:
            raise AssertionError(f"unauthorized diff status: {line}")
    assert seen_modified == set(plan_by_source) | {"README.md"}, "pointer-source diff set mismatch"
    assert seen_renames == {
        (row["old_path"], row["new_path"]) for row in move_map
    }, "rename set mismatch"

    test_result = None
    if args.test_baseline:
        test_result = json.loads(args.test_baseline.read_text(encoding="utf-8"))
        assert test_result["baseline_match"] is True
        assert test_result["passed"] == 69
        assert test_result["failed"] == 1
        assert test_result["xfailed"] == 1

    catchproof = {
        "missing_move_rejected": rejected(
            lambda: validate_move_map(repo, premove, move_map[:-1])
        ),
        "bad_after_hash_rejected": rejected(
            lambda: validate_move_map(
                repo,
                premove,
                [dict(row, sha256_after="0" * 64) if index == 0 else row for index, row in enumerate(move_map)],
            )
        ),
        "content_identical_launder_rejected": rejected(
            lambda: validate_move_map(
                repo,
                premove,
                [dict(row, content_identical="NO") if index == 0 else row for index, row in enumerate(move_map)],
            )
        ),
    }
    report = {
        "result": "PASS",
        "mode": "POSTMOVE_FAIL_CLOSED_STATIC_VERIFIER",
        "base": args.base,
        "moved_files": len(move_map),
        "path_substitutions": sum(int(row["occurrences"]) for row in rewrite_plan),
        "pointer_sources": len(plan_by_source),
        "pointer_census_rows": len(pointer_rows),
        "stale_non_frozen_pointers": 0,
        "frozen_packages": frozen_results,
        "dirty_rows_metadata_only": len(current_dirty),
        "test_baseline": test_result,
        "catchproof": catchproof,
    }
    args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
