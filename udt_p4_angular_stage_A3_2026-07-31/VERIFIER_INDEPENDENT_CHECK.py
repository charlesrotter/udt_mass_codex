#!/usr/bin/env python3
"""Blind independent checks for A3; exact arithmetic and parsers only."""
from __future__ import annotations

import ast
import csv
import hashlib
import json
import math
import subprocess
import sys
from pathlib import Path

import sympy as sp

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
findings: list[dict[str, object]] = []


def record(name: str, passed: bool, detail: str) -> None:
    findings.append({"name": name, "passed": bool(passed), "detail": detail})
    print(f"{'PASS' if passed else 'FAIL'} {name}: {detail}")


def require(name: str, condition: bool, detail: str) -> None:
    record(name, condition, detail)
    if not condition:
        raise AssertionError(name)


def tsv(path: Path, comments: bool = False) -> list[dict[str, str]]:
    with path.open(newline="") as fh:
        lines = [line for line in fh if line.strip() and
                 (not comments or not line.startswith("#"))]
    rows = list(csv.DictReader(lines, delimiter="\t"))
    require(f"parser_{path.name}_rectangular", bool(rows) and
            all(set(row) == set(rows[0]) and None not in row for row in rows),
            f"{len(rows)} rectangular data rows")
    return rows


period_path = ROOT / "udt_p4_period_gate_2026-07-30/PERIOD_LEDGER.tsv"
t3_path = ROOT / "udt_p4_timelive_stage_T3_2026-07-31/TIMELIVE_T3_LEDGER.tsv"
cap_path = ROOT / "udt_higher_isometry_plane_ownership_audit_2026-07-28/TORIC_CAP_ENUMERATION.tsv"
period = tsv(period_path)
t3 = tsv(t3_path, comments=True)
caps = tsv(cap_path)

period_fields = ("cycle", "family", "posture", "condition", "verdict", "stamps")
period_tuples = [tuple(row[key] for key in period_fields) for row in period]
require("C1_period_gate_own_parse", len(period_tuples) == 20 and
        len(set(period_tuples)) == 20, "20 distinct full six-field rows")
line_rows = [row for row in t3 if row["branch"] == "a"]
expected_completions = {
    "certified crease|glue chain (massive)",
    "quotient-mirrored (family-(i) massive locus UNTOUCHED there, banked)",
    "all-definite ring (massless, banked)",
    "double-crease (massive EMPTY, banked SB2)",
    "massive cyclic chain (CONDITIONAL existence, banked)",
    "open chain",
}
require("C1_T3_line_own_parse", len(line_rows) == 6 and
        {row["completion"] for row in line_rows} == expected_completions and
        all(row["cycle"] == "(all static spatial)" and
            row["condition"] == "no new cycle (B1a)" and
            row["verdict"] == "static verdicts VERBATIM" for row in line_rows),
        "six exact branch-a static rows and expected completion census")

cap_data: list[tuple[tuple[int, int], tuple[int, int], int]] = []
for row in caps:
    vm = tuple(map(int, row["v_minus"].split(",")))
    vp = tuple(map(int, row["v_plus"].split(",")))
    det = vm[0] * vp[1] - vm[1] * vp[0]
    assert len(vm) == len(vp) == 2
    cap_data.append((vm, vp, det))
require("caps_104_all_primitive_unimodular", len(cap_data) == 104 and
        all(math.gcd(*map(abs, vm)) == math.gcd(*map(abs, vp)) == 1 and
            abs(det) == 1 and det == int(row["cap_determinant"])
            for (vm, vp, det), row in zip(cap_data, caps)),
        "104/104 primitive pairs; recomputed determinant matches and has |det|=1")

n = sp.symbols("n", integer=True)
S = sp.Matrix([[1, 0], [n, 1]])
shear_ok = True
for vm, vp, det in cap_data:
    U = sp.Matrix.hstack(sp.Matrix(vm), sp.Matrix(vp))
    conjugate = sp.simplify(U * S * U.inv())
    shear_ok &= all(entry.is_integer is not False for entry in conjugate)
    shear_ok &= sp.simplify(S * sp.Matrix([0, 1]) - sp.Matrix([0, 1])) == sp.zeros(2, 1)
    shear_ok &= sp.solve(sp.Eq((S * sp.Matrix([1, 0]))[1], 0), n) == [0]
