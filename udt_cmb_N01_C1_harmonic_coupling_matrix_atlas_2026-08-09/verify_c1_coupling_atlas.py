#!/usr/bin/env python3
"""Independent N01 verifier using adaptive quadrature and table mutations.

It does not import the production derivation or reuse its quadrature implementation.
"""

from __future__ import annotations

import copy
import csv
import hashlib
import json
import math
import subprocess
from pathlib import Path

import sympy as sp
from scipy.integrate import quad
from scipy.special import lpmv


ROOT = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent
PREREG_COMMIT = "1537d669d411c1bb4c18c0814dc1aef3af7ea36d"
B_GRID = {0.0, 0.01, 0.1, 1.0, 10.0, 100.0}
M_GRID = {0, 1, 2, 3}
MATRICES = {"W", "M", "K", "H", "L"}
TOL = 2.0e-11
CHECKS: dict[str, bool] = {}


def check(name: str, condition: object) -> None:
    CHECKS[name] = bool(condition)
    print(f"CHECK {name}: {CHECKS[name]}")


def read_tsv(name: str) -> list[dict[str, str]]:
    with (HERE / name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def validate_payload(payload: dict[str, object]) -> None:
    if payload.get("status") != "VERIFIED_BOUNDED_C1_COUPLING_MAP__CONDITIONAL_SCALAR_DIAGNOSTIC__NO_EIGENSOLVE":
        raise ValueError("status")
    keys = payload.get("keys")
    if not isinstance(keys, dict) or payload.get("key_count") != 20 or len(keys) != 20 or not all(keys.values()):
        raise ValueError("key census")
    if payload.get("B_grid") != [0.0, 0.01, 0.1, 1.0, 10.0, 100.0]:
        raise ValueError("B universe")
    if payload.get("abs_m_grid") != [0, 1, 2, 3]:
        raise ValueError("m universe")
    if payload.get("matrix_names") != ["W", "M", "K", "H", "L"]:
        raise ValueError("matrix universe")
    if payload.get("element_count") != 15420 or payload.get("block_summary_count") != 120:
        raise ValueError("table census")
    equation = str(payload.get("matrix_equation"))
    for token in ("d_r[r^2 A W(B) d_r R]", "K(B)+H_m(B)", "2h omega m", "M(B)R"):
        if token not in equation:
            raise ValueError("matrix equation")
    if "same angular matrices" not in str(payload.get("negative_m_status")) or "retains sign" not in str(payload.get("negative_m_status")):
        raise ValueError("m sign")
    structure = str(payload.get("structural_result"))
    if "same-parity ell coupling" not in structure or "fixed abs_m" not in structure or "finite-band" in structure:
        raise ValueError("structure")
    maximum = str(payload.get("maximum_conclusion"))
    for token in ("conditional C1", "no physical screen", "no physical screen, spectrum", "FD2", "GPU"):
        if token not in maximum:
            raise ValueError("maximum conclusion")


def validate_tables(elements: list[dict[str, str]], summaries: list[dict[str, str]], first: list[dict[str, str]]) -> None:
    if len(elements) != 15420:
        raise ValueError("element census")
    element_keys = {
        (float(r["B"]), int(r["abs_m"]), r["matrix"], int(r["ell_i"]), int(r["ell_j"]))
        for r in elements
    }
    expected_element_keys = {
        (B, abs_m, matrix, ell_i, ell_j)
        for B in B_GRID
        for abs_m in M_GRID
        for matrix in MATRICES
        for ell_i in range(abs_m, 17)
        for ell_j in range(ell_i, 17)
    }
    if element_keys != expected_element_keys:
        raise ValueError("exact element key universe")
    if any(int(r["ell_i"]) > int(r["ell_j"]) for r in elements):
        raise ValueError("triangle")
    if any(float(r["abs_quad_difference"]) >= TOL for r in elements):
        raise ValueError("quadrature")
    if any(r["same_parity"] == "FALSE" and abs(float(r["value_q512"])) >= TOL for r in elements):
        raise ValueError("parity")
    summary_keys = {(float(r["B"]), int(r["abs_m"]), r["matrix"]) for r in summaries}
    expected_summary_keys = {(B, abs_m, matrix) for B in B_GRID for abs_m in M_GRID for matrix in MATRICES}
    if len(summaries) != 120 or summary_keys != expected_summary_keys:
        raise ValueError("exact summary key universe")
    if any(r["opposite_parity_entries_above_threshold"] != "0" for r in summaries):
        raise ValueError("summary parity")
    first_keys = {(int(r["abs_m"]), int(r["ell_i"]), int(r["ell_j"])) for r in first}
    expected_first_keys = {
        (abs_m, ell_i, ell_j)
        for abs_m in M_GRID
        for ell_i in range(abs_m, min(16, abs_m + 4) + 1)
        for ell_j in range(ell_i, min(16, abs_m + 4) + 1)
        if (ell_i - ell_j) % 2 == 0
    }
    if len(first) != 36 or first_keys != expected_first_keys:
        raise ValueError("exact first-order key universe")
    if any(int(r["delta_ell"]) > 2 and any(r[field] != "0" for field in ("W_prime_0", "M_prime_0", "L_prime_0")) for r in first):
        raise ValueError("first-order bandwidth")

    grouped: dict[tuple[float, int, str], list[dict[str, str]]] = {}
    for row in elements:
        grouped.setdefault((float(row["B"]), int(row["abs_m"]), row["matrix"]), []).append(row)
    summary_lookup = {(float(r["B"]), int(r["abs_m"]), r["matrix"]): r for r in summaries}

    def close(left: str, right: float) -> bool:
        return math.isclose(float(left), right, rel_tol=2e-15, abs_tol=2e-18)

    for block_key in expected_summary_keys:
        rows = grouped[block_key]
        summary = summary_lookup[block_key]
        abs_m = block_key[1]
        dimension = 17 - abs_m
        diagonal = [float(r["value_q512"]) for r in rows if r["ell_i"] == r["ell_j"]]
        same_offdiag = [r for r in rows if r["ell_i"] != r["ell_j"] and r["same_parity"] == "TRUE"]
        opposite = [r for r in rows if r["same_parity"] == "FALSE"]
        observed = [
            int(r["ell_j"]) - int(r["ell_i"])
            for r in same_offdiag if r["above_1e_minus_12"] == "TRUE"
        ]
        parity_even = sum((ell + abs_m) % 2 == 0 for ell in range(abs_m, 17))
        rebuilt = (
            int(summary["dimension"]) == dimension,
            int(summary["parity_even_dimension"]) == parity_even,
            int(summary["parity_odd_dimension"]) == dimension - parity_even,
            close(summary["diagonal_min"], min(diagonal)),
            close(summary["diagonal_max"], max(diagonal)),
            int(summary["same_parity_offdiag_above_threshold"])
            == sum(r["above_1e_minus_12"] == "TRUE" for r in same_offdiag),
            int(summary["opposite_parity_entries_above_threshold"])
            == sum(r["above_1e_minus_12"] == "TRUE" for r in opposite),
            close(summary["maximum_same_parity_offdiag_abs"], max((abs(float(r["value_q512"])) for r in same_offdiag), default=0.0)),
            int(summary["farthest_observed_delta_ell"]) == max(observed, default=0),
            close(summary["maximum_opposite_parity_abs"], max((abs(float(r["value_q512"])) for r in opposite), default=0.0)),
            close(summary["maximum_quadrature_difference"], max(float(r["abs_quad_difference"]) for r in rows)),
        )
        if not all(rebuilt):
            raise ValueError("summary reconstruction")


def p(abs_m: int, ell: int, x: float) -> float:
    norm = math.sqrt((2 * ell + 1) / 2 * math.factorial(ell - abs_m) / math.factorial(ell + abs_m))
    return norm * float(lpmv(abs_m, ell, x))


def dp(abs_m: int, ell: int, x: float) -> float:
    norm = math.sqrt((2 * ell + 1) / 2 * math.factorial(ell - abs_m) / math.factorial(ell + abs_m))
    current = float(lpmv(abs_m, ell, x))
    previous = 0.0 if ell == abs_m else float(lpmv(abs_m, ell - 1, x))
    return norm * (ell * x * current - (ell + abs_m) * previous) / (x * x - 1)


def adaptive_element(B: float, abs_m: int, matrix: str, ell_i: int, ell_j: int) -> float:
    def integrand(x: float) -> float:
        F = math.sqrt(1 + B * (1 - x * x))
        pi, pj = p(abs_m, ell_i, x), p(abs_m, ell_j, x)
        if matrix == "W":
            return pi * F * pj
        if matrix == "M":
            return pi * pj / F
        angular = (1 - x * x) * F * dp(abs_m, ell_i, x) * dp(abs_m, ell_j, x)
        polar = 0.0 if abs_m == 0 else abs_m**2 * pi * pj / ((1 - x * x) * F)
        if matrix == "K":
            return angular
        if matrix == "H":
            return polar
        if matrix == "L":
            return angular + polar
        raise ValueError(matrix)
    return float(quad(integrand, -1, 1, epsabs=2e-12, epsrel=2e-12, limit=300)[0])


def main() -> None:
    payload = json.loads((HERE / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    elements = read_tsv("MATRIX_ELEMENTS.tsv")
    summaries = read_tsv("BLOCK_SUMMARY.tsv")
    first = read_tsv("FIRST_ORDER_COUPLING.tsv")
    validate_payload(payload)
    validate_tables(elements, summaries, first)
    check("V01_payload", True)
    check("V02_table_census", True)

    lookup = {
        (float(r["B"]), int(r["abs_m"]), r["matrix"], int(r["ell_i"]), int(r["ell_j"])): float(r["value_q512"])
        for r in elements
    }
    controls = (
        (0.0, 0, "W", 0, 0),
        (0.0, 1, "L", 1, 1),
        (0.0, 1, "L", 1, 3),
        (0.01, 0, "W", 0, 8),
        (0.1, 1, "M", 1, 5),
        (1.0, 2, "L", 2, 6),
        (10.0, 3, "H", 3, 7),
        (100.0, 0, "K", 10, 16),
    )
    differences = {control: abs(lookup[control] - adaptive_element(*control)) for control in controls}
    check("V03_adaptive_controls", max(differences.values()) < TOL and len(differences) == 8)
    check("V04_round_identity", abs(lookup[(0.0, 0, "W", 0, 0)] - 1) < TOL)
    check("V05_round_spherical_diagonal", abs(lookup[(0.0, 1, "L", 1, 1)] - 2) < TOL)
    check("V06_round_spherical_offdiagonal", abs(lookup[(0.0, 1, "L", 1, 3)]) < TOL)

    first_lookup = {(int(r["abs_m"]), int(r["ell_i"]), int(r["ell_j"])): r for r in first}
    check("V07_exact_W1_control", first_lookup[(0, 0, 2)]["W_prime_0"] == "-sqrt(5)/15")
    check("V08_exact_L1_control", first_lookup[(1, 1, 3)]["L_prime_0"] == "-4*sqrt(14)/35")
    check("V09_exact_delta4_zero", all(first_lookup[key]["L_prime_0"] == "0" for key in ((0, 0, 4), (1, 1, 5), (2, 2, 6), (3, 3, 7))))

    first_order_max_difference = 0.0
    for row in first:
        abs_m, ell_i, ell_j = int(row["abs_m"]), int(row["ell_i"]), int(row["ell_j"])
        numeric = {
            "W_prime_0": quad(lambda x: 0.5 * (1 - x*x) * p(abs_m, ell_i, x) * p(abs_m, ell_j, x), -1, 1, epsabs=2e-12, epsrel=2e-12)[0],
            "M_prime_0": quad(lambda x: -0.5 * (1 - x*x) * p(abs_m, ell_i, x) * p(abs_m, ell_j, x), -1, 1, epsabs=2e-12, epsrel=2e-12)[0],
            "K_prime_0": quad(lambda x: 0.5 * (1 - x*x)**2 * dp(abs_m, ell_i, x) * dp(abs_m, ell_j, x), -1, 1, epsabs=2e-12, epsrel=2e-12)[0],
            "H_prime_0": -0.5 * abs_m**2 * int(ell_i == ell_j),
        }
        numeric["L_prime_0"] = numeric["K_prime_0"] + numeric["H_prime_0"]
        for field, value in numeric.items():
            first_order_max_difference = max(first_order_max_difference, abs(float(sp.sympify(row[field])) - value))
    check("V09B_all_first_order_adaptive", first_order_max_difference < TOL)

    source_ok = True
    with (HERE / "SOURCE_MANIFEST.tsv").open(encoding="utf-8") as handle:
        next(handle)
        for line in handle:
            path_text, digest = line.rstrip("\n").split("\t")
            data = subprocess.run(["git", "show", f"{PREREG_COMMIT}:{path_text}"], cwd=ROOT, check=True, capture_output=True).stdout
            source_ok &= hashlib.sha256(data).hexdigest() == digest
    check("V10_source_manifest", source_ok)
    check("V11_negative_m_disclosed", "retains sign" in str(payload["negative_m_status"]))
    check("V12_no_parity_leakage", max(abs(float(r["value_q512"])) for r in elements if r["same_parity"] == "FALSE") < TOL)
    check("V13_quadrature_gate", max(float(r["abs_quad_difference"]) for r in elements) < TOL)
    check("V14_finite_B_coupling_observed", abs(lookup[(1.0, 2, "L", 2, 6)]) > 1e-3)
    check("V15_round_KH_cancellation", abs(lookup[(0.0, 1, "K", 1, 3)] + lookup[(0.0, 1, "H", 1, 3)]) < TOL)

    mutations: dict[str, tuple[str, object]] = {
        "M01_status_promotion": ("status", "NATIVE_C1_PHYSICAL_SCREEN_DERIVED"),
        "M02_key_loss": ("key_count", 19),
        "M03_drop_B": ("B_grid", [0.0, 0.01, 0.1, 1.0, 10.0]),
        "M04_drop_m": ("abs_m_grid", [0, 1, 2]),
        "M05_drop_H": ("matrix_names", ["W", "M", "K", "L"]),
        "M06_drop_radial_W": ("matrix_equation", "d_r[r^2 A d_r R]-[K(B)+H_m(B)]R+omega^2 M(B)R=0"),
        "M07_false_fixed_band": ("structural_result", "fixed abs_m with universal finite-band coupling"),
        "M08_authorize_FD2": ("maximum_conclusion", "conditional C1; FD2 and GPU authorized"),
        "M09_data_merit": ("maximum_conclusion", "best CMB fit selects C1"),
        "M10_negative_m_loss": ("negative_m_status", "negative m discarded"),
    }
    caught: dict[str, bool] = {}
    for name, (field, value) in mutations.items():
        trial = copy.deepcopy(payload)
        trial[field] = value
        try:
            validate_payload(trial)
        except ValueError:
            caught[name] = True
        else:
            caught[name] = False
    check("V16_payload_mutations", all(caught.values()) and len(caught) == 10)

    table_caught: dict[str, bool] = {}
    trials = {}
    trials["T01_missing_element"] = (elements[:-1], summaries, first)
    trials["T02_duplicate_element"] = (elements + [copy.deepcopy(elements[0])], summaries, first)
    parity_trial = copy.deepcopy(elements)
    next(r for r in parity_trial if r["same_parity"] == "FALSE")["value_q512"] = "1e-3"
    trials["T03_parity_mix"] = (parity_trial, summaries, first)
    quad_trial = copy.deepcopy(elements)
    quad_trial[0]["abs_quad_difference"] = "1e-3"
    trials["T04_quadrature_failure"] = (quad_trial, summaries, first)
    first_trial = copy.deepcopy(first)
    next(r for r in first_trial if int(r["delta_ell"]) == 4)["L_prime_0"] = "1"
    trials["T05_false_first_band"] = (elements, summaries, first_trial)
    summary_trial = copy.deepcopy(summaries)
    summary_trial[0]["opposite_parity_entries_above_threshold"] = "1"
    trials["T06_summary_parity"] = (elements, summary_trial, first)
    element_replacement = copy.deepcopy(elements)
    element_replacement[-1]["ell_j"] = "99"
    trials["T07_invalid_element_replaces_key"] = (element_replacement, summaries, first)
    summary_replacement = copy.deepcopy(summaries)
    summary_replacement[-1]["matrix"] = "INVALID"
    trials["T08_invalid_summary_replaces_key"] = (elements, summary_replacement, first)
    first_replacement = copy.deepcopy(first)
    first_replacement[-1]["ell_j"] = "99"
    trials["T09_invalid_first_order_replaces_key"] = (elements, summaries, first_replacement)
    for name, tables in trials.items():
        try:
            validate_tables(*tables)
        except ValueError:
            table_caught[name] = True
        else:
            table_caught[name] = False
    print(f"TABLE MUTATIONS: {json.dumps(table_caught, sort_keys=True)}")
    check("V17_table_mutations", all(table_caught.values()) and len(table_caught) == 9)

    exact_text = " ".join((HERE / "EXACT_DERIVATION.md").read_text(encoding="utf-8").split())
    report_text = (HERE / "AUDIT_REPORT.md").read_text(encoding="utf-8")
    external_text = (HERE / "EXTERNAL_ADVERSARIAL_REVIEW.md").read_text(encoding="utf-8")
    check("V18_exact_scope", "C1 remains `CHOSE`" in exact_text and "No eigenvalue" in exact_text)
    check("V19_report_stop", "FD2_REMAINS_GATED" in report_text and "NO_EIGENVALUE_SOLVE" in report_text)
    check("V20_external_review", "VERIFIED-WITH-CAVEATS" in external_text and "mutation authority: none" in external_text)

    if not all(CHECKS.values()):
        raise SystemExit("independent N01 verification failed")
    result = {
        "verdict": "VERIFIED-WITH-CAVEATS__BOUNDED_CONDITIONAL_C1_COUPLING_ARCHITECTURE",
        "independence": "local: separate SciPy adaptive quadrature for 8 selected elements and all 36 first-order rows; cold review: symbolic 180-value first-order replay plus 18 hard controls at 50 digits; production module not imported",
        "check_count": len(CHECKS),
        "checks": CHECKS,
        "adaptive_control_differences": {"|".join(map(str, key)): value for key, value in differences.items()},
        "first_order_adaptive_max_difference": first_order_max_difference,
        "mutations": caught,
        "table_mutations": table_caught,
        "mutation_count": len(caught) + len(table_caught),
        "remaining_open": "physical screen, radial profile and boundary, eigenproblem, native dynamics, source/population/polarization, FD2, data comparison, and GPU work",
    }
    (HERE / "VERIFICATION_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"PASS: {len(CHECKS)}/{len(CHECKS)} local independent checks; {len(caught)+len(table_caught)}/{len(caught)+len(table_caught)} mutations caught")


if __name__ == "__main__":
    main()
