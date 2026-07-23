#!/usr/bin/env python3
"""Build the preregistered complete bank-simplex causal atlas."""

from __future__ import annotations

import csv
import gzip
import hashlib
import importlib.util
import itertools
import json
import math
import platform
import sys
from collections import Counter, deque
from fractions import Fraction
from pathlib import Path

import numpy as np


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
SOURCE_PATH = (
    ROOT
    / "udt_configuration_space_adjacency_atlas_2026-07-22"
    / "build_configuration_adjacency_atlas.py"
)
CARRIER_FILE = (
    ROOT
    / "udt_structural_ensemble_metric_atlas_2026-07-21"
    / "CARRIER_VECTOR_REGISTRY.tsv"
)
IDENTITY_FILE = (
    ROOT
    / "udt_motif_hopf_correspondence_audit_2026-07-22"
    / "COHERENT_IDENTITY_REGISTRY.tsv"
)
CAUSAL_FILE = (
    ROOT
    / "udt_phi_causal_interface_atlas_2026-07-22"
    / "IDENTITY_CAUSAL_CERTIFICATES.tsv"
)
ADJACENCY_RESULT = (
    ROOT / "udt_configuration_space_adjacency_atlas_2026-07-22" / "RESULT.json"
)
ENDPOINT_PAIR_FILE = (
    ROOT
    / "udt_configuration_space_adjacency_atlas_2026-07-22"
    / "ENDPOINT_PAIR_REGISTRY.tsv"
)
PRIOR_SHEET_FILE = (
    ROOT
    / "udt_configuration_space_adjacency_atlas_2026-07-22"
    / "SHEET_CLASSIFICATION.tsv"
)

BASE = "6597f3a50584d17b2a5248348e9a6ca471e1d179"
CHARTS = ("J1_GENERATOR_COEFFICIENT_BARYCENTRIC", "J2_EVALUATED_COFIELD_BARYCENTRIC")
GRID = {"u": 8, "r": 8, "v": 8, "t": 16}
MAX_ADAPTIVE_DEPTH = 18
BATCH = 64
POINT_GRID = (0.0, 0.25, 0.5, 0.75, 1.0)


