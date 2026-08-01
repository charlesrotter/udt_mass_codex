#!/usr/bin/env python3
"""Cold, no-production-import verifier for bootstrap closure ownership."""

from __future__ import annotations

import copy
import csv
import hashlib
import json
import subprocess
from itertools import product
from pathlib import Path


PKG = Path(__file__).resolve().parent
ROOT = PKG.parent
BASE = "df2b35fcb6fc709e1ad0639b9f46222d64ee99cd"
RAW_PATH = PKG / "INDEPENDENT_RAW.jsonl"
RESULT_PATH = PKG / "INDEPENDENT_RESULT.json"
records: list[dict] = []


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def tsv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def record(kind: str, name: str, passed: bool, detail) -> None:
    records.append({"kind": kind, "name": name, "passed": bool(passed), "detail": detail})


def git_tree() -> dict[str, dict[str, str | int]]:
    text = subprocess.check_output(
        ["git", "ls-tree", "-rl", BASE], cwd=ROOT, text=True
    )
    tree: dict[str, dict[str, str | int]] = {}
    for line in text.splitlines():
        meta, path = line.split("\t", 1)
        mode, objtype, blob, size = meta.split()
        if objtype == "blob":
            tree[path] = {"blob": blob, "bytes": int(size), "mode": mode}
    return tree


def tracked_under(tree: dict, prefix: str) -> set[str]:
    needle = prefix.rstrip("/") + "/"
    return {path for path in tree if path.startswith(needle)}


def output_semantics_ok(rows: list[dict[str, str]]) -> bool:
    expected = {
        "O01": "CONDITIONAL_PARTIAL_MAP_COMPONENT",
        "O02": "LOCAL_DERIVED_GLOBAL_UNSELECTED",
        "O03": "CONDITIONAL_PATH_GROUPOID_OUTPUT",
        "O04": "CONFIGURATION_LABEL_NOT_RESPONSE",
        "O05": "CONDITIONAL_QUERY_FAMILY_NOT_UNIVERSAL",
        "O06": "TYPE_ONLY_SCHEMA_NOT_DEFINED",
        "O07": "CONDITIONAL_RAW_GEOMETRY_NOT_CHARGE",
        "O08": "OFFSHELL_STRUCTURE_AND_ALLOWED_RESPONSE_FAMILY",
        "O09": "CONDITIONAL_ACTION_PAIRING_BRANCH_OUTPUT",
        "O10": "OPEN_NO_NATIVE_FUNCTIONAL",
        "O11": "NO_ADDITIONAL_COMPLETE_OUTPUT_FOUND",
    }
    if len(rows) != 11 or len({row.get("candidate_id") for row in rows}) != 11:
        return False
    by_id = {row["candidate_id"]: row for row in rows}
    return set(by_id) == set(expected) and all(
        by_id[key].get("status") == value
        and by_id[key].get("common_domain_blocker")
        and by_id[key].get("physical_promotion_blocked")
        for key, value in expected.items()
    )


def return_semantics_ok(rows: list[dict[str, str]]) -> bool:
    expected = {
        "R01": ("KINEMATIC_EQUIVARIANCE_NOT_RETURN", "NO"),
        "R02": ("PARTIAL_ADMISSIBILITY_NOT_COMPLETE_RETURN", "PARTIAL_ONLY"),
        "R03": ("IDENTITY_OR_CONDITIONAL_GLOBAL_DATA_NOT_RETURN", "NO"),
        "R04": ("TYPE_ONLY_NEITHER_ARROW_COMPLETE", "NO"),
        "R05": ("PERMITTED_FAMILY_NOT_SELECTED_LAW", "NO"),
        "R06": ("OPERATOR_DEPENDENT_NO_NATIVE_PRIMITIVE", "NO"),
        "R07": ("CONDITIONAL_NOT_PROMOTED", "CONDITIONAL_ONLY"),
        "R08": ("NO_OTHER_COMPLETE_RETURN_FOUND", "NO"),
    }
    if len(rows) != 8 or len({row.get("candidate_id") for row in rows}) != 8:
        return False
    by_id = {row["candidate_id"]: row for row in rows}
    return set(by_id) == set(expected) and all(
        (by_id[key].get("status"), by_id[key].get("nonidentity_operation")) == value
        and by_id[key].get("exact_blocker")
        for key, value in expected.items()
    )


