#!/usr/bin/env python3
"""Freeze the preregistered inverse-stability source universe."""

from __future__ import annotations

import csv
import hashlib
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = Path(__file__).resolve().parent
BASE = "46c763770f3f71376a0e57338c276ed3981ce36b"
ROOTS = (
    "udt_f01_lambda_schur_check_2026-08-01/",
    "udt_p4_stability_slice_2026-07-30/",
    "udt_p4_boundary_action_gate_2026-07-30/",
    "udt_stability_derivation_closure_sweep_2026-08-01/",
    "udt_stability_action_boundary_bridge_audit_2026-08-01/",
)
FILES = {
    "CURRENT_SCIENTIFIC_PREMISES.md",
    "CURRENT_SCIENTIFIC_PREMISES.tsv",
    "PONDER_MATH_ELEGANCE_2026-07-31.md",
}


def git(*args: str, binary: bool = False):
    proc = subprocess.run(["git", *args], cwd=ROOT, check=True, capture_output=True)
    return proc.stdout if binary else proc.stdout.decode("utf-8")


def main() -> None:
    raw = git("ls-tree", "-r", "-z", "--long", BASE, binary=True)
    rows = []
    for token in raw.split(b"\0"):
        if not token:
            continue
        meta, raw_path = token.split(b"\t", 1)
        _mode, kind, blob, size = meta.decode().split()
        path = raw_path.decode("utf-8")
        if path not in FILES and not any(path.startswith(root) for root in ROOTS):
            continue
        if kind != "blob":
            raise RuntimeError(path)
        data = git("cat-file", "blob", blob, binary=True)
        if len(data) != int(size):
            raise RuntimeError(f"size mismatch: {path}")
        rows.append([path, blob, size, hashlib.sha256(data).hexdigest()])
    rows.sort(key=lambda row: row[0])
    with (OUT / "SOURCE_INVENTORY.tsv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
        writer.writerow(["path", "git_blob", "bytes", "sha256"])
        writer.writerows(rows)
    (OUT / "SOURCE_PATHS.txt").write_text("".join(f"{row[0]}\n" for row in rows), encoding="utf-8")
    (OUT / "SOURCE_MANIFEST.sha256").write_text(
        "".join(f"{row[3]}  {row[0]}\n" for row in rows), encoding="utf-8"
    )
    print(f"source_count={len(rows)}")


if __name__ == "__main__":
    main()

