#!/usr/bin/env python3
"""Verify the fixed G82 package and its scoped authority."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream, delimiter="\t"))


def main() -> None:
    source_rows = rows(HERE / "SOURCE_MANIFEST.tsv")
    assert len(source_rows) == 6
    for row in source_rows:
        assert digest(ROOT / row["path"]) == row["sha256"]
    controls = rows(HERE / "CONTROL_UNIVERSE.tsv")
    assert len(controls) == 1 and controls[0]["control_id"] == "C1_FULL_ANGULAR"
    assert controls[0]["integrator"] == "Radau"
    result = json.loads((HERE / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    independent = json.loads((HERE / "INDEPENDENT_VERIFICATION.json").read_text(encoding="utf-8"))
    catches = json.loads((HERE / "CATCH_PROOF_RESULTS.json").read_text(encoding="utf-8"))
    assert result["status"] == independent["status"] == catches["status"] == "PASS"
    assert catches["count"] == 15 and all(catches["catches"].values())
    assert result["method"]["integrator"] == "Radau"
    assert result["maximum_conclusion_if_pass"] == "G81_C1_SCREEN_COVARIANCE_SURVIVES_ONE_FIXED_NON_DOP853_RADAU_REPLAY"
    assert result["scientific_maximum_unchanged"] == "DERIVED_CONDITIONAL_SCREEN_COVARIANCE_ON_TWO_FIXED_CONTROLS"
    assert digest(HERE / "DERIVATION_RESULT.json") == digest(HERE / "DERIVATION_STDOUT.txt")
    payload = {
        "schema": "udt-cmb-g82-package-verification-v1",
        "status": "PASS",
        "source_rows": len(source_rows),
        "controls": len(controls),
        "catch_proofs": catches["count"],
        "radau_vs_dop853_max_relative": independent["radau_vs_dop853_max_relative"],
        "scientific_maximum_unchanged": True,
    }
    rendered = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    (HERE / "PACKAGE_VERIFICATION.json").write_text(rendered, encoding="utf-8")
    print(rendered, end="")


if __name__ == "__main__":
    main()
