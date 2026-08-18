#!/usr/bin/env python3
"""Exact G149 Levi-Civita first-jet calculation on the preregistered witness."""

from __future__ import annotations

import json
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent
R = sp.Rational


def mat(rows):
    return sp.Matrix(rows)


def registered_data():
    B0 = mat([[2, R(1, 2)], [0, 3]])
    Q0 = mat([[1, R(1, 3)], [0, 2]])
    S0 = mat([[R(1, 5), -R(1, 7)], [R(1, 4), R(1, 6)]])
    dB = [
        mat([[R(1, 11), R(1, 13)], [-R(1, 17), R(1, 19)]]),
        mat([[-R(1, 23), R(1, 29)], [R(1, 31), -R(1, 37)]]),
        mat([[R(1, 41), -R(1, 43)], [R(1, 47), R(1, 53)]]),
        mat([[-R(1, 59), -R(1, 61)], [R(1, 67), R(1, 71)]]),
    ]
    dQ = [
        mat([[R(1, 73), -R(1, 79)], [R(1, 83), R(1, 89)]]),
        mat([[-R(1, 97), R(1, 101)], [R(1, 103), R(1, 107)]]),
        mat([[R(1, 109), R(1, 113)], [-R(1, 127), R(1, 131)]]),
        mat([[R(1, 137), -R(1, 139)], [R(1, 149), -R(1, 151)]]),
    ]
    dS = [
        mat([[-R(1, 157), R(1, 163)], [R(1, 167), -R(1, 173)]]),
        mat([[R(1, 179), R(1, 181)], [-R(1, 191), R(1, 193)]]),
        mat([[R(1, 197), -R(1, 199)], [R(1, 211), R(1, 223)]]),
        mat([[-R(1, 227), R(1, 229)], [-R(1, 233), R(1, 239)]]),
    ]
    J0 = mat([1, 0, R(1, 10), -R(1, 12)])
    J1 = mat([0, 1, -R(1, 8), R(1, 9)])
    Ftt = mat([R(1, 59), -R(1, 67), -R(1, 73), R(1, 83)])
    Fts = mat([R(1, 61), R(1, 71), R(1, 79), R(1, 89)])
    Fss = mat([R(1, 241), -R(1, 251), R(1, 257), -R(1, 263)])
    return B0, Q0, S0, dB, dQ, dS, J0, J1, Ftt, Fts, Fss


def assemble_E(B, Q, S):
    z = sp.zeros(2)
    return B.row_join(z).col_join((Q * S).row_join(Q))


def metric_and_derivatives(B0, Q0, S0, dB, dQ, dS):
    eta = sp.diag(-1, 1, 1, 1)
    E0 = assemble_E(B0, Q0, S0)
    dE = []
    for mu in range(4):
        upper = dB[mu].row_join(sp.zeros(2))
        lower_left = dQ[mu] * S0 + Q0 * dS[mu]
        lower = lower_left.row_join(dQ[mu])
        dE.append(upper.col_join(lower))
    g = sp.simplify(E0.T * eta * E0)
    dg = [sp.simplify(d.T * eta * E0 + E0.T * eta * d) for d in dE]
    return eta, E0, dE, g, dg


def christoffel(g, dg):
    gi = g.inv()
    Gamma = [[[sp.S.Zero for _ in range(4)] for _ in range(4)] for _ in range(4)]
    for rho in range(4):
        for mu in range(4):
            for nu in range(4):
                Gamma[rho][mu][nu] = sp.factor(
                    sum(
                        gi[rho, sig]
                        * (dg[mu][sig, nu] + dg[nu][sig, mu] - dg[sig][mu, nu])
                        for sig in range(4)
                    )
                    / 2
                )
    return Gamma


def gamma_apply(Gamma, a, b):
    return mat(
        [
            sum(Gamma[rho][mu][nu] * a[mu] * b[nu] for mu in range(4) for nu in range(4))
            for rho in range(4)
        ]
    )


def inner(g, a, b):
    return sp.factor((a.T * g * b)[0])


def exact_zero(expr):
    return sp.simplify(expr) == 0


def vector_zero(vec):
    return all(exact_zero(x) for x in vec)


