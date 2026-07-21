#!/usr/bin/env python3
"""Independent verifier for the bounded eleven-amplitude volume atlas.

The verifier never imports the volume-atlas builder.  It independently reconstructs the
Halton/radial design, reconciles every saved raw jet with the tabular classifications, and uses
the preceding independently written geometry verifier only as a frozen curvature/split-rank
implementation.
"""

from __future__ import annotations

import copy
import csv
import hashlib
import importlib.util
import json
import re
from collections import Counter
from fractions import Fraction
from pathlib import Path

import numpy as np


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
PARENT_VERIFIER = ROOT / "udt_independent_amplitude_metric_atlas_2026-07-21" / "verify_independent_amplitude_atlas.py"
SPEC = importlib.util.spec_from_file_location("frozen_independent_geometry_verifier", PARENT_VERIFIER)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("cannot load frozen independent geometry verifier")
independent = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(independent)

SCHEMA = "udt-amplitude-volume-metric-atlas-1.0"
CLASSIFICATION = "BOUNDED_AMPLITUDE_VOLUME_CONFIGURATIONS_OBSERVED"
MAXIMUM = "BOUNDED_ELEVEN_AMPLITUDE_INTERIOR_AND_RADIAL_CONFIGURATION_VOLUME_CHARACTERIZED"
PARAMETERS = tuple(f"alpha_{index}" for index in range(10)) + ("beta",)
HALTON_BASES = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31)
HADAMARD_COLUMNS = (1, 2, 4, 8, 16, 3, 5, 6, 7, 9, 10)
RADII = (0.125, 0.25, 0.5, 0.75, 1.0)
SCHEDULE = {0: ("P0", "P4"), 1: ("P1", "P5"), 2: ("P2", "P6"), 3: ("P3", "P7")}
PAIRS = ((0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3))
RANK_TOLERANCE = 1e-9
TOLERANCE = 2e-10
SOURCE_HASHES = {
    "udt_independent_amplitude_metric_atlas_2026-07-21/SHA256SUMS.txt": "8b7ad5fab519c6ed0d0e83a590869356d3bcffc097681997a591d7d793500aa4",
    "udt_canonical_geometry_evaluator_p01_2026-07-21/SHA256SUMS.txt": "b7d8917cb27627c7ad7767fcffbd5b5d7a9dc6da2171b2d8fba329d04014ffad",
    "udt_amplitude_volume_metric_atlas_2026-07-21/PREREGISTRATION.md": "7769083d00d14cff004dfef8f0151a16bacd729f078a6bf6fdde6eae5c331d99",
}
TABLE_NAMES = (
    "SOURCE_LINEAGE.tsv",
    "AMPLITUDE_VOLUME_DESIGN.tsv",
    "SAMPLE_SCHEDULE.tsv",
    "CONFIGURATION_OBSERVATIONS.tsv",
    "NUMERIC_RANK_MARGINS.tsv",
    "RADIAL_INCIDENCE.tsv",
    "GEOMETRIC_CLASS_CENSUS.tsv",
    "COVERAGE_LEDGER.tsv",
    "TEN_CRITERION_SCOPE.tsv",
    "ANTI_IMPOSITION_AUDIT.tsv",
)


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(131072), b""):
            value.update(block)
    return value.hexdigest()


def canonical_hash(value: object) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def tsv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def replay_manifest(path: Path) -> bool:
    base = path.parent
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line:
            continue
        expected, relative = line.split("  ", 1)
        target = base / relative
        if not target.is_file() or digest(target) != expected:
            return False
    return True


def parsed_preregistered_design(text: str) -> tuple[tuple[int, ...], tuple[int, ...], tuple[float, ...]]:
    patterns = (
        r"Use indices `1\.\.64` and bases\s+```text\s*([^`]+?)\s*```",
        r"with zero-based columns\s+```text\s*([^`]+?)\s*```",
        r"evaluate exactly five positive radii\s+```text\s*([^`]+?)\s*```",
    )
    blocks = []
    for pattern in patterns:
        match = re.search(pattern, text, flags=re.DOTALL)
        if match is None:
            raise ValueError("missing preregistered design block")
        blocks.append(match.group(1).strip().rstrip("."))
    bases = tuple(int(value.strip()) for value in blocks[0].split(","))
    columns = tuple(int(value.strip()) for value in blocks[1].split(","))
    radii = tuple(float(Fraction(value.strip())) for value in blocks[2].split(","))
    return bases, columns, radii


