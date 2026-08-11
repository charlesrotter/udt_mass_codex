#!/usr/bin/env python3
"""Independent finite-difference null-geodesic bundle check for all G68 profiles.

This verifier does not import the production solver and does not construct Riemann or integrate the
Jacobi equation. It differentiates a separately implemented family of null geodesics instead.
"""

from __future__ import annotations

import csv
import json
import math
from dataclasses import dataclass
from pathlib import Path

import numpy as np
from scipy.integrate import solve_ivp


HERE = Path(__file__).resolve().parent
DELTAS = (1.0e-4, 5.0e-5)  # NUMERIC: frozen independent-difference controls.


@dataclass(frozen=True)
class Profile:
    profile_id: str
    family: str
    lapse_a: float
    shape: str
    epsilon: float


def number(text: str) -> float:
    if "/" in text:
        left, right = text.split("/", 1)
        return float(left) / float(right)
    return float(text)


def profiles() -> list[Profile]:
    with (HERE / "PROFILE_UNIVERSE.tsv").open(newline="", encoding="utf-8") as stream:
        rows = list(csv.DictReader(stream, delimiter="\t"))
    out = [Profile(row["profile_id"], row["metric_family"], number(row["lapse_a"]), row["mix_shape"], number(row["mix_epsilon"])) for row in rows]
    if len(out) != 21 or len({row.profile_id for row in out}) != 21:
        raise AssertionError("wrong independent profile universe")
    return out


def fields(profile: Profile, r: float) -> tuple[float, float, float, float]:
    A = 1.0 + profile.lapse_a * r**2
    Ar = 2.0 * profile.lapse_a * r
    e = profile.epsilon
    if profile.family == "F01":
        return A, Ar, 0.0, 0.0
    if profile.shape == "PERSISTENT":
        return A, Ar, e * r**2, 2.0 * e * r
    if profile.shape == "TAPERED":
        return A, Ar, e * r**2 * (1.0 - r) ** 2, e * (2.0 * r - 6.0 * r**2 + 4.0 * r**3)
    if profile.shape == "SIGN_CHANGING":
        return A, Ar, e * r**2 * (1.0 - 2.0 * r), e * (2.0 * r - 6.0 * r**2)
    raise ValueError(profile.shape)


