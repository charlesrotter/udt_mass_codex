"""Stdlib-only saved-input recomputation; no production-module imports.

Same author/context: implementation distinction is not independent review.
Computes a Minkowski Gram and determinant using Fraction, then checks saved
baseline output. Writes no files. The general smooth proof is not recomputed.
"""
from fractions import Fraction as Q
import json
from math import isqrt
from pathlib import Path

package = Path(__file__).parent
inputs = json.loads((package/'WITNESS_INPUTS.json').read_text())
saved = json.loads((package/'CHECK_RESULTS.json').read_text())
baseline = json.loads(saved['runs'][0]['stdout'])


def dot(v, w):
    return -v[0]*w[0]+sum(v[i]*w[i] for i in range(1, 4))


def square_root(value):
    numerator, denominator = isqrt(value.numerator), isqrt(value.denominator)
    assert numerator*numerator == value.numerator
    assert denominator*denominator == value.denominator
    return Q(numerator, denominator)


rows = []
for cut in inputs['cuts']:
    rad = Q(cut['radius'])
    qv, qw = map(Q, inputs['cut_gradient'])
    v, w = (qv, 2*rad, Q(0), qv), (qw, Q(0), 2*rad, qw)
    area = square_root(dot(v,v)*dot(w,w)-dot(v,w)**2)
    u = list(map(Q, cut['observer']))
    k = (Q(1),Q(0),Q(0),Q(1))
    assert dot(u,u) == -1 and dot(k,k) == 0
    omega = -dot(u,k)
    # Stereographic solid angle at origin: source derivative cross product has area4.
    dx, dy = (Q(2),Q(0),Q(0)), (Q(0),Q(2),Q(0))
    cross = (dx[1]*dy[2]-dx[2]*dy[1], dx[2]*dy[0]-dx[0]*dy[2],
             dx[0]*dy[1]-dx[1]*dy[0])
    source_area = square_root(sum(a*a for a in cross))
    rho = Q(inputs['measure_per_solid_angle'])*source_area/Q(inputs['phase_spacing'])/area
    row = {key: str(value) for key, value in
           {'area': area, 'omega': omega, 'rho': rho, 'gamma': omega*rho}.items()}
    rows.append(row)
for recomputed, claimed in zip(rows, baseline['cut_witness'], strict=True):
    for key, value in recomputed.items():
        assert value == claimed[key], (key, value, claimed[key])
ratio = Q(rows[1]['gamma'])/Q(rows[0]['gamma'])
assert ratio == Q(baseline['ratio'])
print(json.dumps({'kind': 'same-context stdlib rational saved-input recomputation',
                  'cut_witness': rows, 'ratio': str(ratio), 'matches_saved': True}, indent=2))
