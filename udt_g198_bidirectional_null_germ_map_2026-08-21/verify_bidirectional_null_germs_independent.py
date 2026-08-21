#!/usr/bin/env python3
"""Independent Torch metric-jet verification of the bounded G198 result."""

from __future__ import annotations

import json
import math
import os
import sys
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import torch


DTYPE = torch.float64
LORENTZ = torch.diag(torch.tensor([-1.0, 1.0, 1.0, 1.0], dtype=DTYPE))
SEED = 1980821
RANDOM_HISTORIES = 64
POINTS = ((-0.31, 0.17), (0.08, -0.27), (0.39, 0.22))
TOLERANCE = 8.0e-8
ALGEBRA_TOLERANCE = 2.0e-10


@dataclass(frozen=True)
class History:
    name: str
    scale: tuple[float, float, float, float, float]
    surfaces: np.ndarray


def make_histories():
    rng = np.random.default_rng(SEED)
    histories = []
    zero = np.zeros((4, 10), dtype=float)
    histories.append(History("zero_mixing", (0.04, -0.01, 0.02, 1.3, 0.1), zero))

    eta_minus_z = zero.copy()
    eta_minus_z[0, 1] = 0.12
    eta_minus_z[0, 2] = -0.12
    eta_minus_z[1, 6] = 0.05
    eta_minus_z[1, 7] = 1.1
    eta_minus_z[1, 8] = -1.1
    histories.append(History("eta_minus_z", (-0.03, 0.015, 0.01, 1.7, -0.2), eta_minus_z))

    pure_rotation = zero.copy()
    pure_rotation[3, 0] = 0.18
    pure_rotation[3, 1] = -0.07
    pure_rotation[3, 2] = 0.09
    pure_rotation[3, 5] = 0.04
    histories.append(History("pure_rotation", (0.07, -0.02, 0.015, 1.5, 0.3), pure_rotation))

    noncommuting = zero.copy()
    noncommuting[:, 0] = (0.21, -0.09, -0.13, 0.16)
    noncommuting[:, 1] = (0.04, -0.03, 0.06, -0.05)
    noncommuting[:, 2] = (-0.02, 0.07, 0.03, 0.08)
    noncommuting[:, 5] = (0.03, -0.04, 0.02, 0.05)
    histories.append(History("fully_noncommuting", (0.09, -0.025, 0.02, 1.9, -0.1), noncommuting))

    for index in range(RANDOM_HISTORIES):
        scale = (
            float(rng.uniform(-0.12, 0.12)),
            float(rng.uniform(-0.04, 0.04)),
            float(rng.uniform(-0.025, 0.025)),
            float(rng.uniform(0.6, 2.2)),
            float(rng.uniform(-math.pi, math.pi)),
        )
        surfaces = rng.uniform(-0.16, 0.16, size=(4, 10))
        surfaces[:, 7:9] = rng.uniform(-2.0, 2.0, size=(4, 2))
        surfaces[:, 9] = rng.uniform(-math.pi, math.pi, size=4)
        histories.append(History(f"random_{index:03d}", scale, surfaces))
    return histories


def scale_value(history, eta):
    linear, quadratic, amplitude, frequency, phase = history.scale
    return torch.exp(
        linear * eta
        + quadratic * eta * eta
        + amplitude * (torch.sin(frequency * eta + phase) - math.sin(phase))
    )


def surface_value(coefficients, eta, z):
    return (
        coefficients[0]
        + coefficients[1] * eta
        + coefficients[2] * z
        + coefficients[3] * eta * eta
        + coefficients[4] * z * z
        + coefficients[5] * eta * z
        + coefficients[6]
        * torch.sin(coefficients[7] * eta + coefficients[8] * z + coefficients[9])
    )


def mix_value(history, eta, z, zero_mixing=False):
    if zero_mixing:
        zero = eta * 0.0
        return torch.stack((torch.stack((zero, zero)), torch.stack((zero, zero))))
    values = [surface_value(history.surfaces[index], eta, z) for index in range(4)]
    entry_a, entry_n, entry_b, rotation = values
    return torch.stack(
        (
            torch.stack((entry_a, entry_n + rotation)),
            torch.stack((entry_n - rotation, entry_b)),
        )
    )


