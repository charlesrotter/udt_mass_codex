"""HB2 exact coordinate regressions, not an independent proof.

Reuses the frozen, inspected G337 time-dual curvature engine. Separately
contracted tensors test the candidate; actual hostile perturbations must fail.
No metric development is solved, and no finite test certifies a whole family.
"""
import hashlib
import importlib.util
import json
from fractions import Fraction as F
from pathlib import Path

root = Path(__file__).resolve().parents[2]
source = root / 'udt_g337_double_silent_third_normal_ownership_2026-09-03/derive_double_silent_third_response.py'
source_sha = hashlib.sha256(source.read_bytes()).hexdigest()
assert source_sha == 'd5dfe3161b7eebe1754f58313ce2c3030d5299048dead333d0d598aaf979b891'
spec = importlib.util.spec_from_file_location('hb2_g337_engine', source)
engine = importlib.util.module_from_spec(spec)
spec.loader.exec_module(engine)
J, T = engine.Jet2, engine.TimeDual

def mv(a, v):
    return [sum(a[i][j]*v[j] for j in range(3)) for i in range(3)]

def dot(a, b):
    return sum(x*y for x, y in zip(a, b))

def outer(a, b):
    return [[a[i]*b[j] for j in range(3)] for i in range(3)]

def check_domain(w1, w2, x, C, D):
    assert w1 > 0 and w2 > 0 and 0 < x < 1 and D != 0
    _, _, R = engine.weighted_fields(x, w1, w2)
    lam = R.v/2+C*C-D*D/4
    ends = [16*w1-8*w2-2, -8*w1+16*w2-2]
    assert (6-ends[0])*(6-ends[1]) > 0, 'global simple-gap condition'
    assert min(ends)+2*C*C-2*lam > 0, 'global strict-root condition'
    return lam

