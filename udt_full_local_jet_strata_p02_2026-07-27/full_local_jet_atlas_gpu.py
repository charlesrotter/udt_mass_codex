#!/usr/bin/env python3
"""Construct and evaluate the preregistered P02 full-local-jet atlas."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import os
import platform
import time
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import scipy
import torch
from scipy.stats import qmc


AMPLITUDES = ("phi", "sigma", "alpha", "k", "S10", "S11", "S20", "S21")
HESSIAN_PAIRS = ((0, 0), (0, 1), (0, 2), (0, 3), (1, 1), (1, 2), (1, 3), (2, 2), (2, 3), (3, 3))
FEATURE_NAMES = (
    "det_relative_error",
    "dphi_norm",
    "dphi_target_residual",
    "scalar_curvature",
    "kretschmann",
    "ricci_frame_frobenius",
    "pair_screen_ricci_mixing",
    "tidal_discriminant",
    "tidal_repeated",
    "base_section_R0101",
    "angular_section_R2323",
    "curvature_operator_rank",
    "curvature_operator_smallest_largest_ratio",
    "numerically_finite",
)


@dataclass
class Jet2:
    value: torch.Tensor
    first: torch.Tensor
    second: torch.Tensor

    def __add__(self, other):
        if not isinstance(other, Jet2):
            other = constant_like(self, other)
        return Jet2(self.value + other.value, self.first + other.first, self.second + other.second)

    __radd__ = __add__

    def __neg__(self):
        return Jet2(-self.value, -self.first, -self.second)

    def __sub__(self, other):
        return self + (-other if isinstance(other, Jet2) else -float(other))

    def __rsub__(self, other):
        return constant_like(self, other) - self

    def __mul__(self, other):
        if not isinstance(other, Jet2):
            other = constant_like(self, other)
        return Jet2(
            self.value * other.value,
            self.first * other.value[..., None] + self.value[..., None] * other.first,
            self.second * other.value[..., None, None]
            + self.value[..., None, None] * other.second
            + torch.einsum("...i,...j->...ij", self.first, other.first)
            + torch.einsum("...j,...i->...ij", self.first, other.first),
        )

    __rmul__ = __mul__


def constant_like(reference: Jet2, value: float) -> Jet2:
    val = torch.zeros_like(reference.value) + value
    return Jet2(val, torch.zeros_like(reference.first), torch.zeros_like(reference.second))


def exp_jet(value: Jet2) -> Jet2:
    exponential = torch.exp(value.value)
    return Jet2(
        exponential,
        exponential[..., None] * value.first,
        exponential[..., None, None] * (value.second + torch.einsum("...i,...j->...ij", value.first, value.first)),
    )


def stack_matrix(rows: list[list[Jet2]]) -> Jet2:
    value = torch.stack([torch.stack([entry.value for entry in row], dim=-1) for row in rows], dim=-2)
    first = torch.stack([torch.stack([entry.first for entry in row], dim=-2) for row in rows], dim=-3)
    second = torch.stack([torch.stack([entry.second for entry in row], dim=-3) for row in rows], dim=-4)
    return Jet2(value, first, second)


def coframe_jets(q: torch.Tensor, dq: torch.Tensor, ddq: torch.Tensor) -> Jet2:
    jets = [Jet2(q[:, index], dq[:, index], ddq[:, index]) for index in range(8)]
    phi, sigma, alpha, k, s10, s11, s20, s21 = jets
    zero = constant_like(phi, 0.0)
    clock = exp_jet(-phi)
    ruler = exp_jet(phi)
    r = exp_jet(0.5 * sigma - alpha)
    qang = exp_jet(0.5 * sigma + alpha)
    return stack_matrix(
        [
            [clock, zero, zero, zero],
            [zero, ruler, zero, zero],
            [r * (s10 + k * s20), r * (s11 + k * s21), r, k * r],
            [qang * s20, qang * s21, zero, qang],
        ]
    )


def metric_jets(E: Jet2) -> Jet2:
    eta = torch.tensor((-1.0, 1.0, 1.0, 1.0), dtype=E.value.dtype, device=E.value.device)
    return Jet2(
        torch.einsum("...am,a,...an->...mn", E.value, eta, E.value),
        torch.einsum("...ami,a,...an->...mni", E.first, eta, E.value)
        + torch.einsum("...am,a,...ani->...mni", E.value, eta, E.first),
        torch.einsum("...amij,a,...an->...mnij", E.second, eta, E.value)
        + torch.einsum("...ami,a,...anj->...mnij", E.first, eta, E.first)
        + torch.einsum("...amj,a,...ani->...mnij", E.first, eta, E.first)
        + torch.einsum("...am,a,...anij->...mnij", E.value, eta, E.second),
    )


def geometry(E: Jet2, metric: Jet2) -> dict[str, torch.Tensor]:
    g = metric.value
    ginv = torch.linalg.inv(g)
    dg = metric.first.permute(0, 3, 1, 2)
    ddg = metric.second.permute(0, 3, 4, 1, 2)
    dginv = -torch.einsum("...ra,...kab,...bs->...krs", ginv, dg, ginv)
    batch = g.shape[0]
    B = torch.zeros((batch, 4, 4, 4), dtype=g.dtype, device=g.device)
    dB = torch.zeros((batch, 4, 4, 4, 4), dtype=g.dtype, device=g.device)
    for s in range(4):
        for m in range(4):
            for n in range(4):
                B[:, s, m, n] = dg[:, m, s, n] + dg[:, n, s, m] - dg[:, s, m, n]
                for axis in range(4):
                    dB[:, axis, s, m, n] = ddg[:, axis, m, s, n] + ddg[:, axis, n, s, m] - ddg[:, axis, s, m, n]
    gamma = 0.5 * torch.einsum("...rs,...smn->...rmn", ginv, B)
    dgamma = 0.5 * (
        torch.einsum("...krs,...smn->...krmn", dginv, B)
        + torch.einsum("...rs,...ksmn->...krmn", ginv, dB)
    )
    product1 = torch.einsum("...rml,...lns->...rsmn", gamma, gamma)
    product2 = torch.einsum("...rnl,...lms->...rsmn", gamma, gamma)
    rup = torch.zeros((batch, 4, 4, 4, 4), dtype=g.dtype, device=g.device)
    for mu in range(4):
        for nu in range(4):
            rup[:, :, :, mu, nu] = (
                dgamma[:, mu, :, nu, :] - dgamma[:, nu, :, mu, :]
                + product1[:, :, :, mu, nu] - product2[:, :, :, mu, nu]
            )
    ricci = torch.zeros((batch, 4, 4), dtype=g.dtype, device=g.device)
    for rho in range(4):
        ricci += rup[:, rho, :, rho, :]
    scalar = torch.einsum("...mn,...mn->...", ginv, ricci)
    rdown = torch.einsum("...ar,...rsmn->...asmn", g, rup)
    dual = torch.linalg.inv(E.value)
    rframe = torch.einsum("...ma,...nb,...pc,...qd,...mnpq->...abcd", dual, dual, dual, dual, rdown)
    ricci_frame = torch.einsum("...ma,...nb,...mn->...ab", dual, dual, ricci)
    signs = torch.tensor((-1.0, 1.0, 1.0, 1.0), dtype=g.dtype, device=g.device)
    kretschmann = torch.einsum("a,b,c,d,...abcd,...abcd->...", signs, signs, signs, signs, rframe, rframe)
    return {
        "g": g,
        "ginv": ginv,
        "gamma": gamma,
        "ricci": ricci,
        "scalar": scalar,
        "rframe": rframe,
        "ricci_frame": ricci_frame,
        "kretschmann": kretschmann,
    }


def evaluate(q: torch.Tensor, dq: torch.Tensor, ddq: torch.Tensor, target_norm: torch.Tensor) -> tuple[np.ndarray, torch.Tensor]:
    E = coframe_jets(q, dq, ddq)
    metric = metric_jets(E)
    geo = geometry(E, metric)
    det = torch.linalg.det(geo["g"])
    expected = -torch.exp(2 * q[:, 1])
    det_error = torch.abs(det - expected) / (1 + torch.abs(expected))
    dphi_norm = torch.einsum("...m,...mn,...n->...", dq[:, 0], geo["ginv"], dq[:, 0])
    target_residual = torch.abs(dphi_norm - target_norm) / (1 + torch.abs(target_norm))
    ricf = geo["ricci_frame"]
    ricci_frob = torch.linalg.matrix_norm(ricf, dim=(-2, -1))
    mixing = torch.sqrt(torch.sum(ricf[:, 0:2, 2:4] ** 2, dim=(-2, -1)) + torch.sum(ricf[:, 2:4, 0:2] ** 2, dim=(-2, -1)))
    rframe = geo["rframe"]
    t22 = rframe[:, 2, 0, 2, 0]
    t23 = 0.5 * (rframe[:, 2, 0, 3, 0] + rframe[:, 3, 0, 2, 0])
    t33 = rframe[:, 3, 0, 3, 0]
    discriminant = (t22 - t33) ** 2 + 4 * t23 ** 2
    tidal_scale = 1e-10 * (1 + t22 * t22 + 2 * t23 * t23 + t33 * t33)
    repeated = discriminant <= tidal_scale
    pairs = ((0, 1), (0, 2), (0, 3), (2, 3), (3, 1), (1, 2))
    curvature_operator = torch.stack(
        [torch.stack([rframe[:, a, b, c, d] for c, d in pairs], dim=-1) for a, b in pairs],
        dim=-2,
    )
    singular = torch.linalg.svdvals(curvature_operator)
    threshold = 1e-10 * torch.maximum(torch.ones_like(singular[:, 0]), singular[:, 0])
    curvature_rank = torch.sum(singular > threshold[:, None], dim=-1)
    ratio = singular[:, -1] / torch.clamp(singular[:, 0], min=1e-300)
    finite_stack = torch.stack(
        (
            det_error,
            dphi_norm,
            target_residual,
            geo["scalar"],
            geo["kretschmann"],
            ricci_frob,
            mixing,
            discriminant,
            rframe[:, 0, 1, 0, 1],
            rframe[:, 2, 3, 2, 3],
            ratio,
        ),
        dim=-1,
    )
    finite = torch.all(torch.isfinite(finite_stack), dim=-1)
    features = torch.stack(
        (
            det_error,
            dphi_norm,
            target_residual,
            geo["scalar"],
            geo["kretschmann"],
            ricci_frob,
            mixing,
            discriminant,
            repeated.to(q.dtype),
            rframe[:, 0, 1, 0, 1],
            rframe[:, 2, 3, 2, 3],
            curvature_rank.to(q.dtype),
            ratio,
            finite.to(q.dtype),
        ),
        dim=-1,
    )
    return features.detach().cpu().numpy(), geo["g"]


def coframe_numpy(q: np.ndarray) -> np.ndarray:
    phi, sigma, alpha, k, s10, s11, s20, s21 = q
    r = math.exp(0.5 * sigma - alpha)
    qang = math.exp(0.5 * sigma + alpha)
    return np.array(
        [
            [math.exp(-phi), 0.0, 0.0, 0.0],
            [0.0, math.exp(phi), 0.0, 0.0],
            [r * (s10 + k * s20), r * (s11 + k * s21), r, k * r],
            [qang * s20, qang * s21, 0.0, qang],
        ],
        dtype=np.float64,
    )


def nonzero(value: float, floor: float = 0.25) -> float:
    sign = -1.0 if value < 0 else 1.0
    return sign * (floor + (1 - floor) * abs(value))


def truncated_matrix(raw: np.ndarray, rows: int, columns: int, rank: int, shell: float) -> np.ndarray:
    if rank == 0:
        return np.zeros((rows, columns), dtype=np.float64)
    matrix = raw[: rows * columns].reshape(rows, columns)
    u, _, vh = np.linalg.svd(matrix, full_matrices=False)
    singular = shell * (1.0 + 0.125 * np.arange(rank))
    return (u[:, :rank] * singular) @ vh[:rank]


def numerical_rank(matrix: np.ndarray) -> int:
    singular = np.linalg.svd(matrix, compute_uv=False)
    if singular.size == 0:
        return 0
    return int(np.sum(singular > 1e-10 * max(1.0, singular[0])))


def construct(universe: list[dict[str, str]], controls: np.ndarray) -> dict[str, np.ndarray]:
    count = len(universe) * 2
    q = np.zeros((count, 8), dtype=np.float64)
    dq = np.zeros((count, 8, 4), dtype=np.float64)
    ddq = np.zeros((count, 8, 4, 4), dtype=np.float64)
    target = np.full(count, np.nan, dtype=np.float64)
    status = np.empty(count, dtype="U48")
    stratum_ids = np.empty(count, dtype="U10")
    replicates = np.empty(count, dtype=np.int8)
    requested = np.empty((count, 8), dtype=np.int16)
    attempt = 0
    for stratum_index, row in enumerate(universe):
        for replicate in range(2):
            z = controls[attempt]
            shell = float(row["shell"])
            static = row["coordinate_time"] == "COORDINATE_STATIC"
            phi_class = row["phi_gradient"]
            angular_shape = row["angular_shape"]
            shift_value_rank = int(row["shift_value_rank"])
            angular_rank = int(row["angular_first_rank"])
            shift_rank = int(row["shift_first_rank"])
            hessian_rank = int(row["collective_Hessian_rank"])
            stratum_ids[attempt] = row["stratum_id"]
            replicates[attempt] = replicate
            requested[attempt] = (
                0 if shell == 0.3 else 1,
                1 if static else 0,
                ("ZERO", "TIMELIKE", "NULL", "SPACELIKE").index(phi_class),
                ("ISOTROPIC", "DIAGONAL_ANISOTROPIC", "SHEARED").index(angular_shape),
                shift_value_rank,
                angular_rank,
                shift_rank,
                hessian_rank,
            )
            qi = q[attempt]
            qi[0] = shell * z[0]
            qi[1] = shell * z[1]
            if angular_shape == "ISOTROPIC":
                qi[2:4] = 0
            elif angular_shape == "DIAGONAL_ANISOTROPIC":
                qi[2] = shell * nonzero(z[2])
                qi[3] = 0
            else:
                qi[2] = shell * nonzero(z[2])
                qi[3] = shell * nonzero(z[3])
            if shift_value_rank == 0:
                shift = np.zeros((2, 2))
            elif shift_value_rank == 1:
                u = z[4:6] / max(np.linalg.norm(z[4:6]), 1e-15)
                v = z[6:8] / max(np.linalg.norm(z[6:8]), 1e-15)
                shift = shell * (0.4 + 0.6 * abs(z[8])) * np.outer(u, v)
            else:
                shift = truncated_matrix(z[4:8], 2, 2, 2, shell)
            qi[4:8] = shift.reshape(-1)
            active_columns = (1, 2, 3) if static else (0, 1, 2, 3)
            if static and shift_rank == 4:
                status[attempt] = "STRUCTURALLY_INCOMPATIBLE_SHIFT_RANK"
                attempt += 1
                continue
            if static and hessian_rank == 8:
                status[attempt] = "STRUCTURALLY_INCOMPATIBLE_HESSIAN_RANK"
                attempt += 1
                continue
            angular_matrix = truncated_matrix(z[24:36], 3, len(active_columns), angular_rank, shell)
            shift_matrix = truncated_matrix(z[40:56], 4, len(active_columns), shift_rank, shell)
            dq[attempt, 1:4][:, active_columns] = angular_matrix
            dq[attempt, 4:8][:, active_columns] = shift_matrix
            available_pairs = tuple(pair for pair in HESSIAN_PAIRS if not static or (pair[0] != 0 and pair[1] != 0))
            hessian_matrix = truncated_matrix(z[64:144], 8, len(available_pairs), hessian_rank, shell)
            for column, (a, b) in enumerate(available_pairs):
                ddq[attempt, :, a, b] = hessian_matrix[:, column]
                ddq[attempt, :, b, a] = hessian_matrix[:, column]
            E = coframe_numpy(qi)
            eta = np.diag((-1.0, 1.0, 1.0, 1.0))
            ginv = np.linalg.inv(E.T @ eta @ E)
            if phi_class == "ZERO":
                pcoord = np.zeros(4)
                target[attempt] = 0.0
            elif not static:
                direction = z[150:153]
                direction /= max(np.linalg.norm(direction), 1e-15)
                if phi_class == "TIMELIKE":
                    spatial = 0.25 * shell * direction
                    pframe = np.concatenate(([math.sqrt(shell * shell + spatial @ spatial)], spatial))
                    target[attempt] = -shell * shell
                elif phi_class == "SPACELIKE":
                    time_component = 0.25 * shell * z[153]
                    spatial = math.sqrt(shell * shell + time_component * time_component) * direction
                    pframe = np.concatenate(([time_component], spatial))
                    target[attempt] = shell * shell
                else:
                    pframe = np.concatenate(([shell], shell * direction))
                    target[attempt] = 0.0
                pcoord = E.T @ pframe
            else:
                spatial_block = 0.5 * (ginv[1:, 1:] + ginv[1:, 1:].T)
                eigenvalues, eigenvectors = np.linalg.eigh(spatial_block)
                negative = np.flatnonzero(eigenvalues < -1e-12)
                positive = np.flatnonzero(eigenvalues > 1e-12)
                near_zero = np.flatnonzero(np.abs(eigenvalues) <= 1e-12)
                vector = None
                if phi_class == "TIMELIKE" and negative.size:
                    index = negative[0]
                    vector = shell * eigenvectors[:, index] / math.sqrt(-eigenvalues[index])
                    target[attempt] = -shell * shell
                elif phi_class == "SPACELIKE" and positive.size:
                    index = positive[-1]
                    vector = shell * eigenvectors[:, index] / math.sqrt(eigenvalues[index])
                    target[attempt] = shell * shell
                elif phi_class == "NULL" and near_zero.size:
                    vector = shell * eigenvectors[:, near_zero[0]]
                    target[attempt] = 0.0
                elif phi_class == "NULL" and negative.size and positive.size:
                    neg, pos = negative[0], positive[-1]
                    vector = eigenvectors[:, neg] / math.sqrt(-eigenvalues[neg]) + eigenvectors[:, pos] / math.sqrt(eigenvalues[pos])
                    vector *= shell / np.linalg.norm(vector)
                    target[attempt] = 0.0
                if vector is None:
                    status[attempt] = "NO_CAUSAL_WITNESS_AT_SAMPLED_VALUE"
                    attempt += 1
                    continue
                pcoord = np.concatenate(([0.0], vector))
            dq[attempt, 0] = pcoord
            observed_norm = float(pcoord @ ginv @ pcoord)
            causal_residual = abs(observed_norm - target[attempt]) / (1 + abs(target[attempt]))
            rank_ok = (
                numerical_rank(dq[attempt, 1:4]) == angular_rank
                and numerical_rank(dq[attempt, 4:8]) == shift_rank
                and numerical_rank(np.column_stack([ddq[attempt, :, a, b] for a, b in HESSIAN_PAIRS])) == hessian_rank
            )
            static_ok = not static or (np.all(dq[attempt, :, 0] == 0) and np.all(ddq[attempt, :, 0, :] == 0) and np.all(ddq[attempt, :, :, 0] == 0))
            if causal_residual > 1e-10 or not rank_ok or not static_ok:
                raise AssertionError(f"construction fidelity failure {row['stratum_id']} replicate {replicate}: {causal_residual} {rank_ok} {static_ok}")
            status[attempt] = "CONSTRUCTED"
            attempt += 1
    return {
        "q": q,
        "dq": dq,
        "ddq": ddq,
        "target_norm": target,
        "status": status,
        "stratum_id": stratum_ids,
        "replicate": replicates,
        "requested_axes": requested,
    }


def run_controls(device: torch.device) -> dict[str, float | bool]:
    dtype = torch.float64
    q = torch.zeros((1, 8), dtype=dtype, device=device)
    dq = torch.zeros((1, 8, 4), dtype=dtype, device=device)
    ddq = torch.zeros((1, 8, 4, 4), dtype=dtype, device=device)
    zero_features, _ = evaluate(q, dq, ddq, torch.zeros(1, dtype=dtype, device=device))
    q[0] = torch.tensor((0.2, -0.3, 0.1, 0.15, 0.05, -0.08, 0.12, -0.04), dtype=dtype, device=device)
    constant_features, _ = evaluate(q, dq, ddq, torch.zeros(1, dtype=dtype, device=device))
    E = coframe_jets(q, dq, ddq)
    metric = metric_jets(E)
    rapidity = torch.tensor(0.37, dtype=dtype, device=device)
    boost = torch.eye(4, dtype=dtype, device=device)
    boost[0, 0] = torch.cosh(rapidity)
    boost[0, 1] = torch.sinh(rapidity)
    boost[1, 0] = torch.sinh(rapidity)
    boost[1, 1] = torch.cosh(rapidity)
    transformed = Jet2(
        torch.einsum("ab,...bm->...am", boost, E.value),
        torch.einsum("ab,...bmi->...ami", boost, E.first),
        torch.einsum("ab,...bmij->...amij", boost, E.second),
    )
    transformed_metric = metric_jets(transformed)
    lorentz_metric_error = float(torch.max(torch.abs(metric.value - transformed_metric.value)).cpu())
    result = {
        "zero_det_error": float(zero_features[0, 0]),
        "zero_scalar": float(abs(zero_features[0, 3])),
        "zero_kretschmann": float(abs(zero_features[0, 4])),
        "constant_det_error": float(constant_features[0, 0]),
        "constant_scalar": float(abs(constant_features[0, 3])),
        "constant_kretschmann": float(abs(constant_features[0, 4])),
        "constant_lorentz_coframe_metric_error": lorentz_metric_error,
    }
    result["pass"] = all(value <= 1e-10 for value in result.values())
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--package", type=Path, required=True)
    parser.add_argument("--device", default="cuda:0")
    parser.add_argument("--batch", type=int, default=512)
    parser.add_argument("--production", action="store_true")
    args = parser.parse_args()
    package = args.package.resolve()
    if args.production and (args.device != "cuda:0" or args.batch != 512):
        raise SystemExit("production arguments differ from preregistration")
    outputs = ("JET_ATLAS.npz", "ATLAS_RESULT.json", "CPU_ANCHOR_GPU.json")
    if any((package / name).exists() for name in outputs):
        raise FileExistsError("P02 production output already exists")
    device = torch.device(args.device)
    if device.type == "cuda" and not torch.cuda.is_available():
        raise RuntimeError("CUDA requested but unavailable")
    start = time.time()
    with (package / "STRATUM_UNIVERSE.tsv").open(newline="") as handle:
        universe = list(csv.DictReader(handle, delimiter="\t"))
    sampler = qmc.Sobol(d=256, scramble=True, seed=20260728)
    controls_full = 2 * sampler.random_base2(15) - 1
    controls = controls_full[:23040].astype(np.float64)
    controls_hash = hashlib.sha256(controls.tobytes()).hexdigest()
    constructed = construct(universe, controls)
    controls_result = run_controls(device)
    if not controls_result["pass"]:
        raise AssertionError(controls_result)
    features = np.full((23040, len(FEATURE_NAMES)), np.nan, dtype=np.float64)
    indices = np.flatnonzero(constructed["status"] == "CONSTRUCTED")
    peak_memory = 0
    for offset in range(0, len(indices), args.batch):
        selected = indices[offset : offset + args.batch]
        q = torch.tensor(constructed["q"][selected], dtype=torch.float64, device=device)
        dq = torch.tensor(constructed["dq"][selected], dtype=torch.float64, device=device)
        ddq = torch.tensor(constructed["ddq"][selected], dtype=torch.float64, device=device)
        target = torch.tensor(constructed["target_norm"][selected], dtype=torch.float64, device=device)
        evaluated, _ = evaluate(q, dq, ddq, target)
        features[selected] = evaluated
        if device.type == "cuda":
            peak_memory = max(peak_memory, torch.cuda.max_memory_allocated(device))
    if peak_memory > 2 * 1024**3:
        raise RuntimeError(f"registered memory gate exceeded: {peak_memory}")
    constructed_features = features[indices]
    if np.any(constructed_features[:, 0] > 1e-10) or np.any(constructed_features[:, 2] > 1e-10):
        raise AssertionError("determinant or causal target control failed")
    shell_code = constructed["requested_axes"][:, 0]
    finite = constructed_features[:, FEATURE_NAMES.index("numerically_finite")] > 0.5
    for code, threshold in ((0, 0.01), (1, 0.05)):
        subset = indices[shell_code[indices] == code]
        fraction = 1 - np.mean(features[subset, FEATURE_NAMES.index("numerically_finite")] > 0.5)
        if fraction > threshold:
            raise RuntimeError(f"shell {code} nonfinite threshold exceeded: {fraction}")
    np.savez_compressed(
        package / "JET_ATLAS.npz",
        q=constructed["q"],
        dq=constructed["dq"],
        ddq=constructed["ddq"],
        target_norm=constructed["target_norm"],
        status=constructed["status"],
        stratum_id=constructed["stratum_id"],
        replicate=constructed["replicate"],
        requested_axes=constructed["requested_axes"],
        requested_axis_names=np.array(("shell_code", "static_code", "phi_class_code", "angular_shape_code", "shift_value_rank", "angular_first_rank", "shift_first_rank", "collective_Hessian_rank")),
        features=features,
        feature_names=np.array(FEATURE_NAMES),
    )
    anchor_positions = np.linspace(0, len(indices) - 1, 64, dtype=int)
    anchor_indices = indices[anchor_positions]
    q_anchor = torch.tensor(constructed["q"][anchor_indices], dtype=torch.float64, device=device)
    dq_anchor = torch.tensor(constructed["dq"][anchor_indices], dtype=torch.float64, device=device)
    ddq_anchor = torch.tensor(constructed["ddq"][anchor_indices], dtype=torch.float64, device=device)
    target_anchor = torch.tensor(constructed["target_norm"][anchor_indices], dtype=torch.float64, device=device)
    anchor_features, anchor_metric = evaluate(q_anchor, dq_anchor, ddq_anchor, target_anchor)
    anchor = {
        "schema": "udt-p02-gpu-cpu-anchor-1.0",
        "indices": anchor_indices.tolist(),
        "q": constructed["q"][anchor_indices].tolist(),
        "dq": constructed["dq"][anchor_indices].tolist(),
        "ddq": constructed["ddq"][anchor_indices].tolist(),
        "metric": anchor_metric.detach().cpu().tolist(),
        "scalar": anchor_features[:, FEATURE_NAMES.index("scalar_curvature")].tolist(),
        "dphi_norm": anchor_features[:, FEATURE_NAMES.index("dphi_norm")].tolist(),
    }
    (package / "CPU_ANCHOR_GPU.json").write_text(json.dumps(anchor, indent=2, sort_keys=True) + "\n")
    status_values, status_counts = np.unique(constructed["status"], return_counts=True)
    summary = {
        "schema": "udt-full-local-jet-strata-p02-result-1.0",
        "status": "PASS",
        "epistemic_scope": "BOUNDED_LOCAL_OFF_SHELL_TWO_JET_STRATA_NOT_SOLUTIONS",
        "strata": len(universe),
        "attempts": 23040,
        "status_counts": {str(name): int(count) for name, count in zip(status_values, status_counts)},
        "constructed": int(len(indices)),
        "controls": controls_result,
        "controls_consumed_sha256": controls_hash,
        "stratum_universe_sha256": hashlib.sha256((package / "STRATUM_UNIVERSE.tsv").read_bytes()).hexdigest(),
        "atlas_npz_sha256": hashlib.sha256((package / "JET_ATLAS.npz").read_bytes()).hexdigest(),
        "feature_names": list(FEATURE_NAMES),
        "constructed_feature_ranges": {
            name: {
                "minimum": float(np.nanmin(constructed_features[:, column])),
                "median": float(np.nanmedian(constructed_features[:, column])),
                "maximum": float(np.nanmax(constructed_features[:, column])),
            }
            for column, name in enumerate(FEATURE_NAMES)
        },
        "environment": {
            "python": platform.python_version(),
            "numpy": np.__version__,
            "scipy": scipy.__version__,
            "torch": torch.__version__,
            "device": torch.cuda.get_device_name(device) if device.type == "cuda" else str(device),
            "dtype": "float64",
            "batch": args.batch,
            "peak_memory_bytes": peak_memory,
            "wall_seconds": time.time() - start,
            "pid": os.getpid(),
        },
        "maximum_conclusion": "CONSTRUCTIVE_AND_NO_WITNESS_CENSUS_IN_THE_EXACT_PREREGISTERED_LOCAL_JET_UNIVERSE_WITHOUT_GLOBAL_REALIZATION_OR_PHYSICAL_SELECTION",
    }
    (package / "ATLAS_RESULT.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(summary, sort_keys=True))


if __name__ == "__main__":
    main()
