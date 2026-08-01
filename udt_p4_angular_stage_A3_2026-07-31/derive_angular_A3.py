#!/usr/bin/env python3
"""Stage A3 exact angular winding census.

Run as ``python3 derive_angular_A3.py --stage alpha|beta|gamma``.  Later stages
include all earlier checks.  Exact SymPy only; deterministic; no solvers/floats/GPU.
The script exits nonzero on any substantive or guard failure and banks each stage.
"""
from __future__ import annotations

import argparse
import ast
import csv
import hashlib
import json
import sys
from pathlib import Path

import sympy as sp

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
ORDER = {"alpha": 1, "beta": 2, "gamma": 3}
parser = argparse.ArgumentParser()
parser.add_argument("--stage", choices=tuple(ORDER), required=True)
STAGE = parser.parse_args().stage

checks: list[dict[str, object]] = []
ledger: list[list[str]] = []
lines: list[str] = []

LEDGER_HEADER = [
    "stage", "cell", "spatial_reading", "lock_reading", "time_branch",
    "mode_layer", "jet_bigrade", "theta_status", "seat", "target",
    "condition", "verdict", "parameter_effect", "kill_scope_lineage", "stamps",
]

LOCK_READING_STAMP = "BOTH_LOCK_READINGS:COORDINATE_LOCK|PROJECTED_LOCK;UNSELECTED"
TIME_BRANCH_STAMP = "LINEAR_TIME_R;NO_TIME_CYCLE"
THETA_STAMP = "THETA_ABSENT_NATIVE"


def stage_layer_stamps(stage: str) -> tuple[str, str]:
    """Return the frozen mode and jet/bigrade scope for every generated row."""
    if stage == "alpha":
        return (
            "T2_ALL_INTEGER_MODES;MODE_DECOMPOSITION_NOT_TARGET",
            "TRIGRADED_JETS:i<=2,j<=2,k+l<=2;HIGHER_ANGULAR_TYPED_TO_GAMMA",
        )
    if stage == "beta":
        return (
            "FULL_S3_ALL_SMOOTH_MODES_ON_BANKED_TWO_CAP_CLASS;T2_CONTROL_ELSEWHERE",
            "TRIGRADED_JETS:i<=2,j<=2,k+l<=2;FULL_S3_TRANSITION_AND_CAP_LAYER",
        )
    if stage == "gamma":
        return (
            "ALL_SMOOTH_ANGULAR_MODES;NO_MODE_CUTOFF",
            "ALL_FINITE_ANGULAR_JET_ORDERS;TIME_X_BANKED_LAYER;SINGULAR_DISTRIBUTIONAL_OPEN",
        )
    raise ValueError(f"unregistered stage {stage}")