def evaluate(dB, dQ, dS, Ftt, Fts):
    B0, Q0, S0, _, _, _, J0, J1, _, _, _ = registered_data()
    _, E0, dE, g, dg = metric_and_derivatives(B0, Q0, S0, dB, dQ, dS)
    Gamma = christoffel(g, dg)

    J = J0.row_join(J1)
    Jtau = Ftt.row_join(Fts)
    h = sp.simplify(J.T * g * J)
    g_tau = sp.simplify(sum((J0[mu] * dg[mu] for mu in range(4)), sp.zeros(4)))
    h_tau = sp.simplify(Jtau.T * g * J + J.T * g_tau * J + J.T * g * Jtau)

    h00, h01 = h[0, 0], h[0, 1]
    h00_tau, h01_tau = h_tau[0, 0], h_tau[0, 1]
    T = sp.sqrt(-h00)
    T_tau = sp.factor(-h00_tau / (2 * T))
    beta = sp.factor(h01 / h00)
    beta_tau = sp.factor((h01_tau * h00 - h01 * h00_tau) / h00**2)

    rvec = sp.simplify(J1 - beta * J0)
    rvec_tau = sp.simplify(Fts - beta_tau * J0 - beta * Ftt)
    L2 = inner(g, rvec, rvec)
    L = sp.sqrt(L2)
    L2_tau = sp.factor(2 * inner(g, rvec_tau, rvec) + inner(g_tau, rvec, rvec))
    L_tau = sp.factor(L2_tau / (2 * L))

    u = sp.simplify(J0 / T)
    u_tau = sp.simplify(Ftt / T - J0 * T_tau / T**2)
    n = sp.simplify(rvec / L)
    n_tau = sp.simplify(rvec_tau / L - rvec * L_tau / L**2)

    nabla_u_u = sp.simplify(u_tau / T + gamma_apply(Gamma, u, u))
    nabla_u_n = sp.simplify(n_tau / T + gamma_apply(Gamma, u, n))
    a_n = sp.factor(inner(g, nabla_u_u, n))
    gnu = sp.factor(inner(g, nabla_u_n, u))
    gnn = sp.factor(inner(g, nabla_u_n, n))
    Omega = sp.simplify(nabla_u_n + gnu * u - gnn * n)

    det_h = sp.factor(h.det())
    det_h_tau = sp.factor(det_h * sp.trace(h.inv() * h_tau))
    phi_ratio = sp.factor((-det_h) / h00**2)
    phi_tau_direct = sp.factor((det_h_tau / det_h - 2 * h00_tau / h00) / 4)
    phi_tau_trace = sp.factor(sp.trace(h.inv() * h_tau) / 4 - h00_tau / (2 * h00))
    dotphi = sp.factor(phi_tau_direct / T)

    X, q = sp.symbols("X q", real=True)
    rho = X * q
    rho_tau = X * (1 - q**2) * phi_tau_direct
    xi = sp.simplify(rho * n)
    xi_tau = sp.simplify(rho_tau * n + rho * n_tau)
    nabla_u_xi_direct = sp.simplify(xi_tau / T + gamma_apply(Gamma, u, xi))
    nabla_u_xi_split = sp.simplify(
        X * (1 - q**2) * dotphi * n + X * q * Omega + X * q * a_n * u
    )
    xi_residual = sp.simplify(nabla_u_xi_direct - nabla_u_xi_split)

    metric_compatibility = []
    torsion = []
    for rho_i in range(4):
        for mu in range(4):
            for nu in range(4):
                metric_compatibility.append(
                    sp.simplify(
                        dg[rho_i][mu, nu]
                        - sum(Gamma[sig][rho_i][mu] * g[sig, nu] for sig in range(4))
                        - sum(Gamma[sig][rho_i][nu] * g[mu, sig] for sig in range(4))
                    )
                )
                torsion.append(sp.simplify(Gamma[rho_i][mu][nu] - Gamma[rho_i][nu][mu]))

    return {
        "E0": E0,
        "dE": dE,
        "g": g,
        "dg": dg,
        "Gamma": Gamma,
        "h": h,
        "h_tau": h_tau,
        "det_h": det_h,
        "phi_ratio": phi_ratio,
        "T": T,
        "L": L,
        "beta": beta,
        "u": u,
        "n": n,
        "dotphi": dotphi,
        "phi_tau_direct": phi_tau_direct,
        "phi_tau_trace": phi_tau_trace,
        "nabla_u_u": nabla_u_u,
        "nabla_u_n": nabla_u_n,
        "a_n": a_n,
        "Omega": Omega,
        "xi_direct": nabla_u_xi_direct,
        "xi_split": nabla_u_xi_split,
        "xi_residual": xi_residual,
        "metric_compatibility": metric_compatibility,
        "torsion": torsion,
        "orthonormal": {
            "uu_plus_one": sp.simplify(inner(g, u, u) + 1),
            "nn_minus_one": sp.simplify(inner(g, n, n) - 1),
            "un": sp.simplify(inner(g, u, n)),
        },
        "screen": {
            "Omega_u": sp.simplify(inner(g, Omega, u)),
            "Omega_n": sp.simplify(inner(g, Omega, n)),
        },
        "nabla_n_decomposition": sp.simplify(nabla_u_n - a_n * u - Omega),
    }


