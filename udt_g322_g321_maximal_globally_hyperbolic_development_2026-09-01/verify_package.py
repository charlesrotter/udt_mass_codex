#!/usr/bin/env python3
"""Aggregate verification for the G322 theorem-interface package."""

import ast
import csv
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
LANDING = (
    "FIXED_G321_DATA_HAVE_CONDITIONAL_UNIQUE_MAXIMAL_GLOBALLY_HYPERBOLIC_"
    "DEVELOPMENTS__MAXIMALITY_IS_PER_DATUM_AND_NOT_COMPLETENESS_OR_OCCUPANCY"
)
OWNERSHIP = (
    "MAXIMAL_GLOBALLY_HYPERBOLIC_DEVELOPMENT__CONDITIONAL_ON_IMPORTED_"
    "CHOQUET_BRUHAT_GEROCH_THEOREM"
)
SCOPE = (
    "NO_CLAIM__GEODESIC_COMPLETENESS_OR_SINGULARITY_FREEDOM_OR_PHYSICAL_"
    "OCCUPANCY_OR_UNMARKED_CLASSIFICATION"
)
REQUIRED = (
    "MAP.md", "PREREGISTRATION.md", "PREMISE_LEDGER.tsv", "SOURCE_SCOPE.tsv",
    "COMPLETENESS_MAP.md", "PREREGISTRATION_ANCESTRY.md", "SOURCE_NOTE.md",
    "EXACT_DERIVATION.md", "AUDIT_REPORT.md", "LAY_REPORT.md", "EVIDENCE_GATES.md",
    "STATUS_LEDGER.tsv", "RUN_RECORD.md", "REPLAY_COMMANDS.txt", "DATA_INTERFACE.tsv",
    "THEOREM_INTERFACE.tsv", "SCOPE_MATRIX.tsv", "DERIVATION_RESULT.json",
    "INDEPENDENT_VERIFICATION.json", "derive_maximal_development.py",
    "verify_independent.py", "run_catch_proofs.py", "verify_package.py",
    "build_review_intake.py", "EXTERNAL_REVIEW_REQUEST.md",
    "S09_PRIMARY_ABSTRACT_EVIDENCE.json", "REPAIR_LEDGER.tsv",
    "EXTERNAL_REVIEW_RESPONSE.md", "EXTERNAL_REPAIR_FOLLOWUP_REQUEST.md",
    "build_repair_followup_intake.py", "EXTERNAL_REPAIR_FOLLOWUP_RESPONSE.md",
    "EXTERNAL_REPAIR_FOLLOWUP_TRANSMISSION.md", "REPAIR_PREREGISTRATION_ANCESTRY.md",
)
ALLOWED_IMPORTS = {
    "ast", "csv", "fractions", "hashlib", "json", "math", "pathlib", "shutil",
    "subprocess", "sys", "tempfile",
}
EXPECTED_INTERFACE = {
    "H1": "SUPPORTED_BOUNDED",
    "H2": "SUPPORTED_BOUNDED",
    "H3": "SUPPORTED_BOUNDED",
    "H4": "SUPPORTED_BOUNDED",
    "H5": "CONDITIONAL_IMPORTED",
    "H6": "IMPORTED_DEFINITION",
    "H7": "IMPORTED_DEFINITION",
    "H8": "CONDITIONAL_IMPORTED",
}
EXPECTED_SCOPE = {
    "maximal_GH_exists_per_fixed_datum": "CONDITIONAL_IMPORTED_THEOREM_CONSEQUENCE",
    "every_same_datum_GH_development_embeds": "CONDITIONAL_IMPORTED_THEOREM_CONSEQUENCE",
    "same_datum_maximal_developments_isometric": "CONDITIONAL_IMPORTED_THEOREM_CONSEQUENCE",
    "geodesic_completeness": "OPEN_NOT_ENTAILED",
    "singularity_or_curvature_control": "OPEN_NOT_ENTAILED",
    "arbitrary_Lorentzian_inextendibility": "OPEN_NOT_ENTAILED",
    "stability": "OPEN_NOT_TESTED",
    "unmarked_cross_datum_spacetime_identity": "OPEN_NOT_CLASSIFIED",
    "physical_initial_data_occupancy": "OPEN_NOT_SELECTED",
    "metric_kernel_angular_interface": "UNCHANGED",
}


def require(condition, message):
    if not condition:
        raise AssertionError(message)


mutation_probe = (HERE / ".g322_mutation_probe").is_file()
for name in REQUIRED:
    require((HERE / name).is_file(), f"missing {name}")
if not mutation_probe:
    require((HERE / "CATCH_PROOF_RESULT.json").is_file(), "missing CATCH_PROOF_RESULT.json")

