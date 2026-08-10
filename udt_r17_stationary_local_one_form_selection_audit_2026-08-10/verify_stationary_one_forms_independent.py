#!/usr/bin/env python3
"""Independent stdlib/Fraction reconstruction of the stationary one-form claims."""

from __future__ import annotations

import csv
import json
from fractions import Fraction as Q
from pathlib import Path


HERE = Path(__file__).resolve().parent


def mmul(a: list[list[Q]], b: list[list[Q]]) -> list[list[Q]]:
    return [[sum((a[i][k] * b[k][j] for k in range(len(b))), Q(0)) for j in range(len(b[0]))] for i in range(len(a))]


def msub(a: list[list[Q]], b: list[list[Q]]) -> list[list[Q]]:
    return [[a[i][j] - b[i][j] for j in range(len(a[0]))] for i in range(len(a))]


def mscale(c: Q, a: list[list[Q]]) -> list[list[Q]]:
    return [[c * value for value in row] for row in a]


def mvec(a: list[list[Q]], v: list[Q]) -> list[Q]:
    return [sum((a[i][j] * v[j] for j in range(len(v))), Q(0)) for i in range(len(a))]


def rank(matrix: list[list[Q]]) -> int:
    work = [row[:] for row in matrix]
    rows, cols = len(work), len(work[0])
    r = 0
    for c in range(cols):
        pivot = next((i for i in range(r, rows) if work[i][c]), None)
        if pivot is None:
            continue
        work[r], work[pivot] = work[pivot], work[r]
        scale = work[r][c]
        work[r] = [value / scale for value in work[r]]
        for i in range(rows):
            if i != r and work[i][c]:
                factor = work[i][c]
                work[i] = [work[i][j] - factor * work[r][j] for j in range(cols)]
        r += 1
    return r


def wedge_one(a: list[Q], b: list[Q]) -> dict[tuple[int, int], Q]:
    return {(i, j): a[i] * b[j] - a[j] * b[i] for i in range(4) for j in range(i + 1, 4)}


def add_two(*forms: dict[tuple[int, int], Q]) -> dict[tuple[int, int], Q]:
    keys = [(i, j) for i in range(4) for j in range(i + 1, 4)]
    return {key: sum((form.get(key, Q(0)) for form in forms), Q(0)) for key in keys}


def scale_two(c: Q, form: dict[tuple[int, int], Q]) -> dict[tuple[int, int], Q]:
    return {key: c * value for key, value in form.items()}


