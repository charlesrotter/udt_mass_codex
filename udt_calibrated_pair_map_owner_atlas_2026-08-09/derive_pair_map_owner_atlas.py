#!/usr/bin/env python3
"""Exact CPU controller for the preregistered calibrated pair-map owner atlas."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path
import subprocess

import sympy as sp


ROOT = Path(__file__).resolve().parents[1]
PACKAGE = Path(__file__).resolve().parent
ALLOWED_DISPOSITIONS = {
    "DERIVED_FROM_METRIC_AND_DECLARED_QUERY",
    "CONDITIONAL_QUERY_DATA",
    "CONDITIONAL_BRANCH_STRUCTURE",
    "LOCAL_ONLY_BRANCH_VALUED",
    "FAILS_REQUIRED_TYPE",
    "OPEN_NOT_DECIDED_BY_CURRENT_FOUNDATION",
}


class Checks:
    def __init__(self) -> None:
        self.rows: list[dict[str, object]] = []

    def exact(self, name: str, actual: object, expected: object) -> None:
        passed = bool(sp.simplify(sp.sympify(actual) - sp.sympify(expected)) == 0)
        self.rows.append(
            {
                "name": name,
                "passed": passed,
                "actual": str(sp.simplify(actual)),
                "expected": str(sp.simplify(expected)),
            }
        )

    def truth(self, name: str, condition: object, detail: object = "") -> None:
        passed = bool(condition)
        self.rows.append(
            {
                "name": name,
                "passed": passed,
                "actual": str(detail if detail != "" else passed),
                "expected": "True",
            }
        )


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def replay_sources(checks: Checks) -> None:
    with (PACKAGE / "SOURCE_MANIFEST.tsv").open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
    checks.exact("source_count", len(rows), 20)
    checks.truth("source_paths_unique", len({row["path"] for row in rows}) == 20)
    for index, row in enumerate(rows, start=1):
        data = subprocess.check_output(["git", "show", row["source_ref"]], cwd=ROOT)
        checks.truth(f"source_{index:02d}", sha256(data) == row["sha256"], row["path"])


def read_atlas(checks: Checks) -> tuple[list[dict[str, str]], dict[str, int]]:
    with (PACKAGE / "PAIR_MAP_ATLAS.tsv").open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
    checks.exact("atlas_row_count", len(rows), 66)
    identities = {(row["candidate_id"], row["axis_id"]) for row in rows}
    checks.exact("atlas_unique_identity_count", len(identities), 66)
    candidates = {row["candidate_id"] for row in rows}
    checks.truth("atlas_candidate_set", candidates == {f"P{i:02d}" for i in range(1, 7)})
    for candidate in candidates:
        checks.exact(
            f"atlas_{candidate}_axis_count",
            sum(row["candidate_id"] == candidate for row in rows),
            11,
        )
    checks.truth(
        "atlas_dispositions_registered",
        all(row["disposition"] in ALLOWED_DISPOSITIONS for row in rows),
    )
    checks.truth(
        "atlas_no_merit_filter",
        all(row["merit_filter"] == "NONE_CHARACTERIZE_ONLY" for row in rows),
    )
    counts = {
        disposition: sum(row["disposition"] == disposition for row in rows)
        for disposition in sorted(ALLOWED_DISPOSITIONS)
    }
    return rows, counts


def derive() -> dict[str, object]:
    checks = Checks()
    replay_sources(checks)
    atlas_rows, disposition_counts = read_atlas(checks)

    # Generic supplied regular pair metric. Positive symbols are algebraic-domain declarations.
    T, L = sp.symbols("T L", positive=True)
    beta = sp.symbols("beta", real=True)
    h = sp.Matrix([[-T**2, -T**2 * beta], [-T**2 * beta, L**2 - T**2 * beta**2]])
    checks.exact("generic_pair_det", h.det(), -(T * L) ** 2)
    checks.exact("generic_clock_recovery", sp.sqrt(-h[0, 0]), T)
    checks.exact("generic_shift_recovery", h[0, 1] / h[0, 0], beta)
    checks.exact("generic_ruler_recovery", h[1, 1] - h[0, 1] ** 2 / h[0, 0], L**2)
    phi_pair = sp.Rational(1, 2) * sp.log(L / T)
    checks.exact(
        "generic_terminal_formula",
        sp.Rational(1, 4) * sp.log((-h.det()) / h[0, 0] ** 2),
        phi_pair,
    )

    # P01/P04: exact flat accelerated orthogonal tube. y is already the c_E-matched clock length.
    y, s, a = sp.symbols("y s a", real=True, nonzero=True)
    F_acc = sp.Matrix(
        [
            (sp.Rational(1, 1) / a + s) * sp.sinh(a * y),
            (sp.Rational(1, 1) / a + s) * sp.cosh(a * y),
        ]
    )
    J_acc = F_acc.jacobian([y, s])
    eta2 = sp.diag(-1, 1)
    h_acc = sp.simplify(J_acc.T * eta2 * J_acc)
    checks.exact("accelerated_tube_h00", h_acc[0, 0], -(1 + a * s) ** 2)
    checks.exact("accelerated_tube_h01", h_acc[0, 1], 0)
    checks.exact("accelerated_tube_h11", h_acc[1, 1], 1)
    checks.truth("accelerated_tube_not_inertial_generic", sp.simplify(h_acc[0, 0] + 1) != 0)
    checks.exact("accelerated_tube_inertial_limit", h_acc[0, 0].subs(a, 0), -1)

    # P04: same flat metric and central worldline, but arbitrary rotating direction evolution.
    omega = sp.symbols("omega", real=True, nonzero=True)
    F_rot = sp.Matrix([y, s * sp.cos(omega * y), s * sp.sin(omega * y), 0])
    eta4 = sp.diag(-1, 1, 1, 1)
    J_rot = F_rot.jacobian([y, s])
    h_rot = sp.simplify(J_rot.T * eta4 * J_rot)
    checks.exact("rotating_tube_h00", h_rot[0, 0], -1 + omega**2 * s**2)
    checks.exact("rotating_tube_h01", h_rot[0, 1], 0)
    checks.exact("rotating_tube_h11", h_rot[1, 1], 1)
    h_rot_reverse = sp.simplify(h_rot.subs(omega, -omega))
    checks.truth("opposite_rotations_same_pair_metric", h_rot_reverse == h_rot)
    F_rot_reverse = F_rot.subs(omega, -omega)
    checks.truth("opposite_rotations_distinct_maps", sp.simplify(F_rot - F_rot_reverse) != sp.zeros(4, 1))
    checks.exact("rotating_tube_null_boundary", h_rot[0, 0].subs(s, 1 / omega), 0)

    # P02: flat metric, coframe-presentation-dependent reciprocal-plane integrability.
    angle = sp.symbols("angle", real=True)
    rotation = sp.Matrix([[sp.cos(angle), -sp.sin(angle)], [sp.sin(angle), sp.cos(angle)]])
    checks.truth("spatial_rotation_preserves_flat_metric", sp.simplify(rotation.T * rotation) == sp.eye(2))
    # e1=(cos(omega*y),sin(omega*y)); [e0,e1]=omega*e2 is transverse to span(e0,e1).
    e1 = sp.Matrix([sp.cos(omega * y), sp.sin(omega * y)])
    e2 = sp.Matrix([-sp.sin(omega * y), sp.cos(omega * y)])
    bracket_spatial = sp.diff(e1, y)
    checks.truth("rotated_plane_frobenius_obstruction", sp.simplify(bracket_spatial - omega * e2) == sp.zeros(2, 1))
    checks.truth("frobenius_obstruction_nonzero", bracket_spatial != sp.zeros(2, 1))
    checks.truth("same_flat_metric_has_integrable_zero_rotation", bracket_spatial.subs(omega, 0) == sp.zeros(2, 1))

    # P03: stationary flow surface. Killing norm alone and full pair readout coincide only if TL=1.
    N, R = sp.symbols("N R", positive=True)
    h_stationary = sp.Matrix([[-N**2, -N**2 * beta], [-N**2 * beta, R**2 - N**2 * beta**2]])
    checks.exact("stationary_pair_det", h_stationary.det(), -(N * R) ** 2)
    stationary_phi = sp.Rational(1, 2) * sp.log(R / N)
    checks.exact(
        "stationary_terminal_phi",
        sp.Rational(1, 4) * sp.log((-h_stationary.det()) / h_stationary[0, 0] ** 2),
        stationary_phi,
    )
    delta_k = -sp.log(N)  # reference A has N_A=1
    checks.exact("stationary_killing_terminal_difference", stationary_phi - delta_k, sp.Rational(1, 2) * sp.log(N * R))
    checks.exact("stationary_join_under_reciprocal_area", (stationary_phi - delta_k).subs(R, 1 / N), 0)
    checks.truth("stationary_norm_not_terminal_generic", sp.simplify(stationary_phi - delta_k) != 0)

    # P05: dExp position block fails subdivision and vanishes at a conjugate point; full Jacobi phase composes.
    dexp_half = sp.sin(sp.pi / 6) / (sp.pi / 6)
    dexp_full = sp.sin(sp.pi / 3) / (sp.pi / 3)
    checks.truth("dexp_position_block_noncompositional", sp.simplify(dexp_half**2 - dexp_full) != 0)
    checks.exact("dexp_conjugate_rank_factor", sp.sin(sp.pi) / sp.pi, 0)
    p, q = sp.symbols("p q", real=True)
    jacobi = lambda x: sp.Matrix([[sp.cos(x), sp.sin(x)], [-sp.sin(x), sp.cos(x)]])
    checks.truth("full_jacobi_phase_composes", sp.simplify(jacobi(q) * jacobi(p) - jacobi(p + q)) == sp.zeros(2))
    checks.truth("jacobi_position_block_does_not_compose", sp.simplify(sp.sin(p + q) - sp.sin(p) * sp.sin(q)) != 0)

    # P06: compatible carried calibration composes; an unowned reciprocal reset at B shifts the result arbitrarily.
    depth_a, depth_b, reset = sp.symbols("depth_a depth_b reset", real=True)
    D = lambda x: sp.diag(sp.exp(-x), sp.exp(x))
    def diagonal_depth(matrix: sp.Matrix) -> sp.Expr:
        return sp.Rational(1, 2) * sp.log(matrix[1, 1] / matrix[0, 0])

    checks.exact("carried_tapes_compose", diagonal_depth(D(depth_b) * D(depth_a)), depth_a + depth_b)
    checks.exact(
        "rebuilt_tape_reset_ambiguity",
        diagonal_depth(D(depth_b) * D(reset) * D(depth_a)),
        depth_a + depth_b + reset,
    )
    checks.truth("unowned_reset_changes_composite", reset != 0)
    common = sp.symbols("common", real=True)
    checks.exact(
        "common_scale_join_cancels",
        diagonal_depth(D(depth_b) * (sp.exp(common) * sp.eye(2)) * D(depth_a)),
        depth_a + depth_b,
    )

    # Pair readout does not identify a unique pair map: opposite rotations are an exact witness.
    checks.truth("equal_readout_does_not_select_map", h_rot_reverse == h_rot and F_rot_reverse != F_rot)

    failed = [row for row in checks.rows if not row["passed"]]
    return {
        "schema": "udt-calibrated-pair-map-owner-atlas-v1",
        "base": "3ad41b15551d31cc2c6da5bf8313b6531f4f0279",
        "preregistration_commit": "7851b445",
        "source_freeze_commit": "bda866a6",
        "checks_total": len(checks.rows),
        "checks_passed": len(checks.rows) - len(failed),
        "checks_failed": len(failed),
        "failed": failed,
        "atlas_rows": len(atlas_rows),
        "disposition_counts": disposition_counts,
        "landing": (
            "NO_UNIQUE_UNIVERSAL_PAIR_MAP_OWNER_FROM_METRIC_PLUS_BARE_ORDERED_EVENTS__"
            "ORTHOGONAL_EXPONENTIAL_TUBES_ARE_LOCAL_METRIC_NATURAL_ONLY_AFTER_WORLDLINE_EVENT_PAIRING_AND_BRANCH_DATA__"
            "COFRAME_PLANE_SURFACES_REQUIRE_PHYSICAL_SPLIT_AND_FROBENIUS_INTEGRABILITY__"
            "STATIONARY_KILLING_FLOW_IS_CONDITIONAL_AND_ITS_NORM_DEPTH_EQUALS_TERMINAL_PAIR_DEPTH_ONLY_WHEN_TL_EQUALS_ONE__"
            "ACCELERATED_TUBES_FORM_QUERY_DEPENDENT_FAMILIES__"
            "CUT_LOCI_FORCE_BRANCH_VALUED_RELATIONS__"
            "PAIR_SURFACES_ARE_NOT_COMPOSABLE_ARROWS_WITHOUT_CARRIED_CALIBRATION_STATE__"
            "PHYSICAL_CALIBRATED_PAIR_RELATION_FUNCTOR_REMAINS_OPEN"
        ),
        "rows": checks.rows,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = derive()
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    return 0 if result["checks_failed"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