production = json.loads((HERE / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
independent = json.loads((HERE / "INDEPENDENT_VERIFICATION.json").read_text(encoding="utf-8"))
require(production["landing"] == LANDING, "landing drift")
require(production["status"] == "PASS_PENDING_INDEPENDENT_AND_EXTERNAL_REVIEW", "production status drift")
require(production["raw_tracefree_principal_rank"] == 9, "raw rank drift")
require(production["fixed_lambda_principal_rank"] == 10, "fixed rank drift")
require(production["constraint_sector"] == "Lambda=0", "constraint sector drift")
require(production["max_hamiltonian_residual"] < 5e-12, "production Hamiltonian")
require(production["max_momentum_residual"] < 5e-12, "production momentum")
require(
    production["theorem_interface_status"]
    == "CONDITIONAL_APPLICATION_SUPPORTED__IMPORTED_THEOREM_NOT_MACHINE_PROVED",
    "theorem import boundary drift",
)
require(
    production["maximal_GH_per_fixed_datum"]
    == "CONDITIONAL_IMPORTED_THEOREM_CONSEQUENCE",
    "maximal conclusion drift",
)
require(production["geodesic_completeness"] == "OPEN_NOT_ENTAILED", "completeness overclaim")
require(
    production["arbitrary_Lorentzian_inextendibility"] == "OPEN_NOT_ENTAILED",
    "inextendibility overclaim",
)
require(production["physical_occupancy"] == "OPEN_NOT_SELECTED", "occupancy overclaim")
require(
    production["unmarked_cross_datum_classification"] == "OPEN_NOT_CLASSIFIED",
    "unmarked classification overclaim",
)
require(production["metric_kernel_angular_interface"] == "UNCHANGED", "metric/kernel regression")

require(independent["status"] == "PASS_INDEPENDENT", "independent status")
require(not independent["production_imported"], "independent imported production")
require(not independent["production_output_read"], "independent read production output")
require(independent["max_hamiltonian_residual"] < 6e-12, "independent Hamiltonian")
require(independent["max_momentum_residual"] < 6e-12, "independent momentum")
require(independent["max_ricci_formula_error"] < 3e-13, "independent Ricci")
require(independent["max_time_reversal_error"] < 6e-12, "independent time reversal")
require(
    independent["maximal_development_conclusion"]
    == "UPHELD_CONDITIONAL_ON_IMPORTED_THEOREM",
    "independent theorem boundary",
)
require(independent["completeness_or_occupancy_claim"] == "NONE", "independent overclaim")

with (HERE / "DATA_INTERFACE.tsv").open(encoding="utf-8", newline="") as handle:
    atlas = list(csv.DictReader(handle, delimiter="\t"))
require(len(atlas) == 8, "data interface row count")
base = float(next(row for row in atlas if row["mode"] == "1" and row["sign"] == "1")["Q_R"])
for row in atlas:
    mode = int(row["mode"])
    require(float(row["max_hamiltonian"]) < 5e-12, "atlas Hamiltonian")
    require(float(row["max_momentum"]) < 5e-12, "atlas momentum")
    require(abs(float(row["Q_R"]) / base - mode ** 2) < 5e-12, "atlas Q_R")

with (HERE / "THEOREM_INTERFACE.tsv").open(encoding="utf-8", newline="") as handle:
    interface = {row["id"]: row for row in csv.DictReader(handle, delimiter="\t")}
require({key: row["status"] for key, row in interface.items()} == EXPECTED_INTERFACE, "theorem interface drift")
require(all(row["evidence_type"].strip() and row["boundary"].strip() for row in interface.values()), "empty theorem evidence")

with (HERE / "SCOPE_MATRIX.tsv").open(encoding="utf-8", newline="") as handle:
    scope_rows = {row["claim"]: row["status"] for row in csv.DictReader(handle, delimiter="\t")}
require(scope_rows == EXPECTED_SCOPE, "scope matrix drift")

with (HERE / "STATUS_LEDGER.tsv").open(encoding="utf-8", newline="") as handle:
    ledger = {row["object"]: row["status"] for row in csv.DictReader(handle, delimiter="\t")}
require(ledger["Choquet-Bruhat--Geroch theorem"] == "IMPORTED_MATHEMATICAL_METHOD__CONDITIONAL", "theorem ownership")
require(ledger["geodesic completeness"] == "OPEN_NOT_ENTAILED", "ledger completeness")
require(ledger["physical initial-data occupancy"] == "OPEN_NOT_SELECTED", "ledger occupancy")
require(ledger["metric reciprocal kernel angular interface"] == "UNCHANGED", "ledger interface")

for name in ("EXACT_DERIVATION.md", "AUDIT_REPORT.md", "LAY_REPORT.md"):
    normalized = "".join((HERE / name).read_text(encoding="utf-8").split())
    require(LANDING in normalized, f"landing missing from {name}")
    require(OWNERSHIP in normalized, f"ownership missing from {name}")
    require(SCOPE in normalized, f"scope missing from {name}")

source_note = (HERE / "SOURCE_NOTE.md").read_text(encoding="utf-8")
require("10.1007/BF01645389" in source_note, "primary source locator missing")
require("PRIMARY_PUBLISHER_ABSTRACT_METADATA__IMPORTED_MATHEMATICAL_METHOD" in source_note, "source grade drift")

primary = json.loads((HERE / "S09_PRIMARY_ABSTRACT_EVIDENCE.json").read_text(encoding="utf-8"))
fragments = primary["official_abstract_fragments"]
joined_fragments = " ".join(fragments).lower()
require(primary["schema"] == "udt-g322-s09-primary-abstract-bounded-evidence-v1", "primary evidence schema")
require(primary["source_grade"] == "PRIMARY_PUBLISHER_ABSTRACT_BOUNDED_EXCERPT", "primary evidence grade")
require(primary["doi"] == "10.1007/BF01645389", "primary evidence DOI")
require(sum(len(fragment.split()) for fragment in fragments) == primary["bounded_excerpt_word_count"] == 25, "primary excerpt word count")
require("constraint conditions" in joined_fragments, "primary constraint antecedent")
require("extension of every other development" in joined_fragments, "primary extension scope")
require("embedded in exactly one such maximal development" in joined_fragments, "primary unique embedding scope")

registered_commands = (HERE / "REPLAY_COMMANDS.txt").read_text(encoding="utf-8").splitlines()
run_record = (HERE / "RUN_RECORD.md").read_text(encoding="utf-8")
require(len(registered_commands) == 4, "registered command count")
require(all(command in run_record for command in registered_commands), "human run record incomplete")

with (HERE / "REPAIR_LEDGER.tsv").open(encoding="utf-8", newline="") as handle:
    repairs = {row["repair"]: row for row in csv.DictReader(handle, delimiter="\t")}
require(set(repairs) == {"R1", "R2"}, "repair ledger scope")
require(all(row["scientific_landing"] == "UNCHANGED" for row in repairs.values()), "repair changed science")

for script_name in (
    "derive_maximal_development.py", "verify_independent.py", "run_catch_proofs.py",
    "verify_package.py", "build_review_intake.py", "build_repair_followup_intake.py",
):
    tree = ast.parse((HERE / script_name).read_text(encoding="utf-8"))
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imports = [alias.name.split(".")[0] for alias in node.names]
        elif isinstance(node, ast.ImportFrom):
            imports = [(node.module or "").split(".")[0]]
        else:
            continue
        require(all(name in ALLOWED_IMPORTS for name in imports), f"unregistered import in {script_name}: {imports}")

if not mutation_probe:
    catches = json.loads((HERE / "CATCH_PROOF_RESULT.json").read_text(encoding="utf-8"))
    require(catches["status"] == "PASS_ALL_MUTATIONS_CAUGHT", "hostile status")
    require(catches["caught_count"] == catches["expected_count"] == 14, "hostile count")
    require(all(item["verifier_returncode"] != 0 for item in catches["details"]), "hostile survivor")

external_text = (HERE / "EXTERNAL_REVIEW_RESPONSE.md").read_text(encoding="utf-8")
require("G322_REPAIRABLE_DEFECTS__BOUNDED_LANDING_RETAINED" in external_text, "fresh repairable verdict absent")
followup = HERE / "EXTERNAL_REPAIR_FOLLOWUP_RESPONSE.md"
if followup.is_file():
    followup_text = followup.read_text(encoding="utf-8")
    require(
        "G322_REPAIRS_ACCEPTED__CONDITIONAL_MAXIMAL_GLOBALLY_HYPERBOLIC_DEVELOPMENT_PER_FIXED_DATUM_UPHELD"
        in followup_text,
        "repair follow-up acceptance absent",
    )
    package_status = "PASS_EXTERNALLY_ACCEPTED__CONDITIONAL_MAXIMAL_GH_PER_FIXED_DATUM"
else:
    package_status = "PASS_REPAIRED__EXTERNAL_FOLLOWUP_PENDING"

result = {
    "schema": "udt-g322-package-verification-v1",
    "status": package_status,
    "landing": LANDING,
    "required_files": len(REQUIRED) + 1,
    "data_rows": len(atlas),
    "production_assertions": production["machine_assertion_count"],
    "independent_assertions": independent["assertion_count"],
    "hostile_catches": 0 if mutation_probe else catches["caught_count"],
    "primary_excerpt_words": primary["bounded_excerpt_word_count"],
    "repairs_registered": sorted(repairs),
}
with (HERE / "PACKAGE_VERIFICATION_RESULT.json").open("w", encoding="utf-8") as handle:
    json.dump(result, handle, indent=2, sort_keys=True)
    handle.write("\n")
print(json.dumps(result, indent=2, sort_keys=True))