def numeric(x, digits=17):
    return float(sp.N(x, digits))


def numeric_vector(v):
    return [numeric(x) for x in v]


def changed(base, control):
    if not exact_zero(base["dotphi"] - control["dotphi"]):
        return True
    if not exact_zero(base["a_n"] - control["a_n"]):
        return True
    return any(not exact_zero(base["Omega"][i] - control["Omega"][i]) for i in range(4))


def g148_registered_lambda_phidot():
    """Reconstruct the exact G148 algebraic lambda derivative (not a spacetime derivative)."""
    B0, Q0, S0, _, _, _, J0, J1, _, _, _ = registered_data()
    eta = sp.diag(-1, 1, 1, 1)
    dB = mat([[R(1, 11), R(1, 13)], [-R(1, 17), R(1, 19)]])
    dQ = mat([[R(1, 23), -R(1, 29)], [R(1, 31), R(1, 37)]])
    dS = mat([[-R(1, 41), R(1, 43)], [R(1, 47), -R(1, 53)]])
    dY = mat([[R(1, 59), R(1, 61)], [-R(1, 67), R(1, 71)]])
    dZ = mat([[-R(1, 73), R(1, 79)], [R(1, 83), R(1, 89)]])
    E0 = assemble_E(B0, Q0, S0)
    dE = dB.row_join(sp.zeros(2)).col_join(
        (dQ * S0 + Q0 * dS).row_join(dQ)
    )
    g = sp.simplify(E0.T * eta * E0)
    gdot = sp.simplify(dE.T * eta * E0 + E0.T * eta * dE)
    J = J0.row_join(J1)
    Jdot = dY.col_join(dZ)
    h = sp.simplify(J.T * g * J)
    hdot = sp.simplify(Jdot.T * g * J + J.T * gdot * J + J.T * g * Jdot)
    return sp.factor(sp.trace(h.inv() * hdot) / 4 - hdot[0, 0] / (2 * h[0, 0]))


