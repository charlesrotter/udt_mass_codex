#!/usr/bin/env python3
"""Dependency-free aggregate verifier for the bounded G337 package."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import subprocess
import tempfile
from pathlib import Path


PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parent
PREREG_COMMIT = "96135e03"
LANDING = (
    "G337_FULL_INITIAL_FIELDS_OWN_INHERITED_DOUBLE_SILENT_THIRD_JET"
    "__POINTWISE_R_B_C_LAMBDA_MU_TUPLE_DOES_NOT"
    "__SPATIAL_JETS_SURVIVE"
    "__BOTH_STRICT_ROOTS_AND_NONZERO_HOMOGENEOUS_RESPONSE_RETAINED"
    "__NO_FINITE_TIME_STABILITY_OR_HISTORY_SELECTION"
)


def run(script: str, output: Path):
    result = subprocess.run(
        ["python3", "-B", "-S", str(PACKAGE / script), "--output", str(output)],
        text=True, capture_output=True, check=False,
    )
    if result.returncode:
        raise AssertionError(f"{script} failed: {result.stderr or result.stdout}")
    return json.loads(output.read_text(encoding="utf-8")), result.stdout.strip()


def frozen_source(relative: Path, size: int, digest: str) -> bytes:
    for base in (ROOT, ROOT / "sources"):
        resolved_base = base.resolve()
        candidate = (base / relative).resolve()
        if not candidate.is_relative_to(resolved_base):
            raise AssertionError(f"source escaped allowed root: {relative}")
        payload = candidate.read_bytes() if candidate.is_file() else b""
        if len(payload) == size and hashlib.sha256(payload).hexdigest() == digest:
            return payload
    replay = subprocess.run(
        ["git", "show", f"{PREREG_COMMIT}:{relative.as_posix()}"],
        cwd=ROOT, capture_output=True, check=False,
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

    with tempfile.TemporaryDirectory(prefix="g337_package_") as temporary:
        temp = Path(temporary)
        production, pstdout = run("derive_double_silent_third_response.py", temp / "p.json")
        independent, istout = run(
            "verify_double_silent_third_response_independent.py", temp / "i.json"
        )
        catches, cstdout = run("run_catch_proofs.py", temp / "c.json")
        require(production["landing"] == LANDING, "landing_exact")
        require(production["grade"] ==
                "DERIVED_CONDITIONAL_BOUNDED__PENDING_INDEPENDENT_REVIEW",
                "production_grade_exact")
        require(production["preregistration_commit"] == PREREG_COMMIT, "prereg_commit_exact")
        require(production["checks_passed"] == 149, "production_149_exact")
        require(production["finite_boost_controls"] == 30, "thirty_boost_controls")
        require(production["classifications"]["complete_initial_field_ownership"] ==
                "YES_CONDITIONAL", "complete_field_ownership")
        require(production["classifications"]["pointwise_tuple_ownership"] == "NO",
                "pointwise_tuple_nonownership")
        twins = production["exact_pointwise_twins"]
        require(len(twins) == 4, "four_exact_twins")
        require(twins[0]["R"] == twins[1]["R"] == twins[2]["R"] == twins[3]["R"] ==
                "319/200", "twins_same_R")
        require(twins[0]["s2"] != twins[1]["s2"] and twins[2]["s2"] != twins[3]["s2"],
                "twins_different_s2")
        require(twins[0]["grad_R_squared"] != twins[1]["grad_R_squared"],
                "twins_invariantly_distinct")
        require(production["homogeneous_controls"][0]["s2"] == "-128/25" and
                production["homogeneous_controls"][1]["s2"] == "128/25",
                "homogeneous_both_roots")
        require(independent["all_passed"], "independent_pass")
        require(independent["check_count"] == 26, "independent_26_exact")
        require(not independent["imports_production_code"], "independent_no_import")
        require(not independent["reads_production_output"], "independent_no_output_read")
        require(catches["verdict"] == "PASS", "hostile_pass")
        require(catches["mutations_caught"] == 17, "hostile_17_exact")
        require("149" in pstdout and "G337 independent PASS: 26" in istout and "17" in cstdout,
                "stdout_counts")
        for filename, replay in (
            ("DERIVATION_RESULT.json", production),
            ("INDEPENDENT_VERIFICATION.json", independent),
            ("CATCH_PROOF_RESULT.json", catches),
        ):
            expected = (json.dumps(replay, indent=2, sort_keys=True) + "\n").encode()
            require((PACKAGE / filename).read_bytes() == expected,
                    f"registered_{filename}_byte_exact")

    required = (
        "MAP.md", "EXPLORATORY_MAP_NOTE.md", "PREREGISTRATION.md", "PREMISE_LEDGER.tsv",
        "COMPLETENESS_MAP.md", "SOURCE_SCOPE.tsv", "SOURCE_MANIFEST.tsv", "EXECUTION_NOTE.md",
        "EXACT_DERIVATION.md", "LAY_REPORT.md", "STATUS_LEDGER.tsv", "AUDIT_REPORT.md",
        "EVIDENCE_GATES.md", "COMMANDS.md", "RUN_RECORD.md",
    )
    for filename in required:
        require((PACKAGE / filename).is_file(), f"document_{filename}")

    prereg = (PACKAGE / "PREREGISTRATION.md").read_text(encoding="utf-8")
    exact = (PACKAGE / "EXACT_DERIVATION.md").read_text(encoding="utf-8")
    lay = (PACKAGE / "LAY_REPORT.md").read_text(encoding="utf-8")
    ledger = (PACKAGE / "PREMISE_LEDGER.tsv").read_text(encoding="utf-8")
    require("HAND_STRUCTURE_DISCLOSED" in prereg, "prereg_disclosure")
    require("s2 = -(n Ric3)(v,v) + 2(n[K gamma^{-1}K])(v,v)" in prereg,
            "preregistered_identity")
    require("momentum constraint cannot be substituted" in exact,
            "no_premature_momentum_reduction")
    require("not fixed by the compressed pointwise tuple" in exact,
            "tuple_nonownership_stated")
    require("s2 = 8 b mu" in exact, "homogeneous_formula_stated")
    require("short pointwise summary does not" in lay, "lay_pointwise_distinction")
    require("does not choose which initial" in lay, "lay_no_history_selection")
    require("Universal_Reciprocity_DDR\tOWNER_ADOPTED_PROVISIONAL_POSTULATE" in ledger,
            "DDR_owner_provisional")
    require("observations_scale_Xmax\tOMITTED_OPEN" in ledger, "scale_Xmax_open")

    rows = list(csv.DictReader(
        (PACKAGE / "SOURCE_MANIFEST.tsv").open(encoding="utf-8"), delimiter="\t"
    ))
    require(len(rows) == 6, "six_frozen_sources")
    for row in rows:
        relative = Path(row["path"])
        require(not relative.is_absolute() and ".." not in relative.parts,
                f"source_{row['source_id']}_path_safe")
        payload = frozen_source(relative, int(row["bytes"]), row["sha256"])
        require(len(payload) == int(row["bytes"]), f"source_{row['source_id']}_bytes")
        require(hashlib.sha256(payload).hexdigest() == row["sha256"],
                f"source_{row['source_id']}_sha256")

    for script in (
        "derive_double_silent_third_response.py",
        "verify_double_silent_third_response_independent.py",
        "run_catch_proofs.py",
    ):
        source = (PACKAGE / script).read_text(encoding="utf-8")
        require("import numpy" not in source and "import sympy" not in source,
                f"{script}_standard_library_only")
    independent_source = (
        PACKAGE / "verify_double_silent_third_response_independent.py"
    ).read_text(encoding="utf-8")
    require("derive_double_silent_third_response" not in independent_source,
            "independent_source_separation")

    payload = {
        "package": "G337", "all_passed": True, "check_count": len(checks),
        "checks": checks, "landing": LANDING,
        "registered_outputs_replayed": True, "package_mutated": False,
        "external_review": "PENDING",
    }
    text = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(text, encoding="utf-8")
    print(f"G337 package PASS: {len(checks)} aggregate gates")


if __name__ == "__main__":
    main()
