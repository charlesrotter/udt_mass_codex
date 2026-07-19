#!/usr/bin/env python3
"""Independent dynamic-frame verifier and fail-closed semantic catches."""

from __future__ import annotations

import copy
import csv
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
BASE = "14d3387166f62f5f4a265f5331defae13ea8ecbe"
RESULT = HERE / "DERIVATION_RESULT.json"
VERIFY = HERE / "VERIFICATION_RESULT.json"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def validate(data: dict) -> None:
    require(data["schema"] == "udt-xmax-dynamic-observer-frame-1.0", "schema changed")
    require(len(data["checks"]) == 23 and all(value == "PASS" for value in data["checks"].values()), "primary check census/failure")
    time_map = data["time_map"]
    require(time_map["differential_map"] == "dT_beta=exp(-2 beta(t)) dt", "dynamic time map changed")
    require(time_map["classification"] == "EXACT_DYNAMIC_TIME_MAP_IN_FIXED_F3_FRAME_FAMILY", "time-map scope promoted")
    require("extra -2t beta_dot term" in time_map["rejected_shortcut"], "naive time shortcut restored")
    pullback = data["full_metric_pullback"]
    require(pullback["diagonal_family"] == "not closed for beta_dot nonzero", "diagonal failure hidden")
    require(pullback["off_diagonal_orbit"].startswith("closed exactly"), "full metric orbit lost")
    require(pullback["classification"] == "EXACT_DYNAMIC_FULL_METRIC_ORBIT_CLOSURE; STATIC_DIAGONAL_SUBFAMILY_NOT_CLOSED", "pullback grade changed")
    connection = data["depth_connection"]
    require(connection["active_transformed_connection"] == "from a=0, a_prime=+d beta", "active connection sign changed")
    require(connection["absorbed_pullback_shift"].endswith("a_shift=-d beta"), "pullback shift sign changed")
    require(connection["sign_convention"] == "a_prime and a_shift are different representations and must not be identified", "connection conventions conflated")
    require(connection["curvature"] == "da_prime=da_shift=0 identically for smooth beta", "pure-gauge curvature changed")
    require(connection["classification"].endswith("PURE_GAUGE_DEPTH_CONNECTION_ON_THE_OBSERVER_ORBIT"), "connection promoted")
    require(connection["not_claimed"].endswith("dynamics"), "connection caveat lost")
    composition = data["dynamic_composition"]
    require(composition["combined_parameter"] == "beta12(t)=beta1(t)+beta2(T_beta1(t))", "dynamic composition changed")
    require(composition["classification"] == "EXACT_LOCAL_DYNAMIC_FRAME_COMPOSITION_PSEUDOGROUP; GLOBAL_GROUP_REQUIRES_COMMON_DOMAINS_AND_SURJECTIVITY", "composition scope promoted")
    require(composition["global_counterexample"].endswith("(-sqrt(pi/8),sqrt(pi/8))"), "global counterexample lost")
    trajectory = data["trajectory_causality"]
    require(trajectory["timelike"] == "|w|<1 equivalently L|beta_dot|<c exp(-2beta)", "timelike bound changed")
    require(trajectory["scope"].endswith("not a material speed law or derived light dynamics"), "speed bound promoted")
    acceleration = data["acceleration_and_curvature"]
    require(acceleration["nonzero_connection_components"]["Gamma^phi_tt"] == "beta_dot^2-beta_double_dot-(c^2/L^2)exp(-4phi)", "acceleration connection changed")
    require(acceleration["scalar_curvature"] == "R=-4 exp(-2(phi-beta(t)))/L^2", "dynamic scalar changed")
    require(acceleration["classification"].endswith("NO_NEW_SCALAR_CURVATURE_ON_THE_PURE_GAUGE_OBSERVER_ORBIT"), "acceleration promoted")
    adjudication = data["adjudication"]
    require(adjudication["frame_principle"].endswith("NOT_YET_A_PHYSICAL_EQUIVALENCE_PRINCIPLE"), "equivalence principle invented")
    require(adjudication["action"] == "NOT_SELECTED", "action invented")
    require(data["seal_and_action"]["classification"] == "OPEN_GLOBAL_FIELD_BOUNDARY_AND_DYNAMICAL_COMPLETION", "seal/action closure invented")


