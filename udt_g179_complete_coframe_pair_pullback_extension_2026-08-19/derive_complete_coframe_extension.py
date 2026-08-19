#!/usr/bin/env python3
"""Exact symbolic and rational-witness derivation for G179."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent
ETA4 = sp.diag(-1, 1, 1, 1)
ETA2 = sp.diag(-1, 1)


def source_hashes() -> tuple[int, list[str]]:
    rows = list(csv.DictReader((HERE / "SOURCE_MANIFEST.tsv").open(), delimiter="\t"))
    failures = []
    for row in rows:
        actual = hashlib.sha256((ROOT / row["path"]).read_bytes()).hexdigest()
        if actual != row["sha256"]:
            failures.append(row["path"])
    return len(rows), failures


def block_coframe(
    b: sp.Matrix, q: sp.Matrix, s: sp.Matrix
) -> sp.Matrix:
    return b.row_join(sp.zeros(2)).col_join((q * s).row_join(q))


def pullback(e: sp.Matrix, j: sp.Matrix) -> sp.Matrix:
    return sp.simplify(j.T * e.T * ETA4 * e * j)


def det_derivative(h: sp.Matrix, dh: sp.Matrix) -> sp.Expr:
    return sp.expand(
        dh[0, 0] * h[1, 1]
        + h[0, 0] * dh[1, 1]
        - 2 * h[0, 1] * dh[0, 1]
    )


def main() -> None:
    # Generic two-dimensional theorem, with nonzero shift retained.
    h00, h01, h11, m = sp.symbols("h00 h01 h11 m", real=True)
    h_generic = sp.Matrix([[h00, h01], [h01, h11]])
    det_h = sp.expand(h_generic.det())
    t2 = -h00
    beta = h01 / h00
    l2 = h11 - h01**2 / h00
    density2 = -det_h
    calibrated = sp.diag(1, 1 / m).T * h_generic * sp.diag(1, 1 / m)

    generic_checks = {
        "shifted_decomposition_reconstructs_h": sp.simplify(
            h_generic
            - sp.Matrix(
                [
                    [-t2, -t2 * beta],
                    [-t2 * beta, l2 - t2 * beta**2],
                ]
            )
        ) == sp.zeros(2),
        "determinant_identity": sp.simplify(t2 * l2 + det_h) == 0,
        "reciprocal_density_unique_positive_square": sp.simplify(
            density2 - t2 * l2
        ) == 0,
        "calibrated_determinant_minus_one": sp.simplify(
            calibrated.det().subs(m**2, density2) + 1
        ) == 0,
        "calibrated_reciprocal_product_one": sp.simplify(
            (t2 * l2 / m**2).subs(m**2, density2) - 1
        ) == 0,
    }

    # Fully symbolic complete block chart. No inverse of Y is used.
    b_symbols = sp.symbols("b00 b01 b10 b11", real=True)
    q_symbols = sp.symbols("q00 q01 q10 q11", real=True)
    s_symbols = sp.symbols("s00 s01 s10 s11", real=True)
    y_symbols = sp.symbols("y00 y01 y10 y11", real=True)
    z_symbols = sp.symbols("z00 z01 z10 z11", real=True)
    b = sp.Matrix(2, 2, b_symbols)
    q = sp.Matrix(2, 2, q_symbols)
    s = sp.Matrix(2, 2, s_symbols)
    y = sp.Matrix(2, 2, y_symbols)
    z = sp.Matrix(2, 2, z_symbols)
    e = block_coframe(b, q, s)
    j = y.col_join(z)
    h_direct = pullback(e, j)
    h_factored = sp.simplify(
        y.T * b.T * ETA2 * b * y
        + (s * y + z).T * q.T * q * (s * y + z)
    )
    block_identity = sp.simplify(h_direct - h_factored) == sp.zeros(2)

    # Exact full-sector witness: nonspherical Q, every S entry, Z, and shift active.
    b0 = sp.Matrix([[2, -2], [2, 1]])
    q0 = sp.Matrix([[1, 2], [2, 3]])
    s0 = sp.Matrix([[-1, 1], [-1, -1]])
    y0 = sp.Matrix([[3, 2], [-3, 1]])
    z0 = sp.Matrix([[1, -2], [2, -3]])
    e0 = block_coframe(b0, q0, s0)
    j0 = y0.col_join(z0)
    h0 = pullback(e0, j0)

    singular_y = sp.Matrix([[-8, 0], [2, 0]])
    singular_z = sp.Matrix([[-6, 3], [-6, -6]])
    singular_j = singular_y.col_join(singular_z)
    singular_h = pullback(e0, singular_j)

    # Gauge and ambient-coordinate covariance. K is unimodular and mixes all blocks.
    lorentz = sp.Matrix(
        [
            [sp.Rational(5, 3), sp.Rational(4, 3), 0, 0],
            [sp.Rational(4, 3), sp.Rational(5, 3), 0, 0],
            [0, 0, 0, -1],
            [0, 0, 1, 0],
        ]
    )
    k4 = sp.Matrix(
        [[1, 1, 0, 0], [0, 1, 1, 0], [0, 0, 1, 1], [0, 0, 0, 1]]
    )
    e_coordinate = sp.simplify(e0 * k4.inv())
    j_coordinate = sp.simplify(k4 * j0)
    h_gauge = pullback(lorentz * e0, j0)
    h_coordinate = pullback(e_coordinate, j_coordinate)

    # Positive ruler rescaling and orientation reversal are density statements.
    pair_scale = sp.diag(1, 3)
    pair_reverse = sp.diag(1, -1)
    h_scale = sp.simplify(pair_scale.T * h0 * pair_scale)
    h_reverse = sp.simplify(pair_reverse.T * h0 * pair_reverse)

    # Exact directional census. Search all four entries per live sector and retain
    # the first mutation changing h and at least one completed-pair output.
    sector_bases = {"B": b0, "Q": q0, "S": s0, "Y": y0, "Z": z0}
    sector_effects: dict[str, dict[str, object]] = {}
    tau = sp.symbols("tau", real=True)
    for sector, base in sector_bases.items():
        selected = None
        for row in range(2):
            for col in range(2):
                perturb = sp.zeros(2)
                perturb[row, col] = 1
                values = dict(sector_bases)
                values[sector] = base + tau * perturb
                e_tau = block_coframe(values["B"], values["Q"], values["S"])
                j_tau = values["Y"].col_join(values["Z"])
                h_tau = pullback(e_tau, j_tau)
                dh = sp.simplify(h_tau.diff(tau).subs(tau, 0))
                dm2 = sp.simplify(-det_derivative(h0, dh))
                dphi = sp.simplify(-dh[0, 0] / (2 * h0[0, 0]))
                if dh != sp.zeros(2) and (dm2 != 0 or dphi != 0):
                    selected = {
                        "entry": [row, col],
                        "dh": [[str(v) for v in dh.row(i)] for i in range(2)],
                        "d_m_squared": str(dm2),
                        "d_Phi": str(dphi),
                    }
                    break
            if selected is not None:
                break
        if selected is None:
            raise SystemExit(f"FAIL: no live effect found for {sector}")
        sector_effects[sector] = selected

    # Product-rule identity for arbitrary instantaneous dotE,dotJ at the exact witness.
    de_symbols = sp.symbols("de0:16", real=True)
    dj_symbols = sp.symbols("dj0:8", real=True)
    de = sp.Matrix(4, 4, de_symbols)
    dj = sp.Matrix(4, 2, dj_symbols)
    e_tau = e0 + tau * de
    j_tau = j0 + tau * dj
    direct_dot_h = sp.simplify(pullback(e_tau, j_tau).diff(tau).subs(tau, 0))
    g0 = e0.T * ETA4 * e0
    dot_g = de.T * ETA4 * e0 + e0.T * ETA4 * de
    product_dot_h = sp.simplify(dj.T * g0 * j0 + j0.T * dot_g * j0 + j0.T * g0 * dj)

    checks = {
        **generic_checks,
        "complete_block_pullback_identity": block_identity,
        "full_witness_expected_h": h0 == sp.Matrix([[-118, 102], [102, 822]]),
        "full_witness_regular": bool(h0[0, 0] < 0 and h0.det() < 0),
        "full_witness_shift_nonzero": h0[0, 1] != 0,
        "all_four_mixing_entries_active": all(value != 0 for value in s0),
        "screen_nonspherical": q0.T * q0 != sp.eye(2) * (q0.T * q0)[0, 0],
        "singular_Y_retained": singular_y.det() == 0,
        "singular_Y_full_J_rank_two": singular_j.rank() == 2,
        "singular_Y_pair_regular": bool(
            singular_h[0, 0] < 0 and singular_h.det() < 0
        ),
        "lorentz_gauge_exact": sp.simplify(lorentz.T * ETA4 * lorentz - ETA4)
        == sp.zeros(4),
        "lorentz_gauge_pullback_invariant": sp.simplify(h_gauge - h0) == sp.zeros(2),
        "ambient_coordinate_pullback_invariant": sp.simplify(h_coordinate - h0)
        == sp.zeros(2),
        "nonblock_coordinate_coframe_exercised": e_coordinate[:2, 2:] != sp.zeros(2),
        "positive_pair_scale_determinant_density": sp.simplify(
            h_scale.det() - 9 * h0.det()
        ) == 0,
        "positive_pair_scale_depth_invariant": h_scale[0, 0] == h0[0, 0],
        "orientation_reversal_determinant_invariant": h_reverse.det() == h0.det(),
        "orientation_reversal_shift_sign": h_reverse[0, 1] == -h0[0, 1],
        "query_live_product_rule": sp.simplify(direct_dot_h - product_dot_h)
        == sp.zeros(2),
        "all_BQSYZ_sectors_live": set(sector_effects) == {"B", "Q", "S", "Y", "Z"},
    }

    count, hash_failures = source_hashes()
    status = "PASS" if all(checks.values()) and count == 10 and not hash_failures else "FAIL"
    result = {
        "audit": "G179",
        "status": status,
        "landing": (
            "GENERAL_COMPLETE_COFRAME_PULLBACK_EXTENDS_COMPLETED_PAIR_KERNEL_"
            "WITHOUT_EXTRA_SCALAR"
            if status == "PASS"
            else "PREREGISTERED_FAILURE"
        ),
        "checks": checks,
        "source_count": count,
        "source_hash_failures": hash_failures,
        "full_witness": {
            "B": [[int(v) for v in b0.row(i)] for i in range(2)],
            "Q": [[int(v) for v in q0.row(i)] for i in range(2)],
            "S": [[int(v) for v in s0.row(i)] for i in range(2)],
            "Y": [[int(v) for v in y0.row(i)] for i in range(2)],
            "Z": [[int(v) for v in z0.row(i)] for i in range(2)],
            "h": [[int(v) for v in h0.row(i)] for i in range(2)],
            "det_h": int(h0.det()),
            "m_squared": int(-h0.det()),
            "beta": str(sp.factor(h0[0, 1] / h0[0, 0])),
            "Phi": "-log(118)/2",
        },
        "singular_Y_witness": {
            "Y": [[int(v) for v in singular_y.row(i)] for i in range(2)],
            "Z": [[int(v) for v in singular_z.row(i)] for i in range(2)],
            "rank_J": singular_j.rank(),
            "h": [[int(v) for v in singular_h.row(i)] for i in range(2)],
            "det_h": int(singular_h.det()),
        },
        "sector_effects": sector_effects,
        "scope": "local supplied smooth regular rank-two completed pair germs",
        "open": [
            "event_and_germ_realization",
            "null_degenerate_and_global_strata",
            "non_scalar_transport",
            "history_completion_and_X_max",
            "observations_dynamics_source_matter_and_signalling",
        ],
    }
    (HERE / "DERIVATION_RESULT.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n"
    )
    if status != "PASS":
        failed = [name for name, passed in checks.items() if not passed]
        raise SystemExit(f"FAIL: checks={failed}, hashes={hash_failures}")
    print(
        "PASS: arbitrary coframe/pair theorem, full BQSYZ witness, singular-Y witness, "
        "gauge/coordinate/reparameterization covariance, and live product rule"
    )


if __name__ == "__main__":
    main()
