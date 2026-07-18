#!/usr/bin/env python3
"""Independent fail-closed verifier for the R1C lane navigation overlay."""

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
from pathlib import Path
from typing import Any, Callable
from urllib.parse import unquote


OWNERS = {
    "CONTROL_ROOT", "FOUNDATIONS", "NATIVE_ACTION", "PARTICLE_MASS",
    "MACRO", "LEGACY_FROZEN", "CROSS_LANE_SHARED", "UNKNOWN_BLOCKED",
}
LANES = {"FOUNDATIONS", "NATIVE_ACTION", "PARTICLE_MASS", "MACRO"}
READINESS = {
    "RETAIN_ROOT", "IMMUTABLE_PATH", "MOVE_READY", "POINTER_MIGRATION_REQUIRED",
    "IMPORT_MIGRATION_REQUIRED", "MANIFEST_MIGRATION_REQUIRED", "BLOCKED",
}
PACKAGES = {
    "native_action_stage1_2026-07-18/arm_A": "d72e8d6e1b4bc8682bd5518264a1a43a3b5f7b3b246b3d218ea6bfecc6927d19",
    "native_action_stage1_2026-07-18/arm_B": "a99937a8fbba57ac24f490c2974937718f7dfbc2f2f7dd7c960d57fc5e839b92",
    "native_action_stage2_2026-07-18/arm_A": "ad63ffacdd5282a35fe0aef62269464d987aa61b710a4d393d95836234fd670a",
    "native_action_stage2_2026-07-18/arm_B": "30b2a3863f1d16e3b3507b5d0bf10a6b5b59c1e54d769cacc53127cc676d6d45",
    "native_action_arm_c_2026-07-18": "99fc0d6c26aff24e43b8636d74f80e3486c56131590552308b47c1d107ed500f",
    "native_action_final_adjudication_2026-07-18": "57be0046432c27046e84eaafd1706959558f43170d0f1e23dc3047966e512f33",
}
SOURCE_RANGES = {
    "LIVE.md": [(1, 103)],
    "HANDOFF.md": [(1, 65), (68, 135)],
    "INDEX.md": [(1, 110)],
    "MEMORY.md": [(1, 25)],
}
README_INSERTION = """
## Research lane index

Phase R1C adds an ownership and navigation-only [research lane index](research/README.md). It does not move or copy research artifacts and does not create a new physics authority.
"""
CORRECTION_BASE = "204f3637f134811f05df12aa7494ef41289ee3b4"
SELECTOR_AUDIT_PATHS = (
    "UDT_GR_TO_UDT_SELECTOR_AUDIT_2026-07-18.md",
    "UDT_GR_TO_UDT_SELECTOR_AUDIT_PREREG_2026-07-18.md",
)
CORRECTION_MODIFIED_PATHS = {
    "reorganization_r1c/R1C_AUDIT_REPORT.md",
    "reorganization_r1c/verify_r1c_overlay.py",
    "research/_registry/FIRST_ACTIVE_FAMILY_MIGRATION_RECOMMENDATION.md",
    "research/_registry/VERIFY_RESULT.json",
}


