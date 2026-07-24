#!/usr/bin/env python3
"""Independent stdlib verification of the clock/angular solder audit."""

from __future__ import annotations

import copy
import csv
import hashlib
import json
import math
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def read_tsv(name: str) -> list[dict[str, str]]:
    with (HERE / name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def require(label: str, condition: bool, checks: dict[str, str]) -> None:
    if not condition:
        raise AssertionError(label)
    checks[label] = "PASS"


def close(actual: float, expected: float, rtol: float = 2e-6, atol: float = 2e-7) -> bool:
    return abs(actual - expected) <= atol + rtol * abs(expected)


def derivatives(function, x: float, h: float = 1e-4) -> tuple[float, float]:
    fm2 = function(x - 2 * h)
    fm1 = function(x - h)
    f0 = function(x)
    fp1 = function(x + h)
    fp2 = function(x + 2 * h)
    first = (fm2 - 8 * fm1 + 8 * fp1 - fp2) / (12 * h)
    second = (-fp2 + 16 * fp1 - 30 * f0 + 16 * fm1 - fm2) / (12 * h * h)
    return first, second


def scalar_from_lapse(function, eta: float) -> float:
    first, second = derivatives(function, eta)
    laplace_ratio = (second + 2 / math.tan(2 * eta) * first) / function(eta)
    return 6.0 - 2.0 * laplace_ratio


def N1(eta: float, kappa: float) -> float:
    return math.tan(eta) ** (-1.0 / (2.0 * kappa))


def N2(eta: float, kappa: float) -> float:
    return math.sin(2 * eta) * math.tan(eta) ** (-1.0 / kappa)


def R1_exact(eta: float, kappa: float) -> float:
    return 6.0 - 2.0 / (kappa * kappa * math.sin(2 * eta) ** 2)


def R2_exact(eta: float, kappa: float) -> float:
    numerator = (
        3 * kappa * kappa * math.sin(2 * eta) ** 2
        - 4 * kappa * kappa * math.cos(4 * eta)
        + 8 * kappa * math.cos(2 * eta)
        - 4
    )
    return 2 * numerator / (kappa * kappa * math.sin(2 * eta) ** 2)


def validate_semantics(
    families: list[dict[str, str]],
    caps: list[dict[str, str]],
    pairs: list[dict[str, str]],
    opens: list[dict[str, str]],
    statuses: list[dict[str, str]],
    preregistration: str,
) -> None:
    by_family = {row["family_id"]: row for row in families}
    if len(families) != 6 or len(by_family) != 6:
        raise AssertionError("family coverage")
    if list(by_family) != [f"F0{index}" for index in range(1, 7)]:
        raise AssertionError("family order")
    if len(caps) != 5:
        raise AssertionError("cap coverage")
    if {row["case"] for row in pairs} != {
        "GENERIC_KAPPA_NOT_ONE",
        "KAPPA_EQUALS_ONE",
        "SAME_SIGN_PROPOSED_PAIR",
    }:
        raise AssertionError("pair coverage")
    pair_by_case = {row["case"]: row for row in pairs}
    if pair_by_case["SAME_SIGN_PROPOSED_PAIR"]["ruling"] != "FAILS_FIXED_K_INVARIANCE":
        raise AssertionError("same sign pairing")
    if (
        "finite `kappa>0`" not in preregistration
        or "free and explored analytically over all" not in preregistration
    ):
        raise AssertionError("kappa domain")
    if any(
        row["compact_two_cap_pass"] == "YES"
        for row in families
        if row["family_id"] in {"F01", "F02", "F03", "F04"}
    ):
        raise AssertionError("false compact pass")
    if by_family["F03"]["classification"] != (
        "OBSTRUCTED_FOR_SMOOTH_POSITIVE_NONZERO_COMMON_FACTOR"
    ):
        raise AssertionError("common factor")
    if by_family["F04"]["classification"] != "OPEN_INFINITE_PROFILE_FAMILY":
        raise AssertionError("open family")
    if by_family["F06"]["classification"] != "OPEN_OUTSIDE_BOUNDED_CLASS":
        raise AssertionError("outside scope")
    open_by_quantity = {row["quantity"]: row for row in opens}
    if open_by_quantity["finite_positive_endpoint"]["selected"] != "NO":
        raise AssertionError("profile selection")
    if open_by_quantity["angular_global_diameter"]["selected"] != "NO":
        raise AssertionError("diameter promotion")
    status_by_claim = {row["claim"]: row for row in statuses}
    if status_by_claim["global_Xmax"]["status"] != "OPEN_NOT_EVALUABLE":
        raise AssertionError("Xmax promotion")
    if status_by_claim["same_scalar_globally_impossible_in_UDT"]["status"] != "NOT_DERIVED":
        raise AssertionError("global no-go")


def expect_failure(label: str, callback, catches: dict[str, str]) -> None:
    try:
        callback()
    except AssertionError:
        catches[label] = "PASS"
        return
    raise AssertionError(f"catch accepted corruption: {label}")


def validate_sources(corrupt: bool = False) -> None:
    rows = read_tsv("SOURCE_LINEAGE.tsv")
    if len(rows) != 8:
        raise AssertionError("source coverage")
    for index, row in enumerate(rows):
        expected = row["sha256"]
        if corrupt and index == 0:
            expected = "0" * 64
        actual = hashlib.sha256((ROOT / row["path"]).read_bytes()).hexdigest()
        if actual != expected:
            raise AssertionError("source identity")


def main() -> None:
    checks: dict[str, str] = {}
    catches: dict[str, str] = {}

    result_bytes = (HERE / "DERIVATION_RESULT.json").read_bytes()
    result = json.loads(result_bytes)
    families = read_tsv("SOLDER_CLASSIFICATION.tsv")
    caps = read_tsv("CAP_REGULARITY_LEDGER.tsv")
    pairs = read_tsv("PAIRING_CLASSIFICATION.tsv")
    opens = read_tsv("OPEN_PROFILE_LEDGER.tsv")
    statuses = read_tsv("STATUS_LEDGER.tsv")
    preregistration = (HERE / "PREREGISTRATION.md").read_text(encoding="utf-8")

    validate_semantics(families, caps, pairs, opens, statuses, preregistration)
    require("semantic_ledgers", True, checks)

    # Direct fixed-pairing exponent arithmetic, separate from SymPy.
    for kappa in (0.25, 0.5, 1.0, 2.0, 4.0):
        weights = (-1.0, 1.0, -kappa, kappa)
        require(
            f"determinant_weight_sum_{kappa}",
            abs(sum(weights)) < 1e-15,
            checks,
        )
        edges = {
            (i, j)
            for i in range(4)
            for j in range(i + 1, 4)
            if abs(weights[i] + weights[j]) < 1e-14
        }
        expected = (
            {(0, 1), (0, 3), (1, 2), (2, 3)}
            if kappa == 1.0
            else {(0, 1), (2, 3)}
        )
        require(f"pair_edges_{kappa}", edges == expected, checks)

    # Independent five-point coordinate derivatives of the 4D scalar curvature.
    for kappa in (0.5, 1.0, 2.0):
        for eta in (0.31, 0.67, 1.07):
            require(
                f"F01_curvature_fd_{kappa}_{eta}",
                close(
                    scalar_from_lapse(lambda value: N1(value, kappa), eta),
                    R1_exact(eta, kappa),
                    rtol=8e-6,
                ),
                checks,
            )
            require(
                f"F02_curvature_fd_{kappa}_{eta}",
                close(
                    scalar_from_lapse(lambda value: N2(value, kappa), eta),
                    R2_exact(eta, kappa),
                    rtol=8e-6,
                ),
                checks,
            )

    epsilon = 1e-6
    for kappa in (0.5, 1.0, 2.0):
        require(
            f"F01_minus_pole_{kappa}",
            close(epsilon**2 * R1_exact(epsilon, kappa), -1 / (2 * kappa**2), rtol=2e-5),
            checks,
        )
        require(
            f"F01_plus_pole_{kappa}",
            close(
                epsilon**2 * R1_exact(math.pi / 2 - epsilon, kappa),
                -1 / (2 * kappa**2),
                rtol=2e-5,
            ),
            checks,
        )
        if kappa != 1.0:
            require(
                f"F02_minus_pole_{kappa}",
                close(
                    epsilon**2 * R2_exact(epsilon, kappa),
                    -2 * (1 - 1 / kappa) ** 2,
                    rtol=3e-4,
                    atol=3e-8,
                ),
                checks,
            )
        require(
            f"F02_plus_pole_{kappa}",
            close(
                epsilon**2 * R2_exact(math.pi / 2 - epsilon, kappa),
                -2 * (1 + 1 / kappa) ** 2,
                rtol=3e-4,
                atol=3e-8,
            ),
            checks,
        )
    require("F02_kappa_one_minus_regular", close(R2_exact(1e-4, 1.0), 14.0, rtol=2e-7), checks)

    # A smooth positive nonzero physical factor contributes only finite terms.
    alpha = 0.3

    def omega(value: float) -> float:
        return 1 + alpha * math.sin(2 * value) ** 2

    def conformal_scalar(value: float, kappa: float) -> float:
        q = lambda point: math.log(omega(point))
        q1, q2 = derivatives(q, value)
        n = lambda point: N1(point, kappa)
        n1, _ = derivatives(n, value)
        box_q = q2 + (2 / math.tan(2 * value) + n1 / n(value)) * q1
        return (R1_exact(value, kappa) - 6 * box_q - 6 * q1 * q1) / omega(value) ** 2

    for kappa in (0.5, 1.0, 2.0):
        require(
            f"F03_minus_pole_persists_{kappa}",
            close(
                epsilon**2 * conformal_scalar(epsilon, kappa),
                -1 / (2 * kappa**2),
                rtol=3e-4,
            ),
            checks,
        )
        require(
            f"F03_plus_pole_persists_{kappa}",
            close(
                epsilon**2 * conformal_scalar(math.pi / 2 - epsilon, kappa),
                -1 / (2 * kappa**2),
                rtol=3e-4,
            ),
            checks,
        )

    validate_sources()
    for row in read_tsv("SOURCE_LINEAGE.tsv"):
        actual = hashlib.sha256((ROOT / row["path"]).read_bytes()).hexdigest()
        require(f"source_{row['id']}", actual == row["sha256"], checks)

    require("production_check_count", result["check_count"] == 37, checks)
    require("production_checks_pass", set(result["checks"].values()) == {"PASS"}, checks)
    require("production_family_count", result["family_count"] == 6, checks)
    require("production_compact_pass_zero", result["compact_same_scalar_pass_count"] == 0, checks)

    args = [families, caps, pairs, opens, statuses, preregistration]

    bad = copy.deepcopy(families)
    bad.pop()
    expect_failure(
        "missing_family",
        lambda: validate_semantics(bad, *args[1:]),
        catches,
    )
    bad = copy.deepcopy(families)
    bad.append(copy.deepcopy(bad[0]))
    expect_failure(
        "duplicate_family",
        lambda: validate_semantics(bad, *args[1:]),
        catches,
    )
    bad_pairs = copy.deepcopy(pairs)
    next(row for row in bad_pairs if row["case"] == "SAME_SIGN_PROPOSED_PAIR")[
        "ruling"
    ] = "ALLOWED"
    expect_failure(
        "same_sign_pair",
        lambda: validate_semantics(families, caps, bad_pairs, opens, statuses, preregistration),
        catches,
    )
    bad = copy.deepcopy(families)
    next(row for row in bad if row["family_id"] == "F02")["compact_two_cap_pass"] = "YES"
    expect_failure(
        "false_two_cap_pass",
        lambda: validate_semantics(bad, caps, pairs, opens, statuses, preregistration),
        catches,
    )
    bad = copy.deepcopy(families)
    next(row for row in bad if row["family_id"] == "F03")["classification"] = "REPAIRED_BY_CSN"
    expect_failure(
        "false_common_factor_repair",
        lambda: validate_semantics(bad, caps, pairs, opens, statuses, preregistration),
        catches,
    )
    bad = copy.deepcopy(families)
    next(row for row in bad if row["family_id"] == "F04")["classification"] = "UNIQUE_PROFILE"
    expect_failure(
        "false_profile_selection",
        lambda: validate_semantics(bad, caps, pairs, opens, statuses, preregistration),
        catches,
    )
    bad = copy.deepcopy(families)
    next(row for row in bad if row["family_id"] == "F06")["classification"] = "GLOBALLY_OBSTRUCTED"
    expect_failure(
        "false_scope_extension",
        lambda: validate_semantics(bad, caps, pairs, opens, statuses, preregistration),
        catches,
    )
    bad_open = copy.deepcopy(opens)
    next(row for row in bad_open if row["quantity"] == "finite_positive_endpoint")[
        "selected"
    ] = "YES"
    expect_failure(
        "false_endpoint_selection",
        lambda: validate_semantics(families, caps, pairs, bad_open, statuses, preregistration),
        catches,
    )
    bad_status = copy.deepcopy(statuses)
    next(row for row in bad_status if row["claim"] == "global_Xmax")["status"] = "DERIVED"
    expect_failure(
        "false_Xmax",
        lambda: validate_semantics(families, caps, pairs, opens, bad_status, preregistration),
        catches,
    )
    expect_failure(
        "single_kappa_scope",
        lambda: validate_semantics(
            families,
            caps,
            pairs,
            opens,
            statuses,
            preregistration.replace(
                "free and explored analytically over all", "fixed at kappa=1"
            ),
        ),
        catches,
    )
    expect_failure(
        "source_identity",
        lambda: validate_sources(corrupt=True),
        catches,
    )

    output = {
        "schema": "udt-clock-angular-solder-independent-verification-1.0",
        "implementation": "python_stdlib_five_point_coordinate_derivatives_no_production_import",
        "status": "PASS",
        "check_count": len(checks),
        "checks": checks,
        "catch_count": len(catches),
        "catches": catches,
        "family_count": len(families),
        "source_count": len(read_tsv("SOURCE_LINEAGE.tsv")),
        "derivation_sha256": hashlib.sha256(result_bytes).hexdigest(),
        "classification_sha256": hashlib.sha256(
            (HERE / "SOLDER_CLASSIFICATION.tsv").read_bytes()
        ).hexdigest(),
        "cap_ledger_sha256": hashlib.sha256(
            (HERE / "CAP_REGULARITY_LEDGER.tsv").read_bytes()
        ).hexdigest(),
    }
    (HERE / "INDEPENDENT_VERIFICATION.json").write_text(
        json.dumps(output, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print("status=PASS")
    print(f"checks={len(checks)}")
    print(f"catches={len(catches)}")
    print(f"families={len(families)}")
    print(
        "independent_sha256="
        + hashlib.sha256((HERE / "INDEPENDENT_VERIFICATION.json").read_bytes()).hexdigest()
    )


if __name__ == "__main__":
    main()
