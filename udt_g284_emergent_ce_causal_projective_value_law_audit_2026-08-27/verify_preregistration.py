#!/usr/bin/env python3
"""Fail-closed preregistration verifier for G284."""

from __future__ import annotations

import csv
import hashlib
from pathlib import Path


PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parent


def rows(name: str) -> list[dict[str, str]]:
    with (PACKAGE / name).open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream, delimiter="\t"))


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def main() -> None:
    scope = rows("SOURCE_SCOPE.tsv")
    manifest = rows("SOURCE_MANIFEST.tsv")
    premises = rows("PREMISE_LEDGER.tsv")
    scope_paths = [row["path"] for row in scope]
    manifest_by_path = {row["path"]: row for row in manifest}
    checks = {
        "source_count_15": len(scope) == len(manifest) == 15,
        "source_paths_unique": len(set(scope_paths)) == len(scope_paths),
        "scope_manifest_exact": set(scope_paths) == set(manifest_by_path),
        "hashes_and_sizes_exact": all(
            (ROOT / path).is_file()
            and sha256(ROOT / path) == manifest_by_path[path]["sha256"]
            and str((ROOT / path).stat().st_size) == manifest_by_path[path]["bytes"]
            for path in scope_paths
        ),
        "premise_count_16": len(premises) == 16,
        "premise_ids_exact": [row["id"] for row in premises]
        == [f"P{index:02d}" for index in range(1, 17)],
        "candidate_landings_frozen": all(
            token in (PACKAGE / "PREREGISTRATION.md").read_text(encoding="utf-8")
            for token in (
                "EMERGENT_CE_CAUSAL_PROJECTIVE_CLOSURE_SELECTS_TIDAL_VALUES",
                "EMERGENT_CE_CAUSAL_PROJECTIVE_CLOSURE_RESTRICTS_BUT_DOES_NOT_SELECT_TIDAL_VALUES",
                "EMERGENT_CE_CAUSAL_PROJECTIVE_NETWORK_RECONSTRUCTS_BUT_DOES_NOT_SELECT_TIDAL_HISTORY",
                "CANDIDATE_INCONSISTENT_WITH_THE_FIXED_COMPLETE_METRIC_WITNESS",
            )
        ),
        "scope_exclusions_explicit": all(
            token in (PACKAGE / "PREREGISTRATION.md").read_text(encoding="utf-8")
            for token in (
                "observations",
                "fitted targets",
                "field equation",
                "X_max",
                "canonize",
            )
        ),
    }
    if not all(checks.values()):
        raise AssertionError({name: value for name, value in checks.items() if not value})
    print(f"PASS: G284 preregistration; sources={len(scope)} premises={len(premises)}")


if __name__ == "__main__":
    main()
