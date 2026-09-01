#!/usr/bin/env python3
"""Dependency-free package gate for G314."""

from __future__ import annotations

import csv
import json
from pathlib import Path


PACKAGE = Path(__file__).resolve().parent
LANDING = (
    "GLOBAL_ADMISSIBILITY_AND_ACTUALIZATION_ARE_DISTINCT_MISSING_TYPES"
    "__CURRENT_STRUCTURE_SUPPLIES_NEITHER"
)
REQUIRED = (
    "PREREGISTRATION.md",
    "SOURCE_SCOPE.tsv",
    "REPLAY_COMMANDS.txt",
    "EXACT_DERIVATION.md",
    "AUDIT_REPORT.md",
    "LAY_REPORT.md",
    "STATUS_LEDGER.tsv",
    "EVIDENCE_GATES.md",
    "RUN_RECORD.md",
    "ADMISSIBILITY_TYPE_ATLAS.tsv",
    "WITNESS_SIGNATURES.tsv",
    "DERIVATION_RESULT.json",
    "INDEPENDENT_VERIFICATION.json",
    "CATCH_PROOF_RESULT.json",
    "derive_admissibility_types.py",
    "verify_independent.py",
    "run_catch_proofs.py",
    "EXTERNAL_REVIEW_REQUEST.md",
    "EXTERNAL_REVIEW_RESPONSE.md",
    "EXTERNAL_REVIEW_TRANSCRIPT.txt",
    "EXTERNAL_REVIEW_TRANSMISSION.md",
    "build_review_intake.py",
    "verify_package.py",
)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def read_tsv(name: str) -> list[dict[str, str]]:
    with (PACKAGE / name).open(encoding="utf-8", newline="") as stream:
        return list(csv.DictReader(stream, delimiter="\t"))


def main() -> None:
    for name in REQUIRED:
        require((PACKAGE / name).is_file(), f"missing package file: {name}")
    production = json.loads((PACKAGE / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    independent = json.loads((PACKAGE / "INDEPENDENT_VERIFICATION.json").read_text(encoding="utf-8"))
    catches = json.loads((PACKAGE / "CATCH_PROOF_RESULT.json").read_text(encoding="utf-8"))
    require(production["status"] == "PASS" and production["landing"] == LANDING,
            "production landing changed")
    require(production["assertions"] == 43, "production assertion count changed")
    require(production["complete_moduli_witness_count"] == 4, "complete witness count changed")
    require(production["control_nonhistory_count"] == 2, "nonhistory control count changed")
    require(production["admissibility_actualization"]["positive_acceptance_count"] == 3,
            "nonunique admissibility control changed")
    require(not production["minimum_missing_type"]["two_premises_logically_forced"],
            "two-premise overclaim introduced")
    require(not production["interpretive_boundary"]["conditional_field_theory_requires_unique_universe_selector"],
            "conditional field theory misgraded")
    require(independent["status"] == "PASS" and independent["landing"] == LANDING,
            "independent landing changed")
    require(independent["assertions"] == 114, "independent assertion count changed")
    require(not independent["production_imported"] and not independent["production_result_read"],
            "independent route contaminated")
    require(independent["boolean_predicates_exhausted"] == 16,
            "Boolean predicate census changed")
    require(independent["endomaps_exhausted"] == 27
            and independent["distinct_fixed_point_sets"] == 8,
            "endomap census changed")
    require(catches["status"] == "PASS" and catches["baseline_clean"],
            "hostile baseline changed")
    require(catches["mutations_registered"] == 17 and catches["mutations_caught"] == 17,
            "hostile catch count changed")
    atlas = {row["candidate_id"]: row for row in read_tsv("ADMISSIBILITY_TYPE_ATLAS.tsv")}
    require(len(atlas) == 14, "candidate atlas count changed")
    require(atlas["C03_NETWORK_RECONSTRUCTION"]["identity_on_registered_complete_family"] == "True",
            "network reconstruction promoted")
    require(atlas["C05_POSITIVE_LAMBDA"]["accepted_count"] == "3",
            "positive filter count changed")
    require(atlas["C10_POSITIVE_ROUND_S3"]["accepted_count"] == "2",
            "positive round-S3 filter count changed")
    require("not maximal symmetry alone" in atlas["C10_POSITIVE_ROUND_S3"]["note"],
            "round/maximal-symmetry correction missing")
    require(atlas["C11_ROUND_AND_SCALE"]["ownership"] == "NOT_OWNED_CANDIDATE_CONTROL",
            "finite singleton promoted")
    witnesses = {row["name"]: row for row in read_tsv("WITNESS_SIGNATURES.tsv")}
    require(witnesses["berger_S3_data"]["complete_history"] == "False",
            "Berger data promoted")
    require(witnesses["ricci_flat_plane_wave"]["complete_history"] == "False",
            "plane wave global scope promoted")
    audit = (PACKAGE / "AUDIT_REPORT.md").read_text(encoding="utf-8")
    exact = (PACKAGE / "EXACT_DERIVATION.md").read_text(encoding="utf-8")
    lay = (PACKAGE / "LAY_REPORT.md").read_text(encoding="utf-8")
    for text, label in ((audit, "audit"), (exact, "exact")):
        require("GLOBAL_ADMISSIBILITY_AND_ACTUALIZATION_ARE_DISTINCT_MISSING_TYPES" in text,
                f"{label} landing missing")
        require("conditional field theory" in text.lower(), f"{label} field-theory boundary missing")
    require("not automatically a flaw" in lay, "lay reframe changed")
    review = (PACKAGE / "EXTERNAL_REVIEW_RESPONSE.md").read_text(encoding="utf-8")
    transcript = (PACKAGE / "EXTERNAL_REVIEW_TRANSCRIPT.txt").read_text(
        encoding="utf-8", errors="replace"
    )
    verdict = "G314_ACCEPTED__ADMISSIBILITY_ACTUALIZATION_DISTINCTION_UPHELD"
    require(verdict in review, "external-review verdict missing from response")
    require(verdict in transcript, "external-review verdict missing from transcript")
    require("ALL_MANIFEST_PAYLOADS_VERIFIED" in transcript,
            "external manifest authentication missing")
    require("No exact in-scope scientific defect was found" in transcript,
            "external detailed finding missing")
    sources = {row["path"] for row in read_tsv("SOURCE_SCOPE.tsv")}
    require("udt_g313_tracefree_ricci_solution_space_bootstrap_map_2026-09-01/AUDIT_REPORT.md"
            in sources, "G313 controlling source missing")
    require("startup_surface_g312_two_premise_adoption_refresh_2026-09-01/ADOPTION_RECORD.md"
            in sources, "G312 adoption source missing")
    print("G314 package verification PASS")
    print("production assertions: 43")
    print("independent assertions: 114")
    print("hostile semantic mutations caught: 17/17")
    print("landing: " + LANDING)


if __name__ == "__main__":
    main()
