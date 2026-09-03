#!/usr/bin/env python3
"""Aggregate dependency-free verifier for the bounded pre-review G335 package."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import subprocess
import tempfile
from pathlib import Path


PACKAGE = Path(__file__).resolve().parent
REPO = PACKAGE.parent
PREREG_COMMIT = "a3324f62"
LANDING = (
    "NONZERO_INITIAL_GEOMETRIC_PAIR_RESPONSE_PERSISTS_ON_PER_DATUM_LOCAL_MARKED_INTERVAL"
    "__SILENT_DIRECTIONS_REQUIRE_HIGHER_JET"
    "__FIXED_COMPACT_ALL_DIRECTION_GAP_GIVES_UNIFORM_LOCAL_INTERVAL"
    "__RAW_COMPONENT_AND_OBSERVER_TIME_REMAIN_CARRY_QUALIFIED"
)


def digest_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def run(script: str, output: Path) -> tuple[dict, str]:
    result = subprocess.run(
        ["python3", "-B", "-S", str(PACKAGE / script), "--output", str(output)],
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode:
        raise AssertionError(f"{script} failed: {result.stderr or result.stdout}")
    return json.loads(output.read_text(encoding="utf-8")), result.stdout.strip()


def frozen_source(relative: Path, expected_bytes: int, expected_digest: str) -> bytes:
    source_root = REPO / "sources" if (REPO / "sources").is_dir() else REPO
    candidate = (source_root / relative).resolve()
    if not candidate.is_relative_to(source_root.resolve()):
        raise AssertionError(f"source escaped root: {relative}")
    payload = candidate.read_bytes() if candidate.is_file() else b""
    if len(payload) == expected_bytes and digest_bytes(payload) == expected_digest:
        return payload
    replay = subprocess.run(
        ["git", "show", f"{PREREG_COMMIT}:{relative.as_posix()}"],
        cwd=REPO,
        capture_output=True,
        check=False,
    )
    if replay.returncode:
        raise AssertionError(f"frozen source unavailable: {relative}")
    return replay.stdout


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    checks: list[str] = []

    def require(condition: bool, label: str) -> None:
        if not condition:
            raise AssertionError(label)
        checks.append(label)

    with tempfile.TemporaryDirectory(prefix="g335_package_") as temporary:
        temp = Path(temporary)
        production, production_stdout = run(
            "derive_local_pair_persistence.py", temp / "production.json"
        )
        independent, independent_stdout = run(
            "verify_local_pair_persistence_independent.py", temp / "independent.json"
        )
        catches, catches_stdout = run("run_catch_proofs.py", temp / "catches.json")

        require(production["landing"] == LANDING, "landing_exact")
        require(production["grade"] ==
                "EXTERNALLY_ACCEPTED_DERIVED_CONDITIONAL_BOUNDED", "grade_accepted_exact")
        require(production["classifications"] == [
            "CONDITIONAL_PER_DATUM_LOCAL_PERSISTENCE",
            "FIRST_ORDER_SILENT_STRATUM_REQUIRES_HIGHER_JET",
            "FIXED_DATUM_UNIFORM_ALL_DIRECTION_PERSISTENCE",
            "FULL_FAMILY_UNIFORM_INTERVAL_NOT_DERIVED",
            "RAW_COMPONENT_PERSISTENCE_TRANSPORT_QUALIFIED",
            "OBSERVER_TIME_RESPONSE_OPEN",
        ], "classifications_exact")
        require(production["checks_passed"] == 171124, "production_171124_exact")
        require(production["case_count"] == 13728, "production_13728_cases")
        require(production["nonzero_direction_controls"] == 1054,
                "production_nonzero_controls")
        require(production["silent_direction_controls"] == 2,
                "production_silent_controls")
        require(production["gap_branch_controls"] == 12,
                "production_gap_controls")
        require(production["scope"]["both_G332_branches"], "both_branches")
        require(production["scope"]["all_directions"].startswith("analytic"),
                "all_directions_analytic")
        require(production["scope"]["all_finite_boosts"].startswith("analytic"),
                "all_finite_boosts_analytic")
        require(production["scope"]["topology_inputs_used"] == [], "no_topology_inputs")
        require(independent["verdict"] == "PASS", "independent_pass")
        require(independent["checks_passed"] == 4448, "independent_4448_exact")
        require(not independent["imports_production"], "independent_no_production_import")
        require(not independent["reads_production_result"], "independent_no_result_read")
        require(independent["max_trace_relative"] < 5e-12,
                "independent_trace_relative")
        require(independent["max_rank_relative"] < 2e-10,
                "independent_rank_relative")
        require(catches["verdict"] == "PASS", "catch_pass")
        require(catches["mutations_caught"] == 12, "twelve_mutations_caught")
        require("171124" in production_stdout and "13728" in production_stdout,
                "production_stdout")
        require("4448" in independent_stdout, "independent_stdout")
        require("12" in catches_stdout, "catch_stdout")

        for filename, replay in (
            ("DERIVATION_RESULT.json", production),
            ("INDEPENDENT_VERIFICATION.json", independent),
            ("CATCH_PROOF_RESULT.json", catches),
        ):
            registered = PACKAGE / filename
            require(registered.is_file(), f"registered_{filename}_exists")
            expected = (json.dumps(replay, indent=2, sort_keys=True) + "\n").encode()
            require(registered.read_bytes() == expected,
                    f"registered_{filename}_byte_exact")

    required_files = (
        "MAP.md", "PREREGISTRATION.md", "PREMISE_LEDGER.tsv", "COMPLETENESS_MAP.md",
        "SOURCE_SCOPE.tsv", "SOURCE_MANIFEST.tsv", "EXECUTION_NOTE.md", "EXACT_DERIVATION.md",
        "LAY_REPORT.md", "STATUS_LEDGER.tsv", "AUDIT_REPORT.md", "EVIDENCE_GATES.md",
        "COMMANDS.md", "RUN_RECORD.md", "EXTERNAL_REVIEW_REQUEST.md",
        "EXTERNAL_REVIEW_RESPONSE.md", "EXTERNAL_REVIEW_TRANSMISSION.md",
    )
    for filename in required_files:
        require((PACKAGE / filename).is_file(), f"document_{filename}")

    prereg = (PACKAGE / "PREREGISTRATION.md").read_text(encoding="utf-8")
    exact = (PACKAGE / "EXACT_DERIVATION.md").read_text(encoding="utf-8")
    lay = (PACKAGE / "LAY_REPORT.md").read_text(encoding="utf-8")
    audit = (PACKAGE / "AUDIT_REPORT.md").read_text(encoding="utf-8")
    ledger = (PACKAGE / "PREMISE_LEDGER.tsv").read_text(encoding="utf-8")
    completeness = (PACKAGE / "COMPLETENESS_MAP.md").read_text(encoding="utf-8")
    require("both square-root branches" in prereg, "branches_preregistered")
    require("every unit spatial" in prereg, "directions_preregistered")
    require("every finite local boost" in prereg, "boosts_preregistered")
    require("q0 = (b-C)/2 - b*mu" in exact, "initial_rate_formula")
    require("silent unit direction exists iff |b|>=|C|" in exact,
            "silent_condition_stated")
    require("sup over the slice |b| < |C|" in exact, "compact_gap_stated")
    require("does not extend uniformly" in exact, "family_uniform_boundary")
    require("not yet a full evolution" in lay, "lay_not_full_evolution")
    require("ACCEPT__G335_BOUNDED_LOCAL_PAIR_PERSISTENCE_RETAINED" in audit,
            "audit_external_accepted")
    require("standard_local_wellposedness\tIMPORTED_MATHEMATICAL_METHOD" in ledger,
            "method_import_typed")
    require("physical_germ_population_history\tOMITTED_OPEN" in ledger,
            "history_open")
    require("finite/long time and stability" in completeness, "finite_time_omitted")
    review = (PACKAGE / "EXTERNAL_REVIEW_RESPONSE.md").read_text(encoding="utf-8")
    require("ACCEPT__G335_BOUNDED_LOCAL_PAIR_PERSISTENCE_RETAINED" in review,
            "external_verdict_exact")
    require("No repairs requested" in review, "external_no_repairs")

    rows = list(csv.DictReader(
        (PACKAGE / "SOURCE_MANIFEST.tsv").open(encoding="utf-8"), delimiter="\t"
    ))
    require(len(rows) == 6, "six_source_rows")
    for row in rows:
        relative = Path(row["path"])
        require(not relative.is_absolute() and ".." not in relative.parts,
                f"source_{row['source_id']}_path_safe")
        payload = frozen_source(relative, int(row["bytes"]), row["sha256"])
        require(len(payload) == int(row["bytes"]), f"source_{row['source_id']}_bytes")
        require(digest_bytes(payload) == row["sha256"],
                f"source_{row['source_id']}_sha256")

    for script in (
        "derive_local_pair_persistence.py",
        "verify_local_pair_persistence_independent.py",
        "run_catch_proofs.py",
    ):
        source = (PACKAGE / script).read_text(encoding="utf-8")
        require("import numpy" not in source and "import sympy" not in source,
                f"{script}_standard_library_only")
    independent_source = (PACKAGE / "verify_local_pair_persistence_independent.py").read_text(
        encoding="utf-8"
    )
    require("derive_local_pair_persistence" not in independent_source,
            "independent_source_separation")

    payload = {
        "package": "G335",
        "all_passed": True,
        "check_count": len(checks),
        "checks": checks,
        "landing": LANDING,
        "registered_outputs_replayed": True,
        "package_mutated": False,
        "external_review": "ACCEPTED_NO_REPAIRS",
    }
    text = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(text, encoding="utf-8")
    print(f"G335 package PASS: {len(checks)} aggregate gates")


if __name__ == "__main__":
    main()
