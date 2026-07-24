#!/usr/bin/env python3
"""Independent numerical/algebraic verification without production imports."""

from __future__ import annotations

import csv
import hashlib
import json
import math
import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def check(checks: dict[str, str], name: str, condition: bool) -> None:
    if not condition:
        raise AssertionError(name)
    checks[name] = "PASS"


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def mm(a: list[list[float]], b: list[list[float]]) -> list[list[float]]:
    return [
        [sum(a[i][k] * b[k][j] for k in range(len(b))) for j in range(len(b[0]))]
        for i in range(len(a))
    ]


def madd(
    a: list[list[float]], b: list[list[float]], scale: float = 1.0
) -> list[list[float]]:
    return [
        [a[i][j] + scale * b[i][j] for j in range(len(a[0]))]
        for i in range(len(a))
    ]


def mscale(a: list[list[float]], scale: float) -> list[list[float]]:
    return [[scale * x for x in row] for row in a]


def maxerr(a: list[list[float]], b: list[list[float]]) -> float:
    return max(
        abs(a[i][j] - b[i][j])
        for i in range(len(a))
        for j in range(len(a[0]))
    )


def det2(a: list[list[float]]) -> float:
    return a[0][0] * a[1][1] - a[0][1] * a[1][0]


def round_m(length: float, radius: float) -> list[list[float]]:
    c = math.cos(length / radius)
    s = math.sin(length / radius)
    return [[c, radius * s], [-s / radius, c]]


def wrl_k(distance: float, scale: float) -> float:
    radius = distance - distance * distance / (4.0 * scale)
    return 1.0 / (2.0 * scale * radius)


def rhs(distance: float, matrix: list[list[float]], scale: float) -> list[list[float]]:
    generator = [[0.0, 1.0], [-wrl_k(distance, scale), 0.0]]
    return mm(generator, matrix)


def integrate_fundamental(
    start: float, end: float, scale: float, steps: int
) -> list[list[float]]:
    h = (end - start) / steps
    state = [[1.0, 0.0], [0.0, 1.0]]
    distance = start
    for _ in range(steps):
        k1 = rhs(distance, state, scale)
        k2 = rhs(
            distance + h / 2.0, madd(state, k1, h / 2.0), scale
        )
        k3 = rhs(
            distance + h / 2.0, madd(state, k2, h / 2.0), scale
        )
        k4 = rhs(distance + h, madd(state, k3, h), scale)
        increment = madd(madd(k1, k2, 2.0), madd(k3, k4, 0.5), 2.0)
        # The expression above is k1+2k2+2k3+k4.
        state = madd(state, increment, h / 6.0)
        distance += h
    return state


def validate_state(state: dict[str, object]) -> None:
    required = {
        "derived_object": "METRIC_GEODESIC_DEVIATION_PATH_COCYCLE",
        "combined_object": "REDUCIBLE_DIRECT_SUM_S_LOG_Q_PLUS_M",
        "founding_reciprocal_solder": "CONDITIONAL",
        "irreducible_native_solder": "OPEN",
        "universal_all_observer_operator": "OPEN",
        "physical_Xmax": "OPEN",
        "cross_branch_splice": "FORBIDDEN_NOT_USED",
        "completion_count": 12,
        "equation_count": 28,
        "branch_count": 6,
        "type_count": 6,
        "b19_clock": "Q=1;S=IDENTITY",
        "wrl_global": "NO",
        "temporal_solder": "PHYSICAL_SOLDER_OPEN",
    }
    for key, value in required.items():
        if state.get(key) != value:
            raise AssertionError(key)


def rejected(state: dict[str, object], key: str, value: object) -> str:
    mutated = dict(state)
    mutated[key] = value
    try:
        validate_state(mutated)
    except AssertionError:
        return "PASS_REJECTED"
    raise AssertionError(f"mutation accepted: {key}")


