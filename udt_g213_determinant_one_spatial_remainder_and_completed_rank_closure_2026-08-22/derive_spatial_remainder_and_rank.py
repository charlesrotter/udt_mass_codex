#!/usr/bin/env python3
"""Exact symbolic production derivation for G213; writes no files."""

import json

import sympy as sp


checks = {}


def check(name, condition):
    value = bool(condition)
    checks[name] = value
    if not value:
        raise AssertionError(name)


# Unique logarithmic 1+2+2 decomposition of Sym_0(3).
gamma, w1, w2, s1, s2 = sp.symbols("gamma w1 w2 s1 s2", real=True)
grade = sp.diag(2 * gamma, -gamma, -gamma)
mix = sp.Matrix([[0, w1, w2], [w1, 0, 0], [w2, 0, 0]])
screen = sp.Matrix([[0, 0, 0], [0, s1, s2], [0, s2, -s1]])
X = grade + mix + screen

check("log_coordinate_symmetric", X == X.T)
check("log_coordinate_tracefree", sp.trace(X) == 0)
check("grade_dimension_one", sp.Matrix([grade[0, 0], grade[0, 1], grade[0, 2], grade[1, 1], grade[1, 2]]).jacobian([gamma]).rank() == 1)
check("mix_dimension_two", sp.Matrix([mix[0, 0], mix[0, 1], mix[0, 2], mix[1, 1], mix[1, 2]]).jacobian([w1, w2]).rank() == 2)
check("screen_dimension_two", sp.Matrix([screen[0, 0], screen[0, 1], screen[0, 2], screen[1, 1], screen[1, 2]]).jacobian([s1, s2]).rank() == 2)

coordinate_vector = sp.Matrix([X[0, 0], X[0, 1], X[0, 2], X[1, 1], X[1, 2]])
coordinate_jacobian = coordinate_vector.jacobian([gamma, w1, w2, s1, s2])
check("full_log_coordinate_rank_five", coordinate_jacobian.rank() == 5)
check("g207_g208_tangent_rank_four", coordinate_jacobian[:, 1:].rank() == 4)
check("grading_completes_rank_five", sp.Matrix.hstack(coordinate_jacobian[:, 1:], coordinate_jacobian[:, 0]).rank() == 5)

x00, x01, x02, x11, x12 = sp.symbols("x00 x01 x02 x11 x12", real=True)
x22 = -x00 - x11
X_generic = sp.Matrix([[x00, x01, x02], [x01, x11, x12], [x02, x12, x22]])
gamma_back = x00 / 2
w1_back, w2_back = x01, x02
s1_back, s2_back = x11 + gamma_back, x12
X_back = sp.diag(2 * gamma_back, -gamma_back, -gamma_back)
X_back += sp.Matrix([[0, w1_back, w2_back], [w1_back, 0, 0], [w2_back, 0, 0]])
X_back += sp.Matrix([[0, 0, 0], [0, s1_back, s2_back], [0, s2_back, -s1_back]])
check("log_coordinate_inverse", sp.simplify(X_back - X_generic) == sp.zeros(3))

# Independent global Schur factorization count for SPD(3) at determinant one.
a, u1, u2, p, q = sp.symbols("a u1 u2 p q", positive=True)
B = sp.Matrix([[p, q], [q, (1 + q**2) / p]])
L = sp.Matrix([[1, 0, 0], [u1, 1, 0], [u2, 0, 1]])
middle = sp.diag(a, 1, 1)
middle[1:3, 1:3] = a ** sp.Rational(-1, 2) * B
R = sp.simplify(L * middle * L.T)
c = R[1:3, 0]
schur = sp.simplify(R[1:3, 1:3] - c * c.T / R[0, 0])
check("screen_B_det_one", sp.simplify(B.det()) == 1)
check("schur_R_det_one", sp.simplify(R.det()) == 1)
check("schur_extract_a", sp.simplify(R[0, 0] - a) == 0)
check("schur_extract_mixing", sp.simplify(c / R[0, 0] - sp.Matrix([u1, u2])) == sp.zeros(2, 1))
check("schur_extract_screen", sp.simplify(sp.sqrt(a) * schur - B) == sp.zeros(2))

