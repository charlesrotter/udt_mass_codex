#!/usr/bin/env python3
"""Independent direct-loop and neighboring-ray check of the G79 endpoint map."""

from __future__ import annotations

import csv
import io
import json
import math
import subprocess
from pathlib import Path

import numpy as np
from scipy.integrate import solve_ivp


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
BASE = "26f90fc22271c682fe00ef350eac01b3113a5b9e"
PROFILE_PATH = "udt_cmb_G75_center_regular_axial_profile_family_2026-08-11/PROFILE_ATLAS.tsv"
DELTAS = (1.0e-4, 5.0e-5)


def number(text: str) -> float:
    if "/" in text:
        left, right = text.split("/", 1)
        return float(left) / float(right)
    return float(text)


def selected() -> tuple[dict[str, str], float, tuple[float, float, float]]:
    raw = subprocess.check_output(["git", "show", f"{BASE}:{PROFILE_PATH}"], cwd=ROOT)
    rows = list(csv.DictReader(io.StringIO(raw.decode("utf-8")), delimiter="\t"))
    row = next(item for item in rows if item["shape_id"] != "ZERO")
    assert row["profile_id"] == "G75_AM_S01_E05" and row["q_of_s"] == "s**2/20"
    return row, number(row["lapse_a"]), (0.0, 0.0, 0.05)


def fields(a: float, c: tuple[float, float, float], x: float) -> tuple[float, float, float, float]:
    c0, c1, c2 = c
    A = 1.0 + a * x**2
    Ar = 2.0 * a * x
    h = c0 * x**2 + c1 * x**4 + c2 * x**6
    hr = 2.0 * c0 * x + 4.0 * c1 * x**3 + 6.0 * c2 * x**5
    return A, Ar, h, hr


