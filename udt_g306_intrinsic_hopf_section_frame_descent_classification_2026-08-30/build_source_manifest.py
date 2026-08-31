#!/usr/bin/env python3
"""Build the exact G306 source manifest from the frozen source scope."""

from __future__ import annotations

import csv
import hashlib
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
SCOPE = HERE / "SOURCE_SCOPE.tsv"
OUT = HERE / "SOURCE_MANIFEST.tsv"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> None:
    rows = []
    with SCOPE.open(encoding="utf-8", newline="") as fh:
        for row in csv.DictReader(fh, delimiter="\t"):
            rel = Path(row["path"])
            assert not any(token in str(rel) for token in (
                "8_25",
                "udt_native_onshell_timelive_reset_owner_audit",
                "udt_pair_regime_flow_reciprocal_orchestra_amplification",
                "udt_sne_xmax_G88_am_radial_compatibility_atlas",
                "udt_kernel_plane_global_curvature_holonomy_atlas",
            ))
            path = ROOT / rel
            assert path.is_file(), rel
            rows.append((str(rel), sha256(path), row["role"]))
    with OUT.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.writer(fh, delimiter="\t", lineterminator="\n")
        writer.writerow(("path", "sha256", "role"))
        writer.writerows(rows)
    print(f"PASS: {len(rows)} source hashes")


if __name__ == "__main__":
    main()

