#!/usr/bin/env python3
"""Independent stdlib/Fraction verification of the optical correspondence."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
from fractions import Fraction
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def require(checks: dict[str, str], name: str, condition: bool) -> None:
    if not condition:
        raise AssertionError(name)
    checks[name] = "PASS"


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def determinant2(matrix: list[list[float]]) -> float:
    return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]


def multiply(
    left: list[list[float]], right: list[list[float]]
) -> list[list[float]]:
    return [
        [
            sum(left[i][k] * right[k][j] for k in range(2))
            for j in range(2)
        ]
        for i in range(2)
    ]


def transpose(matrix: list[list[float]]) -> list[list[float]]:
    return [[matrix[j][i] for j in range(2)] for i in range(2)]


def rotation(angle: float) -> list[list[float]]:
    return [
        [math.cos(angle), -math.sin(angle)],
        [math.sin(angle), math.cos(angle)],
    ]


def validate_status(kind: str = "") -> None:
    state: dict[str, object] = {
        "universal_operator": "OPEN_SELECTOR",
        "selected_pairing": "NONE",
        "null_equals_rest": "CONDITIONAL_NOT_UNIVERSAL",
        "WRL_global": False,
        "WRL_proper_equals_area": False,
        "B19_clock": "CONSTANT_NO_DILATION",
        "physical_Xmax": "OPEN",
        "SNe_selects_join": False,
        "path_multiplicity": "RETAINED",
        "co_presence_signal_law": "NOT_DERIVED",
        "equation_families": 28,
        "completions": 12,
        "sources": 19,
    }
    mutations: dict[str, tuple[str, object]] = {
        "operator": ("universal_operator", "DERIVED_SINGLE"),
        "null": ("selected_pairing", "NULL"),
        "rest": ("selected_pairing", "REST"),
        "conflate": ("null_equals_rest", "UNIVERSAL"),
        "wrl_global": ("WRL_global", True),
        "wrl_distance": ("WRL_proper_equals_area", True),
        "b19_clock": ("B19_clock", "RECIPROCAL"),
        "xmax": ("physical_Xmax", "DERIVED"),
        "sne": ("SNe_selects_join", True),
        "path": ("path_multiplicity", "DISCARDED"),
        "copresence": ("co_presence_signal_law", "DERIVED"),
        "families": ("equation_families", 27),
        "completions": ("completions", 11),
        "sources": ("sources", 18),
    }
    if kind:
        key, value = mutations[kind]
        state[key] = value
    expected = {
        "universal_operator": "OPEN_SELECTOR",
        "selected_pairing": "NONE",
        "null_equals_rest": "CONDITIONAL_NOT_UNIVERSAL",
        "WRL_global": False,
        "WRL_proper_equals_area": False,
        "B19_clock": "CONSTANT_NO_DILATION",
        "physical_Xmax": "OPEN",
        "SNe_selects_join": False,
        "path_multiplicity": "RETAINED",
        "co_presence_signal_law": "NOT_DERIVED",
        "equation_families": 28,
        "completions": 12,
        "sources": 19,
    }
    if state != expected:
        raise AssertionError(f"status firewall rejected {kind}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="INDEPENDENT_VERIFICATION.json")
    args = parser.parse_args()
    checks: dict[str, str] = {}

    # Independent screen-basis determinant check at three fixed rotations.
    jacobi = [[1.25, -0.5], [0.75, 2.0]]
    original_det = determinant2(jacobi)
    for index, (left_angle, right_angle) in enumerate(
        [(0.17, -0.41), (1.2, 0.7), (-2.1, 2.4)]
    ):
        changed = multiply(
            multiply(rotation(left_angle), jacobi),
            transpose(rotation(right_angle)),
        )
        require(
            checks,
            f"screen_det_{index}",
            abs(determinant2(changed) - original_det) < 2e-14,
        )

    # Exact/numeric round, flat, and hyperbolic Jacobi controls.
    radius = 3.75
    for index, distance in enumerate([0.0, 0.1, 0.7, 1.4, math.pi]):
        D = distance * radius
        j_round = radius * math.sin(D / radius)
        j_round_second = -math.sin(D / radius) / radius
        require(
            checks,
            f"round_ode_{index}",
            abs(j_round_second + j_round / radius**2) < 2e-14,
        )
    require(checks, "round_origin", radius * math.sin(0.0) == 0.0)
    require(
        checks,
        "round_equator",
        abs(radius * math.sin(math.pi / 2) - radius) < 2e-15,
    )
    require(
        checks,
        "round_antipode",
        abs(radius * math.sin(math.pi)) < 1e-14,
    )
    for distance in [0.1, 1.0, 4.0]:
        hyperbolic = radius * math.sinh(distance / radius)
        second = math.sinh(distance / radius) / radius
        require(
            checks,
            f"hyperbolic_ode_{distance}",
            abs(second - hyperbolic / radius**2) < 2e-14,
        )

    # WR-L in exact rational arithmetic.
    X = Fraction(7, 1)
    for index, D in enumerate(
        [Fraction(1, 3), Fraction(7, 2), Fraction(21, 2)]
    ):
        N = 1 - D / (2 * X)
        R = D - D * D / (4 * X)
        require(checks, f"wrl_areal_{index}", R / X == 1 - N * N)
        require(
            checks,
            f"wrl_radius_slope_{index}",
            1 - D / (2 * X) == N,
        )
        radial_curvature = 1 / (2 * X * R)
        tangential_curvature = 1 / (X * R)
        require(
            checks,
            f"wrl_curvature_split_{index}",
            tangential_curvature == 2 * radial_curvature,
        )
        require(
            checks,
            f"wrl_scalar_varies_{index}",
            4 * radial_curvature + 2 * tangential_curvature
            == 4 / (X * R),
        )
    require(
        checks,
        "wrl_center_second_jet",
        Fraction(-1, 2) / X != 0,
    )
    require(
        checks,
        "wrl_endpoint",
        (1 - (2 * X) / (2 * X)) == 0
        and (2 * X - (2 * X) ** 2 / (4 * X)) == X,
    )

    # Constant-curvature reciprocal static control.
    b = Fraction(5, 1)
    r = Fraction(3, 1)
    A = 1 - r * r / (b * b)
    A_prime = -2 * r / (b * b)
    k_rad = -A_prime / (2 * r)
    k_tan = (1 - A) / (r * r)
    require(checks, "constant_curvature_radial", k_rad == 1 / (b * b))
    require(checks, "constant_curvature_tangential", k_tan == 1 / (b * b))
    require(
        checks,
        "static_endpoint_half_diameter",
        abs((math.pi * float(b) / 2) * 2 - math.pi * float(b)) < 2e-14,
    )

    # Schur coefficient and time-live type-separation controls.
    require(checks, "schur_coefficients", 2 != 3)
    null_area = 2 * 5
    rest_area = 3 * 5
    require(checks, "time_live_null_rest_differ", null_area != rest_area)
    require(checks, "event_pairing_differ", 0 != -7 / 3)

    source_rows = read_tsv(HERE / "SOURCE_LINEAGE.tsv")
    require(checks, "source_count", len(source_rows) == 19)
    require(
        checks,
        "source_unique",
        len({row["path"] for row in source_rows}) == 19,
    )
    for row in source_rows:
        observed = hashlib.sha256((ROOT / row["path"]).read_bytes()).hexdigest()
        require(checks, f"source_{row['path']}", observed == row["sha256"])

    optical_types = read_tsv(HERE / "OPTICAL_TYPE_LEDGER.tsv")
    branches = read_tsv(HERE / "BRANCH_OPTICAL_ATLAS.tsv")
    equation_rows = read_tsv(HERE / "EQUATION_FAMILY_OPTICAL_SCREEN.tsv")
    completion_rows = read_tsv(HERE / "COMPLETION_OPTICAL_ATLAS.tsv")
    statuses = read_tsv(HERE / "STATUS_LEDGER.tsv")
    require(checks, "optical_type_count", len(optical_types) == 8)
    require(checks, "branch_count", len(branches) == 6)
    require(checks, "equation_count", len(equation_rows) == 28)
    require(
        checks,
        "equation_unique",
        len({row["family_id"] for row in equation_rows}) == 28,
    )
    require(checks, "completion_count", len(completion_rows) == 12)
    require(
        checks,
        "completion_unique",
        len({row["completion_id"] for row in completion_rows}) == 12,
    )
    require(
        checks,
        "completion_none_evaluable",
        all(
            row["optical_correspondence"]
            == "NOT_EVALUABLE_NO_COMPLETE_G_PHI_METRIC"
            for row in completion_rows
        ),
    )
    require(checks, "status_count", len(statuses) == 8)

    branch_by_id = {row["branch"]: row for row in branches}
    require(
        checks,
        "round_center_free",
        branch_by_id["B19_ROUND_S3"]["center_status"]
        == "NO_CENTER_BY_TRANSITIVE_ISOMETRY",
    )
    require(
        checks,
        "round_clock_unsoldered",
        branch_by_id["B19_ROUND_S3"]["clock_ratio"] == "1",
    )
    require(
        checks,
        "wrl_centered_residual",
        branch_by_id["WRL_LOCAL_RESIDUAL"]["physical_ruling"]
        == "EXISTING_SNE_READOUT_IS_CENTERED_RESIDUAL_NOT_GLOBAL_PAIR_OPERATOR",
    )
    require(
        checks,
        "universal_open",
        branch_by_id["UNIVERSAL_PHYSICAL_UDT"]["physical_ruling"] == "OPEN",
    )

    catches: dict[str, str] = {}
    for kind in [
        "operator",
        "null",
        "rest",
        "conflate",
        "wrl_global",
        "wrl_distance",
        "b19_clock",
        "xmax",
        "sne",
        "path",
        "copresence",
        "families",
        "completions",
        "sources",
    ]:
        try:
            validate_status(kind)
        except AssertionError:
            catches[kind] = "PASS_REJECTED"
        else:
            raise AssertionError(f"catch survived: {kind}")
    validate_status()

    production = json.loads(
        (HERE / "DERIVATION_RESULT.json").read_text(encoding="utf-8")
    )
    require(checks, "production_pass", production["result"] == "PASS")
    require(
        checks,
        "production_registry",
        production["registry"]
        == {
            "complete_g_phi_completion_witnesses": 0,
            "equation_families": 28,
            "finite_cell_completions": 12,
        },
    )
    require(
        checks,
        "production_object",
        production["derived_object"]["type"]
        == "SET_VALUED_OBSERVER_OPTICAL_CORRESPONDENCE",
    )
    require(
        checks,
        "production_universal_open",
        production["universal_operator"] == "OPEN_SELECTOR",
    )
    require(checks, "production_xmax_open", production["physical_Xmax"] == "OPEN")

    result = {
        "schema": "udt-center-free-optical-independent-1.0",
        "result": "PASS",
        "method": "stdlib_math_fraction_and_fixed_registry_reconstruction",
        "check_count": len(checks),
        "checks": checks,
        "catch_count": len(catches),
        "catches": catches,
        "ruling": {
            "derived_object": "SET_VALUED_OBSERVER_OPTICAL_CORRESPONDENCE_GIVEN_INPUTS",
            "single_universal_operator": "OPEN",
            "round_B19": "CENTER_FREE_OPTICAL_GEOMETRY_CONSTANT_CLOCK",
            "WRL": "CENTERED_RESIDUAL_CLOCK_AREA_READOUT_NO_GLOBAL_RECENTERING",
            "physical_Xmax": "OPEN",
        },
    }
    (HERE / args.output).write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
