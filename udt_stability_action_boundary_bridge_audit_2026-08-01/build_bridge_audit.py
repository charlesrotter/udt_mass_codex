#!/usr/bin/env python3
"""Build the preregistered stability/action boundary-bridge audit."""

from __future__ import annotations

import csv
import hashlib
import json
import re
import subprocess
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parents[1]
OUT = Path(__file__).resolve().parent
BASE = "3d136a8"
OUTCOME = "PARTIAL_ANALOGIES_ONLY__F01_BOUNDARY_BRIDGE_OPEN"

SOURCE_ROOTS = (
    "native_action_final_adjudication_2026-07-18/",
    "native_action_arm_c_2026-07-18/",
    "native_action_stage1_2026-07-18/",
    "native_action_stage2_2026-07-18/",
    "native_action_external_verifier_2026-07-18/",
    "udt_native_stability_configuration_space_audit_2026-08-01/",
    "udt_f01_lambda_schur_check_2026-08-01/",
    "udt_stability_derivation_closure_sweep_2026-08-01/",
    "udt_p4_boundary_action_gate_2026-07-30/",
    "udt_p4_stability_slice_2026-07-30/",
)
SOURCE_FILES = {
    "UDT_GR_TO_UDT_SELECTOR_AUDIT_2026-07-18.md",
    "UDT_GR_TO_UDT_SELECTOR_AUDIT_PREREG_2026-07-18.md",
    "UDT_NATIVE_ACTION_DERIVATION_DISPATCH.md",
    "CURRENT_SCIENTIFIC_PREMISES.md",
    "CURRENT_SCIENTIFIC_PREMISES.tsv",
    "PONDER_MATH_ELEGANCE_2026-07-31.md",
}


def git(*args: str, binary: bool = False):
    proc = subprocess.run(["git", *args], cwd=ROOT, check=True, capture_output=True)
    return proc.stdout if binary else proc.stdout.decode("utf-8")


def write_tsv(name: str, header: list[str], rows: list[list[str]]) -> None:
    with (OUT / name).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
        writer.writerow(header)
        writer.writerows(rows)


def source_inventory() -> tuple[list[dict[str, object]], dict[str, bytes]]:
    tree = git("ls-tree", "-r", "-z", "--long", BASE, binary=True)
    rows: list[dict[str, object]] = []
    payloads: dict[str, bytes] = {}
    for token in tree.split(b"\0"):
        if not token:
            continue
        meta, raw_path = token.split(b"\t", 1)
        _mode, kind, blob, size = meta.decode().split()
        path = raw_path.decode("utf-8")
        selected = path in SOURCE_FILES or any(path.startswith(root) for root in SOURCE_ROOTS)
        if not selected:
            continue
        if kind != "blob":
            raise RuntimeError(f"non-blob source: {path}")
        data = git("cat-file", "blob", blob, binary=True)
        if len(data) != int(size):
            raise RuntimeError(f"size mismatch: {path}")
        payloads[path] = data
        rows.append({
            "path": path,
            "git_blob": blob,
            "bytes": int(size),
            "sha256": hashlib.sha256(data).hexdigest(),
        })
    rows.sort(key=lambda row: str(row["path"]))
    return rows, payloads


