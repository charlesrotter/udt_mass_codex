#!/usr/bin/env python3
"""Independent block-metric and high-precision verification of the simplex atlas."""

from __future__ import annotations

import csv
import copy
import gzip
import hashlib
import itertools
import json
import math
import platform
import sys
from collections import Counter
from fractions import Fraction
from pathlib import Path

from mpmath import iv
import numpy as np


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
CARRIER_FILE = (
    ROOT
    / "udt_structural_ensemble_metric_atlas_2026-07-21"
    / "CARRIER_VECTOR_REGISTRY.tsv"
)
CENSUS_FILE = HERE / "LATTICE_SHEET_CENSUS.tsv"
COORDINATE_FILE = HERE / "LATTICE_COORDINATES.json"
RESULT_FILE = HERE / "RESULT.json"
PRIOR_SHEET_FILE = (
    ROOT
    / "udt_configuration_space_adjacency_atlas_2026-07-22"
    / "SHEET_CLASSIFICATION.tsv"
)
ENDPOINT_PAIR_FILE = (
    ROOT
    / "udt_configuration_space_adjacency_atlas_2026-07-22"
    / "ENDPOINT_PAIR_REGISTRY.tsv"
)
EXPECTED_SOURCE_HASHES = {
    "udt_configuration_space_adjacency_atlas_2026-07-22/ENDPOINT_PAIR_REGISTRY.tsv":
        "bab9c0b7e5ba1966a9521cecd3aff5a576b0e83bb97bbf0e100065d661038ac7",
    "udt_configuration_space_adjacency_atlas_2026-07-22/SHEET_CLASSIFICATION.tsv":
        "3d5a01c86ee7576a4a6c13917b5bed3315373c731bd8fa8fc9603e2d9e4041ca",
    "udt_structural_ensemble_metric_atlas_2026-07-21/CARRIER_VECTOR_REGISTRY.tsv":
        "b1251073a9f8e916259d29ebcae71a9b86a5f8235c3b0b581430967d6aeadbe8",
}
PARAMETERS = tuple(f"alpha_{index}" for index in range(10)) + ("beta",)
BASE_VALUES = tuple(
    map(
        Fraction,
        ("0.08", "0.14", "-0.06", "0.12", "-0.09", "0.05", "0.11",
         "-0.07", "0.09", "0.04"),
    )
)
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
CHARTS = ("J1_GENERATOR_COEFFICIENT_BARYCENTRIC", "J2_EVALUATED_COFIELD_BARYCENTRIC")
ZERO_MULTIPLIER = 64.0
POINT_BATCH = 4096
GROUP_BATCH = 8


def coefficient(bank, field, term):
    raw = (
        (bank + 2) * 11
        + (field + 1) * 7
        + (term + 1) * 5
        + (bank + 1) * (field + term + 3)
    ) % 19 - 9
    if raw == 0:
        raw = 1 if (bank + field + term) % 2 == 0 else -1
    return Fraction(raw, 60 if term < 4 else 90 if term < 8 else 120)


COEFFICIENTS = tuple(
    tuple(
        tuple(coefficient(bank, field, term) for term in range(14))
        for field in range(11)
    )
    for bank in range(4)
)
FLOAT_COEFFICIENTS = np.asarray(COEFFICIENTS, dtype=np.float64)
FLOAT_BASE = np.asarray(BASE_VALUES, dtype=np.float64)


def read_tsv(path):
    with Path(path).open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def write_tsv(path, fieldnames, rows):
    with Path(path).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle, fieldnames=fieldnames, delimiter="\t", lineterminator="\n"
        )
        writer.writeheader()
        writer.writerows(rows)


def digest(path):
    value = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for block in iter(lambda: handle.read(131072), b""):
            value.update(block)
    return value.hexdigest()


def fmt(value):
    return f"{float(value):.17g}"


def amplitude_vector(carrier, mask):
    output = [Fraction(0) for _ in range(11)]
    for indices, bit in (
        ((0, 1, 2), 1),
        ((3, 4, 5), 2),
        ((6, 7, 8, 9), 4),
        ((10,), 8),
    ):
        if mask & bit:
            for index in indices:
                output[index] = carrier[index]
    return tuple(output)


def load_groups():
    carriers = {
        row["carrier_id"]: tuple(Fraction(row[name]) for name in PARAMETERS)
        for row in read_tsv(CARRIER_FILE)
    }
    rows = []
    amplitudes = []
    for carrier_id in sorted(carriers):
        for mask in range(8, 16):
            rows.append(
                {
                    "group_index": len(rows),
                    "group_id": f"{carrier_id}_M{mask:X}",
                    "carrier_id": carrier_id,
                    "mask_id": f"M{mask:X}",
                }
            )
            amplitudes.append(amplitude_vector(carriers[carrier_id], mask))
    if len(rows) != 384:
        raise AssertionError("independent group reconstruction")
    return rows, amplitudes