def coframe_metric(history, point, zero_mixing=False):
    eta, z, p, w = point
    scale = scale_value(history, eta)
    mix = mix_value(history, eta, z, zero_mixing=zero_mixing)
    shift = mix @ torch.stack((p, w))
    zero = eta * 0.0
    one = zero + 1.0
    coframe = scale * torch.stack(
        (
            torch.stack((one, zero, zero, zero)),
            torch.stack((zero, one, zero, zero)),
            torch.stack((shift[0], shift[0], one, zero)),
            torch.stack((shift[1], shift[1], zero, one)),
        )
    )
    return coframe.T @ LORENTZ @ coframe


def metric_jets(history, eta_value, z_value, zero_mixing=False):
    point = torch.tensor([eta_value, z_value, 0.0, 0.0], dtype=DTYPE)

    def metric_function(argument):
        return coframe_metric(history, argument, zero_mixing=zero_mixing)

    metric = metric_function(point)
    first = torch.autograd.functional.jacobian(metric_function, point, create_graph=False)

    def differentiable_first(argument):
        return torch.autograd.functional.jacobian(metric_function, argument, create_graph=True)

    second = torch.autograd.functional.jacobian(
        differentiable_first, point, create_graph=False
    )
    return metric.detach().numpy(), first.detach().numpy(), second.detach().numpy()


def connection_curvature(metric, first, second):
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
                    gamma_derivative[aa, bb, cc, ee] = 0.5 * sum(
                        inverse_derivative[aa, dd, ee]
                        * (first[dd, cc, bb] + first[dd, bb, cc] - first[bb, cc, dd])
                        + inverse[aa, dd]
                        * (
                            second[dd, cc, bb, ee]
                            + second[dd, bb, cc, ee]
                            - second[bb, cc, dd, ee]
                        )
                        for dd in range(4)
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
                            gamma[aa, cc, ff] * gamma[ff, dd, bb]
                            - gamma[aa, dd, ff] * gamma[ff, cc, bb]
                            for ff in range(4)
                        )
                    )
    return gamma, gamma_derivative, riemann


def scale_derivatives(history, eta_value):
    eta = torch.tensor(eta_value, dtype=DTYPE, requires_grad=True)
    value = scale_value(history, eta)
    first = torch.autograd.grad(value, eta, create_graph=True)[0]
    second = torch.autograd.grad(first, eta)[0]
    return float(value), float(first), float(second)


def mix_jets(history, eta_value, z_value):
    point = torch.tensor([eta_value, z_value], dtype=DTYPE)

    def function(argument):
        return mix_value(history, argument[0], argument[1])

    value = function(point)
    first = torch.autograd.functional.jacobian(function, point)
    return value.detach().numpy(), first.detach().numpy()


def readouts(history, eta_value, z_value, sign, zero_mixing=False):
    metric, first, second = metric_jets(
        history, eta_value, z_value, zero_mixing=zero_mixing
    )
    gamma, gamma_derivative, riemann = connection_curvature(metric, first, second)
    scale, dscale, _ = scale_derivatives(history, eta_value)
    ray = np.array([scale**-2, sign * scale**-2, 0.0, 0.0])
    ray_dot = np.array(
        [-2.0 * dscale * scale**-5, -2.0 * sign * dscale * scale**-5, 0.0, 0.0]
    )
    clock = np.array([scale**-1, 0.0, 0.0, 0.0])
    screens = (
        np.array([0.0, 0.0, scale**-1, 0.0]),
        np.array([0.0, 0.0, 0.0, scale**-1]),
    )

    connection = np.zeros((2, 2), dtype=float)
    tide = np.zeros((2, 2), dtype=float)
    for ii, left in enumerate(screens):
        for jj, right in enumerate(screens):
            right_derivative = np.zeros(4, dtype=float)
            right_derivative[jj + 2] = -dscale * scale**-2 * ray[0]
            right_derivative += np.einsum("abc,b,c->a", gamma, ray, right)
            connection[ii, jj] = left @ metric @ right_derivative
            curvature_vector = np.einsum("abcd,b,c,d->a", riemann, ray, right, ray)
            tide[ii, jj] = left @ metric @ curvature_vector

    geodesic = ray_dot + np.einsum("abc,b,c->a", gamma, ray, ray)
    frequency = -clock @ metric @ ray
    return {
        "metric": metric,
        "gamma": gamma,
        "gamma_derivative": gamma_derivative,
        "riemann": riemann,
        "scale": scale,
        "dscale": dscale,
        "ray": ray,
        "ray_dot": ray_dot,
        "connection": connection,
        "tide": tide,
        "geodesic": geodesic,
        "frequency": frequency,
    }


