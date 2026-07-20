#!/usr/bin/env python3
"""Independent projective-join verifier and fail-closed semantic catches."""

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
BASE = "85f94e10324d5c56f81d335b524afc700435d4c9"
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
    require(data["schema"] == "udt-projective-position-join-audit-1.0", "schema changed")
    require(len(data["checks"]) == 41 and all(value == "PASS" for value in data["checks"].values()), "primary check census/failure")
    ray = data["reciprocal_csn_ray"]
    require(ray["classification"] == "DERIVED_IN_DECLARED_DUAL_RECIPROCAL_REPRESENTATION", "projective ray grade changed")
    normalized = data["normalized_imbalance"]
    require(normalized["uniqueness"].startswith("UNIQUE_ONLY_AMONG_FIRST_DEGREE"), "bounded uniqueness overclaimed")
    require(normalized["physical_join"] == "NOT_YET_DERIVED", "physical join invented")
    family = data["counterfamily"]
    require(family["definition"] == "f_epsilon(xi)=xi+epsilon*xi*(1-xi^2)", "registered counterfamily changed")
    require(family["parameter_interval"] == "-1<epsilon<1/2", "counterfamily interval changed")
    require(family["classification"] == "EXACT_KINEMATIC_READOUT_COUNTERFAMILY_UNDER_CURRENT_PREMISES", "counterfamily rejected without premise")
    require(family["slope_matched_companion"]["neutral_derivative"] == "g_epsilon_prime(0)=1 for every epsilon", "slope-matched counterfamily lost")
    coframe = data["composition_and_coframe"]
    require(coframe["selection_result"].startswith("THE_COMPLETE_PHI_COFRAME_ACTION_IS_IDENTICAL"), "coframe falsely selected chart")
    depths = data["two_depths"]
    require(depths["classification"] == "DERIVED_CONDITIONAL_IN_THE_SHARED_STATIC_RECIPROCAL_REPRESENTATION", "two-depth map scope changed")
    require(depths["seal_seen_by_observer"] == "phi_rel(S;O)=-Phi(O)", "seal relative depth changed")
    require("generically neither zero nor an endpoint" in depths["seal_projective_display"], "seal silently identified with endpoint")
    global_data = data["finite_cell_and_bootstrap"]
    require(global_data["classification"] == "NO_CURRENT_FINITE_CELL_OR_BOOTSTRAP_READOUT_SELECTOR_FOUND", "bootstrap selector invented")
    adjudication = data["adjudication"]
    require(adjudication["projective_position_join"].startswith("OPEN"), "projective join promoted")
    require(adjudication["selector_status"] == "ABSENT; IDENTIFIED_NOT_ADOPTED", "missing selector adopted")
    require(adjudication["smallest_missing_selector"].startswith("PHYSICAL_POSITION_IS_A_FIRST_DEGREE"), "missing selector obscured")


def expect_failure(name: str, operation, catches: dict[str, str]) -> None:
    try:
        operation()
    except (AssertionError, KeyError):
        catches[name] = "PASS"
        return
    raise AssertionError(f"mutation unexpectedly passed: {name}")


