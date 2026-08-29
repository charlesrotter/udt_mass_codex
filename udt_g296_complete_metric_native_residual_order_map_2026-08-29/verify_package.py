#!/usr/bin/env python3
"""Aggregate bounded package verifier for G296."""

from __future__ import annotations

import csv
import hashlib
import json
import subprocess
import sys
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
OUT = HERE / "PACKAGE_VERIFICATION_RESULT.json"
LANDING = (
    "COMPLETE_METRIC_IS_A_MINIMAL_FAITHFUL_PRIMITIVE_STATE"
    "__SECOND_METRIC_DERIVATIVE_ORDER_IS_THE_FIRST_LOCAL_NATURAL_NONIDENTITY_HOME"
    "__CURRENT_PREMISES_DO_NOT_PRIVILEGE_ONE_RESIDUAL_FORM"
)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    for script in (
        "derive_native_residual_order_map.py",
        "verify_native_residual_independent.py",
        "run_catch_proofs.py",
        "verify_prereg_ancestry_proof.py",
    ):
        subprocess.run([sys.executable, str(HERE / script)], cwd=ROOT, check=True,
                       stdout=subprocess.DEVNULL)

    source_rows = []
    with (HERE / "SOURCE_MANIFEST.tsv").open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle, delimiter="\t"):
            path = ROOT / row["path"]
            assert path.is_file(), row["path"]
            assert digest(path) == row["sha256"], row["path"]
            source_rows.append(row)

    prod = json.loads((HERE / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    ind = json.loads((HERE / "INDEPENDENT_VERIFICATION.json").read_text(encoding="utf-8"))
    catches = json.loads((HERE / "CATCH_PROOF_RESULT.json").read_text(encoding="utf-8"))
    ancestry = json.loads((HERE / "PREREG_ANCESTRY_PROOF.json").read_text(encoding="utf-8"))
    assert prod["all_pass"] and prod["landing"] == LANDING and prod["check_count"] == 32
    assert ind["all_pass"] and ind["assertions"] == 3080 and ind["cases"] == 128
    assert ind["imports_production"] is False and ind["reads_production_output"] is False
    assert catches["all_pass"] and catches["catch_count"] == 13
    assert ancestry["all_pass"] is True
    assert ancestry["commit"] == "f7a050f054d83583c449b9854ce9b17b7d2f2186"
    assert ancestry["implementation_or_outcome_files_in_prereg_tree"] == []
    audit = (HERE / "AUDIT_REPORT.md").read_text(encoding="utf-8")
    exact = (HERE / "EXACT_DERIVATION.md").read_text(encoding="utf-8")
    assert LANDING in audit.replace("\n", "")
    assert LANDING in exact.replace("\n", "")
    assert "G296_ACCEPT_WITH_REPAIRS" in audit
    assert "G296_REPAIRS_VERIFIED__BOUNDED_SCIENTIFIC_LANDING_RETAINED" in audit
    followup = (HERE / "EXTERNAL_REPAIR_FOLLOWUP_GPT54.md").read_text(encoding="utf-8")
    transmission = (HERE / "EXTERNAL_REPAIR_FOLLOWUP_TRANSMISSION.md").read_text(encoding="utf-8")
    assert "G296_REPAIRS_VERIFIED__BOUNDED_SCIENTIFIC_LANDING_RETAINED" in followup
    assert "No repair failures were found" in followup
    assert "0f59ecb109f28fa96d3bb6a34a20dc1bb9ac6e3e6aa1a5c447d1322aa5af65f" in transmission

    result = {
        "all_pass": True,
        "source_rows": len(source_rows),
        "production_checks": prod["check_count"],
        "independent_assertions": ind["assertions"],
        "independent_cases": ind["cases"],
        "hostile_catches": catches["catch_count"],
        "preregistration_ancestry_verified": True,
        "landing": LANDING,
        "blind_review_verdict": "G296_ACCEPT_WITH_REPAIRS",
        "repair_followup_verdict": "G296_REPAIRS_VERIFIED__BOUNDED_SCIENTIFIC_LANDING_RETAINED",
        "repair_followup_outstanding": False,
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
