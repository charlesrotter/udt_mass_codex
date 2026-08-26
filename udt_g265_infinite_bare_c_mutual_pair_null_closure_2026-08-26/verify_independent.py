#!/usr/bin/env python3
"""Implementation-distinct numerical G265 replay. Writes no files."""

import json
import math


def gauss8(fn, a, b, panels=80):
    nodes = (
        -0.9602898564975363,
        -0.7966664774136267,
        -0.5255324099163290,
        -0.1834346424956498,
        0.1834346424956498,
        0.5255324099163290,
        0.7966664774136267,
        0.9602898564975363,
    )
    weights = (
        0.1012285362903763,
        0.2223810344533745,
        0.3137066458778873,
        0.3626837833783620,
        0.3626837833783620,
        0.3137066458778873,
        0.2223810344533745,
        0.1012285362903763,
    )
    total = 0.0
    width = (b - a) / panels
    for panel in range(panels):
        left = a + panel * width
        mid = left + width / 2
        half = width / 2
        total += half * sum(w * fn(mid + half * x) for x, w in zip(nodes, weights))
    return total


def rk4_null_time(f, a, b, steps=20000):
    h = (b - a) / steps
    r = a
    t = 0.0
    for _ in range(steps):
        fun = lambda x: 1.0 / f(x)
        k1 = fun(r)
        k2 = fun(r + h / 2)
        k3 = fun(r + h / 2)
        k4 = fun(r + h)
        t += h * (k1 + 2 * k2 + 2 * k3 + k4) / 6
        r += h
    return t


def main() -> None:
    profiles = {
        "flat": lambda r: 1.0,
        "quiet_comparator": lambda r: 1.0 + 0.4 / r,
        "alpha_two": lambda r: 1.0 + 0.3 * r * r,
        "g264_bump": lambda r: 1.0 + 7.0 * (r / 1.3) ** 2 * math.exp(-(r / 1.3) ** 2),
    }
    intervals = ((0.7, 1.1), (0.9, 1.8), (1.2, 2.7))
    assertions = 0
    rows = []
    for name, f in profiles.items():
        for a, b in intervals:
            dopt = gauss8(lambda r: 1.0 / f(r), a, b)
            dopt_rk = rk4_null_time(f, a, b)
            proper = gauss8(lambda r: 1.0 / math.sqrt(f(r)), a, b)
            assert abs(dopt - dopt_rk) < 2e-11
            assertions += 1
            na, nb = math.sqrt(f(a)), math.sqrt(f(b))
            arrow = nb / na
            assert abs(arrow * (na / nb) - 1.0) < 2e-15
            assertions += 1
            va = proper / (na * dopt)
            vb = proper / (nb * dopt)
            assert abs(va / vb - arrow) < 2e-13
            assertions += 1
            delta = math.log(na / nb)
            mgeo = proper / (math.sqrt(na * nb) * dopt)
            even = 1.0 / math.cosh(delta)
            if name == "flat":
                assert abs(dopt - proper) < 2e-14
                assert abs(va - vb) < 2e-14
                assert abs(mgeo - even) < 2e-14
                assertions += 3
            else:
                # At least one nonflat interval must expose every stronger closure.
                assertions += int(abs(dopt - proper) > 1e-6)
                assertions += int(abs(va - vb) > 1e-6)
            rows.append(
                {
                    "profile": name,
                    "a": a,
                    "b": b,
                    "optical": dopt,
                    "proper": proper,
                    "arrow_ab": arrow,
                    "speed_a_over_cE": va,
                    "speed_b_over_cE": vb,
                    "symmetric_speed": mgeo,
                    "sech_delta": even,
                }
            )
    assert assertions == 63
    print(
        json.dumps(
            {
                "status": "PASS",
                "assertions": assertions,
                "profiles": len(profiles),
                "intervals_per_profile": len(intervals),
                "rows": rows,
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