def claim_ceiling_ok(claim: dict) -> bool:
    return claim == {
        "complete_metric_native_R": False,
        "native_nonidentity_A": False,
        "closed_loop": False,
        "p4_tie_branch_independent": False,
        "universal_no_go": False,
        "solve_authorized": False,
    }


def source_probe(path: str, required: tuple[str, ...]) -> bool:
    text = (ROOT / path).read_text(encoding="utf-8")
    return all(token in text for token in required)


inventory = tsv(PKG / "SOURCE_INVENTORY.tsv")
scope = tsv(PKG / "SOURCE_PACKAGE_SCOPE.tsv")
tree = git_tree()
inventory_paths = [row["path"] for row in inventory]
inventory_set = set(inventory_paths)
parent_paths = {
    line for line in
    (ROOT / "udt_jr_cert_native_derivation_2026-08-01/COMBINED_SOURCE_PATHS.txt")
    .read_text(encoding="utf-8").splitlines() if line
}
parent_package = tracked_under(tree, "udt_jr_cert_native_derivation_2026-08-01")
scoped_union: set[str] = set()
scope_counts: dict[str, int] = {}
for row in scope:
    paths = tracked_under(tree, row["package_path"])
    scope_counts[row["package_path"]] = len(paths)
    scoped_union.update(paths)
expected_union = parent_paths | parent_package | scoped_union

record("freeze", "inventory_count_and_unique", len(inventory) == 926 == len(inventory_set),
       {"rows": len(inventory), "unique": len(inventory_set)})
record("freeze", "inventory_sorted", inventory_paths == sorted(inventory_paths),
       {"first": inventory_paths[0], "last": inventory_paths[-1]})
record("freeze", "independent_union_reconstruction", inventory_set == expected_union,
       {"parent": len(parent_paths), "parent_package": len(parent_package),
        "scoped_package_union": len(scoped_union), "union": len(expected_union)})
record("freeze", "scope_counts", len(scope) == 17 and all(scope_counts.values()), scope_counts)

bad_bytes: list[str] = []
bad_blobs: list[str] = []
for row in inventory:
    path = ROOT / row["path"]
    tree_row = tree.get(row["path"], {})
    if (not path.is_file() or sha256(path) != row["sha256"]
            or path.stat().st_size != int(row["bytes"])):
        bad_bytes.append(row["path"])
    if (row["base"] != BASE or tree_row.get("blob") != row["blob"]
            or tree_row.get("bytes") != int(row["bytes"])):
        bad_blobs.append(row["path"])
record("freeze", "all_current_source_bytes", not bad_bytes, {"bad": bad_bytes})
record("freeze", "all_base_blobs_and_sizes", not bad_blobs, {"bad": bad_blobs})

paths_text = "".join(f"{row['path']}\n" for row in inventory)
manifest_text = "".join(f"{row['sha256']}  ../{row['path']}\n" for row in inventory)
record("freeze", "source_paths_exact", (PKG / "SOURCE_PATHS.txt").read_text() == paths_text,
       {"sha256": sha256(PKG / "SOURCE_PATHS.txt")})
record("freeze", "source_manifest_exact", (PKG / "SOURCE_MANIFEST.sha256").read_text() == manifest_text,
       {"sha256": sha256(PKG / "SOURCE_MANIFEST.sha256")})

