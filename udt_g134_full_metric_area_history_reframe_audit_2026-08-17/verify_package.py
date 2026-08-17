#!/usr/bin/env python3
"""Verify current G134 evidence without importing either algebra implementation."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> None:
    checks: dict[str, bool] = {}
    expected_results = {
        "DERIVATION_RESULT.json": ("PASS", 23, 23),
        "INDEPENDENT_VERIFICATION.json": ("PASS", 19, 19),
        "CATCH_PROOF_RESULT.json": ("PASS", 5, 5),
    }
    for name, expected in expected_results.items():
        payload = json.loads((HERE / name).read_text(encoding="utf-8"))
        checks[f"{name}_status"] = payload["status"] == expected[0]
        checks[f"{name}_count"] = payload["check_count"] == expected[1]
        checks[f"{name}_passed"] = payload["passed"] == expected[2]

    with (HERE / "SOURCE_MANIFEST.tsv").open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
    checks["source_manifest_nonempty"] = bool(rows)
    immutable_rows = [row for row in rows if row["role"] != "exact premise authority at preregistration"]
    checks["immutable_source_hashes_match"] = all(
        sha256(ROOT / row["path"]) == row["sha256"] for row in immutable_rows
    )
    prereg_registry_rows = [row for row in rows if row["role"] == "exact premise authority at preregistration"]
    checks["preregistered_registry_hash_frozen"] = len(prereg_registry_rows) == 1 and prereg_registry_rows[0][
        "sha256"
    ] == "23fe40c8066235d4c123b18f67f10e0cd3174951c0431e265d4e639424f02e9c"
    checks["current_registry_banks_G134"] = "G134\tfull_metric_bivector_area_faithfulness" in (
        ROOT / "CURRENT_SCIENTIFIC_PREMISES.tsv"
    ).read_text(encoding="utf-8")
    protected_tokens = ("native_onshell_timelive", "pair_regime_flow", "sne_xmax_G88", "curvature_holonomy_atlas")
    checks["no_protected_source"] = not any(token in row["path"] for row in rows for token in protected_tokens)

    prereg = (HERE / "PREREGISTRATION.md").read_text(encoding="utf-8")
    report = (HERE / "AUDIT_REPORT.md").read_text(encoding="utf-8")
    derivation = (HERE / "EXACT_DERIVATION.md").read_text(encoding="utf-8")
    ledger = (HERE / "PREMISE_LEDGER.tsv").read_text(encoding="utf-8")
    checks["preregistered_landing_present"] = "AREA_BILINEAR_METRIC_FAITHFUL__RELATION_NETWORK_ADMISSIBILITY_REFRAMED__HISTORY_SELECTION_OPEN" in prereg
    checks["report_external_math_pass"] = (
        "FRESH_ADVERSARIAL_FOLLOWUP_PASS" in report
        and "AREA_BILINEAR_METRIC_FAITHFUL" in report
    )
    checks["history_selection_guard"] = "does **not** select a physical history" in report
    checks["full_area_not_self_area_guard"] = "Individual plane areas are not the complete object" in derivation
    checks["metric_first_relation_first_split"] = "Metric-first" in report and "Relation-first" in report
    checks["no_numeric_physics_choice"] = "numeric_parameters\tNONE" in ledger
    checks["external_review_recorded"] = (HERE / "FRESH_ADVERSARIAL_REVIEW.md").is_file()
    checks["followup_scope_is_repair_only"] = "Verify only the registered intake-count repair" in (
        HERE / "FOLLOWUP_REVIEW_REQUEST.md"
    ).read_text(encoding="utf-8")
    followup = (HERE / "FOLLOWUP_REVIEW.md").read_text(encoding="utf-8")
    checks["followup_review_recorded"] = "FOLLOWUP_PASS" in followup
    checks["followup_count_semantics"] = all(token in followup for token in ("19 manifest", "20 files", "21 total"))
    checks["followup_manifest_hash"] = (
        "ad7016c760f17b459495e1ece705eb7637d0cf5df98aba31b054d7373dc0e041" in followup
    )
    checks["final_status_guard"] = "FRESH_ADVERSARIAL_FOLLOWUP_PASS" in (HERE / "STATUS.md").read_text(
        encoding="utf-8"
    )

    status = "PASS" if all(checks.values()) else "FAIL"
    print(f"{status}: {sum(checks.values())}/{len(checks)} G134 package checks")
    if status != "PASS":
        for name, value in checks.items():
            if not value:
                print(f"FAIL: {name}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