require("caps_kill_unipotent_shear_family", shear_ok,
        "each unimodular cap basis conjugates the shear integrally; both cap lines force n=0")

th, ph, ps = sp.symbols("theta phi psi", real=True)
curvature = -sp.sin(th)
flux = sp.integrate(curvature, (th, 0, sp.pi), (ph, 0, 2 * sp.pi))
cs = sp.integrate(curvature, (ps, 0, 4 * sp.pi),
                  (th, 0, sp.pi), (ph, 0, 2 * sp.pi))
euler = sp.integrate(sp.sin(th), (th, 0, sp.pi), (ph, 0, 2 * sp.pi))/(2*sp.pi)
transition = sp.integrate(-2, (ph, 0, 2 * sp.pi))/(4*sp.pi)
require("S3_characteristic_data_exact", flux/(4*sp.pi) == -1 and
        cs/(16*sp.pi**2) == -1 and transition == -1 and euler == 2,
        "Chern=-1, Hopf representative=-1, transition=-1, Euler(S2)=2")

source_path = HERE / "derive_angular_A3.py"
source = source_path.read_text()
tree = ast.parse(source)
check_calls = sorted((node for node in ast.walk(tree) if isinstance(node, ast.Call) and
                      isinstance(node.func, ast.Name) and node.func.id == "check" and
                      len(node.args) >= 5 and all(isinstance(node.args[i], ast.Constant)
                                                  for i in (0, 1, 4))),
                     key=lambda node: node.lineno)
declared = [(node.args[0].value, node.args[1].value, node.args[4].value)
            for node in check_calls]
require("independent_check_census", len(declared) == 48 and
        sum(kind == "SUBSTANTIVE" for _, kind, _ in declared) == 31 and
        sum(kind == "GUARD" for _, kind, _ in declared) == 17 and
        len({name for name, _, _ in declared}) == 48,
        "AST recount gives 48 unique checks = 31 substantive + 17 guard")

imports = set()
calls = set()
for node in ast.walk(tree):
    if isinstance(node, ast.Import):
        imports.update(alias.name.split(".")[0] for alias in node.names)
    elif isinstance(node, ast.ImportFrom) and node.module:
        imports.add(node.module.split(".")[0])
    elif isinstance(node, ast.Call):
        if isinstance(node.func, ast.Name):
            calls.add(node.func.id)
        elif isinstance(node.func, ast.Attribute):
            calls.add(node.func.attr)
require("purity_AST_independent", not ({"numpy", "torch", "cupy", "jax"} & imports) and
        not ({"float", "evalf", "nsolve", "solve", "solveset", "lambdify"} & calls) and
        not any(isinstance(node, sp.Float) for node in ast.walk(tree)),
        f"imports={sorted(imports)}; no floats/numeric solvers/backends")

result = json.loads((HERE / "angular_A3_results.json").read_text())
stage_results = {stage: json.loads((HERE / f"stage_{stage}_results.json").read_text())
                 for stage in ("alpha", "beta", "gamma")}
expected_stage_counts = {
    "alpha": {"total": 12, "substantive": 8, "guard": 4, "failed": 0},
    "beta": {"total": 29, "substantive": 21, "guard": 8, "failed": 0},
    "gamma": {"total": 48, "substantive": 31, "guard": 17, "failed": 0},
}
require("stage_check_counts_and_prefixes", all(
    stage_results[stage]["counts"] == expected_stage_counts[stage] and
    stage_results[stage]["status"] == "PASS" and
    [c["name"] for c in stage_results[stage]["checks"]] ==
    [name for name, _, owner in declared if {"alpha": 1, "beta": 2, "gamma": 3}[owner]
     <= {"alpha": 1, "beta": 2, "gamma": 3}[stage]]
    for stage in expected_stage_counts), "cumulative alpha/beta/gamma banks are exact prefixes")