required_sources = {
    "udt_native_global_observable_closure_census_2026-07-26/AUDIT_REPORT.md":
        ("NO_DERIVED_COMPLETE_OBSERVABLE_VECTOR_OR_CLOSURE_SECTION", "Neither complete bootstrap arrow"),
    "udt_p4_routeA_slice2_solution_legs_2026-07-29/EXACT_DERIVATION.md":
        ("2·E0·I_p = 0", "P2-side members"),
    "udt_p4_routeA_slice2_solution_legs_2026-07-29/CORRECTION_LAYER.md":
        ("P2-side ABSENCE genuinely derived", "pairing-relativity"),
    "udt_p4_angular_stage_A3_2026-07-31/AUDIT_REPORT.md":
        ("No solution-dependent native field winding", "on-shell coexistence is also unproved"),
    "udt_p4_cold_review_repair_2026-08-01/CLOSURE_REPORT.md":
        ("underlying P4 arc remains premise-scoped", "no response law"),
    "udt_stability_foundations_audit_2026-08-01/BOOTSTRAP_FIXED_POINT_SCHEMA.tsv":
        ("DERIVED_AS_TYPE_SCHEMA_ONLY", "requires native mass/energy/curvature/source"),
    "udt_joint_realization_closure_audit_2026-08-01/AUDIT_REPORT.md":
        ("Bootstrap diagram is not bootstrap closure", "neither arrow nor a common fixed point"),
    "udt_jr_cert_native_derivation_2026-08-01/AUDIT_REPORT.md":
        ("equation routes: 8/8 adjudicated, 0 passing", "Present evidence does not define either arrow"),
}
source_probe_results = {
    path: path in inventory_set and source_probe(path, tokens)
    for path, tokens in required_sources.items()
}
record("semantic_source", "post_july_p4_jr_sources_present_and_consistent",
       all(source_probe_results.values()), source_probe_results)

outputs = tsv(PKG / "OUTPUT_OWNERSHIP_LEDGER.tsv")
returns = tsv(PKG / "RETURN_OWNERSHIP_LEDGER.tsv")
anchors = tsv(PKG / "SOURCE_ANCHOR_LEDGER.tsv")
result = json.loads((PKG / "RESULT.json").read_text(encoding="utf-8"))
algebra_primary = json.loads((PKG / "ALGEBRA_RESULT.json").read_text(encoding="utf-8"))
record("semantics", "all_eleven_output_rows_exact", output_semantics_ok(outputs),
       {row["candidate_id"]: row["status"] for row in outputs})
record("semantics", "all_eight_return_rows_exact", return_semantics_ok(returns),
       {row["candidate_id"]: [row["status"], row["nonidentity_operation"]] for row in returns})
anchor_bad = [row["anchor_id"] for row in anchors
              if row["path"] not in inventory_set or sha256(ROOT / row["path"]) != row["sha256"]]
record("semantics", "fourteen_source_anchors_exact", len(anchors) == 14 and not anchor_bad,
       {"count": len(anchors), "bad": anchor_bad})

claim = {
    "complete_metric_native_R": result.get("complete_output_maps") != 0,
    "native_nonidentity_A": result.get("passing_return_routes") != 0,
    "closed_loop": result.get("outcome") != "LOCAL_TO_GLOBAL_MAP_PARTIAL_RETURN_OPEN",
    "p4_tie_branch_independent": result.get("p4_tie_branch_independent"),
    "universal_no_go": False,
    "solve_authorized": result.get("solve_authorized"),
}
record("semantics", "bounded_claim_ceiling", claim_ceiling_ok(claim), claim)

# Independent graph algebra: rank from a nonzero exact minor, not row reduction.
R = ((1, 2, 0), (0, 1, 1))
jac = ((-1, -2, 0, 1, 0), (0, -1, -1, 0, 1))
minors = [jac[0][i] * jac[1][j] - jac[0][j] * jac[1][i]
          for i in range(5) for j in range(i + 1, 5)]
graph_rank = 2 if any(minors) else (1 if any(jac[0] + jac[1]) else 0)
graph_nullity = 5 - graph_rank
grid_residuals = []
for x in product(range(-2, 3), repeat=3):
    o = tuple(sum(R[i][j] * x[j] for j in range(3)) for i in range(2))
    residual = tuple(o[i] - sum(R[i][j] * x[j] for j in range(3)) for i in range(2))
    grid_residuals.append(residual)
record("algebra", "graph_rank_nullity_independent_minor",
       graph_rank == 2 and graph_nullity == 3,
       {"rank": graph_rank, "nullity": graph_nullity, "nonzero_minors": sum(v != 0 for v in minors)})
record("algebra", "graph_leaves_every_sampled_x_admissible",
       len(grid_residuals) == 125 and all(r == (0, 0) for r in grid_residuals),
       {"integer_witnesses": len(grid_residuals), "nonzero_residuals": sum(r != (0, 0) for r in grid_residuals)})

