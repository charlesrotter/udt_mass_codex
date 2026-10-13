"""Exact original-metric controls; no scientific premise is selected here."""
import hashlib
import json
import platform
from pathlib import Path

import sympy as s

t, x, y, z = s.symbols('t x y z', real=True)
coords = (t, x, y, z)
a = s.Function('a')(t)
g = s.diag(-1, a*a, a*a, a*a)
inv = g.inv()
Gamma = [[[s.simplify(sum(inv[i,j]*(s.diff(g[j,k],coords[l])
    +s.diff(g[j,l],coords[k])-s.diff(g[k,l],coords[j]))/2
    for j in range(4))) for l in range(4)] for k in range(4)] for i in range(4)]
Ric = s.Matrix(4,4,lambda b,d:s.simplify(sum(
    s.diff(Gamma[c][b][d],coords[c])-s.diff(Gamma[c][b][c],coords[d])
    +sum(Gamma[c][c][e]*Gamma[e][b][d]-Gamma[c][d][e]*Gamma[e][b][c]
         for e in range(4)) for c in range(4))))
R = s.simplify(sum(inv[i,j]*Ric[i,j] for i in range(4) for j in range(4)))
S = s.simplify(Ric-R*g/4)
divS=[]
for b in range(4):
    divS.append(s.simplify(sum(inv[i,j]*(s.diff(S[i,b],coords[j])
       -sum(Gamma[c][j][i]*S[c,b]+Gamma[c][j][b]*S[i,c] for c in range(4)))
       for i in range(4) for j in range(4))))
residual=[s.simplify(divS[b]-s.diff(R,coords[b])/4) for b in range(4)]
assert residual == [0]*4
M = s.simplify(-Ric[0,0]/3)
# k=U+e_1, with U=partial_t and e_1=a^-1 partial_x; all six agree in FLRW.
N = s.simplify(Ric[0,0]+Ric[1,1]/a**2)
assert s.simplify(M+N/4-R/12)==0

def substitute(expr, aa):
    expr=expr.subs({s.diff(a,t,3):s.diff(aa,t,3),
                   s.diff(a,t,2):s.diff(aa,t,2),s.diff(a,t):s.diff(aa,t),a:aa})
    return s.simplify(s.expand(expr))

dust=s.Pow(t,s.Rational(2,3))
dust_out={name:substitute(expr,dust) for name,expr in
    [('R',R),('K',R/12),('M',M),('N',N),('divS_t',divS[0])]}
assert s.simplify(dust_out['R']-s.Rational(4,3)/t**2)==0
assert s.simplify(dust_out['K']-s.Rational(1,9)/t**2)==0
assert s.simplify(dust_out['M']+s.Rational(2,9)/t**2)==0
assert s.simplify(dust_out['N']-s.Rational(4,3)/t**2)==0
Einstein=s.simplify(Ric-R*g/2)
dust_G=Einstein.applyfunc(lambda e:substitute(e,dust))
assert dust_G==s.diag(s.Rational(4,3)/t**2,0,0,0)

constantR=s.sqrt(s.sinh(2*t))
constantR_out={name:substitute(expr,constantR) for name,expr in
    [('R',R),('K',R/12),('S00',S[0,0]),('divS_t',divS[0])]}
assert s.simplify(constantR_out['R']-12)==0
assert s.simplify(constantR_out['S00']-3/s.sinh(2*t)**2)==0
assert constantR_out['divS_t']==0

sources=['UDT_DEVELOPMENT.md',
 'udt_positional_selection_whiteboard_2026-10-01/INITIAL_CANDIDATE.md',
 'udt_positional_selection_whiteboard_2026-10-01/REPAIR.md',
 'udt_goal_research_campaign_2026-10-13/researcher_b/CANDIDATE.md',
 'udt_positional_curvature_connection_2026-10-01/INITIAL_DERIVATION.md',
 'udt_clock_optical_physical_connection_2026-10-13/researcher_a/CHECK_PLAN.md',
 __file__]
out={'scope':'Exact symbolic original-metric FLRW controls; no finite observational or native selection claim',
 'versions':{'python':platform.python_version(),'sympy':s.__version__},
 'general':{'R':str(R),'M':str(M),'N':str(N),'divS':[str(v) for v in divS],
 'bianchi_residual':[str(v) for v in residual]},
 'dust':{k:str(v) for k,v in dust_out.items()},
 'dust_Einstein_tensor':str(dust_G),
 'constant_scalar_non_Einstein':{k:str(v) for k,v in constantR_out.items()},
 'source_sha256':{p:hashlib.sha256(Path(p).read_bytes()).hexdigest() for p in sources},
 'status':'PASS'}
dest=Path(__file__).parent/'REGIONAL_CHECK_RESULT.json'
with dest.open('x') as f:json.dump(out,f,indent=2);f.write('\n')
print(json.dumps(out,indent=2))
