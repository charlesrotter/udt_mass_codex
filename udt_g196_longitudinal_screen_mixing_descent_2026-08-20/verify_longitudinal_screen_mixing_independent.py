#!/usr/bin/env python3
"""Independent Torch/SciPy verification of the preregistered G196 family."""

from __future__ import annotations

import json
import math
import os
import sys
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import torch
from scipy.integrate import solve_ivp


DTYPE = torch.float64
LORENTZ = torch.diag(torch.tensor([-1.0, 1.0, 1.0, 1.0], dtype=DTYPE))
SEED = 1960820
TENSOR_CEILING = 3.0e-8
ALGEBRA_CEILING = 3.0e-10
CURVATURE_POINTS = ((-0.23, -0.31), (0.11, 0.29), (0.47, 0.18))
ETA_FORWARD = 0.62
ETA_BACKWARD = -0.34
RAY_OFFSETS = (-0.17, 0.0, 0.21)
RANDOM_COUNT = 192


@dataclass(frozen=True)
class LogScale:
    linear: float = 0.0
    quadratic: float = 0.0
    amplitude: float = 0.0
    frequency: float = 1.0
    phase: float = 0.0

    def torch_value(self, eta):
        log_value = (
            self.linear * eta
            + self.quadratic * eta * eta
            + self.amplitude
            * (torch.sin(self.frequency * eta + self.phase) - math.sin(self.phase))
        )
        return torch.exp(log_value)

    def values(self, eta):
        argument = self.frequency * eta + self.phase
        log_value = (
            self.linear * eta
            + self.quadratic * eta * eta
            + self.amplitude * (math.sin(argument) - math.sin(self.phase))
        )
        dlog = (
            self.linear
            + 2.0 * self.quadratic * eta
            + self.amplitude * self.frequency * math.cos(argument)
        )
        ddlog = (
            2.0 * self.quadratic
            - self.amplitude * self.frequency * self.frequency * math.sin(argument)
        )
        scale = math.exp(log_value)
        return scale, scale * dlog, scale * (ddlog + dlog * dlog)


@dataclass(frozen=True)
class Surface:
    constant: float = 0.0
    eta_linear: float = 0.0
    z_linear: float = 0.0
    eta_quadratic: float = 0.0
    z_quadratic: float = 0.0
    cross: float = 0.0
    amplitude: float = 0.0
    eta_frequency: float = 1.0
    z_frequency: float = 1.0
    phase: float = 0.0

    def torch_value(self, eta, z):
        argument = self.eta_frequency * eta + self.z_frequency * z + self.phase
        return (
            self.constant
            + self.eta_linear * eta
            + self.z_linear * z
            + self.eta_quadratic * eta * eta
            + self.z_quadratic * z * z
            + self.cross * eta * z
            + self.amplitude * torch.sin(argument)
        )

    def values(self, eta, z):
        argument = self.eta_frequency * eta + self.z_frequency * z + self.phase
        sine = math.sin(argument)
        cosine = math.cos(argument)
        value = (
            self.constant
            + self.eta_linear * eta
            + self.z_linear * z
            + self.eta_quadratic * eta * eta
            + self.z_quadratic * z * z
            + self.cross * eta * z
            + self.amplitude * sine
        )
        d_eta = (
            self.eta_linear
            + 2.0 * self.eta_quadratic * eta
            + self.cross * z
            + self.amplitude * self.eta_frequency * cosine
        )
        d_z = (
            self.z_linear
            + 2.0 * self.z_quadratic * z
            + self.cross * eta
            + self.amplitude * self.z_frequency * cosine
        )
        mixed = self.cross - (
            self.amplitude * self.eta_frequency * self.z_frequency * sine
        )
        return value, d_eta, d_z, mixed


ZERO = Surface()


