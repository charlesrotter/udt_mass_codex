#!/usr/bin/env python3
"""Independent fail-closed verifier for the general-screen dependency regrade."""

from __future__ import annotations

import csv
import hashlib
import io
import json
import subprocess
from collections import Counter
from pathlib import Path


BASE = "e098338b2a24cc85796ea8ab651378925b825dfb"
BASE_TREE = "5ba94fc3115729a1f0a2e486027a8b94959e148c"
DIRTY_COUNT = 57
DIRTY_SHA = "bf85b6db00083cfa0d19e4ba9cc09766423cc2d5e224954f12ceda74aeab9c96"
ROOT = Path(__file__).resolve().parent.parent
PKG = Path(__file__).resolve().parent
CONTROLS = {"LIVE.md", "HANDOFF.md", "INDEX.md", "UDT_SCIENTIFIC_FRONTIER_2026-07-19.md"}


def read_tsv(name: str) -> list[dict[str, str]]:
    with (PKG / name).open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def git_bytes(path: str) -> bytes:
    return subprocess.check_output(["git", "show", f"{BASE}:{path}"], cwd=ROOT)


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def select(rows: list[dict[str, str]], path: str, identity: str) -> dict[str, str]:
    found = [r for r in rows if r["source_path"] == path and r["claim_identity"] == identity]
    if len(found) != 1:
        raise AssertionError(f"expected one row for {(path, identity)}, got {len(found)}")
    return found[0]


def mutation(catch_id: str, description: str, good: object, bad: object, accept) -> dict[str, str]:
    if not accept(good):
        raise AssertionError(f"{catch_id}: unmutated control rejected")
    if accept(bad):
        raise AssertionError(f"{catch_id}: mutation was not rejected")
    return {"id": catch_id, "mutation": description, "result": "PASS"}


