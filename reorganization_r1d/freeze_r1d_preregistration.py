#!/usr/bin/env python3
"""Freeze R1D's exact pre-mutation inputs and fixed-history records."""

from __future__ import annotations

import csv
import hashlib
import json
import subprocess
from pathlib import Path

BASE = "b3c50109df90658378d157c65fc723b1265c48c8"
SOURCE = "simple_metric_S8_action_provenance_note.md"
DESTINATION = "research/macro/simple_metric_S8_action_provenance_note.md"
EXPECTED_BLOB = "94b494cd326a27aacbbbedbd9aa91febb8acf471"
EXPECTED_SHA256 = "a3fae1798f64c4bdc3a79692a618281c407d162309073a02dc72d89eb9c554f9"
EXPECTED_LINE_10 = "| **Re-run** | light CAS in `simple_metric_solution_space_ZOOM.md` session |"
PREFIXES = ("reorganization_r0/", "reorganization_r1a/", "reorganization_r1b/", "reorganization_r1c/")
REGISTRY_PREFIX = "research/_registry/"


def run(repo: Path, command: list[str], binary: bool = False) -> bytes | str:
    result = subprocess.run(command, cwd=repo, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                            text=not binary, check=False)
    if result.returncode:
        err = result.stderr if not binary else result.stderr.decode("utf-8", "replace")
        raise AssertionError(f"command failed: {' '.join(command)}\n{err}")
    return result.stdout


def blob(repo: Path, path: str) -> bytes:
    return bytes(run(repo, ["git", "show", f"{BASE}:{path}"], binary=True))


def main() -> int:
    repo = Path(__file__).resolve().parents[1]
    out = Path(__file__).resolve().parent
    assert str(run(repo, ["git", "rev-parse", "HEAD"])).strip() == BASE
    paths = [p for p in str(run(repo, ["git", "ls-tree", "-r", "--name-only", BASE])).splitlines()
             if p.startswith(PREFIXES) or p.startswith(REGISTRY_PREFIX)]
    rows = []
    for path in sorted(paths):
        payload = blob(repo, path)
        oid = str(run(repo, ["git", "rev-parse", f"{BASE}:{path}"])).strip()
        rows.append((path, oid, hashlib.sha256(payload).hexdigest(), len(payload)))
    fixed = out / "FIXED_HISTORY_SHA256.tsv"
    with fixed.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
        writer.writerow(("path", "git_blob_oid", "sha256", "size_bytes"))
        writer.writerows(rows)
    source = blob(repo, SOURCE)
    assert str(run(repo, ["git", "rev-parse", f"{BASE}:{SOURCE}"])).strip() == EXPECTED_BLOB
    assert hashlib.sha256(source).hexdigest() == EXPECTED_SHA256
    assert source.decode("utf-8").splitlines()[9] == EXPECTED_LINE_10
    inventory = repo / "reorganization_r1c/FROZEN_ROOT_INVENTORY.tsv"
    with inventory.open(encoding="utf-8", newline="") as handle:
        root_count = sum(1 for _ in csv.DictReader(handle, delimiter="\t"))
    assert root_count == 1114
    dirty = repo / "reorganization_r1b/postmove_forensic_census/DIRTY_WORKSTATION_INVENTORY.tsv"
    payload = {
        "base": BASE,
        "source": SOURCE,
        "destination": DESTINATION,
        "source_blob": EXPECTED_BLOB,
        "source_sha256": EXPECTED_SHA256,
        "source_line_10": EXPECTED_LINE_10,
        "source_line_10_classification": "REPOSITORY_ROOT_INFORMATIONAL_TOKEN_NOT_MARKDOWN_LINK_OR_RUNTIME_OPEN",
        "forbidden_substitution": "../../simple_metric_solution_space_ZOOM.md",
        "fixed_history_rows": len(rows),
        "fixed_history_tsv_sha256": hashlib.sha256(fixed.read_bytes()).hexdigest(),
        "fixed_root_inventory_rows": root_count,
        "fixed_root_inventory_sha256": hashlib.sha256(inventory.read_bytes()).hexdigest(),
        "preimage_research_readme_sha256": hashlib.sha256((repo / "research/README.md").read_bytes()).hexdigest(),
        "preimage_macro_inventory_sha256": hashlib.sha256((repo / "research/macro/ROOT_INVENTORY.tsv").read_bytes()).hexdigest(),
        "dirty_inventory_sha256": hashlib.sha256(dirty.read_bytes()).hexdigest(),
        "dirty_path_count": 54,
        "status_contract": {"ROOT_RETAINED": 1113, "MIGRATED_R1D": 1},
        "generated_records_excluded_from_fixed_base_universe": True,
    }
    prereg = out / "PREREGISTERED_INPUTS.json"
    prereg.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    result = {"result": "PASS", **payload}
    (out / "PREREG_VERIFY_RESULT.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