schur_entries = sp.Matrix([R[0, 0], R[0, 1], R[0, 2], R[1, 1], R[1, 2]])
schur_jac = schur_entries.jacobian([a, u1, u2, p, q])
check("schur_global_parameter_rank_five", sp.simplify(schur_jac.det()) != 0)

# G176 completed tuple is exactly equivalent to the auxiliary pullback when m is retained.
T, beta, Ls = sp.symbols("T beta Lsigma", positive=True)
h_sigma = sp.Matrix([[-T**2, -T**2 * beta], [-T**2 * beta, Ls**2 - T**2 * beta**2]])
m = T * Ls
J = sp.diag(1, m)
h_completed = sp.simplify(J.inv().T * h_sigma * J.inv())
h_roundtrip = sp.simplify(J.T * h_completed * J)
check("auxiliary_determinant", sp.simplify(h_sigma.det() + m**2) == 0)
check("completed_determinant_minus_one", sp.simplify(h_completed.det() + 1) == 0)
check("completed_tuple_roundtrip", sp.simplify(h_roundtrip - h_sigma) == sp.zeros(2))
check("completed_clock_retained", sp.simplify(h_completed[0, 0] + T**2) == 0)
check("completed_shift_retained", sp.simplify(h_completed[0, 1] + T * beta / Ls) == 0)

# Exact G129 six-plane restriction design.
directions = [(1, 0, 0), (0, 1, 0), (0, 0, 1), (1, 1, 0), (1, 0, 1), (0, 1, 1)]
rows = []
for v1, v2, v3 in directions:
    rows.append([1, 0, 0, 0, 0, 0, 0, 0, 0, 0])
    rows.append([0, v1, v2, v3, 0, 0, 0, 0, 0, 0])
    rows.append([0, 0, 0, 0, v1**2, 2*v1*v2, 2*v1*v3, v2**2, 2*v2*v3, v3**2])
design = sp.Matrix(rows)
check("g129_six_plane_rank_ten", design.rank() == 10)

# Without m, a common spatial calibration rescaling is exactly invisible.
aa, bb, mm, lam = sp.symbols("aa bb mm lam", nonzero=True)
cc = (bb**2 - mm**2) / aa
h = sp.Matrix([[aa, bb], [bb, cc]])
Jn = sp.diag(1, mm)
hs = sp.simplify(Jn.inv().T * h * Jn.inv())
h_scaled = sp.Matrix([[aa, lam * bb], [lam * bb, lam**2 * cc]])
Jn_scaled = sp.diag(1, lam * mm)
hs_scaled = sp.simplify(Jn_scaled.inv().T * h_scaled * Jn_scaled.inv())
check("density_blind_completed_metric_equal", sp.simplify(hs_scaled - hs) == sp.zeros(2))
check("density_blind_auxiliary_metric_changes", sp.simplify(h_scaled - h) != sp.zeros(2))

result = {
    "audit": "G213",
    "status": "PASS",
    "landing": "FIVE_MODE_REMAINDER__G207_G208_COVER_FOUR__DENSITY_COMPLETES_RANK_TEN",
    "symbolic_checks": len(checks),
    "all_checks_pass": all(checks.values()),
    "checks": checks,
    "mode_count": {"grading": 1, "radial_screen_mixing": 2, "tracefree_screen_shape": 2, "total": 5},
    "prior_tile_tangent_coverage": {"G207": 2, "G208": 2, "union": 4, "missing_independent_mode": "radial_versus_screen_grading"},
    "g129_design_rank": int(design.rank()),
    "maximum_conclusion": "local_metric_decomposition_and_rank_reconstruction_only",
}
print(json.dumps(result, sort_keys=True))

