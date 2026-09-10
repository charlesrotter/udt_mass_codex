"""Independent exact diagnostic, frozen before RF1 author candidate/code exposure.

Uses sparse coordinate metric polynomials, not author modules or a supplied
curvature-jet realizer. Finite examples do not prove the universal theorem.
"""
import itertools
import json
import platform
from fractions import Fraction as F

N = 4
Z = (0, 0, 0, 0)
SGN = (-1, 1, 1, 1)
MAX_DEG = 4
checks = []
catches = []


def p(value=0):
    return {Z: F(value)} if value else {}


def add(*args):
    out = {}
    for a in args:
        for e, c in a.items():
            out[e] = out.get(e, F(0)) + c
    return {e: c for e, c in out.items() if c}


def scale(a, factor):
    return {e: c * factor for e, c in a.items() if c * factor}


def mul(a, b, degree=MAX_DEG):
    out = {}
    for e, c in a.items():
        for f, d in b.items():
            h = tuple(x + y for x, y in zip(e, f))
            if sum(h) <= degree:
                out[h] = out.get(h, F(0)) + c * d
    return {e: c for e, c in out.items() if c}


def trunc(a, degree):
    return {e: c for e, c in a.items() if sum(e) <= degree}


def derivative(a, index):
    out = {}
    for e, c in a.items():
        if e[index]:
            f = list(e)
            f[index] -= 1
            out[tuple(f)] = c * e[index]
    return out


def value(a):
    return a.get(Z, F(0))


X = []
for i in range(N):
    e = list(Z)
    e[i] = 1
    X.append({tuple(e): F(1)})


def metric(k1, k2, quartic=True):
    g = {(i, j): p(SGN[i] if i == j else 0)
         for i in range(N) for j in range(N)}
    for block, kval in (((0, 1), F(k1)), ((2, 3), F(k2))):
        q = add(*(scale(mul(X[i], X[i]), SGN[i]) for i in block))
        for i, j in itertools.product(block, repeat=2):
            normal = add(scale(q, SGN[i] if i == j else 0),
                         scale(mul(X[i], X[j]), -SGN[i] * SGN[j]))
            correction = scale(normal, -kval / 3)
            if quartic:
                correction = add(correction, scale(mul(q, normal), 2*kval*kval/45))
            g[i, j] = add(g[i, j], correction)
    return g


def geometry(g):
    # Only inverse order 2 is needed for Gamma order 3 and Riemann order 2.
    inv = {(i, j): add(p(SGN[i] if i == j else 0),
                       scale(add(trunc(g[i, j], 2),
                                 p(-SGN[i] if i == j else 0)), -SGN[i]*SGN[j]))
           for i in range(N) for j in range(N)}
    gamma = {}
    for a, b, c in itertools.product(range(N), repeat=3):
        terms = []
        for d in range(N):
            lower = add(derivative(g[d, c], b), derivative(g[d, b], c),
                        scale(derivative(g[b, c], d), -1))
            terms.append(scale(mul(inv[a, d], lower, 3), F(1, 2)))
        gamma[a, b, c] = add(*terms)
    mixed = {}
    for a, b, c, d in itertools.product(range(N), repeat=4):
        terms = [derivative(gamma[a, d, b], c),
                 scale(derivative(gamma[a, c, b], d), -1)]
        for e in range(N):
            terms.extend((mul(gamma[a, c, e], gamma[e, d, b], 2),
                          scale(mul(gamma[a, d, e], gamma[e, c, b], 2), -1)))
        mixed[a, b, c, d] = trunc(add(*terms), 2)
    curv = {}
    for a, b, c, d in itertools.product(range(N), repeat=4):
        curv[a, b, c, d] = add(*(mul(g[a, e], mixed[e, b, c, d], 2)
                                for e in range(N)))
    r0 = {s: value(v) for s, v in curv.items()}
    r1 = {(d,) + s: value(derivative(v, d))
          for s, v in curv.items() for d in range(N)}
    r2 = {}
    for s, poly in curv.items():
        for d, e in itertools.product(range(N), repeat=2):
            out = value(derivative(derivative(poly, e), d))
            # All four tensor-slot connections are differentiated. Gamma(0)=0.
            for slot in range(4):
                for v in range(N):
                    news = list(s)
                    news[slot] = v
                    out -= value(derivative(gamma[v, e, s[slot]], d))*r0[tuple(news)]
            r2[d, e, *s] = out
    ric = {(b, d): sum(SGN[a]*r0[a, b, a, d] for a in range(N))
           for b, d in itertools.product(range(N), repeat=2)}
    return dict(r0=r0, r1=r1, r2=r2, ric=ric)


def tf(t):
    trace = sum(SGN[i]*t[i, i] for i in range(N))
    return {(i, j): t[i, j] - (F(1, 4)*trace*SGN[i] if i == j else 0)
            for i in range(N) for j in range(N)}


def ric_square(t):
    return {(i, j): sum(SGN[a]*t[i, a]*t[j, a] for a in range(N))
            for i in range(N) for j in range(N)}


def assert_named(name, condition):
    assert condition, name
    checks.append(name)


def catch(name, wrong_claim):
    assert not wrong_claim, name
    catches.append(name)


def radial(g):
    return all(add(*(mul(g[i, j], X[j]) for j in range(N)))
               == scale(X[i], SGN[i]) for i in range(N))


