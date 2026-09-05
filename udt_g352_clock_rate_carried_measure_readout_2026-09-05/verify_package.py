#!/usr/bin/env python3
"""Aggregate no-write verifier for the bounded G352 package."""

import csv
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys


PACKAGE = Path(__file__).resolve().parent
REPO = PACKAGE.parent
OUTPUT = PACKAGE / "VERIFICATION_RESULT.json"


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def snapshot():
    rows = []
    for path in sorted(PACKAGE.rglob("*")):
        if path.is_file():
            rows.append((str(path.relative_to(PACKAGE)), path.stat().st_size, digest(path)))
    return rows


def run_json(script):
    env = dict(os.environ)
    env["UDT_NO_WRITE"] = "1"
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    process = subprocess.run(
        [sys.executable, "-B", "-S", script],
        cwd=PACKAGE,
        env=env,
        check=True,
        capture_output=True,
        text=True,
    )
    lines = [line for line in process.stdout.splitlines() if line.strip()]
    if not lines:
        raise AssertionError(f"no JSON output from {script}")
    return json.loads(lines[-1])


def main():
    checks = []

    def gate(name, condition):
        if not condition:
            raise AssertionError(name)
        checks.append(name)

    required = [
        "ADOPTION_RECORD.md",
        "MAP.md",
        "PREMISE_LEDGER.tsv",
        "PREREGISTRATION.md",
        "R1_PREREGISTRATION_SIGN_REPAIR.md",
        "R2_PREREGISTRATION_EXTERNAL_REVIEW_REPAIRS.md",
        "R2_REPAIRED_PREMISE_LEDGER.tsv",
        "REPAIR_FOLLOWUP_REVIEW_REQUEST.md",
        "build_repair_followup_intake.py",
        "EXTERNAL_REVIEW_RESPONSE.md",
        "EXTERNAL_REPAIR_FOLLOWUP_RESPONSE.md",
        "EXTERNAL_REVIEW_TRANSMISSION.md",
        "PREREGISTRATION_EXECUTION_NOTE.md",
        "FROZEN_PREREGISTRATION_HASHES.tsv",
        "FROZEN_SOURCE_HASHES.tsv",
        "SOURCE_SCOPE.tsv",
        "EXACT_DERIVATION.md",
        "LAY_REPORT.md",
        "COMPLETENESS_MAP.md",
        "STATUS_LEDGER.tsv",
        "AUDIT_REPORT.md",
        "EVIDENCE_GATES.md",
        "RUN_RECORD.md",
        "DERIVATION_RESULT.json",
        "INDEPENDENT_VERIFICATION.json",
        "CATCH_PROOF_RESULT.json",
        "derive_clock_rate_readout.py",
        "verify_clock_rate_readout_independent.py",
        "run_catch_proofs.py",
    ]
    gate("required_files", all((PACKAGE / name).is_file() for name in required))

    with (PACKAGE / "FROZEN_PREREGISTRATION_HASHES.tsv").open(newline="") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
    gate("four_frozen_preregistration_files", len(rows) == 4)
    gate(
        "frozen_preregistration_hashes",
        all(digest(PACKAGE / row["path"]) == row["sha256"] for row in rows),
    )

    with (PACKAGE / "FROZEN_SOURCE_HASHES.tsv").open(newline="") as handle:
        source_rows = list(csv.DictReader(handle, delimiter="\t"))
    gate("five_frozen_sources", len(source_rows) == 5)
    gate(
        "frozen_source_hashes",
        all(digest(REPO / row["path"]) == row["sha256"] for row in source_rows),
    )

    before = snapshot()
    production = run_json("derive_clock_rate_readout.py")
    independent = run_json("verify_clock_rate_readout_independent.py")
    hostile = run_json("run_catch_proofs.py")
    after = snapshot()
    gate("registered_children_no_write", before == after)
    gate("no_bytecode", not any(PACKAGE.rglob("*.pyc")))

    saved_production = json.loads((PACKAGE / "DERIVATION_RESULT.json").read_text())
    saved_independent = json.loads((PACKAGE / "INDEPENDENT_VERIFICATION.json").read_text())
    saved_hostile = json.loads((PACKAGE / "CATCH_PROOF_RESULT.json").read_text())
    gate("saved_production_exact", saved_production == production)
    gate("saved_independent_exact", saved_independent == independent)
    gate("saved_hostile_exact", saved_hostile == hostile)

    gate("production_threshold", production["case_count"] >= 2000)
    gate("production_distinct_states", production["distinct_base_states"] == production["case_count"])
    gate("production_all_pass", production["checks_passed"] == production["checks_total"])
    gate("production_p_one", production["frequency_weight_for_clock_rate"] == 1)
    gate("production_q_minus_one", production["area_weight_for_regular_density"] == -1)
    gate("production_phase_scale", production["phase_rescaling_cancels"])
    gate("production_continuous_not_atomic", production["continuous_phase_intensity"] and not production["literal_discrete_instantaneous_rate_claimed"])
    gate("production_nonnegative_product", production["product_measure_nonnegative"])
    gate("production_explicit_supplied_factorization", production["phase_label_factorization_explicit_and_supplied"] and not production["phase_label_factorization_derived_from_g351"])
    gate("production_observer_weight", production["observer_covariance_weight"] == 1)
    gate("production_no_universal_p", not production["universal_p_selected"])
    gate("production_p0_retained", production["observer_neutral_p0_retained"])
    gate("production_no_source_creation", not production["source_or_population_generated"])
    gate("production_no_light_energy", not production["light_or_energy_identified"])

    gate("independent_threshold", independent["checks_total"] >= 10000)
    gate("independent_distinct_states", independent["distinct_base_states"] == independent["case_count"])
    gate("independent_all_pass", independent["checks_passed"] == independent["checks_total"])
    gate("independent_method", independent["method"] == "independent_additive_log_coordinate_reconstruction")
    gate("independent_no_import", not independent["imports_production"])
    gate("independent_no_result_read", not independent["reads_production_result"])
    gate("independent_p_one", independent["typed_frequency_weight"] == 1)
    gate("independent_q_minus_one", independent["typed_area_weight"] == -1)
    gate("independent_no_universal_p", not independent["universal_p_selected"])
    gate("independent_continuous_not_atomic", independent["continuous_phase_intensity"] and not independent["literal_discrete_instantaneous_rate_claimed"])
    gate("independent_nonnegative_product", independent["product_measure_nonnegative"])
    gate("independent_explicit_supplied_factorization", independent["phase_label_factorization_explicit_and_supplied"])

    gate("hostile_all_caught", hostile["mutations_caught"] == hostile["mutations_total"] >= 10)
    gate("hostile_regression_scope", hostile["semantic_regression_only"])

    exact_text = (PACKAGE / "EXACT_DERIVATION.md").read_text()
    lay_text = (PACKAGE / "LAY_REPORT.md").read_text()
    adoption_text = (PACKAGE / "ADOPTION_RECORD.md").read_text()
    gate("adoption_provisional", "OWNER_ADOPTED_PROVISIONAL_PREMISE" in adoption_text)
    gate("phase_sign_repaired", "abs(dTheta/dtau)/DeltaTheta" in (PACKAGE / "R1_PREREGISTRATION_SIGN_REPAIR.md").read_text())
    gate("external_repairs_preregistered", "PREREGISTERED_BEFORE_REPAIR_EXECUTION" in (PACKAGE / "R2_PREREGISTRATION_EXTERNAL_REVIEW_REPAIRS.md").read_text())
    gate("external_repair_verdict_banked", (PACKAGE / "EXTERNAL_REVIEW_RESPONSE.md").read_text().rstrip().endswith("REPAIR_G352_BOUNDED_CLOCK_RATE_READOUT"))
    gate("external_r2_acceptance_banked", (PACKAGE / "EXTERNAL_REPAIR_FOLLOWUP_RESPONSE.md").read_text().rstrip().endswith("ACCEPT_G352_R2_REPAIR_COMPLETION"))
    gate("exact_nonuniversal", "not selection of one\nuniversal observer weight" in exact_text)
    gate("exact_phase_domain", "continuous phase-intensity realization" in exact_text)
    gate("exact_continuous_atomic_split", "literal atomic crossing count" in exact_text)
    gate("exact_total_variation_product", "|d\\Theta|" in exact_text and "product measurable space" in exact_text)
    gate("lay_no_light_promotion", "not identify the crossings as light" in lay_text)
    gate("lay_p0_retained", "`p=0`" in lay_text)

    result = {
        "aggregate_checks_passed": len(checks),
        "aggregate_checks_total": len(checks),
        "checks": checks,
        "production_checks": production["checks_total"],
        "independent_checks": independent["checks_total"],
        "hostile_mutations": hostile["mutations_total"],
        "review_status": "EXTERNALLY_ACCEPTED_R2_REPAIR_COMPLETION",
        "status": "PASS",
    }
    if os.environ.get("UDT_NO_WRITE") != "1":
        OUTPUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
