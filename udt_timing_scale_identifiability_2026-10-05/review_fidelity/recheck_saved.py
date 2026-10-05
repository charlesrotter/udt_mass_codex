"""Independent saved-quantity recomputation; no producer import or execution."""
import ast
import hashlib
import json
from pathlib import Path
import mpmath as mp

root=Path(__file__).resolve().parent
source=root/'independent_checks.py'
# Reuse the exact frozen reviewer implementation without re-running its
# top-level confirmation loop. No producer source is loaded.
tree=ast.parse(source.read_text())
defs=ast.Module(body=[n for n in tree.body if isinstance(n,(ast.Import,ast.ImportFrom,ast.FunctionDef))],type_ignores=[])
scope={}
exec(compile(defs,str(source),'exec'),scope)
branch=scope['branch']
mp.mp.dps=50
saved_path=root.parent/'CONSTRUCTION_RESULT.json'
saved=json.loads(saved_path.read_text())['precisions'][-1]
assert saved['dps']==60
rows=[]
for q in saved['actual_incidences']:
    if mp.mpf(q['R'])!=100000:
        continue
    m,a,H,E,bs,R=(mp.mpf(q[k]) for k in ['m','a','H','E','b_star','R'])
    out=branch(m,a,H,E,bs,R)
    b=out['b']
    omega=mp.sqrt(m/a**3-H**2)
    def s(r,b):return mp.sqrt(1+H*H*b*b-b*b/r**2+2*m*b*b/r**3)
    def v(r):return mp.sqrt(E*E-1+2*m/r+H*H*r*r)
    def angle(r,b):
        A=1/(E+v(r))+v(r)*b*b/(r*r*(1+s(r,b)))
        np=b/(r*A)
        nr=(s(r,b)/(E+v(r))-v(r)*b*b/(r*r*(1+s(r,b))))/A
        return mp.atan2(np,nr)
    I=mp.quad(lambda y:1/mp.sqrt(1+H*H*b*b-b*b*y*y+2*m*b*b*y**3)**3,[1/R,1/a])
    db=-(omega*out['A']/(v(R)*(1-omega*b))+b/(R*R*s(R,b)))/I
    theta=angle(R,b)
    rate=-v(R)*(mp.diff(lambda r:angle(r,b),R)+mp.diff(lambda bb:angle(R,bb),b)*db)/theta
    independent={k:out[k] for k in ['b','A','Z']}
    independent.update(K_length=out['drift'],theta=theta,angular_rate=rate)
    errors={k:abs(value-mp.mpf(q[k]))/max(1,abs(value)) for k,value in independent.items()}
    assert max(errors.values())<mp.mpf('1e-25'),errors
    rows.append(dict(E=E,b_star=bs,R=R,independent=independent,scaled_errors=errors))
assert len(rows)==6
averages=[]
for q in saved['timed_differences']:
    minus,plus=q['minus'],q['plus']
    m,H,E=(mp.mpf(minus[k]) for k in ['m','H','E'])
    lo,hi=mp.mpf(minus['R']),mp.mpf(plus['R'])
    delta=mp.quad(lambda r:1/mp.sqrt(E*E-1+2*m/r+H*H*r*r),[lo,hi])
    timing=mp.log(mp.mpf(plus['Z'])/mp.mpf(minus['Z']))/delta
    angular=-mp.log(abs(mp.mpf(plus['theta'])/mp.mpf(minus['theta'])))/delta
    vals=dict(delta_ell=delta,time_averaged_K=timing,time_averaged_angular=angular)
    errors={k:abs(v-mp.mpf(q[k]))/max(1,abs(v)) for k,v in vals.items()}
    assert max(errors.values())<mp.mpf('1e-25'),errors
    averages.append(dict(step_fraction=q['step_fraction'],independent=vals,scaled_errors=errors))
assert len(averages)==2
print(json.dumps(dict(status='PASS',finite_solves=6,saved_average_controls=2,dps=mp.mp.dps,
    source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
    saved_result_sha256=hashlib.sha256(saved_path.read_bytes()).hexdigest(),
    rows=rows,averages=averages),indent=2,default=lambda v:mp.nstr(v,45)))