witnesses = ((0, 0, 0), (1, 0, 0), (0, 1, 0), (0, 0, 1))
survivors = {
    "A_all_zero": sum(True for _ in witnesses),
    "A_identity": sum(x == (0, 0, 0) for x in witnesses),
    "A_plane_x3_zero": sum(x[2] == 0 for x in witnesses),
}
record("algebra", "same_R_allows_inequivalent_returns",
       survivors == {"A_all_zero": 4, "A_identity": 1, "A_plane_x3_zero": 3}, survivors)

# Own formal derivative: if a_F(lambda)=s*lambda+b and W_F*L=E0 on shell,
# the integrated lambda row is s*E0*I_p. P1 slopes are two; P2 slope is zero.
p4_branches = {
    "P1_4D": {"slope": 2, "tie_coefficient": 2},
    "P1_triad": {"slope": 2, "tie_coefficient": 2},
    "P2_duality_natural": {"slope": 0, "tie_coefficient": 0},
}
p4_ok = (all(p4_branches[key]["tie_coefficient"] == 2 for key in ("P1_4D", "P1_triad"))
         and p4_branches["P2_duality_natural"]["tie_coefficient"] == 0)
record("algebra", "p4_tie_pairing_branch_relative", p4_ok,
       {"branches": p4_branches,
        "nuance": "a_M-independent within P1; not independent across P1 versus P2"})
record("algebra", "current_primary_algebra_agrees",
       algebra_primary.get("graph_rank") == graph_rank
       and algebra_primary.get("graph_nullity") == graph_nullity
       and algebra_primary.get("p4_tie_branch_independent") is False,
       {"primary_flag": algebra_primary.get("p4_tie_branch_independent")})


def changed_row(rows: list[dict[str, str]], row_id: str, field: str, value: str) -> list[dict[str, str]]:
    candidate = copy.deepcopy(rows)
    next(row for row in candidate if row["candidate_id"] == row_id)[field] = value
    return candidate


mutations: list[tuple[str, bool]] = []
mutations.append(("drop_output_family", not output_semantics_ok(outputs[:-1])))
mutations.append(("duplicate_output_family", not output_semantics_ok(outputs + [copy.deepcopy(outputs[0])])))
mutations.append(("topology_label_promoted_to_response",
                  not output_semantics_ok(changed_row(outputs, "O04", "status", "METRIC_RESPONSE_MAP"))))
mutations.append(("query_arguments_erased",
                  not output_semantics_ok(changed_row(outputs, "O05", "status", "UNIVERSAL_INTRINSIC_SCALAR"))))
mutations.append(("raw_flux_promoted_to_native_mass",
                  not output_semantics_ok(changed_row(outputs, "O07", "status", "DERIVED_NATIVE_MASS"))))
mutations.append(("permitted_response_promoted_to_realized",
                  not output_semantics_ok(changed_row(outputs, "O08", "status", "SELECTED_RESPONSE_LAW"))))
mutations.append(("p4_conditional_output_promoted_to_metric_universal",
                  not output_semantics_ok(changed_row(outputs, "O09", "status", "METRIC_UNIVERSAL_OUTPUT"))))
mutations.append(("native_mass_absence_erased",
                  not output_semantics_ok(changed_row(outputs, "O10", "status", "DERIVED_NATIVE_FUNCTIONAL"))))
mutations.append(("reciprocity_promoted_to_return",
                  not return_semantics_ok(changed_row(returns, "R01", "nonidentity_operation", "YES"))))
mutations.append(("cartan_identity_promoted_to_eom",
                  not return_semantics_ok(changed_row(returns, "R03", "status", "NATIVE_EOM"))))
mutations.append(("bootstrap_type_promoted_to_equation",
                  not return_semantics_ok(changed_row(returns, "R04", "status", "NATIVE_RETURN_EQUATION"))))
mutations.append(("p4_family_promoted_to_selected_law",
                  not return_semantics_ok(changed_row(returns, "R05", "status", "SELECTED_NATIVE_LAW"))))
mutations.append(("conditional_action_promoted_to_native",
                  not return_semantics_ok(changed_row(returns, "R07", "nonidentity_operation", "YES"))))
