#!/usr/bin/env python3
"""Read-only exact replay of the original external-review intake."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
PACKAGE = HERE.name
PROTECTED = "udt_kernel_plane_global_curvature_holonomy_atlas_2026-08-02"
STOPPED = "udt_native_onshell_timelive_reset_owner_audit_2026-08-10"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("intake", type=Path)
    args = parser.parse_args()
    intake = args.intake.resolve()
    with (HERE / "REVIEWED_INTAKE_SHA256SUMS.tsv").open() as f:
        rows = list(csv.DictReader(f, delimiter="\t"))
    actual = sorted(p.relative_to(intake).as_posix() for p in intake.rglob("*") if p.is_file())
    assert len(rows) == len({r['path'] for r in rows}) == 50
    assert actual == sorted(r["path"] for r in rows)
    for row in rows:
        p = intake / row["path"]
        assert p.stat().st_size == int(row["size"]), row["path"]
        assert hashlib.sha256(p.read_bytes()).hexdigest() == row["sha256"], row["path"]
        assert PROTECTED not in row["path"] and STOPPED not in row["path"]
    package = sum(r["path"].startswith(PACKAGE + "/") for r in rows)
    sources = sum(r["path"].startswith("sources/") for r in rows)
    assert package == 28 and sources == 22
    print(json.dumps({"status":"PASS","files":50,"package_files":28,"source_files":22,"protected":False,"stopped":False}, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
