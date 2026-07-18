#!/usr/bin/env python3
"""Fail-closed verifier for the navigation-only R1G checkpoint integration."""

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


SOURCE = "ec18725237d93e5821ce7eae555ba02b4e4ecbd7"
EXPECTED_GROK = "8015342a81b2d27cc310dde95ab7f386c6441a77"
PREREG = "15f2b8632127b4c01ed66c3ba0478b936d363957"
R1G_REMOTE = "origin/codex/reorg-r1g-provenance-audit-2026-07-18"
AUTHORIZED = {
    "LIVE.md",
    "HANDOFF.md",
    "INDEX.md",
    "README.md",
    "research/README.md",
    "research/_registry/README.md",
}
PROTECTED_REGISTRIES = {
    "research/_registry/CURRENT_ARTIFACT_PATHS.tsv",
    "research/_registry/MIGRATION_LEDGER.tsv",
    "research/_registry/MIGRATION_READINESS.tsv",
    "research/_registry/ROOT_OWNERSHIP.tsv",
}
PACKAGES = {
    "native_action_stage1_2026-07-18/arm_A": "d72e8d6e1b4bc8682bd5518264a1a43a3b5f7b3b246b3d218ea6bfecc6927d19",
    "native_action_stage1_2026-07-18/arm_B": "a99937a8fbba57ac24f490c2974937718f7dfbc2f2f7dd7c960d57fc5e839b92",
    "native_action_stage2_2026-07-18/arm_A": "ad63ffacdd5282a35fe0aef62269464d987aa61b710a4d393d95836234fd670a",
    "native_action_stage2_2026-07-18/arm_B": "30b2a3863f1d16e3b3507b5d0bf10a6b5b59c1e54d769cacc53127cc676d6d45",
    "native_action_arm_c_2026-07-18": "99fc0d6c26aff24e43b8636d74f80e3486c56131590552308b47c1d107ed500f",
    "native_action_final_adjudication_2026-07-18": "57be0046432c27046e84eaafd1706959558f43170d0f1e23dc3047966e512f33",
}
R1G_CATCHPROOFS = {
    "post_july_cascade_without_lineage_rejected",
    "removing_pre_native_lineage_evidence_rejected",
    "pre_native_destination_without_pre_native_provenance_rejected",
    "missing_candidate_rejected",
    "duplicate_candidate_rejected",
    "reference_only_gr_readout_demotion_rejected",
    "deleted_readout_disclosure_rejected",
    "imported_action_coupling_as_reference_only_rejected",
}


class GateError(AssertionError):
    def __init__(self, code: str, detail: str = "") -> None:
        super().__init__(f"{code}: {detail}")
        self.code = code


def run(cwd: Path, command: list[str], *, binary: bool = False, check: bool = True):
    completed = subprocess.run(
        command,
        cwd=cwd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=not binary,
        check=False,
    )
    if check and completed.returncode:
        error = completed.stderr if not binary else completed.stderr.decode("utf-8", "replace")
        raise AssertionError(f"command failed: {' '.join(command)}\n{error}")
    return completed


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


def validate_remote(repo: Path, expected_grok: str = EXPECTED_GROK) -> dict[str, object]:
    grok = str(git(repo, "rev-parse", "origin/grok")).strip()
    r1g = str(git(repo, "rev-parse", R1G_REMOTE)).strip()
    merge_base = str(git(repo, "merge-base", "origin/grok", R1G_REMOTE)).strip()
    ancestor = git(repo, "merge-base", "--is-ancestor", "origin/grok", R1G_REMOTE, check=False)
    if grok != expected_grok or r1g != SOURCE or merge_base != expected_grok or ancestor.returncode:
        raise GateError("REMOTE_GUARD", f"{grok}:{r1g}:{merge_base}:{ancestor.returncode}")
    count = int(str(git(repo, "rev-list", "--count", f"origin/grok..{R1G_REMOTE}")).strip())
    merges = str(git(repo, "rev-list", "--merges", f"origin/grok..{R1G_REMOTE}")).splitlines()
    if count != 4 or merges:
        raise GateError("REMOTE_GUARD", f"commits={count};merges={merges}")
    return {
        "origin_grok": grok,
        "r1g_tip": r1g,
        "merge_base": merge_base,
        "linear_commits": count,
    }


def validate_r1g_scope(repo: Path, injected: str | None = None) -> list[str]:
    changed = [line for line in str(git(repo, "diff", "--name-only", EXPECTED_GROK, SOURCE)).splitlines() if line]
    if injected:
        changed.append(injected)
    invalid = sorted(path for path in changed if not path.startswith("reorganization_r1g/"))
    if not changed or invalid:
        raise GateError("R1G_SOURCE_SCOPE", ",".join(invalid))
    return sorted(set(changed))