def metric_first(a: float, c: tuple[float, float, float], position: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    _, x, theta, _ = position
    A, Ar, h, hr = fields(a, c, float(x))
    sine, cosine = math.sin(float(theta)), math.cos(float(theta))
    g = np.zeros((4, 4), dtype=np.float64)
    g[0, 0], g[1, 1], g[2, 2], g[3, 3] = -A, 1.0 / A, x**2, x**2 * sine**2
    g[0, 3] = g[3, 0] = h * sine**2
    dg = np.zeros((4, 4, 4), dtype=np.float64)
    dg[1, 0, 0] = -Ar
    dg[1, 1, 1] = -Ar / A**2
    dg[1, 2, 2] = 2.0 * x
    dg[1, 3, 3] = 2.0 * x * sine**2
    dg[1, 0, 3] = dg[1, 3, 0] = hr * sine**2
    dg[2, 3, 3] = 2.0 * x**2 * sine * cosine
    dg[2, 0, 3] = dg[2, 3, 0] = 2.0 * h * sine * cosine
    return g, dg


def christoffel(a: float, c: tuple[float, float, float], position: np.ndarray) -> np.ndarray:
    g, dg = metric_first(a, c, position)
    inverse = np.linalg.inv(g)
    Gamma = np.zeros((4, 4, 4), dtype=np.float64)
    for rho in range(4):
        for mu in range(4):
            for nu in range(4):
                for lam in range(4):
                    Gamma[rho, mu, nu] += 0.5 * inverse[rho, lam] * (
                        dg[mu, lam, nu] + dg[nu, lam, mu] - dg[lam, mu, nu]
                    )
    return Gamma


def initial(a: float, c: tuple[float, float, float]) -> tuple[np.ndarray, ...]:
    position = np.array([0.0, 0.25, math.pi / 2.0, 0.0], dtype=np.float64)
    A, _, h, _ = fields(a, c, 0.25)
    block = A * 0.25**2 + h**2
    u = np.array([1.0 / math.sqrt(A), 0.0, 0.0, 0.0])
    radial = np.array([0.0, math.sqrt(A), 0.0, 0.0])
    e_theta = np.array([0.0, 0.0, 4.0, 0.0])
    e_psi = np.array([h / (math.sqrt(A) * math.sqrt(block)), 0.0, 0.0, math.sqrt(A) / math.sqrt(block)])
    return position, u, radial, e_theta, e_psi


def integrate(a: float, c: tuple[float, float, float], k0: np.ndarray, end: float | None, with_screen: bool) -> object:
    position, _, _, e_theta, e_psi = initial(a, c)
    if with_screen:
        y0 = np.concatenate((position, k0, e_theta, e_psi))
    else:
        y0 = np.concatenate((position, k0))

    def rhs(_s: float, state: np.ndarray) -> np.ndarray:
        x, k = state[:4], state[4:8]
        Gamma = christoffel(a, c, x)
        dk = np.zeros(4)
        for rho in range(4):
            for mu in range(4):
                for nu in range(4):
                    dk[rho] -= Gamma[rho, mu, nu] * k[mu] * k[nu]
        if not with_screen:
            return np.concatenate((k, dk))
        E = state[8:16].reshape(2, 4)
        dE = np.zeros((2, 4))
        for aa in range(2):
            for rho in range(4):
                for mu in range(4):
                    for nu in range(4):
                        dE[aa, rho] -= Gamma[rho, mu, nu] * k[mu] * E[aa, nu]
        return np.concatenate((k, dk, dE.ravel()))

    def event(_s: float, state: np.ndarray) -> float:
        return float(state[1] - 1.0)

    event.terminal = True
    event.direction = 1.0
    interval = (0.0, 10.0 if end is None else end)
    return solve_ivp(
        rhs,
        interval,
        y0,
        method="DOP853",
        rtol=2.0e-12,
        atol=2.0e-14,
        max_step=1.0 / 400.0,
        events=event if end is None else None,
        dense_output=True,
    )


def relative(left: np.ndarray, right: np.ndarray) -> float:
    return float(np.linalg.norm(left - right) / max(1.0, np.linalg.norm(left), np.linalg.norm(right)))


def main() -> None:
    _, a, c = selected()
    production = json.loads((HERE / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    reference_D = np.asarray(production["endpoint"]["D"], dtype=np.float64)
    position0, u, radial, e_theta, e_psi = initial(a, c)
    central = integrate(a, c, u + radial, None, True)
    assert central.success and len(central.t_events[0]) == 1
    affine = float(central.t_events[0][0])
    central_state = np.asarray(central.sol(affine), dtype=np.float64)
    endpoint = central_state[:4]
    endpoint_k = central_state[4:8]
    endpoint_screen = central_state[8:16].reshape(2, 4)
    endpoint_g, _ = metric_first(a, c, endpoint)

    by_delta: dict[float, np.ndarray] = {}
    max_null = 0.0
    for delta in DELTAS:
        D = np.zeros((2, 2))
        for column, screen in enumerate((e_theta, e_psi)):
            plus_k = u + radial * math.cos(delta) + screen * math.sin(delta)
            minus_k = u + radial * math.cos(delta) - screen * math.sin(delta)
            plus = integrate(a, c, plus_k, affine, False)
            minus = integrate(a, c, minus_k, affine, False)
            assert plus.success and minus.success
            jacobi = (plus.y[:4, -1] - minus.y[:4, -1]) / (2.0 * delta)
            D[:, column] = endpoint_screen @ endpoint_g @ jacobi
            for solution in (plus, minus):
                x, k = solution.y[:4, -1], solution.y[4:8, -1]
                g, _ = metric_first(a, c, x)
                max_null = max(max_null, abs(float(k @ g @ k)))
        by_delta[delta] = D

    coarse, fine = (by_delta[value] for value in DELTAS)
    A_receiver = fields(a, c, 0.25)[0]
    A_source = fields(a, c, float(endpoint[1]))[0]
    initial_g, _ = metric_first(a, c, position0)
    omega_receiver = -float(initial_g[0] @ (u + radial)) / math.sqrt(A_receiver)
    omega_source = -float(endpoint_g[0] @ endpoint_k) / math.sqrt(A_source)
    one_plus_z = omega_source / omega_receiver
    analytic = math.sqrt(A_receiver / A_source)
    output = {
        "schema": "udt-cmb-g79-independent-neighboring-ray-v1",
        "status": "PASS",
        "profile_id": "G75_AM_S01_E05",
        "method": "independent direct-loop Christoffel central screen plus finite-difference neighboring null geodesics; no production Riemann or Jacobi equation",
        "central_affine_over_R": affine,
        "production_affine_over_R": production["endpoint"]["affine_over_R"],
        "affine_absolute_difference": abs(affine - production["endpoint"]["affine_over_R"]),
        "coarse_delta": DELTAS[0],
        "fine_delta": DELTAS[1],
        "coarse_D": coarse.tolist(),
        "fine_D": fine.tolist(),
        "coarse_fine_relative": relative(coarse, fine),
        "fine_production_relative": relative(fine, reference_D),
        "independent_dA_over_R": math.sqrt(abs(float(np.linalg.det(fine)))),
        "production_dA_over_R": production["distance"]["dA_over_R"],
        "one_plus_z_independent": one_plus_z,
        "one_plus_z_analytic": analytic,
        "redshift_absolute_difference": abs(one_plus_z - analytic),
        "max_endpoint_null_absolute": max_null,
    }
    assert output["affine_absolute_difference"] < 1.0e-8
    assert output["fine_production_relative"] < 2.0e-4
    assert output["redshift_absolute_difference"] < 1.0e-10
    assert output["max_endpoint_null_absolute"] < 1.0e-9
    (HERE / "INDEPENDENT_VERIFICATION.json").write_text(
        json.dumps(output, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
