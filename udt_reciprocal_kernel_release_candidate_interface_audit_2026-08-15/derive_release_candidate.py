#!/usr/bin/env python3
"""Exact release-candidate interface replay for the rebuilt reciprocal kernel."""

from __future__ import annotations

import json

import sympy as sp


R = sp.Rational
ETA2 = sp.diag(-1, 1)
ETA4 = sp.diag(-1, 1, 1, 1)
E00 = sp.Matrix([[1, 0], [0, 0]])
ZERO2 = sp.zeros(2)


def zero_matrix(matrix: sp.Matrix) -> bool:
    return all(sp.simplify(value) == 0 for value in matrix)


def state_matrices() -> list[dict[str, sp.Matrix]]:
    return [
        {
            "B": sp.Matrix([[2, R(1, 3)], [0, R(3, 2)]]),
            "Q": sp.Matrix([[R(3, 2), R(1, 5)], [0, R(4, 3)]]),
            "S": sp.Matrix([[R(1, 5), -R(1, 7)], [R(2, 9), R(1, 6)]]),
            "Y": sp.Matrix([[1, R(1, 10)], [-R(1, 8), 1]]),
            "Z": sp.Matrix([[R(1, 12), -R(1, 11)], [R(1, 13), R(1, 14)]]),
        },
        {
            "B": sp.Matrix([[R(9, 5), -R(1, 4)], [0, R(8, 5)]]),
            "Q": sp.Matrix([[R(7, 5), -R(1, 6)], [0, R(5, 4)]]),
            "S": sp.Matrix([[-R(1, 6), R(2, 11)], [R(1, 8), -R(1, 5)]]),
            "Y": sp.Matrix([[R(9, 10), -R(1, 9)], [R(1, 7), R(11, 10)]]),
            "Z": sp.Matrix([[-R(1, 15), R(1, 12)], [R(1, 10), -R(1, 16)]]),
        },
        {
            "B": sp.Matrix([[R(11, 5), R(2, 7)], [0, R(7, 5)]]),
            "Q": sp.Matrix([[R(5, 4), R(1, 7)], [0, R(3, 2)]]),
            "S": sp.Matrix([[R(2, 9), R(1, 10)], [-R(1, 6), R(2, 13)]]),
            "Y": sp.Matrix([[R(11, 10), R(1, 12)], [-R(1, 9), R(9, 10)]]),
            "Z": sp.Matrix([[R(1, 18), R(1, 13)], [-R(1, 11), R(1, 17)]]),
        },
    ]


def complete_coframe(state: dict[str, sp.Matrix]) -> sp.Matrix:
    b, q, s = state["B"], state["Q"], state["S"]
    return b.row_join(ZERO2).col_join((q * s).row_join(q))


def pair_jacobian(state: dict[str, sp.Matrix]) -> sp.Matrix:
    return state["Y"].col_join(state["Z"])


def pair_metric(state: dict[str, sp.Matrix]) -> tuple[sp.Matrix, sp.Matrix, sp.Matrix]:
    b, q, s, y, z = (state[key] for key in ("B", "Q", "S", "Y", "Z"))
    u = b * y
    a = q * (s * y + z)
    h = sp.simplify(u.T * ETA2 * u + a.T * a)
    return h, u, a


def terminal_coframe(h: sp.Matrix) -> tuple[sp.Matrix, sp.Expr, sp.Expr, sp.Expr]:
    t2 = -h[0, 0]
    beta = sp.simplify(h[0, 1] / h[0, 0])
    l2 = sp.simplify(h[1, 1] - h[0, 1] ** 2 / h[0, 0])
    t = sp.sqrt(t2)
    l = sp.sqrt(l2)
    bpair = sp.Matrix([[t, t * beta], [0, l]])
    return bpair, t, l, beta


def dphi(h: sp.Matrix, dh: sp.Matrix) -> sp.Expr:
    return sp.factor(sp.trace(h.inv() * dh) / 4 - dh[0, 0] / (2 * h[0, 0]))


def channel_variation(state: dict[str, sp.Matrix], channel: str) -> tuple[sp.Matrix, sp.Expr]:
    b, q, s, y, z = (state[key] for key in ("B", "Q", "S", "Y", "Z"))
    db = E00 if channel == "B" else ZERO2
    dq = E00 if channel == "Q" else ZERO2
    ds = E00 if channel == "S" else ZERO2
    dy = E00 if channel == "Y" else ZERO2
    dz = E00 if channel == "Z" else ZERO2
    u = b * y
    rleg = s * y + z
    aleg = q * rleg
    du = db * y + b * dy
    dr = ds * y + s * dy + dz
    da = dq * rleg + q * dr
    dh = sp.simplify(du.T * ETA2 * u + u.T * ETA2 * du + da.T * aleg + aleg.T * da)
    h, _, _ = pair_metric(state)
    return dh, dphi(h, dh)


