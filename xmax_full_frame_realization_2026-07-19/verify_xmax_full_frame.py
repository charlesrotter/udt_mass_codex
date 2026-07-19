#!/usr/bin/env python3
"""Independent Lie-derivative/projective verifier and fail-closed catches."""

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
BASE = "07f397607c2ca784630034a97fb7f24cf08d378d"
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
    require(data["schema"] == "udt-xmax-full-frame-realization-1.0", "schema changed")
    require(len(data["checks"]) == 36 and all(value == "PASS" for value in data["checks"].values()), "primary check census/failure")
    projective = data["projective_position"]
    require(projective["anchored_coordinate"] == "xi=(r-1)/(r+1)=(v-u)/(v+u)=tanh(phi)", "projective chart changed")
    require("CONDITIONAL_ON_IDENTIFYING_POSITIONAL_SEPARATION" in projective["classification"], "projective join promoted or lost")
    require(projective["remaining_choice"].endswith("not yet owner-locked by the current foundation"), "projective caveat lost")
    frame = data["full_frame"]
    require(frame["frame_map"] == "phi'=phi-beta; t'=exp(-2beta)t; y'=y; X_max'=X_max; c'=c", "frame map changed")
    require(frame["metric_action"] == "F_beta pullback g = exp(-2beta) g", "common CSN factor changed")
    require(frame["classification"] == "EXACT_FULL_FOUR_DIMENSIONAL_FRAME_REALIZATION_IN_DECLARED_RECIPROCAL_CSN_COFRAME_FAMILY", "frame scope promoted or lost")
    require(frame["spatial_seed_condition"].startswith("h=h(y) is stationary and F_beta-invariant"), "stationarity/frame invariance lost")
    depth = data["depth_vs_bounded_differential"]
    require(depth["pure_depth_solution"] == "k(phi)=constant=L, hence reciprocal spatial coframe L dphi", "depth coframe changed")
    require(depth["bounded_dx_witness_beta_atanh_one_third"] == {"time_ratio": "1/2", "spatial_ratio_phi_zero": "32/81", "spatial_ratio_xi_half": "512/625"}, "bounded dx counterwitness changed")
    require(depth["free_time_exponent_counterfamily"] == "k(phi)=exp(a phi), t'=exp(-(a+2)beta)t gives common factor exp(-2(a+1)beta)", "free time-exponent counterfamily lost")
    require(depth["classification"].startswith("FIXED_F3_TIME_ACTION_SELECTS"), "fixed F3 scope lost")
    require(depth["scope"].startswith("constant k is selected only with fixed"), "depth-selection scope lost")
    transverse = data["transverse_sector"]
    require(transverse["positive_solution"] == "R(phi)=C exp(phi)", "transverse warp solution changed")
    require("INTRINSIC_TRANSVERSE_GEOMETRY_TOPOLOGY_ROUNDNESS_TWIST_AND_BOUNDARY_REMAIN_OPEN" in transverse["classification"], "angular result promoted")
    require(len(transverse["surviving_intrinsic_seeds"]) == 3, "transverse counterfamily lost")
    counter = data["two_dimensional_conformal_counterfamily"]
    require(counter["classification"].startswith("EXACT_COUNTERFAMILY"), "1+1 conformal nonuniqueness lost")
    seal = data["seal_and_bootstrap"]
    require(seal["classification"] == "RELATIONAL_DEPTH_AND_ABSOLUTE_STATIC_SEAL_FIELD_CANNOT_BE_SILENTLY_IDENTIFIED_IN_THIS_FRAME_REALIZATION", "seal silently joined")
    require("not derived" in seal["c_caveat"], "c value/origin promoted")
    adjudication = data["adjudication"]
    require(adjudication["realization"].startswith("EXACT_CONDITIONAL"), "conditional realization promoted")
    require(adjudication["positional_law"].startswith("DERIVED_CONDITIONAL_ON_PROJECTIVE_POSITION_JOIN"), "positional law promoted")
    require(adjudication["action"] == "NOT_SELECTED", "action invented")


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
        [sys.executable, "-B", str(HERE / "derive_xmax_full_frame.py")],
        cwd=ROOT, env=env, text=True, capture_output=True, timeout=180, check=False,
    )
    require(replay.returncode == 0, f"derivation replay failed: {replay.stderr}")
    require(not replay.stderr, "derivation replay emitted stderr")
    require(sha256(RESULT) == before, "derivation replay changed result")
    data = json.loads(RESULT.read_text(encoding="utf-8"))
    validate(data)
    checks["deterministic_primary_replay_and_contract"] = "PASS"

    # Independent projective-coordinate derivation.
    r = sp.symbols("r", positive=True)
    a, b, c, d = sp.symbols("a b c d")
    solution = sp.solve((b + d, a + b, a - c), (b, c, d), dict=True)
    require(solution == [{b: -a, c: a, d: a}], "independent projective anchor solution mismatch")
    anchored = sp.cancel((a * r - a) / (a * r + a))
    require(sp.simplify(anchored - (r - 1) / (r + 1)) == 0, "independent anchored chart mismatch")
    r1, r2 = sp.symbols("r1 r2", positive=True)
    cayley = lambda value: sp.cancel((value - 1) / (value + 1))
    require(sp.simplify(cayley(r1 * r2) - (cayley(r1) + cayley(r2)) / (1 + cayley(r1) * cayley(r2))) == 0, "independent projective composition mismatch")
    checks["independent_projective_anchor_and_composition"] = "PASS"

    # Independent infinitesimal homothety calculation. The generator of the
    # finite frame map is K=-2t d_t-d_phi. Compute the full Lie derivative.
    t, phi, y1, y2 = sp.symbols("t phi y1 y2", real=True)
    coords = (t, phi, y1, y2)
    c0 = sp.symbols("c", positive=True)
    h11, h12, h13, h22, h23, h33 = sp.symbols("h11 h12 h13 h22 h23 h33", real=True)
    H = sp.Matrix([[h11, h12, h13], [h12, h22, h23], [h13, h23, h33]])
    g = sp.diag(-sp.exp(-2 * phi) * c0**2, 1, 1, 1)
    g[1:4, 1:4] = sp.exp(2 * phi) * H
    K = sp.Matrix([-2 * t, -1, 0, 0])
    lie = sp.zeros(4)
    for mu in range(4):
        for nu in range(4):
            transport = sum(K[rho] * sp.diff(g[mu, nu], coords[rho]) for rho in range(4))
            index_terms = sum(g[rho, nu] * sp.diff(K[rho], coords[mu]) + g[mu, rho] * sp.diff(K[rho], coords[nu]) for rho in range(4))
            lie[mu, nu] = sp.simplify(transport + index_terms)
    require(lie.applyfunc(sp.simplify) == (-2 * g).applyfunc(sp.simplify), "independent Lie homothety mismatch")
    checks["independent_full_metric_Lie_homothety"] = "PASS"

    # Independent finite bounded-dx mismatch at the registered parameter.
    xi = sp.symbols("xi", real=True)
    alpha = sp.Rational(1, 3)
    derivative = (1 - alpha**2) / (1 - alpha * xi) ** 2
    time_ratio = (1 - alpha) / (1 + alpha)
    spatial = sp.simplify(time_ratio * derivative**2)
    samples = [sp.simplify(spatial.subs(xi, point)) for point in (0, sp.Rational(1, 2))]
    require(time_ratio == sp.Rational(1, 2), "independent time ratio mismatch")
    require(samples == [sp.Rational(32, 81), sp.Rational(512, 625)], "independent bounded dx witnesses mismatch")
    checks["independent_bounded_dx_counterwitness"] = "PASS"

    # Independent counterfamily when the time exponent is not fixed.
    exponent, beta_general = sp.symbols("a beta_general", real=True)
    common_general = sp.exp(-2 * (exponent + 1) * beta_general)
    temporal_general = sp.exp(2 * beta_general) * sp.exp(-2 * (exponent + 2) * beta_general)
    spatial_general = sp.exp(2 * (phi - beta_general)) * sp.exp(2 * exponent * (phi - beta_general)) / (sp.exp(2 * phi) * sp.exp(2 * exponent * phi))
    require(sp.simplify(temporal_general - common_general) == 0 and sp.simplify(spatial_general - common_general) == 0, "free time-exponent counterfamily mismatch")
    checks["independent_free_time_exponent_counterfamily"] = "PASS"

    # Independent transverse functional equation and surviving intrinsic seeds.
    beta, C = sp.symbols("beta C", real=True, positive=True)
    R = C * sp.exp(phi)
    require(sp.simplify(R.subs(phi, phi - beta) - sp.exp(-beta) * R) == 0, "independent transverse functional equation mismatch")
    theta = sp.symbols("theta", real=True)
    q_round = sp.diag(1, sp.sin(theta)**2)
    q_flat = sp.eye(2)
    require(sp.diff(q_round, phi) == sp.zeros(2) and sp.diff(q_flat, phi) == sp.zeros(2), "intrinsic transverse counterfamily lost")
    checks["independent_transverse_weight_and_counterfamily"] = "PASS"

    # Independent null-coordinate proof of unrestricted local 1+1 freedom.
    p, q, A0, A1 = sp.symbols("p q A0 A1", positive=True)
    eta0 = sp.Matrix([[0, -A0 / 2], [-A0 / 2, 0]])
    eta1 = sp.Matrix([[0, -A1 / 2], [-A1 / 2, 0]])
    J = sp.diag(p, q)
    factor = A1 * p * q / A0
    require((J.T * eta1 * J - factor * eta0).applyfunc(sp.simplify) == sp.zeros(2), "independent null conformal counterfamily mismatch")
    checks["independent_1plus1_conformal_counterfamily"] = "PASS"

    # The same internally shifted scalar cannot retain an absolute zero seal.
    nonzero_beta = sp.symbols("nonzero_beta", nonzero=True)
    require(sp.simplify(0 - nonzero_beta) != 0, "absolute seal falsely invariant")
    checks["independent_relational_absolute_seal_mismatch"] = "PASS"

    inventory_before = sha256(HERE / "SOURCE_INVENTORY.tsv")
    inventory_run = subprocess.run(
        [sys.executable, "-B", str(HERE / "build_source_inventory.py")],
        cwd=ROOT, env=env, text=True, capture_output=True, timeout=90, check=False,
    )
    require(inventory_run.returncode == 0, f"source replay failed: {inventory_run.stderr}")
    require(sha256(HERE / "SOURCE_INVENTORY.tsv") == inventory_before, "source inventory changed")
    sources = read_tsv(HERE / "SOURCE_INVENTORY.tsv")
    require(len(sources) == 13 and len({row["path"] for row in sources}) == 13, "source census mismatch")
    require(next(row for row in sources if row["path"] == "simple_metric_xmax_POSTULATE.md")["source_class"] == "POST_JULY_WORKING_LEAD", "Xmax source promoted")
    checks["source_inventory_replay"] = "PASS"

    components = read_tsv(HERE / "FRAME_COMPONENT_LEDGER.tsv")
    statuses = read_tsv(HERE / "STATUS_LEDGER.tsv")
    require(len(components) == 14 and len({row["id"] for row in components}) == 14, "component ledger mismatch")
    require(len(statuses) == 14 and len({row["id"] for row in statuses}) == 14, "status ledger mismatch")
    require(next(row for row in statuses if row["id"] == "S02")["status"] == "DERIVED_CONDITIONAL_ON_PROJECTIVE_POSITION_JOIN", "projective conditional stamp lost")
    require(next(row for row in statuses if row["id"] == "S10")["status"] == "OPEN_ROLE_DISTINCTION", "seal role promoted")
    checks["ledger_coverage"] = "PASS"

    report = (HERE / "AUDIT_REPORT.md").read_text(encoding="utf-8")
    flat_report = " ".join(report.split())
    for phrase in (
        "A complete four-dimensional positional frame action **does exist**",
        "It is a CSN homothety, not generally an isometry",
        "`PROJECTIVE_POSITION_JOIN` is the smallest remaining premise",
        "the reciprocal spatial coframe must be based on **additive positional depth**",
        "This selection is scoped to the fixed F3 time action",
        "It does **not** select the intrinsic two-metric `q_AB`",
        "local 1+1 conformal freedom nor CSN alone selects XR1",
        "The finite-cell seam remains real",
        "does not yet turn the null cone into a native propagation theorem",
        "It is not itself that action",
    ):
        require(phrase in flat_report, f"report disclosure missing: {phrase}")
    for forbidden in (
        "P2 is unconditionally derived",
        "the round S2 is selected",
        "the finite-cell seal is observer gauge",
        "Xmax is derived from total mass",
        "c is derived from the universe",
        "the complete UDT action is selected",
    ):
        require(forbidden not in report, f"forbidden promotion: {forbidden}")
    checks["report_contract"] = "PASS"

    changed = subprocess.check_output(["git", "diff", "--name-only", BASE, "--"], cwd=ROOT, text=True).splitlines()
    forbidden_controls = {"LIVE.md", "HANDOFF.md", "INDEX.md", "README.md", "MEMORY.md", "CANON.md"}
    require(not forbidden_controls.intersection(changed), f"forbidden controls changed: {forbidden_controls.intersection(changed)}")
    checks["no_control_or_canon_edits"] = "PASS"

    mutation = copy.deepcopy(data)
    mutation["projective_position"]["classification"] = "UNCONDITIONAL_NATIVE_POSITION_LAW"
    expect_failure("projective_position_join_promoted", lambda: validate(mutation), catches)
    mutation = copy.deepcopy(data)
    mutation["projective_position"]["remaining_choice"] = "owner-locked"
    expect_failure("projective_join_caveat_deleted", lambda: validate(mutation), catches)
    mutation = copy.deepcopy(data)
    mutation["full_frame"]["metric_action"] = "F_beta pullback g = g"
    expect_failure("CSN_homothety_falsely_promoted_to_isometry", lambda: validate(mutation), catches)
    mutation = copy.deepcopy(data)
    mutation["full_frame"]["frame_map"] = "phi'=phi-beta; t'=t"
    expect_failure("time_frame_action_deleted", lambda: validate(mutation), catches)
    mutation = copy.deepcopy(data)
    mutation["full_frame"]["spatial_seed_condition"] = "partial_phi h=0 only"
    expect_failure("stationary_frame_invariance_deleted", lambda: validate(mutation), catches)
    mutation = copy.deepcopy(data)
    mutation["depth_vs_bounded_differential"]["pure_depth_solution"] = "bounded dx"
    expect_failure("additive_depth_selection_deleted", lambda: validate(mutation), catches)
    mutation = copy.deepcopy(data)
    del mutation["depth_vs_bounded_differential"]["free_time_exponent_counterfamily"]
    expect_failure("free_time_exponent_counterfamily_deleted", lambda: validate(mutation), catches)
    mutation = copy.deepcopy(data)
    mutation["depth_vs_bounded_differential"]["bounded_dx_witness_beta_atanh_one_third"]["spatial_ratio_phi_zero"] = "1/2"
    expect_failure("bounded_dx_counterwitness_hidden", lambda: validate(mutation), catches)
    mutation = copy.deepcopy(data)
    mutation["transverse_sector"]["classification"] = "UNIQUE_ROUND_S2"
    expect_failure("intrinsic_angular_geometry_invented", lambda: validate(mutation), catches)
    mutation = copy.deepcopy(data)
    mutation["transverse_sector"]["surviving_intrinsic_seeds"] = ["round S2"]
    expect_failure("transverse_counterfamily_deleted", lambda: validate(mutation), catches)
    mutation = copy.deepcopy(data)
    mutation["two_dimensional_conformal_counterfamily"]["classification"] = "XR1_UNIQUE_FROM_1PLUS1_CSN"
    expect_failure("1plus1_conformal_nonuniqueness_deleted", lambda: validate(mutation), catches)
    mutation = copy.deepcopy(data)
    mutation["seal_and_bootstrap"]["classification"] = "RELATIONAL_PHI_EQUALS_ABSOLUTE_SEAL_FIELD"
    expect_failure("seal_role_silently_identified", lambda: validate(mutation), catches)
    mutation = copy.deepcopy(data)
    mutation["seal_and_bootstrap"]["c_caveat"] = "c derived"
    expect_failure("c_value_origin_invented", lambda: validate(mutation), catches)
    mutation = copy.deepcopy(data)
    mutation["adjudication"]["realization"] = "UNCONDITIONAL_COMPLETE_UDT_FRAME"
    expect_failure("declared_frame_scope_promoted", lambda: validate(mutation), catches)
    mutation = copy.deepcopy(data)
    mutation["adjudication"]["positional_law"] = "UNCONDITIONAL_DERIVED"
    expect_failure("positional_law_promoted", lambda: validate(mutation), catches)
    mutation = copy.deepcopy(data)
    mutation["adjudication"]["action"] = "EH_DERIVED"
    expect_failure("action_invented", lambda: validate(mutation), catches)

    output = {
        "schema": "udt-xmax-full-frame-verification-1.0",
        "python": sys.version.split()[0],
        "sympy": sp.__version__,
        "checks": checks,
        "catch_proofs": catches,
        "independent_witnesses": {
            "anchored_projective_coordinate": str(anchored),
            "Lie_derivative_K_g": "-2 g",
            "bounded_dx_time_ratio": str(time_ratio),
            "bounded_dx_spatial_ratios": [str(value) for value in samples],
            "free_time_exponent_common_factor": "exp(-2(a+1)beta)",
            "transverse_solution": "C*exp(phi)",
            "null_conformal_factor": str(factor),
            "absolute_seal_after_nonzero_shift": "-beta != 0",
        },
        "result": "PASS",
    }
    VERIFY.write_text(json.dumps(output, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