def metric_and_first(profile: Profile, x: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    _, r, theta, _ = x
    A, Ar, h, hr = fields(profile, float(r))
    sine, cosine = math.sin(float(theta)), math.cos(float(theta))
    g = np.zeros((4, 4))
    g[0, 0], g[1, 1], g[2, 2], g[3, 3] = -A, 1.0 / A, r**2, r**2 * sine**2
    g[0, 3] = g[3, 0] = h * sine**2
    partial = np.zeros((4, 4, 4))
    partial[1, 0, 0] = -Ar
    partial[1, 1, 1] = -Ar / A**2
    partial[1, 2, 2] = 2.0 * r
    partial[1, 3, 3] = 2.0 * r * sine**2
    partial[1, 0, 3] = partial[1, 3, 0] = hr * sine**2
    partial[2, 3, 3] = 2.0 * r**2 * sine * cosine
    partial[2, 0, 3] = partial[2, 3, 0] = 2.0 * h * sine * cosine
    return g, partial


def christoffel(profile: Profile, x: np.ndarray) -> np.ndarray:
    g, dg = metric_and_first(profile, x)
    inverse = np.linalg.inv(g)
    Gamma = np.zeros((4, 4, 4))
    # Deliberately use direct loops rather than the production tensor assembly.
    for rho in range(4):
        for mu in range(4):
            for nu in range(4):
                total = 0.0
                for lam in range(4):
                    total += inverse[rho, lam] * (dg[mu, lam, nu] + dg[nu, lam, mu] - dg[lam, mu, nu])
                Gamma[rho, mu, nu] = 0.5 * total
    return Gamma


def initial(profile: Profile) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    x = np.array([0.0, 0.25, math.pi / 2.0, 0.0])
    A, _, h, _ = fields(profile, 0.25)
    D = A * 0.25**2 + h**2
    u = np.array([1.0 / math.sqrt(A), 0.0, 0.0, 0.0])
    radial = np.array([0.0, math.sqrt(A), 0.0, 0.0])
    theta = np.array([0.0, 0.0, 4.0, 0.0])
    psi = np.array([h / (math.sqrt(A) * math.sqrt(D)), 0.0, 0.0, math.sqrt(A) / math.sqrt(D)])
    return x, u, radial, theta, psi


def integrate_geodesic(profile: Profile, k0: np.ndarray, end_s: float) -> object:
    x0, _, _, _, _ = initial(profile)
    state0 = np.concatenate((x0, k0))

    def rhs(_s: float, state: np.ndarray) -> np.ndarray:
        x, k = state[:4], state[4:]
        Gamma = christoffel(profile, x)
        acceleration = np.zeros(4)
        for rho in range(4):
            for mu in range(4):
                for nu in range(4):
                    acceleration[rho] -= Gamma[rho, mu, nu] * k[mu] * k[nu]
        return np.concatenate((k, acceleration))

    return solve_ivp(rhs, (0.0, end_s), state0, method="DOP853", rtol=2.0e-12, atol=2.0e-14, max_step=1.0 / 400.0)


def relative(left: np.ndarray, right: np.ndarray) -> float:
    return float(np.linalg.norm(left - right) / max(1.0, np.linalg.norm(left), np.linalg.norm(right)))


def main() -> None:
    production = json.loads((HERE / "FINITE_PATH_RESULT.json").read_text(encoding="utf-8"))
    by_id = {row["profile_id"]: row for row in production["profiles"]}
    rows = []
    stdout_lines: list[str] = []
    for profile in profiles():
        reference = by_id[profile.profile_id]
        end_s = float(reference["affine_final"])
        endpoint = np.asarray(reference["endpoint_coordinates"])
        endpoint_screen = np.asarray(reference["endpoint_screen"])
        reference_D = np.asarray(reference["endpoint_D"])
        endpoint_g, _ = metric_and_first(profile, endpoint)
        x0, u, radial, e_theta, e_psi = initial(profile)
        columns_by_delta: dict[float, np.ndarray] = {}
        max_null = 0.0
        for delta in DELTAS:
            D_bundle = np.zeros((2, 2))
            for column, screen in enumerate((e_theta, e_psi)):
                plus_k = u + radial * math.cos(delta) + screen * math.sin(delta)
                minus_k = u + radial * math.cos(delta) - screen * math.sin(delta)
                plus = integrate_geodesic(profile, plus_k, end_s)
                minus = integrate_geodesic(profile, minus_k, end_s)
                if not (plus.success and minus.success):
                    raise AssertionError(f"bundle geodesic failed: {profile.profile_id}")
                jacobi = (plus.y[:4, -1] - minus.y[:4, -1]) / (2.0 * delta)
                D_bundle[:, column] = endpoint_screen @ endpoint_g @ jacobi
                for solution in (plus, minus):
                    x, k = solution.y[:4, -1], solution.y[4:, -1]
                    g, _ = metric_and_first(profile, x)
                    max_null = max(max_null, abs(float(k @ g @ k)))
            columns_by_delta[delta] = D_bundle
        coarse, fine = (columns_by_delta[delta] for delta in DELTAS)
        row = {
            "profile_id": profile.profile_id,
            "coarse_delta": DELTAS[0],
            "fine_delta": DELTAS[1],
            "coarse_D": coarse.tolist(),
            "fine_D": fine.tolist(),
            "coarse_fine_relative": relative(coarse, fine),
            "fine_reference_relative": relative(fine, reference_D),
            "max_endpoint_null_absolute": max_null,
        }
        rows.append(row)
        line = f'{profile.profile_id} {row["fine_reference_relative"]}'
        stdout_lines.append(line)
        print(line, flush=True)

    max_error = max(row["fine_reference_relative"] for row in rows)
    max_delta = max(row["coarse_fine_relative"] for row in rows)
    max_null = max(row["max_endpoint_null_absolute"] for row in rows)
    payload = {
        "schema": "UDT_CMB_G68_GEODESIC_BUNDLE_VERIFY_V1",
        "method": "separate direct-loop Christoffel implementation; finite differences of null geodesic family; no Riemann or Jacobi integration",
        "rows": rows,
        "profile_rows": len(rows),
        "max_fine_reference_relative": max_error,
        "max_coarse_fine_relative": max_delta,
        "max_endpoint_null_absolute": max_null,
        "passed": bool(len(rows) == 21 and max_error <= 2.0e-4),
    }
    (HERE / "BUNDLE_VERIFICATION_RESULT.json").write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    final_line = json.dumps({key: payload[key] for key in ("profile_rows", "max_fine_reference_relative", "max_coarse_fine_relative", "max_endpoint_null_absolute", "passed")}, sort_keys=True)
    stdout_lines.append(final_line)
    (HERE / "BUNDLE_VERIFICATION_STDOUT.txt").write_text("\n".join(stdout_lines) + "\n", encoding="utf-8")
    print(final_line)
    if not payload["passed"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
