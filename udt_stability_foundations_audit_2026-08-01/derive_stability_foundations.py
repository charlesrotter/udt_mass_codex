#!/usr/bin/env python3
"""Deterministic CPU derivation and census for the UDT stability-foundations audit.

This script does not propose UDT dynamics.  Its small algebraic models are
countermodels proving that kinematic configuration data alone cannot determine a
stability verdict.  All repository conclusions are source-led and premise-scoped.
"""

from __future__ import annotations

import csv
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parents[1]
OUT = Path(__file__).resolve().parent


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


requirements = [
    ["R01", "GEOMETRIC_PERSISTENCE", "configuration/admissibility domain", "PARTIAL_DERIVED_REGISTERED", "metric/coframe and P4 formal response spaces are registered", "defines which configurations and formal deformations are kinematically admissible", "does not select a physical curve or realized solution"],
    ["R02", "GEOMETRIC_PERSISTENCE", "one-parameter admissible family", "FORMAL_ONLY", "P4 static/time/angular pointwise modules", "permits a curve through formal configuration space", "no native evolution or response selects the curve"],
    ["R03", "GEOMETRIC_PERSISTENCE", "fixed realized on-shell configuration", "OPEN", "P4 cold review Q2", "anchors persistence to one solution rather than a formal family", "formal module containment cannot establish realized coexistence"],
    ["R04", "GEOMETRIC_PERSISTENCE", "boundary/global completion along family", "OPEN", "finite-cell boundary and native-action ledgers", "keeps the family inside one physical finite-cell problem", "seal data alone do not complete the boundary problem"],
    ["R05", "ENERGETIC_OR_SPECTRAL_STABILITY", "functional or native response generator", "CONDITIONAL_OR_OPEN", "P4 stability slice; native-action final adjudication", "defines Hessian, spectrum, or flow", "metric kinematics alone admit opposite verdicts"],
    ["R06", "ENERGETIC_OR_SPECTRAL_STABILITY", "stationary/on-shell background", "CONDITIONAL_SLICES_ONLY", "P4 stability slice; corrected Hopfion work", "provides the configuration about which variation is taken", "no complete native joint solution is selected"],
    ["R07", "ENERGETIC_OR_SPECTRAL_STABILITY", "perturbation and variation domain", "PARTIAL_CHOSEN", "P4 stability slice premise stamps", "specifies allowed perturbations and constraints", "different domains can change an index or certificate"],
    ["R08", "ENERGETIC_OR_SPECTRAL_STABILITY", "gauge quotient or physical-reading rule", "OPEN_FORK", "P4 response and time-live audits", "separates gauge/calibration changes from physical modes", "formal response slots do not choose their physical reading"],
    ["R09", "ENERGETIC_OR_SPECTRAL_STABILITY", "norm, symplectic form, or dual pairing", "CONDITIONAL_OR_CHOSEN", "P4 pairing branches and particle operator", "defines size and spectral adjointness", "no complete native pairing is selected"],
    ["R10", "ENERGETIC_OR_SPECTRAL_STABILITY", "boundary domain and wall-germ data", "PARTIAL_CHOSEN_OPEN", "P4 stability slice", "makes the operator differentiable and fixes admissible boundary modes", "free higher wall germs block full certification"],
    ["R11", "ENERGETIC_OR_SPECTRAL_STABILITY", "conserved, monotone, or coercive certificate", "OPEN_NATIVE_CONDITIONAL_IN_SLICES", "P4 and Hopfion conditional energy/Hessian results", "turns bounded perturbations into a stability statement", "positive conditional Hessians are not native time stability"],
    ["R12", "ENERGETIC_OR_SPECTRAL_STABILITY", "topology/carrier", "CONDITIONAL_POSIT", "native Hopfion topology audit", "defines the matter configuration space where used", "celestial S2 fiber does not select the carrier or section"],
    ["R13", "BOOTSTRAP_SELF_CONSISTENCY", "global background/observable state", "WORKING_PARTIAL", "bootstrap response audits", "provides the global argument of the closure loop", "complete observable census and physical representative remain open"],
    ["R14", "BOOTSTRAP_SELF_CONSISTENCY", "global-to-local admissibility map", "OPEN", "bootstrap-to-local response ledger", "selects which local equations/branches a background admits", "a density window is an after-solution filter, not this map"],
    ["R15", "BOOTSTRAP_SELF_CONSISTENCY", "local-to-global response map", "OPEN", "bootstrap-to-local response ledger", "recomputes mass/energy/curvature observables from local structures", "native mass, source, boundary charge, and total ledger are absent"],
    ["R16", "BOOTSTRAP_SELF_CONSISTENCY", "fixed-point existence and branch selection", "TYPE_SCHEMA_ONLY", "bootstrap closure audits", "requires a common state satisfying both arrows", "a typed fixed-point equation supplies neither map nor a solution"],
    ["R17", "BOOTSTRAP_SELF_CONSISTENCY", "fixed-point linearization and stability criterion", "OPEN", "bootstrap-to-local response ledger", "tests whether a self-consistent state persists under coupled changes", "no derivative, norm, or spectrum is selected"],
]

