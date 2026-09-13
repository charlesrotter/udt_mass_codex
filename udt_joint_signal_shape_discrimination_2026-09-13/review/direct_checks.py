#!/usr/bin/env python3
"""Direct-exposure checks; no parent scientific implementation imported.

The unchanged source-first definitions supply mpmath profile/quadrature code.
The parent output is used only as a comparison target. The failed gate is
recomputed at its original inputs, with no substitute confirmation range.
"""
from pathlib import Path
import hashlib
import json
import math
import sys
import time

HERE=Path(__file__).resolve().parent
P=HERE.parent
source=HERE/'source_first_check.py'
assert hashlib.sha256(source.read_bytes()).hexdigest() == 'af8e691b6e602ac88bb8e0dd1cc8c38cf1956b010eed888d1e697f1311571d60'
prefix,sep,_=source.read_text().partition('\ncases = ')
assert sep
ns={}
exec(compile(prefix,str(source),'exec'),ns)
mp=ns['mp'];records=ns['records'];serial=ns['serial'];beta=ns['beta'];c1=ns['c1']
started=time.monotonic()
parent=json.loads((P/'checks/discrimination_complete.stdout').read_text())
first=json.loads((HERE/'checks/source_first.stdout').read_text().splitlines()[-1])
first_diffs={key:mp.mpf(0) for key in ['R','Dy','Dz','W','dlogR','dW']}
for row in first['rows']:
    if row['n']!=8:continue
    other=next(z for z in first['rows'] if z['n']==12 and
               all(z[k]==row[k] for k in ['Q','eta','d']))
    for key in first_diffs:
        first_diffs[key]=max(first_diffs[key],abs(mp.mpf(row['records'][key])-mp.mpf(other['records'][key])))
assert max(first_diffs.values())<mp.mpf('1e-24')

Q=mp.mpf('.3')*c1;eta=mp.mpf('.15');q=3*Q/2
theta=ns['theta'];k=ns['k'];c2=ns['c2']
r=mp.mpf('1.5')*(-k*(Q-c2*eta)/c1*mp.sin(theta)-2*k*eta*mp.sin(2*theta))
target=mp.mpf(1)/8-q*q/8+q*r/2
rows=[];differences={key:mp.mpf(0) for key in ['R','Dy','Dz','H','deta_logR','deta_H']}
order_differences={key:mp.mpf(0) for key in ['R','Dy','Dz','W','dlogR','dW']}
for dtext in ['.2','.1','.05','.025','.0125']:
    d=mp.mpf(dtext)
    low=records(Q,eta,d,12);high=records(Q,eta,d,20)
    for key in order_differences:
        order_differences[key]=max(order_differences[key],abs(low[key]-high[key]))
    old=next(z['tight'] for z in parent['records'] if z['tight']['Q']!=0 and
             z['tight']['eta']==.15 and z['tight']['d']==float(d))
    for key,own in [('R','R'),('Dy','Dy'),('Dz','Dz'),('H','W'),
                    ('deta_logR','dlogR'),('deta_H','dW')]:
        differences[key]=max(differences[key],abs(mp.mpf(str(old[key]))-high[own]))
    estimate=(mp.log(high['R'])-(q*q-1)*d/4)/d**2
    rows.append(dict(d=d,records=high,clock_second_estimate=estimate,
                     clock_second_target=target,absolute_error=abs(estimate-target)))
    print(json.dumps(serial(rows[-1])),flush=True)
assert max(differences.values())<mp.mpf('2e-12')
assert max(order_differences.values())<mp.mpf('1e-24')
frozen_error=rows[-1]['absolute_error']
frozen_tolerance=mp.mpf('.8')*rows[0]['absolute_error']+mp.mpf('1e-8')
assert frozen_error>frozen_tolerance

# The omission variant changes the readout itself. At Q=eta=0, H_eta equals
# beta/3*d^2 at leading order; without the receiver ruler it tends to -2 beta/3.
mutants=[]
for d in [mp.mpf('.04'),mp.mpf('.02')]:
    own=records(mp.mpf(0),mp.mpf(0),d,12)
    H=ns['profile'](d,mp.mpf(0),mp.mpf(0))[2]
    wrong=own['dW']-H
    mutants.append(dict(d=d,correct_eta_shape=own['dW'],
                        omitted_receiver_eta_shape=wrong,
                        correct_coefficient=beta/3,wrong_coefficient=-2*beta/3))
    assert own['dW']<0 and wrong>0

old=json.loads((P/'checks/discrimination_repaired.stdout').read_text())
assert parent['records']==old['records']
assert parent['guards'][:len(old['guards'])]==old['guards']
assert parent['parameter_difference_checks']==old['parameter_difference_checks']
assert parent['convergence'][:len(old['convergence'])]==old['convergence']
failed=[g for g in parent['guards'] if not math.isfinite(g['error']) or g['error']>g['tolerance']]
assert parent['status']=='FAIL' and failed==parent['failed_guards'] and len(failed)==1
assert len(parent['records'])==30 and len(parent['guards'])==388
print(json.dumps(serial(dict(status='PASS_REVIEW_CHECKS_ORIGINAL_GATE_FAILURE_CONFIRMED',
    precision_digits=mp.mp.dps,mpmath=mp.__version__,python=sys.version,
    source_first_8_12_max_differences=first_diffs,
    original_failed_case_12_20_max_differences=order_differences,
    parent_record_max_differences=differences,failed_gate_error=frozen_error,
    failed_gate_tolerance=frozen_tolerance,failed_case_records=rows,
    independent_ruler_omission_checks=mutants,original_guard_failure=failed,
    preserved_records_and_prefixes=True,elapsed_seconds=time.monotonic()-started))),flush=True)
