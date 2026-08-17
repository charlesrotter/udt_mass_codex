#!/usr/bin/env python3
"""Exact G148 production derivation. Uses SymPy only; no observational inputs."""

from __future__ import annotations

import json
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent


def all_zero(matrix: sp.Matrix) -> bool:
    return all(sp.simplify(x) == 0 for x in matrix)


def any_nonzero(matrix: sp.Matrix) -> bool:
    return any(sp.simplify(x) != 0 for x in matrix)


def q(n: int, d: int = 1) -> sp.Rational:
    return sp.Rational(n, d)


eta2 = sp.diag(-1, 1)
eta4 = sp.diag(-1, 1, 1, 1)

B0 = sp.Matrix([[2, q(1, 2)], [0, 3]])
Q0 = sp.Matrix([[1, q(1, 3)], [0, 2]])
S0 = sp.Matrix([[q(1, 5), q(-1, 7)], [q(1, 4), q(1, 6)]])
Y0 = sp.eye(2)
Z0 = sp.Matrix([[q(1, 10), q(-1, 8)], [q(-1, 12), q(1, 9)]])

jets = {
    "B": sp.Matrix([[q(1, 11), q(1, 13)], [q(-1, 17), q(1, 19)]]),
    "Q": sp.Matrix([[q(1, 23), q(-1, 29)], [q(1, 31), q(1, 37)]]),
    "S": sp.Matrix([[q(-1, 41), q(1, 43)], [q(1, 47), q(-1, 53)]]),
    "Y": sp.Matrix([[q(1, 59), q(1, 61)], [q(-1, 67), q(1, 71)]]),
    "Z": sp.Matrix([[q(-1, 73), q(1, 79)], [q(1, 83), q(1, 89)]]),
}


def build(t: sp.Symbol, active: tuple[str, ...]):
    zero = sp.zeros(2)
    B = B0 + t * (jets["B"] if "B" in active else zero)
    Q = Q0 + t * (jets["Q"] if "Q" in active else zero)
    S = S0 + t * (jets["S"] if "S" in active else zero)
    Y = Y0 + t * (jets["Y"] if "Y" in active else zero)
    Z = Z0 + t * (jets["Z"] if "Z" in active else zero)
    E = B.row_join(sp.zeros(2)).col_join((Q * S).row_join(Q))
    J = Y.col_join(Z)
    g = sp.simplify(E.T * eta4 * E)
    h = sp.simplify(J.T * g * J)
    P = sp.simplify(sp.eye(4) - J * h.inv() * J.T * g)
    return g, J, h, P


checks: dict[str, bool] = {}
details: dict[str, object] = {}

# Abstract covariant decomposition in an orthonormal query flag.
phi, dphi, X, a, o1, o2 = sp.symbols("phi dphi X a o1 o2", real=True)
u = sp.Matrix([1, 0, 0, 0])
n = sp.Matrix([0, 1, 0, 0])
e1 = sp.Matrix([0, 0, 1, 0])
e2 = sp.Matrix([0, 0, 0, 1])
Omega = o1 * e1 + o2 * e2
rho = X * sp.tanh(phi)
drho = X * sp.sech(phi) ** 2 * dphi
dn = a * u + Omega
dxi = drho * n + rho * dn
claimed = drho * n + rho * a * u + rho * Omega
P_rest = sp.eye(4) + u * (u.T * eta4)
P_screen = sp.eye(4) + u * (u.T * eta4) - n * (n.T * eta4)
v_rest = sp.simplify(P_rest * dxi)

checks["covariant_vector_decomposition"] = all_zero(sp.simplify(dxi - claimed))
checks["screen_piece_in_pair_screen"] = all_zero(sp.simplify(P_screen * Omega - Omega))
checks["rest_projection"] = all_zero(sp.simplify(v_rest - drho * n - rho * Omega))
rest_norm = sp.simplify((v_rest.T * eta4 * v_rest)[0])
full_norm = sp.simplify((dxi.T * eta4 * dxi)[0])
checks["rest_norm_split"] = sp.simplify(rest_norm - drho**2 - rho**2 * (o1**2 + o2**2)) == 0
checks["ambient_norm_split"] = sp.simplify(
    full_norm - drho**2 + rho**2 * a**2 - rho**2 * (o1**2 + o2**2)
) == 0
checks["radial_derivative"] = sp.simplify(sp.diff(X * sp.tanh(phi), phi) * dphi - drho) == 0

# Catch proofs: deleting any genuine component must leave a nonzero symbolic residual.
checks["catch_missing_screen_term"] = any_nonzero(sp.simplify(dxi - (drho * n + rho * a * u)))
checks["catch_missing_rest_space_tilt"] = any_nonzero(sp.simplify(dxi - (drho * n + rho * Omega)))
checks["catch_wrong_radial_weight"] = any_nonzero(
    sp.simplify(dxi - (X * dphi * n + rho * a * u + rho * Omega))
)

