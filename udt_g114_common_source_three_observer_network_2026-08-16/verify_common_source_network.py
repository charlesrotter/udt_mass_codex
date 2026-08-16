#!/usr/bin/env python3
"""Exact finite-dimensional checks for the G114 typed observer network."""

from dataclasses import dataclass
import json
import sympy as sp


@dataclass(frozen=True)
class TypedMap:
    source: str
    target: str
    matrix: sp.Matrix

    def inverse(self):
        return TypedMap(self.target, self.source, self.matrix.inv())


def compose(left: TypedMap, right: TypedMap) -> TypedMap:
    """Return left after right."""
    if right.target != left.source:
        raise TypeError(f"cannot compose {right.source}->{right.target} with {left.source}->{left.target}")
    return TypedMap(right.source, left.target, sp.simplify(left.matrix * right.matrix))


def block2(a, b, c, d):
    eye = sp.eye(2)
    return sp.Matrix.vstack(
        sp.Matrix.hstack(a * eye, b * eye),
        sp.Matrix.hstack(c * eye, d * eye),
    )


def lift_screen(q):
    z = sp.zeros(2)
    return sp.Matrix.vstack(sp.Matrix.hstack(q, z), sp.Matrix.hstack(z, q))


def rot(c, s):
    return sp.Matrix([[c, -s], [s, c]])


def is_zero(m):
    return m.applyfunc(sp.simplify) == sp.zeros(*m.shape)


I4 = sp.eye(4)
I2 = sp.eye(2)
Z2 = sp.zeros(2)
Omega = sp.Matrix.vstack(
    sp.Matrix.hstack(Z2, I2),
    sp.Matrix.hstack(-I2, Z2),
)

# Three exact, invertible phase-space propagators. They stand for the full
# (J, nabla_K J) carrier, not for the singularable J-position block alone.
Pmat = {
    "A": block2(1, 1, 0, 1),
    "B": block2(sp.Rational(3, 5), sp.Rational(4, 5), -sp.Rational(4, 5), sp.Rational(3, 5)),
    "C": block2(1, 0, -2, 1),
}
P = {i: TypedMap(f"V_{i}", f"E_{i}", Pmat[i]) for i in "ABC"}

# B_i trivializes the ray-i endpoint phase fiber E_i into one supplied
# common source phase frame E_0. Hence C_ji = B_j^-1 B_i maps E_i -> E_j.
Bmat = {
    "A": I4,
    "B": lift_screen(rot(sp.Rational(3, 5), sp.Rational(4, 5))),
    "C": lift_screen(rot(sp.Rational(5, 13), sp.Rational(12, 13))),
}
B = {i: TypedMap(f"E_{i}", "E_0", Bmat[i]) for i in "ABC"}

# General source-frequency calibration control. In native affine phase
# coordinates the momentum comparison carries omega_j/omega_i. Equivalently,
# T_i=diag(q_i,q_i/omega_i) trivializes E_i into a common source-normalized
# phase frame. The unit-omega B_i above is the matched-calibration special case.
omega = {"A": sp.Rational(2), "B": sp.Rational(3), "C": sp.Rational(5)}
qmat = {
    "A": sp.eye(2),
    "B": rot(sp.Rational(3, 5), sp.Rational(4, 5)),
    "C": rot(sp.Rational(5, 13), sp.Rational(12, 13)),
}


def phase_diag(q_pos, q_mom):
    z = sp.zeros(2)
    return sp.Matrix.vstack(sp.Matrix.hstack(q_pos, z), sp.Matrix.hstack(z, q_mom))


T_source = {i: phase_diag(qmat[i], qmat[i] / omega[i]) for i in "ABC"}


def calibrated_junction(j, i):
    return sp.simplify(T_source[j].inv() * T_source[i])


def junction(j, i):
    return compose(B[j].inverse(), B[i])


def edge(j, i, cji=None):
    cji = junction(j, i) if cji is None else cji
    return compose(P[j].inverse(), compose(cji, P[i]))


R_BA = edge("B", "A")
R_CB = edge("C", "B")
R_AC = edge("A", "C")
loop = compose(R_AC, compose(R_CB, R_BA))

# Point-observer angular variations occupy only the Lagrangian vertex
# subspace L0={(J,Pi): J=0}. Full phase-space composability does not imply
# that one observer's physical beam subspace is carried into another's.
Iota = sp.Matrix.vstack(sp.zeros(2), sp.eye(2))
Lambda_common = {i: Bmat[i] * Pmat[i] * Iota for i in "ABC"}


def intersection_dimension(a, b):
    return int(a.rank() + b.rank() - a.row_join(b).rank())


generic_intersections = {
    "BA": intersection_dimension(Lambda_common["B"], Lambda_common["A"]),
    "CB": intersection_dimension(Lambda_common["C"], Lambda_common["B"]),
    "AC": intersection_dimension(Lambda_common["A"], Lambda_common["C"]),
}

# A separate aligned control proves that equality is possible but is a real
# restriction: choose propagators whose source-trivialized vertex images are
# the same Lagrangian plane.
P0 = block2(1, 2, 0, 1)
P_aligned = {i: Bmat[i].inv() * P0 for i in "ABC"}
Lambda_aligned = {i: Bmat[i] * P_aligned[i] * Iota for i in "ABC"}
aligned_equal = all(is_zero(Lambda_aligned[i] - Lambda_aligned["A"]) for i in "BC")

# Exact cocycle/descent and reversal tests.
C_CA_via_B = compose(junction("C", "B"), junction("B", "A"))
C_CA_direct = junction("C", "A")
R_AB = edge("A", "B")

