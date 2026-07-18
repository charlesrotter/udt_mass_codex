#!/usr/bin/env python3
"""Fail-closed final verifier for the R1A inbound-reference correction."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import stat
import subprocess
from pathlib import Path
from typing import Any

from reference_boundary import occurrences


FROZEN_PREFIXES = (
    "native_action_stage1_2026-07-18/",
    "native_action_stage2_2026-07-18/",
    "native_action_arm_c_2026-07-18/",
    "native_action_final_adjudication_2026-07-18/",
)
EXPECTED_MANIFESTS = {
    "native_action_stage1_2026-07-18/arm_A": "d72e8d6e1b4bc8682bd5518264a1a43a3b5f7b3b246b3d218ea6bfecc6927d19",
    "native_action_stage1_2026-07-18/arm_B": "a99937a8fbba57ac24f490c2974937718f7dfbc2f2f7dd7c960d57fc5e839b92",
    "native_action_stage2_2026-07-18/arm_A": "ad63ffacdd5282a35fe0aef62269464d987aa61b710a4d393d95836234fd670a",
    "native_action_stage2_2026-07-18/arm_B": "30b2a3863f1d16e3b3507b5d0bf10a6b5b59c1e54d769cacc53127cc676d6d45",
    "native_action_arm_c_2026-07-18": "99fc0d6c26aff24e43b8636d74f80e3486c56131590552308b47c1d107ed500f",
    "native_action_final_adjudication_2026-07-18": "57be0046432c27046e84eaafd1706959558f43170d0f1e23dc3047966e512f33",
}
HISTORICAL_ARTIFACTS = (
    "reorganization_r1a/ADJUDICATION_SUMMARY.json",
    "reorganization_r1a/CANDIDATE_ADJUDICATION.tsv",
    "reorganization_r1a/ELIGIBLE_BATCH.txt",
    "reorganization_r1a/INBOUND_REFERENCES.tsv",
    "reorganization_r1a/POINTER_REWRITE_PLAN.tsv",
    "reorganization_r1a/PREMOVE_HASHES.tsv",
    "reorganization_r1a/PREMOVE_ADJUDICATION_REPORT.md",
    "reorganization_r1a/PREMOVE_VERIFY_RESULT.json",
    "reorganization_r1a/MOVE_MAP.tsv",
    "reorganization_r1a/POSTMOVE_POINTER_CENSUS.tsv",
)
AUTHORIZED = {
    "HANDOFF_ARCHIVE.md": (
        "PROVENANCE_AUDIT_2026-06-30.md",
        "coupled_timelive_VERIFIER.md",
    ),
    "FOUNDATIONAL_ASSUMPTIONS_LEDGER.md": ("STEP2_timelive_matter_results.md",),
    "archive/tier_d_round3_contract.md": ("lepton_ladder_test_results.md",),
    "NEGATIVES_REGISTRY.md": ("weld_discriminator_results.md",),
}
COLOCATED_SOURCE = "archive/pre_native_coupled/timelive_nonround_native_solve_results.md"
COLOCATED_TARGET = "timelive_nonround_VERIFIER.md"
COLOCATED_DESTINATION = "archive/pre_native_coupled/timelive_nonround_VERIFIER.md"
AUDIT_PREFIXES = ("reorganization_r0/", "reorganization_r1a/")


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
        error = completed.stderr if not binary else completed.stderr.decode("utf-8", "replace")
        raise AssertionError(f"command failed: {' '.join(command)}\n{error}")
    return completed.stdout


def load_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def write_tsv(path: Path, rows: list[dict[str, Any]], fields: tuple[str, ...]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "-") for field in fields})


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def git_blob(repo: Path, revision: str, path: str) -> bytes:
    return bytes(run(repo, ["git", "show", f"{revision}:{path}"], binary=True))


def git_blob_oid(data: bytes) -> str:
    header = f"blob {len(data)}\0".encode("ascii")
    return hashlib.sha1(header + data).hexdigest()


def frozen(source: str, classes: dict[str, str]) -> bool:
    return classes.get(source) == "FROZEN_EVIDENCE" or source.startswith(FROZEN_PREFIXES)


def line_column(text: str, offset: int) -> tuple[int, int]:
    line = text.count("\n", 0, offset) + 1
    start = text.rfind("\n", 0, offset) + 1
    return line, offset - start + 1


def worktree_texts(repo: Path) -> dict[str, str]:
    listed = str(run(repo, ["git", "ls-files", "-co", "--exclude-standard", "-z"]))
    result: dict[str, str] = {}
    for path in sorted(filter(None, listed.split("\0"))):
        payload = (repo / path).read_bytes()
        if b"\0" in payload[:8192]:
            continue
        try:
            result[path] = payload.decode("utf-8")
        except UnicodeDecodeError:
            continue
    return result


def package_state_from_revision(repo: Path, revision: str, package: str) -> tuple[str, int]:
    paths = str(run(repo, ["git", "ls-tree", "-r", "--name-only", revision, "--", package])).splitlines()
    ledger = "".join(f"{path}\0{sha256(git_blob(repo, revision, path))}\n" for path in paths)
    return sha256(ledger.encode("utf-8")), len(paths)


def package_state_from_worktree(repo: Path, revision: str, package: str) -> tuple[str, int]:
    expected = str(run(repo, ["git", "ls-tree", "-r", "--name-only", revision, "--", package])).splitlines()
    current = str(run(repo, ["git", "ls-files", "--", package])).splitlines()
    assert current == expected, f"frozen package path set changed: {package}"
    ledger = "".join(f"{path}\0{sha256((repo / path).read_bytes())}\n" for path in current)
    return sha256(ledger.encode("utf-8")), len(current)


def dirty_metadata(checkout: Path) -> dict[str, tuple[str, int, str]]:
    environment = os.environ.copy()
    environment["GIT_OPTIONAL_LOCKS"] = "0"
    raw = subprocess.check_output(
        ["git", "--no-optional-locks", "status", "--porcelain=v2", "-z", "--untracked-files=all"],
        cwd=checkout,
        env=environment,
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
        object_type = (
            "regular_file" if stat.S_ISREG(info.st_mode)
            else "directory" if stat.S_ISDIR(info.st_mode)
            else "symlink" if stat.S_ISLNK(info.st_mode)
            else "other"
        )
        result[path] = (status_code, info.st_size, object_type)
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--r0-base", required=True)
    parser.add_argument("--historical-base", required=True)
    parser.add_argument("--mutation-base", required=True)
    parser.add_argument("--dirty-checkout", type=Path, required=True)
    parser.add_argument("--pointer-output", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    repo = args.repo.resolve()
    correction = Path(__file__).resolve().parent
    inventory = load_tsv(repo / "reorganization_r0/ROOT_FILE_INVENTORY.tsv")
    classes = {row["path"]: row["classification"] for row in inventory}
    move_map = load_tsv(repo / "reorganization_r1a/MOVE_MAP.tsv")
    omissions = load_tsv(correction / "OMISSION_LEDGER.tsv")

    historical = []
    for path in HISTORICAL_ARTIFACTS:
        actual = (repo / path).read_bytes()
        assert actual == git_blob(repo, args.historical_base, path), path
        historical.append({"path": path, "sha256": sha256(actual), "result": "PASS"})

    pointer_log = {row["source"]: row for row in load_tsv(correction / "POINTER_CORRECTION_RESULT.tsv")}
    assert set(pointer_log) == set(AUTHORIZED)
    pointer_results = []
    for source, targets in AUTHORIZED.items():
        before = git_blob(repo, args.mutation_base, source)
        expected = before.decode("utf-8")
        for target in targets:
            new_target = "archive/pre_2026-07-01/" + target
            assert expected.count(target) == 1, (source, target)
            assert new_target not in expected, (source, new_target)
            expected = expected.replace(target, new_target, 1)
        actual = (repo / source).read_bytes()
        assert actual == expected.encode("utf-8"), source
        recorded = pointer_log[source]
        assert recorded["authorized_targets"].split(";") == list(targets)
        assert int(recorded["replacement_count"]) == len(targets)
        assert recorded["before_sha256"] == sha256(before)
        assert recorded["after_sha256"] == sha256(actual)
        pointer_results.append({"source": source, "replacements": len(targets), "result": "PASS"})

    colocated_before = git_blob(repo, args.mutation_base, COLOCATED_SOURCE)
    colocated_current = (repo / COLOCATED_SOURCE).read_bytes()
    assert colocated_current == colocated_before
    colocated_text = colocated_current.decode("utf-8")
    assert len(occurrences(colocated_text, COLOCATED_TARGET)) == 1
    assert (repo / COLOCATED_DESTINATION).is_file()

    retained = [row for row in omissions if row["disposition"] == "RETAINED_TARGET_NO_REWRITE"]
    assert len(retained) == 8
    for row in retained:
        assert (repo / row["target"]).is_file(), row["target"]
        text = (repo / row["source"]).read_text(encoding="utf-8")
        matches = occurrences(text, row["target"])
        assert matches, (row["source"], row["target"])

    consolidated = load_tsv(correction / "CORRECTED_CONSOLIDATED_ADJUDICATION.tsv")
    eligible = [row for row in consolidated if row["corrected_eligibility_recheck"] == "PASS_UNCHANGED"]
    assert len(eligible) == 17
    assert {row["path"] for row in eligible} == {row["old_path"] for row in move_map}

    moved_results = []
    destinations = {row["new_path"] for row in move_map}
    for row in move_map:
        assert not (repo / row["old_path"]).exists()
        payload = (repo / row["new_path"]).read_bytes()
        assert sha256(payload) == row["sha256_before"] == row["sha256_after"]
        assert git_blob_oid(payload) == row["git_blob_oid_before"]
        assert int(row["size_bytes"]) == len(payload)
        assert row["content_identical"] == "YES"
        moved_results.append({"path": row["new_path"], "sha256": sha256(payload), "result": "PASS"})

    frozen_results = []
    for package, expected_manifest in EXPECTED_MANIFESTS.items():
        manifest = repo / package / "SHA256SUMS.txt"
        assert sha256(manifest.read_bytes()) == expected_manifest, package
        base_state = package_state_from_revision(repo, args.r0_base, package)
        current_state = package_state_from_worktree(repo, args.r0_base, package)
        assert current_state == base_state, package
        frozen_results.append(
            {
                "package": package,
                "manifest_sha256": expected_manifest,
                "complete_state_sha256": current_state[0],
                "tracked_files": current_state[1],
                "result": "PASS",
            }
        )

    texts = worktree_texts(repo)
    for generated in (args.pointer_output, args.output):
        try:
            texts.pop(str(generated.resolve().relative_to(repo)), None)
        except ValueError:
            pass
    pointer_rows: list[dict[str, Any]] = []
    stale: list[tuple[str, int, str]] = []
    for move in move_map:
        old, new = move["old_path"], move["new_path"]
        for source, text in texts.items():
            for offset in occurrences(text, old):
                if text[max(0, offset - len("archive/pre_2026-07-01/")):offset].endswith(
                    "archive/pre_2026-07-01/"
                ):
                    role = "NEW_PATH_SUFFIX"
                elif source == COLOCATED_SOURCE and old == COLOCATED_TARGET:
                    role = "INTENTIONAL_COLOCATED_ARCHIVE_REFERENCE"
                elif offset and text[offset - 1] == "/":
                    role = "QUALIFIED_OTHER_PATH"
                elif source.startswith(AUDIT_PREFIXES):
                    role = "AUDIT_RECORD"
                elif source in destinations:
                    role = "BYTE_PRESERVED_MOVED_RECORD"
                elif frozen(source, classes):
                    role = "FROZEN_SOURCE"
                else:
                    role = "STALE_NON_FROZEN_POINTER"
                    line, _ = line_column(text, offset)
                    stale.append((source, line, old))
                line, column = line_column(text, offset)
                pointer_rows.append(
                    {
                        "moved_path": old,
                        "source": source,
                        "line": line,
                        "column": column,
                        "source_frozen": "YES" if frozen(source, classes) else "NO",
                        "role": role,
                    }
                )
    assert not stale, f"stale non-frozen pointers: {stale[:20]}"
    write_tsv(
        args.pointer_output,
        sorted(pointer_rows, key=lambda row: (row["moved_path"], row["source"], row["line"], row["column"])),
        ("moved_path", "source", "line", "column", "source_frozen", "role"),
    )

    recorded_dirty = {
        row["path"]: (row["status"], int(row["size_bytes_lstat"]), row["object_type"])
        for row in load_tsv(repo / "reorganization_r0/DIRTY_WORKSTATION_INVENTORY.tsv")
    }
    assert all(row["content_sha256"] == "NOT_READ" for row in load_tsv(repo / "reorganization_r0/DIRTY_WORKSTATION_INVENTORY.tsv"))
    current_dirty = dirty_metadata(args.dirty_checkout.resolve())
    assert current_dirty == recorded_dirty
    assert len(current_dirty) == 54

    test = json.loads((correction / "TEST_BASELINE.json").read_text(encoding="utf-8"))
    assert test["baseline_match"] is True
    assert (test["passed"], test["failed"], test["xfailed"]) == (69, 1, 1)

    census = json.loads((correction / "CENSUS_VERIFY_RESULT.json").read_text(encoding="utf-8"))
    assert census["result"] == "PASS" and census["literal_git_grep_exact_agreement"] is True
    assert (
        census["corrected_occurrences"],
        census["corrected_sources"],
        census["corrected_frozen_source_occurrences"],
    ) == (815, 92, 16)

    changed = str(run(repo, ["git", "diff", "--name-status", args.mutation_base])).splitlines()
    allowed_modified = set(AUTHORIZED) | {
        "reorganization_r1a/R1A_AUDIT_REPORT.md",
        "reorganization_r1a/README.md",
    }
    for item in changed:
        status_code, *paths = item.split("\t")
        assert status_code in {"M", "A"}, f"unexpected mutation-base diff: {item}"
        if status_code == "M":
            assert paths[0] in allowed_modified, f"unauthorized modification: {paths[0]}"
        else:
            assert paths[0].startswith("reorganization_r1a/correction_2026-07-18/"), item
        assert not any(frozen(path, classes) for path in paths), item

    report = {
        "result": "PASS",
        "mode": "R1A_BOUNDARY_CORRECTION_FINAL_FAIL_CLOSED_VERIFIER",
        "r0_base": args.r0_base,
        "historical_base": args.historical_base,
        "mutation_base": args.mutation_base,
        "corrected_census": {
            "occurrences": 815,
            "sources": 92,
            "frozen_source_occurrences": 16,
            "literal_git_grep_exact_agreement": True,
        },
        "historical_artifacts_unchanged": historical,
        "authorized_pointer_corrections": pointer_results,
        "intentional_colocated_reference": "PASS",
        "retained_target_omissions": 8,
        "moved_files_still_eligible": len(eligible),
        "moved_payloads": moved_results,
        "frozen_packages": frozen_results,
        "stale_non_frozen_pointers": 0,
        "pointer_census_rows": len(pointer_rows),
        "dirty_rows_metadata_only": len(current_dirty),
        "test_baseline": test,
        "catchproof": {
            "file_md_period_detected": "PASS" if occurrences("See file.md.", "file.md") else "FAIL",
            "file_md_parenthesis_detected": "PASS" if occurrences("See file.md)", "file.md") else "FAIL",
            "file_md_bak_rejected": "PASS" if not occurrences("See file.md.bak", "file.md") else "FAIL",
        },
    }
    assert set(report["catchproof"].values()) == {"PASS"}
    args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
