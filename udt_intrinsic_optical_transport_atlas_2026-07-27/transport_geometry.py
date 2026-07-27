#!/usr/bin/env python3
"""Production orthonormal-frame geometry for the frozen twisted-S3 family."""

from __future__ import annotations

import numpy as np

ETA = np.diag((-1.0, 1.0, 1.0, 1.0))
ETA_SIGN = np.array((-1.0, 1.0, 1.0, 1.0))
EPSILON = 1.0 / 50.0
TWIST = 1.0 / 64.0
KAPPA = -2.0


def quaternion_and_derivative(x: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    r2 = np.dot(x, x)
    denominator = 1.0 + r2
    q = np.empty(4, dtype=x.dtype)
    q[0] = (1.0 - r2) / denominator
    q[1:] = 2.0 * x / denominator
    dq = np.empty((4, 3), dtype=x.dtype)
    dq[0] = -4.0 * x / denominator**2
    dq[1:] = 2.0 * np.eye(3, dtype=x.dtype) / denominator - 4.0 * np.outer(x, x) / denominator**2
    return q, dq


def profile_and_gradient(x: np.ndarray) -> tuple[np.number, np.ndarray]:
    q, dq = quaternion_and_derivative(x)
    q1, q2, q3 = q[1:]
    profile = (
        q1 + 2 * q2 + 3 * q3
        + q1 * q2 + 2 * q2 * q3 + 3 * q3 * q1
        + 2 * q1**2 - 3 * q2**2 + 5 * q3**2
        + q1 * q2 * q3 + 2 * q1**3 - q2**3 + 3 * q3**3
    )
    derivative_q = np.array((
        1 + q2 + 3 * q3 + 4 * q1 + q2 * q3 + 6 * q1**2,
        2 + q1 + 2 * q3 - 6 * q2 + q1 * q3 - 3 * q2**2,
        3 + 2 * q2 + 3 * q1 + 10 * q3 + q1 * q2 + 9 * q3**2,
    ), dtype=x.dtype)
    return EPSILON * profile, EPSILON * derivative_q @ dq[1:]


def sigma_coframe(x: np.ndarray) -> np.ndarray:
    q, dq = quaternion_and_derivative(x)
    q0, qvector = q[0], q[1:]
    sigma = np.empty((3, 3), dtype=x.dtype)
    for axis in range(3):
        dqvector = dq[1:, axis]
        sigma[:, axis] = q0 * dqvector - qvector * dq[0, axis] - np.cross(qvector, dqvector)
    return sigma


def coframe_data(x: np.ndarray, lambda_value: float) -> tuple[np.number, np.ndarray, np.ndarray, np.ndarray]:
    phi, dphi = profile_and_gradient(x)
    sigma = sigma_coframe(x)
    coframe = np.zeros((4, 4), dtype=x.dtype)
    coframe[0, 0] = np.exp(-phi)
    coframe[0, 1:] = np.exp(-phi) * TWIST * sigma[2]
    coframe[1, 1:] = np.exp(phi) * sigma[2]
    coframe[2, 1:] = np.exp(lambda_value * phi) * sigma[0]
    coframe[3, 1:] = np.exp(lambda_value * phi) * sigma[1]
    frame = np.linalg.inv(coframe)
    return phi, dphi, coframe, frame


def metric(x: np.ndarray, lambda_value: float) -> np.ndarray:
    _, _, coframe, _ = coframe_data(x, lambda_value)
    return coframe.T @ ETA @ coframe


def connection_and_structure(x: np.ndarray, lambda_value: float) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.number]:
    phi, dphi, coframe, frame = coframe_data(x, lambda_value)
    p = frame[1:, :].T @ dphi
    structure = np.zeros((4, 4, 4), dtype=x.dtype)

    def set_coefficient(upper: int, left: int, right: int, de_coefficient) -> None:
        structure[upper, left, right] = -de_coefficient
        structure[upper, right, left] = de_coefficient

    at = TWIST * KAPPA * np.exp(-(1.0 + 2.0 * lambda_value) * phi)
    bt = KAPPA * np.exp((1.0 - 2.0 * lambda_value) * phi)
    ct = KAPPA * np.exp(-phi)
    set_coefficient(0, 0, 1, p[1])
    set_coefficient(0, 0, 2, p[2])
    set_coefficient(0, 0, 3, p[3])
    set_coefficient(0, 2, 3, at)
    set_coefficient(1, 1, 2, -p[2])
    set_coefficient(1, 1, 3, -p[3])
    set_coefficient(1, 2, 3, bt)
    set_coefficient(2, 1, 2, lambda_value * p[1])
    set_coefficient(2, 2, 3, -lambda_value * p[3])
    set_coefficient(2, 1, 3, -ct)
    set_coefficient(3, 1, 3, lambda_value * p[1])
    set_coefficient(3, 2, 3, lambda_value * p[2])
    set_coefficient(3, 1, 2, ct)

    connection = np.zeros((4, 4, 4), dtype=x.dtype)
    for out in range(4):
        for left in range(4):
            for middle in range(4):
                lowered = (
                    ETA_SIGN[out] * structure[out, left, middle]
                    - ETA_SIGN[left] * structure[left, middle, out]
                    + ETA_SIGN[middle] * structure[middle, out, left]
                ) / 2.0
                connection[out, left, middle] = ETA_SIGN[out] * lowered
    return connection, structure, frame, phi


