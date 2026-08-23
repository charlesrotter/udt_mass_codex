#!/usr/bin/env python3
"""Certify that G237 review repairs changed no frozen scientific result."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


PACKAGE = Path(__file__).resolve().parent
OUT = PACKAGE / "REPAIR_CERTIFICATION.json"
OLD_LABEL = "CHOSE_ZERO_BLOCK"
NEW_LABEL = "CHOSE_ZERO_AFTER_EXACT_CID_DEOVERLAP__UNKNOWN_SHARED_SYSTEMATICS_OPEN"
FROZEN = {
    "JOINT_STATE_RESULT.json": "0407fb233158beb06fba771d78e1e2ec66e1d857858b4a094e78d294d417c951",
    "FROZEN_PRIMARY_K12_STATE.json": "88d3006a646f2be105a3fb15f2c4c694732b884da97f8fdeefc39323e6bbc8cf",
    "JOINT_STATE.tsv": "548219b37459a12c590a43568120e519fc58fa79b322c2059a7b06ba8b88c4b1",
}
OLD_INDEPENDENT_HASH = "725d8e57e4ab9fc927a3cc7a3a0ee49bebb8da372bf137d58acffde9accd7239"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    checks = {f"frozen_{name}": digest(PACKAGE / name) == expected for name, expected in FROZEN.items()}
    independent = json.loads((PACKAGE / "INDEPENDENT_RAW_GLS.json").read_text())
    checks["expanded_covariance_label"] = independent.get("cross_release_covariance") == NEW_LABEL
    reconstructed = dict(independent)
    reconstructed["cross_release_covariance"] = OLD_LABEL
    reconstructed_bytes = (json.dumps(reconstructed, indent=2, sort_keys=True) + "\n").encode()
    checks["independent_only_label_changed"] = (
        hashlib.sha256(reconstructed_bytes).hexdigest() == OLD_INDEPENDENT_HASH
    )
    chronology = json.loads((PACKAGE / "CHRONOLOGY_BUNDLE_VERIFICATION.json").read_text())
    checks["self_contained_chronology"] = chronology.get("status") == "PASS"
    result = {
        "audit": "G237_EXTERNAL_REVIEW_REPAIR_CERTIFICATION",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "checks": checks,
        "scientific_landing_changed": False,
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))
    if result["status"] != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