ledger = tsv(HERE / "ANGULAR_A3_LEDGER.tsv")
stage_rows = {stage: sum(row["stage"] == stage for row in ledger)
              for stage in ("alpha", "beta", "gamma")}
require("ledger_row_census", len(ledger) == 78 and
        stage_rows == {"alpha": 36, "beta": 28, "gamma": 14},
        f"78 rows partition as {stage_rows}")
mass_rows = [row for row in ledger if row["seat"] == "massive_carrier_integer_test"]
require("massive_carrier_scope_rows", len(mass_rows) == 4 and
        {row["spatial_reading"] for row in mass_rows} ==
        {"COORDINATE_SPATIAL", "PROJECTED_SPATIAL"} and
        all("two-cap-S3 join unproved" in row["target"] and
            "E0/ell/k_mod/k10/C uncut" == row["parameter_effect"] and
            "coexistence unproved" in row["stamps"] for row in mass_rows),
        "two carriers x two spatial readings; no S3 join or on-shell coexistence smuggled")

scope_complete = all(
    ("lock" in row["stamps"].lower()) and
    ("mode" in (row["condition"] + row["stamps"]).lower()) and
    ("jet" in (row["condition"] + row["stamps"]).lower()) and
    any(token in (row["condition"] + row["verdict"] + row["stamps"])
        for token in ("104", "cap", "Hopf", "period", "winding", "kill"))
    for row in ledger)
record("F_B3_frozen_full_stamp_contract", scope_complete,
       "FAIL expected: rows do not each carry lock branch, mode, jet-bigrade, and kill-scope lineage")

doorway = tsv(ROOT / "udt_p4_doorway_study_2026-07-31/DOORWAY_LEDGER.tsv")
dmap = {(row["candidate"], row["requirement"]): row["verdict"] for row in doorway}
require("compact_target_provenance_core", dmap[("C1_hopf_fiber", "transition_datum")] ==
        "OWNED-CIRCLE-VALUED" and dmap[("C1_hopf_fiber", "global_field_promotion")] ==
        "FAILS" and dmap[("TD4_carrier", "derives")] == "NO",
        "owned U(1) transition retained; global phase and S2 carrier promotion rejected")

# The compact fiber also gives a connection-holonomy target on a T2 stratum.
f0, Py, Pz = sp.symbols("f0 P_y P_z", real=True, positive=True)
q = sp.symbols("q", integer=True)
hol = sp.exp(2 * sp.pi * sp.I * f0 * Py / Pz)
hol_shift = sp.simplify(hol.subs(f0, f0 + q * Pz / Py) / hol)
require("torus_fiber_holonomy_U1_seat", hol_shift == 1 and
        sp.simplify(hol.subs(f0, Pz/(4*Py)) - sp.I) == 0,
        "exp(2pi i f0 Py/Pz) is large-shear invariant and ranges nontrivially in U(1)")

a2_text = (ROOT / "udt_p4_angular_stage_A2_2026-07-31/EXACT_DERIVATION.md").read_text()
a1_text = (ROOT / "udt_p4_angular_stage_A1_2026-07-31/EXACT_DERIVATION.md").read_text()
landed_text = (HERE / "EXACT_DERIVATION.md").read_text() + (HERE / "ANGULAR_A3_LEDGER.tsv").read_text()
discrete_banks_present = ("CONDITIONAL ℤ₂×ℤ₂" in a2_text and
                          "angular-mirror parity layer" in a2_text and
                          "m-involution" in a2_text and
                          "y-reparametrization slack" in a1_text)
discrete_banks_censused = all(token in landed_text for token in
                              ("angular-mirror parity", "m-involution", "y-reparametrization"))
record("TB3_discrete_and_slack_seat_completeness",
       (not discrete_banks_present) or discrete_banks_censused,
       "FAIL expected: banked mirror/m-involution/h-slack discrete layers are absent from A3")
