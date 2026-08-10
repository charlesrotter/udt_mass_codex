#!/usr/bin/env python3
"""Fail-closed verification and mutation catches for the complete R17 connection audit."""

from __future__ import annotations

import csv
import hashlib
import json
import subprocess
import sys
from copy import deepcopy
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
LANDING = "COMPLETE_METRIC_PROJECTED_H_CONNECTION_AND_PATH_FUNCTOR_DERIVED_ON_SUPPLIED_REGULAR_STATIONARY_R17__FULL_CURVATURE_GENERALLY_NONZERO__PATH_SELECTION_AND_PHYSICAL_ARROW_OPEN"
EXTERNAL_RECEIVED_SHA256 = "c0f5b6a8c277081d37d1212e93124f9adde9ed364da068eb376a94a99e12b685"
EXTERNAL_COMMITTED_SHA256 = "395c069f60b0f1d4018a2080e9ecb7bb12b4efbbdb6b167064a80f0b6dff0213"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def table(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream, delimiter="\t"))


def verify_sources(rows: list[dict[str, str]]) -> bool:
    require(len(rows) == 14, "source count")
    require(len({row["source_id"] for row in rows}) == 14, "source ids")
    require(len({row["path"] for row in rows}) == 14, "source paths")
    for row in rows:
        data = subprocess.check_output(["git", "show", row["source_ref"]], cwd=ROOT)
        require(digest(data) == row["sha256"], f"source sha: {row['path']}")
        require(str(len(data)) == row["size"], f"source size: {row['path']}")
        blob = subprocess.check_output(["git", "rev-parse", row["source_ref"]], cwd=ROOT, text=True).strip()
        require(blob == row["git_blob"], f"source blob: {row['path']}")
    return True


def verify_controller_source(source: str) -> bool:
    for token in (
        "frame = sp.Matrix",
        "coframe = sp.simplify(frame.inv())",
        "def frame_bracket",
        "def gamma",
        "connection = [gamma(direction, 2, 3)",
        "for left in range(4)",
        "vertical_contractions =",
    ):
        require(token in source, f"derivation token missing: {token}")
    return True


def expr(text: str, symbols: dict[str, sp.Symbol]) -> sp.Expr:
    return sp.sympify(text.replace("lambda", "lam"), locals=symbols)


def verify_production(state: dict) -> bool:
    phi, lam, a, p1, p2, p3 = sp.symbols("phi lam a p1 p2 p3", real=True)
    q21, q31, q22, q33 = sp.symbols("q21 q31 q22 q33", real=True)
    u, v = sp.exp(phi), sp.exp(lam * phi)
    symbols = {value.name: value for value in (phi, lam, a, p1, p2, p3, q21, q31, q22, q33)}
    expected_A = [a / (u * v**2), 2 / u - u / v**2, -lam * p3 / v, lam * p2 / v]
    expected_F = {
        "F_01": 2 * a * (1 + lam) * p1 / (u**2 * v**2),
        "F_02": 2 * a * (1 + lam) * p2 / (u * v**3),
        "F_03": 2 * a * (1 + lam) * p3 / (u * v**3),
        "F_12": 2 * (1 - lam) * p2 * u / v**3 - lam * q31 / (u * v),
        "F_13": 2 * (1 - lam) * p3 * u / v**3 + lam * q21 / (u * v),
        "F_23": lam * (q22 + q33) / v**2 + 2 * u**2 / v**4 - 4 / v**2 - 2 * a**2 / (u**2 * v**4),
    }
    require(state["landing"] == LANDING, "landing")
    require(all(state["checks"].values()), "production checks")
    require(len(state["connection_mc_plus"]) == 4, "connection count")
    for actual, expected in zip(state["connection_mc_plus"], expected_A):
        require(sp.simplify(expr(actual, symbols) - expected) == 0, "connection expression")
    require(set(state["curvature_mc_plus"]) == set(expected_F), "curvature keys")
    for key, expected in expected_F.items():
        require(sp.simplify(expr(state["curvature_mc_plus"][key], symbols) - expected) == 0, f"curvature {key}")
    require(state["path_transport"]["base_path_selected"] is False, "base path selected")
    require(state["selected_lambda"] is None and state["selected_leaf"] is None and state["selected_path"] is None, "selection")
    require(state["physical_observer_arrow_derived"] is False, "physical arrow")
    require(not any(state["scope_guards"].values()), "scope promotion")
    return True


def verify_independent(state: dict) -> bool:
    require(state["mode"] == "standard_library_fraction_second_jet_constructive", "independent mode")
    require(state["imports_production_controller"] is False and state["imports_sympy"] is False, "false independence")
    require(state["assigns_connection_or_curvature"] is False, "assigned result")
    require(state["derives_frame_by_gauss_jordan"] is True, "frame derivation")
    require(state["derives_all_curvature_planes_by_exterior_derivative"] is True, "curvature derivation")
    require(state["compatible_noncommuting_second_jets"] is True, "jet compatibility")
    require(state["lambda_strata"] == 6 and state["maurer_cartan_signs"] == 2, "arena")
    require(len(state["witnesses"]) == 12, "witness count")
    require(all(all(row["checks"].values()) for row in state["witnesses"]), "witness failure")
    require(state["aggregate_atomic_checks"] == 300, "atomic check count")
    return True


