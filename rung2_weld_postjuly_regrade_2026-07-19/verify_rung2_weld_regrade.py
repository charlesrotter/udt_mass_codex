#!/usr/bin/env python3
"""Fail-closed verifier and mutation catches for the rung-2 weld package."""

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
BASE = "d0b5d824432e1ac621d5e198e9ac490b265d2ea6"
RESULT_PATH = HERE / "DERIVATION_RESULT.json"
VERIFY_PATH = HERE / "VERIFICATION_RESULT.json"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def normalized_script_body(path: Path) -> str:
    """Remove util-linux script's timestamp header/footer, retaining stdout."""
    lines = path.read_text(encoding="utf-8").splitlines()
    require(lines and lines[0].startswith("Script started on "), "transcript header absent")
    require(lines[-1].startswith("Script done on ") and 'COMMAND_EXIT_CODE="0"' in lines[-1], "transcript footer/exit absent")
    body = lines[1:-1]
    while body and body[0] == "":
        body.pop(0)
    while body and body[-1] == "":
        body.pop()
    return "\n".join(body) + "\n"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def validate_derivation(data: dict) -> None:
    require(data["schema"] == "rung2-weld-regrade-1.0", "wrong derivation schema")
    checks = data["checks"]
    required_checks = {
        "linear_mixed_curvature_rederived",
        "K_retained_with_half_coefficient",
        "pre_july_action_algebraic_EL_rederived",
        "nonlinear_reciprocity_does_not_zero_mixed_curvature",
        "static_reciprocal_mixed_zero_petrov_I",
        "kasner_petrov_I_nonzero_discriminant",
    }
    require(required_checks <= set(checks), "missing load-bearing algebra check")
    require(all(value.startswith("PASS") for value in checks.values()), "failed algebra check")

    linear = data["linearized_historical_tile"]
    require(linear["classification"] == "RAW_METRIC_DERIVED_LINEARIZED_CURVATURE_COMPONENT_NOT_AN_EOM", "curvature/EOM conflation")
    require("8 pi G" in linear["equation_step"] and "imported Einstein/source" in linear["equation_step"], "Einstein/source step lost")
    expression = linear["delta_G_up_t_theta"]
    require("Derivative(K(t, r), t)" in expression, "K term dropped")
    require("Derivative(H1(t, r), r)" in expression, "differential H1 term dropped")

    old_action = data["pre_july_scalar_action_tile"]
    require(old_action["classification"] == "HISTORICAL_PRE_NATIVE_ACTION_CONDITIONAL_NOT_IN_CURRENT_C0_C1_ACTION_LEDGER", "pre-July action promoted")
    require("Derivative(phi0(r), r)" in old_action["second_variation_EL_H1"], "old algebraic EL lost")
    require("Derivative(p(t, r), t)" in old_action["second_variation_EL_H1"], "old p_t coupling lost")

    nonlinear = data["exact_nonlinear_diagonal_tile"]
    require(nonlinear["classification"] == "EXACT_METRIC_DERIVED_READOUT_NOT_A_NATIVE_ZERO_EQUATION", "nonlinear readout promoted")
    require("Phi,A,B free" in nonlinear["metric"], "angular freedoms dropped")
    require(nonlinear["nonzero_witness"] != "0", "reciprocity falsely zeroed mixed curvature")

    for family in ("differential_weld_causal_counterjets", "algebraic_weld_causal_counterjets"):
        family_data = data[family]
        require("perturbation first jet dp" in family_data["scope"], f"counterjet scope lost: {family}")
        witnesses = family_data["witnesses"]
        require(set(witnesses) == {"TIMELIKE", "SPACELIKE", "NULL", "ZERO"}, f"incomplete causal census: {family}")
        require(witnesses["TIMELIKE"] == {"residual": "0", "gradient_norm": "-1"}, f"timelike witness lost: {family}")
        require(witnesses["SPACELIKE"] == {"residual": "0", "gradient_norm": "1"}, f"spacelike witness lost: {family}")
        require(witnesses["NULL"] == {"residual": "0", "gradient_norm": "0"}, f"null witness lost: {family}")

    full_gradient = data["full_gradient_spacelike_historical_vacuum_witness"]
    require(full_gradient["background_scalar_EL_E0"] == "0", "historical vacuum background off shell")
    require(full_gradient["differential_weld_residual"] == "0", "full-gradient differential residual")
    require(full_gradient["algebraic_weld_residual"] == "0", "full-gradient algebraic residual")
    require(full_gradient["causal_class"] == "SPACELIKE_NONZERO", "full-gradient causal class changed")
    require(full_gradient["total_dphi_norm"] == "C_vac**2/(4*r**3*(C_vac + r))", "full-gradient norm changed")

    static = data["static_reciprocal_historical_family_comparison"]
    require(static["mixed_component"].startswith("G^t_theta=0"), "mixed-zero witness lost")
    require(static["electric_characteristic_discriminant"] == "11913/1250000000", "static Petrov discriminant changed")
    require(static["petrov_type"] == "I", "static witness not Petrov I")
    require("not a complete UDT universe" in static["scope"], "conditional witness promoted")

    kasner = data["kasner_conditional_comparison"]
    require(kasner["pnd_discriminant"] == "1194393600/(13841287201*tau**12)", "Kasner discriminant changed")
    require("CONDITIONAL_COMPARISON_NOT_COMPLETE_UDT" in kasner["classification"], "Kasner promoted")