cal_C_BA = calibrated_junction("B", "A")
cal_C_CB = calibrated_junction("C", "B")
cal_C_AC = calibrated_junction("A", "C")
cal_loop = sp.simplify(cal_C_AC * cal_C_CB * cal_C_BA)
cal_conformal = {
    j + i: is_zero(calibrated_junction(j, i).T * Omega * calibrated_junction(j, i)
                    - (omega[j] / omega[i]) * Omega)
    for j, i in [("B", "A"), ("C", "B"), ("A", "C")]
}

# Path-labelled source holonomy: change only C_AC by a nonidentity rotation
# in E_A. The observer loop must be its conjugate by P_A.
H_A = lift_screen(rot(0, 1))
C_AC_h = TypedMap("E_C", "E_A", H_A * junction("A", "C").matrix)
R_AC_h = edge("A", "C", C_AC_h)
loop_h = compose(R_AC_h, compose(R_CB, R_BA))
expected_h = Pmat["A"].inv() * H_A * Pmat["A"]

# Source endpoint frame changes must cancel out of carried observer edges.
G = {
    "A": block2(1, 2, 0, 1),
    "B": block2(1, 0, 3, 1),
    "C": block2(sp.Rational(5, 4), sp.Rational(3, 4), sp.Rational(3, 4), sp.Rational(5, 4)),
}
source_gauge_ok = True
for j, i in [("B", "A"), ("C", "B"), ("A", "C")]:
    p_i_prime = G[i] * Pmat[i]
    p_j_prime = G[j] * Pmat[j]
    c_prime = G[j] * junction(j, i).matrix * G[i].inv()
    r_prime = p_j_prime.inv() * c_prime * p_i_prime
    source_gauge_ok &= is_zero(r_prime - edge(j, i).matrix)

# A Jacobi caustic can kill the position block without killing the full
# phase carrier. Derive the constant-positive-curvature fundamental matrix,
# verify its ODE and initial condition, and only then evaluate at lambda=pi.
lam = sp.symbols("lam", real=True)
A_osc = block2(0, 1, -1, 0)
P_osc = block2(sp.cos(lam), sp.sin(lam), -sp.sin(lam), sp.cos(lam))
P_caustic = sp.simplify(P_osc.subs(lam, sp.pi))
D_caustic = sp.simplify(sp.sin(sp.pi) * I2)

# Equal matrix size is not a type relation.
bad_comp_rejected = False
try:
    D_A = TypedMap("Sky_A", "Screen_EA", I2)
    D_B = TypedMap("Sky_B", "Screen_EB", I2)
    compose(D_B, D_A)
except TypeError:
    bad_comp_rejected = True

# Observer endpoint frame covariance: R'_ji=S_j R_ji S_i^-1 and the based
# loop is conjugated in the A frame.
S = {
    "A": block2(1, 3, 0, 1),
    "B": block2(1, 0, -1, 1),
    "C": block2(1, 2, 0, 1),
}
Rprime = {
    "BA": S["B"] * R_BA.matrix * S["A"].inv(),
    "CB": S["C"] * R_CB.matrix * S["B"].inv(),
    "AC": S["A"] * R_AC_h.matrix * S["C"].inv(),
}
loop_prime = Rprime["AC"] * Rprime["CB"] * Rprime["BA"]

checks = {
    "all_phase_propagators_symplectic": all(is_zero(m.T * Omega * m - Omega) for m in Pmat.values()),
    "all_phase_propagators_invertible": all(sp.simplify(m.det()) == 1 for m in Pmat.values()),
    "junction_descent_exact": is_zero(C_CA_via_B.matrix - C_CA_direct.matrix),
    "common_trivialization_loop_identity": is_zero(loop.matrix - I4),
    "edge_reversal_exact": is_zero(R_AB.matrix - R_BA.matrix.inv()),
    "path_holonomy_conjugacy_exact": is_zero(loop_h.matrix - expected_h),
    "path_holonomy_nonidentity": not is_zero(loop_h.matrix - I4),
    "source_endpoint_gauge_cancels": bool(source_gauge_ok),
    "observer_frame_loop_covariant": is_zero(loop_prime - S["A"] * loop_h.matrix * S["A"].inv()),
    "caustic_position_block_singular": D_caustic.det() == 0,
    "caustic_full_phase_invertible": P_caustic.det() == 1,
    "caustic_full_phase_symplectic": is_zero(P_caustic.T * Omega * P_caustic - Omega),
    "caustic_fundamental_ode_exact": is_zero(sp.diff(P_osc, lam) - A_osc * P_osc),
    "caustic_fundamental_initial_identity": is_zero(P_osc.subs(lam, 0) - I4),
    "same_size_wrong_type_rejected": bad_comp_rejected,
    "generic_full_loop_does_not_force_beam_alignment": all(v == 0 for v in generic_intersections.values()),
    "aligned_beam_control_exists": aligned_equal,
    "unequal_source_frequency_loop_identity": is_zero(cal_loop - I4),
    "unequal_source_frequency_junctions_conformally_symplectic": all(cal_conformal.values()),
}

result = {
    "status": "PASS" if all(checks.values()) else "FAIL",
    "checks": checks,
    "common_loop_rank_from_identity": int((loop.matrix - I4).rank()),
    "holonomy_loop_rank_from_identity": int((loop_h.matrix - I4).rank()),
    "phase_caustic_position_rank": int(D_caustic.rank()),
    "phase_caustic_full_rank": int(P_caustic.rank()),
    "generic_vertex_image_intersection_dimensions": generic_intersections,
}
print(json.dumps(result, indent=2, sort_keys=True))
if result["status"] != "PASS":
    raise SystemExit(1)
