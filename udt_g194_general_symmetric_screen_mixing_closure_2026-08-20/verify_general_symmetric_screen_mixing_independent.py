#!/usr/bin/env python3
"""Independent two-leg metric-jet and matrix-IVP replay for G194.

This verifier does not import the production module or read its artifact.  It
uses Torch automatic differentiation to spot-check metric jets and
Riemann curvature.  A separate formula-driven SciPy DOP853 leg compares the
direct Jacobi IVP with an independently integrated ordered representation.
It is not a metric-derived tide evaluation at every adaptive IVP call.
"""

from __future__ import annotations

import json
import math
import os
import random
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path

# Dill asks only for a resolved temp path during the initial Torch import.  In
# a genuinely read-only replay, pinning tempfile.tempdir bypasses its writable
# discovery probe.  The write-triggering torch.func.jacfwd dependency path is
# not used below, and the package verifier proves this directory stays empty.
if (
    os.environ.get("G194_NO_WRITE") == "1"
    and os.environ.get("G194_REVIEW_RUNTIME_REQUIRED") == "1"
):
    raw_runtime = os.environ.get("TMPDIR")
    if not raw_runtime:
        raise SystemExit("sealed replay requires TMPDIR before Torch import")
    runtime = Path(raw_runtime)
    if not runtime.is_absolute():
        runtime = Path.cwd() / runtime
    runtime = runtime.resolve()
    expected_runtime = (Path.cwd() / ".review_runtime").resolve()
    if runtime != expected_runtime or not runtime.is_dir() or list(runtime.iterdir()):
        raise SystemExit(f"invalid sealed replay runtime before Torch import: {runtime}")
    tempfile.tempdir = str(runtime)

import numpy as np
import torch
from scipy.integrate import solve_ivp


torch.set_default_dtype(torch.float64)
DTYPE = torch.float64
LORENTZ = torch.diag(torch.tensor([-1.0, 1.0, 1.0, 1.0], dtype=DTYPE))
ETA_FORWARD = 0.65
ETA_BACKWARD = -0.35
CURVATURE_POINTS = (-0.23, 0.11, 0.47)
TENSOR_CEILING = 2.0e-8
ALGEBRA_CEILING = 2.0e-10
SEED = 1940820


@dataclass(frozen=True)
class ScalarSeries:
    c0: float
    c1: float
    c2: float
    sin_amp: float
    cos_amp: float
    frequency: float

    def torch_value(self, value):
        return (
            self.c0
            + self.c1 * value
            + self.c2 * value * value
            + self.sin_amp * torch.sin(self.frequency * value)
            + self.cos_amp * (torch.cos(self.frequency * value) - 1.0)
        )

    def value_derivatives(self, value):
        omega = self.frequency
        scalar = (
            self.c0
            + self.c1 * value
            + self.c2 * value * value
            + self.sin_amp * math.sin(omega * value)
            + self.cos_amp * (math.cos(omega * value) - 1.0)
        )
        first = (
            self.c1
            + 2.0 * self.c2 * value
            + self.sin_amp * omega * math.cos(omega * value)
            - self.cos_amp * omega * math.sin(omega * value)
        )
        second = (
            2.0 * self.c2
            - self.sin_amp * omega * omega * math.sin(omega * value)
            - self.cos_amp * omega * omega * math.cos(omega * value)
        )
        return scalar, first, second


@dataclass(frozen=True)
class Profile:
    name: str
    log_scale: ScalarSeries
    entry_a: ScalarSeries
    entry_n: ScalarSeries
    entry_b: ScalarSeries

    def torch_values(self, eta):
        scale = torch.exp(self.log_scale.torch_value(eta))
        return (
            scale,
            self.entry_a.torch_value(eta),
            self.entry_n.torch_value(eta),
            self.entry_b.torch_value(eta),
        )

    def values(self, eta):
        log_a, dlog_a, ddlog_a = self.log_scale.value_derivatives(eta)
        scale = math.exp(log_a)
        dscale = scale * dlog_a
        ddscale = scale * (ddlog_a + dlog_a * dlog_a)
        entry_a, dentry_a, _ = self.entry_a.value_derivatives(eta)
        entry_n, dentry_n, _ = self.entry_n.value_derivatives(eta)
        entry_b, dentry_b, _ = self.entry_b.value_derivatives(eta)
        return (
            scale,
            dscale,
            ddscale,
            entry_a,
            dentry_a,
            entry_n,
            dentry_n,
            entry_b,
            dentry_b,
        )


