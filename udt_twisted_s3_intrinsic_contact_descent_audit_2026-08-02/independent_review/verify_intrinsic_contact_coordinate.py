#!/usr/bin/env python3
"""Independent coordinate/autodiff check of the intrinsic-contact witness.

This script deliberately imports no repository production module.  It builds the
stereographic S3 coframe, coordinate metric, Killing twist, projectors, exterior
derivatives, and contractions directly with torch float64 autodiff.
"""

from __future__ import annotations

import itertools
import json
import math

import torch


torch.set_default_dtype(torch.float64)


def levi_civita_4() -> torch.Tensor:
    eps = torch.zeros((4, 4, 4, 4))
    for p in itertools.permutations(range(4)):
        inversions = sum(p[i] > p[j] for i in range(4) for j in range(i + 1, 4))
        eps[p] = -1.0 if inversions % 2 else 1.0
    return eps


EPS = levi_civita_4()


def q_sigma_u(coords: torch.Tensor):
    """Unit quaternion, left-invariant forms, and frozen u profile."""
    xyz = coords[1:]
    r2 = xyz @ xyz
    den = 1.0 + r2
    q0 = (1.0 - r2) / den
    qsp = 2.0 * xyz / den
    q = torch.cat((q0.reshape(1), qsp))

    # Exact coordinate derivatives of stereographic quaternion components.
    dq0 = -4.0 * xyz / den**2
    eye3 = torch.eye(3, dtype=coords.dtype)
    dqsp = 2.0 * eye3 / den - 4.0 * torch.outer(xyz, xyz) / den**2
    dq = torch.cat((dq0.reshape(1, 3), dqsp), dim=0)
    q0, q1, q2, q3 = q
    dq0, dq1, dq2, dq3 = dq
    sigma1_sp = q0 * dq1 - q1 * dq0 - q2 * dq3 + q3 * dq2
    sigma2_sp = q0 * dq2 - q2 * dq0 - q3 * dq1 + q1 * dq3
    sigma3_sp = q0 * dq3 - q3 * dq0 - q1 * dq2 + q2 * dq1
    zero = torch.zeros(1, dtype=coords.dtype)
    sigma = (
        torch.cat((zero, sigma1_sp)),
        torch.cat((zero, sigma2_sp)),
        torch.cat((zero, sigma3_sp)),
    )
    u = 3.0 + q[0] ** 2 + 2.0 * q[1] ** 2 + 4.0 * q[2] ** 2 + 8.0 * q[3] ** 2
    return q, sigma, u


def coframe_metric(coords: torch.Tensor, lam: int):
    _, (s1, s2, s3), u = q_sigma_u(coords)
    dt = torch.tensor([1.0, 0.0, 0.0, 0.0], dtype=coords.dtype)
    th0 = u ** (-0.5) * (dt + s3)
    th1 = u ** 0.5 * s3
    th2 = u ** (0.5 * lam) * s1
    th3 = u ** (0.5 * lam) * s2
    coframe = torch.stack((th0, th1, th2, th3))
    eta = torch.diag(torch.tensor([-1.0, 1.0, 1.0, 1.0], dtype=coords.dtype))
    metric = coframe.T @ eta @ coframe
    return metric, coframe, u


def exterior_from_covector(covector_fn, coords: torch.Tensor) -> torch.Tensor:
    jac = torch.autograd.functional.jacobian(covector_fn, coords, create_graph=True, vectorize=True)
    # jac[component, derivative-coordinate]
    return jac.T - jac


def killing_flat(coords: torch.Tensor, lam: int, scale: float = 1.0) -> torch.Tensor:
    metric, _, _ = coframe_metric(coords, lam)
    return scale * metric[:, 0]


def normalized_clock(coords: torch.Tensor, lam: int, scale: float = 1.0):
    metric, _, _ = coframe_metric(coords, lam)
    kvec = torch.tensor([scale, 0.0, 0.0, 0.0], dtype=coords.dtype)
    kflat = metric @ kvec
    norm = torch.sqrt(-(kvec @ kflat))
    return kvec / norm, kflat / norm


def raw_twist_flat(coords: torch.Tensor, lam: int, orientation: float = 1.0):
    metric, _, _ = coframe_metric(coords, lam)
    inv = torch.linalg.inv(metric)
    kflat = killing_flat(coords, lam)
    dk = exterior_from_covector(lambda c: killing_flat(c, lam), coords)
    h3 = torch.zeros((4, 4, 4), dtype=coords.dtype)
    for a, b, c in itertools.product(range(4), repeat=3):
        h3[a, b, c] = kflat[a] * dk[b, c] + kflat[b] * dk[c, a] + kflat[c] * dk[a, b]
    root_abs_g = torch.sqrt(torch.abs(torch.linalg.det(metric)))
    twist = orientation * root_abs_g * torch.einsum(
        "mnrs,na,rb,sc,abc->m", EPS, inv, inv, inv, h3
    ) / 6.0
    return twist


