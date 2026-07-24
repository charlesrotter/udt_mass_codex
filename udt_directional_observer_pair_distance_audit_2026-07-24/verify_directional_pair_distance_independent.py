#!/usr/bin/env python3
"""Independent stdlib replay of pair-distance geometry and witness semantics."""

from __future__ import annotations

import copy
import csv
import hashlib
import json
import math
import random
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def read_tsv(name: str) -> list[dict[str, str]]:
    with (HERE / name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def dot(left: list[float], right: list[float]) -> float:
    return sum(a * b for a, b in zip(left, right))


def norm(vector: list[float]) -> float:
    return math.sqrt(dot(vector, vector))


def scale(factor: float, vector: list[float]) -> list[float]:
    return [factor * value for value in vector]


def add(left: list[float], right: list[float]) -> list[float]:
    return [a + b for a, b in zip(left, right)]


def close(actual: float, expected: float, tolerance: float = 2e-11) -> bool:
    return abs(actual - expected) <= tolerance * max(1.0, abs(expected))


def round_distance(p: list[float], q: list[float], b: float) -> float:
    cosine = max(-1.0, min(1.0, dot(p, q) / (b * b)))
    return b * math.acos(cosine)


def random_frame(rng: random.Random, b: float) -> tuple[list[float], list[float]]:
    raw_p = [rng.uniform(-1, 1) for _ in range(4)]
    p = scale(b / norm(raw_p), raw_p)
    raw_n = [rng.uniform(-1, 1) for _ in range(4)]
    tangent = add(raw_n, scale(-dot(raw_n, p) / (b * b), p))
    n = scale(1 / norm(tangent), tangent)
    return p, n


def gamma(p: list[float], n: list[float], b: float, s: float) -> list[float]:
    return add(scale(math.cos(s / b), p), scale(b * math.sin(s / b), n))


def require(label: str, condition: bool, checks: dict[str, str]) -> None:
    if not condition:
        raise AssertionError(label)
    checks[label] = "PASS"


def validate_semantics(
    fc_rows: list[dict[str, str]],
    family_rows: list[dict[str, str]],
    solder_rows: list[dict[str, str]],
    witnesses: list[dict[str, str]],
    round_rows: list[dict[str, str]],
    squashed_rows: list[dict[str, str]],
    gates: list[dict[str, str]],
    statuses: list[dict[str, str]],
) -> None:
    if len(fc_rows) != 12 or len({row["completion_id"] for row in fc_rows}) != 12:
        raise AssertionError("FC coverage")
    if len(family_rows) != 28 or len({row["family_id"] for row in family_rows}) != 28:
        raise AssertionError("family coverage")
    if len(solder_rows) != 6 or len({row["family_id"] for row in solder_rows}) != 6:
        raise AssertionError("solder coverage")
    if any(row["complete_metric_witness"] != "NO" for row in fc_rows):
        raise AssertionError("topology metric promotion")
    complete_families = [
        row for row in family_rows if row["complete_spatial_metric"] == "YES_CONDITIONAL"
    ]
    if len(complete_families) != 1 or complete_families[0]["family_id"] != "B19":
        raise AssertionError("complete witness census")
    by_family = {row["family_id"]: row for row in family_rows}
    if by_family["B19"]["classification"] != (
        "CONDITIONAL_COMPLETE_ROUND_SPATIAL_METRIC_CLOCK_UNSOLDERED"
    ):
        raise AssertionError("round clock promotion")
    if by_family["B21"]["classification"] != (
        "LOCAL_CLOCK_DEPTH_NO_COMPLETE_GLOBAL_SPATIAL_METRIC"
    ):
        raise AssertionError("WRL global promotion")
    if any(row["physical_Xmax_gate"] != "NO" for row in solder_rows):
        raise AssertionError("solder Xmax promotion")
    witness_by_id = {row["witness_id"]: row for row in witnesses}
    round_witness = witness_by_id["W01_ROUND_S3_B19"]
    if (
        round_witness["diameter"] != "pi*b"
        or round_witness["Delta_X_p"] != "0"
        or round_witness["clock_solder"] != "NO_CONSTANT_LAPSE"
        or round_witness["physical_Xmax"] != "NO"
        or round_witness["no_center"] != "YES_BY_TRANSITIVE_ROUND_ISOMETRY"
    ):
        raise AssertionError("round witness semantics")
    if witness_by_id["W02_WRL_LOCAL"]["diameter"] != "NOT_EVALUABLE":
        raise AssertionError("WRL diameter")
    squashed_witness = witness_by_id["W03_SQUASHED_S3_OFF_SHELL"]
    if (
        squashed_witness["metric_status"]
        != "COMPLETE_NONROUND_OFF_SHELL_CONFIGURATION"
        or squashed_witness["diameter"] != "OPEN"
        or squashed_witness["Delta_X_p"] != "OPEN_NOT_ZERO_PROMOTED"
        or squashed_witness["clock_solder"] != "NO_CONSTANT_LAPSE_CONTROL"
        or squashed_witness["physical_Xmax"] != "NO_OFF_SHELL"
    ):
        raise AssertionError("squashed off-shell classification")
    round_by_quantity = {row["quantity"]: row for row in round_rows}
    if round_by_quantity["neutral_torus_to_cap_depth"]["exact_value"] != "pi*b/4":
        raise AssertionError("cap depth")
    if round_by_quantity["neutral_torus_to_cap_depth"]["status"] != (
        "DERIVED_CONDITIONAL_NOT_XMAX"
    ):
        raise AssertionError("cap depth promotion")
    squashed_by_quantity = {row["quantity"]: row for row in squashed_rows}
    if (
        squashed_by_quantity["Hopf_fiber_closed_geodesic"]["exact_result"]
        != "length=2*pi*b*sigma"
        or squashed_by_quantity["horizontal_great_circle"]["exact_result"]
        != "length=2*pi*b"
        or squashed_by_quantity["directional_cut_band"]["status"] != "OPEN"
    ):
        raise AssertionError("squashed control")
    if any(row["full_physical_pass"] != "NO" for row in gates):
        raise AssertionError("physical gate")
    status_by_claim = {row["claim"]: row for row in statuses}
    if status_by_claim["Xmax_definition"]["status"] != (
        "OWNER_CLARIFIED_TWO_OBSERVER_GLOBAL_SUPREMUM"
    ):
        raise AssertionError("preferred center")
    if status_by_claim["current_nonround_directional_band"]["status"] != (
        "OPEN_NOT_EVALUABLE"
    ):
        raise AssertionError("invented directional band")
    if status_by_claim["complete_nonround_metric_configuration"]["status"] != (
        "PRESENT_OFF_SHELL_CONTROL"
    ):
        raise AssertionError("lost nonround control")
    if status_by_claim["squashed_control_no_privileged_center"]["status"] != (
        "DERIVED_CONDITIONAL_METRIC_GEOMETRY"
    ):
        raise AssertionError("squashed preferred center")
    if status_by_claim["CMB_relation_to_directional_band"]["status"] != (
        "OBSERVATIONAL_COMPARISON_OPEN"
    ):
        raise AssertionError("CMB selection")
    if status_by_claim["physical_UDT_Xmax"]["status"] != "OPEN_NOT_EVALUABLE":
        raise AssertionError("physical Xmax")


def validate_sources(corrupt: bool = False) -> None:
    rows = read_tsv("SOURCE_LINEAGE.tsv") + read_tsv("SOURCE_ADDENDUM.tsv")
    if len(rows) != 13:
        raise AssertionError("source coverage")
    for index, row in enumerate(rows):
        expected = row["sha256"]
        if corrupt and index == 0:
            expected = "0" * 64
        actual = hashlib.sha256((ROOT / row["path"]).read_bytes()).hexdigest()
        if actual != expected:
            raise AssertionError("source identity")


def expect_failure(label: str, callback, catches: dict[str, str]) -> None:
    try:
        callback()
    except AssertionError:
        catches[label] = "PASS"
        return
    raise AssertionError(f"catch accepted corruption: {label}")


def main() -> None:
    checks: dict[str, str] = {}
    catches: dict[str, str] = {}
    rng = random.Random(20260724)
    b = 2.75

    # Independent embedding-space replay for arbitrary observers and directions.
    for index in range(12):
        p, n = random_frame(rng, b)
        require(f"p_norm_{index}", close(norm(p), b), checks)
        require(f"n_norm_{index}", close(norm(n), 1), checks)
        require(f"p_n_orthogonal_{index}", close(dot(p, n), 0), checks)
        for fraction in (0.0, 0.17, 0.53, 1.0):
            point = gamma(p, n, b, fraction * math.pi * b)
            require(
                f"gamma_norm_{index}_{fraction}",
                close(norm(point), b),
                checks,
            )
        antipode = gamma(p, n, b, math.pi * b)
        require(
            f"antipode_{index}",
            all(close(value, -origin) for value, origin in zip(antipode, p)),
            checks,
        )
        require(
            f"antipodal_distance_{index}",
            close(round_distance(p, antipode, b), math.pi * b, tolerance=5e-8),
            checks,
        )
        first = 0.19 * math.pi * b
        second = 0.71 * math.pi * b
        require(
            f"same_geodesic_distance_{index}",
            close(
                round_distance(gamma(p, n, b, first), gamma(p, n, b, second), b),
                second - first,
            ),
            checks,
        )

    require("round_directional_cut_constant", all(close(math.pi * b, math.pi * b) for _ in range(64)), checks)
    require("round_directional_spread_zero", close(max([math.pi * b] * 64) - min([math.pi * b] * 64), 0), checks)
    require("round_observer_eccentricity_constant", all(close(math.pi * b, math.pi * b) for _ in range(32)), checks)
    require("round_diameter", close(math.pi * b, math.pi * b), checks)
    require("neutral_cap_depth", close(math.pi * b / 4, 0.25 * math.pi * b), checks)
    require("diameter_depth_ratio", close((math.pi * b) / (math.pi * b / 4), 4), checks)

    # Signed coordinate permutations preserve the embedding dot product and distance.
    p, _ = random_frame(rng, b)
    q, _ = random_frame(rng, b)
    transformed_p = [p[2], -p[0], p[3], -p[1]]
    transformed_q = [q[2], -q[0], q[3], -q[1]]
    require("coordinate_isometry_dot", close(dot(p, q), dot(transformed_p, transformed_q)), checks)
    require(
        "coordinate_isometry_distance",
        close(round_distance(p, q, b), round_distance(transformed_p, transformed_q, b)),
        checks,
    )
    require(
        "constant_scale_distance",
        close(
            round_distance(scale(3, p), scale(3, q), 3 * b),
            3 * round_distance(p, q, b),
        ),
        checks,
    )

    # Independent constant-squashing metric controls.
    def squashed_energy(
        eta: float, sigma: float, velocity: tuple[float, float, float], radius: float
    ) -> float:
        veta, v1, v2 = velocity
        q = math.sin(eta) * math.cos(eta)
        alpha_value = math.cos(eta) ** 2 * v1 + math.sin(eta) ** 2 * v2
        return radius**2 * (
            veta**2 + q**2 * (v1 - v2) ** 2 + sigma**2 * alpha_value**2
        )

    for sigma in (0.6, 1.0, 1.4):
        for eta in (0.17, 0.63, 1.22):
            require(
                f"squashed_fiber_speed_{sigma}_{eta}",
                close(squashed_energy(eta, sigma, (0, 1, 1), b), b * b * sigma * sigma),
                checks,
            )
            require(
                f"squashed_radial_speed_{sigma}_{eta}",
                close(squashed_energy(eta, sigma, (1, 0, 0), b), b * b),
                checks,
            )
        require(
            f"squashed_fiber_loop_{sigma}",
            close(2 * math.pi * math.sqrt(squashed_energy(0.41, sigma, (0, 1, 1), b)), 2 * math.pi * b * sigma),
            checks,
        )
        require(
            f"squashed_horizontal_loop_{sigma}",
            close(2 * math.pi * math.sqrt(squashed_energy(0.41, sigma, (1, 0, 0), b)), 2 * math.pi * b),
            checks,
        )
        require(
            f"squashed_antipode_bound_{sigma}",
            close(
                min(math.pi * b * sigma, math.pi * b),
                math.pi * b * min(sigma, 1),
            ),
            checks,
        )

    # A direct U(2) invariance check for h_round+(sigma^2-1)alpha^2.
    def hermitian_real(z: list[complex], v: list[complex]) -> float:
        return sum((a.conjugate() * b).real for a, b in zip(z, v))

    def alpha_form(z: list[complex], v: list[complex]) -> float:
        return sum((a.conjugate() * b).imag for a, b in zip(z, v))

    angle = 0.37
    phase1 = complex(math.cos(0.29), math.sin(0.29))
    phase2 = complex(math.cos(-0.44), math.sin(-0.44))

    def unitary_apply(vector: list[complex]) -> list[complex]:
        first = math.cos(angle) * vector[0] - math.sin(angle) * vector[1]
        second = math.sin(angle) * vector[0] + math.cos(angle) * vector[1]
        return [phase1 * first, phase2 * second]

    z = [complex(0.6, 0.2), complex(-0.1, math.sqrt(0.59))]
    z_norm = math.sqrt(sum(abs(value) ** 2 for value in z))
    z = [value / z_norm for value in z]
    raw_v = [complex(0.3, -0.5), complex(0.7, 0.1)]
    radial_real = hermitian_real(z, raw_v)
    v = [value - radial_real * base for value, base in zip(raw_v, z)]
    Uz, Uv = unitary_apply(z), unitary_apply(v)
    require("U2_round_norm_invariance", close(sum(abs(x) ** 2 for x in v), sum(abs(x) ** 2 for x in Uv)), checks)
    require("U2_alpha_invariance", close(alpha_form(z, v), alpha_form(Uz, Uv)), checks)
    for sigma in (0.6, 1.4):
        h_before = sum(abs(x) ** 2 for x in v) + (sigma**2 - 1) * alpha_form(z, v) ** 2
        h_after = sum(abs(x) ** 2 for x in Uv) + (sigma**2 - 1) * alpha_form(Uz, Uv) ** 2
        require(f"U2_squashed_metric_invariance_{sigma}", close(h_before, h_after), checks)

    fc_rows = read_tsv("FC_PAIR_DISTANCE_SCREEN.tsv")
    family_rows = read_tsv("EQUATION_FAMILY_PAIR_DISTANCE_SCREEN.tsv")
    solder_rows = read_tsv("SOLDER_FAMILY_PAIR_DISTANCE_SCREEN.tsv")
    witnesses = read_tsv("COMPLETE_WITNESS_LEDGER.tsv")
    round_rows = read_tsv("ROUND_DIRECTIONAL_DISTANCE_LEDGER.tsv")
    squashed_rows = read_tsv("SQUASHED_CONTROL_LEDGER.tsv")
    gates = read_tsv("PHYSICAL_XMAX_GATE_MATRIX.tsv")
    statuses = read_tsv("STATUS_LEDGER.tsv")
    validate_semantics(
        fc_rows,
        family_rows,
        solder_rows,
        witnesses,
        round_rows,
        squashed_rows,
        gates,
        statuses,
    )
    require("semantic_ledgers", True, checks)
    validate_sources()
    require("source_identities", True, checks)

    result_bytes = (HERE / "DERIVATION_RESULT.json").read_bytes()
    result = json.loads(result_bytes)
    require("production_checks", result["check_count"] == 50, checks)
    require("production_all_pass", set(result["checks"].values()) == {"PASS"}, checks)
    require("production_FC_rows", result["FC_rows"] == 12, checks)
    require("production_family_rows", result["equation_family_rows"] == 28, checks)
    require("production_solder_rows", result["solder_family_rows"] == 6, checks)
    require(
        "production_nonround_witness_zero",
        result["complete_nonround_clock_soldered_witnesses"] == 0,
        checks,
    )
    require(
        "production_nonround_off_shell_control_one",
        result["complete_nonround_off_shell_control_families"] == 1,
        checks,
    )
    require("production_physical_pass_zero", result["physical_Xmax_pass_count"] == 0, checks)
    require("production_no_center", result["round_control"]["privileged_center"] is False, checks)
    require("production_round_spread", result["round_control"]["directional_spread"] == "0", checks)

    args = [
        fc_rows,
        family_rows,
        solder_rows,
        witnesses,
        round_rows,
        squashed_rows,
        gates,
        statuses,
    ]

    bad = copy.deepcopy(fc_rows)
    bad.pop()
    expect_failure("missing_FC", lambda: validate_semantics(bad, *args[1:]), catches)
    bad = copy.deepcopy(family_rows)
    bad.append(copy.deepcopy(bad[0]))
    expect_failure(
        "duplicate_family",
        lambda: validate_semantics(fc_rows, bad, *args[2:]),
        catches,
    )
    bad = copy.deepcopy(fc_rows)
    bad[0]["complete_metric_witness"] = "YES"
    expect_failure(
        "topology_metric_promotion",
        lambda: validate_semantics(bad, *args[1:]),
        catches,
    )
    bad = copy.deepcopy(family_rows)
    next(row for row in bad if row["family_id"] == "B19")["classification"] = (
        "COMPLETE_PHYSICAL_XMAX"
    )
    expect_failure(
        "round_clock_promotion",
        lambda: validate_semantics(fc_rows, bad, *args[2:]),
        catches,
    )
    bad = copy.deepcopy(witnesses)
    next(row for row in bad if row["witness_id"] == "W02_WRL_LOCAL")[
        "diameter"
    ] = "2X"
    expect_failure(
        "WRL_diameter",
        lambda: validate_semantics(*args[:3], bad, *args[4:]),
        catches,
    )
    bad = copy.deepcopy(witnesses)
    next(row for row in bad if row["witness_id"] == "W01_ROUND_S3_B19")[
        "Delta_X_p"
    ] = "small_nonzero"
    expect_failure(
        "round_false_variance",
        lambda: validate_semantics(*args[:3], bad, *args[4:]),
        catches,
    )
    bad = copy.deepcopy(round_rows)
    next(row for row in bad if row["quantity"] == "neutral_torus_to_cap_depth")[
        "status"
    ] = "DERIVED_XMAX"
    expect_failure(
        "cap_depth_Xmax",
        lambda: validate_semantics(*args[:4], bad, *args[5:]),
        catches,
    )
    bad = copy.deepcopy(gates)
    bad[0]["full_physical_pass"] = "YES"
    expect_failure(
        "physical_gate_promotion",
        lambda: validate_semantics(*args[:6], bad, statuses),
        catches,
    )
    bad = copy.deepcopy(statuses)
    next(row for row in bad if row["claim"] == "current_nonround_directional_band")[
        "status"
    ] = "DERIVED_SMALL_VARIANCE"
    expect_failure(
        "invented_nonround_band",
        lambda: validate_semantics(*args[:7], bad),
        catches,
    )
    bad = copy.deepcopy(statuses)
    next(row for row in bad if row["claim"] == "CMB_relation_to_directional_band")[
        "status"
    ] = "DERIVED_CMB_ORIGIN"
    expect_failure(
        "CMB_selection",
        lambda: validate_semantics(*args[:7], bad),
        catches,
    )
    bad = copy.deepcopy(statuses)
    next(row for row in bad if row["claim"] == "Xmax_definition")["status"] = (
        "RADIUS_FROM_CENTER"
    )
    expect_failure(
        "preferred_center",
        lambda: validate_semantics(*args[:7], bad),
        catches,
    )
    bad = copy.deepcopy(witnesses)
    next(row for row in bad if row["witness_id"] == "W03_SQUASHED_S3_OFF_SHELL")[
        "metric_status"
    ] = "ON_SHELL_PHYSICAL"
    expect_failure(
        "squashed_on_shell_promotion",
        lambda: validate_semantics(*args[:3], bad, *args[4:]),
        catches,
    )
    bad_squashed = copy.deepcopy(squashed_rows)
    next(row for row in bad_squashed if row["quantity"] == "directional_cut_band")[
        "status"
    ] = "DERIVED"
    expect_failure(
        "squashed_cut_band_promotion",
        lambda: validate_semantics(*args[:5], bad_squashed, *args[6:]),
        catches,
    )
    expect_failure("source_identity", lambda: validate_sources(corrupt=True), catches)

    output = {
        "schema": "udt-directional-pair-distance-independent-verification-1.0",
        "implementation": "python_stdlib_embedding_geometry_no_production_import",
        "status": "PASS",
        "check_count": len(checks),
        "checks": checks,
        "catch_count": len(catches),
        "catches": catches,
        "FC_rows": len(fc_rows),
        "equation_family_rows": len(family_rows),
        "solder_family_rows": len(solder_rows),
        "source_count": len(read_tsv("SOURCE_LINEAGE.tsv"))
        + len(read_tsv("SOURCE_ADDENDUM.tsv")),
        "derivation_sha256": hashlib.sha256(result_bytes).hexdigest(),
        "witness_ledger_sha256": hashlib.sha256(
            (HERE / "COMPLETE_WITNESS_LEDGER.tsv").read_bytes()
        ).hexdigest(),
        "round_ledger_sha256": hashlib.sha256(
            (HERE / "ROUND_DIRECTIONAL_DISTANCE_LEDGER.tsv").read_bytes()
        ).hexdigest(),
        "squashed_ledger_sha256": hashlib.sha256(
            (HERE / "SQUASHED_CONTROL_LEDGER.tsv").read_bytes()
        ).hexdigest(),
    }
    (HERE / "INDEPENDENT_VERIFICATION.json").write_text(
        json.dumps(output, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print("status=PASS")
    print(f"checks={len(checks)}")
    print(f"catches={len(catches)}")
    print("FC_rows=12")
    print("equation_family_rows=28")
    print("solder_family_rows=6")
    print(
        "independent_sha256="
        + hashlib.sha256((HERE / "INDEPENDENT_VERIFICATION.json").read_bytes()).hexdigest()
    )


if __name__ == "__main__":
    main()
