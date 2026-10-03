"""Frozen small forward/serialization/inverse smoke; not the main benchmark."""
from pathlib import Path
import json,time,hashlib,sys
from forward import Geometry,clock_triplet,expand_frames
from inverse import reconstruct

B=Path(__file__).resolve().parent;out=B/'smoke';out.mkdir(exist_ok=False)
start=time.monotonic(); records=[]; raw=[];calls=0
for fine in [False,True]:
 for kind in ['flat','cubic_control']:
  g=Geometry(kind,fine)
  for t,site in [(0.,'o'),(.05,'t+'),(-.05,'t-')]+[(None,k) for k in ['x+','x-','y+','y-','z+','z-']]:
   tt=g.spatial_site_time(0.,.05) if t is None else t
   for L in [.02,.01,.005]:
    val=clock_triplet(g,tt,L,.6)
    raw.append(dict(fine=fine,kind=kind,t=tt,L=L,values=val))
    if kind=='flat':assert max(abs(row['log_p']) for row in val)<1e-11
    for row in expand_frames(val):records.append(dict(case=f'{kind}_{fine}',center=0,h=.05,site=site,L=L,frame=row['frame'],direction=row['direction'],log_p=row['log_p']))
  try:g.observe(1.49,.02,.6,0)
  except (AssertionError,RuntimeError):stopped=True
  else:stopped=False
  assert stopped
  calls+=g.calls
data=dict(schema='CBR1_CLOCK_ONLY',speed=.6,records=records)
def save(name,data):
 with (out/name).open('x') as f:json.dump(data,f,indent=2,allow_nan=False);f.write('\n')
save('observations.json',data);save('forward_checks.json',raw)
# Serialize then parse at the interface, not direct in-memory oracle use.
result=reconstruct(json.loads((out/'observations.json').read_text()))
save('inverse.json',result)
for row in result['events']:
 if row['case'].startswith('flat'):assert abs(row['R'])<1e-6 and abs(row['Q'])<1e-3
summary=dict(status='PASS',seconds=time.monotonic()-start,clock_calls=calls,records=len(records),
 max_norm_error=max(row['norm_error'] for group in raw for row in group['values']),
 max_null_residual=max(row['null_residual'] for group in raw for row in group['values']),
 inverse_events=result['events'],domain_stop=True,
 limits='Finite smoke only, cubic t0 and flat controls; no main-law or hardware outcome.',
 source_sha256={str(B/name):hashlib.sha256((B/name).read_bytes()).hexdigest() for name in ['forward.py','inverse.py','SMOKE_PLAN.md','smoke.py']})
save('RESULT.json',summary);print(json.dumps(summary,indent=2))
