#!/usr/bin/env python3
"""Independent fail-closed verifier for the R1E batch plan."""

from __future__ import annotations

import argparse
import copy
import csv
import hashlib
import json
import re
import stat
import subprocess
from collections import Counter, defaultdict
from pathlib import Path
from urllib.parse import unquote


BASE = "b59005dba9acaf6c575185876655bd6a5c792094"
PREREG_COMMIT = "2755abb"
EXPECTED_CANDIDATE_SHA = "7fc413f8046de195f56424b12fa6607fed690dbd0a72064f5118e9c958f47141"
ALLOWED_DISPOSITIONS = {
    "SAFE_BYTE_IDENTICAL", "SAFE_WITH_PATH_POINTER_CHANGES",
    "BLOCKED_IMMUTABLE_COMPANION", "BLOCKED_RUNTIME_OR_MISSING_INPUT",
    "BLOCKED_TEST_SCOPE", "BLOCKED_FRONTIER_OR_CONTROL", "NEEDS_MANUAL_ADJUDICATION",
}
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


def run(repo: Path, command: list[str], binary: bool = False) -> str | bytes:
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


def expect_code(code: str, callback) -> str:
    try:
        callback()
    except GateError as exc:
        if exc.code == code:
            return "PASS"
        raise AssertionError(f"expected {code}, got {exc.code}: {exc}") from exc
    raise AssertionError(f"catch-proof corruption accepted; expected {code}")


def unique_rows(rows: list[dict[str, str]], key: str, expected: set[str]) -> dict[str, dict[str, str]]:
    values = [row[key] for row in rows]
    duplicates = sorted(value for value, count in Counter(values).items() if count > 1)
    if duplicates:
        raise GateError("DUPLICATE_CANDIDATE", ";".join(duplicates))
    actual = set(values)
    missing = sorted(expected - actual)
    extra = sorted(actual - expected)
    if missing:
        raise GateError("MISSING_CANDIDATE", ";".join(missing))
    if extra:
        raise GateError("EXTRA_CANDIDATE", ";".join(extra))
    return {row[key]: row for row in rows}


def validate_ledger(repo: Path, candidates: list[dict[str, str]], ledger: list[dict[str, str]]) -> dict[str, dict[str, str]]:
    expected = {row["current_path"] for row in candidates}
    by_path = unique_rows(ledger, "candidate_path", expected)
    candidate_by_path = {row["current_path"]: row for row in candidates}
    destinations: set[str] = set()
    for path, row in by_path.items():
        candidate = candidate_by_path[path]
        if row["disposition"] not in ALLOWED_DISPOSITIONS:
            raise GateError("BAD_DISPOSITION", path)
        for column in ("original_path", "destination", "primary_owner", "artifact_type", "git_blob_oid", "sha256"):
            source_column = "recommended_destination" if column == "destination" else (
                "fixed_base_blob_oid" if column == "git_blob_oid" else
                "fixed_base_sha256" if column == "sha256" else column
            )
            if row[column] != candidate[source_column]:
                raise GateError("CANDIDATE_METADATA_DRIFT", f"{path}:{column}")
        destination = row["destination"]
        if destination in destinations:
            raise GateError("DESTINATION_COLLISION", destination)
        destinations.add(destination)
        if (repo / destination).exists():
            raise GateError("DESTINATION_COLLISION", destination)
        artifact = repo / path
        if not artifact.is_file():
            raise GateError("MISSING_CANDIDATE", path)
        if sha(artifact.read_bytes()) != row["sha256"]:
            raise GateError("CANDIDATE_BYTE_DRIFT", path)
        oid = str(run(repo, ["git", "hash-object", "--no-filters", path])).strip()
        if oid != row["git_blob_oid"]:
            raise GateError("CANDIDATE_BLOB_DRIFT", path)
    return by_path