@dataclass(frozen=True)
class Profile:
    name: str
    scale: LogScale
    entry_a: Surface
    entry_n: Surface
    entry_b: Surface
    rotation_r: Surface
    ray_offset: float = 0.0

    def torch_values(self, eta, z):
        return (
            self.scale.torch_value(eta),
            self.entry_a.torch_value(eta, z),
            self.entry_n.torch_value(eta, z),
            self.entry_b.torch_value(eta, z),
            self.rotation_r.torch_value(eta, z),
        )


def surface(**kwargs):
    return Surface(**kwargs)


def named_profiles():
    mild_scale = LogScale(0.08, -0.025, 0.018, 1.4, 0.2)
    return [
        Profile("zero_mixing", LogScale(0.04, 0.01), ZERO, ZERO, ZERO, ZERO),
        Profile(
            "z_independent_g195_limit",
            mild_scale,
            surface(constant=0.05, eta_linear=0.08, eta_quadratic=-0.02),
            surface(constant=-0.03, eta_linear=0.04, amplitude=0.02, z_frequency=0.0),
            surface(constant=0.02, eta_linear=-0.06),
            surface(constant=0.01, eta_linear=0.05),
        ),
        Profile(
            "pure_longitudinal_gradient",
            mild_scale,
            surface(z_linear=0.11, z_quadratic=-0.025),
            surface(z_linear=-0.07, amplitude=0.018, eta_frequency=0.0, z_frequency=1.7),
            surface(z_linear=0.04, z_quadratic=0.018),
            ZERO,
            0.21,
        ),
        Profile(
            "eta_minus_z_field",
            LogScale(-0.03, 0.012),
            surface(eta_linear=0.09, z_linear=-0.09, eta_quadratic=0.04,
                    z_quadratic=0.04, cross=-0.08),
            surface(amplitude=0.03, eta_frequency=1.2, z_frequency=-1.2),
            surface(eta_linear=-0.05, z_linear=0.05),
            ZERO,
            -0.17,
        ),
        Profile(
            "pure_rotation_spacetime",
            mild_scale,
            ZERO,
            ZERO,
            ZERO,
            surface(constant=0.08, eta_linear=0.06, z_linear=-0.04, cross=0.03,
                    amplitude=0.02, eta_frequency=1.3, z_frequency=0.8),
        ),
        Profile(
            "fully_noncommuting",
            LogScale(0.06, -0.018, 0.012, 1.8, -0.1),
            surface(constant=0.16, eta_linear=0.05, z_linear=-0.03, cross=0.025),
            surface(constant=-0.07, eta_linear=0.04, z_linear=0.06, amplitude=0.02,
                    eta_frequency=1.1, z_frequency=1.6),
            surface(constant=-0.10, eta_linear=-0.02, z_linear=0.05, cross=-0.02),
            surface(constant=0.11, eta_linear=-0.06, z_linear=0.03),
            0.21,
        ),
        Profile(
            "rank_transition",
            LogScale(),
            surface(eta_linear=1.0, z_linear=1.0),
            ZERO,
            surface(constant=1.0),
            ZERO,
        ),
        Profile(
            "rotation_zero_crossing",
            LogScale(0.02),
            surface(constant=0.04),
            surface(constant=0.02),
            surface(constant=-0.03),
            surface(eta_linear=0.7, z_linear=0.7),
        ),
        Profile(
            "mixed_eta_z_cross",
            LogScale(-0.05, 0.02),
            surface(cross=0.12, eta_quadratic=-0.03, z_quadratic=0.02),
            surface(cross=-0.08, amplitude=0.025, eta_frequency=1.5, z_frequency=0.9),
            surface(cross=0.06, eta_linear=0.03, z_linear=-0.04),
            surface(cross=0.05, eta_linear=-0.02, z_linear=0.03),
            -0.17,
        ),
        Profile(
            "large_but_regular",
            LogScale(0.10, -0.03, 0.025, 2.1, 0.3),
            surface(constant=0.42, eta_linear=-0.18, z_linear=0.15, cross=0.08),
            surface(constant=-0.31, eta_linear=0.16, z_linear=0.12, cross=-0.06),
            surface(constant=0.27, eta_linear=0.11, z_linear=-0.17, cross=0.07),
            surface(constant=0.24, eta_linear=-0.10, z_linear=0.13, cross=0.04),
            0.21,
        ),
        Profile(
            "same_ray_base",
            mild_scale,
            surface(constant=0.07, eta_linear=0.04, z_linear=0.03),
            surface(constant=-0.02, cross=0.015),
            surface(constant=0.05, eta_linear=-0.03, z_linear=0.02),
            surface(constant=0.04, eta_linear=0.02, z_linear=-0.01),
        ),
        Profile(
            "same_ray_offray_alias",
            mild_scale,
            surface(constant=0.07, eta_linear=0.04, z_linear=0.03,
                    eta_quadratic=0.7, z_quadratic=0.7, cross=-1.4),
            surface(constant=-0.02, cross=0.015),
            surface(constant=0.05, eta_linear=-0.03, z_linear=0.02),
            surface(constant=0.04, eta_linear=0.02, z_linear=-0.01),
        ),
    ]


