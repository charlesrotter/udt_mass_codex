#!/usr/bin/env python3
"""Exact longitudinal/transverse observer-cocycle audit."""

from __future__ import annotations

import csv
import hashlib
import json
import subprocess
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
PREREG_COMMIT = "563564951ec8761ce2e253d1cf3929d9644ae4cf"
RATIO_CLARIFICATION_COMMIT = "41ff2101f9244b2390dcac43bbe1b6b91bc3e163"
SOURCE_BASE = "dc81c489b9e27bd86b2d58d93fbacf4a4fd01496"


def check(checks: dict[str, str], name: str, condition: object) -> None:
    if not bool(condition):
        raise AssertionError(name)
    checks[name] = "PASS"


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def write_tsv(
    name: str, fields: list[str], rows: list[dict[str, object]]
) -> None:
    with (HERE / name).open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle, fieldnames=fields, delimiter="\t", lineterminator="\n"
        )
        writer.writeheader()
        writer.writerows(rows)


def S(delta: sp.Expr) -> sp.Matrix:
    return sp.diag(sp.exp(-delta), sp.exp(delta))


def round_M(length: sp.Expr, b: sp.Expr) -> sp.Matrix:
    c = sp.cos(length / b)
    s = sp.sin(length / b)
    return sp.Matrix([[c, b * s], [-s / b, c]])


def source_checks(checks: dict[str, str]) -> int:
    rows = read_tsv(HERE / "SOURCE_LINEAGE.tsv")
    check(checks, "source_count", len(rows) == 18)
    check(checks, "source_unique", len({row["path"] for row in rows}) == 18)
    for row in rows:
        path = ROOT / row["path"]
        check(checks, f"source_exists_{row['role']}", path.is_file())
        if row["role"] == "frontier_scope":
            data = subprocess.run(
                ["git", "show", f"{SOURCE_BASE}:{row['path']}"],
                cwd=ROOT,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=True,
            ).stdout
        else:
            data = path.read_bytes()
        check(
            checks,
            f"source_hash_{row['role']}",
            hashlib.sha256(data).hexdigest() == row["sha256"],
        )
    return len(rows)


