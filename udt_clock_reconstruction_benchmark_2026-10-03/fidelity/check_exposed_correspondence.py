"""Post-inverse oracle/source correspondence, exact simple controls, finite errors."""
import json,hashlib,platform
from pathlib import Path
from fractions import Fraction as F
from decimal import Decimal as D
from collections import defaultdict
from replay_inverse import eventkey,fitkey,jsonable

B=Path(__file__).resolve().parent.parent;HERE=B/'fidelity'
load=lambda p:json.loads(p.read_text())
fine=load(HERE/'REPLAY_fine_clean.json');coarse=load(HERE/'REPLAY_coarse_clean.json')
oracle={(r['case'],r['center']):r for r in load(B/'main/oracle.json')['truth']}
assert len(fine['events'])==90 and len(fine['fits'])==18 and len(oracle)==15
frozen=load(B/'RUN_FREEZE.json')['files']
for name,sha in frozen.items():assert hashlib.sha256((B/name).read_bytes()).hexdigest()==sha,name
mapping=[]
for level in ['coarse','fine']:
    obs=load(B/f'main/{level}/observations.json')['records']; details=load(B/f'main/{level}/forward_details.json')
    unique=details['unique_queries'];ids=details['observation_query_ids'];places=details['placements']
    assert len(obs)==25515 and len(unique)==1296 and len(ids)==len(obs) and len(places)==405
    place={(r['case'],r['center'],r['h'],r['site']):r['cosmic_time'] for r in places}
    for record,qid in zip(obs,ids):
        q=unique[qid]
        assert q['case']==record['case'] and q['L']==record['L'] and q['log_p']==record['log_p']
        assert q['t']==place[tuple(record[k] for k in ['case','center','h','site'])]
        expected='rest' if record['frame']==0 else ('boost_long' if record['direction']==0 else 'boost_trans')
        assert q['unique_forward_kind']==expected
        assert -1.5<=q['prep_time']<q['arrival']<=1.5 and q['emission']<q['arrival']
    spatial=[r for r in places if r['site'][0] in 'xyz']
    nontrivial=sum(r['cosmic_time']!=r['center'] for r in spatial)
    assert nontrivial>0
    mapping.append(dict(level=level,records=len(obs),unique_queries=len(unique),placements=len(places),non_equal_time_spatial_labels=nontrivial))

exact_controls=[]
for t0 in [-.6,-.3,0.,.3,.6]:
    t=F(str(t0));b=F(3,100);a=1+b*t**3
    h=3*b*t*t/a;aa=6*b*t/a;third=6*b/a
    rr=6*(aa+h*h);prime=6*(third+h*aa-2*h**3)
    second=6*(aa**2-8*h*h*aa+6*h**4);qq=-second-3*h*prime
    target=oracle['C',t0]
    assert abs(float(rr)-target['R'])<1e-14 and abs(float(qq)-target['Q'])<1e-14
    hh=F(1,5)/(1+F(2,5)*t);false00=3*hh*hh
    assert false00>F(1,100) and oracle['B',t0]['R']==oracle['B',t0]['Q']==0
    exact_controls.append(dict(t=t0,C_R=str(rr),C_Q=str(qq),B_original_E00=str(false00)))

errors=[];groups=defaultdict(list)
for e in fine['events']:
    target=oracle[e['case'],e['center']]
    rerr=abs(D(e['R'])-D(str(target['R'])));qerr=abs(D(e['Q'])-D(str(target['Q'])))
    errors.append(dict(case=e['case'],center=e['center'],h=e['h'],L_small=e['L_small'],R_error=rerr,Q_error=qerr))
    groups[e['case'],e['h'],e['L_small']].append((rerr,qerr))
finest=[e for e in errors if e['h']==.04 and e['L_small']==.005]
maxR=max(e['R_error'] for e in finest);maxQ=max(e['Q_error'] for e in finest)
assert maxR<=D('5e-4') and maxQ<=D('2e-3')
fits={e['case']:e for e in fine['fits'] if e['h']==.04 and e['L_small']==.005}
assert abs(D(fits['A']['alpha'])-1)<D('.05') and abs(D(fits['A']['Lambda']))<D('.0005')
assert D(fits['A']['max_heldout_residual'])<D('.001')
assert fits['B']['status']=='UNINFORMATIVE_AT_DECLARED_RESOLUTION'
assert D(fits['C']['max_heldout_residual'])>D('.005')
cmap={eventkey(e):e for e in coarse['events']}
sensitivity={field:max(abs(D(e[field])-D(cmap[eventkey(e)][field])) for e in fine['events']) for field in ['R','Q']}
assert sensitivity['R']<D('5e-5') and sensitivity['Q']<D('.001')
result=dict(scope='Post-inverse exact simple controls and correspondence; no independent positive ODE or full tensor numerical replay',
    python=platform.python_version(),frozen_source_hashes_unchanged=True,mapping=mapping,exact_controls=exact_controls,
    finest_max_R_error=maxR,finest_max_Q_error=maxQ,independent_finest_fits=fits,numerical_sensitivity=sensitivity,
    error_table=[dict(case=c,h=h,L_small=l,max_R_error=max(q[0] for q in rows),max_Q_error=max(q[1] for q in rows)) for (c,h,l),rows in sorted(groups.items())])
with (HERE/'EXPOSED_CORRESPONDENCE_RESULT.json').open('x') as f:json.dump(jsonable(result),f,indent=2);f.write('\n')
print(json.dumps(jsonable(result),indent=2))