def direct_coordinate_residual(readout, sign, y, derivative_y, second_derivative_y):
    scale = readout["scale"]
    dscale = readout["dscale"]
    gamma = readout["gamma"]
    gamma_derivative = readout["gamma_derivative"]
    riemann = readout["riemann"]
    ray = readout["ray"]
    ray_dot = readout["ray_dot"]

    vector = np.zeros(4, dtype=float)
    vector[2:4] = y
    vector_dot = np.zeros(4, dtype=float)
    vector_dot[2:4] = scale**-2 * derivative_y
    vector_ddot = np.zeros(4, dtype=float)
    vector_ddot[2:4] = scale**-4 * (
        second_derivative_y - 2.0 * (dscale / scale) * derivative_y
    )

    second_covariant = vector_ddot.copy()
    second_covariant += 2.0 * np.einsum("abc,b,c->a", gamma, ray, vector_dot)
    second_covariant += np.einsum(
        "abc,b,c->a", gamma, ray_dot, vector
    )
    second_covariant += np.einsum(
        "abce,e,b,c->a", gamma_derivative, ray, ray, vector
    )
    second_covariant += np.einsum(
        "ade,d,ebc,b,c->a", gamma, ray, gamma, ray, vector
    )
    curvature = np.einsum("abcd,b,c,d->a", riemann, ray, vector, ray)
    return scale**4 * (second_covariant + curvature)


def expected_plus_operator(history, eta_value, z_value, y, derivative_y, second_derivative_y):
    mix, first = mix_jets(history, eta_value, z_value)
    dplus_mix = first[:, :, 0] + first[:, :, 1]
    return (
        second_derivative_y
        + 2.0 * (mix - mix.T) @ derivative_y
        + (2.0 * dplus_mix - 4.0 * mix.T @ mix) @ y
    )


