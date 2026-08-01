#!/usr/bin/env python3
"""Same-verifier closure checks for the corrected A3 package."""
from __future__ import annotations

import ast
import csv
import hashlib
import json
import math
import os
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


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def tsv(path: Path, comments: bool = False) -> list[dict[str, str]]:
    with path.open(newline="") as fh:
        lines = [line for line in fh if line.strip() and
                 (not comments or not line.startswith("#"))]
    rows = list(csv.DictReader(lines, delimiter="\t"))
    require(f"parser_{path.name}_rectangular", bool(rows) and
            all(set(row) == set(rows[0]) and None not in row for row in rows),
            f"{len(rows)} rectangular rows")
    return rows


frozen = {
    "PREREGISTRATION.md": "fbd16a3d33ae5c2b71c9940fb3c2f07b700997a891b5dd44f861a05df97e2fa7",
    "VERIFIER_INDEPENDENT_CHECK.py": "ff151fa8750e0bd6a2e7995468e03f209c9d5581c037b50cd2b28bf5f9fb6466",
    "VERIFIER_INDEPENDENT_RESULTS.json": "3eaf1e3b59d8625dc6e209c3d4df8ca94e5289e0832af7466389da5876d6fed6",
}
require("round_one_sources_frozen", all(digest(HERE / name) == value
        for name, value in frozen.items()),
        "preregistration plus round-one independent checker/results remain byte-exact")

report_text = (HERE / "VERIFIER_REPORT.md").read_text()
closure_marker = "\n## Same-verifier closure — 2026-08-01\n"
round_one_hash = "8756e582303d79311113e110e0fd59010f8e181a94e1ab4902ee4be64a3f4980"
required_closure_tokens = (
    "**Verdict: CLOSED-PASS.**",
    "all 13 generated",
    "F-B3 closes:",
    "20 rows x 6 fields = 120/120",
    "round-one prefix remains byte-exact",
    "(**30/30 independent closure checks, zero failed**)",
)


def report_layout_ok(text: str) -> bool:
    if text.count(closure_marker) != 1:
        return False
    prefix, marker, suffix = text.partition(closure_marker)
    return (
        marker == closure_marker
        and hashlib.sha256(prefix.encode()).hexdigest() == round_one_hash
        and suffix.startswith("\n**Verdict: CLOSED-PASS.**")
        and "\n## " not in suffix
        and all(token in suffix for token in required_closure_tokens)
    )


require("report_round_one_prefix_plus_one_closure", report_layout_ok(report_text),
        "exact round-one prefix plus exactly one structured closure section")
prefix, _, suffix = report_text.partition(closure_marker)
prefix_mutant = ("X" if prefix[0] != "X" else "Y") + prefix[1:]
require("report_prefix_mutation_rejected", not report_layout_ok(
        prefix_mutant + closure_marker + suffix),
        "single-byte mutation of immutable round-one prefix fails the closure contract")

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
require("check_census_57", len(declared) == 57 and len({name for name, _, _ in declared}) == 57 and
        sum(kind == "SUBSTANTIVE" for _, kind, _ in declared) == 37 and
        sum(kind == "GUARD" for _, kind, _ in declared) == 20,
        "AST recount = 57 unique checks = 37 substantive + 20 guard")

imports: set[str] = set()
calls: set[str] = set()
float_literals = []
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
    elif isinstance(node, ast.Constant) and isinstance(node.value, float):
        float_literals.append(node.value)
require("purity_independent", not ({"numpy", "torch", "cupy", "jax", "random"} & imports) and
        not ({"float", "evalf", "nsolve", "lambdify"} & calls) and not float_literals,
        "no float literals/evaluation, numeric solvers/backends, GPU, or randomness")

rank = {"alpha": 1, "beta": 2, "gamma": 3}
stage_results = {stage: json.loads((HERE / f"stage_{stage}_results.json").read_text())
                 for stage in rank}
