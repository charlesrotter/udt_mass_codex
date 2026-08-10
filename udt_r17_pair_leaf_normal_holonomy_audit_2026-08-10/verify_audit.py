#!/usr/bin/env python3
"""Fail-closed verification and exercised mutations for the R17 normal audit."""

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
LANDING = (
    "CONDITIONAL_METRIC_OWNED_NORMAL_CONNECTION_AND_REPRESENTATIVE_FREE_"
    "HOLONOMY_DATA_ON_SUPPLIED_R17_PAIR_LEAVES__PHYSICAL_PATH_AND_COMPLETE_ARROW_OPEN"
)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def load_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream, delimiter="\t"))


def verify_sources(rows: list[dict[str, str]]) -> bool:
    require(len(rows) == 12, "source count")
    require(len({row["source_id"] for row in rows}) == 12, "source ids")
    require(len({row["path"] for row in rows}) == 12, "source paths")
    for row in rows:
        data = subprocess.check_output(["git", "show", row["source_ref"]], cwd=ROOT)
        require(digest(data) == row["sha256"], f"source sha: {row['path']}")
        require(str(len(data)) == row["size"], f"source size: {row['path']}")
        blob = subprocess.check_output(
            ["git", "rev-parse", row["source_ref"]], cwd=ROOT, text=True
        ).strip()
        require(blob == row["git_blob"], f"source blob: {row['path']}")
    return True


def verify_controller_source(source: str) -> bool:
    for token in (
        "frame = sp.Matrix",
        "coframe = sp.simplify(frame.inv())",
        "def frame_bracket",
        "def gamma",
        "normal = [gamma(direction, 2, 3)",
        "curvature_01 = sp.simplify",
    ):
        require(token in source, f"derivation token missing: {token}")
    return True


def same_expression(actual: str, expected: sp.Expr) -> bool:
    local_symbols = {symbol.name: symbol for symbol in expected.free_symbols}
    if "lambda" in local_symbols:
        local_symbols["lam"] = local_symbols.pop("lambda")
        actual = actual.replace("lambda", "lam")
    return sp.simplify(sp.sympify(actual, locals=local_symbols) - expected) == 0


def verify_production(state: dict) -> bool:
    phi, lam, a, p1 = sp.symbols("phi lambda a p1", real=True)
    u = sp.exp(phi)
    v = sp.exp(lam * phi)
    plus = state["expressions_mc_plus"]
    minus = state["expressions_mc_minus"]
    expected = {
        "A_e0": a / (u * v**2),
        "A_e1": 2 / u - u / v**2,
        "F_e0e1": 2 * a * (1 + lam) * p1 / (u**2 * v**2),
        "A_T": a / (u**2 * v**2),
        "A_Z": 2 - u**2 / v**2 + a**2 / (u**2 * v**2),
    }
    require(state["landing"] == LANDING, "landing")
    require(all(state["checks"].values()), "production checks")
    for key, expression in expected.items():
        require(same_expression(plus[key], expression), f"plus expression: {key}")
        require(same_expression(minus[key], -expression), f"minus expression: {key}")
    require(state["leaf_topology"] == "R_x_S1", "leaf topology")
    require("curvature_flux" in state["winding_holonomy_rule"], "winding/flux split")
    require(state["orientation_free_holonomy_character"] == "trace(Hol)=2*cos(Theta)", "O2 invariant")
    require(state["selected_lambda"] is None, "lambda selected")
    require(state["selected_leaf"] is None, "leaf selected")
    require(state["selected_path"] is None, "path selected")
    require(state["physical_observer_arrow_derived"] is False, "physical arrow promoted")
    require(not any(state["scope_guards"].values()), "scope promotion")
    return True


