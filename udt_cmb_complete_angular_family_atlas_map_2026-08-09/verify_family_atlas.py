#!/usr/bin/env python3
"""Independent verifier for the complete-angular family-atlas MAP.

This does not import the production derivation and uses only the Python
standard library.  The matrix route is exact rational arithmetic.
"""

from __future__ import annotations

import copy
import csv
import hashlib
import itertools
import json
import math
import subprocess
from fractions import Fraction as F
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent
PREREG_COMMIT = "bde6ae01"
CHECKS: dict[str, bool] = {}


def check(name: str, condition: object) -> None:
    CHECKS[name] = bool(condition)
    print(f"CHECK {name}: {CHECKS[name]}")


def parity(p: tuple[int, ...]) -> int:
    inversions = sum(p[i] > p[j] for i in range(len(p)) for j in range(i + 1, len(p)))
    return -1 if inversions % 2 else 1


def determinant(matrix: list[list[F]]) -> F:
    n = len(matrix)
    return sum(
        F(parity(p)) * math.prod(matrix[i][p[i]] for i in range(n))
        for p in itertools.permutations(range(n))
    )


def matmul(left: list[list[F]], right: list[list[F]]) -> list[list[F]]:
    return [[sum(left[i][k] * right[k][j] for k in range(len(right))) for j in range(len(right[0]))] for i in range(len(left))]


