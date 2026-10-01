"""Recover curvature from saved parent connection; no parent code import."""
from pathlib import Path
import hashlib,json,platform
import sympy as s
base=Path(__file__).resolve().parent.parent
saved=base/'checks/curvature_repaired.stdout'
prior=base/'fidelity/EXACT_CONTROLS.json'
obj=json.loads(saved.read_text()); independent=json.loads(prior.read_text())
t,r,theta,phi=s.symbols('t r theta phi',real=True)
mu,kappa=s.symbols('mu kappa',real=True)
lookup={str(z):z for z in (t,r,theta,phi,mu,kappa)}
expr=lambda v:s.sympify(v,locals=lookup)
coords=[t,r,theta,phi]
g=[expr(v) for v in obj['metric_diagonal']]
conn={tuple(map(int,key.split(','))):expr(v) for key,v in obj['christoffels'].items()}
stored={tuple(map(int,key.split(','))):expr(v) for key,v in obj['orthonormal_curvature'].items()}
G=lambda a,c,d:conn.get((a,c,d),s.S.Zero)
f=1-2*mu/r-kappa*r*r
frame=[1/s.sqrt(f),s.sqrt(f),1/r,1/(r*s.sin(theta))]
residuals=[]
def equal(label,v):
    v=s.simplify(s.trigsimp(s.expand_trig(v)))
    residuals.append({'name':label,'residual':str(v),'pass':v==0})
    assert v==0,(label,v)
for j,ref in enumerate([-f,1/f,r*r,r*r*s.sin(theta)**2]):equal('saved_metric_'+str(j),g[j]-ref)
rec={}
for a in range(4):
  for b in range(4):
    for c in range(4):
      for d in range(4):
        coordinate=s.diff(G(d,b,c),coords[a])-s.diff(G(d,a,c),coords[b])+sum(G(d,a,h)*G(h,b,c)-G(d,b,h)*G(h,a,c) for h in range(4))
        val=s.simplify(s.trigsimp(s.expand_trig(g[d]*coordinate*frame[a]*frame[b]*frame[c]*frame[d])))
        rec[a,b,c,d]=val
        equal('saved_curvature_'+str((a,b,c,d)),val-stored.get((a,b,c,d),0))
source_lookup={**lookup,'m':mu,'k':kappa}
for key,val in independent['sections'].items():
    a,b=map(int,key)
    equal('source_first_section_'+key,rec[a,b,b,a]-s.sympify(val,locals=source_lookup))
eta=[-1,1,1,1]
Ric=s.Matrix(4,4,lambda a,b:s.simplify(sum(eta[i]*rec[i,a,b,i] for i in range(4))))
scalar=s.simplify(sum(eta[i]*Ric[i,i] for i in range(4)))
equal('recovered_scalar',scalar-12*kappa)
equal('recovered_anisotropy',rec[1,0,0,1]-rec[2,0,0,2]+3*mu/r**3)
# Exact algebraic check on the preserved actual failure; no execution of mutable diagnostic.
diag=json.loads((base/'checks/curvature_diagnostic.stdout').read_text())
equal('preserved_failure_is_zero',expr(diag['original_component']))
# Recover one load-bearing numerical event directly with rationals.
point={mu:s.Rational(1,50),r:s.Integer(1),kappa:s.Rational(1,25)}
actual=[s.factor(rec[i,0,0,i].subs(point)) for i in (1,2,3)]
reference=[s.factor(rec[i,0,0,i].subs(kappa,0).subs(point)) for i in (1,2,3)]
delta=[s.factor(x-y) for x,y in zip(actual,reference)]
assert delta==[-s.Rational(1,25)]*3
out={'status':'PASS','python':platform.python_version(),'sympy':s.__version__,
     'method':'Saved original connection to all 256 curvature entries; no parent code import',
     'checks':residuals,'assertion_count':len(residuals)+1,
     'input_sha256':{str(p.relative_to(base)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [saved,prior,base/'checks/curvature_diagnostic.stdout']},
     'event_actual_tides':list(map(str,actual)),'event_reference_tides':list(map(str,reference)),
     'event_delta_tides':list(map(str,delta)),'event_outgoing_delta_coefficient':'1/50',
     'event_return_delta_coefficient':'3/50'}
with (base/'fidelity/SAVED_RECOVERY.json').open('x') as fh:json.dump(out,fh,indent=2);fh.write('\n')
print(json.dumps({key:out[key] for key in ('status','assertion_count','event_actual_tides','event_reference_tides','event_delta_tides','event_outgoing_delta_coefficient','event_return_delta_coefficient')}))
