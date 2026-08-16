#!/usr/bin/env python3
"""Derive the bounded G109 same-query terminal-depth/propagation join."""

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


def verify_sources() -> dict[str, bool]:
    with (HERE / "SOURCE_MANIFEST.tsv").open(newline="") as handle:
        return {
            row["path"]: sha256(ROOT / row["path"]) == row["sha256"]
            for row in csv.DictReader(handle, delimiter="\t")
        }


def zero_matrix(matrix: sp.Matrix) -> bool:
    return all(sp.simplify(entry) == 0 for entry in matrix)


def endpoint_identities() -> dict[str, object]:
    k0, k1, k2 = sp.symbols("k0 k1 k2", real=True)
    p0, p1, p2 = sp.symbols("p0 p1 p2", real=True)
    b0, b1, b2 = sp.symbols("b0 b1 b2", real=True)

    def terminal(k: sp.Expr, p: sp.Expr, beta: sp.Expr) -> sp.Matrix:
        clock = sp.exp(k - p)
        ruler = sp.exp(k + p)
        return sp.Matrix([[clock, clock * beta], [0, ruler]])

    B0 = terminal(k0, p0, b0)
    B1 = terminal(k1, p1, b1)
    B2 = terminal(k2, p2, b2)
    eta = sp.diag(-1, 1)
    h1 = sp.simplify(B1.T * eta * B1)
    terminal_ratio = sp.simplify(-h1.det() / h1[0, 0] ** 2)

    R10 = sp.simplify(B1 * B0.inv())
    R21 = sp.simplify(B2 * B1.inv())
    R20 = sp.simplify(B2 * B0.inv())
    dp10 = p1 - p0
    diagonal_ratio = sp.simplify(R10[0, 0] / R10[1, 1])

    return {
        "terminal_ratio_is_exp_4phi": sp.simplify(terminal_ratio - sp.exp(4 * p1)) == 0,
        "transition_clock_factor": sp.simplify(
            R10[0, 0] - sp.exp((k1 - k0) - dp10)
        ) == 0,
        "transition_ruler_factor": sp.simplify(
            R10[1, 1] - sp.exp((k1 - k0) + dp10)
        ) == 0,
        "reciprocal_character": sp.simplify(
            diagonal_ratio - sp.exp(-2 * dp10)
        ) == 0,
        "matched_composition": zero_matrix(sp.simplify(R21 * R10 - R20)),
        "reversal": zero_matrix(sp.simplify(R10.inv() - B0 * B1.inv())),
        "identity": zero_matrix(sp.simplify(B0 * B0.inv() - sp.eye(2))),
        "common_scale_absent_from_depth": not dp10.has(k0, k1),
    }


