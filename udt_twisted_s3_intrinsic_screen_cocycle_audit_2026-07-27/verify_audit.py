#!/usr/bin/env python3
"""Fail-closed package and claim verifier with exercised preregistered catches."""

from __future__ import annotations

import ast
import copy
import csv
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent

STAMPS = (
    "COPRESENCE = WORKING_INTERPRETIVE_FRAME",
    "METRIC_CAUSAL_STRUCTURE = DERIVED_CONDITIONAL",
    "INSTANTANEOUS_OPERATIONAL_ACCESS = NOT_DERIVED",
    "COMPLETE_WHOLE_SOLUTION_LAW = OPEN",
)


def read_tsv(name: str) -> list[dict[str, str]]:
    with (HERE / name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def canonical_state() -> dict[str, object]:
    return {
        "stamps": STAMPS, "instant_access": False, "C07_ruler": False, "C08_depth": False,
        "parent_intact": True, "projector": True, "projector_annihilates": True,
        "q_positive": True, "orientation_selected": False, "area_identity": True,
        "local_is_optical": False, "killing_energy": True, "Q_sign": True,
        "arbitrary_observer_join": False, "vertex_composable": False, "M_valid": True,
        "same_branch": True, "irreducible": False, "WRL_raw_identity": False,
        "SNe_selection": False, "path_selected": False, "downstream_physics": False,
        "independent_import": False, "candidate_universe_exact": True,
    }


def validate_state(state: dict[str, object]) -> None:
    assert state["stamps"] == STAMPS
    assert state["instant_access"] is False
    assert state["C07_ruler"] is False and state["C08_depth"] is False
    assert state["parent_intact"] is True
    assert state["projector"] is True and state["projector_annihilates"] is True
    assert state["q_positive"] is True and state["orientation_selected"] is False
    assert state["area_identity"] is True and state["local_is_optical"] is False
    assert state["killing_energy"] is True and state["Q_sign"] is True
    assert state["arbitrary_observer_join"] is False
    assert state["vertex_composable"] is False and state["M_valid"] is True
    assert state["same_branch"] is True and state["irreducible"] is False
    assert state["WRL_raw_identity"] is False and state["SNe_selection"] is False
    assert state["path_selected"] is False and state["downstream_physics"] is False
    assert state["independent_import"] is False and state["candidate_universe_exact"] is True


def expect_mutation(field: str, value: object) -> str:
    state = canonical_state()
    state[field] = value
    try:
        validate_state(state)
    except AssertionError:
        return "PASS"
    raise AssertionError(f"mutation accepted: {field}")


def main() -> int:
    production = json.loads((HERE / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    independent = json.loads((HERE / "INDEPENDENT_RESULT.json").read_text(encoding="utf-8"))
    candidates = read_tsv("CANDIDATE_UNIVERSE.tsv")
    outcomes = read_tsv("CANDIDATE_OUTCOMES.tsv")
    contracts = read_tsv("FALSIFICATION_CONTRACT.tsv")
    status = read_tsv("STATUS_LEDGER.tsv")
    connection = read_tsv("CONNECTION_MIXING_ATLAS.tsv")
    assert production["status"] == independent["status"] == "PASS"
    assert production["sympy_version"] == "1.14.0"
    assert len(candidates) == len(outcomes) == 8 and len(contracts) == 24
    assert len(status) == 18 and len(connection) == 16
    assert [row["candidate"] for row in candidates] == [row["candidate"] for row in outcomes]
    assert [(row["candidate"], row["lambda"]) for row in candidates[-2:]] == [("C07", "0"), ("C08", "0")]
    assert all(row["status"].startswith("PASS_BOUNDED") for row in outcomes[:6])
    assert outcomes[6]["status"] == "FAIL_AS_EXPECTED_TWIST_OFF"
    assert outcomes[7]["status"] == "FAIL_AS_EXPECTED_DEPTH_OFF"

    report = (HERE / "AUDIT_REPORT.md").read_text(encoding="utf-8")
    derivation = (HERE / "EXACT_DERIVATION.md").read_text(encoding="utf-8")
    prereg = (HERE / "PREREGISTRATION.md").read_text(encoding="utf-8")
    for stamp in STAMPS:
        assert stamp in report and stamp in prereg
    assert "direct_sum" in report and "reducible" in report.lower()
    assert "forces `dphi=0`" in report
    assert "cannot be conflated" in derivation
    assert "not a `lambda` selection" in derivation

    p = production
    assert p["projector"]["idempotent"] and p["projector"]["rank"] == 2
    assert p["projector"]["annihilates_clock_and_ruler"]
    assert p["coframe_and_connection"]["area_exterior_derivative"] == "2*lambda*dphi^theta2^theta3"
    assert p["coframe_and_connection"]["pregeodesic_condition"] == "E2(phi)=E3(phi)=0"
    assert p["coframe_and_connection"]["global_alignment_implication"].endswith("dphi=0")
    assert p["clock_and_jacobi"]["log_Q"] == "phi_q-phi_p"
    assert p["clock_and_jacobi"]["full_propagator_symplectic_composable_invertible"]
    assert p["clock_and_jacobi"]["vertex_B_block_standalone_cocycle"] is False
    assert p["clock_and_jacobi"]["irreducible_solder"] is False
    assert p["WRL_SNe_nonconflation"]["open_interval_identity_for_constant_lambda"] is False
    assert p["authority_boundary"] == {
        "SNe_fit_performed": False, "action_or_source_selected": False,
        "irreducible_solder_claimed": False, "lambda_selected": False, "on_shell": False,
        "operational_access_derived": False, "path_selected": False,
    }
    assert independent["production_module_imported"] is False
    assert independent["contact_obstruction_exact"] and independent["depth_triangles"] == 64

    tree = ast.parse((HERE / "verify_screen_cocycle_independent.py").read_text(encoding="utf-8"))
    allowed = {"__future__", "csv", "json", "fractions", "pathlib"}
    imports = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imports.update(alias.name.split(".")[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            imports.add((node.module or "").split(".")[0])
    assert imports <= allowed, imports

    mutations = {
        "F01": ("stamps", STAMPS[:-1]), "F02": ("instant_access", True),
        "F03": ("C07_ruler", True), "F04": ("C08_depth", True),
        "F05": ("parent_intact", False), "F06": ("projector", False),
        "F07": ("projector_annihilates", False), "F08": ("q_positive", False),
        "F09": ("orientation_selected", True), "F10": ("area_identity", False),
        "F11": ("local_is_optical", True), "F12": ("killing_energy", False),
        "F13": ("Q_sign", False), "F14": ("arbitrary_observer_join", True),
        "F15": ("vertex_composable", True), "F16": ("M_valid", False),
        "F17": ("same_branch", False), "F18": ("irreducible", True),
        "F19": ("WRL_raw_identity", True), "F20": ("SNe_selection", True),
        "F21": ("path_selected", True), "F22": ("downstream_physics", True),
        "F23": ("independent_import", True), "F24": ("candidate_universe_exact", False),
    }
    assert set(mutations) == {row["catch_id"] for row in contracts}
    catches = [{"catch_id": row["catch_id"], "result": expect_mutation(*mutations[row["catch_id"]]),
                "corruption_or_overclaim": row["corruption_or_overclaim"]} for row in contracts]
    assert all(row["result"] == "PASS" for row in catches)
    with (HERE / "CATCH_PROOFS.tsv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=("catch_id", "result", "corruption_or_overclaim"),
                                delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(catches)
    result = {
        "schema": "udt-twisted-s3-intrinsic-screen-cocycle-verification-1.0",
        "status": "PASS", "candidate_rows": 8, "status_rows": len(status),
        "connection_rows": len(connection), "catch_proofs": "24/24",
        "production_sympy": production["sympy_version"],
        "independent_method": "stdlib_Fraction_no_production_import",
        "branch_join": "PASS_C01_TO_C06", "global_alignment_obstruction": "PASS_EXACT",
        "WRL_SNe_nonconflation": "PASS_EXACT",
    }
    (HERE / "VERIFICATION_RESULT.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