fixed_gate = [
    ["G01", "common configuration type U", "PARTIAL", "metric/coframe/P4 alphabets are registered", "field ownership and complete physical object remain open"],
    ["G02", "static module inclusion i_static", "FORMAL_EXACT_IN_SCOPE", "banked P4 static module", "not a fixed realized solution"],
    ["G03", "time-live module inclusion i_time", "FORMAL_EXACT_IN_SCOPE", "banked P4 T2 plus cold regrade", "integration/gauge closure and on-shell coexistence open"],
    ["G04", "angular-live module inclusion i_angular", "FORMAL_EXACT_IN_SCOPE", "banked P4 angular module plus cold regrade", "on-shell coexistence and global completion open"],
    ["G05", "one common full field assignment u with nonzero time-live and angular-live sectors when live coexistence is claimed", "OPEN", "P4 cold review Q2 and A2 correction", "a shared static or mode-zero member is only a compatibility control, not a live coexistence witness"],
    ["G06", "native whole-system equation E_native[u]=0", "OPEN", "native-action final adjudication", "complete native action/response/source is open"],
    ["G07", "one differentiable finite-cell boundary condition B_native[u]=0", "OPEN", "boundary and native-action ledgers", "seal parity alone is insufficient"],
    ["G08", "one compatible premise stack", "PARTIAL", "premise registry and cold-review regrades", "conditional action/carrier/reading branches must not be silently merged"],
    ["G09", "nonempty compatible realized pullback/fiber-product R_live", "OPEN", "G05-G08", "formal module images or a common zero mode do not prove this realized live set nonempty"],
    ["G10", "native stability test on T_u R", "BLOCKED_BY_MISSING_JOIN", "R03-R17", "requires a realized u plus response/certificate/boundary/pairing data"],
]

bootstrap_schema = [
    ["B01", "B", "global background/observable state", "WORKING_PARTIAL", "density/curvature/scale candidates exist; complete ontology open"],
    ["B02", "A(B)", "global-to-local admissibility/equation data", "OPEN", "must map B to local equations, coefficients, boundaries, or admitted branches"],
    ["B03", "u in Sol(A(B))", "realized local finite-cell solution", "OPEN", "requires native equation, boundary, and joint static/time/angular realization"],
    ["B04", "R(u)", "local-to-global observable response", "OPEN", "requires native mass/energy/curvature/source and global aggregation"],
    ["B05", "B = R(u)", "self-consistency equation", "DERIVED_AS_TYPE_SCHEMA_ONLY", "well-typed once B, A, Sol, and R are independently supplied"],
    ["B06", "Fix(R o Sol o A)", "fixed-point set", "OPEN", "existence/uniqueness cannot be inferred from the schema"],
    ["B07", "D(R o Sol o A)", "linear response around a fixed point", "OPEN", "the derivative cannot exist as a determined object before both arrows and branch regularity"],
    ["B08", "rho=M/V", "density quotient", "DERIVED_CONDITIONAL", "delta rho=(delta M-rho delta V)/V for same-solution native M and V; M is open"],
    ["B09", "stability of fixed point", "bootstrap persistence", "OPEN", "needs a topology/norm and a specified update or dynamical law; contraction is not assumed"],
]