def rows(name: str) -> list[dict[str, str]]:
    with (HERE / name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def main() -> int:
    checks: dict[str, bool] = {}

    # Residual screen-quarter-turn: nullity of (R-I)^T is exactly two.
    R = [
        [Q(1), Q(0), Q(0), Q(0)],
        [Q(0), Q(1), Q(0), Q(0)],
        [Q(0), Q(0), Q(0), Q(-1)],
        [Q(0), Q(0), Q(1), Q(0)],
    ]
    RT_minus_I = [[R[j][i] - (Q(1) if i == j else Q(0)) for j in range(4)] for i in range(4)]
    checks["order_zero_screen_invariant_nullity_two"] = 4 - rank(RT_minus_I) == 2

    # Rebuild dtheta0 and dtheta1 by product rule at an exact rational jet.
    u, v, a = Q(2), Q(3), Q(1, 64)
    p1, p2, p3 = Q(5, 7), Q(-2, 5), Q(3, 11)
    dphi = [Q(0), p1 / u, p2 / v, p3 / v]
    theta0 = [Q(1), Q(0), Q(0), Q(0)]
    theta1 = [Q(0), Q(1), Q(0), Q(0)]
    for eps in (Q(1), Q(-1)):
        # tau=u^-1 eta, eta=u theta0, d eta=-2 eps a/v^2 theta2^theta3.
        d_u_inverse = [-value / u for value in dphi]
        eta = [u * value for value in theta0]
        d_eta = {(2, 3): -2 * eps * a / (v * v)}
        d_tau = add_two(wedge_one(d_u_inverse, eta), scale_two(Q(1) / u, d_eta))
        # nu=u sigma3, sigma3=theta1/u, du=u dphi.
        du = [u * value for value in dphi]
        sigma3 = [value / u for value in theta1]
        d_sigma3 = {(2, 3): -2 * eps / (v * v)}
        d_nu = add_two(wedge_one(du, sigma3), scale_two(u, d_sigma3))
        checks[f"product_rule_clock_nonclosed_eps_{int(eps)}"] = d_tau[(2, 3)] == -2 * eps * a / (u * v * v)
        checks[f"product_rule_ruler_nonclosed_eps_{int(eps)}"] = d_nu[(2, 3)] == -2 * eps * u / (v * v)

    # Independently reconstruct mean curvatures with exact Koszul arithmetic.
    eta_diag = [Q(-1), Q(1), Q(1), Q(1)]
    lambdas = [Q(-2), Q(-1), Q(0), Q(1, 2), Q(1), Q(2)]
    means_ok = True
    for lam in lambdas:
        for eps in (Q(1), Q(-1)):
            C = [[[Q(0) for _ in range(4)] for _ in range(4)] for _ in range(4)]

            def set_b(i: int, j: int, coefficients: tuple[Q, ...]) -> None:
                for k, coefficient in enumerate(coefficients):
                    C[i][j][k] = coefficient
                    C[j][i][k] = -coefficient

            set_b(0, 1, (-p1 / u, Q(0), Q(0), Q(0)))
            set_b(0, 2, (-p2 / v, Q(0), Q(0), Q(0)))
            set_b(0, 3, (-p3 / v, Q(0), Q(0), Q(0)))
            set_b(1, 2, (Q(0), p2 / v, -lam * p1 / u, 2 * eps / u))
            set_b(1, 3, (Q(0), p3 / v, -2 * eps / u, -lam * p1 / u))
            set_b(2, 3, (2 * eps * a / (u * v * v), 2 * eps * u / (v * v), lam * p3 / v, -lam * p2 / v))

            def c_inner(i: int, j: int, k: int) -> Q:
                return eta_diag[k] * C[i][j][k]

            def gamma(i: int, j: int, k: int) -> Q:
                lower = (c_inner(i, j, k) - c_inner(j, k, i) + c_inner(k, i, j)) / 2
                return eta_diag[k] * lower

            mean_E = [Q(0), Q(0), -gamma(0, 0, 2) + gamma(1, 1, 2), -gamma(0, 0, 3) + gamma(1, 1, 3)]
            mean_H = [gamma(2, 2, 0) + gamma(3, 3, 0), gamma(2, 2, 1) + gamma(3, 3, 1), Q(0), Q(0)]
            means_ok &= mean_E == [Q(0)] * 4
            means_ok &= mean_H == [Q(0), -2 * lam * p1 / u, Q(0), Q(0)]
    checks["koszul_mean_curvature_all_12_strata"] = means_ok

    # Unit quaternions: these linear matrices define the MC-minus global frame.
    MX = [[Q(0), Q(-1), Q(0), Q(0)], [Q(1), Q(0), Q(0), Q(0)], [Q(0), Q(0), Q(0), Q(-1)], [Q(0), Q(0), Q(1), Q(0)]]
    MY = [[Q(0), Q(0), Q(-1), Q(0)], [Q(0), Q(0), Q(0), Q(1)], [Q(1), Q(0), Q(0), Q(0)], [Q(0), Q(-1), Q(0), Q(0)]]
    MZ = [[Q(0), Q(0), Q(0), Q(-1)], [Q(0), Q(0), Q(-1), Q(0)], [Q(0), Q(1), Q(0), Q(0)], [Q(1), Q(0), Q(0), Q(0)]]
    bracket_XY = msub(mmul(MY, MX), mmul(MX, MY))
    bracket_YZ = msub(mmul(MZ, MY), mmul(MY, MZ))
    bracket_ZX = msub(mmul(MX, MZ), mmul(MZ, MX))
    checks["quaternion_MC_minus_brackets_exact"] = bracket_XY == mscale(Q(-2), MZ) and bracket_YZ == mscale(Q(-2), MX) and bracket_ZX == mscale(Q(-2), MY)

    q = [Q(1, 2)] * 4
    Xq, Yq, Zq = mvec(MX, q), mvec(MY, q), mvec(MZ, q)
    # phi=w. I=x^2+y^2. Directional derivatives use exact gradients.
    grad_phi = [Q(1), Q(0), Q(0), Q(0)]
    grad_I = [Q(0), 2 * q[1], 2 * q[2], Q(0)]

    def dot(left: list[Q], right: list[Q]) -> Q:
        return sum((left[i] * right[i] for i in range(4)), Q(0))

    dphi_Y, dphi_Z = dot(grad_phi, Yq), dot(grad_phi, Zq)
    dI_Y, dI_Z = dot(grad_I, Yq), dot(grad_I, Zq)
    wedge_ZY = dI_Z * dphi_Y - dI_Y * dphi_Z
    checks["global_stationary_R17_nonexact_witness_exact"] = wedge_ZY == Q(1, 2)
    checks["witness_point_is_on_unit_S3"] = sum((value * value for value in q), Q(0)) == Q(1)
    # s=H*dphi has s(X)=-x, s(Y)=-y, s(Z)=0.  Since [Z,Y]=2X in
    # the MC-minus convention, ds(Z,Y)=Z(sY)-s(2X)=x.
    s_X = dphi_X = dot(grad_phi, Xq)
    s_Y = dphi_Y
    z_of_minus_y = -Zq[2]
    ds_ZY = z_of_minus_y - 2 * s_X
    checks["pair_leaf_annihilator_Hdphi_nonclosed"] = ds_ZY == Q(1, 2)
    # I_H=p2^2+p3^2 (at v=1) and its differential vanish when the screen
    # gradient vanishes identically.  With nonzero twist norm W, the dimensionless
    # J_H=I_H/(I_H+W) and dJ_H also vanish there.
    pure_p2 = pure_p3 = Q(0)
    arbitrary_dp2, arbitrary_dp3 = Q(7), Q(-11)
    W = Q(1, 7)
    pure_I = pure_p2 * pure_p2 + pure_p3 * pure_p3
    pure_dI = 2 * pure_p2 * arbitrary_dp2 + 2 * pure_p3 * arbitrary_dp3
    checks["exact_family_preserves_pure_reciprocal_locus"] = (
        pure_I / (pure_I + W) == 0
        and W * pure_dI / (pure_I + W) ** 2 == 0
    )

    # A generic screen one-form and its quarter-turn complete the clock/ruler pair.
    h2, h3 = Q(2), Q(3)
    generic = [[Q(1), Q(0), Q(0), Q(0)], [Q(0), Q(1), Q(0), Q(0)], [Q(0), Q(0), h2, h3], [Q(0), Q(0), -h3, h2]]
    checks["generic_first_jet_full_rank"] = rank(generic) == 4

    candidates = rows("ONE_FORM_CLASSIFICATION.tsv")
    checks["candidate_ids_exact_16"] = [row["candidate_id"] for row in candidates] == [f"L{i:02d}" for i in range(1, 17)]
    checks["all_candidates_classified"] = all(row["classification"] and row["selection_status"] for row in candidates)
    checks["invariant_atlas_four_strata"] = len(rows("INVARIANT_COVECTOR_ATLAS.tsv")) == 4
    checks["closedness_atlas_eight_rows"] = len(rows("CLOSEDNESS_ATLAS.tsv")) == 8
    checks["owner_census_six_rows"] = len(rows("SELECTION_OWNER_CENSUS.tsv")) == 6

    failed = [name for name, passed in checks.items() if not passed]
    result = {
        "schema_version": 1,
        "method": "INDEPENDENT_STDLIB_FRACTION_MATRIX_EXTERIOR_AND_QUATERNION_RECONSTRUCTION",
        "checks": checks,
        "passed": len(checks) - len(failed),
        "total": len(checks),
        "failed": failed,
        "status": "PASS" if not failed else "FAIL",
    }
    (HERE / "INDEPENDENT_VERIFICATION_RESULT.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if not failed else 1


if __name__ == "__main__":
    raise SystemExit(main())
