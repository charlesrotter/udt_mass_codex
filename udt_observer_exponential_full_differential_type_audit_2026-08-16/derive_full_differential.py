#!/usr/bin/env python3
"""Exact symbolic production for the bounded G110 full-differential audit."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def source_hashes() -> dict[str, bool]:
    with (HERE / "SOURCE_MANIFEST.tsv").open(newline="") as handle:
        return {
            row["path"]: sha256(ROOT / row["path"]) == row["sha256"]
            for row in csv.DictReader(handle, delimiter="\t")
        }


def zero_matrix(matrix: sp.Matrix) -> bool:
    return all(sp.simplify(value) == 0 for value in matrix)


def flat_full_differential() -> tuple[dict[str, object], list[dict[str, object]]]:
    tau, lam, a, b = sp.symbols("tau lambda a b", real=True)
    n0 = sp.sqrt(1 - a**2 - b**2)
    F = sp.Matrix([tau + lam, lam * n0, lam * a, lam * b])
    eta = sp.diag(-1, 1, 1, 1)
    values = {a: 0, b: 0}
    T = F.diff(tau).subs(values)
    K = F.diff(lam).subs(values)
    J1 = F.diff(a).subs(values)
    J2 = F.diff(b).subs(values)
    Jpair = T.row_join(K)
    Jsky = J1.row_join(J2)
    Jfull = Jpair.row_join(Jsky)
    h = sp.simplify(Jpair.T * eta * Jpair)
    H = sp.simplify(Jfull.T * eta * Jfull)
    screen = sp.Matrix([[0, 0, 1, 0], [0, 0, 0, 1]])
    Wpair = sp.simplify(screen * Jpair)
    Dsky = sp.simplify(screen * Jsky)
    phi = sp.simplify(sp.log((-h.det()) / h[0, 0] ** 2) / 4)

    mixed_1 = sp.simplify(F.diff(a).diff(lam) - F.diff(lam).diff(a))
    mixed_2 = sp.simplify(F.diff(b).diff(lam) - F.diff(lam).diff(b))
    checks = {
        "pair_metric": h == sp.Matrix([[-1, -1], [-1, 0]]),
        "pair_lorentzian": h[0, 0] < 0 and h.det() == -1,
        "terminal_phi_zero": phi == 0,
        "pair_screen_zero": Wpair == sp.zeros(2),
        "sky_jacobi_lambda_identity": Dsky == lam * sp.eye(2),
        "distinct_rank_at_lambda_one": Wpair.subs(lam, 1).rank() == 0
        and Dsky.subs(lam, 1).rank() == 2,
        "sky_vertex_zero": Dsky.subs(lam, 0) == sp.zeros(2),
        "sky_vertex_derivative_identity": Dsky.diff(lam).subs(lam, 0) == sp.eye(2),
        "full_pullback_blocks": H
        == sp.diag(1, 1, lam, lam)
        * sp.Matrix([[-1, -1, 0, 0], [-1, 0, 0, 0], [0, 0, lam, 0], [0, 0, 0, lam]]),
        "full_jacobian_determinant": sp.simplify(Jfull.det() - lam**2) == 0,
        "mixed_partial_a": zero_matrix(mixed_1),
        "mixed_partial_b": zero_matrix(mixed_2),
        "phi_not_sky_coordinate": sp.diff(phi, lam) == 0
        and sp.diff(sp.log(Dsky.det()), lam) == 2 / lam,
    }
    rows = [
        {
            "control": "flat_observer_sky",
            "lambda": value,
            "det_h_pair": str(h.det()),
            "phi_pair": str(phi),
            "rank_pair_screen": Wpair.subs(lam, value).rank(),
            "rank_sky_jacobi": Dsky.subs(lam, value).rank(),
            "det_sky_jacobi": str(Dsky.det().subs(lam, value)),
            "trace_tidal": "NA",
        }
        for value in (0, 1, 2)
    ]
    return checks, rows


def curvature_controls() -> tuple[dict[str, object], list[dict[str, object]]]:
    lam, alpha = sp.symbols("lambda alpha", positive=True, real=True)
    controls = {
        "focusing": (sp.sin(alpha * lam) / alpha * sp.eye(2), alpha**2 * sp.eye(2)),
        "flat": (lam * sp.eye(2), sp.zeros(2)),
        "defocusing": (
            sp.sinh(alpha * lam) / alpha * sp.eye(2),
            -alpha**2 * sp.eye(2),
        ),
        "anisotropic": (sp.diag(sp.sin(lam), lam), sp.diag(1, 0)),
    }
    checks: dict[str, object] = {}
    rows: list[dict[str, object]] = []
    for name, (D, tidal) in controls.items():
        residual = sp.simplify(D.diff(lam, 2) + tidal * D)
        checks[f"{name}_jacobi"] = zero_matrix(residual)
        checks[f"{name}_vertex_zero"] = D.subs(lam, 0) == sp.zeros(2)
        checks[f"{name}_vertex_derivative"] = D.diff(lam).subs(lam, 0) == sp.eye(2)
        rows.append(
            {
                "control": name,
                "jacobi_residual_zero": zero_matrix(residual),
                "det_D": str(sp.simplify(D.det())),
                "trace_tidal": str(sp.trace(tidal)),
            }
        )

    Daniso = controls["anisotropic"][0]
    Laniso = sp.simplify(Daniso.diff(lam) * Daniso.inv())
    sigma = sp.simplify(Laniso - sp.trace(Laniso) * sp.eye(2) / 2)
    checks["anisotropic_shear_nonzero"] = not zero_matrix(sigma)
    checks["anisotropic_trace"] = sp.simplify(
        sp.trace(Laniso) - (sp.cot(lam) + 1 / lam)
    ) == 0

    Dfocus = sp.sin(lam) * sp.eye(2)
    Lfocus = sp.simplify(Dfocus.diff(lam) * Dfocus.inv())
    checks["caustic_det_zero"] = Dfocus.det().subs(lam, sp.pi) == 0
    checks["caustic_map_finite"] = all(
        value.is_finite for value in Dfocus.subs(lam, sp.pi)
    )
    checks["caustic_derivative_finite"] = all(
        value.is_finite for value in Dfocus.diff(lam).subs(lam, sp.pi)
    )
    checks["caustic_riccati_pole"] = sp.limit(
        sp.trace(Lfocus), lam, sp.pi, dir="-"
    ) == -sp.oo
    return checks, rows


def covariance_and_join() -> dict[str, object]:
    lam = sp.symbols("lambda", positive=True, real=True)
    t1, t2 = sp.symbols("t1 t2", real=True)
    eta = sp.diag(-1, 1, 1, 1)
    E = sp.Matrix([[2, 1, 0, 0], [0, 3, 0, 0], [1, 0, 2, 1], [0, 1, 0, 2]])
    J = sp.Matrix([[1, 0], [1, 1], [0, 1], [1, -1]])
    P = sp.Matrix([[1, 1, 0, 0], [0, 1, 0, 0], [0, 0, 2, 1], [0, 0, 0, 1]])
    V = E * J
    transformed = E * P.inv() * P * J
    h = sp.simplify(V.T * eta * V)
    h_transformed = sp.simplify(transformed.T * eta * transformed)

    h0 = sp.Matrix([[-4, -1], [-1, 3]])
    shear_basis = sp.Matrix([[1, sp.Rational(2, 3)], [0, 1]])
    hs = sp.simplify(shear_basis.T * h0 * shear_basis)
    phi0 = sp.simplify(sp.log((-h0.det()) / h0[0, 0] ** 2) / 4)
    phis = sp.simplify(sp.log((-hs.det()) / hs[0, 0] ** 2) / 4)

    D = sp.diag(sp.sinh(lam), lam)
    phi = lam + lam**2
    optical = sp.simplify(D.diff(lam) * D.inv())
    direct = sp.simplify(sp.diff(sp.log(D.det()), lam) / (2 * sp.diff(phi, lam)))
    joined = sp.simplify(sp.trace(optical) / (2 * sp.diff(phi, lam)))

    O = sp.Matrix([[0, -1], [1, 0]])
    C = sp.Matrix([[2, 1], [0, 3]])
    optical_left = sp.simplify((O * D).diff(lam) * (O * D).inv())
    optical_right = sp.simplify((D * C).diff(lam) * (D * C).inv())

    canonical_pair_screen = sp.Matrix([[t1, 0], [t2, 0]])
    pair_action = sp.Matrix([[2, 0], [0, 1]])
    sky_action = sp.Matrix([[1, 0], [0, 3]])
    seed_pair = sp.eye(2)
    seed_sky = sp.eye(2)
    mutated_pair = seed_pair * pair_action
    mutated_sky = seed_sky * sky_action
    return {
        "EJ_refactorization": transformed == V,
        "EJ_metric_invariant": h_transformed == h,
        "pair_shear_phi_invariant": sp.simplify(phis - phi0) == 0,
        "distinct_block_join": sp.simplify(direct - joined) == 0,
        "left_screen_conjugacy": zero_matrix(
            sp.simplify(optical_left - O * optical * O.inv())
        ),
        "right_constant_basis_cancels": zero_matrix(
            sp.simplify(optical_right - optical)
        ),
        "trace_screen_invariant": sp.simplify(
            sp.trace(optical_left) - sp.trace(optical)
        ) == 0,
        "canonical_null_pair_screen_det_zero": sp.simplify(
            canonical_pair_screen.det()
        ) == 0,
        "independent_domain_actions_break_matrix_equality": not zero_matrix(
            sp.simplify(mutated_pair - mutated_sky)
        ),
    }


def write_atlas(rows: list[dict[str, object]]) -> None:
    fields = sorted({key for row in rows for key in row})
    with (HERE / "CONTROL_ATLAS.tsv").open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    hashes = source_hashes()
    flat, flat_rows = flat_full_differential()
    curvature, curvature_rows = curvature_controls()
    covariance = covariance_and_join()
    checks = {**flat, **curvature, **covariance}
    result = {
        "schema": "UDT_G110_OBSERVER_FULL_DIFFERENTIAL_V1",
        "source_hashes": hashes,
        "all_source_hashes_match": all(hashes.values()),
        "checks": checks,
        "all_checks_pass": all(hashes.values()) and all(checks.values()),
        "maximum_conclusion": (
            "for the conditional point-observer exponential query the terminal pair and angular "
            "Jacobi maps are distinct blocks of one full differential; point-vertex data and local "
            "branch evolution are metric-derived, while physical history and global weights remain open"
        ),
    }
    write_atlas(flat_rows + curvature_rows)
    (HERE / "DERIVATION_RESULT.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n"
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    raise SystemExit(0 if result["all_checks_pass"] else 1)


if __name__ == "__main__":
    main()
