#!/usr/bin/env python3
"""Read-only final verifier for the frozen stability-foundations package."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
MANIFEST = HERE / "PACKAGE_MANIFEST.sha256"


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def load_json(name: str) -> dict[str, object]:
    return json.loads((HERE / name).read_text(encoding="utf-8"))


def rows(name: str) -> list[dict[str, str]]:
    with (HERE / name).open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def main() -> int:
    checks: list[tuple[str, bool]] = []
    entries: dict[str, str] = {}
    for line in MANIFEST.read_text(encoding="utf-8").splitlines():
        sha, name = line.split("  ", 1)
        entries[name] = sha
    actual = {path.name for path in HERE.iterdir() if path.is_file() and path != MANIFEST}
    checks.append(("manifest_exact_file_set", set(entries) == actual))
    checks.append(("manifest_all_hashes", all((HERE / name).is_file() and digest(HERE / name) == sha for name, sha in entries.items())))

    primary = load_json("DERIVATION_RESULT.json")
    checks.append(("primary_pass", primary.get("pass") is True))
    counts = primary.get("counts", {})
    checks.append(("primary_counts", isinstance(counts, dict) and counts.get("checks") == 17 and counts.get("mutation_catches") == 7))
    checks.append(("primary_ceiling", primary.get("primary_outcome") == "FOUNDATIONS_PARTIAL_MINIMAL_JOIN_IDENTIFIED" and primary.get("current_operational_stability") == "CONDITIONAL_STABILITY_ONLY"))

    amendments = load_json("AMENDMENT_VERIFIER_RESULTS.json")
    checks.append(("amendments_pass", amendments.get("verdict") == "PASS" and amendments.get("passed") == amendments.get("checks") == 10))
    checks.append(("transitive_freeze_four", len(rows("TRANSITIVE_PREMISE_FREEZE.tsv")) == 4))

    cold = load_json("VERIFIER_RESULTS.json")
    checks.append(("cold_review_preserved", cold.get("verdict") == "PASS-WITH-REQUIRED-AMENDMENTS" and cold.get("scientific_ceiling_survives") is True))
    closure = load_json("FINAL_CLOSURE_VERIFIER_RESULTS.json")
    checks.append(("cold_closure_pass", closure.get("verdict") == "CLOSED-PASS" and not closure.get("failed", [])))

    gate = {row["id"]: row for row in rows("FIXED_REALIZATION_GATE.tsv")}
    checks.append(("live_gate_open", gate["G05"]["current_status"] == "OPEN" and "nonzero time-live and angular-live" in gate["G05"]["gate_object"]))
    checks.append(("pullback_not_image_intersection", "pullback/fiber-product" in gate["G09"]["gate_object"]))
    checks.append(("original_source_freeze_94", len(rows("SOURCE_INVENTORY.tsv")) == 94))
    checks.append(("premises_13", len(rows("PREMISE_LEDGER.tsv")) == 13))

    failed = [name for name, passed in checks if not passed]
    for name, passed in checks:
        print(f"{name}\t{'PASS' if passed else 'FAIL'}")
    print(f"RESULT\t{'PASS' if not failed else 'FAIL'}\t{len(checks)-len(failed)}/{len(checks)}")
    return 0 if not failed else 1


if __name__ == "__main__":
    raise SystemExit(main())
