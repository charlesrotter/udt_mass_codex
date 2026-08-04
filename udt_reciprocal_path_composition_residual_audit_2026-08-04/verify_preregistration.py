#!/usr/bin/env python3
"""Fail-closed verification of the preregistered audit universe."""

from __future__ import annotations

import csv
import hashlib
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def rows(name: str) -> list[dict[str, str]]:
    with (HERE / name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


premises = rows("PREMISE_LEDGER.tsv")
candidates = rows("RESIDUAL_CANDIDATE_UNIVERSE.tsv")
failures = rows("FALSIFICATION_CONTRACT.tsv")
sources = rows("SOURCE_MANIFEST.tsv")

assert len(premises) == 16 and len({row["premise_id"] for row in premises}) == 16
assert len(candidates) == 12 and len({row["candidate_id"] for row in candidates}) == 12
assert len(failures) == 22 and len({row["failure_id"] for row in failures}) == 22
assert len(sources) == 32 and len({row["path"] for row in sources}) == 32
source_paths = [line for line in (HERE / "SOURCE_PATHS.txt").read_text(encoding="utf-8").splitlines() if line]
assert [row["path"] for row in sources] == source_paths
for row in sources:
    path = ROOT / row["path"]
    assert path.is_file()
    assert digest(path) == row["sha256"]
    assert str(path.stat().st_size) == row["bytes"]

text = (HERE / "PREREGISTRATION.md").read_text(encoding="utf-8")
for required in (
    "termination test",
    "SOURCE_DERIVES_NONTRIVIAL_METRIC_RESIDUAL",
    "CONDITIONAL_RESIDUAL_ONLY",
    "COMPOSITION_IDENTITY_NONSELECTING",
    "MIXED_OR_OPEN",
    "No outcome is preferred",
):
    assert required in text

print(
    "PASS "
    f"premises={len(premises)} candidates={len(candidates)} failures={len(failures)} "
    f"sources={len(sources)} source_manifest_sha256={digest(HERE / 'SOURCE_MANIFEST.sha256')}"
)
