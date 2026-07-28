#!/usr/bin/env python3
"""Batched float64 complete-coframe configuration and transport atlas."""

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
import torch
from scipy.stats import qmc


AMPLITUDES = ("phi", "sigma", "alpha", "k", "S10", "S11", "S20", "S21")
FEATURE_NAMES = (
    "det_relative_error_max",
    "scalar_abs_max",
    "scalar_rms",
    "kretschmann_abs_max",
    "pair_screen_ricci_mix_max",
    "dphi_norm_min",
    "dphi_norm_max",
    "dphi_timelike_fraction",
    "dphi_null_fraction",
    "dphi_spacelike_fraction",
    "dphi_zero_fraction",
    "tidal_repeated_fraction",
    "tidal_discriminant_min",
    "grid_nonfinite_fraction",
    "holonomy_deviation",
    "holonomy_trace_minus_four",
    "holonomy_determinant_minus_one",
    "holonomy_pair_screen_mixing",
    "holonomy_lorentz_error",
    "reverse_composition_error",
    "frame_connection_projection_error",
    "holonomy_nontrivial",
    "transport_numerically_unresolved",
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
        value = self.value * other.value
        first = self.first * other.value[..., None] + self.value[..., None] * other.first
        second = (
            self.second * other.value[..., None, None]
            + self.value[..., None, None] * other.second
            + torch.einsum("...i,...j->...ij", self.first, other.first)
            + torch.einsum("...j,...i->...ij", self.first, other.first)
        )
        return Jet2(value, first, second)

    __rmul__ = __mul__


def constant_like(reference: Jet2, value) -> Jet2:
    val = torch.zeros_like(reference.value) + value
    return Jet2(val, torch.zeros_like(reference.first), torch.zeros_like(reference.second))


def exp_jet(value: Jet2) -> Jet2:
    ev = torch.exp(value.value)
    first = ev[..., None] * value.first
    second = ev[..., None, None] * (
        value.second + torch.einsum("...i,...j->...ij", value.first, value.first)
    )
    return Jet2(ev, first, second)


def stack_matrix(rows: list[list[Jet2]]) -> Jet2:
    value = torch.stack([torch.stack([entry.value for entry in row], dim=-1) for row in rows], dim=-2)
    first = torch.stack([torch.stack([entry.first for entry in row], dim=-2) for row in rows], dim=-3)
    second = torch.stack([torch.stack([entry.second for entry in row], dim=-3) for row in rows], dim=-4)
    return Jet2(value, first, second)


def basis_jets(t: torch.Tensor, x: torch.Tensor) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
    """Return basis values, first jets (t,x), and Hessians at flat point arrays."""
    pi = torch.tensor(math.pi, dtype=t.dtype, device=t.device)
    zero = torch.zeros_like(t)
    one = torch.ones_like(t)
    values = [
        one,
        x,
        (3 * x * x - 1) / 2,
        torch.sin(pi * x),
        torch.sin(pi * t),
        torch.cos(pi * t),
        torch.sin(pi * t) * torch.cos(pi * x),
        torch.cos(2 * pi * t) * torch.sin(pi * x),
    ]
    first = [
        (zero, zero),
        (zero, one),
        (zero, 3 * x),
        (zero, pi * torch.cos(pi * x)),
        (pi * torch.cos(pi * t), zero),
        (-pi * torch.sin(pi * t), zero),
        (pi * torch.cos(pi * t) * torch.cos(pi * x), -pi * torch.sin(pi * t) * torch.sin(pi * x)),
        (-2 * pi * torch.sin(2 * pi * t) * torch.sin(pi * x), pi * torch.cos(2 * pi * t) * torch.cos(pi * x)),
    ]
    second = [
        (zero, zero, zero),
        (zero, zero, zero),
        (zero, zero, 3 * one),
        (zero, zero, -pi * pi * torch.sin(pi * x)),
        (-pi * pi * torch.sin(pi * t), zero, zero),
        (-pi * pi * torch.cos(pi * t), zero, zero),
        (-pi * pi * values[6], -pi * pi * torch.cos(pi * t) * torch.sin(pi * x), -pi * pi * values[6]),
        (-4 * pi * pi * values[7], -2 * pi * pi * torch.sin(2 * pi * t) * torch.cos(pi * x), -pi * pi * values[7]),
    ]
    b = torch.stack(values, dim=-1)
    db = torch.stack([torch.stack(pair, dim=-1) for pair in first], dim=-2)
    ddb = torch.stack(
        [torch.stack((tt, tx, tx, xx), dim=-1).reshape(t.shape + (2, 2)) for tt, tx, xx in second],
        dim=-3,
    )
    return b, db, ddb


def amplitude_jets(coefficients: torch.Tensor, shell: float, t: torch.Tensor, x: torch.Tensor) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
    b, db, ddb = basis_jets(t, x)
    factor = shell / math.sqrt(8.0)
    q = factor * torch.einsum("baj,pj->bpa", coefficients, b)
    dq = factor * torch.einsum("baj,pji->bpai", coefficients, db)
    ddq = factor * torch.einsum("baj,pjkl->bpakl", coefficients, ddb)
    return q, dq, ddq


def coframe_jets(coefficients: torch.Tensor, shell: float, t: torch.Tensor, x: torch.Tensor) -> tuple[Jet2, torch.Tensor, torch.Tensor]:
    q, dq, ddq = amplitude_jets(coefficients, shell, t, x)
    jets = [Jet2(q[..., index], dq[..., index, :], ddq[..., index, :, :]) for index in range(8)]
    phi, sigma, alpha, k, s10, s11, s20, s21 = jets
    zero = constant_like(phi, 0.0)
    e_clock = exp_jet(-phi)
    e_ruler = exp_jet(phi)
    r = exp_jet(0.5 * sigma - alpha)
    qang = exp_jet(0.5 * sigma + alpha)
    E = stack_matrix([
        [e_clock, zero, zero, zero],
        [zero, e_ruler, zero, zero],
        [r * (s10 + k * s20), r * (s11 + k * s21), r, k * r],
        [qang * s20, qang * s21, zero, qang],
    ])
    return E, q, dq


def metric_jets(E: Jet2) -> Jet2:
    eta = torch.tensor((-1.0, 1.0, 1.0, 1.0), dtype=E.value.dtype, device=E.value.device)
    value = torch.einsum("...am,a,...an->...mn", E.value, eta, E.value)
    first = (
        torch.einsum("...ami,a,...an->...mni", E.first, eta, E.value)
        + torch.einsum("...am,a,...ani->...mni", E.value, eta, E.first)
    )
    second = (
        torch.einsum("...amij,a,...an->...mnij", E.second, eta, E.value)
        + torch.einsum("...ami,a,...anj->...mnij", E.first, eta, E.first)
        + torch.einsum("...amj,a,...ani->...mnij", E.first, eta, E.first)
        + torch.einsum("...am,a,...anij->...mnij", E.value, eta, E.second)
    )
    return Jet2(value, first, second)


def connection_and_curvature(E: Jet2, metric: Jet2, *, curvature: bool) -> dict[str, torch.Tensor]:
    g = metric.value
    ginv = torch.linalg.inv(g)
    shape = g.shape[:-2]
    dg = torch.zeros(shape + (4, 4, 4), dtype=g.dtype, device=g.device)
    ddg = torch.zeros(shape + (4, 4, 4, 4), dtype=g.dtype, device=g.device)
    dg[..., 0, :, :] = metric.first[..., :, :, 0]
    dg[..., 1, :, :] = metric.first[..., :, :, 1]
    for i in range(2):
        for j in range(2):
            ddg[..., i, j, :, :] = metric.second[..., :, :, i, j]
    dginv = -torch.einsum("...ra,...kab,...bs->...krs", ginv, dg, ginv)
    B = torch.zeros(shape + (4, 4, 4), dtype=g.dtype, device=g.device)
    dB = torch.zeros(shape + (4, 4, 4, 4), dtype=g.dtype, device=g.device)
    for s in range(4):
        for m in range(4):
            for n in range(4):
                B[..., s, m, n] = dg[..., m, s, n] + dg[..., n, s, m] - dg[..., s, m, n]
                for k in range(4):
                    dB[..., k, s, m, n] = ddg[..., k, m, s, n] + ddg[..., k, n, s, m] - ddg[..., k, s, m, n]
    gamma = 0.5 * torch.einsum("...rs,...smn->...rmn", ginv, B)
    result = {"g": g, "ginv": ginv, "gamma": gamma}
    if not curvature:
        return result
    dgamma = 0.5 * (
        torch.einsum("...krs,...smn->...krmn", dginv, B)
        + torch.einsum("...rs,...ksmn->...krmn", ginv, dB)
    )
    rup = torch.zeros(shape + (4, 4, 4, 4), dtype=g.dtype, device=g.device)
    product1 = torch.einsum("...rml,...lns->...rsmn", gamma, gamma)
    product2 = torch.einsum("...rnl,...lms->...rsmn", gamma, gamma)
    for mu in range(4):
        for nu in range(4):
            rup[..., :, :, mu, nu] = dgamma[..., mu, :, nu, :] - dgamma[..., nu, :, mu, :] + product1[..., :, :, mu, nu] - product2[..., :, :, mu, nu]
    ricci = torch.zeros(shape + (4, 4), dtype=g.dtype, device=g.device)
    for rho in range(4):
        ricci += rup[..., rho, :, rho, :]
    scalar = torch.einsum("...mn,...mn->...", ginv, ricci)
    rdown = torch.einsum("...ar,...rsmn->...asmn", g, rup)
    dual = torch.linalg.inv(E.value)
    rframe = torch.einsum("...ma,...nb,...pc,...qd,...mnpq->...abcd", dual, dual, dual, dual, rdown)
    ricci_frame = torch.einsum("...ma,...nb,...mn->...ab", dual, dual, ricci)
    signs = torch.tensor((-1.0, 1.0, 1.0, 1.0), dtype=g.dtype, device=g.device)
    kretsch = torch.einsum("a,b,c,d,...abcd,...abcd->...", signs, signs, signs, signs, rframe, rframe)
    result.update({"rup": rup, "ricci": ricci, "scalar": scalar, "rframe": rframe, "ricci_frame": ricci_frame, "kretschmann": kretsch})
    return result


def evaluate_grid(coefficients: torch.Tensor, shell: float, t: torch.Tensor, x: torch.Tensor) -> np.ndarray:
    E, q, dq = coframe_jets(coefficients, shell, t, x)
    metric = metric_jets(E)
    geo = connection_and_curvature(E, metric, curvature=True)
    g, ginv = geo["g"], geo["ginv"]
    det = torch.linalg.det(g)
    expected_det = -torch.exp(2 * q[..., 1])
    det_error = torch.abs(det - expected_det) / (1 + torch.abs(expected_det))
    dphi = torch.zeros(q.shape[:-1] + (4,), dtype=q.dtype, device=q.device)
    dphi[..., 0:2] = dq[..., 0, :]
    dphi_norm = torch.einsum("...m,...mn,...n->...", dphi, ginv, dphi)
    grad_control = torch.sum(dq[..., 0, :] ** 2, dim=-1)
    causal_scale = 1e-10 * (1 + grad_control)
    zero = grad_control <= 1e-20
    null = (~zero) & (torch.abs(dphi_norm) <= causal_scale)
    timelike = (~zero) & (~null) & (dphi_norm < 0)
    spacelike = (~zero) & (~null) & (dphi_norm > 0)
    rframe = geo["rframe"]
    t22 = rframe[..., 2, 0, 2, 0]
    t23 = 0.5 * (rframe[..., 2, 0, 3, 0] + rframe[..., 3, 0, 2, 0])
    t33 = rframe[..., 3, 0, 3, 0]
    discr = (t22 - t33) ** 2 + 4 * t23 ** 2
    tidal_scale = 1e-12 * (1 + t22 * t22 + 2 * t23 * t23 + t33 * t33)
    repeated = discr <= tidal_scale
    ricf = geo["ricci_frame"]
    mix = torch.sqrt(torch.sum(ricf[..., 0:2, 2:4] ** 2, dim=(-2, -1)) + torch.sum(ricf[..., 2:4, 0:2] ** 2, dim=(-2, -1)))
    finite_stack = torch.stack((det_error, geo["scalar"], geo["kretschmann"], mix, dphi_norm, discr), dim=-1)
    finite = torch.all(torch.isfinite(finite_stack), dim=-1)
    count = float(t.numel())

    def max_abs(value):
        return torch.amax(torch.abs(torch.nan_to_num(value, nan=0.0, posinf=0.0, neginf=0.0)), dim=1)

    features = torch.stack((
        torch.amax(torch.nan_to_num(det_error, nan=1e300, posinf=1e300, neginf=1e300), dim=1),
        max_abs(geo["scalar"]),
        torch.sqrt(torch.mean(torch.nan_to_num(geo["scalar"], nan=0.0, posinf=0.0, neginf=0.0) ** 2, dim=1)),
        max_abs(geo["kretschmann"]),
        torch.amax(torch.nan_to_num(mix, nan=0.0, posinf=1e300, neginf=1e300), dim=1),
        torch.amin(torch.nan_to_num(dphi_norm, nan=0.0, posinf=1e300, neginf=-1e300), dim=1),
        torch.amax(torch.nan_to_num(dphi_norm, nan=0.0, posinf=1e300, neginf=-1e300), dim=1),
        torch.sum(timelike, dim=1) / count,
        torch.sum(null, dim=1) / count,
        torch.sum(spacelike, dim=1) / count,
        torch.sum(zero, dim=1) / count,
        torch.sum(repeated, dim=1) / count,
        torch.amin(torch.nan_to_num(discr, nan=0.0, posinf=1e300, neginf=0.0), dim=1),
        1 - torch.sum(finite, dim=1) / count,
    ), dim=-1)
    return features.detach().cpu().numpy()


def connection_at_points(coefficients: torch.Tensor, shell: float, t: torch.Tensor, x: torch.Tensor) -> tuple[torch.Tensor, Jet2, torch.Tensor]:
    E, _, _ = coframe_jets(coefficients, shell, t, x)
    metric = metric_jets(E)
    geo = connection_and_curvature(E, metric, curvature=False)
    return geo["gamma"], E, geo["g"]


def integrate_loop(coefficients: torch.Tensor, shell: float, steps_per_side: int, reverse: bool = False) -> tuple[torch.Tensor, torch.Tensor]:
    """Parallel transport in the orthonormal coframe using midpoint exponentials.

    The frame connection is computed from the Levi-Civita coordinate connection and
    the complete coframe.  Its tiny symmetric-lowered part is retained as a numerical
    diagnostic; only its Lorentz-algebra projection is exponentiated.  This avoids the
    severe conditioning of coordinate-basis RK4 at the larger preregistered shells.
    """
    device, dtype = coefficients.device, coefficients.dtype
    vertices = [(-0.5, -0.5), (-0.5, 0.5), (0.5, 0.5), (0.5, -0.5), (-0.5, -0.5)]
    if reverse:
        vertices = list(reversed(vertices))
    stage_t, stage_x, velocities = [], [], []
    for start, end in zip(vertices[:-1], vertices[1:]):
        dt, dx = end[0] - start[0], end[1] - start[1]
        for step in range(steps_per_side):
            sm = (step + 0.5) / steps_per_side
            stage_t.append(start[0] + sm * dt)
            stage_x.append(start[1] + sm * dx)
            velocities.append((dt, dx, 0.0, 0.0))
    t = torch.tensor(stage_t, dtype=dtype, device=device)
    x = torch.tensor(stage_x, dtype=dtype, device=device)
    velocity = torch.tensor(velocities, dtype=dtype, device=device)
    gamma, E, _ = connection_at_points(coefficients, shell, t, x)
    gamma_v = torch.einsum("bprmn,pm->bprn", gamma, velocity)
    dE_v = torch.einsum("bpami,pi->bpam", E.first, velocity[..., 0:2])
    Einv = torch.linalg.inv(E.value)
    omega = torch.matmul(torch.matmul(E.value, gamma_v), Einv) - torch.matmul(dE_v, Einv)
    eta = torch.diag(torch.tensor((-1.0, 1.0, 1.0, 1.0), dtype=dtype, device=device))
    lowered = torch.matmul(eta, omega)
    symmetric = 0.5 * (lowered + lowered.transpose(-1, -2))
    antisymmetric = 0.5 * (lowered - lowered.transpose(-1, -2))
    omega_lorentz = torch.matmul(eta, antisymmetric)
    projection_error = torch.linalg.matrix_norm(symmetric, dim=(-2, -1)) / (
        1 + torch.linalg.matrix_norm(antisymmetric, dim=(-2, -1))
    )
    batch = coefficients.shape[0]
    transport = torch.eye(4, dtype=dtype, device=device).expand(batch, 4, 4).clone()
    h = 1.0 / steps_per_side
    stages = 4 * steps_per_side
    for index in range(stages):
        step_transport = torch.matrix_exp(-h * omega_lorentz[:, index])
        transport = torch.matmul(step_transport, transport)
    return transport, torch.amax(projection_error, dim=1)


def evaluate_transport(coefficients: torch.Tensor, shell: float, steps: int) -> np.ndarray:
    forward, forward_projection_error = integrate_loop(coefficients, shell, steps, reverse=False)
    reverse, reverse_projection_error = integrate_loop(coefficients, shell, steps, reverse=True)
    identity = torch.eye(4, dtype=forward.dtype, device=forward.device).expand_as(forward)
    hframe = forward
    eta = torch.diag(torch.tensor((-1.0, 1.0, 1.0, 1.0), dtype=forward.dtype, device=forward.device)).expand_as(forward)
    lorentz = torch.matmul(torch.matmul(hframe.transpose(-1, -2), eta), hframe) - eta
    lorentz_error = torch.linalg.matrix_norm(lorentz) / (1 + torch.linalg.matrix_norm(eta))
    reverse_error = torch.linalg.matrix_norm(torch.matmul(reverse, forward) - identity) / (1 + torch.linalg.matrix_norm(identity))
    deviation = torch.linalg.matrix_norm(hframe - identity)
    trace_minus = torch.diagonal(hframe, dim1=-2, dim2=-1).sum(-1) - 4
    det_minus = torch.linalg.det(hframe) - 1
    mixing = torch.sqrt(
        torch.sum(hframe[:, 0:2, 2:4] ** 2, dim=(-2, -1))
        + torch.sum(hframe[:, 2:4, 0:2] ** 2, dim=(-2, -1))
    )
    nontrivial = (deviation > 1e-8) & (deviation > 10 * reverse_error)
    projection_error = torch.maximum(forward_projection_error, reverse_projection_error)
    unresolved = (~torch.isfinite(deviation)) | (lorentz_error > 1e-7) | (reverse_error > 1e-6) | (projection_error > 1e-10)
    return torch.stack((deviation, trace_minus, det_minus, mixing, lorentz_error, reverse_error, projection_error, nontrivial.to(forward.dtype), unresolved.to(forward.dtype)), dim=-1).detach().cpu().numpy()


def coefficient_universe(count: int, seed: int) -> np.ndarray:
    power = int(round(math.log2(count)))
    if 2 ** power != count:
        raise ValueError("configurations per shell must be a power of two")
    sampler = qmc.Sobol(d=64, scramble=True, seed=seed)
    return (2 * sampler.random_base2(power) - 1).reshape(count, 8, 8).astype(np.float64)


def write_shell(outdir: Path, shell: float, coefficients: np.ndarray, features: np.ndarray) -> tuple[Path, Path]:
    tag = f"{int(round(shell * 1000)):04d}"
    npz_path = outdir / f"ATLAS_shell_{tag}_N{len(coefficients)}_T17_X33_MEXP64.npz"
    json_path = outdir / f"ATLAS_shell_{tag}_SUMMARY.json"
    if npz_path.exists() or json_path.exists():
        raise FileExistsError(f"checkpoint exists for shell {shell}")
    np.savez_compressed(npz_path, coefficients=coefficients, features=features, feature_names=np.array(FEATURE_NAMES))
    grid_unresolved = features[:, FEATURE_NAMES.index("grid_nonfinite_fraction")] > 0
    transport_unresolved = features[:, FEATURE_NAMES.index("transport_numerically_unresolved")] > 0.5
    summary = {
        "shell": shell,
        "configurations": len(coefficients),
        "grid_unresolved": int(grid_unresolved.sum()),
        "transport_unresolved": int(transport_unresolved.sum()),
        "holonomy_nontrivial": int((features[:, FEATURE_NAMES.index("holonomy_nontrivial")] > 0.5).sum()),
        "dphi_all_timelike": int((features[:, FEATURE_NAMES.index("dphi_timelike_fraction")] == 1).sum()),
        "dphi_all_spacelike": int((features[:, FEATURE_NAMES.index("dphi_spacelike_fraction")] == 1).sum()),
        "dphi_type_changing": int(((features[:, FEATURE_NAMES.index("dphi_timelike_fraction")] > 0) & (features[:, FEATURE_NAMES.index("dphi_spacelike_fraction")] > 0)).sum()),
        "tidal_repeated_somewhere": int((features[:, FEATURE_NAMES.index("tidal_repeated_fraction")] > 0).sum()),
        "feature_min": {name: float(np.nanmin(features[:, i])) for i, name in enumerate(FEATURE_NAMES)},
        "feature_median": {name: float(np.nanmedian(features[:, i])) for i, name in enumerate(FEATURE_NAMES)},
        "feature_max": {name: float(np.nanmax(features[:, i])) for i, name in enumerate(FEATURE_NAMES)},
        "npz_sha256": hashlib.sha256(npz_path.read_bytes()).hexdigest(),
    }
    json_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    return npz_path, json_path


def run_controls(device: torch.device, dtype: torch.dtype) -> dict[str, float | bool]:
    points_t = torch.linspace(-1, 1, 5, dtype=dtype, device=device)
    points_x = torch.linspace(-1, 1, 5, dtype=dtype, device=device)
    tt, xx = torch.meshgrid(points_t, points_x, indexing="ij")
    t, x = tt.reshape(-1), xx.reshape(-1)
    neutral = torch.zeros((1, 8, 8), dtype=dtype, device=device)
    neutral_grid = evaluate_grid(neutral, 1.0, t, x)[0]
    neutral_transport = evaluate_transport(neutral, 1.0, 64)[0]
    constant = torch.zeros((1, 8, 8), dtype=dtype, device=device)
    constant[0, :, 0] = torch.tensor((0.2, -0.3, 0.1, 0.15, 0.05, -0.08, 0.12, -0.04), dtype=dtype, device=device) * math.sqrt(8)
    constant_grid = evaluate_grid(constant, 1.0, t, x)[0]
    constant_transport = evaluate_transport(constant, 1.0, 64)[0]
    result = {
        "neutral_det_error": float(neutral_grid[0]),
        "neutral_scalar_abs_max": float(neutral_grid[1]),
        "neutral_kretschmann_abs_max": float(neutral_grid[3]),
        "neutral_holonomy_deviation": float(neutral_transport[0]),
        "constant_det_error": float(constant_grid[0]),
        "constant_scalar_abs_max": float(constant_grid[1]),
        "constant_kretschmann_abs_max": float(constant_grid[3]),
        "constant_holonomy_deviation": float(constant_transport[0]),
    }
    result["pass"] = all(result[key] < 1e-10 for key in result if key != "pass")
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--configs-per-shell", type=int, default=1024)
    parser.add_argument("--shells", type=float, nargs="+", default=[0.03, 0.1, 0.3, 1.0, 2.5])
    parser.add_argument("--grid-t", type=int, default=17)
    parser.add_argument("--grid-x", type=int, default=33)
    parser.add_argument("--rk4", type=int, default=64)
    parser.add_argument("--batch", type=int, default=64)
    parser.add_argument("--seed", type=int, default=20260727)
    parser.add_argument("--device", default="cuda:0")
    parser.add_argument("--production", action="store_true")
    args = parser.parse_args()
    if args.production:
        expected = (args.configs_per_shell, args.shells, args.grid_t, args.grid_x, args.rk4, args.batch, args.seed, args.device)
        registered = (1024, [0.03, 0.1, 0.3, 1.0, 2.5], 17, 33, 64, 64, 20260727, "cuda:0")
        if expected != registered:
            raise SystemExit("production arguments differ from preregistration")
    outdir = args.output_dir.resolve()
    outdir.mkdir(parents=True, exist_ok=True)
    if args.production and any(outdir.glob("ATLAS_shell_*")):
        raise FileExistsError("production checkpoint already exists")
    device = torch.device(args.device)
    if device.type == "cuda" and not torch.cuda.is_available():
        raise RuntimeError("CUDA requested but unavailable")
    dtype = torch.float64
    torch.set_default_dtype(dtype)
    start = time.time()
    controls = run_controls(device, dtype)
    if not controls["pass"]:
        raise AssertionError(controls)
    coefficients = coefficient_universe(args.configs_per_shell, args.seed)
    universe_hash = hashlib.sha256(coefficients.tobytes()).hexdigest()
    t_axis = torch.linspace(-1, 1, args.grid_t, dtype=dtype, device=device)
    x_axis = torch.linspace(-1, 1, args.grid_x, dtype=dtype, device=device)
    tt, xx = torch.meshgrid(t_axis, x_axis, indexing="ij")
    t_grid, x_grid = tt.reshape(-1), xx.reshape(-1)
    summaries = []
    anchor_payload = None
    convergence_payload = None
    peak_memory = 0
    for shell in args.shells:
        all_features = []
        for start_index in range(0, args.configs_per_shell, args.batch):
            stop_index = min(start_index + args.batch, args.configs_per_shell)
            coeff = torch.tensor(coefficients[start_index:stop_index], dtype=dtype, device=device)
            grid_features = evaluate_grid(coeff, shell, t_grid, x_grid)
            transport_features = evaluate_transport(coeff, shell, args.rk4)
            combined = np.concatenate((grid_features, transport_features), axis=1)
            all_features.append(combined)
            if device.type == "cuda":
                peak_memory = max(peak_memory, torch.cuda.max_memory_allocated(device))
            if shell == 0.3 and start_index == 0:
                anchor_t = torch.tensor((-0.37, 0.11, 0.44), dtype=dtype, device=device)
                anchor_x = torch.tensor((0.19, -0.43, 0.53), dtype=dtype, device=device)
                anchor_count = min(32, coeff.shape[0])
                anchor_coeff = coeff[:anchor_count]
                E, q, dq = coframe_jets(anchor_coeff, shell, anchor_t, anchor_x)
                metric = metric_jets(E)
                geo = connection_and_curvature(E, metric, curvature=True)
                dphi = torch.zeros((anchor_count, 3, 4), dtype=dtype, device=device)
                dphi[..., 0:2] = dq[..., 0, :]
                dphi_norm = torch.einsum("...m,...mn,...n->...", dphi, geo["ginv"], dphi)
                anchor_payload = {
                    "shell": shell,
                    "indices": list(range(anchor_count)),
                    "points": [[float(a), float(b)] for a, b in zip(anchor_t.cpu(), anchor_x.cpu())],
                    "coefficients": anchor_coeff.detach().cpu().tolist(),
                    "metric": geo["g"].detach().cpu().tolist(),
                    "scalar": geo["scalar"].detach().cpu().tolist(),
                    "dphi_norm": dphi_norm.detach().cpu().tolist(),
                }
        features = np.concatenate(all_features, axis=0)
        npz_path, summary_path = write_shell(outdir, shell, coefficients, features)
        summary = json.loads(summary_path.read_text())
        summaries.append(summary)
        if summary["grid_unresolved"] > 0.25 * args.configs_per_shell:
            raise RuntimeError(f"local grid unresolved threshold exceeded at shell {shell}")
        if shell == 1.0:
            convergence_count = min(32, len(coefficients))
            coeff = torch.tensor(coefficients[:convergence_count], dtype=dtype, device=device)
            p32, _ = integrate_loop(coeff, shell, 32, reverse=False)
            p64, _ = integrate_loop(coeff, shell, 64, reverse=False)
            p128, _ = integrate_loop(coeff, shell, 128, reverse=False)
            e32 = torch.linalg.matrix_norm(p32 - p64, dim=(-2, -1))
            e64 = torch.linalg.matrix_norm(p64 - p128, dim=(-2, -1))
            ratio = e32 / torch.clamp(e64, min=1e-30)
            convergence_payload = {
                "shell": shell,
                "indices": list(range(convergence_count)),
                "error_32_64": e32.detach().cpu().tolist(),
                "error_64_128": e64.detach().cpu().tolist(),
                "ratio": ratio.detach().cpu().tolist(),
                "median_ratio": float(torch.median(ratio).cpu()),
                "all_errors_reduced": bool(torch.all(e64 < e32).cpu()),
            }
    if anchor_payload is None or convergence_payload is None:
        raise AssertionError("registered anchor or convergence shell missing")
    (outdir / "CPU_ANCHOR_GPU.json").write_text(json.dumps(anchor_payload, indent=2, sort_keys=True) + "\n")
    (outdir / "TRANSPORT_CONVERGENCE.json").write_text(json.dumps(convergence_payload, indent=2, sort_keys=True) + "\n")
    total_grid_unresolved = sum(row["grid_unresolved"] for row in summaries)
    total_transport_unresolved = sum(row["transport_unresolved"] for row in summaries)
    final = {
        "schema": "udt-complete-coframe-metric-telescope-p01-result-1.0",
        "status": "PASS",
        "epistemic_scope": "OFF_SHELL_CONFIGURATION_ATLAS_NOT_DYNAMICAL_SOLUTIONS",
        "controls": controls,
        "coefficient_universe_sha256": universe_hash,
        "amplitudes": list(AMPLITUDES),
        "feature_names": list(FEATURE_NAMES),
        "shell_summaries": summaries,
        "totals": {
            "production_configurations": len(args.shells) * args.configs_per_shell,
            "grid_unresolved": total_grid_unresolved,
            "transport_unresolved": total_transport_unresolved,
            "holonomy_nontrivial": sum(row["holonomy_nontrivial"] for row in summaries),
            "dphi_type_changing": sum(row["dphi_type_changing"] for row in summaries),
            "tidal_repeated_somewhere": sum(row["tidal_repeated_somewhere"] for row in summaries),
        },
        "transport_convergence": {
            "all_errors_reduced": convergence_payload["all_errors_reduced"],
            "median_ratio": convergence_payload["median_ratio"],
        },
        "environment": {
            "python": platform.python_version(),
            "torch": torch.__version__,
            "scipy": __import__("scipy").__version__,
            "device": torch.cuda.get_device_name(device) if device.type == "cuda" else str(device),
            "dtype": "float64",
            "peak_memory_bytes": peak_memory,
            "wall_seconds": time.time() - start,
            "pid": os.getpid(),
        },
        "maximum_conclusion": "BOUNDED_COMPLETE_COFRAME_CONFIGURATIONS_AND_THEIR_PATHWISE_GEOMETRY_CLASSIFIED_WITHOUT_BACKGROUND_DYNAMICS_OR_PHYSICAL_SELECTION",
    }
    (outdir / "ATLAS_RESULT.json").write_text(json.dumps(final, indent=2, sort_keys=True) + "\n")
    print(json.dumps(final, sort_keys=True))


if __name__ == "__main__":
    main()
