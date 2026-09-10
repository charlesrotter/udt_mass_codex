"""Exact finite geometry checks, written before opening the GL2 candidate/code.

One-coordinate Taylor jets and coordinate Levi-Civita definitions are used.
No author code or scientific repository module is imported. Finite witnesses
do not establish the universal limiting theorem. Taylor coefficients above
the differentiation order needed for each value are not used as evidence.
"""
from fractions import Fraction as Q
from itertools import product
from functools import lru_cache
import json
import platform

DEG = 4
AX = range(4)


class Jet:
    def __init__(self, coefficients):
        if isinstance(coefficients, Jet):
            self.c = coefficients.c
        elif isinstance(coefficients, (int, Q)):
            self.c = (Q(coefficients),) + (Q(0),) * DEG
        else:
            vals = tuple(Q(x) for x in coefficients)
            self.c = (vals + (Q(0),) * (DEG + 1))[: DEG + 1]

    def __add__(self, other):
        other = Jet(other)
        return Jet([a + b for a, b in zip(self.c, other.c)])

    __radd__ = __add__

    def __neg__(self):
        return Jet([-x for x in self.c])

    def __sub__(self, other):
        return self + -Jet(other)

    def __rsub__(self, other):
        return Jet(other) + -self

    def __mul__(self, other):
        other = Jet(other)
        return Jet([sum(self.c[k] * other.c[n-k] for k in range(n+1))
                    for n in range(DEG+1)])

    __rmul__ = __mul__

    def inverse(self):
        assert self.c[0] != 0
        vals = [1 / self.c[0]]
        for n in range(1, DEG+1):
            vals.append(-sum(self.c[k] * vals[n-k] for k in range(1, n+1))
                        / self.c[0])
        return Jet(vals)

    def __truediv__(self, other):
        return self * Jet(other).inverse()

    def derivative(self):
        return Jet([(n+1) * self.c[n+1] for n in range(DEG)])

    @property
    def value(self):
        return self.c[0]


ZERO = Jet(0)
checks = []
catches = []


def require(name, condition):
    assert condition, name
    checks.append(name)


def catch(name, wrong_claim):
    assert not wrong_claim, 'false pass: ' + name
    catches.append(name)


def geometry(diagonal, active):
    g = [Jet(x) for x in diagonal]
    inv = [x.inverse() for x in g]

    def dg(a, b, d):
        return g[a].derivative() if a == b and d == active else ZERO

    gamma = {}
    for a, b, c in product(AX, repeat=3):
        gamma[a, b, c] = inv[a] * (dg(a, c, b) + dg(a, b, c) - dg(b, c, a)) / 2
    mixed = {}
    for a, b, c, d in product(AX, repeat=4):
        result = ((gamma[a, b, d].derivative() if c == active else ZERO)
                  - (gamma[a, b, c].derivative() if d == active else ZERO))
        for e in AX:
            result += (gamma[a, e, c] * gamma[e, b, d]
                       - gamma[a, e, d] * gamma[e, b, c])
        mixed[a, b, c, d] = result
    lower = {ix: g[ix[0]] * val for ix, val in mixed.items()}
    ric = {(b, d): sum((mixed[a, b, a, d] for a in AX), ZERO)
           for b, d in product(AX, repeat=2)}
    scalar = sum((inv[a] * ric[a, a] for a in AX), ZERO)
    tf = {(a, b): ric[a, b] - (scalar * g[a] / 4 if a == b else ZERO)
          for a, b in product(AX, repeat=2)}

    @lru_cache(None)
    def covariant(indices):
        if len(indices) == 4:
            return lower[indices]
        d, rest = indices[0], indices[1:]
        result = covariant(rest).derivative() if d == active else ZERO
        for slot, index in enumerate(rest):
            for e in AX:
                if any(gamma[e, d, index].c):
                    replacement = rest[:slot] + (e,) + rest[slot+1:]
                    result -= gamma[e, d, index] * covariant(replacement)
        return result

    return g, inv, gamma, mixed, lower, ric, scalar, tf, covariant


# Nonzero warped geometry, independent of any Einstein assumption.
A = Jet([Q(5, 4), Q(2, 3), Q(1, 7), Q(-2, 11), Q(3, 13)])
base = geometry([-1, 1, A*A, 1], 1)
g, inv, gamma, mixed, lower, ric, scalar, tf, covariant = base
K = -A.derivative().derivative() / A
require('warp sectional curvature from coordinate definition',
        lower[1, 2, 1, 2].value / A.value**2 == K.value)
require('warp scalar from independent contractions', scalar.value == 2*K.value)
require('nonzero non-Einstein witness', any(v.value for v in tf.values()))
require('first covariant frame derivative',
        covariant((1, 1, 2, 1, 2)).value / A.value**2 == K.derivative().value)
require('second covariant frame derivative',
        covariant((1, 1, 1, 2, 1, 2)).value / A.value**2
        == K.derivative().derivative().value)

for b in AX:
    divergence = ZERO
    for a in AX:
        value = ric[a, b].derivative() if a == 1 else ZERO
        for e in AX:
            value -= gamma[e, a, a] * ric[e, b] + gamma[e, a, b] * ric[a, e]
        divergence += inv[a] * value
    target = scalar.derivative()/2 if b == 1 else ZERO
    require('contracted Bianchi component ' + str(b), divergence.value == target.value)