def main() -> None:
    checks: dict[str, str] = {}

    # Independent analytic constant-curvature controls.
    radius = 2.7
    l1 = 0.61
    l2 = 1.13
    m1 = round_m(l1, radius)
    m2 = round_m(l2, radius)
    m12 = round_m(l1 + l2, radius)
    check(checks, "round_composition_numeric", maxerr(mm(m2, m1), m12) < 2e-15)
    check(checks, "round_det_m1", abs(det2(m1) - 1.0) < 2e-15)
    check(checks, "round_det_m2", abs(det2(m2) - 1.0) < 2e-15)
    check(
        checks,
        "round_reversal_numeric",
        maxerr(mm(round_m(-l1, radius), m1), [[1.0, 0.0], [0.0, 1.0]])
        < 2e-15,
    )
    false_projected = abs(m12[0][1] - m2[0][1] * m1[0][1])
    check(checks, "projected_map_noncomposition_numeric", false_projected > 0.1)
    anti = round_m(math.pi * radius, radius)
    check(checks, "antipode_projected_block_zero", abs(anti[0][1]) < 2e-15)
    check(checks, "antipode_full_det_one", abs(det2(anti) - 1.0) < 2e-15)
    check(
        checks,
        "antipode_full_minus_identity",
        maxerr(anti, [[-1.0, 0.0], [0.0, -1.0]]) < 2e-15,
    )

    # Variable-coefficient WR-L propagation via a fresh RK4 implementation.
    scale = 2.0
    d0, d1, d2 = 0.25, 0.85, 1.40
    m01 = integrate_fundamental(d0, d1, scale, 12000)
    m12w = integrate_fundamental(d1, d2, scale, 11000)
    m02 = integrate_fundamental(d0, d2, scale, 23000)
    composition_error = maxerr(mm(m12w, m01), m02)
    check(checks, "wrl_variable_composition", composition_error < 2e-11)
    check(checks, "wrl_variable_det_m01", abs(det2(m01) - 1.0) < 2e-11)
    check(checks, "wrl_variable_det_m12", abs(det2(m12w) - 1.0) < 2e-11)
    check(checks, "wrl_variable_det_m02", abs(det2(m02) - 1.0) < 2e-11)

    # Directly verify the known WR-L vertex solution without symbolic code.
    def wrl_r(distance: float) -> float:
        return distance - distance * distance / (4.0 * scale)

    for index, distance in enumerate((0.2, 0.7, 1.5, 2.2), start=1):
        residual = -1.0 / (2.0 * scale) + wrl_k(distance, scale) * wrl_r(distance)
        check(checks, f"wrl_vertex_residual_{index}", abs(residual) < 2e-15)

    n0 = 1.0 - d0 / (2.0 * scale)
    n1 = 1.0 - d1 / (2.0 * scale)
    n2 = 1.0 - d2 / (2.0 * scale)
    q01, q12, q02 = n0 / n1, n1 / n2, n0 / n2
    check(checks, "clock_ratio_composition_numeric", abs(q01 * q12 - q02) < 2e-15)
    check(
        checks,
        "clock_log_additivity_numeric",
        abs(math.log(q01) + math.log(q12) - math.log(q02)) < 2e-15,
    )
    check(
        checks,
        "centered_wrl_clock_exp_phi_numeric",
        abs(
            1.0 / (1.0 - d2 / (2.0 * scale))
            - math.exp(-math.log(1.0 - d2 / (2.0 * scale)))
        )
        < 2e-15,
    )

    production = json.loads((HERE / "DERIVATION_RESULT.json").read_text())
    branches = {
        row["branch"]: row for row in read_tsv(HERE / "BRANCH_COCYCLE_ATLAS.tsv")
    }
    types = {row["object"]: row for row in read_tsv(HERE / "COCYCLE_TYPE_LEDGER.tsv")}
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
    check(checks, "production_pass", production["result"] == "PASS")
    check(checks, "production_checks_all_pass", set(production["checks"].values()) == {"PASS"})
    check(checks, "branch_count", len(branches) == 6)
    check(checks, "type_count", len(types) == 6)
    check(checks, "completion_count", len(completions) == 12)
    check(checks, "completion_unique", len({r["completion_id"] for r in completions}) == 12)
    check(checks, "equation_count", len(equations) == 28)
    check(checks, "equation_unique", len({r["family_id"] for r in equations}) == 28)
    check(
        checks,
        "vertex_type_not_composable",
        types["VERTEX_JACOBI_MAP_J"]["composition"] == "NO_NOT_STANDALONE",
    )
    check(
        checks,
        "full_type_composable",
        types["FULL_TRANSVERSE_PROPAGATOR_M"]["composition"] == "YES_PATH_GROUPOID",
    )
    check(
        checks,
        "b19_trivial_clock",
        branches["B19_ROUND_S3"]["clock_block"] == "Q=1;S=IDENTITY",
    )
    check(
        checks,
        "wrl_not_global",
        branches["WRL_LOCAL_RESIDUAL"]["global_recentring"] == "NO",
    )
    check(
        checks,
        "universal_open",
        branches["UNIVERSAL_PHYSICAL_UDT"]["composition"] == "OPEN",
    )

    # Recheck every frozen source identity without using production helpers.
    sources = read_tsv(HERE / "SOURCE_LINEAGE.tsv")
    check(checks, "source_count", len(sources) == 18)
    check(checks, "source_unique", len({row["path"] for row in sources}) == 18)
    for row in sources:
        if row["role"] == "frontier_scope":
            data = subprocess.run(
                [
                    "git",
                    "show",
                    "dc81c489b9e27bd86b2d58d93fbacf4a4fd01496:"
                    + row["path"],
                ],
                cwd=ROOT,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=True,
            ).stdout
        else:
            data = (ROOT / row["path"]).read_bytes()
        observed = hashlib.sha256(data).hexdigest()
        check(checks, f"source_hash_{row['role']}", observed == row["sha256"])

    state: dict[str, object] = {
        "derived_object": production["derived_object"],
        "combined_object": production["combined_object"],
        "founding_reciprocal_solder": production["founding_reciprocal_solder"],
        "irreducible_native_solder": production["irreducible_native_solder"],
        "universal_all_observer_operator": production["universal_all_observer_operator"],
        "physical_Xmax": production["physical_Xmax"],
        "cross_branch_splice": production["cross_branch_splice"],
        "completion_count": len(completions),
        "equation_count": len(equations),
        "branch_count": len(branches),
        "type_count": len(types),
        "b19_clock": branches["B19_ROUND_S3"]["clock_block"],
        "wrl_global": branches["WRL_LOCAL_RESIDUAL"]["global_recentring"],
        "temporal_solder": branches["TEMPORAL_PHI_SLICE_FAMILY"]["clock_block"],
    }
    validate_state(state)
    catches = {
        "projected_map_promotion": rejected(
            state, "derived_object", "VERTEX_JACOBI_PATH_COCYCLE"
        ),
        "missing_full_completion": rejected(state, "type_count", 5),
        "cross_branch_splice": rejected(state, "cross_branch_splice", "USED"),
        "caustic_deletion": rejected(state, "b19_clock", "CAUSTIC_REMOVED"),
        "founding_solder_promotion": rejected(
            state, "founding_reciprocal_solder", "DERIVED"
        ),
        "irreducible_solder_promotion": rejected(
            state, "irreducible_native_solder", "DERIVED"
        ),
        "global_operator_promotion": rejected(
            state, "universal_all_observer_operator", "DERIVED"
        ),
        "physical_xmax_promotion": rejected(state, "physical_Xmax", "DERIVED"),
        "wrl_global_promotion": rejected(state, "wrl_global", "YES"),
        "temporal_solder_promotion": rejected(
            state, "temporal_solder", "DERIVED"
        ),
        "completion_omission": rejected(state, "completion_count", 11),
        "equation_omission": rejected(state, "equation_count", 27),
        "branch_omission": rejected(state, "branch_count", 5),
    }

    result = {
        "result": "PASS",
        "method": "PURE_PYTHON_ANALYTIC_CONTROLS_PLUS_FRESH_RK4",
        "production_imported": False,
        "check_count": len(checks),
        "checks": checks,
        "catch_count": len(catches),
        "catches": catches,
        "wrl_composition_max_abs_error": composition_error,
        "wrl_direct_det_error": abs(det2(m02) - 1.0),
        "projected_noncomposition_abs_difference": false_projected,
    }
    (HERE / "INDEPENDENT_VERIFICATION.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
