"""Independent replay of saved smoke; no parent forward/inverse imports."""
import json,math,hashlib
from pathlib import Path
from collections import defaultdict
import numpy as np
from scipy.integrate import quad
import source_first_check as own

B=Path(__file__).resolve().parents[1]
def ah(t,k):
    a=1+k*t**3
    return a,3*k*t*t/a
own.metric=ah
own.eta=lambda t,k:quad(lambda s:1/(1+k*s**3),0,t,epsabs=1e-14,epsrel=1e-14)[0]

raw=json.loads((B/'smoke/forward_checks.json').read_text())
seen=set();checks=[]
for block in raw:
    if not block['fine'] or block['kind']!='cubic_control':continue
    identity=(block['t'],block['L'])
    if identity in seen:continue
    seen.add(identity)
    for j,r in enumerate(block['values']):
        U,triad=own.frame(block['t'],[0 if j==0 else .6,0,0],.03)
        q=own.clock(block['t'],U,triad[1 if j==2 else 0],block['L'],.03)
        checks.append(dict(t=block['t'],L=block['L'],kind=r['unique_forward_kind'],
                           parent_log=r['log_p'],independent_log=q['logp'],error=abs(q['logp']-r['log_p'])))
assert max(z['error'] for z in checks)<2e-12

data=json.loads((B/'smoke/observations.json').read_text());v=data['speed']
group=defaultdict(list)
for r in data['records']:
    key=tuple(r[k] for k in ['case','center','h','site','L'])
    w=2*(1+3/v**2) if r['frame']==0 else -(1-v*v)/(v*v)
    group[key].append(w*r['log_p']/r['L']**2)
scalar={key:math.fsum(vals) for key,vals in group.items()}
saved=json.loads((B/'smoke/inverse.json').read_text());replays=[]
weights={'o':-4,'t+':-1,'t-':-1,'x+':1,'x-':1,'y+':1,'y-':1,'z+':1,'z-':1}
for r in saved['events']:
    prefix=(r['case'],r['center'],r['h'])
    site={name:2*scalar[prefix+(name,r['L_small'])]-scalar[prefix+(name,r['L_large'])] for name in weights}
    R=site['o'];Q=math.fsum(weights[k]*x for k,x in site.items())/r['h']**2
    replays.append(dict(case=r['case'],h=r['h'],L_small=r['L_small'],R_error=abs(R-r['R']),Q_error=abs(Q-r['Q'])))
assert max(x['R_error'] for x in replays)<2e-12
assert max(x['Q_error'] for x in replays)<1e-9
report=dict(status='PASS independent saved-smoke replay',forward=checks,inverse=replays,
            parent_imports=False,own_prior_source_import='math/source_first_check.py',
            limits='Shared Python, NumPy/SciPy libraries and model. Independently authored direct-coordinate solve and weighted scalar/Box reconstruction. No main outcomes exposed.')
with (B/'math/EXPOSED_SMOKE_CHECK.json').open('x') as f:json.dump(report,f,indent=2);f.write('\n')
print(json.dumps(dict(status=report['status'],clock_count=len(checks),forward_max=max(x['error'] for x in checks),
                      R_max=max(x['R_error'] for x in replays),Q_max=max(x['Q_error'] for x in replays))))
