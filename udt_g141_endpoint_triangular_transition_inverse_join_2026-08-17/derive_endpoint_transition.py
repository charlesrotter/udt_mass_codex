#!/usr/bin/env python3
"""Exact production derivation for G141 without radical matrix expansion."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
ETA4 = sp.diag(-1, 1, 1, 1)


def require(condition: bool, label: str, checks: list[str]) -> None:
    if not condition:
        raise AssertionError(label)
    checks.append(label)


def matrix_zero(matrix: sp.Matrix) -> bool:
    return all(sp.cancel(value) == 0 for value in matrix)


def main() -> None:
    checks: list[str] = []

    # Abstract positive-triangular theorem.  Positivity is a declared regular-stratum hypothesis;
    # all polynomial/rational identities below are exact.
    TA, LA, TB, LB, TC, LC = sp.symbols("T_A L_A T_B L_B T_C L_C", positive=True)
    bA, bB, bC = sp.symbols("beta_A beta_B beta_C", real=True)

    def R(T, L, beta):
        return sp.Matrix([[T, T * beta], [0, L]])

    RA, RB, RC = R(TA, LA, bA), R(TB, LB, bB), R(TC, LC, bC)
    CBA, CCB, CCA, CAB = RB * RA.inv(), RC * RB.inv(), RC * RA.inv(), RA * RB.inv()
    # Two different, carrier-dependent automorphisms are useful and must not be conflated:
    # C_BA acts on the shared model clock/ruler plane and compares calibrations; D_BA acts on the
    # shared pair-coordinate carrier and matches h_B back to h_A.  Neither is thereby the full
    # four-dimensional observer-chart differential.
    DBA, DCB, DCA, DAB = RB.inv() * RA, RC.inv() * RB, RC.inv() * RA, RA.inv() * RB
    require(matrix_zero(CBA * RA - RB), "relative_transition_definition", checks)
    require(matrix_zero(CCB * CBA - CCA), "transition_composition", checks)
    require(matrix_zero(CAB * CBA - sp.eye(2)), "transition_reversal", checks)
    require(matrix_zero(RA * RA.inv() - sp.eye(2)), "transition_identity", checks)
    require(CBA[1, 0] == CCB[1, 0] == CCA[1, 0] == 0, "positive_triangular_subgroup", checks)
    require(sp.cancel(CBA[1, 1] / CBA[0, 0] - (LB / TB) / (LA / TA)) == 0,
            "grading_is_endpoint_ratio_BA", checks)
    require(sp.cancel(CCB[1, 1] / CCB[0, 0] - (LC / TC) / (LB / TB)) == 0,
            "grading_is_endpoint_ratio_CB", checks)
    require(sp.cancel(CCA[1, 1] / CCA[0, 0] - (LC / TC) / (LA / TA)) == 0,
            "grading_is_endpoint_ratio_CA", checks)
    require(sp.cancel((CCB * CBA)[1, 1] / (CCB * CBA)[0, 0]
                      - (CCB[1, 1] / CCB[0, 0]) * (CBA[1, 1] / CBA[0, 0])) == 0,
            "grading_character_composes", checks)
    require(sp.cancel((CAB[1, 1] / CAB[0, 0]) * (CBA[1, 1] / CBA[0, 0]) - 1) == 0,
            "grading_character_reverses", checks)
    require(sp.cancel(CBA[0, 0] * CBA[1, 1] - (TB * LB) / (TA * LA)) == 0,
            "scale_character_is_endpoint_difference", checks)
    require(sp.cancel((CCB * CBA).det() - CCB.det() * CBA.det()) == 0,
            "scale_character_composes", checks)
    require(sp.cancel(CBA[0, 1] - TB * (bB - bA) / LA) == 0,
            "relative_shift_retained", checks)
    p0, p1 = sp.symbols("p_0 p_1", positive=True)
    pw = sp.symbols("p_w", real=True)
    P = sp.Matrix([[p0, pw], [0, p1]])
    Rprime = RA * P
    require(sp.cancel((Rprime[1, 1] / Rprime[0, 0])
                      / (RA[1, 1] / RA[0, 0]) - p1 / p0) == 0,
            "endpoint_phi_changes_under_independent_triangular_gauge", checks)
    require(matrix_zero(DCB * DBA - DCA), "pair_carrier_matching_map_composes", checks)
    require(matrix_zero(DAB * DBA - sp.eye(2)), "pair_carrier_matching_map_reverses", checks)
    require(DBA[1, 0] == DCB[1, 0] == DCA[1, 0] == 0,
            "pair_carrier_matching_map_positive_triangular", checks)
    require(sp.cancel(DBA[1, 1] / DBA[0, 0] - (LA / TA) / (LB / TB)) == 0,
            "pair_carrier_matching_grading_is_negative_endpoint_depth", checks)
    require(sp.cancel(DAB[1, 1] / DAB[0, 0] - (LB / TB) / (LA / TA)) == 0,
            "inverse_pair_carrier_matching_grading_is_endpoint_depth", checks)
    hA, hB = RA.T * sp.diag(-1, 1) * RA, RB.T * sp.diag(-1, 1) * RB
    require(matrix_zero(DBA.T * hB * DBA - hA), "pair_carrier_matching_map_preserves_metrics", checks)
    require(sp.cancel(DBA.det() - (TA * LA) / (TB * LB)) == 0,
            "pair_carrier_matching_common_scale_character", checks)
    require(sp.cancel(CBA[1, 1] / CBA[0, 0] - DAB[1, 1] / DAB[0, 0]) == 0,
            "calibration_and_carrier_maps_share_inverse_grading_not_shift", checks)
    boost = sp.Matrix([[sp.Rational(5, 4), sp.Rational(3, 4)],
                       [sp.Rational(3, 4), sp.Rational(5, 4)]])
    require(matrix_zero(boost.T * sp.diag(-1, 1) * boost - sp.diag(-1, 1)),
            "endpoint_metric_allows_nontrivial_lorentz_transition", checks)
    require(boost != sp.eye(2), "nontrivial_transition_not_recovered_from_equal_metrics", checks)

    # The terminal formula of h_rel=C^T eta C reads the grading of C exactly.  Squaring avoids
    # branch-sensitive log simplification while positivity fixes the unique logarithm.
    a, d = sp.symbols("a d", positive=True)
    u = sp.symbols("u", real=True)
    C = sp.Matrix([[a, u], [0, d]])
    hrel = C.T * sp.diag(-1, 1) * C
    terminal_rho = sp.cancel((-hrel.det()) / hrel[0, 0] ** 2)
    require(sp.cancel(terminal_rho - (d / a) ** 2) == 0,
            "relative_terminal_readout_is_grading_squared", checks)

    qA, qB, qC = sp.symbols("q_A q_B q_C", positive=True)
    qBA, qCB, qCA = qB / qA, qC / qB, qC / qA
    require(sp.cancel(qCB * qBA - qCA) == 0, "q_ratio_composes", checks)
    require(sp.cancel((qA / qB) * qBA - 1) == 0, "q_ratio_reverses", checks)
    xBA, xCB, xCA = [(1 - q) / (1 + q) for q in (qBA, qCB, qCA)]
    require(sp.cancel((xBA + xCB) / (1 + xBA * xCB) - xCA) == 0,
            "mobius_position_composes", checks)
    z = sp.symbols("z", positive=True)
    D = sp.diag(1 / z, z)
    require(sp.cancel((D[1, 1] / D[0, 0]) - z**2) == 0,
            "pure_reciprocal_matrix_retained", checks)

    # Exact rational all-instruments witness.  Endpoint logarithms are represented by their
    # positive rational rho_i=exp(4 Phi_i), so no radical expansion enters certification.
    B = sp.Matrix([[2, sp.Rational(1, 5)], [0, sp.Rational(3, 2)]])
    Q = sp.Matrix([[sp.Rational(4, 3), sp.Rational(1, 7)], [0, sp.Rational(5, 4)]])
    S = sp.Matrix([
        [sp.Rational(1, 10), -sp.Rational(1, 12)],
        [sp.Rational(1, 15), sp.Rational(1, 9)],
    ])
    E = B.row_join(sp.zeros(2)).col_join((Q * S).row_join(Q))
    g = E.T * ETA4 * E

    def complete_metric(Bx, Qx, Sx):
        Ex = Bx.row_join(sp.zeros(2)).col_join((Qx * Sx).row_join(Qx))
        return Ex.T * ETA4 * Ex

    B_no_shift = B.copy()
    B_no_shift[0, 1] = 0
    Q_no_shear = Q.copy()
    Q_no_shear[0, 1] = 0
    g_no_base_shift = complete_metric(B_no_shift, Q, S)
    g_no_screen_shear = complete_metric(B, Q_no_shear, S)
    g_no_mixing = complete_metric(B, Q, sp.zeros(2))
    raw = {
        "A": (sp.eye(2), sp.Matrix([[sp.Rational(1, 20), -sp.Rational(1, 25)],
                                     [sp.Rational(1, 30), sp.Rational(1, 18)]])),
        "B": (sp.Matrix([[1, sp.Rational(1, 20)], [-sp.Rational(1, 30), 1]]),
              sp.Matrix([[-sp.Rational(1, 24), sp.Rational(1, 28)],
                         [sp.Rational(1, 32), -sp.Rational(1, 21)]])),
        "C": (sp.Matrix([[1, -sp.Rational(1, 25)], [sp.Rational(1, 40), 1]]),
              sp.Matrix([[sp.Rational(1, 27), sp.Rational(1, 31)],
                         [-sp.Rational(1, 29), sp.Rational(1, 26)]])),
    }
    require(E.det() != 0, "complete_coframe_invertible", checks)
    require(g == E.T * ETA4 * E, "metric_is_complete_coframe_pullback", checks)
    require(B[0, 1] != 0 and Q[0, 1] != 0 and all(value != 0 for value in S),
            "base_screen_mixing_channels_nonzero", checks)

    endpoints = {}
    endpoint_J = {}
    channel_sensitivity = {
        "base_shift": False,
        "screen_shear": False,
        "mixing": False,
        "angular_embedding": False,
    }
    for name, (Y, Z) in raw.items():
        J = Y.col_join(Z)
        A_screen = (E * J)[2:, :]
        h = J.T * g * J
        J_no_angular = Y.col_join(sp.zeros(2))
        channel_sensitivity["base_shift"] |= not matrix_zero(h - J.T * g_no_base_shift * J)
        channel_sensitivity["screen_shear"] |= not matrix_zero(h - J.T * g_no_screen_shear * J)
        channel_sensitivity["mixing"] |= not matrix_zero(h - J.T * g_no_mixing * J)
        channel_sensitivity["angular_embedding"] |= not matrix_zero(h - J_no_angular.T * g * J_no_angular)
        det_h = sp.factor(h.det())
        beta = sp.cancel(h[0, 1] / h[0, 0])
        rho = sp.factor((-det_h) / h[0, 0] ** 2)
        require(J.rank() == 2, f"rank_two_J_{name}", checks)
        require(h[0, 0] < 0, f"timelike_clock_{name}", checks)
        require(det_h < 0, f"lorentz_pair_{name}", checks)
        require(A_screen != sp.zeros(2), f"screen_mixing_reaches_pair_{name}", checks)
        require(rho > 0, f"positive_terminal_ratio_{name}", checks)
        endpoint_J[name] = J
        endpoints[name] = {"h": h, "det_h": det_h, "beta": beta, "rho": rho}

    # The witness domains share the deliberately supplied abstract pair coordinates, but their
    # ambient image planes are different.  This prevents the 2D carrier algebra from being
    # misreported as an ambient/full-chart transition.
    for target, source in (("B", "A"), ("C", "B"), ("C", "A")):
        require(endpoint_J[source].row_join(endpoint_J[target]).rank() == 4,
                f"ambient_pair_planes_distinct_{target}{source}", checks)
    for channel, sensitive in channel_sensitivity.items():
        require(sensitive, f"witness_sensitive_to_{channel}", checks)

    require(any(endpoints[t]["beta"] != endpoints[s]["beta"]
                for t, s in (("B", "A"), ("C", "B"), ("C", "A"))),
            "nonzero_relative_shift_witness", checks)
    rho_BA = sp.cancel(endpoints["B"]["rho"] / endpoints["A"]["rho"])
    rho_CB = sp.cancel(endpoints["C"]["rho"] / endpoints["B"]["rho"])
    rho_CA = sp.cancel(endpoints["C"]["rho"] / endpoints["A"]["rho"])
    require(sp.cancel(rho_CB * rho_BA - rho_CA) == 0,
            "witness_endpoint_grading_ratio_composes", checks)
    require(sp.cancel((1 / rho_BA) * rho_BA - 1) == 0,
            "witness_endpoint_grading_ratio_reverses", checks)

    lines = (HERE / "SOURCE_MANIFEST.tsv").read_text(encoding="utf-8").splitlines()[1:]
    hashes = {}
    for line in lines:
        expected, rel, _role = line.split("\t")
        actual = hashlib.sha256((ROOT / rel).read_bytes()).hexdigest()
        require(actual == expected, f"source_hash_{Path(rel).parent.name or Path(rel).stem}", checks)
        hashes[rel] = actual

    result = {
        "status": "PASS",
        "checks_passed": len(checks),
        "checks_total": len(checks),
        "checks": checks,
        "abstract_landing": {
            "preregistered_calibration_transition": "C_BA=R_B R_A^-1 on a supplied shared carrier",
            "pair_carrier_matching_map": "D_BA=R_B^-1 R_A; D_CB D_BA=D_CA on the same supplied carrier",
            "reciprocal_character": "delta_AB=log(C_BA11/C_BA00)/2=Phi_B-Phi_A",
            "common_scale_character": "kappa(C)=log(C00*C11)/2=kappa_B-kappa_A",
            "relative_terminal": "phi_pair(C_BA^T eta C_BA)=delta_AB on the positive triangular stratum",
            "type_guard": "neither 2D map is identified with the full G123 four-dimensional chart differential",
        },
        "metric": {
            "det_E": str(E.det()),
            "det_g": str(g.det()),
            "signature_proof": "g=E^T diag(-1,1,1,1) E with det(E)!=0",
        },
        "endpoints": {
            name: {
                "h00": str(state["h"][0, 0]),
                "det_h": str(state["det_h"]),
                "beta": str(state["beta"]),
                "rho_exp_4Phi": str(state["rho"]),
            }
            for name, state in endpoints.items()
        },
        "witness_ratios": {
            "rho_BA": str(rho_BA), "rho_CB": str(rho_CB), "rho_CA": str(rho_CA),
        },
        "source_hashes": hashes,
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