def registered_design_matches_active(text: str, bases=HALTON_BASES, columns=HADAMARD_COLUMNS, radii=RADII) -> bool:
    return parsed_preregistered_design(text) == (tuple(bases), tuple(columns), tuple(radii))


def sylvester(order: int) -> np.ndarray:
    matrix = np.ones((1, 1), dtype=int)
    while matrix.shape[0] < order:
        matrix = np.block([[matrix, matrix], [matrix, -matrix]])
    return matrix


def radical_inverse(index: int, base: int) -> float:
    value = 0.0
    factor = 1.0 / base
    current = index
    while current:
        current, digit = divmod(current, base)
        value += digit * factor
        factor /= base
    return value


def expected_design() -> dict[str, tuple[str, str, str, str, np.ndarray]]:
    result = {"O00": ("ORIGIN", "-", "0", "-", np.zeros(11))}
    signs = sylvester(32)[:, HADAMARD_COLUMNS]
    for direction in range(16):
        for radius_index, radius in enumerate(RADII):
            result[f"R{direction:02d}_{radius_index}"] = (
                "RADIAL", f"D{direction:02d}", str(radius), "-", radius * signs[direction].astype(float)
            )
    for index in range(1, 65):
        result[f"V{index:03d}"] = (
            "INTERIOR", "-", "-", str(index),
            np.array([2 * radical_inverse(index, base) - 1 for base in HALTON_BASES]),
        )
    return result


def dphi_class(phi_first: np.ndarray, metric: np.ndarray) -> tuple[str, float]:
    norm = float(phi_first @ np.linalg.inv(metric) @ phi_first)
    if float(np.max(np.abs(phi_first))) <= RANK_TOLERANCE:
        return "ZERO", norm
    if abs(norm) <= RANK_TOLERANCE:
        return "NONZERO_NEAR_NULL", norm
    return ("TIMELIKE" if norm < 0 else "SPACELIKE"), norm


def geometry_class(ricci_rank: int, curvature_rank: int, shear_rank: int, twist_rank: int, mixed: float) -> str:
    return f"R{ricci_rank}_K{curvature_rank}_S{shear_rank}_T{twist_rank}_M{int(mixed > RANK_TOLERANCE)}"