def main() -> None:
    states = state_matrices()
    es = [complete_coframe(state) for state in states]
    js = [pair_jacobian(state) for state in states]
    hs = [pair_metric(state)[0] for state in states]
    terminals = [terminal_coframe(h) for h in hs]
    bps = [item[0] for item in terminals]
    ts = [item[1] for item in terminals]
    ls = [item[2] for item in terminals]

    direct_pullbacks = [sp.simplify(j.T * e.T * ETA4 * e * j) for e, j in zip(es, js)]
    terminal_reconstructions = [sp.simplify(bp.T * ETA2 * bp) for bp in bps]
    regular = [bool(h[0, 0] < 0 and h.det() < 0) for h in hs]

    # Ambient endpoint transitions and terminal endpoint transitions are distinct groupoids.
    a01 = sp.simplify(es[1] * es[0].inv())
    a12 = sp.simplify(es[2] * es[1].inv())
    a02 = sp.simplify(es[2] * es[0].inv())
    r01 = sp.simplify(bps[1] * bps[0].inv())
    r12 = sp.simplify(bps[2] * bps[1].inv())
    r02 = sp.simplify(bps[2] * bps[0].inv())

    ceff = [sp.simplify(t / l) for t, l in zip(ts, ls)]
    opz = [sp.sqrt(sp.simplify(l / t)) for t, l in zip(ts, ls)]
    ceff_rel_01 = sp.simplify(ceff[1] / ceff[0])
    ceff_rel_12 = sp.simplify(ceff[2] / ceff[1])
    ceff_rel_02 = sp.simplify(ceff[2] / ceff[0])

    sensitivities: dict[str, dict[str, object]] = {}
    for channel in ("B", "Q", "S", "Y", "Z"):
        dh, value = channel_variation(states[0], channel)
        sensitivities[channel] = {
            "dh_nonzero": not zero_matrix(dh),
            "dphi": str(value),
            "dphi_nonzero": bool(value != 0),
        }

    # Exact S/Z compensation: same pair metric and terminal state, different ambient transition.
    d = sp.Matrix([[R(2, 5), R(1, 11)], [-R(1, 13), R(3, 7)]])
    state1_alt = {key: value.copy() for key, value in states[1].items()}
    state1_alt["S"] = states[1]["S"] + d
    state1_alt["Z"] = states[1]["Z"] - d * states[1]["Y"]
    e1_alt = complete_coframe(state1_alt)
    h1_alt = pair_metric(state1_alt)[0]
    a01_alt = sp.simplify(e1_alt * es[0].inv())
    bp1_alt = terminal_coframe(h1_alt)[0]
    r01_alt = sp.simplify(bp1_alt * bps[0].inv())

    all_blocks_distinct = all(
        states[i][key] != states[j][key]
        for key in ("B", "Q", "S", "Y", "Z")
        for i, j in ((0, 1), (1, 2), (0, 2))
    )

    checks = {
        "three_states_regular": all(regular),
        "all_blocks_change_between_states": all_blocks_distinct,
        "direct_and_factored_pair_metrics_match": all(
            zero_matrix(direct - h) for direct, h in zip(direct_pullbacks, hs)
        ),
        "terminal_reconstruction_exact": all(
            zero_matrix(reconstructed - h) for reconstructed, h in zip(terminal_reconstructions, hs)
        ),
        "ambient_three_state_composition": zero_matrix(a12 * a01 - a02),
        "ambient_reversal": zero_matrix(a01.inv() - es[0] * es[1].inv()),
        "terminal_three_state_composition": zero_matrix(r12 * r01 - r02),
        "terminal_reversal": zero_matrix(r01.inv() - bps[0] * bps[1].inv()),
        "terminal_ceff_character_composes": sp.simplify(ceff_rel_12 * ceff_rel_01 - ceff_rel_02) == 0,
        "redshift_ceff_identity_each_state": all(
            sp.simplify(c * zfactor**2 - 1) == 0 for c, zfactor in zip(ceff, opz)
        ),
        "all_five_dh_sensitivities_nonzero": all(item["dh_nonzero"] for item in sensitivities.values()),
        "all_five_dphi_sensitivities_nonzero": all(item["dphi_nonzero"] for item in sensitivities.values()),
        "SZ_compensation_preserves_pair_metric": zero_matrix(h1_alt - hs[1]),
        "SZ_compensation_preserves_terminal_transition": zero_matrix(r01_alt - r01),
        "SZ_compensation_changes_ambient_transition": not zero_matrix(a01_alt - a01),
        "ambient_and_terminal_transitions_are_not_identical": a01.shape != r01.shape,
    }

    result = {
        "all_checks_pass": all(checks.values()),
        "checks": checks,
        "state_regularities": regular,
        "sensitivities": sensitivities,
        "sne_interface": {
            "pair_metric_to_phi_pair": "DERIVED_CONDITIONAL",
            "phi_pair_to_1_plus_z": "CONDITIONAL_REGISTERED_SNE_READOUT",
            "phi_pair_to_c_eff_over_cE": "DERIVED_CONDITIONAL_PAIR_IDENTITY",
            "null_screen_query_to_dA": "DERIVED_CONDITIONAL_ON_SUPPLIED_JACOBI_QUERY",
            "dA_to_dL_or_flux": "CONDITIONAL_NOT_KERNEL_DERIVED",
            "physical_history_and_pair_family": "OPEN",
        },
        "separation_witness": {
            "same_h_after_SZ_compensation": checks["SZ_compensation_preserves_pair_metric"],
            "same_terminal_R_after_SZ_compensation": checks["SZ_compensation_preserves_terminal_transition"],
            "different_ambient_A_after_SZ_compensation": checks["SZ_compensation_changes_ambient_transition"],
        },
        "landing": "KERNEL_COHERENT__GEOMETRIC_SNE_QUERY_READY_CONDITIONALLY__FULL_SNE_VALIDATION_BLOCKED_BY_PHYSICAL_HISTORY_AND_FLUX_OWNERSHIP",
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