def validate_prereg(repo: Path) -> None:
    parent = str(git(repo, "rev-parse", f"{PREREG}^")).strip()
    changed = str(git(repo, "diff-tree", "--no-commit-id", "--name-only", "-r", PREREG)).splitlines()
    expected = ["reorganization_r1g_checkpoint/R1G_CHECKPOINT_INTEGRATION_PREREGISTRATION.md"]
    if parent != SOURCE or changed != expected:
        raise GateError("PREREGISTRATION", f"{parent}:{changed}")


def validate_scope(repo: Path, extra: str | None = None) -> list[str]:
    changed = set(str(git(repo, "diff", "--name-only", SOURCE)).splitlines())
    changed.update(str(git(repo, "ls-files", "--others", "--exclude-standard")).splitlines())
    if extra:
        changed.add(extra)
    invalid = sorted(
        path for path in changed
        if path not in AUTHORIZED and not path.startswith("reorganization_r1g_checkpoint/")
    )
    if invalid:
        raise GateError("UNAUTHORIZED_EDIT", ",".join(invalid))
    if not AUTHORIZED.issubset(changed):
        raise GateError("AUTHORIZED_FILE_MISSING", ",".join(sorted(AUTHORIZED - changed)))
    if PROTECTED_REGISTRIES & changed:
        raise GateError("UNAUTHORIZED_EDIT", ",".join(sorted(PROTECTED_REGISTRIES & changed)))
    if str(git(repo, "diff", "--name-only", SOURCE, "--", "reorganization_r1g")).strip():
        raise GateError("UNAUTHORIZED_EDIT", "reorganization_r1g")
    return sorted(changed)


def validate_navigation(repo: Path, replacement: dict[str, str] | None = None) -> None:
    replacement = replacement or {}
    for path in sorted(AUTHORIZED):
        text = replacement.get(path, (repo / path).read_text(encoding="utf-8"))
        flat = " ".join(text.split())
        lower = flat.lower()
        required = (
            "R1G",
            "prefix-based pre-native classification",
            "false",
            "121",
            "NATIVE_2026-07-01",
            "zero `MIXED`",
            "29",
            "two `MIXED`",
            "one `OPEN`",
            "GR/Einstein/Misner–Sharp",
            "phi_source_derivation.py",
            "homog_alpha_test.py",
            "action/EOM",
            "archive/pre_2026-07-01/",
            "ROOT_OWNERSHIP.tsv",
            "MIGRATION_READINESS.tsv",
            "supersedes",
            "separately authorized correction",
            "B02/B03",
            "further migration",
        )
        if any(needle not in flat for needle in required) or "withdrawn" not in lower or "authorized" not in lower:
            raise GateError("NAVIGATION_WORDING", path)
    readme = replacement.get("README.md", (repo / "README.md").read_text(encoding="utf-8"))
    order = [readme.index(token) for token in ("LIVE.md", "HANDOFF.md", "stability_branch_follow_256_DECISION.md")]
    if order != sorted(order):
        raise GateError("NAVIGATION_WORDING", "README startup order")


def validate_r1g_hashes(repo: Path, corrupt: bool = False) -> dict[str, object]:
    index_path = repo / "reorganization_r1g/OUTPUT_SHA256SUMS.tsv"
    index = rows(index_path)
    tracked = set(str(git(repo, "ls-files", "reorganization_r1g")).splitlines())
    expected_indexed = tracked - {"reorganization_r1g/OUTPUT_SHA256SUMS.tsv"}
    indexed = [row["path"] for row in index]
    if len(index) != 25 or len(set(indexed)) != 25 or set(indexed) != expected_indexed:
        raise GateError("R1G_HASH", f"rows={len(index)};tracked={len(tracked)}")
    for number, row in enumerate(index):
        payload = (repo / row["path"]).read_bytes()
        observed = sha(payload)
        if corrupt and number == 0:
            observed = "0" * 64
        if observed != row["sha256"] or len(payload) != int(row["size_bytes"]):
            raise GateError("R1G_HASH", row["path"])
    source_index = bytes(git(repo, "show", f"{SOURCE}:reorganization_r1g/OUTPUT_SHA256SUMS.tsv", binary=True))
    if index_path.read_bytes() != source_index:
        raise GateError("R1G_HASH", "hash index differs from source tip")
    candidates = rows(repo / "reorganization_r1g/B02_B03_ADJUDICATION.tsv")
    affected = rows(repo / "reorganization_r1g/AFFECTED_CASCADE_FILE_CENSUS.tsv")
    candidate_counts = Counter(row["operator_provenance"] for row in candidates)
    affected_counts = Counter(row["operator_provenance"] for row in affected)
    if candidate_counts != Counter({"NATIVE_2026-07-01": 29, "MIXED": 2, "OPEN": 1}):
        raise GateError("R1G_HASH", f"candidate counts={candidate_counts}")
    if affected_counts != Counter({"NATIVE_2026-07-01": 121}):
        raise GateError("R1G_HASH", f"affected counts={affected_counts}")
    return {
        "indexed_files": len(index),
        "hash_index_sha256": sha(index_path.read_bytes()),
        "b02_b03_operator_provenance": dict(candidate_counts),
        "affected_operator_provenance": dict(affected_counts),
    }


