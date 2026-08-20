#!/usr/bin/env python3
"""Exact symbolic production derivation for G186."""

from __future__ import annotations

import json

import sympy as sp


LANDING = (
    "NONRADIAL_COMPLETED_PAIR_CHANNELS_RESOLVE_WITHOUT_EXTRA_SCALAR"
    "__CLOCK_ANGULAR_NORM_CONTROLS_DEPTH"
    "__FULL_ANGULAR_GRAM_CONTROLS_TAPE_SHIFT_AND_LOCAL_SCREEN"
)


def zero_matrix(matrix: sp.Matrix) -> bool:
    return all(sp.simplify(entry) == 0 for entry in matrix)


def main() -> None:
    p, r, v = sp.symbols("p r v", positive=True, real=True)
    w00, w01, w10, w11 = sp.symbols("w00 w01 w10 w11", real=True)

    g = sp.diag(-1 / p, p, r**2, r**2)
    J = sp.Matrix(
        [
            [1, 0],
            [0, v],
            [w00, w10],
            [w01, w11],
        ]
    )
    h = sp.simplify(J.T * g * J)

    A = sp.expand(w00**2 + w01**2)
    B = sp.expand(w10**2 + w11**2)
    C = sp.expand(w00 * w10 + w01 * w11)
    wedge2 = sp.expand(A * B - C**2)
    nu2 = sp.expand(p * r**2 * A)

    expected_h = sp.Matrix(
        [
            [-(1 - nu2) / p, r**2 * C],
            [r**2 * C, p * v**2 + r**2 * B],
        ]
    )
    m2 = sp.factor(-h.det())
    expected_m2 = sp.factor(
        (1 - nu2) * v**2 + (r**2 / p) * B - r**4 * wedge2
    )
    beta = sp.factor(h[0, 1] / h[0, 0])
    expected_beta = sp.factor(-p * r**2 * C / (1 - nu2))

    projector = sp.simplify(sp.eye(4) - J * h.inv() * J.T * g)
    projector_checks = {
        "annihilates_pair_tangents": zero_matrix(projector * J),
        "g_self_adjoint": zero_matrix(projector.T * g - g * projector),
        "idempotent": zero_matrix(projector * projector - projector),
        "rank_trace_two": sp.simplify(sp.trace(projector) - 2) == 0,
    }

    rotation = sp.Matrix([[sp.Rational(3, 5), -sp.Rational(4, 5)],
                          [sp.Rational(4, 5), sp.Rational(3, 5)]])
    W = sp.Matrix([[w00, w10], [w01, w11]])
    Wr = sp.simplify(rotation * W)
    Jr = sp.Matrix([[1, 0], [0, v], [Wr[0, 0], Wr[0, 1]], [Wr[1, 0], Wr[1, 1]]])
    rotation_invariant = zero_matrix(sp.simplify(Jr.T * g * Jr - h))

    k = sp.Integer(-3)
    Jk = J.copy()
    Jk[:, 1] = k * J[:, 1]
    hk = sp.simplify(Jk.T * g * Jk)
    reparameterization = {
        "h00_invariant": sp.simplify(hk[0, 0] - h[0, 0]) == 0,
        "h01_oriented_scaling": sp.simplify(hk[0, 1] - k * h[0, 1]) == 0,
        "h11_quadratic_scaling": sp.simplify(hk[1, 1] - k**2 * h[1, 1]) == 0,
        "m2_quadratic_scaling": sp.simplify(-hk.det() - k**2 * m2) == 0,
    }

    collinear_subs = {
        p: 4,
        r: 3,
        v: sp.Rational(1, 2),
        w00: sp.Rational(1, 12),
        w01: 0,
        w10: sp.Rational(1, 3),
        w11: 0,
    }
    noncollinear_subs = dict(collinear_subs)
    noncollinear_subs[w10] = 0
    noncollinear_subs[w11] = sp.Rational(1, 3)
    static_subs = dict(collinear_subs)
    static_subs[w00] = 0

    def witness(subs: dict[sp.Symbol, sp.Expr]) -> dict[str, object]:
        hw = sp.simplify(h.subs(subs))
        nuw = sp.simplify(nu2.subs(subs))
        phiw = sp.simplify(-sp.log(-hw[0, 0]) / 2)
        pw = sp.simplify(projector.subs(subs))
        return {
            "beta": str(sp.simplify(hw[0, 1] / hw[0, 0])),
            "h": [[str(x) for x in row] for row in hw.tolist()],
            "m2": str(sp.simplify(-hw.det())),
            "nu2": str(nuw),
            "phi_completed": str(phiw),
            "projector_trace": str(sp.simplify(sp.trace(pw))),
            "regular": bool(hw[0, 0] < 0 and hw.det() < 0),
        }

    endpoint_formula = (
        "delta_AB = phi_B-phi_A "
        "- 1/2 log[(1-nu_B^2)/(1-nu_A^2)]"
    )
    checks = {
        "beta_formula": sp.simplify(beta - expected_beta) == 0,
        "direct_pullback": zero_matrix(h - expected_h),
        "m2_formula": sp.simplify(m2 - expected_m2) == 0,
        "rotation_invariant": rotation_invariant,
        "static_clock_phi_equals_phi": sp.simplify(
            (-sp.log(-h[0, 0]) / 2).subs({w00: 0, w01: 0}) - sp.log(p) / 2
        ) == 0,
        "wedge_is_squared_angular_area": sp.factor(
            wedge2 - (w00 * w11 - w01 * w10) ** 2
        ) == 0,
        **projector_checks,
        **{f"reparam_{name}": value for name, value in reparameterization.items()},
    }

    result = {
        "audit": "G186_PRODUCTION",
        "checks": checks,
        "endpoint_response": endpoint_formula,
        "expressions": {
            "Phi": "phi - 1/2 log(1-nu^2)",
            "beta": str(expected_beta),
            "h00": str(expected_h[0, 0]),
            "h01": str(expected_h[0, 1]),
            "h11": str(expected_h[1, 1]),
            "m2": str(expected_m2),
            "nu2": str(nu2),
            "wedge2": str(sp.factor(wedge2)),
        },
        "landing": LANDING,
        "local_screen": (
            "Pi = I - J (J^T g J)^-1 J^T g; finite Jacobi response not inferred"
        ),
        "status": "PASS" if all(checks.values()) else "FAIL",
        "witnesses": {
            "collinear": witness(collinear_subs),
            "noncollinear": witness(noncollinear_subs),
            "static_clock_nonradial_ruler": witness(static_subs),
        },
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
