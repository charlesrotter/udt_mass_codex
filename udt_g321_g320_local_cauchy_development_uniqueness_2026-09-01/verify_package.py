#!/usr/bin/env python3
"""Aggregate G321 package verification."""

import ast
import csv
import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
LANDING = (
    "G320_DATA_HAVE_CONDITIONAL_UNIQUE_LOCAL_MARKED_DEVELOPMENTS__"
    "REGISTERED_BREADTH_IS_ORDINARY_CAUCHY_DATA_FREEDOM_IN_BOUNDED_ARENA__"
    "NO_GLOBAL_OR_OCCUPANCY_SELECTION"
)
THEOREM_STAMP = (
    "LOCAL_GEOMETRIC_UNIQUENESS__CONDITIONAL_ON_IMPORTED_STANDARD_SMOOTH_"
    "HARMONIC_WELLPOSEDNESS_THEOREM"
)
SCOPE_STAMP = (
    "NO_CLAIM__GLOBAL_HISTORY_OR_PHYSICAL_OCCUPANCY_OR_UNMARKED_"
    "SPACETIME_CLASSIFICATION"
)
EXPECTED_HYPOTHESIS_STATUSES = {
    "H1_initial_manifold": "DECLARED_DIAGNOSTIC_DOMAIN__STANDARD_SMOOTH_COMPACT_BOUNDARY_FREE_T3",
    "H2_gamma_regular": "ANALYTICALLY_VERIFIED_ON_REGISTERED_FAMILY",
    "H3_K_regular": "ANALYTICALLY_VERIFIED_ON_REGISTERED_REGULAR_BRANCH",
    "H4_constraints": "ANALYTIC_IDENTITY_WITH_TWO_NUMERICAL_REPLAYS",
    "H5_connected_scalar_sector": "DERIVED_FROM_HAMILTONIAN_VALUE",
    "H6_full_principal_operator": "EXACT_LINEAR_ALGEBRA_AUDIT",
    "H7_gauge_constraint_propagation": "FORMAL_BIANCHI_CONSEQUENCE__THEOREM_APPLICATION_REMAINS_IMPORTED",
    "H8_gauge_quotient": "IMPORTED_STANDARD_GEOMETRIC_CAUCHY_INTERFACE",
}
REQUIRED = (
    "MAP.md", "PREMISE_LEDGER.tsv", "COMPLETENESS_MAP.md", "PREREGISTRATION.md",
    "PREREGISTRATION_ANCESTRY.md", "SOURCE_SCOPE.tsv", "REPLAY_COMMANDS.txt",
    "EXACT_DERIVATION.md", "AUDIT_REPORT.md", "LAY_REPORT.md", "STATUS_LEDGER.tsv",
    "EVIDENCE_GATES.md", "RUN_RECORD.md", "DEVELOPMENT_ATLAS.tsv",
    "DERIVATION_RESULT.json", "INDEPENDENT_VERIFICATION.json", "CATCH_PROOF_RESULT.json",
    "derive_local_development.py", "verify_independent.py", "run_catch_proofs.py",
    "verify_package.py", "build_review_intake.py", "EXTERNAL_REVIEW_REQUEST.md",
    "EXTERNAL_REVIEW_RESPONSE.md", "EXTERNAL_REVIEW_CLI_FINAL.md",
    "EXTERNAL_REVIEW_TRANSCRIPT.txt", "EXTERNAL_REVIEW_TRANSMISSION.md",
    "REPAIR_FOLLOWUP_REQUEST.md", "build_repair_followup_intake.py",
    "EXTERNAL_REPAIR_FOLLOWUP_RESPONSE.md", "EXTERNAL_REPAIR_FOLLOWUP_CLI_FINAL.md",
    "EXTERNAL_REPAIR_FOLLOWUP_TRANSCRIPT.txt", "EXTERNAL_REPAIR_FOLLOWUP_TRANSMISSION.md",
)
ALLOWED_IMPORTS = {
    "ast", "csv", "fractions", "hashlib", "json", "math", "pathlib", "shutil",
    "subprocess", "sys", "tempfile",
}


def require(condition, message):
    if not condition:
        raise AssertionError(message)


for name in REQUIRED:
    require((HERE / name).is_file(), f"missing {name}")