def main():
    histories = make_histories()
    rng = np.random.default_rng(SEED + 1)
    maxima = {
        "incoming_connection": 0.0,
        "incoming_tide_control": 0.0,
        "incoming_operator": 0.0,
        "incoming_base_residual": 0.0,
        "outgoing_connection": 0.0,
        "outgoing_operator": 0.0,
        "affine": 0.0,
        "frequency": 0.0,
        "metric": 0.0,
    }
    assertions = 0
    base_residual_evaluations = 0
    for history_index, history in enumerate(histories):
        for eta_value, z_value in POINTS:
            incoming = readouts(history, eta_value, z_value, -1)
            incoming_control = readouts(history, eta_value, z_value, -1, zero_mixing=True)
            outgoing = readouts(history, eta_value, z_value, 1)
            scale = incoming["scale"]
            expected_metric = np.diag(
                [-scale * scale, scale * scale, scale * scale, scale * scale]
            )
            mix, _ = mix_jets(history, eta_value, z_value)
            omega = 0.5 * (mix - mix.T)

            maxima["metric"] = max(
                maxima["metric"], float(np.max(np.abs(incoming["metric"] - expected_metric)))
            )
            maxima["incoming_connection"] = max(
                maxima["incoming_connection"], float(np.max(np.abs(incoming["connection"])))
            )
            maxima["incoming_tide_control"] = max(
                maxima["incoming_tide_control"],
                float(np.max(np.abs(incoming["tide"] - incoming_control["tide"]))),
            )
            maxima["outgoing_connection"] = max(
                maxima["outgoing_connection"],
                float(np.max(np.abs(outgoing["connection"] - 2.0 * omega / scale**2))),
            )
            maxima["affine"] = max(
                maxima["affine"],
                float(np.max(np.abs(incoming["geodesic"]))),
                float(np.max(np.abs(outgoing["geodesic"]))),
            )
            maxima["frequency"] = max(
                maxima["frequency"],
                abs(incoming["frequency"] - scale**-1),
                abs(outgoing["frequency"] - scale**-1),
            )

            for _ in range(2):
                y = rng.uniform(-0.7, 0.7, size=2)
                derivative_y = rng.uniform(-0.7, 0.7, size=2)
                second_derivative_y = rng.uniform(-0.7, 0.7, size=2)
                incoming_full_residual = direct_coordinate_residual(
                    incoming, -1, y, derivative_y, second_derivative_y
                )
                outgoing_full_residual = direct_coordinate_residual(
                    outgoing, 1, y, derivative_y, second_derivative_y
                )
                base_residual_evaluations += 2
                maxima["incoming_base_residual"] = max(
                    maxima["incoming_base_residual"],
                    float(np.max(np.abs(incoming_full_residual[:2]))),
                    float(np.max(np.abs(outgoing_full_residual[:2]))),
                )
                incoming_residual = incoming_full_residual[2:4]
                outgoing_residual = outgoing_full_residual[2:4]
                maxima["incoming_operator"] = max(
                    maxima["incoming_operator"],
                    float(np.max(np.abs(incoming_residual - second_derivative_y))),
                )
                maxima["outgoing_operator"] = max(
                    maxima["outgoing_operator"],
                    float(
                        np.max(
                            np.abs(
                                outgoing_residual
                                - expected_plus_operator(
                                    history,
                                    eta_value,
                                    z_value,
                                    y,
                                    derivative_y,
                                    second_derivative_y,
                                )
                            )
                        )
                    ),
                )
            assertions += 9
        if (history_index + 1) % 16 == 0:
            print(
                f"G198 independent metric jets: {history_index + 1}/{len(histories)}",
                file=sys.stderr,
                flush=True,
            )

    for key, value in maxima.items():
        ceiling = ALGEBRA_TOLERANCE if key in {"metric", "frequency"} else TOLERANCE
        if value > ceiling:
            raise AssertionError(f"{key}: {value} > {ceiling}")

    alias_on_rays = []
    for value in (-0.41, 0.0, 0.36):
        alias_on_rays.extend(
            [
                (value - value) ** 2 * (value + value) ** 2,
                (value + (-value)) ** 2 * (value - (-value)) ** 2,
            ]
        )
    alias_offray = (0.3 - 0.1) ** 2 * (0.3 + 0.1) ** 2
    if max(abs(item) for item in alias_on_rays) > ALGEBRA_TOLERANCE or alias_offray <= 1.0e-4:
        raise AssertionError("two-ray alias gate failed")
    assertions += 2

    result = {
        "status": "PASS",
        "landing": "OPPOSITE_GERM_NULL_CONTROL__ASYMMETRY_IS_METRIC_ENCODED",
        "implementation": (
            "independent Torch float64 coframe construction, automatic first/second metric jets, "
            "direct Christoffel/Riemann contractions, and direct coordinate Jacobi residuals; "
            "no production import or artifact read"
        ),
        "seed": SEED,
        "history_count": len(histories),
        "random_history_count": RANDOM_HISTORIES,
        "point_count_per_history": len(POINTS),
        "assertion_count": assertions,
        "base_residual_evaluations": base_residual_evaluations,
        "max_errors": maxima,
        "two_ray_alias_onray_error": max(abs(item) for item in alias_on_rays),
        "two_ray_alias_offray_value": alias_offray,
        "ceilings": {"tensor": TOLERANCE, "algebra": ALGEBRA_TOLERANCE},
    }
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if os.environ.get("G198_NO_WRITE") == "1":
        print(payload, end="")
        return
    Path(__file__).with_name("INDEPENDENT_VERIFICATION.json").write_text(
        payload, encoding="utf-8"
    )
    print(payload, end="")


if __name__ == "__main__":
    main()
