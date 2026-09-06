"""Exact algebraic curvature/record map checks, not a PDE or device test."""
import argparse
from fractions import Fraction as F
from itertools import product
import json

ap = argparse.ArgumentParser()
ap.add_argument('--mutant', choices=('missing_mixed', 'wrong_scalar',
                                    'same_null_sign', 'omit_cyclic'))
mode = ap.parse_args().mutant
guards = []


def check(name, value):
    if not value:
        print(json.dumps({'status': 'FAIL', 'guard': name, 'mutant': mode,
                          'passed_before_failure': guards}, sort_keys=True))
        raise SystemExit(1)
    guards.append(name)


def eps(i, j, k):
    if len({i, j, k}) < 3:
        return 0
    return 1 if (i, j, k) in ((1, 2, 3), (2, 3, 1), (3, 1, 2)) else -1


def delta(i, j):
    return F(i == j)


def rank(matrix):
    a = [list(map(F, row)) for row in matrix]
    if not a:
        return 0
    r = 0
    for col in range(len(a[0])):
        pivot = next((i for i in range(r, len(a)) if a[i][col]), None)
        if pivot is None:
            continue
        a[r], a[pivot] = a[pivot], a[r]
        q = a[r][col]
        a[r] = [x/q for x in a[r]]
        for i in range(len(a)):
            if i != r and a[i][col]:
                q = a[i][col]
                a[i] = [x-q*y for x, y in zip(a[i], a[r])]
        r += 1
        if r == len(a):
            break
    return r


spatial = (1, 2, 3)
cycles = ((1, 2, 3), (2, 3, 1), (3, 1, 2))
e_slots = ((1, 1), (2, 2), (3, 3), (1, 2), (2, 3), (3, 1))
b_slots = ((1, 1), (2, 2), (1, 2), (2, 3), (3, 1))
eta = (-1, 1, 1, 1)


def data(values):
    e = {(i, j): F(0) for i, j in product(spatial, repeat=2)}
    b = dict(e)
    for (i, j), x in zip(e_slots, values[:6]):
        e[i, j] = e[j, i] = F(x)
    for (i, j), x in zip(b_slots, values[6:]):
        b[i, j] = b[j, i] = F(x)
    b[3, 3] = -b[1, 1]-b[2, 2]
    return e, b


def tensor(values):
    e, b = data(values)
    if mode == 'missing_mixed':
        b = {key: F(0) for key in b}
    tau = sum(e[i, i] for i in spatial)
    lam, kappa = -tau, -tau/3
    if mode == 'wrong_scalar':
        kappa = -kappa
    c = {(i, j): e[i, j]-tau*delta(i, j)/3 for i, j in e}
    q = {}

    def put(a, b0, c0, d, value):
        orbit = ((a, b0, c0, d, 1), (b0, a, c0, d, -1),
                 (a, b0, d, c0, -1), (b0, a, d, c0, 1),
                 (c0, d, a, b0, 1), (d, c0, a, b0, -1),
                 (c0, d, b0, a, -1), (d, c0, b0, a, 1))
        for a1, b1, c1, d1, sign in orbit:
            key = (a1, b1, c1, d1)
            val = sign*value
            if key in q and q[key] != val:
                raise ValueError(('inconsistent tensor assignment', key))
            q[key] = val

    for i, j in product(spatial, repeat=2):
        put(i, 0, 0, j, e[i, j])
    for i, j, k in product(spatial, repeat=3):
        put(i, 0, j, k, sum(eps(j, k, l)*b[l, i] for l in spatial))
    for i, j, k, l in product(spatial, repeat=4):
        val = sum(eps(i, j, m)*eps(k, l, n)*c[m, n]
                  for m, n in product(spatial, repeat=2))
        val += kappa*(delta(j, k)*delta(i, l)-delta(i, k)*delta(j, l))
        put(i, j, k, l, val)
    return {(a, b0, c0, d): q.get((a, b0, c0, d), F(0))
            for a, b0, c0, d in product(range(4), repeat=4)}, lam


def record(q):
    out = [q[i, 0, 0, j] for i, j in e_slots]
    for i, j, k in cycles:
        for sign in (1, -1):
            if mode == 'same_null_sign':
                sign = 1
            tangent = (F(1),)+tuple(F(sign if a == i else 0) for a in spatial)
            for a, b in ((j, j), (k, k), (j, k)):
                out.append(sum(q[a, c, d, b]*tangent[c]*tangent[d]
                               for c, d in product(range(4), repeat=2)))
    return tuple(out)


def unpack(y):
    e, _ = data(tuple(y[:6])+(F(0),)*5)
    pairs = [(tuple(y[6+6*i:9+6*i]), tuple(y[9+6*i:12+6*i])) for i in range(3)]
    h = [tuple((a+b)/2 for a, b in zip(p, m)) for p, m in pairs]
    o = [tuple((a-b)/2 for a, b in zip(p, m)) for p, m in pairs]
    return e, pairs, h, o