expected_counts = {
    "alpha": {"total": 18, "substantive": 14, "guard": 4, "failed": 0},
    "beta": {"total": 35, "substantive": 27, "guard": 8, "failed": 0},
    "gamma": {"total": 57, "substantive": 37, "guard": 20, "failed": 0},
}
require("stage_counts_and_prefixes", all(stage_results[stage]["counts"] == expected_counts[stage]
        and stage_results[stage]["status"] == "PASS"
        and [c["name"] for c in stage_results[stage]["checks"]] ==
        [name for name, _, owner in declared if rank[owner] <= rank[stage]]
        for stage in rank), "alpha 18; beta 35; gamma 57, each an exact cumulative prefix")

header = ["stage", "cell", "spatial_reading", "lock_reading", "time_branch", "mode_layer",
          "jet_bigrade", "theta_status", "seat", "target", "condition", "verdict",
          "parameter_effect", "kill_scope_lineage", "stamps"]
ledger = tsv(HERE / "ANGULAR_A3_LEDGER.tsv")
require("ledger_header_and_census", list(ledger[0]) == header and len(ledger) == 126 and
        {stage: sum(row["stage"] == stage for row in ledger) for stage in rank} ==
        {"alpha": 84, "beta": 28, "gamma": 14},
        "15 fields; 126 rows = alpha 84 + beta 28 + gamma 14")

layer = {
    "alpha": ("T2_ALL_INTEGER_MODES;MODE_DECOMPOSITION_NOT_TARGET",
              "TRIGRADED_JETS:i<=2,j<=2,k+l<=2;HIGHER_ANGULAR_TYPED_TO_GAMMA"),
    "beta": ("FULL_S3_ALL_SMOOTH_MODES_ON_BANKED_TWO_CAP_CLASS;T2_CONTROL_ELSEWHERE",
             "TRIGRADED_JETS:i<=2,j<=2,k+l<=2;FULL_S3_TRANSITION_AND_CAP_LAYER"),
    "gamma": ("ALL_SMOOTH_ANGULAR_MODES;NO_MODE_CUTOFF",
              "ALL_FINITE_ANGULAR_JET_ORDERS;TIME_X_BANKED_LAYER;SINGULAR_DISTRIBUTIONAL_OPEN"),
}
lineage = {
    "native_real_fields": "A1:A2a_periodic_domain;A3:A02/A03;PERIOD_GATE:real_target;DOORWAY:C2_toric_kill",
    "T2_character_modes": "A1:A3a/A3c/A3e;A2:P2j_mode_uniform;A3:A01/A03",
    "large_zeta_chart_shear": "A1:A1s/A1s4_zeta_slack;A3:A05/A06;B07_two_cap_kill",
    "fiber_U1_connection_holonomy": "A1:O05/A1s_connection_moment;DOORWAY:C1_owned_fiber_U1;A3:A11-A13",
    "angular_mirror_characters": "A1:A1e2/A1f/A3e;A2:P1i_granted_only_mirror_layer",
    "stratum_m_involution": "A1:A1i2;A2:P2d/P2e/P3g;A2_CORRECTION:A-1/A-2",
    "h_reparam_orientation_degree": "A1:A1p/A1p2;A1:J07_chain_rule_overlap;A3:A16",
    "native_opened_metric_fields": "A1:ten_covariant_components;A3:B00/B09;SMOOTH_TARGET_CONTRACTION",
    "registered_Hopf_bundle": "DOORWAY:C1_owned_transition;A3:B02-B05a/B11/B12",
    "full_S3_extension_applicability": "ANGULAR_COMPLETION:banked_two_cap_S3_only;A3:B06/B13a",
    "registered_Hopf_bundle_applicability": "DOORWAY:C1;ANGULAR_COMPLETION:completion_join_required",
    "massive_carrier_integer_test": "MASS_BANKS:two_certified_carriers;PERIOD_GATE:G08;A3:B12/B13/B14",
    "all_smooth_modes_and_jets": "A1/A2:smooth_mode_uniform;A3:G01-G04/G09/G10",
    "singular_or_distributional_angular_fields": "A3_FROZEN_CONTRACT:regular_scope_residual",
    "completion_topology": "A3_FROZEN_CONTRACT:exotic_non_Hopf_completion_residual",
}
common_ok = all(all(row[field] for field in header) and
    row["lock_reading"] == "BOTH_LOCK_READINGS:COORDINATE_LOCK|PROJECTED_LOCK;UNSELECTED" and
    row["time_branch"] == "LINEAR_TIME_R;NO_TIME_CYCLE" and
    (row["mode_layer"], row["jet_bigrade"]) == layer[row["stage"]] and
    row["theta_status"] == "THETA_ABSENT_NATIVE" and
    row["seat"] in lineage and row["kill_scope_lineage"] == lineage[row["seat"]]
    for row in ledger)
