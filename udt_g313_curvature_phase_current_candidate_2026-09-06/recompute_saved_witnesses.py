"""Stdlib exact saved-artifact anchor; no curvature/checker module imports.

Same author/context, distinct finite arithmetic implementation, NOT independent
review. Does not re-prove the full symbolic tensor or the general argument.
"""
from fractions import Fraction as Q
from math import isqrt
from pathlib import Path
import json
import platform

p = Path(__file__).parent
inputs = json.loads((p/'WITNESS_INPUTS.json').read_text())
saved = json.loads((p/'AUTHOR_RESULT.json').read_text())


def sqrtq(z):
    n,d = isqrt(z.numerator),isqrt(z.denominator)
    assert n*n == z.numerator and d*d == z.denominator
    return Q(n,d)


rows = []
for av, recorded in zip(inputs['A_values'],saved['witnesses'],strict=True):
    A = Q(av)
    # Lower tidal components from -one-half the exact Hessian of H.
    tidal = (-A,A)
    # Equal squared transverse norms for W and its first-pair dual here.
    B = 2*sum(z*z for z in tidal)
    b = sqrtq(sqrtq(B))
    point = list(map(Q,inputs['point']))
    H = A*(point[2]**2-point[3]**2)
    alpha,px,py = map(Q,[inputs['observer_u_component'],
                       inputs['observer_x_component'],inputs['observer_y_component']])
    U = [alpha,(1+H*alpha**2+px**2+py**2)/(2*alpha),px,py]
    def dot(z,w):
        return H*z[0]*w[0]-z[0]*w[1]-z[1]*w[0]+z[2]*w[2]+z[3]*w[3]
    assert dot(U,U) == -1
    C = [Q(0),b,Q(0),Q(0)]
    assert dot(C,C) == 0
    qx,qy = map(Q,inputs['cut_v_gradient'])
    e1,e2 = [Q(0),qx,Q(1),Q(0)],[Q(0),qy,Q(0),Q(1)]
    J = sqrtq(dot(e1,e1)*dot(e2,e2)-dot(e1,e2)**2)
    Gamma = -dot(U,C)
    Delta = Q(inputs['phase_spacing'])
    phase_factor = Q(inputs['phase_unit_factor'])
    assert Gamma == b*alpha*Delta/(Delta*J)
    assert Gamma == phase_factor*b*alpha*Delta/(phase_factor*Delta*J)
    row = {'A':str(A),'B_uuuu':str(B),'beta_u':str(-b),
           'C_v_component':str(b),'observer':list(map(str,U)),'J':str(J),'Gamma':str(Gamma)}
    assert row == recorded, (row,recorded)
    rows.append(row)
rect = [[Q(z) for z in side] for side in inputs['finite_label_rectangle']]
area = (rect[0][1]-rect[0][0])*(rect[1][1]-rect[1][0])
patch = {'coordinate_area':str(area),'mu':str(Delta*area),
         'Xi':str(Q(inputs['phase_interval_width'])*area),
         'homothetic_mu':str(Q(inputs['metric_homothety_factor'])**2*Delta*area)}
assert patch == saved['finite_patch']
print(json.dumps({'kind':'same-context stdlib rational saved-artifact recomputation',
    'python':platform.python_version(),'matches_saved':True,'witnesses':rows,'finite_patch':patch},indent=2))
