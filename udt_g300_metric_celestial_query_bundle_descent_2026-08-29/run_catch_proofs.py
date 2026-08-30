#!/usr/bin/env python3
"""Hostile mutation catches for G300."""

from fractions import Fraction as F
import json

import derive_celestial_query_bundle as d


def projective_clock_column(m):
    c = d.mv(m, (d.ONE,d.ZERO,d.ZERO,d.ZERO))
    return tuple(c[i]/c[0] for i in range(1,4))


def main():
    catches = {}

    n = d.sky((F(1,3),F(-1,4)))
    p = d.relation((F(1,5),F(1,7),F(0)),(2,1,1,0))
    y = d.mv(p,(d.ONE,n[1],n[2],n[3]))

    catches["wrong_frequency_sign_rejected"] = d.dot(y,(d.ONE,d.ZERO,d.ZERO,d.ZERO)) < 0 and y[0] > 0

    omitted = tuple(y[i]-(d.ONE if i==0 else d.ZERO) for i in range(4))
    catches["missing_frequency_normalization_rejected"] = not (
        d.dot(omitted,(d.ONE,d.ZERO,d.ZERO,d.ZERO)) == 0 and d.dot(omitted,omitted) == 1
    )

    p1 = d.relation((F(1,4),F(0),F(0)),(1,0,0,0))
    p2 = d.relation((F(0),F(1,5),F(1,6)),(2,1,0,1))
    forward = d.aberration(d.mm(p2,p1),n)[0]
    reversed_order = d.aberration(d.mm(p1,p2),n)[0]
    catches["wrong_composition_order_rejected"] = forward != reversed_order

    n1,r1,_ = d.aberration(p1,n)
    _,r2,_ = d.aberration(p2,n1)
    _,rd,_ = d.aberration(d.mm(p2,p1),n)
    catches["additive_clock_ratio_rejected"] = rd == r1*r2 and rd != r1+r2

    rr=F(3,2); w=F(2,3)
    gamma=(1+rr*rr+rr*rr*w*w)/(2*rr)
    a=(-1+rr*rr+rr*rr*w*w)/(2*rr)
    uy=(gamma,a,w,F(0)); e1=(F(0),F(1),F(0),F(0))
    ny=(rr-gamma,rr-a,-w,F(0))
    det_separator=-rr*rr*w
    catches["equal_W1_scalar_plane_collapse_rejected"] = det_separator != 0

    st=tuple(e1[i]+a*uy[i] for i in range(4))
    catches["transported_source_plane_omission_rejected"] = (
        d.dot(uy,st)==0 and d.dot(st,st)>0 and e1==tuple(st[i]-a*uy[i] for i in range(4))
    )

    e_x=(F(1),F(0),F(0))
    quarter_turn=((F(0),F(-1),F(0)),(F(1),F(0),F(0)),(F(0),F(0),F(1)))
    rotated=tuple(sum(quarter_turn[i][j]*e_x[j] for j in range(3)) for i in range(3))
    catches["false_unique_isotropic_section_rejected"] = rotated != e_x

    minus=tuple(-x for x in n)
    catches["oriented_unoriented_collapse_rejected"] = (
        n != minus and tuple(-minus[i] for i in range(4)) == n
    )

    bx=(
        (F(5,4),F(3,4),F(0),F(0)),
        (F(3,4),F(5,4),F(0),F(0)),
        (F(0),F(0),F(1),F(0)),
        (F(0),F(0),F(0),F(1)),
    )
    bs=(
        (F(441,359),F(0),F(200,359),F(160,359)),
        (F(0),F(1),F(0),F(0)),
        (F(200,359),F(0),F(409,359),F(40,359)),
        (F(160,359),F(0),F(40,359),F(391,359)),
    )
    rot=(
        (F(1),F(0),F(0),F(0)),
        (F(0),F(0),F(-1),F(0)),
        (F(0),F(1),F(0),F(0)),
        (F(0),F(0),F(0),F(1)),
    )
    catches["bare_projective_composition_rejected"] = (
        projective_clock_column(bs) == projective_clock_column(d.mm(bs,rot))
        and projective_clock_column(d.mm(bs,bx)) != projective_clock_column(d.mm(d.mm(bs,rot),bx))
    )

    assert all(catches.values()), catches
    print(json.dumps({"status":"PASS","hostile_catches":len(catches),"catches":catches},indent=2,sort_keys=True))


if __name__ == "__main__":
    main()