require("F_B3_all_rows_exact", common_ok, "all 126 emissions match the full frozen stack and lineage")

cells = {"RING_CYCLIC", "MIXED_CREASE_GLUE_CHAIN", "OPEN_CHAIN", "QUOTIENT_MIRRORED",
         "MIRRORED_DOUBLE_CREASE", "TORIC_TWO_CAP_INTERIOR"}
readings = {"COORDINATE_SPATIAL", "PROJECTED_SPATIAL"}
alpha_seats = {"native_real_fields", "T2_character_modes", "large_zeta_chart_shear",
               "fiber_U1_connection_holonomy", "angular_mirror_characters",
               "stratum_m_involution", "h_reparam_orientation_degree"}
require("alpha_cross_exact", all({row["seat"] for row in ledger if row["stage"] == "alpha"
        and row["cell"] == cell and row["spatial_reading"] == reading} == alpha_seats
        for cell in cells for reading in readings), "6 cells x 2 readings x all 7 seats")

checks = {item["name"]: item for item in stage_results["gamma"]["checks"]}
require("exit_wired_catch_checks", all(checks[name]["passed"] for name in
        ("F_B3_full_stamp_coverage", "F_B3a_stamp_and_lineage_mutations_rejected",
         "F_B7a_C1_field_mutation_rejected", "F_B2a_forced_trivial_holonomy_rejected")),
        "all four landed catch-proof guards execute and pass")

period = tsv(ROOT / "udt_p4_period_gate_2026-07-30/PERIOD_LEDGER.tsv")
recovery = tsv(HERE / "C1_MODE_ZERO_PERIOD_RECOVERY.tsv")
period_fields = ("cycle", "family", "posture", "condition", "verdict", "stamps")
expected_recovery = {(str(index), field): hashlib.sha256(row[field].encode()).hexdigest()
                     for index, row in enumerate(period, 1) for field in period_fields}
actual_recovery = {(row["row_index"], row["field"]): row for row in recovery}
require("C1_120_emitted_comparisons", len(period) == 20 and len(recovery) == 120 and
        set(actual_recovery) == set(expected_recovery) and all(
            actual_recovery[key]["expected_sha256"] == expected and
            actual_recovery[key]["recovered_sha256"] == expected and
            actual_recovery[key]["match"] == "PASS"
            for key, expected in expected_recovery.items()),
        "own source parser reproduces every emitted digest: 20 rows x 6 fields = 120/120")

mirror_rows = [row for row in ledger if row["seat"] == "angular_mirror_characters"]
m_rows = [row for row in ledger if row["seat"] == "stratum_m_involution"]
h_rows = [row for row in ledger if row["seat"] == "h_reparam_orientation_degree"]
require("discrete_seats_emitted", len(mirror_rows) == len(m_rows) == len(h_rows) == 12 and
        all("CONDITIONAL" in row["target"] or "conditional" in row["target"]
            for row in mirror_rows + m_rows) and
        all("PRESENTATION" in row["verdict"] for row in mirror_rows + h_rows) and
        all(("STRATUM-CONDITIONAL" in row["verdict"]) ==
            (row["spatial_reading"] == "COORDINATE_SPATIAL") for row in m_rows),
        "12 mirror + 12 m-involution + 12 h-degree rows, with branch-correct classifications")

My, Mz = sp.diag(-1, 1), sp.diag(1, -1)
my, mz, gyy, gyz = sp.symbols("my mz gyy gyz", real=True, nonzero=True)
my1, mz1 = -my, mz - 2*gyz*my/gyy
my2, mz2 = -my1, sp.simplify(mz1 - 2*gyz*my1/gyy)
require("discrete_algebra_independent", My**2 == Mz**2 == sp.eye(2) and My*Mz == Mz*My and
        my2 == my and mz2 == mz, "mirror Z2xZ2 and general flip-and-shear m involution exact")