def validate(result: dict, tables: dict[str, list[dict[str, str]]], raw: list[dict], *, rehash: bool, anchors: bool) -> list[str]:
    checks: list[str] = []

    def require(condition: bool, name: str) -> None:
        if not condition:
            raise AssertionError(name)
        checks.append(name)

    require(result["schema"] == SCHEMA and result["status"] == "PASS", "schema_status")
    require(result["classification"] == CLASSIFICATION and result["maximum_conclusion"] == MAXIMUM, "scope_stamp")
    require(
        result["amplitude_identities"] == 145 and result["interior_rows"] == 64
        and result["radial_rows"] == 80 and result["configuration_records"] == 1160
        and result["radial_edges"] == 640,
        "result_counts",
    )
    require(
        result["ensemble_interpretation_performed"] is False
        and result["physical_transition_claimed"] is False
        and result["dynamics_loaded"] is False and result["solutions_run"] == 0
        and result["physics_ranking_used"] is False
        and result["finite_exhaustiveness_claim"] is False and result["gpu_used"] is False,
        "authority_stop",
    )

    lineage = {row["path"]: row["sha256"] for row in tables["SOURCE_LINEAGE.tsv"]}
    require(lineage == {path: value for path, value in SOURCE_HASHES.items() if "PREREGISTRATION" not in path}, "source_lineage")
    if rehash:
        require(all(digest(ROOT / path) == expected for path, expected in SOURCE_HASHES.items()), "source_and_prereg_rehash")
        require(
            all(replay_manifest(ROOT / path) for path in SOURCE_HASHES if path.endswith("SHA256SUMS.txt")),
            "all_parent_manifest_entries_replayed",
        )
        prereg = (HERE / "PREREGISTRATION.md").read_text(encoding="utf-8")
        require(registered_design_matches_active(prereg), "design_constants_parsed_from_preregistration")

    expected = expected_design()
    design = tables["AMPLITUDE_VOLUME_DESIGN.tsv"]
    require(len(design) == 145 and len({row["design_id"] for row in design}) == 145, "design_census")
    design_ok = True
    for row in design:
        identity = row["design_id"]
        if identity not in expected:
            design_ok = False
            continue
        kind, direction, radius, index, vector = expected[identity]
        saved = np.array([float(row[name]) for name in PARAMETERS])
        design_ok &= row["design_kind"] == kind and row["direction_id"] == direction
        design_ok &= row["radius"] == radius and row["halton_index"] == index
        design_ok &= bool(np.max(np.abs(saved - vector)) < 1e-15)
    require(design_ok and {row["design_id"] for row in design} == set(expected), "design_reconstructed")
    interior = np.array([expected[f"V{index:03d}"][4] for index in range(1, 65)])
    require(np.linalg.matrix_rank(interior[:, :10]) == 10 and np.linalg.matrix_rank(interior) == 11, "interior_ranks")
    require(all(np.min(interior[:, column]) < 0 < np.max(interior[:, column]) for column in range(11)), "interior_sign_coverage")
    signs = sylvester(32)[:16, HADAMARD_COLUMNS]
    require(np.linalg.matrix_rank(signs) == 11 and len({tuple(row) for row in signs}) == 16, "radial_direction_rank")

    schedule = tables["SAMPLE_SCHEDULE.tsv"]
    expected_schedule = {(f"B{bank}", point) for bank, points in SCHEDULE.items() for point in points}
    require(len(schedule) == 8 and {(row["bank"], row["point_id"]) for row in schedule} == expected_schedule, "schedule")
    require(all(int(row["design_rows"]) == 145 for row in schedule), "schedule_design_count")
    expected_ids = {f"{design_id}_B{bank}_{point}" for design_id in expected for bank, points in SCHEDULE.items() for point in points}

    observations = tables["CONFIGURATION_OBSERVATIONS.tsv"]
    obs_by_id = {row["configuration_id"]: row for row in observations}
    require(len(observations) == 1160 and len(obs_by_id) == 1160 and set(obs_by_id) == expected_ids, "observation_census")
    require(all(row["retained"] == "YES" and row["physical_merit"] == "NOT_EVALUATED" for row in observations), "no_filter")
    require(all(row["inertia"] == "1,3,0" and int(row["latent_to_slot_rank"]) == 10 for row in observations), "regular_lorentzian_chart")
    require(max(float(row["identity_residual"]) for row in observations) < TOLERANCE, "identity_gate")

    raw_by_id = {row["configuration_id"]: row for row in raw}
    require(len(raw) == 1160 and len(raw_by_id) == 1160 and set(raw_by_id) == expected_ids, "raw_census")
    recomputed_class: Counter[str] = Counter()
    recomputed_kind: Counter[str] = Counter()
    recomputed_dphi: Counter[str] = Counter()
    recomputed_phi = Counter()
    raw_ok = True
    for config_id, saved in raw_by_id.items():
        observation = obs_by_id[config_id]
        identity = {"slots": saved["slot_values"], "slot_first": saved["slot_first"], "slot_second": saved["slot_second"], "phi": saved["phi"]}
        metric_jet = {"metric": saved["metric"], "first": saved["metric_first"], "second": saved["metric_second"]}
        raw_ok &= canonical_hash(identity) == saved["configuration_sha256"] == observation["configuration_sha256"]
        raw_ok &= canonical_hash(metric_jet) == saved["metric_jet_sha256"] == observation["metric_jet_sha256"]
        ricci = np.asarray(saved["ricci"])
        riemann = np.asarray(saved["riemann_down"])
        curvature = np.array([[riemann[a, b, c, d] for c, d in PAIRS] for a, b in PAIRS])
        ricci_rank = int(np.linalg.matrix_rank(ricci, tol=RANK_TOLERANCE))
        curvature_rank = int(np.linalg.matrix_rank(curvature, tol=RANK_TOLERANCE))
        shear_rank, twist_rank = independent.independent_split_ranks(np.asarray(saved["slot_values"]), np.asarray(saved["slot_first"]))
        mixed_values = []
        for i in range(2):
            for j in range(2):
                for a in range(2, 4):
                    for b in range(2, 4):
                        mixed_values.extend((riemann[i, a, j, b], riemann[i, j, a, b]))
        mixed = float(np.max(np.abs(mixed_values)))
        dphi, phi_norm = dphi_class(np.asarray(saved["phi"]["first"]), np.asarray(saved["metric"]))
        class_id = geometry_class(ricci_rank, curvature_rank, shear_rank, twist_rank, mixed)
        raw_ok &= ricci_rank == int(observation["ricci_rank"])
        raw_ok &= curvature_rank == int(observation["curvature_operator_rank"])
        raw_ok &= shear_rank == int(observation["shear_rank"]) and twist_rank == int(observation["twist_rank"])
        raw_ok &= abs(mixed - float(observation["mixed_curvature_max_abs"])) < 2e-12
        raw_ok &= abs(phi_norm - float(observation["phi_gradient_norm"])) < 2e-12
        raw_ok &= dphi == observation["dphi_class"] and class_id == observation["geometry_class"]
        recomputed_class[class_id] += 1
        recomputed_kind[observation["design_kind"]] += 1
        recomputed_dphi[dphi] += 1
        phi_value = float(saved["phi"]["value"])
        recomputed_phi["negative" if phi_value < -RANK_TOLERANCE else "positive" if phi_value > RANK_TOLERANCE else "near_zero"] += 1
    require(raw_ok, "all_raw_geometry_and_hashes")
    if rehash:
        require(digest(HERE / "RAW_CONFIGURATION_JETS.jsonl") == result["raw_configuration_sha256"], "raw_file_hash")

    observed_census = result["observed_census"]
    require(dict(sorted(recomputed_class.items())) == observed_census["geometry_class_counts"], "geometry_census")
    require(dict(sorted(recomputed_kind.items())) == observed_census["design_kind_counts"], "design_kind_census")
    require(dict(sorted(recomputed_dphi.items())) == observed_census["dphi_class_counts"], "dphi_census")
    require(dict(recomputed_phi) == observed_census["phi_sign_counts"], "phi_sign_census")

    class_table = tables["GEOMETRIC_CLASS_CENSUS.tsv"]
    table_counts = {(row["design_kind"], row["geometry_class"]): int(row["records"]) for row in class_table}
    expected_counts = Counter((row["design_kind"], row["geometry_class"]) for row in observations)
    require(table_counts == dict(expected_counts) and sum(table_counts.values()) == 1160, "class_table_reconciled")

    margins = tables["NUMERIC_RANK_MARGINS.tsv"]
    margin_by_id = {row["configuration_id"]: row for row in margins}
    margin_ok = len(margins) == 1160 and set(margin_by_id) == expected_ids
    for config_id, saved in raw_by_id.items():
        row = margin_by_id[config_id]
        slot_values = np.asarray(saved["slot_values"])
        slot_first = np.asarray(saved["slot_first"])
        screen = np.array([[slot_values[3], slot_values[4]], [slot_values[4], slot_values[5]]])
        shifts = np.array([[slot_values[6], slot_values[8]], [slot_values[7], slot_values[9]]])
        screen_first = [np.array([[slot_first[k, 3], slot_first[k, 4]], [slot_first[k, 4], slot_first[k, 5]]]) for k in range(4)]
        shifts_first = [np.array([[slot_first[k, 6], slot_first[k, 8]], [slot_first[k, 7], slot_first[k, 9]]]) for k in range(4)]
        inverse_screen = np.linalg.inv(screen)
        twist = np.zeros(2)
        for vertical in range(2):
            twist[vertical] = (
                shifts_first[0][vertical, 1] - shifts_first[1][vertical, 0]
                - sum(shifts[other, 0] * shifts_first[2 + other][vertical, 1] for other in range(2))
                + sum(shifts[other, 1] * shifts_first[2 + other][vertical, 0] for other in range(2))
            )
        shear_rows = []
        for base in range(2):
            horizontal = screen_first[base] - sum(shifts[vertical, base] * screen_first[2 + vertical] for vertical in range(2))
            vertical_derivative = np.array([[shifts_first[2 + derivative][output, base] for output in range(2)] for derivative in range(2)])
            deformation = 0.5 * (horizontal - vertical_derivative @ screen - screen @ vertical_derivative.T)
            expansion = float(np.trace(inverse_screen @ deformation))
            shear = deformation - 0.5 * expansion * screen
            shear_rows.append((shear[0, 0], shear[0, 1], shear[1, 1]))
        shear_singular = np.linalg.svd(np.asarray(shear_rows), compute_uv=False)
        margin_ok &= abs(float(row["ricci_min_singular"]) - min(saved["ricci_singular_values"])) < 2e-14
        margin_ok &= abs(float(row["curvature_min_singular"]) - min(saved["curvature_singular_values"])) < 2e-14
        margin_ok &= abs(float(row["shear_min_singular"]) - min(shear_singular)) < 2e-14
        margin_ok &= abs(float(row["twist_norm"]) - float(np.linalg.norm(twist))) < 2e-14
        margin_ok &= abs(float(row["mixed_curvature_max_abs"]) - float(obs_by_id[config_id]["mixed_curvature_max_abs"])) < 2e-14
        margin_ok &= int(row["ricci_rank"]) == int(obs_by_id[config_id]["ricci_rank"])
        margin_ok &= int(row["curvature_operator_rank"]) == int(obs_by_id[config_id]["curvature_operator_rank"])
        margin_ok &= int(row["shear_rank"]) == int(obs_by_id[config_id]["shear_rank"])
        margin_ok &= int(row["twist_rank"]) == int(obs_by_id[config_id]["twist_rank"])
        margin_ok &= float(row["rank_threshold"]) == RANK_TOLERANCE
    require(margin_ok, "rank_margins_reconciled")

    incidence = tables["RADIAL_INCIDENCE.tsv"]
    require(len(incidence) == 640 and len({row["edge_id"] for row in incidence}) == 640, "radial_edge_census")
    edge_ok = True
    changed = 0
    for row in incidence:
        left, right = obs_by_id[row["from_configuration"]], obs_by_id[row["to_configuration"]]
        edge = int(row["edge_id"].rsplit("E", 1)[1])
        diagnostic = any(left[field] != right[field] for field in ("ricci_rank", "curvature_operator_rank", "shear_rank", "twist_rank", "geometry_class", "dphi_class"))
        changed += diagnostic
        edge_ok &= row["diagnostic_tuple_changed"] == ("YES" if diagnostic else "NO")
        edge_ok &= row["physical_transition_claimed"] == "NO"
        edge_ok &= abs(float(row["from_radius"]) - (0.0 if edge == 0 else RADII[edge - 1])) < 1e-15
        edge_ok &= abs(float(row["to_radius"]) - RADII[edge]) < 1e-15
        edge_ok &= int(row["ricci_rank_change"]) == int(right["ricci_rank"]) - int(left["ricci_rank"])
        edge_ok &= int(row["curvature_rank_change"]) == int(right["curvature_operator_rank"]) - int(left["curvature_operator_rank"])
        edge_ok &= int(row["shear_rank_change"]) == int(right["shear_rank"]) - int(left["shear_rank"])
        edge_ok &= int(row["twist_rank_change"]) == int(right["twist_rank"]) - int(left["twist_rank"])
    require(edge_ok and changed == 128, "radial_edges_reconciled")
    require(observed_census["radial_changed_edges"] == changed and observed_census["radial_unchanged_edges"] == 640 - changed, "radial_result_reconciled")

    require(len(tables["COVERAGE_LEDGER.tsv"]) == 9 and all(row["status"] == "PASS" for row in tables["COVERAGE_LEDGER.tsv"]), "coverage_ledger")
    require(len(tables["TEN_CRITERION_SCOPE.tsv"]) == 10, "ten_criterion_scope")
    anti = tables["ANTI_IMPOSITION_AUDIT.tsv"]
    require(len(anti) == 10 and all(row["present"] == "ABSENT" for row in anti), "anti_imposition")

    if anchors:
        reconstruction_errors = []
        for saved in raw:
            riemann, ricci, scalar = independent.independent_curvature(
                np.asarray(saved["metric"]), np.asarray(saved["metric_first"]), np.asarray(saved["metric_second"])
            )
            reconstruction_errors.append(
                max(
                    float(np.max(np.abs(riemann - np.asarray(saved["riemann_down"])))),
                    float(np.max(np.abs(ricci - np.asarray(saved["ricci"])))),
                    abs(scalar - float(saved["observables"]["scalar_curvature"])),
                )
            )
        require(max(reconstruction_errors) < TOLERANCE, "all_1160_curvatures_reconstructed")
        for anchor_id in ("O00_B0_P0", "V037_B2_P6", "R07_4_B3_P7"):
            saved = raw_by_id[anchor_id]
            riemann, ricci, scalar = independent.independent_curvature(
                np.asarray(saved["metric"]), np.asarray(saved["metric_first"]), np.asarray(saved["metric_second"])
            )
            require(np.max(np.abs(riemann - np.asarray(saved["riemann_down"]))) < TOLERANCE, f"curvature_anchor_{anchor_id}")
            require(np.max(np.abs(ricci - np.asarray(saved["ricci"]))) < TOLERANCE, f"ricci_anchor_{anchor_id}")
            require(abs(scalar - float(saved["observables"]["scalar_curvature"])) < TOLERANCE, f"scalar_anchor_{anchor_id}")
    return checks


