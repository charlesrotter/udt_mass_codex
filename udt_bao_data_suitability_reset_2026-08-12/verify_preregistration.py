#!/usr/bin/env python3
from pathlib import Path
import csv

ROOT = Path(__file__).resolve().parent


def rows(name):
    with (ROOT / name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def main():
    gates = rows("SUITABILITY_GATES.tsv")
    candidates = rows("CANDIDATE_LEDGER.tsv")
    statuses = rows("STATUS_LEDGER.tsv")
    sources = rows("SOURCE_MANIFEST.tsv")

    assert len(gates) == 10
    assert len({r["gate"] for r in gates}) == len(gates)
    assert len(candidates) == 6
    assert len({r["candidate"] for r in candidates}) == len(candidates)
    assert any(r["candidate"] == "OFFICIAL_DR2_GAUSSIAN" and r["blind_numeric_audit"] == "YES"
               for r in candidates)
    assert any(r["item"] == "joint_SNe_BAO_CMB_fit" and r["status"] == "FORBIDDEN_IN_THIS_PACKAGE"
               for r in statuses)
    assert any(r["item"] == "X_max_estimate" and r["status"] == "FORBIDDEN_IN_THIS_PACKAGE"
               for r in statuses)
    assert sum(r["scope"] == "local" for r in sources) == 7
    assert sum(r["scope"] == "external" for r in sources) == 6

    text = (ROOT / "PREREGISTRATION.md").read_text(encoding="utf-8")
    for landing in (
        "OFFICIAL_PRODUCT_READY_FOR_TYPED_UDT_LIKELIHOOD",
        "OFFICIAL_PRODUCT_READY_ONLY_WITH_DECLARED_FIDUCIAL_OR_RULER_NUISANCE",
        "RAW_PRODUCTS_REQUIRE_NEW_PREREGISTERED_REDUCTION",
        "NO_CURRENT_BAO_PRODUCT_IS_CALIBRATION_READY",
        "TYPE_FAILURE",
    ):
        assert landing in text
    print("BAO preregistration: 10 gates, 6 candidates, 5 landings; PASS")


if __name__ == "__main__":
    main()