def validate_graph(graph: dict, ledger: dict[str, dict[str, str]]) -> dict[str, set[str]]:
    if graph.get("candidate_count") != 119 or graph.get("candidate_universe_sha256") != EXPECTED_CANDIDATE_SHA:
        raise GateError("GRAPH_UNIVERSE_DRIFT")
    graph_candidates = [node["id"] for node in graph["nodes"] if node["kind"] == "candidate"]
    if len(graph_candidates) != len(set(graph_candidates)) or set(graph_candidates) != set(ledger):
        raise GateError("GRAPH_CANDIDATE_COVERAGE")
    families: dict[str, set[str]] = {}
    seen: set[str] = set()
    for family in graph["families"]:
        members = set(family["candidate_members"])
        if not members or seen & members:
            raise GateError("DUPLICATE_FAMILY_MEMBER")
        seen |= members
        families[family["family_id"]] = members
        for path in members:
            if ledger[path]["atomic_family_id"] != family["family_id"]:
                raise GateError("FAMILY_LEDGER_MISMATCH", path)
    if seen != set(ledger):
        raise GateError("GRAPH_CANDIDATE_COVERAGE")
    for edge in graph["edges"]:
        if edge.get("required_for_migration") is not True:
            continue
        source, target = edge["source"], edge["target"]
        if source in ledger and target in ledger:
            if ledger[source]["atomic_family_id"] != ledger[target]["atomic_family_id"]:
                raise GateError("SPLIT_GRAPH_FAMILY", f"{source}->{target}")
    return families


def validate_batch_rows(repo: Path, rows: list[dict[str, str]], ledger: dict[str, dict[str, str]],
                        families: dict[str, set[str]], require_declared: bool = True) -> None:
    if not rows:
        raise GateError("EMPTY_BATCH_PLAN")
    seen: set[str] = set()
    destinations: set[str] = set()
    grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        path = row["current_path"]
        if path in seen:
            raise GateError("DUPLICATE_BATCH_MEMBER", path)
        seen.add(path)
        if path not in ledger:
            raise GateError("UNKNOWN_BATCH_MEMBER", path)
        grouped[row["batch_id"]].append(row)
    for batch_id, batch in grouped.items():
        paths = {row["current_path"] for row in batch}
        for path in paths:
            family_id = ledger[path]["atomic_family_id"]
            if not families[family_id].issubset(paths):
                raise GateError("SPLIT_DEPENDENCY_COMPONENT", f"{batch_id}:{family_id}")
        lanes = {ledger[path]["lane_class"] for path in paths}
        if len(lanes) != 1:
            raise GateError("ACTIVE_LEGACY_MIX", batch_id)
        for row in batch:
            path = row["current_path"]
            item = ledger[path]
            if item["required_companions"] != "NONE" or item["frozen_companions"] != "NONE":
                raise GateError("IMMUTABLE_COMPANION", path)
            if item["unresolved_runtime_paths"] != "NONE" or item["runtime_paths"] != "NONE" or item["generated_outputs"] != "NONE":
                raise GateError("UNRESOLVED_RUNTIME_PATH", path)
            if item["test_scope"] != "NONE":
                raise GateError("BLOCKED_TEST_SCOPE", path)
            if item["frontier_or_control"] != "NONE":
                raise GateError("FRONTIER_OR_CONTROL", path)
            if not item["disposition"].startswith("SAFE_"):
                raise GateError("UNSAFE_DISPOSITION", path)
            destination = row["destination"]
            if destination != item["destination"] or destination in destinations or (repo / destination).exists():
                raise GateError("DESTINATION_COLLISION", destination)
            destinations.add(destination)
            pointer = row["exact_future_pointer_plan"]
            if "CURRENT_ARTIFACT_PATHS.tsv" not in pointer or "MIGRATION_LEDGER.tsv" not in pointer:
                raise GateError("STALE_CURRENT_POINTER", path)
            if row["artifact_content_edit"] != "NONE_BYTE_IDENTICAL_GIT_MV_ONLY":
                raise GateError("SCIENTIFIC_BYTE_EDIT", path)
            if require_declared and item["proposed_batch_id"] != batch_id:
                raise GateError("BATCH_DECLARATION_MISMATCH", path)