production = json.loads((HERE / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
independent = json.loads((HERE / "INDEPENDENT_VERIFICATION.json").read_text(encoding="utf-8"))
catches = json.loads((HERE / "CATCH_PROOF_RESULT.json").read_text(encoding="utf-8"))
mutation_probe = (HERE / ".g321_mutation_probe").is_file()
require(production["landing"] == LANDING, "landing drift")
require(production["local_geometric_uniqueness"] == "CONDITIONAL_ON_IMPORTED_STANDARD_THEOREM", "conditional theorem caveat lost")
require(production["raw_tracefree_principal_rank"] == 9, "raw rank")
require(production["fixed_lambda_principal_rank"] == 10, "completed rank")
require(production["constraint_sector"] == "Lambda=0", "sector")
require(production["theorem_interface_status"] == "AUDITED_CONDITIONAL__NOT_MACHINE_PROVED_IN_FULL", "theorem interface type")
require(
    {key: value["status"] for key, value in production["theorem_hypothesis_audit"].items()}
    == EXPECTED_HYPOTHESIS_STATUSES,
    "theorem hypothesis ledger drift",
)
require(all(value["evidence"].strip() for value in production["theorem_hypothesis_audit"].values()), "empty theorem evidence")
require(not production["lapse_shift_are_physical_data"], "gauge variables promoted to physical data")
require(production["initial_adm_rhs_single_valued_after_gauge_fix"], "initial ADM response lost")
require(production["opposite_signs_are_distinct_full_data"], "K sign branches collapsed")
require(production["opposite_signs_are_time_reversed_data"], "time reversal field")
require(production["different_modes_distinct_as_marked_developments"], "marked mode separation field")
require(not production["physical_initial_data_selected"], "data selection overclaim")
require(not production["global_history_selected"], "global history overclaim")
require(not production["unmarked_same_spacetime_different_slice_classified"], "unmarked quotient overclaim")
require(not production["metric_or_kernel_changed"], "metric/kernel regression")
require(independent["status"] == "PASS_INDEPENDENT", "independent status")
require(not independent["production_imported"], "independent imports production")
require(not independent["production_output_read"], "independent reads production result")
require(independent["max_hamiltonian_residual"] < 5e-12, "independent Hamiltonian")
require(independent["max_momentum_residual"] < 5e-12, "independent momentum")
require(independent["max_time_reversal_error"] < 5e-12, "time reversal")
if not mutation_probe:
    require(catches["status"] == "PASS_ALL_MUTATIONS_CAUGHT", "catch status")
    require(catches["caught_count"] == catches["expected_count"] == 12, "catch count")
    require(catches["mutation_method"] == "EPHEMERAL_PACKAGE_MUTATION_THEN_AGGREGATE_VERIFIER_REJECTION", "hostile method")
    require(all(item["verifier_returncode"] != 0 for item in catches["details"]), "a hostile mutation survived verifier")

with (HERE / "DEVELOPMENT_ATLAS.tsv").open(encoding="utf-8", newline="") as handle:
    atlas = list(csv.DictReader(handle, delimiter="\t"))
require(len(atlas) == 8, "atlas row count")
base = float(next(row for row in atlas if row["mode"] == "1" and row["sign"] == "1")["Q_R"])
for row in atlas:
    mode = int(row["mode"])
    require(float(row["max_hamiltonian"]) < 5e-12, "atlas Hamiltonian")
    require(float(row["max_momentum"]) < 5e-12, "atlas momentum")
    require(abs(float(row["Q_R"]) / base - mode ** 2) < 5e-12, "atlas Q_R ratio")

for script_name in ("derive_local_development.py", "verify_independent.py", "run_catch_proofs.py", "verify_package.py", "build_review_intake.py", "build_repair_followup_intake.py"):
    tree = ast.parse((HERE / script_name).read_text(encoding="utf-8"))
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imports = [alias.name.split(".")[0] for alias in node.names]
        elif isinstance(node, ast.ImportFrom):
            imports = [(node.module or "").split(".")[0]]
        else:
            continue
        require(all(name in ALLOWED_IMPORTS for name in imports), f"unregistered import in {script_name}: {imports}")

for name in ("EXACT_DERIVATION.md", "AUDIT_REPORT.md", "LAY_REPORT.md"):
    report_text = (HERE / name).read_text(encoding="utf-8")
    require(LANDING in report_text.replace("\n", ""), f"exact landing missing from {name}")
    require(THEOREM_STAMP in report_text.replace("\n", ""), f"exact theorem ownership stamp missing from {name}")
    require(SCOPE_STAMP in report_text.replace("\n", ""), f"exact scope stamp missing from {name}")

with (HERE / "STATUS_LEDGER.tsv").open(encoding="utf-8", newline="") as handle:
    status_rows = {row["object"]: row for row in csv.DictReader(handle, delimiter="\t")}
require(status_rows["standard local wellposedness"]["status"] == "IMPORTED_MATHEMATICAL_METHOD__CONDITIONAL", "wellposedness ownership drift")
require(status_rows["unmarked same-spacetime relation"]["status"] == "OPEN", "unmarked classification drift")
require(status_rows["physical data occupancy"]["status"] == "OPEN_NOT_SELECTED", "occupancy drift")
require(status_rows["global history existence stability"]["status"] == "OPEN", "global history drift")

external_review = (HERE / "EXTERNAL_REVIEW_RESPONSE.md").read_text(encoding="utf-8")
require("G321_REPAIRABLE_DEFECTS__BOUNDED_LANDING_RETAINED" in external_review, "fresh review verdict not preserved")
transmission = (HERE / "EXTERNAL_REVIEW_TRANSMISSION.md").read_text(encoding="utf-8")
require("aeda3727b7ff5e66c5ec7a0da9363c84ec6084245006c2fec5d421cc97654202" in transmission, "fresh scope hash missing")
require("c9c50ccec969cb9911b1ce197cc129fbbbd26d51e40c32305d2617ed72789bd9" in transmission, "fresh manifest hash missing")

followup_response = HERE / "EXTERNAL_REPAIR_FOLLOWUP_RESPONSE.md"
followup_cli = HERE / "EXTERNAL_REPAIR_FOLLOWUP_CLI_FINAL.md"
followup_transcript = HERE / "EXTERNAL_REPAIR_FOLLOWUP_TRANSCRIPT.txt"
require(hashlib.sha256(followup_response.read_bytes()).hexdigest() == "1c37a3bd4ef2674bf356b92c3511e01f1d6432836286121483c1a02ece74af58", "followup response byte drift")
require(hashlib.sha256(followup_cli.read_bytes()).hexdigest() == "7ceb79e58ea9a11f134985b96604dfee4695fb6d6a497494b7444b23ea903aec", "followup CLI byte drift")
require(hashlib.sha256(followup_transcript.read_bytes()).hexdigest() == "6c796cb5e6b52b092120ad0d85a93d24e359493b0129b7e66f4c69cd6fc43208", "followup transcript byte drift")
require("G321_REPAIRS_ACCEPTED__CONDITIONAL_LOCAL_MARKED_UNIQUENESS_UPHELD" in followup_response.read_text(encoding="utf-8"), "followup acceptance missing")
followup_transmission = (HERE / "EXTERNAL_REPAIR_FOLLOWUP_TRANSMISSION.md").read_text(encoding="utf-8")
require("9e4f58351c9f1b6cce976c4104641314d361d3abe03c11a2d3c87c6b643b99f6" in followup_transmission, "followup scope hash missing")
require("6b09326c49976134e968c50fdcf634f985e9c0e4751aebb15dedce5e81e35d1a" in followup_transmission, "followup manifest hash missing")

result = {
    "schema": "udt-g321-package-verification-v1",
    "status": "PASS_EXTERNALLY_ACCEPTED__CONDITIONAL_LOCAL_MARKED_UNIQUENESS",
    "landing": LANDING,
    "required_files": len(REQUIRED),
    "atlas_rows": len(atlas),
    "production_assertions": production["assertion_count"],
    "independent_assertions": independent["assertion_count"],
    "hostile_catches": catches["caught_count"],
}
with (HERE / "PACKAGE_VERIFICATION_RESULT.json").open("w", encoding="utf-8") as handle:
    json.dump(result, handle, indent=2, sort_keys=True)
    handle.write("\n")
print(json.dumps(result, indent=2, sort_keys=True))