countermodels = [
    ["C01", "same scalar configuration q and equilibrium q=0", "q_dot=-q", "V=q^2/2; dV/dt=-q^2", "ASYMPTOTICALLY_STABLE", "logic control only; not a UDT law"],
    ["C02", "same scalar configuration q and equilibrium q=0", "q_dot=+q", "V=q^2/2; dV/dt=+q^2", "UNSTABLE", "logic control only; not a UDT law"],
    ["C03", "same scalar configuration q and equilibrium q=0", "q_dot=0", "V=q^2/2; dV/dt=0", "NEUTRAL", "logic control only; not a UDT law"],
    ["C04", "same scalar configuration q and background q=0", "E_plus=q^2/2", "Hessian=+1", "STRICT_LOCAL_MINIMUM", "shows a functional is load-bearing"],
    ["C05", "same scalar configuration q and background q=0", "E_minus=-q^2/2", "Hessian=-1", "STRICT_LOCAL_MAXIMUM", "shows metric/configuration data do not fix energetic sign"],
    ["C06", "same bootstrap state line B", "F(B)=B/2", "fixed point 0; derivative 1/2", "CONTRACTING_FIXED_POINT", "logic control only; no UDT map selected"],
    ["C07", "same bootstrap state line B", "F(B)=2B", "fixed point 0; derivative 2", "EXPANDING_FIXED_POINT", "logic control only; no UDT map selected"],
    ["C08", "same bootstrap state line B", "F(B)=B+1", "no fixed point", "NO_FIXED_POINT", "logic control only; schema does not imply closure"],
]

status_rows = [
    ["S01", "metric/P4 kinematic response architecture", "DERIVED_OR_REGISTERED_IN_STATED_SCOPES", "formal configuration and response modules exist", "not a native physical evolution"],
    ["S02", "static/time/angular formal module embeddings", "FORMAL_EXACT_IN_SCOPE", "banked package controls and cold parser/regrade", "fixed realized on-shell coexistence open"],
    ["S03", "fixed realized static/time/angular-live finite-cell solution with nonzero live sectors", "OPEN", "corrected compatible pullback gate G05-G09 fails open", "a purely static or mode-zero control does not pass; no negative existence claim beyond audited sources"],
    ["S04", "native evolution or response selector", "OPEN", "native-action and time-live ledgers", "formal time dependence is not physical dynamics"],
    ["S05", "geometric persistence", "KINEMATICALLY_DEFINABLE_NOT_PHYSICALLY_SELECTED", "admissible one-parameter families can be mapped", "no physical family is selected"],
    ["S06", "P4 reduced stationary stability slice", "DERIVED_CONDITIONAL", "registered quadratic jet<=2 slice, named postures/pairings/wall germs", "not whole joint or dynamical stability"],
    ["S07", "corrected no-null Hopfion static finite-box stability", "SETTLED_WITHIN_CONDITIONAL_PREMISES", "S2 carrier, L2+L4 functional, finite box, audited operator", "not carrier emergence, infinite-volume, or time persistence"],
    ["S08", "native energetic/spectral stability", "OPEN", "functional/domain/pairing/boundary are not jointly selected", "opposite-Hessian controls establish underdetermination"],
    ["S09", "bootstrap fixed-point architecture", "DERIVED_CONDITIONAL_RESPONSE_SKELETON", "two-arrow type structure and density quotient variation", "maps, fixed point, derivative, and stability remain open"],
    ["S10", "bootstrap supplies native stability", "OPEN", "no complete A or R map", "working interpretation is not a theorem"],
    ["S11", "complete native action", "OPEN", "final native-action adjudication", "an action may implement closure but is not assumed to precede it"],
    ["S12", "minimal missing realization join", "IDENTIFIED", "one common u plus E_native plus B_native plus compatible premises", "identification does not construct the join"],
    ["S13", "minimal missing persistence join", "IDENTIFIED", "native response/evolution or certificate with perturbation domain, pairing, and boundary", "identification does not choose action, carrier, or dynamics"],
    ["S14", "current whole-audit outcome", "FOUNDATIONS_PARTIAL_MINIMAL_JOIN_IDENTIFIED", "requirement census plus exact underdetermination controls", "current operational stability remains CONDITIONAL_STABILITY_ONLY"],
]


