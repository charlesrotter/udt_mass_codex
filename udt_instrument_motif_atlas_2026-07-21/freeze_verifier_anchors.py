#!/usr/bin/env python3
"""Freeze the preregistered outcome-blind configuration-ID hash anchors."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
PARENT = ROOT / "udt_structural_ensemble_metric_atlas_2026-07-21"
COUNT = 384


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(131072), b""):
            value.update(block)
    return value.hexdigest()


def main() -> None:
    with (PARENT / "RAW_SHARD_REGISTRY.tsv").open(encoding="utf-8", newline="") as handle:
        shards = list(csv.DictReader(handle, delimiter="\t"))
    identifiers = []
    for shard in shards:
        path = PARENT / shard["path"]
        if digest(path) != shard["sha256"]:
            raise AssertionError(f"shard hash {shard['path']}")
        with path.open(encoding="utf-8") as handle:
            identifiers.extend(json.loads(line)["configuration_id"] for line in handle)
    if len(identifiers) != 6144 or len(set(identifiers)) != 6144:
        raise AssertionError("configuration identity census")
    selected = sorted(identifiers, key=lambda item: (hashlib.sha256(item.encode()).hexdigest(), item))[:COUNT]
    (HERE / "VERIFIER_ANCHOR_IDS.txt").write_text("\n".join(selected) + "\n", encoding="utf-8")
    print(f"anchors={len(selected)} sha256={digest(HERE / 'VERIFIER_ANCHOR_IDS.txt')}")


if __name__ == "__main__":
    main()