def fixture(w1, w2, x, C, D, mutation=None):
    lam = check_domain(w1, w2, x, C, D)
    g, eta, R = engine.weighted_fields(x, w1, w2)
    b, bp = D-C, R.d1/D
    bpp = (R.d2-bp*bp)/D
    bj = J(b, bp, bpp)
    if mutation == 'drop_spatial_b_derivatives':
        bj = J(b)
    if mutation == 'wrong_root_derivative':
        bj = J(b, -bp, bpp)
    K = [[(C-bj)/2*g[i][j]+bj*eta[i]*eta[j] for j in range(3)] for i in range(3)]
    dual = [[T(g[i][j], -2*K[i][j]) for j in range(3)] for i in range(3)]
    inv, ric = engine.ricci_of_dual_metric(dual)
    endo = engine.mm(inv, ric)
    gv = [[v.v for v in row] for row in g]
    gi = [[v.a.v for v in row] for row in inv]
    xi, et = [F(0), w1, w2], [v.v for v in eta]
    P = outer(xi, et)
    assert dot(et, xi) == 1 and mv(gv, xi) == et
    R0 = sum(endo[i][i].a.v for i in range(3))
    assert R0 == R.v
    delta, lh = (6-R.v)/2, (R.v-2)/2
    B = [[v.a.v for v in row] for row in endo]
    assert B == [[lh*(i == j)+delta*P[i][j] for j in range(3)] for i in range(3)]
    conn = [[[sum(gi[k][l]*((g[l][j].d1 if i == 0 else 0)
                              +(g[l][i].d1 if j == 0 else 0)
                              -(g[i][j].d1 if l == 0 else 0)) for l in range(3))/2
              for j in range(3)] for i in range(3)] for k in range(3)]
    A = [[sum(conn[k][i][j]*xi[j] for j in range(3)) for i in range(3)] for k in range(3)]
    gA = engine.mm(gv, A)
    assert all(gA[i][j]+gA[j][i] == 0 for i in range(3) for j in range(3))
    assert engine.mm(A, A) == [[P[i][j]-(i == j) for j in range(3)] for i in range(3)]
    Kg = engine.mm(gi, [[v.v for v in row] for row in K])
    trK = sum(Kg[i][i] for i in range(3))
    assert R0+trK*trK-sum(Kg[i][j]*Kg[j][i] for i in range(3) for j in range(3)) == 2*lam
    gij = [[v.a for v in row] for row in inv]
    Kgj = engine.mm(gij, K)
    tj = sum(Kgj[i][i] for i in range(3))
    Kup = engine.mm(Kgj, gij)
    mom = [[Kup[i][j]-tj*gij[i][j] for j in range(3)] for i in range(3)]
    divmom = [mom[i][0].d1+sum(conn[i][j][k]*mom[k][j].v+conn[j][j][k]*mom[i][k].v
                for j in range(3) for k in range(3)) for i in range(3)]
    assert divmom == [0, 0, 0], 'momentum constraint'
    Bd = [[v.b.v for v in row] for row in endo]
    raising = engine.mm(gi, [[v.b.v for v in row] for row in ric])
    correction = engine.mm(Kg, B)
    assert all(Bd[i][j] == raising[i][j]+2*correction[i][j] for i in range(3) for j in range(3))
    if mutation == 'omit_inverse_variation':
        Bd = raising
    # The transverse projection alone cannot detect omitted index variation.
    assert dot(et, mv(Bd, xi))-dot(et, mv(raising, xi)) == 2*D, 'full ambient variation'
    vv = mv(Bd, xi)
    off = [vv[i]-dot(et, vv)*xi[i] for i in range(3)]
    rot = mv(A, [gi[i][0]*bp for i in range(3)])
    coefficient = F(3, 2) if mutation == 'wrong_coefficient' else F(5, 2)
    assert off == [coefficient*v for v in rot], 'transverse Ricci variation'
    denominator = 1 if mutation == 'omit_gap' else delta
    Y = [coefficient*v/denominator for v in rot]
    assert [delta*y for y in Y] == off, 'spectral-gap division'
    yf = mv(gv, Y)
    Pd = [[Y[i]*et[j]+xi[i]*yf[j] for j in range(3)] for i in range(3)]
    assert all(sum(Pd[i][k]*P[k][j]+P[i][k]*Pd[k][j] for k in range(3)) == Pd[i][j]
               for i in range(3) for j in range(3)), 'differentiated projector identity'
    hs = sum(Pd[i][j]*Pd[j][i] for i in range(3) for j in range(3))
    gradR2 = gi[0][0]*R.d1*R.d1
    assert hs == F(25, 2)*gradR2/(delta*delta*D*D)
    assert (hs > 0) == (w1 != w2)
    return dict(weights=[str(w1), str(w2)], x=str(x), C=str(C), root_D=str(D),
                Lambda=str(lam), gap=str(delta), Y=list(map(str, Y)),
                projector_HS_squared=str(hs), full_raising_correction=str(2*D))

fixtures = [fixture(w1, w2, x, C, D)
            for w1, w2, x in [(F(1, 4), F(1, 2), F(1, 3)),
                              (F(2), F(7, 4), F(2, 5)),
                              (F(1, 2), F(1, 2), F(1, 4))]
            for C in (F(-3), F(3)) for D in (F(-8), F(8))]
hostiles = []

def rejected(label, action):
    try:
        action()
    except AssertionError as exc:
        hostiles.append(dict(mutation=label, actual_rejection=str(exc)))
    else:
        raise AssertionError('HOSTILE FALSE PASS: '+label)

for mutation in ['drop_spatial_b_derivatives', 'wrong_root_derivative',
                 'omit_inverse_variation', 'wrong_coefficient', 'omit_gap']:
    rejected(mutation, lambda m=mutation: fixture(F(1, 4), F(1, 2), F(1, 3), F(3), F(8), m))
for label, w1, w2, D in [('endpoint_gap_closure', F(2), F(3, 2), F(8)),
                         ('round_no_simple_line', F(1), F(1), F(8)),
                         ('root_boundary', F(1, 4), F(1, 2), F(0)),
                         ('interior_root_not_global', F(1, 4), F(1, 2), F(1, 4))]:
    rejected(label, lambda a=w1, b=w2, d=D: check_domain(a, b, F(1, 3), F(3), d))
print(json.dumps(dict(status='PASS_EXACT_REGRESSION_NOT_GENERAL_PROOF',
    reused_engine_sha256=source_sha, fixtures=fixtures, hostile_checks=hostiles,
    limits=['shared G337 engine is not independent review',
            'finite exact fixtures do not establish the analytic family claim',
            'no time evolution, orbit-closure, Hopfion-energy or stability calculation']), indent=2))