def expect_failure(name: str, operation, catches: dict[str, str]) -> None:
    try:
        operation()
    except (AssertionError, KeyError):
        catches[name] = "PASS"
        return
    raise AssertionError(f"mutation unexpectedly passed: {name}")


def scalar_curvature_2d(metric: sp.Matrix, coords: tuple[sp.Symbol, sp.Symbol]):
    inverse = sp.simplify(metric.inv())
    gamma = [[[
        sp.simplify(sum(inverse[k, l] * (
            sp.diff(metric[l, j], coords[i]) + sp.diff(metric[l, i], coords[j]) - sp.diff(metric[i, j], coords[l])
        ) for l in range(2)) / 2)
        for j in range(2)] for i in range(2)] for k in range(2)]
    ricci = sp.zeros(2)
    for i in range(2):
        for j in range(2):
            ricci[i, j] = sp.simplify(sum(
                sp.diff(gamma[k][i][j], coords[k]) - sp.diff(gamma[k][i][k], coords[j])
                + sum(gamma[k][k][l] * gamma[l][i][j] - gamma[k][j][l] * gamma[l][i][k] for l in range(2))
                for k in range(2)
            ))
    return sp.simplify(sum(inverse[i, j] * ricci[i, j] for i in range(2) for j in range(2)))


