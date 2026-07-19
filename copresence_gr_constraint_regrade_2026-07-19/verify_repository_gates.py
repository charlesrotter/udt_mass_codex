#!/usr/bin/env python3
"""Fail-closed repository gates for the co-presence GR-constraint regrade."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import re
import stat
import subprocess
from pathlib import Path
from urllib.parse import unquote


BASE = "b083deea5711aa4dc6f571036114e5304272955d"
PACKAGE = "copresence_gr_constraint_regrade_2026-07-19"
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


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def run(cwd: Path, command: list[str], *, env: dict[str, str] | None = None, binary: bool = False):
    return subprocess.run(
        command,
        cwd=cwd,
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=not binary,
        check=False,
    )


def git(repo: Path, *args: str, binary: bool = False):
    completed = run(repo, ["git", *args], binary=binary)
    if completed.returncode:
        output = completed.stdout if not binary else completed.stdout.decode("utf-8", "replace")
        raise GateError("GIT", output)
    return completed.stdout


def rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def expect(code: str, callback) -> str:
    try:
        callback()
    except GateError as exc:
        if exc.code == code:
            return "PASS"
        raise
    raise AssertionError(f"catch-proof accepted corruption: {code}")


def validate_scope(repo: Path, injected: str | None = None) -> list[str]:
    changed = set(str(git(repo, "diff", "--name-only", BASE)).splitlines())
    changed.update(str(git(repo, "ls-files", "--others", "--exclude-standard")).splitlines())
    if injected:
        changed.add(injected)
    invalid = sorted(path for path in changed if path and not path.startswith(PACKAGE + "/"))
    if invalid:
        raise GateError("SCOPE", invalid[0])
    return sorted(path for path in changed if path)


def validate_frozen(repo: Path, corrupt: bool = False) -> dict[str, object]:
    base_paths = set(str(git(repo, "ls-tree", "-r", "--name-only", BASE)).splitlines())
    current_paths = set(str(git(repo, "ls-files")).splitlines())
    index = {
        line.split(None, 3)[3]: line.split()[1]
        for line in str(git(repo, "ls-files", "-s")).splitlines()
    }
    details = []
    total_entries = 0
    total_paths = 0
    for number, (package, expected_manifest_sha) in enumerate(PACKAGES.items()):
        manifest = repo / package / "SHA256SUMS.txt"
        observed_manifest_sha = digest(manifest.read_bytes())
        if corrupt and number == 0:
            observed_manifest_sha = "0" * 64
        if observed_manifest_sha != expected_manifest_sha:
            raise GateError("FROZEN", package + ":manifest")
        replay = run(manifest.parent, ["sha256sum", "--check", manifest.name])
        if replay.returncode or "FAILED" in replay.stdout:
            raise GateError("FROZEN", package + ":replay")
        before = sorted(path for path in base_paths if path.startswith(package + "/"))
        after = sorted(path for path in current_paths if path.startswith(package + "/"))
        if not before or before != after:
            raise GateError("FROZEN", package + ":paths")
        for path in before:
            base_oid = str(git(repo, "rev-parse", f"{BASE}:{path}")).strip()
            if index.get(path) != base_oid:
                raise GateError("FROZEN", path + ":blob")
        entry_count = sum(bool(line) for line in manifest.read_text(encoding="utf-8").splitlines())
        total_entries += entry_count
        total_paths += len(before)
        details.append({"package": package, "entries": entry_count, "paths": len(before), "result": "PASS"})
    if total_entries != 127 or total_paths != 133:
        raise GateError("FROZEN", f"totals:{total_entries}:{total_paths}")
    return {"packages": details, "manifest_entries": total_entries, "tracked_paths": total_paths}


def validate_navigation(repo: Path, corrupt: str | None = None) -> dict[str, int]:
    current = rows(repo / "research/_registry/CURRENT_ARTIFACT_PATHS.tsv")
    current_paths = [row["current_path"] for row in current]
    if corrupt == "current":
        current_paths = current_paths[:-1]
    if len(current) != 1114 or len(current_paths) != 1114 or len(set(current_paths)) != 1114:
        raise GateError("NAVIGATION", "current-count")
    if not all((repo / path).exists() for path in current_paths):
        raise GateError("NAVIGATION", "current-target")

    frontier = rows(repo / "research/_registry/CURRENT_FRONTIER_TARGETS.tsv")
    targets = {row["target_path"].rstrip("/") for row in frontier}
    if corrupt == "frontier":
        targets.pop()
    if len(frontier) != 306 or len(targets) != 101:
        raise GateError("NAVIGATION", "frontier-count")
    if not all((repo / path).exists() for path in targets):
        raise GateError("NAVIGATION", "frontier-target")

    link_pattern = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
    links = []
    for source in sorted((repo / PACKAGE).glob("*.md")):
        for raw in link_pattern.findall(source.read_text(encoding="utf-8")):
            target = raw.strip().strip("<>")
            if target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            target = unquote(target.split("#", 1)[0])
            links.append(source.parent.joinpath(target).resolve())
    if not all(path.exists() for path in links):
        raise GateError("NAVIGATION", "markdown-link")
    return {
        "current_paths": len(current),
        "frontier_rows": len(frontier),
        "frontier_targets": len(targets),
        "package_links": len(links),
    }


def dirty_metadata(repo: Path) -> dict[str, tuple[str, int, str]]:
    raw = bytes(git(repo, "status", "--porcelain=v2", "-z", "--untracked-files=all", binary=True))
    records = raw.split(b"\0")
    observed: dict[str, tuple[str, int, str]] = {}
    index = 0
    while index < len(records):
        record = records[index]
        index += 1
        if not record:
            continue
        marker = record[:1]
        if marker == b"1":
            fields = record.split(b" ", 8)
            code, raw_path = fields[1].decode(), fields[8]
        elif marker == b"2":
            fields = record.split(b" ", 9)
            code, raw_path = fields[1].decode(), fields[9]
            index += 1
        elif marker == b"u":
            fields = record.split(b" ", 10)
            code, raw_path = fields[1].decode(), fields[10]
        elif marker in {b"?", b"!"}:
            code, raw_path = ("??" if marker == b"?" else "!!"), record[2:]
        else:
            raise GateError("DIRTY", repr(record[:40]))
        path = raw_path.decode("utf-8", "surrogateescape")
        info = (repo / path).lstat()
        kind = (
            "regular_file" if stat.S_ISREG(info.st_mode)
            else "directory" if stat.S_ISDIR(info.st_mode)
            else "symlink" if stat.S_ISLNK(info.st_mode)
            else "other"
        )
        observed[path] = (code, info.st_size, kind)
    return observed


def validate_dirty(repo: Path, original: Path, corrupt: bool = False) -> int:
    recorded = {
        row["path"]: row
        for row in rows(repo / "reorganization_r1b/postmove_forensic_census/DIRTY_WORKSTATION_INVENTORY.tsv")
    }
    observed = dirty_metadata(original)
    if corrupt:
        observed = dict(observed)
        observed.pop(next(iter(observed)))
    if len(recorded) != 54 or len(observed) != 54 or set(recorded) != set(observed):
        raise GateError("DIRTY", f"count:{len(recorded)}:{len(observed)}")
    for path, value in observed.items():
        row = recorded[path]
        expected = (row["status"], int(row["size_bytes_lstat"]), row["object_type"])
        if value != expected or row["content_sha256"] != "NOT_READ":
            raise GateError("DIRTY", path)
    return len(observed)


def validate_tests(repo: Path) -> dict[str, object]:
    env = dict(os.environ)
    env["CUDA_VISIBLE_DEVICES"] = ""
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    completed = run(repo, ["python3", "-m", "pytest", "tests/"], env=env)
    match = re.search(r"(\d+) failed, (\d+) passed, (\d+) xfailed", completed.stdout)
    if completed.returncode != 1 or match is None:
        raise GateError("TESTS", f"return:{completed.returncode}")
    failed, passed, xfailed = map(int, match.groups())
    if (passed, failed, xfailed) != (69, 1, 1):
        raise GateError("TESTS", f"counts:{passed}:{failed}:{xfailed}")
    expected_failure = "tests/test_hygiene_header.py::test_covered_results_have_hygiene_header"
    if expected_failure not in completed.stdout:
        raise GateError("TESTS", "unexpected-failure")
    return {
        "command": "CUDA_VISIBLE_DEVICES= PYTHONDONTWRITEBYTECODE=1 python3 -m pytest tests/",
        "collected": 71,
        "passed": passed,
        "failed": failed,
        "xfailed": xfailed,
        "failure": expected_failure,
        "baseline_match": True,
        "stdout_sha256": digest(completed.stdout.encode("utf-8")),
    }


def validate_package_manifest(repo: Path, corrupt: bool = False) -> dict[str, object]:
    manifest = repo / PACKAGE / "SHA256SUMS.txt"
    replay = run(manifest.parent, ["sha256sum", "--check", manifest.name])
    if corrupt:
        replay = type(replay)(replay.args, 1, stdout="FAILED")
    if replay.returncode or "FAILED" in replay.stdout:
        raise GateError("PACKAGE", "hash-replay")
    entries = [line.split("  ", 1)[1] for line in manifest.read_text(encoding="utf-8").splitlines() if line]
    excluded = {"SHA256SUMS.txt", "REPOSITORY_GATE_RESULT.json"}
    actual = sorted(path.name for path in manifest.parent.iterdir() if path.is_file() and path.name not in excluded)
    if sorted(entries) != actual:
        raise GateError("PACKAGE", f"coverage:{sorted(set(entries) ^ set(actual))}")
    return {"entries": len(entries), "sha256": digest(manifest.read_bytes()), "result": "PASS"}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--dirty-checkout", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    repo = args.repo.resolve()
    dirty = args.dirty_checkout.resolve()

    scope = validate_scope(repo)
    frozen = validate_frozen(repo)
    navigation = validate_navigation(repo)
    dirty_count = validate_dirty(repo, dirty)
    tests = validate_tests(repo)
    package = validate_package_manifest(repo)
    catches = {
        "out_of_scope_change_rejected": expect("SCOPE", lambda: validate_scope(repo, "LIVE.md")),
        "frozen_manifest_corruption_rejected": expect("FROZEN", lambda: validate_frozen(repo, corrupt=True)),
        "missing_current_path_rejected": expect("NAVIGATION", lambda: validate_navigation(repo, corrupt="current")),
        "missing_frontier_target_rejected": expect("NAVIGATION", lambda: validate_navigation(repo, corrupt="frontier")),
        "dirty_metadata_loss_rejected": expect("DIRTY", lambda: validate_dirty(repo, dirty, corrupt=True)),
        "package_hash_failure_rejected": expect("PACKAGE", lambda: validate_package_manifest(repo, corrupt=True)),
    }

    output = {
        "schema": "udt-copresence-gr-constraint-regrade-repository-gates-v1",
        "result": "PASS",
        "base": BASE,
        "scope_paths": scope,
        "frozen": frozen,
        "navigation": navigation,
        "dirty_checkout": {"paths": dirty_count, "contents_read": False},
        "tests": tests,
        "package_manifest": package,
        "catch_proofs": catches,
    }
    args.output.write_text(json.dumps(output, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print("repository_gates=PASS")
    print(f"frozen_manifests=6 entries={frozen['manifest_entries']} paths={frozen['tracked_paths']}")
    print(f"navigation={navigation}")
    print(f"tests={tests['passed']} passed/{tests['failed']} known failed/{tests['xfailed']} xfailed")
    print(f"dirty_metadata_paths={dirty_count}")
    print(f"gate_result_sha256={digest(args.output.read_bytes())}")


if __name__ == "__main__":
    main()
