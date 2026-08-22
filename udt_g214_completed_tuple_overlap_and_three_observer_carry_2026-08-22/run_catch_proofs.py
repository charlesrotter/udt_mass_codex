#!/usr/bin/env python3
"""Hostile mutation witnesses for G214."""

from fractions import Fraction as F
import json


def mm(a, b):
    return tuple(tuple(sum(a[i][k] * b[k][j] for k in range(2)) for j in range(2)) for i in range(2))


def tr(a):
    return tuple(zip(*a))


def det(a):
    return a[0][0] * a[1][1] - a[0][1] * a[1][0]


def diag(a, b):
    return ((a, F(0)), (F(0), b))


def cong(h, p):
    return mm(mm(tr(p), h), p)


def norm(h, m):
    return cong(h, diag(F(1), F(1) / m))


h = ((F(-4), F(1)), (F(1), F(3)))
m = F(13).sqrt() if hasattr(F(13), "sqrt") else None
# Use a determinant-square metric for exact normalization.
h = ((F(-4), F(2)), (F(2), F(3)))
m = F(4)
p = ((F(2), F(1)), (F(0), F(3)))
q = ((F(5), F(-2)), (F(0), F(7)))
hp = cong(h, p)
mp = det(p) * m
hs = norm(h, m)
hsp = norm(hp, mp)
j = diag(F(1), m)
jp_inv = diag(F(1), F(1) / mp)
c = mm(mm(j, p), jp_inv)

catches = []


def caught(name, condition):
    if not condition:
        raise AssertionError(name)
    catches.append(name)


caught("omit_clock_density_weight", F(3) * m != mp)
caught("inverse_density_weight", m / det(p) != mp)
caught("reverse_transition_order", mm(p, q) != mm(q, p))
caught("false_full_rechart_invariance", hsp != hs)
caught("missing_completed_congruence", cong(hs, c) == hsp)
caught("drop_density_reconstruction", hs != hp)

scale = F(5, 2)
h_scaled = cong(h, diag(F(1), scale))
caught("density_blindness_if_m_deleted", norm(h_scaled, scale * m) == hs and h_scaled != h)

b_on_ab, b_on_bc = F(1), F(2)
caught("shared_observer_not_matched_incidence", b_on_ab != b_on_bc)

h_one = ((F(-1), F(1)), (F(1), F(2)))
h_two = ((F(-2), F(3)), (F(3), F(1)))
product = mm(h_one, h_two)
caught("pair_metric_product_not_metric_composition", product != tr(product))

caught("completed_transition_is_not_original_transition", c != p and det(c) == 1)

print(json.dumps({
    "audit": "G214",
    "status": "PASS",
    "catches": len(catches),
    "catch_names": catches,
}, sort_keys=True))
