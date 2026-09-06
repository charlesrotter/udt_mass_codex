"""Reviewer implementation: differentiate the full endpoint map and use wedge coefficients.

No candidate imports. Input constants transcribed from authenticated WITNESS_INPUTS.json.
An additional off-origin, transverse-boost witness is reviewer chosen mathematical data.
"""
from itertools import permutations
import json
import sympy as sp

v, w, theta, R, qv, qw = sp.symbols("v w theta R qv qw", real=True)
d = 1 + v*v + w*w
n = sp.Matrix([2*v/d, 2*w/d, (1-v*v-w*w)/d])
radius = R + qv*v + qw*w
X = sp.Matrix([radius-theta, *(radius*n)])
derivatives = [X.diff(v), X.diff(w)]


def minkowski(a, b):
    return -a[0]*b[0] + sum(a[i]*b[i] for i in range(1, 4))


def wedge4(columns):
    result = 0
    for p in permutations(range(4)):
        inversions = sum(p[i] > p[j] for i in range(4) for j in range(i+1, 4))
        term = (-1)**inversions
        for j in range(4):
            term *= columns[j][p[j]]
        result += term
    return sp.simplify(result)


def row(cut_radius, observer, v0=sp.Integer(0), w0=sp.Integer(0)):
    values = {v:v0, w:w0, R:cut_radius, qv:sp.Rational(1,3), qw:-sp.Rational(2,7)}
    E = [D.subs(values) for D in derivatives]
    area = sp.sqrt(sp.factor(minkowski(E[0],E[0])*minkowski(E[1],E[1])-minkowski(E[0],E[1])**2))
    tangents = [n.diff(v).subs(values), n.diff(w).subs(values)]
    source_area = sp.sqrt(sp.factor(tangents[0].cross(tangents[1]).dot(tangents[0].cross(tangents[1]))))
    density = sp.Rational(7,3)*source_area
    spacing = sp.Rational(5,2)
    k = sp.Matrix([1, *n.subs(values)])
    omega = -minkowski(observer,k)
    rho = sp.simplify(density/(spacing*area))
    C = rho*k
    assert minkowski(observer,observer) == -1 and observer[0] > 0
    assert sp.simplify(minkowski(k,k)) == 0
    projected = [e + minkowski(observer,e)*k/omega for e in E]
    assert all(sp.simplify(minkowski(observer,e)) == 0 for e in projected)
    form = abs(wedge4([C, observer, *projected]))
    gamma_from_form = sp.simplify(form/area)
    gamma_from_contraction = sp.simplify(-minkowski(observer,C))
    assert gamma_from_form == gamma_from_contraction
    # Flux in the observer's rest-space 3-volume is the same via spatial coarea.
    rest_longitudinal = k/omega-observer
    coarea_form = abs(wedge4([C, rest_longitudinal, *projected]))
    assert sp.simplify(coarea_form/area) == gamma_from_contraction
    return {key: str(value) for key,value in {
        "cut_radius_at_point": radius.subs(values), "source_area":source_area,
        "cut_area":area, "omega":omega, "rho":rho,
        "gamma_contraction":gamma_from_contraction, "gamma_wedge":gamma_from_form,
        "absolute_time_screen_form":form}.items()}

rows = [row(sp.Integer(2), sp.Matrix([1,0,0,0])),
        row(sp.Integer(5), sp.Matrix([sp.Rational(5,4),0,0,sp.Rational(3,4)]))]
assert rows[0]["cut_area"] == "16" and rows[1]["cut_area"] == "100"
assert rows[0]["gamma_wedge"] == "7/30" and rows[1]["gamma_wedge"] == "7/375"
ratio = sp.Rational(rows[1]["gamma_wedge"])/sp.Rational(rows[0]["gamma_wedge"])
assert ratio == sp.Rational(2,25)
off_origin = row(sp.Integer(3), sp.Matrix([sp.Rational(5,4),sp.Rational(3,4),0,0]),
                 sp.Rational(1,3), sp.Rational(2,5))
print(json.dumps({"method":"full map differentiation plus explicit exterior product",
                  "input_source":"authenticated WITNESS_INPUTS.json, constants transcribed",
                  "saved_witness_reconstruction":rows, "ratio":str(ratio),
                  "additional_off_origin_transverse_observer":off_origin,
                  "all_checks_passed":True}, indent=2))