def bank_coordinates(bank, u):
    start_name, end_name = POINT_PAIRS[bank]
    start = np.asarray(POINTS[start_name], dtype=np.float64)
    end = np.asarray(POINTS[end_name], dtype=np.float64)
    return start[None, :] + u[:, None] * (end - start)[None, :]


def field_values(coefficients, coordinates):
    values = np.sum(coefficients[..., :4] * coordinates[..., None, :], axis=-1)
    values += np.sum(
        coefficients[..., 4:8] * coordinates[..., None, :] ** 2 / 2.0,
        axis=-1,
    )
    for pair_index, (first, second) in enumerate(PAIRS):
        values += (
            coefficients[..., 8 + pair_index]
            * coordinates[..., None, first]
            * coordinates[..., None, second]
        )
    return values


def field_gradient(coefficients, coordinates):
    output = np.empty(coordinates.shape[:-1] + (4,), dtype=np.float64)
    for axis in range(4):
        value = coefficients[..., axis] + coefficients[..., 4 + axis] * coordinates[..., axis]
        for pair_index, (first, second) in enumerate(PAIRS):
            if axis == first:
                value = value + coefficients[..., 8 + pair_index] * coordinates[..., second]
            elif axis == second:
                value = value + coefficients[..., 8 + pair_index] * coordinates[..., first]
        output[..., axis] = value
    return output


def independent_basis(chart, u, q, t):
    bank_points = np.stack([bank_coordinates(bank, u) for bank in range(4)], axis=1)
    weights = np.column_stack(((1.0 - t)[:, None] * q, t))
    if chart.startswith("J1"):
        point = np.einsum("pb,pbd->pd", weights, bank_points)
        coefficients = np.einsum("pb,bft->pft", weights, FLOAT_COEFFICIENTS)
        values = field_values(coefficients, point)
        return values[:, :10], field_gradient(coefficients[:, 10, :], point)
    bank_values = []
    bank_gradient = []
    for bank in range(4):
        values = field_values(
            FLOAT_COEFFICIENTS[bank][None, :, :], bank_points[:, bank, :]
        )
        bank_values.append(values[:, :10])
        bank_gradient.append(
            field_gradient(
                FLOAT_COEFFICIENTS[bank, 10, :][None, :],
                bank_points[:, bank, :],
            )
        )
    return (
        np.einsum("pb,bpf->pf", weights, np.asarray(bank_values)),
        np.einsum("pb,bpd->pd", weights, np.asarray(bank_gradient)),
    )


def block_metric_scalar(amplitudes, features, unit_gradient):
    """Use independently assembled h/q/shift blocks and their Schur inverse."""
    amplitudes = np.asarray(amplitudes, dtype=np.float64)
    latent = [
        FLOAT_BASE[field]
        + amplitudes[:, field, None] * features[None, :, field]
        for field in range(10)
    ]
    beta = amplitudes[:, 10, None]
    p0, p1, p2, p3 = [
        beta * unit_gradient[None, :, axis] for axis in range(4)
    ]
    a, b, c, d, e, f, a20, a30, a21, a31 = latent
    u = np.exp(a)
    w = np.exp(c)
    radial = np.exp(d)
    transverse = np.exp(f)

    h00 = -(u * u)
    h01 = -(u * b)
    h11 = w * w - b * b
    q00 = radial * radial
    q01 = radial * e
    q11 = e * e + transverse * transverse
    hdet = h00 * h11 - h01 * h01
    qdet = q00 * q11 - q01 * q01

    shifted0 = p0 - a20 * p2 - a30 * p3
    shifted1 = p1 - a21 * p2 - a31 * p3
    base_quadratic = (
        h11 * shifted0 * shifted0
        - 2.0 * h01 * shifted0 * shifted1
        + h00 * shifted1 * shifted1
    ) / hdet
    angular_quadratic = (
        q11 * p2 * p2 - 2.0 * q01 * p2 * p3 + q00 * p3 * p3
    ) / qdet
    scalar = base_quadratic + angular_quadratic
    determinant = hdet * qdet
    return scalar, determinant


def lattice_arrays(payload):
    triples = np.asarray(payload["barycentric_integer_triples"], dtype=np.float64)
    denominator = int(payload["barycentric_denominator"])
    q_nodes = triples / denominator
    u_nodes = np.asarray(payload["u_nodes"], dtype=np.float64)
    t_nodes = np.asarray(payload["t_nodes"], dtype=np.float64)
    u, q_index, t = np.meshgrid(
        u_nodes,
        np.arange(len(q_nodes), dtype=np.int64),
        t_nodes,
        indexing="ij",
    )
    return (
        u.reshape(-1),
        q_nodes[q_index.reshape(-1)],
        t.reshape(-1),
        (len(u_nodes), len(q_nodes), len(t_nodes)),
    )


def load_signs(path):
    with gzip.open(path, "rb") as handle:
        return np.load(handle, allow_pickle=False)