def series(c0=0.0, c1=0.0, c2=0.0, sin_amp=0.0, cos_amp=0.0, frequency=1.0):
    return ScalarSeries(c0, c1, c2, sin_amp, cos_amp, frequency)


def named_profiles():
    return [
        Profile(
            "g193_limit",
            series(c1=0.12, c2=-0.04, sin_amp=0.03, frequency=2.0),
            series(c0=0.25, c1=-0.13, sin_amp=0.05, frequency=1.5),
            series(c0=-0.11, c1=0.19, c2=0.04),
            series(),
        ),
        Profile(
            "g192_limit",
            series(c1=0.10, c2=0.03),
            series(c0=0.18, c1=-0.09, sin_amp=0.04, frequency=1.5),
            series(),
            series(),
        ),
        Profile("conformal_limit", series(c1=0.16, c2=0.05), series(), series(), series()),
        Profile(
            "scalar_trace",
            series(c1=-0.04, c2=0.06),
            series(c0=0.13, c1=0.08),
            series(),
            series(c0=0.13, c1=0.08),
        ),
        Profile(
            "diagonal_unequal",
            series(c1=0.07),
            series(c0=0.18, c1=-0.05),
            series(),
            series(c0=-0.09, c1=0.17, c2=-0.03),
        ),
        Profile(
            "constant_full_rank",
            series(c1=0.10),
            series(c0=0.21),
            series(c0=-0.14),
            series(c0=-0.08),
        ),
        Profile(
            "noncommuting_rotating_axes",
            series(c1=0.08, sin_amp=0.02, frequency=2.0),
            series(c0=0.10, c1=0.17),
            series(c0=0.19, c2=-0.11),
            series(c0=-0.07, c1=-0.13, sin_amp=0.06, frequency=2.0),
        ),
        Profile(
            "rank_transition",
            series(c1=-0.06, c2=0.08),
            series(c0=0.20),
            series(c0=0.10, c1=0.30),
            series(c0=0.10),
        ),
        Profile(
            "signed_triple_crossing",
            series(c1=0.04),
            series(c1=0.38),
            series(c0=-0.03, c1=0.29),
            series(c0=0.02, c1=-0.33),
        ),
        Profile(
            "frequency_turn",
            series(c1=0.25, c2=-0.40),
            series(c0=-0.12, sin_amp=0.08, frequency=2.0),
            series(c0=0.09, c1=-0.16),
            series(c0=0.15, c2=-0.09),
        ),
        Profile(
            "near_singular_regular",
            series(c2=-4.0),
            series(c0=0.22, c1=0.07),
            series(c0=-0.18, c1=0.09),
            series(c0=0.16, c1=-0.11),
        ),
    ]


def random_profiles():
    generator = random.Random(SEED)
    profiles = []
    for index in range(256):
        log_scale = series(
            c1=generator.uniform(-0.25, 0.25),
            c2=generator.uniform(-0.20, 0.20),
            sin_amp=generator.uniform(-0.08, 0.08),
            cos_amp=generator.uniform(-0.05, 0.05),
            frequency=float(generator.choice((1, 2, 3))),
        )

        def random_entry():
            return series(
                c0=generator.uniform(-0.25, 0.25),
                c1=generator.uniform(-0.25, 0.25),
                c2=generator.uniform(-0.12, 0.12),
                sin_amp=generator.uniform(-0.10, 0.10),
                cos_amp=generator.uniform(-0.10, 0.10),
                frequency=float(generator.choice((1, 2, 3))),
            )

        profiles.append(
            Profile(f"random_{index:03d}", log_scale, random_entry(), random_entry(), random_entry())
        )
    return profiles


def coframe_metric(profile, point):
    eta, _, p_value, w_value = point
    scale, entry_a, entry_n, entry_b = profile.torch_values(eta)
    shift_0 = entry_a * p_value + entry_n * w_value
    shift_1 = entry_n * p_value + entry_b * w_value
    zero = eta * 0.0
    one = zero + 1.0
    coframe = scale * torch.stack(
        [
            torch.stack((one, zero, zero, zero)),
            torch.stack((zero, one, zero, zero)),
            torch.stack((shift_0, shift_0, one, zero)),
            torch.stack((shift_1, shift_1, zero, one)),
        ]
    )
    return coframe.T @ LORENTZ @ coframe


