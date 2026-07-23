#!/usr/bin/env python3
"""Independent matrix/adjugate verification of the phi causal-interface atlas.

This verifier deliberately does not import the production builder.  It reconstructs the
registered metric directly as a 4x4 interval matrix, obtains the inverse-norm sign from
the adjugate and determinant, and then compares only completed scientific outputs.
"""

from __future__ import annotations

import csv
import gzip
import hashlib
import importlib.util
import itertools
import json
import sys
from collections import Counter, deque
from fractions import Fraction
from pathlib import Path

from mpmath import iv
import numpy as np


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
IV_DPS = 80
MAX_DEPTH = 22
PARAMETERS = tuple(f"alpha_{index}" for index in range(10)) + ("beta",)
BASE_VALUES = tuple(map(Fraction, ("0.08", "0.14", "-0.06", "0.12", "-0.09", "0.05", "0.11", "-0.07", "0.09", "0.04")))
PAIRS = ((0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3))
POINTS = {
    "P0": (Fraction(0), Fraction(0), Fraction(0), Fraction(0)),
    "P1": (Fraction(1, 3), Fraction(-1, 4), Fraction(1, 5), Fraction(-1, 6)),
    "P2": (Fraction(-1, 4), Fraction(1, 5), Fraction(-1, 6), Fraction(1, 7)),
    "P3": (Fraction(1, 5), Fraction(1, 6), Fraction(-1, 7), Fraction(-1, 8)),
    "P4": (Fraction(-1, 6), Fraction(-1, 7), Fraction(1, 8), Fraction(1, 9)),
    "P5": (Fraction(1, 2), Fraction(0), Fraction(-1, 3), Fraction(1, 4)),
    "P6": (Fraction(0), Fraction(-1, 2), Fraction(1, 4), Fraction(-1, 3)),
    "P7": (Fraction(1, 3), Fraction(1, 3), Fraction(1, 3), Fraction(1, 3)),
}
POINT_PAIRS = {0: ("P0", "P4"), 1: ("P1", "P5"), 2: ("P2", "P6"), 3: ("P3", "P7")}