def check_source_manifest(checks: list[dict[str, object]]) -> None:
    entries = []
    with (OUT / "SOURCE_INVENTORY.tsv").open(encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle, delimiter="\t"):
            entries.append(row)
    ok = len(entries) == 94 and len({r["path"] for r in entries}) == 94
    checks.append({"id": "D01_SOURCE_COUNT", "kind": "SUBSTANTIVE", "pass": ok, "detail": f"rows={len(entries)} unique={len({r['path'] for r in entries})}"})
    mismatches = []
    for row in entries:
        path = ROOT / row["path"]
        if not path.is_file() or sha256(path) != row["sha256"] or path.stat().st_size != int(row["bytes"]):
            mismatches.append(row["path"])
    checks.append({"id": "D02_SOURCE_IDENTITY", "kind": "SUBSTANTIVE", "pass": not mismatches, "detail": f"mismatches={mismatches}"})


def source_token_checks(checks: list[dict[str, object]]) -> None:
    anchors = [
        ("D03_P4_SCOPE", ROOT / "udt_p4_stability_slice_2026-07-30/STABILITY_LEDGER.tsv", "UNDEFINED-AT-LAYER"),
        ("D04_COLD_Q2", ROOT / "udt_p4_cold_adversarial_review_2026-08-01/PREMISE_QUANTIFIER_AUDIT.tsv", "FIXED_REALIZED_SOLUTION_OPEN"),
        ("D05_NATIVE_ACTION", ROOT / "native_action_final_adjudication_2026-07-18/FINAL_STATUS_LEDGER.tsv", "Complete native action\tOPEN"),
        ("D06_BOOTSTRAP_MAP", ROOT / "udt_bootstrap_to_local_response_map_audit_2026-07-25/STATUS_LEDGER.tsv", "complete_bootstrap_to_local_map\tOPEN"),
        ("D07_HOPFION_SCOPE", ROOT / "native_hopfion_topology_audit_2026-07-19/AUDIT_REPORT.md", "carrier"),
    ]
    for ident, path, token in anchors:
        text = path.read_text(encoding="utf-8")
        checks.append({"id": ident, "kind": "SUBSTANTIVE", "pass": token in text, "detail": f"{path.relative_to(ROOT)} contains required scoped token"})


def exact_countermodel_checks(checks: list[dict[str, object]]) -> dict[str, object]:
    q, b = sp.symbols("q b", real=True)
    V = q**2 / 2
    flow_results = {}
    for name, flow, expected in (("stable", -q, -q**2), ("unstable", q, q**2), ("neutral", sp.Integer(0), sp.Integer(0))):
        value = sp.expand(sp.diff(V, q) * flow)
        ok = sp.simplify(value - expected) == 0
        checks.append({"id": f"D08_FLOW_{name.upper()}", "kind": "SUBSTANTIVE", "pass": ok, "detail": f"dV/dt={value}"})
        flow_results[name] = str(value)
    hplus = sp.diff(q**2 / 2, q, 2)
    hminus = sp.diff(-q**2 / 2, q, 2)
    checks.append({"id": "D09_OPPOSITE_HESSIANS", "kind": "SUBSTANTIVE", "pass": hplus == 1 and hminus == -1, "detail": f"hplus={hplus} hminus={hminus}"})
    fixed = {
        "contract": sp.solve(sp.Eq(b, b / 2), b),
        "expand": sp.solve(sp.Eq(b, 2 * b), b),
        "shift": sp.solve(sp.Eq(b, b + 1), b),
    }
    derivatives = {"contract": sp.Rational(1, 2), "expand": sp.Integer(2), "shift": sp.Integer(1)}
    ok = fixed["contract"] == [0] and fixed["expand"] == [0] and fixed["shift"] == []
    checks.append({"id": "D10_BOOTSTRAP_COUNTERMODELS", "kind": "SUBSTANTIVE", "pass": ok, "detail": f"fixed={fixed} derivatives={derivatives}"})
    return {"flow_dVdt": flow_results, "hessians": {"plus": str(hplus), "minus": str(hminus)}, "bootstrap_fixed_points": {k: [str(x) for x in v] for k, v in fixed.items()}, "bootstrap_derivatives": {k: str(v) for k, v in derivatives.items()}}