def metric_jets(profile, eta_value):
    point = torch.tensor([eta_value, eta_value, 0.0, 0.0], dtype=DTYPE)
    metric_function = lambda argument: coframe_metric(profile, argument)
    metric = metric_function(point)
    first = torch.autograd.functional.jacobian(
        metric_function,
        point,
        create_graph=False,
        strict=False,
        vectorize=False,
        strategy="reverse-mode",
    )

    def differentiable_first(argument):
        return torch.autograd.functional.jacobian(
            metric_function,
            argument,
            create_graph=True,
            strict=False,
            vectorize=False,
            strategy="reverse-mode",
        )

    second = torch.autograd.functional.jacobian(
        differentiable_first,
        point,
        create_graph=False,
        strict=False,
        vectorize=False,
        strategy="reverse-mode",
    )
    return metric.detach().numpy(), first.detach().numpy(), second.detach().numpy()


def curvature_from_jets(metric, first, second):
    inverse = np.linalg.inv(metric)
    gamma = np.zeros((4, 4, 4), dtype=float)
    for aa in range(4):
        for bb in range(4):
            for cc in range(4):
                gamma[aa, bb, cc] = 0.5 * sum(
                    inverse[aa, dd]
                    * (first[dd, cc, bb] + first[dd, bb, cc] - first[bb, cc, dd])
                    for dd in range(4)
                )

    inverse_derivative = np.zeros((4, 4, 4), dtype=float)
    for aa in range(4):
        for dd in range(4):
            for ee in range(4):
                inverse_derivative[aa, dd, ee] = -sum(
                    inverse[aa, pp] * first[pp, qq, ee] * inverse[qq, dd]
                    for pp in range(4)
                    for qq in range(4)
                )

    gamma_derivative = np.zeros((4, 4, 4, 4), dtype=float)
    for aa in range(4):
        for bb in range(4):
            for cc in range(4):
                for ee in range(4):
                    first_term = sum(
                        inverse_derivative[aa, dd, ee]
                        * (first[dd, cc, bb] + first[dd, bb, cc] - first[bb, cc, dd])
                        for dd in range(4)
                    )
                    second_term = sum(
                        inverse[aa, dd]
                        * (
                            second[dd, cc, bb, ee]
                            + second[dd, bb, cc, ee]
                            - second[bb, cc, dd, ee]
                        )
                        for dd in range(4)
                    )
                    gamma_derivative[aa, bb, cc, ee] = 0.5 * (first_term + second_term)

    riemann = np.zeros((4, 4, 4, 4), dtype=float)
    for aa in range(4):
        for bb in range(4):
            for cc in range(4):
                for dd in range(4):
                    riemann[aa, bb, cc, dd] = (
                        gamma_derivative[aa, dd, bb, cc]
                        - gamma_derivative[aa, cc, bb, dd]
                        + sum(
                            gamma[aa, cc, ee] * gamma[ee, dd, bb]
                            - gamma[aa, dd, ee] * gamma[ee, cc, bb]
                            for ee in range(4)
                        )
                    )
    return riemann


def tide_from_metric(profile, eta_value):
    metric, first, second = metric_jets(profile, eta_value)
    riemann = curvature_from_jets(metric, first, second)
    scale = profile.values(eta_value)[0]
    ray = np.array([scale**-2, scale**-2, 0.0, 0.0])
    screens = (
        np.array([0.0, 0.0, scale**-1, 0.0]),
        np.array([0.0, 0.0, 0.0, scale**-1]),
    )
    tide = np.zeros((2, 2), dtype=float)
    for left_index, left in enumerate(screens):
        for right_index, right in enumerate(screens):
            curvature_vector = np.zeros(4, dtype=float)
            for aa in range(4):
                curvature_vector[aa] = sum(
                    riemann[aa, bb, cc, dd] * ray[bb] * right[cc] * ray[dd]
                    for bb in (0, 1)
                    for cc in (2, 3)
                    for dd in (0, 1)
                )
            tide[left_index, right_index] = left @ metric @ curvature_vector
    return tide, metric


def candidate_matrices(profile, eta_value):
    values = profile.values(eta_value)
    scale, dscale, ddscale = values[:3]
    entry_a, dentry_a, entry_n, dentry_n, entry_b, dentry_b = values[3:]
    mix = np.array([[entry_a, entry_n], [entry_n, entry_b]])
    dmix = np.array([[dentry_a, dentry_n], [dentry_n, dentry_b]])
    hubble = dscale / scale
    dhubble = ddscale / scale - hubble * hubble
    isotropic = (hubble * hubble - dhubble) / scale**4
    tide = isotropic * np.eye(2) + (2.0 * dmix - 4.0 * mix @ mix) / scale**4
    return scale, dscale, mix, tide