def random_profiles():
    rng = np.random.default_rng(SEED)

    def random_surface():
        coefficients = rng.uniform(-0.16, 0.16, size=7)
        return Surface(
            *coefficients,
            eta_frequency=float(rng.uniform(0.55, 2.2)),
            z_frequency=float(rng.uniform(-2.2, 2.2)),
            phase=float(rng.uniform(-math.pi, math.pi)),
        )

    profiles = []
    for index in range(RANDOM_COUNT):
        scale = LogScale(
            linear=float(rng.uniform(-0.12, 0.12)),
            quadratic=float(rng.uniform(-0.04, 0.04)),
            amplitude=float(rng.uniform(-0.03, 0.03)),
            frequency=float(rng.uniform(0.6, 2.2)),
            phase=float(rng.uniform(-math.pi, math.pi)),
        )
        profiles.append(
            Profile(
                f"random_{index:03d}",
                scale,
                random_surface(),
                random_surface(),
                random_surface(),
                random_surface(),
                RAY_OFFSETS[index % len(RAY_OFFSETS)],
            )
        )
    return profiles


def coframe_metric(profile, point):
    eta, z, p_value, w_value = point
    scale, entry_a, entry_n, entry_b, rotation_r = profile.torch_values(eta, z)
    shift_0 = entry_a * p_value + (entry_n + rotation_r) * w_value
    shift_1 = (entry_n - rotation_r) * p_value + entry_b * w_value
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


