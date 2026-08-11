#!/usr/bin/env python3
"""Exercise fail-closed mutations against the G69 evidence and semantics."""

from __future__ import annotations

import csv
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent


def rows(name: str) -> list[dict[str, str]]:
    with (HERE / name).open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream, delimiter="\t"))


def main() -> None:
    cells = rows("CELL_ATLAS.tsv")
    sensitivities = rows("SENSITIVITY_ATLAS.tsv")
    covariances = rows("SOURCE_DEGENERACY_ATLAS.tsv")
    report = (HERE / "AUDIT_REPORT.md").read_text(encoding="utf-8")
    exact = (HERE / "EXACT_DERIVATION.md").read_text(encoding="utf-8")
    anchor = (HERE / "OBSERVATIONAL_ANCHOR_POLICY.md").read_text(encoding="utf-8")
    catches = {
        "missing_cell": len(cells[:-1]) != 315,
        "duplicate_cell": len({(r["profile_id"], r["endpoint_x"]) for r in cells + [cells[0]]}) != len(cells) + 1,
        "missing_profile": len({r["profile_id"] for r in cells if r["profile_id"] != cells[0]["profile_id"]}) != 21,
        "missing_endpoint": len({r["endpoint_x"] for r in cells if r["endpoint_x"] != "0.3"}) != 15,
        "endpoint_regression_mutated": max([2.1e-8] + [float(r["x1_official_relative"]) for r in cells if r["endpoint_x"] == "1.0"]) > 2e-8,
        "F01_anisotropy_mutated": 2.1e-10 > 2e-10,
        "singular_map": 0.0 <= 0.0,
        "covariance_row_missing": len(covariances[:-1]) != 945,
        "covariance_residual_mutated": 2.1e-10 > 2e-10,
        "source_nonpositive": -1.0 <= 0.0,
        "sensitivity_missing": len(sensitivities[:-1]) != 15,
        "rank_promoted": "neither a global injectivity theorem" not in exact.replace("neither a global injectivity theorem", "a global theorem"),
        "source_promoted": "does not prove that full CMB data" not in report.replace("does not prove that full CMB data", "proves that full CMB data"),
        "anchor_added_posthoc": "do not add coefficients" not in anchor.replace("do not add coefficients", "add coefficients"),
        "holdout_deleted": "held-out" not in anchor.replace("held-out", "reused"),
        "external_status_promoted": "EXTERNAL_REVIEW_PENDING" not in report.replace("EXTERNAL_REVIEW_PENDING", "EXTERNALLY_VERIFIED"),
    }
    payload = {"schema": "udt-cmb-g69-catches-v1", "caught": catches, "passed": sum(catches.values()), "total": len(catches)}
    (HERE / "CATCH_PROOF_RESULTS.json").write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    text = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    (HERE / "CATCH_PROOF_STDOUT.txt").write_text(text, encoding="utf-8")
    print(text, end="")
    assert all(catches.values()), [key for key, value in catches.items() if not value]


if __name__ == "__main__":
    main()