def integrate_profile(profile, endpoint):
    initial = np.concatenate((np.zeros(4), np.eye(2).reshape(-1), np.eye(2).reshape(-1), np.zeros(4)))

    def right_hand_side(eta_value, state):
        direct = state[0:4].reshape(2, 2)
        velocity = state[4:8].reshape(2, 2)
        fundamental = state[8:12].reshape(2, 2)
        scale, _, mix, tide = candidate_matrices(profile, eta_value)
        inverse_fundamental = np.linalg.inv(fundamental)
        return np.concatenate(
            (
                (scale * scale * velocity).reshape(-1),
                (-scale * scale * tide @ direct).reshape(-1),
                (-2.0 * mix @ fundamental).reshape(-1),
                (inverse_fundamental @ inverse_fundamental.T).reshape(-1),
            )
        )

    sample = np.linspace(0.0, endpoint, 25)
    solution = solve_ivp(
        right_hand_side,
        (0.0, endpoint),
        initial,
        method="DOP853",
        t_eval=sample,
        rtol=2.0e-12,
        atol=2.0e-13,
    )
    if not solution.success:
        raise RuntimeError(f"{profile.name}: {solution.message}")

    max_factor_error = 0.0
    min_nonvertex_determinant = math.inf
    max_wronskian_residual = 0.0
    endpoint_direct = None
    for column, eta_value in enumerate(solution.t):
        state = solution.y[:, column]
        direct = state[0:4].reshape(2, 2)
        velocity = state[4:8].reshape(2, 2)
        fundamental = state[8:12].reshape(2, 2)
        integral = state[12:16].reshape(2, 2)
        scale = candidate_matrices(profile, float(eta_value))[0]
        represented = scale * fundamental @ integral
        max_factor_error = max(max_factor_error, float(np.max(np.abs(direct - represented))))
        wronskian = direct.T @ velocity - velocity.T @ direct
        max_wronskian_residual = max(
            max_wronskian_residual, float(np.max(np.abs(wronskian)))
        )
        if abs(float(eta_value)) > 1.0e-12:
            min_nonvertex_determinant = min(
                min_nonvertex_determinant, float(np.linalg.det(direct))
            )
        endpoint_direct = direct.copy()
    return max_factor_error, max_wronskian_residual, min_nonvertex_determinant, endpoint_direct


def verify_profile(profile):
    max_tide_error = 0.0
    max_symmetry_error = 0.0
    max_frame_error = 0.0
    assertion_count = 0
    minimum_scale = math.inf

    for eta_value in CURVATURE_POINTS:
        reconstructed, metric = tide_from_metric(profile, eta_value)
        scale, _, _, candidate = candidate_matrices(profile, eta_value)
        max_tide_error = max(max_tide_error, float(np.max(np.abs(reconstructed - candidate))))
        max_symmetry_error = max(
            max_symmetry_error, float(np.max(np.abs(reconstructed - reconstructed.T)))
        )
        central_expected = np.diag([-scale * scale, scale * scale, scale * scale, scale * scale])
        max_frame_error = max(max_frame_error, float(np.max(np.abs(metric - central_expected))))
        minimum_scale = min(minimum_scale, scale)
        assertion_count += 3

    forward = integrate_profile(profile, ETA_FORWARD)
    backward = integrate_profile(profile, ETA_BACKWARD)
    max_factor_error = max(forward[0], backward[0])
    max_wronskian_residual = max(forward[1], backward[1])
    minimum_determinant = min(forward[2], backward[2])
    assertion_count += 6

    if max_tide_error > TENSOR_CEILING:
        raise AssertionError(f"{profile.name}: tide error {max_tide_error}")
    if max_symmetry_error > ALGEBRA_CEILING:
        raise AssertionError(f"{profile.name}: asymmetry {max_symmetry_error}")
    if max_frame_error > ALGEBRA_CEILING:
        raise AssertionError(f"{profile.name}: frame error {max_frame_error}")
    if max_factor_error > TENSOR_CEILING:
        raise AssertionError(f"{profile.name}: factor error {max_factor_error}")
    if max_wronskian_residual > TENSOR_CEILING:
        raise AssertionError(f"{profile.name}: Wronskian error {max_wronskian_residual}")
    if minimum_determinant <= 0.0:
        raise AssertionError(f"{profile.name}: determinant {minimum_determinant}")

    result = {
        "name": profile.name,
        "max_tide_error": max_tide_error,
        "max_tide_asymmetry": max_symmetry_error,
        "max_central_frame_error": max_frame_error,
        "max_factorization_error": max_factor_error,
        "max_wronskian_error": max_wronskian_residual,
        "minimum_sampled_nonvertex_determinant": minimum_determinant,
        "minimum_sampled_scale": minimum_scale,
        "assertions": assertion_count,
    }
    if not profile.name.startswith("random_"):
        endpoint = forward[3]
        result["forward_endpoint_jacobi"] = endpoint.tolist()
        result["forward_cross_asymmetry"] = float(endpoint[0, 1] - endpoint[1, 0])
        result["forward_polar_rotation_angle"] = math.atan2(
            float(endpoint[1, 0] - endpoint[0, 1]),
            float(endpoint[0, 0] + endpoint[1, 1]),
        )
    return result