def validate_r1g_replay(path: Path, corrupt: bool = False) -> dict[str, object]:
    replay = json.loads(path.read_text(encoding="utf-8"))
    if corrupt:
        replay = copy.deepcopy(replay)
        replay["catchproof"][next(iter(R1G_CATCHPROOFS))] = "FAIL"
    catchproof = replay.get("catchproof", {})
    if replay.get("result") != "PASS" or set(catchproof) != R1G_CATCHPROOFS or set(catchproof.values()) != {"PASS"}:
        raise GateError("R1G_CATCHPROOF", str(catchproof))
    if replay.get("candidate_operator_provenance") != {"MIXED": 2, "NATIVE_2026-07-01": 29, "OPEN": 1}:
        raise GateError("R1G_CATCHPROOF", "candidate totals")
    if replay.get("affected_operator_provenance") != {"NATIVE_2026-07-01": 121}:
        raise GateError("R1G_CATCHPROOF", "affected totals")
    return replay


def validate_links(repo: Path, injected_missing: bool = False) -> int:
    sources = [repo / path for path in sorted(AUTHORIZED)]
    sources += sorted((repo / "research").rglob("*.md"))
    sources += sorted((repo / "reorganization_r1g").rglob("*.md"))
    sources += sorted((repo / "reorganization_r1g_checkpoint").rglob("*.md"))
    pattern = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
    targets: list[Path] = []
    for source in dict.fromkeys(sources):
        for raw in pattern.findall(source.read_text(encoding="utf-8")):
            target = raw.strip().strip("<>")
            if target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            target = unquote(target.split("#", 1)[0])
            targets.append(source.parent.joinpath(target).resolve())
    if injected_missing:
        targets.append(repo / "missing-r1g-checkpoint-catchproof")
    missing = [path for path in targets if not path.exists()]
    if missing:
        raise GateError("BROKEN_LINK", str(missing[0]))
    return len(targets)


def validate_frontier(repo: Path) -> dict[str, int]:
    frontier = rows(repo / "research/_registry/CURRENT_FRONTIER_TARGETS.tsv")
    targets = {row["target_path"].rstrip("/") for row in frontier}
    if len(frontier) != 306 or len(targets) != 101 or not all((repo / target).exists() for target in targets):
        raise GateError("FRONTIER", f"{len(frontier)}/{len(targets)}")
    return {"rows": len(frontier), "unique_targets": len(targets)}


def validate_manifests(repo: Path, corrupt: bool = False) -> list[dict[str, object]]:
    source_paths = set(str(git(repo, "ls-tree", "-r", "--name-only", SOURCE)).splitlines())
    current_paths = set(str(git(repo, "ls-files")).splitlines())
    index_oids = {
        line.split(None, 3)[3]: line.split()[1]
        for line in str(git(repo, "ls-files", "-s")).splitlines()
    }
    result = []
    for number, (package, expected_digest) in enumerate(PACKAGES.items()):
        expected = "0" * 64 if corrupt and number == 0 else expected_digest
        manifest = repo / package / "SHA256SUMS.txt"
        if sha(manifest.read_bytes()) != expected:
            raise GateError("MANIFEST", package)
        replay = run(repo / package, ["sha256sum", "--check", "SHA256SUMS.txt"])
        source_package = sorted(path for path in source_paths if path.startswith(package + "/"))
        current_package = sorted(path for path in current_paths if path.startswith(package + "/"))
        if not source_package or current_package != source_package:
            raise GateError("MANIFEST", f"{package}:path state")
        for path in source_package:
            if index_oids[path] != str(git(repo, "rev-parse", f"{SOURCE}:{path}")).strip():
                raise GateError("MANIFEST", path)
        result.append({
            "package": package,
            "manifest_sha256": expected_digest,
            "manifest_entries_passed": len(replay.stdout.splitlines()),
            "tracked_paths_byte_identical_to_source": len(source_package),
            "result": "PASS",
        })
    return result


