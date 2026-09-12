#!/usr/bin/env python3
"""Direct-stage source-formula evaluation of saved parent states; never imports parent code."""
import hashlib
import json
import math
import sys
from pathlib import Path

import mpmath as mp

mp.mp.dps=50
P=Path(__file__).resolve().parent.parent
hostile=len(sys.argv)>1 and sys.argv[1]=='--hostile-frequency'
assert len(sys.argv)==1 or hostile
freeze=json.loads((P/'IMPLEMENTATION_FREEZE.json').read_text())
assert hashlib.sha256((P/'check_numeric.py').read_bytes()).hexdigest()==freeze['sha256']
baseline=P/'checks/parent_baseline.stdout'
replay=P/'checks/parent_replay.stdout'
assert baseline.read_bytes()==replay.read_bytes(), 'parent baseline replay bytes'
data=json.loads(baseline.read_text())
assert data['status']=='PASS' and data['mutation'] is None
for name in ['parent_baseline','parent_replay']:
    cap=json.loads((P/f'checks/{name}.json').read_text())
    assert cap['returncode']==0 and not cap['timeout'], 'successful parent capture'
mutations={}
for name,wanted in [('drop_bxi','clock_transport'),('freeze_lambda','clock_transport'),('axial_background','zero_amplitude_recovery')]:
    out=json.loads((P/f'checks/mutation_{name}.stdout').read_text())
    cap=json.loads((P/f'checks/mutation_{name}.json').read_text())
    assert out['status']=='FAIL' and cap['returncode']==1 and wanted in out['failure'], 'actual hostile scientific rejection'
    mutations[name]=out['failure']
rows=list(data['finite_cases'])
rows.append(data['worst_finite_tight_repeat'])
for run in data['long_reception_illustrations']: rows.extend(run['samples'])
rows.extend(data['long_tight_repeat'])
assert len(data['finite_cases'])==144 and len(data['long_reception_illustrations'])==12 and len(rows)==210
if hostile: rows[0]=dict(rows[0],log_frequency_integrated=rows[0]['log_frequency_integrated']+.001)
K=mp.mpf(3)/4
Ac=-3*mp.pi/4*mp.bessely(0,K)
Bc=3*mp.pi/4*mp.besselj(0,K)
err_integrated=err_stored=err_contrast=err_bound=mp.mpf(0)
for i,row in enumerate(rows):
    vals={name:mp.mpf(str(row[name])) for name in ['epsilon','mu','psi','xi','eta','reception_t']}
    e,mu,psi,xi,eta,t=[vals[name] for name in ['epsilon','mu','psi','xi','eta','reception_t']]
    f=Ac*mp.besselj(0,K*t)+Bc*mp.bessely(0,K*t)
    profile=e*f*mp.cos(K*xi)
    M=(1-mu*mu)*(mp.cos(psi)**2*mp.exp(-profile)+mp.sin(psi)**2*mp.exp(profile))
    logw=mp.log(M/t)/2+mp.log(mp.cosh(eta))
    logw0=mp.log(mu*mu*mp.sqrt(t)+(1-mu*mu)/t)/2
    logc=logw0-logw
    bound=abs(e*f)/2+mp.log(1+t**mp.mpf('1.5')*mu*mu/(1-mu*mu))/2
    e1=abs(logw-mp.mpf(str(row['log_frequency_integrated'])))
    e2=abs(logw-mp.mpf(str(row['log_frequency_reconstructed'])))
    e3=abs(logc-mp.mpf(str(row['log_contrast'])))
    e4=abs(bound-mp.mpf(str(row['log_momentum_upper_bound'])))
    err_integrated=max(err_integrated,e1);err_stored=max(err_stored,e2)
    err_contrast=max(err_contrast,e3);err_bound=max(err_bound,e4)
    if e1>mp.mpf('2e-7'):
        print(json.dumps({'failed_row':i,'integrated_frequency_discrepancy':str(e1),'hostile':hostile}),flush=True)
    assert e1<=mp.mpf('2e-7'), 'saved-state metric frequency'
    assert max(e2,e4)<=mp.mpf('2e-8'), 'stored algebraic source correspondence'
    assert e3<=mp.mpf('2e-7'), 'saved-state metric contrast'
    assert logc<=bound+mp.mpf('2e-7'), 'saved-state transverse-momentum bound'
print(json.dumps({'result':'PASS','hostile':hostile,'state_rows':len(rows),'mpmath_version':mp.__version__,
    'decimal_digits':mp.mp.dps,'max_integrated_log_frequency_error':str(err_integrated),
    'max_stored_log_frequency_error':str(err_stored),'max_log_contrast_error':str(err_contrast),
    'max_stored_log_bound_error':str(err_bound),'parent_warnings':data['warnings'],
    'parent_finite_repeat_scaled_error':data['finite_repeat_scaled_error'],
    'parent_long_repeat_scaled_error':data['long_repeat_scaled_error'],
    'mutations':mutations,'baseline_replay_byte_equal':True,
    'input_baseline_sha256':hashlib.sha256(baseline.read_bytes()).hexdigest(),
    'epistemic_scope':'Saved float64 trajectory states evaluated with mpmath; no new integration or interval/asymptotic certification.'},indent=2))