def structural_checks(checks: list[dict[str, object]]) -> None:
    req_ids = [r[0] for r in requirements]
    checks.append({"id": "D11_REQUIREMENT_COMPLETENESS", "kind": "GUARD", "pass": len(req_ids) == 17 and len(set(req_ids)) == 17 and all(all(cell for cell in row) for row in requirements), "detail": f"rows={len(req_ids)}"})
    gate_ids = [r[0] for r in fixed_gate]
    checks.append({"id": "D12_GATE_COMPLETENESS", "kind": "GUARD", "pass": len(gate_ids) == 10 and len(set(gate_ids)) == 10 and all(all(cell for cell in row) for row in fixed_gate), "detail": f"rows={len(gate_ids)}"})
    schema_ids = [r[0] for r in bootstrap_schema]
    checks.append({"id": "D13_SCHEMA_NOT_MAP", "kind": "GUARD", "pass": len(schema_ids) == 9 and bootstrap_schema[4][3] == "DERIVED_AS_TYPE_SCHEMA_ONLY" and bootstrap_schema[1][3] == "OPEN" and bootstrap_schema[3][3] == "OPEN", "detail": "type schema retained; both maps OPEN"})
    statuses = {r[0]: r[2] for r in status_rows}
    checks.append({"id": "D14_NO_SCOPE_PROMOTION", "kind": "GUARD", "pass": statuses["S06"] == "DERIVED_CONDITIONAL" and statuses["S07"] == "SETTLED_WITHIN_CONDITIONAL_PREMISES" and statuses["S08"] == "OPEN" and statuses["S10"] == "OPEN", "detail": "conditional P4/Hopfion results not promoted"})
    checks.append({"id": "D15_OUTCOME_CEILING", "kind": "GUARD", "pass": statuses["S14"] == "FOUNDATIONS_PARTIAL_MINIMAL_JOIN_IDENTIFIED", "detail": statuses["S14"]})


def contract_violations(
    req_rows: list[list[str]],
    gate_rows: list[list[str]],
    schema_rows: list[list[str]],
    ledger_rows: list[list[str]],
) -> list[str]:
    """One production predicate used for both the real package and mutations."""
    bad: list[str] = []
    if [r[0] for r in req_rows] != [f"R{i:02d}" for i in range(1, 18)]:
        bad.append("requirements_exact_R01_R17")
    if [r[0] for r in gate_rows] != [f"G{i:02d}" for i in range(1, 11)]:
        bad.append("gates_exact_G01_G10")
    if [r[0] for r in schema_rows] != [f"B{i:02d}" for i in range(1, 10)]:
        bad.append("schema_exact_B01_B09")
    if any(not cell for table in (req_rows, gate_rows, schema_rows, ledger_rows) for row in table for cell in row):
        bad.append("no_blank_cells")
    req_status = {r[0]: r[3] for r in req_rows}
    gate_status = {r[0]: r[2] for r in gate_rows}
    schema_status = {r[0]: r[3] for r in schema_rows}
    ledger_status = {r[0]: r[2] for r in ledger_rows}
    expected = {
        "R12": (req_status, "CONDITIONAL_POSIT"),
        "G05": (gate_status, "OPEN"),
        "G06": (gate_status, "OPEN"),
        "G07": (gate_status, "OPEN"),
        "G09": (gate_status, "OPEN"),
        "B02": (schema_status, "OPEN"),
        "B04": (schema_status, "OPEN"),
        "B05": (schema_status, "DERIVED_AS_TYPE_SCHEMA_ONLY"),
        "S06": (ledger_status, "DERIVED_CONDITIONAL"),
        "S07": (ledger_status, "SETTLED_WITHIN_CONDITIONAL_PREMISES"),
        "S08": (ledger_status, "OPEN"),
        "S10": (ledger_status, "OPEN"),
        "S11": (ledger_status, "OPEN"),
        "S14": (ledger_status, "FOUNDATIONS_PARTIAL_MINIMAL_JOIN_IDENTIFIED"),
    }
    for ident, (mapping, value) in expected.items():
        if mapping.get(ident) != value:
            bad.append(f"{ident}_must_equal_{value}")
    return bad