AUTHORITIES = [
    ["A01", "native_action_final_adjudication_2026-07-18/FINAL_ADJUDICATION_REPORT.md", "FINAL", "C2/Bach is unique-conditional only in the registered pre-scale bulk class; EH is conditional post-scale; complete variation and finite-cell boundary remain open."],
    ["A02", "native_action_final_adjudication_2026-07-18/FINAL_STATUS_LEDGER.tsv", "FINAL", "S10, S23, and S24 remain OPEN; S11-S13 are unique-conditional bulk statements; S14 is conditional."],
    ["A03", "UDT_GR_TO_UDT_SELECTOR_AUDIT_2026-07-18.md", "HISTORICAL_CONDITIONAL_SELECTOR_AUDIT", "The variation-before-scale versus representative-before-variation discriminator was missing; current use is controlled by the later premise registry."],
    ["A04", "native_action_arm_c_2026-07-18/ARM_C_RETURN/ARM_C_REPORT.md", "FROZEN_ADVERSARIAL", "Variation domains are inequivalent; total derivatives preserve bulk equations while shifting boundary momentum; both action routes lack finite-cell completion."],
    ["A05", "native_action_arm_c_2026-07-18/ARM_C_RETURN/cas_armc_variation_domain.py", "FROZEN_ALGEBRA", "Tangent restriction can lose normal equations and cannot be replaced by a hand-imposed equation."],
    ["A06", "native_action_arm_c_2026-07-18/ARM_C_RETURN/cas_armc_boundary_charge.py", "FROZEN_ALGEBRA", "Bulk Euler invariance does not fix the boundary primitive, reference, or normalization."],
    ["A07", "udt_p4_boundary_action_gate_2026-07-30/AUDIT_REPORT.md", "CONDITIONAL_P4", "The P4 wall response is conditional; N4 and corners are typed but do not supply the missing equation."],
    ["A08", "udt_p4_boundary_action_gate_2026-07-30/EXACT_DERIVATION.md", "CONDITIONAL_P4", "The boundary function is generic; selective content remains typed-open and is not a derived preferred boundary."],
    ["A09", "udt_f01_lambda_schur_check_2026-08-01/AUDIT_REPORT.md", "VERIFIED_F01", "All four exact local domains have joint index one; the independently free second wall germ remains unowned."],
    ["A10", "udt_f01_lambda_schur_check_2026-08-01/EXACT_DERIVATION.md", "VERIFIED_F01", "F01 fixes an exact conditional joint Hessian in p,f,h,lambda/mu and the R05/R06 plus Dirichlet/free-right forks."],
    ["A11", "udt_native_stability_configuration_space_audit_2026-08-01/AUDIT_REPORT.md", "VERIFIED_NATIVE_ARENA", "The complete metric/coframe supplies a typed off-shell arena but no selected realized variation law."],
    ["A12", "udt_stability_derivation_closure_sweep_2026-08-01/AUDIT_REPORT.md", "VERIFIED_CLOSURE_SWEEP", "Jet<=2 data do not own the second germ; N4 is typed without an equation."],
    ["A13", "PONDER_MATH_ELEGANCE_2026-07-31.md", "WORKING_LEAD_ONLY", "Global-local closure and taxonomy-times-stability are hypotheses to test, not affirmative action or boundary authority."],
    ["A14", "CURRENT_SCIENTIFIC_PREMISES.tsv", "CURRENT_PRECEDENCE", "G04 makes strong local CSN inactive without explicit reauthorization; G10 makes C2/Bach inactive without that premise; G11 leaves EH conditional and unselected."],
]

GATES = [
    "varied_object_and_field_identity",
    "common_background_and_onshell_realization",
    "tangent_domain_and_gauge_quotient",
    "derivative_order_and_principal_symbol",
    "boundary_polarization_and_differentiability",
    "boundary_functional_and_charge",
    "explicit_reduction_to_p_f_h_lambda",
    "preservation_of_R05_R06_trace_fork",
    "ownership_of_second_wall_germ",
    "scale_ordering_and_bootstrap_dependence",
    "carrier_and_source_independence",
    "full_premise_stack_compatibility",
]

