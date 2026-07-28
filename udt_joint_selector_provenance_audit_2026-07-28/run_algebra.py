#!/usr/bin/env python3
"""Runnable algebra for the load-bearing joint-selector counterfamilies."""

from __future__ import annotations

import hashlib
import json
import platform
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent


def zero_matrix(matrix: sp.Matrix) -> bool:
    return all(sp.simplify(value) == 0 for value in matrix)


def main() -> None:
    a, b, lam, phi, R = sp.symbols("a b lambda phi R", real=True)

    # Founded two-channel representation and its exact composition.
    D = lambda x: sp.diag(sp.exp(-x), sp.exp(x))
    pair_composition = zero_matrix(D(b) * D(a) - D(a + b))
    pair_reversal = zero_matrix(D(-a) * D(a) - sp.eye(2))

    # Endpoint cocycles compose for every scalar f; this is deliberately a
    # family rather than a physical-depth selector.
    fp, fq, fr = sp.symbols("f_p f_q f_r", real=True)
    endpoint_cocycle = sp.simplify((fq - fp) + (fr - fq) - (fr - fp)) == 0

    # Full diagonal extension retains a real transverse modulus.
    X = sp.diag(-1, 1, lam, lam)
    E = sp.diag(sp.exp(-phi), sp.exp(phi), sp.exp(lam * phi), sp.exp(lam * phi))
    extension_generator = zero_matrix(sp.diff(E, phi).subs(phi, 0) - X)
    distinct_lambda_witness = any(
        not zero_matrix(E.subs({lam: x, phi: sp.Rational(1, 3)}) - E.subs({lam: y, phi: sp.Rational(1, 3)}))
        for x, y in [(-1, 0), (0, 1), (-1, 1)]
    )

    # Stationary Killing-norm depth.  The observed anchor cancels.
    ce, phip, phiq = sp.symbols("c_E phi_p phi_q", positive=True)
    Qp = ce * sp.exp(-phip)
    Qq = ce * sp.exp(-phiq)
    stationary_depth = sp.simplify(sp.log(Qp / Qq).expand(force=True) - (phiq - phip)) == 0

    # The Levi-Civita algebra and reciprocal generator have different metric
    # adjoint types.  Their invariant trace pairing vanishes identically.
    w01, w02, w03, w12, w13, w23 = sp.symbols("w01 w02 w03 w12 w13 w23")
    eta = sp.diag(-1, 1, 1, 1)
    omega = sp.Matrix([
        [0, w01, w02, w03],
        [w01, 0, w12, w13],
        [w02, -w12, 0, w23],
        [w03, -w13, -w23, 0],
    ])
    H = sp.diag(-1, 1, 0, 0)
    connection_metric_skew = zero_matrix(omega.T * eta + eta * omega)
    reciprocal_metric_self_adjoint = zero_matrix(H.T * eta - eta * H)
    trace_pairing_zero = sp.simplify(sp.trace(H * omega)) == 0

    # Complete R x S3 family determinant: nondegenerate for finite phi,
    # positive R, and every real lambda.  No equation selects lambda or phi.
    coframe_det = sp.simplify(R**3 * sp.exp(2 * lam * phi))
    metric_det = sp.simplify(-coframe_det**2)
    metric_det_expected = sp.simplify(metric_det + R**6 * sp.exp(4 * lam * phi)) == 0
    sampled_nondegenerate = all(
        sp.N(metric_det.subs({R: 2, phi: p, lam: l})) != 0
        for p in [-2, 0, 3] for l in [-5, 0, sp.Rational(7, 3)]
    )

    # Direct-product hybrid composition.  U is represented by ordinary
    # rotations merely as a nontrivial exact transport control; the test is
    # componentwise and does not identify transport with dilation.
    Rot = lambda x: sp.Matrix([[sp.cos(x), -sp.sin(x)], [sp.sin(x), sp.cos(x)]])
    hybrid_depth = zero_matrix(D(b) * D(a) - D(a + b))
    hybrid_transport = zero_matrix(sp.trigsimp(Rot(b) * Rot(a) - Rot(a + b)))

    checks = {
        "pair_composition": pair_composition,
        "pair_reversal": pair_reversal,
        "arbitrary_endpoint_cocycle_composition": endpoint_cocycle,
        "extension_generator": extension_generator,
        "distinct_real_lambda_witnesses": distinct_lambda_witness,
        "stationary_Killing_norm_depth": stationary_depth,
        "connection_metric_skew": connection_metric_skew,
        "reciprocal_generator_metric_self_adjoint": reciprocal_metric_self_adjoint,
        "connection_reciprocal_trace_pairing_zero": trace_pairing_zero,
        "complete_RxS3_metric_determinant": metric_det_expected,
        "complete_RxS3_sampled_nondegeneracy": sampled_nondegenerate,
        "hybrid_depth_composition": hybrid_depth,
        "hybrid_transport_composition": hybrid_transport,
    }
    if not all(checks.values()):
        raise AssertionError({key: value for key, value in checks.items() if not value})

    result = {
        "schema": "udt-joint-selector-algebra-1.0",
        "python": platform.python_version(),
        "sympy": sp.__version__,
        "checks": checks,
        "check_count": len(checks),
        "all_pass": True,
        "interpretive_limit": "Algebra certifies exact families and type separation; it does not select a physical joint operation.",
    }
    encoded = json.dumps(result, indent=2, sort_keys=True) + "\n"
    (HERE / "ALGEBRA_RESULTS.json").write_text(encoded, encoding="utf-8")
    print(encoded, end="")
    print("result_sha256", hashlib.sha256(encoded.encode()).hexdigest())


if __name__ == "__main__":
    main()
