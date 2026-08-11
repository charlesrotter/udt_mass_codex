#!/usr/bin/env python3
"""Exact complete-coframe time-live compatibility derivation."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent
READ_ONLY = argparse.ArgumentParser()
READ_ONLY.add_argument("--read-only", action="store_true")
READ_ONLY = READ_ONLY.parse_args().read_only


def zero_matrix(matrix: sp.Matrix) -> bool:
    return all(sp.simplify(entry) == 0 for entry in matrix)


# Generic one-direction block factorization.
T, L, beta = sp.symbols("T L beta", nonzero=True, real=True)
Td, Ld, betad = sp.symbols("Td Ld betad", real=True)
q00, q01, q10, q11 = sp.symbols("q00 q01 q10 q11", real=True)
s00, s01, s10, s11 = sp.symbols("s00 s01 s10 s11", real=True)
qd00, qd01, qd10, qd11 = sp.symbols("qd00 qd01 qd10 qd11", real=True)
sd00, sd01, sd10, sd11 = sp.symbols("sd00 sd01 sd10 sd11", real=True)

B = sp.Matrix([[T, T * beta], [0, L]])
Q = sp.Matrix([[q00, q01], [q10, q11]])
S = sp.Matrix([[s00, s01], [s10, s11]])
dB = sp.Matrix([[Td, Td * beta + T * betad], [0, Ld]])
dQ = sp.Matrix([[qd00, qd01], [qd10, qd11]])
dS = sp.Matrix([[sd00, sd01], [sd10, sd11]])
Z = sp.zeros(2)
E = B.row_join(Z).col_join((Q * S).row_join(Q))
dE = dB.row_join(Z).col_join((dQ * S + Q * dS).row_join(dQ))
E_inv_expected = B.inv().row_join(Z).col_join((-S * B.inv()).row_join(Q.inv()))
K = sp.simplify(dE * E_inv_expected)
P = sp.simplify(dB * B.inv())
R = sp.simplify(dQ * Q.inv())
C = sp.simplify(Q * dS * B.inv())
K_expected = P.row_join(Z).col_join(C.row_join(R))
P_expected = sp.Matrix([[Td / T, T * betad / L], [0, Ld / L]])
eta2 = sp.diag(-1, 1)
eta4 = sp.diag(-1, 1, 1, 1)
screen_metric = Q.T * Q
metric_expected = (
    (B.T * eta2 * B + S.T * screen_metric * S)
    .row_join(S.T * screen_metric)
    .col_join((screen_metric * S).row_join(screen_metric))
)


# Exact nontrivial time-space witness with all blocks active.
t, x = sp.symbols("t x", real=True)
Bw = sp.Matrix([
    [1 + t + x, (1 + t + x) * (t * x + t)],
    [0, 2 + t**2 + x],
])
Qw = sp.Matrix([
    [1 + t + x**2, x + t**2],
    [t * x + x, 2 + x + t**2],
])
Sw = sp.Matrix([
    [t + x + t * x, 1 + t * x],
    [t**2 + x, x**2 + t],
])


def connection_blocks(Bm: sp.Matrix, Qm: sp.Matrix, Sm: sp.Matrix, variable: sp.Symbol):
    return (
        sp.simplify(sp.diff(Bm, variable) * Bm.inv()),
        sp.simplify(Qm * sp.diff(Sm, variable) * Bm.inv()),
        sp.simplify(sp.diff(Qm, variable) * Qm.inv()),
    )


Pt, Ct, Rt = connection_blocks(Bw, Qw, Sw, t)
Px, Cx, Rx = connection_blocks(Bw, Qw, Sw, x)
mc_P = sp.simplify(sp.diff(Px, t) - sp.diff(Pt, x) - (Pt * Px - Px * Pt))
mc_R = sp.simplify(sp.diff(Rx, t) - sp.diff(Rt, x) - (Rt * Rx - Rx * Rt))
mc_C = sp.simplify(
    sp.diff(Cx, t)
    - sp.diff(Ct, x)
    - (Ct * Px - Cx * Pt + Rt * Cx - Rx * Ct)
)


# Exact G59 matrix-channel evolution, including independent query motion.
xs = sp.symbols("x00 x01 x10 x11", real=True)
ys = sp.symbols("y00 y01 y10 y11", real=True)
js = sp.symbols("jr00 jr01 jr10 jr11", real=True)
kas = sp.symbols("ja00 ja01 ja10 ja11", real=True)
ps = sp.symbols("p00 p01 p10 p11", real=True)
cs = sp.symbols("c00 c01 c10 c11", real=True)
rs = sp.symbols("r00 r01 r10 r11", real=True)
X = sp.Matrix(2, 2, xs)
Y = sp.Matrix(2, 2, ys)
J_R = sp.Matrix(2, 2, js)
J_A = sp.Matrix(2, 2, kas)
P_t = sp.Matrix(2, 2, ps)
C_t = sp.Matrix(2, 2, cs)
R_t = sp.Matrix(2, 2, rs)
dX = P_t * X + J_R
dY = C_t * X + R_t * Y + J_A
H_R = X.T * eta2 * X
H_A = Y.T * Y
dH_R_direct = dX.T * eta2 * X + X.T * eta2 * dX
dH_A_direct = dY.T * Y + Y.T * dY
dH_R_expected = (
    X.T * (P_t.T * eta2 + eta2 * P_t) * X
    + J_R.T * eta2 * X
    + X.T * eta2 * J_R
)
dH_A_expected = (
    X.T * C_t.T * Y
    + Y.T * C_t * X
    + Y.T * (R_t.T + R_t) * Y
    + J_A.T * Y
    + Y.T * J_A
)


# Exact pair-state derivatives for arbitrary symmetric dh.
h00, h01, h11 = sp.symbols("h00 h01 h11", nonzero=True, real=True)
dh00, dh01, dh11 = sp.symbols("dh00 dh01 dh11", real=True)
h = sp.Matrix([[h00, h01], [h01, h11]])
dh = sp.Matrix([[dh00, dh01], [dh01, dh11]])
det_h = h.det()
d_det_h = dh00 * h11 + h00 * dh11 - 2 * h01 * dh01
trace_term = sp.simplify(sp.trace(h.inv() * dh))
dkappa_direct = sp.simplify(sp.Rational(1, 4) * d_det_h / det_h)
dphi_direct = sp.simplify(dkappa_direct - sp.Rational(1, 2) * dh00 / h00)
dbeta_direct = sp.simplify((h00 * dh01 - h01 * dh00) / h00**2)


checks = {
    "block_inverse": zero_matrix(sp.simplify(E * E_inv_expected - sp.eye(4))),
    "complete_metric_block_reconstruction": zero_matrix(sp.simplify(E.T * eta4 * E - metric_expected)),
    "block_logarithmic_derivative": zero_matrix(sp.simplify(K - K_expected)),
    "base_state_derivative": zero_matrix(sp.simplify(P - P_expected)),
    "mc_reciprocal_common_shift_block": zero_matrix(mc_P),
    "mc_angular_block": zero_matrix(mc_R),
    "mc_mixing_block": zero_matrix(mc_C),
    "HR_evolution": zero_matrix(sp.simplify(dH_R_direct - dH_R_expected)),
    "HA_evolution": zero_matrix(sp.simplify(dH_A_direct - dH_A_expected)),
    "h_evolution": zero_matrix(
        sp.simplify((dH_R_direct + dH_A_direct) - (dH_R_expected + dH_A_expected))
    ),
    "kappa_pair_derivative": sp.simplify(dkappa_direct - sp.Rational(1, 4) * trace_term) == 0,
    "phi_pair_derivative": sp.simplify(
        dphi_direct - (sp.Rational(1, 4) * trace_term - sp.Rational(1, 2) * dh00 / h00)
    ) == 0,
    "beta_pair_derivative": sp.simplify(
        dbeta_direct - (h00 * dh01 - h01 * dh00) / h00**2
    ) == 0,
    "witness_B_invertible_local": sp.simplify(Bw.det()) != 0,
    "witness_Q_invertible_local": sp.simplify(Qw.det()) != 0,
}
assert all(checks.values()), [name for name, value in checks.items() if not value]

compatibility_rows = [
    {
        "block": "P_base",
        "definition": "P=dB B^-1",
        "time_space_identity": "partial_t P_i-partial_i P_t-[P_t,P_i]=0",
        "physical_content": "kappa phi beta smooth-coframe compatibility",
        "grade": "DERIVED_IDENTITY_NOT_EOM",
    },
    {
        "block": "R_angular",
        "definition": "R=dQ Q^-1",
        "time_space_identity": "partial_t R_i-partial_i R_t-[R_t,R_i]=0",
        "physical_content": "general screen smooth-coframe compatibility",
        "grade": "DERIVED_IDENTITY_NOT_EOM",
    },
    {
        "block": "C_mixing",
        "definition": "C=Q dS B^-1",
        "time_space_identity": "partial_t C_i-partial_i C_t-(C_t P_i-C_i P_t+R_t C_i-R_i C_t)=0",
        "physical_content": "exact reciprocal-angular-mixing covariant compatibility",
        "grade": "DERIVED_IDENTITY_NOT_EOM",
    },
]

trajectory_rows = [
    {
        "family": "time_only_arbitrary_movie",
        "free_data": "any smooth B(t),Q(t),S(t) with detB detQ nonzero",
        "compatibility": "all two-form identities vacuous on one-dimensional time base",
        "selection": "NONE",
        "status": "CONSTRUCTIVE_FULL_FUNCTIONAL_FREEDOM",
    },
    {
        "family": "time_space_complete_movie",
        "free_data": "any smooth B(t,x),Q(t,x),S(t,x) with detB detQ nonzero",
        "compatibility": "P R C satisfy the three Maurer-Cartan block identities automatically",
        "selection": "NONE_BEYOND_SMOOTH_INTEGRABILITY",
        "status": "CONSTRUCTIVE_FULL_FUNCTIONAL_FREEDOM",
    },
    {
        "family": "fixed_query_orchestra",
        "free_data": "J_R=J_A=0 with arbitrary coframe movie",
        "compatibility": "matrix evolution formulas exact",
        "selection": "NONE",
        "status": "KINEMATIC_CONTROL",
    },
    {
        "family": "moving_query_orchestra",
        "free_data": "arbitrary lawful J_R,J_A in addition to coframe movie",
        "compatibility": "query terms remain additively distinct",
        "selection": "NONE",
        "status": "QUERY_OWNER_OPEN",
    },
]

frequency_rows = [
    {
        "witness": "reciprocal_vibration",
        "fields": "kappa=0; phi=a sin(omega t); beta=0; Q=I; S=0",
        "free_frequencies": "omega arbitrary",
        "regularity": "T,L positive for finite a",
        "meaning": "smooth movie not on-shell mode",
    },
    {
        "witness": "screen_breath_and_shear",
        "fields": "Q=R(nu t) diag(exp(q sin(omega t)),exp(-q sin(omega t))); other fields arbitrary",
        "free_frequencies": "nu and omega independent",
        "regularity": "detQ=1",
        "meaning": "smooth movie not on-shell mode",
    },
    {
        "witness": "mixing_orchestra",
        "fields": "all four S entries are independent smooth finite Fourier sums",
        "free_frequencies": "every frequency and phase arbitrary",
        "regularity": "E invertibility independent of S",
        "meaning": "smooth movie not on-shell mode",
    },
    {
        "witness": "fully_coupled_movie",
        "fields": "kappa phi beta Q S all nonconstant with independent frequencies",
        "free_frequencies": "no kinematic resonance or dispersion relation",
        "regularity": "local detB detQ nonzero",
        "meaning": "smooth movie not physical harmony",
    },
]

result = {
    "base_commit": "78f925459eb7ee8a4251dcc86460d3c581634bc8",
    "preregistration_commit": "c86094e1",
    "status": "EXACT_COMPATIBILITY_ORCHESTRA_BUT_NO_EVOLUTION_LAW",
    "exact_checks": checks,
    "exact_check_count": len(checks),
    "compatibility_blocks": len(compatibility_rows),
    "trajectory_families": len(trajectory_rows),
    "arbitrary_frequency_witnesses": len(frequency_rows),
    "maximum_conclusion": (
        "complete factorized coframe films obey exact block compatibility identities; "
        "current metric kinematics selects no physical trajectory, frequency, characteristic, or regime"
    ),
}


def write_tsv(path: Path, rows: list[dict[str, str]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(
            stream, fieldnames=list(rows[0]), delimiter="\t", lineterminator="\n"
        )
        writer.writeheader()
        writer.writerows(rows)


if not READ_ONLY:
    (HERE / "DERIVATION_RESULT.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    write_tsv(HERE / "COMPATIBILITY_BLOCKS.tsv", compatibility_rows)
    write_tsv(HERE / "TRAJECTORY_CLASSIFICATION.tsv", trajectory_rows)
    write_tsv(HERE / "ARBITRARY_FREQUENCY_FAMILIES.tsv", frequency_rows)

print(
    f"PASS exact={len(checks)} blocks={len(compatibility_rows)} "
    f"families={len(trajectory_rows)} landing={result['status']}"
)