def constraints(y):
    e, pairs, h, o = unpack(y)
    out = [t[0]+t[1] for pair in pairs for t in pair]
    for a, (_, j, k) in enumerate(cycles):
        out.extend((h[a][0]-(e[j, j]-e[k, k]), h[a][2]-2*e[j, k]))
    out.append(F(0) if mode == 'omit_cyclic' else sum(t[2] for t in o))
    return tuple(out)


def reconstruct(y):
    _, _, _, o = unpack(y)
    a, b, c = (x[2] for x in o)
    return tuple(y[:6])+((b-c)/3, (c-a)/3, o[2][0]/2, o[0][0]/2, o[1][0]/2)


basis = [tuple(F(i == j) for i in range(11)) for j in range(11)]
tensors = [tensor(v) for v in basis]
indices = list(product(range(4), repeat=4))
check('all_riemann_pair_symmetries', all(
    q[a, b, c, d] == -q[b, a, c, d] == -q[a, b, d, c] == q[c, d, a, b]
    for q, _ in tensors for a, b, c, d in indices))
check('full_first_bianchi', all(q[a, b, c, d]+q[b, c, a, d]+q[c, a, b, d] == 0
                              for q, _ in tensors for a, b, c, d in indices))
check('full_einstein_ricci_contraction', all(
    sum(eta[a]*q[a, b, c, a] for a in range(4)) == lam*eta[b]*delta(b, c)
    for q, lam in tensors for b, c in product(range(4), repeat=2)))
records = [record(q) for q, _ in tensors]
map_matrix = [list(row) for row in zip(*records)]
check('record_map_rank_eleven', rank(map_matrix) == 11)
check('all_thirteen_constraints_on_tensor_basis',
      all(constraints(y) == (F(0),)*13 for y in records))
record_basis = [tuple(F(i == j) for i in range(24)) for j in range(24)]
constraint_matrix = [list(row) for row in zip(*(constraints(y) for y in record_basis))]
check('constraint_rank_thirteen', rank(constraint_matrix) == 13)
check('full_basis_parameter_reconstruction',
      all(reconstruct(y) == v for y, v in zip(records, basis)))
controls = [tuple(F((i+2)*s-i*i, i+1) for i in range(11)) for s in range(-3, 4)]
check('mixed_rational_parameter_reconstruction',
      all(reconstruct(record(tensor(v)[0])) == v for v in controls))
check('timelike_record_rank_six', rank(map_matrix[:6]) == 6)
check('null_record_rank_ten', rank(map_matrix[6:]) == 10)
scalar = (F(-2), F(-2), F(-2))+(F(0),)*8
q_scalar, lam_scalar = tensor(scalar)
check('constant_curvature_null_blindness', record(q_scalar)[6:] == (F(0),)*18 and lam_scalar == 6)
check('timelike_mixed_curvature_blindness', all(y[:6] == (F(0),)*6 for y in records[6:]))

bad_even = [F(0)]*24
bad_even[6], bad_even[7], bad_even[9], bad_even[10] = F(1), F(-1), F(1), F(-1)
bad_odd = [F(0)]*24
bad_odd[8], bad_odd[11] = F(1), F(-1)
even_resid, odd_resid = constraints(bad_even), constraints(bad_odd)
check('even_incompatible_record_detected', even_resid[:6] == (F(0),)*6 and even_resid[6] == 1)
check('cyclic_incompatible_record_detected', odd_resid[:12] == (F(0),)*12 and odd_resid[12] == 1)
check('same_future_normalized_null_queries', all(
    sum(eta[a]*((1 if a == 0 else sign if a == i else 0)**2) for a in range(4)) == 0
    for i in spatial for sign in (1, -1)))

print(json.dumps({
    'status': 'PASS', 'mutant': mode, 'guard_count': len(guards), 'guards': guards,
    'tensor_basis_dimension': 11, 'tensor_components_per_basis': 256,
    'additional_rational_controls': len(controls), 'record_dimension': 24,
    'record_rank': rank(map_matrix), 'constraint_rank': rank(constraint_matrix),
    'timelike_rank': rank(map_matrix[:6]), 'null_rank': rank(map_matrix[6:]),
    'bad_even_constraints': list(map(str, even_resid)),
    'bad_odd_constraints': list(map(str, odd_resid)),
    'record_map': [[str(x) for x in row] for row in map_matrix],
    'constraint_matrix': [[str(x) for x in row] for row in constraint_matrix],
    'arithmetic': 'standard-library Fraction exact rational',
    'scope': 'finite-dimensional linear tensor identities; no PDE or instrument theorem',
}, indent=2, sort_keys=True))