def continuous_identities() -> tuple[dict[str, object], list[dict[str, float]]]:
    x = sp.symbols("x", real=True)
    phi = x + x**2 / 5
    kappa = x**3 / 10
    beta = x / 7 + x**2 / 17
    clock = sp.exp(kappa - phi)
    ruler = sp.exp(kappa + phi)
    B = sp.Matrix([[clock, clock * beta], [0, ruler]])
    eta = sp.diag(-1, 1)
    h = sp.simplify(B.T * eta * B)
    ratio = sp.simplify(-h.det() / h[0, 0] ** 2)
    hdot = h.diff(x)
    terminal_phi_dot = sp.simplify(
        sp.trace(h.inv() * hdot) / 4 - hdot[0, 0] / (2 * h[0, 0])
    )
    hddot = hdot.diff(x)
    terminal_phi_ddot = sp.simplify(
        sp.trace(h.inv() * hddot - h.inv() * hdot * h.inv() * hdot) / 4
        - (hddot[0, 0] / h[0, 0] - (hdot[0, 0] / h[0, 0]) ** 2) / 2
    )

    u = 2 * x / 5 + x**2 / 11
    v = -x / 6 + x**3 / 13
    angle = x**2 / 9
    rotation = sp.Matrix(
        [[sp.cos(angle), -sp.sin(angle)], [sp.sin(angle), sp.cos(angle)]]
    )
    W = sp.simplify(rotation * sp.diag(sp.exp(u), sp.exp(v)))
    Lopt = sp.simplify(W.diff(x) * W.inv())
    area_log_dot = sp.simplify(sp.diff(sp.log(sp.det(W)), x))
    joined_rate = sp.simplify(sp.trace(Lopt) / (2 * terminal_phi_dot))
    direct_rate = sp.simplify(area_log_dot / (2 * sp.diff(phi, x)))
    tidal = sp.simplify(-W.diff(x, 2) * W.inv())
    riccati_residual = sp.simplify(Lopt.diff(x) + Lopt * Lopt + tidal)

    Kphi = sp.simplify(Lopt / sp.diff(phi, x))
    drag = sp.simplify(sp.diff(phi, x, 2) / sp.diff(phi, x) ** 2)
    tidal_phi = sp.simplify(tidal / sp.diff(phi, x) ** 2)
    reparam_residual = sp.simplify(
        Kphi.diff(x) / sp.diff(phi, x) + Kphi * Kphi + drag * Kphi + tidal_phi
    )

    gamma = x**3 / 19
    passive_rotation = sp.Matrix(
        [[sp.cos(gamma), -sp.sin(gamma)], [sp.sin(gamma), sp.cos(gamma)]]
    )
    Wrot = sp.simplify(passive_rotation * W)
    rotated_rate = sp.simplify(
        sp.trace(Wrot.diff(x) * Wrot.inv()) / (2 * terminal_phi_dot)
    )

    rows = []
    for value in (0, sp.Rational(1, 5), sp.Rational(1, 2), sp.Rational(4, 5)):
        rows.append(
            {
                "lambda": float(value),
                "phi_pair": float(phi.subs(x, value)),
                "phi_dot": float(sp.diff(phi, x).subs(x, value)),
                "screen_area": float(sp.det(W).subs(x, value)),
                "a_eff_joined": float(joined_rate.subs(x, value)),
                "a_eff_direct": float(direct_rate.subs(x, value)),
                "joined_direct_residual": float(
                    abs((joined_rate - direct_rate).subs(x, value))
                ),
            }
        )

    return (
        {
            "terminal_phi_recovery": sp.simplify(ratio - sp.exp(4 * phi)) == 0,
            "terminal_phi_dot": sp.simplify(terminal_phi_dot - sp.diff(phi, x)) == 0,
            "terminal_phi_ddot": sp.simplify(
                terminal_phi_ddot - sp.diff(phi, x, 2)
            ) == 0,
            "joined_rate_equals_direct": sp.simplify(joined_rate - direct_rate) == 0,
            "jacobi_riccati": zero_matrix(riccati_residual),
            "depth_reparameterized_riccati": zero_matrix(reparam_residual),
            "passive_rotation_invariant": sp.simplify(rotated_rate - joined_rate) == 0,
            "wrong_factor_detected": sp.simplify(
                sp.trace(Lopt) / terminal_phi_dot - direct_rate
            ) != 0,
            "wrong_affine_substitution_detected": sp.simplify(
                sp.trace(Lopt) / 2 - direct_rate
            ) != 0,
        },
        rows,
    )


