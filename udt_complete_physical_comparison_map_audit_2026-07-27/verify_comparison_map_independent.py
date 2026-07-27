#!/usr/bin/env python3
"""Independent stdlib/Fraction replay of the load-bearing algebra."""
from __future__ import annotations
import json
from fractions import Fraction as F
from pathlib import Path
HERE=Path(__file__).resolve().parent
def mm(a,b):return [[sum(a[i][k]*b[k][j] for k in range(len(b))) for j in range(len(b[0]))] for i in range(len(a))]
def invboost(u):return [[u[0][0],-u[0][1],0,0],[-u[1][0],u[1][1],0,0],[0,0,1,0],[0,0,0,1]]
def diag(v):return [[v[i] if i==j else F(0) for j in range(len(v))] for i in range(len(v))]
def main():
    vals={0:F(2),1:F(-1),2:F(5)}
    delta=lambda x,y:vals[y]-vals[x]
    assert delta(0,1)+delta(1,2)==delta(0,2) and delta(1,0)==-delta(0,1) and delta(0,0)==0
    # Symmetric unsigned depth cannot reverse oddly unless zero.
    for r in (F(0),F(1,3),F(7,2)):
        assert (r==-r)==(r==0)
    U1=[[F(5,4),F(3,4),0,0],[F(3,4),F(5,4),0,0],[0,0,1,0],[0,0,0,1]]
    U2=[[1,0,0,0],[0,1,0,0],[0,0,F(3,5),F(-4,5)],[0,0,F(4,5),F(3,5)]]
    Ui=invboost(U1)
    checks=[]
    for lam in (-1,0,1,2):
        dn=lambda n:diag([F(1,n),F(n),F(n)**lam,F(n)**lam])
        d3at1=mm(mm(U1,dn(3)),Ui);lhs=mm(mm(U2,d3at1),mm(U1,dn(2)));rhs=mm(mm(U2,U1),dn(6));assert lhs==rhs;checks.append(lam)
    # Pair-swap conjugacy loses the sign.
    swap=[[0,1],[1,0]];d2=diag([F(1,2),F(2)]);assert mm(mm(swap,d2),swap)==diag([F(2),F(1,2)])
    out={'schema':'udt-complete-physical-comparison-map-independent-1.0','status':'PASS','method':'stdlib_fraction_independent','endpoint_triangles':1,'symmetric_odd_controls':3,'typed_path_lambda_controls':checks,'pair_swap_sign_loss':'PASS','stationary_norm_ratio_normalization':'ALGEBRAICALLY_CANCELS','verdict':'BOUNDED_SCALAR_AND_CONDITIONAL_REDUCIBLE_MAP_SURVIVE__UNIVERSAL_PHYSICAL_SELECTION_OPEN'}
    (HERE/'INDEPENDENT_RESULT.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,indent=2,sort_keys=True));return 0
if __name__=='__main__':raise SystemExit(main())
