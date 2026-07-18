#!/usr/bin/env python3
"""Fail-closed verifier for the bounded R1B two-file archive migration."""

from __future__ import annotations

import argparse
import csv
import hashlib
import importlib.util
import json
import os
import stat
import subprocess
from pathlib import Path
from typing import Any

EXPECTED_MANIFESTS = {
    "native_action_stage1_2026-07-18/arm_A": "d72e8d6e1b4bc8682bd5518264a1a43a3b5f7b3b246b3d218ea6bfecc6927d19",
    "native_action_stage1_2026-07-18/arm_B": "a99937a8fbba57ac24f490c2974937718f7dfbc2f2f7dd7c960d57fc5e839b92",
    "native_action_stage2_2026-07-18/arm_A": "ad63ffacdd5282a35fe0aef62269464d987aa61b710a4d393d95836234fd670a",
    "native_action_stage2_2026-07-18/arm_B": "30b2a3863f1d16e3b3507b5d0bf10a6b5b59c1e54d769cacc53127cc676d6d45",
    "native_action_arm_c_2026-07-18": "99fc0d6c26aff24e43b8636d74f80e3486c56131590552308b47c1d107ed500f",
    "native_action_final_adjudication_2026-07-18": "57be0046432c27046e84eaafd1706959558f43170d0f1e23dc3047966e512f33",
}


