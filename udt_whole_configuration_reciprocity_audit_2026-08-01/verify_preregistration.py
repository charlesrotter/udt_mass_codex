#!/usr/bin/env python3
"""Fail closed on the whole-configuration Reciprocity preregistration."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path


PKG = Path(__file__).resolve().parent
ROOT = PKG.parent


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def tsv(name: str) -> list[dict[str, str]]:
    with (PKG / name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


snap = json.loads((PKG / "PREREG_SNAPSHOT.json").read_text(encoding="utf-8"))
inv = tsv("SOURCE_INVENTORY.tsv")
premises = tsv("PREMISE_LEDGER.tsv")
interpretations = tsv("INTERPRETATION_CANDIDATES.tsv")
scopes = tsv("SOURCE_PACKAGE_SCOPE.tsv")
assert snap["base"] == "9fe5202e86627aa47a5200ea776dcb468a6531f6"
assert len(inv) == snap["source_union"] == len({row["path"] for row in inv})
assert [row["path"] for row in inv] == sorted(row["path"] for row in inv)
assert all((ROOT / row["path"]).is_file() and sha256(ROOT / row["path"]) == row["sha256"] for row in inv)
assert len(premises) == snap["premises"] == 15
assert len(interpretations) == snap["interpretations"] == 10
assert len(scopes) == snap["package_scopes"] == 14
assert {row["candidate_id"] for row in interpretations} == {f"I{i:02d}" for i in range(1, 11)}
text = (PKG / "PREREGISTRATION.md").read_text(encoding="utf-8")
for token in ["observer-frame Reciprocity", "internal dual Reciprocity", "conditional `Xmax` reciprocity", "orbit-versus-fixed-point", "equivariance-versus-selection", "RECIPROCITY_DERIVES_EQUIVARIANT_QUOTIENT_ONLY"]:
    assert token in text
assert "Pre-July-1 material" in text and "cannot provide\naffirmative UDT physics" in text
print(f"PASS Reciprocity preregistration: sources={len(inv)} premises={len(premises)} interpretations={len(interpretations)}")