for epsilon in [Q(1, 2), Q(1, 3), Q(1, 5)]:
    scale = 1 / epsilon**2
    rescaled = geometry([scale*x for x in g], 1)
    rg, ri, rga, rm, rl, rr, rs, rt, rc = rescaled
    tag = ' epsilon=' + str(epsilon)
    require('connection constant-scale invariance' + tag,
            all(rga[k].value == gamma[k].value for k in gamma))
    require('mixed Riemann constant-scale invariance' + tag,
            all(rm[k].value == mixed[k].value for k in mixed))
    require('covariant Riemann coordinate scale' + tag,
            all(rl[k].value == scale*lower[k].value for k in lower))
    require('covariant Ricci invariance' + tag,
            all(rr[k].value == ric[k].value for k in ric))
    require('scalar inverse scale' + tag, rs.value == epsilon**2*scalar.value)
    require('covariant trace-free Ricci invariance' + tag,
            all(rt[k].value == tf[k].value for k in tf))
    # e_x=partial_x, e_y=A^-1 partial_y; E=epsilon e.
    for j in range(3):
        indices = (1,)*j + (1, 2, 1, 2)
        h_component = covariant(indices).value / A.value**2
        g_component = rc(indices).value * epsilon**(4+j) / A.value**2
        require('orthonormal curvature-jet weight j=' + str(j) + tag,
                g_component == epsilon**(j+2)*h_component)
    require('normalized TF frame conversion' + tag,
            epsilon**2 * rt[0, 0].value / epsilon**2 == tf[0, 0].value)
    catch('coordinate Riemann mistaken for ON weight' + tag,
          rl[1, 2, 1, 2].value == epsilon**2*lower[1, 2, 1, 2].value)
    catch('coordinate Ricci incorrectly scales' + tag,
          rr[1, 1].value == epsilon**2*ric[1, 1].value)
    catch('absolute flattening implies normalized flatness' + tag,
          epsilon**2*rt[0, 0].value / epsilon**2 == 0)

# Explicit Einstein controls with differing Lambda; these do not select F.
for H in [Q(1), Q(2)]:
    time = Jet([Q(3, 2), 1])
    conformal = (H*H*time*time).inverse()
    einstein = geometry([-conformal, conformal, conformal, conformal], 0)
    eg, ei, ega, em, el, er, es, et, ec = einstein
    require('Einstein scalar H=' + str(H), es.value == 12*H*H)
    require('Einstein Ricci H=' + str(H),
            all(er[a, b].value == (3*H*H*eg[a].value if a == b else 0)
                for a, b in product(AX, repeat=2)))
    require('Einstein TF H=' + str(H), all(v.value == 0 for v in et.values()))
catch('Bianchi forces Lambda zero', es.value == 0)

diagnostics = []
for epsilon in [Q(1, 2), Q(1, 4), Q(1, 8)]:
    for phase in ['zero', 'quarter']:
        # Taylor jets at x=0 and x=pi*epsilon/2, exactly, without float sin.
        # A=1+epsilon^4 sin(x/epsilon), A>0 globally for epsilon<1.
        if phase == 'zero':
            warp = Jet([1, epsilon**3, 0, -epsilon/6, 0])
        else:
            warp = Jet([1+epsilon**4, 0, -epsilon**2/2, 0, Q(1, 24)])
        result = geometry([-1, 1, warp*warp, 1], 1)
        derivative = result[-1]
        observed = [derivative((1,)*j+(1, 2, 1, 2)).value / warp.value**2
                    for j in range(3)]
        if phase == 'zero':
            expected = [Q(0), epsilon, -2*epsilon**4]
        else:
            expected = [epsilon**2/(1+epsilon**4), Q(0), -1/(1+epsilon**4)**2]
        require('high-frequency actual metric derivatives ' + str(epsilon) + ' ' + phase,
                observed == expected)
        require('high-frequency positive metric warp ' + str(epsilon) + ' ' + phase,
                1-epsilon**4 > 0 and warp.value > 0)
        diagnostics.append({'epsilon': str(epsilon), 'phase': phase,
                            'K_DK_DDK': list(map(str, observed))})
    catch('curvature bound alone gives derivative epsilon cubed ' + str(epsilon),
          epsilon <= epsilon**3)
    catch('curvature bound alone gives second derivative epsilon fourth ' + str(epsilon),
          1/(1+epsilon**4)**2 <= epsilon**4)

# Local bookkeeping on the analytic coefficient of contracted Bianchi in 4D.
require('Bianchi scalar coefficient nonzero', Q(1, 4)-Q(1, 2) != 0)
catch('zero-a allows division', Q(0) != 0)

print(json.dumps({'status': 'PASS', 'python': platform.python_version(),
                  'arithmetic': 'exact Fraction Taylor jets, degree 4',
                  'mathematical_checks': len(checks),
                  'wrong_claim_catches': len(catches),
                  'check_names': checks, 'catch_names': catches,
                  'high_frequency_metric': diagnostics,
                  'limitations': ['finite diagonal one-coordinate metric witnesses',
                                  'no universal compactness or metric limit computation',
                                  'high-frequency diagnostic not asserted DDR balanced',
                                  'zero-a catch is an elementary branch check only']},
                 indent=2, sort_keys=True))
