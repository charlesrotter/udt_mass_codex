#!/usr/bin/env python3
"""Fail-closed semantic and mutation verifier for intrinsic contact descent."""

from __future__ import annotations

import copy
import csv
import json
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent


class GateError(AssertionError):
    pass


def table(name: str) -> list[dict[str, str]]:
    with (HERE / name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def state_from_disk() -> dict:
    return {
        "result": json.loads((HERE / "DERIVATION_RESULT.json").read_text(encoding="utf-8")),
        "lambda": {row["lambda"]: row for row in table("LAMBDA_CERTIFICATE.tsv")},
        "controls": {row["control"]: row for row in table("CONTROL_OUTCOMES.tsv")},
        "atlas": {row["object_id"]: row for row in table("DESCENT_ATLAS.tsv")},
    }


def require(condition: bool, message: str) -> None:
    if not condition:
        raise GateError(message)


def equivalent(raw: str, expected: sp.Expr, u: sp.Symbol) -> bool:
    return sp.simplify(sp.sympify(raw, locals={"u": u}) - expected) == 0


def validate(state: dict) -> None:
    result = state["result"]
    lambdas = state["lambda"]
    controls = state["controls"]
    atlas = state["atlas"]
    u = sp.symbols("u", positive=True)

    require(result["objects_classified"] == len(atlas) == 22, "object census")
    require(set(lambdas) == {"-1", "0", "1"}, "lambda census")
    require(result["registered_lambda_values"] == [-1, 0, 1], "lambda order")
    for key in ("T_SIGN", "S_SIGN", "SCREEN_ORIENTATION", "K_CONSTANT_RESCALE", "FULL_FRAME_COVARIANCE"):
        require(controls[key]["result"] == "PASS", key)
    require(controls["NAIVE_SLOT_RELABEL"]["result"] == "REJECTED_AS_REQUIRED", "naive slot")
    require(controls["CONSTANT_DEPTH"]["result"] == "AUTHORITY_BLOCKED", "constant control")
    require(controls["TWIST_FREE"]["result"] == "PAIR_UNDEFINED", "twist control")
    require(controls["SLICE_NULL"]["result"] == "INELIGIBLE_RETAINED", "slice-null control")

    for raw_lam, row in lambdas.items():
        lam = int(raw_lam)
        qt = 4 * u ** (-1 - 2 * lam)
        qs = 4 * u ** (1 - 2 * lam)
        q = sp.factor(qs - qt)
        require(equivalent(row["Q_T"], qt, u), f"QT {lam}")
        require(equivalent(row["Q_S"], qs, u), f"QS {lam}")
        require(equivalent(row["Q"], q, u), f"Q {lam}")
        require(row["dphi_reconstruction_coefficient"] == "1", f"dphi {lam}")
        require(row["dsigma_reconstruction_coefficient"] == str(2 * lam), f"dsigma {lam}")
        require(sp.Rational(row["Q_min"]) > 0, f"positive minimum {lam}")
        require(row["realized_stratum"] == "Q_POSITIVE_ONLY", f"stratum {lam}")

    required_status = {
        "O07": "METRIC_SCALAR_ON_WITNESS",
        "O08": "METRIC_SCALAR_ON_WITNESS",
        "O09": "METRIC_SCALAR_ON_WITNESS",
        "O10": "Q_POSITIVE_ONLY_ON_WITNESS",
        "O11": "METRIC_ONE_FORM_ON_WITNESS",
        "O12": "METRIC_ONE_FORM_ON_WITNESS",
        "O13": "PHI_CONTACT_METRIC_SCALAR_ON_FROZEN_UNIT_WITNESS__SIGMA_REFERENCE_DEPENDENT",
        "O14": "REFERENCE_DEPENDENT_ABSOLUTE_DZ_INTRINSIC",
        "O16": "AVAILABLE_REFERENCE_DEPENDENT_NOT_SELECTED",
        "O18": "SCREEN_O2_GAUGE_NOT_SELECTED",
        "O20": "CONNECTION_GAUGE_NOT_TENSOR",
        "O21": "PATH_DEPENDENT_NOT_FIXED_BY_LOCAL_DESCENT",
        "O22": "NOT_DERIVED_ADDITIONAL_GLOBAL_DATA",
    }
    for object_id, status in required_status.items():
        require(atlas[object_id]["status"] == status, object_id)
    require(atlas["O09"]["exact_scope"] == "Q_S minus Q_T", "tensorial Q definition")
    require(
        atlas["O13"]["exact_scope"]
        == "phi_contact=one_quarter_log_QS_over_QT_equals_phi;absolute_sigma_needs_dimensionful_reference",
        "O13 phi/sigma split",
    )

    require(result["realized_contact_stratum"] == "Q_POSITIVE_ONLY", "result stratum")
    require(result["null_contact_points"] == result["negative_contact_points"] == 0, "absent strata")
    require(result["contact_two_form_on_witness"] == "IDENTICALLY_ZERO", "contact collapse")
    require(result["O13_subclassifications"] == 2, "O13 subclassification count")
    require(
        result["Phi_contact"]
        == "ABSOLUTE_METRIC_SCALAR_EQUALS_PHI_ON_FROZEN_a_EQUALS_R_EQUALS_ONE_WITNESS",
        "absolute contact phi",
    )
    require(result["absolute_sigma"] == "REFERENCE_DEPENDENT__DSIGMA_INTRINSIC", "absolute sigma")
    require(result["naive_slot_relabel_rejected"] is True, "slot guard")
    require(result["full_GL2_generality_claimed"] is False, "GL2 scope")
    require(result["on_shell_claimed"] is False, "on-shell scope")
    require(result["universal_claimed"] is False, "universal scope")
    require(result["physics_promoted"] is False, "physics scope")


def mutate_control(name: str, value: str):
    def mutation(state: dict) -> None:
        state["controls"][name]["result"] = value
    return mutation


def mutate_lambda(lam: str, field: str, value: str):
    def mutation(state: dict) -> None:
        state["lambda"][lam][field] = value
    return mutation


def mutate_atlas(object_id: str, field: str, value: str):
    def mutation(state: dict) -> None:
        state["atlas"][object_id][field] = value
    return mutation


def mutate_result(field: str, value):
    def mutation(state: dict) -> None:
        state["result"][field] = value
    return mutation


def main() -> int:
    base = state_from_disk()
    validate(base)
    mutations = {
        "F01": mutate_control("T_SIGN", "FAIL"),
        "F02": mutate_control("S_SIGN", "FAIL"),
        "F03": mutate_control("SCREEN_ORIENTATION", "FAIL"),
        "F04": mutate_control("K_CONSTANT_RESCALE", "FAIL"),
        "F05": mutate_control("FULL_FRAME_COVARIANCE", "FAIL"),
        "F06": mutate_control("NAIVE_SLOT_RELABEL", "PASS"),
        "F07": mutate_lambda("0", "Q_T", "5/u"),
        "F08": mutate_lambda("0", "Q_S", "5*u"),
        "F09": mutate_lambda("0", "Q", "4*u"),
        "F10": mutate_lambda("0", "dphi_reconstruction_coefficient", "0"),
        "F11": mutate_lambda("1", "dsigma_reconstruction_coefficient", "0"),
        "F12": mutate_lambda("1", "Q_min", "0"),
        "F13": mutate_control("CONSTANT_DEPTH", "METRIC_INTRINSIC_PAIR"),
        "F14": mutate_control("TWIST_FREE", "PAIR_DERIVED"),
        "F15": mutate_control("SLICE_NULL", "PROMOTED"),
        "F16": mutate_atlas("O14", "status", "REFERENCE_INDEPENDENT_METRIC_SCALAR"),
        "F17": mutate_atlas("O16", "status", "UNIQUE_SELECTED_PRIMITIVE"),
        "F18": mutate_atlas("O20", "status", "METRIC_SCALAR"),
        "F19": mutate_atlas("O21", "status", "LOCAL_PROJECTOR_FIXES_HOLONOMY"),
        "F20": mutate_result("full_GL2_generality_claimed", True),
        "F21": mutate_result("universal_claimed", True),
        "F22": mutate_result("physics_promoted", True),
        "F23": mutate_result("contact_two_form_on_witness", "NONZERO_PRODUCTION"),
        "F24": mutate_atlas("O09", "exact_scope", "inherited raw q_squared slot"),
    }
    registered = [row["gate_id"] for row in table("FALSIFICATION_CONTRACT.tsv")]
    require(registered == list(mutations), "mutation/contract order")
    catches = []
    for gate_id, mutation in mutations.items():
        trial = copy.deepcopy(base)
        mutation(trial)
        caught = False
        detail = ""
        try:
            validate(trial)
        except GateError as error:
            caught = True
            detail = str(error)
        require(caught, f"uncaught mutation {gate_id}")
        catches.append({"gate_id": gate_id, "result": "PASS_CAUGHT", "trigger": detail})
    with (HERE / "CATCH_PROOFS.tsv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle, delimiter="\t", fieldnames=["gate_id", "result", "trigger"], lineterminator="\n"
        )
        writer.writeheader()
        writer.writerows(catches)
    print(json.dumps({"status": "PASS", "base_validation": "PASS", "catches": len(catches)}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
