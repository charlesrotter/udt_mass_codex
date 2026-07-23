#!/usr/bin/env python3
"""Independent stdlib verifier for the metric-pure frame rederivation."""

from __future__ import annotations

import csv
import hashlib
import json
import subprocess
from fractions import Fraction as F
from pathlib import Path


EXPECTED_MAXIMUM = (
    "THE_METRIC_PURE_PARENT_IS_THE_FOUR_DIMENSIONAL_CONFORMAL_LORENTZIAN_"
    "METRIC_COFRAME_CLASS_NOT_WRL;IT_DERIVES_NO_PREFERRED_LOCAL_TIMELIKE_"
    "OBSERVER_AND_EXACT_LOCAL_SO_PLUS_1_3_FRAME_RECIPROCITY_WITH_A_COMMON_"
    "NULL_CONE;IT_DOES_NOT_DERIVE_GLOBAL_ISOMETRIC_RECENTERING_OR_AN_"
    "OBSERVER_INDEXED_PAIR_METRIC;WRL_IS_A_ONE_FUNCTION_STATIC_SPHERICAL_"
    "DIAGONAL_AREAL_ZERO_SHIFT_REDUCTION_NOT_CLOSED_AS_A_COMPLETE_FRAME_"
    "RECIPROCAL_CONFIGURATION_SPACE;ITS_PROFILE_ASYMPTOTE_AND_SNE_READOUT_"
    "SURVIVE_ONLY_IN_THAT_REDUCTION;PHYSICAL_ACCELERATION_INDUCED_METRIC_"
    "WARPING_REMAINS_OPEN"
)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def eye(n: int) -> list[list[F]]:
    return [[F(int(i == j)) for j in range(n)] for i in range(n)]


def transpose(a: list[list[F]]) -> list[list[F]]:
    return [list(row) for row in zip(*a)]


def matmul(a: list[list[F]], b: list[list[F]]) -> list[list[F]]:
    return [
        [sum((a[i][k] * b[k][j] for k in range(len(b))), F(0)) for j in range(len(b[0]))]
        for i in range(len(a))
    ]


def matsub(a: list[list[F]], b: list[list[F]]) -> list[list[F]]:
    return [[a[i][j] - b[i][j] for j in range(len(a[0]))] for i in range(len(a))]


def matvec(a: list[list[F]], v: list[F]) -> list[F]:
    return [sum((a[i][j] * v[j] for j in range(len(v))), F(0)) for i in range(len(a))]


def rank(matrix: list[list[F]]) -> int:
    work = [row[:] for row in matrix]
    rows = len(work)
    cols = len(work[0])
    pivot_row = 0
    for col in range(cols):
        pivot = next((r for r in range(pivot_row, rows) if work[r][col] != 0), None)
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        scale = work[pivot_row][col]
        work[pivot_row] = [value / scale for value in work[pivot_row]]
        for r in range(rows):
            if r == pivot_row:
                continue
            factor = work[r][col]
            if factor:
                work[r] = [
                    work[r][j] - factor * work[pivot_row][j] for j in range(cols)
                ]
        pivot_row += 1
    return pivot_row


def boost(axis: int) -> list[list[F]]:
    matrix = eye(4)
    matrix[0][0] = F(5, 4)
    matrix[axis][axis] = F(5, 4)
    matrix[0][axis] = F(3, 4)
    matrix[axis][0] = F(3, 4)
    return matrix


def inner(a: list[F], b: list[F]) -> F:
    return -a[0] * b[0] + sum((a[i] * b[i] for i in range(1, 4)), F(0))


def verify_manifest(package: Path) -> tuple[int, bool]:
    count = 0
    ok = True
    for line in package.joinpath("MANIFEST.sha256").read_text().splitlines():
        if not line:
            continue
        expected, rel = line.split("  ", 1)
        ok = ok and digest(package / rel) == expected
        count += 1
    return count, ok


