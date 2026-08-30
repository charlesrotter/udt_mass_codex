#!/usr/bin/env python3
"""Aggregate no-write verifier for the G299 package."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent
LANDING = (
    "ACTIVE_PREMISES_REQUIRE_COMPLETE_CARRY_BUT_DO_NOT_TYPE_THE_KERNEL_DOMAIN"
    "__ARCHITECTURE_REMAINS_OPEN"
)


def main() -> None:
    for line in (HERE / "SOURCE_MANIFEST.tsv").read_text().splitlines()[1:]:
        expected, relative = line.split("\t")
        actual = hashlib.sha256((ROOT / relative).read_bytes()).hexdigest()
        assert actual == expected, relative

    production = json.loads((HERE / "DERIVATION_RESULT.json").read_text())
    independent = json.loads((HERE / "INDEPENDENT_VERIFICATION.json").read_text())
    catches = json.loads((HERE / "CATCH_PROOF_RESULT.json").read_text())
    assert production["status"] == independent["status"] == catches["status"] == "PASS"
    assert production["landing"] == LANDING
    assert production["cases"] >= 10_000
    assert independent["cases"] >= 20_000
    assert production["right_carry_inputs_equal"]
    assert production["right_carry_outputs_different"]
    assert independent["active_screen_planes_distinct"]
    assert independent["registered_W1_clock_entry_shared"]
    assert catches["hostile_catches"] >= 7

    exact = (HERE / "EXACT_DERIVATION.md").read_text()
    lay = (HERE / "LAY_REPORT.md").read_text()
    ledger = (HERE / "STATUS_LEDGER.tsv").read_text()
    assert LANDING in exact.replace("\n", "")
    assert "architecture is compatible with UDT, not yet derived as the unique kernel domain" in lay
    assert "unique_direct_transfer_to_G2\tNOT_DERIVED" in ledger
    assert "compatible_query_factorization\tCOMPATIBLE_NOT_ACTIVE_PREMISE_OWNED" in ledger
    assert (
        "package_grade\tEXTERNALLY_REVIEWED_REPAIRS_CLOSED"
        in ledger
    )

    print(json.dumps({
        "status": "PASS",
        "source_hashes": production["source_hashes"],
        "production_cases": production["cases"],
        "production_assertions": production["assertions"],
        "independent_cases": independent["cases"],
        "independent_assertions": independent["assertions"],
        "hostile_catches": catches["hostile_catches"],
        "grade": "EXTERNALLY_REVIEWED_REPAIRS_CLOSED",
    }, indent=2))


if __name__ == "__main__":
    main()
