"""HB3 exact algebra/quantifier controls; no evolution or orbit solve.

The geometric, symmetry-extension, and intermediate-value arguments are prose
proof obligations. This program cannot certify them by finite sampling.
"""
import hashlib
import json
import platform
import sys
from fractions import Fraction as F
from pathlib import Path
import sympy as s

step = Path(__file__).resolve().parent
hb2 = step.parent/'step_02'
assert hashlib.sha256((hb2/'CANDIDATE_INITIAL.md').read_bytes()).hexdigest() == 'd5238bc2ef9407e3de483d386823b65a128eddaea6e10d7b0e85c33e9b42260c'
assert hashlib.sha256((hb2/'review/REVIEW_RECORD.md').read_bytes()).hexdigest() == '4982cb33d09abd86aac98116124ce28a1275b833ae4234d2d8e7431cb369905b'

x = s.symbols('x', real=True)
u, v = s.symbols('u v', positive=True)
D = s.symbols('D', nonzero=True, real=True)
flux = u*x+v*(1-x)
eta = s.Matrix([x/flux, (1-x)/flux])
zeta = s.Matrix([v/flux, -u/flux])
H = x*(1-x)/flux*zeta*zeta.T+eta*eta.T
Hi = (s.Matrix([[H[1, 1], -H[0, 1]], [-H[1, 0], H[0, 0]]])/H.det()).applyfunc(s.cancel)
ep = eta.diff(x)
assert (Hi*ep-s.Matrix([1/x, -1/(1-x)])).applyfunc(s.cancel) == s.zeros(2, 1)
R = 24*u*v/flux-8*(u+v)-2
Rp, Delta = s.diff(R, x), (6-R)/2
rot = (2*x*(1-x)*flux*Hi*ep*Rp/D).applyfunc(s.cancel)
assert (rot-2*flux*Rp/D*s.Matrix([1-x, -x])).applyfunc(s.cancel) == s.zeros(2, 1)
Y = s.Rational(5, 2)*rot/Delta
qdot = s.cancel((Y[0]*v-u*Y[1])/v**2)
kappa = -120*u*(u-v)/v
assert s.cancel(qdot-kappa/(Delta*D)) == 0
rr, sector = s.symbols('R sector', real=True)
poly = s.Poly((6-rr)**2*(rr+sector)/2, rr)
assert poly.degree() == 3 and poly.LC() == s.Rational(1, 2)

# Recompute an actual saved quantity from reviewed HB2, not a generated HB3 target.
saved = json.loads((hb2/'author_check_initial.stdout').read_text())
matched = []
for row in saved['fixtures']:
    w1, w2 = map(F, row['weights'])
    xx, gap, dd = F(row['x']), F(row['gap']), F(row['root_D'])
    y = list(map(F, row['Y']))
    actual = (y[1]*w2-w1*y[2])/(w2*w2)
    expected = -120*w1*(w1-w2)/(w2*gap*dd)
    assert actual == expected
    matched.append(dict(weights=row['weights'], x=row['x'], C=row['C'],
                        Lambda=row['Lambda'], root_D=str(dd), qdot=str(actual)))

def radial(w1, w2, xx):
    ff = w1*xx+w2*(1-xx)
    return 24*w1*w2/ff-8*(w1+w2)-2

def anchor(w1, w2, xx, C, lam):
    scalar = radial(w1, w2, xx)
    gap = (6-scalar)/2
    root2 = 2*(scalar+2*C*C-2*lam)
    assert gap != 0 and root2 > 0
    kap = -120*w1*(w1-w2)/w2
    return dict(x=str(xx), R=str(scalar), gap=str(gap), D_squared=str(root2),
                qdot_squared=str(kap*kap/(gap*gap*root2)))

pairs = []
for w1, w2 in [(F(1, 4), F(1, 2)), (F(2), F(7, 4)), (F(1, 2), F(1, 4))]:
    C, lam = F(3), F(0)
    ends = [radial(w1, w2, F(0)), radial(w1, w2, F(1))]
    assert (6-ends[0])*(6-ends[1]) > 0
    assert min(ends)+2*C*C-2*lam > 0
    a, b = anchor(w1, w2, F(1, 4), C, lam), anchor(w1, w2, F(3, 4), C, lam)
    assert a['qdot_squared'] != b['qdot_squared']
    pairs.append(dict(weights=[str(w1), str(w2)], C=str(C), Lambda=str(lam),
                      anchors=[a, b], both_root_signs='same square; signed slope reverses'))

hostiles = []
def reject(label, action):
    try:
        action()
    except AssertionError as exc:
        hostiles.append(dict(wrong_claim=label, actual_rejection=str(exc)))
    else:
        raise AssertionError('HOSTILE FALSE PASS: '+label)

def same(actual, expected):
    assert actual == expected, 'exact residual is nonzero'

row = saved['fixtures'][0]
y = list(map(F, row['Y'])); w1, w2 = map(F, row['weights'])
reject('ratio derivative from first angular component only',
       lambda: same(y[1]/w2, F(matched[0]['qdot'])))
negative = next(r for r in saved['fixtures'] if F(r['gap']) < 0)
u0, v0 = map(F, negative['weights'])
kap0 = -120*u0*(u0-v0)/v0
reject('replace signed negative gap by its modulus',
       lambda: same(kap0/(abs(F(negative['gap']))*F(negative['root_D'])),
                    kap0/(F(negative['gap'])*F(negative['root_D']))))
reject('cubic denominator could be constant on an open scalar interval',
       lambda: same(poly.degree(), 0))
reject('constant spatial slope derivative proves dispersion',
       lambda: same(F(1)-F(1) != 0, True))
reject('one saved slope determines a second at fixed C and Lambda',
       lambda: same(pairs[0]['anchors'][0]['qdot_squared'], pairs[0]['anchors'][1]['qdot_squared']))

# Rational closed-orbit property and free Hopf action are different questions.
circle_controls = []
for p, q in [(1, 1), (1, 2), (2, 3)]:
    axis_periods = [F(1, p), F(1, q)]  # units of 2pi, effective integer action
    free = all(z == 1 for z in axis_periods)
    assert free == (p == q == 1)
    circle_controls.append(dict(integer_weights=[p, q], every_orbit_closed=True,
                                axis_primitive_periods_over_2pi=list(map(str, axis_periods)),
                                free_circle_action=free))
reject('unequal rational all-closed action is automatically a free Hopf action',
       lambda: same(circle_controls[1]['free_circle_action'], True))

print(json.dumps(dict(status='PASS_EXACT_ALGEBRA_AND_SAVED_QUANTITY_CONTROLS',
    all_symbolic_checks=['inverse angular metric contraction', 'Killing rotation of scalar gradient',
                         'normalization-independent slope derivative', 'nonconstant cubic for every sector'],
    saved_HB2_recomputed=matched, fixed_data_two_point_anchors=pairs,
    circle_controls=circle_controls, hostile_checks=hostiles,
    versions=dict(python=sys.version, sympy=s.__version__, platform=platform.platform()),
    limits=['No Einstein evolution or orbit solve',
            'No finite check proves the symmetry-extension or time-quantifier argument',
            'No assertion of topology change, particle stability, physical size or scale']), indent=2))
