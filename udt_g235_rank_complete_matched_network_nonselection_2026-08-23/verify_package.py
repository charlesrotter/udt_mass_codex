#!/usr/bin/env python3
"""No-write G235 package verifier."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path


PACKAGE = Path(__file__).resolve().parent
REPO = PACKAGE.parent
SEALED_SOURCE_ROOT = PACKAGE / "SEALED_SOURCES"
SOURCE_ROOT = SEALED_SOURCE_ROOT if SEALED_SOURCE_ROOT.is_dir() else REPO


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def main() -> None:
    required = [
        "PREREGISTRATION.md",
        "VERIFICATION_STRENGTHENING_PREREGISTRATION.md",
        "EXTERNAL_REVIEW_REPAIR_PREREGISTRATION.md",
        "EXTERNAL_REVIEW.md",
        "REPAIR_FOLLOWUP_REQUEST.md",
        "EXTERNAL_REPAIR_FOLLOWUP.md",
        "FINAL_EVIDENCE_MANIFEST.tsv",
        "POST_REVIEW_STARTUP_REPAIR_PREREGISTRATION.md",
        "MAP.md",
        "PREMISE_LEDGER.tsv",
        "SOURCE_MANIFEST.tsv",
        "derive_matched_network_nonselection.py",
        "verify_matched_network_independent.py",
        "DERIVATION_RESULT.json",
        "INDEPENDENT_VERIFICATION.json",
        "NETWORK_TWIN_ATLAS.tsv",
        "EXACT_DERIVATION.md",
        "AUDIT_REPORT.md",
        "LAY_REPORT.md",
        "EVIDENCE_GATES.md",
        "STATUS_LEDGER.tsv",
    ]
    checks: dict[str, bool] = {f"file::{name}": (PACKAGE / name).is_file() for name in required}

    source_rows = read_tsv(PACKAGE / "SOURCE_MANIFEST.tsv")
    checks["source_count_9"] = len(source_rows) == 9
    checks["source_root_exists"] = SOURCE_ROOT.is_dir()
    for row in source_rows:
        source = (SOURCE_ROOT / row["path"]).resolve()
        contained = source.is_relative_to(SOURCE_ROOT.resolve())
        actual = hashlib.sha256(source.read_bytes()).hexdigest() if source.is_file() else ""
        checks[f"source_contained::{row['path']}"] = contained
        checks[f"source::{row['path']}"] = contained and actual == row["sha256"]

    production = json.loads((PACKAGE / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    independent = json.loads((PACKAGE / "INDEPENDENT_VERIFICATION.json").read_text(encoding="utf-8"))
    checks.update(
        {
            "production_landing": production["landing"].endswith("__NO_CANDIDATE"),
            "production_positive_checks": production["all_positive_checks_pass"] is True,
            "production_nonidentity_gate_fails": production["candidate_nonidentity_gate_passes"] is False,
            "production_rank_10": production["design_rank"] == 10,
            "production_separator": production["g233_invariant_separator"] == "560/81",
            "production_both_twins": (
                production["checks"]["seed_network_passes_structural_condition"] is True
                and production["checks"]["b7_network_passes_structural_condition"] is True
            ),
            "production_hostile_rank": production["checks"]["five_ruler_mutation_drops_rank"] is True,
            "production_hostile_edge": production["checks"]["corrupted_edge_mutation_breaks_composition"] is True,
            "independent_landing": independent["landing"] == "INDEPENDENT_CONFIRMATION__NO_CANDIDATE",
            "independent_positive_checks": independent["all_positive_checks_pass"] is True,
            "independent_nonidentity_gate_fails": independent["candidate_nonidentity_gate_passes"] is False,
            "independent_rank_10_9": independent["rank"] == 10 and independent["five_ruler_rank"] == 9,
            "independent_both_twins": independent["network_pass_by_b"] == {"0": True, "7": True},
            "independent_separator": independent["separator"] == "560/81",
            "independent_assertions_strengthened": independent["assertions"] > 30005,
            "independent_six_pair_completions": independent["checks"][
                "independent_six_pair_completions_per_profile"
            ]
            is True,
            "independent_common_clock": independent["checks"][
                "independent_six_constructed_h00_entries_match"
            ]
            is True,
            "independent_overlap": independent["checks"]["independent_two_chart_screen_overlap"] is True,
            "production_overlap": production["checks"]["two_chart_screen_overlap_recovers_metric"] is True,
        }
    )

    twin_rows = read_tsv(PACKAGE / "NETWORK_TWIN_ATLAS.tsv")
    premise_rows = read_tsv(PACKAGE / "PREMISE_LEDGER.tsv")
    status_rows = read_tsv(PACKAGE / "STATUS_LEDGER.tsv")
    checks["twin_rows_2"] = len(twin_rows) == 2
    checks["twin_atlas_both_accepted"] = [row["candidate_verdict"] for row in twin_rows] == [
        "ACCEPTED",
        "ACCEPTED_NOT_REJECTED",
    ]
    checks["premise_rows_14"] = len(premise_rows) == 14
    checks["status_rows_10"] = len(status_rows) == 10

    exact = (PACKAGE / "EXACT_DERIVATION.md").read_text(encoding="utf-8")
    audit = (PACKAGE / "AUDIT_REPORT.md").read_text(encoding="utf-8")
    checks["exact_quantifier_boundary"] = "exists one matched rank-complete" in exact
    checks["exact_untyped_full_tuple_guard"] = "not typed linear arrows" in exact
    checks["audit_external_accepted"] = "G235_ACCEPTED_WITH_CAVEATS" in audit
    checks["repair_followup_accepted"] = (
        "G235_REPAIRS_ACCEPTED__NO_CANDIDATE_RETAINED"
        in (PACKAGE / "EXTERNAL_REPAIR_FOLLOWUP.md").read_text(encoding="utf-8")
    )
    production_script = (PACKAGE / "derive_matched_network_nonselection.py").read_text(encoding="utf-8")
    independent_script = (PACKAGE / "verify_matched_network_independent.py").read_text(encoding="utf-8")
    checks["production_no_write_entrypoint"] = '"--no-write"' in production_script
    checks["independent_no_write_entrypoint"] = '"--no-write"' in independent_script
    checks["no_latex_formfeed"] = all(b"\x0c" not in (PACKAGE / name).read_bytes() for name in required)

    manifest_rows = read_tsv(PACKAGE / "FINAL_EVIDENCE_MANIFEST.tsv")
    registered = {row["path"]: row["sha256"] for row in manifest_rows}
    actual = {
        path.name: hashlib.sha256(path.read_bytes()).hexdigest()
        for path in PACKAGE.iterdir()
        if path.is_file() and path.name != "FINAL_EVIDENCE_MANIFEST.tsv"
    }
    checks["final_manifest_no_duplicates"] = len(registered) == len(manifest_rows)
    checks["final_manifest_exact_top_level"] = registered == actual

    failures = [name for name, passed in checks.items() if not passed]
    result = {"all_pass": not failures, "failures": failures, "checks": checks}
    print(json.dumps(result, indent=2))
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
