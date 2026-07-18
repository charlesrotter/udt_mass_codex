#!/usr/bin/env python3
"""Independent fail-closed final verifier for R1F B01."""

from __future__ import annotations

import argparse
import copy
import csv
import hashlib
import json
import re
import stat
import subprocess
from collections import Counter
from pathlib import Path
from urllib.parse import unquote


BASE = "14ba31a77aed1553c5df8ecd59b0f7a000c10e20"
MIGRATION_COMMIT = "c4cf405bba49625a9352a022b60754e7249c27f9"
ROLLBACK_PARENT = "fa211047fd9d81fcc64c424376facc6378837dfc"
PACKAGES = {
    "native_action_stage1_2026-07-18/arm_A": "d72e8d6e1b4bc8682bd5518264a1a43a3b5f7b3b246b3d218ea6bfecc6927d19",
    "native_action_stage1_2026-07-18/arm_B": "a99937a8fbba57ac24f490c2974937718f7dfbc2f2f7dd7c960d57fc5e839b92",
    "native_action_stage2_2026-07-18/arm_A": "ad63ffacdd5282a35fe0aef62269464d987aa61b710a4d393d95836234fd670a",
    "native_action_stage2_2026-07-18/arm_B": "30b2a3863f1d16e3b3507b5d0bf10a6b5b59c1e54d769cacc53127cc676d6d45",
    "native_action_arm_c_2026-07-18": "99fc0d6c26aff24e43b8636d74f80e3486c56131590552308b47c1d107ed500f",
    "native_action_final_adjudication_2026-07-18": "57be0046432c27046e84eaafd1706959558f43170d0f1e23dc3047966e512f33",
}
LEDGER_FIELDS = [
    "migration_id", "committed_at_utc", "phase", "batch_id", "original_path",
    "old_current_path", "new_current_path", "rename_score", "git_blob_oid_before",
    "git_blob_oid_after", "sha256_before", "sha256_after", "pointer_change_record",
    "verification_record", "commit", "rollback_parent", "notes",
]


class GateError(AssertionError):
    def __init__(self, code: str, detail: str = "") -> None:
        super().__init__(f"{code}: {detail}")
        self.code = code


def run(repo: Path, command: list[str], binary: bool = False, check: bool = True):
    result = subprocess.run(command, cwd=repo, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                            text=not binary, check=False)
    if check and result.returncode:
        err = result.stderr if not binary else result.stderr.decode("utf-8", "replace")
        raise AssertionError(f"command failed: {' '.join(command)}\n{err}")
    return result


def git(repo: Path, *args: str, binary: bool = False, check: bool = True):
    result = run(repo, ["git", *args], binary=binary, check=check)
    return result.stdout if check else result


def rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def sha(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def expect(code: str, callback) -> str:
    try:
        callback()
    except GateError as exc:
        if exc.code == code:
            return "PASS"
        raise AssertionError(f"expected {code}, got {exc.code}") from exc
    raise AssertionError(f"catch-proof accepted corruption; expected {code}")


def validate_moves(repo: Path, batch: list[dict[str, str]]) -> None:
    if len(batch) != 4:
        raise GateError("MISSING_MOVE", str(len(batch)))
    index_lines = str(git(repo, "ls-files", "-s")).splitlines()
    by_oid: dict[str, list[str]] = {}
    for line in index_lines:
        fields = line.split(None, 3)
        by_oid.setdefault(fields[1], []).append(fields[3])
    for item in batch:
        old, destination = item["current_path"], item["destination"]
        if (repo / old).exists() or not (repo / destination).is_file():
            raise GateError("WRONG_DESTINATION", f"{old}->{destination}")
        if sha((repo / destination).read_bytes()) != item["sha256"]:
            raise GateError("ARTIFACT_MUTATION", destination)
        oid = str(git(repo, "hash-object", "--no-filters", destination)).strip()
        if oid != item["git_blob_oid"]:
            raise GateError("ARTIFACT_MUTATION", destination)
        if by_oid.get(oid) != [destination]:
            raise GateError("DUPLICATE_ARTIFACT", destination)


def validate_behavior(pre: list[dict[str, str]], post: list[dict[str, str]]) -> None:
    before = {row["original_path"]: row for row in pre}
    after = {row["original_path"]: row for row in post}
    if len(before) != 4 or set(before) != set(after):
        raise GateError("BEHAVIOR_OUTPUT_MISMATCH", "coverage")
    for path in before:
        for field in ("exit_code", "stdout_size", "stdout_sha256", "stderr_size", "stderr_sha256",
                      "python_version", "python_executable", "sympy_version"):
            if before[path][field] != after[path][field]:
                raise GateError("BEHAVIOR_OUTPUT_MISMATCH", f"{path}:{field}")


def validate_current(repo: Path, current: list[dict[str, str]], batch: list[dict[str, str]]) -> Counter:
    if len(current) != 1114:
        raise GateError("CURRENT_MAP_COUNT", str(len(current)))
    originals = [row["original_path"] for row in current]
    destinations = [row["current_path"] for row in current]
    if len(set(originals)) != 1114:
        raise GateError("DUPLICATE_ORIGINAL_PATH")
    if len(set(destinations)) != 1114:
        raise GateError("DUPLICATE_CURRENT_PATH")
    counts = Counter(row["path_status"] for row in current)
    if counts != Counter({"ROOT_RETAINED": 1109, "MIGRATED_R1D": 1, "MIGRATED_R1F": 4}):
        raise GateError("CURRENT_MAP_STATUS", str(counts))
    by_original = {row["original_path"]: row for row in current}
    for item in batch:
        mapped = by_original[item["current_path"]]
        if mapped["current_path"] != item["destination"] or mapped["path_status"] != "MIGRATED_R1F":
            raise GateError("STALE_CURRENT_POINTER", item["current_path"])
    if not all((repo / row["current_path"]).exists() for row in current):
        raise GateError("STALE_CURRENT_POINTER", "missing mapped target")
    return counts


def validate_occurrences(occurrences: list[dict[str, str]]) -> None:
    if not occurrences:
        raise GateError("STALE_CURRENT_POINTER", "empty census")
    if any(row["classification"] == "STALE_CURRENT_POINTER" for row in occurrences):
        raise GateError("STALE_CURRENT_POINTER", "classified stale row")


def commit_parent(repo: Path, commit: str) -> str:
    return str(git(repo, "rev-parse", f"{commit}^")).strip()


def validate_ledger(repo: Path, ledger: list[dict[str, str]], batch: list[dict[str, str]]) -> None:
    if len(ledger) != 4 or list(ledger[0]) != LEDGER_FIELDS:
        raise GateError("INVALID_LEDGER_COMMIT", "schema/count")
    if {row["commit"] for row in ledger} != {MIGRATION_COMMIT}:
        raise GateError("INVALID_LEDGER_COMMIT", "commit field")
    if {row["rollback_parent"] for row in ledger} != {ROLLBACK_PARENT}:
        raise GateError("INVALID_LEDGER_COMMIT", "parent field")
    if commit_parent(repo, MIGRATION_COMMIT) != ROLLBACK_PARENT:
        raise GateError("INVALID_LEDGER_COMMIT", "Git parent")
    ancestor = git(repo, "merge-base", "--is-ancestor", MIGRATION_COMMIT, "HEAD", check=False)
    if ancestor.returncode != 0:
        raise GateError("INVALID_LEDGER_COMMIT", "not ancestor")
    self_ref = git(repo, "cat-file", "-e", f"{MIGRATION_COMMIT}:research/_registry/MIGRATION_LEDGER.tsv", check=False)
    if self_ref.returncode == 0:
        raise GateError("INVALID_LEDGER_COMMIT", "self-referential ledger")
    by_old = {row["old_current_path"]: row for row in ledger}
    if set(by_old) != {row["current_path"] for row in batch}:
        raise GateError("INVALID_LEDGER_COMMIT", "coverage")
    timestamp = str(git(repo, "show", "-s", "--format=%cI", MIGRATION_COMMIT)).strip()
    for item in batch:
        row = by_old[item["current_path"]]
        checks = {
            "committed_at_utc": timestamp, "phase": "R1F", "batch_id": item["batch_id"],
            "original_path": item["current_path"], "new_current_path": item["destination"],
            "rename_score": "R100", "git_blob_oid_before": item["git_blob_oid"],
            "git_blob_oid_after": item["git_blob_oid"], "sha256_before": item["sha256"],
            "sha256_after": item["sha256"], "verification_record": "reorganization_r1f/MIGRATION_VERIFY_RESULT.json",
        }
        if any(row[key] != value for key, value in checks.items()):
            raise GateError("INVALID_LEDGER_COMMIT", item["current_path"])


def validate_links(repo: Path) -> int:
    sources = [repo / "README.md"]
    sources += sorted((repo / "research").rglob("*.md"))
    sources += sorted((repo / "reorganization_r1f").rglob("*.md"))
    pattern = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
    count = 0
    for source in sources:
        for raw in pattern.findall(source.read_text(encoding="utf-8")):
            target = raw.strip().strip("<>")
            if target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            target = unquote(target.split("#", 1)[0])
            if not source.parent.joinpath(target).resolve().exists():
                raise AssertionError(f"broken link: {source}:{raw}")
            count += 1
    return count


def dirty_metadata(repo: Path) -> dict[str, tuple[str, int, str]]:
    raw = bytes(git(repo, "status", "--porcelain=v2", "-z", "--untracked-files=all", binary=True))
    records = raw.split(b"\0"); result = {}; index = 0
    while index < len(records):
        record = records[index]; index += 1
        if not record:
            continue
        marker = record[:1]
        if marker == b"1":
            fields = record.split(b" ", 8); code, raw_path = fields[1].decode(), fields[8]
        elif marker == b"2":
            fields = record.split(b" ", 9); code, raw_path = fields[1].decode(), fields[9]; index += 1
        elif marker == b"u":
            fields = record.split(b" ", 10); code, raw_path = fields[1].decode(), fields[10]
        elif marker in {b"?", b"!"}:
            code, raw_path = ("??" if marker == b"?" else "!!"), record[2:]
        else:
            raise AssertionError(f"unknown status record: {record[:40]!r}")
        path = raw_path.decode("utf-8", "surrogateescape")
        info = (repo / path).lstat()
        kind = "regular_file" if stat.S_ISREG(info.st_mode) else "directory" if stat.S_ISDIR(info.st_mode) else "symlink" if stat.S_ISLNK(info.st_mode) else "other"
        result[path] = (code, info.st_size, kind)
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--dirty-checkout", type=Path, required=True)
    parser.add_argument("--test-result", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(); repo = args.repo.resolve(); r1f = repo / "reorganization_r1f"

    batch = rows(r1f / "PREREGISTERED_BATCH.tsv")
    validate_moves(repo, batch)
    pre = rows(r1f / "pre_move/BEHAVIOR_RUNS.tsv")
    post = rows(r1f / "post_move/BEHAVIOR_RUNS.tsv")
    validate_behavior(pre, post)
    current = rows(repo / "research/_registry/CURRENT_ARTIFACT_PATHS.tsv")
    status_counts = validate_current(repo, current, batch)
    occurrences = rows(r1f / "OLD_PATH_OCCURRENCE_CLASSIFICATION.tsv")
    validate_occurrences(occurrences)
    ledger = rows(repo / "research/_registry/MIGRATION_LEDGER.tsv")
    validate_ledger(repo, ledger, batch)

    migration_changes = str(git(repo, "diff-tree", "--no-commit-id", "--name-status", "-r", "-M100%",
                                ROLLBACK_PARENT, MIGRATION_COMMIT)).splitlines()
    expected_renames = {f"R100\t{item['current_path']}\t{item['destination']}" for item in batch}
    if {line for line in migration_changes if line.startswith("R")} != expected_renames:
        raise AssertionError("migration commit does not contain four exact R100 renames")
    if str(git(repo, "diff", "--name-only", BASE, "--", "reorganization_r0", "reorganization_r1a",
               "reorganization_r1b", "reorganization_r1c", "reorganization_r1d", "reorganization_r1e")):
        raise AssertionError("R0-R1E record changed")
    final_changes = str(git(repo, "diff", "--name-status", MIGRATION_COMMIT)).splitlines()
    for line in final_changes:
        status, path = line.split("\t", 1)
        if status == "A" and path == "research/_registry/MIGRATION_LEDGER.tsv":
            continue
        if status in {"A", "M"} and path.startswith("reorganization_r1f/"):
            continue
        raise AssertionError(f"unauthorized post-migration diff: {line}")

    macro = {row["current_path"] for row in rows(repo / "research/macro/ROOT_INVENTORY.tsv")}
    if not all(item["destination"] in macro and item["current_path"] not in macro for item in batch):
        raise AssertionError("macro inventory mismatch")
    links = validate_links(repo)
    frontier = rows(repo / "research/_registry/CURRENT_FRONTIER_TARGETS.tsv")
    targets = {row["target_path"].rstrip("/") for row in frontier}
    if len(frontier) != 306 or len(targets) != 101 or not all((repo / target).exists() for target in targets):
        raise AssertionError("frontier verification failed")

    base_paths = set(str(git(repo, "ls-tree", "-r", "--name-only", BASE)).splitlines())
    current_paths = set(str(git(repo, "ls-files")).splitlines())
    index_oids = {line.split(None, 3)[3]: line.split()[1]
                  for line in str(git(repo, "ls-files", "-s")).splitlines()}
    manifests = []
    for package, digest in PACKAGES.items():
        manifest = repo / package / "SHA256SUMS.txt"
        if sha(manifest.read_bytes()) != digest:
            raise AssertionError(f"manifest drift: {package}")
        replay = run(repo / package, ["sha256sum", "--check", "SHA256SUMS.txt"])
        package_base = sorted(path for path in base_paths if path.startswith(package + "/"))
        package_current = sorted(path for path in current_paths if path.startswith(package + "/"))
        if not package_base or package_current != package_base:
            raise AssertionError(f"package path drift: {package}")
        for path in package_base:
            base_oid = str(git(repo, "rev-parse", f"{BASE}:{path}")).strip()
            if index_oids[path] != base_oid:
                raise AssertionError(f"package byte drift: {path}")
        manifests.append({"package": package, "manifest_sha256": digest,
                          "tracked_paths_byte_identical_to_base": len(package_base), "result": "PASS"})

    recorded = {row["path"]: row for row in rows(repo / "reorganization_r1b/postmove_forensic_census/DIRTY_WORKSTATION_INVENTORY.tsv")}
    dirty = dirty_metadata(args.dirty_checkout.resolve())
    if len(recorded) != len(dirty) or len(dirty) != 54 or set(recorded) != set(dirty):
        raise AssertionError("dirty checkout path metadata drift")
    for path, value in dirty.items():
        row = recorded[path]
        if (row["status"], int(row["size_bytes_lstat"]), row["object_type"], row["content_sha256"]) != (*value, "NOT_READ"):
            raise AssertionError(f"dirty checkout metadata drift: {path}")
    test = json.loads(args.test_result.read_text())
    if not test.get("baseline_match") or (test["passed"], test["failed"], test["xfailed"]) != (69, 1, 1):
        raise AssertionError("test baseline drift")

    bad_batch_missing = copy.deepcopy(batch[:-1])
    bad_batch_mutation = copy.deepcopy(batch); bad_batch_mutation[0]["sha256"] = "0" * 64
    bad_batch_destination = copy.deepcopy(batch); bad_batch_destination[0]["destination"] = "research/macro/not_the_registered_destination.py"
    bad_post = copy.deepcopy(post); bad_post[0]["stdout_sha256"] = "0" * 64
    bad_current = copy.deepcopy(current); bad_current[-1]["current_path"] = bad_current[0]["current_path"]
    bad_occurrences = copy.deepcopy(occurrences) + [{"classification": "STALE_CURRENT_POINTER"}]
    bad_ledger = copy.deepcopy(ledger); bad_ledger[0]["commit"] = BASE
    catchproof = {
        "missing_move_rejected": expect("MISSING_MOVE", lambda: validate_moves(repo, bad_batch_missing)),
        "artifact_mutation_rejected": expect("ARTIFACT_MUTATION", lambda: validate_moves(repo, bad_batch_mutation)),
        "wrong_destination_rejected": expect("WRONG_DESTINATION", lambda: validate_moves(repo, bad_batch_destination)),
        "behavioral_output_mismatch_rejected": expect("BEHAVIOR_OUTPUT_MISMATCH", lambda: validate_behavior(pre, bad_post)),
        "duplicate_current_path_rejected": expect("DUPLICATE_CURRENT_PATH", lambda: validate_current(repo, bad_current, batch)),
        "stale_pointer_rejected": expect("STALE_CURRENT_POINTER", lambda: validate_occurrences(bad_occurrences)),
        "invalid_ledger_commit_rejected": expect("INVALID_LEDGER_COMMIT", lambda: validate_ledger(repo, bad_ledger, batch)),
    }

    result = {
        "result": "PASS", "mode": "R1F_FINAL_EXTERNAL_FAIL_CLOSED_VERIFY", "base": BASE,
        "preregistration_commit": ROLLBACK_PARENT, "migration_commit": MIGRATION_COMMIT,
        "rollback_parent": ROLLBACK_PARENT, "r100_renames": 4,
        "identical_blobs_and_sha256": 4, "duplicate_copies": 0,
        "behaviorally_identical_runs": 4, "python_version": pre[0]["python_version"],
        "sympy_version": pre[0]["sympy_version"],
        "current_artifact_paths": {"rows": 1114, "unique_original_paths": 1114,
                                   "unique_current_paths": 1114, "status_counts": dict(status_counts)},
        "migration_ledger_rows": 4, "self_referential_ledger": False,
        "old_path_occurrences": len(occurrences), "stale_current_navigation_pointers": 0,
        "markdown_links_verified": links, "frontier_rows": 306, "frontier_unique_targets": 101,
        "frozen_manifest_replays": manifests, "dirty_workstation_rows_metadata_only": 54,
        "dirty_content_policy": "NOT_READ", "test_baseline": test, "catchproof": catchproof,
        "b02_b03_authorized": False,
    }
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
