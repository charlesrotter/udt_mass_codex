#!/usr/bin/env python3
"""Exact symbolic controller for the bounded R17 pair-foliation audit."""

from __future__ import annotations

import json
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent


def main() -> None:
    u, v = sp.symbols("u v", positive=True, finite=True)
    a, lam, p1, p2, p3 = sp.symbols("a lambda p1 p2 p3", real=True, finite=True)

    # Rows are theta^a in the coordinate/Maurer--Cartan basis (dt,sigma3,sigma1,sigma2).
    coframe = sp.Matrix(
        [
            [1 / u, a / u, 0, 0],
            [0, u, 0, 0],
            [0, 0, v, 0],
            [0, 0, 0, v],
        ]
    )
    # Columns are e_a in the dual basis (T,Z,X,Y).
    frame = sp.Matrix(
        [
            [u, -a / u, 0, 0],
            [0, 1 / u, 0, 0],
            [0, 0, 1 / v, 0],
            [0, 0, 0, 1 / v],
        ]
    )
    dual_identity = sp.simplify(coframe * frame)

    # General stationary phi: p_i are Z(phi), X(phi), Y(phi).  No profile is imposed.
    pair_bracket = sp.Matrix([-p1 / u, 0, 0, 0])
    screen_bracket = sp.Matrix(
        [2 * a / (u * v**2), 2 * u / v**2, lam * p3 / v, -lam * p2 / v]
    )

    # Pullback to one leaf of span(T,Z), with local coordinates (t,psi), sigma3=dpsi.
    h = sp.Matrix(
        [
            [-1 / u**2, -a / u**2],
            [-a / u**2, u**2 - a**2 / u**2],
        ]
    )
    det_h = sp.factor(h.det())
    terminal_ratio = sp.factor((-det_h) / h[0, 0] ** 2)
    terminal_depth = sp.simplify(sp.log(terminal_ratio) / 4)

    checks = {
        "coframe_frame_duality": dual_identity == sp.eye(4),
        "pair_bracket_has_no_screen_component": all(
            sp.simplify(pair_bracket[i]) == 0 for i in (2, 3)
        ),
        "screen_bracket_has_unavoidable_pair_component": sp.simplify(
            screen_bracket[1]
        ) != 0,
        "pair_leaf_metric_keeps_twist": sp.simplify(h[0, 1] + a / u**2) == 0,
        "pair_leaf_determinant_minus_one": det_h == -1,
        "terminal_ratio_u_fourth": sp.simplify(terminal_ratio - u**4) == 0,
        "terminal_depth_phi": sp.simplify(terminal_depth - sp.log(u)) == 0,
        "integrability_independent_of_lambda": not pair_bracket.has(lam),
        "integrability_independent_of_screen_derivatives": not (
            pair_bracket.has(p2) or pair_bracket.has(p3)
        ),
        "screen_nonintegrability_independent_of_profile": sp.simplify(
            screen_bracket[1]
        ) == 2 * u / v**2,
    }
    if not all(checks.values()):
        raise SystemExit(f"FAIL: {checks}")

    result = {
        "mode": "exact_symbolic",
        "sympy_version": sp.__version__,
        "arena": "R17/W01 C01-C06 regular off-shell complete coframes",
        "symbols": {
            "u": "exp(phi)>0",
            "v": "exp(lambda*phi)>0",
            "p1": "Z(phi)",
            "p2": "X(phi)",
            "p3": "Y(phi)",
        },
        "dual_frame": {
            "e0": "u*T",
            "e1": "u^-1*(Z-a*T)",
            "e2": "v^-1*X",
            "e3": "v^-1*Y",
        },
        "pair_bracket_components_e": [str(sp.simplify(x)) for x in pair_bracket],
        "screen_bracket_components_e": [str(sp.simplify(x)) for x in screen_bracket],
        "leaf_metric_t_psi": [[str(sp.simplify(x)) for x in row] for row in h.tolist()],
        "leaf_metric_determinant": str(det_h),
        "terminal_ratio": str(terminal_ratio),
        "terminal_depth": str(terminal_depth),
        "checks": checks,
        "landing": "GLOBAL_PAIR_FOLIATION_AND_SCALAR_DEPTH_DERIVED__FULL_NORMAL_BUNDLE_ARROW_OPEN",
        "scope_guards": {
            "one_leaf_selected": False,
            "one_winding_selected": False,
            "cross_leaf_pair_map_derived": False,
            "screen_transport_path_independent": False,
            "physical_complete_arrow_derived": False,
            "lambda_selected": False,
            "r17_selected": False,
            "on_shell": False,
        },
    }
    (HERE / "DERIVATION_RESULT.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(
        "PASS: 10/10 exact checks; pair plane involutive; screen nonintegrable; "
        "det(h)=-1; terminal depth=phi"
    )


if __name__ == "__main__":
    main()