def independent_node_replay(group_rows, amplitude_rows, coordinates, census):
    census_lookup = {
        (row["level"], row["sheet_id"]): row for row in census
    }
    replay_rows = []
    selected_values = {}
    total_nodes = 0
    sign_mismatches = 0
    transition_mismatches = 0
    determinant_failures = 0
    amplitudes = np.asarray(amplitude_rows, dtype=np.float64)
    for level in ("L1", "L2"):
        u, q, t, shape = lattice_arrays(coordinates[level])
        nodes = len(u)
        for chart in CHARTS:
            short = "J1" if chart.startswith("J1") else "J2"
            raw_path = HERE / f"RAW_SIGNS_{level}_{short}.npy.gz"
            saved = load_signs(raw_path)
            if saved.shape != (384, nodes):
                raise AssertionError("raw sign shape")
            features = np.empty((nodes, 10), dtype=np.float64)
            gradient = np.empty((nodes, 4), dtype=np.float64)
            for start in range(0, nodes, POINT_BATCH):
                stop = min(start + POINT_BATCH, nodes)
                features[start:stop], gradient[start:stop] = independent_basis(
                    chart, u[start:stop], q[start:stop], t[start:stop]
                )
            for group_start in range(0, 384, GROUP_BATCH):
                group_stop = min(group_start + GROUP_BATCH, 384)
                values, determinant = block_metric_scalar(
                    amplitudes[group_start:group_stop], features, gradient
                )
                determinant_failures += int(np.sum(determinant >= 0.0))
                for local, group_index in enumerate(range(group_start, group_stop)):
                    current = values[local]
                    threshold = (
                        ZERO_MULTIPLIER
                        * np.finfo(np.float64).eps
                        * max(1.0, float(np.max(np.abs(current))))
                    )
                    signs = np.where(
                        current > threshold, 1, np.where(current < -threshold, -1, 0)
                    ).astype(np.int8)
                    mismatch = int(np.sum(signs != saved[group_index]))
                    sign_mismatches += mismatch
                    sheet_id = f"{group_rows[group_index]['group_id']}_{short}"
                    row = census_lookup[(level, sheet_id)]
                    transition = np.sum(
                        signs.reshape(shape)[:, :, 1:]
                        != signs.reshape(shape)[:, :, :-1],
                        axis=2,
                    )
                    observed = {
                        0: int(np.sum(transition == 0)),
                        1: int(np.sum(transition == 1)),
                        2: int(np.sum(transition == 2)),
                        3: int(np.sum(transition >= 3)),
                    }
                    expected = {
                        0: int(row["transition_count_0_fibers"]),
                        1: int(row["transition_count_1_fibers"]),
                        2: int(row["transition_count_2_fibers"]),
                        3: int(row["transition_count_3plus_fibers"]),
                    }
                    transition_mismatches += int(observed != expected)
                    if level == "L2":
                        selected_values[(chart, group_index)] = current.copy()
                    total_nodes += nodes
            replay_rows.append(
                {
                    "level": level,
                    "chart": chart,
                    "sheets": 384,
                    "nodes_per_sheet": nodes,
                    "node_signs_checked": 384 * nodes,
                    "raw_sign_sha256": digest(raw_path),
                    "status": "ALL_NODE_SIGNS_AND_TRANSITION_COUNTS_REPRODUCED",
                }
            )
    return {
        "rows": replay_rows,
        "total_nodes": total_nodes,
        "sign_mismatches": sign_mismatches,
        "transition_mismatches": transition_mismatches,
        "determinant_failures": determinant_failures,
        "selected_values": selected_values,
    }


def boundary_edge_replay(coordinates):
    same_sign_nodes = 0
    cross_fibers = 0
    failures = 0
    for level in ("L1", "L2"):
        payload = coordinates[level]
        triples = [tuple(item) for item in payload["barycentric_integer_triples"]]
        denominator = int(payload["barycentric_denominator"])
        shape = (
            len(payload["u_nodes"]),
            len(triples),
            len(payload["t_nodes"]),
        )
        boundary_indices = [
            index for index, triple in enumerate(triples) if 0 in triple
        ]
        vertex_indices = [
            triples.index(vertex)
            for vertex in (
                (denominator, 0, 0),
                (0, denominator, 0),
                (0, 0, denominator),
            )
        ]
        for chart in ("J1", "J2"):
            raw = load_signs(HERE / f"RAW_SIGNS_{level}_{chart}.npy.gz")
            signs = raw.reshape((384,) + shape)
            base_edges = signs[:, :, boundary_indices, 0]
            same_sign_nodes += base_edges.size
            failures += int(np.sum(base_edges != 1))
            radial = signs[:, :, vertex_indices, :]
            transitions = np.sum(radial[:, :, :, 1:] != radial[:, :, :, :-1], axis=3)
            cross_fibers += transitions.size
            failures += int(np.sum(transitions != 1))
    prior = read_tsv(PRIOR_SHEET_FILE)
    prior_counts = Counter(row["primary_class"] for row in prior)
    prior_ok = (
        len(prior) == 4608
        and prior_counts["UNIFORMLY_SPACELIKE_SHEET"] == 2304
        and prior_counts["FORCED_SINGLE_REGULAR_NULL_GRAPH"] == 2304
    )
    return {
        "same_sign_boundary_nodes_checked": same_sign_nodes,
        "cross_sector_boundary_fibers_checked": cross_fibers,
        "boundary_failures": failures,
        "prior_sheet_rows": len(prior),
        "prior_class_counts": dict(prior_counts),
        "prior_adjacency_status": "REPRODUCED" if prior_ok else "MISMATCH",
    }