def verify_atlas(rows: list[dict[str, str]]) -> bool:
    require(len(rows) == 6, "lambda row count")
    require([row["lambda"] for row in rows] == ["-2", "-1", "0", "1/2", "1", "2"], "lambda arena")
    require(rows[1]["generic_curvature_class"] == "FLAT_FOR_ALL_STATIONARY_PHI", "lambda -1 flat")
    require(all(row["selected"] == "NO" for row in rows), "lambda selection")
    for index, row in enumerate(rows):
        if index != 1:
            require(row["generic_curvature_class"] == "CURVED_WHERE_A_P1_NONZERO", "generic curvature")
    require(rows[2]["quotient_screen_metric_basic_condition"] == "YES_ALL_PHI", "lambda zero basic")
    return True


def verify_holonomy(rows: list[dict[str, str]]) -> bool:
    require(len(rows) == 7, "holonomy classes")
    by_id = {row["class_id"]: row for row in rows}
    require(by_id["H02"]["contractible_loop"] == "TRIVIAL", "flat contractible")
    require(by_id["H02"]["wound_loop"] == "POTENTIALLY_NONTRIVIAL_PI1_CHARACTER", "winding erased")
    require(by_id["H06"]["representative_free_datum"] == "TRACE_OR_CONJUGACY_UNCHANGED", "reflection invariant")
    require(by_id["H07"]["status"] == "OPEN", "cross-leaf path promoted")
    return True


def verify_independent(state: dict) -> bool:
    require(state["mode"] == "standard_library_fraction_dual_constructive", "independent mode")
    require(state["imports_production_controller"] is False, "false independence")
    require(state["assigns_connection_or_curvature"] is False, "assigned formulas")
    require(state["derives_frame_by_gauss_jordan"] is True, "frame derivation")
    require(state["derives_frame_derivative_by_inverse_identity"] is True, "frame derivative")
    require(state["derives_connection_by_koszul"] is True, "connection derivation")
    require(state["derives_curvature_by_exterior_derivative"] is True, "curvature derivation")
    require(state["arbitrary_second_jets_exercised"] is True, "second-jet control")
    require(state["lambda_strata"] == 6, "independent lambdas")
    require(state["maurer_cartan_sign_conventions"] == 2, "independent MC signs")
    require(len(state["witnesses"]) == 12, "independent witnesses")
    require(state["passed_checks"] == 72, "independent check count")
    require(all(all(w["checks"].values()) for w in state["witnesses"]), "independent witness")
    return True


def rejected(callable_) -> bool:
    try:
        callable_()
    except (ValueError, KeyError):
        return True
    return False


def run_and_record(command: list[str], label: str) -> dict[str, object]:
    result = subprocess.run(command, cwd=ROOT, capture_output=True, check=False, timeout=120)
    (HERE / f"{label}.stdout").write_bytes(result.stdout)
    (HERE / f"{label}.stderr").write_bytes(result.stderr)
    return {
        "label": label,
        "command": " ".join(command),
        "exit_code": result.returncode,
        "stdout_sha256": digest(result.stdout),
        "stderr_sha256": digest(result.stderr),
    }


