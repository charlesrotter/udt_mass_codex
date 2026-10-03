"""Independent direct linear-functional reconstruction of all main observations."""
import json,math,random,hashlib
from pathlib import Path
from collections import defaultdict
B=Path(__file__).resolve().parents[1]
sw={'o':-4,'t+':-1,'t-':-1,'x+':1,'x-':1,'y+':1,'y-':1,'z+':1,'z-':1}

def scalar_rows(data,epsilon):
 rng=random.Random(1729);sums=defaultdict(list);v=data['speed']
 for r in data['records']:
  y=r['log_p']+epsilon*rng.uniform(-1,1)
  key=tuple(r[k] for k in ['case','center','h','site','L'])
  w=2*(1+3/v**2) if r['frame']==0 else -(1-v*v)/v**2
  sums[key].append(w*y/r['L']**2)
 return {k:math.fsum(v) for k,v in sums.items()}

checks=[];mapping=[];independent={}
for level in ['coarse','fine']:
 data=json.loads((B/f'main/{level}/observations.json').read_text())
 raw=json.loads((B/f'main/{level}/forward_details.json').read_text())
 assert len(raw['observation_query_ids'])==len(data['records'])
 for r,qid in zip(data['records'],raw['observation_query_ids']):
  q=raw['unique_queries'][qid]
  assert q['query_id']==qid and q['case']==r['case'] and q['L']==r['L'] and q['log_p']==r['log_p']
  kind='rest' if r['frame']==0 else ('boost_long' if r['direction']==0 else 'boost_trans')
  assert q['unique_forward_kind']==kind
 mapping.append(dict(level=level,records=len(data['records']),unique=len(raw['unique_queries'])))
 for eps in ([0] if level=='coarse' else [0,1e-14,1e-12,1e-10]):
  tag='clean' if eps==0 else f'noise_{eps:.0e}'
  result=json.loads((B/f'main/{level}/inverse_{tag}.json').read_text())
  scal=scalar_rows(data,eps);er=[];eq=[];my_events={}
  for r in result['events']:
   prefix=(r['case'],r['center'],r['h'])
   site={k:2*scal[prefix+(k,r['L_small'])]-scal[prefix+(k,r['L_large'])] for k in sw}
   R=site['o'];Q=math.fsum(sw[k]*value for k,value in site.items())/r['h']**2
   er.append(abs(R-r['R']));eq.append(abs(Q-r['Q']))
   my_events[tuple(r[k] for k in ['case','center','h','L_large','L_small'])]=(R,Q)
  assert max(er)<2e-12 and max(eq)<1e-8
  fitdiff=[]
  for fit in result['fits']:
   if 'slope' not in fit:continue
   common=(fit['h'],fit['L_large'],fit['L_small'])
   left=my_events[(fit['case'],fit['fit_centers'][0])+common]
   right=my_events[(fit['case'],fit['fit_centers'][1])+common]
   slope=(right[1]-left[1])/(right[0]-left[0]);intercept=left[1]-slope*left[0]
   hold=[my_events[(fit['case'],h['center'])+common][1]-slope*my_events[(fit['case'],h['center'])+common][0]-intercept for h in fit['heldout']]
   delta=max([abs(slope-fit['slope']),abs(intercept-fit['intercept'])]+[abs(a-b['residual']) for a,b in zip(hold,fit['heldout'])])
   fitdiff.append(delta)
  assert max(fitdiff)<1e-8
  independent[level,tag]=my_events
  checks.append(dict(level=level,epsilon=eps,events=len(er),max_R_difference=max(er),max_Box_difference=max(eq),max_fit_difference=max(fitdiff)))

adv=json.loads((B/'main/adversarial_observations.json').read_text());scal=scalar_rows(adv,0)
site={k:2*scal[('A',0,.04,k,.005)]-scal[('A',0,.04,k,.01)] for k in sw}
q=math.fsum(sw[k]*v for k,v in site.items())/.04**2
clean=independent['fine','clean']['A',0,.04,.01,.005][1]
bound=12*88*1e-12*(2/.005**2+1/.01**2)/.04**2
assert abs((q-clean)/bound-1)<.001
out=dict(status='PASS independent main mapping/inverse/noise/fit replay',mapping=mapping,checks=checks,
         adversarial=dict(independent_Q_change=q-clean,analytic_bound=bound),
         limits='No parent module imports; shared stdlib random reproduces declared synthetic perturbations. This is numerical correspondence, not an independent noise sample or physical uncertainty bound.')
with (B/'math/MAIN_INVERSE_CHECK.json').open('x') as f:json.dump(out,f,indent=2);f.write('\n')
print(json.dumps(out))
