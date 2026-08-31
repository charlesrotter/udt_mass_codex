#!/usr/bin/env python3
"""Hostile formula mutations for the G309 load-bearing claims."""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path


def build_result() -> dict:
    t = 1.0
    a = math.cosh(t)
    ap = math.sinh(t)
    app = math.cosh(t)
    kt = app / a
    ks = (ap * ap + 1.0) / (a * a)
    cases = []

    wrong_scalar = 6.0 * (kt - ks)
    cases.append({
        "mutation": "wrong_scalar_curvature_relative_sign",
        "caught": abs(wrong_scalar - 12.0) > 1.0,
    })

    q_missing_constant = a * app - ap * ap
    cases.append({
        "mutation": "omit_minus_one_from_tracefree_residual",
        "caught": abs(q_missing_constant) > 0.5,
    })

    eps = 0.1
    bump = math.exp(-1.0 / (t * t))
    bp = bump * 2.0 / t**3
    bpp = bump * (4.0 / t**6 - 6.0 / t**4)
    logp = math.tanh(t) + eps * bp
    logpp = 1.0 / math.cosh(t) ** 2 + eps * bpp
    ae = math.cosh(t) * math.exp(eps * bump)
    aep = ae * logp
    aepp = ae * (logp * logp + logpp)
    qe = ae * aepp - aep * aep - 1.0
    cases.append({
        "mutation": "claim_every_positive_round_warp_satisfies_tracefree_law",
        "caught": abs(qe) > 1e-3,
    })

    false_carry = -ap / (a * a)
    cases.append({
        "mutation": "drop_warped_connection_from_normalized_hopf_time_carry",
        "caught": abs(false_carry) > 1e-3,
    })

    assert all(item["caught"] for item in cases)
    return {"status": "PASS", "hostile_cases": len(cases), "cases": cases}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = build_result()
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")


if __name__ == "__main__":
    main()