def commutator_gate(profile):
    left = candidate_matrices(profile, -0.21)[2]
    right = candidate_matrices(profile, 0.43)[2]
    return float(np.linalg.norm(left @ right - right @ left))


def rank_transition_gate(profile):
    left = np.linalg.det(candidate_matrices(profile, -0.40)[2])
    right = np.linalg.det(candidate_matrices(profile, 0.40)[2])
    return float(left), float(right)


def main():
    profiles = named_profiles() + random_profiles()
    results = []
    for index, profile in enumerate(profiles):
        results.append(verify_profile(profile))
        if (index + 1) % 32 == 0:
            print(
                f"G194 independent replay: {index + 1}/{len(profiles)}",
                file=sys.stderr,
                flush=True,
            )

    named = {profile.name: profile for profile in profiles if not profile.name.startswith("random_")}
    commutator_norm = commutator_gate(named["noncommuting_rotating_axes"])
    if commutator_norm <= 1.0e-4:
        raise AssertionError(f"noncommuting census gate inactive: {commutator_norm}")
    rank_left, rank_right = rank_transition_gate(named["rank_transition"])
    if rank_left * rank_right >= 0.0:
        raise AssertionError(f"rank-transition gate inactive: {rank_left}, {rank_right}")

    summary = {
        "status": "PASS",
        "landing": "GENERAL_SYMMETRIC_MATRIX_FACTORIZATION_AND_NO_CAUSTIC_CLOSE",
        "implementation": (
            "independent Torch-autodiff metric-jet/Riemann reconstruction plus SciPy DOP853 "
            "matrix IVPs; "
            "no production import or artifact read"
        ),
        "independence_grade": (
            "METRIC_JET_RIEMANN_SPOTCHECK_PLUS_FORMULA_DRIVEN_MATRIX_IVP"
        ),
        "seed": SEED,
        "history_count": len(results),
        "assertion_count": sum(item["assertions"] for item in results) + 2,
        "named_history_count": len(named_profiles()),
        "random_history_count": len(random_profiles()),
        "noncommuting_control_commutator_norm": commutator_norm,
        "rank_transition_determinants": [rank_left, rank_right],
        "max_tide_error": max(item["max_tide_error"] for item in results),
        "max_tide_asymmetry": max(item["max_tide_asymmetry"] for item in results),
        "max_central_frame_error": max(item["max_central_frame_error"] for item in results),
        "max_factorization_error": max(item["max_factorization_error"] for item in results),
        "max_wronskian_error": max(item["max_wronskian_error"] for item in results),
        "minimum_sampled_nonvertex_determinant": min(
            item["minimum_sampled_nonvertex_determinant"] for item in results
        ),
        "minimum_sampled_scale": min(item["minimum_sampled_scale"] for item in results),
        "ceilings": {"tensor": TENSOR_CEILING, "algebra": ALGEBRA_CEILING},
        "profiles": results,
    }
    payload = json.dumps(summary, indent=2, sort_keys=True) + "\n"
    if os.environ.get("G194_NO_WRITE") == "1":
        print(payload, end="")
        return
    Path(__file__).with_name("INDEPENDENT_VERIFICATION.json").write_text(
        payload, encoding="utf-8"
    )
    print(payload, end="")


if __name__ == "__main__":
    main()
