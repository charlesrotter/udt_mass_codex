"""Post-exposure four-dimensional tensor check of Weyl frame invariance.

Uses the reviewer source-first metric tensor engine, not author code. Actual
Lorentz-tensor transformation precedes extraction of electric/magnetic parts;
this differs from the author's direct complex-orthogonal matrix example.
"""
import importlib.util
import itertools
import json
import sympy as s

spec=importlib.util.spec_from_file_location('source_engine',
    'udt_localized_evolution_followup_2026-09-09/review/source_first_check.py')
m=importlib.util.module_from_spec(spec)
try:
    spec.loader.exec_module(m)
except AssertionError:
    assert hasattr(m,'kretsch')  # preserved normalization issue; tensors exist
else:
    raise AssertionError('Expected source-first retained failure was absent')

point={m.t:1,m.q:s.Rational(6,5)}
R={key:s.factor((m.metric[key[0]]*value).subs(point))
   for key,value in m.curv.items() if value!=0}
eta=s.diag(-1,1,1,1)
# Supplied rational proper boost in direction y: gamma=5/3, gamma*v=4/3.
L=s.Matrix([[s.Rational(5,3),0,s.Rational(4,3),0],
            [0,1,0,0],
            [s.Rational(4,3),0,s.Rational(5,3),0],
            [0,0,0,1]])
assert L.T*eta*L==eta and L.det()==1 and L[0,0]>0
Rp={}
for out in itertools.product(range(4),repeat=4):
    Rp[out]=s.factor(sum(value*s.prod(L[key[j],out[j]] for j in range(4))
                        for key,value in R.items()))
E=s.Matrix(3,3,lambda i,j:Rp[i+1,0,j+1,0])
B=s.Matrix(3,3,lambda i,j:s.Rational(1,2)*sum(
    s.LeviCivita(i,k,l)*Rp[k+1,l+1,j+1,0]
    for k,l in itertools.product(range(3),repeat=2)))
assert E==E.T and B==B.T and s.trace(E)==0 and s.trace(B)==0
Q=E+s.I*B
Q0=s.Matrix(m.electric.subs(point))

def shape(matrix):
    return s.factor(1-6*s.trace(matrix**3)**2/s.trace(matrix**2)**3)

assert s.trace(Q**2)==s.trace(Q0**2)
assert s.trace(Q**3)==s.trace(Q0**3)
assert shape(Q)==s.Rational(18496,753571)
assert shape(E)!=shape(Q)
assert B!=s.zeros(3)
print(json.dumps({
 'route':'full rank-four Lorentz transformation, then E and B extraction',
 'boost':str(L),'electric_boosted':str(E),'magnetic_boosted':str(B),
 'full_Weyl_shape':str(shape(Q)),
 'electric_only_shape':str(shape(E)),
 'original_Weyl_shape':str(shape(Q0)),
 'status':'PASS',
 'limitation':'One exact boost is a counterexample to electric-only invariance; universal full-Weyl invariance follows from tensor/operator similarity.'
},indent=2))