ROUTE_GATES = {
    "C2_BACH_PRE_SCALE": [
        ("BLOCK", "unrestricted metric variation is not identified with the conditional P4 fields"),
        ("BLOCK", "no shared F01 background is constructed or proved Bach-on-shell"),
        ("BLOCK", "reciprocal hard/multiplier/readout domains remain inequivalent"),
        ("CONDITIONAL_ANALOGY_ONLY", "fourth-order bulk suggests v and v-prime boundary slots but supplies no P4 symbol map"),
        ("BLOCK", "fourth-order finite-cell boundary and corner completion is open"),
        ("BLOCK", "primitive, reference, charge, and normalization are open"),
        ("BLOCK", "no explicit pullback or action reduction to p,f,h,lambda exists"),
        ("BLOCK", "no map carries either R05/R06 or Dirichlet/free-right domains"),
        ("BLOCK", "bulk derivative order does not determine the Hessian-active wall germ"),
        ("PASS_CONDITIONAL_PREMISE", "route is defined before scale selection within its added class premises"),
        ("PASS_CONDITIONAL_PREMISE", "metric-only route imports no carrier/source, but also supplies none"),
        ("BLOCK", "complete native field/domain/boundary/solution premise stack is not closed"),
    ],
    "EH_POST_SCALE": [
        ("BLOCK", "metric variation is not identified with conditional P4 fields"),
        ("BLOCK", "no selected representative or shared F01 Einstein background is constructed"),
        ("BLOCK", "unrestricted metric domain is an added premise and no P4 tangent pullback exists"),
        ("CONDITIONAL_ANALOGY_ONLY", "second-order bulk suggests a v boundary slot but supplies no P4 symbol map"),
        ("BLOCK", "GHY/corners/orientation and finite-cell admissible data are unselected"),
        ("BLOCK", "reference, generator, charge, and normalization are open"),
        ("BLOCK", "no explicit pullback or action reduction to p,f,h,lambda exists"),
        ("BLOCK", "no map carries either R05/R06 or Dirichlet/free-right domains"),
        ("BLOCK", "a second-order bulk does not determine the independent wall second germ"),
        ("BLOCK", "the required physical representative/bootstrap selection is not derived"),
        ("PASS_CONDITIONAL_PREMISE", "metric-only route imports no carrier/source, but also supplies none"),
        ("BLOCK", "post-scale selection, constants, boundary, source, and solution are open"),
    ],
    "TWO_STAGE_BRIDGE": [
        ("BLOCK", "no composed field map from conformal class through representative to P4 is registered"),
        ("BLOCK", "no dynamically matched background across stages exists"),
        ("BLOCK", "no tangent/gauge matching theorem crosses the stage boundary"),
        ("BLOCK", "no rule reconciles the fourth-order and second-order degrees of freedom"),
        ("BLOCK", "no matched boundary polarization is registered"),
        ("BLOCK", "no common differentiable boundary functional or charge is registered"),
        ("BLOCK", "no explicit composed reduction to p,f,h,lambda exists"),
        ("BLOCK", "no composed map preserves the F01 trace-domain forks"),
        ("BLOCK", "no stage owns or matches the Hessian-active second wall germ"),
        ("BLOCK", "bootstrap representative selection and stage ordering remain open"),
        ("BLOCK", "carrier/source independence across both stages is unproved"),
        ("BLOCK", "the bridge is a proposed diagram rather than a completed premise stack"),
    ],
}

ROUTE_STATUS = {
    "C2_BACH_PRE_SCALE": "INACTIVE_WITHOUT_STRONG_CSN_PREMISE__COUNTERFACTUAL_ONLY",
    "EH_POST_SCALE": "CONDITIONAL_NOT_SELECTED",
    "TWO_STAGE_BRIDGE": "OPEN_UNDERIVED",
}

MAPS = [
    ["M01", "C2_BACH_PRE_SCALE", "unrestricted metric variations modulo gauge", "conditional P4 tangent variables p,f,h,lambda/mu", "NONE_REGISTERED", "NO", "no field/background/tangent pullback; no F01 boundary image"],
    ["M02", "EH_POST_SCALE", "post-scale metric variations modulo gauge", "conditional P4 tangent variables p,f,h,lambda/mu", "NONE_REGISTERED", "NO", "representative and background absent; no field or boundary pullback"],
    ["M03", "TWO_STAGE_BRIDGE", "pre-scale conformal class", "post-scale representative then F01 P4 realization", "DIAGRAM_ONLY", "NO", "selection arrow, dynamic matching, tangent map, and boundary map all open"],
    ["M04", "P4_INTERNAL", "conditional P4 field/action posture", "F01 joint Hessian on named trace domains", "EXACT_WITHIN_CONDITIONAL_MODEL", "YES_CONDITIONAL_ONLY", "does not identify the P4 model with C2, EH, or a native bridge"],
]

OBSTRUCTIONS = [
    ["O01", "FIELD_IDENTITY", "metric/coframe variations are not mapped to p,f,h,lambda/mu", "blocks all three routes"],
    ["O02", "BACKGROUND", "no common C2/EH on-shell realization is proved for the F01 background", "blocks Hessian transfer"],
    ["O03", "VARIATION_DOMAIN", "hard, multiplier, unrestricted-then-restrict, and restrict-then-vary routes are inequivalent", "blocks tangent transfer"],
    ["O04", "BOUNDARY_COMPLETION", "C2 fourth-order and EH finite-cell boundary/corner completions remain open", "blocks differentiability and charge transfer"],
    ["O05", "TOTAL_DERIVATIVE", "equal bulk Euler equations allow distinct boundary one-forms and Hessians", "bulk route cannot own F01 second germ"],
    ["O06", "TRACE_DOMAIN", "R05/R06 and Dirichlet/free-right forks have no image under any candidate route", "blocks exact F01 preservation"],
    ["O07", "SCALE_ORDERING", "EH requires an unselected representative; the two-stage selection and dynamic match are open", "blocks post-scale and bridge routes"],
    ["O08", "P4_CONDITIONALITY", "the P4 response itself is conditional and its N4 layer is typed without an equation", "prevents reverse promotion to native action"],
]