def qiv(value):
    value = Fraction(value)
    return iv.mpf(value.numerator) / iv.mpf(value.denominator)


def iv_det(matrix):
    size = len(matrix)
    if size == 1:
        return matrix[0][0]
    output = qiv(0)
    for column in range(size):
        minor = [
            [matrix[row][other] for other in range(size) if other != column]
            for row in range(1, size)
        ]
        output += (-1 if column % 2 else 1) * matrix[0][column] * iv_det(minor)
    return output


def iv_bounds(value):
    return float(value.a), float(value.b)


def iv_field_value(coefficients, point):
    output = qiv(0)
    for axis in range(4):
        output += coefficients[axis] * point[axis]
        output += coefficients[4 + axis] * point[axis] * point[axis] / qiv(2)
    for pair_index, (first, second) in enumerate(PAIRS):
        output += coefficients[8 + pair_index] * point[first] * point[second]
    return output


def iv_field_gradient(coefficients, point):
    output = []
    for axis in range(4):
        value = coefficients[axis] + coefficients[4 + axis] * point[axis]
        for pair_index, (first, second) in enumerate(PAIRS):
            if axis == first:
                value += coefficients[8 + pair_index] * point[second]
            elif axis == second:
                value += coefficients[8 + pair_index] * point[first]
        output.append(value)
    return output


def iv_point_full_matrix(chart, amplitudes, u, q, t):
    bank_points = []
    for bank in range(4):
        start_name, end_name = POINT_PAIRS[bank]
        bank_points.append(
            [
                qiv(POINTS[start_name][axis])
                + qiv(u)
                * qiv(POINTS[end_name][axis] - POINTS[start_name][axis])
                for axis in range(4)
            ]
        )
    weights = [(qiv(1) - qiv(t)) * qiv(item) for item in q] + [qiv(t)]
    if chart.startswith("J1"):
        point = [
            sum((weights[bank] * bank_points[bank][axis] for bank in range(4)), qiv(0))
            for axis in range(4)
        ]
        mixed = [
            [
                sum(
                    (
                        weights[bank] * qiv(COEFFICIENTS[bank][field][term])
                        for bank in range(4)
                    ),
                    qiv(0),
                )
                for term in range(14)
            ]
            for field in range(11)
        ]
        features = [iv_field_value(mixed[field], point) for field in range(10)]
        unit_gradient = iv_field_gradient(mixed[10], point)
    else:
        features = []
        for field in range(10):
            features.append(
                sum(
                    (
                        weights[bank]
                        * iv_field_value(
                            [qiv(item) for item in COEFFICIENTS[bank][field]],
                            bank_points[bank],
                        )
                        for bank in range(4)
                    ),
                    qiv(0),
                )
            )
        unit_gradient = [
            sum(
                (
                    weights[bank]
                    * iv_field_gradient(
                        [qiv(item) for item in COEFFICIENTS[bank][10]],
                        bank_points[bank],
                    )[axis]
                    for bank in range(4)
                ),
                qiv(0),
            )
            for axis in range(4)
        ]
    latent = [
        qiv(BASE_VALUES[field]) + qiv(amplitudes[field]) * features[field]
        for field in range(10)
    ]
    p = [qiv(amplitudes[10]) * item for item in unit_gradient]
    a, b, c, d, e, f, a20, a30, a21, a31 = latent
    expa, expc, expd, expf = iv.exp(a), iv.exp(c), iv.exp(d), iv.exp(f)
    h = [[-(expa * expa), -(expa * b)], [-(expa * b), expc * expc - b * b]]
    angular = [[expd * expd, expd * e], [expd * e, e * e + expf * expf]]
    shift = [[a20, a21], [a30, a31]]
    metric = [[qiv(0) for _ in range(4)] for _ in range(4)]
    for first in range(2):
        for second in range(2):
            value = h[first][second]
            for alpha in range(2):
                for beta in range(2):
                    value += (
                        angular[alpha][beta]
                        * shift[alpha][first]
                        * shift[beta][second]
                    )
            metric[first][second] = value
        for beta in range(2):
            value = qiv(0)
            for alpha in range(2):
                value += angular[alpha][beta] * shift[alpha][first]
            metric[first][2 + beta] = value
            metric[2 + beta][first] = value
    for alpha in range(2):
        for beta in range(2):
            metric[2 + alpha][2 + beta] = angular[alpha][beta]
    determinant = iv_det(metric)
    adjugate = [[qiv(0) for _ in range(4)] for _ in range(4)]
    for row in range(4):
        for column in range(4):
            minor = [
                [
                    metric[source_row][source_column]
                    for source_column in range(4)
                    if source_column != row
                ]
                for source_row in range(4)
                if source_row != column
            ]
            adjugate[row][column] = (
                -1 if (row + column) % 2 else 1
            ) * iv_det(minor)
    numerator = qiv(0)
    for row in range(4):
        for column in range(4):
            numerator += p[row] * adjugate[row][column] * p[column]
    return numerator / determinant, determinant


