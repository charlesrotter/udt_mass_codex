#!/usr/bin/env python3
"""Independent exact covariant-variation verifier for G337; imports no production code."""

from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction as Q
from pathlib import Path


class J:
    __slots__ = ("v", "p", "q")

    def __init__(self, v=0, p=0, q=0):
        self.v, self.p, self.q = Q(v), Q(p), Q(q)

    @staticmethod
    def up(x):
        return x if isinstance(x, J) else J(x)

    def __add__(self, x):
        x = self.up(x)
        return J(self.v + x.v, self.p + x.p, self.q + x.q)

    __radd__ = __add__

    def __neg__(self):
        return J(-self.v, -self.p, -self.q)

    def __sub__(self, x):
        return self + (-self.up(x))

    def __rsub__(self, x):
        return self.up(x) - self

    def __mul__(self, x):
        x = self.up(x)
        return J(self.v*x.v, self.p*x.v+self.v*x.p,
                 self.q*x.v+2*self.p*x.p+self.v*x.q)

    __rmul__ = __mul__

    def inv(self):
        return J(1/self.v, -self.p/self.v**2, 2*self.p**2/self.v**3-self.q/self.v**2)

    def __truediv__(self, x):
        return self * self.up(x).inv()

    def __rtruediv__(self, x):
        return self.up(x) * self.inv()


def matrix_inverse_j(a):
    n = len(a)
    z, o = J(0), J(1)
    m = [list(a[i]) + [o if i == j else z for j in range(n)] for i in range(n)]
    for c in range(n):
        k = next(k for k in range(c, n) if m[k][c].v)
        m[c], m[k] = m[k], m[c]
        d = m[c][c]
        m[c] = [u/d for u in m[c]]
        for k in range(n):
            if k != c:
                d = m[k][c]
                m[k] = [m[k][j]-d*m[c][j] for j in range(2*n)]
    return [u[n:] for u in m]


def weighted_data(x0, u, v, sign, mu=Q(16, 25)):
    x, one = J(x0, 1, 0), J(1)
    f = u*x + v*(one-x)
    rho = x*(one-x)
    eta = [J(0), x/f, (one-x)/f]
    zeta = [J(0), J(v)/f, J(-u)/f]
    g = [[J(0) for _ in range(3)] for _ in range(3)]
    g[0][0] = 1/(4*rho*f)
    for i in (1, 2):
        for k in (1, 2):
            g[i][k] = rho/f*zeta[i]*zeta[k]+eta[i]*eta[k]
    n = 4*u*u*x-8*u*v+u*x-4*v*v*x+4*v*v-v*x+v
    Rj = -2*n/f
    b = Q(sign)
    C = b*(1-2*mu)
    L = Rj.v/2-2*b*b*mu+3*b*b*mu*mu
    bp = Rj.p/(b+C)
    bpp = (Rj.q-bp*bp)/(b+C)
    bj = J(b, bp, bpp)
    aj = (C-bj)/2
    K = [[aj*g[i][k]+bj*eta[i]*eta[k] for k in range(3)] for i in range(3)]
    return g, K, eta, Rj, b, C, L


def geometry(g):
    gi = matrix_inverse_j(g)
    G = [[[[Q(0), Q(0)] for _ in range(3)] for _ in range(3)] for _ in range(3)]
    for a in range(3):
        for i in range(3):
            for j in range(3):
                value = J(0)
                for l in range(3):
                    term = (g[l][j].p if i == 0 else 0)+(g[l][i].p if j == 0 else 0)
                    term -= g[i][j].p if l == 0 else 0
                    dterm = (g[l][j].q if i == 0 else 0)+(g[l][i].q if j == 0 else 0)
                    dterm -= g[i][j].q if l == 0 else 0
                    value += gi[a][l]*J(term, dterm, 0)/2
                G[a][i][j] = [value.v, value.p]
    Ric = [[Q(0) for _ in range(3)] for _ in range(3)]
    for i in range(3):
        for j in range(3):
            z = G[0][i][j][1]
            if j == 0:
                z -= sum(G[k][i][k][1] for k in range(3))
            z += sum(G[k][i][j][0]*G[l][k][l][0]-G[l][i][k][0]*G[k][j][l][0]
                     for k in range(3) for l in range(3))
            Ric[i][j] = z
    return gi, G, Ric


def covariant_ricci_variation(g, K, gi, G):
    """Compute D Ric[-2K] without differentiating a time-deformed metric."""
    h = [[-2*K[i][j] for j in range(3)] for i in range(3)]
    # First covariant derivative as x-jets. Only its value and x derivative are needed.
    Dh = [[[[Q(0), Q(0)] for _ in range(3)] for _ in range(3)] for _ in range(3)]
    for a in range(3):
        for i in range(3):
            for j in range(3):
                partial = J(h[i][j].p if a == 0 else 0,
                            h[i][j].q if a == 0 else 0, 0)
                value = partial
                for l in range(3):
                    value -= J(*G[l][a][i], 0)*h[l][j]
                    value -= J(*G[l][a][j], 0)*h[i][l]
                Dh[a][i][j] = [value.v, value.p]
    D2 = [[[[Q(0) for _ in range(3)] for _ in range(3)] for _ in range(3)] for _ in range(3)]
    for outer in range(3):
        for inner in range(3):
            for i in range(3):
                for j in range(3):
                    z = Dh[inner][i][j][1] if outer == 0 else Q(0)
                    for l in range(3):
                        z -= G[l][outer][inner][0]*Dh[l][i][j][0]
                        z -= G[l][outer][i][0]*Dh[inner][l][j][0]
                        z -= G[l][outer][j][0]*Dh[inner][i][l][0]
                    D2[outer][inner][i][j] = z
    # tr(h)=-2 tau; obtain its complete x-jet directly, including inverse-metric variation.
    trh = sum(gi[i][j]*h[i][j] for i in range(3) for j in range(3))
    Hess = [[Q(0) for _ in range(3)] for _ in range(3)]
    for i in range(3):
        for j in range(3):
            z = trh.q if i == 0 and j == 0 else Q(0)
            z -= G[0][i][j][0]*trh.p
            Hess[i][j] = z
    out = [[Q(0) for _ in range(3)] for _ in range(3)]
    giv = [[gi[i][j].v for j in range(3)] for i in range(3)]
    for i in range(3):
        for j in range(3):
            first = sum(giv[k][a]*D2[a][i][k][j] for k in range(3) for a in range(3))
            second = sum(giv[k][a]*D2[a][j][k][i] for k in range(3) for a in range(3))
            lap = sum(giv[a][k]*D2[a][k][i][j] for a in range(3) for k in range(3))
            out[i][j] = (first+second-lap-Hess[i][j])/2
    return out