def verify_atlas(rows: list[dict[str, str]]) -> bool:
    require(len(rows) == 6, "lambda rows")
    require([row["lambda"] for row in rows] == ["-2", "-1", "0", "1/2", "1", "2"], "lambda set")
    require(rows[1]["identically_zero_curvature_components"] == "F_01;F_02;F_03", "lambda -1 role")
    require(rows[1]["complete_curvature_identically_zero"] == "NO", "lambda -1 promoted")
    require(rows[2]["normal_frame_horizontal_A2_A3_zero"] == "YES", "lambda zero role")
    require(rows[2]["base_metric_hopf_basic_for_arbitrary_stationary_phi"] == "YES", "lambda zero basic")
    require(rows[4]["ruler_screen_first_gradient_terms_zero"] == "YES", "lambda one role")
    require(all(row["base_curvature_horizontal_for_arbitrary_stationary_phi"] == "NO" for row in rows), "base descent promoted")
    require(all(row["selected"] == "NO" for row in rows), "lambda selected")
    return True


def verify_global(rows: list[dict[str, str]]) -> bool:
    by_id = {row["item_id"]: row for row in rows}
    require(len(rows) == len(by_id) == 13, "global atlas")
    require(by_id["G03"]["status"] == "DERIVED_CONDITIONAL_QUERY", "horizontal lift ownership")
    require(by_id["G05"]["status"] == "DERIVED_CONDITIONAL_QUERY", "path functor ownership")
    require(by_id["G08"]["status"] == "REFUTED_IN_GENERIC_JET_SPACE", "lambda -1 full flatness")
    require(by_id["G09"]["status"] == "REFUTED_IN_GENERIC_JET_SPACE", "lambda zero descent")
    require(by_id["G10"]["status"] == "NONE", "generic descent")
    require(by_id["G13"]["status"] == "OPEN", "physical arrow promoted")
    return True


def verify_path(state: dict) -> bool:
    require(state["passed_checks"] == 7 and all(state["checks"].values()), "path checks")
    require(state["base_path_selected"] is False and state["physical_arrow_derived"] is False, "path promoted")
    return True


def verify_external_review() -> bool:
    raw = (HERE / "EXTERNAL_REVIEW_RAW.md").read_bytes()
    require(digest(raw) == EXTERNAL_COMMITTED_SHA256, "external raw review committed hash")
    require(digest(raw[:-1]) == EXTERNAL_RECEIVED_SHA256 and raw.endswith(b"\n"), "external terminal-LF normalization")
    text = raw.decode("utf-8")
    require("`VERIFIED_AS_STATED`" in text, "external verdict")
    require("Exact objections: none." in text, "external objections")
    require("not the physical non-isometric observer arrow" in text, "external scope guard")
    return True


def rejected(callable_) -> bool:
    try:
        callable_()
    except (ValueError, KeyError):
        return True
    return False


def run(command: list[str], label: str) -> dict[str, object]:
    result = subprocess.run(command, cwd=ROOT, capture_output=True, check=False, timeout=120)
    (HERE / f"{label}.stdout").write_bytes(result.stdout)
    (HERE / f"{label}.stderr").write_bytes(result.stderr)
    return {"label": label, "command": " ".join(command), "exit_code": result.returncode, "stdout_sha256": digest(result.stdout), "stderr_sha256": digest(result.stderr)}


