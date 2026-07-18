#!/usr/bin/env python3
"""Final fail-closed verifier for Phase R1B."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import stat
import subprocess
from collections import Counter
from pathlib import Path
from typing import Any


PACKAGES = {
    "native_action_stage1_2026-07-18/arm_A": "d72e8d6e1b4bc8682bd5518264a1a43a3b5f7b3b246b3d218ea6bfecc6927d19",
    "native_action_stage1_2026-07-18/arm_B": "a99937a8fbba57ac24f490c2974937718f7dfbc2f2f7dd7c960d57fc5e839b92",
    "native_action_stage2_2026-07-18/arm_A": "ad63ffacdd5282a35fe0aef62269464d987aa61b710a4d393d95836234fd670a",
    "native_action_stage2_2026-07-18/arm_B": "30b2a3863f1d16e3b3507b5d0bf10a6b5b59c1e54d769cacc53127cc676d6d45",
    "native_action_arm_c_2026-07-18": "99fc0d6c26aff24e43b8636d74f80e3486c56131590552308b47c1d107ed500f",
    "native_action_final_adjudication_2026-07-18": "57be0046432c27046e84eaafd1706959558f43170d0f1e23dc3047966e512f33",
}
REORGANIZATION_PREFIXES = ("reorganization_r0/", "reorganization_r1a/", "reorganization_r1b/")
ALLOWED_ADDITIONS = {
    "reorganization_r1b/DUAL_CENSUS_COMPARISON.json",
    "reorganization_r1b/FINAL_VERIFY_RESULT.json",
    "reorganization_r1b/R1B_AUDIT_REPORT.md",
    "reorganization_r1b/README.md",
    "reorganization_r1b/build_r1b_postmove_censuses.py",
    "reorganization_r1b/final_validation/TEST_BASELINE.json",
    "reorganization_r1b/final_validation/TEST_BASELINE.txt",
    "reorganization_r1b/postmove_forensic_census/DEPENDENCY_MAP.tsv",
    "reorganization_r1b/postmove_forensic_census/DIRTY_WORKSTATION_INVENTORY.tsv",
    "reorganization_r1b/postmove_forensic_census/ROOT_FILE_INVENTORY.tsv",
    "reorganization_r1b/postmove_forensic_census/SCAN_SUMMARY.json",
    "reorganization_r1b/postmove_operational_census/DEPENDENCY_MAP.tsv",
    "reorganization_r1b/postmove_operational_census/SCAN_SUMMARY.json",
    "reorganization_r1b/verify_r1b_final.py",
}


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


def load_tsv(path: Path) -> tuple[list[dict[str, str]], tuple[str, ...]]:
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        rows = list(reader)
        assert reader.fieldnames
        return rows, tuple(reader.fieldnames)


def sha256(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def git_blob(repo: Path, revision: str, path: str) -> bytes:
    return bytes(run(repo, ["git", "show", f"{revision}:{path}"], binary=True))


def git_paths(repo: Path, revision: str) -> list[str]:
    raw = str(run(repo, ["git", "ls-tree", "-r", "-z", "--name-only", revision]))
    return [path for path in raw.split("\0") if path]


def current_dirty_metadata(checkout: Path) -> dict[str, tuple[str, int, str]]:
    env = os.environ.copy()
    env["GIT_OPTIONAL_LOCKS"] = "0"
    raw = subprocess.check_output(
        ["git", "--no-optional-locks", "status", "--porcelain=v2", "-z", "--untracked-files=all"],
        cwd=checkout,
        env=env,
    )
    records = raw.split(b"\0")
    result: dict[str, tuple[str, int, str]] = {}
    index = 0
    while index < len(records):
        record = records[index]
        index += 1
        if not record:
            continue
        marker = record[:1]
        if marker == b"1":
            fields = record.split(b" ", 8)
            status_code, raw_path = fields[1].decode("ascii", "replace"), fields[8]
        elif marker == b"2":
            fields = record.split(b" ", 9)
            status_code, raw_path = fields[1].decode("ascii", "replace"), fields[9]
            index += 1
        elif marker == b"u":
            fields = record.split(b" ", 10)
            status_code, raw_path = fields[1].decode("ascii", "replace"), fields[10]
        elif marker in {b"?", b"!"}:
            status_code, raw_path = ("??" if marker == b"?" else "!!"), record[2:]
        else:
            raise AssertionError(f"unknown status record: {record[:80]!r}")
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


def counts(rows: list[dict[str, str]], field: str) -> dict[str, int]:
    return dict(sorted(Counter(row[field] for row in rows).items()))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--base", required=True)
    parser.add_argument("--mutation-base", required=True)
    parser.add_argument("--migration-commit", required=True)
    parser.add_argument("--dirty-checkout", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    repo = args.repo.resolve()

    assert str(run(repo, ["git", "rev-parse", f"{args.migration_commit}^"])).strip() == args.mutation_base
    assert str(run(repo, ["git", "rev-parse", args.migration_commit])).strip() == args.migration_commit

    # The migration commit contains exactly the authorized State edit, R100 pair, and audit additions.
    migration_diff = str(
        run(repo, ["git", "diff", "--name-status", "--find-renames=100%", args.mutation_base, args.migration_commit])
    ).splitlines()
    renames: set[tuple[str, str]] = set()
    modifications: set[str] = set()
    for line in migration_diff:
        fields = line.split("\t")
        if fields[0] == "M":
            modifications.add(fields[1])
        elif fields[0] == "R100":
            renames.add((fields[1], fields[2]))
        elif fields[0] == "A":
            assert fields[1].startswith("reorganization_r1b/"), line
        else:
            raise AssertionError(f"unauthorized migration diff: {line}")
    assert modifications == {"STATE.md"}
    assert renames == {
        ("STEP2_timelive_matter_MAP.md", "archive/pre_2026-07-01/STEP2_timelive_matter_MAP.md"),
        ("p4_VERIFIER.md", "archive/pre_2026-07-01/p4_VERIFIER.md"),
    }

    # Nothing present at the migration checkpoint may be modified or removed afterward.
    for path in git_paths(repo, args.migration_commit):
        assert (repo / path).is_file(), path
        assert (repo / path).read_bytes() == git_blob(repo, args.migration_commit, path), path
    current_diff = str(run(repo, ["git", "diff", "--name-status", args.migration_commit])).splitlines()
    additions = set()
    for line in current_diff:
        fields = line.split("\t")
        assert fields[0] == "A" and fields[1] in ALLOWED_ADDITIONS, line
        additions.add(fields[1])
    assert additions == ALLOWED_ADDITIONS

    candidate_rows, _ = load_tsv(repo / "reorganization_r1b/adjudication/CANDIDATE_ADJUDICATION.tsv")
    assert len(candidate_rows) == 99
    assert counts(candidate_rows, "classification") == {
        "ACTIVE_CROSS_ERA": 17,
        "ARCHIVE_ELIGIBLE": 2,
        "BLOCKED": 8,
        "HARD_FROZEN": 58,
        "HISTORICAL_SNAPSHOT": 2,
        "PERMANENT_ROOT": 10,
        "SOFT_EVIDENCE_PATH_ONLY": 2,
    }
    assert {row["path"] for row in candidate_rows if row["move_authorized"] == "YES"} == {
        "STEP2_timelive_matter_MAP.md",
        "p4_VERIFIER.md",
    }

    migration_rows, _ = load_tsv(repo / "reorganization_r1b/migration/MIGRATION_RESULT.tsv")
    assert len(migration_rows) == 2
    for row in migration_rows:
        payload = (repo / row["new_path"]).read_bytes()
        assert not (repo / row["old_path"]).exists()
        assert row["content_identical"] == "YES"
        assert row["git_blob_oid_before"] == row["git_blob_oid_after"]
        assert row["sha256_before"] == row["sha256_after"] == sha256(payload)
    pointer_rows, _ = load_tsv(repo / "reorganization_r1b/migration/POSTMOVE_POINTER_CENSUS.tsv")
    assert not [row for row in pointer_rows if row["role"] == "STALE_NON_FROZEN_OPERATIONAL_POINTER"]

    forensic_map_path = repo / "reorganization_r1b/postmove_forensic_census/DEPENDENCY_MAP.tsv"
    operational_map_path = repo / "reorganization_r1b/postmove_operational_census/DEPENDENCY_MAP.tsv"
    forensic_rows, forensic_fields = load_tsv(forensic_map_path)
    operational_rows, operational_fields = load_tsv(operational_map_path)
    assert forensic_fields == operational_fields
    expected_operational = [
        row for row in forensic_rows if not row["source"].startswith(REORGANIZATION_PREFIXES)
    ]
    assert operational_rows == expected_operational
    forensic_summary = json.loads(
        (repo / "reorganization_r1b/postmove_forensic_census/SCAN_SUMMARY.json").read_text(encoding="utf-8")
    )
    operational_summary = json.loads(
        (repo / "reorganization_r1b/postmove_operational_census/SCAN_SUMMARY.json").read_text(encoding="utf-8")
    )
    comparison = json.loads(
        (repo / "reorganization_r1b/DUAL_CENSUS_COMPARISON.json").read_text(encoding="utf-8")
    )
    assert forensic_summary["base_commit"] == args.migration_commit
    assert forensic_summary["dependency_edge_count"] == len(forensic_rows) == 25470
    assert operational_summary["dependency_edge_count"] == len(operational_rows) == 14827
    assert comparison["postmove_historical_reorganization_edges_excluded"] == 10643
    assert comparison["stale_non_frozen_operational_pointers"] == 0
    assert comparison["generated_audit_records_influence_selection"] is False
    assert sha256(forensic_map_path.read_bytes()) == comparison["forensic_map_sha256"]
    assert sha256(operational_map_path.read_bytes()) == comparison["operational_map_sha256"]

    frozen_results = []
    for package, expected_manifest_sha in PACKAGES.items():
        manifest = repo / package / "SHA256SUMS.txt"
        assert sha256(manifest.read_bytes()) == expected_manifest_sha
        replay = subprocess.run(
            ["sha256sum", "--check", "SHA256SUMS.txt"],
            cwd=repo / package,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=False,
        )
        assert replay.returncode == 0, f"{package}: {replay.stdout}\n{replay.stderr}"
        frozen_results.append({"package": package, "manifest_sha256": expected_manifest_sha, "replay": "PASS"})

    dirty_rows, _ = load_tsv(repo / "reorganization_r1b/base_forensic_census/DIRTY_WORKSTATION_INVENTORY.tsv")
    recorded_dirty = {row["path"]: row for row in dirty_rows}
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

    test_result = json.loads(
        (repo / "reorganization_r1b/final_validation/TEST_BASELINE.json").read_text(encoding="utf-8")
    )
    assert test_result["baseline_match"] is True
    assert (test_result["passed"], test_result["failed"], test_result["xfailed"]) == (69, 1, 1)

    result: dict[str, Any] = {
        "result": "PASS",
        "base": args.base,
        "mutation_base": args.mutation_base,
        "migration_commit": args.migration_commit,
        "candidate_rows": len(candidate_rows),
        "classification_counts": counts(candidate_rows, "classification"),
        "moved_files": len(migration_rows),
        "r100_renames": len(renames),
        "exact_path_substitutions": 1,
        "postmove_full_forensic_edges": len(forensic_rows),
        "postmove_operational_edges": len(operational_rows),
        "excluded_historical_reorganization_edges": len(forensic_rows) - len(operational_rows),
        "stale_non_frozen_operational_pointers": 0,
        "frozen_manifest_replays": frozen_results,
        "dirty_workstation_rows_metadata_only": len(current_dirty),
        "dirty_content_policy": "NOT_READ",
        "test_baseline": test_result,
        "generated_audit_records_influence_selection": False,
        "authorized_final_additions": len(additions),
    }
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