def boundary_identities() -> dict[str, object]:
    pA, pBin, pBout, pC = sp.symbols("pA pBin pBout pC", real=True)
    dAB = pBin - pA
    dBC = pC - pBout
    dreset = pBout - pBin
    dAC = pC - pA
    omitted_error = sp.simplify(dAB + dBC - dAC)

    # A genuine zero-rate control: endpoint depth remains finite while the
    # same-query depth coordinate fails locally because the screen-area rate
    # is nonzero and d(phi_pair)/dz vanishes.
    z = sp.symbols("z", real=True)
    phi_turn = z**2
    W_regular = sp.exp(z) * sp.eye(2)
    optical_regular = sp.simplify(W_regular.diff(z) * W_regular.inv())
    optical_trace = sp.simplify(sp.trace(optical_regular))
    zero_rate = sp.simplify(phi_turn.diff(z).subs(z, 0))
    endpoint_delta = sp.simplify(phi_turn.subs(z, 1) - phi_turn.subs(z, 0))

    # A genuine caustic control: the screen map loses rank and its optical
    # trace develops a pole even though this says nothing adverse about the
    # endpoint reciprocal scalar itself.
    W_caustic = z * sp.eye(2)
    caustic_det = sp.simplify(W_caustic.det().subs(z, 0))
    caustic_optical_trace = sp.simplify(sp.trace(W_caustic.diff(z) * W_caustic.inv()))
    return {
        "reset_restores_composition": sp.simplify(dAB + dreset + dBC - dAC) == 0,
        "omitted_reset_error": str(omitted_error),
        "omitted_reset_detected": sp.simplify(omitted_error + dreset) == 0,
        "zero_rate_endpoint_delta": str(endpoint_delta),
        "zero_rate_endpoint_depth_exists": endpoint_delta == 1,
        "zero_rate_phi_dot_zero": zero_rate == 0,
        "zero_rate_optical_trace": str(optical_trace),
        "zero_rate_optical_trace_nonzero": optical_trace.subs(z, 0) != 0,
        "zero_rate_reparameterization_rejected": zero_rate == 0
        and optical_trace.subs(z, 0) != 0,
        "noninjective_turning_depth": sp.simplify(
            phi_turn.subs(z, -1) - phi_turn.subs(z, 1)
        )
        == 0,
        "caustic_determinant_zero": caustic_det == 0,
        "caustic_optical_trace": str(caustic_optical_trace),
        "caustic_optical_trace_has_pole": sp.limit(
            caustic_optical_trace, z, 0, dir="+"
        )
        == sp.oo,
    }


def write_atlas(rows: list[dict[str, float]]) -> None:
    with (HERE / "CONTROL_ATLAS.tsv").open("w", newline="") as handle:
        writer = csv.DictWriter(
            handle, fieldnames=list(rows[0]), delimiter="\t", lineterminator="\n"
        )
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    source_hashes = verify_sources()
    endpoint = endpoint_identities()
    continuous, rows = continuous_identities()
    boundaries = boundary_identities()
    write_atlas(rows)
    result = {
        "schema": "UDT_G109_SAME_QUERY_DEPTH_JOIN_V1",
        "source_hashes": source_hashes,
        "all_source_hashes_match": all(source_hashes.values()),
        "endpoint_identities": endpoint,
        "continuous_identities": continuous,
        "boundary_identities": boundaries,
        "all_checks_pass": all(endpoint.values())
        and all(value for key, value in continuous.items())
        and boundaries["reset_restores_composition"]
        and boundaries["omitted_reset_detected"]
        and boundaries["zero_rate_endpoint_depth_exists"]
        and boundaries["zero_rate_phi_dot_zero"]
        and boundaries["zero_rate_optical_trace_nonzero"]
        and boundaries["zero_rate_reparameterization_rejected"]
        and boundaries["noninjective_turning_depth"]
        and boundaries["caustic_determinant_zero"]
        and boundaries["caustic_optical_trace_has_pole"],
        "maximum_conclusion": (
            "one supplied coherent regular calibrated pair query realizes the founded reciprocal "
            "increment as terminal Delta phi_pair and thereby supplies G108's local depth map; "
            "physical history query branch initial screen and universal global descent remain open"
        ),
    }
    (HERE / "DERIVATION_RESULT.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n"
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    raise SystemExit(0 if result["all_checks_pass"] else 1)


if __name__ == "__main__":
    main()