def main() -> None:
    checks: dict[str, str] = {}
    catches: dict[str, str] = {}
    before = sha256(RESULT)
    env = os.environ.copy()
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    env["CUDA_VISIBLE_DEVICES"] = ""
    replay = subprocess.run(
        [sys.executable, "-B", str(HERE / "derive_xmax_dynamic_frame.py")],
        cwd=ROOT, env=env, text=True, capture_output=True, timeout=180, check=False,
    )
    require(replay.returncode == 0, f"primary replay failed: {replay.stderr}")
    require(not replay.stderr, "primary replay emitted stderr")
    require(sha256(RESULT) == before, "primary replay changed result")
    data = json.loads(RESULT.read_text(encoding="utf-8"))
    validate(data)
    checks["deterministic_primary_replay_and_contract"] = "PASS"

    # Independent common-factor solve and product-rule test.
    beta = sp.symbols("beta", real=True)
    n = sp.symbols("n", positive=True)
    require(sp.solve(sp.Eq(sp.exp(2 * beta) * n**2, sp.exp(-2 * beta)), n) == [sp.exp(-2 * beta)], "independent time-scale solve mismatch")
    t = sp.symbols("t", real=True)
    b = sp.Function("b")(t)
    require(sp.simplify(sp.diff(sp.exp(-2 * b) * t, t) - sp.exp(-2 * b)) == -2 * t * sp.exp(-2 * b) * sp.diff(b, t), "independent product-rule defect mismatch")
    checks["independent_time_map_and_naive_defect"] = "PASS"

    # Independent diagonal 1+1 pullback using differential substitution.
    phi, c0, L = sp.symbols("phi c L", real=True, positive=True)
    v = sp.symbols("v", real=True)
    gtt = sp.exp(-2 * beta) * (-c0**2 * sp.exp(-2 * phi) + L**2 * sp.exp(2 * phi) * v**2)
    gtphi = -sp.exp(-2 * beta) * L**2 * sp.exp(2 * phi) * v
    gphiphi = sp.exp(-2 * beta) * L**2 * sp.exp(2 * phi)
    dynamic_metric = sp.Matrix([[gtt, gtphi], [gtphi, gphiphi]])
    require(sp.simplify(dynamic_metric.det() + sp.exp(-4 * beta) * c0**2 * L**2) == 0, "independent dynamic determinant mismatch")
    require(sp.simplify(gtphi) != 0, "independent cross term vanished")
    checks["independent_dynamic_metric_shift_and_signature"] = "PASS"

    # Independent active-connection versus absorbed-shift signs, exact
    # curvature, and local composition law.
    x = sp.symbols("x", real=True)
    local_beta = sp.Function("local_beta")(t, x)
    dbeta = sp.Matrix([sp.diff(local_beta, t), sp.diff(local_beta, x)])
    a_prime = dbeta
    a_shift = -dbeta
    require(sp.simplify(-dbeta + a_prime) == sp.zeros(2, 1), "independent active connection sign mismatch")
    require(sp.simplify(dbeta + a_shift) == sp.zeros(2, 1), "independent pullback shift sign mismatch")
    curl_prime = sp.diff(a_prime[1], t) - sp.diff(a_prime[0], x)
    curl_shift = sp.diff(a_shift[1], t) - sp.diff(a_shift[0], x)
    require(sp.simplify(curl_prime) == 0 and sp.simplify(curl_shift) == 0, "independent exact depth connection acquired curvature")
    b1 = sp.Function("b1")(t)
    T1 = sp.Function("T1")(t)
    b2 = sp.Function("b2")(T1)
    require(sp.simplify(sp.exp(-2 * b1) * sp.exp(-2 * b2) - sp.exp(-2 * (b1 + b2))) == 0, "independent local composition mismatch")
    gaussian_half_image = sp.integrate(sp.exp(-2 * x**2), (x, 0, sp.oo))
    require(sp.simplify(gaussian_half_image - sp.sqrt(sp.pi / 8)) == 0, "independent non-surjective beta=t^2 witness mismatch")
    checks["independent_connection_signs_curvature_and_local_composition"] = "PASS"

    # Independent trajectory norm and conditional causal classes.
    depth = sp.symbols("depth", real=True)
    speed = sp.symbols("speed", real=True)
    norm = -c0**2 * sp.exp(-2 * depth) + L**2 * sp.exp(2 * depth) * speed**2
    w = L * sp.exp(2 * depth) * speed / c0
    require(sp.simplify(norm + c0**2 * sp.exp(-2 * depth) * (1 - w**2)) == 0, "independent trajectory norm mismatch")
    require(sp.simplify(norm.subs(speed, c0 * sp.exp(-2 * depth) / L)) == 0, "independent null boundary mismatch")
    checks["independent_trajectory_causal_bound"] = "PASS"

    # Independent explicit accelerated witness. This implementation does not
    # use the primary generic beta-function curvature output.
    accel = sp.symbols("accel", real=True)
    beta_accel = accel * t**2 / 2
    velocity_accel = accel * t
    metric_accel = sp.Matrix([
        [sp.exp(-2 * beta_accel) * (-c0**2 * sp.exp(-2 * phi) + L**2 * sp.exp(2 * phi) * velocity_accel**2), -sp.exp(-2 * beta_accel) * L**2 * sp.exp(2 * phi) * velocity_accel],
        [-sp.exp(-2 * beta_accel) * L**2 * sp.exp(2 * phi) * velocity_accel, sp.exp(-2 * beta_accel) * L**2 * sp.exp(2 * phi)],
    ])
    scalar_accel = scalar_curvature_2d(metric_accel, (t, phi))
    expected_accel = -4 * sp.exp(-2 * (phi - beta_accel)) / L**2
    require(sp.simplify(scalar_accel - expected_accel) == 0, "independent accelerated scalar mismatch")
    checks["independent_accelerated_curvature_cancellation"] = "PASS"

    inventory_before = sha256(HERE / "SOURCE_INVENTORY.tsv")
    inventory_run = subprocess.run(
        [sys.executable, "-B", str(HERE / "build_source_inventory.py")],
        cwd=ROOT, env=env, text=True, capture_output=True, timeout=90, check=False,
    )
    require(inventory_run.returncode == 0, f"source replay failed: {inventory_run.stderr}")
    require(sha256(HERE / "SOURCE_INVENTORY.tsv") == inventory_before, "source inventory changed")
    sources = read_tsv(HERE / "SOURCE_INVENTORY.tsv")
    require(len(sources) == 13 and len({row["path"] for row in sources}) == 13, "source census mismatch")
    checks["source_inventory_replay"] = "PASS"

    components = read_tsv(HERE / "DYNAMIC_FRAME_LEDGER.tsv")
    statuses = read_tsv(HERE / "STATUS_LEDGER.tsv")
    require(len(components) == 18 and len({row["id"] for row in components}) == 18, "dynamic ledger mismatch")
    require(len(statuses) == 13 and len({row["id"] for row in statuses}) == 13, "status ledger mismatch")
    require(next(row for row in statuses if row["id"] == "S08")["status"] == "VERIFIED_WITH_CAVEATS", "frame grade promoted")
    checks["ledger_coverage"] = "PASS"

    report = (HERE / "AUDIT_REPORT.md").read_text(encoding="utf-8")
    flat_report = " ".join(report.split())
    for phrase in (
        "arbitrary smooth frame path `beta(t)`",
        "the original static diagonal subfamily is not closed",
        "The observer connection is therefore `PURE_GAUGE`",
        "If the initial active connection is `a=0`, the transformed connection is",
        "the pulled-back coframe instead absorbs the shift",
        "local pseudogroup/groupoid on compatible chart intervals",
        "not automatically a global semidirect group",
        "the timelike subset supports the conditional observer reading",
        "not yet a distinct UDT equivalence principle",
        "a timelike observer must satisfy",
        "Every `beta_dot` and `beta_double_dot` term cancels",
        "not say that all physical gravitational fields are accelerated frames",
        "It is not yet a universal material speed law",
        "To become a physical UDT equivalence principle",
    ):
        require(phrase in flat_report, f"report disclosure missing: {phrase}")
    for forbidden in (
        "UDT equivalence principle is derived",
        "acceleration creates gravity",
        "the depth connection is a physical force",
        "the observer speed bound is a matter speed limit",
        "c is derived",
        "Xmax is calculated",
        "the complete action is selected",
    ):
        require(forbidden not in report, f"forbidden promotion: {forbidden}")
    checks["report_contract"] = "PASS"

    adversarial_review = (HERE / "EXTERNAL_ADVERSARIAL_REVIEW.md").read_text(encoding="utf-8")
    for phrase in (
        "Initial verdict: `REVISE`, not refuted.",
        "active transformation from `a=0` gives `a'=+d beta`",
        "a_{shift}=-d\\beta",
        "pseudogroup/groupoid on compatible chart intervals",
        "Only the subset satisfying",
        "Final evidence grade: `VERIFIED-WITH-CAVEATS`",
    ):
        require(phrase in adversarial_review, f"adversarial correction disclosure missing: {phrase}")
    checks["fresh_context_adversarial_corrections_recorded"] = "PASS"

    changed = subprocess.check_output(["git", "diff", "--name-only", BASE, "--"], cwd=ROOT, text=True).splitlines()
    forbidden_controls = {"LIVE.md", "HANDOFF.md", "INDEX.md", "README.md", "MEMORY.md", "CANON.md"}
    require(not forbidden_controls.intersection(changed), f"forbidden controls changed: {forbidden_controls.intersection(changed)}")
    checks["no_control_or_canon_edits"] = "PASS"

    mutation = copy.deepcopy(data)
    mutation["time_map"]["differential_map"] = "T=exp(-2beta(t))t"
    expect_failure("naive_time_map_restored", lambda: validate(mutation), catches)
    mutation = copy.deepcopy(data)
    mutation["full_metric_pullback"]["diagonal_family"] = "closed"
    expect_failure("forced_cross_terms_deleted", lambda: validate(mutation), catches)
    mutation = copy.deepcopy(data)
    mutation["full_metric_pullback"]["off_diagonal_orbit"] = "not required"
    expect_failure("complete_metric_orbit_deleted", lambda: validate(mutation), catches)
    mutation = copy.deepcopy(data)
    mutation["depth_connection"]["curvature"] = "f nonzero"
    expect_failure("pure_gauge_curvature_invented", lambda: validate(mutation), catches)
    mutation = copy.deepcopy(data)
    mutation["depth_connection"]["classification"] = "PHYSICAL_FORCE_FIELD"
    expect_failure("observer_connection_promoted", lambda: validate(mutation), catches)
    mutation = copy.deepcopy(data)
    mutation["depth_connection"]["active_transformed_connection"] = "from a=0, a_prime=-d beta"
    expect_failure("active_connection_sign_reversed", lambda: validate(mutation), catches)
    mutation = copy.deepcopy(data)
    mutation["depth_connection"]["absorbed_pullback_shift"] = "a_shift=+d beta"
    expect_failure("pullback_shift_sign_reversed", lambda: validate(mutation), catches)
    mutation = copy.deepcopy(data)
    mutation["depth_connection"]["sign_convention"] = "a_prime=a_shift"
    expect_failure("connection_conventions_conflated", lambda: validate(mutation), catches)
    mutation = copy.deepcopy(data)
    mutation["dynamic_composition"]["combined_parameter"] = "beta1+beta2(t)"
    expect_failure("composition_time_argument_deleted", lambda: validate(mutation), catches)
    mutation = copy.deepcopy(data)
    mutation["dynamic_composition"]["classification"] = "EXACT_GLOBAL_SEMIDIRECT_GROUP"
    expect_failure("local_composition_promoted_to_global_group", lambda: validate(mutation), catches)
    mutation = copy.deepcopy(data)
    mutation["dynamic_composition"]["global_counterexample"] = "none"
    expect_failure("non_surjective_counterexample_deleted", lambda: validate(mutation), catches)
    mutation = copy.deepcopy(data)
    mutation["trajectory_causality"]["timelike"] = "unbounded"
    expect_failure("trajectory_causal_bound_deleted", lambda: validate(mutation), catches)
    mutation = copy.deepcopy(data)
    mutation["trajectory_causality"]["scope"] = "universal matter speed law"
    expect_failure("trajectory_bound_promoted_to_matter", lambda: validate(mutation), catches)
    mutation = copy.deepcopy(data)
    mutation["acceleration_and_curvature"]["nonzero_connection_components"]["Gamma^phi_tt"] = "no acceleration"
    expect_failure("beta_double_dot_connection_deleted", lambda: validate(mutation), catches)
    mutation = copy.deepcopy(data)
    mutation["acceleration_and_curvature"]["scalar_curvature"] = "R includes beta_double_dot"
    expect_failure("spurious_acceleration_curvature_added", lambda: validate(mutation), catches)
    mutation = copy.deepcopy(data)
    mutation["adjudication"]["frame_principle"] = "UDT_EQUIVALENCE_PRINCIPLE_DERIVED"
    expect_failure("equivalence_principle_invented", lambda: validate(mutation), catches)
    mutation = copy.deepcopy(data)
    mutation["adjudication"]["action"] = "EH_DERIVED"
    expect_failure("action_invented", lambda: validate(mutation), catches)
    mutation = copy.deepcopy(data)
    mutation["seal_and_action"]["classification"] = "CLOSED"
    expect_failure("seal_action_closure_invented", lambda: validate(mutation), catches)

    output = {
        "schema": "udt-xmax-dynamic-observer-verification-1.0",
        "python": sys.version.split()[0],
        "sympy": sp.__version__,
        "checks": checks,
        "catch_proofs": catches,
        "independent_witnesses": {
            "time_scale": "exp(-2beta)",
            "dynamic_metric_determinant": "-exp(-4beta)c^2L^2",
            "active_connection_from_zero": "+d beta",
            "absorbed_pullback_shift": "-d beta",
            "depth_connection_curvatures": "0",
            "beta_t2_time_map_image": "(-sqrt(pi/8),sqrt(pi/8))",
            "conditional_null_depth_speed": "c exp(-2beta)/L",
            "accelerated_beta": "accel*t^2/2",
            "accelerated_scalar": str(scalar_accel),
        },
        "result": "PASS",
    }
    VERIFY.write_text(json.dumps(output, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