def main() -> None:
    result = json.loads((HERE / "ATLAS_RESULT.json").read_text(encoding="utf-8"))
    tables = {name: tsv(HERE / name) for name in TABLE_NAMES}
    raw = [json.loads(line) for line in (HERE / "RAW_CONFIGURATION_JETS.jsonl").read_text(encoding="utf-8").splitlines()]
    checks = validate(result, tables, raw, rehash=True, anchors=True)

    catches: list[str] = []

    def catch(name: str, mutator) -> None:
        changed_result, changed_tables, changed_raw = copy.deepcopy(result), copy.deepcopy(tables), copy.deepcopy(raw)
        mutator(changed_result, changed_tables, changed_raw)
        try:
            validate(changed_result, changed_tables, changed_raw, rehash=False, anchors=False)
        except (AssertionError, KeyError, ValueError, IndexError):
            catches.append(name)
            return
        raise AssertionError(f"uncaught_mutation_{name}")

    catch("missing_design", lambda _r, t, _w: t["AMPLITUDE_VOLUME_DESIGN.tsv"].pop())
    catch("duplicate_design", lambda _r, t, _w: t["AMPLITUDE_VOLUME_DESIGN.tsv"].__setitem__(1, copy.deepcopy(t["AMPLITUDE_VOLUME_DESIGN.tsv"][0])))
    catch("changed_halton_coordinate", lambda _r, t, _w: t["AMPLITUDE_VOLUME_DESIGN.tsv"][-1].__setitem__("beta", "0.0"))
    catch("changed_halton_base", lambda _r, t, _w: t["AMPLITUDE_VOLUME_DESIGN.tsv"][81].__setitem__("alpha_1", "0.25"))
    catch("changed_hadamard_direction", lambda _r, t, _w: t["AMPLITUDE_VOLUME_DESIGN.tsv"][1].__setitem__("alpha_0", "-0.125"))
    catch("changed_radius", lambda _r, t, _w: t["AMPLITUDE_VOLUME_DESIGN.tsv"][1].__setitem__("radius", "0.2"))
    catch("missing_observation", lambda _r, t, _w: t["CONFIGURATION_OBSERVATIONS.tsv"].pop())
    catch("raw_jet_mutation", lambda _r, _t, w: w[100]["metric"].__setitem__(0, [0.0, 0.0, 0.0, 0.0]))
    catch("class_mutation", lambda _r, t, _w: t["CONFIGURATION_OBSERVATIONS.tsv"][10].__setitem__("geometry_class", "R0_K0_S0_T0_M0"))
    catch("rank_margin_mutation", lambda _r, t, _w: t["NUMERIC_RANK_MARGINS.tsv"][10].__setitem__("rank_threshold", "1e-6"))
    catch("edge_mutation", lambda _r, t, _w: t["RADIAL_INCIDENCE.tsv"][0].__setitem__("diagnostic_tuple_changed", "NO"))
    catch("filtered_record", lambda _r, t, _w: t["CONFIGURATION_OBSERVATIONS.tsv"][10].__setitem__("retained", "NO"))
    catch("ensemble_promotion", lambda r, _t, _w: r.__setitem__("ensemble_interpretation_performed", True))
    catch("physical_transition_promotion", lambda r, _t, _w: r.__setitem__("physical_transition_claimed", True))
    catch("dynamics_promotion", lambda r, _t, _w: r.__setitem__("dynamics_loaded", True))
    catch("solution_promotion", lambda r, _t, _w: r.__setitem__("solutions_run", 1))
    catch("finite_exhaustiveness", lambda r, _t, _w: r.__setitem__("finite_exhaustiveness_claim", True))
    catch("census_corruption", lambda r, _t, _w: r["observed_census"]["geometry_class_counts"].__setitem__("R4_K6_S2_T1_M1", 0))
    catch("anti_imposition_corruption", lambda _r, t, _w: t["ANTI_IMPOSITION_AUDIT.tsv"][1].__setitem__("present", "PRESENT"))
    prereg = (HERE / "PREREGISTRATION.md").read_text(encoding="utf-8")
    if registered_design_matches_active(prereg, bases=(2, 5, *HALTON_BASES[2:])):
        raise AssertionError("uncaught_common_mode_design_constant_drift")
    catches.append("common_mode_design_constant_drift")

    output = {
        "schema": "udt-amplitude-volume-metric-atlas-verification-1.0",
        "status": "PASS",
        "independent_checks": len(checks),
        "catch_proofs": len(catches),
        "catches": catches,
        "volume_builder_imported": False,
        "frozen_independent_geometry_verifier_reused": True,
        "all_configuration_curvatures_reconstructed": 1160,
        "curvature_anchors": ["O00_B0_P0", "V037_B2_P6", "R07_4_B3_P7"],
        "classification_verified": CLASSIFICATION,
        "maximum_verified": MAXIMUM,
    }
    (HERE / "VERIFICATION_RESULT.json").write_text(json.dumps(output, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    transcript = [
        "UDT_AMPLITUDE_VOLUME_ATLAS_VERIFICATION=PASS",
        f"independent_checks={len(checks)} catch_proofs={len(catches)}",
        "volume_builder_imported=NO frozen_independent_geometry_verifier_reused=YES",
        "design=145 configurations=1160 radial_edges=640 ALL_RECONCILED",
        "all_1160_curvatures_reconstructed=PASS anchors=O00_B0_P0,V037_B2_P6,R07_4_B3_P7",
        f"classification={CLASSIFICATION}",
        f"maximum={MAXIMUM}",
    ]
    (HERE / "VERIFICATION_TRANSCRIPT.txt").write_text("\n".join(transcript) + "\n", encoding="utf-8")
    print("\n".join(transcript))


if __name__ == "__main__":
    main()
