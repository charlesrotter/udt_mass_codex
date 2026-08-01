#!/usr/bin/env python3
"""Exact CPU controls and deterministic ledgers for the derivation-closure sweep.

The countermodels below are logic controls.  They prove scoped nonimplications from
the frozen premise set; they are not candidate UDT actions, time laws, or boundaries.
"""

from __future__ import annotations

import csv
import hashlib
import json
import platform
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parents[1]
PKG = Path(__file__).resolve().parent


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_tsv(name: str, records: list[dict[str, object]]) -> None:
    with (PKG / name).open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(records[0]), delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(records)


def require_text(path: str, needles: list[str]) -> None:
    text = (ROOT / path).read_text(encoding="utf-8")
    for needle in needles:
        if needle not in text:
            raise RuntimeError(f"source anchor missing in {path}: {needle}")


def main() -> None:
    logs: list[str] = []
    checks: list[dict[str, object]] = []

    def check(check_id: str, group: str, claim: str, condition: bool, detail: str) -> None:
        if not condition:
            raise RuntimeError(f"{check_id} failed: {claim}: {detail}")
        checks.append({"check_id": check_id, "group_id": group, "claim": claim, "result": "PASS", "detail": detail})
        logs.append(f"PASS {check_id} {group}: {claim} :: {detail}")

    # Source anchors are semantic guards, not independent derivations.
    require_text("udt_joint_realization_closure_audit_2026-08-01/AUDIT_REPORT.md", [
        "FORMAL_COMPATIBILITY_ONLY_COMMON_REALIZATION_OPEN", "JR_CERT_NATIVE",
    ])
    require_text("udt_p4_stability_slice_2026-07-30/EXACT_DERIVATION.md", [
        "SECOND germ", "ACTIVATES in the second variation", "UNPINNED by",
    ])
    require_text("udt_p4_boundary_action_gate_2026-07-30/EXACT_DERIVATION.md", [
        "N = 4 TYPED", "not run", "TYPED-OPEN",
    ])
    require_text("udt_p4_period_gate_2026-07-30/AUDIT_REPORT.md", [
        "NO QUANTIZATION", "open-end germs FREED",
    ])
    require_text("native_hopfion_topology_audit_2026-07-19/TOPOLOGY_STATUS_LEDGER.tsv", [
        "physical finite-cell carrier completion", "OPEN", "SETTLED_STATIC_FINITE_BOX_CONDITIONAL",
    ])
    require_text("udt_stability_foundations_audit_2026-08-01/AUDIT_REPORT.md", [
        "stable, unstable, and neutral", "native structure to turn",
    ])
    require_text("udt_bootstrap_to_local_response_map_audit_2026-07-25/AUDIT_REPORT.md", [
        "neither complete arrow", "arrow is yet complete", "DERIVED_CONDITIONAL_RESPONSE_SKELETON",
    ])
    check("S01", "ALL", "all seven semantic source anchors resolve", True, "frozen source texts matched")

    # Q02: same value and first germ, arbitrary second germ.
    z, eps, v = sp.symbols("z eps v", real=True)
    b0, b1, kappa = sp.symbols("b0 b1 kappa", real=True)
    B = b0 + b1 * z + sp.Rational(1, 2) * kappa * z**2
    lower = (sp.expand(B.subs(z, 0)), sp.diff(B, z).subs(z, 0))
    second = sp.diff(B, z, 2).subs(z, 0)
    check("G01", "Q02", "boundary value is independent of the second germ", lower[0] == b0, str(lower[0]))
    check("G02", "Q02", "first germ is independent of the second germ", lower[1] == b1, str(lower[1]))
    check("G03", "Q02", "second germ remains the free parameter kappa", second == kappa, str(second))
    B_eps = sp.expand(B.subs(z, eps * v))
    hessian = sp.diff(B_eps, eps, 2).subs(eps, 0)
    check("G04", "Q02", "the free second germ enters the wall Hessian", hessian == kappa * v**2, str(hessian))
    h0 = sp.simplify(hessian.subs(kappa, 0))
    h1 = sp.simplify(hessian.subs(kappa, 1))
    check("G05", "Q02", "two lower-germ-identical completions have different Hessians", h0 != h1, f"kappa=0:{h0};kappa=1:{h1}")
    J = sp.symbols("J", real=True)
    period_source = b1 + J
    check("G06", "Q02", "the registered first-germ period source is second-germ blind", sp.diff(period_source, kappa) == 0, str(period_source))

    # Q03: the same ring closure and stationary point admit opposite responses.
    x = sp.symbols("x", real=True)
    E1, E2, L1, L2 = sp.symbols("E1 E2 L1 L2", real=True)
    ring = E1 * L1 + E2 * L2
    check("R01", "Q03", "massless two-cell ring satisfies the exact period law", ring.subs({E1: 0, E2: 0}) == 0, str(ring))
    F_plus = sp.Rational(1, 2) * x**2
    F_minus = -sp.Rational(1, 2) * x**2
    F_flat = sp.Integer(0)
    slopes = [sp.diff(F, x).subs(x, 0) for F in (F_plus, F_minus, F_flat)]
    curvatures = [sp.diff(F, x, 2).subs(x, 0) for F in (F_plus, F_minus, F_flat)]
    check("R02", "Q03", "three response controls share the same stationary background", slopes == [0, 0, 0], str(slopes))
    check("R03", "Q03", "the same ring data admit positive, negative, and flat Hessians", curvatures == [1, -1, 0], str(curvatures))
    check("R04", "Q03", "ring closure does not algebraically contain the response coordinate", x not in ring.free_symbols, str(ring.free_symbols))

    # Q04: one static datum does not select a physical flow.
    q1, q2 = sp.symbols("q1 q2", real=True)
    qvec = sp.Matrix([q1, q2])
    E_static = sp.Rational(1, 2) * (q1**2 + q2**2)
    flows = {
        "contracting": sp.Matrix([-q1, -q2]),
        "rotating": sp.Matrix([-q2, q1]),
        "frozen": sp.Matrix([0, 0]),
    }
    check("T01", "Q04", "all three time controls share the same static equilibrium", all(F.subs({q1: 0, q2: 0}) == sp.zeros(2, 1) for F in flows.values()), str(E_static))
    jacobians = {name: F.jacobian(qvec) for name, F in flows.items()}
    check("T02", "Q04", "the shared static equilibrium has inequivalent linearized time laws", len({str(Jm) for Jm in jacobians.values()}) == 3, ";".join(f"{k}:{v}" for k, v in jacobians.items()))
    energy_rates = {name: sp.expand(sp.Matrix([sp.diff(E_static, q1), sp.diff(E_static, q2)]).dot(F)) for name, F in flows.items()}
    check("T03", "Q04", "the time controls have contracting, conserving, and frozen energy rates", list(energy_rates.values()) == [-q1**2 - q2**2, 0, 0], str(energy_rates))

    theta = sp.symbols("theta", real=True)
    s0 = sp.Matrix([0, 0, 1])
    s1 = sp.Matrix([sp.cos(theta), sp.sin(theta), 0])
    check("T04", "Q04", "one S2 fiber admits inequivalent unit sections", sp.simplify(s0.dot(s0)) == 1 and sp.simplify(s1.dot(s1)) == 1 and s0 != s1, f"s0={s0.T};s1={s1.T}")

    Bglob = sp.symbols("Bglob", real=True)
    maps = {"identity": Bglob, "contracting": Bglob / 2, "translation": Bglob + 1}
    fixed_sets = {
        "identity": "all",
        "contracting": sp.solve(sp.Eq(Bglob, maps["contracting"]), Bglob),
        "translation": sp.solve(sp.Eq(Bglob, maps["translation"]), Bglob),
    }
    check("T05", "Q04", "an unspecified bootstrap map admits all, one, or no fixed points", fixed_sets == {"identity": "all", "contracting": [0], "translation": []}, str(fixed_sets))

    source_paths = [
        ("A01", "Q01", "udt_joint_realization_closure_audit_2026-08-01/AUDIT_REPORT.md", "primary adjudication", "formal compatibility; common realized certificate open"),
        ("A02", "Q01", "udt_joint_realization_closure_audit_2026-08-01/JOINT_GATE_MATRIX.tsv", "mechanical joint gates", "common nonzero field/equation/boundary/tangent gates"),
        ("A03", "Q01", "udt_joint_realization_closure_audit_2026-08-01/ROUTE_ADJUDICATION.tsv", "route census", "eight construction routes do not supply JR_CERT_NATIVE"),
        ("A04", "Q02", "udt_p4_boundary_action_gate_2026-07-30/EXACT_DERIVATION.md", "wall-response provenance", "N2 first germs active; N4 typed open"),
        ("A05", "Q02", "udt_p4_stability_slice_2026-07-30/EXACT_DERIVATION.md", "Hessian provenance", "second germ enters Hessian and is unpinned"),
        ("A06", "Q02;Q03", "udt_p4_period_gate_2026-07-30/AUDIT_REPORT.md", "period/completion provenance", "periods constrain global first-order data, not a response or second germ"),
        ("A07", "Q03;Q04", "udt_stability_foundations_audit_2026-08-01/AUDIT_REPORT.md", "missing-law architecture", "response/time/domain joins remain open"),
        ("A08", "Q04", "native_hopfion_topology_audit_2026-07-19/TOPOLOGY_STATUS_LEDGER.tsv", "carrier/topology status", "fiber/section/boundary/time distinctions"),
        ("A09", "Q04", "udt_bootstrap_to_local_response_map_audit_2026-07-25/AUDIT_REPORT.md", "bootstrap response status", "two-arrow skeleton only; maps absent"),
        ("A10", "Q04", "udt_global_local_relational_closure_audit_2026-07-25/AUDIT_REPORT.md", "global-local closure status", "native off-shell response one-form absent"),
        ("A11", "ALL", "udt_stability_family_survivor_map_2026-08-01/SURVIVOR_LEDGER.tsv", "parent family status", "readiness and premise ceilings before sweep"),
    ]
    authorities = []
    for authority_id, group, path, role, claim in source_paths:
        authorities.append({"authority_id": authority_id, "group_id": group, "path": path, "sha256": sha256(ROOT / path), "role": role, "exact_claim": claim})
    write_tsv("SOURCE_AUTHORITY_LEDGER.tsv", authorities)

    objects = [
        {"object_id": "O01", "group_id": "Q01", "family": "F02;F07", "status": "FORMAL_COMPATIBILITY_ONLY", "exact_scope": "registered static/time/angular modules", "source_basis": "A01-A03", "branch_census": "8/8 routes adjudicated; separate modules exact", "witness_or_obstruction": "formal pullbacks and shared zero controls; no common nonzero on-shell field", "readiness_consequence": "no realized background"},
        {"object_id": "O02", "group_id": "Q01", "family": "F02;F07", "status": "UNDERDETERMINED_NO_NATIVE_OBJECT", "exact_scope": "complete common field system", "source_basis": "A01-A03", "branch_census": "no source-derived whole equation in any route", "witness_or_obstruction": "JR_CERT_NATIVE missing", "readiness_consequence": "on-shell status open"},
        {"object_id": "O03", "group_id": "Q01", "family": "F02;F07", "status": "PARTIAL_CONSTRAINT_ONLY", "exact_scope": "finite-cell boundary modules", "source_basis": "A01-A03", "branch_census": "static/time/angular boundary duties separately typed", "witness_or_obstruction": "no one differentiable boundary closes all modules", "readiness_consequence": "global domain open"},
        {"object_id": "O04", "group_id": "Q01", "family": "F02;F07", "status": "UNDERDETERMINED_NO_NATIVE_OBJECT", "exact_scope": "tangent at a common realized field", "source_basis": "A01-A03", "branch_census": "common realized field not supplied", "witness_or_obstruction": "no native tangent domain is defined before its base point and complete domain exist", "readiness_consequence": "variation test blocked"},
        {"object_id": "O05", "group_id": "Q01", "family": "F02;F07", "status": "PARTIAL_CONSTRAINT_ONLY", "exact_scope": "premise fiber product", "source_basis": "A01-A03", "branch_census": "module premise stacks separately nonempty", "witness_or_obstruction": "separate stack compatibility does not establish one common stack", "readiness_consequence": "joint premise stack open"},
        {"object_id": "O06", "group_id": "Q02", "family": "F01", "status": "DERIVED_SCOPED_OBSTRUCTION", "exact_scope": "banked jet<=2 wall/period/seal scope", "source_basis": "A04-A06;G01-G06", "branch_census": "fold;partner;glue;open;quotient/cyclic/acyclic periods", "witness_or_obstruction": "B_kappa shares value/first germ for every kappa but delta2B=kappa*v^2", "readiness_consequence": "full Hessian remains germ-conditional"},
        {"object_id": "O07", "group_id": "Q02", "family": "F01", "status": "PARTIAL_CONSTRAINT_ONLY", "exact_scope": "registered N4/period/holonomy/seal content", "source_basis": "A04-A06;G01-G06", "branch_census": "N4 is typed-not-run; periods/holonomy reach first/global data only", "witness_or_obstruction": "no explicit second-germ equation; lower constraints are kappa-blind", "readiness_consequence": "N4 ownership derivation still required"},
        {"object_id": "O08", "group_id": "Q03", "family": "F05", "status": "DERIVED_SCOPED_OBSTRUCTION", "exact_scope": "frozen ring/period identities", "source_basis": "A06-A07;R01-R04", "branch_census": "massless constant; all-definite massive excluded; mixed-sign conditional", "witness_or_obstruction": "same ring identity/background admits +x^2/2,-x^2/2,0 response controls", "readiness_consequence": "no F05-native stability object"},
        {"object_id": "O09", "group_id": "Q03", "family": "F05", "status": "UNDERDETERMINED_NO_NATIVE_OBJECT", "exact_scope": "ring perturbation/variation domain", "source_basis": "A06-A07", "branch_census": "period tangent constraints exist only after a response/domain choice", "witness_or_obstruction": "no native field pairing, norm, or boundary variation domain", "readiness_consequence": "second variation undefined"},
        {"object_id": "O10", "group_id": "Q03", "family": "F05", "status": "FORMAL_COMPATIBILITY_ONLY", "exact_scope": "ring closure identities", "source_basis": "A06;R01", "branch_census": "massless constant ring exact; mixed-sign full witness conditional", "witness_or_obstruction": "E1=E2=0 satisfies sum(E_i L_i)=0 but is not on shell for an absent response", "readiness_consequence": "no response-evaluation point"},
        {"object_id": "O11", "group_id": "Q04", "family": "F04", "status": "DERIVED_SCOPED_OBSTRUCTION", "exact_scope": "static chosen-functional finite-box data", "source_basis": "A07-A10;T01-T03", "branch_census": "contracting;rotating;frozen logic controls", "witness_or_obstruction": "identical static equilibrium admits three inequivalent time linearizations", "readiness_consequence": "time persistence undefined"},
        {"object_id": "O12", "group_id": "Q04", "family": "F04", "status": "UNDERDETERMINED_NO_NATIVE_OBJECT", "exact_scope": "physical carrier finite-cell completion", "source_basis": "A08-A10", "branch_census": "computational pinned box exists; physical boundary classes remain open", "witness_or_obstruction": "solver mask is not a selected physical boundary", "readiness_consequence": "global carrier domain open"},
        {"object_id": "O13", "group_id": "Q04", "family": "F04", "status": "PARTIAL_CONSTRAINT_ONLY", "exact_scope": "conditional Lorentzian null-direction S2 fiber", "source_basis": "A08;T04", "branch_census": "fiber exists conditionally; constant and varying sections both mathematical", "witness_or_obstruction": "a fiber admits inequivalent unit sections and selects neither", "readiness_consequence": "carrier emergence/transport open"},
        {"object_id": "O14", "group_id": "Q04", "family": "F04", "status": "UNDERDETERMINED_NO_NATIVE_OBJECT", "exact_scope": "time perturbations and topology propagation", "source_basis": "A07-A10", "branch_census": "static finite-box topology only", "witness_or_obstruction": "no native time law, physical boundary, or section defines the required perturbation/propagation rule", "readiness_consequence": "no persistence certificate"},
        {"object_id": "O15", "group_id": "Q04", "family": "F04", "status": "UNDERDETERMINED_NO_NATIVE_OBJECT", "exact_scope": "working global-local bootstrap schema", "source_basis": "A09-A10;T05", "branch_census": "identity/contracting/translation map controls", "witness_or_obstruction": "the schema admits all, one, or no fixed point until both maps are derived", "readiness_consequence": "no family membership selection"},
    ]
    write_tsv("OBJECT_STATUS_LEDGER.tsv", objects)

    groups = [
        {"group_id": "Q01", "families": "F02;F07", "result": "FORMAL_COMPATIBILITY_ONLY_COMMON_REALIZATION_OPEN", "object_status_census": "FORMAL_COMPATIBILITY_ONLY=1;PARTIAL_CONSTRAINT_ONLY=2;UNDERDETERMINED_NO_NATIVE_OBJECT=2", "exact_result": "the eight routes supply modules but not JR_CERT_NATIVE", "readiness_before": "BLOCKED_MISSING_FIXED_REALIZATION", "readiness_after": "BLOCKED_MISSING_FIXED_REALIZATION", "maximum_conclusion": "no common nonzero realized field has been derived or ruled out universally"},
        {"group_id": "Q02", "families": "F01", "result": "SECOND_GERM_NONUNIQUE_AT_BANKED_LAYER_N4_OPEN", "object_status_census": "DERIVED_SCOPED_OBSTRUCTION=1;PARTIAL_CONSTRAINT_ONLY=1", "exact_result": "lower wall and period data do not own the Hessian-active second germ", "readiness_before": "LOCAL_LAMBDA_CHECK_ONLY_FULL_HESSIAN_BLOCKED", "readiness_after": "LOCAL_LAMBDA_CHECK_ONLY_FULL_HESSIAN_BLOCKED", "maximum_conclusion": "nonuniqueness at frozen jet<=2 scope; not a no-go for a future N4 law"},
        {"group_id": "Q03", "families": "F05", "result": "RING_IDENTITIES_DO_NOT_DETERMINE_RESPONSE", "object_status_census": "DERIVED_SCOPED_OBSTRUCTION=1;UNDERDETERMINED_NO_NATIVE_OBJECT=1;FORMAL_COMPATIBILITY_ONLY=1", "exact_result": "period/mass identities admit inequivalent stationary response controls", "readiness_before": "BLOCKED_MISSING_NATIVE_RESPONSE", "readiness_after": "BLOCKED_MISSING_NATIVE_RESPONSE", "maximum_conclusion": "no F05 response/domain derived; ring family retained"},
        {"group_id": "Q04", "families": "F04", "result": "STATIC_DATA_DO_NOT_DETERMINE_TIME_BOUNDARY_OR_BOOTSTRAP", "object_status_census": "DERIVED_SCOPED_OBSTRUCTION=1;PARTIAL_CONSTRAINT_ONLY=1;UNDERDETERMINED_NO_NATIVE_OBJECT=3", "exact_result": "static carrier-conditional data admit inequivalent flows and sections; physical boundary/maps absent", "readiness_before": "BLOCKED_MISSING_TIME_EQUATION", "readiness_after": "BLOCKED_MISSING_TIME_EQUATION", "maximum_conclusion": "no physical time/boundary/bootstrap law derived; static finite-box result unchanged"},
    ]
    write_tsv("GROUP_RESULT_LEDGER.tsv", groups)

    branches = [
        {"branch_id": "B01", "group_id": "Q01", "branch": "eight registered construction routes", "coverage": "8/8", "result": "formal modules only; no JR_CERT_NATIVE", "source_basis": "A01-A03"},
        {"branch_id": "B02", "group_id": "Q02", "branch": "fold/quotient wall", "coverage": "covered", "result": "active first germ forced/inert at N2; second germ not owned", "source_basis": "A04-A06"},
        {"branch_id": "B03", "group_id": "Q02", "branch": "partner/germ-flat stratum", "coverage": "covered", "result": "chosen flat witness does not derive second germ", "source_basis": "A04-A06"},
        {"branch_id": "B04", "group_id": "Q02", "branch": "glue+pinned first germ", "coverage": "covered", "result": "value/first germ pinned; second germ free in Hessian", "source_basis": "A04-A06;G01-G06"},
        {"branch_id": "B05", "group_id": "Q02", "branch": "open endpoint", "coverage": "covered", "result": "first-germ functions free; no cycle reaches endpoint", "source_basis": "A04-A06"},
        {"branch_id": "B06", "group_id": "Q02", "branch": "N4/holonomy/period deeper layer", "coverage": "covered as registered", "result": "N4 typed-not-run; real period/holonomy equations contain no second-germ owner", "source_basis": "A04-A06"},
        {"branch_id": "B07", "group_id": "Q03", "branch": "massless constant cyclic ring", "coverage": "covered", "result": "exact closure witness; response absent", "source_basis": "A06;R01-R04"},
        {"branch_id": "B08", "group_id": "Q03", "branch": "all-definite massive cyclic ring", "coverage": "covered", "result": "excluded by period/mass law; not instability", "source_basis": "A06"},
        {"branch_id": "B09", "group_id": "Q03", "branch": "mixed-sign multicell ring", "coverage": "covered", "result": "conditional structural branch; full response/background not certified", "source_basis": "A06"},
        {"branch_id": "B10", "group_id": "Q04", "branch": "round-S2 L2+L4 finite-box static branch", "coverage": "covered", "result": "conditional static certificate retained", "source_basis": "A08"},
        {"branch_id": "B11", "group_id": "Q04", "branch": "physical carrier boundary", "coverage": "covered", "result": "open; computational mask cannot substitute", "source_basis": "A08-A10"},
        {"branch_id": "B12", "group_id": "Q04", "branch": "carrier section/transport", "coverage": "covered", "result": "conditional fiber only; section and transport open", "source_basis": "A08;T04"},
        {"branch_id": "B13", "group_id": "Q04", "branch": "native time response", "coverage": "covered", "result": "same static data admit inequivalent logic-control flows", "source_basis": "A07-A10;T01-T03"},
        {"branch_id": "B14", "group_id": "Q04", "branch": "bootstrap membership", "coverage": "covered", "result": "two-arrow architecture coherent; operation absent", "source_basis": "A09-A10;T05"},
    ]
    write_tsv("BRANCH_CENSUS.tsv", branches)
    q02_trace = [
        {"condition_id": "N4", "registered_layer": "fourth-order wall variation", "source_basis": "A04", "actual_content": "typed with 2-jet wall and third-derivative momenta; not run", "second_germ_effect": "OPEN_NO_EQUATION", "ruling": "cannot own the germ at the frozen layer"},
        {"condition_id": "R9", "registered_layer": "real periods on completion cycles", "source_basis": "A06", "actual_content": "cycle balances and supplied seam sources", "second_germ_effect": "NONE_IN_DERIVED_FORM", "ruling": "first/global data only"},
        {"condition_id": "J11", "registered_layer": "real affine holonomy", "source_basis": "A06", "actual_content": "real matrix/classification value on chart loops", "second_germ_effect": "NONE_IN_DERIVED_FORM", "ruling": "no wall-Hessian owner"},
        {"condition_id": "SEAL_PARITY", "registered_layer": "fold/glue/open posture wall rules", "source_basis": "A04-A05", "actual_content": "value and first-germ pins/forces at N2", "second_germ_effect": "FREE_ON_TRACE_ACTIVE_POSTURES", "ruling": "same lower data admit B_kappa family"},
        {"condition_id": "COMPLETE_CELL", "registered_layer": "quotient/cyclic/acyclic/open completion", "source_basis": "A06", "actual_content": "period strength differs by completion", "second_germ_effect": "NONE_IN_DERIVED_FORM", "ruling": "no completion branch supplies an equation"},
    ]
    write_tsv("Q02_CONDITION_TRACE.tsv", q02_trace)
    write_tsv("EXACT_CONTROL_LEDGER.tsv", checks)

    premises = [
        {"premise_id": "P01", "object": "UDT metric/Reciprocity/finite-cell record", "status": "PINNED_BY_FROZEN_THEORY_RECORD", "use": "source universe; no new premise"},
        {"premise_id": "P02", "object": "P4 response/action", "status": "CONDITIONAL_REGISTERED_ONLY", "use": "not transferred outside P4"},
        {"premise_id": "P03", "object": "second wall germ", "status": "FREE_AND_EXPLORED", "use": "kappa=0 and kappa=1 exact obstruction controls"},
        {"premise_id": "P04", "object": "N4 wall law", "status": "OPEN_TYPED_NOT_RUN", "use": "not invented; future falsifier of Q02 obstruction"},
        {"premise_id": "P05", "object": "F05 ring response/domain", "status": "OPEN", "use": "logic controls only; no action adopted"},
        {"premise_id": "P06", "object": "round S2 carrier", "status": "POSIT", "use": "F04 conditional branch only"},
        {"premise_id": "P07", "object": "L2+L4 carrier functional", "status": "CONDITIONAL_CHOSEN", "use": "static finite-box result only"},
        {"premise_id": "P08", "object": "computational box/mask", "status": "CHOSE_SOLVER_BOUNDARY", "use": "never promoted to physical boundary"},
        {"premise_id": "P09", "object": "native physical time law", "status": "OPEN", "use": "logic controls demonstrate nonselection"},
        {"premise_id": "P10", "object": "bootstrap global-local maps", "status": "WORKING_SCHEMA_MAPS_OPEN", "use": "not promoted to selection"},
        {"premise_id": "P11", "object": "countermodel functionals/flows", "status": "LOGIC_CONTROLS_NOT_UDT_PHYSICS", "use": "prove nonimplications only"},
        {"premise_id": "P12", "object": "GPU/stability solve", "status": "NOT_LAUNCHED", "use": "outside authorized sweep"},
    ]
    write_tsv("PREMISE_LEDGER.tsv", premises)

    readiness = [
        {"family": "F01", "before": "CPU_EXACT_CHECK_READY_LAMBDA_SCHUR_ONLY", "after": "CPU_EXACT_CHECK_READY_LAMBDA_SCHUR_ONLY", "delta": "NONE", "reason": "second germ remains unowned; local lambda check stays separately bounded"},
        {"family": "F02", "before": "BLOCKED_MISSING_FIXED_REALIZATION", "after": "BLOCKED_MISSING_FIXED_REALIZATION", "delta": "NONE", "reason": "Q01 supplies no common realized object"},
        {"family": "F04", "before": "BLOCKED_MISSING_TIME_EQUATION", "after": "BLOCKED_MISSING_TIME_EQUATION", "delta": "NONE", "reason": "time/boundary/section/bootstrap objects remain open"},
        {"family": "F05", "before": "BLOCKED_MISSING_NATIVE_RESPONSE", "after": "BLOCKED_MISSING_NATIVE_RESPONSE", "delta": "NONE", "reason": "ring identities do not determine response/domain"},
        {"family": "F07", "before": "BLOCKED_MISSING_FIXED_REALIZATION", "after": "BLOCKED_MISSING_FIXED_REALIZATION", "delta": "NONE", "reason": "formal modules do not supply realized field"},
    ]
    write_tsv("READINESS_DELTA.tsv", readiness)

    result = {
        "package": PKG.name,
        "outcome": "DERIVATION_SWEEP_MIXED_WITH_SCOPED_OBSTRUCTION",
        "groups": 4,
        "families": 5,
        "objects": 15,
        "source_authorities": len(authorities),
        "exact_controls": len(checks),
        "exact_controls_passed": sum(row["result"] == "PASS" for row in checks),
        "readiness_promotions": 0,
        "gpu_ready_families": 0,
        "stability_solves_launched": 0,
        "gpu_processes_launched": 0,
        "object_status_counts": {status: sum(row["status"] == status for row in objects) for status in sorted({row["status"] for row in objects})},
        "environment": {"python": platform.python_version(), "sympy": sp.__version__},
        "maximum_conclusion": "The sweep derives scoped nonselection/underdetermination results and partial constraints, but no missing native object closes and no readiness state advances.",
    }
    (PKG / "DERIVATION_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    logs.append(f"PASS sweep derivation: checks={len(checks)} outcome={result['outcome']} readiness_promotions=0")
    (PKG / "DERIVATION_STDOUT.txt").write_text("\n".join(logs) + "\n", encoding="utf-8")
    print(logs[-1])


if __name__ == "__main__":
    main()