def metric_jets(profile, eta_value, z_value):
    point = torch.tensor([eta_value, z_value, 0.0, 0.0], dtype=DTYPE)
    metric_function = lambda argument: coframe_metric(profile, argument)
    metric = metric_function(point)
    first = torch.autograd.functional.jacobian(
        metric_function, point, create_graph=False, strict=False, vectorize=False
    )

    def differentiable_first(argument):
        return torch.autograd.functional.jacobian(
            metric_function, argument, create_graph=True, strict=False, vectorize=False
        )

    second = torch.autograd.functional.jacobian(
        differentiable_first, point, create_graph=False, strict=False, vectorize=False
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
                    gamma_derivative[aa, bb, cc, ee] = 0.5 * (
                        first_term + second_term
                    )

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
    return riemann, gamma


def metric_readouts(profile, eta_value, z_value):
    metric, first, second = metric_jets(profile, eta_value, z_value)
    riemann, gamma = curvature_from_jets(metric, first, second)
    scale, dscale, _ = profile.scale.values(eta_value)
    ray = np.array([scale**-2, scale**-2, 0.0, 0.0])
    clock = np.array([scale**-1, 0.0, 0.0, 0.0])
    screens = (
        np.array([0.0, 0.0, scale**-1, 0.0]),
        np.array([0.0, 0.0, 0.0, scale**-1]),
    )
    tide = np.zeros((2, 2), dtype=float)
    connection = np.zeros((2, 2), dtype=float)
    gram = np.zeros((2, 2), dtype=float)
    for left_index, left in enumerate(screens):
        for right_index, right in enumerate(screens):
            gram[left_index, right_index] = left @ metric @ right
            derivative = np.zeros(4, dtype=float)
            derivative[right_index + 2] = -dscale * scale**-2 * ray[0]
            for aa in range(4):
                derivative[aa] += sum(
                    gamma[aa, bb, cc] * ray[bb] * right[cc]
                    for bb in range(4)
                    for cc in range(4)
                )
            connection[left_index, right_index] = left @ metric @ derivative
            curvature_vector = np.zeros(4, dtype=float)
            for aa in range(4):
                curvature_vector[aa] = sum(
                    riemann[aa, bb, cc, dd] * ray[bb] * right[cc] * ray[dd]
                    for bb in (0, 1)
                    for cc in (2, 3)
                    for dd in (0, 1)
                )
            tide[left_index, right_index] = left @ metric @ curvature_vector

    geodesic = np.zeros(4, dtype=float)
    geodesic[0:2] = -2.0 * dscale * scale**-5
    for aa in range(4):
        geodesic[aa] += sum(
            gamma[aa, bb, cc] * ray[bb] * ray[cc]
            for bb in range(4)
            for cc in range(4)
        )
    frequency = -clock @ metric @ ray
    return metric, tide, connection, gram, geodesic, frequency


def candidate_matrices(profile, eta_value, z_value):
    scale, dscale, ddscale = profile.scale.values(eta_value)
    a_value = profile.entry_a.values(eta_value, z_value)
    n_value = profile.entry_n.values(eta_value, z_value)
    b_value = profile.entry_b.values(eta_value, z_value)
    r_value = profile.rotation_r.values(eta_value, z_value)
    strain = np.array([[a_value[0], n_value[0]], [n_value[0], b_value[0]]])
    dplus_strain = np.array(
        [
            [a_value[1] + a_value[2], n_value[1] + n_value[2]],
            [n_value[1] + n_value[2], b_value[1] + b_value[2]],
        ]
    )
    omega = np.array([[0.0, r_value[0]], [-r_value[0], 0.0]])
    mix = strain + omega
    dplus_mix = np.array(
        [
            [a_value[1] + a_value[2], n_value[1] + n_value[2] + r_value[1] + r_value[2]],
            [n_value[1] + n_value[2] - r_value[1] - r_value[2], b_value[1] + b_value[2]],
        ]
    )
    hubble = dscale / scale
    dhubble = ddscale / scale - hubble * hubble
    isotropic = (hubble * hubble - dhubble) / scale**4
    commutator = strain @ omega - omega @ strain
    tide = isotropic * np.eye(2) + (
        2.0 * dplus_strain - 4.0 * strain @ strain - 4.0 * commutator
    ) / scale**4
    connection = 2.0 * omega / scale**2
    return {
        "scale": scale,
        "strain": strain,
        "omega": omega,
        "mix": mix,
        "dplus_mix": dplus_mix,
        "tide": tide,
        "connection": connection,
        "mixed_jets": np.array([a_value[3], n_value[3], b_value[3], r_value[3]]),
        "z_jets": np.array([a_value[2], n_value[2], b_value[2], r_value[2]]),
        "eta_jets": np.array([a_value[1], n_value[1], b_value[1], r_value[1]]),
    }


def integrate_profile(profile, endpoint):
    initial = np.concatenate((np.zeros(4), np.eye(2).reshape(-1), np.eye(2).reshape(-1), np.zeros(4)))

    def right_hand_side(s_value, state):
        z_value = s_value - profile.ray_offset
        candidate = candidate_matrices(profile, s_value, z_value)
        direct = state[0:4].reshape(2, 2)
        velocity = state[4:8].reshape(2, 2)
        fundamental = state[8:12].reshape(2, 2)
        inverse_fundamental = np.linalg.inv(fundamental)
        mix = candidate["mix"]
        dplus_mix = candidate["dplus_mix"]
        velocity_derivative = (
            -2.0 * (mix - mix.T) @ velocity
            - (2.0 * dplus_mix - 4.0 * mix.T @ mix) @ direct
        )
        return np.concatenate(
            (
                velocity.reshape(-1),
                velocity_derivative.reshape(-1),
                (-2.0 * mix @ fundamental).reshape(-1),
                (inverse_fundamental @ inverse_fundamental.T).reshape(-1),
            )
        )

    sample = np.linspace(0.0, endpoint, 27)
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
    minimum_nonvertex_determinant = math.inf
    endpoint_direct = None
    for column, s_value in enumerate(solution.t):
        state = solution.y[:, column]
        direct = state[0:4].reshape(2, 2)
        fundamental = state[8:12].reshape(2, 2)
        integral = state[12:16].reshape(2, 2)
        represented = fundamental @ integral
        max_factor_error = max(
            max_factor_error, float(np.max(np.abs(direct - represented)))
        )
        if abs(float(s_value)) > 1.0e-12:
            minimum_nonvertex_determinant = min(
                minimum_nonvertex_determinant, float(np.linalg.det(direct))
            )
        endpoint_direct = direct.copy()
    return max_factor_error, minimum_nonvertex_determinant, endpoint_direct


def verify_profile(profile):
    maxima = {
        "pair": 0.0,
        "frequency": 0.0,
        "affine": 0.0,
        "screen_gram": 0.0,
        "tide": 0.0,
        "symmetry": 0.0,
        "connection": 0.0,
    }
    minimum_scale = math.inf
    assertion_count = 0
    for eta_value, z_value in CURVATURE_POINTS:
        metric, tide, connection, gram, geodesic, frequency = metric_readouts(
            profile, eta_value, z_value
        )
        candidate = candidate_matrices(profile, eta_value, z_value)
        scale = candidate["scale"]
        expected_central = np.diag([-scale * scale, scale * scale, scale * scale, scale * scale])
        maxima["pair"] = max(maxima["pair"], float(np.max(np.abs(metric - expected_central))))
        maxima["frequency"] = max(maxima["frequency"], abs(frequency - scale**-1))
        maxima["affine"] = max(maxima["affine"], float(np.max(np.abs(geodesic))))
        maxima["screen_gram"] = max(maxima["screen_gram"], float(np.max(np.abs(gram - np.eye(2)))))
        maxima["tide"] = max(maxima["tide"], float(np.max(np.abs(tide - candidate["tide"]))))
        maxima["symmetry"] = max(maxima["symmetry"], float(np.max(np.abs(tide - tide.T))))
        maxima["connection"] = max(
            maxima["connection"], float(np.max(np.abs(connection - candidate["connection"])))
        )
        minimum_scale = min(minimum_scale, scale)
        assertion_count += 7

    for key in ("pair", "frequency", "affine", "screen_gram", "symmetry"):
        if maxima[key] > ALGEBRA_CEILING:
            raise AssertionError(f"{profile.name}: {key} error {maxima[key]}")
    for key in ("tide", "connection"):
        if maxima[key] > TENSOR_CEILING:
            raise AssertionError(f"{profile.name}: {key} error {maxima[key]}")

    forward = integrate_profile(profile, ETA_FORWARD)
    backward = integrate_profile(profile, ETA_BACKWARD)
    for label, result in (("forward", forward), ("backward", backward)):
        if result[0] > TENSOR_CEILING:
            raise AssertionError(f"{profile.name}: {label} factor error {result[0]}")
        if result[1] <= 0.0:
            raise AssertionError(f"{profile.name}: {label} determinant {result[1]}")
        assertion_count += 2
    if minimum_scale <= 0.0:
        raise AssertionError(f"{profile.name}: nonpositive scale {minimum_scale}")
    assertion_count += 1

    result = {
        "name": profile.name,
        "ray_offset_eta_minus_z": profile.ray_offset,
        "max_central_metric_error": maxima["pair"],
        "max_frequency_error": maxima["frequency"],
        "max_affine_ray_error": maxima["affine"],
        "max_screen_gram_error": maxima["screen_gram"],
        "max_tide_error": maxima["tide"],
        "max_tide_asymmetry": maxima["symmetry"],
        "max_screen_connection_error": maxima["connection"],
        "max_factorization_error": max(forward[0], backward[0]),
        "minimum_sampled_nonvertex_determinant": min(forward[1], backward[1]),
        "minimum_sampled_scale": minimum_scale,
        "assertions": assertion_count,
    }
    if not profile.name.startswith("random_"):
        result["forward_endpoint_jacobi"] = forward[2].tolist()
    return result


def main():
    profiles = named_profiles() + random_profiles()
    results = []
    for index, profile in enumerate(profiles):
        results.append(verify_profile(profile))
        if (index + 1) % 24 == 0:
            print(
                f"G196 independent replay: {index + 1}/{len(profiles)}",
                file=sys.stderr,
                flush=True,
            )

    named = {profile.name: profile for profile in profiles if not profile.name.startswith("random_")}
    noncommuting = candidate_matrices(named["fully_noncommuting"], 0.31, 0.12)
    commutator_norm = float(
        np.linalg.norm(noncommuting["strain"] @ noncommuting["omega"] - noncommuting["omega"] @ noncommuting["strain"])
    )
    if commutator_norm <= 1.0e-4:
        raise AssertionError(f"noncommuting gate inactive: {commutator_norm}")

    rank_profile = named["rank_transition"]
    rank_values = [
        float(np.linalg.det(candidate_matrices(rank_profile, value, value)["mix"]))
        for value in (-0.40, 0.40)
    ]
    if rank_values[0] * rank_values[1] >= 0.0:
        raise AssertionError(f"rank-transition gate inactive: {rank_values}")

    rotation_profile = named["rotation_zero_crossing"]
    rotation_values = [rotation_profile.rotation_r.values(value, value)[0] for value in (-0.40, 0.40)]
    if rotation_values[0] * rotation_values[1] >= 0.0:
        raise AssertionError(f"rotation-crossing gate inactive: {rotation_values}")

    z_control = candidate_matrices(named["pure_longitudinal_gradient"], 0.27, 0.08)
    z_gradient_norm = float(np.linalg.norm(z_control["z_jets"]))
    if z_gradient_norm <= 1.0e-4:
        raise AssertionError(f"z-gradient gate inactive: {z_gradient_norm}")

    mixed_control = candidate_matrices(named["mixed_eta_z_cross"], 0.23, -0.14)
    mixed_jet_norm = float(np.linalg.norm(mixed_control["mixed_jets"]))
    if mixed_jet_norm <= 1.0e-4:
        raise AssertionError(f"mixed-jet gate inactive: {mixed_jet_norm}")

    null_control = candidate_matrices(named["eta_minus_z_field"], 0.29, 0.11)
    null_directional_norm = float(np.linalg.norm(null_control["dplus_mix"]))
    if null_directional_norm > ALGEBRA_CEILING:
        raise AssertionError(f"eta-z directional gate failed: {null_directional_norm}")

    alias_base = named["same_ray_base"]
    alias_shift = named["same_ray_offray_alias"]
    on_ray_errors = []
    for value in (-0.31, 0.0, 0.37):
        base = candidate_matrices(alias_base, value, value)
        alias = candidate_matrices(alias_shift, value, value)
        on_ray_errors.append(float(np.max(np.abs(base["mix"] - alias["mix"]))))
        on_ray_errors.append(float(np.max(np.abs(base["dplus_mix"] - alias["dplus_mix"]))))
    alias_on_ray_error = max(on_ray_errors)
    if alias_on_ray_error > ALGEBRA_CEILING:
        raise AssertionError(f"same-ray alias mismatch: {alias_on_ray_error}")
    offray_base = candidate_matrices(alias_base, 0.31, 0.07)["mix"]
    offray_alias = candidate_matrices(alias_shift, 0.31, 0.07)["mix"]
    alias_offray_difference = float(np.linalg.norm(offray_base - offray_alias))
    if alias_offray_difference <= 1.0e-4:
        raise AssertionError(f"off-ray alias gate inactive: {alias_offray_difference}")

    pure_rotation = named["pure_rotation_spacetime"]
    pure_candidate = candidate_matrices(pure_rotation, 0.28, 0.09)
    hubble_only_profile = Profile("hubble_only", pure_rotation.scale, ZERO, ZERO, ZERO, ZERO)
    hubble_candidate = candidate_matrices(hubble_only_profile, 0.28, 0.09)
    pure_rotation_tide_error = float(np.max(np.abs(pure_candidate["tide"] - hubble_candidate["tide"])))
    if pure_rotation_tide_error > ALGEBRA_CEILING:
        raise AssertionError(f"pure-rotation tide gate failed: {pure_rotation_tide_error}")

    global_assertions = 9
    summary = {
        "status": "PASS",
        "landing": "NULL_DIRECTIONAL_DESCENT__FACTORIZATION_AND_NO_CAUSTIC_SURVIVE",
        "implementation": (
            "independent Torch float64 second metric jets and direct Riemann/connection contraction "
            "plus SciPy DOP853 direct-versus-ordered Jacobi IVPs; no production import or artifact read"
        ),
        "seed": SEED,
        "history_count": len(results),
        "named_history_count": len(named_profiles()),
        "random_history_count": len(random_profiles()),
        "assertion_count": sum(item["assertions"] for item in results) + global_assertions,
        "global_assertion_count": global_assertions,
        "commutator_norm": commutator_norm,
        "rank_transition_determinants": rank_values,
        "rotation_zero_crossing_values": rotation_values,
        "z_gradient_norm": z_gradient_norm,
        "mixed_jet_norm": mixed_jet_norm,
        "eta_minus_z_dplus_norm": null_directional_norm,
        "same_ray_alias_error": alias_on_ray_error,
        "same_ray_alias_offray_difference": alias_offray_difference,
        "pure_rotation_tide_error": pure_rotation_tide_error,
        "max_central_metric_error": max(item["max_central_metric_error"] for item in results),
        "max_frequency_error": max(item["max_frequency_error"] for item in results),
        "max_affine_ray_error": max(item["max_affine_ray_error"] for item in results),
        "max_screen_gram_error": max(item["max_screen_gram_error"] for item in results),
        "max_tide_error": max(item["max_tide_error"] for item in results),
        "max_tide_asymmetry": max(item["max_tide_asymmetry"] for item in results),
        "max_screen_connection_error": max(item["max_screen_connection_error"] for item in results),
        "max_factorization_error": max(item["max_factorization_error"] for item in results),
        "minimum_sampled_nonvertex_determinant": min(item["minimum_sampled_nonvertex_determinant"] for item in results),
        "minimum_sampled_scale": min(item["minimum_sampled_scale"] for item in results),
        "ceilings": {"tensor": TENSOR_CEILING, "algebra": ALGEBRA_CEILING},
        "profiles": results,
    }
    payload = json.dumps(summary, indent=2, sort_keys=True) + "\n"
    if os.environ.get("G196_NO_WRITE") == "1":
        print(payload, end="")
        return
    Path(__file__).with_name("INDEPENDENT_VERIFICATION.json").write_text(payload, encoding="utf-8")
    print(payload, end="")


if __name__ == "__main__":
    main()
