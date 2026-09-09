"""Finite Lorentz frame product differentiation; independent of author code."""
import contextlib
import io
import itertools
import json
import pathlib
import runpy
import sys
import sympy as s

with contextlib.redirect_stdout(io.StringIO()):
    scope=runpy.run_path(str(pathlib.Path(__file__).with_name('source_first_check.py')))
Q=scope['tensor'](scope['from_electric']([1,-1,0]))
t=s.symbols('t',real=True)
eta=s.diag(-1,1,1,1)
rotation=s.eye(4)
rotation[1,1]=rotation[2,2]=(1-t*t)/(1+t*t)
rotation[1,2]=2*t/(1+t*t)
rotation[2,1]=-2*t/(1+t*t)
boost=s.eye(4)
boost[0,0]=boost[1,1]=(1+t*t)/(1-t*t)
boost[0,1]=boost[1,0]=2*t/(1-t*t)
mutant=sys.argv[1] if len(sys.argv)>1 else 'baseline'
cases=[]
for label,L in [('rotation12',rotation),('boost01',boost)]:
    assert (L*eta*L.T-eta).applyfunc(s.simplify)==s.zeros(4)
    assert L.subs(t,0)==s.eye(4)
    omega=L.diff(t).subs(t,0)
    transformed={}
    for key in Q:
        supports=[[r for r in range(4) if L[a,r]!=0] for a in key]
        value=sum(s.prod(L[a,r] for a,r in zip(key,replaced))*Q[replaced]
                  for replaced in itertools.product(*supports))
        transformed[key]=s.simplify(s.diff(value,t).subs(t,0))
    correction={}
    for key in Q:
        total=0
        for slot in range(3 if mutant=='omit_last_slot' else 4):
            for r in range(4):
                repl=list(key)
                repl[slot]=r
                total+=omega[key[slot],r]*Q[tuple(repl)]
        correction[key]=total
    if mutant=='wrong_sign':
        correction={key:-value for key,value in correction.items()}
    residual={str(key):str(transformed[key]-correction[key])
              for key in Q if transformed[key]!=correction[key]}
    cases.append(dict(case=label,nonzero_direct_derivative_components=sum(v!=0 for v in transformed.values()),
                      residual=residual))
    if residual:
        print(json.dumps(dict(status='FAIL',mutant=mutant,cases=cases),indent=2))
        raise AssertionError('finite_Lorentz_product_derivative_matches_full_connection_correction')
print(json.dumps(dict(status='PASS',mutant=mutant,cases=cases,
    limits='finite tensor covariance identity, not an actual Einstein development',
    exposure='post-source-first seal, author proof/code/results still unexposed'),indent=2))