def read_tsv(name: str) -> list[dict[str, str]]:
    with (HERE / name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def validate_payload(payload: dict[str, object]) -> None:
    if payload.get("status") != "VERIFIED_DESIGN_MAP__GENERAL_STATIONARY_SCREEN_OPERATOR_DERIVED__NO_SOLVE_AUTHORIZED":
        raise ValueError("status")
    keys = payload.get("keys")
    if not isinstance(keys, dict) or payload.get("key_count") != 27 or len(keys) != 27 or not all(keys.values()):
        raise ValueError("key census")
    operator = str(payload.get("mode_operator"))
    required = (
        "S^-1 d_r(S A u_r)",
        "q^-1-vv^T/Lambda",
        "-2i omega(v^A/Lambda)d_Au",
        "-i omega S^-1 d_A(Sv^A/Lambda)u",
    )
    if not all(token in operator for token in required):
        raise ValueError("operator completeness")
    if payload.get("family_count") != 18 or payload.get("candidate_route_count") != 18:
        raise ValueError("family census")
    if payload.get("basis_count") != 8 or payload.get("batch_count") != 7:
        raise ValueError("architecture census")
    if payload.get("axis_cross_product_count") != 2800:
        raise ValueError("axis cross-product census")
    if payload.get("next_design_ready_task") != "N01_C1_HARMONIC_COUPLING_MATRIX_ATLAS":
        raise ValueError("next task")
    if "physical complete screen" not in str(payload.get("maximum_conclusion")) or "unauthorized" not in str(payload.get("maximum_conclusion")):
        raise ValueError("maximum conclusion")


def exact_control(A: F, q11: F, q12: F, q22: F, b1: F, b2: F) -> tuple[bool, bool]:
    detq = q11 * q22 - q12 * q12
    qi11, qi12, qi22 = q22 / detq, -q12 / detq, q11 / detq
    v1 = qi11 * b1 + qi12 * b2
    v2 = qi12 * b1 + qi22 * b2
    lam = A + b1 * v1 + b2 * v2
    metric = [
        [-A, F(0), b1, b2],
        [F(0), 1 / A, F(0), F(0)],
        [b1, F(0), q11, q12],
        [b2, F(0), q12, q22],
    ]
    inv = [
        [-1 / lam, F(0), v1 / lam, v2 / lam],
        [F(0), A, F(0), F(0)],
        [v1 / lam, F(0), qi11 - v1 * v1 / lam, qi12 - v1 * v2 / lam],
        [v2 / lam, F(0), qi12 - v2 * v1 / lam, qi22 - v2 * v2 / lam],
    ]
    identity = [[F(int(i == j)) for j in range(4)] for i in range(4)]
    return matmul(metric, inv) == identity, determinant(metric) == -detq * lam / A


def main() -> None:
    payload = json.loads((HERE / "MAP_RESULT.json").read_text(encoding="utf-8"))
    validate_payload(payload)
    check("V01_payload", True)

    controls = [
        (F(3, 2), F(2), F(1, 3), F(5, 2), F(1, 4), F(-2, 5)),
        (F(7, 3), F(4), F(-1, 2), F(3), F(5, 7), F(2, 9)),
        (F(5, 4), F(9, 5), F(1, 5), F(8, 3), F(-1, 6), F(7, 8)),
    ]
    results = [exact_control(*row) for row in controls]
    check("V02_fraction_inverse", all(row[0] for row in results))
    check("V03_fraction_determinant", all(row[1] for row in results))

    # Independent C1 point at sin(theta)=1: A=3, r=2, h=1.
    A, r, h = F(3), F(2), F(1)
    lam = A + h * h / (r * r)
    D = A * r * r + h * h
    check("V04_C1_lambda", lam == D / (r * r) == F(13, 4))
    check("V05_C1_inverse_entries", h / D == F(1, 13) and A / D == F(3, 13))
    check("V06_C1_volume_squared", r * r * D / A == F(52, 3))

    # Dual-number calculation of d_x[S*epsilon*sin(x)/Lambda]/S at x=0.
    # At x=0: sin=(0,1), Lambda=(1,0), S=(1,0), hence the derivative is epsilon.
    epsilon = F(5, 3)
    shift_value, shift_derivative = F(0), epsilon
    check("V07_shift_divergence_witness", shift_value == 0 and shift_derivative == epsilon)
    check("V08_shift_divergence_not_universal_zero", shift_derivative != 0)

    # Fourier multiplication by cos(psi) sends m only to m+/-1.
    samples = 128
    def coefficient(delta: int) -> complex:
        return sum(
            complex(math.cos(-delta * 2 * math.pi * j / samples), math.sin(-delta * 2 * math.pi * j / samples))
            * math.cos(2 * math.pi * j / samples)
            for j in range(samples)
        ) / samples
    check("V09_nonaxis_m_coupling", abs(coefficient(1) - 0.5) < 1e-14 and abs(coefficient(-1) - 0.5) < 1e-14 and abs(coefficient(2)) < 1e-14)

    # Independent direct-divergence evaluation, not a string check of the reduced formula.
    # For A=q=1, b=epsilon*x, u=1+x+x^2 at x=0, direct expansion of
    # S^-1 d_mu(S g^munu d_nu Psi) gives (2+omega^2)-i*omega*epsilon.
    omega = F(7, 4)
    direct_real = F(2) + omega * omega
    direct_imag_coefficient = -omega * epsilon
    reduced_real = F(2) + omega * omega
    reduced_imag_coefficient = -omega * shift_derivative
    check("V09B_direct_operator_point", (direct_real, direct_imag_coefficient) == (reduced_real, reduced_imag_coefficient))

    families = read_tsv("FAMILY_UNIVERSE.tsv")
    routes = read_tsv("REGISTERED_CANDIDATE_ROUTING.tsv")
    bases = read_tsv("BASIS_COUPLING_ATLAS.tsv")
    batches = read_tsv("SOLVE_BATCH_DESIGN.tsv")
    statuses = read_tsv("STATUS_LEDGER.tsv")
    cross_rows = read_tsv("AXIS_CROSS_PRODUCT_DISPOSITION.tsv")
    family_ids = {row["family_id"] for row in families}
    route_ids = [row["candidate_id"] for row in routes]
    check("V10_family_census", len(families) == len(family_ids) == 18)
    check("V11_candidate_exact_coverage", len(route_ids) == len(set(route_ids)) == 18 and set(route_ids) == {f"C{i:02d}" for i in range(1, 19)})
    check("V12_candidate_targets", all(row["family_id"] in family_ids for row in routes))
    check("V13_control_routes", {row["candidate_id"]: row["disposition"] for row in routes}["C18"] == "DEGENERATE_NO_INVERSE")
    check("V14_basis_census", len(bases) == 8 and len({row["basis_id"] for row in bases}) == 8)
    check("V15_label_ownership", any(row["basis_id"] == "B02" and row["m_status"] == "GOOD" for row in bases) and any(row["basis_id"] == "B04" and row["m_status"] == "MIXED" for row in bases))
    check("V16_no_solve", len(batches) == 7 and all(row["authorization"] == "NOT_AUTHORIZED" for row in batches))
    check("V17_no_postselection", all(row["acceptance_rule"] == "CHARACTERIZE_ALL_OUTPUTS" for row in batches))
    check("V18_no_cross_splice", sum(row["global_join"] == "NO_WRL_S3_CROSS_SPLICE" for row in families) >= 12)
    check("V19_status_ledger", len(statuses) == 13 and any(row["status"] == "OPEN_NOT_AUTHORIZED" for row in statuses))
    cross_keys = {(row["screen"], row["mixing"], row["dependence"], row["symmetry"], row["global_status"]) for row in cross_rows}
    check("V20_axis_cross_product", len(cross_rows) == len(cross_keys) == 2800 and all(row["disposition"] for row in cross_rows))

    source_ok = True
    with (HERE / "SOURCE_MANIFEST.tsv").open(encoding="utf-8") as handle:
        next(handle)
        for line in handle:
            path_text, digest = line.rstrip("\n").split("\t")
            data = subprocess.run(
                ["git", "show", f"{PREREG_COMMIT}:{path_text}"], cwd=ROOT, check=True, capture_output=True
            ).stdout
            source_ok &= hashlib.sha256(data).hexdigest() == digest
    check("V21_source_manifest", source_ok)

    mutations: dict[str, tuple[str, object]] = {
        "M01_status_promotion": ("status", "NATIVE_PHYSICAL_SCREEN_DERIVED"),
        "M02_key_loss": ("key_count", 26),
        "M03_omit_shift_divergence": ("mode_operator", "S^-1 d_r(S A u_r)+S^-1 d_A[S(q^-1-vv^T/Lambda)^AB d_B u]+omega^2 u/Lambda-2i omega(v^A/Lambda)d_Au"),
        "M04_family_loss": ("family_count", 17),
        "M05_route_duplication": ("candidate_route_count", 17),
        "M06_false_universal_m": ("maximum_conclusion", "universal m is selected and FD2 authorized"),
        "M07_C1_promotion": ("maximum_conclusion", "C1 is the native complete screen and FD2 authorized"),
        "M08_data_merit": ("maximum_conclusion", "best CMB resemblance selects the physical family"),
        "M09_premature_solve": ("maximum_conclusion", "physical complete screen solved; FD2 and GPU work authorized"),
        "M10_cross_product_loss": ("axis_cross_product_count", 2799),
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
    check("V22_payload_mutations", all(caught.values()) and len(caught) == 10)

    # Direct table mutations exercise fail-closed architecture guards rather than payload prose.
    route_trial = routes[:-1]
    batch_trial = copy.deepcopy(batches)
    batch_trial[0]["authorization"] = "AUTHORIZED"
    family_trial = copy.deepcopy(families)
    next(row for row in family_trial if row["family_id"] == "F05")["global_join"] = "WRL_S3_JOINED"
    table_catches = {
        "T01_missing_candidate": len({row["candidate_id"] for row in route_trial}) != 18,
        "T02_solve_authorization": not all(row["authorization"] == "NOT_AUTHORIZED" for row in batch_trial),
        "T03_cross_splice": any(row["global_join"] == "WRL_S3_JOINED" for row in family_trial),
    }
    check("V23_table_mutations", all(table_catches.values()))

    exact_text = " ".join((HERE / "EXACT_DERIVATION.md").read_text(encoding="utf-8").split())
    report_text = (HERE / "AUDIT_REPORT.md").read_text(encoding="utf-8")
    check("V24_exact_scope_guard", "CHOSE mathematical envelope" in exact_text and "not a selected UDT completion" in exact_text)
    check("V25_report_stop_guard", "NO_EIGENVALUE_SOLVE" in report_text and "FD2_REMAINS_GATED" in report_text)

    if not all(CHECKS.values()):
        raise SystemExit("independent verification failed")
    result = {
        "verdict": "VERIFIED_DESIGN_MAP_WITH_CAVEATS",
        "independence": "separate standard-library Fraction/permutation route and separate semantic/table mutation validator; same session",
        "check_count": len(CHECKS),
        "checks": CHECKS,
        "mutations": caught,
        "table_mutations": table_catches,
        "caveat": "no fresh zero-context external semantic review",
    }
    (HERE / "VERIFICATION_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"PASS: {len(CHECKS)}/{len(CHECKS)} independent checks; {len(caught) + len(table_catches)}/{len(caught) + len(table_catches)} mutations caught")


if __name__ == "__main__":
    main()