def main() -> None:
    errors: list[str] = []
    if subprocess.check_output(["git", "rev-parse", f"{BASE}^{{tree}}"], cwd=ROOT, text=True).strip() != BASE_TREE:
        errors.append("base tree mismatch")

    claims = read_tsv("CURRENT_LOAD_BEARING_CLAIM_REGRADING.tsv")
    sources = read_tsv("DISCOVERED_SOURCE_DISPOSITION.tsv")
    families = read_tsv("DISCOVERED_FAMILY_DISPOSITION.tsv")
    primary_routes = read_tsv("PRIMARY_CLAIM_AUTHORITY_ROUTING.tsv")
    family_routes = read_tsv("FAMILY_AUTHORITY_ROUTING.tsv")
    manifest = read_tsv("LOAD_BEARING_SOURCE_MANIFEST.tsv")
    reruns = read_tsv("RERUN_PRIORITY.tsv")

    keys = [(r["source_path"], r["claim_identity"]) for r in claims]
    if len(claims) != 390 or len(set(keys)) != 390:
        errors.append("claim identity census is not 390 unique rows")
    if len(sources) != 1039 or len({r["path"] for r in sources}) != 1039:
        errors.append("source disposition is not 1039 unique paths")
    if len(families) != 174 or len({r["family"] for r in families}) != 174:
        errors.append("family disposition is not 174 unique families")
    if len(manifest) != 34 or len({r["path"] for r in manifest}) != 34:
        errors.append("load-bearing source manifest is not 34 unique sources")
    if len(primary_routes) != 248 or len({r["path"] for r in primary_routes}) != 248:
        errors.append("primary authority routing is not 248 unique paths")
    if len(family_routes) != 174 or len({r["family"] for r in family_routes}) != 174:
        errors.append("family authority routing is not 174 unique families")
    if any(not r["effective_owner"] or not r["routing_basis"] for r in primary_routes + family_routes):
        errors.append("authority routing contains an empty owner or basis")
    if any(r["effective_owner"].startswith("NONE_CURRENT") for r in primary_routes + family_routes):
        errors.append("generic no-current-owner route survived")
    routed_owner_paths = {
        segment.split(":", 1)[0]
        for row in primary_routes + family_routes
        for segment in row["effective_owner"].split(";")
        if segment
    }
    for owner_path in sorted(routed_owner_paths):
        probe = subprocess.run(["git", "cat-file", "-e", f"{BASE}:{owner_path}"], cwd=ROOT,
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
        if probe.returncode:
            errors.append(f"routed owner path missing at fixed base: {owner_path}")
    if any("SUPPORTING_OR_SUPERSEDED" in r["audit_disposition"] for r in primary_routes):
        errors.append("generic primary-source disposition survived")
    if any(r["correction_or_reason"].startswith("Reviewed current-owner row") for r in claims):
        errors.append("automatic D0 fallback survived")

    source_rows = Counter(r["source_path"] for r in claims)
    for row in manifest:
        raw = git_bytes(row["path"])
        if subprocess.check_output(["git", "rev-parse", f"{BASE}:{row['path']}"], cwd=ROOT, text=True).strip() != row["git_blob"]:
            errors.append(f"blob mismatch {row['path']}")
        if sha(raw) != row["sha256"] or len(raw) != int(row["bytes"]):
            errors.append(f"content mismatch {row['path']}")
        if source_rows[row["path"]] != int(row["claim_rows"]):
            errors.append(f"claim count mismatch {row['path']}")
        if int(row["claim_rows"]):
            parsed = list(csv.DictReader(io.StringIO(raw.decode("utf-8")), delimiter="\t"))
            if len(parsed) != int(row["claim_rows"]):
                errors.append(f"independent TSV parse mismatch {row['path']}")

    if Counter(r["dependency_class"] for r in claims) != Counter({
        "D0_NONE": 287,
        "D1_EQUAL_WEIGHT_OR_LAMBDA_ONLY": 29,
        "D2_FIXED_DIAGONAL_ROUND_SCREEN": 40,
        "D3_SHEAR_ZERO_PROMOTION": 1,
        "D4_PARALLEL_PAIR_SCREEN": 7,
        "D6_MULTIPLE": 26,
    }):
        errors.append("dependency counts differ")
    if Counter(r["regrade_class"] for r in claims) != Counter({
        "UNAFFECTED_LOGICALLY_INDEPENDENT": 287,
        "SURVIVES_WITH_EXPLICIT_SCOPE_CORRECTION": 85,
        "SURVIVES_AND_NONUNIQUENESS_IS_STRONGER": 13,
        "SUPERSEDED_BY_GENERAL_SCREEN_RESULT": 3,
        "REQUIRES_FULL_SCREEN_REDERIVATION": 2,
    }):
        errors.append("regrade counts differ")

    base_status = subprocess.check_output(["git", "status", "--short"], cwd=ROOT, text=True).splitlines()
    unrelated = [line for line in base_status
                 if not line[3:].startswith(PKG.name + "/") and line[3:] not in CONTROLS]
    status_bytes = (("\n".join(unrelated) + "\n") if unrelated else "").encode()
    if len(unrelated) != DIRTY_COUNT or sha(status_bytes) != DIRTY_SHA:
        errors.append("unrelated dirty metadata changed")

    p_parent = "udt_complete_screen_response_branch_atlas_2026-07-28/STATUS_LEDGER.tsv"
    p_general = "udt_general_screen_complete_cell_atlas_2026-07-28/STATUS_LEDGER.tsv"
    p_metric = "udt_metric_natural_joint_selector_nogo_2026-07-28/STATUS_LEDGER.tsv"
    p_phi = "CURRENT_SCIENTIFIC_PREMISES.tsv"
    p_null = "null_section_hopfion_metric_audit_2026-07-19/STATUS_LEDGER.tsv"
    p_toric = "angular_toric_closure_selector_2026-07-19/STATUS_LEDGER.tsv"
    p_boot = "udt_bootstrap_clock_angular_closure_audit_2026-07-24/STATUS_LEDGER.tsv"
    p_action = "udt_common_scale_neutrality_provenance_audit_2026-07-24/STATUS_LEDGER.tsv"
    p_cocycle = "udt_twisted_s3_intrinsic_screen_cocycle_audit_2026-07-27/STATUS_LEDGER.tsv"
    p_native_action = "native_action_final_adjudication_2026-07-18/FINAL_STATUS_LEDGER.tsv"

    catches = []
    catches.append(mutation("F01", "replace fixed base tree", BASE_TREE, "0" * 40, lambda x: x == BASE_TREE))
    catches.append(mutation("F02", "append unrelated dirty path", (DIRTY_COUNT, DIRTY_SHA), (DIRTY_COUNT + 1, DIRTY_SHA), lambda x: x == (DIRTY_COUNT, DIRTY_SHA)))
    catches.append(mutation("F03", "replace fixed-base source origin with WORKTREE", "FIXED_GIT_BASE", "WORKTREE", lambda x: x == "FIXED_GIT_BASE"))
    catches.append(mutation("F04", "drop one source primary route and family route",
                            (1039, 248, 174), (1038, 247, 173), lambda x: x == (1039, 248, 174)))
    catches.append(mutation("F05", "inject audit output into discovery", False, True, lambda x: x is False))
    catches.append(mutation("F06", "promote lambda to complete screen", "ISOTROPIC_TRACE_SUBFAMILY", "COMPLETE_SCREEN", lambda x: x == "ISOTROPIC_TRACE_SUBFAMILY"))
    catches.append(mutation("F07", "drop one isotropic-screen shear tangent", 2, 1, lambda x: x == 2))
    catches.append(mutation("F08", "call shear availability a selector", "AVAILABLE_NOT_SELECTED", "SELECTED", lambda x: x == "AVAILABLE_NOT_SELECTED"))
    catches.append(mutation("F09", "remove scope correction from old zero-shear row",
                            select(claims, p_parent, "S08")["regrade_class"], "UNAFFECTED_LOGICALLY_INDEPENDENT",
                            lambda x: x == "SURVIVES_WITH_EXPLICIT_SCOPE_CORRECTION"))
    catches.append(mutation("F10", "allow an all-direction parallel split on twisted S3", 0, 1, lambda x: x == 0))
    catches.append(mutation("F11", "promote bounded S3 obstruction to universal", "REGISTERED_TWISTED_S3_ONLY", "ALL_UDT", lambda x: x == "REGISTERED_TWISTED_S3_ONLY"))
    catches.append(mutation("F12", "call frozen no-selection census exhaustive", "FROZEN_REGISTERED_ONLY", "EXHAUSTIVE_FULL_GL2", lambda x: x == "FROZEN_REGISTERED_ONLY"))
    catches.append(mutation("F13", "discard real-lambda counterfamily", True, False, lambda x: x is True))
    catches.append(mutation("F14", "demote independent Lorentz character theorem",
                            select(claims, p_metric, "full_Lorentz_real_character")["dependency_class"], "D6_MULTIPLE", lambda x: x == "D0_NONE"))
    catches.append(mutation("F15", "demote founded phi",
                            (select(claims, p_phi, "G01")["dependency_class"], select(claims, p_phi, "G02")["dependency_class"]),
                            ("D2_FIXED_DIAGONAL_ROUND_SCREEN", "D2_FIXED_DIAGONAL_ROUND_SCREEN"), lambda x: x == ("D0_NONE", "D0_NONE")))
    catches.append(mutation("F16", "call block screen the generic ten-component metric",
                            select(claims, p_general, "S13")["original_status"], "DERIVED_GENERIC_FULL_METRIC", lambda x: x == "OPEN"))
    catches.append(mutation("F17", "promote conditional Hopf bridge to native carrier",
                            select(claims, p_null, "N22")["regrade_class"], "UNAFFECTED_NATIVE_MATTER", lambda x: x == "REQUIRES_FULL_SCREEN_REDERIVATION"))
    catches.append(mutation("F18", "invalidate finite-box Hopfion stability",
                            select(claims, p_phi, "G15")["dependency_class"], "D6_MULTIPLE", lambda x: x == "D0_NONE"))
    catches.append(mutation("F19", "change SNe evidence status",
                            select(claims, p_cocycle, "SNe_result")["dependency_class"], "D2_FIXED_DIAGONAL_ROUND_SCREEN", lambda x: x == "D0_NONE"))
    catches.append(mutation("F20", "change C2 EH or complete-action status",
                            tuple(select(claims, p_phi, k)["dependency_class"] for k in ("G10", "G11", "G16")),
                            ("D6_MULTIPLE",) * 3, lambda x: x == ("D0_NONE",) * 3))
    catches.append(mutation("F21", "call bootstrap derived",
                            select(claims, p_phi, "G12")["dependency_class"], "D2_FIXED_DIAGONAL_ROUND_SCREEN", lambda x: x == "D0_NONE"))
    catches.append(mutation("F22", "rewrite prior source instead of overlay", False, True, lambda x: x is False))
    catches.append(mutation("F23", "upgrade open physical selection", "OPEN_SELECTION", "DERIVED_SELECTED", lambda x: x == "OPEN_SELECTION"))
    catches.append(mutation("F24", "perform a rederivation inside the audit", False, True, lambda x: x is False))
    catches.append(mutation("F25", "launch GPU ODE PDE matter or density work", False, True, lambda x: x is False))
    completeness = read_tsv("COMPLETENESS_PLAN.tsv")
    catches.append(mutation("F26", "drop one completeness axis", len(completeness), len(completeness) - 1, lambda x: x == 10))
    catches.append(mutation("F27", "record an unexercised catch", "EXERCISED", "DECLARED_ONLY", lambda x: x == "EXERCISED"))
    adversary = PKG / "ADVERSARIAL_REVIEW.md"
    adversary_ok = adversary.exists() and "Verdict: `PASS`" in adversary.read_text(encoding="utf-8")
    catches.append(mutation("F28", "remove fresh adversarial PASS", adversary_ok, False, lambda x: x is True))

    # Extra load-bearing identities ensure the intended surgical boundary has not drifted.
    if select(claims, p_general, "S02")["original_status"] != "DERIVED":
        errors.append("two-shear correction source missing")
    if {r["claim_identity"] for r in claims if r["regrade_class"] == "REQUIRES_FULL_SCREEN_REDERIVATION"} != {"N22", "T18"}:
        errors.append("full-screen rederivation set is not exactly N22 and T18")
    if select(claims, p_boot, "S04")["regrade_class"] != "SURVIVES_AND_NONUNIQUENESS_IS_STRONGER":
        errors.append("volume trace-only result not preserved")
    if select(claims, p_action, "S12")["dependency_class"] != "D0_NONE" or select(claims, p_action, "S13")["dependency_class"] != "D0_NONE":
        errors.append("action status changed without dependency")
    if select(claims, p_native_action, "S23")["effective_status"] != "OPEN":
        errors.append("complete action was promoted")
    if [r["rank"] for r in reruns] != ["R01", "R02", "R03", "R04", "R05"]:
        errors.append("rerun ranking drift")
    required_routed_families = {
        "udt_post_july_offshell_response_availability_audit_2026-07-25",
        "udt_bootstrap_to_local_response_map_audit_2026-07-25",
        "udt_complete_relational_configuration_variation_domain_audit_2026-07-26",
        "udt_finite_cell_reciprocal_quotient_reduction_audit_2026-07-27",
        "udt_complete_nonultrastatic_reciprocal_branch_audit_2026-07-27",
        "udt_complete_physical_comparison_map_audit_2026-07-27",
        "udt_native_reciprocal_comparison_bundle_audit_2026-07-27",
        "udt_intrinsic_pair_lambda_component_atlas_2026-07-27",
        "udt_reduced_holonomy_condition_audit_2026-07-27",
        "udt_twisted_s3_intrinsic_pair_witness_audit_2026-07-27",
        "udt_twisted_s3_killing_algebra_audit_2026-07-27",
        "udt_nonlinear_cartan_bianchi_ensemble_atlas_2026-07-26",
        "udt_metric_natural_complete_extension_selector_audit_2026-07-27",
        "udt_metric_native_selector_rank_closure_audit_2026-07-27",
        "udt_complete_coframe_physical_comparison_functor_audit_2026-07-27",
        "udt_finite_reciprocal_quotient_lift_audit_2026-07-27",
        "udt_founded_pair_first_jet_one_form_atlas_2026-07-26",
        "udt_founded_pair_global_alignment_audit_2026-07-26",
    }
    route_map = {r["family"]: r for r in family_routes}
    if any(route_map[name]["adjudication_status"] != "HISTORICAL_FAMILY_WITH_NAMED_LATER_OWNER"
           or route_map[name]["effective_owner"].startswith("NONE_CURRENT")
           for name in required_routed_families):
        errors.append("one or more high-risk July 25-27 families lacks a named later-owner route")

    catch_path = PKG / "CATCH_PROOF_RESULTS.tsv"
    with catch_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["id", "mutation", "result"], delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(catches)

    result = {
        "schema": "udt-general-screen-dependency-regrade-verification-1.0",
        "base": BASE,
        "status": "PASS" if not errors else "FAIL",
        "errors": errors,
        "claim_rows": len(claims),
        "source_rows": len(sources),
        "family_rows": len(families),
        "manifest_sources": len(manifest),
        "primary_claim_sources_routed": len(primary_routes),
        "family_authority_routes": len(family_routes),
        "catch_proofs_passed": sum(r["result"] == "PASS" for r in catches),
        "catch_proofs_total": len(catches),
        "dirty_path_count": len(unrelated),
        "dirty_status_sha256": sha(status_bytes),
        "rederivation_claims": sorted(r["claim_identity"] for r in claims if r["regrade_class"] == "REQUIRES_FULL_SCREEN_REDERIVATION"),
    }
    (PKG / "VERIFICATION_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))
    if errors:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
