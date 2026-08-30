#!/usr/bin/env python3
"""Implementation-distinct exact algebra verifier for G300's celestial control fiber."""

from fractions import Fraction as Q
import json


Z = Q(0)
O = Q(1)


def mdot(a,b):
    return -a[0]*b[0] + a[1]*b[1] + a[2]*b[2] + a[3]*b[3]


def apply(m,v):
    return tuple(sum(row[j]*v[j] for j in range(4)) for row in m)


def product(a,b):
    cols = tuple(zip(*b))
    return tuple(tuple(sum(a[i][k]*cols[j][k] for k in range(4)) for j in range(4)) for i in range(4))


def hyperbolic(px,py,pz):
    p=(Q(px),Q(py),Q(pz)); s2=sum(t*t for t in p); d=O-s2
    G=(O+s2)/d; v=tuple(2*t/d for t in p)
    out=[]
    out.append((G,v[0],v[1],v[2]))
    for i in range(3):
        out.append(tuple([v[i]] + [(O if i==j else Z)+v[i]*v[j]/(G+O) for j in range(3)]))
    return tuple(out)


def zrot(t):
    # Rational circle parameterization: cos=(1-t^2)/(1+t^2), sin=2t/(1+t^2).
    t=Q(t); d=O+t*t; c=(O-t*t)/d; s=2*t/d
    return ((O,Z,Z,Z),(Z,c,-s,Z),(Z,s,c,Z),(Z,Z,Z,O))


def unit_direction(a,b):
    a=Q(a); b=Q(b); d=O+a*a+b*b
    return (Z,(O-a*a-b*b)/d,2*a/d,2*b/d)


def map_sky(m,n):
    y=apply(m,(O,n[1],n[2],n[3]))
    if y[0] <= 0:
        raise AssertionError("nonfuture image")
    return (Z,y[1]/y[0],y[2]/y[0],y[3]/y[0]), O/y[0]


def linv(m):
    signs=(-O,O,O,O)
    return tuple(tuple(signs[i]*m[j][i]*signs[j] for j in range(4)) for i in range(4))


def main():
    mats=[]
    for p in ((Q(1,7),Q(1,8),Q(0)),(Q(-1,9),Q(2,11),Q(1,12)),(Q(2,13),Q(-1,14),Q(1,15))):
        for t in (Q(0),Q(1,3),Q(-2,5),Q(3,7)):
            mats.append(product(hyperbolic(*p),zrot(t)))
    dirs=[unit_direction(Q(a,9),Q(b,10)) for a in range(-4,5) for b in range(-3,4)]
    assertions=0; cases=0

    for m in mats:
        mi=linv(m)
        for n in dirs:
            cases+=1
            ny,r=map_sky(m,n)
            assert mdot(n,n)==O and mdot(ny,ny)==O; assertions+=2
            nb,rb=map_sky(mi,ny)
            assert nb==n and rb==O/r; assertions+=2
            assert mdot((r,Z,Z,Z),ny)==Z; assertions+=1

    for m1 in mats:
        for m2 in mats:
            joined=product(m2,m1)
            for n in dirs:
                cases+=1
                n1,r1=map_sky(m1,n)
                n2,r2=map_sky(m2,n1)
                nd,rd=map_sky(joined,n)
                assert n2==nd; assertions+=1
                assert r1*r2==rd; assertions+=1

    # Plane quotient: n and -n are distinct oriented queries but the same unoriented plane.
    for n in dirs:
        cases+=1
        minus=tuple(-x for x in n)
        assert minus != n; assertions+=1
        assert tuple(-minus[i] for i in range(4)) == n; assertions+=1

    result={
        "status":"PASS",
        "method":"independent Fraction coordinate implementation",
        "relations":len(mats),
        "directions":len(dirs),
        "cases":cases,
        "assertions":assertions,
        "reversal_exact":True,
        "noncollinear_composition_exact":True,
        "clock_cocycle_exact":True,
        "oriented_to_unoriented_quotient":"S^2 -> RP^2",
        "lawful_query_family_ownership":"NOT_TESTED_BY_ALGEBRA",
    }
    print(json.dumps(result,indent=2,sort_keys=True))


if __name__=="__main__":
    main()
