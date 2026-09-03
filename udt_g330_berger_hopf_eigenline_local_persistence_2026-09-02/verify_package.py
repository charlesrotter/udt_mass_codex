#!/usr/bin/env python3
"""Aggregate deterministic verifier for the bounded G330 package."""

from __future__ import annotations

import argparse
import ast
import csv
import hashlib
import json
import subprocess
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parent
REPO = ROOT.parent
SOURCE_ROOT = REPO / "sources" if (REPO / "sources").is_dir() else REPO
FROZEN_SOURCE_COMMIT = "add519ae"
LANDING = (
    "NONROUND_BERGER_S3_METRIC_DEFINES_INTRINSIC_HOPF_EIGENLINE"
    "__NORMALIZED_ABSOLUTE_HELICITY_ONE"
    "__LOCAL_SMOOTH_EINSTEIN_DEVELOPMENT_PRESERVES_WHILE_GAP_OPEN"
    "__ROUND_AND_OTHER_TOPOLOGY_CONTROLS_BLOCK_UNIVERSAL_SELECTOR"
)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="PACKAGE_VERIFICATION_RESULT.json")
    args = parser.parse_args()
    checks = []

    def require(condition, name):
        if not condition:
            raise AssertionError(name)
        checks.append(name)

    required = (
        "MAP.md", "PREMISE_LEDGER.tsv", "PREREGISTRATION.md", "COMPLETENESS_MAP.md",
        "derive_berger_hopf.py", "verify_berger_hopf_independent.py", "run_catch_proofs.py",
        "DERIVATION_RESULT.json", "INDEPENDENT_VERIFICATION.json", "CATCH_PROOF_RESULT.json",
        "EXACT_DERIVATION.md", "LAY_REPORT.md", "STATUS_LEDGER.tsv", "EVIDENCE_GATES.md",
        "RUN_RECORD.md", "COMMANDS.md",
        "AUDIT_REPORT.md", "SOURCE_SCOPE.tsv", "SOURCE_MANIFEST.tsv",
        "EXTERNAL_REVIEW_REQUEST.md", "build_source_manifest.py", "build_review_intake.py",
        "verify_review_intake.py", "EXTERNAL_REVIEW.md", "EXTERNAL_REVIEW_TRANSMISSION.md",
        "REPAIR_PREREGISTRATION.md", "REPAIR_FOLLOWUP_REQUEST.md",
        "EXTERNAL_REPAIR_FOLLOWUP.md", "R3_COMPLETION_PREREGISTRATION.md",
        "R3_COMPLETION_FOLLOWUP_REQUEST.md", "R3_COMPLETION_TRANSMISSION.md",
        "EXTERNAL_R3_COMPLETION_FOLLOWUP.md",
    )
    for name in required:
        require((ROOT / name).is_file(), f"required_{name}")

    production = json.loads((ROOT / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    independent = json.loads((ROOT / "INDEPENDENT_VERIFICATION.json").read_text(encoding="utf-8"))
    hostile = json.loads((ROOT / "CATCH_PROOF_RESULT.json").read_text(encoding="utf-8"))
    require(production["all_passed"] and production["check_count"] == 39, "production_count")
    require(production["landing"] == LANDING, "production_landing")
    require(production["normalized_hopf"] == "-1", "production_hopf")
    require(production["universal_selector"] is False, "production_nonselector")
    require(production["carrier_imported"] is False, "production_no_carrier")
    require(production["action_imported"] is False, "production_no_action")
    require(production["stability_claimed"] is False, "production_no_stability")
    require(production["history_selected"] is False, "production_no_history")
    require(production["scale_selected"] is False, "production_no_scale")
    require(production["Xmax_selected"] is False, "production_no_xmax")

    require(independent["all_passed"] and independent["check_count"] == 40,
            "independent_count")
    require(independent["reads_production_output"] is False, "independent_no_result_read")
    require(independent["imports_production_code"] is False, "independent_no_code_import")
    require(independent["normalized_absolute_hopf"] == 1, "independent_hopf")
    require(independent["round_line_selected"] is False, "independent_round_control")
    require(independent["universal_history_selector"] is False, "independent_nonselector")
    require(independent["historical_carrier_used"] is False, "independent_no_carrier")
    require(independent["historical_action_used"] is False, "independent_no_action")

    require(hostile["all_caught"] and hostile["catch_count"] == 8, "hostile_count")
    require(hostile["production_output_read"] is False, "hostile_no_result_read")
    require(len({row["name"] for row in hostile["records"]}) == 8, "hostile_unique")
    require(all(row["caught"] and row["returncode"] != 0 for row in hostile["records"]),
            "hostile_all_fail")

    exact = (ROOT / "EXACT_DERIVATION.md").read_text(encoding="utf-8")
    audit = (ROOT / "EVIDENCE_GATES.md").read_text(encoding="utf-8")
    lay = (ROOT / "LAY_REPORT.md").read_text(encoding="utf-8")
    status = (ROOT / "STATUS_LEDGER.tsv").read_text(encoding="utf-8")
    prereg = (ROOT / "PREREGISTRATION.md").read_text(encoding="utf-8")
    premise = (ROOT / "PREMISE_LEDGER.tsv").read_text(encoding="utf-8")
    completeness = (ROOT / "COMPLETENESS_MAP.md").read_text(encoding="utf-8")
    exact_flat = " ".join(exact.split())
    require(LANDING in exact.replace("\n", ""), "exact_landing")
    for token in (
        "DERIVED_CONDITIONAL__EXTERNALLY_ACCEPTED_AFTER_PREREGISTERED_R1_R3_REPAIRS",
        "The current equation admits both",
        "old static finite-box stability result cannot be transferred",
        "not a separate field equation",
    ):
        require(token in exact_flat, f"exact_token_{token[:24]}")
    for token in ("add519ae", "39 exact production", "40 implementation-distinct", "8 direct"):
        require(token in audit, f"evidence_token_{token}")
    for token in (
        "not a universe selector", "does not revive the old", "some nonzero interval",
        "metric-measured circumference",
    ):
        require(token in lay, f"lay_token_{token}")
    for token in (
        "global_time_persistence\tOPEN",
        "history_or_occupancy_selection\tOPEN",
        "historical_L2_L4_stability\tNOT_TRANSFERRED",
        "metric_kernel_angular_equation\tUNCHANGED",
    ):
        require(token in status, f"status_token_{token.split(chr(9))[0]}")
    for token in ("Candidate outcomes", "Falsification contract", "Nonuniversality gate"):
        require(token in prereg, f"prereg_token_{token}")
    for token in (
        "S2_carrier\tOMITTED_OPEN",
        "action_or_energy\tOMITTED_OPEN",
        "observations_scale_Xmax\tOMITTED_OPEN",
        "local_Cauchy_theorem\tIMPORTED_MATHEMATICAL_METHOD",
    ):
        require(token in premise, f"premise_token_{token.split(chr(9))[0]}")
    require("This is one bounded topology/geometry tile" in completeness,
            "completeness_bounded_tile")
    external = (ROOT / "EXTERNAL_REVIEW.md").read_text(encoding="utf-8")
    require(
        "ACCEPT_WITH_REPAIRS__G330_BOUNDED_SCIENTIFIC_LANDING_RETAINED" in external,
        "external_repair_verdict",
    )
    repair = (ROOT / "REPAIR_PREREGISTRATION.md").read_text(encoding="utf-8")
    for token in ("R1 — self-contained", "R2 — explicitly intrinsic", "R3 — explicit imported"):
        require(token in repair, f"repair_token_{token[:10]}")
    external_repair = (ROOT / "EXTERNAL_REPAIR_FOLLOWUP.md").read_text(encoding="utf-8")
    require("REPAIR_INCOMPLETE__G330_BOUNDED_SCIENTIFIC_LANDING_RETAINED" in external_repair,
            "external_r3_incomplete_verdict")
    r3_records = {
        "exact": exact,
        "lay": lay,
        "premise": premise,
        "status": status,
        "evidence": audit,
    }
    for name, record in r3_records.items():
        require("isometry-extension consequence" in record, f"r3_explicit_{name}")
    external_r3 = (ROOT / "EXTERNAL_R3_COMPLETION_FOLLOWUP.md").read_text(encoding="utf-8")
    require(
        "R3_COMPLETION_ACCEPTED__G330_BOUNDED_SCIENTIFIC_LANDING_RETAINED" in external_r3,
        "external_r3_completion_accepted",
    )

    allowed_imports = {"__future__", "argparse", "ast", "csv", "hashlib", "json", "fractions",
                       "pathlib", "shutil", "subprocess", "tempfile"}
    for script_name in ("derive_berger_hopf.py", "verify_berger_hopf_independent.py",
                        "run_catch_proofs.py", "verify_package.py", "build_source_manifest.py",
                        "build_review_intake.py", "verify_review_intake.py"):
        source = (ROOT / script_name).read_text(encoding="utf-8")
        compile(source, script_name, "exec")
        require(True, f"syntax_{script_name}")
        tree = ast.parse(source)
        imported = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imported.update(alias.name.split(".")[0] for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                imported.add(node.module.split(".")[0])
        require(imported <= allowed_imports, f"stdlib_only_{script_name}")

    forbidden = (
        "import torch", "import numpy", "import scipy", "import sympy",
        "native_hopfion_topology_audit_2026-07-19/derive_topology.py",
        "noNull_energy", "solver_action", "X_max =", "LambdaCDM",
    )
    combined_scripts = "\n".join(
        (ROOT / name).read_text(encoding="utf-8")
        for name in ("derive_berger_hopf.py", "verify_berger_hopf_independent.py")
    )
    for token in forbidden:
        require(token not in combined_scripts, f"forbidden_absent_{token}")

    source_rows = list(csv.DictReader((ROOT / "SOURCE_MANIFEST.tsv").open(encoding="utf-8"),
                                      delimiter="\t"))
    require(len(source_rows) == 15, "source_manifest_count")
    require(len({row["source_id"] for row in source_rows}) == 15, "source_ids_unique")
    for row in source_rows:
        relative = Path(row["path"])
        require(not relative.is_absolute() and ".." not in relative.parts,
                f"source_path_safe_{row['source_id']}")
        source_path = SOURCE_ROOT / relative
        source_bytes = source_path.read_bytes() if source_path.is_file() else b""
        if (len(source_bytes) != int(row["bytes"])
                or hashlib.sha256(source_bytes).hexdigest() != row["sha256"]):
            # In a sealed intake, SOURCE_ROOT is the immutable intake-local sources tree. In the
            # live repository, current status files legitimately advance when G330 is banked, so
            # resolve a drifted source from the pushed preregistration commit instead of silently
            # rewriting the reviewed source manifest.
            frozen = subprocess.run(
                ["git", "show", f"{FROZEN_SOURCE_COMMIT}:{relative.as_posix()}"],
                cwd=REPO, capture_output=True, check=False,
            )
            source_bytes = frozen.stdout if frozen.returncode == 0 else b""
        require(bool(source_bytes), f"source_exists_{row['source_id']}")
        require(len(source_bytes) == int(row["bytes"]),
                f"source_bytes_{row['source_id']}")
        require(hashlib.sha256(source_bytes).hexdigest() == row["sha256"],
                f"source_hash_{row['source_id']}")

    with tempfile.TemporaryDirectory(prefix="g330_replay_") as tmp:
        tmp_path = Path(tmp)
        replay_commands = (
            ("derive_berger_hopf.py", "DERIVATION_RESULT.json"),
            ("verify_berger_hopf_independent.py", "INDEPENDENT_VERIFICATION.json"),
            ("run_catch_proofs.py", "CATCH_PROOF_RESULT.json"),
        )
        for script_name, result_name in replay_commands:
            target = tmp_path / result_name
            completed = subprocess.run(
                ["python3", "-S", str(ROOT / script_name), "--output", str(target)],
                text=True, capture_output=True, check=False,
            )
            require(completed.returncode == 0, f"replay_exit_{script_name}")
            require(target.read_bytes() == (ROOT / result_name).read_bytes(),
                    f"replay_byte_exact_{result_name}")

    payload = {
        "all_passed": True,
        "check_count": len(checks),
        "checks": checks,
        "landing": LANDING,
        "maximum_internal_grade":
            "DERIVED_CONDITIONAL__EXTERNALLY_ACCEPTED_AFTER_PREREGISTERED_R1_R3_REPAIRS",
        "production_checks": 39,
        "independent_checks": 40,
        "hostile_catches": 8,
    }
    Path(args.output).write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n",
                                 encoding="utf-8")
    print(f"G330 package PASS: {len(checks)} aggregate gates")


if __name__ == "__main__":
    main()
