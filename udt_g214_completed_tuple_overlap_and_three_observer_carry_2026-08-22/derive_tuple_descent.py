#!/usr/bin/env python3
"""Exact dependency-free controller for the bounded G214 descent theorem."""

from fractions import Fraction as F
import json


def mm(a, b):
    return tuple(tuple(sum(a[i][k] * b[k][j] for k in range(2)) for j in range(2)) for i in range(2))


def tr(a):
    return tuple(zip(*a))


def det(a):
    return a[0][0] * a[1][1] - a[0][1] * a[1][0]


def diag(x, y):
    return ((x, F(0)), (F(0), y))


def cong(h, p):
    return mm(mm(tr(p), h), p)


def pair_metric(t, ell, beta):
    return (
        (-t * t, -t * t * beta),
        (-t * t * beta, ell * ell - t * t * beta * beta),
    )


def complete(h, density):
    return cong(h, diag(F(1), F(1, 1) / density))


def reconstruct(hs, density):
    return cong(hs, diag(F(1), density))


def completed_transition(p, density_i, density_j):
    return mm(mm(diag(F(1), density_i), p), diag(F(1), F(1, 1) / density_j))


checks = []


def check(name, condition):
    if not condition:
        raise AssertionError(name)
    checks.append(name)


t, ell, beta = F(2, 3), F(5, 4), F(-3, 7)
h_i = pair_metric(t, ell, beta)
m_i = t * ell
h_si = complete(h_i, m_i)
check("pair_determinant", det(h_i) == -(m_i * m_i))
check("completed_determinant", det(h_si) == -1)
check("local_round_trip", reconstruct(h_si, m_i) == h_i)

a, n, d = F(3, 2), F(4, 5), F(7, 3)
p_ij = ((a, n), (F(0), d))
h_j = cong(h_i, p_ij)
m_j = a * d * m_i
h_sj = complete(h_j, m_j)
c_ij = completed_transition(p_ij, m_i, m_j)
check("transition_determinant", det(p_ij) == a * d)
check("density_weight", m_j == det(p_ij) * m_i)
check("transformed_pair_determinant", det(h_j) == -(m_j * m_j))
check("completed_transition_determinant_one", det(c_ij) == 1)
check("completed_transition_formula", c_ij == ((a, n / m_j), (F(0), F(1, 1) / a)))
check("completed_equivariance", h_sj == cong(h_si, c_ij))
check("reconstruction_naturality", reconstruct(h_sj, m_j) == h_j)
check("reconstruction_matches_tensor_transition", reconstruct(h_sj, m_j) == cong(h_i, p_ij))

p_jk = ((F(5, 4), F(-2, 3)), (F(0), F(9, 5)))
p_ik = mm(p_ij, p_jk)
h_k = cong(h_j, p_jk)
m_k = det(p_jk) * m_j
h_sk = complete(h_k, m_k)
c_jk = completed_transition(p_jk, m_j, m_k)
c_ik = completed_transition(p_ik, m_i, m_k)
check("ordinary_transition_cocycle", h_k == cong(h_i, p_ik))
check("density_cocycle", m_k == det(p_ik) * m_i)
check("completed_transition_cocycle", mm(c_ij, c_jk) == c_ik)
check("completed_metric_triple_overlap", h_sk == cong(h_si, c_ik))

k = F(11, 6)
p_ruler = diag(F(1), k)
m_ruler = k * m_i
c_ruler = completed_transition(p_ruler, m_i, m_ruler)
check("pure_ruler_completed_transition_identity", c_ruler == diag(F(1), F(1)))
check("pure_ruler_reparameterization_invariance", complete(cong(h_i, p_ruler), m_ruler) == h_si)

r = diag(F(1), F(-1))
h_r = cong(h_i, r)
h_sr = complete(h_r, m_i)
check("orientation_reversal_determinant", det(h_r) == det(h_i))
check("orientation_reversal_congruence", h_sr == cong(h_si, r))
check("orientation_reversal_shift_sign", h_r[0][1] == -h_i[0][1])

lam = F(7, 4)
p_scale = diag(F(1), lam)
h_scale = cong(h_i, p_scale)
m_scale = lam * m_i
check("density_deletion_blind_family", complete(h_scale, m_scale) == h_si and h_scale != h_i)

# Scalar composition is tested multiplicatively, avoiding logarithmic approximation.
t_a_ab, t_b_ab = F(1), F(1)
t_b_bc, t_c_bc = F(2), F(1)
t_a_ac, t_c_ac = F(1), F(1)
q_ab = t_a_ab / t_b_ab
q_bc = t_b_bc / t_c_bc
q_ac = t_a_ac / t_c_ac
check("nonmatched_three_pair_defect_survives", q_ab * q_bc != q_ac)

t_a, t_b, t_c = F(5, 3), F(7, 4), F(11, 6)
check("matched_three_pair_scalar_telescopes", (t_a / t_b) * (t_b / t_c) == t_a / t_c)

print(json.dumps({
    "audit": "G214",
    "status": "PASS",
    "exact_checks": len(checks),
    "check_names": checks,
    "completed_transition_rank": 2,
    "completed_transition_determinant": 1,
    "landing": "TYPED_COMPLETED_TUPLE_DESCENDS__G130_TRANSFERS__ARBITRARY_THREE_PAIR_PRODUCT_NOT_DERIVED",
}, sort_keys=True))