def validate_report(text: str) -> None:
    required = [
        "metric-derived mixed-curvature expression",
        "Einstein/source equation",
        "HISTORICAL_PRE_NATIVE_ACTION_CONDITIONAL",
        "K=0 FORCED` wording is regraded",
        "A geometric coupling is not a law setting the component to zero",
        "observational agreement would show compatibility",
        "Charles alone decides whether and how to revise that entry",
        "not a complete UDT universe",
    ]
    for phrase in required:
        require(phrase in text, f"report disclosure missing: {phrase}")
    forbidden = [
        "the raw curvature component is the native equation",
        "Petrov D has one unique repeated PND",
        "the CMB fit derives the weld",
        "Kasner is a complete UDT universe",
        "K=0 is forced by current UDT",
    ]
    for phrase in forbidden:
        require(phrase not in text, f"forbidden promotion present: {phrase}")


def expect_failure(label: str, operation, catches: dict[str, str]) -> None:
    try:
        operation()
    except (AssertionError, KeyError):
        catches[label] = "PASS"
        return
    raise AssertionError(f"mutation catch did not fail: {label}")


def main() -> None:
    checks: dict[str, str] = {}
    catches: dict[str, str] = {}

    before_result_hash = sha256(RESULT_PATH)
    env = os.environ.copy()
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    env["CUDA_VISIBLE_DEVICES"] = ""
    derive = subprocess.run(
        [sys.executable, "-B", str(HERE / "derive_rung2_weld_regrade.py")],
        cwd=ROOT,
        env=env,
        text=True,
        capture_output=True,
        timeout=180,
        check=False,
    )
    require(derive.returncode == 0, f"derivation replay failed: {derive.stderr}")
    require(not derive.stderr, "derivation emitted stderr")
    require(sha256(RESULT_PATH) == before_result_hash, "derivation replay changed result bytes")
    transcript_body = normalized_script_body(HERE / "DERIVATION_TRANSCRIPT.txt")
    require(transcript_body == derive.stdout, "derivation transcript is stale or byte-different")
    checks["deterministic_derivation_replay"] = "PASS"
    checks["derivation_transcript_matches_stdout"] = "PASS"

    historical = subprocess.run(
        [sys.executable, "-B", str(ROOT / "legacy/root_oneoffs_2026-07-01/native_weld_status_derivation.py")],
        cwd=ROOT,
        env=env,
        text=True,
        capture_output=True,
        timeout=180,
        check=False,
    )
    require(historical.returncode == 0, f"historical replay failed: {historical.stderr}")
    require("All symbolic/exact checks PASSED" in historical.stdout, "historical pass sentinel missing")
    require("EINSTEIN IMPORT" in historical.stdout, "historical import disclosure missing")
    require("native ALGEBRAIC weld" in historical.stdout, "historical distinct-weld disclosure missing")
    checks["historical_replay"] = "PASS"

    data = json.loads(RESULT_PATH.read_text(encoding="utf-8"))
    validate_derivation(data)
    checks["derivation_contract"] = "PASS"

    # Independent closed-form checks on the two PND discriminants.
    lam = sp.symbols("lambda")
    matrix = sp.Matrix(
        [
            [sp.Rational(-1, 75), -sp.sqrt(2) / 20, 0],
            [-sp.sqrt(2) / 20, sp.Rational(-7, 75), 0],
            [0, 0, sp.Rational(8, 75)],
        ]
    )
    static_disc = sp.factor(sp.discriminant(matrix.charpoly(lam).as_expr(), lam))
    require(static_disc == sp.Rational(11913, 1250000000), "independent static discriminant mismatch")
    tau, root = sp.symbols("tau root", nonzero=True)
    kasner_poly = 3 * (root**4 + 18 * root**2 + 1) / (49 * tau**2)
    kasner_disc = sp.factor(sp.discriminant(kasner_poly, root))
    require(kasner_disc == sp.Rational(1194393600, 13841287201) / tau**12, "independent Kasner discriminant mismatch")
    checks["independent_PND_discriminants"] = "PASS"

    sources_before = sha256(HERE / "SOURCE_INVENTORY.tsv")
    rebuilt = subprocess.run(
        [sys.executable, "-B", str(HERE / "build_source_inventory.py")],
        cwd=ROOT,
        env=env,
        text=True,
        capture_output=True,
        timeout=60,
        check=False,
    )
    require(rebuilt.returncode == 0, f"source inventory replay failed: {rebuilt.stderr}")
    require(sha256(HERE / "SOURCE_INVENTORY.tsv") == sources_before, "source inventory replay changed bytes")
    sources = read_tsv(HERE / "SOURCE_INVENTORY.tsv")
    require(len(sources) == 17 and len({row["path"] for row in sources}) == 17, "source inventory count/uniqueness failure")
    by_path = {row["path"]: row for row in sources}
    require(by_path["legacy/root_oneoffs_2026-07-01/native_weld_status_derivation.py"]["first_date"] < "2026-07-01", "legacy script date laundered")
    require(by_path["weld_status_results.md"]["first_date"] < "2026-07-01", "legacy result date laundered")
    checks["source_inventory_replay"] = "PASS"

    cold = (ROOT / "UDT_NATIVE_ACTION_COLD_PACKET.md").read_text(encoding="utf-8")
    adjudication = (ROOT / "native_action_final_adjudication_2026-07-18/FINAL_ADJUDICATION_REPORT.md").read_text(encoding="utf-8")
    historical_result = (ROOT / "weld_status_results.md").read_text(encoding="utf-8")
    require("an action, field equation" in cold, "cold-packet missing-action disclosure absent")
    require("complete action" in adjudication and "OPEN" in adjudication, "current action-open ruling absent")
    require(historical_result.startswith("> **SUPERSEDED"), "historical supersession banner absent")
    checks["current_vs_historical_source_separation"] = "PASS"

    objects = read_tsv(HERE / "WELD_OBJECT_LEDGER.tsv")
    statuses = read_tsv(HERE / "STATUS_LEDGER.tsv")
    require(len(objects) == 12 and len({row["id"] for row in objects}) == 12, "object ledger coverage failure")
    require(len(statuses) == 20 and len({row["id"] for row in statuses}) == 20, "status ledger coverage failure")
    require(next(row for row in objects if row["id"] == "W03")["current_status"] == "IMPORTED_EINSTEIN_SOURCE_EQUATION", "differential weld misgraded")
    require(next(row for row in objects if row["id"] == "W05")["current_status"] == "HISTORICAL_PRE_NATIVE_ACTION_CONDITIONAL_NOT_CURRENT_C0_C1", "algebraic weld misgraded")
    checks["ledger_contract"] = "PASS"

    report = (HERE / "AUDIT_REPORT.md").read_text(encoding="utf-8")
    validate_report(report)
    checks["report_contract"] = "PASS"

    changed = subprocess.check_output(["git", "diff", "--name-only", BASE, "--"], cwd=ROOT, text=True).splitlines()
    forbidden_changes = {"LIVE.md", "HANDOFF.md", "INDEX.md", "README.md", "CANON.md"}
    require(not forbidden_changes.intersection(changed), f"forbidden control change: {forbidden_changes.intersection(changed)}")
    checks["no_control_or_canon_edits"] = "PASS"

    # Exercised fail-closed mutations.
    mutation = copy.deepcopy(data)
    mutation["linearized_historical_tile"]["equation_step"] = "native equation"
    expect_failure("deleted_Einstein_source_step", lambda: validate_derivation(mutation), catches)

    mutation = copy.deepcopy(data)
    mutation["linearized_historical_tile"]["classification"] = "NATIVE_EOM"
    expect_failure("curvature_component_called_EOM", lambda: validate_derivation(mutation), catches)

    mutation = copy.deepcopy(data)
    mutation["linearized_historical_tile"]["delta_G_up_t_theta"] = mutation["linearized_historical_tile"]["delta_G_up_t_theta"].replace("Derivative(K(t, r), t)", "0")
    expect_failure("K_term_dropped", lambda: validate_derivation(mutation), catches)

    mutation = copy.deepcopy(data)
    mutation["pre_july_scalar_action_tile"]["classification"] = "CURRENT_NATIVE_C1"
    expect_failure("pre_july_label_promoted", lambda: validate_derivation(mutation), catches)

    mutation = copy.deepcopy(data)
    del mutation["differential_weld_causal_counterjets"]["witnesses"]["SPACELIKE"]
    expect_failure("compatibility_called_implication", lambda: validate_derivation(mutation), catches)

    mutation = copy.deepcopy(data)
    mutation["full_gradient_spacelike_historical_vacuum_witness"]["causal_class"] = "NULL"
    expect_failure("full_gradient_spacelike_witness_demoted", lambda: validate_derivation(mutation), catches)

    mutation = copy.deepcopy(data)
    mutation["static_reciprocal_historical_family_comparison"]["electric_characteristic_discriminant"] = "0"
    expect_failure("Petrov_I_counterwitness_deleted", lambda: validate_derivation(mutation), catches)

    mutation = copy.deepcopy(data)
    mutation["static_reciprocal_historical_family_comparison"]["scope"] = "complete UDT universe"
    expect_failure("conditional_countermetric_promoted", lambda: validate_derivation(mutation), catches)

    expect_failure("CMB_comparison_called_derivation", lambda: validate_report(report + "\nthe CMB fit derives the weld\n"), catches)
    expect_failure("Petrov_D_called_unique", lambda: validate_report(report + "\nPetrov D has one unique repeated PND\n"), catches)
    expect_failure("K_zero_called_current_forced", lambda: validate_report(report + "\nK=0 is forced by current UDT\n"), catches)

    output = {
        "schema": "rung2-weld-verification-1.0",
        "checks": checks,
        "catch_proofs": catches,
        "counts": {
            "algebra_checks": len(data["checks"]),
            "source_rows": len(sources),
            "object_rows": len(objects),
            "status_rows": len(statuses),
            "catch_proofs": len(catches),
        },
        "hashes": {
            "derivation_result_sha256": sha256(RESULT_PATH),
            "source_inventory_sha256": sha256(HERE / "SOURCE_INVENTORY.tsv"),
            "historical_stdout_sha256": hashlib.sha256(historical.stdout.encode()).hexdigest(),
            "derivation_stdout_sha256": hashlib.sha256(derive.stdout.encode()).hexdigest(),
            "derivation_transcript_body_sha256": hashlib.sha256(transcript_body.encode()).hexdigest(),
            "derivation_transcript_file_sha256": sha256(HERE / "DERIVATION_TRANSCRIPT.txt"),
        },
        "maximum_verified_conclusion": (
            "HISTORICAL_DIFFERENTIAL_WELD_REPRODUCED_AS_EINSTEIN_SOURCE_CONDITIONAL;_"
            "DISTINCT_ALGEBRAIC_WELD_REPRODUCED_AS_PRE_NATIVE_ACTION_CONDITIONAL;_"
            "NO_NULL_DPHI_OR_UNIQUE_REPEATED_PND_SELECTOR_FOLLOWS_IN_THE_TESTED_TILES"
        ),
    }
    VERIFY_PATH.write_text(json.dumps(output, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
