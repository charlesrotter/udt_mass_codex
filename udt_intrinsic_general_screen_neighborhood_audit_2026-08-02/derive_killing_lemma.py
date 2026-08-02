#!/usr/bin/env python3
"""Exact residual Killing-equation lemma after invariant gradients remove spatial components."""

from __future__ import annotations

import json
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent


def main() -> int:
    gtt = sp.symbols("g_tt", nonzero=True)
    gt1, gt2, gt3 = sp.symbols("g_t1 g_t2 g_t3", real=True)
    coefficient = sp.Matrix([
        [2*gtt, 0, 0, 0],
        [gt1, gtt, 0, 0],
        [gt2, 0, gtt, 0],
        [gt3, 0, 0, gtt],
    ])
    determinant = sp.factor(coefficient.det())
    assert determinant == 2*gtt**4
    assert determinant != 0
    result = {
        "schema": "udt-stationary-residual-Killing-lemma-1.0",
        "status": "PASS_EXACT",
        "premise": "invariant_gradient_J_nonzero_forces_all_spatial_components_of_X_to_zero",
        "remaining_candidate": "X=f(t,x1,x2,x3)*partial_t",
        "equations": [
            "(L_X g)_tt=2*g_tt*partial_t(f)=0",
            "(L_X g)_ti=g_ti*partial_t(f)+g_tt*partial_i(f)=0",
        ],
        "coefficient_determinant": str(determinant),
        "conclusion": "all_four_derivatives_of_f_zero__f_constant",
        "covers_time_dependent_candidate_coefficients": True,
        "requires_stationary_metric_and_g_tt_nonzero": True,
        "does_not_assert_stationarity_under_arbitrary_metric_perturbation": True,
    }
    (HERE / "KILLING_LEMMA_CERTIFICATE.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
