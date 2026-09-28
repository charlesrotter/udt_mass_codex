#!/usr/bin/env python3
"""Additional exact pairing control suggested by source-first reviewer."""
import json
import sympy as s
r=s.symbols('r',positive=True)
C=(r+1/r)/2;S=(r-1/r)/2
g=s.diag(-1,1,1,1);U=s.Matrix([C,S,0,0]);n=s.Matrix([S,C,0,0])
P=(g*U)*(g*U).T/2;H=2*((g*U)*(g*U).T+(g*n)*(g*n).T)
facts={'unit_U':((U.T*g*U)[0],-1),'unit_n':((n.T*g*n)[0],1),
       'orthogonal':((U.T*g*n)[0],0),'reciprocal_trace':(s.trace(g*H),0),
       'covariant_variation_pairing':(s.trace(g*P*g*H),1),
       'inverse_variation_pairing':(s.trace(g*(-P)*g*H),-1)}
for name,(actual,expected) in facts.items():assert s.simplify(actual-expected)==0,name
print(json.dumps({'status':'PASS','checks':len(facts),'sympy':s.__version__,
     'results':{name:str(s.simplify(actual)) for name,(actual,_) in facts.items()},
     'scope':'orthonormal-pair contraction and sign control; not physical response admission'}))