def dirty_metadata(repo: Path) -> dict[str, tuple[str, int, str]]:
    raw = bytes(git(repo, "status", "--porcelain=v2", "-z", "--untracked-files=all", binary=True))
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
        kind = (
            "regular_file" if stat.S_ISREG(info.st_mode)
            else "directory" if stat.S_ISDIR(info.st_mode)
            else "symlink" if stat.S_ISLNK(info.st_mode)
            else "other"
        )
        result[path] = (code, info.st_size, kind)
    return result


def validate_dirty(repo: Path, dirty_checkout: Path, corrupt: bool = False) -> int:
    inventory = repo / "reorganization_r1b/postmove_forensic_census/DIRTY_WORKSTATION_INVENTORY.tsv"
    recorded = {row["path"]: row for row in rows(inventory)}
    observed = dirty_metadata(dirty_checkout)
    if corrupt:
        observed = dict(observed)
        observed.pop(next(iter(observed)))
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
    parser.add_argument("--r1g-replay", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    repo = args.repo.resolve()

    remote = validate_remote(repo)
    r1g_source_paths = validate_r1g_scope(repo)
    validate_prereg(repo)
    changed = validate_scope(repo)
    validate_navigation(repo)
    hashes = validate_r1g_hashes(repo)
    replay = validate_r1g_replay(args.r1g_replay.resolve())
    links = validate_links(repo)
    frontier = validate_frontier(repo)
    manifests = validate_manifests(repo)
    dirty_count = validate_dirty(repo, args.dirty_checkout.resolve())
    test = json.loads(args.test_result.read_text(encoding="utf-8"))
    if (test.get("passed"), test.get("failed"), test.get("xfailed"), test.get("baseline_match")) != (69, 1, 1, True):
        raise GateError("TEST_BASELINE", str(test))

    omitted = re.sub(
        r"prefix-based pre-native\s+classification",
        "prefix classification",
        (repo / "LIVE.md").read_text(encoding="utf-8"),
        count=1,
    )
    catchproof = {
        "remote_drift_rejected": catch("REMOTE_GUARD", lambda: validate_remote(repo, "0" * 40)),
        "r1g_source_scope_drift_rejected": catch("R1G_SOURCE_SCOPE", lambda: validate_r1g_scope(repo, "LIVE.md")),
        "unauthorized_navigation_edit_rejected": catch("UNAUTHORIZED_EDIT", lambda: validate_scope(repo, "CANON.md")),
        "navigation_omission_rejected": catch("NAVIGATION_WORDING", lambda: validate_navigation(repo, {"LIVE.md": omitted})),
        "r1g_hash_mutation_rejected": catch("R1G_HASH", lambda: validate_r1g_hashes(repo, True)),
        "r1g_catchproof_drift_rejected": catch("R1G_CATCHPROOF", lambda: validate_r1g_replay(args.r1g_replay.resolve(), True)),
        "manifest_mutation_rejected": catch("MANIFEST", lambda: validate_manifests(repo, True)),
        "broken_link_rejected": catch("BROKEN_LINK", lambda: validate_links(repo, True)),
        "dirty_metadata_drift_rejected": catch("DIRTY_METADATA", lambda: validate_dirty(repo, args.dirty_checkout.resolve(), True)),
    }

    result = {
        "result": "PASS",
        "mode": "R1G_CHECKPOINT_NAVIGATION_ONLY_FAIL_CLOSED_VERIFY",
        "source_tip": SOURCE,
        "preregistration_commit": PREREG,
        "remote_guard": remote,
        "r1g_source_changed_paths": len(r1g_source_paths),
        "r1g_source_scope": "reorganization_r1g/ only",
        "authorized_navigation_files_changed": sorted(AUTHORIZED),
        "all_integration_changed_paths": changed,
        "r1g_hash_replay": hashes,
        "r1g_fresh_replay_sha256": sha(args.r1g_replay.resolve().read_bytes()),
        "r1g_catchproof": replay["catchproof"],
        "markdown_links_verified": links,
        "frontier": frontier,
        "frozen_manifest_replays": manifests,
        "test_baseline": test,
        "dirty_checkout_metadata_rows": dirty_count,
        "dirty_content_policy": "NOT_READ",
        "integration_catchproof": catchproof,
        "r1g_supersedes_fixed_snapshot_for_affected_paths": True,
        "old_b02_b03_pre_2026_07_01_destinations_withdrawn": True,
        "b02_b03_or_further_migration_authorized": False,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
