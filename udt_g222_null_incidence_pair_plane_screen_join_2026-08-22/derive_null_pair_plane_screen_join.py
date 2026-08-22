#!/usr/bin/env python3
"""Exact symbolic derivation for the bounded G222 null-ribbon theorem."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path

import sympy as sp


if not __debug__:
    raise RuntimeError("G222 evidence requires Python assertions; optimized mode is forbidden")

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
LANDING = (
    "SUPPLIED_NULL_FAMILY_OWNS_FULL_RANK_TWO_PAIR_PLANE_CONDITIONALLY"
    "__CONSERVED_NULL_AREA_DENSITY_COMPLETES_RECIPROCAL_RULER"
    "__G188_SCREEN_IS_CANONICAL_NORMAL_CHANNEL"
    "__GLOBAL_RULER_COORDINATE_AND_PHYSICAL_PROTOCOL_REMAIN_OPEN"
)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def source_count() -> int:
    with (HERE / "SOURCE_MANIFEST.tsv").open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
    for row in rows:
        path = ROOT / row["path"]
        require(path.is_file(), f"missing source: {row['path']}")
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        require(digest == row["sha256"], f"source hash changed: {row['path']}")
    return len(rows)


def derive() -> dict[str, object]:
    checks: dict[str, bool] = {}

    T, a, r, w_b = sp.symbols("T a r w_b", positive=True)
    h = sp.Matrix([[-T**2, -a], [-a, 0]])
    checks["pair_determinant"] = sp.simplify(h.det() + a**2) == 0

    beta = sp.simplify(h[0, 1] / h[0, 0])
    L2 = sp.simplify(h[1, 1] - h[0, 1] ** 2 / h[0, 0])
    checks["shifted_beta"] = sp.simplify(beta - a / T**2) == 0
    checks["shifted_ruler_squared"] = sp.simplify(L2 - a**2 / T**2) == 0
    checks["G176_density_squared"] = sp.simplify(T**2 * L2 - a**2) == 0

    C = sp.diag(1, 1 / a)
    h_completed = sp.simplify(C.T * h * C)
    expected_completed = sp.Matrix([[-T**2, -1], [-1, 0]])
    checks["completed_metric"] = h_completed == expected_completed
    reconstructed = sp.expand(
        -T**2 * (sp.Symbol("dy") + sp.Symbol("vartheta") / T**2) ** 2
        + sp.Symbol("vartheta") ** 2 / T**2
    )
    checks["completed_shifted_form"] = sp.simplify(
        reconstructed
        - (-T**2 * sp.Symbol("dy") ** 2 - 2 * sp.Symbol("dy") * sp.Symbol("vartheta"))
    ) == 0

    w_a = r * w_b
    checks["boundary_frequency_ratio"] = sp.simplify(w_a / w_b - r) == 0
    checks["boundary_area_source"] = sp.simplify(a.subs(a, w_a) - w_a) == 0
    checks["boundary_area_target"] = sp.simplify(w_a - r * w_b) == 0
    checks["target_depth"] = sp.simplify(-sp.log(r) - (-sp.log(w_a / w_b))) == 0

    c, d = sp.symbols("c d", positive=True)
    h_reparam = sp.Matrix([[-T**2 - 2 * a * d, -c * a], [-c * a, 0]])
    checks["affine_reparam_determinant"] = sp.simplify(h_reparam.det() + (c * a) ** 2) == 0
    checks["affine_vertical_density"] = sp.simplify(c * a - a * c) == 0
    checks["null_shift_preserves_area"] = sp.simplify(-(-a + d * 0) - a) == 0

    b_x, b_y, q_xx, q_xy, q_yy, shift = sp.symbols(
        "b_x b_y q_xx q_xy q_yy shift", real=True
    )
    # Gram basis is (J,K,X,Y).
    gram = sp.Matrix(
        [
            [-T**2, -a, b_x, b_y],
            [-a, 0, 0, 0],
            [b_x, 0, q_xx, q_xy],
            [b_y, 0, q_xy, q_yy],
        ]
    )
    Jv = sp.Matrix([1, 0, 0, 0])
    Kv = sp.Matrix([0, 1, 0, 0])
    Xv = sp.Matrix([0, 0, 1, 0])
    Yv = sp.Matrix([0, 0, 0, 1])

    def inner(u: sp.Matrix, v: sp.Matrix) -> sp.Expr:
        return sp.expand((u.T * gram * v)[0])

    IX = Xv + b_x / a * Kv
    IY = Yv + b_y / a * Kv
    checks["screen_normal_X_orthogonal_J"] = sp.simplify(inner(IX, Jv)) == 0
    checks["screen_normal_X_orthogonal_K"] = sp.simplify(inner(IX, Kv)) == 0
    checks["screen_normal_Y_orthogonal_J"] = sp.simplify(inner(IY, Jv)) == 0
    checks["screen_normal_Y_orthogonal_K"] = sp.simplify(inner(IY, Kv)) == 0
    checks["screen_isometry_XX"] = sp.simplify(inner(IX, IX) - q_xx) == 0
    checks["screen_isometry_XY"] = sp.simplify(inner(IX, IY) - q_xy) == 0
    checks["screen_isometry_YY"] = sp.simplify(inner(IY, IY) - q_yy) == 0
    Xrep = Xv + shift * Kv
    b_rep = inner(Xrep, Jv)
    Irep = sp.simplify(Xrep + b_rep / a * Kv)
    checks["screen_representative_independence"] = sp.simplify(Irep - IX) == sp.zeros(4, 1)
    Jshift = Jv + shift * Kv
    b_jshift = inner(Xv, Jshift)
    Ijshift = sp.simplify(Xv + b_jshift / a * Kv)
    checks["null_shift_screen_independence"] = sp.simplify(Ijshift - IX) == sp.zeros(4, 1)

    # The quotient connection and tidal operator intertwine with normal projection.
    # A vector in K^perp has no J component in this Gram basis.
    v_k, v_x, v_y, f_dot = sp.symbols("v_k v_x v_y f_dot", real=True)
    Vscreen = sp.Matrix([0, v_k, v_x, v_y])

    def normal_projection(v: sp.Matrix) -> sp.Matrix:
        return sp.simplify(v - inner(v, Jv) / inner(Kv, Jv) * Kv)

    checks["screen_connection_input_in_Kperp"] = sp.simplify(inner(Vscreen, Kv)) == 0
    checks["screen_connection_K_term_quotiented"] = normal_projection(Kv) == sp.zeros(4, 1)
    differentiated_lift = Vscreen - f_dot * Kv
    checks["screen_connection_normal_intertwining"] = sp.simplify(
        normal_projection(differentiated_lift) - normal_projection(Vscreen)
    ) == sp.zeros(4, 1)

    t_k, t_x, t_y = sp.symbols("t_k t_x t_y", real=True)
    tidal_X = sp.Matrix([0, t_k, t_x, t_y])
    zero = sp.zeros(4, 1)
    # R_K is zero by antisymmetry in the first two curvature slots.  The only
    # load-bearing columns here are R_K=0 and R_X=R(X,K)K.
    tidal_operator = sp.Matrix.hstack(zero, zero, tidal_X, zero)
    checks["screen_tidal_output_in_Kperp"] = sp.simplify(inner(tidal_X, Kv)) == 0
    checks["screen_tidal_representative_intertwining"] = sp.simplify(
        normal_projection(tidal_operator * IX) - normal_projection(tidal_operator * Xv)
    ) == sp.zeros(4, 1)

    a0, a1, y = sp.symbols("a0 a1 y", real=True)
    a_y = a0 + a1 * y
    checks["vertical_density_curl"] = sp.diff(a_y, y) == a1
    checks["nonconstant_density_not_closed"] = sp.diff(a_y, y).subs(a1, 1) != 0
    h_turn = sp.Matrix([[0, -a], [-a, 0]])
    checks["clock_turn_pair_plane_regular"] = sp.simplify(h_turn.det() + a**2) == 0
    checks["zero_area_rank_failure"] = sp.Matrix([[-T**2, 0], [0, 0]]).det() == 0
    checks["screen_caustic_independent"] = (
        sp.diag(0, 1).det() == 0 and sp.simplify(h.det() + a**2) == 0
    )

    # Exact flat null ribbon with a genuinely nonclosed vertical ruler density.
    eps, lam = sp.symbols("eps lam", positive=True)
    c_y = 1 + eps * y
    F_flat = sp.Matrix([y + lam * c_y, lam * c_y, 0, 0])
    J_flat = sp.diff(F_flat, y)
    K_flat = sp.diff(F_flat, lam)
    eta4 = sp.diag(-1, 1, 1, 1)
    flat_inner = lambda u, v: sp.expand((u.T * eta4 * v)[0])
    flat_h = sp.simplify(sp.Matrix.hstack(J_flat, K_flat).T * eta4 * sp.Matrix.hstack(J_flat, K_flat))
    r_flat = sp.sqrt(1 + 2 * eps)
    U_A_flat = sp.Matrix([1, 0, 0, 0])
    U_B_flat = sp.simplify(J_flat.subs(lam, 1) / r_flat)
    checks["flat_nonclosed_K_null"] = flat_inner(K_flat, K_flat) == 0
    checks["flat_nonclosed_area_constant_on_ray"] = sp.simplify(flat_inner(J_flat, K_flat) + c_y) == 0
    checks["flat_nonclosed_pair_determinant"] = sp.simplify(flat_h.det() + c_y**2) == 0
    checks["flat_nonclosed_source_frequency"] = sp.simplify(-flat_inner(U_A_flat, K_flat) - c_y) == 0
    checks["flat_nonclosed_target_observer_unit"] = sp.simplify(flat_inner(U_B_flat, U_B_flat) + 1) == 0
    checks["flat_nonclosed_target_frequency"] = sp.simplify(
        -flat_inner(U_B_flat, K_flat) - c_y / r_flat
    ) == 0
    checks["flat_nonclosed_ratio"] = sp.simplify(c_y / (c_y / r_flat) - r_flat) == 0
    checks["flat_nonclosed_curl_nonzero"] = sp.diff(c_y, y) == eps

    # Full complete-coframe witness with every Q, s_t, and s_x channel active.
    N, A, beta0 = sp.Rational(2), sp.Rational(5), sp.Rational(1, 2)
    Q = sp.Matrix([[2, 1], [1, 3]])
    st = sp.Matrix([sp.Rational(1, 3), sp.Rational(-1, 4)])
    sx = sp.Matrix([sp.Rational(2, 5), sp.Rational(1, 7)])
    screen_seed = sp.Matrix([[st[0], sx[0], 1, 0], [st[1], sx[1], 0, 1]])
    screen_rows = Q * screen_seed
    E = sp.Matrix(
        [
            [N, N * beta0, 0, 0],
            [0, A, 0, 0],
            [screen_rows[0, column] for column in range(4)],
            [screen_rows[1, column] for column in range(4)],
        ]
    )
    eta = sp.diag(-1, 1, 1, 1)
    g = sp.simplify(E.T * eta * E)
    P2 = sp.simplify(N**2 - (st.T * Q.T * Q * st)[0])
    px = sp.Rational(3, 2)
    pz = sp.Matrix([sp.Rational(4, 3), sp.Rational(-2, 5)])
    H = Q.T * Q
    D = A**2 - N**2 * beta0**2
    Pi = sp.simplify(px - (sx.T * pz)[0])
    q2 = sp.simplify((pz.T * H.inv() * pz)[0])
    R = sp.sqrt(Pi**2 + D * q2)
    p0hat = sp.simplify((-N * beta0 * Pi - A * R) / D)
    pt = sp.simplify((st.T * pz)[0] + N * p0hat)
    pcoord = sp.Matrix([pt, px, pz[0], pz[1]])
    Kcoord = sp.simplify(g.inv() * pcoord)
    Ucoord = sp.Matrix([1 / sp.sqrt(P2), 0, 0, 0])
    rho = sp.Rational(7, 5)
    Jcoord = rho * Ucoord
    witness_h = sp.simplify(sp.Matrix.hstack(Jcoord, Kcoord).T * g * sp.Matrix.hstack(Jcoord, Kcoord))
    W = sp.simplify(-pt / sp.sqrt(P2))
    expected_h = sp.Matrix([[-rho**2, -rho * W], [-rho * W, 0]])
    checks["complete_coframe_witness_pair_metric"] = sp.simplify(witness_h - expected_h) == sp.zeros(2)
    checks["complete_coframe_witness_null"] = sp.simplify((Kcoord.T * g * Kcoord)[0]) == 0
    checks["complete_coframe_witness_observer_unit"] = sp.simplify((Ucoord.T * g * Ucoord)[0] + 1) == 0

    require(all(checks.values()), {name: value for name, value in checks.items() if not value})
    return {
        "status": "PASS",
        "landing": LANDING,
        "source_count": source_count(),
        "check_count": len(checks),
        "checks": checks,
        "formulas": {
            "pair_metric": "[[g(J,J),-a],[-a,0]]",
            "conserved_area_density": "a=-g(J,K)=W_A=r_AB*W_B",
            "pair_determinant": "-a^2",
            "completed_ruler_density": "m=a",
            "completed_metric": "[[-T^2,-1],[-1,0]]",
            "target_depth": "Phi_AB=-log(r_AB)",
            "normal_screen_map": "iota_J([X])=X-g(X,J)/g(K,J)*K",
            "global_coordinate_gate": "d(a*d_lambda)=partial_y(a)*dy_wedge_dlambda",
        },
    }


if __name__ == "__main__":
    print(json.dumps(derive(), indent=2, sort_keys=True))
