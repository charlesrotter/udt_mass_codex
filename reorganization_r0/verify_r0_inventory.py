#!/usr/bin/env python3
"""Fail-closed verifier for the Phase-R0 repository census."""

from __future__ import annotations

import argparse
from collections import deque
import csv
import copy
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import stat
import subprocess
from typing import Any, Iterable


VALID_CLASSES = {
    "CONTROL",
    "ACTIVE",
    "FROZEN_EVIDENCE",
    "ARCHIVE_CANDIDATE",
    "MOVE_CANDIDATE",
    "UNKNOWN/BLOCKED",
}
REQUIRED_CATEGORIES = {
    "PYTHON_IMPORT",
    "FILE_PATH",
    "MARKDOWN_LINK",
    "MANIFEST",
    "TEST",
    "STARTUP",
}
REQUIRED_ROOT = {
    "LIVE.md",
    "HANDOFF.md",
    "INDEX.md",
    "AGENTS.md",
    "CLAUDE.md",
    "CANON.md",
    "MEMORY.md",
}
TEXT_SUFFIXES = {
    ".cfg",
    ".csv",
    ".ini",
    ".json",
    ".log",
    ".md",
    ".py",
    ".rst",
    ".sh",
    ".tex",
    ".toml",
    ".tsv",
    ".txt",
    ".yaml",
    ".yml",
}
FROZEN = (
    (
        "stage1_A",
        "native_action_stage1_2026-07-18/arm_A",
        "d72e8d6e1b4bc8682bd5518264a1a43a3b5f7b3b246b3d218ea6bfecc6927d19",
    ),
    (
        "stage1_B",
        "native_action_stage1_2026-07-18/arm_B",
        "a99937a8fbba57ac24f490c2974937718f7dfbc2f2f7dd7c960d57fc5e839b92",
    ),
    (
        "stage2_A",
        "native_action_stage2_2026-07-18/arm_A",
        "ad63ffacdd5282a35fe0aef62269464d987aa61b710a4d393d95836234fd670a",
    ),
    (
        "stage2_B",
        "native_action_stage2_2026-07-18/arm_B",
        "30b2a3863f1d16e3b3507b5d0bf10a6b5b59c1e54d769cacc53127cc676d6d45",
    ),
    (
        "arm_C",
        "native_action_arm_c_2026-07-18",
        "99fc0d6c26aff24e43b8636d74f80e3486c56131590552308b47c1d107ed500f",
    ),
    (
        "final_adjudication",
        "native_action_final_adjudication_2026-07-18",
        "57be0046432c27046e84eaafd1706959558f43170d0f1e23dc3047966e512f33",
    ),
)


def execute(command: list[str], cwd: Path, *, binary: bool = False) -> str | bytes:
    completed = subprocess.run(
        command,
        cwd=cwd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=True,
    )
    return completed.stdout if binary else completed.stdout.decode("utf-8", "replace")


