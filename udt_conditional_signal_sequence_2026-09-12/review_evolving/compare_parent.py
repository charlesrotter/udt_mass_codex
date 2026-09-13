#!/usr/bin/env python3
import hashlib,json,sys
from pathlib import Path
import numpy as np
HERE=Path(__file__).resolve().parent;PACK=HERE.parent
pp=Path(sys.argv[1]) if len(sys.argv)>1 else PACK/'checks/evolving_repaired.stdout'
p=json.loads(pp.read_text())
if p['status']!='PASS':raise RuntimeError('Parent has no passing scientific output')
own=[json.loads(x)['row'] for x in (HERE/'affine_initial.stdout').read_text().splitlines() if json.loads(x)['kind']=='sample']
frozen=[json.loads(x)['row'] for x in (HERE/'frozen_independent.stdout').read_text().splitlines() if json.loads(x)['kind']=='frozen']
ext=[json.loads(x) for x in (HERE/'affine_extended_repaired.stdout').read_text().splitlines()]
checks=[]
def check(name,got,want,tol,key):
    a=np.asarray(got,dtype=float);b=np.asarray(want,dtype=float)
    error=float(np.max(abs(a-b)/(1+abs(b))))
    checks.append({'name':name,'key':list(key),'scaled_error':error,'tolerance':tol,
                   'pass':bool(np.isfinite(error) and error<=tol)})
for par in p['records']:
    key=(par['epsilon'],par['source_clock'])
    o=next(x for x in own if (x['eps'],x['tau_e'])==key);of=o['fine'];fr=next(x for x in frozen if (x['eps'],x['tau_e'])==key)
    for sub,label in [(par,'base'),(par['tight'],'tight')]:
        for kp,ki in [('te','t_e'),('to','t_o'),('R','R'),('arrival_clock','tau_o'),('source_sky','sky_e'),('arrival_sky','sky_o')]:
            check(label+'_'+kp,sub[kp],of[ki],2e-7,key)
        check(label+'_spatial_momentum',sub['state'][3:6],of['p_o'][1:],2e-7,key)
        for kp,ki in [('area','area'),('widths','widths'),('screen_map','D')]:
            check(label+'_'+kp,sub[kp],o['beam_fine_angle'][ki],2e-6,key)
    sub=par['frozen_control']
    for kp,ki in [('te','t_e'),('to','t_o'),('R','R'),('source_sky','sky_e'),('arrival_sky','sky_o')]:
        check('frozen_'+kp,sub[kp],fr[ki],2e-7,key)
    for kp,ki in [('area','area'),('widths','widths')]:
        check('frozen_'+kp,sub[kp],fr[ki],2e-6,key)
for par in p['events']:
    o=next(x['row'] for x in ext if x['kind']=='duration' and x['row']['eps']==par['epsilon'])
    for kp,ki in [('arrival_duration','arrival_difference'),('mean_R','D_event'),('single_initial_pulse_duration_error','initial_pulse_duration_error')]:
        check('event_'+kp,par[kp],o[ki],2e-7,(par['epsilon'],))
for par in p['reverse']:
    o=next(x['row'] for x in ext if x['kind']=='reverse' and (x['row']['eps'],x['row']['tau_e'])==(par['epsilon'],par['source_clock']))
    check('reverse_area',par['reverse_area'],o['fine']['area'],2e-6,(par['epsilon'],par['source_clock']))
paths=[pp,HERE/'affine_initial.stdout',HERE/'affine_extended_repaired.stdout',HERE/'frozen_independent.stdout',PACK/'step_03/check_evolving.py']
result={'status':'PASS' if all(c['pass'] for c in checks) else 'FAIL','check_count':len(checks),'all12_parent_records_compared':len(p['records'])==12,
  'max_central_scaled_error':max(c['scaled_error'] for c in checks if c['tolerance']==2e-7),
  'max_beam_scaled_error':max(c['scaled_error'] for c in checks if c['tolerance']==2e-6),
  'sha256':{str(x.relative_to(PACK)):hashlib.sha256(x.read_bytes()).hexdigest() for x in paths},'checks':checks,
  'scope':'Distinct full-affine vs reduced-Hamiltonian derivative implementations; shared scipy Bessel/library; finite FLOAT64 diagnostic, not interval certification.'}
print(json.dumps(result,indent=2))
if result['status']!='PASS' or not result['all12_parent_records_compared']:raise SystemExit(1)
