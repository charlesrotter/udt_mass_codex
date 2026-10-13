"""Exposed independent FAC1 arithmetic and contraction audit; no author imports."""
import hashlib
import itertools
import json
import math
from pathlib import Path
import platform
import sympy as sp

BASE=Path(__file__).resolve().parents[2]
OWN=Path(__file__).resolve().parent
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()

freeze=json.loads((BASE/'researcher_a/FREEZE_01.json').read_text())
for name,digest in freeze['files'].items():
    assert sha(BASE/'researcher_a'/name)==digest,name
initial=json.loads((OWN/'SOURCE_FIRST_PINS.json').read_text())
for name,digest in initial['sha256'].items():
    assert sha(name)==digest,name

def partial_pairings(slots):
    # An unpaired slot carries U; a pair carries the inverse metric.
    if not slots:
        yield (),()
        return
    x,*rest=slots
    for us,pairs in partial_pairings(rest):
        yield (x,)+us,pairs
    for i,y in enumerate(rest):
        leftover=rest[:i]+rest[i+1:]
        for us,pairs in partial_pairings(leftover):
            yield us,((x,y),)+pairs

contractions={}
for order in (0,1,2):
    counts={'two_U_in_antisymmetric_pair':0,'Weyl_trace':0,'inner_divergence':0}
    failures=[]
    for us,pairs in partial_pairings(list(range(4+order))):
        if (0 in us and 1 in us) or (2 in us and 3 in us):
            counts['two_U_in_antisymmetric_pair']+=1
        elif any(a<4 and b<4 for a,b in pairs):
            counts['Weyl_trace']+=1
        elif order and any((a==3+order and b<4) or (b==3+order and a<4) for a,b in pairs):
            counts['inner_divergence']+=1
        else:
            failures.append((us,pairs))
    assert not failures,(order,failures)
    contractions[str(order)]={'classified':counts,'total':sum(counts.values()),'unclassified':failures}

z,X,D,T=sp.symbols('z X D T')
pw=json.loads((BASE/'researcher_a/formal_plane_wave_01_result.json').read_text())
own=json.loads((OWN/'source_first_plane_wave_result.json').read_text())
for theirs,ours in [('forward','plus'),('reverse','minus')]:
    for key in ('log_L2','log_L4'):
        a=sp.sympify(pw[theirs][key],locals={'X':X,'Z':z})
        b=sp.sympify(own['clock_series'][ours][key],locals={'D':D,'T':T,'z':z})
        assert sp.expand(a-b.subs({D:2*X+z*z-1,T:1-z*z}))==0

kas=json.loads((BASE/'researcher_a/formal_kasner_01_result.json').read_text())
mu=sp.symbols('mu')
kas_means={}
for branch in ('forward','reverse'):
    values=[]
    for c in kas[branch]['log_ratio']:
        poly=sp.sympify(c,locals={'z':mu**2})
        values.append(sp.factor(sp.integrate(poly,(mu,0,1))))
    assert [str(v) for v in values]==kas[branch]['spherical_mean']
    kas_means[branch]=[str(v) for v in values]
a,b=sp.symbols('a b')
coefs=sp.solve([a*sp.Rational(8,27)-sp.Rational(4,1215),
               (a+b)/2-sp.Rational(1,720)],(a,b))
assert coefs=={a:sp.Rational(1,90),b:-sp.Rational(1,120)}

raw=json.loads((BASE/'researcher_b/vacuum_fine_data.json').read_text())
exponents=(-1/3,2/3,2/3)
recomputed=[]
max_point_error=0.
for record in raw['results']:
    weights=record['angular_weights']
    assert abs(math.fsum(weights)-1)<1e-14
    plus=[];minus=[]
    for ray in record['angular_records']:
        P=ray['receiver_momenta']; qp=ray['outgoing_q']; qm=ray['reverse_q']
        def inva(t):return [t**(-2*p) for p in exponents]
        def W(q,t):return math.sqrt(math.fsum(qi*qi*ai for qi,ai in zip(q,inva(t))))
        def gamma(t):return math.sqrt(1+math.fsum(Pi*Pi*ai for Pi,ai in zip(P,inva(t))))
        def omega(q,t):return W(q,t)*gamma(t)-math.fsum(qi*Pi*ai for qi,Pi,ai in zip(q,P,inva(t)))
        lp=math.log(W(qp,1)/omega(qp,ray['outgoing_t']))
        lm=math.log(omega(qm,ray['preparation_t'])/W(qm,ray['reverse_t']))
        max_point_error=max(max_point_error,abs(lp-ray['log_plus']),abs(lm-ray['log_minus']))
        plus.append(lp);minus.append(lm)
    mp=math.fsum(w*v for w,v in zip(weights,plus))
    mm=math.fsum(w*v for w,v in zip(weights,minus))
    assert abs(mp-record['M_plus'])<5e-15
    assert abs(mm-record['M_minus'])<5e-15
    recomputed.append({'L':record['L'],'M_plus':mp,'M_minus':mm,
        'saved_difference_plus':mp-record['M_plus'],'saved_difference_minus':mm-record['M_minus'],
        'coefficient_plus':mp/record['L']**4,'coefficient_minus':mm/record['L']**4})
assert max_point_error<5e-15
inputs=['INVARIANT_ROUTE_CANDIDATE.md','RECOVERY_CANDIDATE.md','RECOVERY_CONTINUATION.md',
    'researcher_a/CANDIDATE.md','researcher_a/VACUUM_QUARTIC_CANDIDATE.md','researcher_a/FREEZE_01.json',
    'researcher_a/formal_kasner_01.py','researcher_a/formal_kasner_01_result.json',
    'researcher_a/formal_plane_wave_01.py','researcher_a/formal_plane_wave_01_result.json',
    'researcher_b/CANDIDATE.md','researcher_b/vacuum_fine_data.json','researcher_b/MANIFEST.json']
result={'contraction_bookkeeping':contractions,'plane_wave_independent_coefficient_agreement':True,
    'kasner_saved_exact_moments':kas_means,'invariant_constants':{str(k):str(v) for k,v in coefs.items()},
    'recomputed_clock_means':recomputed,'maximum_endpoint_log_difference':max_point_error,
    'python':platform.python_version(),'sympy':sp.__version__, 'source_sha256':sha(__file__),
    'input_sha256':{p:sha(BASE/p) for p in inputs},
    'limitations':'pairing arithmetic is not geometric certification; raw data replay is not a new null solve or interval proof'}
with (OWN/'direct_check01_result.json').open('x') as f:
    json.dump(result,f,indent=2);f.write('\n')
print(json.dumps(result,indent=2))