def read_tsv(path):
    opener = gzip.open if Path(path).suffix == ".gz" else open
    with opener(path, "rt", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def digest(path):
    value = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for block in iter(lambda: handle.read(131072), b""):
            value.update(block)
    return value.hexdigest()


def qiv(value):
    value = Fraction(value)
    return iv.mpf(value.numerator) / iv.mpf(value.denominator)


def interval(lo, hi):
    left, right = qiv(lo), qiv(hi)
    return iv.mpf([left.a, right.b])


def bounds(value):
    return float(value.a), float(value.b)


def coefficient(bank, field, term):
    raw = ((bank + 2) * 11 + (field + 1) * 7 + (term + 1) * 5 + (bank + 1) * (field + term + 3)) % 19 - 9
    if raw == 0:
        raw = 1 if (bank + field + term) % 2 == 0 else -1
    return Fraction(raw, 60 if term < 4 else 90 if term < 8 else 120)


def field_value(bank, field, coordinates):
    output = qiv(0)
    for index in range(4):
        output += qiv(coefficient(bank, field, index)) * coordinates[index]
    for index in range(4):
        output += qiv(coefficient(bank, field, 4 + index)) * coordinates[index] * coordinates[index] / 2
    for pair_index, (first, second) in enumerate(PAIRS):
        output += qiv(coefficient(bank, field, 8 + pair_index)) * coordinates[first] * coordinates[second]
    return output


def field_gradient(bank, field, coordinates):
    output = []
    for index in range(4):
        current = qiv(coefficient(bank, field, index))
        current += qiv(coefficient(bank, field, 4 + index)) * coordinates[index]
        for pair_index, (first, second) in enumerate(PAIRS):
            cross = qiv(coefficient(bank, field, 8 + pair_index))
            if index == first:
                current += cross * coordinates[second]
            elif index == second:
                current += cross * coordinates[first]
        output.append(current)
    return output


def permutation_sign(permutation):
    inversions = sum(permutation[i] > permutation[j] for i in range(len(permutation)) for j in range(i + 1, len(permutation)))
    return -1 if inversions % 2 else 1


def determinant(matrix):
    size = len(matrix)
    output = qiv(0)
    for permutation in itertools.permutations(range(size)):
        term = qiv(permutation_sign(permutation))
        for row, column in enumerate(permutation):
            term *= matrix[row][column]
        output += term
    return output


def minor(matrix, deleted_row, deleted_column):
    return [
        [matrix[row][column] for column in range(len(matrix)) if column != deleted_column]
        for row in range(len(matrix))
        if row != deleted_row
    ]


def cofactor(matrix, row, column):
    return qiv(-1 if (row + column) % 2 else 1) * determinant(minor(matrix, row, column))


def amplitudes(identity, carriers):
    mask = int(identity["mask_id"][1:], 16)
    complete = carriers[identity["carrier_id"]]
    selected = [Fraction(0) for _ in range(11)]
    for indices, bit in (((0, 1, 2), 1), ((3, 4, 5), 2), ((6, 7, 8, 9), 4), ((10,), 8)):
        if mask & bit:
            for index in indices:
                selected[index] = complete[index]
    return mask, selected


def matrix_interval(bank, selected, lo, hi, omit_shifts=False):
    start_name, end_name = POINT_PAIRS[bank]
    start, end = POINTS[start_name], POINTS[end_name]
    parameter = interval(lo, hi)
    coordinates = [qiv(start[index]) + parameter * qiv(end[index] - start[index]) for index in range(4)]
    latent = [
        qiv(BASE_VALUES[index]) + qiv(selected[index]) * field_value(bank, index, coordinates)
        for index in range(10)
    ]
    a, b, c, d, e, f, a20, a30, a21, a31 = latent
    u, w, r, t = iv.exp(a), iv.exp(c), iv.exp(d), iv.exp(f)
    base = [[-(u * u), -(u * b)], [-(u * b), w * w - b * b]]
    angular = [[r * r, r * e], [r * e, e * e + t * t]]
    shifts = [[a20, a21], [a30, a31]]
    if omit_shifts:
        shifts = [[qiv(0), qiv(0)], [qiv(0), qiv(0)]]
    metric = [[qiv(0) for _ in range(4)] for _ in range(4)]
    for first in range(2):
        for second in range(2):
            metric[first][second] = base[first][second]
            for angular_first in range(2):
                for angular_second in range(2):
                    metric[first][second] += (
                        angular[angular_first][angular_second]
                        * shifts[angular_first][first]
                        * shifts[angular_second][second]
                    )
        for angular_second in range(2):
            metric[first][2 + angular_second] = sum(
                (angular[angular_first][angular_second] * shifts[angular_first][first] for angular_first in range(2)),
                qiv(0),
            )
            metric[2 + angular_second][first] = metric[first][2 + angular_second]
    for first in range(2):
        for second in range(2):
            metric[2 + first][2 + second] = angular[first][second]
    gradient = [qiv(selected[10]) * value for value in field_gradient(bank, 10, coordinates)]
    determinant_value = determinant(metric)
    numerator = qiv(0)
    for first in range(4):
        for second in range(4):
            numerator += gradient[first] * cofactor(metric, second, first) * gradient[second]
    return metric, gradient, determinant_value, numerator


def classify_identity(bank, selected):
    if selected[10] == 0:
        return "IDENTICALLY_ZERO_DPHI_INTERVAL", 0, 0.0
    queue = deque([(Fraction(0), Fraction(1), 0)])
    signs = set()
    deepest = 0
    minimum_gap = float("inf")
    while queue:
        lo, hi, depth = queue.popleft()
        deepest = max(deepest, depth)
        _, _, determinant_value, numerator = matrix_interval(bank, selected, lo, hi)
        determinant_lo, determinant_hi = bounds(determinant_value)
        numerator_lo, numerator_hi = bounds(numerator)
        if determinant_hi < 0 and numerator_hi < 0:
            signs.add("SPACELIKE")
            minimum_gap = min(minimum_gap, -numerator_hi)
        elif determinant_hi < 0 and numerator_lo > 0:
            signs.add("TIMELIKE")
            minimum_gap = min(minimum_gap, numerator_lo)
        elif depth >= MAX_DEPTH:
            return "UNRESOLVED_MULTIPLE_OR_NUMERIC", deepest, 0.0
        else:
            midpoint = (lo + hi) / 2
            queue.extend(((lo, midpoint, depth + 1), (midpoint, hi, depth + 1)))
    if signs == {"SPACELIKE"}:
        return "UNIFORMLY_SPACELIKE", deepest, minimum_gap
    if signs == {"TIMELIKE"}:
        return "UNIFORMLY_TIMELIKE", deepest, minimum_gap
    return "CERTIFIED_MIXED_SIGNS", deepest, minimum_gap


def point_s(bank, selected, parameter, omit_shifts=False):
    _, _, determinant_value, numerator = matrix_interval(bank, selected, parameter, parameter, omit_shifts=omit_shifts)
    det_lo, det_hi = bounds(determinant_value)
    num_lo, num_hi = bounds(numerator)
    det = (det_lo + det_hi) / 2
    num = (num_lo + num_hi) / 2
    return num / det


def validate_saved(saved_rows, independently_classified):
    if len(saved_rows) != 3_072:
        raise AssertionError("missing saved identity")
    if len({row["identity_id"] for row in saved_rows}) != 3_072:
        raise AssertionError("duplicate saved identity")
    saved = {row["identity_id"]: row for row in saved_rows}
    for identity_id, status in independently_classified.items():
        if saved[identity_id]["causal_status"] != status:
            raise AssertionError(f"causal mismatch {identity_id}")
    return saved


def expect_failure(name, operation, catches):
    try:
        operation()
    except (AssertionError, KeyError):
        catches[name] = "PASS_REJECTED"
    else:
        raise AssertionError(f"mutation escaped: {name}")


def family_contains_d(family_id):
    return "D" in family_id.split("_")[1:]


def recompute_join_evidence(temporal_rows, classified, timelike_evidence, spacelike_evidence, claim_continuity=False):
    timelike = [
        row for row in temporal_rows
        if classified[row["identity_id"]] == "UNIFORMLY_TIMELIKE"
        and row["local_temporal_class"] == "UNIQUE_LOCAL_UNORIENTED_TIMELIKE_LINE"
        and row["motif_word"] == "LINE_PLUS_THREE"
        and family_contains_d(row["family_id"])
    ]
    spacelike = [
        row for row in temporal_rows
        if classified[row["identity_id"]] == "UNIFORMLY_SPACELIKE"
        and row["local_temporal_class"] == "RANK_ONE_LINE_SPACELIKE__LORENTZ_COMPLEMENT"
        and family_contains_d(row["family_id"])
    ]
    if len(timelike) != 720 or len(spacelike) != 2_160:
        raise AssertionError("independent phi-projector join count")
    if len({row["identity_id"] for row in timelike}) != 384:
        raise AssertionError("timelike join identity count")
    if len({row["identity_id"] for row in spacelike}) != 1_152:
        raise AssertionError("spacelike join identity count")
    if not (
        timelike_evidence["path_presentations"] == 720
        and timelike_evidence["node_presentations"] == 12_240
        and timelike_evidence["all_families_contain_D"]
        and timelike_evidence["all_nodes_s_negative"]
        and max(timelike_evidence["max_residuals"].values()) <= 1.0e-9
    ):
        raise AssertionError("frozen timelike projector evidence")
    if not (
        spacelike_evidence["path_presentations"] == 2_160
        and spacelike_evidence["node_presentations"] == 36_720
        and spacelike_evidence["all_families_contain_D"]
        and spacelike_evidence["all_nodes_s_positive"]
        and max(spacelike_evidence["max_residuals"].values()) <= 1.0e-9
    ):
        raise AssertionError("frozen spacelike projector evidence")
    if claim_continuity:
        raise AssertionError("full motif continuity is not interval-certified")
    return timelike, spacelike


def load_frozen_generator():
    source = ROOT / "udt_motif_hopf_correspondence_audit_2026-07-22/verify_correspondence_independent.py"
    source_parent = str(source.parent)
    if source_parent not in sys.path:
        sys.path.insert(0, source_parent)
    specification = importlib.util.spec_from_file_location("frozen_phi_interface_generator", source)
    module = importlib.util.module_from_spec(specification)
    assert specification.loader is not None
    sys.modules[specification.name] = module
    specification.loader.exec_module(module)
    return module


def frozen_generator_probe(classified):
    generator = load_frozen_generator()
    frozen_identities = generator.identity_data()
    if set(frozen_identities) != set(classified):
        raise AssertionError("frozen-generator identity universe")
    parameters = tuple(Fraction(value, 37) for value in (1, 5, 9, 13, 17, 21, 25, 29, 33))
    probes = 0
    minimum_abs_s = float("inf")
    for identity_id, expected in classified.items():
        if expected == "IDENTICALLY_ZERO_DPHI_INTERVAL":
            continue
        bank, selected = frozen_identities[identity_id]
        start_name, end_name = generator.POINT_PAIRS[bank]
        start = np.asarray(generator.POINTS[start_name], dtype=float)
        end = np.asarray(generator.POINTS[end_name], dtype=float)
        for parameter in parameters:
            weight = float(parameter)
            point = (1.0 - weight) * start + weight * end
            metric, _dg, _ddg, dphi, _ddphi = generator.metric_phi_jets(bank, selected, point)
            value = float(dphi @ np.linalg.solve(metric, dphi))
            observed = "UNIFORMLY_SPACELIKE" if value > 0 else "UNIFORMLY_TIMELIKE" if value < 0 else "NULL"
            if observed != expected:
                raise AssertionError(f"frozen-generator sign mismatch {identity_id} {parameter}")
            minimum_abs_s = min(minimum_abs_s, abs(value))
            probes += 1
    if probes != 13_824:
        raise AssertionError("frozen-generator probe coverage")
    return {
        "method": "DIRECT_IMPORT_OF_FROZEN_GENERATOR_FULL_MATRIX_SOLVE",
        "probe_parameters": [str(value) for value in parameters],
        "active_identity_probes": probes,
        "causal_mismatches": 0,
        "minimum_abs_s": minimum_abs_s,
    }


def main():
    iv.dps = IV_DPS
    carrier_rows = read_tsv(ROOT / "udt_structural_ensemble_metric_atlas_2026-07-21/CARRIER_VECTOR_REGISTRY.tsv")
    carriers = {row["carrier_id"]: tuple(Fraction(row[name]) for name in PARAMETERS) for row in carrier_rows}
    identities = read_tsv(ROOT / "udt_motif_hopf_correspondence_audit_2026-07-22/COHERENT_IDENTITY_REGISTRY.tsv")
    if len(identities) != 3_072 or len({row["identity_id"] for row in identities}) != 3_072:
        raise AssertionError("independent identity universe")
    independent = {}
    selected_lookup = {}
    depth_census = Counter()
    for row in identities:
        bank = int(row["bank"][1:])
        _, selected = amplitudes(row, carriers)
        selected_lookup[row["identity_id"]] = (bank, selected)
        status, depth, _gap = classify_identity(bank, selected)
        independent[row["identity_id"]] = status
        depth_census[depth] += 1

    saved_rows = read_tsv(HERE / "IDENTITY_CAUSAL_CERTIFICATES.tsv")
    saved = validate_saved(saved_rows, independent)
    for identity_id, row in saved.items():
        bank, selected = selected_lookup[identity_id]
        for parameter, field in ((Fraction(0), "s_at_u0"), (Fraction(1, 2), "s_at_umid"), (Fraction(1), "s_at_u1")):
            observed = point_s(bank, selected, parameter)
            expected = float(row[field])
            if abs(observed - expected) > 5e-14 * max(1.0, abs(observed), abs(expected)):
                raise AssertionError(f"point value mismatch {identity_id} {field}")

    bank_partition = read_tsv(HERE / "REGISTERED_BANK_CAUSAL_PARTITION.tsv")
    if len(bank_partition) != 4:
        raise AssertionError("bank partition row count")
    expected_bank_status = {}
    for bank in sorted({row["bank"] for row in identities}):
        statuses = {
            independent[row["identity_id"]]
            for row in identities
            if row["bank"] == bank and int(row["mask_id"][1:], 16) & 8
        }
        expected_bank_status[bank] = ";".join(sorted(statuses))
    if {row["bank"]: row["active_causal_status_set"] for row in bank_partition} != expected_bank_status:
        raise AssertionError("bank causal partition")
    if any(
        row["interpretation_guard"] != "REGISTERED_ANALYTIC_BANK_AND_COORDINATE_CHORD__NOT_PHYSICAL_SCALE_OR_REGIME"
        for row in bank_partition
    ):
        raise AssertionError("bank physical-regime overclaim")

    temporal_rows = read_tsv(
        ROOT / "udt_temporal_soldering_atlas_2026-07-22/PATH_TEMPORAL_CLASSIFICATION.tsv.gz"
    )
    if len(temporal_rows) != 95_232:
        raise AssertionError("frozen temporal presentation universe")
    timelike_evidence = json.loads(
        (ROOT / "udt_temporal_soldering_atlas_2026-07-22/PHI_GRADIENT_SOLDERING_RESULT.json").read_text()
    )
    spacelike_evidence = json.loads(
        (ROOT / "udt_temporal_soldering_atlas_2026-07-22/PHI_GRADIENT_SPACELIKE_BRANCH_RESULT.json").read_text()
    )
    timelike_join, spacelike_join = recompute_join_evidence(
        temporal_rows, independent, timelike_evidence, spacelike_evidence
    )
    generator_probe = frozen_generator_probe(independent)

    path_rows = read_tsv(HERE / "PATH_PRESENTATION_CAUSAL_ATLAS.tsv.gz")
    if len(path_rows) != 95_232 or len({(row["identity_id"], row["family_id"]) for row in path_rows}) != 95_232:
        raise AssertionError("path presentation universe")
    path_census = Counter(row["causal_status"] for row in path_rows)
    if path_census != Counter({status: count * 31 for status, count in Counter(independent.values()).items()}):
        raise AssertionError("path identity/presentation accounting")
    for row in path_rows:
        if row["causal_status"] != independent[row["identity_id"]]:
            raise AssertionError("path causal join mismatch")

    completion = read_tsv(HERE / "COMPLETION_CAUSAL_COMPATIBILITY.tsv")
    expected_completion = {(status, row["completion_id"]) for status in set(independent.values())
                           for row in read_tsv(ROOT / "udt_global_metric_assembly_atlas_2026-07-22/COMPLETION_CLASS_REGISTRY.tsv")}
    actual_completion = {(row["causal_status"], row["completion_id"]) for row in completion}
    if actual_completion != expected_completion or len(completion) != 36:
        raise AssertionError("completion cross")
    if any(row["compatibility_grade"] != "REQUIREMENTS_ONLY__NO_COMPLETE_METRIC_WITNESS" for row in completion):
        raise AssertionError("completion overclaim")

    catches = {}
    expect_failure(
        "MISSING_IDENTITY",
        lambda: validate_saved(saved_rows[:-1], independent),
        catches,
    )
    expect_failure(
        "DUPLICATE_IDENTITY",
        lambda: validate_saved(saved_rows + [dict(saved_rows[0])], independent),
        catches,
    )
    mutated = [dict(row) for row in saved_rows]
    mutated[0]["causal_status"] = "UNIFORMLY_TIMELIKE"
    expect_failure("FLIPPED_CAUSAL_STATUS", lambda: validate_saved(mutated, independent), catches)
    active_id = next(identity_id for identity_id, status in independent.items() if status != "IDENTICALLY_ZERO_DPHI_INTERVAL")
    active_bank, active_selected = selected_lookup[active_id]
    full_value = point_s(active_bank, active_selected, Fraction(1, 2))
    no_shift_value = point_s(active_bank, active_selected, Fraction(1, 2), omit_shifts=True)
    if abs(full_value - no_shift_value) <= 1e-12:
        for identity_id, status in independent.items():
            if status == "IDENTICALLY_ZERO_DPHI_INTERVAL":
                continue
            bank, selected = selected_lookup[identity_id]
            candidate_full = point_s(bank, selected, Fraction(1, 2))
            candidate_mutated = point_s(bank, selected, Fraction(1, 2), omit_shifts=True)
            if abs(candidate_full - candidate_mutated) > abs(full_value - no_shift_value):
                active_id, full_value, no_shift_value = identity_id, candidate_full, candidate_mutated
    if abs(full_value - no_shift_value) <= 1e-12:
        raise AssertionError("shift-omission mutation was vacuous")
    expect_failure(
        "OMITTED_SHIFT_SECTOR",
        lambda: (_ for _ in ()).throw(AssertionError()) if abs(no_shift_value - float(saved[active_id]["s_at_umid"])) > 5e-14 else None,
        catches,
    )
    mutated_paths = [dict(row) for row in path_rows]
    mutated_paths[0]["causal_status"] = "UNIFORMLY_SPACELIKE"
    expect_failure(
        "STALE_PATH_PRESENTATION_JOIN",
        lambda: (_ for _ in ()).throw(AssertionError()) if any(
            row["causal_status"] != independent[row["identity_id"]] for row in mutated_paths
        ) else None,
        catches,
    )
    mutated_completion = [dict(row) for row in completion]
    mutated_completion[0]["compatibility_grade"] = "GLOBAL_WITNESS"
    expect_failure(
        "OVERCLAIMED_GLOBAL_COMPLETION",
        lambda: (_ for _ in ()).throw(AssertionError()) if any(
            row["compatibility_grade"] != "REQUIREMENTS_ONLY__NO_COMPLETE_METRIC_WITNESS"
            for row in mutated_completion
        ) else None,
        catches,
    )
    stale_temporal = [dict(row) for row in temporal_rows]
    target = next(
        row for row in stale_temporal
        if row["local_temporal_class"] == "RANK_ONE_LINE_SPACELIKE__LORENTZ_COMPLEMENT"
    )
    target["local_temporal_class"] = "NO_PROPER_INTRINSIC_TEMPORAL_SUBSPACE"
    expect_failure(
        "STALE_PHI_PROJECTOR_JOIN",
        lambda: recompute_join_evidence(
            stale_temporal, independent, timelike_evidence, spacelike_evidence
        ),
        catches,
    )
    expect_failure(
        "FALSE_CONTINUOUS_MOTIF_CLASSIFICATION",
        lambda: recompute_join_evidence(
            temporal_rows, independent, timelike_evidence, spacelike_evidence, claim_continuity=True
        ),
        catches,
    )

    result = {
        "status": "PASS",
        "method": "INDEPENDENT_FULL_4X4_INTERVAL_MATRIX_ADJUGATE_OVER_DETERMINANT",
        "identity_causal_census": dict(sorted(Counter(independent.values()).items())),
        "path_presentation_census": dict(sorted(path_census.items())),
        "independent_subdivision_depth_census": {str(key): value for key, value in sorted(depth_census.items())},
        "identity_rows_verified": len(independent),
        "path_presentations_verified": len(path_rows),
        "completion_rows_verified": len(completion),
        "phi_projector_join_verification": {
            "timelike_path_presentations": len(timelike_join),
            "timelike_node_evidence": timelike_evidence["node_presentations"],
            "spacelike_path_presentations": len(spacelike_join),
            "spacelike_node_evidence": spacelike_evidence["node_presentations"],
            "continuous_s_sign_certified": True,
            "continuous_complete_motif_classification_certified": False,
        },
        "frozen_generator_crosscheck": generator_probe,
        "mutation_catches": catches,
        "shift_mutation_witness": {
            "identity_id": active_id,
            "full_s_mid": full_value,
            "shift_omitted_s_mid": no_shift_value,
        },
        "verified_artifact_sha256": {
            name: digest(HERE / name)
            for name in (
                "IDENTITY_CAUSAL_CERTIFICATES.tsv",
                "INTERVAL_SIGN_CERTIFICATES.tsv.gz",
                "INTERFACE_ATLAS.tsv",
                "REGISTERED_BANK_CAUSAL_PARTITION.tsv",
                "PATH_PRESENTATION_CAUSAL_ATLAS.tsv.gz",
                "COMPLETION_CAUSAL_COMPATIBILITY.tsv",
                "RESULT.json",
            )
        },
    }
    (HERE / "INDEPENDENT_VERIFICATION.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
