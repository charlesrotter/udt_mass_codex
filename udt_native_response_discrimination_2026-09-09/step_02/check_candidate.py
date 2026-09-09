#!/usr/bin/env python3
"""Exact Laurent-polynomial and matrix support for ND2; no proof by sampling.

No scientific source/author-step1 imports. These algebraic checks do not
construct general metric developments or prove function-space closure.
"""
import json
import platform
from fractions import Fraction as F


def poly(values):
    return {k: F(v) for k, v in values.items() if v}


def add(p, q):
    return poly({k: p.get(k, 0) + q.get(k, 0) for k in p.keys() | q.keys()})


def scale(p, c):
    return poly({k: c*v for k, v in p.items()})


def mul(p, q):
    out = {}
    for k, a in p.items():
        for l, b in q.items():
            out[k+l] = out.get(k+l, F(0)) + a*b
    return poly(out)


def derivative(p):
    return poly({k-1: k*v for k, v in p.items()})


def blocks(h):
    first = derivative(h)
    a = add(scale(derivative(first), F(-1, 2)), scale(mul({-1: F(1)}, first), -1))
    b = scale(add(mul({-2: F(1)}, h), mul({-1: F(1)}, first)), -1)
    q = scale(add(mul(a, a), scale(mul(b, b), -1)), F(1, 2))
    angular = add(scale(mul({2: F(1)}, derivative(first)), F(1, 2)), scale(h, -1))
    return a, b, q, angular


checks = []


def gate(name, value):
    checks.append({'name': name, 'passed': bool(value)})
    if not value:
        raise AssertionError(name)


records = []
for exponent in range(-4, 6):
    a, b, q, angular = blocks({exponent: F(1)})
    gate(f'monomial_{exponent}_A', a == poly({exponent-2: F(-exponent*(exponent+1), 2)}))
    gate(f'monomial_{exponent}_B', b == poly({exponent-2: -(exponent+1)}))
    gate(f'monomial_{exponent}_Q', q == poly({2*exponent-4: F((exponent+1)**2 * (exponent**2-4), 8)}))
    gate(f'monomial_{exponent}_angular_kernel', (not angular) == (exponent in (-1, 2)))
    gate(f'monomial_{exponent}_Q_integrable', (not q) == (exponent in (-2, -1, 2)))

for alpha in (F(-2), F(1, 9), F(3)):
    for delta in (F(-1, 4), F(1, 5), F(2)):
        for beta in (F(-1), F(0), F(2, 3)):
            he = poly({2: alpha, -1: beta})
            hz = poly({-2: delta, -1: beta})
            mixed = poly({2: alpha, -2: delta, -1: beta})
            ae, be, qe, ce = blocks(he)
            az, bz, qz, cz = blocks(hz)
            am, bm, qm, cm = blocks(mixed)
            label = f'{alpha}_{delta}_{beta}'
            gate(label + ':E_exact_direction', not qe and not ce and ae == be)
            gate(label + ':Z_exact_direction', not qz and add(az, bz) == {})
            gate(label + ':Z_filter', cz == poly({-2: 2*delta}))
            gate(label + ':sum_obstruction', qm == poly({-4: 6*alpha*delta}) and bool(qm))
            gate(label + ':sum_filter', cm == poly({-2: 2*delta}))
            records.append({'alpha': str(alpha), 'delta': str(delta), 'beta': str(beta),
                            'mixed_Q_coefficient': {str(k): str(v) for k,v in qm.items()}})


def mm(a, b):
    return [[sum((a[i][k]*b[k][j] for k in range(4)), F(0)) for j in range(4)] for i in range(4)]


def madd(a, b):
    return [[a[i][j]+b[i][j] for j in range(4)] for i in range(4)]


def mscale(a, c):
    return [[c*a[i][j] for j in range(4)] for i in range(4)]


def tf(a):
    trace = sum(a[i][i] for i in range(4))
    return [[a[i][j]-(trace/4 if i == j else 0) for j in range(4)] for i in range(4)]


def diagonal(entries):
    return [[F(entries[i]) if i == j else F(0) for j in range(4)] for i in range(4)]


zero = diagonal([0, 0, 0, 0])
n = diagonal([1, 2, 3, 4])
p = diagonal([2, -1, 4, -3])
leading = tf(mm(n,n))
cubic = tf(madd(mm(n,p), mm(p,n)))
quartic = tf(mm(p,p))
gate('nonzero_general_necessary_obstruction', leading != zero)
for eps in (F(-1, 3), F(1, 7), F(2, 5)):
    m = madd(mscale(n,eps), mscale(p,eps**2))
    exact = tf(mm(m,m))
    expanded = madd(madd(mscale(leading,eps**2), mscale(cubic,eps**3)), mscale(quartic,eps**4))
    gate('matrix_exact_epsilon_polynomial_' + str(eps), exact == expanded)

# An indefinite-metric control prevents falsely inferring N=0 from TF(N²)=0.
null_n = [[F(-1), F(-1), F(0), F(0)],
          [F(1), F(1), F(0), F(0)],
          [F(0)]*4, [F(0)]*4]
eta = diagonal([-1,1,1,1])
eta_n = mm(eta, null_n)
gate('nonzero_nilpotent_is_not_excluded', null_n != zero and mm(null_n,null_n) == zero)
gate('nilpotent_is_Lorentz_self_adjoint', all(eta_n[i][j] == eta_n[j][i] for i in range(4) for j in range(4)))
gate('nilpotent_passes_necessary_condition_only', tf(mm(null_n,null_n)) == zero)

print(json.dumps({'status': 'PASS_EXACT_ALGEBRA_NOT_METRIC_SUFFICIENCY',
    'python': platform.python_version(), 'checks_passed': len(checks),
    'method': 'standalone Fraction Laurent polynomial and matrix arithmetic',
    'scientific_source_imports': False,
    'monomial_directions': list(range(-4,6)), 'mixed_direction_records': records,
    'checks': checks,
    'limits': ['no general metric-realization sufficiency', 'no finite-sample tangent classification',
               'no dynamics or physical superposition law', 'no physical response adoption']},indent=2))