def main() -> None:
    checks: dict[str, str] = {}
    catches: dict[str, str] = {}
    before = sha256(RESULT)
    env = os.environ.copy()
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    env["CUDA_VISIBLE_DEVICES"] = ""
    replay = subprocess.run(
        [sys.executable, "-B", str(HERE / "derive_projective_join.py")],
        cwd=ROOT,
        env=env,
        text=True,
        capture_output=True,
        timeout=180,
        check=False,
    )
    require(replay.returncode == 0, f"primary replay failed: {replay.stderr}")
    require(not replay.stderr, "primary replay emitted stderr")
    require(sha256(RESULT) == before, "primary replay changed result")
    data = json.loads(RESULT.read_text(encoding="utf-8"))
    validate(data)
    checks["deterministic_primary_replay_and_contract"] = "PASS"

    # Independent anchored Mobius solution without reusing the primary solve.
    r = sp.symbols("r", positive=True)
    A, B, C, D = sp.symbols("A B C D", real=True)
    # Homogeneous coefficient scale is fixed by D=1. Anchor equations then
    # directly determine the remaining coefficients.
    equations = [sp.Eq(D, 1), sp.Eq(B, -D), sp.Eq(A + B, 0), sp.Eq(A, C)]
    solution = sp.solve(equations, [A, B, C, D], dict=True)
    require(solution == [{A: 1, B: -1, C: 1, D: 1}], f"independent anchored Mobius solution mismatch: {solution}")
    anchored = (r - 1) / (r + 1)
    require(anchored.subs(r, 1) == 0 and sp.limit(anchored, r, 0, dir="+") == -1 and sp.limit(anchored, r, sp.oo) == 1, "independent anchors failed")
    checks["independent_anchored_projective_uniqueness_in_class"] = "PASS"

    # Independent, stronger counterfamily. It preserves the three anchors and
    # the first derivative at the neutral point and both endpoints.
    x = sp.symbols("x", real=True)
    lam = sp.Rational(1, 100)
    h = x + lam * x**3 * (1 - x**2) ** 2
    hp = sp.expand(sp.diff(h, x))
    require(sp.simplify(h.subs(x, 0)) == 0 and sp.simplify(h.subs(x, 1) - 1) == 0 and sp.simplify(h.subs(x, -1) + 1) == 0, "independent counterfamily anchors failed")
    require(sp.simplify(h.subs(x, -x) + h) == 0, "independent counterfamily parity failed")
    require(hp.subs(x, 0) == 1 and hp.subs(x, 1) == 1 and hp.subs(x, -1) == 1, "independent counterfamily slope anchors failed")
    correction = sp.expand((hp - 1) / lam)
    coefficient_bound = sum(abs(coefficient) for coefficient in sp.Poly(correction, x).all_coeffs())
    require(coefficient_bound == 20, "independent derivative bound changed")
    require(1 - lam * coefficient_bound == sp.Rational(4, 5), "independent monotonic lower bound changed")
    require(sp.simplify(h.subs(x, sp.Rational(1, 2)) - sp.Rational(1, 2)) != 0, "independent counterfamily became identity")
    checks["independent_anchor_and_slope_matched_counterfamily"] = "PASS"

    # Independent conjugate composition witness.
    mobius = lambda left, right: sp.simplify((left + right) / (1 + left * right))
    left, right = sp.Rational(1, 4), sp.Rational(1, 6)
    h_of = lambda value: sp.simplify(value + lam * value**3 * (1 - value**2) ** 2)
    conjugate = h_of(mobius(left, right))
    naive = mobius(h_of(left), h_of(right))
    require(sp.simplify(conjugate - naive) != 0, "independent nonlinear display obeyed original Mobius law")
    p, q, s = sp.symbols("p q s", real=True)
    display = lambda depth: h_of(sp.tanh(depth))
    require(sp.simplify((display((p + q) + s) - display(p + (q + s))).rewrite(sp.exp)) == 0, "independent conjugate associativity failed")
    checks["independent_conjugate_group_not_original_mobius"] = "PASS"

    # Independent CSN and coframe checks.
    common = sp.symbols("common", positive=True)
    u, v = sp.symbols("u v", positive=True)
    xi = (v - u) / (v + u)
    require(sp.simplify(xi.subs({u: common * u, v: common * v}) - xi) == 0, "independent CSN invariance failed")
    require(sp.simplify(xi.xreplace({u: v, v: u}) + xi) == 0, "independent reciprocal exchange failed")
    phi, beta = sp.symbols("phi beta", real=True)
    Dmap = lambda depth: sp.diag(sp.exp(-depth), sp.exp(depth))
    require((Dmap(phi) * Dmap(-beta) - Dmap(phi - beta)).applyfunc(sp.simplify) == sp.zeros(2), "independent coframe group failed")
    checks["independent_csn_exchange_and_coframe_indifference"] = "PASS"

    # Independent two-depth matrix calculation and seal evaluation.
    PhiP, PhiO = sp.symbols("PhiP PhiO", real=True)
    relative = (Dmap(PhiP) * Dmap(PhiO).inv()).applyfunc(sp.simplify)
    require((relative - Dmap(PhiP - PhiO)).applyfunc(sp.simplify) == sp.zeros(2), "independent two-depth map failed")
    seal_relative = -PhiO
    require(sp.simplify(sp.tanh(seal_relative) + sp.tanh(PhiO)) == 0, "independent seal display failed")
    checks["independent_absolute_relative_depth_and_seal"] = "PASS"

    inventory_before = sha256(HERE / "SOURCE_INVENTORY.tsv")
    inventory_run = subprocess.run(
        [sys.executable, "-B", str(HERE / "build_source_inventory.py")],
        cwd=ROOT,
        env=env,
        text=True,
        capture_output=True,
        timeout=90,
        check=False,
    )
    require(inventory_run.returncode == 0, f"source replay failed: {inventory_run.stderr}")
    require(sha256(HERE / "SOURCE_INVENTORY.tsv") == inventory_before, "source inventory changed")
    sources = read_tsv(HERE / "SOURCE_INVENTORY.tsv")
    require(len(sources) == 13 and len({row["path"] for row in sources}) == 13, "source census mismatch")
    checks["source_inventory_replay"] = "PASS"

    components = read_tsv(HERE / "PROJECTIVE_JOIN_LEDGER.tsv")
    statuses = read_tsv(HERE / "STATUS_LEDGER.tsv")
    require(len(components) == 18 and len({row["id"] for row in components}) == 18, "join ledger mismatch")
    require(len(statuses) == 14 and len({row["id"] for row in statuses}) == 14, "status ledger mismatch")
    require(next(row for row in statuses if row["id"] == "S03")["status"] == "OPEN", "join promoted in ledger")
    checks["ledger_coverage"] = "PASS"

    report = (HERE / "AUDIT_REPORT.md").read_text(encoding="utf-8")
    flat_report = " ".join(report.split()).casefold()
    for phrase in (
        "The normalized imbalance is already almost derived",
        "current UDT does not yet require physical position",
        "even silently matching the local slope",
        "The complete metric continues to use `dphi`",
        "the physical seal remains at absolute zero",
        "qualitative bootstrap statement cannot distinguish epsilon",
        "identifies that selector but does not adopt it",
    ):
        require(phrase.casefold() in flat_report, f"report disclosure missing: {phrase}")
    for forbidden in (
        "projective-position join is derived unconditionally",
        "the seal is the X_max endpoint",
        "bootstrap selects tanh",
        "physical position must equal normalized imbalance",
        "the complete action is selected",
    ):
        require(forbidden not in report, f"forbidden promotion: {forbidden}")
    checks["report_contract"] = "PASS"

    changed = subprocess.check_output(["git", "diff", "--name-only", BASE, "--"], cwd=ROOT, text=True).splitlines()
    forbidden_controls = {"LIVE.md", "HANDOFF.md", "INDEX.md", "README.md", "MEMORY.md", "CANON.md"}
    require(not forbidden_controls.intersection(changed), f"forbidden controls changed: {forbidden_controls.intersection(changed)}")
    checks["no_control_or_canon_edits"] = "PASS"

    mutation = copy.deepcopy(data)
    mutation["normalized_imbalance"]["uniqueness"] = "UNIQUE_AMONG_ALL_BOUNDED_COORDINATES"
    expect_failure("anchored_class_scope_deleted", lambda: validate(mutation), catches)
    mutation = copy.deepcopy(data)
    mutation["normalized_imbalance"]["physical_join"] = "DERIVED"
    expect_failure("physical_join_invented", lambda: validate(mutation), catches)
    mutation = copy.deepcopy(data)
    mutation["counterfamily"]["classification"] = "REJECTED"
    expect_failure("counterfamily_rejected_without_premise", lambda: validate(mutation), catches)
    mutation = copy.deepcopy(data)
    mutation["counterfamily"]["slope_matched_companion"]["neutral_derivative"] = "not matched"
    expect_failure("slope_matched_counterfamily_deleted", lambda: validate(mutation), catches)
    mutation = copy.deepcopy(data)
    mutation["composition_and_coframe"]["selection_result"] = "COFRAME_SELECTS_EPSILON_ZERO"
    expect_failure("coframe_chart_selection_invented", lambda: validate(mutation), catches)
    mutation = copy.deepcopy(data)
    mutation["two_depths"]["classification"] = "UNCONDITIONAL_GLOBAL_THEOREM"
    expect_failure("two_depth_map_scope_promoted", lambda: validate(mutation), catches)
    mutation = copy.deepcopy(data)
    mutation["two_depths"]["seal_seen_by_observer"] = "phi_rel(S;O)=0"
    expect_failure("seal_moved_to_relative_zero", lambda: validate(mutation), catches)
    mutation = copy.deepcopy(data)
    mutation["two_depths"]["seal_projective_display"] = "xi=1 endpoint"
    expect_failure("seal_moved_to_xmax_endpoint", lambda: validate(mutation), catches)
    mutation = copy.deepcopy(data)
    mutation["finite_cell_and_bootstrap"]["classification"] = "BOOTSTRAP_SELECTS_TANH"
    expect_failure("bootstrap_selector_invented", lambda: validate(mutation), catches)
    mutation = copy.deepcopy(data)
    mutation["adjudication"]["projective_position_join"] = "DERIVED"
    expect_failure("join_status_promoted", lambda: validate(mutation), catches)
    mutation = copy.deepcopy(data)
    mutation["adjudication"]["selector_status"] = "ADOPTED"
    expect_failure("missing_selector_adopted", lambda: validate(mutation), catches)

    output = {
        "schema": "udt-projective-position-join-verification-1.0",
        "python": sys.version.split()[0],
        "sympy": sp.__version__,
        "checks": checks,
        "catch_proofs": catches,
        "independent_witnesses": {
            "anchored_mobius": "(r-1)/(r+1)",
            "counterfamily": "h(x)=x+(1/100)x^3(1-x^2)^2",
            "counterfamily_derivative_lower_bound": "4/5 on [-1,1] by coefficient triangle bound",
            "counterfamily_slopes": "h'(0)=h'(-1)=h'(+1)=1",
            "conjugate_not_original_mobius": str(sp.simplify(conjugate - naive)),
            "relative_depth": "PhiP-PhiO",
            "seal_relative_depth": "-PhiO",
        },
        "result": "PASS",
    }
    VERIFY.write_text(json.dumps(output, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
