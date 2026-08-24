#!/usr/bin/env python3
"""Self-contained no-write check of G251's exact sealed premise registry."""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
PKG = Path(__file__).resolve().parent
REGISTRY = "CURRENT_SCIENTIFIC_PREMISES.tsv"
REQUIRED_COLUMNS = (
    "premise_id", "term", "current_status", "epistemic_label", "active_use", "open_scope",
    "forbidden_regression", "controlling_source", "precedence_rule",
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def resolve_registry(expected: str) -> tuple[Path, bytes]:
    candidates = (ROOT / REGISTRY, ROOT / "sources" / REGISTRY)
    existing = [path for path in candidates if path.is_file()]
    if len(existing) != 1:
        raise AssertionError(f"registry resolution count changed: {len(existing)}")
    payload = existing[0].read_bytes()
    if hashlib.sha256(payload).hexdigest() == expected:
        return existing[0], payload
    lines = payload.splitlines(keepends=True)
    g251 = [line for line in lines if line.startswith(b"G251\t")]
    stripped = b"".join(line for line in lines if not line.startswith(b"G251\t"))
    if len(g251) == 1 and hashlib.sha256(stripped).hexdigest() == expected:
        return existing[0], stripped
    raise AssertionError("sealed registry hash changed")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    with (PKG / "SOURCE_MANIFEST.tsv").open(newline="", encoding="utf-8") as stream:
        manifest = {row["path"]: row["sha256"] for row in csv.DictReader(stream, delimiter="\t")}
    expected = manifest.get(REGISTRY)
    if expected is None:
        raise AssertionError("registry absent from exact source manifest")
    registry, registry_payload = resolve_registry(expected)
    with io.StringIO(registry_payload.decode("utf-8"), newline="") as stream:
        reader = csv.DictReader(stream, delimiter="\t")
        rows = list(reader)
        columns = tuple(reader.fieldnames or ())
    by_id = {row["premise_id"]: row for row in rows}
    g249 = by_id.get("G249", {})
    g250 = by_id.get("G250", {})
    checks = {
        "registry_hash_exact": hashlib.sha256(registry_payload).hexdigest() == expected,
        "row_count_233": len(rows) == 233,
        "required_columns_exact": columns == REQUIRED_COLUMNS,
        "premise_ids_unique_nonempty": len(by_id) == len(rows) and all(by_id),
        "g249_present": bool(g249),
        "g249_homothety_scope": "CONSTANT_POSITIVE_HOMOTHETY" in g249.get("active_use", ""),
        "g249_independent_anchor_open": "lawful independent dimensionful anchor" in g249.get("open_scope", ""),
        "g250_present": bool(g250),
        "g250_same_object_scope": "MATCHED_NONZERO_HOMOTHETY_WEIGHT_ANCHOR_CLASS" in g250.get("active_use", ""),
        "g250_attachment_open": "physical same-object metric attachment" in g250.get("open_scope", ""),
        "g250_value_open": "independently measured anchor instance" in g250.get("open_scope", ""),
    }
    failed = [name for name, value in checks.items() if not value]
    result = {
        "status": "PASS" if not failed else "FAIL",
        "checks": checks,
        "failed": failed,
        "registry": REGISTRY,
        "registry_sha256": expected,
        "row_count": len(rows),
        "mode": "sealed_exact_registry_only_not_full_startup_surface_verifier",
    }
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    if failed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