def anchor_selection(group_rows, amplitude_rows, coordinates, selected_values):
    payload = coordinates["L2"]
    u_nodes = [Fraction(item) for item in payload["u_nodes"]]
    t_nodes = [Fraction(item) for item in payload["t_nodes"]]
    triples = [tuple(item) for item in payload["barycentric_integer_triples"]]
    denominator = int(payload["barycentric_denominator"])
    shape = (len(u_nodes), len(triples), len(t_nodes))
    carrier_indices = [
        round(index * 47 / 15) for index in range(16)
    ]
    rows = []
    for chart_index, chart in enumerate(CHARTS):
        for selection_index, carrier_index in enumerate(carrier_indices):
            mask_offset = selection_index % 8
            group_index = carrier_index * 8 + mask_offset
            values = selected_values[(chart, group_index)].reshape(shape)
            anchor_kind = selection_index % 4
            if anchor_kind == 0:
                flat = int(np.argmin(values[:, :, 0]))
                u_index, q_index = np.unravel_index(flat, shape[:2])
                t_index = 0
                kind = "BASE_FACE_MINIMUM_NODE"
            elif anchor_kind == 1:
                absolute = np.abs(values)
                flat = int(np.argmin(absolute))
                u_index, q_index, t_index = np.unravel_index(flat, shape)
                kind = "NARROWEST_ABSOLUTE_NODE"
            else:
                rising = anchor_kind == 2 and chart.startswith("J1")
                candidates = []
                for u_index in range(shape[0]):
                    for q_index in range(shape[1]):
                        fiber = values[u_index, q_index]
                        for t_index in range(shape[2] - 1):
                            first, second = fiber[t_index], fiber[t_index + 1]
                            if (rising and first < 0.0 < second) or (
                                not rising and first > 0.0 > second
                            ):
                                candidates.append(
                                    (
                                        max(abs(first), abs(second)),
                                        u_index,
                                        q_index,
                                        t_index if abs(first) <= abs(second) else t_index + 1,
                                    )
                                )
                if not candidates:
                    flat = int(np.argmin(np.abs(values)))
                    u_index, q_index, t_index = np.unravel_index(flat, shape)
                    kind = "NO_RISING_BRANCH__NARROWEST_NODE"
                else:
                    _, u_index, q_index, t_index = min(candidates)
                    kind = (
                        "RISING_INTERFACE_BRACKET_NODE"
                        if rising else "FALLING_INTERFACE_BRACKET_NODE"
                    )
            q = tuple(Fraction(item, denominator) for item in triples[q_index])
            scalar, determinant = iv_point_full_matrix(
                chart,
                amplitude_rows[group_index],
                u_nodes[u_index],
                q,
                t_nodes[t_index],
            )
            scalar_lo, scalar_hi = iv_bounds(scalar)
            determinant_lo, determinant_hi = iv_bounds(determinant)
            saved_value = values[u_index, q_index, t_index]
            if scalar_lo > 0.0:
                interval_sign = 1
            elif scalar_hi < 0.0:
                interval_sign = -1
            else:
                interval_sign = 0
            rows.append(
                {
                    "anchor_id": f"A{len(rows)+1:02d}",
                    "chart": chart,
                    "group_id": group_rows[group_index]["group_id"],
                    "carrier_id": group_rows[group_index]["carrier_id"],
                    "mask_id": group_rows[group_index]["mask_id"],
                    "anchor_kind": kind,
                    "u": str(u_nodes[u_index]),
                    "q0": str(q[0]),
                    "q1": str(q[1]),
                    "q2": str(q[2]),
                    "t": str(t_nodes[t_index]),
                    "saved_float64_s": fmt(saved_value),
                    "mpmath80_full_matrix_s_interval": str(scalar),
                    "mpmath80_full_matrix_s_lo": fmt(scalar_lo),
                    "mpmath80_full_matrix_s_hi": fmt(scalar_hi),
                    "mpmath80_det_g_interval": str(determinant),
                    "mpmath80_det_g_lo": fmt(determinant_lo),
                    "mpmath80_det_g_hi": fmt(determinant_hi),
                    "interval_sign": interval_sign,
                    "float64_sign": 1 if saved_value > 0 else -1 if saved_value < 0 else 0,
                    "status": (
                        "HIGH_PRECISION_INTERVAL_SIGN_AND_DETERMINANT_AGREE"
                        if interval_sign != 0
                        and interval_sign
                        == (1 if saved_value > 0 else -1 if saved_value < 0 else 0)
                        and determinant_hi < 0.0
                        else "HIGH_PRECISION_UNRESOLVED_OR_MISMATCH"
                    ),
                }
            )
    for chart in CHARTS:
        best = None
        for group_index in range(len(group_rows)):
            values = selected_values[(chart, group_index)]
            flat_index = int(np.argmin(np.abs(values)))
            candidate = (
                float(abs(values[flat_index])),
                group_index,
                flat_index,
            )
            if best is None or candidate < best:
                best = candidate
        _absolute, group_index, flat_index = best
        u_index, q_index, t_index = np.unravel_index(flat_index, shape)
        q = tuple(Fraction(item, denominator) for item in triples[q_index])
        scalar, determinant = iv_point_full_matrix(
            chart,
            amplitude_rows[group_index],
            u_nodes[u_index],
            q,
            t_nodes[t_index],
        )
        scalar_lo, scalar_hi = iv_bounds(scalar)
        determinant_lo, determinant_hi = iv_bounds(determinant)
        saved_value = selected_values[(chart, group_index)].reshape(shape)[
            u_index, q_index, t_index
        ]
        interval_sign = 1 if scalar_lo > 0.0 else -1 if scalar_hi < 0.0 else 0
        float_sign = 1 if saved_value > 0.0 else -1 if saved_value < 0.0 else 0
        rows.append(
            {
                "anchor_id": f"A{len(rows)+1:02d}",
                "chart": chart,
                "group_id": group_rows[group_index]["group_id"],
                "carrier_id": group_rows[group_index]["carrier_id"],
                "mask_id": group_rows[group_index]["mask_id"],
                "anchor_kind": "GLOBAL_NARROWEST_L2_NODE",
                "u": str(u_nodes[u_index]),
                "q0": str(q[0]),
                "q1": str(q[1]),
                "q2": str(q[2]),
                "t": str(t_nodes[t_index]),
                "saved_float64_s": fmt(saved_value),
                "mpmath80_full_matrix_s_interval": str(scalar),
                "mpmath80_full_matrix_s_lo": fmt(scalar_lo),
                "mpmath80_full_matrix_s_hi": fmt(scalar_hi),
                "mpmath80_det_g_interval": str(determinant),
                "mpmath80_det_g_lo": fmt(determinant_lo),
                "mpmath80_det_g_hi": fmt(determinant_hi),
                "interval_sign": interval_sign,
                "float64_sign": float_sign,
                "status": (
                    "HIGH_PRECISION_INTERVAL_SIGN_AND_DETERMINANT_AGREE"
                    if interval_sign != 0
                    and interval_sign == float_sign
                    and determinant_hi < 0.0
                    else "HIGH_PRECISION_UNRESOLVED_OR_MISMATCH"
                ),
            }
        )
    return rows