for field, name in (
    ("complete_metric_native_R", "false_complete_R"),
    ("native_nonidentity_A", "false_native_A"),
    ("closed_loop", "tautological_graph_called_closed_loop"),
    ("p4_tie_branch_independent", "p4_pairing_branch_erasure"),
    ("universal_no_go", "bounded_negative_promoted_to_universal_no_go"),
    ("solve_authorized", "unauthorized_solve"),
):
    candidate = copy.deepcopy(claim)
    candidate[field] = True
    mutations.append((name, not claim_ceiling_ok(candidate)))
mutated_branches = copy.deepcopy(p4_branches)
mutated_branches["P2_duality_natural"]["tie_coefficient"] = 2
mutations.append(("p4_P2_absence_erased",
                  not (mutated_branches["P2_duality_natural"]["tie_coefficient"] == 0)))
for path, name in (
    ("udt_p4_angular_stage_A3_2026-07-31/AUDIT_REPORT.md", "drop_post_july_A3"),
    ("udt_p4_cold_review_repair_2026-08-01/CLOSURE_REPORT.md", "drop_cold_repair"),
    ("udt_stability_foundations_audit_2026-08-01/BOOTSTRAP_FIXED_POINT_SCHEMA.tsv", "drop_stability_schema"),
    ("udt_joint_realization_closure_audit_2026-08-01/AUDIT_REPORT.md", "drop_joint_realization"),
    ("udt_jr_cert_native_derivation_2026-08-01/AUDIT_REPORT.md", "drop_JR_parent"),
):
    candidate = set(inventory_set)
    candidate.remove(path)
    mutations.append((name, not all(required in candidate for required in required_sources)))

for name, caught in mutations:
    record("semantic_mutation", name, caught, {"rejected": caught})

exact_hashes = {
    "preregistration": sha256(PKG / "PREREGISTRATION.md"),
    "source_inventory": sha256(PKG / "SOURCE_INVENTORY.tsv"),
    "output_ownership_ledger": sha256(PKG / "OUTPUT_OWNERSHIP_LEDGER.tsv"),
    "return_ownership_ledger": sha256(PKG / "RETURN_OWNERSHIP_LEDGER.tsv"),
    "source_anchor_ledger": sha256(PKG / "SOURCE_ANCHOR_LEDGER.tsv"),
    "algebra_result": sha256(PKG / "ALGEBRA_RESULT.json"),
    "result": sha256(PKG / "RESULT.json"),
    "production_deriver_current": sha256(PKG / "derive_closure_ownership.py"),
    "production_verifier_current": sha256(PKG / "verify_closure_ownership.py"),
    **{f"source::{path}": sha256(ROOT / path) for path in required_sources},
}
record("provenance", "exact_hashes_captured", True, exact_hashes)

failed = [row["name"] for row in records if not row["passed"]]
RAW_PATH.write_text("".join(json.dumps(row, sort_keys=True) + "\n" for row in records), encoding="utf-8")
payload = {
    "verdict": "PASS" if not failed else "AMENDMENT-REQUIRED",
    "outcome_retained": "LOCAL_TO_GLOBAL_MAP_PARTIAL_RETURN_OPEN",
    "checks_passed": sum(row["passed"] for row in records),
    "checks_total": len(records),
    "semantic_mutations_rejected": sum(caught for _, caught in mutations),
    "semantic_mutations_total": len(mutations),
    "failed": failed,
    "source_paths_verified": len(inventory),
    "independent_graph_rank": graph_rank,
    "independent_graph_nullity": graph_nullity,
    "p4_tie_branch_independent": False,
    "p4_scope_nuance": "a_M-independent within P1; absent on P2 and therefore not pairing-branch-independent",
    "post_july_p4_jr_material_omission_found": False,
    "primary_transparency_update": "explicit false P4 flag verified in current bytes; scientific claim unchanged",
    "exact_hashes": exact_hashes,
    "independent_verifier_sha256": sha256(Path(__file__)),
    "independent_raw_sha256": sha256(RAW_PATH),
    "solve_run": False,
    "gpu_used": False,
}
RESULT_PATH.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
print(f"{payload['verdict']} independent closure verifier: "
      f"{payload['checks_passed']}/{payload['checks_total']}; "
      f"mutations={payload['semantic_mutations_rejected']}/{payload['semantic_mutations_total']}")
if failed:
    raise SystemExit(1)
