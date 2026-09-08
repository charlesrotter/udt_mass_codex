"""Declared HB2 exploratory exact first-jet probe, not a frozen proof.

Reuse the fully inspected G337 coordinate time-dual curvature engine. New
fixtures and tensor contractions; shared implementation is explicit. No solve.
"""
import hashlib
import importlib.util
import json
from fractions import Fraction as F
from pathlib import Path

root = Path(__file__).resolve().parents[2]
source = root / 'udt_g337_double_silent_third_normal_ownership_2026-09-03/derive_double_silent_third_response.py'
assert hashlib.sha256(source.read_bytes()).hexdigest() == 'd5dfe3161b7eebe1754f58313ce2c3030d5299048dead333d0d598aaf979b891'
spec = importlib.util.spec_from_file_location('hb2_g337_engine', source)
engine = importlib.util.module_from_spec(spec)
spec.loader.exec_module(engine)
J, T = engine.Jet2, engine.TimeDual

def mv(a, v):
    return [sum(a[i][j]*v[j] for j in range(3)) for i in range(3)]
def dot(a,b):
    return sum(x*y for x,y in zip(a,b))
def mat(a):
    return [[v.v for v in row] for row in a]

def probe(w1,w2,x0,C,D):
    g,eta,R = engine.weighted_fields(x0,w1,w2)
    Lambda = R.v/2+C*C-D*D/4
    b = D-C
    bp = R.d1/D
    bpp = (R.d2-bp*bp)/D
    bj=J(b,bp,bpp)
    K=[[(C-bj)/2*g[i][j]+bj*eta[i]*eta[j] for j in range(3)] for i in range(3)]
    dual=[[T(g[i][j],-2*K[i][j]) for j in range(3)] for i in range(3)]
    inv,ric=engine.ricci_of_dual_metric(dual)
    endo=engine.mm(inv,ric)
    gv=mat(g); gi=[[a.a.v for a in row] for row in inv]
    xi=[F(0),w1,w2]; et=[a.v for a in eta]
    rd=[[a.b.v for a in row] for row in ric]
    adot=[[a.b.v for a in row] for row in endo]
    av=mv(adot,xi); off=[av[i]-dot(et,av)*xi[i] for i in range(3)]
    conn=[[[sum(gi[k][l]*((g[l][j].d1 if i==0 else 0)
                           +(g[l][i].d1 if j==0 else 0)
                           -(g[i][j].d1 if l==0 else 0)) for l in range(3))/2
             for j in range(3)] for i in range(3)] for k in range(3)]
    dxi=[[sum(conn[k][i][j]*xi[j] for j in range(3)) for i in range(3)] for k in range(3)]
    gradb=[gi[i][0]*bp for i in range(3)]
    rot=mv(dxi,gradb)
    residual=[off[i]-F(5,2)*rot[i] for i in range(3)]
    directR=sum(gi[i][j]*ric[i][j].a.v for i in range(3) for j in range(3))
    delta=3-R.v/2
    return dict(weights=[str(w1),str(w2)],x=str(x0),C=str(C),D=str(D),
        Lambda=str(Lambda),b=str(b),R=str(R.v),direct_R=str(directR),gap=str(delta),
        off=[str(z) for z in off],rot_grad_b=[str(z) for z in rot],
        proposed_five_halves_residual=[str(z) for z in residual],
        vertical_adot=str(dot(et,av)),
        vertical_without_inverse_variation=str(dot(et,mv(engine.mm(gi,rd),xi))))

results=[probe(w1,w2,x,C,D)
    for w1,w2,x in [(F(1,4),F(1,2),F(1,3)),(F(2),F(3,2),F(2,5)),(F(1,2),F(1,2),F(1,4))]
    for C in (F(-3),F(3)) for D in (F(-8),F(8))]
print(json.dumps(dict(kind='EXPLORATORY_EXACT_COORDINATE_FIRST_JET_NOT_PROOF',
    method='shared frozen G337 time-dual engine; new geometric query',fixtures=results),indent=2))
