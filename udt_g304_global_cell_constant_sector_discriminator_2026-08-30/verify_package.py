#!/usr/bin/env python3
"""Mechanical package verifier for the bounded G304 result."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
LAYOUT_ROOT = HERE.parent
LANDING = (
    "FOUNDED_RELATION_LAYERS_NONSELECTIVE"
    "__WORKING_FINITE_CEILING_CONDITIONALLY_SELECTS_POSITIVE_CONSTANT_IN_PRIMARY_STATIC_SMOOTH_CENTER_BRANCH"
    "__X_EMERGES__FULL_WRL_ARCHITECTURE_INCOMPATIBLE"
)


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def resolve_frozen_source(relative_path: str) -> Path:
    candidates = [
        LAYOUT_ROOT / relative_path,
        LAYOUT_ROOT / "frozen_sources" / relative_path,
    ]
    matches = [path for path in candidates if path.is_file()]
    assert len(matches) == 1, {
        "relative_path": relative_path,
        "resolved_matches": [str(path) for path in matches],
        "candidate_layouts": [str(path) for path in candidates],
    }
    return matches[0]


def main() -> None:
    required = {
        "MAP.md",
        "PREREGISTRATION.md",
        "PREREGISTRATION_ANCESTRY.md",
        "PREMISE_LEDGER.tsv",
        "STATUS_LEDGER.tsv",
        "SOURCE_MANIFEST.tsv",
        "GLOBAL_PREMISE_AUDIT.tsv",
        "derive_global_cell_discriminator.py",
        "verify_global_cell_discriminator_independent.py",
        "run_catch_proofs.py",
        "DERIVATION_RESULT.json",
        "DOMAIN_CLASSIFICATION.tsv",
        "INDEPENDENT_VERIFICATION.json",
        "CATCH_PROOF_RESULT.json",
        "EXACT_DERIVATION.md",
        "LAY_REPORT.md",
        "AUDIT_REPORT.md",
        "EVIDENCE_GATES.md",
        "COMMANDS.md",
        "RUN_RECORD.md",
        "EXTERNAL_REVIEW_REQUEST.md",
        "EXTERNAL_REVIEW_RESPONSE.md",
        "EXTERNAL_REVIEW_TRANSMISSION.md",
        "REPAIR_PREREGISTRATION.md",
        "REPAIR_FOLLOWUP_REQUEST.md",
        "EXTERNAL_REPAIR_FOLLOWUP_RESPONSE.md",
        "EXTERNAL_REPAIR_FOLLOWUP_TRANSMISSION.md",
    }
    missing = sorted(name for name in required if not (HERE / name).is_file())
    assert not missing, missing

    production = json.loads((HERE / "DERIVATION_RESULT.json").read_text())
    independent = json.loads((HERE / "INDEPENDENT_VERIFICATION.json").read_text())
    catches = json.loads((HERE / "CATCH_PROOF_RESULT.json").read_text())
    assert production["schema"] == "UDT_G304_GLOBAL_CELL_CONSTANT_SECTOR_DISCRIMINATOR_V1"
    assert production["landing"] == LANDING
    assert production["assertions"] == 65
    assert production["direct_geometry"]["smooth_center"] == "b=0"
    assert production["center_regular_sign_census"]["R0_positive"]["finite_outer_causal_ceiling"] is True
    assert production["center_regular_sign_census"]["R0_zero"]["finite_outer_causal_ceiling"] is False
    assert production["center_regular_sign_census"]["R0_negative"]["finite_outer_causal_ceiling"] is False
    assert production["working_G17"]["grade"] == "WORKING"
    assert "R0 magnitude" in production["working_G17"]["does_not_fix"]
    assert production["WRL"]["tracefree_ODE_residual"] == "2r/X"
    assert independent["status"] == "PASS" and independent["assertions"] == 55
    assert independent["landing_matched"] is True
    assert catches["status"] == "PASS" and catches["caught"] == 10
    assert all(item["caught"] for item in catches["mutations"])

    with (HERE / "DOMAIN_CLASSIFICATION.tsv").open(newline="") as handle:
        domains = list(csv.DictReader(handle, delimiter="\t"))
    assert len(domains) == 8
    assert {row["R0_sign"] for row in domains} == {"positive", "zero", "negative"}
    assert all(row["outer_causal_ceiling"] in {"yes", "no", "no_outer_ceiling", "degenerate_not_simple"} for row in domains)

    with (HERE / "SOURCE_MANIFEST.tsv").open(newline="") as handle:
        sources = list(csv.DictReader(handle, delimiter="\t"))
    assert len(sources) == 14
    for row in sources:
        source = resolve_frozen_source(row["path"])
        assert digest(source) == row["sha256"], row["path"]

    exact = (HERE / "EXACT_DERIVATION.md").read_text()
    lay = (HERE / "LAY_REPORT.md").read_text()
    audit = (HERE / "AUDIT_REPORT.md").read_text()
    evidence = (HERE / "EVIDENCE_GATES.md").read_text()
    status = (HERE / "STATUS_LEDGER.tsv").read_text()
    for document in (exact, audit):
        assert LANDING in document.replace("\n", "")
    for document in (exact, lay, audit):
        lowered = document.lower()
        assert "not" in lowered and "history" in lowered and "mass" in lowered
    assert "all-frame" in exact and "all-frame" in lay
    assert "magnitude" in exact and "magnitude" in lay
    assert "WORKING" in audit and "WORKING" in status
    assert "FULL_WRL_ARCHITECTURE_INCOMPATIBLE" in audit
    assert "external adversarial review | PASS WITH CAVEATS, REPAIRS VERIFIED" in evidence
    assert "REPAIRS_VERIFIED" in (HERE / "EXTERNAL_REPAIR_FOLLOWUP_RESPONSE.md").read_text()
    assert "01a053cc-851a-70e2-a5b0-50c781d5050b" in (
        HERE / "EXTERNAL_REPAIR_FOLLOWUP_TRANSMISSION.md"
    ).read_text()
    assert "d35e31c3" in (HERE / "PREREGISTRATION_ANCESTRY.md").read_text()

    result = {
        "schema": "UDT_G304_PACKAGE_VERIFICATION_V1",
        "status": "PASS",
        "landing": LANDING,
        "required_files": len(required),
        "source_hashes_verified": len(sources),
        "domain_rows": len(domains),
        "production_assertions": production["assertions"],
        "independent_assertions": independent["assertions"],
        "hostile_mutations_caught": catches["caught"],
        "external_review": "VERIFIED_WITH_CAVEATS_REPAIRS_VERIFIED",
    }
    (HERE / "PACKAGE_VERIFICATION_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("G304 package verification PASS")
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
