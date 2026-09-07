"""Intrinsic constraints built only from independent reviewer metric data."""
import contextlib
import io
import itertools
import json
import pathlib
import runpy
import sympy as s

with contextlib.redirect_stdout(io.StringIO()):
    data=runpy.run_path(str(pathlib.Path(__file__).with_name('source_first_metric.py')))
gamma=data['gamma']; K=data['K']; coords=(data['u'],data['x'],data['y'])
gi=gamma.inv(); ids=range(3); clean=lambda q:s.factor(q)
Gamma=[s.Matrix(3,3,lambda d,b:clean(sum(gi[d,h]*(s.diff(gamma[h,b],coords[a])+s.diff(gamma[h,a],coords[b])-s.diff(gamma[a,b],coords[h])) for h in ids)/2)) for a in ids]
F={(a,b):(Gamma[b].diff(coords[a])-Gamma[a].diff(coords[b])+Gamma[a]*Gamma[b]-Gamma[b]*Gamma[a]).applyfunc(clean) for a,b in itertools.product(ids,repeat=2)}
Ric=s.Matrix(3,3,lambda b,c:clean(sum(F[a,b][a,c] for a in ids)))
scalar=clean(s.trace(gi*Ric)); mixed=(gi*K).applyfunc(clean); tr=clean(s.trace(mixed))
ham=clean(scalar+tr*tr-s.trace(mixed*mixed))
P=(K-tr*gamma).applyfunc(clean)
mom=[]
for i in ids:
    value=0
    for j,k in itertools.product(ids,repeat=2):
        cov=s.diff(P[i,j],coords[k])-sum(Gamma[k][a,i]*P[a,j]+Gamma[k][a,j]*P[i,a] for a in ids)
        value+=gi[j,k]*cov
    mom.append(clean(value))
assert ham==0 and mom==[0,0,0]
print(json.dumps(dict(independent_intrinsic_H=str(ham),independent_intrinsic_M=list(map(str,mom)),intrinsic_scalar=str(scalar),trace_K=str(tr),full_open_patch=True),indent=2))