def validate_links(repo: Path) -> int:
    sources = [repo / "README.md"]
    sources += sorted((repo / "research").rglob("*.md"))
    sources += sorted((repo / "reorganization_r1e").rglob("*.md"))
    pattern = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
    count = 0
    for source in sources:
        for raw in pattern.findall(source.read_text(encoding="utf-8")):
            target = raw.strip().strip("<>")
            if target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            target = unquote(target.split("#", 1)[0])
            if not source.parent.joinpath(target).resolve().exists():
                raise GateError("BROKEN_MARKDOWN_LINK", f"{source}:{raw}")
            count += 1
    return count


def dirty_metadata(checkout: Path) -> dict[str, tuple[str, int, str]]:
    raw = bytes(run(checkout, ["git", "status", "--porcelain=v2", "-z", "--untracked-files=all"], binary=True))
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
    args = parser.parse_args()
    repo = args.repo.resolve()
    r1e = repo / "reorganization_r1e"

    if str(run(repo, ["git", "rev-parse", BASE])).strip() != BASE:
        raise AssertionError("base is unavailable")
    candidates = load_tsv(r1e / "PREREGISTERED_CANDIDATE_UNIVERSE.tsv")
    if len(candidates) != 119 or sha((r1e / "PREREGISTERED_CANDIDATE_UNIVERSE.tsv").read_bytes()) != EXPECTED_CANDIDATE_SHA:
        raise AssertionError("preregistered candidate universe drift")
    last_candidate_commit = str(run(repo, ["git", "log", "-1", "--format=%h", "--", "reorganization_r1e/PREREGISTERED_CANDIDATE_UNIVERSE.tsv"])).strip()
    if last_candidate_commit != PREREG_COMMIT:
        raise AssertionError(f"candidate freeze was altered after preregistration: {last_candidate_commit}")

    ledger_rows = load_tsv(r1e / "COMPLETE_CANDIDATE_LEDGER.tsv")
    ledger = validate_ledger(repo, candidates, ledger_rows)
    graph = json.loads((r1e / "ATOMIC_FAMILY_GRAPH.json").read_text())
    families = validate_graph(graph, ledger)
    plan_rows = load_tsv(r1e / "PROPOSED_BATCH_FILE_PLAN.tsv")
    validate_batch_rows(repo, plan_rows, ledger, families)
    ranking = load_tsv(r1e / "BATCH_RANKING.tsv")
    if [row["rank"] for row in ranking] != ["1", "2", "3"] or {row["status"] for row in ranking} != {"PROPOSED_NOT_AUTHORIZED"}:
        raise AssertionError("ranking is not plan-only")
    if Counter(row["disposition"] for row in ledger_rows) != Counter({
        "SAFE_BYTE_IDENTICAL": 36, "BLOCKED_IMMUTABLE_COMPANION": 37,
        "BLOCKED_RUNTIME_OR_MISSING_INPUT": 42, "BLOCKED_TEST_SCOPE": 1,
        "NEEDS_MANUAL_ADJUDICATION": 3,
    }):
        raise AssertionError("disposition totals drift")

    # No generated R1E record may retroactively influence the frozen universe.
    prereg = json.loads((r1e / "PREREGISTERED_INPUTS.json").read_text())
    if prereg["candidate_rows"] != 119 or prereg["candidate_tsv_sha256"] != EXPECTED_CANDIDATE_SHA:
        raise AssertionError("preregistration inputs drift")

    # No research artifact or pre-existing path may change in a plan-only phase.
    diff = str(run(repo, ["git", "diff", "--name-status", BASE])).splitlines()
    for line in diff:
        status, path = line.split("\t", 1)
        if status != "A" or not path.startswith("reorganization_r1e/"):
            raise AssertionError(f"unauthorized plan-only diff: {line}")

    current_map = load_tsv(repo / "research/_registry/CURRENT_ARTIFACT_PATHS.tsv")
    if len(current_map) != 1114 or len({row["original_path"] for row in current_map}) != 1114 or len({row["current_path"] for row in current_map}) != 1114:
        raise AssertionError("current-path registry drift")
    if not all((repo / row["current_path"]).exists() for row in current_map):
        raise AssertionError("current-path registry contains a missing target")
    if Counter(row["path_status"] for row in current_map) != Counter({"ROOT_RETAINED": 1113, "MIGRATED_R1D": 1}):
        raise AssertionError("current-path statuses drift")

    frontier = load_tsv(repo / "research/_registry/CURRENT_FRONTIER_TARGETS.tsv")
    frontier_targets = {row["target_path"].rstrip("/") for row in frontier}
    if len(frontier) != 306 or len(frontier_targets) != 101 or not all((repo / target).exists() for target in frontier_targets):
        raise AssertionError("frontier target verification failed")
    links = validate_links(repo)

    base_tracked = set(str(run(repo, ["git", "ls-tree", "-r", "--name-only", BASE])).splitlines())
    current_tracked = set(str(run(repo, ["git", "ls-files"])).splitlines())
    index_oids = {line.split(None, 3)[3]: line.split()[1]
                  for line in str(run(repo, ["git", "ls-files", "-s"])).splitlines()}
    manifest_results = []
    for package, digest in PACKAGES.items():
        manifest = repo / package / "SHA256SUMS.txt"
        if sha(manifest.read_bytes()) != digest:
            raise AssertionError(f"manifest hash drift: {package}")
        replay = subprocess.run(["sha256sum", "--check", "SHA256SUMS.txt"], cwd=repo / package,
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=False)
        if replay.returncode:
            raise AssertionError(replay.stdout + replay.stderr)
        base_paths = sorted(path for path in base_tracked if path.startswith(package + "/"))
        current_paths = sorted(path for path in current_tracked if path.startswith(package + "/"))
        if not base_paths or current_paths != base_paths:
            raise AssertionError(f"frozen package path drift: {package}")
        for path in base_paths:
            base_oid = str(run(repo, ["git", "rev-parse", f"{BASE}:{path}"])).strip()
            if index_oids[path] != base_oid:
                raise AssertionError(f"frozen package byte drift: {path}")
        manifest_results.append({"package": package, "manifest_sha256": digest,
                                 "tracked_paths_byte_identical_to_base": len(base_paths), "result": "PASS"})

    recorded = {row["path"]: row for row in load_tsv(repo / "reorganization_r1b/postmove_forensic_census/DIRTY_WORKSTATION_INVENTORY.tsv")}
    current_dirty = dirty_metadata(args.dirty_checkout.resolve())
    if len(recorded) != len(current_dirty) or len(recorded) != 54 or set(recorded) != set(current_dirty):
        raise AssertionError("dirty checkout path metadata drift")
    for path, value in current_dirty.items():
        row = recorded[path]
        if (row["status"], int(row["size_bytes_lstat"]), row["object_type"], row["content_sha256"]) != (*value, "NOT_READ"):
            raise AssertionError(f"dirty checkout metadata drift: {path}")

    test = json.loads(args.test_result.read_text())
    if not test.get("baseline_match") or (test["passed"], test["failed"], test["xfailed"]) != (69, 1, 1):
        raise AssertionError("test baseline drift")

    # Catch proofs use in-memory corruptions only.
    missing_ledger = copy.deepcopy(ledger_rows[:-1])
    duplicate_ledger = copy.deepcopy(ledger_rows) + [copy.deepcopy(ledger_rows[0])]
    bv11 = next(row for row in ledger_rows if row["atomic_family_id"] == "F_BV11_RUNTIME")
    split_row = {
        "batch_id": "BAD_SPLIT", "current_path": bv11["candidate_path"], "destination": bv11["destination"],
        "artifact_content_edit": "NONE_BYTE_IDENTICAL_GIT_MV_ONLY",
        "exact_future_pointer_plan": "CURRENT_ARTIFACT_PATHS.tsv;MIGRATION_LEDGER.tsv",
    }
    immutable_item = next(row for row in ledger_rows if row["candidate_path"] == "simple_metric_dotted_line.py")
    immutable_row = {**split_row, "batch_id": "BAD_IMMUTABLE", "current_path": immutable_item["candidate_path"], "destination": immutable_item["destination"]}
    runtime_item = next(row for row in ledger_rows if row["candidate_path"] == "verify_sne_adversarial.py")
    runtime_row = {**split_row, "batch_id": "BAD_RUNTIME", "current_path": runtime_item["candidate_path"], "destination": runtime_item["destination"]}
    collision_rows = copy.deepcopy(plan_rows)
    collision_rows[0]["destination"] = "README.md"
    stale_rows = copy.deepcopy(plan_rows)
    stale_rows[0]["exact_future_pointer_plan"] = "MIGRATION_LEDGER.tsv append"
    active = copy.deepcopy(next(row for row in plan_rows if row["lane_class"] == "ACTIVE"))
    legacy = copy.deepcopy(next(row for row in plan_rows if row["lane_class"] == "LEGACY"))
    active["batch_id"] = legacy["batch_id"] = "BAD_MIXED"

    catchproof = {
        "missing_candidate_rejected": expect_code("MISSING_CANDIDATE", lambda: validate_ledger(repo, candidates, missing_ledger)),
        "duplicate_candidate_rejected": expect_code("DUPLICATE_CANDIDATE", lambda: validate_ledger(repo, candidates, duplicate_ledger)),
        "split_dependency_component_rejected": expect_code("SPLIT_DEPENDENCY_COMPONENT", lambda: validate_batch_rows(repo, [split_row], ledger, families, False)),
        "immutable_companion_rejected": expect_code("IMMUTABLE_COMPANION", lambda: validate_batch_rows(repo, [immutable_row], ledger, families, False)),
        "destination_collision_rejected": expect_code("DESTINATION_COLLISION", lambda: validate_batch_rows(repo, collision_rows, ledger, families)),
        "unresolved_runtime_path_rejected": expect_code("UNRESOLVED_RUNTIME_PATH", lambda: validate_batch_rows(repo, [runtime_row], ledger, families, False)),
        "stale_current_pointer_rejected": expect_code("STALE_CURRENT_POINTER", lambda: validate_batch_rows(repo, stale_rows, ledger, families)),
        "active_legacy_mixed_batch_rejected": expect_code("ACTIVE_LEGACY_MIX", lambda: validate_batch_rows(repo, [active, legacy], ledger, families, False)),
    }

    result = {
        "result": "PASS", "mode": "R1E_BATCH_PLAN_EXTERNAL_FAIL_CLOSED_VERIFY", "base": BASE,
        "candidate_universe": {"rows": 119, "sha256": EXPECTED_CANDIDATE_SHA,
                               "last_modified_commit": PREREG_COMMIT},
        "candidate_ledger_rows": len(ledger_rows), "atomic_families": len(families),
        "disposition_counts": dict(sorted(Counter(row["disposition"] for row in ledger_rows).items())),
        "proposed_batches": {row["batch_id"]: int(row["file_count"]) for row in ranking},
        "plan_only_diff_paths": len(diff), "research_artifact_moves_or_edits": 0,
        "current_artifact_paths": {"rows": 1114, "unique_current_paths": 1114},
        "markdown_links_verified": links, "frontier_rows": 306, "frontier_unique_targets": 101,
        "frozen_manifest_replays": manifest_results,
        "dirty_workstation_rows_metadata_only": 54, "dirty_content_policy": "NOT_READ",
        "test_baseline": test, "catchproof": catchproof,
        "migration_authorized": False,
    }
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
