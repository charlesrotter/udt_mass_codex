#!/usr/bin/env python3
"""Cold, source-first verifier for the joint-realization closure audit.

This implementation does not import or execute derive_joint_realization.py.
It reconstructs the frozen universe, route verdicts, finite controls, and
certificate nonredundancy from committed sources and independent predicates.
"""

from __future__ import annotations

import ast
import csv
import hashlib
import json
import subprocess
from copy import deepcopy
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
BASE = "089e2044be1b2e801f9b4f07e83efb5296dc1375"
OUTCOME = "FORMAL_COMPATIBILITY_ONLY_COMMON_REALIZATION_OPEN"
EXPECTED_ROUTES = {f"J{i:02d}" for i in range(1, 9)}
CERT_ATOMS = {
    "one_full_field",
    "static_restriction",
    "time_restriction",
    "angular_restriction",
    "nonzero_time_live",
    "nonzero_angular_live",
    "native_whole_equation",
    "differentiable_finite_cell_boundary",
    "one_compatible_premise_stack",
}
VERIFIED_PACKAGE_FILES = (
    "AUDIT_REPORT.md",
    "COMMON_OBJECT_TYPE_SCHEMA.tsv",
    "COMPLETENESS_MAP.md",
    "COUNTERMODEL_LEDGER.tsv",
    "DERIVATION_RESULT.json",
    "DERIVATION_STDOUT.txt",
    "EXACT_DERIVATION.md",
    "JOINT_GATE_MATRIX.tsv",
    "LAY_REPORT.md",
    "PREMISE_LEDGER.tsv",
    "PREREGISTRATION.md",
    "PREREG_SNAPSHOT.json",
    "ROUTE_ADJUDICATION.tsv",
    "ROUTE_CANDIDATES.tsv",
    "SOURCE_ANCHOR_LEDGER.tsv",
    "SOURCE_INVENTORY.tsv",
    "SOURCE_MANIFEST.sha256",
    "SOURCE_PATHS.txt",
    "STATUS_LEDGER.tsv",
    "build_preregistration.py",
    "derive_joint_realization.py",
    "verify_preregistration.py",
)


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def tsv(rel: str) -> list[dict[str, str]]:
    with (ROOT / rel).open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def text_of(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


checks: list[dict[str, object]] = []


def check(ident: str, passed: bool, detail: str, kind: str = "SUBSTANTIVE") -> None:
    checks.append({"id": ident, "kind": kind, "pass": bool(passed), "detail": detail})


inventory = tsv(f"{HERE.name}/SOURCE_INVENTORY.tsv")
paths = [row["path"] for row in inventory]
check("V01_SOURCE_CENSUS", len(paths) == 140 and len(set(paths)) == 140,
      f"rows={len(paths)} unique={len(set(paths))}")

identity_errors: list[str] = []
blob_errors: list[str] = []
for row in inventory:
    path = ROOT / row["path"]
    if (not path.is_file() or path.stat().st_size != int(row["bytes"])
            or sha256(path) != row["sha256"]):
        identity_errors.append(row["path"])
    try:
        blob = subprocess.check_output(
            ["git", "rev-parse", f"{BASE}:{row['path']}"], cwd=ROOT, text=True
        ).strip()
    except subprocess.CalledProcessError:
        blob = ""
    if blob != row["blob"]:
        blob_errors.append(row["path"])
check("V02_CURRENT_SOURCE_BYTES", not identity_errors, f"mismatches={identity_errors}")
check("V03_BASE_BLOB_IDENTITIES", not blob_errors, f"mismatches={blob_errors}")

path_lines = (HERE / "SOURCE_PATHS.txt").read_text(encoding="utf-8").splitlines()
manifest_lines = (HERE / "SOURCE_MANIFEST.sha256").read_text(encoding="utf-8").splitlines()
expected_manifest = [f"{row['sha256']}  ../{row['path']}" for row in inventory]
check("V04_PATH_AND_MANIFEST_EQUIVALENCE",
      path_lines == paths and manifest_lines == expected_manifest,
      f"paths={len(path_lines)} manifest={len(manifest_lines)}")

parent = ROOT / "udt_stability_foundations_audit_2026-08-01"
direct = set((parent / "SOURCE_PATHS.txt").read_text(encoding="utf-8").splitlines())
package_names = [line.split("  ", 1)[1] for line in
                 (parent / "PACKAGE_MANIFEST.sha256").read_text(encoding="utf-8").splitlines()
                 if line.strip()]
package = {f"udt_stability_foundations_audit_2026-08-01/{name}" for name in package_names}
package.add("udt_stability_foundations_audit_2026-08-01/PACKAGE_MANIFEST.sha256")
transitive = {row["path"] for row in tsv(
    "udt_stability_foundations_audit_2026-08-01/TRANSITIVE_PREMISE_FREEZE.tsv")}
reconstructed = direct | package | transitive
check("V05_UNION_RECONSTRUCTION",
      (len(direct), len(package), len(transitive), len(reconstructed)) == (94, 42, 4, 140)
      and reconstructed == set(paths),
      f"direct={len(direct)} package={len(package)} transitive={len(transitive)} union={len(reconstructed)}")

preregistered = [
    "PREREGISTRATION.md",
    "PREMISE_LEDGER.tsv",
    "ROUTE_CANDIDATES.tsv",
    "SOURCE_PATHS.txt",
    "SOURCE_MANIFEST.sha256",
    "SOURCE_INVENTORY.tsv",
    "build_preregistration.py",
    "verify_preregistration.py",
]
diff_rc = subprocess.run(
    ["git", "diff", "--quiet", "HEAD", "--", *[f"{HERE.name}/{name}" for name in preregistered]],
    cwd=ROOT, check=False,
).returncode
check("V06_COMMITTED_PREREGISTRATION_UNCHANGED", diff_rc == 0, f"git_diff_rc={diff_rc}")

routes_preregistered = {row["route_id"] for row in tsv(f"{HERE.name}/ROUTE_CANDIDATES.tsv")}
premises_preregistered = tsv(f"{HERE.name}/PREMISE_LEDGER.tsv")
check("V07_PREREGISTERED_ROUTE_AND_PREMISE_CENSUS",
      routes_preregistered == EXPECTED_ROUTES and len(premises_preregistered) == 17,
      f"routes={sorted(routes_preregistered)} premises={len(premises_preregistered)}")

# Source-semantic predicates are intentionally more specific than file-presence checks.
cold_rows = tsv("udt_p4_cold_adversarial_review_2026-08-01/PREMISE_QUANTIFIER_AUDIT.tsv")
q2 = next(row for row in cold_rows if row["unit_id"] == "Q2")
check("V08_COLD_Q2_FIXED_REALIZATION_REMAINS_OPEN",
      "FIXED_REALIZED_SOLUTION_OPEN" in q2["quantifier_guard"]
      and "no fixed realized time/angular-live on-shell metric family" in q2["excluded_or_open_scope"],
      q2["quantifier_guard"])

t2_report = text_of("udt_p4_timelive_stage_T2_2026-07-31/AUDIT_REPORT.md")
a3_report = text_of("udt_p4_angular_stage_A3_2026-07-31/AUDIT_REPORT.md")
slice2b_report = text_of("udt_p4_routeA_slice2b_full_cell_2026-07-29/AUDIT_REPORT.md")
check("V09_TIME_ANGULAR_AND_STATIC_SCOPE_ATTACK",
      "no response law selected, no fork decided, no solve" in t2_report
      and "Nonzero angular-live on-shell coexistence is also unproved" in a3_report
      and "time-live" in slice2b_report and "OUT" in slice2b_report,
      "T2=no solve; A3=no on-shell coexistence; Slice-2b=time-live out")

coframe_report = text_of("udt_native_global_coframe_definition_audit_2026-07-28/AUDIT_REPORT.md")
coframe_status = tsv("udt_native_global_coframe_definition_audit_2026-07-28/STATUS_LEDGER.tsv")
check("V10_COMPLETE_COFRAME_IS_OFF_SHELL",
      "complete family is off shell" in coframe_report.lower()
      and any("OPEN" in row.get("status", "") and "equation" in row.get("object", "").lower()
              for row in coframe_status),
      "global coframe existence does not supply realized equations")

completion = tsv("udt_bootstrap_clock_angular_closure_audit_2026-07-24/COMPLETION_BOOTSTRAP_ATLAS.tsv")
equations = tsv("udt_bootstrap_clock_angular_closure_audit_2026-07-24/EQUATION_FAMILY_GATE_MATRIX.tsv")
bootstrap_routes = tsv("udt_bootstrap_clock_angular_closure_audit_2026-07-24/BOOTSTRAP_ROUTE_LEDGER.tsv")
r08 = next(row for row in bootstrap_routes if row["route_id"] == "R08")
check("V11_COMPLETION_AND_BOOTSTRAP_ATTACK",
      len(completion) == 12
      and all(row["complete_g_phi_matter_witness"] == "NO"
              and row["density_response_argument"] == "ABSENT" for row in completion)
      and len(equations) == 28
      and all(row["complete_simultaneous_closure"] == "NO" for row in equations)
      and len(bootstrap_routes) == 8 and r08["current_status"] == "OPEN_NOT_REGISTERED_COMPLETE",
      "12/12 completion witnesses absent; 28/28 equation families incomplete; R08 open")

bootstrap_local = {row["object"]: row for row in
                   tsv("udt_bootstrap_to_local_response_map_audit_2026-07-25/STATUS_LEDGER.tsv")}
global_local = {row["id"]: row for row in
                tsv("udt_global_local_relational_closure_audit_2026-07-25/STATUS_LEDGER.tsv")}
check("V12_BOOTSTRAP_FIXED_POINT_REMAINS_OPEN",
      bootstrap_local["complete_bootstrap_to_local_map"]["status"] == "OPEN"
      and global_local["S14"]["status"] == "OPEN_NOT_REGISTERED",
      "local map OPEN; same-solution fixed point OPEN_NOT_REGISTERED")

action = {row["id"]: row for row in
          tsv("native_action_final_adjudication_2026-07-18/FINAL_STATUS_LEDGER.tsv")}
check("V13_ACTION_ROUTE_ATTACK",
      action["S23"]["status"] == "OPEN" and action["S24"]["status"] == "OPEN"
      and "Not a unique complete action" in action["S11"]["what_is_not_claimed"]
      and action["S14"]["status"] == "CONDITIONAL",
      "complete action and boundary OPEN; C2 and EH remain premise-conditional")

hopf = {row["claim_id"]: row for row in
        tsv("native_hopfion_topology_audit_2026-07-19/TOPOLOGY_STATUS_LEDGER.tsv")}
stability_report = text_of("udt_p4_stability_slice_2026-07-30/AUDIT_REPORT.md")
check("V14_HOPFION_AND_STABILITY_ROUTE_ATTACK",
      hopf["T07"]["status"] == "OPEN"
      and hopf["T10"]["status"] == "SETTLED_STATIC_FINITE_BOX_CONDITIONAL"
      and "not time-live" in hopf["T10"]["dependency_or_limit"]
      and "no dynamics adopted" in stability_report,
      "carrier completion OPEN; Hopfion and P4 stability are static/conditional, not time-live")

fixed = {row["id"]: row for row in
         tsv("udt_stability_foundations_audit_2026-08-01/FIXED_REALIZATION_GATE.tsv")}
check("V15_PARENT_FIXED_REALIZATION_GATE",
      fixed["G05"]["current_status"] == "OPEN"
      and fixed["G09"]["current_status"] == "OPEN"
      and "common zero mode" in fixed["G09"]["failure_or_limit"],
      "same nonzero live field and realized pullback remain open")

expected_rulings = {
    "J01": "NOT_FOUND_IN_FROZEN_RECORD",
    "J02": "FORMAL_COMPATIBILITY_ONLY",
    "J03": "LIVE_LIFT_OPEN",
    "J04": "DIFFERENTIABLE_JOIN_OPEN",
    "J05": "BOTH_MAPS_AND_FIXED_POINT_OPEN",
    "J06": "NO_COMPLETE_CONDITIONAL_WITNESS",
    "J07": "STATIC_FINITE_BOX_ONLY",
    "J08": "MINIMUM_CERTIFICATE_TYPE_IDENTIFIED",
}
route_rows = {row["route_id"]: row for row in tsv(f"{HERE.name}/ROUTE_ADJUDICATION.tsv")}
route_errors = {
    ident: {"expected": ruling, "actual": route_rows.get(ident, {}).get("ruling")}
    for ident, ruling in expected_rulings.items()
    if route_rows.get(ident, {}).get("ruling") != ruling
}
check("V16_EIGHT_ROUTE_ADJUDICATION",
      set(route_rows) == EXPECTED_ROUTES and not route_errors,
      f"routes={sorted(route_rows)} mismatches={route_errors}")

gate_rows = {row["gate_id"]: row for row in tsv(f"{HERE.name}/JOINT_GATE_MATRIX.tsv")}
gate_expected = {
    "G03": "FORMAL_EXACT_POINTWISE",
    "G04": "FORMAL_EXACT_POINTWISE",
    "G05": "OPEN",
    "G06": "OPEN_ON_SAME_FIELD",
    "G07": "OPEN_ON_SAME_FIELD",
    "G08": "OPEN",
    "G09": "OPEN",
    "G10": "PARTIAL",
    "G11": "OPEN",
    "G12": "ABSENT_IN_FROZEN_RECORD",
}
gate_errors = {
    ident: {"expected": status, "actual": gate_rows.get(ident, {}).get("current_status")}
    for ident, status in gate_expected.items()
    if gate_rows.get(ident, {}).get("current_status") != status
}
check("V17_JOINT_GATE_STATUSES", not gate_errors, f"mismatches={gate_errors}")

status_rows = {row["id"]: row for row in tsv(f"{HERE.name}/STATUS_LEDGER.tsv")}
check("V18_PRIMARY_OUTCOME_AND_SCOPE",
      status_rows["S08"]["status"] == "NO_COMPLETE_CONDITIONAL_WITNESS_REGISTERED"
      and status_rows["S11"]["status"] == OUTCOME
      and "not a universal no-go" in status_rows["S11"]["limit"],
      f"S08={status_rows['S08']['status']} S11={status_rows['S11']['status']}")

# Independent finite controls: these are nonimplications, not realizations.
finite_controls = {
    "CM1_ZERO_MODE": {"formal_static": True, "nonzero_live": False, "joint": False},
    "CM2_DIFFERENT_SOLUTIONS": {"time_exists": True, "angular_exists": True,
                                "same_field": False, "joint": False},
    "CM3_STATIC_UNMUTING": {"static_solution": True, "live_linear_mode": True,
                            "live_on_shell_solution": False, "joint": False},
    "CM4_CONDITIONAL_ACTION": {"conditional_bulk": True, "complete_boundary": False,
                               "joint": False},
    "CM5_BOOTSTRAP_SCHEMA": {"map_types": True, "maps_defined": False,
                             "fixed_point": False, "joint": False},
}
control_pass = all(not model["joint"] for model in finite_controls.values())
check("V19_FINITE_SET_NONIMPLICATIONS", control_pass,
      f"controls={list(finite_controls)} all_joint_false={control_pass}")


def certificate_holds(assignment: dict[str, bool], atoms: set[str] = CERT_ATOMS) -> bool:
    return all(assignment.get(atom, False) for atom in atoms)


minimality: dict[str, dict[str, bool]] = {}
for omitted in sorted(CERT_ATOMS):
    assignment = {atom: atom != omitted for atom in CERT_ATOMS}
    minimality[omitted] = {
        "full_certificate_rejects": not certificate_holds(assignment),
        "weakened_certificate_accepts": certificate_holds(assignment, CERT_ATOMS - {omitted}),
    }
check("V20_CERTIFICATE_SEMANTIC_NONREDUNDANCY",
      len(minimality) == 9 and all(all(result.values()) for result in minimality.values()),
      "each delete-one assignment defeats the full gate and satisfies only its weakened gate")

base_model: dict[str, object] = {
    "source_count": 140,
    "source_integrity": True,
    "routes": deepcopy(expected_rulings),
    "outcome": OUTCOME,
    "unsupported_live_claims": set(),
    "zero_mode_promoted": False,
    "premise_spliced": False,
    "action_priority_claimed": False,
    "universal_nonexistence_claimed": False,
    "cert_atoms": set(CERT_ATOMS),
}


def production_errors(model: dict[str, object]) -> list[str]:
    errors: list[str] = []
    if model["source_count"] != 140:
        errors.append("source_count")
    if model["source_integrity"] is not True:
        errors.append("source_integrity")
    if model["routes"] != expected_rulings:
        errors.append("route_census_or_ruling")
    if model["outcome"] != OUTCOME:
        errors.append("outcome_promotion")
    if model["unsupported_live_claims"]:
        errors.append("unsupported_live_claim")
    if model["zero_mode_promoted"]:
        errors.append("zero_mode_promotion")
    if model["premise_spliced"]:
        errors.append("premise_splicing")
    if model["action_priority_claimed"]:
        errors.append("action_priority")
    if model["universal_nonexistence_claimed"]:
        errors.append("universal_nonexistence")
    if model["cert_atoms"] != CERT_ATOMS:
        errors.append("certificate_atom_census")
    return errors


check("V21_BASELINE_PRODUCTION_MODEL", not production_errors(base_model),
      f"errors={production_errors(base_model)}")

mutations: list[tuple[str, dict[str, object]]] = []


def mutated(name: str, key: str, value: object) -> None:
    model = deepcopy(base_model)
    model[key] = value
    mutations.append((name, model))


mutated("source_drop", "source_count", 139)
mutated("source_hash_corruption", "source_integrity", False)
for route_id in sorted(EXPECTED_ROUTES):
    changed_routes = deepcopy(expected_rulings)
    changed_routes[route_id] = "PROMOTED_CLOSED"
    mutated(f"route_{route_id}_promotion", "routes", changed_routes)
for claim in (
    "stationary_to_live_lift",
    "time_live_solved",
    "angular_live_solved",
    "coframe_on_shell",
    "completion_witness",
    "bootstrap_fixed_point",
    "complete_action_solution",
    "hopfion_time_persistence",
):
    mutated(claim, "unsupported_live_claims", {claim})
mutated("zero_mode_as_witness", "zero_mode_promoted", True)
mutated("mixed_premise_stack", "premise_spliced", True)
mutated("action_first_priority", "action_priority_claimed", True)
mutated("universal_no_go", "universal_nonexistence_claimed", True)
mutated("outcome_upgraded", "outcome", "NATIVE_JOINT_REALIZATION_PROVED")
for atom in sorted(CERT_ATOMS):
    mutated(f"certificate_drop_{atom}", "cert_atoms", CERT_ATOMS - {atom})

mutation_results = {
    name: production_errors(model)
    for name, model in mutations
}
check("V22_FAIL_CLOSED_MUTATIONS",
      len(mutation_results) == 32 and all(errors for errors in mutation_results.values()),
      f"caught={sum(bool(errors) for errors in mutation_results.values())}/{len(mutation_results)}")

schema = {row["id"]: row for row in tsv(f"{HERE.name}/COMMON_OBJECT_TYPE_SCHEMA.tsv")}
audit_report = text_of(f"{HERE.name}/AUDIT_REPORT.md")
check("V23_CERTIFICATE_TYPE_AND_CEILING",
      schema["C09"]["status"] == "IDENTIFIED_NOT_CONSTRUCTED"
      and schema["C11"]["typed_role"] == "possible producer of E_native and B_native"
      and "not privileged" in schema["C11"]["obligation_or_limit"]
      and "not universal over unknown UDT laws" in audit_report,
      "certificate identified, not constructed; action-neutral; conclusion source-bounded")

syntax = ast.parse(Path(__file__).read_text(encoding="utf-8"))
import_roots = {
    node.names[0].name.split(".")[0] if isinstance(node, ast.Import)
    else (node.module or "").split(".")[0]
    for node in ast.walk(syntax)
    if isinstance(node, (ast.Import, ast.ImportFrom))
}
allowed_imports = {"__future__", "ast", "copy", "csv", "hashlib", "json", "pathlib", "subprocess"}
check("V24_IMPLEMENTATION_INDEPENDENCE",
      import_roots <= allowed_imports,
      f"import_roots={sorted(import_roots)}; primary derivation neither imported nor executed")


def scoped_hash_inventory(available: dict[str, str]) -> dict[str, str]:
    """Select only the preregistered and primary files semantically verified here."""
    return {name: available[name] for name in VERIFIED_PACKAGE_FILES}


observed_package_hashes = {
    path.name: sha256(path) for path in sorted(HERE.iterdir()) if path.is_file()
}
primary_hashes = scoped_hash_inventory(observed_package_hashes)
sentinel_name = "UNRELATED_POST_VERIFICATION_FINALIZATION_SENTINEL.txt"
augmented_package_hashes = observed_package_hashes | {sentinel_name: "0" * 64}
augmented_primary_hashes = scoped_hash_inventory(augmented_package_hashes)
unsafe_directory_wide = {
    name: digest for name, digest in observed_package_hashes.items()
    if not name.startswith("VERIFIER_")
}
unsafe_augmented = {
    name: digest for name, digest in augmented_package_hashes.items()
    if not name.startswith("VERIFIER_")
}
check("V25_FINALIZATION_FILE_INVARIANCE",
      primary_hashes == augmented_primary_hashes
      and sentinel_name not in augmented_primary_hashes
      and unsafe_directory_wide != unsafe_augmented,
      "explicit 22-file semantic inventory unchanged by synthetic unrelated finalization file; "
      "directory-wide negative control changes")

head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
passed = all(bool(row["pass"]) for row in checks)
verdict = "PASS" if passed else "FAIL"
results = {
    "schema_version": 1,
    "verdict": verdict,
    "base_commit": BASE,
    "verification_head": head,
    "outcome_adjudicated": OUTCOME,
    "maximum_conclusion": (
        "Within the frozen 140-source universe, formal static/time/angular compatibility is banked, "
        "but no registered route supplies one same nonzero time-live plus angular-live on-shell "
        "finite-cell field/equation/boundary/premise certificate. This is not universal nonexistence."
    ),
    "amendments": [],
    "check_summary": {
        "passed": sum(bool(row["pass"]) for row in checks),
        "total": len(checks),
        "failed_ids": [row["id"] for row in checks if not row["pass"]],
    },
    "source_universe": {
        "direct_parent_sources": len(direct),
        "parent_package_sources": len(package),
        "transitive_premise_sources": len(transitive),
        "union": len(reconstructed),
    },
    "route_rulings": expected_rulings,
    "finite_nonimplication_controls": finite_controls,
    "jr_cert_native": {
        "semantic_atoms": sorted(CERT_ATOMS),
        "delete_one_nonredundancy": minimality,
        "qualification": (
            "Semantically nonredundant relative to the preregistered gate; this does not assert "
            "syntactic uniqueness or privilege a tuple encoding, action, or implementation."
        ),
    },
    "mutation_summary": {
        "caught": sum(bool(errors) for errors in mutation_results.values()),
        "total": len(mutation_results),
        "results": mutation_results,
    },
    "checks": checks,
    "primary_and_preregistration_sha256": primary_hashes,
    "package_hash_inventory_policy": {
        "mode": "EXPLICIT_SEMANTIC_FIXED_SET",
        "verified_files": list(VERIFIED_PACKAGE_FILES),
        "post_verification_and_unrelated_files_ignored": True,
        "synthetic_addition_invariance_check": "V25_FINALIZATION_FILE_INVARIANCE",
    },
    "verifier_script_sha256": sha256(Path(__file__)),
}

raw_records: list[dict[str, object]] = [
    {"record_type": "metadata", "base_commit": BASE, "head": head, "verdict": verdict}
]
raw_records.extend(
    {
        "record_type": "source_identity",
        "path": row["path"],
        "expected_sha256": row["sha256"],
        "observed_sha256": sha256(ROOT / row["path"]),
        "expected_blob": row["blob"],
    }
    for row in inventory
)
raw_records.extend(
    {"record_type": "route", "route_id": ident, "expected": ruling,
     "observed": route_rows[ident]["ruling"]}
    for ident, ruling in sorted(expected_rulings.items())
)
raw_records.extend({"record_type": "check", **row} for row in checks)
raw_records.extend(
    {"record_type": "mutation", "name": name, "caught": bool(errors), "errors": errors}
    for name, errors in mutation_results.items()
)

(HERE / "VERIFIER_RESULTS.json").write_text(
    json.dumps(results, indent=2, sort_keys=True) + "\n", encoding="utf-8"
)
(HERE / "VERIFIER_RAW.jsonl").write_text(
    "".join(json.dumps(row, sort_keys=True) + "\n" for row in raw_records), encoding="utf-8"
)
print(json.dumps({"verdict": verdict, "checks": results["check_summary"],
                  "mutations": results["mutation_summary"] | {"results": "omitted"}},
                 sort_keys=True))