PREMISES = [
    ["P01", "founded reciprocal phi and complete metric/coframe arena", "DERIVED_AS_TYPED_BACKGROUND", "carried; no dynamics inferred"],
    ["P02", "C2/Bach pre-scale bulk", "UNIQUE_CONDITIONAL_INACTIVE_WITHOUT_STRONG_CSN", "counterfactual compatibility audit only; not active candidate"],
    ["P03", "EH post-scale bulk", "CONDITIONAL", "tested only as registered conditional route"],
    ["P04", "two-stage bridge", "OPEN", "not assumed"],
    ["P05", "P4 response", "CONDITIONAL", "exact target; not promoted"],
    ["P06", "F01 local joint index on four domains", "DERIVED_IN_EXACT_CONDITIONAL_SCOPE", "carried"],
    ["P07", "second wall germ", "OPEN", "ownership is the tested join"],
    ["P08", "bootstrap representative selection", "WORKING_POSIT_WITHOUT_OPERATION", "not assumed"],
    ["P09", "carrier/source", "POSIT_OR_OPEN", "not used"],
    ["P10", "PONDER global-local closure interpretation", "WORKING_LEAD_ONLY", "never affirmative authority"],
    ["P11", "pre-July-1 material", "FAILURE_OR_COUNTEREXAMPLE_ONLY", "not used affirmatively"],
]


def literal_search(payloads: dict[str, bytes]) -> list[list[str]]:
    groups = {
        "ACTION_CORPUS": [p for p in payloads if p.startswith(("native_action_", "UDT_GR_TO_UDT"))],
        "P4_F01_CORPUS": [p for p in payloads if p.startswith(("udt_p4_", "udt_f01_"))],
    }
    patterns = [
        ("F01", r"\bF01\b"),
        ("R05", r"\bR05\b"),
        ("R06", r"\bR06\b"),
        ("second_wall_germ", r"second wall germ"),
        ("Bach", r"\bBach\b"),
        ("EH_or_Einstein_Hilbert", r"\bEH\b|Einstein[- ]Hilbert"),
        ("p_f_h_lambda_tuple", r"p\s*,\s*f\s*,\s*h\s*,\s*lambda"),
    ]
    rows: list[list[str]] = []
    for group, paths in groups.items():
        for label, pattern in patterns:
            regex = re.compile(pattern, re.IGNORECASE)
            hits: list[str] = []
            occurrences = 0
            for path in sorted(paths):
                text = payloads[path].decode("utf-8", errors="replace")
                count = len(regex.findall(text))
                if count:
                    occurrences += count
                    hits.append(path)
            rows.append([group, label, str(occurrences), str(len(hits)), ";".join(hits)])
    return rows


def exact_controls() -> list[list[str]]:
    x, eps, kappa = sp.symbols("x eps kappa")
    u = sp.Function("u")(x)
    v = sp.Function("v")(x)
    ue = u + eps * v
    d = lambda expr, n=1: sp.diff(expr, x, n)
    var = lambda expr: sp.diff(expr, eps).subs(eps, 0)

    l2_variation = var(sp.diff(ue, x) ** 2 / 2)
    l2_decomposition = -d(d(u)) * v + d(d(u) * v)
    l4_variation = var(sp.diff(ue, x, 2) ** 2 / 2)
    l4_decomposition = d(u, 4) * v + d(d(u, 2) * d(v) - d(u, 3) * v)
    total = d(kappa * ue**2 / 2)
    total_variation = var(total)
    total_boundary_derivative = d(kappa * u * v)
    boundary_second = sp.diff(kappa * ue**2 / 2, eps, 2).subs(eps, 0)

    controls = [
        ["C01", "second_order_boundary_type", "delta integral(1/2 u_prime^2) = integral(-u_doubleprime v) + [u_prime v]", "one boundary trace v; no F01 field map follows", "PASS" if sp.simplify(l2_variation - l2_decomposition) == 0 else "FAIL"],
        ["C02", "fourth_order_boundary_type", "delta integral(1/2 u_doubleprime^2) = integral(u_fourth v) + [u_doubleprime v_prime-u_tripleprime v]", "two boundary traces v and v_prime; no F01 field map follows", "PASS" if sp.simplify(l4_variation - l4_decomposition) == 0 else "FAIL"],
        ["C03", "total_derivative_counterfamily", "L_tilde=L+d(kappa u^2/2)/dx", "same bulk Euler equation; boundary one-form shifts by kappa u v", "PASS" if sp.simplify(total_variation - total_boundary_derivative) == 0 else "FAIL"],
        ["C04", "boundary_hessian_nonuniqueness", "second variation of [kappa u^2/2] along v is [kappa v^2]", "bulk identity leaves an arbitrary boundary Hessian coefficient", "PASS" if sp.simplify(boundary_second - kappa * v**2) == 0 else "FAIL"],
        ["C05", "map_type_separation", "bulk equation equality != action reduction != boundary one-form pullback != boundary Hessian identity", "none of the first three may be inferred from derivative order", "PASS"],
    ]
    return controls