f0, Py, Pz, n, z = sp.symbols("f0 Py Pz n z", real=True, positive=True)
n = sp.symbols("n", integer=True)
hol = sp.exp(2*sp.pi*sp.I*f0*Py/Pz)
fz = f0 + sp.symbols("fc", real=True)*sp.cos(2*sp.pi*z/Pz)
angle = 2*sp.pi*Py*fz/Pz
require("holonomy_math_independent", sp.simplify(
        hol.subs(f0, f0+n*Pz/Py)/hol) == 1 and hol.subs(f0, 0) == 1 and
        sp.simplify(hol.subs(f0, Pz/(4*Py))-sp.I) == 0 and
        sp.simplify(hol.subs(f0, Pz/(2*Py))+1) == 0 and
        sp.simplify((angle.subs(z, z+Pz)-angle)/(2*sp.pi)) == 0,
        "U1 seat is shear-invariant, nontrivial continuous, and global real lift has winding zero")
hol_rows = [row for row in ledger if row["seat"] == "fiber_U1_connection_holonomy"]
require("holonomy_emitted_all_alpha_cells", len(hol_rows) == 12 and
        all("CONTINUOUS U1 HOLONOMY" in row["verdict"] and
            "H_y not forced to 1" in row["parameter_effect"] and
            "transition monodromy" in row["stamps"] for row in hol_rows),
        "holonomy condition/classification emitted in all 12 alpha cell-reading rows")

cap_rows = tsv(ROOT / "udt_higher_isometry_plane_ownership_audit_2026-07-28/TORIC_CAP_ENUMERATION.tsv")
cap_data = []
for row in cap_rows:
    vm = tuple(map(int, row["v_minus"].split(",")))
    vp = tuple(map(int, row["v_plus"].split(",")))
    determinant = vm[0]*vp[1] - vm[1]*vp[0]
    cap_data.append((vm, vp, determinant, int(row["cap_determinant"])))
require("caps_recomputed_104", len(cap_data) == 104 and all(
        math.gcd(*map(abs, vm)) == math.gcd(*map(abs, vp)) == 1 and
        abs(det) == 1 and det == bank for vm, vp, det, bank in cap_data),
        "104/104 primitive, recorded determinant reproduced, |det|=1")

th, ph, ps = sp.symbols("theta phi psi", real=True)
curvature = -sp.sin(th)
chern = sp.integrate(curvature, (th, 0, sp.pi), (ph, 0, 2*sp.pi))/(4*sp.pi)
hopf = sp.integrate(curvature, (ps, 0, 4*sp.pi), (th, 0, sp.pi),
                    (ph, 0, 2*sp.pi))/(16*sp.pi**2)
euler = sp.integrate(sp.sin(th), (th, 0, sp.pi), (ph, 0, 2*sp.pi))/(2*sp.pi)
require("S3_characteristics_independent", chern == hopf == -1 and euler == 2,
        "Chern=-1, canonical Hopf=-1, Euler(S2)=2")

completion_text = (ROOT / "udt_p4_angular_completion_2026-07-30/EXACT_DERIVATION.md").read_text()
require("completion_boundary_rechecked", "two-cap c=1 class is the BANKED complete class" in completion_text
        and "PACKAGE-INTRODUCED, UNREGISTERED" in completion_text
        and "OUTSIDE the registered R_t×S³ arena" in completion_text,
        "banked two-cap S3 only; same-closer/crease class remains outside and unregistered")

mass_rows = [row for row in ledger if row["seat"] == "massive_carrier_integer_test"]
require("massive_carrier_boundary_emitted", len(mass_rows) == 4 and
        all("two-cap-S3 join unproved" in row["target"] and
            row["parameter_effect"] == "E0/ell/k_mod/k10/C uncut" and
            "coexistence unproved" in row["stamps"] for row in mass_rows),
        "two carriers x two readings; no S3 join, parameter cut, or on-shell coexistence smuggled")