def digest(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def base_tree(repo: Path, base: str) -> dict[str, tuple[str, str]]:
    raw = execute(["git", "ls-tree", "-r", "-z", base], repo, binary=True)
    assert isinstance(raw, bytes)
    result: dict[str, tuple[str, str]] = {}
    for record in raw.split(b"\0"):
        if not record:
            continue
        metadata, name = record.split(b"\t", 1)
        mode, object_type, oid = metadata.decode().split()
        if object_type == "blob":
            result[name.decode("utf-8", "surrogateescape")] = (mode, oid)
    return result


def batch_blobs(repo: Path, path_oids: dict[str, str]) -> dict[str, bytes]:
    process = subprocess.Popen(
        ["git", "cat-file", "--batch"],
        cwd=repo,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    assert process.stdin is not None and process.stdout is not None
    result: dict[str, bytes] = {}
    for path, oid in path_oids.items():
        process.stdin.write((oid + "\n").encode())
        process.stdin.flush()
        header = process.stdout.readline().decode().strip().split()
        if len(header) != 3 or header[1] != "blob":
            raise AssertionError(f"bad blob header for {path}: {header}")
        payload = process.stdout.read(int(header[2]))
        assert process.stdout.read(1) == b"\n"
        result[path] = payload
    process.stdin.close()
    process.wait(timeout=60)
    if process.returncode:
        stderr = process.stderr.read().decode("utf-8", "replace") if process.stderr else ""
        raise AssertionError(f"cat-file failed: {stderr}")
    return result


def independent_commit_map(
    repo: Path, base: str, tracked: set[str]
) -> dict[str, tuple[str, str, str]]:
    raw = execute(
        [
            "git",
            "-c",
            "core.quotepath=false",
            "log",
            "--no-renames",
            "--format=VERIFYCOMMIT:%H%x09%cs%x09%s",
            "--name-only",
            base,
            "--",
        ],
        repo,
    )
    assert isinstance(raw, str)
    current: tuple[str, str, str] | None = None
    found: dict[str, tuple[str, str, str]] = {}
    for line in raw.splitlines():
        if line.startswith("VERIFYCOMMIT:"):
            commit, date, subject = line[len("VERIFYCOMMIT:") :].split("\t", 2)
            current = (commit, date, subject)
        elif current and line in tracked and line not in found:
            found[line] = current
    assert set(found) == tracked, f"commit coverage mismatch: {len(found)} != {len(tracked)}"
    return found


def is_text(path: str, payload: bytes) -> bool:
    return (
        PurePosixPath(path).suffix.lower() in TEXT_SUFFIXES
        and b"\0" not in payload[:8192]
    )


class AhoMatcher:
    """Independent multi-pattern matcher for exact root-name references."""

    def __init__(self, patterns: Iterable[str]) -> None:
        self.transitions: list[dict[str, int]] = [{}]
        self.failure: list[int] = [0]
        self.outputs: list[list[str]] = [[]]
        for pattern in patterns:
            state = 0
            for character in pattern:
                next_state = self.transitions[state].get(character)
                if next_state is None:
                    next_state = len(self.transitions)
                    self.transitions[state][character] = next_state
                    self.transitions.append({})
                    self.failure.append(0)
                    self.outputs.append([])
                state = next_state
            self.outputs[state].append(pattern)
        queue: deque[int] = deque()
        for state in self.transitions[0].values():
            queue.append(state)
        while queue:
            state = queue.popleft()
            for character, child in self.transitions[state].items():
                queue.append(child)
                fallback = self.failure[state]
                while fallback and character not in self.transitions[fallback]:
                    fallback = self.failure[fallback]
                self.failure[child] = self.transitions[fallback].get(character, 0)
                self.outputs[child].extend(self.outputs[self.failure[child]])

    @staticmethod
    def word_character(character: str) -> bool:
        return character.isalnum() or character in "_.-"

    def find(self, text: str) -> set[str]:
        state = 0
        matches: set[str] = set()
        for index, character in enumerate(text):
            while state and character not in self.transitions[state]:
                state = self.failure[state]
            state = self.transitions[state].get(character, 0)
            for pattern in self.outputs[state]:
                start = index - len(pattern) + 1
                before_ok = start == 0 or not self.word_character(text[start - 1])
                after_index = index + 1
                after_ok = after_index == len(text) or not self.word_character(text[after_index])
                if before_ok and after_ok:
                    matches.add(pattern)
        return matches


def load_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def validate_inventory_shape(
    rows: list[dict[str, str]], root_paths: set[str]
) -> None:
    paths = [row.get("path", "") for row in rows]
    assert len(paths) == len(set(paths)), "duplicate root inventory row"
    assert set(paths) == root_paths, "missing or extra root inventory row"
    assert all(row.get("classification") in VALID_CLASSES for row in rows), "bad classification"
    assert all(len(row.get("sha256", "")) == 64 for row in rows), "bad SHA-256 shape"


def validate_dependencies(rows: list[dict[str, str]]) -> None:
    categories = {row.get("category", "") for row in rows}
    assert REQUIRED_CATEGORIES <= categories, f"missing categories: {REQUIRED_CATEGORIES - categories}"
    assert all(row.get("source") for row in rows), "dependency without source"
    assert all(row.get("kind") for row in rows), "dependency without kind"
    assert any(row.get("status") == "DYNAMIC" for row in rows), "dynamic paths were suppressed"
    assert any(
        row.get("status") in {"MISSING_OR_GENERATED", "AMBIGUOUS_BASENAME"} for row in rows
    ), "unresolved paths were suppressed"


def additions_only(diff_rows: list[tuple[str, str]]) -> None:
    forbidden = [row for row in diff_rows if row[0] != "A"]
    assert not forbidden, f"non-addition diff entries: {forbidden[:20]}"


def current_dirty_metadata(checkout: Path) -> dict[str, tuple[str, int, str]]:
    environment = os.environ.copy()
    environment["GIT_OPTIONAL_LOCKS"] = "0"
    completed = subprocess.run(
        [
            "git",
            "--no-optional-locks",
            "status",
            "--short",
            "-z",
            "--untracked-files=all",
        ],
        cwd=checkout,
        env=environment,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=True,
    )
    records = completed.stdout.split(b"\0")
    result: dict[str, tuple[str, int, str]] = {}
    index = 0
    while index < len(records):
        record = records[index]
        index += 1
        if not record:
            continue
        status_code = record[:2].decode("ascii", "replace").replace(" ", ".")
        path = record[3:].decode("utf-8", "surrogateescape")
        if "R" in status_code or "C" in status_code:
            index += 1  # consume original path; no such row exists in the recorded R0 snapshot
        metadata = os.lstat(checkout / path)
        if stat.S_ISREG(metadata.st_mode):
            object_type = "regular_file"
        elif stat.S_ISDIR(metadata.st_mode):
            object_type = "directory"
        elif stat.S_ISLNK(metadata.st_mode):
            object_type = "symlink"
        else:
            object_type = "other"
        result[path] = (status_code, metadata.st_size, object_type)
    return result


def frozen_checks(repo: Path) -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []
    for label, relative, expected in FROZEN:
        package = repo / relative
        manifest = package / "SHA256SUMS.txt"
        payload = manifest.read_bytes()
        assert digest(payload) == expected, f"frozen manifest changed: {label}"
        failures: list[str] = []
        rows = payload.decode("utf-8").splitlines()
        for row in rows:
            expected_file, listed = row.split("  ", 1)
            listed = listed[2:] if listed.startswith("./") else listed
            target = package / listed
            if not target.is_file() or digest(target.read_bytes()) != expected_file:
                failures.append(listed)
        assert not failures, f"frozen internal mismatch {label}: {failures[:10]}"
        output.append(
            {
                "label": label,
                "manifest_sha256": expected,
                "entries": len(rows),
                "result": "PASS",
            }
        )
    return output


def catchproof(root_paths: set[str], inventory: list[dict[str, str]], dependencies: list[dict[str, str]]) -> dict[str, str]:
    probes: dict[str, bool] = {}

    def rejects(action: Any) -> bool:
        try:
            action()
        except AssertionError:
            return True
        return False

    missing = copy.deepcopy(inventory[:-1])
    probes["missing_root_row_rejected"] = rejects(
        lambda: validate_inventory_shape(missing, root_paths)
    )
    duplicate = copy.deepcopy(inventory)
    duplicate.append(copy.deepcopy(inventory[0]))
    probes["duplicate_root_row_rejected"] = rejects(
        lambda: validate_inventory_shape(duplicate, root_paths)
    )
    bad_sha = copy.deepcopy(inventory)
    bad_sha[0]["sha256"] = "bad"
    probes["bad_sha256_rejected"] = rejects(
        lambda: validate_inventory_shape(bad_sha, root_paths)
    )
    bad_class = copy.deepcopy(inventory)
    bad_class[0]["classification"] = "INVENTED"
    probes["unknown_classification_rejected"] = rejects(
        lambda: validate_inventory_shape(bad_class, root_paths)
    )
    missing_category = [row for row in copy.deepcopy(dependencies) if row["category"] != "MANIFEST"]
    probes["missing_dependency_category_rejected"] = rejects(
        lambda: validate_dependencies(missing_category)
    )
    probes["modified_base_path_rejected"] = rejects(
        lambda: additions_only([("A", "new.txt"), ("M", "CANON.md")])
    )
    failed = [name for name, passed in probes.items() if not passed]
    assert not failed, f"catch-proof failures: {failed}"
    return {name: "PASS" for name in sorted(probes)}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--base", required=True)
    parser.add_argument("--inventory", type=Path, required=True)
    parser.add_argument("--dependencies", type=Path, required=True)
    parser.add_argument("--dirty-inventory", type=Path, required=True)
    parser.add_argument("--dirty-checkout", type=Path, required=True)
    parser.add_argument("--test-baseline", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    arguments = parser.parse_args()

    repo = arguments.repo.resolve()
    base = str(execute(["git", "rev-parse", arguments.base], repo)).strip()
    tree = base_tree(repo, base)
    root_paths = {path for path in tree if "/" not in path}
    inventory = load_tsv(arguments.inventory)
    dependencies = load_tsv(arguments.dependencies)
    dirty_inventory = load_tsv(arguments.dirty_inventory)

    validate_inventory_shape(inventory, root_paths)
    validate_dependencies(dependencies)
    inventory_by_path = {row["path"]: row for row in inventory}
    root_blobs = batch_blobs(repo, {path: tree[path][1] for path in sorted(root_paths)})
    commits = independent_commit_map(repo, base, set(tree))
    for path in sorted(root_paths):
        row = inventory_by_path[path]
        payload = root_blobs[path]
        assert row["git_mode"] == tree[path][0], f"mode mismatch: {path}"
        assert row["git_blob_oid"] == tree[path][1], f"blob mismatch: {path}"
        assert row["sha256"] == digest(payload), f"SHA-256 mismatch: {path}"
        assert int(row["size_bytes"]) == len(payload), f"size mismatch: {path}"
        commit, date, subject = commits[path]
        assert row["last_commit"] == commit, f"last commit mismatch: {path}"
        assert row["last_commit_date"] == date, f"last date mismatch: {path}"
        assert row["last_commit_subject"] == subject.replace("\t", " "), (
            f"last subject mismatch: {path}"
        )
    for path in REQUIRED_ROOT:
        assert inventory_by_path[path]["classification"] == "CONTROL", (
            f"required root not CONTROL: {path}"
        )

    all_blobs = batch_blobs(repo, {path: oid for path, (_, oid) in sorted(tree.items())})
    matcher = AhoMatcher(sorted(root_paths))
    inbound: dict[str, set[str]] = {path: set() for path in root_paths}
    for source, payload in all_blobs.items():
        if not is_text(source, payload):
            continue
        text = payload.decode("utf-8", "replace")
        for target in matcher.find(text):
            inbound[target].add(source)
    for path, sources in inbound.items():
        row = inventory_by_path[path]
        recorded = set(filter(None, row["referenced_by"].split(";")))
        assert recorded == sources, f"reference-source mismatch: {path}"
        assert int(row["reference_count"]) == len(sources), f"reference count mismatch: {path}"

    current_dirty = current_dirty_metadata(arguments.dirty_checkout.resolve())
    recorded_dirty = {row["path"]: row for row in dirty_inventory}
    assert set(recorded_dirty) == set(current_dirty), "dirty path set changed or incomplete"
    for path, (status_code, size, object_type) in current_dirty.items():
        row = recorded_dirty[path]
        assert row["status"] == status_code, f"dirty status mismatch: {path}"
        assert int(row["size_bytes_lstat"]) == size, f"dirty size mismatch: {path}"
        assert row["object_type"] == object_type, f"dirty type mismatch: {path}"
        assert row["content_sha256"] == "NOT_READ", f"dirty content was read: {path}"
        assert row["firewall"] == "STATUS_AND_LSTAT_ONLY", f"dirty firewall missing: {path}"

    diff_text = str(execute(["git", "diff", "--name-status", base], repo))
    diff_rows = []
    for line in diff_text.splitlines():
        if not line:
            continue
        status_code, path = line.split("\t", 1)
        diff_rows.append((status_code, path))
    additions_only(diff_rows)

    frozen = frozen_checks(repo)
    catchproof_result = catchproof(root_paths, inventory, dependencies)

    test_result: dict[str, Any] | None = None
    if arguments.test_baseline:
        test_result = json.loads(arguments.test_baseline.read_text(encoding="utf-8"))
        assert test_result["baseline_match"] is True, "test baseline mismatch"
        assert test_result["passed"] == 69
        assert test_result["failed"] == 1
        assert test_result["xfailed"] == 1

    report = {
        "result": "PASS",
        "mode": "INDEPENDENT_MECHANICAL_STATIC_VALIDATOR",
        "date": "2026-07-18",
        "base_commit": base,
        "root_rows_verified": len(inventory),
        "root_references_independently_recomputed": True,
        "dependency_edges_checked": len(dependencies),
        "dependency_categories": sorted({row["category"] for row in dependencies}),
        "dirty_rows_verified_metadata_only": len(dirty_inventory),
        "frozen_packages": frozen,
        "base_diff_entries": [list(row) for row in diff_rows],
        "base_diff_additions_only": True,
        "catchproof": catchproof_result,
        "test_baseline": test_result,
        "semantic_caveat": (
            "Hashes, coverage, references, categories, dirty metadata, and additions-only scope are "
            "mechanically verified. R0 classifications are conservative proposals, not move authorization."
        ),
    }
    arguments.output.write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
