"""No-oracle exposed noise and raw-record mutation checks; own inverse only."""
import copy,json,hashlib,platform
from pathlib import Path
from decimal import Decimal as D
from replay_inverse import replay,eventkey,raw_coeff,SITES,jsonable,compare,dec

B=Path(__file__).resolve().parent.parent; F=B/'fidelity'
data=json.loads((B/'main/fine/observations.json').read_text())
clean=json.loads((F/'REPLAY_fine_clean.json').read_text())
base={eventkey(e):e for e in clean['events']}
noise_results=[]
for eps in ['1e-14','1e-12','1e-10']:
    got=json.loads((F/f'REPLAY_fine_noise_{eps}.json').read_text())
    rr=[];qq=[]
    for e in got['events']:
        before=base[eventkey(e)]
        for field,arr,slack in [('R',rr,D('1e-12')),('Q',qq,D('1e-10'))]:
            change=abs(D(e[field])-D(before[field]));bound=D(e[field+'_noise_bound'])
            assert change<=bound+slack,(eps,eventkey(e),field,change,bound)
            arr.append(change/bound)
    finest=[e for e in got['events'] if e['h']==.04 and e['L_small']==.005]
    noise_results.append(dict(epsilon=eps,max_R_fraction=max(rr),max_Q_fraction=max(qq),
        finest_Q_change=max(abs(D(e['Q'])-D(base[eventkey(e)]['Q'])) for e in finest),
        finest_Q_bound=max(D(e['Q_noise_bound']) for e in finest)))

# Keep only one event's calibration/observations; no truth/oracle is used.
subset={**data,'records':[r for r in data['records'] if r['case']=='A' and r['center']==0 and r['h']==.04]}
zero=replay(subset)
target=('A',0.,.04,.01,.005)
z={eventkey(e):e for e in zero['events']}[target]
adversarial=copy.deepcopy(subset); epsilon=1e-12
for row in adversarial['records']:
    if row['L'] not in [.01,.005]:continue
    ew=-1 if row['L']==.01 else 2
    weight=raw_coeff(data['speed'],row['frame'],row['L'])*ew*SITES[row['site']]/dec(row['h'])**2
    row['log_p']+=epsilon*(1 if weight>0 else -1)
attack=replay(adversarial)
q={eventkey(e):e for e in attack['events']}[target]['Q']
# Reconstruct direct absolute-weight bound for the same subset.
bound={eventkey(e):e for e in replay(subset,epsilon)['events']}[target]['Q_noise_bound']
ratio=(q-z['Q'])/bound
assert abs(ratio-1)<D('1e-6'),ratio

parent_attack=json.loads((B/'main/adversarial_observations.json').read_text())
assert parent_attack==adversarial,'parent saved adversarial raw rows differ from independently built sign pattern'
parent_out=json.loads((B/'main/adversarial_inverse.json').read_text())
comparison=compare(attack,parent_out)

# Mutation check: a one-record log error has the independently derived coefficient.
mutant=copy.deepcopy(subset)
row=next(r for r in mutant['records'] if r['site']=='o' and r['L']==.005 and r['frame']==0 and r['direction']==0)
old=row['log_p'];row['log_p']+=1e-6
delta=D.from_float(row['log_p'])-D.from_float(old)
actual={eventkey(e):e for e in replay(mutant)['events']}[target]
w=2*raw_coeff(data['speed'],0,.005)
dr=actual['R']-z['R'];dq=actual['Q']-z['Q']
assert abs(dr-w*delta)<D('1e-40')
assert abs(dq+4*w*delta/dec(.04)**2)<D('1e-37')
assert abs(dr)>D('1e-3') and abs(dq)>1

# Directly challenge independent schema guard with an undeclared oracle input.
bad=copy.deepcopy(subset);bad['records'][0]['oracle_R']=123
try:replay(bad)
except AssertionError:guard_rejected=True
else:guard_rejected=False
assert guard_rejected

result=dict(scope='Saved-clock independent replay/noise/catches before oracle exposure',
    python=platform.python_version(),noise_results=noise_results,
    adversarial=dict(signed_Q_change=q-z['Q'],direct_absolute_weight_bound=bound,attained_fraction=ratio,parent_raw_exact_match=True,parent_inverse_comparison=comparison),
    one_record_mutation=dict(R_change=dr,Q_change=dq,predicted_R=w*delta,predicted_Q=-4*w*delta/dec(.04)**2),
    undeclared_oracle_guard_rejected=guard_rejected,
    sha256={str(p.relative_to(B)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [B/'main/fine/observations.json',B/'main/adversarial_observations.json',B/'main/adversarial_inverse.json',F/'replay_inverse.py',Path(__file__)]})
with (F/'NOISE_AND_CATCH_RESULT.json').open('x') as f:json.dump(jsonable(result),f,indent=2);f.write('\n')
print(json.dumps(jsonable(result),indent=2))