def run(repo: Path, command: list[str], *, binary: bool = False) -> str | bytes:
    completed = subprocess.run(
        command, cwd=repo, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        text=not binary, check=False,
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


def git_paths(repo: Path, revision: str, root_only: bool = False) -> list[str]:
    command = ["git", "ls-tree", "-r", "-z", "--name-only", revision]
    raw = str(run(repo, command)).split("\0")
    paths = [path for path in raw if path]
    return [path for path in paths if "/" not in path] if root_only else paths


def validate_tables(
    frozen: list[dict[str, str]],
    ownership: list[dict[str, str]],
    readiness: list[dict[str, str]],
) -> None:
    frozen_by_path = {row["path"]: row for row in frozen}
    own_paths = [row["current_path"] for row in ownership]
    ready_paths = [row["current_path"] for row in readiness]
    assert len(frozen_by_path) == len(frozen) == len(ownership) == len(readiness) == 1114
    assert len(own_paths) == len(set(own_paths)) and len(ready_paths) == len(set(ready_paths))
    assert set(own_paths) == set(ready_paths) == set(frozen_by_path)
    ready_by_path = {row["current_path"]: row for row in readiness}
    for row in ownership:
        base = frozen_by_path[row["current_path"]]
        assert row["primary_owner"] in OWNERS
        assert row["artifact_type"] == base["artifact_type"]
        assert row["first_commit_date"] == base["first_commit_date"]
        assert row["last_commit_date"] == base["last_commit_date"]
        assert row["physics_status_source"]
        assert row["frozen_manifest_status"]
        assert row["runtime_import_test_dependencies"]
        assert row["ownership_evidence"] and "FILENAME_ONLY" not in row["ownership_evidence"]
        secondaries = set() if row["secondary_consumers"] == "NONE" else set(row["secondary_consumers"].split(";"))
        assert secondaries <= LANES and row["primary_owner"] not in secondaries
        ready = ready_by_path[row["current_path"]]
        assert ready["primary_owner"] == row["primary_owner"]
        assert ready["migration_readiness"] in READINESS
        assert ready["blocking_or_change_requirement"]


def validate_lane_inventory(
    ownership: list[dict[str, str]], lane: str, rows: list[dict[str, str]]
) -> None:
    expected = {}
    for row in ownership:
        secondaries = set() if row["secondary_consumers"] == "NONE" else set(row["secondary_consumers"].split(";"))
        if row["primary_owner"] == lane or lane in secondaries:
            expected[row["current_path"]] = "PRIMARY" if row["primary_owner"] == lane else "SECONDARY_CONSUMER"
    paths = [row["current_path"] for row in rows]
    assert len(paths) == len(set(paths)) == len(expected)
    assert set(paths) == set(expected)
    for row in rows:
        assert row["relationship"] == expected[row["current_path"]]


def markdown_sources(repo: Path) -> dict[str, str]:
    sources = {"README.md": (repo / "README.md").read_text(encoding="utf-8")}
    for prefix in (repo / "research", repo / "reorganization_r1c"):
        for path in prefix.rglob("*.md"):
            sources[str(path.relative_to(repo))] = path.read_text(encoding="utf-8")
    return sources


def validate_links(repo: Path, sources: dict[str, str]) -> int:
    count = 0
    pattern = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
    for source, text in sources.items():
        for raw_target in pattern.findall(text):
            target = raw_target.strip().strip("<>")
            if target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            target = unquote(target.split("#", 1)[0])
            resolved = (repo / source).parent.joinpath(target).resolve()
            assert resolved.exists(), f"broken link: {source} -> {raw_target}"
            count += 1
    return count


def validate_readme(repo: Path, base: str, payload: bytes | None = None) -> None:
    base_payload = git_blob(repo, base, "README.md")
    needle = (
        b"Frozen evidence packages and their historical records are immutable. Any later\n"
        b"reorganization phase must preserve their bytes, manifests, and provenance.\n"
    )
    assert base_payload.count(needle) == 1
    expected = base_payload.replace(needle, needle + README_INSERTION.encode("utf-8"), 1)
    current = payload if payload is not None else (repo / "README.md").read_bytes()
    assert current == expected
    text = current.decode("utf-8")
    assert text.count("[research lane index](research/README.md)") == 1
    assert text.index("[`LIVE.md`](LIVE.md)") < text.index("[`HANDOFF.md`](HANDOFF.md)")
    assert text.index("[`HANDOFF.md`](HANDOFF.md)") < text.index("[`stability_branch_follow_256_DECISION.md`](stability_branch_follow_256_DECISION.md)")


def validate_diff(lines: list[str]) -> set[str]:
    additions = set()
    for line in lines:
        fields = line.split("\t")
        if fields[0] == "M":
            assert fields[1] == "README.md", line
        elif fields[0] == "A":
            assert fields[1].startswith(("research/", "reorganization_r1c/")), line
            additions.add(fields[1])
        else:
            raise AssertionError(f"move/delete/copy/unauthorized status: {line}")
    return additions


def validate_correction_diff(lines: list[str]) -> tuple[set[str], set[str]]:
    additions: set[str] = set()
    modifications: set[str] = set()
    for line in lines:
        fields = line.split("\t")
        if fields[0] == "M":
            assert fields[1] in CORRECTION_MODIFIED_PATHS, line
            modifications.add(fields[1])
        elif fields[0] == "A":
            path = fields[1]
            assert path.startswith("reorganization_r1c/correction/") or path == (
                "research/_registry/FIRST_ACTIVE_FAMILY_MIGRATION_RECOMMENDATION.json"
            ), line
            additions.add(path)
        else:
            raise AssertionError(f"correction move/delete/copy/unauthorized status: {line}")
    assert modifications <= CORRECTION_MODIFIED_PATHS
    assert {
        "reorganization_r1c/R1C_AUDIT_REPORT.md",
        "reorganization_r1c/verify_r1c_overlay.py",
        "research/_registry/FIRST_ACTIVE_FAMILY_MIGRATION_RECOMMENDATION.md",
    } <= modifications
    return additions, modifications


def reference_positions(text: str, token: str) -> list[int]:
    left_continuation = frozenset(
        "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_.-"
    )
    right_continuation = frozenset(
        "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_-"
    )
    found: list[int] = []
    offset = 0
    while True:
        offset = text.find(token, offset)
        if offset < 0:
            return found
        end = offset + len(token)
        left_ok = not offset or text[offset - 1] not in left_continuation
        right_ok = end == len(text)
        if not right_ok:
            following = text[end]
            if following not in right_continuation:
                right_ok = not (
                    following == "."
                    and end + 1 < len(text)
                    and text[end + 1] in right_continuation
                )
        if left_ok and right_ok:
            found.append(offset)
        offset = end


def validate_recommendation(
    repo: Path,
    payload: dict[str, Any],
    candidate_rows: list[dict[str, str]],
    audit_rows: list[dict[str, str]],
    mechanical: dict[str, Any],
    ownership: list[dict[str, str]],
    readiness: list[dict[str, str]],
    operational_dependencies: list[dict[str, str]],
    forensic_dependencies: list[dict[str, str]],
) -> dict[str, Any]:
    candidate_paths = [row["current_path"] for row in candidate_rows]
    assert len(candidate_paths) == len(set(candidate_paths)) == 13
    audit_paths = [row["current_path"] for row in audit_rows]
    assert len(audit_paths) == len(set(audit_paths)) == 13
    assert set(audit_paths) == set(candidate_paths)
    audit_by_path = {row["current_path"]: row for row in audit_rows}
    assert sorted(int(row["rank"]) for row in audit_rows) == list(range(1, 14))
    assert all(all(value for value in row.values()) for row in audit_rows)

    own_rows: dict[str, list[dict[str, str]]] = __import__("collections").defaultdict(list)
    ready_rows: dict[str, list[dict[str, str]]] = __import__("collections").defaultdict(list)
    for row in ownership:
        own_rows[row["current_path"]].append(row)
    for row in readiness:
        ready_rows[row["current_path"]].append(row)

    assert mechanical["result"] == "PASS" and mechanical["base"] == CORRECTION_BASE
    mechanical_rows = {row["current_path"]: row for row in mechanical["candidates"]}
    assert len(mechanical_rows) == mechanical["candidate_count"] == 13
    assert set(mechanical_rows) == set(candidate_paths)
    for path in candidate_paths:
        assert len(own_rows[path]) == len(ready_rows[path]) == 1
        own = own_rows[path][0]
        ready = ready_rows[path][0]
        audit = audit_by_path[path]
        mech = mechanical_rows[path]
        assert own["primary_owner"] in LANES
        assert ready["migration_readiness"] == "MOVE_READY"
        assert ready["recommended_destination_if_migrated"] != "-"
        assert audit["primary_owner"] == own["primary_owner"] == mech["primary_owner"]
        assert audit["destination"] == ready["recommended_destination_if_migrated"] == mech["destination"]
        assert audit["git_blob_oid"] == mech["git_blob_oid"]
        assert audit["sha256"] == mech["sha256"]
        assert (repo / path).is_file()
        assert (repo / path).read_bytes() == git_blob(repo, CORRECTION_BASE, path)

    ranking = payload["ranked_candidates"]
    assert len(ranking) == 13
    assert {
        (item["current_path"], int(item["rank"]), item["ruling"]) for item in ranking
    } == {
        (row["current_path"], int(row["rank"]), row["closure_ruling"]) for row in audit_rows
    }
    assert payload["candidate_count"] == 13
    assert payload["base"] == CORRECTION_BASE
    assert payload["research_artifact_moves_renames_copies_deletes"] == 0
    assert payload["decision"] in {
        "RECOMMEND_SINGLE_AUDITED_FAMILY", "NO_MIGRATION_AUTHORIZED_YET"
    }

    recommended = payload["recommended_files"]
    if payload["decision"] == "NO_MIGRATION_AUTHORIZED_YET":
        assert recommended == []
        return {"decision": payload["decision"], "recommended_files": 0}
    assert payload["decision"] == "RECOMMEND_SINGLE_AUDITED_FAMILY"
    assert len(recommended) >= 1
    for item in recommended:
        path = item["current_path"]
        assert path in candidate_paths
        assert len(ready_rows[path]) == len(own_rows[path]) == 1
        ready = ready_rows[path][0]
        own = own_rows[path][0]
        audit = audit_by_path[path]
        mech = mechanical_rows[path]
        assert ready["migration_readiness"] == item["migration_readiness"] == "MOVE_READY"
        assert ready["recommended_destination_if_migrated"] != "-"
        assert item["destination"] == ready["recommended_destination_if_migrated"]
        assert item["primary_owner"] == own["primary_owner"] in LANES
        assert own["frozen_manifest_status"] == item["frozen_manifest_status"] == "NOT_FROZEN_OR_MANIFEST"
        assert "FROZEN" not in ready["blocking_or_change_requirement"]
        assert "MANIFEST" not in ready["blocking_or_change_requirement"]
        assert audit["closure_ruling"] == item["closure_audit_ruling"] == "PASS_RECOMMENDED"
        assert int(audit["rank"]) == int(item["rank"])
        assert item["git_blob_oid"] == mech["git_blob_oid"]
        assert item["sha256"] == mech["sha256"]
        assert not mech["destination_collision"]
        assert mech["registered_unresolved_dynamic_touches"] == 0
        assert mech["operational_inbound_edges"] == []
        assert mech["frozen_package_inbound_sources"] == []
        assert not (repo / item["destination"]).exists()

        operational_inbound = [
            edge for edge in operational_dependencies
            if path in edge["resolved_target"].split("|") and edge["source"] != path
        ]
        frozen_inbound = [
            edge for edge in forensic_dependencies
            if path in edge["resolved_target"].split("|")
            and edge["source"].startswith((
                "native_action_stage1_2026-07-18/",
                "native_action_stage2_2026-07-18/",
                "native_action_arm_c_2026-07-18/",
                "native_action_final_adjudication_2026-07-18/",
            ))
        ]
        assert operational_inbound == [] and frozen_inbound == []

        substitutions = item["required_path_substitutions"]
        assert substitutions
        for substitution in substitutions:
            assert substitution["future_source"] == item["destination"]
            assert substitution["old_target"] in mech["file_like_tokens"]
            expected = os.path.relpath(
                repo / substitution["old_target"],
                (repo / item["destination"]).parent,
            )
            assert substitution["new_target"] == expected
            source_text = (repo / path).read_text(encoding="utf-8")
            positions = reference_positions(source_text, substitution["old_target"])
            assert len(positions) == 1
            assert source_text.count("\n", 0, positions[0]) + 1 == int(substitution["line_at_base"])

    prior = {row["current_path"]: row for row in payload["rejected_prior_recommendation"]}
    assert set(prior) == set(SELECTOR_AUDIT_PATHS)
    for path in SELECTOR_AUDIT_PATHS:
        assert len(ready_rows[path]) == 1
        ready = ready_rows[path][0]
        assert ready["migration_readiness"] == prior[path]["migration_readiness"] == "IMMUTABLE_PATH"
        assert ready["blocking_or_change_requirement"] == prior[path]["blocker"] == "R0_FROZEN_EVIDENCE"
        assert ready["recommended_destination_if_migrated"] == prior[path]["destination"] == "-"
    return {
        "decision": payload["decision"],
        "recommended_files": len(recommended),
        "recommended_paths": [item["current_path"] for item in recommended],
    }


def current_dirty_metadata(checkout: Path) -> dict[str, tuple[str, int, str]]:
    env = os.environ.copy()
    env["GIT_OPTIONAL_LOCKS"] = "0"
    raw = subprocess.check_output(
        ["git", "--no-optional-locks", "status", "--porcelain=v2", "-z", "--untracked-files=all"],
        cwd=checkout, env=env,
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
            fields = record.split(b" ", 8); status_code, raw_path = fields[1].decode(), fields[8]
        elif marker == b"2":
            fields = record.split(b" ", 9); status_code, raw_path = fields[1].decode(), fields[9]; index += 1
        elif marker == b"u":
            fields = record.split(b" ", 10); status_code, raw_path = fields[1].decode(), fields[10]
        elif marker in {b"?", b"!"}:
            status_code, raw_path = ("??" if marker == b"?" else "!!"), record[2:]
        else:
            raise AssertionError(f"unknown status record: {record[:80]!r}")
        path = raw_path.decode("utf-8", "surrogateescape")
        info = (checkout / path).lstat()
        kind = "regular_file" if stat.S_ISREG(info.st_mode) else "directory" if stat.S_ISDIR(info.st_mode) else "symlink" if stat.S_ISLNK(info.st_mode) else "other"
        result[path] = (status_code, info.st_size, kind)
    return result


def rejected(check: Callable[[], Any]) -> str:
    try:
        check()
    except (AssertionError, KeyError, FileNotFoundError):
        return "PASS"
    raise AssertionError("catch-proof corruption was accepted")


def validate_manifest_payload(payload: bytes, expected_sha256: str) -> None:
    assert sha256(payload) == expected_sha256


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--base", required=True)
    parser.add_argument("--correction-base", required=True)
    parser.add_argument("--inventory", type=Path, required=True)
    parser.add_argument("--ownership", type=Path, required=True)
    parser.add_argument("--readiness", type=Path, required=True)
    parser.add_argument("--frontier", type=Path, required=True)
    parser.add_argument("--dependency-map", type=Path, required=True)
    parser.add_argument("--forensic-dependency-map", type=Path, required=True)
    parser.add_argument("--candidates", type=Path, required=True)
    parser.add_argument("--candidate-audit", type=Path, required=True)
    parser.add_argument("--mechanical-closure", type=Path, required=True)
    parser.add_argument("--recommendation", type=Path, required=True)
    parser.add_argument("--dirty-inventory", type=Path, required=True)
    parser.add_argument("--dirty-checkout", type=Path, required=True)
    parser.add_argument("--test-result", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    repo = args.repo.resolve()
    base = str(run(repo, ["git", "rev-parse", args.base])).strip()
    assert base == "07c67bfbe661705c6b936243fa1ed697f23c1644"
    correction_base = str(run(repo, ["git", "rev-parse", args.correction_base])).strip()
    assert correction_base == CORRECTION_BASE

    frozen, _ = load_tsv(args.inventory)
    ownership, _ = load_tsv(args.ownership)
    readiness, _ = load_tsv(args.readiness)
    validate_tables(frozen, ownership, readiness)
    own_by_path = {row["current_path"]: row for row in ownership}

    lane_files = {
        "FOUNDATIONS": repo / "research/foundations/ROOT_INVENTORY.tsv",
        "NATIVE_ACTION": repo / "research/native_action/ROOT_INVENTORY.tsv",
        "PARTICLE_MASS": repo / "research/particle_mass/ROOT_INVENTORY.tsv",
        "MACRO": repo / "research/macro/ROOT_INVENTORY.tsv",
    }
    for lane, path in lane_files.items():
        lane_rows, _ = load_tsv(path)
        validate_lane_inventory(ownership, lane, lane_rows)
        assert all((repo / row["current_path"]).exists() for row in lane_rows)

    links = markdown_sources(repo)
    link_count = validate_links(repo, links)
    validate_readme(repo, base)

    dependencies, _ = load_tsv(args.dependency_map)
    forensic_dependencies, _ = load_tsv(args.forensic_dependency_map)
    candidate_rows, _ = load_tsv(args.candidates)
    audit_rows, _ = load_tsv(args.candidate_audit)
    mechanical = json.loads(args.mechanical_closure.read_text(encoding="utf-8"))
    recommendation = json.loads(args.recommendation.read_text(encoding="utf-8"))
    recommendation_summary = validate_recommendation(
        repo, recommendation, candidate_rows, audit_rows, mechanical,
        ownership, readiness, dependencies, forensic_dependencies,
    )
    expected_frontier = set()
    for edge in dependencies:
        source = edge["source"]
        if source not in SOURCE_RANGES or not edge["line"].isdigit() or not edge["status"].startswith("RESOLVED"):
            continue
        line = int(edge["line"])
        if not any(start <= line <= end for start, end in SOURCE_RANGES[source]):
            continue
        for target in filter(None, edge["resolved_target"].split("|")):
            target_path = repo / target.rstrip("/")
            if target_path.exists():
                kind = "ROOT_FILE" if target in own_by_path else ("DIRECTORY" if target.endswith("/") else "TRACKED_NESTED")
                expected_frontier.add((target, kind, source, str(line), edge["category"]))
    for target in ("UDT_METHOD_MUSIC.md", "UDT_DOTTED_LINE.md", "UDT_ELEGANCE_UNCOVER.md", "SIMPLE_METRIC_MACRO.md"):
        expected_frontier.add((target, "ROOT_FILE", "LIVE.md", "8", "EXPLICIT_MACRO_READ_ORDER"))
    frontier_rows, _ = load_tsv(args.frontier)
    actual_frontier = {
        (row["target_path"], row["target_kind"], row["source"], row["line"], row["category"])
        for row in frontier_rows
    }
    assert actual_frontier == expected_frontier
    frontier_targets = {row["target_path"].rstrip("/") for row in frontier_rows}
    assert all((repo / target).exists() for target in frontier_targets)
    assert all(target in own_by_path for target in frontier_targets if "/" not in target and (repo / target).is_file())

    diff_lines = str(run(repo, ["git", "diff", "--name-status", "--find-renames=100%", base])).splitlines()
    additions = validate_diff(diff_lines)
    correction_diff_lines = str(
        run(repo, ["git", "diff", "--name-status", "--find-renames=100%", correction_base])
    ).splitlines()
    correction_additions, correction_modifications = validate_correction_diff(correction_diff_lines)
    assert "research/_registry/FIRST_ACTIVE_FAMILY_MIGRATION_RECOMMENDATION.json" in correction_additions
    assert "reorganization_r1c/correction/R1C_CORRECTION_PREREGISTRATION.md" in correction_additions
    assert "README.md" in str(run(repo, ["git", "diff", "--name-only", base])).splitlines()
    # No added research file is an exact byte copy of a fixed-base artifact.
    base_hashes = {sha256(git_blob(repo, base, path)) for path in git_paths(repo, base)}
    for path in additions:
        if path.startswith("research/"):
            assert sha256((repo / path).read_bytes()) not in base_hashes, path

    frozen_replays = []
    base_paths = set(git_paths(repo, base))
    for package, expected_manifest in PACKAGES.items():
        manifest = repo / package / "SHA256SUMS.txt"
        assert sha256(manifest.read_bytes()) == expected_manifest
        replay = subprocess.run(
            ["sha256sum", "--check", "SHA256SUMS.txt"], cwd=repo / package,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=False,
        )
        assert replay.returncode == 0, f"{package}: {replay.stdout}\n{replay.stderr}"
        package_paths = sorted(path for path in base_paths if path.startswith(package + "/"))
        assert package_paths
        for path in package_paths:
            assert (repo / path).read_bytes() == git_blob(repo, base, path)
        frozen_replays.append({"package": package, "manifest_sha256": expected_manifest, "result": "PASS"})

    recorded_dirty_rows, _ = load_tsv(args.dirty_inventory)
    recorded_dirty = {row["path"]: row for row in recorded_dirty_rows}
    current_dirty = current_dirty_metadata(args.dirty_checkout.resolve())
    assert len(recorded_dirty) == len(current_dirty) == 54 and set(recorded_dirty) == set(current_dirty)
    for path, (status_code, size, kind) in current_dirty.items():
        row = recorded_dirty[path]
        assert (row["status"], int(row["size_bytes_lstat"]), row["object_type"], row["content_sha256"]) == (status_code, size, kind, "NOT_READ")

    test = json.loads(args.test_result.read_text(encoding="utf-8"))
    assert test["baseline_match"] is True
    assert (test["passed"], test["failed"], test["xfailed"]) == (69, 1, 1)

    bad_ownership = [dict(row) for row in ownership]
    bad_ownership[0]["primary_owner"] = "TWO_OWNERS"
    bad_readiness = [dict(row) for row in readiness]
    bad_readiness[0]["migration_readiness"] = "MAYBE"
    bad_links = dict(links)
    bad_links["research/README.md"] = bad_links["research/README.md"].replace("foundations/README.md", "foundations/MISSING.md", 1)
    bad_destination = copy.deepcopy(recommendation)
    bad_destination["recommended_files"][0]["destination"] = "research/macro/WRONG_DESTINATION.md"

    def selector_recommendation(selector_path: str) -> dict[str, Any]:
        bad = copy.deepcopy(recommendation)
        bad["recommended_files"][0]["current_path"] = selector_path
        bad["recommended_files"][0]["primary_owner"] = "NATIVE_ACTION"
        bad["recommended_files"][0]["migration_readiness"] = "IMMUTABLE_PATH"
        bad["recommended_files"][0]["destination"] = "-"
        bad["recommended_files"][0]["frozen_manifest_status"] = "R0_FROZEN_EVIDENCE"
        return bad

    def check_recommendation(payload: dict[str, Any]) -> dict[str, Any]:
        return validate_recommendation(
            repo, payload, candidate_rows, audit_rows, mechanical,
            ownership, readiness, dependencies, forensic_dependencies,
        )

    result = {
        "result": "PASS",
        "mode": "R1C_INDEPENDENT_FAIL_CLOSED_OVERLAY_VERIFY",
        "base": base,
        "root_rows": len(frozen),
        "ownership_rows": len(ownership),
        "readiness_rows": len(readiness),
        "primary_owner_counts": dict(sorted(__import__("collections").Counter(row["primary_owner"] for row in ownership).items())),
        "readiness_counts": dict(sorted(__import__("collections").Counter(row["migration_readiness"] for row in readiness).items())),
        "current_frontier_reference_rows": len(frontier_rows),
        "current_frontier_unique_targets": len(frontier_targets),
        "verified_markdown_links": link_count,
        "authorized_additions": len(additions),
        "only_existing_path_modified": "README.md",
        "correction_base": correction_base,
        "correction_additions": len(correction_additions),
        "correction_modified_records": sorted(correction_modifications),
        "candidate_closure_rows": len(audit_rows),
        "recommendation": recommendation_summary,
        "research_artifact_moves_renames_copies_deletes": 0,
        "frozen_manifest_replays": frozen_replays,
        "dirty_workstation_rows_metadata_only": len(current_dirty),
        "dirty_content_policy": "NOT_READ",
        "test_baseline": test,
        "catchproof": {
            "missing_ownership_row_rejected": rejected(lambda: validate_tables(frozen, ownership[:-1], readiness)),
            "duplicate_ownership_row_rejected": rejected(lambda: validate_tables(frozen, ownership + [ownership[0]], readiness)),
            "bad_primary_owner_rejected": rejected(lambda: validate_tables(frozen, bad_ownership, readiness)),
            "bad_readiness_rejected": rejected(lambda: validate_tables(frozen, ownership, bad_readiness)),
            "bad_recommendation_destination_rejected": rejected(lambda: check_recommendation(bad_destination)),
            "selector_audit_recommendation_rejected": rejected(
                lambda: check_recommendation(selector_recommendation(SELECTOR_AUDIT_PATHS[0]))
            ),
            "selector_audit_prereg_recommendation_rejected": rejected(
                lambda: check_recommendation(selector_recommendation(SELECTOR_AUDIT_PATHS[1]))
            ),
            "broken_link_rejected": rejected(lambda: validate_links(repo, bad_links)),
            "startup_order_mutation_rejected": rejected(lambda: validate_readme(repo, base, (repo / "README.md").read_bytes().replace(b"LIVE.md", b"L1VE.md", 1))),
            "unauthorized_existing_edit_rejected": rejected(lambda: validate_diff(["M\tLIVE.md"])),
            "manifest_mutation_rejected": rejected(
                lambda: validate_manifest_payload(b"mutated", next(iter(PACKAGES.values())))
            ),
        },
    }
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
