#!/usr/bin/env python3
"""Independent coordinate-basis checks and fail-closed contract verification."""

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
BASE = "ec24c135212d3121e2d5903a29ec669f0b8a982a"
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


def normalized_script_body(path: Path) -> str:
    lines = path.read_text(encoding="utf-8").splitlines()
    require(lines and lines[0].startswith("Script started on "), "transcript header absent")
    require(lines[-1].startswith("Script done on ") and 'COMMAND_EXIT_CODE="0"' in lines[-1], "transcript footer/exit absent")
    body = lines[1:-1]
    while body and not body[0]:
        body.pop(0)
    while body and not body[-1]:
        body.pop()
    return "\n".join(body) + "\n"


def christoffel(metric: sp.Matrix, coordinates: list[sp.Symbol]):
    inverse = sp.simplify(metric.inv())
    dim = len(coordinates)
    return [[[
        sp.simplify(sum(
            inverse[i, ell] * (
                sp.diff(metric[ell, k], coordinates[j])
                + sp.diff(metric[ell, j], coordinates[k])
                - sp.diff(metric[j, k], coordinates[ell])
            ) for ell in range(dim)
        ) / 2)
        for k in range(dim)] for j in range(dim)] for i in range(dim)]


def riemann_up(connection, coordinates, i: int, j: int, k: int, ell: int):
    dim = len(coordinates)
    return sp.simplify(
        sp.diff(connection[i][j][ell], coordinates[k])
        - sp.diff(connection[i][j][k], coordinates[ell])
        + sum(
            connection[i][m][k] * connection[m][j][ell]
            - connection[i][m][ell] * connection[m][j][k]
            for m in range(dim)
        )
    )


def scalar_curvature_2d(metric: sp.Matrix, coordinates: list[sp.Symbol]):
    connection = christoffel(metric, coordinates)
    inverse = sp.simplify(metric.inv())
    scalar = 0
    for j in range(2):
        for ell in range(2):
            ricci = sum(riemann_up(connection, coordinates, i, j, i, ell) for i in range(2))
            scalar += inverse[j, ell] * ricci
    return sp.simplify(scalar)