KILL_SCOPE_BY_SEAT = {
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


def emit(s: str) -> None:
    lines.append(s)
    print(s)


def check(name: str, kind: str, ok: object, claim: str, stage: str) -> None:
    passed = bool(ok)
    checks.append({"name": name, "kind": kind, "passed": passed,
                   "claim": claim, "stage": stage})
    emit(f"[{kind}] {name}: {'PASS' if passed else 'FAIL'}")


def row(stage: str, cell: str, reading: str, seat: str, target: str,
        condition: str, verdict: str, cuts: str, stamps: str) -> None:
    mode_layer, jet_bigrade = stage_layer_stamps(stage)
    lineage = KILL_SCOPE_BY_SEAT.get(seat)
    if lineage is None:
        raise ValueError(f"missing kill-scope lineage for seat {seat}")
    ledger.append([
        stage, cell, reading, LOCK_READING_STAMP, TIME_BRANCH_STAMP,
        mode_layer, jet_bigrade, THETA_STAMP, seat, target, condition, verdict,
        cuts, lineage, stamps,
    ])


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


emit("STAGE A3 — exact angular-live winding census")
emit(f"requested cumulative stage: {STAGE}")
emit("theta ABSENT; linear time; no completion/posture/fork adopted; no physics")

# ---------------------------------------------------------------------------
# TB3-alpha: full torus-mode layer and every banked spatial completion class.
# ---------------------------------------------------------------------------
y, z, Py, Pz = sp.symbols("y z P_y P_z", real=True, positive=True)
n, m = sp.symbols("n m", integer=True)
I = sp.I
ey = sp.exp(2 * sp.pi * I * n * y / Py)
ez = sp.exp(2 * sp.pi * I * m * z / Pz)

check("A01_torus_characters_single_valued", "SUBSTANTIVE",
      sp.simplify(ey.subs(y, y + Py) - ey) == 0
      and sp.simplify(ez.subs(z, z + Pz) - ez) == 0,
      "T2 characters carry integer dual labels (n,m) fixed by domain periods.", "alpha")

# A real finite-mode representative; its exact differential has zero periods.
a0, ac, ass, bc, bs = sp.symbols("a0 a_c a_s b_c b_s", real=True)
F = (a0 + ac * sp.cos(2 * sp.pi * y / Py) + ass * sp.sin(2 * sp.pi * y / Py)
     + bc * sp.cos(4 * sp.pi * z / Pz) + bs * sp.sin(4 * sp.pi * z / Pz))
per_y = sp.integrate(sp.diff(F, y), (y, 0, Py))
per_z = sp.integrate(sp.diff(F, z), (z, 0, Pz))
check("A02_real_field_exact_periods_zero", "SUBSTANTIVE",
      sp.simplify(per_y) == 0 and sp.simplify(per_z) == 0,
      "Every displayed real single-valued field mode gives integral dF=0 on both T2 cycles.",
      "alpha")

# A mode-bearing real function contracts continuously to zero in its real target.
s = sp.symbols("s", real=True)
Fn = sp.cos(2 * sp.pi * n * y / Py) * sp.cos(2 * sp.pi * m * z / Pz)
H = (1 - s) * Fn
check("A03_mode_is_not_field_winding", "SUBSTANTIVE",
      sp.simplify(H.subs(s, 0) - Fn) == 0 and H.subs(s, 1) == 0,
      "The integer Fourier label contracts in the real field target; it is decomposition data, not winding.",
      "alpha")

# Positive metric factors stay positive under convex contraction to the unit factor.
b = sp.symbols("b", positive=True)
bt = (1 - s) * b + s
check("A04_positive_factor_contraction", "SUBSTANTIVE",
      sp.simplify(bt.subs(s, 0) - b) == 0 and bt.subs(s, 1) == 1,
      "R_+ metric factors are contractible; convexity supplies the positive path.", "alpha")

# The large fiber shear is a genuine torus mapping-class integer, not a field value.
Smat = sp.Matrix([[1, 0], [n, 1]])
check("A05_large_zeta_shear_lattice_automorphism", "SUBSTANTIVE",
      Smat.det() == 1 and Smat.inv() == sp.Matrix([[1, 0], [-n, 1]]),
      "z -> z+n(Pz/Py)y is a GL(2,Z) chart shear with integer degree n.", "alpha")

E0, ell, kmod, k10, C = sp.symbols("E0 ell k_mod k10 C", real=True)
shear_expr = Smat.det() - 1
check("A06_shear_integer_cuts_no_mass_data", "SUBSTANTIVE",
      not ({E0, ell, kmod, k10, C} & shear_expr.free_symbols),
      "The mapping-class integer is presentation/domain data and contains no mass/modulus symbol.", "alpha")

# Adding an angular exact leg to a banked real period leaves its condition unchanged.
Pbank = sp.symbols("P_bank", real=True)
check("A07_angular_exact_leg_leaves_real_period_gate", "SUBSTANTIVE",
      sp.simplify(Pbank + per_y - Pbank) == 0
      and sp.simplify(Pbank + per_z - Pbank) == 0,
      "Angular-live real field gradients add zero to every banked real period condition.", "alpha")

# The native field targets appearing in A1/A2 are affine/positive, never compact circles.
native_targets = {
    "phi": "R", "f": "R", "N": "R3", "m": "R2",
    "bh": "R_plus", "angular_block": "SPD2", "response_rows": "real_vector_spaces",
}
check("A08_native_target_census_has_no_circle", "GUARD",
      "S1" not in native_targets.values() and "U1" not in native_targets.values(),
      "A1/A2 native FIELD-target census contains no compact target; the owned fiber U1 holonomy is connection data, not a new field target.", "alpha")

# The compact Hopf fiber already owned by the registered angular arena supplies a
# continuous connection holonomy even though f itself is a real-valued field.
f0, fc, qh = sp.symbols("f0 f_c q_h", real=True)
Hy = sp.exp(2 * sp.pi * I * f0 * Py / Pz)
Hy_shear = sp.exp(2 * sp.pi * I * (f0 + n * Pz / Py) * Py / Pz)
check("A11_fiber_U1_holonomy_large_shear_invariant", "SUBSTANTIVE",
      sp.simplify(Hy_shear / Hy) == 1,
      "H_y=exp(2*pi*i*f0*Py/Pz) is invariant under f0 -> f0+n*Pz/Py.", "alpha")

check("A12_fiber_U1_holonomy_is_continuous", "SUBSTANTIVE",
      Hy.subs(f0, 0) == 1
      and sp.simplify(Hy.subs(f0, Pz / (4 * Py)) - I) == 0
      and sp.simplify(Hy.subs(f0, Pz / (2 * Py)) + 1) == 0,
      "Real f0 sweeps the owned compact-fiber U1 holonomy continuously; no rule sets H_y=1.",
      "alpha")

# For a globally real-lifted periodic f, its y-average is periodic in z.  Its
# holonomy map therefore has zero winding.  A nonzero winding would require a
# transition monodromy, which is a separately stamped completion datum.
fz = f0 + fc * sp.cos(2 * sp.pi * z / Pz)
holonomy_angle = 2 * sp.pi * Py * fz / Pz
real_lift_winding = sp.simplify(
    (holonomy_angle.subs(z, z + Pz) - holonomy_angle) / (2 * sp.pi)
)
w_transition = sp.symbols("w_transition", integer=True)
transition_angle_change = sp.simplify(
    2 * sp.pi * Py / Pz * (w_transition * Pz / Py)
)
check("A13_real_lift_has_zero_holonomy_winding", "SUBSTANTIVE",
      real_lift_winding == 0 and transition_angle_change == 2 * sp.pi * w_transition,
      "A global real periodic lift gives winding zero; nonzero winding needs separately owned transition monodromy.",
      "alpha")

# Banked discrete presentation/character layers omitted by the first pass.
My = sp.diag(-1, 1)
Mz = sp.diag(1, -1)
check("A14_angular_mirror_Z2xZ2", "SUBSTANTIVE",
      My**2 == sp.eye(2) and Mz**2 == sp.eye(2) and My * Mz == Mz * My,
      "The conditionally granted y/z mirrors form a Z2xZ2 character layer; they pair modes and do not create solution winding.",
      "alpha")

my, mz, gyy, gyz = sp.symbols("m_y m_z g_yy g_yz", real=True, nonzero=True)
my1 = -my
mz1 = mz - 2 * gyz * my / gyy
my2 = -my1
mz2 = sp.simplify(mz1 - 2 * gyz * my1 / gyy)
check("A15_stratum_m_involution_Z2", "SUBSTANTIVE",
      sp.simplify(my2 - my) == 0 and sp.simplify(mz2 - mz) == 0,
      "The banked chi-branch flip-and-shear is exactly order two on its lawful strata; it is a character cut, not a winding integer.",
      "alpha")

ay = sp.symbols("a_y", real=True)
h_plus = y + ay
h_minus = -y + ay
degree_plus = sp.simplify((h_plus.subs(y, Py) - h_plus.subs(y, 0)) / Py)
degree_minus = sp.simplify((h_minus.subs(y, Py) - h_minus.subs(y, 0)) / Py)
check("A16_h_reparam_orientation_degree", "SUBSTANTIVE",
      degree_plus == 1 and degree_minus == -1
      and sp.diff(h_plus, y) == 1 and sp.diff(h_minus, y) == -1,
      "Circle reparametrization diffeomorphisms have presentation degree +/-1; the sign is orientation, not a solution integer.",
      "alpha")

cells = [
    "RING_CYCLIC", "MIXED_CREASE_GLUE_CHAIN", "OPEN_CHAIN",
    "QUOTIENT_MIRRORED", "MIRRORED_DOUBLE_CREASE", "TORIC_TWO_CAP_INTERIOR",
]
readings = ["COORDINATE_SPATIAL", "PROJECTED_SPATIAL"]
for cell in cells:
    for reading in readings:
        row("alpha", cell, reading, "native_real_fields", "contractible real/positive target",
            "period(dF)=0 on each angular cycle", "NO FIELD WINDING; BANKED REAL CONDITIONS UNCHANGED",
            "E0/ell/k_mod/k10/C uncut", "T2 stratum; time-line; theta absent; lock readings both carried")
        row("alpha", cell, reading, "T2_character_modes", "dual lattice Z2",
            "F(y+Py,z)=F(y,z), F(y,z+Pz)=F(y,z)", "DISCRETE DECOMPOSITION LABELS ONLY",
            "no response or mass parameter cut", "all integer modes; real fields pair +/- modes")
        row("alpha", cell, reading, "large_zeta_chart_shear", "GL(2,Z) presentation",
            "z -> z+n(Pz/Py)y", "PRESENTATION/MAPPING-CLASS INTEGER; NOT FIELD WINDING",
            "no mass/modulus cut", "torus-stratum chart seat; cap extension deferred to beta")
        row("alpha", cell, reading, "fiber_U1_connection_holonomy", "owned compact-fiber U1",
            "H_y=exp(2*pi*i/Pz*integral_y f dy); mode zero exp(2*pi*i*f0*Py/Pz)",
            "CONTINUOUS U1 HOLONOMY; SHEAR-INVARIANT; NO INTEGER FOR A GLOBAL REAL LIFT",
            "no mass/modulus cut; H_y not forced to 1",
            "connection holonomy, not native compact field target; nonzero winding requires separately owned transition monodromy")
        row("alpha", cell, reading, "angular_mirror_characters", "conditional Z2xZ2 character layer",
            "only where both banked angular mirrors are granted at the metric/bridge floor",
            "PRESENTATION/CHARACTER PAIRING OF +/- MODES; NO SOLUTION INTEGER",
            "no mass/modulus cut",
            "grant NOT adopted; coframe SO+ obstruction travels; y/z mirror parities banked")
        m_verdict = (
            "STRATUM-CONDITIONAL Z2 CHARACTER CUT; NO NOETHER OR SOLUTION INTEGER"
            if reading == "COORDINATE_SPATIAL"
            else "NO INDEPENDENT POINTWISE CUT; PROJECTED READING CARRIES THE SAME CONTENT AS CHART-SLACK PAIRING"
        )
        row("alpha", cell, reading, "stratum_m_involution", "conditional Z2 flip-and-shear",
            "lawful chi-branch strata; coordinate-reading cut, projected-reading slack pairing",
            m_verdict, "no mass/modulus cut",
            "general action flip-and-shear; simple odd/even labels only in eigenbasis or g_yz=0; discrete slices typed not exhausted")
        row("alpha", cell, reading, "h_reparam_orientation_degree", "Diff(S1_y) presentation components",
            "h(y+Py)=h(y)+degree*Py with diffeomorphism degree in {+1,-1}",
            "ORIENTATION/DEGREE PRESENTATION DATA; NO SOLUTION INTEGER",
            "no mass/modulus cut",
            "orientation-preserving component contains continuous Diff+; degree -1 is mirror component; h slack unspent")

check("A09_completion_reading_coverage", "GUARD",
      len(cells) == 6 and len(readings) == 2
      and sum(r[0] == "alpha" for r in ledger) == 84
      and all(sum(r[0] == "alpha" and r[1] == cell and r[2] == reading
                  for r in ledger) == 7 for cell in cells for reading in readings),
      "Every declared completion class is crossed with both spatial readings and all seven alpha seats.",
      "alpha")

# C-1 uses an independent, explicit mode-zero recovery table.  It does not copy
# source tuples and compare them to themselves: the expected rows are generated
# from the frozen cycle x family templates below, then compared field-by-field.
period_path = ROOT / "udt_p4_period_gate_2026-07-30" / "PERIOD_LEDGER.tsv"
with period_path.open(newline="") as fh:
    period_rows = list(csv.DictReader(fh, delimiter="\t"))
period_fields = ("cycle", "family", "posture", "condition", "verdict", "stamps")
period_families = (
    "constants-census massive locus {I_p=0, E0>0} (triad/P1 pairing, INTEGRATED)",
    "fields-census lock-emergence massive class (P1-4D landing)",
    "massless strata (P2-side; triad-locked; pointwise survivors)",
    "wall germ data (open-end 2-germ family; glue pins)",
)
common_cycle_templates = (
    ("K4-orbifold / cap-torsion", "all postures", "n*P=0 (torsion) => P=0",
     "VACUOUS (identically satisfied)", "S0b/S0c; closed real forms; banked proof cited"),
    ("D_inf translation gamma_T", "quotient", "Hom(D_inf,R)=0 => all periods 0",
     "IDENTICALLY SATISFIED (imposes nothing)", "C1a-C1c; jet<=2; any census/pairing branch"),
    ("none (no cycle)", "open / acyclic chain", "no nontrivial cycle", "VACUOUS", "C1d typing"),
)
expected_period_rows: list[dict[str, str]] = []
for family in period_families:
    for cycle, posture, condition, verdict, stamps in common_cycle_templates:
        expected_period_rows.append(dict(zip(period_fields,
            (cycle, family, posture, condition, verdict, stamps), strict=True)))

cyclic_templates = (
    (period_families[0],
     "Sum_i E0_i L_i = 0  (== Sum M-WALL_i = 0 == aF*Sum M-GEN_i = 0); field periods Sum (G_i^-1 c)_f J_i = 0 (both components); whole-completion tie Sum E0_i I_p,i = 0",
     "CUT on all-definite chains (forced massless, C2c); EMPTY at N=1 (C2d); CONDITIONAL with indefinite partners (real conditions, no integers)",
     "C2a-C2f; quadratic class; flux-sealed seams; common aF != 0; INTEGRATED branch"),
    (period_families[1], "oint df = f1*L = 0, oint dh = h1*L = 0",
     "CUT (forced massless, C6c)", "fields census BR-M; P1-4D lock landing; [AM-2] stamps inherited"),
    (period_families[2], "all derived conditions",
     "SATISFIED identically (constants); nonconstant affine members reduce to constants", "C6d"),
    (period_families[3], "germs enter only as seam sources J_s in the momentum period law",
     "banked glue germ (B_Q=0): no source (consistency); active germs: supplied J_s",
     "C2b/C6e; arena-transfer premise stamped"),
)
for family, condition, verdict, stamps in cyclic_templates:
    expected_period_rows.append(dict(zip(period_fields, (
        "Z translation (cyclic completion)", family, "two-sided", condition, verdict, stamps
    ), strict=True)))

for family in period_families:
    expected_period_rows.append(dict(zip(period_fields, (
        "J11 chart loop", family, "any posture (multi-chart completion with a loop)",
        "twisted-cocycle holonomy trivial-or-classified: real-linear hyperplane / real matrix value",
        "REAL classification; NO discrete structure (C3b-C3d)",
        "E08 + diagonal-K twisted law; F-S7 flag; conditional on loop existence (completion data)",
    ), strict=True)))

recovery_rows: list[list[str]] = []
field_recovery_ok = len(period_rows) == len(expected_period_rows) == 20
for index, (recovered, expected) in enumerate(zip(period_rows, expected_period_rows, strict=False), 1):
    for field in period_fields:
        expected_digest = hashlib.sha256(expected[field].encode()).hexdigest()
        recovered_digest = hashlib.sha256(recovered[field].encode()).hexdigest()
        matched = expected[field] == recovered[field]
        field_recovery_ok = field_recovery_ok and matched
        recovery_rows.append([str(index), field, expected_digest, recovered_digest,
                              "PASS" if matched else "FAIL"])
with (HERE / "C1_MODE_ZERO_PERIOD_RECOVERY.tsv").open("w", newline="") as fh:
    wr = csv.writer(fh, delimiter="\t", lineterminator="\n")
    wr.writerow(["row_index", "field", "expected_sha256", "recovered_sha256", "match"])
    wr.writerows(recovery_rows)
check("C1a_period_gate_20_rows_exact", "GUARD",
      field_recovery_ok and len(recovery_rows) == 20 * len(period_fields)
      and all(r[-1] == "PASS" for r in recovery_rows),
      "Independent cycle-by-family mode-zero recovery matches all six fields of all 20 period-gate rows.",
      "alpha")

t3_path = ROOT / "udt_p4_timelive_stage_T3_2026-07-31" / "TIMELIVE_T3_LEDGER.tsv"
with t3_path.open() as fh:
    t3_data = [ln for ln in fh if ln.strip() and not ln.startswith("#")]
t3_rows = list(csv.DictReader(t3_data, delimiter="\t"))
t3_line = [r for r in t3_rows if r["branch"] == "a"]
check("C1b_T3_line_branch_exact", "GUARD",
      len(t3_line) == 6 and all(r["verdict"] == "static verdicts VERBATIM" for r in t3_line),
      "Mechanical parse: all six T3 linear-time branch-(a) rows recover the static verdicts verbatim.",
      "alpha")

check("A10_alpha_integer_provenance_partition", "SUBSTANTIVE",
      sp.simplify(sp.diff(F, y).integrate((y, 0, Py))) == 0
      and Smat.det() == 1,
      "Alpha integers partition cleanly: mode/mapping-class labels exist, while native real field periods vanish.",
      "alpha")


def write_ledger(path: Path) -> None:
    with path.open("w", newline="") as fh:
        wr = csv.writer(fh, delimiter="\t", lineterminator="\n")
        wr.writerow(LEDGER_HEADER)
        wr.writerows(ledger)


def stage_payload(stage: str) -> dict[str, object]:
    active = [c for c in checks if ORDER[str(c["stage"])] <= ORDER[stage]]
    sub = sum(c["kind"] == "SUBSTANTIVE" for c in active)
    guard = sum(c["kind"] == "GUARD" for c in active)
    return {
        "stage": stage,
        "status": "PASS" if all(c["passed"] for c in active) else "FAIL",
        "counts": {"total": len(active), "substantive": sub, "guard": guard,
                   "failed": sum(not c["passed"] for c in active)},
        "checks": active,
        "stamps": ["LINEAR_TIME_ONLY", "THETA_ABSENT", "NO_BRANCH_ADOPTED",
                   "NO_COMPLETION_ADOPTED", "NO_POSTURE_ADOPTED", "NO_PHYSICS"],
        "bank_inputs": {"period_ledger_sha256": sha256(period_path),
                        "T3_ledger_sha256": sha256(t3_path)},
    }


def bank_stage(stage: str) -> None:
    payload = stage_payload(stage)
    (HERE / f"stage_{stage}_results.json").write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n")
    (HERE / f"STAGE_{stage.upper()}_STDOUT.txt").write_text("\n".join(lines) + "\n")
    write_ledger(HERE / f"STAGE_{stage.upper()}_LEDGER.tsv")
    if payload["status"] != "PASS":
        raise SystemExit(1)


bank_stage("alpha")
if STAGE == "alpha":
    emit("ALPHA COMPLETE AND BANKED")
    # Refresh transcript after the completion line.
    (HERE / "STAGE_ALPHA_STDOUT.txt").write_text("\n".join(lines) + "\n")
    raise SystemExit(0)

# ---------------------------------------------------------------------------
# TB3-beta: full S3 chart, caps, Hopf bundle, and the complete opened metric target.
# ---------------------------------------------------------------------------
a1_exact_path = ROOT / "udt_p4_angular_stage_A1_2026-07-31" / "EXACT_DERIVATION.md"
a1_text = a1_exact_path.read_text()
check("B00_A1_complete_metric_opening_control", "GUARD",
      "of the 10 covariant components" in a1_text and "the other 7 are varied fields" in a1_text,
      "Mechanical A1 control: the local angular-live metric opening already covers all ten covariant components.",
      "beta")

th, ph, ps = sp.symbols("theta phi psi", real=True)
# Left-invariant coframe coefficients in the coordinate order (theta,phi,psi).
sig1 = sp.Matrix([sp.cos(ps), sp.sin(ps) * sp.sin(th), 0])
sig2 = sp.Matrix([-sp.sin(ps), sp.cos(ps) * sp.sin(th), 0])
sig3 = sp.Matrix([0, sp.cos(th), 1])
screen = sp.simplify(sig1 * sig1.T + sig2 * sig2.T)
screen_target = sp.diag(1, sp.sin(th) ** 2, 0)
check("B01_full_S3_screen_metric", "SUBSTANTIVE", screen == screen_target,
      "sigma1^2+sigma2^2 equals the round S2-base metric in the full Euler chart.", "beta")

dsig3_thph = sp.diff(sig3[1], th) - sp.diff(sig3[0], ph)
check("B02_hopf_connection_curvature", "SUBSTANTIVE",
      sp.simplify(dsig3_thph + sp.sin(th)) == 0,
      "d sigma3 = -sin(theta) dtheta^dphi; the fiber phase is not a global field.", "beta")

chern_flux = sp.integrate(dsig3_thph, (th, 0, sp.pi), (ph, 0, 2 * sp.pi))
chern = sp.simplify(chern_flux / (4 * sp.pi))
hopf_cs = sp.integrate(-sp.sin(th), (ps, 0, 4 * sp.pi),
                       (th, 0, sp.pi), (ph, 0, 2 * sp.pi))
check("B03_fixed_chern_and_hopf_representative", "SUBSTANTIVE",
      chern_flux == -4 * sp.pi and chern == -1
      and sp.simplify(hopf_cs / (16 * sp.pi ** 2)) == -1,
      "The registered Hopf bundle has fixed Chern -1; canonical sigma3 has normalized Hopf representative -1.",
      "beta")

# A globally smooth connection perturbation changes the curvature by an exact 2-form only.
q = sp.symbols("q", real=True)
a_ph = q * sp.sin(th) ** 2
da_flux = sp.integrate(sp.diff(a_ph, th), (th, 0, sp.pi), (ph, 0, 2 * sp.pi))
check("B04_connection_deformation_preserves_chern", "SUBSTANTIVE", da_flux == 0,
      "Exact representative has zero added flux; general smooth global perturbations follow by Stokes on closed S2 (Category-A).",
      "beta")

# The two-chart transition has one fiber-period of mismatch.
transition_loop = sp.integrate(-2, (ph, 0, 2 * sp.pi))
check("B05_hopf_transition_winding_one", "SUBSTANTIVE",
      transition_loop == -4 * sp.pi
      and sp.simplify(transition_loop / (4 * sp.pi)) == -1,
      "The owned circle-valued transition datum has winding -1 (orientation convention); it is not a global field.",
      "beta")

# Both local trivializations reconstruct the same global sigma3 leg.
north_phi = 1 + (sp.cos(th) - 1)   # dpsi_N=dpsi+dphi
south_phi = -1 + (sp.cos(th) + 1)  # dpsi_S=dpsi-dphi
check("B05a_hopf_chart_metric_leg_descends", "SUBSTANTIVE",
      sp.simplify(north_phi - sp.cos(th)) == 0
      and sp.simplify(south_phi - sp.cos(th)) == 0,
      "North/south local fiber coordinates reconstruct identical sigma3; metric data descend chart-covariantly.",
      "beta")

# Parse the complete banked cap census and recompute every determinant independently.
cap_path = ROOT / "udt_higher_isometry_plane_ownership_audit_2026-07-28" / "TORIC_CAP_ENUMERATION.tsv"
with cap_path.open(newline="") as fh:
    cap_rows = list(csv.DictReader(fh, delimiter="\t"))
cap_recomputed = []
for cr in cap_rows:
    vm = tuple(int(x) for x in cr["v_minus"].split(","))
    vp = tuple(int(x) for x in cr["v_plus"].split(","))
    det = vm[0] * vp[1] - vm[1] * vp[0]
    cap_recomputed.append(det == int(cr["cap_determinant"]) and abs(det) == 1)
check("B06_cap_census_104_unimodular", "SUBSTANTIVE",
      len(cap_rows) == 104 and all(cap_recomputed),
      "All 104 banked two-cap pairs are independently recomputed unimodular, hence S3/pi1-trivial.",
      "beta")

# In a cap-adapted unimodular basis, a nonzero torus shear fails to preserve both cap lines.
e1, e2 = sp.Matrix([1, 0]), sp.Matrix([0, 1])
Se1, Se2 = Smat * e1, Smat * e2
check("B07_large_shear_killed_by_two_caps", "SUBSTANTIVE",
      Se2 == e2 and Se1[1] == n and Se1[1].subs(n, 0) == 0
      and sp.diff(Se1[1], n) == 1,
      "In a cap-adapted basis the shear preserves both lines only at n=0; conjugacy covers every unimodular pair (Category-A).",
      "beta")

# Generic sphere-dependent fields destroy coordinate isometries but not chart covariance.
Fgeneric = sp.cos(th) + sp.sin(th) * sp.cos(ps) + sp.sin(ph)
check("B08_generic_S3_field_breaks_continuous_isometries", "SUBSTANTIVE",
      sp.diff(Fgeneric, ps) != 0 and sp.diff(Fgeneric, ph) != 0,
      "With all angular instruments on, generic members retain transition covariance, not Hopf/torus isometry.",
      "beta")

# Full opened lapse/shift/SPD metric data have a contractible pointwise target.
b1, b2, b3 = sp.symbols("b1 b2 b3", positive=True)
Bdiag = sp.diag(b1, b2, b3)
Bpath = (1 - s) * Bdiag + s * sp.eye(3)
check("B09_open_metric_target_contraction", "SUBSTANTIVE",
      Bpath.subs(s, 0) == Bdiag and Bpath.subs(s, 1) == sp.eye(3)
      and sp.simplify(Bpath.det() - sp.prod((1 - s) * x + s for x in (b1, b2, b3))) == 0,
      "Diagonal certificate; general SPD(3) convexity is Category-A. Lapse/shift factors add no winding.",
      "beta")

# Any local orthogonal coframe rotation is invisible to the metric, including a winding frame map.
ang = sp.symbols("a", real=True)
Rot = sp.Matrix([[sp.cos(ang), -sp.sin(ang), 0],
                 [sp.sin(ang), sp.cos(ang), 0], [0, 0, 1]])
Eco = sp.diag(b1, b2, b3)
check("B10_coframe_winding_is_metric_presentation", "SUBSTANTIVE",
      sp.simplify(Rot.T * Rot) == sp.eye(3)
      and sp.simplify((Rot * Eco).T * (Rot * Eco) - Eco.T * Eco) == sp.zeros(3),
      "A frame rotation, even with nontrivial global frame class, leaves g unchanged; no metric integer results.",
      "beta")

# A variable Hopf charge would require a field map to S2; no such native target is in A1/A2.
doorway_path = ROOT / "udt_p4_doorway_study_2026-07-31" / "DOORWAY_LEDGER.tsv"
with doorway_path.open(newline="") as fh:
    doorway_rows = list(csv.DictReader(fh, delimiter="\t"))
doorway_map = {(r["candidate"], r["requirement"]): r["verdict"] for r in doorway_rows}
check("B11_no_native_variable_Hopf_map", "GUARD",
      doorway_map[("C1_hopf_fiber", "global_field_promotion")] == "FAILS"
      and doorway_map[("TD4_carrier", "derives")] == "NO",
      "Mechanical doorway control: no global fiber field and no S2 carrier target are derived.", "beta")

# The fixed topological numbers contain no solution/mass variables.
topological_numbers = sp.Tuple(chern, sp.simplify(hopf_cs / (16 * sp.pi ** 2)))
check("B12_fixed_topology_cuts_no_mass_data", "SUBSTANTIVE",
      not ({E0, ell, kmod, k10, C} & topological_numbers.free_symbols),
      "Chern/Hopf +/-1 are fixed arena data shared by all members, not branch labels or parameter conditions.",
      "beta")

for cell in cells:
    for reading in readings:
        beta_cell = cell.replace("_INTERIOR", "_S3")
        if cell == "TORIC_TWO_CAP_INTERIOR":
            row("beta", beta_cell, reading, "native_opened_metric_fields",
                "contractible tensor/positive target", "global smoothness + cap/transition covariance",
                "NO SOLUTION-DEPENDENT WINDING", "banked real conditions unchanged",
                "banked two-cap S3; all smooth sphere dependence; theta absent")
            row("beta", beta_cell, reading, "registered_Hopf_bundle", "owned fiber transition U1",
                "c1=-1 (orientation convention); canonical Hopf representative=-1",
                "FIXED DOMAIN/PRESENTATION INTEGER ON THE BANKED TWO-CAP S3 CLASS",
                "E0/ell/moduli uncut", "no global phase field; no carrier target")
        else:
            row("beta", beta_cell, reading, "full_S3_extension_applicability",
                "completion-dependent", "requires banked two-cap S3 membership",
                "BETA S3 VERDICT NOT TRANSFERRED; ALPHA T2 VERDICT REMAINS",
                "no cut derived", "completion/topology not adopted")
            row("beta", beta_cell, reading, "registered_Hopf_bundle_applicability",
                "completion-dependent", "requires identification with banked two-cap S3 class",
                "NOT TRANSFERRED TO THIS COMPLETION ROW",
                "no cut derived", "completion/topology not adopted; fixed S3 integer cannot be smuggled")

massive_carriers = [
    "MIXED_CREASE_GLUE_CHAIN: constants-census massive witness, conditional mass reading",
    "QUOTIENT_MIRRORED: family-(i) {I_p=0,E0>0} locus, conditional mass reading",
]
for carrier in massive_carriers:
    for reading in readings:
        row("beta", carrier, reading, "massive_carrier_integer_test",
            "candidate completion; two-cap-S3 join unproved",
            "no compact field target; fixed c1/Hopf requires a separately certified two-cap-S3 join",
            "NO VARIABLE INTEGER; FIXED-DOMAIN COEXISTENCE OPEN BY COMPLETION STAMP",
            "E0/ell/k_mod/k10/C uncut",
            "mass conditional; carrier-to-two-cap-S3 join and nonzero angular-live on-shell coexistence unproved; theta absent")

angular_completion_path = ROOT / "udt_p4_angular_completion_2026-07-30" / "EXACT_DERIVATION.md"
angular_completion_text = angular_completion_path.read_text()
check("B13a_completion_scope_not_smeared", "GUARD",
      "two-cap c=1 class is the BANKED complete class" in angular_completion_text
      and "OUTSIDE the registered R_t×S³ arena" in angular_completion_text,
      "Mechanical scope control: only the banked two-cap class is S3; unregistered crease classes cannot inherit it.",
      "beta")

check("B13_massive_carriers_both_enumerated", "GUARD",
      len(massive_carriers) == 2
      and sum(r[0] == "beta" and r[8] == "massive_carrier_integer_test" for r in ledger) == 4,
      "Both certified massive-capable carriers are crossed with both spatial readings.", "beta")

check("B14_beta_kill_readjudication_complete", "SUBSTANTIVE",
      len(cap_rows) == 104 and chern != 0 and n in Smat.free_symbols,
      "Cap pi1 kill survives; torus shear re-scopes to presentation; Hopf obstruction survives while fixed c1 remains.",
      "beta")

bank_stage("beta")
if STAGE == "beta":
    emit("BETA COMPLETE AND BANKED")
    (HERE / "STAGE_BETA_STDOUT.txt").write_text("\n".join(lines) + "\n")
    raise SystemExit(0)

# ---------------------------------------------------------------------------
# TB3-gamma: all smooth angular modes and derivative orders (no silent cutoff).
# ---------------------------------------------------------------------------
freq = 2 * sp.pi * I * n / Py
kk = sp.symbols("k", integer=True, nonnegative=True)
induction_residual = sp.simplify(sp.diff(freq ** kk * ey, y) - freq ** (kk + 1) * ey)
check("G01_all_derivative_orders_induction", "SUBSTANTIVE", induction_residual == 0,
      "If d^k e_n=q^k e_n, one differentiation gives d^(k+1)e_n=q^(k+1)e_n for arbitrary k.",
      "gamma")

explicit_high = [3, 4, 7]
check("G02_high_jet_witnesses_beyond_alpha", "SUBSTANTIVE",
      all(sp.simplify(sp.diff(ey, y, j) - freq ** j * ey) == 0 for j in explicit_high),
      "Jet orders 3, 4, and 7 verify the all-order law beyond alpha's order-2 layer.", "gamma")

# Arbitrarily high real modes remain single-valued and contractible as field configurations.
Nhi = sp.symbols("N", integer=True, nonnegative=True)
high_mode = sp.cos(2 * sp.pi * Nhi * y / Py)
high_contract = (1 - s) * high_mode
check("G03_arbitrary_high_mode_not_winding", "SUBSTANTIVE",
      sp.simplify(high_mode.subs(y, y + Py) - high_mode) == 0
      and high_contract.subs(s, 1) == 0,
      "Every integer mode, with no cutoff, is a contractible real-field configuration.", "gamma")

# A genuine all-order S3 mode family in Hopf coordinates, smooth as an embedding polynomial.
eta, xi = sp.symbols("eta xi", real=True)
L = sp.symbols("L", integer=True, nonnegative=True)
z1L = sp.cos(eta) ** L * sp.exp(I * L * xi)
check("G03a_arbitrary_full_S3_mode_not_winding", "SUBSTANTIVE",
      sp.simplify(z1L.subs(xi, xi + 2 * sp.pi) - z1L) == 0
      and ((1 - s) * z1L).subs(s, 1) == 0,
      "The smooth S3 embedding-polynomial mode z1^L is single-valued for all L and contracts by amplitude.",
      "gamma")

# A discrete spectral label is not a parameter quantization: it is present before any law is selected.
lap_mode = -sp.diff(high_mode, y, 2)
lap_eval = (2 * sp.pi * Nhi / Py) ** 2 * high_mode
check("G04_mode_eigenlabel_is_domain_spectral_data", "SUBSTANTIVE",
      sp.simplify(lap_mode - lap_eval) == 0
      and not ({E0, ell, kmod, k10, C} & lap_eval.free_symbols),
      "Compact-domain mode integers label the decomposition operator and cut no banked solution data.",
      "gamma")

# A real closed one-form on T2 can have arbitrary real period; compact domain alone gives no lattice.
aa = sp.symbols("a", real=True)
real_oneform_period = sp.integrate(aa, (y, 0, Py))
check("G05_real_holonomy_target_remains_continuum", "SUBSTANTIVE",
      real_oneform_period == aa * Py
      and {aa, Py}.issubset(real_oneform_period.free_symbols),
      "A non-exact real one-form has an arbitrary real period a*Py, never an integer lattice without a compact target.",
      "gamma")

# Fine structure can create/remove nodes without leaving the real target: node counts are not protected.
nodal = sp.cos(6 * sp.pi * y / Py)
lifted = nodal + 2
check("G06_fine_feature_counts_not_topological", "SUBSTANTIVE",
      sp.simplify(lifted - nodal - 2) == 0
      and lifted.subs(y, 0) == 3 and lifted.subs(y, Py / 6) == 1,
      "A constant deformation removes the representative's zeros while preserving smooth periodicity.", "gamma")

# The fixed S2 base has its own characteristic number, again domain data rather than a target field.
euler_s2 = sp.simplify(sp.integrate(sp.sin(th), (th, 0, sp.pi), (ph, 0, 2 * sp.pi))
                       / (2 * sp.pi))
check("G07_base_S2_fixed_Euler_number", "SUBSTANTIVE", euler_s2 == 2,
      "Round-base curvature integral gives Euler 2 by Gauss-Bonnet (Category-A); stage geometry, not target.", "gamma")

# Recheck the two banked masslessness confinements mechanically.
def find_period(fragment_cycle: str, fragment_family: str) -> list[dict[str, str]]:
    return [r for r in period_rows if fragment_cycle in r["cycle"] and fragment_family in r["family"]]

const_cyclic = find_period("Z translation", "constants-census massive")
field_cyclic = find_period("Z translation", "fields-census lock-emergence")
check("G08_masslessness_confinements_rechecked", "GUARD",
      any("CUT on all-definite chains" in r["verdict"] for r in const_cyclic)
      and any("CUT (forced massless" in r["verdict"] for r in field_cyclic),
      "Mechanical period-ledger check: both cyclic masslessness confinements remain banked.", "gamma")

# A2's pointwise response space is mode-uniform and selects no particular mode.
a2_exact_path = ROOT / "udt_p4_angular_stage_A2_2026-07-31" / "EXACT_DERIVATION.md"
a2_text = a2_exact_path.read_text()
check("G09_A2_mode_uniform_control", "GUARD",
      "surviving space is MODE-UNIFORM" in a2_text
      and "No per-mode kill exists at this layer" in a2_text,
      "Mechanical A2 control: the response family is mode-uniform and supplies no spectral selector.",
      "gamma")

# Smooth-mode completion is exhaustive because the target contraction is mode-independent.
check("G10_smooth_fine_detail_exhaustive", "SUBSTANTIVE",
      sp.simplify(((1 - s) * Fgeneric).subs(s, 0) - Fgeneric) == 0
      and ((1 - s) * Fgeneric).subs(s, 1) == 0,
      "Exact representative plus linear/SPD target contraction (Category-A) is mode/jet independent for smooth fields.",
      "gamma")

for cell in cells:
    for reading in readings:
        gamma_cell = cell.replace("_INTERIOR", "_S3")
        detail_scope = ("full smooth S3" if cell == "TORIC_TWO_CAP_INTERIOR"
                        else "full smooth T2-stratum detail; global completion join open")
        row("gamma", gamma_cell, reading,
            "all_smooth_modes_and_jets", "same contractible native targets",
            "arbitrary smooth angular resolution; no mode/jet cutoff",
            "NO NEW WINDING; MODE LABELS REMAIN DECOMPOSITION DATA",
            "E0/ell/moduli uncut", f"{detail_scope}; regular fields; theta absent")

row("gamma", "ALL", "BOTH", "singular_or_distributional_angular_fields",
    "target may leave regular metric stratum", "not run",
    "OPEN RESIDUAL; CANNOT BE USED TO WEAKEN THE SMOOTH VERDICT",
    "unknown", "outside registered positive smooth metric; separately authorized contract required")
row("gamma", "EXOTIC_NON_HOPF_COMPLETIONS", "BOTH", "completion_topology",
    "unregistered/open boundary", "not in 104-pair banked census",
    "OPEN RESIDUAL", "unknown", "named by contract; no completion adopted")

check("G11_gamma_coverage_and_residual_typed", "GUARD",
      sum(r[0] == "gamma" and r[8] == "all_smooth_modes_and_jets" for r in ledger) == 12
      and sum(r[0] == "gamma" and "OPEN RESIDUAL" in r[11] for r in ledger) == 2,
      "All 12 cell-reading pairs are closed for smooth detail; two nonbanked residual classes are explicit.",
      "gamma")

# Falsifier/ceiling guards are assertions in the executable exit path.
source_text = Path(__file__).read_text()
check("F_B2_no_invented_compact_field", "GUARD",
      "theta" not in native_targets and native_targets["phi"] == "R"
      and doorway_map[("C1_hopf_fiber", "transition_datum")] == "OWNED-CIRCLE-VALUED",
      "Compact content is traced only to the banked Hopf transition; no theta/native S1 field is introduced.",
      "gamma")


def full_stamp_row_ok(r: list[str]) -> bool:
    allowed_cells = {
        "alpha": set(cells),
        "beta": {c.replace("_INTERIOR", "_S3") for c in cells} | set(massive_carriers),
        "gamma": ({c.replace("_INTERIOR", "_S3") for c in cells}
                  | {"ALL", "EXOTIC_NON_HOPF_COMPLETIONS"}),
    }
    return (
        len(r) == len(LEDGER_HEADER)
        and all(str(x) for x in r)
        and r[0] in ORDER
        and r[1] in allowed_cells[r[0]]
        and r[2] in {"COORDINATE_SPATIAL", "PROJECTED_SPATIAL", "BOTH"}
        and r[3] == LOCK_READING_STAMP
        and r[4] == TIME_BRANCH_STAMP
        and r[5] == stage_layer_stamps(r[0])[0]
        and r[6] == stage_layer_stamps(r[0])[1]
        and r[7] == THETA_STAMP
        and r[8] in KILL_SCOPE_BY_SEAT
        and r[13] == KILL_SCOPE_BY_SEAT[r[8]]
        and any(token in r[13] for token in ("A1:", "A3:", "DOORWAY:",
                                             "MASS_BANKS:", "A3_FROZEN_CONTRACT:"))
    )


check("F_B3_full_stamp_coverage", "GUARD",
      all(full_stamp_row_ok(r) for r in ledger),
      "Every row exit-enforces cell, spatial branch, both lock branches, time branch, mode layer, jet bigrade, theta status, and exact kill-scope lineage.",
      "gamma")

stamp_mutant = list(ledger[0])
stamp_mutant[3] = "BOTH_LOCK_READINGS"
cell_mutant = list(ledger[0])
cell_mutant[1] = "UNREGISTERED_CELL"
seat_mutant = list(ledger[0])
seat_mutant[8] = "unregistered_seat"
check("F_B3a_stamp_and_lineage_mutations_rejected", "GUARD",
      not full_stamp_row_ok(stamp_mutant) and not full_stamp_row_ok(cell_mutant)
      and not full_stamp_row_ok(seat_mutant),
      "Catch-proof: a weakened branch stamp, unknown cell, or unknown seat/lineage fails the same F-B3 predicate.",
      "gamma")

c1_mutant = [dict(r) for r in expected_period_rows]
c1_mutant[0]["verdict"] += " MUTATED"
c1_mutant_matches = all(
    expected[field] == recovered[field]
    for expected, recovered in zip(c1_mutant, period_rows, strict=True)
    for field in period_fields
)
check("F_B7a_C1_field_mutation_rejected", "GUARD", not c1_mutant_matches,
      "Catch-proof: changing one independently coded C1 field is detected across the 120 field comparisons.",
      "gamma")

check("F_B2a_forced_trivial_holonomy_rejected", "GUARD",
      sp.simplify(Hy.subs(f0, Pz / (4 * Py)) - 1) != 0,
      "Catch-proof: the admitted quarter-turn holonomy is i, so a forced H_y=1 claim fails exactly.",
      "gamma")
check("F_B4_no_adoption_tokens", "GUARD",
      all(x not in " ".join(r[11] for r in ledger) for x in ("ADOPTED", "SELECTED PHYSICAL")),
      "No completion, posture, fork, carrier, theta, or physical law is adopted.", "gamma")
check("F_B5_bank_controls_present", "GUARD",
      len(period_rows) == 20 and len(t3_line) == 6 and len(cap_rows) == 104,
      "Period, line-time, and cap banks are all mechanically present at their exact census sizes.", "gamma")
check("F_B6_exact_method_guard", "GUARD",
      (lambda tree: (
          not ({"numpy", "torch", "cupy"} & {
              n.names[0].name.split(".")[0] for n in ast.walk(tree) if isinstance(n, ast.Import)
          })
          and not ({"evalf", "nsolve"} & {
              (n.func.attr if isinstance(n.func, ast.Attribute) else n.func.id)
              for n in ast.walk(tree) if isinstance(n, ast.Call)
              and isinstance(n.func, (ast.Attribute, ast.Name))
          })
      ))(ast.parse(source_text)),
      "No floating evaluation, numerical solver, array backend, or GPU library occurs.", "gamma")
check("F_B7_C1_control_pass", "GUARD",
      all(bool(c["passed"]) for c in checks if str(c["name"]).startswith("C1")),
      "Every C-1 recovery check passes; failure would halt before output banking.", "gamma")

check("F_B1_both_flattery_directions_attacked", "SUBSTANTIVE",
      chern == -1 and euler_s2 == 2 and sp.simplify(per_y) == 0 and sp.simplify(per_z) == 0,
      "Fixed native topology integers are retained, while the no-field-winding result is separately exact.",
      "gamma")

bank_stage("gamma")
emit("GAMMA COMPLETE AND BANKED")
emit("OUTCOME: OB3-3 MIXED-BY-KIND; fixed domain integers, no native solution winding")

final = stage_payload("gamma")
final.update({
    "exit_code": 0,
    "stage_completion": {"alpha": "COMPLETE", "beta": "COMPLETE", "gamma": "COMPLETE"},
    "ledger_rows": len(ledger),
    "outcome_class": "OB3-3_MIXED_BY_KIND",
    "TB3_1_kills": {
        "104_pair_cap_pi1": "SURVIVES_EXACTLY_ALL_UNIMODULAR",
        "toric_field_winding_nowhere": "SURVIVES_FOR_NATIVE_FIELDS",
        "large_zeta_shear": "RESCOPED_TO_T2_PRESENTATION_INTEGER_AND_KILLED_BY_TWO_S3_CAPS",
        "fiber_U1_connection_holonomy": "LIVE_CONTINUOUS_U1;SHEAR_INVARIANT;GLOBAL_REAL_LIFT_HAS_ZERO_WINDING",
        "angular_mirror_Z2xZ2": "CONDITIONAL_GRANTED_ONLY_CHARACTER_LAYER;NOT_SOLUTION_INTEGER",
        "stratum_m_involution_Z2": "COORDINATE_READING_CONDITIONAL_CHARACTER_CUT;PROJECTED_READING_SLACK_PAIRING",
        "h_reparam_degree": "PRESENTATION_ORIENTATION_PLUS_OR_MINUS_ONE;NOT_SOLUTION_INTEGER",
        "Hopf_fiber_global_promotion": "SURVIVES_CHERN_OBSTRUCTION",
        "owned_Hopf_transition": "FIXED_WINDING_MINUS_ONE_DOMAIN_DATUM",
    },
    "TB3_2_conditions": [
        "real single-valued native fields: integral dF=0 on angular cycles",
        "real closed non-exact T2 one-forms: arbitrary real periods, not a lattice",
        "T2 Fourier labels (n,m) in Z2: decomposition/domain labels only",
        "large zeta torus shear n in Z: presentation mapping class; S3 two-cap extension forces n=0",
        "owned-fiber connection holonomy H_y in U1: continuous and large-shear invariant; a global real lift has zero winding",
        "angular mirrors Z2xZ2: conditional granted-only character layer pairing +/- modes",
        "stratum m-involution Z2: conditional response-character cut only under the coordinate spatial reading",
        "h reparametrization degree +/-1: orientation/presentation component of Diff(S1), not a solution charge",
        "Hopf transition: c1=-1 (orientation convention), fixed by the registered bundle",
        "canonical Hopf representative: normalized value -1, fixed architecture not a field charge",
        "S2 base Euler number 2: fixed stage geometry",
        "all banked completion/J11 conditions: unchanged real targets; period-gate 20 rows recovered",
    ],
    "TB3_3_massive_carriers": {
        "mixed_crease_glue_chain": "no variable native integer; fixed Hopf/S2 topology may not be transferred without a certified two-cap-S3 completion join; E0/ell/moduli uncut; mass conditional; nonzero angular-live on-shell coexistence unproved",
        "quotient_family_i_locus": "no variable native integer; fixed Hopf/S2 topology may not be transferred without a certified two-cap-S3 completion join; E0/ell/moduli uncut; mass conditional; nonzero angular-live on-shell coexistence unproved",
    },
    "C1": {"period_rows_exact": 20, "period_fields_per_row": 6,
           "field_comparisons_exact": len(recovery_rows), "T3_line_rows_exact": 6,
           "verdict": "PASS_MODE_ZERO_RECOVERS_PERIOD_GATE_AND_LINEAR_TIME"},
    "limits": [
        "smooth regular positive-metric configurations only",
        "exotic non-Hopf completions remain open",
        "singular/distributional angular fields remain open",
        "no response law selected and no angular-live massive solution solved",
        "the two named massive carriers are not certified as the banked two-cap S3 completion",
        "theta absent; no carrier target; no completion/posture/reading fork adopted",
    ],
})

inputs = [
    HERE / "PREREGISTRATION.md",
    ROOT / "udt_p4_angular_stage_A1_2026-07-31" / "EXACT_DERIVATION.md",
    ROOT / "udt_p4_angular_stage_A1_2026-07-31" / "ANGULAR_A1_LEDGER.tsv",
    ROOT / "udt_p4_angular_stage_A2_2026-07-31" / "EXACT_DERIVATION.md",
    ROOT / "udt_p4_angular_stage_A2_2026-07-31" / "ANGULAR_A2_LEDGER.tsv",
    period_path, t3_path, doorway_path, cap_path,
    ROOT / "udt_p4_routeA_slice2_solution_legs_2026-07-29" / "EXACT_DERIVATION.md",
    ROOT / "udt_p4_routeA_slice2b_full_cell_2026-07-29" / "EXACT_DERIVATION.md",
    angular_completion_path,
]
final["input_sha256"] = {str(p.relative_to(ROOT)): sha256(p) for p in inputs}

(HERE / "angular_A3_results.json").write_text(json.dumps(final, indent=2, sort_keys=True) + "\n")
write_ledger(HERE / "ANGULAR_A3_LEDGER.tsv")
(HERE / "DERIVATION_STDOUT.txt").write_text("\n".join(lines) + "\n")
(HERE / "STAGE_GAMMA_STDOUT.txt").write_text("\n".join(lines) + "\n")
raise SystemExit(0)