def main() -> None:
    commands = [
        run_and_record([sys.executable, "--version"], "RUN_PYTHON_VERSION"),
        run_and_record(
            [sys.executable, "-c", "import sympy; print(sympy.__version__)"],
            "RUN_SYMPY_VERSION",
        ),
        run_and_record([sys.executable, str(HERE / "derive_normal_holonomy.py")], "RUN_PRODUCTION"),
        run_and_record([sys.executable, str(HERE / "verify_normal_holonomy_independent.py")], "RUN_INDEPENDENT"),
    ]
    require(all(row["exit_code"] == 0 for row in commands), "calculation command failed")
    with (HERE / "COMMAND_TRANSCRIPT.tsv").open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(commands[0]), delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(commands)

    sources = load_tsv(HERE / "SOURCE_MANIFEST.tsv")
    atlas = load_tsv(HERE / "LAMBDA_STRATUM_ATLAS.tsv")
    holonomy = load_tsv(HERE / "HOLONOMY_CLASSIFICATION.tsv")
    production = json.loads((HERE / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    independent = json.loads((HERE / "INDEPENDENT_VERIFICATION_RESULT.json").read_text(encoding="utf-8"))
    controller_source = (HERE / "derive_normal_holonomy.py").read_text(encoding="utf-8")

    verify_sources(sources)
    verify_controller_source(controller_source)
    verify_production(production)
    verify_atlas(atlas)
    verify_holonomy(holonomy)
    verify_independent(independent)

    catches: list[tuple[str, str, bool]] = []

    def add(cid: str, target: str, mutant) -> None:
        catches.append((cid, target, rejected(mutant)))

    add("F01", "connection assigned / derivation removed", lambda: verify_controller_source(controller_source.replace("def gamma", "def removed")))

    def mutate_expression(key: str, replacement: str):
        altered = deepcopy(production)
        altered["expressions_mc_plus"][key] = replacement
        return lambda: verify_production(altered)

    add("F02", "wrong clock connection", mutate_expression("A_e0", "0"))
    add("F03", "wrong ruler connection", mutate_expression("A_e1", "0"))
    add("F04", "wrong curvature", mutate_expression("F_e0e1", "0"))

    def mutate_atlas(row: int, key: str, value: str):
        altered = deepcopy(atlas)
        altered[row][key] = value
        return lambda: verify_atlas(altered)

    add("F05", "erase lambda -1 flat stratum", mutate_atlas(1, "generic_curvature_class", "CURVED_WHERE_A_P1_NONZERO"))
    add("F06", "call generic curvature zero", mutate_atlas(0, "generic_curvature_class", "FLAT_FOR_ALL_STATIONARY_PHI"))

    def mutate_holonomy(row_id: str, key: str, value: str):
        altered = deepcopy(holonomy)
        next(row for row in altered if row["class_id"] == row_id)[key] = value
        return lambda: verify_holonomy(altered)

    add("F07", "erase winding holonomy", mutate_holonomy("H02", "wound_loop", "TRIVIAL"))
    add("F08", "call signed reflection angle invariant", mutate_holonomy("H06", "representative_free_datum", "SIGNED_ANGLE_UNCHANGED"))

    def promote(name: str):
        altered = deepcopy(production)
        altered["scope_guards"][name] = True
        return lambda: verify_production(altered)

    add("F09", "conflate ambient and normal holonomy", promote("ambient_Lorentz_holonomy_called_normal_SO2_holonomy"))
    add("F10", "select one leaf", promote("one_leaf_selected"))
    add("F11", "select one lambda", promote("one_lambda_selected"))
    add("F12", "call cross-leaf path unique", promote("cross_leaf_path_called_unique"))
    add("F13", "promote projected connection to physical arrow", promote("projected_connection_called_physical_observer_arrow"))
    add("F14", "infer downstream physics", promote("downstream_physics_inferred"))

    bad_independent = deepcopy(independent)
    bad_independent["assigns_connection_or_curvature"] = True
    add("F15", "independent verifier assigns result", lambda: verify_independent(bad_independent))
    add("F16", "missing source", lambda: verify_sources(sources[:-1]))

    require(all(passed for _, _, passed in catches), "mutation catch failure")
    with (HERE / "CATCH_PROOFS.tsv").open("w", newline="", encoding="utf-8") as stream:
        writer = csv.writer(stream, delimiter="\t", lineterminator="\n")
        writer.writerow(["catch_id", "mutant", "expected", "observed"])
        for cid, target, passed in catches:
            writer.writerow([cid, target, "REJECT", "REJECT" if passed else "ACCEPT"])

    result = {
        "schema": "udt-r17-pair-leaf-normal-holonomy-verification-v1",
        "status": "PASS",
        "landing": LANDING,
        "source_manifest_rows": len(sources),
        "production_checks": sum(production["checks"].values()),
        "independent_checks": independent["passed_checks"],
        "mutation_catches": len(catches),
        "lambda_strata": len(atlas),
        "external_adversarial_review": "PENDING",
    }
    (HERE / "VERIFICATION_RESULT.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print("PASS: 12 sources; 10 symbolic; 72 independent; 16/16 catches; external review pending")


if __name__ == "__main__":
    main()