def live_witness_violations(witness: dict[str, bool]) -> list[str]:
    required = (
        "same_field",
        "on_shell",
        "same_boundary",
        "same_premises",
        "time_live_nonzero",
        "angular_live_nonzero",
    )
    return [key for key in required if not witness.get(key, False)]


def mutation_catches() -> list[dict[str, object]]:
    catches = []
    baseline_bad = contract_violations(requirements, fixed_gate, bootstrap_schema, status_rows)
    if baseline_bad:
        raise AssertionError(f"production contract fails before mutation: {baseline_bad}")
    missing = requirements[:-1]
    bad = contract_violations(missing, fixed_gate, bootstrap_schema, status_rows)
    catches.append({"id": "M01_MISSING_REQUIREMENT", "pass": "requirements_exact_R01_R17" in bad, "mutation": "remove R17", "rejection_reason": bad})
    promoted = [row[:] for row in status_rows]
    promoted[7][2] = "DERIVED_NATIVE"
    bad = contract_violations(requirements, fixed_gate, bootstrap_schema, promoted)
    catches.append({"id": "M02_PROMOTE_NATIVE_STABILITY", "pass": "S08_must_equal_OPEN" in bad, "mutation": "change S08 OPEN to DERIVED_NATIVE", "rejection_reason": bad})
    gate = [row[:] for row in fixed_gate]
    gate[4][2] = "DERIVED"
    bad = contract_violations(requirements, gate, bootstrap_schema, status_rows)
    catches.append({"id": "M03_INVENT_JOINT_WITNESS", "pass": "G05_must_equal_OPEN" in bad, "mutation": "change G05 OPEN to DERIVED", "rejection_reason": bad})
    schema = [row[:] for row in bootstrap_schema]
    schema[4][3] = "DERIVED_MAP"
    bad = contract_violations(requirements, fixed_gate, schema, status_rows)
    catches.append({"id": "M04_SCHEMA_AS_MAP", "pass": "B05_must_equal_DERIVED_AS_TYPE_SCHEMA_ONLY" in bad, "mutation": "promote B05 schema to map", "rejection_reason": bad})
    req = [row[:] for row in requirements]
    req[11][3] = "DERIVED_NATIVE"
    bad = contract_violations(req, fixed_gate, bootstrap_schema, status_rows)
    catches.append({"id": "M05_PROMOTE_CARRIER", "pass": "R12_must_equal_CONDITIONAL_POSIT" in bad, "mutation": "promote R12 carrier", "rejection_reason": bad})
    blanked = [row[:] for row in requirements]
    blanked[0][6] = ""
    bad = contract_violations(blanked, fixed_gate, bootstrap_schema, status_rows)
    catches.append({"id": "M06_BLANK_COMPLETENESS_CELL", "pass": "no_blank_cells" in bad, "mutation": "blank R01 limit", "rejection_reason": bad})
    static_only = {
        "same_field": True,
        "on_shell": True,
        "same_boundary": True,
        "same_premises": True,
        "time_live_nonzero": False,
        "angular_live_nonzero": False,
    }
    bad = live_witness_violations(static_only)
    catches.append({"id": "M07_STATIC_ZERO_MODE_AS_LIVE_WITNESS", "pass": bad == ["time_live_nonzero", "angular_live_nonzero"], "mutation": "offer a common static/mode-zero witness as time/angular-live coexistence", "rejection_reason": bad})
    # Every mutation is passed through the same production predicate as the unmutated package.
    return catches


