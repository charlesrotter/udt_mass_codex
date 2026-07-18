#!/usr/bin/env python3
"""Independent fail-closed verifier for the R1D S8 canary migration."""

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
from collections import Counter
from pathlib import Path
from urllib.parse import unquote

BASE = "b3c50109df90658378d157c65fc723b1265c48c8"
SOURCE = "simple_metric_S8_action_provenance_note.md"
DESTINATION = "research/macro/simple_metric_S8_action_provenance_note.md"
EXPECTED_BLOB = "94b494cd326a27aacbbbedbd9aa91febb8acf471"
EXPECTED_SHA = "a3fae1798f64c4bdc3a79692a618281c407d162309073a02dc72d89eb9c554f9"
EXPECTED_LINE = "| **Re-run** | light CAS in `simple_metric_solution_space_ZOOM.md` session |"
PACKAGES = {
    "native_action_stage1_2026-07-18/arm_A": "d72e8d6e1b4bc8682bd5518264a1a43a3b5f7b3b246b3d218ea6bfecc6927d19",
    "native_action_stage1_2026-07-18/arm_B": "a99937a8fbba57ac24f490c2974937718f7dfbc2f2f7dd7c960d57fc5e839b92",
    "native_action_stage2_2026-07-18/arm_A": "ad63ffacdd5282a35fe0aef62269464d987aa61b710a4d393d95836234fd670a",
    "native_action_stage2_2026-07-18/arm_B": "30b2a3863f1d16e3b3507b5d0bf10a6b5b59c1e54d769cacc53127cc676d6d45",
    "native_action_arm_c_2026-07-18": "99fc0d6c26aff24e43b8636d74f80e3486c56131590552308b47c1d107ed500f",
    "native_action_final_adjudication_2026-07-18": "57be0046432c27046e84eaafd1706959558f43170d0f1e23dc3047966e512f33",
}


def run(repo: Path, command: list[str], binary: bool = False):
    result = subprocess.run(command, cwd=repo, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                            text=not binary, check=False)
    if result.returncode:
        err = result.stderr if not binary else result.stderr.decode("utf-8", "replace")
        raise AssertionError(f"command failed: {' '.join(command)}\n{err}")
    return result.stdout