def main() -> None:
    sources, payloads = source_inventory()
    by_path = {str(row["path"]): row for row in sources}
    missing = [row[1] for row in AUTHORITIES if row[1] not in by_path]
    if missing:
        raise RuntimeError(f"missing authority source(s): {missing}")

    write_tsv("SOURCE_INVENTORY.tsv", ["path", "git_blob", "bytes", "sha256"], [
        [str(row["path"]), str(row["git_blob"]), str(row["bytes"]), str(row["sha256"])] for row in sources
    ])
    (OUT / "SOURCE_PATHS.txt").write_text("".join(f"{row['path']}\n" for row in sources), encoding="utf-8")
    (OUT / "SOURCE_MANIFEST.sha256").write_text("".join(f"{row['sha256']}  {row['path']}\n" for row in sources), encoding="utf-8")
    write_tsv("SOURCE_AUTHORITY_LEDGER.tsv", ["id", "path", "status", "load_bearing_statement", "git_blob", "sha256"], [
        row + [str(by_path[row[1]]["git_blob"]), str(by_path[row[1]]["sha256"])] for row in AUTHORITIES
    ])

    gate_rows: list[list[str]] = []
    for route, entries in ROUTE_GATES.items():
        if len(entries) != len(GATES):
            raise RuntimeError(f"gate census mismatch: {route}")
        for gate, (status, reason) in zip(GATES, entries):
            gate_rows.append([route, ROUTE_STATUS[route], gate, status, reason])
    write_tsv("ROUTE_GATE_MATRIX.tsv", ["route", "route_current_status", "gate", "status", "reason"], gate_rows)
    write_tsv("EXACT_MAP_LEDGER.tsv", ["id", "route", "domain", "codomain", "registered_formula", "exact_map_exists", "result"], MAPS)
    write_tsv("OBSTRUCTION_LEDGER.tsv", ["id", "obstruction", "source_fact", "effect"], OBSTRUCTIONS)
    write_tsv("PREMISE_LEDGER.tsv", ["id", "premise", "entry_status", "audit_treatment"], PREMISES)
    write_tsv("LITERAL_MAP_SEARCH.tsv", ["corpus", "token", "occurrences", "source_count", "paths"], literal_search(payloads))
    write_tsv("EXACT_CONTROL_LEDGER.tsv", ["id", "control", "construction", "result", "status"], exact_controls())

    result = {
        "audit": "stability_action_boundary_bridge",
        "date": "2026-08-01",
        "base_commit": BASE,
        "primary_outcome": OUTCOME,
        "source_count": len(sources),
        "authority_count": len(AUTHORITIES),
        "route_count": len(ROUTE_GATES),
        "gate_count_per_route": len(GATES),
        "exact_map_count_from_action_routes": 0,
        "conditional_internal_p4_map_count": 1,
        "control_count": 5,
        "second_wall_germ_owner": "OPEN",
        "c2_bach_current_applicability": "INACTIVE_WITHOUT_STRONG_CSN_PREMISE__COUNTERFACTUAL_ONLY",
        "next_scientific_gate": "derive or select a native realized variation/boundary law before another global stability-family sweep",
        "maximum_conclusion": "The registered C2/Bach, EH, and proposed two-stage routes provide derivative-order and ordering analogies but no exact field, tangent, background, trace-domain, or boundary-Hessian map into F01. The F01 second wall germ remains open; no action, carrier, source, bootstrap operation, physical boundary, or stable matter is selected.",
        "gpu_used": False,
    }
    (OUT / "RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