def main() -> int:
    checks: list[dict[str, object]] = []
    check_source_manifest(checks)
    source_token_checks(checks)
    algebra = exact_countermodel_checks(checks)
    structural_checks(checks)

    write_tsv(OUT / "STABILITY_REQUIREMENT_MATRIX.tsv", ["id", "stability_notion", "required_object", "current_status", "source_basis", "typed_role", "open_limit"], requirements)
    write_tsv(OUT / "FIXED_REALIZATION_GATE.tsv", ["id", "gate_object", "current_status", "source_basis", "failure_or_limit"], fixed_gate)
    write_tsv(OUT / "BOOTSTRAP_FIXED_POINT_SCHEMA.tsv", ["id", "symbol", "typed_object", "current_status", "exact_scope_or_limit"], bootstrap_schema)
    write_tsv(OUT / "COUNTERMODEL_LEDGER.tsv", ["id", "shared_data", "supplied_law_or_functional", "exact_check", "verdict", "scope_warning"], countermodels)
    write_tsv(OUT / "STATUS_LEDGER.tsv", ["id", "object", "status", "basis", "limit"], status_rows)

    catches = mutation_catches()
    all_checks_pass = all(bool(row["pass"]) for row in checks)
    all_catches_pass = all(bool(row["pass"]) for row in catches)
    result = {
        "audit": "UDT_STABILITY_FOUNDATIONS_2026-08-01",
        "base": "5adeb59dde063770c0619d37b76b03f735d82038",
        "python_version": sys.version.split()[0],
        "sympy_version": sp.__version__,
        "question_posture": "METRIC_LED_OBSERVING_NOT_TARGETING",
        "primary_outcome": "FOUNDATIONS_PARTIAL_MINIMAL_JOIN_IDENTIFIED",
        "current_operational_stability": "CONDITIONAL_STABILITY_ONLY",
        "fixed_realized_on_shell_coexistence": "OPEN",
        "native_evolution_or_response": "OPEN",
        "bootstrap_map": "OPEN_TWO_ARROWS_TYPE_SCHEMA_ONLY",
        "algebra": algebra,
        "checks": checks,
        "mutation_catches": catches,
        "counts": {
            "requirements": len(requirements),
            "fixed_realization_gates": len(fixed_gate),
            "bootstrap_schema_rows": len(bootstrap_schema),
            "countermodels": len(countermodels),
            "status_rows": len(status_rows),
            "checks": len(checks),
            "substantive_checks": Counter(row["kind"] for row in checks)["SUBSTANTIVE"],
            "guard_checks": Counter(row["kind"] for row in checks)["GUARD"],
            "mutation_catches": len(catches),
        },
        "pass": all_checks_pass and all_catches_pass,
    }
    (OUT / "DERIVATION_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    lines = []
    for row in checks:
        lines.append(f"{row['id']}\t{row['kind']}\t{'PASS' if row['pass'] else 'FAIL'}\t{row['detail']}")
    for row in catches:
        lines.append(f"{row['id']}\tMUTATION_CATCH\t{'PASS' if row['pass'] else 'FAIL'}\t{row['mutation']} rejected: {row.get('rejection_reason', 'invariant failure')}")
    lines.append(f"RESULT\t{'PASS' if result['pass'] else 'FAIL'}\t{result['primary_outcome']}\tchecks={len(checks)} catches={len(catches)}")
    stdout = "\n".join(lines) + "\n"
    (OUT / "DERIVATION_STDOUT.txt").write_text(stdout, encoding="utf-8")
    print(stdout, end="")
    return 0 if result["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
