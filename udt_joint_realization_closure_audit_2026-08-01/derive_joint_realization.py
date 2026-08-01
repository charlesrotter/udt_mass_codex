#!/usr/bin/env python3
"""Deterministic CPU audit of the registered UDT joint-realization gate.

The finite-set examples are logic controls, not candidate UDT equations.  The
scientific classification is source-led and bounded to SOURCE_INVENTORY.tsv.
"""

from __future__ import annotations

import csv
import hashlib
import json
from copy import deepcopy
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = Path(__file__).resolve().parent
OUTCOME = "FORMAL_COMPATIBILITY_ONLY_COMMON_REALIZATION_OPEN"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def write_tsv(path: Path, header: list[str], rows: list[list[str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
        writer.writerow(header)
        writer.writerows(rows)


gate_rows = [
    ["G01", "full configuration space U_full", "PARTIAL", "metric/coframe and P4 alphabets are registered", "complete physical field ownership remains open"],
    ["G02", "static restriction r_s(u) in M_s", "EXACT_IN_REDUCED_STATIONARY_SCOPES", "Route-A Slice 2/2b exact stationary solution families", "representative and quadratic-class scopes; not a full live solution"],
    ["G03", "time-live restriction r_t(u) in M_t", "FORMAL_EXACT_POINTWISE", "P4 T2 and cold Q2 regrade", "T2 records no solve and no integration/on-shell closure"],
    ["G04", "angular-live restriction r_a(u) in M_a", "FORMAL_EXACT_POINTWISE", "P4 A2/A3 and cold Q2 regrade", "nonzero angular-live on-shell coexistence is unproved"],
    ["G05", "one identical full field u", "OPEN", "cold Q2 and stability-foundations fixed gate", "separate module embeddings or separate solutions cannot be spliced"],
    ["G06", "nonzero time-live content L_t(u)", "OPEN_ON_SAME_FIELD", "T2 no-solve statement and Slice-2b time-live exclusion", "mode zero is only a recovery control"],
    ["G07", "nonzero angular-live content L_a(u)", "OPEN_ON_SAME_FIELD", "A3 explicit on-shell coexistence caveat", "formal angular characters are not a realized live field"],
    ["G08", "native whole-system equation or response E_native[u]=0", "OPEN", "native-action final ledger S23 and global-coframe off-shell statement", "no complete action is required in form but some whole-system operation is required"],
    ["G09", "differentiable finite-cell boundary/completion B_native[u]=0", "OPEN", "native-action final ledger S24 and 12-family completion atlas", "seal parity wall traces and completion types do not supply the full variational problem"],
    ["G10", "one compatible premise assignment P", "PARTIAL", "current premise ledger and cold premise-quantifier audit", "action carrier reading posture and completion branches cannot be silently merged"],
    ["G11", "nonempty live joint pullback R_live", "OPEN", "G05 through G10", "formal common zero mode does not witness nonzero live coexistence"],
    ["G12", "explicit native joint-realization certificate", "ABSENT_IN_FROZEN_RECORD", "all eight preregistered routes adjudicated", "bounded absence from registered sources; not a universal nonexistence theorem"],
]


route_rows = [
    ["J01", "DIRECT_REGISTERED_WITNESS", "NO", "NO", "NO", "NO", "PARTIAL", "NOT_FOUND_IN_FROZEN_RECORD", "No source supplies one full nonzero-live field with its native equation boundary and premise stack."],
    ["J02", "FORMAL_PULLBACK_FIBER_PRODUCT", "FORMAL_ONLY", "NO", "NO", "NO", "PARTIAL", "FORMAL_COMPATIBILITY_ONLY", "The formal module pullbacks recover exactly but their nonzero live on-shell fiber product is not shown nonempty."],
    ["J03", "STATIC_SOLUTION_UNMUTING_LIFT", "STATIC_REDUCED_ONLY", "REDUCED_STATIONARY_ONLY", "PARTIAL_TYPED", "NO", "PARTIAL", "LIVE_LIFT_OPEN", "Exact stationary P4 families exist; Slice-2b excludes time-live and T2/A3 do not solve the lift."],
    ["J04", "FINITE_CELL_BOUNDARY_COMPLETION", "NO", "NO", "COMPLETION_TYPES_ONLY", "NO", "PARTIAL", "DIFFERENTIABLE_JOIN_OPEN", "Twelve completion families are catalogued but every row lacks a complete g-phi-matter witness and density response."],
    ["J05", "BOOTSTRAP_SIMULTANEOUS_CLOSURE", "NO", "TYPE_SKELETON_ONLY", "REQUIRED_TYPE_ONLY", "NO", "WORKING", "BOTH_MAPS_AND_FIXED_POINT_OPEN", "The two-arrow architecture is exact as a type; neither complete arrow nor a common fixed point is registered."],
    ["J06", "ACTION_MEDIATED", "CONDITIONAL_SLICES_ONLY", "CONDITIONAL_OR_OPEN", "OPEN", "NO", "CONDITIONAL_BRANCHES", "NO_COMPLETE_CONDITIONAL_WITNESS", "C2/Bach EH and reduced actions remain conditional and no complete action-source-boundary-live solution is supplied."],
    ["J07", "CARRIER_TOPOLOGY_MEDIATED", "STATIC_CARRIER_ONLY", "CONDITIONAL_CARRIER_ACTION", "SOLVER_BOUNDARY_ONLY", "NO", "POSIT_CONDITIONAL", "STATIC_FINITE_BOX_ONLY", "The full-3D Hopfion is a conditional static finite-box result; carrier selection physical boundary and time persistence remain open."],
    ["J08", "MISSING_OBLIGATION_LOCALIZATION", "TYPE_IDENTIFIED", "TYPE_IDENTIFIED", "TYPE_IDENTIFIED", "TYPE_IDENTIFIED", "TYPE_IDENTIFIED", "MINIMUM_CERTIFICATE_TYPE_IDENTIFIED", "A native joint-realization problem plus one nonzero-live witness is the smallest complete certificate type; it is not constructed."],
]


schema_rows = [
    ["C01", "U_full", "complete finite-cell configuration space", "PARTIAL", "must own all metric coframe phi and any matter/global fields used"],
    ["C02", "Pi_native", "one whole-system problem specification", "OPEN", "Pi_native=(E_native,B_native,P_compatible); an action is one possible package not a required form"],
    ["C03", "E_native", "native equation/response operation on U_full", "OPEN", "must be one operation across static time and angular restrictions"],
    ["C04", "B_native", "differentiable finite-cell boundary/corner/completion operation", "OPEN", "must cover the same field and variation domain"],
    ["C05", "P_compatible", "single premise assignment", "PARTIAL", "cannot merge mutually exclusive action carrier reading posture or completion branches"],
    ["C06", "r_s,r_t,r_a", "restriction maps from one u", "FORMAL_PARTIAL", "registered module recoveries exist but whole-field ownership and on-shell join remain open"],
    ["C07", "L_t,L_a", "nonzero live predicates", "DEFINED_AS_AUDIT_GATE", "both must be nonzero for the same u; static or mode-zero controls fail"],
    ["C08", "u", "one realized full field assignment", "OPEN", "must satisfy Pi_native and all three restrictions"],
    ["C09", "JR_CERT_NATIVE", "(Pi_native,u,proofs of restrictions liveness equation boundary and premise compatibility)", "IDENTIFIED_NOT_CONSTRUCTED", "smallest complete evidence object for the present question"],
    ["C10", "bootstrap implementation", "possible producer of Pi_native and u", "WORKING_TYPE_ONLY", "would require both complete arrows and a solved common fixed point"],
    ["C11", "action implementation", "possible producer of E_native and B_native", "CONDITIONAL_OR_OPEN", "not privileged and does not by itself supply a solution"],
    ["C12", "persistence join", "downstream response or certificate about u", "OUT_OF_SCOPE_BLOCKED", "cannot be tested before JR_CERT_NATIVE exists"],
]


counter_rows = [
    ["CM01", "SEPARATE_LIVE_SECTORS", "U={z,t,a}; time-live={t}; angular-live={a}", "each live module is nonempty but no element is live in both", "separate sector existence does not imply a common field"],
    ["CM02", "ZERO_MODE_FALSE_WITNESS", "U={z}; all formal restrictions and E,B pass; L_t(z)=L_a(z)=0", "formal common member exists but live set is empty", "mode-zero recovery cannot witness live coexistence"],
    ["CM03", "EQUATION_BOUNDARY_MISMATCH", "U={p,q}; both live; E=0 only at p; B=0 only at q", "equation solution set and boundary solution set are nonempty but disjoint", "field liveness does not replace a common problem"],
    ["CM04", "PREMISE_SPLICE", "same symbol u appears on branches A and B; A supplies time/equation while B supplies angular/boundary", "no single branch supplies every clause", "conditional clauses cannot be merged across premise stacks"],
    ["CM05", "PROBLEM_WITHOUT_WITNESS", "a well-typed E and B are declared on U but their common live zero set is empty", "a problem specification alone does not prove existence", "deriving an action or equation is not yet joint realization"],
]


status_rows = [
    ["S01", "static P4 realized content", "EXACT_REDUCED_STATIONARY_SCOPES", "representative/full-cell stationary packages", "time-live excluded and complete physical ownership open"],
    ["S02", "time-live P4 content", "FORMAL_EXACT_POINTWISE", "T2 plus cold Q2", "no response law or solve"],
    ["S03", "angular-live P4 content", "FORMAL_EXACT_POINTWISE", "A2/A3 plus cold Q2", "nonzero on-shell coexistence unproved"],
    ["S04", "formal static/time/angular compatibility", "DERIVED_IN_STATED_SCOPES", "module pullback and mode-zero controls", "not one nonzero joint solution"],
    ["S05", "complete native equation/response", "OPEN", "native-action adjudication", "conditional bulks and reduced equations are not a complete problem"],
    ["S06", "differentiable finite-cell boundary/completion", "OPEN", "native-action boundary ledger and completion atlas", "seal parity and typed completions are incomplete"],
    ["S07", "bootstrap realization", "TYPE_SKELETON_ONLY", "two-arrow response audits", "maps fixed point and witness absent"],
    ["S08", "action-mediated joint realization", "NO_COMPLETE_CONDITIONAL_WITNESS_REGISTERED", "conditional action branches", "no full nonzero-live equation-boundary witness"],
    ["S09", "carrier-mediated joint realization", "STATIC_FINITE_BOX_CONDITIONAL_ONLY", "native Hopfion topology and no-null stability", "not a native metric field boundary or time-live history"],
    ["S10", "native joint-realization certificate JR_CERT_NATIVE", "OPEN_TYPE_IDENTIFIED", "gate nonredundancy and eight-route census", "identification is not construction"],
    ["S11", "joint-realization audit outcome", OUTCOME, "zero of eight routes supplies JR_CERT_NATIVE", "bounded registered-source result not a universal no-go"],
    ["S12", "native stability", "CONDITIONAL_STABILITY_ONLY_UNCHANGED", "parent stability-foundations audit", "persistence join remains downstream and open"],
]


source_anchors = [
    ("A01", "udt_p4_cold_adversarial_review_2026-08-01/PREMISE_QUANTIFIER_AUDIT.tsv", "FIXED_REALIZED_SOLUTION_OPEN", "cold review distinguishes formal module recovery from one realized solution"),
    ("A02", "udt_p4_timelive_stage_T2_2026-07-31/AUDIT_REPORT.md", "no response law selected, no fork decided, no solve", "time-live module is not a solved response"),
    ("A03", "udt_p4_angular_stage_A3_2026-07-31/AUDIT_REPORT.md", "Nonzero angular-live on-shell coexistence is also unproved.", "angular-live on-shell coexistence is explicitly open"),
    ("A04", "udt_p4_routeA_slice2b_full_cell_2026-07-29/AUDIT_REPORT.md", "time-live OUT", "stationary full-cell result cannot itself supply the time-live lift"),
    ("A05", "udt_native_global_coframe_definition_audit_2026-07-28/AUDIT_REPORT.md", "The complete family is off shell.", "complete reciprocal configurations prove existence class not realization"),
    ("A06", "native_action_final_adjudication_2026-07-18/FINAL_STATUS_LEDGER.tsv", "S23\tComplete native action\tOPEN", "complete action and its equations remain open"),
    ("A07", "native_action_final_adjudication_2026-07-18/FINAL_STATUS_LEDGER.tsv", "S24\tFinite-cell differentiable boundary action\tOPEN", "differentiable finite-cell boundary problem remains open"),
    ("A08", "udt_bootstrap_clock_angular_closure_audit_2026-07-24/BOOTSTRAP_ROUTE_LEDGER.tsv", "OPEN_NOT_REGISTERED_COMPLETE", "simultaneous metric-matter-boundary bootstrap is typed but absent"),
    ("A09", "udt_bootstrap_clock_angular_closure_audit_2026-07-24/COMPLETION_BOOTSTRAP_ATLAS.tsv", "FC12_RECIPROCAL_TORIC_DIAGONAL\tNO\tABSENT", "last of twelve completion rows also lacks a complete witness and response"),
    ("A10", "native_hopfion_topology_audit_2026-07-19/AUDIT_REPORT.md", "Global/time-live persistence | `OPEN`", "conditional Hopfion branch cannot supply time-live realization"),
    ("A11", "udt_stability_foundations_audit_2026-08-01/FIXED_REALIZATION_GATE.tsv", "nonempty compatible realized pullback/fiber-product R_live\tOPEN", "parent gate states the exact realization gap"),
    ("A12", "udt_bootstrap_to_local_response_map_audit_2026-07-25/STATUS_LEDGER.tsv", "complete_bootstrap_to_local_map\tOPEN", "neither bootstrap arrow is supplied as a complete map"),
]


def source_inventory_checks(checks: list[dict[str, object]]) -> None:
    with (OUT / "SOURCE_INVENTORY.tsv").open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
    checks.append({"id": "D01_SOURCE_COUNT", "kind": "SUBSTANTIVE", "pass": len(rows) == 140 and len({r["path"] for r in rows}) == 140, "detail": f"rows={len(rows)} unique={len({r['path'] for r in rows})}"})
    mismatches = []
    for row in rows:
        path = ROOT / row["path"]
        if not path.is_file() or path.stat().st_size != int(row["bytes"]) or sha256(path) != row["sha256"]:
            mismatches.append(row["path"])
    checks.append({"id": "D02_SOURCE_IDENTITIES", "kind": "SUBSTANTIVE", "pass": not mismatches, "detail": f"mismatches={mismatches}"})


def source_anchor_checks(checks: list[dict[str, object]]) -> None:
    for ident, rel, token, _inference in source_anchors:
        text = (ROOT / rel).read_text(encoding="utf-8")
        checks.append({"id": ident, "kind": "SUBSTANTIVE", "pass": token in text, "detail": f"{rel}: {token}"})


def exact_controls(checks: list[dict[str, object]]) -> dict[str, object]:
    # CM01: both live sectors separately inhabited, but no common live member.
    universe = {"z", "t", "a"}
    time_live = {"t"}
    angular_live = {"a"}
    joint_live = universe & time_live & angular_live
    checks.append({"id": "D03_SEPARATE_LIVE_NO_JOIN", "kind": "SUBSTANTIVE", "pass": bool(time_live) and bool(angular_live) and joint_live == set(), "detail": f"time={sorted(time_live)} angular={sorted(angular_live)} joint={sorted(joint_live)}"})

    # CM02: zero mode passes every structural clause except the two live predicates.
    zero_record = {"field": True, "static": True, "time_module": True, "angular_module": True, "equation": True, "boundary": True, "premise": True, "time_live": False, "angular_live": False}
    all_without_live = all(value for key, value in zero_record.items() if key not in {"time_live", "angular_live"})
    checks.append({"id": "D04_ZERO_MODE_REJECTED", "kind": "SUBSTANTIVE", "pass": all_without_live and not (zero_record["time_live"] and zero_record["angular_live"]), "detail": "all structural clauses pass; live predicates false"})

    # CM03: equation and boundary zero sets are separately nonempty but disjoint.
    live = {"p", "q"}
    equation_zero = {"p"}
    boundary_zero = {"q"}
    common_on_shell = live & equation_zero & boundary_zero
    checks.append({"id": "D05_EQUATION_BOUNDARY_DISJOINT", "kind": "SUBSTANTIVE", "pass": bool(equation_zero) and bool(boundary_zero) and common_on_shell == set(), "detail": f"E0={sorted(equation_zero)} B0={sorted(boundary_zero)} common={sorted(common_on_shell)}"})

    # CM04: each premise branch fails one required live clause.
    premise_branches = {"A": {"time": True, "angular": False, "equation": True, "boundary": False}, "B": {"time": False, "angular": True, "equation": False, "boundary": True}}
    branch_pass = {name: all(values.values()) for name, values in premise_branches.items()}
    spliced = all(premise_branches["A"][k] or premise_branches["B"][k] for k in ("time", "angular", "equation", "boundary"))
    checks.append({"id": "D06_PREMISE_SPLICE_REJECTED", "kind": "SUBSTANTIVE", "pass": spliced and not any(branch_pass.values()), "detail": f"branch_pass={branch_pass} spliced={spliced}"})

    # CM05: a typed problem can have no live solution.
    typed_universe = {0, 1}
    e_zero = {0}
    b_zero = {0}
    live_nonzero = {1}
    solution = typed_universe & e_zero & b_zero & live_nonzero
    checks.append({"id": "D07_PROBLEM_DOES_NOT_IMPLY_WITNESS", "kind": "SUBSTANTIVE", "pass": solution == set(), "detail": f"solution={sorted(solution)}"})
    return {
        "separate_live_joint": sorted(joint_live),
        "zero_mode_passes_nonlive_clauses": all_without_live,
        "equation_boundary_common": sorted(common_on_shell),
        "premise_branch_pass": branch_pass,
        "typed_problem_live_solution": sorted(solution),
    }


def contract_violations(
    gates: list[list[str]], routes: list[list[str]], schema: list[list[str]], statuses: list[list[str]]
) -> list[str]:
    bad: list[str] = []
    if [row[0] for row in gates] != [f"G{i:02d}" for i in range(1, 13)]:
        bad.append("exact_gate_census")
    if [row[0] for row in routes] != [f"J{i:02d}" for i in range(1, 9)]:
        bad.append("exact_route_census")
    if [row[0] for row in schema] != [f"C{i:02d}" for i in range(1, 13)]:
        bad.append("exact_schema_census")
    if any(not cell for table in (gates, routes, schema, statuses) for row in table for cell in row):
        bad.append("no_blank_cells")
    g = {row[0]: row[2] for row in gates}
    r = {row[0]: row[7] for row in routes}
    c = {row[0]: row[3] for row in schema}
    s = {row[0]: row[2] for row in statuses}
    required = {
        "G05": (g, "OPEN"),
        "G06": (g, "OPEN_ON_SAME_FIELD"),
        "G07": (g, "OPEN_ON_SAME_FIELD"),
        "G08": (g, "OPEN"),
        "G09": (g, "OPEN"),
        "G12": (g, "ABSENT_IN_FROZEN_RECORD"),
        "J01": (r, "NOT_FOUND_IN_FROZEN_RECORD"),
        "J02": (r, "FORMAL_COMPATIBILITY_ONLY"),
        "J03": (r, "LIVE_LIFT_OPEN"),
        "J04": (r, "DIFFERENTIABLE_JOIN_OPEN"),
        "J05": (r, "BOTH_MAPS_AND_FIXED_POINT_OPEN"),
        "J06": (r, "NO_COMPLETE_CONDITIONAL_WITNESS"),
        "J07": (r, "STATIC_FINITE_BOX_ONLY"),
        "C09": (c, "IDENTIFIED_NOT_CONSTRUCTED"),
        "S08": (s, "NO_COMPLETE_CONDITIONAL_WITNESS_REGISTERED"),
        "S11": (s, OUTCOME),
        "S12": (s, "CONDITIONAL_STABILITY_ONLY_UNCHANGED"),
    }
    for ident, (mapping, expected) in required.items():
        if mapping.get(ident) != expected:
            bad.append(f"{ident}_must_be_{expected}")
    complete_routes = [row[0] for row in routes[:7] if row[7] in {"REGISTERED_NATIVE_JOINT_REALIZATION_FOUND", "CONDITIONAL_JOINT_REALIZATION_ONLY"}]
    if complete_routes:
        bad.append("no_unearned_complete_route")
    if "POSIT_CONDITIONAL" not in {row[6] for row in routes}:
        bad.append("carrier_premise_must_remain_conditional")
    return bad


def exercise_mutations(checks: list[dict[str, object]]) -> list[dict[str, object]]:
    mutations: list[tuple[str, list[list[str]], list[list[str]], list[list[str]], list[list[str]]]] = []
    mutations.append(("M01_MISSING_ROUTE", gate_rows, route_rows[:-1], schema_rows, status_rows))
    g = deepcopy(gate_rows); g[7][2] = "DERIVED"; mutations.append(("M02_PROMOTE_NATIVE_EQUATION", g, route_rows, schema_rows, status_rows))
    g = deepcopy(gate_rows); g[8][2] = "DERIVED"; mutations.append(("M03_PROMOTE_BOUNDARY", g, route_rows, schema_rows, status_rows))
    g = deepcopy(gate_rows); g[5][2] = "SATISFIED_BY_ZERO_MODE"; mutations.append(("M04_ZERO_MODE_PROMOTION", g, route_rows, schema_rows, status_rows))
    r = deepcopy(route_rows); r[5][7] = "CONDITIONAL_JOINT_REALIZATION_ONLY"; mutations.append(("M05_ACTION_CONDITIONAL_PROMOTION", gate_rows, r, schema_rows, status_rows))
    r = deepcopy(route_rows); r[6][6] = "DERIVED_NATIVE"; mutations.append(("M06_CARRIER_PREMISE_PROMOTION", gate_rows, r, schema_rows, status_rows))
    r = deepcopy(route_rows); r[0][7] = "REGISTERED_NATIVE_JOINT_REALIZATION_FOUND"; mutations.append(("M07_FALSE_DIRECT_WITNESS", gate_rows, r, schema_rows, status_rows))
    s = deepcopy(status_rows); s[10][2] = "REGISTERED_NATIVE_JOINT_REALIZATION_FOUND"; mutations.append(("M08_OUTCOME_PROMOTION", gate_rows, route_rows, schema_rows, s))
    schema = deepcopy(schema_rows); schema[8][3] = "DERIVED"; mutations.append(("M09_CERTIFICATE_CONSTRUCTION_PROMOTION", gate_rows, route_rows, schema, status_rows))
    results = []
    for ident, gates, routes, schema, statuses in mutations:
        violations = contract_violations(gates, routes, schema, statuses)
        caught = bool(violations)
        checks.append({"id": ident, "kind": "MUTATION", "pass": caught, "detail": f"violations={violations}"})
        results.append({"id": ident, "caught": caught, "violations": violations})
    return results


def main() -> int:
    checks: list[dict[str, object]] = []
    source_inventory_checks(checks)
    source_anchor_checks(checks)
    controls = exact_controls(checks)
    violations = contract_violations(gate_rows, route_rows, schema_rows, status_rows)
    checks.append({"id": "D08_CONTRACT", "kind": "GUARD", "pass": not violations, "detail": f"violations={violations}"})
    complete_routes = [row[0] for row in route_rows[:7] if row[7] in {"REGISTERED_NATIVE_JOINT_REALIZATION_FOUND", "CONDITIONAL_JOINT_REALIZATION_ONLY"}]
    checks.append({"id": "D09_ZERO_COMPLETE_ROUTES", "kind": "SUBSTANTIVE", "pass": complete_routes == [], "detail": f"complete_routes={complete_routes}"})
    checks.append({"id": "D10_MINIMUM_TYPE_NOT_ACTION_PRIORITY", "kind": "GUARD", "pass": "an action is one possible package not a required form" in schema_rows[1][4] and schema_rows[8][3] == "IDENTIFIED_NOT_CONSTRUCTED", "detail": schema_rows[8][2]})
    mutations = exercise_mutations(checks)

    write_tsv(OUT / "JOINT_GATE_MATRIX.tsv", ["gate_id", "required_object", "current_status", "source_basis", "failure_or_limit"], gate_rows)
    write_tsv(OUT / "ROUTE_ADJUDICATION.tsv", ["route_id", "route", "full_field", "equation", "boundary", "same_nonzero_live", "premise_stack", "ruling", "reason"], route_rows)
    write_tsv(OUT / "COMMON_OBJECT_TYPE_SCHEMA.tsv", ["id", "symbol", "typed_role", "status", "obligation_or_limit"], schema_rows)
    write_tsv(OUT / "COUNTERMODEL_LEDGER.tsv", ["id", "control", "construction", "exact_result", "scope"], counter_rows)
    write_tsv(OUT / "STATUS_LEDGER.tsv", ["id", "object", "status", "basis", "limit"], status_rows)
    write_tsv(OUT / "SOURCE_ANCHOR_LEDGER.tsv", ["id", "path", "required_exact_token", "bounded_inference"], [list(row) for row in source_anchors])

    passed = all(bool(row["pass"]) for row in checks)
    result = {
        "audit": "UDT_JOINT_REALIZATION_CLOSURE",
        "outcome": OUTCOME,
        "passed": passed,
        "source_count": 140,
        "route_count": len(route_rows),
        "complete_route_count": len(complete_routes),
        "gate_count": len(gate_rows),
        "schema_count": len(schema_rows),
        "checks": checks,
        "controls": controls,
        "mutations": mutations,
        "maximum_conclusion": "bounded current-record theorem; no universal no-go, stability theorem, action selection, carrier selection, boundary adoption, or T4 authorization",
    }
    (OUT / "DERIVATION_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"outcome={OUTCOME}")
    print(f"sources=140 routes={len(route_rows)} complete_routes={len(complete_routes)} gates={len(gate_rows)} schema={len(schema_rows)}")
    print(f"checks={len(checks)} passed={sum(bool(row['pass']) for row in checks)} mutations={len(mutations)}")
    print("PASS" if passed else "FAIL")
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