def load_boundary(repo: Path) -> Any:
    path = repo / "reorganization_r1a/correction_2026-07-18/reference_boundary.py"
    spec = importlib.util.spec_from_file_location("r1a_corrected_boundary_for_r1b_migration", path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def run(repo: Path, command: list[str], *, binary: bool = False) -> str | bytes:
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


def write_tsv(path: Path, rows: list[dict[str, Any]], fields: tuple[str, ...]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow(
                {field: str(row.get(field, "-")).replace("\t", "\\t").replace("\n", "\\n") for field in fields}
            )


def sha256(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def git_blob_oid(payload: bytes) -> str:
    return hashlib.sha1(f"blob {len(payload)}\0".encode("ascii") + payload).hexdigest()


def git_blob(repo: Path, revision: str, path: str) -> bytes:
    return bytes(run(repo, ["git", "show", f"{revision}:{path}"], binary=True))


def tracked_paths(repo: Path) -> list[str]:
    return [path for path in str(run(repo, ["git", "ls-files", "-z"])).split("\0") if path]


def tracked_texts(repo: Path) -> dict[str, str]:
    result: dict[str, str] = {}
    for path in tracked_paths(repo):
        payload = (repo / path).read_bytes()
        if b"\x00" in payload[:8192]:
            continue
        try:
            result[path] = payload.decode("utf-8")
        except UnicodeDecodeError:
            continue
    return result


def package_state_from_git(repo: Path, revision: str, package: str) -> tuple[str, int]:
    listing = str(run(repo, ["git", "ls-tree", "-r", "--name-only", revision, "--", package]))
    paths = [path for path in listing.splitlines() if path]
    ledger = "".join(f"{path}\0{sha256(git_blob(repo, revision, path))}\n" for path in paths)
    return sha256(ledger.encode("utf-8")), len(paths)


def package_state_from_worktree(repo: Path, base: str, package: str) -> tuple[str, int]:
    listing = str(run(repo, ["git", "ls-tree", "-r", "--name-only", base, "--", package]))
    expected = [path for path in listing.splitlines() if path]
    current = [path for path in tracked_paths(repo) if path == package or path.startswith(package + "/")]
    assert expected == current, f"frozen package path set changed: {package}"
    ledger = "".join(f"{path}\0{sha256((repo / path).read_bytes())}\n" for path in current)
    return sha256(ledger.encode("utf-8")), len(current)


def current_dirty_metadata(checkout: Path) -> dict[str, tuple[str, int, str]]:
    env = os.environ.copy()
    env["GIT_OPTIONAL_LOCKS"] = "0"
    raw = subprocess.check_output(
        ["git", "--no-optional-locks", "status", "--porcelain=v2", "-z", "--untracked-files=all"],
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
            status_code, raw_path = fields[1].decode("ascii", "replace"), fields[8]
        elif marker == b"2":
            fields = entry.split(b" ", 9)
            status_code, raw_path = fields[1].decode("ascii", "replace"), fields[9]
            index += 1
        elif marker == b"u":
            fields = entry.split(b" ", 10)
            status_code, raw_path = fields[1].decode("ascii", "replace"), fields[10]
        elif marker in {b"?", b"!"}:
            status_code, raw_path = ("??" if marker == b"?" else "!!"), entry[2:]
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


def line_column(text: str, offset: int) -> tuple[int, int]:
    line = text.count("\n", 0, offset) + 1
    start = text.rfind("\n", 0, offset) + 1
    return line, offset - start + 1


def literal_git_grep(
    repo: Path, token: str, boundary: Any, ignored_sources: set[str]
) -> set[tuple[str, int, int]]:
    completed = subprocess.run(
        ["git", "grep", "-a", "-n", "-F", "-e", token, "--"],
        cwd=repo,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    assert completed.returncode in {0, 1}, completed.stderr.decode("utf-8", "replace")
    found: set[tuple[str, int, int]] = set()
    for raw in completed.stdout.decode("utf-8", "replace").split("\n"):
        if not raw:
            continue
        source, line_raw, body = raw.split(":", 2)
        if source in ignored_sources:
            continue
        line = int(line_raw)
        for offset in boundary.occurrences(body, token):
            found.add((source, line, offset + 1))
    return found


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--base", required=True)
    parser.add_argument("--mutation-base", required=True)
    parser.add_argument("--move-plan", type=Path, required=True)
    parser.add_argument("--pointer-plan", type=Path, required=True)
    parser.add_argument("--colocated-plan", type=Path, required=True)
    parser.add_argument("--candidate-table", type=Path, required=True)
    parser.add_argument("--source-registry", type=Path, required=True)
    parser.add_argument("--dirty-inventory", type=Path, required=True)
    parser.add_argument("--dirty-checkout", type=Path, required=True)
    parser.add_argument("--migration-dir", type=Path, required=True)
    parser.add_argument("--test-result", type=Path)
    args = parser.parse_args()

    repo = args.repo.resolve()
    output = args.migration_dir.resolve()
    boundary = load_boundary(repo)
    moves = load_tsv(args.move_plan)
    pointers = load_tsv(args.pointer_plan)
    colocated = load_tsv(args.colocated_plan)
    candidates = load_tsv(args.candidate_table)
    registry_rows = load_tsv(args.source_registry)
    source_classes = {row["source"]: row["immutability_class"] for row in registry_rows}
    assert len(moves) == 2 and len(pointers) == 1 and len(colocated) == 1 and len(candidates) == 99

    migration_rows = load_tsv(output / "MIGRATION_RESULT.tsv")
    assert len(migration_rows) == len(moves)
    migration_by_old = {row["old_path"]: row for row in migration_rows}
    for move in moves:
        row = migration_by_old[move["old_path"]]
        assert row["new_path"] == move["new_path"]
        assert not (repo / move["old_path"]).exists()
        payload = (repo / move["new_path"]).read_bytes()
        assert sha256(payload) == move["sha256_before"] == row["sha256_before"] == row["sha256_after"]
        assert git_blob_oid(payload) == move["git_blob_oid_before"] == row["git_blob_oid_before"] == row["git_blob_oid_after"]
        assert len(payload) == int(move["size_bytes"]) == int(row["size_bytes"])
        assert row["content_identical"] == "YES"

    pointer_results = load_tsv(output / "POINTER_SUBSTITUTION_RESULT.tsv")
    assert len(pointer_results) == 1
    for plan, result in zip(pointers, pointer_results, strict=True):
        before = git_blob(repo, args.mutation_base, plan["source"])
        expected = before.decode("utf-8").replace(plan["old_target"], plan["new_target"], 1).encode("utf-8")
        assert before.decode("utf-8").count(plan["old_target"]) == 1
        assert (repo / plan["source"]).read_bytes() == expected
        assert result["replacement_count"] == "1" and result["change_scope"] == "EXACT_PATH_TOKEN_ONLY"
        assert result["before_sha256"] == sha256(before) and result["after_sha256"] == sha256(expected)

    colocated_results = load_tsv(output / "COLOCATED_REFERENCE_RESULT.tsv")
    assert len(colocated_results) == 1 and colocated_results[0]["postmove_resolves"] == "YES"
    for row in colocated:
        source = repo / row["source"]
        assert source.read_bytes() == git_blob(repo, args.mutation_base, row["source"])
        assert boundary.occurrences(source.read_text(encoding="utf-8"), row["target"])
        assert (source.parent / row["target"]).is_file()

    # Every selected candidate is unchanged except the two byte-identical moves and
    # STATE.md's separately verified exact path substitution.
    move_destinations = {row["old_path"]: row["new_path"] for row in moves}
    for row in candidates:
        base_payload = git_blob(repo, args.base, row["path"])
        if row["path"] == "STATE.md":
            continue
        current_path = move_destinations.get(row["path"], row["path"])
        assert (repo / current_path).read_bytes() == base_payload, row["path"]
        assert sha256(base_payload) == row["sha256_at_base"]

    # Preregistration and premove adjudication are immutable historical records.
    historical_records = [
        path for path in str(run(repo, ["git", "ls-tree", "-r", "--name-only", args.mutation_base, "--", "reorganization_r1b"])).splitlines()
        if path and not path.startswith("reorganization_r1b/migration/")
    ]
    for path in historical_records:
        assert (repo / path).read_bytes() == git_blob(repo, args.mutation_base, path), path

    texts = tracked_texts(repo)
    generated_pointer_outputs = {
        str((output / "POSTMOVE_POINTER_CENSUS.tsv").relative_to(repo)),
        str((output / "MIGRATION_VERIFY_RESULT.json").relative_to(repo)),
    }
    for source in generated_pointer_outputs:
        texts.pop(source, None)
    historical_sources = {
        source for source, immutability in source_classes.items() if immutability == "HISTORICAL_SNAPSHOT"
    }
    pointer_census: list[dict[str, Any]] = []
    stale: list[tuple[str, int, str]] = []
    literal_checks: dict[str, str] = {}
    for move in moves:
        old, new = move["old_path"], move["new_path"]
        matcher_rows: set[tuple[str, int, int]] = set()
        for source, text in texts.items():
            for offset in boundary.occurrences(text, old):
                line, column = line_column(text, offset)
                matcher_rows.add((source, line, column))
                operational = not source.startswith("reorganization_r") and source not in historical_sources
                if text[max(0, offset - len("archive/pre_2026-07-01/")):offset] == "archive/pre_2026-07-01/":
                    role = "NEW_PATH_SUFFIX"
                elif source.startswith("reorganization_r"):
                    role = "REORGANIZATION_AUDIT_RECORD"
                elif source in historical_sources:
                    role = "HISTORICAL_SNAPSHOT_SOURCE"
                elif (repo / source).parent.joinpath(old).is_file():
                    role = "COLOCATED_REFERENCE"
                elif source == new:
                    role = "BYTE_PRESERVED_MOVED_RECORD"
                else:
                    role = "STALE_NON_FROZEN_OPERATIONAL_POINTER" if operational else "FORENSIC_ONLY_REFERENCE"
                    if operational:
                        stale.append((source, line, old))
                pointer_census.append(
                    {
                        "moved_path": old,
                        "source": source,
                        "line": line,
                        "column": column,
                        "operational_source": "YES" if operational else "NO",
                        "source_immutability": source_classes.get(source, "GENERATED_OR_UNREGISTERED"),
                        "role": role,
                    }
                )
        literal = literal_git_grep(repo, old, boundary, generated_pointer_outputs)
        assert matcher_rows == literal, f"literal git grep mismatch for {old}"
        literal_checks[old] = "PASS"
    assert not stale, f"stale operational pointers: {stale[:20]}"
    write_tsv(
        output / "POSTMOVE_POINTER_CENSUS.tsv",
        sorted(pointer_census, key=lambda row: (row["moved_path"], row["source"], int(row["line"]))),
        ("moved_path", "source", "line", "column", "operational_source", "source_immutability", "role"),
    )

    frozen_results = []
    for package, manifest_sha in EXPECTED_MANIFESTS.items():
        manifest = repo / package / "SHA256SUMS.txt"
        assert sha256(manifest.read_bytes()) == manifest_sha, package
        base_state, base_count = package_state_from_git(repo, args.base, package)
        current_state, current_count = package_state_from_worktree(repo, args.base, package)
        assert (base_state, base_count) == (current_state, current_count), package
        frozen_results.append(
            {
                "package": package,
                "manifest_sha256": manifest_sha,
                "tracked_files": current_count,
                "complete_state_sha256": current_state,
                "result": "PASS",
            }
        )

    recorded_dirty = {row["path"]: row for row in load_tsv(args.dirty_inventory)}
    current_dirty = current_dirty_metadata(args.dirty_checkout.resolve())
    assert len(recorded_dirty) == len(current_dirty) == 54
    assert set(recorded_dirty) == set(current_dirty)
    for path, (status_code, size, object_type) in current_dirty.items():
        row = recorded_dirty[path]
        assert (row["status"], int(row["size_bytes_lstat"]), row["object_type"], row["content_sha256"]) == (
            status_code,
            size,
            object_type,
            "NOT_READ",
        )

    changed = str(run(repo, ["git", "diff", "--name-status", "--find-renames=100%", args.mutation_base])).splitlines()
    seen_renames: set[tuple[str, str]] = set()
    seen_modified: set[str] = set()
    for line in changed:
        fields = line.split("\t")
        if fields[0] == "M":
            assert fields[1] == "STATE.md", line
            seen_modified.add(fields[1])
        elif fields[0] == "A":
            assert fields[1].startswith("reorganization_r1b/"), line
        elif fields[0].startswith("R"):
            assert fields[0] == "R100" and len(fields) == 3, line
            seen_renames.add((fields[1], fields[2]))
        else:
            raise AssertionError(f"unauthorized diff: {line}")
    assert seen_modified == {"STATE.md"}
    assert seen_renames == {(row["old_path"], row["new_path"]) for row in moves}

    test_result = None
    if args.test_result:
        test_result = json.loads(args.test_result.read_text(encoding="utf-8"))
        assert test_result["baseline_match"] is True
        assert (test_result["passed"], test_result["failed"], test_result["xfailed"]) == (69, 1, 1)

    report = {
        "result": "PASS",
        "base": args.base,
        "mutation_base": args.mutation_base,
        "moved_files": len(moves),
        "r100_renames": len(seen_renames),
        "exact_path_substitutions": 1,
        "candidate_rows_verified": len(candidates),
        "candidate_payloads_byte_identical": len(candidates) - 1,
        "candidate_exact_path_only_edits": 1,
        "stale_non_frozen_operational_pointers": 0,
        "pointer_census_rows": len(pointer_census),
        "literal_git_grep_checks": literal_checks,
        "boundary_catchproof": boundary.catchproof(),
        "frozen_packages": frozen_results,
        "dirty_rows_metadata_only": len(current_dirty),
        "dirty_content_policy": "NOT_READ",
        "test_baseline": test_result,
    }
    (output / "MIGRATION_VERIFY_RESULT.json").write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