class VerificationError(AssertionError):
    pass


def require(condition, label, catches):
    catches.append(
        {
            "catch_id": f"C{len(catches)+1:02d}",
            "check_type": "STATE_ASSERTION",
            "check": label,
            "status": "PASS" if condition else "FAIL",
        }
    )
    if not condition:
        raise AssertionError(label)


def census_gate(rows):
    if len(rows) != 1536 or len(
        {(row["level"], row["sheet_id"]) for row in rows}
    ) != 1536:
        raise VerificationError("census identity")
    if any(int(row["numerically_zero_nodes"]) != 0 for row in rows):
        raise VerificationError("zero node")
    if any(
        row["cross_resolution_status"] != "QUALITATIVE_CLASS_REPRODUCED"
        for row in rows
    ):
        raise VerificationError("resolution")
    l2 = [row for row in rows if row["level"] == "L2"]
    classes = Counter(row["primary_class"] for row in l2)
    if classes != {
        "ONE_OR_TWO_TRANSITION_FAMILIES__TWO_SAMPLED_NULL_COMPONENTS": 384,
        "ONE_TRANSITION_FAMILY__ONE_SAMPLED_NULL_COMPONENT": 384,
    }:
        raise VerificationError("chart class")


def coordinate_gate(payload):
    expected = {"L1": (45, 108), "L2": (153, 408)}
    for level, (nodes, edges) in expected.items():
        triples = payload[level]["barycentric_integer_triples"]
        adjacency = payload[level]["triangular_edges"]
        if (
            len(triples) != nodes
            or len({tuple(item) for item in triples}) != nodes
            or len(adjacency) != edges
            or len({tuple(item) for item in adjacency}) != edges
        ):
            raise VerificationError("simplex adjacency")


def raw_identity_gate(observed, expected):
    if observed.shape != expected.shape or not np.array_equal(observed, expected):
        raise VerificationError("raw identity")


