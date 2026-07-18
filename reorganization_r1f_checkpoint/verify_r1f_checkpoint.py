#!/usr/bin/env python3
"""Fail-closed verifier for the R1F checkpoint integration."""

from __future__ import annotations

import argparse
import copy
import csv
import hashlib
import json
import os
import re
import stat
import subprocess
import sys
from collections import Counter
from pathlib import Path
from urllib.parse import unquote


SOURCE = "3bb88a6b6cfc223d308b8bae6e27d69b1a1b119f"
EXPECTED_GROK = "b59005dba9acaf6c575185876655bd6a5c792094"
MIGRATION_COMMIT = "c4cf405bba49625a9352a022b60754e7249c27f9"
ROLLBACK_PARENT = "fa211047fd9d81fcc64c424376facc6378837dfc"
AUTHORIZED = {
    "LIVE.md", "HANDOFF.md", "INDEX.md", "README.md", "research/README.md",
    "research/_registry/README.md",
}
EXPECTED_STREAMS = {
    "verify_center_escape.py": "f3e0c8d0212d5c01e54abc8de013dd3b62a98b3f6b5583a254c135808c3deff9",
    "verify_center_nogo.py": "a9eae7d513ef994897f04e139f38281dd4372628c443d0d4d3180629e4cbed59",
    "verify_eos_dS_window.py": "310a145c46a66d82c3cbd99df568a41ec562a98b648a6fbacbb3dfd5522bc2d4",
    "verify_wrl_canon.py": "49864b66db59f6f5a4e053f70c4c051f9537d514bd2e3bc1631cfc68888714c8",
}
EMPTY_SHA = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
PACKAGES = {
    "native_action_stage1_2026-07-18/arm_A": "d72e8d6e1b4bc8682bd5518264a1a43a3b5f7b3b246b3d218ea6bfecc6927d19",
    "native_action_stage1_2026-07-18/arm_B": "a99937a8fbba57ac24f490c2974937718f7dfbc2f2f7dd7c960d57fc5e839b92",
    "native_action_stage2_2026-07-18/arm_A": "ad63ffacdd5282a35fe0aef62269464d987aa61b710a4d393d95836234fd670a",
    "native_action_stage2_2026-07-18/arm_B": "30b2a3863f1d16e3b3507b5d0bf10a6b5b59c1e54d769cacc53127cc676d6d45",
    "native_action_arm_c_2026-07-18": "99fc0d6c26aff24e43b8636d74f80e3486c56131590552308b47c1d107ed500f",
    "native_action_final_adjudication_2026-07-18": "57be0046432c27046e84eaafd1706959558f43170d0f1e23dc3047966e512f33",
}


class GateError(AssertionError):
    def __init__(self, code: str, detail: str = "") -> None:
        super().__init__(f"{code}: {detail}")
        self.code = code


def run(cwd: Path, command: list[str], *, binary: bool = False, check: bool = True,
        env: dict[str, str] | None = None) -> subprocess.CompletedProcess:
    result = subprocess.run(command, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                            text=not binary, check=False, env=env)
    if check and result.returncode:
        error = result.stderr if not binary else result.stderr.decode("utf-8", "replace")
        raise AssertionError(f"command failed: {' '.join(command)}\n{error}")
    return result


def git(repo: Path, *args: str, binary: bool = False, check: bool = True):
    result = run(repo, ["git", *args], binary=binary, check=check)
    return result.stdout if check else result


def rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def sha(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def catch(code: str, callback) -> str:
    try:
        callback()
    except GateError as exc:
        if exc.code == code:
            return "PASS"
        raise AssertionError(f"expected {code}, got {exc.code}") from exc
    raise AssertionError(f"catch-proof accepted corruption: {code}")


def validate_remote(repo: Path, expected: str = EXPECTED_GROK) -> tuple[str, str, int]:
    observed = str(git(repo, "rev-parse", "origin/grok")).strip()
    merge_base = str(git(repo, "merge-base", "origin/grok", SOURCE)).strip()
    ancestor = git(repo, "merge-base", "--is-ancestor", "origin/grok", SOURCE, check=False)
    if observed != expected or merge_base != expected or ancestor.returncode:
        raise GateError("REMOTE_GUARD", f"{observed}:{merge_base}:{ancestor.returncode}")
    count = int(str(git(repo, "rev-list", "--count", f"origin/grok..{SOURCE}")).strip())
    return observed, merge_base, count


def validate_scope(repo: Path, extra: str | None = None) -> list[str]:
    changed = set(str(git(repo, "diff", "--name-only", SOURCE)).splitlines())
    changed.update(str(git(repo, "ls-files", "--others", "--exclude-standard")).splitlines())
    if extra:
        changed.add(extra)
    invalid = sorted(path for path in changed
                     if path not in AUTHORIZED and not path.startswith("reorganization_r1f_checkpoint/"))
    if invalid:
        raise GateError("UNAUTHORIZED_EDIT", ",".join(invalid))
    if not AUTHORIZED.issubset(changed):
        raise GateError("AUTHORIZED_FILE_MISSING", ",".join(sorted(AUTHORIZED - changed)))
    for historical in ("reorganization_r0", "reorganization_r1a", "reorganization_r1b",
                       "reorganization_r1c", "reorganization_r1d", "reorganization_r1e",
                       "reorganization_r1f"):
        if str(git(repo, "diff", "--name-only", SOURCE, "--", historical)).strip():
            raise GateError("UNAUTHORIZED_EDIT", historical)
    return sorted(changed)


def validate_navigation(repo: Path) -> None:
    required = {
        "LIVE.md": ("R0–R1F REORGANIZATION CHECKPOINT COMPLETE", "B02/B03 remain proposals"),
        "HANDOFF.md": ("R0–R1F reorganization checkpoint complete", "B02/B03 remain proposals"),
        "INDEX.md": ("R1E batch planning and R1F/B01 are complete", "B02/B03 remain proposals"),
        "README.md": ("Repository reorganization checkpoint R0–R1F", "MIGRATION_LEDGER.tsv"),
        "research/README.md": ("Five active artifacts", "B02/B03 remain proposals"),
        "research/_registry/README.md": ("four `MIGRATED_R1F`", "MIGRATION_LEDGER.tsv"),
    }
    for path, needles in required.items():
        text = (repo / path).read_text(encoding="utf-8")
        if any(needle not in text for needle in needles):
            raise GateError("NAVIGATION_WORDING", path)
    for path in ("LIVE.md", "HANDOFF.md", "INDEX.md"):
        top = "\n".join((repo / path).read_text(encoding="utf-8").splitlines()[:60])
        if "R0–R1D" in top or "one active artifact" in top.lower():
            raise GateError("STALE_WORDING", path)


def validate_current(repo: Path, current: list[dict[str, str]]) -> Counter:
    if len(current) != 1114:
        raise GateError("CURRENT_MAP", f"rows={len(current)}")
    original = [row["original_path"] for row in current]
    target = [row["current_path"] for row in current]
    counts = Counter(row["path_status"] for row in current)
    expected = Counter({"ROOT_RETAINED": 1109, "MIGRATED_R1D": 1, "MIGRATED_R1F": 4})
    if len(set(original)) != 1114 or len(set(target)) != 1114 or counts != expected:
        raise GateError("CURRENT_MAP", f"unique={len(set(original))}/{len(set(target))};{counts}")
    missing = [path for path in target if not (repo / path).exists()]
    if missing:
        raise GateError("CURRENT_MAP", missing[0])
    return counts


def validate_renames(repo: Path, batch: list[dict[str, str]], override: set[str] | None = None) -> list[str]:
    actual = set(str(git(repo, "diff-tree", "--no-commit-id", "--name-status", "-r", "-M100%",
                         ROLLBACK_PARENT, MIGRATION_COMMIT)).splitlines())
    renames = {line for line in actual if line.startswith("R")}
    expected = {f"R100\t{row['current_path']}\t{row['destination']}" for row in batch}
    if override is not None:
        renames = override
    if renames != expected:
        raise GateError("R100_IDENTITY", f"{sorted(renames)}")
    for row in batch:
        destination = repo / row["destination"]
        if (repo / row["current_path"]).exists() or not destination.is_file():
            raise GateError("R100_IDENTITY", row["current_path"])
        if sha(destination.read_bytes()) != row["sha256"]:
            raise GateError("R100_IDENTITY", row["destination"])
        oid = str(git(repo, "hash-object", "--no-filters", row["destination"])).strip()
        if oid != row["git_blob_oid"]:
            raise GateError("R100_IDENTITY", row["destination"])
    return sorted(renames)


def validate_recorded_behavior(pre: list[dict[str, str]], post: list[dict[str, str]],
                               corrupt: bool = False) -> None:
    by_pre = {row["original_path"]: row for row in pre}
    by_post = {row["original_path"]: row for row in post}
    if corrupt:
        by_post = copy.deepcopy(by_post)
        by_post[next(iter(by_post))]["stdout_sha256"] = "0" * 64
    if set(by_pre) != set(EXPECTED_STREAMS) or set(by_pre) != set(by_post):
        raise GateError("BEHAVIOR_HASH", "coverage")
    for path, expected_stdout in EXPECTED_STREAMS.items():
        before, after = by_pre[path], by_post[path]
        if before["exit_code"] != "0" or after["exit_code"] != "0":
            raise GateError("BEHAVIOR_HASH", f"{path}:exit")
        if before["stdout_sha256"] != expected_stdout or after["stdout_sha256"] != expected_stdout:
            raise GateError("BEHAVIOR_HASH", f"{path}:stdout")
        if before["stderr_sha256"] != EMPTY_SHA or after["stderr_sha256"] != EMPTY_SHA:
            raise GateError("BEHAVIOR_HASH", f"{path}:stderr")
        for field in ("exit_code", "stdout_size", "stdout_sha256", "stderr_size", "stderr_sha256",
                      "python_version", "python_executable", "sympy_version"):
            if before[field] != after[field]:
                raise GateError("BEHAVIOR_HASH", f"{path}:{field}")


def replay_behavior(repo: Path, batch: list[dict[str, str]], output_dir: Path) -> list[dict[str, object]]:
    output_dir.mkdir(parents=True, exist_ok=True)
    env = dict(os.environ); env["CUDA_VISIBLE_DEVICES"] = ""; env["PYTHONDONTWRITEBYTECODE"] = "1"
    records = []
    for row in batch:
        completed = run(repo, ["timeout", "30s", "python3", row["destination"]], binary=True,
                        check=False, env=env)
        stem = Path(row["current_path"]).stem
        stdout_path = output_dir / f"{stem}.stdout.txt"
        stderr_path = output_dir / f"{stem}.stderr.txt"
        stdout_path.write_bytes(completed.stdout); stderr_path.write_bytes(completed.stderr)
        record = {
            "original_path": row["current_path"], "executed_path": row["destination"],
            "command": f"env CUDA_VISIBLE_DEVICES= PYTHONDONTWRITEBYTECODE=1 timeout 30s python3 {row['destination']}",
            "exit_code": completed.returncode, "stdout_size": len(completed.stdout),
            "stdout_sha256": sha(completed.stdout), "stderr_size": len(completed.stderr),
            "stderr_sha256": sha(completed.stderr),
        }
        if (record["exit_code"] != 0 or record["stdout_sha256"] != EXPECTED_STREAMS[row["current_path"]]
                or record["stderr_sha256"] != EMPTY_SHA):
            raise GateError("BEHAVIOR_REPLAY", row["current_path"])
        records.append(record)
    fields = list(records[0])
    with (output_dir / "BEHAVIORAL_REPLAY.tsv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader(); writer.writerows(records)
    return records


def validate_ledger(repo: Path, ledger: list[dict[str, str]], batch: list[dict[str, str]],
                    corrupt: bool = False) -> None:
    working = copy.deepcopy(ledger)
    if corrupt:
        working[0]["rollback_parent"] = SOURCE
    if len(working) != 4 or {row["commit"] for row in working} != {MIGRATION_COMMIT}:
        raise GateError("LEDGER", "commit/count")
    if {row["rollback_parent"] for row in working} != {ROLLBACK_PARENT}:
        raise GateError("LEDGER", "rollback parent")
    real_parent = str(git(repo, "rev-parse", f"{MIGRATION_COMMIT}^")).strip()
    if real_parent != ROLLBACK_PARENT:
        raise GateError("LEDGER", "Git parent")
    self_reference = git(repo, "cat-file", "-e",
                         f"{MIGRATION_COMMIT}:research/_registry/MIGRATION_LEDGER.tsv", check=False)
    if self_reference.returncode == 0:
        raise GateError("LEDGER", "self reference")
    by_old = {row["old_current_path"]: row for row in working}
    if set(by_old) != {row["current_path"] for row in batch}:
        raise GateError("LEDGER", "coverage")
    for item in batch:
        row = by_old[item["current_path"]]
        expected = {
            "phase": "R1F", "batch_id": item["batch_id"], "new_current_path": item["destination"],
            "rename_score": "R100", "git_blob_oid_before": item["git_blob_oid"],
            "git_blob_oid_after": item["git_blob_oid"], "sha256_before": item["sha256"],
            "sha256_after": item["sha256"], "commit": MIGRATION_COMMIT,
            "rollback_parent": ROLLBACK_PARENT,
        }
        if any(row[key] != value for key, value in expected.items()):
            raise GateError("LEDGER", item["current_path"])


def validate_links(repo: Path, injected_missing: bool = False) -> int:
    sources = [repo / path for path in sorted(AUTHORIZED)]
    sources += sorted((repo / "research").rglob("*.md"))
    sources += sorted((repo / "reorganization_r1f").rglob("*.md"))
    sources += sorted((repo / "reorganization_r1f_checkpoint").rglob("*.md"))
    pattern = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
    count = 0
    targets = []
    for source in dict.fromkeys(sources):
        for raw in pattern.findall(source.read_text(encoding="utf-8")):
            target = raw.strip().strip("<>")
            if target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            target = unquote(target.split("#", 1)[0])
            targets.append(source.parent.joinpath(target).resolve())
            count += 1
    if injected_missing:
        targets.append(repo / "missing-catchproof-target")
    missing = [path for path in targets if not path.exists()]
    if missing:
        raise GateError("BROKEN_LINK", str(missing[0]))
    return count


def validate_manifests(repo: Path, corrupt: bool = False) -> list[dict[str, object]]:
    base_paths = set(str(git(repo, "ls-tree", "-r", "--name-only", SOURCE)).splitlines())
    current_paths = set(str(git(repo, "ls-files")).splitlines())
    index_oids = {line.split(None, 3)[3]: line.split()[1]
                  for line in str(git(repo, "ls-files", "-s")).splitlines()}
    records = []
    for index, (package, expected_digest) in enumerate(PACKAGES.items()):
        digest = expected_digest if not (corrupt and index == 0) else "0" * 64
        manifest = repo / package / "SHA256SUMS.txt"
        if sha(manifest.read_bytes()) != digest:
            raise GateError("MANIFEST", package)
        replay = run(repo / package, ["sha256sum", "--check", "SHA256SUMS.txt"])
        base = sorted(path for path in base_paths if path.startswith(package + "/"))
        current = sorted(path for path in current_paths if path.startswith(package + "/"))
        if not base or base != current:
            raise GateError("MANIFEST", f"{package}:path state")
        for path in base:
            if index_oids[path] != str(git(repo, "rev-parse", f"{SOURCE}:{path}")).strip():
                raise GateError("MANIFEST", path)
        records.append({"package": package, "manifest_sha256": expected_digest,
                        "manifest_entries_passed": len(replay.stdout.splitlines()),
                        "tracked_paths_byte_identical_to_source": len(base), "result": "PASS"})
    return records


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
        kind = ("regular_file" if stat.S_ISREG(info.st_mode) else
                "directory" if stat.S_ISDIR(info.st_mode) else
                "symlink" if stat.S_ISLNK(info.st_mode) else "other")
        result[path] = (code, info.st_size, kind)
    return result


def validate_dirty(repo: Path, dirty_checkout: Path, corrupt: bool = False) -> int:
    recorded = {row["path"]: row for row in rows(
        repo / "reorganization_r1b/postmove_forensic_census/DIRTY_WORKSTATION_INVENTORY.tsv")}
    observed = dirty_metadata(dirty_checkout)
    if corrupt:
        observed = dict(observed); observed.pop(next(iter(observed)))
    if len(recorded) != 54 or len(observed) != 54 or set(recorded) != set(observed):
        raise GateError("DIRTY_METADATA", f"{len(recorded)}/{len(observed)}")
    for path, value in observed.items():
        row = recorded[path]
        expected = (row["status"], int(row["size_bytes_lstat"]), row["object_type"])
        if value != expected or row["content_sha256"] != "NOT_READ":
            raise GateError("DIRTY_METADATA", path)
    return len(observed)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--dirty-checkout", type=Path, required=True)
    parser.add_argument("--test-result", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(); repo = args.repo.resolve()

    observed, merge_base, ahead = validate_remote(repo)
    changed = validate_scope(repo)
    validate_navigation(repo)
    batch = rows(repo / "reorganization_r1f/PREREGISTERED_BATCH.tsv")
    current = rows(repo / "research/_registry/CURRENT_ARTIFACT_PATHS.tsv")
    counts = validate_current(repo, current)
    renames = validate_renames(repo, batch)
    pre = rows(repo / "reorganization_r1f/pre_move/BEHAVIOR_RUNS.tsv")
    post = rows(repo / "reorganization_r1f/post_move/BEHAVIOR_RUNS.tsv")
    validate_recorded_behavior(pre, post)
    replay = replay_behavior(repo, batch, repo / "reorganization_r1f_checkpoint/behavioral_replay")
    ledger = rows(repo / "research/_registry/MIGRATION_LEDGER.tsv")
    validate_ledger(repo, ledger, batch)
    links = validate_links(repo)
    frontier = rows(repo / "research/_registry/CURRENT_FRONTIER_TARGETS.tsv")
    frontier_targets = {row["target_path"].rstrip("/") for row in frontier}
    if len(frontier) != 306 or len(frontier_targets) != 101 or not all(
            (repo / target).exists() for target in frontier_targets):
        raise GateError("FRONTIER", f"{len(frontier)}/{len(frontier_targets)}")
    manifests = validate_manifests(repo)
    dirty_count = validate_dirty(repo, args.dirty_checkout.resolve())
    test = json.loads(args.test_result.read_text(encoding="utf-8"))
    if (test.get("passed"), test.get("failed"), test.get("xfailed"), test.get("baseline_match")) != (69, 1, 1, True):
        raise GateError("TEST_BASELINE", str(test))

    bad_current = copy.deepcopy(current); bad_current.pop()
    bad_rename = set(renames); bad_rename.pop()
    catchproof = {
        "unexpected_origin_grok_rejected": catch("REMOTE_GUARD", lambda: validate_remote(repo, "0" * 40)),
        "unauthorized_edit_rejected": catch("UNAUTHORIZED_EDIT", lambda: validate_scope(repo, "CANON.md")),
        "current_map_mismatch_rejected": catch("CURRENT_MAP", lambda: validate_current(repo, bad_current)),
        "behavior_hash_mismatch_rejected": catch("BEHAVIOR_HASH", lambda: validate_recorded_behavior(pre, post, True)),
        "non_r100_move_rejected": catch("R100_IDENTITY", lambda: validate_renames(repo, batch, bad_rename)),
        "invalid_ledger_parent_rejected": catch("LEDGER", lambda: validate_ledger(repo, ledger, batch, True)),
        "broken_link_rejected": catch("BROKEN_LINK", lambda: validate_links(repo, True)),
        "manifest_mutation_rejected": catch("MANIFEST", lambda: validate_manifests(repo, True)),
        "dirty_metadata_drift_rejected": catch("DIRTY_METADATA", lambda: validate_dirty(repo, args.dirty_checkout.resolve(), True)),
    }

    result = {
        "result": "PASS", "mode": "R1F_CHECKPOINT_FAIL_CLOSED_VERIFY", "source_tip": SOURCE,
        "origin_grok_preintegration": observed, "merge_base": merge_base,
        "source_commits_ahead": ahead, "authorized_existing_files_changed": sorted(AUTHORIZED),
        "all_changed_paths": changed, "current_map": {"rows": 1114,
            "unique_original_paths": 1114, "unique_current_paths": 1114,
            "status_counts": dict(counts)}, "r100_renames": renames,
        "identical_r100_count": len(renames), "behavioral_record_pairs_verified": 4,
        "behavioral_replays_verified": replay, "migration_ledger_rows": len(ledger),
        "migration_commit": MIGRATION_COMMIT, "rollback_parent": ROLLBACK_PARENT,
        "ledger_self_reference": False, "markdown_links_verified": links,
        "frontier_rows": len(frontier), "frontier_unique_targets": len(frontier_targets),
        "frozen_manifest_replays": manifests, "test_baseline": test,
        "dirty_checkout_metadata_rows": dirty_count, "dirty_content_policy": "NOT_READ",
        "catchproof": catchproof, "b02_b03_authorized": False,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
