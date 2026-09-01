#!/usr/bin/env python3
"""Shared-code hostile regression mutations for the G311 production theorem."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import derive_covariant_response as production


def run() -> dict[str, object]:
    hs = production.exact_pair_basis()
    eta = production.metric()
    e0 = (production.F(1), production.F(0), production.F(0), production.F(0))
    e1 = (production.F(0), production.F(1), production.F(0), production.F(0))
    uflat, nflat = production.lower(e0), production.lower(e1)
    wrong = production.zeros()
    for i in range(4):
        for j in range(4):
            wrong[i][j] = 2 * (uflat[i] * uflat[j] - nflat[i] * nflat[j])

    lambda_at_zero = production.scale(production.F(1), eta)
    lambda_at_one = production.scale(production.F(2), eta)
    variable_trace_balances = all(
        production.tensor_pair(response, h) == 0
        for response in (lambda_at_zero, lambda_at_one)
        for h in hs
    )
    ricci_flrw_t0 = production.zeros()
    for i, value in enumerate(
        (production.F(-6), production.F(2), production.F(2), production.F(2))
    ):
        ricci_flrw_t0[i][i] = value
    zero_weyl_quadratic = production.zeros()
    response_choice_detected = (
        any(production.tensor_pair(ricci_flrw_t0, h) != 0 for h in hs)
        and all(production.tensor_pair(zero_weyl_quadratic, h) == 0 for h in hs)
    )

    catches = {
        "wrong_reciprocal_sign_is_not_tracefree": production.tensor_trace(wrong) != 0,
        "single_radial_pair_rank_is_one": production.rank([production.flatten(hs[0])]) == 1,
        "eight_plane_mutation_is_rank_deficient": production.rank([production.flatten(h) for h in hs[:8]]) == 8,
        "nonzero_pure_trace_response_refutes_full_E_zero": all(
            production.tensor_pair(production.scale(production.F(7), eta), h) == 0 for h in hs
        ),
        "variable_lambda_refutes_constant_from_pointwise_balance": (
            variable_trace_balances and production.F(2) != 0
        ),
        "response_choice_is_detected_by_flrw_twin": response_choice_detected,
    }
    assert all(catches.values())
    return {
        "catches": catches,
        "caught": sum(catches.values()),
        "evidence_grade": "SHARED_CODE_REGRESSION_NOT_INDEPENDENT_CONFIRMATION",
        "expected": len(catches),
        "verdict": "PASS",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    payload = json.dumps(run(), indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(payload, encoding="utf-8")
    else:
        print(payload, end="")


if __name__ == "__main__":
    main()