def apex_gate(raw, payload):
    shape = (
        len(payload["u_nodes"]),
        len(payload["barycentric_integer_triples"]),
        len(payload["t_nodes"]),
    )
    apex = raw.reshape((384,) + shape)[:, :, :, -1]
    if not np.all(apex == -1) or not np.all(apex == apex[:, :, :1]):
        raise VerificationError("apex quotient duplicate")


def source_gate(source_hashes):
    for path, expected in EXPECTED_SOURCE_HASHES.items():
        if source_hashes.get(path) != expected or digest(ROOT / path) != expected:
            raise VerificationError("source hash")


def maximum_gate(value):
    if (
        value
        != "BOUNDED_REGISTERED_COMPLETE_BANK-SIMPLEX_LATTICE_ATLAS_WITH_INTERVAL_AND_MATRIX_CHECKS"
    ):
        raise VerificationError("maximum conclusion")


def expect_rejection(label, callback, catches):
    try:
        callback()
    except VerificationError:
        catches.append(
            {
                "catch_id": f"C{len(catches)+1:02d}",
                "check_type": "END_TO_END_MUTATION_CATCH",
                "check": label,
                "status": "PASS",
            }
        )
        return
    catches.append(
        {
            "catch_id": f"C{len(catches)+1:02d}",
            "check_type": "END_TO_END_MUTATION_CATCH",
            "check": label,
            "status": "FAIL",
        }
    )
    raise AssertionError(f"mutation accepted: {label}")