def main() -> int:
    package = Path(__file__).resolve().parent
    root = package.parent
    production = json.loads(package.joinpath("DERIVATION_RESULT.json").read_text())
    checks: list[tuple[str, bool]] = []

    def check(name: str, condition: bool) -> None:
        checks.append((name, bool(condition)))

    token = "derive_" + "metric_pure_frames"
    check("does_not_import_production", token not in Path(__file__).read_text())
    check("production_pass", production["all_checks_pass"] is True)
    check("maximum_exact", production["maximum_conclusion"] == EXPECTED_MAXIMUM)
    check("production_checks", production["check_count"] == 69)
    check("production_semantic_catches", production["semantic_catch_count"] == 18)

    eta = [[F(-1), F(0), F(0), F(0)], [F(0), F(1), F(0), F(0)], [F(0), F(0), F(1), F(0)], [F(0), F(0), F(0), F(1)]]
    boosts = [boost(axis) for axis in (1, 2, 3)]
    for idx, matrix in enumerate(boosts, 1):
        check(f"boost_{idx}_metric", matmul(matmul(transpose(matrix), eta), matrix) == eta)
        check(f"boost_{idx}_future", matrix[0][0] > 0)
    fixed = []
    identity = eye(4)
    for matrix in boosts:
        fixed.extend(matsub(matrix, identity))
    check("no_fixed_vector_rank", rank(fixed) == 4)

    u = [F(1), F(0), F(0), F(0)]
    v = [F(5, 4), F(3, 4), F(0), F(0)]
    n = [F(0), F(1), F(0), F(0)]
    check("u_unit", inner(u, u) == -1)
    check("v_unit", inner(v, v) == -1)
    check("pair_gamma", -inner(u, v) == F(5, 4))
    check("n_unit", inner(n, n) == 1)
    check("u_n", inner(u, n) == 0)
    check("reciprocal_speed_magnitude", F(3, 5) == v[1] / v[0])
    kplus = [F(1), F(1), F(0), F(0)]
    check("null_before", inner(kplus, kplus) == 0)
    check("null_after", inner(matvec(boosts[0], kplus), matvec(boosts[0], kplus)) == 0)

    Bx, By = boosts[0], boosts[1]
    product_xy = matmul(Bx, By)
    product_yx = matmul(By, Bx)
    check("noncommutative", product_xy != product_yx)
    composed = matvec(product_xy, u)
    check("composed_exact", composed == [F(25, 16), F(15, 16), F(3, 4), F(0)])
    check("composed_unit", inner(composed, composed) == -1)
    Bv = [
        [F(25, 16), F(15, 16), F(3, 4), F(0)],
        [F(15, 16), F(881, 656), F(45, 164), F(0)],
        [F(3, 4), F(45, 164), F(50, 41), F(0)],
        [F(0), F(0), F(0), F(1)],
    ]
    rotation = [
        [F(1), F(0), F(0), F(0)],
        [F(0), F(40, 41), F(9, 41), F(0)],
        [F(0), F(-9, 41), F(40, 41), F(0)],
        [F(0), F(0), F(0), F(1)],
    ]
    check("boost_rotation_factorization", matmul(Bv, rotation) == product_xy)
    check("derived_boost_metric", matmul(matmul(transpose(Bv), eta), Bv) == eta)
    check("rotation_metric", matmul(matmul(transpose(rotation), eta), rotation) == eta)
    check("rotation_fixes_observer", matvec(rotation, u) == u)
    check("rotation_nontrivial", rotation[1][2] == F(9, 41))
    check("rotation_circle_identity", F(40, 41) ** 2 + F(9, 41) ** 2 == 1)

    # Positive common scaling and renormalization leave pair gamma unchanged.
    Omega = F(3)
    us = [value / Omega for value in u]
    vs = [value / Omega for value in v]
    scaled_inner = lambda a, b: Omega**2 * inner(a, b)
    check("CSN_u_unit", scaled_inner(us, us) == -1)
    check("CSN_v_unit", scaled_inner(vs, vs) == -1)
    check("CSN_gamma", -scaled_inner(us, vs) == F(5, 4))
    check("CSN_null", Omega**2 * inner(kplus, kplus) == 0)

    # Independent numeric pullback of the WR-L radial block.
    A = F(1, 2)
    b = F(3, 5)
    gamma_b = F(5, 4)
    jac = [[gamma_b, gamma_b * b], [gamma_b * b, gamma_b]]
    radial = [[-A, F(0)], [F(0), 1 / A]]
    mixed = matmul(matmul(transpose(jac), radial), jac)
    check("WRL_cross_witness", mixed[0][1] == F(45, 32))
    flat = [[F(-1), F(0)], [F(0), F(1)]]
    check("flat_cross_zero", matmul(matmul(transpose(jac), flat), jac)[0][1] == 0)

    expected_rows = {
        "PREMISE_LEDGER.tsv": 19,
        "SOURCE_UNIVERSE.tsv": 18,
        "METRIC_PARENT_LEDGER.tsv": 12,
        "WRL_REDUCTION_LEDGER.tsv": 16,
        "FRAME_RECIPROCITY_LEDGER.tsv": 16,
        "WRL_SURVIVAL_LEDGER.tsv": 16,
        "STATUS_LEDGER.tsv": 35,
        "CATCH_PROOFS.tsv": 22,
    }
    for name, expected in expected_rows.items():
        check(f"{name}_rows", len(read_tsv(package / name)) == expected)

    statuses = {row["claim_id"]: row["status"] for row in read_tsv(package / "STATUS_LEDGER.tsv")}
    check("WRL_not_parent", statuses["Q01"] == "REFUTED_BY_SOURCE_CENSUS")
    check("local_reciprocity", statuses["Q04"] == "DERIVED_LOCAL")
    check("nonabelian", statuses["Q10"] == "REFUTED")
    check("screen_rotation", statuses["Q11"] == "DERIVED_LOCAL")
    check("rapidity_phi_open", statuses["Q13"] == "OPEN_NOT_JOINED")
    check("global_recenter_excluded", statuses["Q14"] == "FALSE_EXCLUDED")
    check("WRL_reduction_count", statuses["Q17"] == "DERIVED_REDUCTION_CENSUS")
    check("acceleration_response_open", statuses["Q30"] == "OPEN")
    check("no_carrier_promotion", statuses["Q35"] == "NO")

    catches = read_tsv(package / "CATCH_PROOFS.tsv")
    check("catch_count", len(catches) == 22)
    check("all_catches_fail_closed", all(row["expected_result"] == "FAIL" for row in catches))
    check("catch_ids_unique", len({row["catch_id"] for row in catches}) == 22)

    report = package.joinpath("AUDIT_REPORT.md").read_text()
    lay = package.joinpath("LAY_REPORT.md").read_text()
    next_step = package.joinpath("NEXT_STEP.md").read_text()
    check("report_scope", "local kinematic theorem, not a global homogeneity theorem" in report)
    check("report_rotation", "40/41" in report and "9/41" in report)
    check("report_WRL_one_function", "one independent function from ten metric components" in report)
    check("lay_orchestra", "reduced that orchestra to one instrument" in lay)
    check("next_step_separates_phi", "keep observer rapidity and local metric `phi` distinct" in next_step)

    for source in production["source_hashes"]:
        path = root / source["path"]
        check(f"source_{source['path']}", path.exists() and digest(path) == source["sha256"])

    parent = root / "udt_observer_centered_xmax_frame_correction_2026-07-23"
    parent_count, parent_ok = verify_manifest(parent)
    check("parent_manifest_entries", parent_count == 22)
    check("parent_manifest_replay", parent_ok)
    check(
        "parent_manifest_identity",
        digest(parent / "MANIFEST.sha256")
        == "024e32b90f0ba6fe7ef56b957f04cc88d375a9325597832d60d887768b7ab57b",
    )
    diff = subprocess.run(
        ["git", "diff", "--quiet", "db069753808425b8f4cb7df481c8c881918ced80", "--", parent.name],
        cwd=root,
        check=False,
    )
    check("parent_unchanged", diff.returncode == 0)

    output = {
        "schema": "udt-metric-pure-frame-independent-1.0",
        "method": "stdlib_fraction_Lorentz_group_reduction_and_semantic_audit",
        "imports_production_module": False,
        "all_checks_pass": all(value for _, value in checks),
        "check_count": len(checks),
        "catch_count": len(catches),
        "source_hash_checks": len(production["source_hashes"]),
        "parent_manifest_entries": parent_count,
        "failed_checks": [name for name, value in checks if not value],
        "grade": "VERIFIED-WITH-CAVEATS",
    }
    text = json.dumps(output, indent=2, sort_keys=True) + "\n"
    package.joinpath("INDEPENDENT_VERIFICATION.json").write_text(text, encoding="utf-8")
    print(text, end="")
    return 0 if output["all_checks_pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
