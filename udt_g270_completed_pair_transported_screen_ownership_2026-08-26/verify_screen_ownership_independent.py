#!/usr/bin/env python3
"""Implementation-distinct exact-rational G270 replay."""

from __future__ import annotations

import argparse
from fractions import Fraction as F
import json
from pathlib import Path
import random


ROOT = Path(__file__).resolve().parent
OUT = ROOT / "INDEPENDENT_VERIFICATION.json"
LANDING = (
    "FULL_SUPPLIED_REALIZATION_EVALUATES_TRANSPORTED_SCREEN_MISMATCH__"
    "COMPLETED_PAIR_DUAL_RECIPROCITY_NORMALIZES_ONLY_THE_INTRINSIC_PULLBACK__"
    "EXACT_SAME_PULLBACK_TILTED_NULL_RIBBONS_HAVE_DIFFERENT_W__"
    "NO_UNIVERSAL_W_VALUE_POPULATION_HISTORY_DISTANCE_OR_XMAX_SELECTION"
)


def dot(x: tuple[F, F, F], y: tuple[F, F, F]) -> F:
    return -x[0] * y[0] + x[1] * y[1] + x[2] * y[2]


def frame(r: F, w: F) -> dict[str, object]:
    gamma = (r + 1 / r + r * w * w) / 2
    long = gamma - 1 / r
    u = (gamma, long, w)
    k = (F(1), F(1), F(0))
    khat = tuple(r * x for x in k)
    n = tuple(khat[i] - u[i] for i in range(3))
    h = ((dot(u, u), dot(u, k)), (dot(k, u), dot(k, k)))
    return {"gamma": gamma, "u": u, "k": k, "khat": khat, "n": n, "h": h}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--no-write", action="store_true")
    args = parser.parse_args()

    rng = random.Random(270826)
    assertions = 0
    cases = 12_000
    tilted = 0
    for _ in range(cases):
        r = F(rng.randint(1, 31), rng.randint(1, 31))
        w = F(rng.randint(-40, 40), rng.randint(1, 23))
        data = frame(r, w)
        u = data["u"]
        k = data["k"]
        khat = data["khat"]
        n = data["n"]
        h = data["h"]

        assert dot(u, u) == -1
        assert -dot(k, u) == 1 / r
        assert dot(n, n) == 1
        assert dot(u, n) == 0
        assert dot(khat, khat) == 0
        assert -dot(u, khat) == 1
        assert tuple(u[i] + n[i] for i in range(3)) == khat
        assert h == ((F(-1), -1 / r), (-1 / r, F(0)))
        assert h[0][0] * h[1][1] - h[0][1] * h[1][0] == -1 / (r * r)
        assert w * w >= 0
        assert data["gamma"] == (r + 1 / r) / 2 + r * w * w / 2
        m = 1 / r
        hs = ((h[0][0], h[0][1] / m), (h[1][0] / m, h[1][1] / (m * m)))
        assert hs == ((F(-1), F(-1)), (F(-1), F(0)))
        assert hs[0][0] * hs[1][1] - hs[0][1] * hs[1][0] == -1

        w_alt = abs(w) + 1
        alt = frame(r, w_alt)
        assert alt["h"] == h
        assert w_alt * w_alt != w * w
        assert alt["gamma"] != data["gamma"]
        assertions += 17
        tilted += int(w != 0)

    # Smooth nonconstant ribbon checks, coded without production imports or SymPy.
    smooth_cases = 1001
    off_axis_cases = 0
    tau_values = tuple(F(j, 5) for j in range(-20, 21) if j != 0)
    for i in range(smooth_cases):
        lam = F(i, 1000)
        r = 1 + lam
        w = lam
        data = frame(r, w)
        gamma_prime = (1 - 1 / (r * r) + w * w + 2 * r * w) / 2
        long_prime = gamma_prime + 1 / (r * r)
        du = (gamma_prime, long_prime, F(1))
        assert dot(data["u"], du) == 0
        assert dot(data["k"], du) == 1 / (r * r)
        assert data["h"] == ((F(-1), -1 / r), (-1 / r, F(0)))
        assert data["h"][0][0] * data["h"][1][1] - data["h"][0][1] ** 2 < 0
        assertions += 4

        coefficient = 4 * lam * lam + 4 * lam + 2
        for tau in tau_values:
            f_tau = data["u"]
            f_lam = tuple(data["k"][j] + tau * du[j] for j in range(3))
            h00 = dot(f_tau, f_tau)
            h01 = dot(f_tau, f_lam)
            h11 = dot(f_lam, f_lam)
            det = h00 * h11 - h01 * h01
            expected_det = -(coefficient * tau * tau + 2 * tau + 1) / (r * r)
            assert h00 == -1
            assert h01 == -1 / r
            assert det == expected_det
            assert det < 0
            assertions += 4
            off_axis_cases += 1

    fixed_r = F(2)
    mutual_values = set()
    for i in range(101):
        w = F(i, 10)
        mutual_values.add(1 / frame(fixed_r, w)["gamma"])
    assert len(mutual_values) == 101
    assertions += 1

    result = {
        "status": "PASS",
        "expected_landing": LANDING,
        "cases": cases,
        "tilted_cases": tilted,
        "smooth_ribbon_axis_cases": smooth_cases,
        "smooth_ribbon_off_axis_cases": off_axis_cases,
        "smooth_ribbon_tau_range": [str(min(tau_values)), str(max(tau_values))],
        "assertions": assertions,
        "fixed_r_distinct_transport_values": len(mutual_values),
        "production_imported": False,
        "production_result_read": False,
    }
    rendered = json.dumps(result, indent=2, sort_keys=True)
    if not args.no_write:
        OUT.write_text(rendered + "\n", encoding="utf-8")
    print(rendered)


if __name__ == "__main__":
    main()
