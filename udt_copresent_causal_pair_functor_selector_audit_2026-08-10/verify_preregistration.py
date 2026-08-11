#!/usr/bin/env python3
"""Fail closed on the preregistered causal selector frame and source intake."""

from __future__ import annotations

import csv
import hashlib
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def rows(name: str) -> list[dict[str, str]]:
    with (HERE / name).open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream, delimiter="\t"))


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    premises = rows("PREMISE_LEDGER.tsv")
    axes = rows("CAUSAL_AXES.tsv")
    catches = rows("FALSIFICATION_CONTRACT.tsv")
    sources = rows("SOURCE_MANIFEST.tsv")
    assert len(premises) == 12 and len({row["premise_id"] for row in premises}) == 12
    assert len(axes) == 13 and len({row["axis_id"] for row in axes}) == 13
    assert len(catches) == 15 and len({row["catch_id"] for row in catches}) == 15
    assert len(sources) == 14 and len({row["path"] for row in sources}) == 14
    for row in sources:
        path = ROOT / row["path"]
        assert path.is_file() and digest(path) == row["sha256"], row["path"]
        assert "udt_kernel_plane_global_curvature_holonomy_atlas_2026-08-02" not in row["path"]
        assert "udt_native_onshell_timelive_reset_owner_audit_2026-08-10" not in row["path"]
    prereg = (HERE / "PREREGISTRATION.md").read_text(encoding="utf-8")
    for token in (
        "PAIR_CONE_DERIVES_PHI_CEFF_JOIN_BUT_CAUSAL_TRANSITIONS_REMAIN_NONUNIQUE",
        "arbitrary time",
        "beta=0",
        "No GR field equations",
        "No on-shell evolution",
    ):
        assert token in prereg, token
    print("PASS: 12 premises, 13 causal axes, 15 falsification catches, 14 frozen sources")


if __name__ == "__main__":
    main()