def normalized_twist_flat(coords: torch.Tensor, lam: int, orientation: float = 1.0):
    metric, _, _ = coframe_metric(coords, lam)
    inv = torch.linalg.inv(metric)
    twist = raw_twist_flat(coords, lam, orientation)
    twist_norm2 = twist @ inv @ twist
    return twist / torch.sqrt(twist_norm2)


def form_norm2(form: torch.Tensor, inv: torch.Tensor) -> torch.Tensor:
    raised = inv @ form @ inv
    return 0.5 * torch.sum(form * raised)


def audit_point(lam: int, point):
    coords = torch.tensor([0.0, *point], requires_grad=True)
    metric, coframe, u = coframe_metric(coords, lam)
    inv = torch.linalg.inv(metric)
    tvec, tflat = normalized_clock(coords, lam)
    sflat = normalized_twist_flat(coords, lam)
    svec = inv @ sflat
    raw_twist = raw_twist_flat(coords, lam)

    pair = -torch.outer(tvec, tflat) + torch.outer(svec, sflat)
    screen = torch.eye(4) - pair
    dtflat = exterior_from_covector(lambda c: normalized_clock(c, lam)[1], coords)
    dsflat = exterior_from_covector(lambda c: normalized_twist_flat(c, lam), coords)
    ft = screen.T @ dtflat @ screen
    fs = screen.T @ dsflat @ screen
    qt = form_norm2(ft, inv)
    qs = form_norm2(fs, inv)
    qcontact = qs - qt

    expected_qt = 4.0 * u ** (-1 - 2 * lam)
    expected_qs = 4.0 * u ** (1 - 2 * lam)
    expected_q = expected_qs - expected_qt
    # Compare the independently normalized twist line to the displayed theta1 line.
    theta1 = coframe[1]
    twist_alignment = torch.abs(sflat @ inv @ theta1)
    raw_twist_theta1 = torch.abs(raw_twist @ inv @ theta1)
    expected_raw_twist_theta1 = 2.0 * u ** (-(3 + 2 * lam) / 2)
    return {
        "lambda": lam,
        "point": list(point),
        "u": u.item(),
        "det_g": torch.linalg.det(metric).item(),
        "T_norm": (tvec @ metric @ tvec).item(),
        "S_norm": (svec @ metric @ svec).item(),
        "T_dot_S": (tvec @ metric @ svec).item(),
        "twist_theta1_abs_inner": twist_alignment.item(),
        "raw_twist_theta1_abs_inner": raw_twist_theta1.item(),
        "raw_twist_theta1_expected": expected_raw_twist_theta1.item(),
        "raw_twist_abs_error": torch.abs(raw_twist_theta1 - expected_raw_twist_theta1).item(),
        "pair_idempotence_max": torch.max(torch.abs(pair @ pair - pair)).item(),
        "screen_idempotence_max": torch.max(torch.abs(screen @ screen - screen)).item(),
        "Q_T": qt.item(),
        "Q_T_expected": expected_qt.item(),
        "Q_T_abs_error": torch.abs(qt - expected_qt).item(),
        "Q_S": qs.item(),
        "Q_S_expected": expected_qs.item(),
        "Q_S_abs_error": torch.abs(qs - expected_qs).item(),
        "Q": qcontact.item(),
        "Q_expected": expected_q.item(),
        "Q_abs_error": torch.abs(qcontact - expected_q).item(),
    }


def main():
    points = [
        (1.0 / 5.0, 1.0 / 7.0, 1.0 / 11.0),
        (1.0 / 3.0, -1.0 / 5.0, 1.0 / 7.0),
        (-2.0 / 5.0, 1.0 / 4.0, 1.0 / 6.0),
        (0.0, 0.0, 0.0),
        (0.0, 0.0, 1.0),
    ]
    rows = [audit_point(lam, point) for lam in (-1, 0, 1) for point in points]
    print(json.dumps(rows, indent=2, sort_keys=True))
    max_errors = {
        key: max(row[key] for row in rows)
        for key in ("Q_T_abs_error", "Q_S_abs_error", "Q_abs_error", "raw_twist_abs_error", "pair_idempotence_max", "screen_idempotence_max")
    }
    print(json.dumps({"max_errors": max_errors}, sort_keys=True))


if __name__ == "__main__":
    main()
