#!/usr/bin/env python3
"""Fail-closed internal verifier for the G55 admissibility atlas."""

from __future__ import annotations

import csv
import json
import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
PREREG_COMMIT = "4affd614"
PREREG_FILES = (
    "PREREGISTRATION.md", "PONDER_MAP.md", "PREMISE_LEDGER.tsv", "CANDIDATE_UNIVERSE.tsv",
    "ADMISSIBILITY_AXES.tsv", "FALSIFICATION_CONTRACT.tsv", "COMPLETENESS_MAP.md",
    "SOURCE_MANIFEST.tsv", "verify_preregistration.py",
)


def table(name: str) -> list[dict[str, str]]:
    with (HERE / name).open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream, delimiter="\t"))


def main() -> int:
    for name in PREREG_FILES:
        relative = f"{HERE.name}/{name}"
        assert subprocess.run(["git", "diff", "--quiet", PREREG_COMMIT, "--", relative], cwd=ROOT).returncode == 0, name
    derivation = json.loads((HERE / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    independent = json.loads((HERE / "INDEPENDENT_VERIFICATION_RESULT.json").read_text(encoding="utf-8"))
    catches = json.loads((HERE / "CATCH_PROOF_RESULT.json").read_text(encoding="utf-8"))
    assert derivation["status"] == "PASS"
    assert derivation["branch_count"] == 24 and derivation["measurement_cells"] == 144 and derivation["axis_cells"] == 240
    assert derivation["pattern_family_count"] == 11
    assert derivation["global_structural_restriction_owners"] == 5
    assert derivation["physical_pair_relation_owners"] == 0
    assert derivation["physical_nonisometric_arrow_owners"] == 0
    assert derivation["optional_measurement_selector_owners"] == 0
    assert derivation["physical_regime_owners"] == 0
    assert independent["status"] == "PASS" and independent["passed"] == independent["total"] == 33
    assert catches["status"] == "PASS" and catches["rejected"] == catches["total"] == 22
    assert len(table("BRANCH_ADMISSIBILITY_PROFILES.tsv")) == 24
    assert len(table("BRANCH_MEASUREMENT_MATRIX.tsv")) == 144
    assert len(table("BRANCH_AXIS_MATRIX.tsv")) == 240
    assert len(table("GEOMETRIC_PATTERN_FAMILIES.tsv")) == 11
    report = " ".join((HERE / "AUDIT_REPORT.md").read_text(encoding="utf-8").split())
    exact = " ".join((HERE / "EXACT_DERIVATION.md").read_text(encoding="utf-8").split())
    for text in (report, exact):
        assert "not yet a physical regime map" in text or "not a derived map of physical regimes" in text
        assert "None owns the complete physical calibrated observer-pair relation" in text
        assert "R17" in text and "conditionally" in text
    matrix = {(row["branch_id"], row["measurement_id"]): row for row in table("BRANCH_MEASUREMENT_MATRIX.tsv")}
    axes = {(row["branch_id"], row["axis_id"]): row for row in table("BRANCH_AXIS_MATRIX.tsv")}
    assert all(matrix[("R04", f"M{i:02d}")]["disposition"] == "INSUFFICIENT_EVIDENCE" for i in range(1, 6))
    assert all(axes[("R04", f"A{i:02d}")]["disposition"] == "INSUFFICIENT_EVIDENCE" for i in range(2, 7))
    external = (HERE / "EXTERNAL_REVIEW_RAW.md").read_text(encoding="utf-8")
    assert external.startswith("`VERIFIED_WITH_CORRECTIONS`")
    assert "R04/M01" in external and "R04/A02" in external
    print("PASS: preregistration immutable; 24 branches; 144 measurement cells; 240 axis cells; 11 apparatus patterns; five bounded global restrictions; zero physical pair, optional-selector, or regime owners; R04 aggregate correction; independent 33/33; catches 22/22; external VERIFIED_WITH_CORRECTIONS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