def load_source():
    spec = importlib.util.spec_from_file_location("adjacency_source", SOURCE_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load frozen adjacency source")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


SRC = load_source()
FLOAT_COEFFICIENTS = np.asarray(SRC.COEFFICIENTS, dtype=np.float64)
FLOAT_BASE_VALUES = np.asarray(SRC.BASE_VALUES, dtype=np.float64)


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


def write_tsv_gz(path, fieldnames, rows):
    with gzip.GzipFile(filename=str(path), mode="wb", mtime=0) as compressed:
        import io

        with io.TextIOWrapper(compressed, encoding="utf-8", newline="") as handle:
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


def mix(items, weights):
    output = SRC.VDual.constant(SRC.VInterval.point(0.0))
    for weight, item in zip(weights, items):
        output += weight * item
    return output


def simplex_weights(r_bounds, v_bounds, t_bounds):
    r = SRC.VDual.constant(SRC.VInterval.bounds(*r_bounds))
    v = SRC.VDual.constant(SRC.VInterval.bounds(*v_bounds))
    t = SRC.VDual(SRC.VInterval.bounds(*t_bounds), SRC.VInterval.point(1.0))
    one = SRC.VDual.constant(SRC.VInterval.point(1.0))
    q0 = one - r
    q1 = r * (one - v)
    q2 = r * v
    return ((one - t) * q0, (one - t) * q1, (one - t) * q2, t)


def configured_fields(chart, amplitude_intervals, u_bounds, r_bounds, v_bounds, t_bounds):
    parameter_u = SRC.VInterval.bounds(*u_bounds)
    weights = simplex_weights(r_bounds, v_bounds, t_bounds)
    if chart.startswith("J2"):
        endpoints = [
            SRC.v_endpoint(bank, amplitude_intervals, parameter_u) for bank in range(4)
        ]
        latent = tuple(
            mix([endpoints[bank][0][field] for bank in range(4)], weights)
            for field in range(10)
        )
        gradient = tuple(
            mix([endpoints[bank][1][axis] for bank in range(4)], weights)
            for axis in range(4)
        )
        return latent, gradient

    coordinates_by_bank = [
        SRC.v_bank_coordinate(bank, parameter_u) for bank in range(4)
    ]
    coordinates = tuple(
        mix(
            [
                SRC.VDual.constant(coordinates_by_bank[bank][axis])
                for bank in range(4)
            ],
            weights,
        )
        for axis in range(4)
    )
    latent = []
    for field in range(10):
        coefficients = tuple(
            mix(
                [
                    SRC.VDual.constant(
                        SRC.v_fraction(SRC.COEFFICIENTS[bank][field][term])
                    )
                    for bank in range(4)
                ],
                weights,
            )
            for term in range(14)
        )
        latent.append(
            SRC.VDual.constant(SRC.v_fraction(SRC.BASE_VALUES[field]))
            + SRC.v_field_value(coefficients, coordinates)
            * amplitude_intervals[field]
        )
    phi_coefficients = tuple(
        mix(
            [
                SRC.VDual.constant(
                    SRC.v_fraction(SRC.COEFFICIENTS[bank][10][term])
                )
                for bank in range(4)
            ],
            weights,
        )
        for term in range(14)
    )
    gradient = tuple(
        item * amplitude_intervals[10]
        for item in SRC.v_field_gradient(phi_coefficients, coordinates)
    )
    return tuple(latent), gradient


def scalar_interval(chart, amplitude_intervals, u_bounds, r_bounds, v_bounds, t_bounds):
    latent, gradient = configured_fields(
        chart, amplitude_intervals, u_bounds, r_bounds, v_bounds, t_bounds
    )
    a, b, c, d, e, f, a20, a30, a21, a31 = latent
    scale_u = SRC.vdual_exp(a)
    scale_w = SRC.vdual_exp(c)
    scale_r = SRC.vdual_exp(d)
    scale_t = SRC.vdual_exp(f)
    first = gradient[0] - a20 * gradient[2] - a30 * gradient[3]
    second = gradient[1] - a21 * gradient[2] - a31 * gradient[3]
    scalar = (
        -((first / scale_u) * (first / scale_u))
        + ((second - b * first / scale_u) / scale_w)
        * ((second - b * first / scale_u) / scale_w)
        + (gradient[2] / scale_r) * (gradient[2] / scale_r)
        + ((gradient[3] - e * gradient[2] / scale_r) / scale_t)
        * ((gradient[3] - e * gradient[2] / scale_r) / scale_t)
    )
    return scalar, gradient


def float_bank_coordinates(bank, u):
    start_name, end_name = SRC.POINT_PAIRS[bank]
    start = np.asarray(SRC.POINTS[start_name], dtype=np.float64)
    end = np.asarray(SRC.POINTS[end_name], dtype=np.float64)
    return start[None, :] + u[:, None] * (end - start)[None, :]


def float_field_values(coefficients, coordinates):
    values = np.sum(coefficients[..., :4] * coordinates[..., None, :], axis=-1)
    values += np.sum(
        coefficients[..., 4:8] * coordinates[..., None, :] ** 2 / 2.0,
        axis=-1,
    )
    for pair_index, (first, second) in enumerate(SRC.PAIRS):
        values += (
            coefficients[..., 8 + pair_index]
            * coordinates[..., None, first]
            * coordinates[..., None, second]
        )
    return values


def float_field_gradient(coefficients, coordinates):
    output = np.empty(coordinates.shape[:-1] + (4,), dtype=np.float64)
    for axis in range(4):
        value = coefficients[..., axis] + coefficients[..., 4 + axis] * coordinates[..., axis]
        for pair_index, (first, second) in enumerate(SRC.PAIRS):
            if axis == first:
                value = value + coefficients[..., 8 + pair_index] * coordinates[..., second]
            elif axis == second:
                value = value + coefficients[..., 8 + pair_index] * coordinates[..., first]
        output[..., axis] = value
    return output


def float_scalar_simplex(chart, amplitudes, u, r, v, t):
    u = np.asarray(u, dtype=np.float64).reshape(-1)
    r = np.asarray(r, dtype=np.float64).reshape(-1)
    v = np.asarray(v, dtype=np.float64).reshape(-1)
    t = np.asarray(t, dtype=np.float64).reshape(-1)
    q = np.stack((1.0 - r, r * (1.0 - v), r * v), axis=1)
    weights = np.column_stack(((1.0 - t)[:, None] * q, t))
    bank_coordinates = np.stack(
        [float_bank_coordinates(bank, u) for bank in range(4)], axis=1
    )
    if chart.startswith("J1"):
        coordinates = np.einsum("pb,pbd->pd", weights, bank_coordinates)
        coefficients = np.einsum("pb,bft->pft", weights, FLOAT_COEFFICIENTS)
        values = float_field_values(coefficients, coordinates)
        latent = FLOAT_BASE_VALUES[None, :] + values[:, :10] * np.asarray(
            amplitudes[:10], dtype=np.float64
        )[None, :]
        gradient = float_field_gradient(coefficients[:, 10, :], coordinates)
        gradient *= float(amplitudes[10])
    else:
        endpoint_latent = []
        endpoint_gradient = []
        for bank in range(4):
            values = float_field_values(
                FLOAT_COEFFICIENTS[bank][None, :, :],
                bank_coordinates[:, bank, :],
            )
            endpoint_latent.append(
                FLOAT_BASE_VALUES[None, :]
                + values[:, :10]
                * np.asarray(amplitudes[:10], dtype=np.float64)[None, :]
            )
            gradient = float_field_gradient(
                FLOAT_COEFFICIENTS[bank, 10, :][None, :],
                bank_coordinates[:, bank, :],
            )
            endpoint_gradient.append(gradient * float(amplitudes[10]))
        latent = np.einsum("pb,bpf->pf", weights, np.asarray(endpoint_latent))
        gradient = np.einsum("pb,bpd->pd", weights, np.asarray(endpoint_gradient))
    a, b, c, d, e, f, a20, a30, a21, a31 = latent.T
    first = gradient[:, 0] - a20 * gradient[:, 2] - a30 * gradient[:, 3]
    second = gradient[:, 1] - a21 * gradient[:, 2] - a31 * gradient[:, 3]
    return (
        -(first / np.exp(a)) ** 2
        + ((second - b * first / np.exp(a)) / np.exp(c)) ** 2
        + (gradient[:, 2] / np.exp(d)) ** 2
        + ((gradient[:, 3] - e * gradient[:, 2] / np.exp(d)) / np.exp(f)) ** 2
    )


def float_basis_simplex(chart, u, r, v, t):
    """Return the ten unit-amplitude latent features and unit-beta dphi."""
    u = np.asarray(u, dtype=np.float64).reshape(-1)
    r = np.asarray(r, dtype=np.float64).reshape(-1)
    v = np.asarray(v, dtype=np.float64).reshape(-1)
    t = np.asarray(t, dtype=np.float64).reshape(-1)
    q = np.stack((1.0 - r, r * (1.0 - v), r * v), axis=1)
    weights = np.column_stack(((1.0 - t)[:, None] * q, t))
    bank_coordinates = np.stack(
        [float_bank_coordinates(bank, u) for bank in range(4)], axis=1
    )
    if chart.startswith("J1"):
        coordinates = np.einsum("pb,pbd->pd", weights, bank_coordinates)
        coefficients = np.einsum("pb,bft->pft", weights, FLOAT_COEFFICIENTS)
        values = float_field_values(coefficients, coordinates)
        gradient = float_field_gradient(coefficients[:, 10, :], coordinates)
        return values[:, :10], gradient

    endpoint_features = []
    endpoint_gradient = []
    for bank in range(4):
        values = float_field_values(
            FLOAT_COEFFICIENTS[bank][None, :, :],
            bank_coordinates[:, bank, :],
        )
        endpoint_features.append(values[:, :10])
        endpoint_gradient.append(
            float_field_gradient(
                FLOAT_COEFFICIENTS[bank, 10, :][None, :],
                bank_coordinates[:, bank, :],
            )
        )
    return (
        np.einsum("pb,bpf->pf", weights, np.asarray(endpoint_features)),
        np.einsum("pb,bpd->pd", weights, np.asarray(endpoint_gradient)),
    )


def float_scalars_from_basis(amplitudes, features, unit_gradient):
    amplitudes = np.asarray(amplitudes, dtype=np.float64)
    latent = [
        FLOAT_BASE_VALUES[field]
        + amplitudes[:, field, None] * features[None, :, field]
        for field in range(10)
    ]
    beta = amplitudes[:, 10, None]
    gradient = [beta * unit_gradient[None, :, axis] for axis in range(4)]
    a, b, c, d, e, f, a20, a30, a21, a31 = latent
    first = gradient[0] - a20 * gradient[2] - a30 * gradient[3]
    second = gradient[1] - a21 * gradient[2] - a31 * gradient[3]
    return (
        -(first / np.exp(a)) ** 2
        + ((second - b * first / np.exp(a)) / np.exp(c)) ** 2
        + (gradient[2] / np.exp(d)) ** 2
        + ((gradient[3] - e * gradient[2] / np.exp(d)) / np.exp(f)) ** 2
    )


def groups():
    carriers = {
        row["carrier_id"]: tuple(Fraction(row[name]) for name in SRC.PARAMETERS)
        for row in read_tsv(CARRIER_FILE)
    }
    if len(carriers) != 48:
        raise AssertionError("carrier universe must contain 48 vectors")
    identities = read_tsv(IDENTITY_FILE)
    active = [row for row in identities if int(row["mask_id"][1:], 16) & 8]
    if len(active) != 1536:
        raise AssertionError("active identity universe must contain 1536 rows")
    lookup = {
        (int(row["bank"][1:]), row["carrier_id"], int(row["mask_id"][1:], 16)):
        row["identity_id"]
        for row in active
    }
    causal = {
        row["identity_id"]: row["causal_status"] for row in read_tsv(CAUSAL_FILE)
    }
    rows = []
    amplitudes = []
    for carrier_id in sorted(carriers):
        for mask in range(8, 16):
            identities_for_group = [
                lookup[(bank, carrier_id, mask)] for bank in range(4)
            ]
            statuses = [causal[item] for item in identities_for_group]
            if (
                statuses[:3] != ["UNIFORMLY_SPACELIKE"] * 3
                or statuses[3] != "UNIFORMLY_TIMELIKE"
            ):
                raise AssertionError("frozen causal bank orientation changed")
            rows.append(
                {
                    "group_index": len(rows),
                    "group_id": f"{carrier_id}_M{mask:X}",
                    "carrier_id": carrier_id,
                    "mask_id": f"M{mask:X}",
                    "identity_b0": identities_for_group[0],
                    "identity_b1": identities_for_group[1],
                    "identity_b2": identities_for_group[2],
                    "identity_b3": identities_for_group[3],
                }
            )
            amplitudes.append(SRC.amplitude_vector(carriers[carrier_id], mask))
    if len(rows) != 384:
        raise AssertionError("group universe must contain 384 rows")
    return rows, amplitudes


def domain_batch(flat_indices):
    indices = np.asarray(flat_indices, dtype=np.int64)
    nt = GRID["t"]
    nv = GRID["v"]
    nr = GRID["r"]
    t_index = indices % nt
    indices //= nt
    v_index = indices % nv
    indices //= nv
    r_index = indices % nr
    u_index = indices // nr
    return {
        "u": (
            (u_index / GRID["u"]).reshape(1, -1),
            ((u_index + 1) / GRID["u"]).reshape(1, -1),
        ),
        "r": (
            (r_index / GRID["r"]).reshape(1, -1),
            ((r_index + 1) / GRID["r"]).reshape(1, -1),
        ),
        "v": (
            (v_index / GRID["v"]).reshape(1, -1),
            ((v_index + 1) / GRID["v"]).reshape(1, -1),
        ),
        "t": (
            (t_index / GRID["t"]).reshape(1, -1),
            ((t_index + 1) / GRID["t"]).reshape(1, -1),
        ),
        "indices": (u_index, r_index, v_index, t_index),
    }


def face_batch(flat_indices):
    indices = np.asarray(flat_indices, dtype=np.int64)
    nv = GRID["v"]
    nr = GRID["r"]
    v_index = indices % nv
    indices //= nv
    r_index = indices % nr
    u_index = indices // nr
    zero = np.zeros((1, len(flat_indices)))
    return {
        "u": (
            (u_index / GRID["u"]).reshape(1, -1),
            ((u_index + 1) / GRID["u"]).reshape(1, -1),
        ),
        "r": (
            (r_index / GRID["r"]).reshape(1, -1),
            ((r_index + 1) / GRID["r"]).reshape(1, -1),
        ),
        "v": (
            (v_index / GRID["v"]).reshape(1, -1),
            ((v_index + 1) / GRID["v"]).reshape(1, -1),
        ),
        "t": (zero, zero),
        "indices": (u_index, r_index, v_index),
    }


def vertex_batch(flat_indices):
    indices = np.asarray(flat_indices, dtype=np.int64)
    zero = np.zeros((1, len(indices)))
    one = np.ones((1, len(indices)))
    return {
        "u": (
            (indices / GRID["u"]).reshape(1, -1),
            ((indices + 1) / GRID["u"]).reshape(1, -1),
        ),
        "r": (zero, zero),
        "v": (zero, zero),
        "t": (one, one),
        "indices": (indices,),
    }


def initial_certificate(chart, amplitude_intervals):
    size = len(np.atleast_1d(amplitude_intervals[0].lo))
    result = {
        "derivative_lo": np.full(size, np.inf),
        "derivative_hi": np.full(size, -np.inf),
        "derivative_pass": np.ones(size, dtype=bool),
        "derivative_fail_cells": [[] for _ in range(size)],
        "derivative_worst_cell": np.zeros(size, dtype=np.int64),
        "face_s_lo": np.full(size, np.inf),
        "face_s_hi": np.full(size, -np.inf),
        "face_pass": np.ones(size, dtype=bool),
        "face_negative_observed": np.zeros(size, dtype=bool),
        "face_fail_cells": [[] for _ in range(size)],
        "face_worst_cell": np.zeros(size, dtype=np.int64),
        "vertex_s_lo": np.full(size, np.inf),
        "vertex_s_hi": np.full(size, -np.inf),
        "vertex_pass": np.ones(size, dtype=bool),
        "vertex_fail_cells": [[] for _ in range(size)],
        "vertex_worst_cell": np.zeros(size, dtype=np.int64),
        "stream_hash": hashlib.sha256(),
    }
    columns = SRC.column_amplitude_intervals(amplitude_intervals)
    total = GRID["u"] * GRID["r"] * GRID["v"] * GRID["t"]
    for start in range(0, total, BATCH):
        flat = list(range(start, min(total, start + BATCH)))
        box = domain_batch(flat)
        scalar, _gradient = scalar_interval(
            chart, columns, box["u"], box["r"], box["v"], box["t"]
        )
        lo = scalar.derivative.lo
        hi = scalar.derivative.hi
        local_argmax = np.argmax(hi, axis=1)
        local_max = hi[np.arange(size), local_argmax]
        replace = local_max > result["derivative_hi"]
        result["derivative_worst_cell"] = np.where(
            replace, start + local_argmax, result["derivative_worst_cell"]
        )
        result["derivative_lo"] = np.minimum(result["derivative_lo"], np.min(lo, axis=1))
        result["derivative_hi"] = np.maximum(result["derivative_hi"], local_max)
        failed = hi >= 0.0
        result["derivative_pass"] &= ~np.any(failed, axis=1)
        for group_index in np.flatnonzero(np.any(failed, axis=1)):
            result["derivative_fail_cells"][group_index].extend(
                start + int(index) for index in np.flatnonzero(failed[group_index])
            )
        result["stream_hash"].update(np.asarray(lo, dtype="<f8").tobytes())
        result["stream_hash"].update(np.asarray(hi, dtype="<f8").tobytes())

    face_total = GRID["u"] * GRID["r"] * GRID["v"]
    for start in range(0, face_total, BATCH):
        flat = list(range(start, min(face_total, start + BATCH)))
        box = face_batch(flat)
        scalar, _gradient = scalar_interval(
            chart, columns, box["u"], box["r"], box["v"], box["t"]
        )
        lo = scalar.value.lo
        hi = scalar.value.hi
        local_argmin = np.argmin(lo, axis=1)
        local_min = lo[np.arange(size), local_argmin]
        replace = local_min < result["face_s_lo"]
        result["face_worst_cell"] = np.where(
            replace, start + local_argmin, result["face_worst_cell"]
        )
        result["face_s_lo"] = np.minimum(result["face_s_lo"], local_min)
        result["face_s_hi"] = np.maximum(result["face_s_hi"], np.max(hi, axis=1))
        failed = lo <= 0.0
        result["face_pass"] &= ~np.any(failed, axis=1)
        result["face_negative_observed"] |= np.any(hi < 0.0, axis=1)
        for group_index in np.flatnonzero(np.any(failed, axis=1)):
            result["face_fail_cells"][group_index].extend(
                start + int(index) for index in np.flatnonzero(failed[group_index])
            )
        result["stream_hash"].update(np.asarray(lo, dtype="<f8").tobytes())
        result["stream_hash"].update(np.asarray(hi, dtype="<f8").tobytes())

    for start in range(0, GRID["u"], BATCH):
        flat = list(range(start, min(GRID["u"], start + BATCH)))
        box = vertex_batch(flat)
        scalar, _gradient = scalar_interval(
            chart, columns, box["u"], box["r"], box["v"], box["t"]
        )
        lo = scalar.value.lo
        hi = scalar.value.hi
        local_argmax = np.argmax(hi, axis=1)
        local_max = hi[np.arange(size), local_argmax]
        replace = local_max > result["vertex_s_hi"]
        result["vertex_worst_cell"] = np.where(
            replace, start + local_argmax, result["vertex_worst_cell"]
        )
        result["vertex_s_lo"] = np.minimum(result["vertex_s_lo"], np.min(lo, axis=1))
        result["vertex_s_hi"] = np.maximum(result["vertex_s_hi"], local_max)
        failed = hi >= 0.0
        result["vertex_pass"] &= ~np.any(failed, axis=1)
        for group_index in np.flatnonzero(np.any(failed, axis=1)):
            result["vertex_fail_cells"][group_index].extend(
                start + int(index) for index in np.flatnonzero(failed[group_index])
            )
        result["stream_hash"].update(np.asarray(lo, dtype="<f8").tobytes())
        result["stream_hash"].update(np.asarray(hi, dtype="<f8").tobytes())
    return result


def point_root_ranges(chart, amplitude_rows):
    points = list(itertools.product(POINT_GRID, repeat=3))
    u = np.asarray([item[0] for item in points], dtype=np.float64).reshape(1, -1)
    r = np.asarray([item[1] for item in points], dtype=np.float64).reshape(1, -1)
    v = np.asarray([item[2] for item in points], dtype=np.float64).reshape(1, -1)
    columns = SRC.column_amplitude_intervals(
        SRC.vector_amplitude_intervals(amplitude_rows)
    )
    lo = np.zeros((len(amplitude_rows), len(points)), dtype=np.float64)
    hi = np.ones_like(lo)
    for endpoint, expected_positive in ((lo, True), (hi, False)):
        scalar, _gradient = scalar_interval(
            chart, columns, (u, u), (r, r), (v, v), (endpoint, endpoint)
        )
        values = (scalar.value.lo + scalar.value.hi) / 2.0
        if expected_positive and not np.all(values > 0.0):
            raise AssertionError("point control positive endpoint signs")
        if not expected_positive and not np.all(values < 0.0):
            raise AssertionError("point control negative endpoint signs")
    for _ in range(52):
        midpoint = (lo + hi) / 2.0
        scalar, _gradient = scalar_interval(
            chart, columns, (u, u), (r, r), (v, v), (midpoint, midpoint)
        )
        values = (scalar.value.lo + scalar.value.hi) / 2.0
        positive = values > 0.0
        lo = np.where(positive, midpoint, lo)
        hi = np.where(positive, hi, midpoint)
    root = (lo + hi) / 2.0
    return np.min(root, axis=1), np.max(root, axis=1), len(points)


def cell_bounds(flat_index):
    box = domain_batch([flat_index])
    return {
        key: (float(value[0][0, 0]), float(value[1][0, 0]))
        for key, value in box.items()
        if key != "indices"
    }


def face_cell_bounds(flat_index):
    box = face_batch([flat_index])
    return {
        key: (float(value[0][0, 0]), float(value[1][0, 0]))
        for key, value in box.items()
        if key != "indices"
    }


def vertex_cell_bounds(flat_index):
    box = vertex_batch([flat_index])
    return {
        key: (float(value[0][0, 0]), float(value[1][0, 0]))
        for key, value in box.items()
        if key != "indices"
    }


def split_box(bounds, active_axes):
    widths = {axis: bounds[axis][1] - bounds[axis][0] for axis in active_axes}
    maximum = max(widths.values())
    axis = next(
        candidate
        for candidate in ("t", "u", "r", "v")
        if candidate in widths and widths[candidate] == maximum
    )
    midpoint = sum(bounds[axis]) / 2.0
    first = dict(bounds)
    second = dict(bounds)
    first[axis] = (bounds[axis][0], midpoint)
    second[axis] = (midpoint, bounds[axis][1])
    return first, second


def adaptive_certify(chart, amplitudes, cells, kind):
    amplitude_intervals = tuple(
        SRC.VInterval.enclosing_fraction(item) for item in amplitudes
    )
    queue = deque((bounds, 0) for bounds in cells)
    certified = 0
    unresolved = []
    strict_opposite = 0
    worst_lower = math.inf
    worst_upper = -math.inf
    while queue:
        bounds, depth = queue.popleft()
        scalar, _gradient = scalar_interval(
            chart,
            amplitude_intervals,
            bounds["u"],
            bounds["r"],
            bounds["v"],
            bounds["t"],
        )
        if kind == "DERIVATIVE":
            lo = float(np.asarray(scalar.derivative.lo))
            hi = float(np.asarray(scalar.derivative.hi))
            passes = hi < 0.0
            opposite = lo > 0.0
            axes = ("u", "r", "v", "t")
        elif kind == "FACE":
            lo = float(np.asarray(scalar.value.lo))
            hi = float(np.asarray(scalar.value.hi))
            passes = lo > 0.0
            opposite = hi < 0.0
            axes = ("u", "r", "v")
        else:
            lo = float(np.asarray(scalar.value.lo))
            hi = float(np.asarray(scalar.value.hi))
            passes = hi < 0.0
            opposite = lo > 0.0
            axes = ("u",)
        worst_lower = min(worst_lower, lo)
        worst_upper = max(worst_upper, hi)
        if passes:
            certified += 1
        elif depth >= MAX_ADAPTIVE_DEPTH:
            unresolved.append((bounds, depth, lo, hi))
            strict_opposite += int(opposite)
        else:
            first, second = split_box(bounds, axes)
            queue.append((first, depth + 1))
            queue.append((second, depth + 1))
    return {
        "certified": certified,
        "unresolved": unresolved,
        "opposite_at_limit": strict_opposite,
        "worst_lower": worst_lower,
        "worst_upper": worst_upper,
    }


LEVELS = {
    "L1": {"nu": 9, "nq": 8, "nt": 65},
    "L2": {"nu": 17, "nq": 16, "nt": 129},
}
POINT_BATCH = 4096
GROUP_BATCH = 8
ZERO_MULTIPLIER = 64.0


def barycentric_triples(denominator):
    return [
        (first, second, denominator - first - second)
        for first in range(denominator + 1)
        for second in range(denominator - first + 1)
    ]


def triangular_edges(triples):
    lookup = {triple: index for index, triple in enumerate(triples)}
    edges = []
    for index, triple in enumerate(triples):
        for first in range(3):
            for second in range(first + 1, 3):
                for sign in (-1, 1):
                    candidate = list(triple)
                    candidate[first] += sign
                    candidate[second] -= sign
                    candidate = tuple(candidate)
                    if candidate in lookup and index < lookup[candidate]:
                        edges.append((index, lookup[candidate]))
    return sorted(set(edges))


def connected_components(mask, q_edges):
    mask = np.asarray(mask, dtype=bool)
    nu, nq = mask.shape
    seen = np.zeros_like(mask)
    components = 0
    for u_index, q_index in zip(*np.nonzero(mask & ~seen)):
        if seen[u_index, q_index]:
            continue
        components += 1
        queue = deque([(u_index, q_index)])
        seen[u_index, q_index] = True
        while queue:
            current_u, current_q = queue.popleft()
            for next_u in (current_u - 1, current_u + 1):
                if (
                    0 <= next_u < nu
                    and mask[next_u, current_q]
                    and not seen[next_u, current_q]
                ):
                    seen[next_u, current_q] = True
                    queue.append((next_u, current_q))
            for first, second in q_edges:
                if first == current_q:
                    next_q = second
                elif second == current_q:
                    next_q = first
                else:
                    continue
                if mask[current_u, next_q] and not seen[current_u, next_q]:
                    seen[current_u, next_q] = True
                    queue.append((current_u, next_q))
    return components


def lattice_coordinates(specification):
    triples = barycentric_triples(specification["nq"])
    u_nodes = np.linspace(0.0, 1.0, specification["nu"])
    t_nodes = np.linspace(0.0, 1.0, specification["nt"])
    u, q_index, t = np.meshgrid(
        u_nodes,
        np.arange(len(triples), dtype=np.int64),
        t_nodes,
        indexing="ij",
    )
    triple_array = np.asarray(triples, dtype=np.float64) / specification["nq"]
    q1 = triple_array[q_index.reshape(-1), 1]
    q2 = triple_array[q_index.reshape(-1), 2]
    r = q1 + q2
    v = np.divide(q2, r, out=np.zeros_like(q2), where=r != 0.0)
    return {
        "triples": triples,
        "q_edges": triangular_edges(triples),
        "u_nodes": u_nodes,
        "t_nodes": t_nodes,
        "u": u.reshape(-1),
        "r": r,
        "v": v,
        "t": t.reshape(-1),
        "shape": (len(u_nodes), len(triples), len(t_nodes)),
    }


def deterministic_npy_gz(path, array):
    with gzip.GzipFile(filename=str(path), mode="wb", mtime=0) as handle:
        np.save(handle, np.asarray(array), allow_pickle=False)


def sheet_lattice_summary(values, signs, coordinates):
    shape = coordinates["shape"]
    values = values.reshape(shape)
    signs = signs.reshape(shape)
    zero_count = int(np.sum(signs == 0))
    transitions = np.sum(signs[:, :, 1:] != signs[:, :, :-1], axis=2)
    base = signs[:, :, 0]
    apex = signs[:, :, -1]
    base_positive_components = connected_components(
        base > 0, coordinates["q_edges"]
    )
    base_negative_components = connected_components(
        base < 0, coordinates["q_edges"]
    )
    transition_counts = Counter(map(int, transitions.reshape(-1)))
    transition_roots = []
    rising_roots = []
    falling_roots = []
    t_nodes = coordinates["t_nodes"]
    for flat_fiber in range(transitions.size):
        current = values.reshape(-1, shape[-1])[flat_fiber]
        changed = np.flatnonzero(
            signs.reshape(-1, shape[-1])[flat_fiber, 1:]
            != signs.reshape(-1, shape[-1])[flat_fiber, :-1]
        )
        for position in changed:
            first, second = current[position], current[position + 1]
            root = t_nodes[position] - first * (
                t_nodes[position + 1] - t_nodes[position]
            ) / (second - first)
            transition_roots.append(root)
            if first < 0.0 < second:
                rising_roots.append(root)
            elif first > 0.0 > second:
                falling_roots.append(root)
    all_one = set(transition_counts) == {1}
    one_or_two = set(transition_counts).issubset({1, 2}) and 2 in transition_counts
    base_all_positive = np.all(base > 0)
    apex_all_negative = np.all(apex < 0)
    if (
        zero_count == 0
        and all_one
        and base_all_positive
        and apex_all_negative
        and base_positive_components == 1
        and base_negative_components == 0
    ):
        primary = "ONE_TRANSITION_FAMILY__ONE_SAMPLED_NULL_COMPONENT"
        null_components = positive_components = negative_components = 1
    elif (
        zero_count == 0
        and one_or_two
        and apex_all_negative
        and base_positive_components == 1
        and base_negative_components == 1
        and transition_counts[2] == int(np.sum(base < 0))
    ):
        primary = "ONE_OR_TWO_TRANSITION_FAMILIES__TWO_SAMPLED_NULL_COMPONENTS"
        null_components = 2
        positive_components = 1
        negative_components = 2
    elif zero_count:
        primary = "RESOLUTION_DEPENDENT_UNRESOLVED"
        null_components = positive_components = negative_components = "UNRESOLVED"
    else:
        primary = "MORE_COMPLEX_SAMPLED_TRANSITION_OR_COMPONENT_STRUCTURE"
        null_components = positive_components = negative_components = "UNRESOLVED"

    def range_or_blank(collection, which):
        if not collection:
            return ""
        return fmt(min(collection) if which == "min" else max(collection))

    absolute = np.abs(values)
    return {
        "primary_class": primary,
        "positive_nodes": int(np.sum(signs > 0)),
        "negative_nodes": int(np.sum(signs < 0)),
        "numerically_zero_nodes": zero_count,
        "minimum_s": fmt(np.min(values)),
        "maximum_s": fmt(np.max(values)),
        "minimum_abs_node_s": fmt(np.min(absolute)),
        "transition_count_0_fibers": transition_counts[0],
        "transition_count_1_fibers": transition_counts[1],
        "transition_count_2_fibers": transition_counts[2],
        "transition_count_3plus_fibers": sum(
            count for key, count in transition_counts.items() if key >= 3
        ),
        "base_positive_nodes": int(np.sum(base > 0)),
        "base_negative_nodes": int(np.sum(base < 0)),
        "base_positive_components": base_positive_components,
        "base_negative_components": base_negative_components,
        "apex_all_negative": bool(apex_all_negative),
        "sampled_null_components": null_components,
        "sampled_positive_components": positive_components,
        "sampled_negative_components": negative_components,
        "all_root_min": range_or_blank(transition_roots, "min"),
        "all_root_max": range_or_blank(transition_roots, "max"),
        "rising_root_min": range_or_blank(rising_roots, "min"),
        "rising_root_max": range_or_blank(rising_roots, "max"),
        "falling_root_min": range_or_blank(falling_roots, "min"),
        "falling_root_max": range_or_blank(falling_roots, "max"),
    }


def build_lattice_level(level, chart, group_rows, amplitude_rows, replay):
    specification = LEVELS[level]
    coordinates = lattice_coordinates(specification)
    nodes = len(coordinates["u"])
    features = np.empty((nodes, 10), dtype=np.float64)
    unit_gradient = np.empty((nodes, 4), dtype=np.float64)
    for start in range(0, nodes, POINT_BATCH):
        stop = min(start + POINT_BATCH, nodes)
        current = slice(start, stop)
        features[current], unit_gradient[current] = float_basis_simplex(
            chart,
            coordinates["u"][current],
            coordinates["r"][current],
            coordinates["v"][current],
            coordinates["t"][current],
        )
    signs = np.empty((len(group_rows), nodes), dtype=np.int8)
    summaries = []
    amplitudes = np.asarray(amplitude_rows, dtype=np.float64)
    for group_start in range(0, len(group_rows), GROUP_BATCH):
        group_stop = min(group_start + GROUP_BATCH, len(group_rows))
        values = float_scalars_from_basis(
            amplitudes[group_start:group_stop], features, unit_gradient
        )
        for local_index, group_index in enumerate(range(group_start, group_stop)):
            current = values[local_index]
            threshold = (
                ZERO_MULTIPLIER
                * np.finfo(np.float64).eps
                * max(1.0, float(np.max(np.abs(current))))
            )
            current_sign = np.where(
                current > threshold, 1, np.where(current < -threshold, -1, 0)
            ).astype(np.int8)
            signs[group_index] = current_sign
            summary = sheet_lattice_summary(current, current_sign, coordinates)
            summary.update(
                {
                    "level": level,
                    "sheet_id": (
                        f"{group_rows[group_index]['group_id']}_"
                        f"{'J1' if chart.startswith('J1') else 'J2'}"
                    ),
                    "group_id": group_rows[group_index]["group_id"],
                    "carrier_id": group_rows[group_index]["carrier_id"],
                    "mask_id": group_rows[group_index]["mask_id"],
                    "chart": chart,
                    "u_nodes": specification["nu"],
                    "simplex_denominator": specification["nq"],
                    "simplex_nodes": len(coordinates["triples"]),
                    "t_nodes": specification["nt"],
                    "total_nodes": nodes,
                    "fibers": specification["nu"] * len(coordinates["triples"]),
                    "zero_threshold": fmt(threshold),
                    "status": "OBSERVED_BOUNDED_LATTICE",
                }
            )
            summaries.append(summary)
    raw_name = (
        f"RAW_SIGNS_{level}_{'J1' if chart.startswith('J1') else 'J2'}.npy.gz"
    )
    raw_path = HERE / raw_name
    if raw_path.exists() and not replay:
        raise FileExistsError(raw_path)
    deterministic_npy_gz(raw_path, signs)
    return summaries, raw_name, digest(raw_path), coordinates


def main():
    replay = "--replay" in sys.argv[1:]
    unknown = [item for item in sys.argv[1:] if item != "--replay"]
    if unknown:
        raise SystemExit(f"unknown arguments: {unknown}")
    group_rows, amplitude_rows = groups()
    outputs = [
        HERE / "GROUP_REGISTRY.tsv",
        HERE / "LATTICE_SHEET_CENSUS.tsv",
        HERE / "COARSE_INTERVAL_CENSUS.tsv.gz",
        HERE / "LATTICE_COORDINATES.json",
        HERE / "RESULT.json",
    ]
    if not replay and any(path.exists() for path in outputs):
        raise FileExistsError("existing output requires --replay")

    amplitude_intervals = SRC.vector_amplitude_intervals(amplitude_rows)
    interval_rows = []
    interval_hashes = {}
    for chart in CHARTS:
        certificate = initial_certificate(chart, amplitude_intervals)
        interval_hashes[chart] = certificate["stream_hash"].hexdigest()
        for index, group in enumerate(group_rows):
            interval_rows.append(
                {
                    "sheet_id": (
                        f"{group['group_id']}_"
                        f"{'J1' if chart.startswith('J1') else 'J2'}"
                    ),
                    "chart": chart,
                    "initial_domain_boxes": (
                        GRID["u"] * GRID["r"] * GRID["v"] * GRID["t"]
                    ),
                    "derivative_certified_negative_boxes": (
                        GRID["u"] * GRID["r"] * GRID["v"] * GRID["t"]
                        - len(certificate["derivative_fail_cells"][index])
                    ),
                    "derivative_indeterminate_boxes": len(
                        certificate["derivative_fail_cells"][index]
                    ),
                    "face_certified_positive_boxes": (
                        GRID["u"] * GRID["r"] * GRID["v"]
                        - len(certificate["face_fail_cells"][index])
                    ),
                    "face_indeterminate_boxes": len(
                        certificate["face_fail_cells"][index]
                    ),
                    "vertex_certified_negative_boxes": (
                        GRID["u"] - len(certificate["vertex_fail_cells"][index])
                    ),
                    "vertex_indeterminate_boxes": len(
                        certificate["vertex_fail_cells"][index]
                    ),
                    "minimum_partial_t_s_lower": fmt(
                        certificate["derivative_lo"][index]
                    ),
                    "maximum_partial_t_s_upper": fmt(
                        certificate["derivative_hi"][index]
                    ),
                    "minimum_base_face_s_lower": fmt(
                        certificate["face_s_lo"][index]
                    ),
                    "maximum_b3_vertex_s_upper": fmt(
                        certificate["vertex_s_hi"][index]
                    ),
                    "cell_stream_sha256": interval_hashes[chart],
                    "arithmetic": "BINARY64_OUTWARD_NEXTAFTER_PLATFORM_SCOPED",
                    "continuous_topology_claim": "NONE",
                }
            )

    lattice_rows = []
    raw_files = {}
    coordinate_payload = {}
    for level in ("L1", "L2"):
        for chart in CHARTS:
            rows, raw_name, raw_hash, coordinates = build_lattice_level(
                level, chart, group_rows, amplitude_rows, replay
            )
            lattice_rows.extend(rows)
            raw_files[raw_name] = raw_hash
            if level not in coordinate_payload:
                coordinate_payload[level] = {
                    "u_nodes": [fmt(item) for item in coordinates["u_nodes"]],
                    "t_nodes": [fmt(item) for item in coordinates["t_nodes"]],
                    "barycentric_denominator": LEVELS[level]["nq"],
                    "barycentric_integer_triples": [
                        list(item) for item in coordinates["triples"]
                    ],
                    "triangular_edges": [
                        list(item) for item in coordinates["q_edges"]
                    ],
                    "raw_sign_order": ["group_index", "u_index", "q_index", "t_index"],
                }

    row_lookup = {
        (row["level"], row["sheet_id"]): row for row in lattice_rows
    }
    for row in lattice_rows:
        other_level = "L2" if row["level"] == "L1" else "L1"
        other = row_lookup[(other_level, row["sheet_id"])]
        row["cross_resolution_status"] = (
            "QUALITATIVE_CLASS_REPRODUCED"
            if row["primary_class"] == other["primary_class"]
            else "RESOLUTION_DEPENDENT_UNRESOLVED"
        )

    write_tsv(HERE / "GROUP_REGISTRY.tsv", list(group_rows[0]), group_rows)
    write_tsv(
        HERE / "LATTICE_SHEET_CENSUS.tsv",
        list(lattice_rows[0]),
        lattice_rows,
    )
    write_tsv_gz(
        HERE / "COARSE_INTERVAL_CENSUS.tsv.gz",
        list(interval_rows[0]),
        interval_rows,
    )
    (HERE / "LATTICE_COORDINATES.json").write_text(
        json.dumps(coordinate_payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    l2_rows = [row for row in lattice_rows if row["level"] == "L2"]
    l2_counts = Counter(row["primary_class"] for row in l2_rows)
    cross_counts = Counter(row["cross_resolution_status"] for row in l2_rows)
    result = {
        "schema": "udt-bank-simplex-interior-atlas-2.0",
        "base": BASE,
        "groups": len(group_rows),
        "charts": len(CHARTS),
        "chart_group_sheets": len(l2_rows),
        "lattice_levels": LEVELS,
        "lattice_rows": len(lattice_rows),
        "l2_primary_class_counts": dict(sorted(l2_counts.items())),
        "cross_resolution_counts": dict(sorted(cross_counts.items())),
        "coarse_interval_rows": len(interval_rows),
        "coarse_initial_domain_boxes": sum(
            int(row["initial_domain_boxes"]) for row in interval_rows
        ),
        "coarse_derivative_indeterminate_boxes": sum(
            int(row["derivative_indeterminate_boxes"]) for row in interval_rows
        ),
        "coarse_face_indeterminate_boxes": sum(
            int(row["face_indeterminate_boxes"]) for row in interval_rows
        ),
        "coarse_vertex_indeterminate_boxes": sum(
            int(row["vertex_indeterminate_boxes"]) for row in interval_rows
        ),
        "coarse_interval_cell_stream_sha256": interval_hashes,
        "raw_sign_files": raw_files,
        "all_angular_and_shift_fields_retained": True,
        "metric_determinant_status": "EXACTLY_NEGATIVE_FOR_FINITE_LATENT_FIELDS",
        "physical_regime_labels_used": 0,
        "actions_or_eom_loaded": 0,
        "carrier_interpretations_loaded": 0,
        "gpu_runs": 0,
        "maximum_conclusion": (
            "BOUNDED_REGISTERED_COMPLETE_BANK-SIMPLEX_LATTICE_ATLAS_"
            "WITH_INTERVAL_AND_MATRIX_CHECKS"
        ),
        "environment": {
            "python": platform.python_version(),
            "numpy": np.__version__,
            "platform": platform.platform(),
            "byteorder": sys.byteorder,
        },
        "source_hashes": {
            str(SOURCE_PATH.relative_to(ROOT)): digest(SOURCE_PATH),
            str(CARRIER_FILE.relative_to(ROOT)): digest(CARRIER_FILE),
            str(IDENTITY_FILE.relative_to(ROOT)): digest(IDENTITY_FILE),
            str(CAUSAL_FILE.relative_to(ROOT)): digest(CAUSAL_FILE),
            str(ADJACENCY_RESULT.relative_to(ROOT)): digest(ADJACENCY_RESULT),
            str(ENDPOINT_PAIR_FILE.relative_to(ROOT)): digest(ENDPOINT_PAIR_FILE),
            str(PRIOR_SHEET_FILE.relative_to(ROOT)): digest(PRIOR_SHEET_FILE),
        },
    }
    (HERE / "RESULT.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
