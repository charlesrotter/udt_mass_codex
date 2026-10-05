from pathlib import Path
import json,math,hashlib
from scipy.integrate import quad
p=Path(__file__).resolve().parent
r=json.loads((p/'SAVED_REPLAY_RESULT.json').read_text())
parent=json.loads((p.parent/'CONSTRUCTION_RESULT.json').read_text())['precisions'][-1]
errors=[]
for pair in r['rows'][-3:]:
    raw=pair['saved_input'];lam=7/3
    bs=float(raw['b_star'])/lam
    base=next(q for q in r['rows'][:6] if abs(float(q['saved_input']['b_star'])-bs)<1e-9 and float(q['saved_input']['E'])==1)
    for key,w in [('b',1),('A',0),('Z',0),('K_length',-1),('theta',0),('angular_rate',-1),('j_parallel',1),('j_perp',1)]:
        a=base['recomputed'][key];b=pair['recomputed'][key]/lam**w
        err=abs(b/a-1)
        errors.append(dict(b_star=bs,key=key,relative_homothety_error=err))
assert max(x['relative_homothety_error'] for x in errors)<1e-7
finite=[]
for j,d in enumerate(parent['timed_differences']):
    p1=r['sides'][2*j];p0=r['sides'][2*j+1]
    R1=float(p1['saved_input']['R']);R0=float(p0['saved_input']['R'])
    m=float(p1['saved_input']['m']);H=float(p1['saved_input']['H'])
    dl=quad(lambda rr:1/math.sqrt(2*m/rr+H*H*rr*rr),R0,R1,epsabs=1e-12,epsrel=1e-12)[0]
    kr=math.log(p1['recomputed']['Z']/p0['recomputed']['Z'])/dl
    ka=-math.log(abs(p1['recomputed']['theta']/p0['recomputed']['theta']))/dl
    er=max(abs(kr/float(d['time_averaged_K'])-1),abs(ka/float(d['time_averaged_angular'])-1),abs(dl/float(d['delta_ell'])-1))
    assert er<1e-7
    finite.append(dict(delta_ell=dl,time_averaged_K=kr,time_averaged_angular=ka,max_relative_error=er))
out={'status':'PASS','source_sha256':hashlib.sha256((p/'SAVED_REPLAY_RESULT.json').read_bytes()).hexdigest(),
     'homothety_errors':errors,'finite_intervals':finite,'additional_incidence_solves':0,'cumulative_case_count':67}
output=p/'CAPTURED_RECOMBINATION_RESULT.json'
assert not output.exists()
output.write_text(json.dumps(out,indent=2)+'\n')
assert out==json.loads((p/'SAVED_RECOMBINATION_RESULT.json').read_text())
print('max homothety rel error',max(x['relative_homothety_error'] for x in errors))
print('max finite rel error',max(x['max_relative_error'] for x in finite))
print('PASS: captured recombination agrees exactly with preserved initial result')
