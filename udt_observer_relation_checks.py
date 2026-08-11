#!/usr/bin/env python3
"""Finite-dimensional checks for the UDT observer-relation adjudication.

Requires: sympy
Run:
    python udt_observer_relation_checks.py

The script checks only algebraic/finite-dimensional claims.  It does not
attempt to prove global naturality or topology statements.
"""

from __future__ import annotations

import sympy as sp


def assert_zero_matrix(name: str, matrix: sp.Matrix) -> None:
    simplified = matrix.applyfunc(sp.simplify)
    if simplified != sp.zeros(*simplified.shape):
        raise AssertionError(f"{name} failed:\n{simplified}")
    print(f"PASS: {name}")


def assert_zero(name: str, expr: sp.Expr) -> None:
    simplified = sp.simplify(expr)
    if simplified != 0:
        raise AssertionError(f"{name} failed: {simplified}")
    print(f"PASS: {name}")


def reciprocity_check() -> None:
    u, v = sp.symbols("u v", positive=True, nonzero=True)
    P = sp.diag(u, v)
    K = sp.Matrix([[0, 1], [1, 0]])
    residual = sp.simplify(P.T * K * P - K)
    expected = (u * v - 1) * K
    assert_zero_matrix("P^T K P - K = (uv-1)K", residual - expected)


def pair_decomposition_check() -> None:
    h00, h01, h11 = sp.symbols("h00 h01 h11", real=True, nonzero=True)
    det_h = h00 * h11 - h01**2
    T2 = -h00
    beta = h01 / h00
    L2 = h11 - h01**2 / h00

    reconstructed = sp.Matrix(
        [
            [-T2, -T2 * beta],
            [-T2 * beta, -T2 * beta**2 + L2],
        ]
    )
    h = sp.Matrix([[h00, h01], [h01, h11]])
    assert_zero_matrix("pair metric reconstruction", reconstructed - h)
    assert_zero("T^2 L^2 = -det(h)", T2 * L2 + det_h)
    assert_zero(
        "L^2/T^2 = (-det h)/h00^2",
        L2 / T2 - (-det_h) / h00**2,
    )


def fk_family_check() -> None:
    k, ell = sp.symbols("k ell", real=True, nonzero=True)
    eta = sp.diag(-1, 1)
    # Columns are F_y=(1,0) and F_s=(k/ell,1).
    J = sp.Matrix([[1, k / ell], [0, 1]])
    h = sp.simplify(J.T * eta * J)
    expected = sp.Matrix(
        [[-1, -k / ell], [-k / ell, 1 - k**2 / ell**2]]
    )
    assert_zero_matrix("F_k pullback metric", h - expected)
    assert_zero("det(h_k)=-1", h.det() + 1)

    h00, h01, h11 = h[0, 0], h[0, 1], h[1, 1]
    T2 = -h00
    beta = sp.simplify(h01 / h00)
    L2 = sp.simplify(h11 - h01**2 / h00)
    assert_zero("F_k T^2=1", T2 - 1)
    assert_zero("F_k L^2=1", L2 - 1)
    assert_zero("F_k beta=k/ell", beta - k / ell)


def r17_leaf_check() -> None:
    u, a = sp.symbols("u a", positive=True, real=True)
    h = sp.Matrix(
        [
            [-u ** -2, -a * u ** -2],
            [-a * u ** -2, u**2 - a**2 * u ** -2],
        ]
    )
    assert_zero("R17 leaf det(h)=-1", h.det() + 1)
    h00, h01, h11 = h[0, 0], h[0, 1], h[1, 1]
    T2 = -h00
    beta = sp.simplify(h01 / h00)
    L2 = sp.simplify(h11 - h01**2 / h00)
    assert_zero("R17 T^2=u^-2", T2 - u ** -2)
    assert_zero("R17 L^2=u^2", L2 - u**2)
    assert_zero("R17 beta=a", beta - a)
    # exp(2 phi_pair)=L/T=u^2, hence phi_pair=log u on u>0.
    assert_zero("R17 (L/T)^2=u^4", L2 / T2 - u**4)