# Regime weights are characterized, never used as an acceptance filter.
wr = sp.sech(phi) ** 2
ws = sp.tanh(phi)
checks["radial_weight_neutral"] = sp.limit(wr, phi, 0) == 1
checks["screen_weight_neutral"] = sp.limit(ws, phi, 0) == 0
checks["screen_weight_unit_slope"] = sp.limit(ws / phi, phi, 0) == 1
checks["radial_weight_positive_endpoint"] = sp.limit(wr, phi, sp.oo) == 0
checks["radial_weight_negative_endpoint"] = sp.limit(wr, phi, -sp.oo) == 0
checks["screen_weight_positive_endpoint"] = sp.limit(ws, phi, sp.oo) == 1
checks["screen_weight_negative_endpoint"] = sp.limit(ws, phi, -sp.oo) == -1

# Generic terminal derivative, derived independently from a formal 2x2 metric jet.
eps = sp.symbols("eps", real=True)
h00, h01, h11, dh00, dh01, dh11 = sp.symbols(
    "h00 h01 h11 dh00 dh01 dh11", real=True, nonzero=True
)
h_generic = sp.Matrix([[h00 + eps * dh00, h01 + eps * dh01], [h01 + eps * dh01, h11 + eps * dh11]])
phi_generic = sp.log(-h_generic.det() / h_generic[0, 0] ** 2) / 4
direct_dphi = sp.simplify(sp.diff(phi_generic, eps).subs(eps, 0))
h_base_generic = h_generic.subs(eps, 0)
dh_generic = sp.diff(h_generic, eps)
trace_dphi = sp.simplify(
    sp.trace(h_base_generic.inv() * dh_generic) / 4 - dh_generic[0, 0] / (2 * h_base_generic[0, 0])
)
checks["terminal_phi_derivative_identity"] = sp.simplify(direct_dphi - trace_dphi) == 0

# Exact complete-coframe liveness at the preregistered witness.
t = sp.symbols("lambda", real=True)
g_base, J_base, h_base, P_base = build(t, tuple())
h_base = h_base.subs(t, 0)
checks["base_h00_timelike"] = bool(h_base[0, 0] < 0)
checks["base_pair_lorentzian"] = bool(h_base.det() < 0)

block_results: dict[str, object] = {}
block_hdot: dict[str, sp.Matrix] = {}
for name in jets:
    g, J, h, P = build(t, (name,))
    hdot = sp.simplify(sp.diff(h, t).subs(t, 0))
    Pdot = sp.simplify(sp.diff(P, t).subs(t, 0))
    phidot = sp.simplify(sp.trace(h_base.inv() * hdot) / 4 - hdot[0, 0] / (2 * h_base[0, 0]))
    live = any_nonzero(hdot) or any_nonzero(Pdot) or phidot != 0
    checks[f"{name}_first_jet_live"] = bool(live)
    block_hdot[name] = hdot
    block_results[name] = {
        "hdot": [[str(sp.factor(x)) for x in hdot.row(i)] for i in range(2)],
        "phidot": str(sp.factor(phidot)),
        "projector_dot_nonzero": any_nonzero(Pdot),
    }

g_all, J_all, h_all, P_all = build(t, tuple(jets))
hdot_all = sp.simplify(sp.diff(h_all, t).subs(t, 0))
Pdot_all = sp.simplify(sp.diff(P_all, t).subs(t, 0))
phidot_all = sp.simplify(
    sp.trace(h_base.inv() * hdot_all) / 4 - hdot_all[0, 0] / (2 * h_base[0, 0])
)
checks["all_block_hdot_additivity"] = all_zero(
    sp.simplify(hdot_all - sum(block_hdot.values(), sp.zeros(2)))
)
checks["all_live_combined_hdot"] = any_nonzero(hdot_all)
checks["all_live_combined_projector_dot"] = any_nonzero(Pdot_all)
checks["all_live_combined_phidot"] = phidot_all != 0

# Direct derivative of the terminal scalar readout on the complete witness.
phi_all = sp.log(-h_all.det() / h_all[0, 0] ** 2) / 4
checks["complete_witness_phi_derivative"] = sp.simplify(sp.diff(phi_all, t).subs(t, 0) - phidot_all) == 0

details["base_h"] = [[str(x) for x in h_base.row(i)] for i in range(2)]
details["base_det_h"] = str(sp.factor(h_base.det()))
details["block_results"] = block_results
details["combined_hdot"] = [[str(sp.factor(x)) for x in hdot_all.row(i)] for i in range(2)]
details["combined_phidot"] = str(sp.factor(phidot_all))
details["combined_projector_dot_nonzero"] = any_nonzero(Pdot_all)
details["regime_weights"] = {
    "radial": "sech(phi)^2",
    "screen_and_rest_space_tilt": "tanh(phi)",
    "reciprocal_clock_ruler": "exp(-phi), exp(+phi)",
}

payload = {
    "status": "PASS" if all(bool(v) for v in checks.values()) else "FAIL",
    "checks_passed": sum(bool(v) for v in checks.values()),
    "checks_total": len(checks),
    "checks": {k: bool(v) for k, v in checks.items()},
    "details": details,
}
(HERE / "DERIVATION_RESULT.json").write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
print(f"{payload['status']}: {payload['checks_passed']}/{payload['checks_total']} G148 production checks")
if payload["status"] != "PASS":
    raise SystemExit(1)