def curvature_frame(x: np.ndarray, lambda_value: float, complex_step: float = 1.0e-5) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.number]:
    connection, structure, frame, phi = connection_and_structure(x, lambda_value)
    derivatives = np.empty((4, 4, 4, 3), dtype=float)
    for axis in range(3):
        shifted = np.asarray(x, dtype=complex).copy()
        shifted[axis] += 1j * complex_step
        shifted_connection = connection_and_structure(shifted, lambda_value)[0]
        derivatives[..., axis] = np.imag(shifted_connection) / complex_step

    riemann = np.zeros((4, 4, 4, 4), dtype=float)
    for out in range(4):
        for acted in range(4):
            for left in range(4):
                for right in range(4):
                    value = 0.0
                    for coordinate in range(1, 4):
                        value += (
                            frame[coordinate, left] * derivatives[out, right, acted, coordinate - 1]
                            - frame[coordinate, right] * derivatives[out, left, acted, coordinate - 1]
                        )
                    for middle in range(4):
                        value += (
                            connection[middle, right, acted] * connection[out, left, middle]
                            - connection[middle, left, acted] * connection[out, right, middle]
                            - structure[middle, left, right] * connection[out, middle, acted]
                        )
                    riemann[out, acted, left, right] = value
    return riemann, connection, frame, phi


def optical_curvature(riemann: np.ndarray, tangent: np.ndarray, transported_frame: np.ndarray) -> np.ndarray:
    screens = (transported_frame[:, 2], transported_frame[:, 3])
    result = np.zeros((2, 2))
    for left, screen_left in enumerate(screens):
        lowered_left = ETA @ screen_left
        for right, screen_right in enumerate(screens):
            acted = np.einsum("abcd,b,c,d->a", riemann, tangent, tangent, screen_right)
            result[left, right] = lowered_left @ acted
    return result


def state_diagnostics(x: np.ndarray, tangent: np.ndarray, transported_frame: np.ndarray,
                      jacobi: np.ndarray, lambda_value: float) -> dict[str, float]:
    phi = float(profile_and_gradient(x[1:])[0])
    null = float(abs(tangent @ ETA @ tangent))
    gram = transported_frame.T @ ETA @ transported_frame
    gram_residual = float(np.max(np.abs(gram - ETA)))
    screen_k = max(abs(transported_frame[:, index] @ ETA @ tangent) for index in (2, 3))
    omega = np.block([[np.zeros((2, 2)), np.eye(2)], [-np.eye(2), np.zeros((2, 2))]])
    symplectic = float(np.max(np.abs(jacobi.T @ omega @ jacobi - omega)))
    return {
        "phi": phi, "null_residual": null, "screen_gram_residual": gram_residual,
        "k_screen_residual": float(screen_k), "symplectic_residual": symplectic,
        "detM_residual": float(abs(np.linalg.det(jacobi) - 1.0)),
        "screen_leakage": float(sum(transported_frame[row, column] ** 2
                                    for row in (0, 1) for column in (2, 3))),
        "pair_leakage": float(sum(transported_frame[row, column] ** 2
                                  for row in (2, 3) for column in (0, 1))),
        "ray_transverse_mismatch": float(np.hypot(tangent[2], tangent[3])),
    }