def main():
    iv.dps = 80
    group_rows, amplitude_rows = load_groups()
    coordinates = json.loads(COORDINATE_FILE.read_text(encoding="utf-8"))
    census = read_tsv(CENSUS_FILE)
    result = json.loads(RESULT_FILE.read_text(encoding="utf-8"))
    replay = independent_node_replay(
        group_rows, amplitude_rows, coordinates, census
    )
    boundary = boundary_edge_replay(coordinates)
    anchors = anchor_selection(
        group_rows, amplitude_rows, coordinates, replay["selected_values"]
    )
    catches = []
    census_gate(census)
    coordinate_gate(coordinates)
    source_gate(result["source_hashes"])
    maximum_gate(result["maximum_conclusion"])
    require(len(group_rows) == 384, "complete_group_universe", catches)
    require(len(census) == 1536, "two_levels_times_768_sheets", catches)
    require(replay["sign_mismatches"] == 0, "all_raw_node_signs_match", catches)
    require(replay["transition_mismatches"] == 0, "all_transition_counts_match", catches)
    require(replay["determinant_failures"] == 0, "all_block_determinants_negative", catches)
    require(
        boundary["boundary_failures"] == 0,
        "all_simplex_boundary_edge_controls",
        catches,
    )
    require(
        boundary["prior_adjacency_status"] == "REPRODUCED",
        "prior_adjacency_class_census",
        catches,
    )
    require(len(anchors) == 34, "thirty_four_high_precision_anchors", catches)
    require(
        len(
            [
                row
                for row in anchors
                if row["anchor_kind"] == "GLOBAL_NARROWEST_L2_NODE"
            ]
        )
        == 2,
        "both_global_narrowest_nodes_anchored",
        catches,
    )
    require(
        len({row["carrier_id"] for row in anchors}) >= 12,
        "anchor_carrier_span",
        catches,
    )
    require(
        {row["mask_id"] for row in anchors} == {f"M{value:X}" for value in range(8, 16)},
        "anchor_all_masks",
        catches,
    )
    require(
        {row["chart"] for row in anchors} == set(CHARTS),
        "anchor_both_charts",
        catches,
    )
    require(
        all(row["status"].endswith("AGREE") for row in anchors),
        "all_high_precision_full_matrix_anchors",
        catches,
    )
    require(
        all(int(row["numerically_zero_nodes"]) == 0 for row in census),
        "zero_numeric_zero_nodes",
        catches,
    )
    require(
        all(row["cross_resolution_status"] == "QUALITATIVE_CLASS_REPRODUCED" for row in census),
        "all_cross_resolution_classes_reproduced",
        catches,
    )
    require(
        result["physical_regime_labels_used"] == 0
        and result["actions_or_eom_loaded"] == 0
        and result["carrier_interpretations_loaded"] == 0,
        "no_physical_filters_loaded",
        catches,
    )
    require(
        result["maximum_conclusion"]
        == "BOUNDED_REGISTERED_COMPLETE_BANK-SIMPLEX_LATTICE_ATLAS_WITH_INTERVAL_AND_MATRIX_CHECKS",
        "bounded_maximum_conclusion",
        catches,
    )

    # Exercised end-to-end in-memory mutations through the actual state gates.
    expect_rejection(
        "missing_sheet_rejected",
        lambda: census_gate(census[:-1]),
        catches,
    )
    expect_rejection(
        "duplicate_sheet_rejected",
        lambda: census_gate(census + [census[0]]),
        catches,
    )
    conflated = [dict(row) for row in census]
    first_j2 = next(
        row for row in conflated if row["level"] == "L2" and row["chart"].startswith("J2")
    )
    first_j2["primary_class"] = (
        "ONE_OR_TWO_TRANSITION_FAMILIES__TWO_SAMPLED_NULL_COMPONENTS"
    )
    expect_rejection(
        "chart_conflation_rejected",
        lambda: census_gate(conflated),
        catches,
    )
    zero_mutation = [dict(row) for row in census]
    zero_mutation[0]["numerically_zero_nodes"] = "1"
    expect_rejection(
        "zero_node_promotion_rejected",
        lambda: census_gate(zero_mutation),
        catches,
    )
    resolution_mutation = [dict(row) for row in census]
    resolution_mutation[0][
        "cross_resolution_status"
    ] = "RESOLUTION_DEPENDENT_UNRESOLVED"
    expect_rejection(
        "resolution_disagreement_rejected",
        lambda: census_gate(resolution_mutation),
        catches,
    )
    coordinate_mutation = copy.deepcopy(coordinates)
    coordinate_mutation["L2"]["triangular_edges"].pop()
    expect_rejection(
        "incomplete_simplex_adjacency_rejected",
        lambda: coordinate_gate(coordinate_mutation),
        catches,
    )
    source_mutation = dict(result["source_hashes"])
    source_mutation[
        "udt_configuration_space_adjacency_atlas_2026-07-22/ENDPOINT_PAIR_REGISTRY.tsv"
    ] = "0" * 64
    expect_rejection(
        "source_hash_corruption_rejected",
        lambda: source_gate(source_mutation),
        catches,
    )
    expect_rejection(
        "continuous_promotion_rejected",
        lambda: maximum_gate("CONTINUOUS_NULL_HYPERSURFACE_PROVED"),
        catches,
    )
    raw = load_signs(HERE / "RAW_SIGNS_L1_J1.npy.gz")
    mutated_raw = raw.copy()
    mutated_raw[0, 0] *= -1
    expect_rejection(
        "raw_sign_mutation_rejected",
        lambda: raw_identity_gate(mutated_raw, raw),
        catches,
    )
    apex_mutation = raw.copy()
    l1_shape = (
        len(coordinates["L1"]["u_nodes"]),
        len(coordinates["L1"]["barycentric_integer_triples"]),
        len(coordinates["L1"]["t_nodes"]),
    )
    apex_mutation.reshape((384,) + l1_shape)[0, 0, 1, -1] = 1
    expect_rejection(
        "apex_duplicate_corruption_rejected",
        lambda: apex_gate(apex_mutation, coordinates["L1"]),
        catches,
    )

    write_tsv(
        HERE / "HIGH_PRECISION_FULL_MATRIX_ANCHORS.tsv",
        list(anchors[0]),
        anchors,
    )
    write_tsv(
        HERE / "INDEPENDENT_NODE_REPLAY.tsv",
        list(replay["rows"][0]),
        replay["rows"],
    )
    write_tsv(HERE / "CATCH_PROOFS.tsv", list(catches[0]), catches)
    output = {
        "schema": "udt-bank-simplex-independent-verification-1.0",
        "verdict": "PASS",
        "independent_method": (
            "COMPLETE_H_Q_SHIFT_BLOCK_RECONSTRUCTION_WITH_SCHUR_INVERSE_"
            "PLUS_MPMATH80_FULL_4X4_ADJUGATE_ANCHORS"
        ),
        "node_signs_checked": replay["total_nodes"],
        "node_sign_mismatches": replay["sign_mismatches"],
        "transition_count_mismatches": replay["transition_mismatches"],
        "nonnegative_metric_determinants": replay["determinant_failures"],
        "boundary_edge_replay": boundary,
        "high_precision_full_matrix_anchors": len(anchors),
        "high_precision_anchor_status_counts": dict(
            Counter(row["status"] for row in anchors)
        ),
        "assertion_checks": sum(
            row["check_type"] == "STATE_ASSERTION" for row in catches
        ),
        "mutation_catch_proofs": sum(
            row["check_type"] == "END_TO_END_MUTATION_CATCH" for row in catches
        ),
        "all_checks_passed": sum(row["status"] == "PASS" for row in catches),
        "environment": {
            "python": platform.python_version(),
            "numpy": np.__version__,
            "mpmath_iv_dps": 80,
            "platform": platform.platform(),
        },
        "input_hashes": {
            "RESULT.json": digest(RESULT_FILE),
            "LATTICE_SHEET_CENSUS.tsv": digest(CENSUS_FILE),
            "LATTICE_COORDINATES.json": digest(COORDINATE_FILE),
            "CARRIER_VECTOR_REGISTRY.tsv": digest(CARRIER_FILE),
        },
    }
    (HERE / "INDEPENDENT_VERIFICATION.json").write_text(
        json.dumps(output, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