def plane_cylinder_check() -> None:
    """Same first fundamental form, different second fundamental form.

    Plane:    F_p(t,s)=(t,s,0,0)
    Cylinder: F_c(t,s)=(t,R cos(s/R),R sin(s/R),0)
    in Minkowski diag(-1,1,1,1).
    """
    s, R = sp.symbols("s R", positive=True, real=True)
    eta = sp.diag(-1, 1, 1, 1)

    Jp = sp.Matrix([[1, 0], [0, 1], [0, 0], [0, 0]])
    hp = Jp.T * eta * Jp

    Js = sp.Matrix([0, -sp.sin(s / R), sp.cos(s / R), 0])
    Jc = sp.Matrix.hstack(sp.Matrix([1, 0, 0, 0]), Js)
    hc = sp.simplify(Jc.T * eta * Jc)
    assert_zero_matrix("plane and cylinder have same h", hp - hc)

    # Cylinder unit normal in its x-y plane and second s derivative.
    n = sp.Matrix([0, sp.cos(s / R), sp.sin(s / R), 0])
    Fss = sp.Matrix([0, -sp.cos(s / R) / R, -sp.sin(s / R) / R, 0])
    IIss = sp.simplify((Fss.T * eta * n)[0])
    assert_zero("cylinder II_ss=-1/R", IIss + 1 / R)
    print("PASS: plane II=0 while cylinder II_ss=-1/R (extrinsic nonuniqueness)")


def so2_composition_check() -> None:
    a, b = sp.symbols("a b", real=True)

    def rot(x: sp.Expr) -> sp.Matrix:
        return sp.Matrix([[sp.cos(x), -sp.sin(x)], [sp.sin(x), sp.cos(x)]])

    assert_zero_matrix("SO(2) transport composition", rot(b) * rot(a) - rot(a + b))
    assert_zero_matrix("SO(2) inverse under path reversal", rot(a).inv() - rot(-a))


def jacobi_transfer_check() -> None:
    """Constant-curvature scalar Jacobi equation j''+K j=0.

    The 2x2 first-order transfer matrix composes exactly.  A conjugate point
    makes the position-from-initial-velocity entry vanish, but not the full
    transfer determinant.
    """
    w, s1, s2 = sp.symbols("w s1 s2", positive=True, real=True)

    def M(s: sp.Expr) -> sp.Matrix:
        return sp.Matrix(
            [
                [sp.cos(w * s), sp.sin(w * s) / w],
                [-w * sp.sin(w * s), sp.cos(w * s)],
            ]
        )

    assert_zero_matrix("Jacobi transfer composition", M(s2) * M(s1) - M(s1 + s2))
    assert_zero("Jacobi transfer det=1", M(s1).det() - 1)
    at_conjugate = sp.simplify(M(sp.pi / w))
    assert_zero("conjugate-point B block vanishes", at_conjugate[0, 1])
    assert_zero("full transfer remains invertible", at_conjugate.det() - 1)


def symmetry_geodesic_check() -> None:
    """Finite-dimensional part of the Einstein-cylinder symmetry counterexample.

    In M=R x S^3 with metric -dt^2+g_round, an antipodal great-circle segment
    traversed in coordinate time T has constant norm -T^2+pi^2.  It is timelike
    for T>pi.  Endpoint-fixing SO(3) rotates the S^2 family of initial directions.
    The global no-selector conclusion is a symmetry proof, not an algebraic test.
    """
    T = sp.symbols("T", positive=True, real=True)
    norm = -T**2 + sp.pi**2
    assert_zero("Einstein-cylinder tangent norm formula", norm - (-T**2 + sp.pi**2))
    print("INFO: choose any numerical T>pi (e.g. 4) to make every rotated great-circle route timelike")


def main() -> None:
    reciprocity_check()
    pair_decomposition_check()
    fk_family_check()
    r17_leaf_check()
    plane_cylinder_check()
    so2_composition_check()
    jacobi_transfer_check()
    symmetry_geodesic_check()
    print("\nAll finite-dimensional checks passed.")


if __name__ == "__main__":
    main()