def main() -> None:
    checks: dict[str, str] = {}
    I2 = sp.eye(2)
    Z2 = sp.zeros(2)
    Omega2 = sp.Matrix([[0, 1], [-1, 0]])
    Omega4 = sp.kronecker_product(Omega2, I2)

    # Generic metric Jacobi generator. Symmetric tidal curvature is the only
    # geometric input required for the canonical first-order structure.
    k11, k12, k22 = sp.symbols("k11 k12 k22", real=True)
    tidal = sp.Matrix([[k11, k12], [k12, k22]])
    generator = Z2.row_join(I2).col_join((-tidal).row_join(Z2))
    check(
        checks,
        "generic_jacobi_generator_is_symplectic",
        generator.T * Omega4 + Omega4 * generator == sp.zeros(4),
    )

    # Constant-curvature exact fundamental matrix and its path laws.
    L, L1, L2, b = sp.symbols("L L1 L2 b", positive=True)
    M1 = round_M(L1, b)
    M2 = round_M(L2, b)
    M12 = round_M(L1 + L2, b)
    check(
        checks,
        "round_scalar_fundamental_composition",
        all(sp.trigsimp(x) == 0 for x in (M2 * M1 - M12)),
    )
    check(
        checks,
        "round_scalar_symplectic",
        all(
            sp.trigsimp(x) == 0
            for x in (round_M(L, b).T * Omega2 * round_M(L, b) - Omega2)
        ),
    )
    check(
        checks,
        "round_scalar_determinant",
        sp.trigsimp(round_M(L, b).det()) == 1,
    )
    check(
        checks,
        "round_scalar_reversal",
        all(
            sp.trigsimp(x) == 0
            for x in (round_M(-L, b) * round_M(L, b) - sp.eye(2))
        ),
    )
    check(checks, "round_scalar_identity", round_M(0, b) == sp.eye(2))

    M4 = sp.kronecker_product(round_M(L, b), I2)
    check(
        checks,
        "round_two_screen_symplectic",
        all(sp.trigsimp(x) == 0 for x in (M4.T * Omega4 * M4 - Omega4)),
    )
    check(
        checks,
        "round_two_screen_determinant",
        sp.trigsimp(M4.det()) == 1,
    )

    # The vertex Jacobi map is the B block only. It does not multiply as a
    # stand-alone propagator; the missing A and D blocks are load-bearing.
    B1 = M1[0, 1]
    B2 = M2[0, 1]
    B12 = M12[0, 1]
    projected_false_difference = sp.simplify(
        (B12 - B2 * B1).subs({b: 1, L1: sp.pi / 3, L2: sp.pi / 3})
    )
    check(
        checks,
        "projected_jacobi_noncomposition_counterexample",
        projected_false_difference != 0,
    )
    check(
        checks,
        "correct_B_block_composition",
        sp.trigsimp(B12 - (M2[0, 0] * B1 + B2 * M1[1, 1])) == 0,
    )

    antipode = sp.simplify(round_M(sp.pi * b, b))
    check(checks, "round_antipode_full_matrix", antipode == -sp.eye(2))
    check(checks, "round_antipode_projected_block_zero", antipode[0, 1] == 0)
    check(checks, "round_antipode_full_matrix_invertible", antipode.det() == 1)

    # Endpoint frequency/lapse ratios and reciprocal matrices.
    N0, N1, N2 = sp.symbols("N0 N1 N2", positive=True)
    Q01 = N0 / N1
    Q12 = N1 / N2
    Q02 = N0 / N2
    check(checks, "clock_ratio_identity", sp.simplify(N0 / N0) == 1)
    check(checks, "clock_ratio_composition", sp.simplify(Q01 * Q12 - Q02) == 0)
    check(checks, "clock_ratio_reversal", sp.simplify(Q01 * (N1 / N0)) == 1)

    d01 = sp.log(Q01)
    d12 = sp.log(Q12)
    d02 = sp.log(Q02)
    check(
        checks,
        "reciprocal_matrix_composition",
        all(
            sp.powsimp(x, force=True) == 0
            for x in (S(d12) * S(d01) - S(d02))
        ),
    )
    check(
        checks,
        "reciprocal_matrix_reversal",
        all(
            sp.powsimp(x, force=True) == 0
            for x in (S(-d01) * S(d01) - sp.eye(2))
        ),
    )

    # Combined 2+4 block. This is a direct-sum cocycle, not yet a theorem
    # that the clock and screen channels form one irreducible UDT object.
    C01 = sp.diag(1, 1, 1, 1, 1, 1)
    C01[:2, :2] = S(d01)
    C01[2:, 2:] = sp.kronecker_product(M1, I2)
    C12 = sp.diag(1, 1, 1, 1, 1, 1)
    C12[:2, :2] = S(d12)
    C12[2:, 2:] = sp.kronecker_product(M2, I2)
    C02 = sp.diag(1, 1, 1, 1, 1, 1)
    C02[:2, :2] = S(d02)
    C02[2:, 2:] = sp.kronecker_product(M12, I2)
    check(
        checks,
        "combined_direct_sum_composition",
        all(sp.trigsimp(sp.powsimp(x, force=True)) == 0 for x in (C12 * C01 - C02)),
    )
    check(
        checks,
        "combined_direct_sum_unit_determinant",
        sp.trigsimp(sp.powsimp(C01.det(), force=True)) == 1,
    )

    # Endpoint screen covariance. Phase-space lifts of endpoint rotations
    # cancel at the intermediate event under concatenation.
    R0 = sp.eye(2)
    R1 = sp.Matrix([[0, -1], [1, 0]])
    R2 = -sp.eye(2)
    G0 = sp.diag(1, 1, 1, 1)
    G0[:2, :2], G0[2:, 2:] = R0, R0
    G1 = sp.diag(1, 1, 1, 1)
    G1[:2, :2], G1[2:, 2:] = R1, R1
    G2 = sp.diag(1, 1, 1, 1)
    G2[:2, :2], G2[2:, 2:] = R2, R2
    M01_4 = sp.kronecker_product(M1, I2)
    M12_4 = sp.kronecker_product(M2, I2)
    M02_4 = sp.kronecker_product(M12, I2)
    cov01 = G1 * M01_4 * G0.T
    cov12 = G2 * M12_4 * G1.T
    cov02 = G2 * M02_4 * G0.T
    check(
        checks,
        "intermediate_screen_gauge_cancels",
        all(sp.trigsimp(x) == 0 for x in (cov12 * cov01 - cov02)),
    )
    check(checks, "screen_phase_lifts_orthogonal", G1.T * G1 == sp.eye(4))

    # WR-L local radial control.
    D, X = sp.symbols("D X", positive=True)
    N = 1 - D / (2 * X)
    R = D - D**2 / (4 * X)
    phi = -sp.log(N)
    K_rad = sp.simplify(1 / (2 * X * R))
    check(
        checks,
        "wrl_radial_jacobi_equation",
        sp.simplify(sp.diff(R, D, 2) + K_rad * R) == 0,
    )
    check(
        checks,
        "wrl_centered_clock_is_exp_phi",
        sp.simplify(sp.powsimp(1 / N - sp.exp(phi), force=True)) == 0,
    )
    check(checks, "wrl_centered_vertex_data_R0", R.subs(D, 0) == 0)
    check(checks, "wrl_centered_vertex_data_Rprime0", sp.diff(R, D).subs(D, 0) == 1)
    A_wrl = sp.Matrix([[0, 1], [-K_rad, 0]])
    check(
        checks,
        "wrl_first_order_generator_symplectic",
        sp.simplify(A_wrl.T * Omega2 + Omega2 * A_wrl) == sp.zeros(2),
    )

    # Frozen registry coverage.
    completions = read_tsv(
        ROOT
        / "udt_center_free_observer_optical_correspondence_audit_2026-07-24"
        / "COMPLETION_OPTICAL_ATLAS.tsv"
    )
    equations = read_tsv(
        ROOT
        / "udt_center_free_observer_optical_correspondence_audit_2026-07-24"
        / "EQUATION_FAMILY_OPTICAL_SCREEN.tsv"
    )
    check(checks, "completion_count", len(completions) == 12)
    check(
        checks,
        "completion_id_unique",
        len({row["completion_id"] for row in completions}) == 12,
    )
    check(checks, "equation_family_count", len(equations) == 28)
    check(
        checks,
        "equation_family_id_unique",
        len({row["family_id"] for row in equations}) == 28,
    )
    source_count = source_checks(checks)

    types = [
        {
            "object": "ENDPOINT_CLOCK_RATIO_Q",
            "space": "POSITIVE_SCALAR",
            "composition": "YES_MATCHED_ENDPOINT_OBSERVER_EVENT",
            "caustic_behavior": "UNAFFECTED",
            "status": "DERIVED_GIVEN_OBSERVERS_PATH_AND_EVENTS",
        },
        {
            "object": "RECIPROCAL_MATRIX_S_LOG_Q",
            "space": "TWO_CLOCK_RULER_CHANNELS",
            "composition": "YES_IF_Q_COMPOSES",
            "caustic_behavior": "UNAFFECTED",
            "status": "CONDITIONAL_SOLDER_TO_FOUNDING_OPERATOR",
        },
        {
            "object": "VERTEX_JACOBI_MAP_J",
            "space": "INITIAL_SCREEN_ANGLE_TO_ENDPOINT_SEPARATION",
            "composition": "NO_NOT_STANDALONE",
            "caustic_behavior": "CAN_BECOME_SINGULAR",
            "status": "DERIVED_PROJECTED_READOUT",
        },
        {
            "object": "FULL_TRANSVERSE_PROPAGATOR_M",
            "space": "SCREEN_POSITION_PLUS_SCREEN_DERIVATIVE",
            "composition": "YES_PATH_GROUPOID",
            "caustic_behavior": "REMAINS_INVERTIBLE",
            "status": "DERIVED_GIVEN_METRIC_PATH",
        },
        {
            "object": "DIRECT_SUM_C",
            "space": "RECIPROCAL_TWO_CHANNEL_PLUS_TRANSVERSE_PHASE_SPACE",
            "composition": "YES_IF_SAME_PATH_EVENT_AND_INTERMEDIATE_DATA",
            "caustic_behavior": "REMAINS_INVERTIBLE",
            "status": "DERIVED_REDUCIBLE_PATHWISE_ASSEMBLY",
        },
        {
            "object": "FULL_COFRAME_PARALLEL_TRANSPORT",
            "space": "SPACETIME_TANGENT_OR_COTANGENT_FRAME",
            "composition": "YES_PATH_GROUPOID",
            "caustic_behavior": "PATHWISE_REGULAR",
            "status": "TYPE_DISTINCT_NO_AUTOMATIC_SOLDER",
        },
    ]
    write_tsv(
        "COCYCLE_TYPE_LEDGER.tsv",
        ["object", "space", "composition", "caustic_behavior", "status"],
        types,
    )

    branches = [
        {
            "branch": "B19_ROUND_S3",
            "metric_status": "CONDITIONAL_COMPLETE_ON_SHELL_SPATIAL_ULTRASTATIC",
            "clock_block": "Q=1;S=IDENTITY",
            "transverse_block": "EXACT_GLOBAL_PATHWISE_M;ANTIPODAL_J_SINGULAR",
            "composition": "YES_PER_RETAINED_PATH",
            "global_recentring": "YES_SET_VALUED_AT_CUT_LOCUS",
            "ruling": "COMPLETE_TRANSVERSE_COCYCLE_TRIVIAL_CLOCK_NO_FOUNDING_SOLDER",
        },
        {
            "branch": "SQUASHED_S3_OFF_SHELL",
            "metric_status": "COMPLETE_HOMOGENEOUS_OFF_SHELL_CONTROL",
            "clock_block": "Q=1;S=IDENTITY",
            "transverse_block": "PATHWISE_M_EXISTS;EXPLICIT_CUT_ATLAS_OPEN",
            "composition": "YES_PER_RETAINED_PATH",
            "global_recentring": "CONDITIONAL_GEOMETRIC_PATH_FAMILY",
            "ruling": "OFF_SHELL_PATHWISE_COCYCLE_TRIVIAL_CLOCK_NOT_SELECTED",
        },
        {
            "branch": "WRL_LOCAL_RESIDUAL",
            "metric_status": "LOCAL_CENTERED_STATIC_PROFILE_NO_GLOBAL_COMPLETION",
            "clock_block": "Q=N_START/N_END;CENTER_TO_D=EXP_PHI",
            "transverse_block": "LOCAL_RADIAL_M_EXISTS;J_CENTER_TO_D=R",
            "composition": "YES_AWAY_FROM_CENTER_IRREGULARITY_AND_LAPSE_ZERO",
            "global_recentring": "NO",
            "ruling": "LOCAL_COMBINED_WITNESS_NO_GLOBAL_OBSERVER_OPERATOR",
        },
        {
            "branch": "TEMPORAL_PHI_SLICE_FAMILY",
            "metric_status": "CONDITIONAL_PRE_SCALE_REST_GEOMETRY_NO_COMPLETE_BRANCH",
            "clock_block": "PHYSICAL_SOLDER_OPEN",
            "transverse_block": "PATHWISE_M_IF_COMPLETE_POSITIVE_LEVEL_SUPPLIED",
            "composition": "CONDITIONAL_GIVEN_ONE_SUPPLIED_PATH_TYPE",
            "global_recentring": "OPEN",
            "ruling": "CONDITIONAL_PATHWISE_GEOMETRY_NO_COMMON_PHYSICAL_SOLDER",
        },
        {
            "branch": "CONSTANT_SPATIAL_CURVATURE_STATIC_CONTROL",
            "metric_status": "MATHEMATICAL_COMPARISON_NOT_REGISTERED_UDT_BRANCH",
            "clock_block": "Q=SEC_RATIO_IN_STATIC_PATCH",
            "transverse_block": "EXACT_ROUND_M_IN_SPATIAL_SECTOR",
            "composition": "YES_INSIDE_STATIC_PATCH",
            "global_recentring": "NO_CLOCK_PATCH_ENDS_BEFORE_SPATIAL_DIAMETER",
            "ruling": "COUNTERCONTROL_LOCAL_COMBINED_COCYCLE_NOT_UDT_BRANCH",
        },
        {
            "branch": "UNIVERSAL_PHYSICAL_UDT",
            "metric_status": "NO_COMPLETE_WITNESS",
            "clock_block": "OPEN",
            "transverse_block": "OPEN",
            "composition": "OPEN",
            "global_recentring": "OPEN",
            "ruling": "OPEN_NO_COMPLETE_NONTRIVIAL_ALL_OBSERVER_WITNESS",
        },
    ]
    write_tsv(
        "BRANCH_COCYCLE_ATLAS.tsv",
        [
            "branch",
            "metric_status",
            "clock_block",
            "transverse_block",
            "composition",
            "global_recentring",
            "ruling",
        ],
        branches,
    )

    statuses = [
        {
            "claim": "metric Jacobi phase-space path cocycle",
            "status": "DERIVED_GIVEN_METRIC_PATH",
            "scope": "complete first-order transverse deviation state",
        },
        {
            "claim": "vertex Jacobi matrix is a path cocycle",
            "status": "REJECTED_GENERICALLY",
            "scope": "projected angular-area block alone",
        },
        {
            "claim": "endpoint clock ratio cocycle",
            "status": "DERIVED_GIVEN_OBSERVERS_PATH_AND_EVENTS",
            "scope": "matched intermediate frequency or static lapse readout",
        },
        {
            "claim": "direct-sum longitudinal/transverse path cocycle",
            "status": "DERIVED_REDUCIBLE_GIVEN_COMMON_PATH_DATA",
            "scope": "S(log Q) direct sum M",
        },
        {
            "claim": "founding reciprocal depth equals log endpoint clock ratio",
            "status": "CONDITIONAL",
            "scope": "true in centered WRL control; no all-observer theorem",
        },
        {
            "claim": "one irreducible native UDT observer representation",
            "status": "OPEN",
            "scope": "direct sum does not prove intrinsic solder or mixing law",
        },
        {
            "claim": "null versus co-present/rest path selection",
            "status": "OPEN",
            "scope": "metric permits typed candidates but does not choose physical interpretation",
        },
        {
            "claim": "complete nontrivial universal observer cocycle",
            "status": "OPEN",
            "scope": "no registered branch has completeness recentering and nontrivial clock together",
        },
        {
            "claim": "physical Xmax",
            "status": "OPEN",
            "scope": "no local horizon caustic or diameter promoted",
        },
        {
            "claim": "action source carrier density bootstrap",
            "status": "OPEN_EXCLUDED",
            "scope": "not used or derived",
        },
    ]
    write_tsv("STATUS_LEDGER.tsv", ["claim", "status", "scope"], statuses)

    result = {
        "result": "PASS",
        "preregistration_commit": PREREG_COMMIT,
        "ratio_clarification_commit": RATIO_CLARIFICATION_COMMIT,
        "check_count": len(checks),
        "checks": checks,
        "source_count": source_count,
        "type_count": len(types),
        "branch_count": len(branches),
        "registry": {
            "finite_cell_completions": len(completions),
            "equation_families": len(equations),
        },
        "derived_object": "METRIC_GEODESIC_DEVIATION_PATH_COCYCLE",
        "combined_object": "REDUCIBLE_DIRECT_SUM_S_LOG_Q_PLUS_M",
        "founding_reciprocal_solder": "CONDITIONAL",
        "irreducible_native_solder": "OPEN",
        "universal_all_observer_operator": "OPEN",
        "physical_Xmax": "OPEN",
        "cross_branch_splice": "FORBIDDEN_NOT_USED",
        "projected_false_difference": str(projected_false_difference),
    }
    (HERE / "DERIVATION_RESULT.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