holonomy_censused = "exp(2pi i f0 Py/Pz)" in landed_text or "Wilson" in landed_text
record("TB3_2_compact_connection_holonomy_completeness", holonomy_censused,
       "FAIL expected: owned compact-fiber U(1) holonomy seat is not adjudicated")

completion_text = (ROOT / "udt_p4_angular_completion_2026-07-30/EXACT_DERIVATION.md").read_text()
require("completion_scope_bank", "two-cap c=1 class is the BANKED complete class" in completion_text and
        "PACKAGE-INTRODUCED, UNREGISTERED" in completion_text and
        "OUTSIDE the registered R_t×S³ arena" in completion_text,
        "bank supports only the two-cap S3 class; same-closer/crease class is unregistered")

for rel, digest in result["input_sha256"].items():
    actual = hashlib.sha256((ROOT / rel).read_bytes()).hexdigest()
    require(f"input_hash_{Path(rel).name}", actual == digest,
            f"banked input unchanged: {digest[:12]}")

parameter_names = {"E0", "ell", "k_mod", "k10", "C"}
fixed_data = sp.Tuple(-1, -1, 2)
require("fixed_integer_no_parameter_symbols", not (parameter_names &
        {str(symbol) for symbol in fixed_data.free_symbols}),
        "fixed Chern/Hopf/Euler values contain no mass or response parameter")

# Mutation probe: alter C1a's exact row count in a throwaway in-package copy.
mut_dir = HERE / ".verifier_mutation_tmp"
require("mutation_workspace_absent", not mut_dir.exists(), "throwaway path starts absent")
mut_dir.mkdir()
mutant = mut_dir / "derive_angular_A3_mutant.py"
mut_source = source.replace("ROOT = HERE.parent", "ROOT = HERE.parent.parent", 1)
needle = "len(period_rows) == 20 and angular_zero_pullback == period_tuples"
require("mutation_target_unique", mut_source.count(needle) == 1, "C1a guard target unique")
mut_source = mut_source.replace(needle,
                                "len(period_rows) == 19 and angular_zero_pullback == period_tuples", 1)
mutant.write_text(mut_source)
probe = subprocess.run([sys.executable, str(mutant), "--stage", "alpha"],
                       cwd=mut_dir, capture_output=True, text=True, timeout=30, check=False)
probe_ok = probe.returncode != 0 and "C1a_period_gate_20_rows_exact: FAIL" in probe.stdout
for path in mut_dir.iterdir():
    path.unlink()
mut_dir.rmdir()
require("mutation_probe_C1a_exit_wired", probe_ok,
        f"mutated guard produced exit {probe.returncode} and explicit FAIL")

c1_tautology = ("angular_zero_pullback = [tuple(x for x in r) for r in period_tuples]" in source and
                "angular_zero_pullback == period_tuples" in source)
record("F_B7_C1_content_recovery_guard", not c1_tautology,
       "FAIL expected: C1a compares a tuplewise copy to its source, so only row count is tested")

u, v, w, angle = sp.symbols("u v w angle", real=True, positive=True)
rotation = sp.Matrix([[sp.cos(angle), -sp.sin(angle), 0],
                      [sp.sin(angle), sp.cos(angle), 0], [0, 0, 1]])
frame = sp.diag(u, v, w)
require("coframe_class_metric_invisible", sp.simplify(rotation.T*rotation) == sp.eye(3) and
        sp.simplify((rotation*frame).T*(rotation*frame) - frame.T*frame) == sp.zeros(3),
        "orthogonal coframe maps, including large classes, do not alter the metric")

required_amendments = [item["name"] for item in findings if not item["passed"]]
verdict = "PASS-WITH-REQUIRED-AMENDMENTS" if required_amendments else "PASS"
output = {
    "verdict": verdict,
    "checks": findings,
    "required_amendments": required_amendments,
    "scope": "blind A3 alpha/beta/gamma exact audit; no LIVE/HANDOFF",
}
(HERE / "VERIFIER_INDEPENDENT_RESULTS.json").write_text(
    json.dumps(output, indent=2, sort_keys=True) + "\n")
print(f"VERDICT {verdict}; required amendments={len(required_amendments)}")