def main() -> None:
    commands = [
        run([sys.executable, "--version"], "RUN_PYTHON_VERSION"),
        run([sys.executable, "-c", "import sympy; print(sympy.__version__)"], "RUN_SYMPY_VERSION"),
        run([sys.executable, str(HERE / "derive_path_labelled_connection.py")], "RUN_PRODUCTION"),
        run([sys.executable, str(HERE / "verify_connection_independent.py")], "RUN_INDEPENDENT"),
        run([sys.executable, str(HERE / "verify_path_functor.py")], "RUN_PATH_FUNCTOR"),
    ]
    require(all(row["exit_code"] == 0 for row in commands), "command failed")
    with (HERE / "COMMAND_TRANSCRIPT.tsv").open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(commands[0]), delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(commands)

    sources = table(HERE / "SOURCE_MANIFEST.tsv")
    atlas = table(HERE / "LAMBDA_CONNECTION_ATLAS.tsv")
    global_rows = table(HERE / "GLOBAL_COMPATIBILITY_ATLAS.tsv")
    production = json.loads((HERE / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    independent = json.loads((HERE / "INDEPENDENT_VERIFICATION_RESULT.json").read_text(encoding="utf-8"))
    path_state = json.loads((HERE / "PATH_FUNCTOR_RESULT.json").read_text(encoding="utf-8"))
    controller = (HERE / "derive_path_labelled_connection.py").read_text(encoding="utf-8")

    verify_sources(sources)
    verify_controller_source(controller)
    verify_production(production)
    verify_independent(independent)
    verify_atlas(atlas)
    verify_global(global_rows)
    verify_path(path_state)
    verify_external_review()

    catches: list[tuple[str, str, bool]] = []

    def add(cid: str, target: str, mutant) -> None:
        catches.append((cid, target, rejected(mutant)))

    add("F01", "remove derived Koszul connection", lambda: verify_controller_source(controller.replace("def gamma", "def removed")))

    def mutate_curvature(key: str):
        altered = deepcopy(production)
        altered["curvature_mc_plus"][key] = "0"
        return lambda: verify_production(altered)

    add("F02", "wrong banked F01", mutate_curvature("F_01"))
    add("F03", "erase mixed F12", mutate_curvature("F_12"))
    add("F04", "erase horizontal F23", mutate_curvature("F_23"))
    bad_checks = deepcopy(production)
    bad_checks["checks"]["compatible_scalar_jet_relations_used"] = False
    add("F05", "use incompatible scalar jets", lambda: verify_production(bad_checks))
    bad_metric = deepcopy(production)
    bad_metric["checks"]["projected_connection_metric"] = False
    add("F06", "break metricity", lambda: verify_production(bad_metric))
    bad_path = deepcopy(path_state)
    bad_path["checks"]["composition"] = False
    add("F07", "break path composition", lambda: verify_path(bad_path))
    altered_global = deepcopy(global_rows)
    next(row for row in altered_global if row["item_id"] == "G08")["status"] = "DERIVED_FULL_FLAT"
    add("F08", "promote lambda -1 to full flatness", lambda: verify_global(altered_global))
    bad_lift = deepcopy(global_rows)
    next(row for row in bad_lift if row["item_id"] == "G03")["status"] = "DERIVED_PATH_SELECTION"
    add("F09", "horizontal lift selects path", lambda: verify_global(bad_lift))
    bad_atlas = deepcopy(atlas)
    bad_atlas[1]["selected"] = "YES"
    add("F10", "select lambda", lambda: verify_atlas(bad_atlas))

    def promote(name: str):
        altered = deepcopy(production)
        altered["scope_guards"][name] = True
        return lambda: verify_production(altered)

    add("F11", "signed angle called O2 invariant", promote("signed_angle_called_O2_invariant"))
    add("F12", "conflate ambient Lorentz holonomy", promote("ambient_Lorentz_holonomy_conflated"))
    add("F13", "promote projected connection to physical arrow", promote("projected_connection_called_physical_arrow"))
    bad_descent = deepcopy(global_rows)
    next(row for row in bad_descent if row["item_id"] == "G09")["status"] = "DERIVED_BASE_DESCENT"
    add("F14", "promote lambda zero base descent", lambda: verify_global(bad_descent))
    add("F15", "generalize bounded result", promote("one_lambda_or_leaf_selected"))
    add("F16", "infer downstream physics", promote("downstream_physics_inferred"))
    bad_independent = deepcopy(independent)
    bad_independent["assigns_connection_or_curvature"] = True
    add("F17", "independent verifier assigns formulas", lambda: verify_independent(bad_independent))
    add("F18", "drop a frozen source", lambda: verify_sources(sources[:-1]))

    require(all(passed for _, _, passed in catches), "catch failure")
    with (HERE / "CATCH_PROOFS.tsv").open("w", newline="", encoding="utf-8") as stream:
        writer = csv.writer(stream, delimiter="\t", lineterminator="\n")
        writer.writerow(["catch_id", "mutant", "expected", "observed"])
        for cid, target, passed in catches:
            writer.writerow([cid, target, "REJECT", "REJECT" if passed else "ACCEPT"])

    result = {
        "schema": "udt-r17-path-labelled-connection-verification-v1",
        "status": "PASS",
        "landing": LANDING,
        "source_manifest_rows": len(sources),
        "production_checks": sum(production["checks"].values()),
        "independent_atomic_checks": independent["aggregate_atomic_checks"],
        "path_functor_checks": path_state["passed_checks"],
        "mutation_catches": len(catches),
        "lambda_strata": len(atlas),
        "external_adversarial_review": "VERIFIED_AS_STATED",
        "external_review_received_sha256": EXTERNAL_RECEIVED_SHA256,
        "external_review_committed_sha256": EXTERNAL_COMMITTED_SHA256,
    }
    (HERE / "VERIFICATION_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print("PASS: 14 sources; 10 production; 300 independent; 7 path; 18/18 catches; external VERIFIED_AS_STATED")


if __name__ == "__main__":
    main()
