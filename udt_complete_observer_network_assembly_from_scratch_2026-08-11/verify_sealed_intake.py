#!/usr/bin/env python3
"""Verify the exact read-only G62 review intake and its source boundary."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
PROTECTED = "udt_kernel_plane_global_curvature_holonomy_atlas_2026-08-02"
STOPPED = "udt_native_onshell_timelive_reset_owner_audit_2026-08-10"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("intake", type=Path)
    parser.add_argument("--write-result", action="store_true")
    args = parser.parse_args()
    intake = args.intake.resolve()
    with (HERE / "SEALED_INTAKE_SHA256SUMS.tsv").open(newline="", encoding="utf-8") as stream:
        rows = list(csv.DictReader(stream, delimiter="\t"))
    assert len(rows) == len({row["path"] for row in rows}) == 36
    actual = sorted(path.relative_to(intake).as_posix() for path in intake.rglob("*") if path.is_file())
    assert actual == sorted(row["path"] for row in rows)
    for row in rows:
        path = intake / row["path"]
        assert path.stat().st_size == int(row["size"]), row["path"]
        assert digest(path) == row["sha256"], row["path"]
        assert PROTECTED not in row["path"] and STOPPED not in row["path"]
    package = sum(row["path"].startswith(HERE.name + "/") for row in rows)
    sources = sum(row["path"].startswith("sources/") for row in rows)
    assert package == 21 and sources == 15
    result = {
        "schema": "udt-g62-sealed-intake-replay-v1",
        "status": "PASS",
        "files": len(rows),
        "package_files": package,
        "source_files": sources,
        "protected_atlas_included": False,
        "stopped_draft_included": False,
    }
    if args.write_result:
        (HERE / "SEALED_INTAKE_REPLAY_RESULT.json").write_text(
            json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