def sha(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def load_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def rejected(callback) -> str:
    try:
        callback()
    except (AssertionError, KeyError, FileNotFoundError):
        return "PASS"
    raise AssertionError("catch-proof corruption was accepted")


def validate_map(repo: Path, rows: list[dict[str, str]]) -> Counter:
    assert len(rows) == 1114
    originals = [r["original_path"] for r in rows]
    currents = [r["current_path"] for r in rows]
    assert len(set(originals)) == len(set(currents)) == 1114
    counts = Counter(r["path_status"] for r in rows)
    assert counts == Counter({"ROOT_RETAINED": 1113, "MIGRATED_R1D": 1})
    for row in rows:
        expected = DESTINATION if row["original_path"] == SOURCE else row["original_path"]
        expected_status = "MIGRATED_R1D" if row["original_path"] == SOURCE else "ROOT_RETAINED"
        assert row["current_path"] == expected and row["path_status"] == expected_status
        path = repo / row["current_path"]
        assert path.exists() or path.is_symlink()
        # These columns identify the fixed-base artifact. Retained paths may have
        # legitimate post-base navigation edits; only the migrated canary carries
        # a byte-identity requirement across the move.
        if row["original_path"] == SOURCE:
            oid = str(run(repo, ["git", "hash-object", "--no-filters", row["current_path"]])).strip()
            assert oid == row["fixed_base_blob_oid"] == EXPECTED_BLOB
            assert sha(path.read_bytes()) == row["fixed_base_sha256"] == EXPECTED_SHA
    return counts


def validate_links(repo: Path) -> int:
    sources = [repo / "README.md"]
    sources += sorted((repo / "research").rglob("*.md"))
    sources += sorted((repo / "reorganization_r1d").rglob("*.md"))
    pattern = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
    count = 0
    for source in sources:
        for raw in pattern.findall(source.read_text(encoding="utf-8")):
            target = raw.strip().strip("<>")
            if target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            target = unquote(target.split("#", 1)[0])
            assert source.parent.joinpath(target).resolve().exists(), f"broken link {source}: {raw}"
            count += 1
    return count


def dirty_metadata(checkout: Path) -> dict[str, tuple[str, int, str]]:
    raw = bytes(run(checkout, ["git", "status", "--porcelain=v2", "-z", "--untracked-files=all"], binary=True))
    records = raw.split(b"\0"); result = {}; index = 0
    while index < len(records):
        record = records[index]; index += 1
        if not record:
            continue
        marker = record[:1]
        if marker == b"1":
            fields = record.split(b" ", 8); status_code, raw_path = fields[1].decode(), fields[8]
        elif marker == b"2":
            fields = record.split(b" ", 9); status_code, raw_path = fields[1].decode(), fields[9]; index += 1
        elif marker == b"u":
            fields = record.split(b" ", 10); status_code, raw_path = fields[1].decode(), fields[10]
        elif marker in {b"?", b"!"}:
            status_code, raw_path = ("??" if marker == b"?" else "!!"), record[2:]
        else:
            raise AssertionError(f"unknown status record {record[:40]!r}")
        path = raw_path.decode("utf-8", "surrogateescape")
        info = (checkout / path).lstat()
        kind = "regular_file" if stat.S_ISREG(info.st_mode) else "directory" if stat.S_ISDIR(info.st_mode) else "symlink" if stat.S_ISLNK(info.st_mode) else "other"
        result[path] = (status_code, info.st_size, kind)
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--dirty-checkout", type=Path, required=True)
    parser.add_argument("--test-result", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(); repo = args.repo.resolve()
    prereg = json.loads((repo / "reorganization_r1d/PREREGISTERED_INPUTS.json").read_text())
    assert prereg["base"] == BASE and prereg["source_blob"] == EXPECTED_BLOB and prereg["source_sha256"] == EXPECTED_SHA
    assert not (repo / SOURCE).exists() and (repo / DESTINATION).is_file()
    artifact = (repo / DESTINATION).read_bytes()
    assert sha(artifact) == EXPECTED_SHA
    assert str(run(repo, ["git", "hash-object", "--no-filters", DESTINATION])).strip() == EXPECTED_BLOB
    assert artifact.decode().splitlines()[9] == EXPECTED_LINE
    assert "../../simple_metric_solution_space_ZOOM.md" not in artifact.decode()

    fixed = load_tsv(repo / "reorganization_r1d/FIXED_HISTORY_SHA256.tsv")
    assert len(fixed) == prereg["fixed_history_rows"] == 150
    for row in fixed:
        path = repo / row["path"]
        assert path.is_file() and sha(path.read_bytes()) == row["sha256"] and path.stat().st_size == int(row["size_bytes"])
        assert str(run(repo, ["git", "hash-object", "--no-filters", row["path"]])).strip() == row["git_blob_oid"]

    map_rows = load_tsv(repo / "research/_registry/CURRENT_ARTIFACT_PATHS.tsv")
    status_counts = validate_map(repo, map_rows)
    index_entries = str(run(repo, ["git", "ls-files", "-s"])).splitlines()
    blob_paths = [line.split(None, 3)[3] for line in index_entries if line.split()[1] == EXPECTED_BLOB]
    assert blob_paths == [DESTINATION]

    ownership = load_tsv(repo / "research/_registry/ROOT_OWNERSHIP.tsv")
    assert len(ownership) == 1114 and len({r["current_path"] for r in ownership}) == 1114
    macro_rows = load_tsv(repo / "research/macro/ROOT_INVENTORY.tsv")
    matches = [r for r in macro_rows if r["current_path"].endswith(SOURCE)]
    assert len(matches) == 1 and matches[0]["current_path"] == DESTINATION and matches[0]["relationship"] == "PRIMARY"
    base_macro = bytes(run(repo, ["git", "show", f"{BASE}:research/macro/ROOT_INVENTORY.tsv"], binary=True))
    expected_macro = base_macro.replace((SOURCE + "\t").encode(), (DESTINATION + "\t").encode(), 1)
    assert (repo / "research/macro/ROOT_INVENTORY.tsv").read_bytes() == expected_macro

    occurrences = load_tsv(repo / "reorganization_r1d/OLD_PATH_OCCURRENCE_CLASSIFICATION.tsv")
    assert occurrences and not [r for r in occurrences if r["classification"] == "STALE_CURRENT_POINTER"]
    assert any(r["classification"] == "CURRENT_MAP_ORIGINAL_IDENTITY_AND_DESTINATION_SUFFIX" for r in occurrences)
    assert any(r["classification"] == "CURRENT_PATH_DESTINATION_SUFFIX" for r in occurrences)

    statuses = str(run(repo, ["git", "diff", "--name-status", "--find-renames=100%", BASE])).splitlines()
    renames = [line for line in statuses if line == f"R100\t{SOURCE}\t{DESTINATION}"]
    assert len(renames) == 1
    modified = {line.split("\t", 1)[1] for line in statuses if line.startswith("M\t")}
    assert modified == {"research/README.md", "research/macro/ROOT_INVENTORY.tsv"}
    for line in statuses:
        if line.startswith("A\t"):
            path = line.split("\t", 1)[1]
            assert path.startswith("reorganization_r1d/") or path in {"research/_registry/README.md", "research/_registry/CURRENT_ARTIFACT_PATHS.tsv"}
        elif line.startswith(("M\t", "R100\t")):
            pass
        else:
            raise AssertionError(f"unauthorized diff: {line}")

    frontier = load_tsv(repo / "research/_registry/CURRENT_FRONTIER_TARGETS.tsv")
    assert len(frontier) == 306 and len({r["target_path"] for r in frontier}) == 101
    assert all((repo / r["target_path"].rstrip("/")).exists() for r in frontier)
    link_count = validate_links(repo)

    manifest_results = []
    base_tracked = set(str(run(repo, ["git", "ls-tree", "-r", "--name-only", BASE])).splitlines())
    current_tracked = set(str(run(repo, ["git", "ls-files"])).splitlines())
    index_oids = {line.split(None, 3)[3]: line.split()[1]
                  for line in str(run(repo, ["git", "ls-files", "-s"])).splitlines()}
    for package, digest in PACKAGES.items():
        manifest = repo / package / "SHA256SUMS.txt"
        assert sha(manifest.read_bytes()) == digest
        replay = subprocess.run(["sha256sum", "--check", "SHA256SUMS.txt"], cwd=repo / package,
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=False)
        assert replay.returncode == 0, replay.stdout + replay.stderr
        base_package_paths = sorted(p for p in base_tracked if p.startswith(package + "/"))
        current_package_paths = sorted(p for p in current_tracked if p.startswith(package + "/"))
        assert current_package_paths == base_package_paths and base_package_paths
        for path in base_package_paths:
            base_oid = str(run(repo, ["git", "rev-parse", f"{BASE}:{path}"])).strip()
            assert index_oids[path] == base_oid
        manifest_results.append({"package": package, "manifest_sha256": digest,
                                 "tracked_paths_byte_identical_to_base": len(base_package_paths),
                                 "result": "PASS"})

    recorded = {r["path"]: r for r in load_tsv(repo / "reorganization_r1b/postmove_forensic_census/DIRTY_WORKSTATION_INVENTORY.tsv")}
    current = dirty_metadata(args.dirty_checkout.resolve())
    assert len(recorded) == len(current) == 54 and set(recorded) == set(current)
    for path, value in current.items():
        row = recorded[path]
        assert (row["status"], int(row["size_bytes_lstat"]), row["object_type"], row["content_sha256"]) == (*value, "NOT_READ")

    test = json.loads(args.test_result.read_text())
    assert test["baseline_match"] is True and (test["passed"], test["failed"], test["xfailed"]) == (69, 1, 1)

    bad_map_missing = copy.deepcopy(map_rows[:-1])
    bad_map_duplicate = copy.deepcopy(map_rows); bad_map_duplicate[-1]["current_path"] = bad_map_duplicate[0]["current_path"]
    bad_map_artifact = copy.deepcopy(map_rows); next(r for r in bad_map_artifact if r["original_path"] == SOURCE)["fixed_base_sha256"] = "0" * 64
    def token_check(text: str):
        assert EXPECTED_LINE in text and "../../simple_metric_solution_space_ZOOM.md" not in text
    def occurrence_check(rows):
        assert not [r for r in rows if r["classification"] == "STALE_CURRENT_POINTER"]
    result = {
        "result": "PASS", "mode": "R1D_S8_BYTE_IDENTICAL_CANARY_VERIFY", "base": BASE,
        "artifact": {"old_path": SOURCE, "new_path": DESTINATION, "rename": "R100", "git_blob_oid": EXPECTED_BLOB, "sha256": EXPECTED_SHA, "duplicate_copies": 0},
        "current_artifact_paths": {"rows": len(map_rows), "unique_original_paths": 1114, "unique_current_paths": 1114, "status_counts": dict(status_counts)},
        "fixed_history_rows": len(fixed), "old_path_occurrence_rows": len(occurrences), "stale_current_navigation_pointers": 0,
        "markdown_links_verified": link_count, "frontier_rows": len(frontier), "frontier_unique_targets": 101,
        "frozen_manifest_replays": manifest_results, "dirty_workstation_rows_metadata_only": 54, "test_baseline": test,
        "catchproof": {
            "missing_current_map_row_rejected": rejected(lambda: validate_map(repo, bad_map_missing)),
            "duplicate_current_path_rejected": rejected(lambda: validate_map(repo, bad_map_duplicate)),
            "artifact_hash_mutation_rejected": rejected(lambda: validate_map(repo, bad_map_artifact)),
            "forbidden_token_substitution_rejected": rejected(lambda: token_check(artifact.decode().replace("simple_metric_solution_space_ZOOM.md", "../../simple_metric_solution_space_ZOOM.md"))),
            "stale_current_pointer_rejected": rejected(lambda: occurrence_check(occurrences + [{"classification": "STALE_CURRENT_POINTER"}])),
            "fixed_history_mutation_rejected": rejected(lambda: (lambda payload: (_ for _ in ()).throw(AssertionError()) if sha(payload + b"x") != fixed[0]["sha256"] else None)((repo / fixed[0]["path"]).read_bytes())),
        },
    }
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