def mm(a, b):
    return [[sum(a[i][k]*b[k][j] for k in range(3)) for j in range(3)] for i in range(3)]


def madd(*args):
    return [[sum(a[i][j] for a in args) for j in range(3)] for i in range(3)]


def mscale(c, a):
    return [[c*a[i][j] for j in range(3)] for i in range(3)]


def one_control(x, u, v, sign, mu=Q(16, 25)):
    g, K, eta, Rj, b, C, L = weighted_data(x, u, v, sign, mu)
    gi, G, Ric = geometry(g)
    gv = [[g[i][j].v for j in range(3)] for i in range(3)]
    giv = [[gi[i][j].v for j in range(3)] for i in range(3)]
    Kv = [[K[i][j].v for j in range(3)] for i in range(3)]
    A = mm(giv, Kv)
    tau = sum(A[i][i] for i in range(3))
    B = mm(Kv, mm(giv, Kv))
    Evol = madd(Ric, mscale(tau, Kv), mscale(-2, B), mscale(-L, gv))
    Bd = madd(mm(Evol, mm(giv, Kv)), mm(Kv, mm(giv, Evol)),
              mscale(2, mm(Kv, mm(giv, mm(Kv, mm(giv, Kv))))))
    Rd = covariant_ricci_variation(g, K, gi, G)
    T = madd(mscale(-1, Rd), mscale(2, Bd))
    xi = [Q(0), u, v]
    ex2 = 1/gv[0][0]
    sx = T[0][0]*ex2
    sv = sum(xi[i]*T[i][j]*xi[j] for i in range(3) for j in range(3))
    cross = sum(T[0][j]*xi[j] for j in range(3))
    s2 = (1-mu)*sx+mu*sv
    q0 = -((1-mu)*(C-b)/2+mu*(C+b)/2)
    s1 = -((1-mu)*Evol[0][0]*ex2+mu*sum(xi[i]*Evol[i][j]*xi[j]
                                                 for i in range(3) for j in range(3)))
    grad_R_squared = ex2*Rj.p*Rj.p
    return Rj.v, q0, s1, s2, cross, grad_R_squared


def verify():
    checks = []
    def ok(c, label):
        if not c:
            raise AssertionError(label)
        checks.append(label)
    controls = ((Q(1438,1919),Q(1,4),Q(1,2)),
                (Q(4071,6157),Q(1,3),Q(1,2)))
    expected = {
        -1: (Q(-11982281327,699840000), Q(-207122235829,18895680000)),
         1: (Q(11982281327,699840000), Q(207122235829,18895680000)),
    }
    obtained = {}
    for sign in (-1,1):
        values=[]
        for k,(x,u,v) in enumerate(controls):
            R,q0,s1,s2,cross,grad_R_squared=one_control(x,u,v,sign)
            ok(R==Q(319,200),f"same_R_{sign}_{k}")
            ok(q0==0,f"q0_{sign}_{k}")
            ok(s1==0,f"s1_{sign}_{k}")
            ok(cross==0,f"cross_{sign}_{k}")
            ok(s2==expected[sign][k],f"production_target_rederived_{sign}_{k}")
            values.append(s2)
        ok(values[0]!=values[1],f"tuple_nonownership_{sign}")
        first = one_control(*controls[0], sign)[5]
        second = one_control(*controls[1], sign)[5]
        ok(first != second, f"invariant_spatial_germs_distinct_{sign}")
        obtained[str(sign)]=[str(z) for z in values]
    for sign in (-1,1):
        R,q0,s1,s2,cross,_=one_control(Q(1,3),Q(719,1600),Q(719,1600),sign)
        ok(s2==8*sign*Q(16,25),f"homogeneous_formula_{sign}")
    payload={
        "all_passed":True,
        "check_count":len(checks),
        "checks_sha256":hashlib.sha256("\n".join(checks).encode()).hexdigest(),
        "checks":checks,
        "imports_production_code":False,
        "reads_production_output":False,
        "method":"exact covariant Ricci-variation formula on independently rebuilt coordinate jets",
        "twin_s2":obtained,
    }
    return payload


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--output",type=Path)
    args=parser.parse_args()
    payload=verify()
    if args.output:
        args.output.write_text(json.dumps(payload,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(f"G337 independent PASS: {payload['check_count']} exact checks")


if __name__ == "__main__":
    main()