def main():
    B0, Q0, S0, dB, dQ, dS, J0, J1, Ftt, Fts, Fss = registered_data()
    base = evaluate(dB, dQ, dS, Ftt, Fts)
    zero2 = [sp.zeros(2) for _ in range(4)]

    Ftt_no_y = Ftt.copy()
    Fts_no_y = Fts.copy()
    Ftt_no_y[0] = Ftt_no_y[1] = 0
    Fts_no_y[0] = Fts_no_y[1] = 0
    Ftt_no_z = Ftt.copy()
    Fts_no_z = Fts.copy()
    Ftt_no_z[2] = Ftt_no_z[3] = 0
    Fts_no_z[2] = Fts_no_z[3] = 0

    controls = {
        "B": evaluate(zero2, dQ, dS, Ftt, Fts),
        "Q": evaluate(dB, zero2, dS, Ftt, Fts),
        "S": evaluate(dB, dQ, zero2, Ftt, Fts),
        "Y": evaluate(dB, dQ, dS, Ftt_no_y, Fts_no_y),
        "Z": evaluate(dB, dQ, dS, Ftt_no_z, Fts_no_z),
    }
    liveness = {name: changed(base, control) for name, control in controls.items()}

    q = sp.symbols("q", real=True)
    X = sp.symbols("X", real=True)
    wrong_sign = sp.simplify(base["xi_direct"] - (
        X * (1 - q**2) * base["dotphi"] * base["n"]
        + X * q * base["Omega"] - X * q * base["a_n"] * base["u"]
    ))
    omitted_omega = sp.simplify(base["xi_direct"] - (
        X * (1 - q**2) * base["dotphi"] * base["n"]
        + X * q * base["a_n"] * base["u"]
    ))

    # G148's lambda derivative is deliberately reconstructed in its own algebraic type.
    lambda_surrogate = g148_registered_lambda_phidot()

    exact_gates = {
        "regular_h00_negative": bool(base["h"][0, 0] < 0),
        "regular_det_h_negative": bool(base["det_h"] < 0),
        "orthonormal": all(exact_zero(v) for v in base["orthonormal"].values()),
        "torsion_free": all(exact_zero(v) for v in base["torsion"]),
        "metric_compatible": all(exact_zero(v) for v in base["metric_compatibility"]),
        "dotphi_trace_identity": exact_zero(base["phi_tau_direct"] - base["phi_tau_trace"]),
        "screen_orthogonal": all(exact_zero(v) for v in base["screen"].values()),
        "nabla_n_decomposition": vector_zero(base["nabla_n_decomposition"]),
        "g148_identity": vector_zero(base["xi_residual"]),
        "all_BQS_gradient_and_clock_direction_YZ_families_live": all(liveness.values()),
        "wrong_sign_caught": not vector_zero(wrong_sign),
        "omitted_omega_caught": not vector_zero(omitted_omega),
        "lambda_substitution_caught": not exact_zero(base["dotphi"] - lambda_surrogate),
    }

    result = {
        "schema": "udt.g149.production.v1",
        "status": "PASS" if all(exact_gates.values()) else "FAIL",
        "scope": "one preregistered local smooth complete-coframe and quadratic pair-immersion witness",
        "witness": {
            "det_E0": str(sp.factor(base["E0"].det())),
            "det_g0": str(sp.factor(base["g"].det())),
            "h": [[str(base["h"][i, j]) for j in range(2)] for i in range(2)],
            "det_h": str(base["det_h"]),
            "phi_ratio": str(base["phi_ratio"]),
            "T_float": numeric(base["T"]),
            "L_float": numeric(base["L"]),
            "beta_float": numeric(base["beta"]),
        },
        "derived_first_jet": {
            "dotphi_exact": str(base["dotphi"]),
            "dotphi_float": numeric(base["dotphi"]),
            "a_n_exact": str(base["a_n"]),
            "a_n_float": numeric(base["a_n"]),
            "Omega_float": numeric_vector(base["Omega"]),
            "Omega_norm2_float": numeric(inner(base["g"], base["Omega"], base["Omega"])),
            "g148_lambda_phidot_float": numeric(lambda_surrogate),
        },
        "liveness": {
            name: {
                "changed": liveness[name],
                "delta_dotphi_float": numeric(base["dotphi"] - control["dotphi"]),
                "delta_a_n_float": numeric(base["a_n"] - control["a_n"]),
                "delta_Omega_float": numeric_vector(base["Omega"] - control["Omega"]),
            }
            for name, control in controls.items()
        },
        "exact_gates": exact_gates,
        "premise_stamps": {
            "metric_and_pullback": "DERIVED_ON_SUPPLIED_SMOOTH_WITNESS",
            "position_representation": "CHOSE_WORKING_RELATION_FIRST_REPRESENTATION",
            "witness_values": "CHOSE_NUMERICAL_WITNESS",
            "levi_civita_first_jet": "DERIVED_FROM_SUPPLIED_METRIC_AND_PAIR",
            "physical_history": "OPEN",
            "dynamics": "OPEN",
            "regime_amplitudes": "OPEN",
            "X_max_value_and_global_realization": "OPEN",
        },
        "maximum_conclusion": (
            "EXPLICIT_SMOOTH_COMPLETE_SPACETIME_QUERY_WITNESS__"
            "PAIR_CLOCK_DERIVED_DOTPHI__LEVI_CIVITA_DERIVED_AN_OMEGA__"
            "G148_COVARIANT_IDENTITY_EXACTLY_REALIZED__"
            "ALL_BQS_SPACETIME_GRADIENT_FAMILIES_AND_PAIR_CLOCK_DIRECTION_YZ_FIRST_JETS_LIVE_IN_THE_REGISTERED_WITNESS__"
            "PHYSICAL_HISTORY_DYNAMICS_REGIME_AMPLITUDES_AND_GLOBAL_COMPLETION_OPEN"
        ),
    }
    (HERE / "DERIVATION_RESULT.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))
    if result["status"] != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