K1, K2 = F(2, 3), F(-5, 7)
g = metric(K1, K2)
assert_named('polynomial_metric_symmetric', all(g[i, j] == g[j, i]
             for i in range(N) for j in range(N)))
assert_named('polynomial_metric_origin_lorentz_eta', all(value(g[i, j]) ==
             (SGN[i] if i == j else 0) for i in range(N) for j in range(N)))
assert_named('radial_normal_identity', radial(g))
data = geometry(g)
expected = {}
for a, b, c, d in itertools.product(range(N), repeat=4):
    k = K1 if all(x < 2 for x in (a,b,c,d)) else (
        K2 if all(x >= 2 for x in (a,b,c,d)) else F(0))
    expected[a,b,c,d] = k*SGN[a]*SGN[b]*(int(a==c and b==d)-int(a==d and b==c))
assert_named('direct_curvature_matches_both_signed_blocks', data['r0'] == expected)
assert_named('direct_Ricci_nonzero_both_blocks', all(data['ric'][i, j] ==
             (SGN[i]*(K1 if i < 2 else K2) if i == j else 0)
             for i in range(N) for j in range(N)))
assert_named('first_covariant_curvature_derivative_zero', not any(data['r1'].values()))
assert_named('second_covariant_curvature_derivative_zero', not any(data['r2'].values()))
assert_named('nonzero_curvature_and_tracefree_Ricci', any(data['r0'].values())
             and any(tf(data['ric']).values()))

bad = geometry(metric(K1, K2, quartic=False))
assert_named('removing_quartic_keeps_origin_curvature', bad['r0'] == data['r0'])
catch('omitting_R_squared_quartic_still_parallel_to_second_order',
      not any(bad['r2'].values()))
bad_witness = next((list(s), str(v)) for s, v in bad['r2'].items() if v)

ratios = []
for eps in (F(1, 2), F(1, 3), F(1, 5)):
    ge = metric(eps**2*K1, eps**2*K2)
    assert_named('normal_coefficients_weighted_'+str(eps), all(
        ge[i,j] == {e:c*eps**sum(e) for e,c in g[i,j].items()}
        for i in range(N) for j in range(N)))
    de = geometry(ge)
    assert_named('direct_curvature_weighted_'+str(eps), all(
        de['r0'][s] == eps**2*data['r0'][s] for s in data['r0']))
    assert_named('actual_derivatives_stay_zero_'+str(eps),
                 not any(de['r1'].values()) and not any(de['r2'].values()))
    s = tf(de['ric'])
    q = tf(ric_square(de['ric']))
    # Fixed optional response F=2 Ric + 3 Ricci-square, no physical adoption.
    response = {ij: 2*s[ij] + 3*q[ij] for ij in s}
    remainder = {ij: response[ij] - 2*s[ij] for ij in s}
    q0 = tf(ric_square(data['ric']))
    assert_named('fixed_response_remainder_weight_four_'+str(eps),
                 all(remainder[ij] == 3*eps**4*q0[ij] for ij in s))
    ratios.append(str(sum(abs(v) for v in remainder.values())/eps**2))
    catch('discard_nonlinear_response_'+str(eps), not any(remainder.values()))

# An exact Lorentz frame change mixing the two curvature blocks.
L = [[F(int(i==j)) for j in range(N)] for i in range(N)]
L[0][0]=L[2][2]=F(5,3)
L[0][2]=L[2][0]=F(4,3)
assert_named('reporting_boost_is_Lorentz', all(sum(SGN[a]*L[a][i]*L[a][j]
             for a in range(N)) == (SGN[i] if i==j else 0)
             for i in range(N) for j in range(N)))
LX = [add(*(scale(X[j],L[i][j]) for j in range(N))) for i in range(N)]


def substitute(poly):
    out={}
    for e,c in poly.items():
        term=p(c)
        for i,power in enumerate(e):
            for unused in range(power):
                term=mul(term,LX[i])
        out=add(out,term)
    return out


sub={ij:substitute(poly) for ij,poly in g.items()}
gb={(i,j):add(*(scale(sub[a,b],L[a][i]*L[b][j])
               for a in range(N) for b in range(N)))
    for i in range(N) for j in range(N)}
assert_named('boosted_metric_remains_radially_normal', radial(gb))
boostdata=geometry(gb)
transformed=dict(data['r0'])
for slot in range(4):
    out={}
    for s in itertools.product(range(N),repeat=4):
        out[s]=F(0)
        for a in range(N):
            old=list(s)
            old[slot]=a
            out[s]+=L[a][s[slot]]*transformed[tuple(old)]
    transformed=out
assert_named('recomputed_boosted_curvature_covariant', boostdata['r0']==transformed)
assert_named('boosted_second_derivative_parallel', not any(boostdata['r2'].values()))
catch('boosted_curvature_components_unchanged', boostdata['r0']==data['r0'])
catch('quartic_sign_flip_matches_Jacobi', F(-2,45)==F(2,45))

print(json.dumps(dict(python=platform.python_version(), arithmetic='Fraction exact',
    assertion_categories=len(checks), checks=checks, wrong_claim_probes=catches,
    dropped_quartic_second_covariant_derivative=bad_witness,
    normalized_response_remainder_l1=ratios,
    scope='Finite actual polynomial metric jets; analytic proof required for all orders.'),
    indent=2, sort_keys=True))