def validate(data: dict) -> None:
    require(data["schema"] == "udt-metric-cartan-holonomy-audit-1.0", "derivation schema changed")
    require(all(value == "PASS" for value in data["checks"].values()), "algebra check failed")
    require(len(data["checks"]) == 50, "algebra-check census changed")
    twist = data["twisted_screen"]
    require(twist["classification"].startswith("EXACT_CHOSEN_EQUAL_BOUNDARY"), "chosen-boundary-equal twist conclusion lost")
    require(twist["bump_family"]["boundary_jets"] == "chosen comparison jets u=q=q_prime=0 at r=+-1 for every lambda", "boundary jets changed")
    require(twist["bump_family"]["midpoint_lambda_one"] == {"q": "-27/16", "q_prime": "9/8"}, "twist witness changed")
    axis = data["conditional_single_axis_challenge"]
    require(axis["pullback_area_F"] == "0", "rank-one area no longer zero")
    require(axis["C2_4"] == "3/4", "rank-one C2 witness changed")
    require(axis["gaussian_curvature"] == "(1 - a)*cos(2*x)/a", "general axis curvature changed")
    require(axis["K_nondiagonal"] == "-3/8", "non-diagonal axis witness changed")
    require(axis["classification"] == "CONDITIONAL_SINGLE_AXIS_CURVATURE_DIFFERENT_FROM_AREA_ONLY_F2", "chosen axis promoted or ordering invented")
    actions = data["curvature_action_comparison"]
    require(actions["C2_density_weight"] == "1" and actions["EH_density_weight"] == "s**2", "scale weights changed")
    adjudication = data["adjudication"]
    require(adjudication["holonomy_selector"] == "UNDERDETERMINED_NOT_SELECTED_BY_CURRENT_FOUNDATION", "holonomy promoted")
    require(adjudication["metric_holonomy_matter"].startswith("NOT_DERIVED"), "matter promoted")
    require(adjudication["C2_EH_bridge"].startswith("NOT_DERIVED"), "bridge promoted")
    require("NOT_CLAIMED_UNIQUE" in adjudication["route_scoped_missing_object"], "route-scoped gap promoted to unique missing object")


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
        [sys.executable, "-B", str(HERE / "derive_metric_cartan_holonomy.py")],
        cwd=ROOT, env=env, text=True, capture_output=True, timeout=180, check=False,
    )
    require(replay.returncode == 0, f"derivation replay failed: {replay.stderr}")
    require(not replay.stderr, "derivation replay emitted stderr")
    require(sha256(RESULT) == before, "derivation replay changed result bytes")
    require(normalized_script_body(HERE / "DERIVATION_TRANSCRIPT.txt") == replay.stdout, "derivation transcript is stale")
    data = json.loads(RESULT.read_text(encoding="utf-8"))
    validate(data)
    checks["deterministic_derivation_and_contract"] = "PASS"
    checks["derivation_transcript_matches_stdout"] = "PASS"

    # Independent coordinate-basis twist calculation.  This does not use the
    # exterior-form routines or spin connection in the derivation script.
    r, x, y, lam = sp.symbols("r x y lambda", real=True)
    u = lam * (1 - r**2) ** 3
    metric3 = sp.Matrix([[1, 0, 0], [0, 1 + u**2, u], [0, u, 1]])
    connection3 = christoffel(metric3, [r, x, y])
    component = sp.factor(riemann_up(connection3, [r, x, y], 1, 2, 1, 2))
    require(sp.simplify(component - sp.diff(u, r) ** 2 / 4) == 0, "coordinate twist curvature mismatch")
    interior = sp.simplify(component.subs({r: sp.Rational(1, 2), lam: 1}))
    require(interior == sp.Rational(729, 1024), "coordinate twist witness changed")
    for endpoint in (-1, 1):
        require(sp.simplify(u.subs(r, endpoint)) == 0, "twist boundary u mismatch")
        require(sp.simplify(sp.diff(u, r).subs(r, endpoint)) == 0, "twist boundary q mismatch")
        require(sp.simplify(sp.diff(u, r, 2).subs(r, endpoint)) == 0, "twist boundary q-prime mismatch")
    checks["independent_coordinate_twist"] = "PASS"

    # Independent Ricci-scalar route for the chosen-axis metric.
    a = sp.symbols("a", positive=True)
    vector = sp.Matrix([sp.cos(x), sp.sin(x)])
    axis_metric = sp.eye(2) + (a - 1) * vector * vector.T
    scalar2 = scalar_curvature_2d(axis_metric, [x, y])
    gaussian2 = sp.simplify(scalar2 / 2)
    require(sp.simplify(gaussian2 + (a - 1) * sp.cos(2 * x) / a) == 0, "independent general axis curvature mismatch")
    scalar_point = sp.simplify(scalar2.subs({x: 0, a: 4}))
    require(scalar_point == sp.Rational(-3, 2), "independent axis scalar mismatch")
    c2_point = sp.simplify(scalar_point**2 / 3)
    require(c2_point == sp.Rational(3, 4), "independent axis Weyl-square mismatch")
    require(sp.simplify(gaussian2.subs({x: sp.pi / 6, a: 4})) == sp.Rational(-3, 8), "independent non-diagonal axis mismatch")
    vector3 = sp.Matrix([sp.cos(x), sp.sin(x), 0])
    require(sp.simplify(vector3.dot(vector3.diff(x).cross(vector3.diff(y)))) == 0, "independent area mismatch")
    checks["independent_coordinate_axis_C2_vs_area"] = "PASS"

    # Independent dimensional count in d=4.
    dimension = 4
    sqrt_g_weight = dimension
    require(sqrt_g_weight - 2 == 2, "EH weight mismatch")
    require(sqrt_g_weight - 4 == 0, "C2 weight mismatch")
    checks["independent_constant_scale_count"] = "PASS"

    inventory_before = sha256(HERE / "SOURCE_INVENTORY.tsv")
    inventory_run = subprocess.run(
        [sys.executable, "-B", str(HERE / "build_source_inventory.py")],
        cwd=ROOT, env=env, text=True, capture_output=True, timeout=90, check=False,
    )
    require(inventory_run.returncode == 0, f"source inventory replay failed: {inventory_run.stderr}")
    require(sha256(HERE / "SOURCE_INVENTORY.tsv") == inventory_before, "source inventory replay changed bytes")
    sources = read_tsv(HERE / "SOURCE_INVENTORY.tsv")
    require(len(sources) == 21 and len({row["path"] for row in sources}) == 21, "source census mismatch")
    provisional = next(row for row in sources if row["source_class"] == "POST_JULY_PROVISIONAL_CANDIDATE")
    require(provisional["first_date"] >= "2026-07-01", "post-July candidate date misclassified")
    provisional_text = (ROOT / provisional["path"]).read_text(encoding="utf-8")
    require("PROVISIONAL CONDITIONAL DERIVATION; not banked and not canon" in provisional_text, "provisional grade absent")
    require("Independent verification | OPEN" in provisional_text, "open verification gate absent")
    correction = (HERE / "PREREGISTRATION_CORRECTION.md").read_text(encoding="utf-8")
    require("POST_JULY_PROVISIONAL_CANDIDATE" in correction, "preregistration correction absent")
    checks["source_inventory_replay_and_provenance_correction"] = "PASS"

    sectors = read_tsv(HERE / "CARTAN_SECTOR_LEDGER.tsv")
    statuses = read_tsv(HERE / "STATUS_LEDGER.tsv")
    require(len(sectors) == 15 and len({row["id"] for row in sectors}) == 15, "sector ledger mismatch")
    require(len(statuses) == 18 and len({row["id"] for row in statuses}) == 18, "status ledger mismatch")
    require(next(row for row in statuses if row["id"] == "S09")["status"] == "REFUTED_IN_TESTED_CLASS", "F2 shortcut status changed")
    require(next(row for row in statuses if row["id"] == "S17")["status"] == "NOT_AUTHORIZED_AND_NOT_YET_DIAGNOSTIC", "GPU gate changed")
    checks["ledger_coverage"] = "PASS"

    report = (HERE / "AUDIT_REPORT.md").read_text(encoding="utf-8")
    flat_report = " ".join(report.split())
    for phrase in (
        "it does not choose which complete metric the universe realizes",
        "Cartan geometry faithfully describes a chosen metric's local curvature and transport",
        "area-only `F^2` carrier functional is therefore false in this tested class",
        "Common origin is not a derived two-stage bridge",
        "route-scoped description, not a claim of uniqueness and not a new postulate",
        "GPU mapping is not indicated",
    ):
        require(phrase in flat_report, f"report disclosure missing: {phrase}")
    for forbidden in (
        "holonomy derives matter",
        "C^2 is exactly F^2",
        "Bianchi identities are the UDT field equations",
        "the two-stage bridge is derived",
    ):
        require(forbidden not in report, f"forbidden promotion present: {forbidden}")
    checks["report_contract"] = "PASS"

    adversarial = (HERE / "EXTERNAL_ADVERSARIAL_REVIEW.md").read_text(encoding="utf-8")
    flat_adversarial = " ".join(adversarial.lower().split())
    require("g_01 R^1_101" in adversarial, "adversarial off-diagonal bug disclosure absent")
    require("PASS after correction" in adversarial, "adversarial final verdict absent")
    require("does not establish different global holonomy groups" in flat_adversarial, "local/global holonomy scope absent")
    checks["fresh_adversarial_review_contract"] = "PASS"

    changed = subprocess.check_output(["git", "diff", "--name-only", BASE, "--"], cwd=ROOT, text=True).splitlines()
    forbidden_changes = {"LIVE.md", "HANDOFF.md", "INDEX.md", "README.md", "CANON.md", "MEMORY.md"}
    require(not forbidden_changes.intersection(changed), f"forbidden controls changed: {forbidden_changes.intersection(changed)}")
    checks["no_control_or_canon_edits"] = "PASS"

    mutation = copy.deepcopy(data)
    mutation["adjudication"]["holonomy_selector"] = "DERIVED_UNIQUE"
    expect_failure("holonomy_selector_promoted", lambda: validate(mutation), catches)
    mutation = copy.deepcopy(data)
    mutation["adjudication"]["metric_holonomy_matter"] = "DERIVED"
    expect_failure("holonomy_called_matter", lambda: validate(mutation), catches)
    mutation = copy.deepcopy(data)
    mutation["conditional_single_axis_challenge"]["C2_4"] = "0"
    expect_failure("rank_one_C2_deleted", lambda: validate(mutation), catches)
    mutation = copy.deepcopy(data)
    mutation["conditional_single_axis_challenge"]["pullback_area_F"] = "nonzero"
    expect_failure("rank_one_area_changed", lambda: validate(mutation), catches)
    mutation = copy.deepcopy(data)
    mutation["twisted_screen"]["bump_family"]["boundary_jets"] = "unspecified"
    expect_failure("twist_boundary_equivalence_deleted", lambda: validate(mutation), catches)
    mutation = copy.deepcopy(data)
    mutation["curvature_action_comparison"]["EH_density_weight"] = "1"
    expect_failure("EH_C2_identity_invented", lambda: validate(mutation), catches)
    mutation = copy.deepcopy(data)
    mutation["conditional_single_axis_challenge"]["classification"] = "NATIVE_CARRIER"
    expect_failure("chosen_axis_promoted", lambda: validate(mutation), catches)
    mutation = copy.deepcopy(data)
    mutation["conditional_single_axis_challenge"]["gaussian_curvature"] = "wrong_off_diagonal_lowering"
    expect_failure("off_diagonal_curvature_lowering_omitted", lambda: validate(mutation), catches)
    mutation = copy.deepcopy(data)
    mutation["twisted_screen"]["classification"] = "UNIQUE_GLOBAL_HOLONOMY_GROUP_SELECTED"
    expect_failure("local_transport_promoted_to_global_holonomy_group", lambda: validate(mutation), catches)
    mutation = copy.deepcopy(data)
    mutation["adjudication"]["route_scoped_missing_object"] = "THE_UNIQUE_MISSING_UDT_OBJECT"
    expect_failure("route_scoped_gap_promoted_to_unique", lambda: validate(mutation), catches)

    output = {
        "schema": "udt-metric-cartan-holonomy-verification-1.0",
        "python": sys.version.split()[0],
        "sympy": sp.__version__,
        "checks": checks,
        "catch_proofs": catches,
        "independent_witnesses": {
            "twist_R_up_x_yxy_at_midpoint": str(interior),
            "axis_R_at_x0_a4": str(scalar_point),
            "axis_C2_at_x0_a4": str(c2_point),
            "axis_K_at_xpi6_a4": str(gaussian2.subs({x: sp.pi / 6, a: 4})),
        },
        "result": "PASS",
    }
    VERIFY.write_text(json.dumps(output, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