final = json.loads((HERE / "angular_A3_results.json").read_text())
require("final_machine_summary", final["counts"] == expected_counts["gamma"] and
        final["ledger_rows"] == 126 and final["C1"]["field_comparisons_exact"] == 120 and
        final["outcome_class"] == "OB3-3_MIXED_BY_KIND" and
        set(final["TB3_1_kills"]) >= {"fiber_U1_connection_holonomy",
            "angular_mirror_Z2xZ2", "stratum_m_involution_Z2", "h_reparam_degree"},
        "57/57, 126 rows, C1 120/120, and all corrected seats in final JSON")

manifest_rows = []
for line in (HERE / "DERIVATION_MANIFEST.sha256").read_text().splitlines():
    if line.strip() and not line.startswith("#"):
        expected, name = line.split(maxsplit=1)
        manifest_rows.append((expected, name))
require("manifest_all_entries_current", len(manifest_rows) == 18 and
        all(digest(HERE / name) == expected for expected, name in manifest_rows),
        "all 18 derivation-manifest entries match actual files")

# Two external source mutations prove actual exit wiring, not merely predicate prose.
mut_dir = HERE / ".closure_mutation_tmp"
require("mutation_workspace_absent", not mut_dir.exists(), "throwaway closure path starts absent")
mut_dir.mkdir()
mutant = mut_dir / "derive_mutant.py"
mut_base = source.replace("ROOT = HERE.parent", "ROOT = HERE.parent.parent", 1)
needle = 'check("F_B3_full_stamp_coverage", "GUARD",'
require("F_B3_mutation_target_unique", mut_base.count(needle) == 1, "F-B3 insertion point unique")
mutant.write_text(mut_base.replace(needle,
    'ledger[0][5] = "MUTATED_MODE_LAYER"\n' + needle, 1))
env = dict(os.environ, OMP_NUM_THREADS="1", OPENBLAS_NUM_THREADS="1", MKL_NUM_THREADS="1",
           NUMEXPR_NUM_THREADS="1")
probe_stamp = subprocess.run([sys.executable, str(mutant), "--stage", "gamma"], cwd=mut_dir,
                             env=env, capture_output=True, text=True, timeout=30, check=False)
stamp_ok = probe_stamp.returncode != 0 and "F_B3_full_stamp_coverage: FAIL" in probe_stamp.stdout
for path in mut_dir.iterdir():
    path.unlink()
mut_dir.rmdir()
require("F_B3_external_mutation_exit", stamp_ok,
        f"mutated emitted mode layer caused named FAIL and exit {probe_stamp.returncode}")

mut_dir.mkdir()
mutant = mut_dir / "derive_mutant.py"
c1_needle = '"C1d typing"'
require("C1_mutation_target_unique", mut_base.count(c1_needle) == 1, "independent C1 field unique")
mutant.write_text(mut_base.replace(c1_needle, '"C1d typing MUTATED"', 1))
probe_c1 = subprocess.run([sys.executable, str(mutant), "--stage", "alpha"], cwd=mut_dir,
                          env=env, capture_output=True, text=True, timeout=30, check=False)
c1_ok = probe_c1.returncode != 0 and "C1a_period_gate_20_rows_exact: FAIL" in probe_c1.stdout
for path in mut_dir.iterdir():
    path.unlink()
mut_dir.rmdir()
require("C1_external_field_mutation_exit", c1_ok,
        f"mutated independently coded C1 field caused named FAIL and exit {probe_c1.returncode}")

failed = [item["name"] for item in findings if not item["passed"]]
verdict = "CLOSED-PASS" if not failed else "FURTHER-AMENDMENTS-REQUIRED"
output = {
    "verdict": verdict,
    "checks": findings,
    "failed": failed,
    "counts": {"total": len(findings), "passed": len(findings)-len(failed), "failed": len(failed)},
    "derivation_artifact_sha256": {
        name: digest(HERE / name) for name in (
            "DERIVATION_STDOUT.txt", "angular_A3_results.json", "ANGULAR_A3_LEDGER.tsv",
            "C1_MODE_ZERO_PERIOD_RECOVERY.tsv", "stage_alpha_results.json",
            "stage_beta_results.json", "stage_gamma_results.json")
    },
}
(HERE / "VERIFIER_CLOSURE_RESULTS.json").write_text(
    json.dumps(output, indent=2, sort_keys=True) + "\n")
print(f"VERDICT {verdict}; checks={len(findings)}; failed={len(failed)}")
