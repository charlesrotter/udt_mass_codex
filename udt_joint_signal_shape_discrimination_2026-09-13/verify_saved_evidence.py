#!/usr/bin/env python3
"""Authenticate the saved history and independently recompute readout/table arithmetic."""
from pathlib import Path
import json,hashlib,math,csv
P=Path(__file__).resolve().parent;ROOT=P.parent
h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
for f,dest in [('CANDIDATE_FREEZE.json','INITIAL_check_discrimination.py'),('SYMBOLIC_REPAIR_FREEZE.json','SIMPLIFIER_REPAIRED_check_discrimination.py'),('COMPLETE_CAPTURE_AMENDMENT.json','check_discrimination.py')]:
 for n,v in json.loads((P/f).read_text())['sha256'].items():
  target=P/dest if n.endswith('/check_discrimination.py') else ROOT/n
  assert h(target)==v,(f,n)
for n,v in json.loads((P/'SOURCE_PINS.json').read_text())['sha256'].items():assert h(ROOT/n)==v,n
old=json.loads((P/'checks/discrimination_repaired.stdout').read_text())
d=json.loads((P/'checks/discrimination_complete.stdout').read_text())
assert d['records']==old['records'] and d['guards'][:len(old['guards'])]==old['guards']
assert d['parameter_difference_checks']==old['parameter_difference_checks']
assert d['convergence'][:len(old['convergence'])]==old['convergence']
assert d['status']=='FAIL' and len(d['records'])==30 and len(d['guards'])==d['guard_count']==388
assert len(d['failed_guards'])==1 and d['failed_guards'][0]['name']=='leading_convergence_clock_second'
assert sum(g['error']<=g['tolerance'] for g in d['guards'])==387
receipt=json.loads((P/'checks/discrimination_complete.json').read_text());assert receipt['returncode']==1 and not receipt['timeout']
mut=json.loads((P/'checks/mutant_endpoint_rulers.stdout').read_text())
mr=json.loads((P/'checks/mutant_endpoint_rulers.json').read_text());assert mr['returncode']==1 and not mr['timeout']
assert mut['mutation'] and mut['status']=='FAIL'
shape_fail=[g for g in mut['failed_guards'] if 'shape' in g['name']];assert shape_fail
rows=[]
def close(a,b,tol=2e-12):assert abs(a-b)<=tol,(a,b)
for pair in d['records']:
 a=pair['tight'];dd=a['d'];c1=math.cos(21/40);c2=math.cos(21/20)
 close(a['a1']*c1+a['eta']*c2,a['Q'])
 close(a['R'],math.exp((a['lambda_endpoint']-4*math.log(.75))/4)/(1+dd)**.25)
 close(a['H'],math.log(a['Dy']/a['Dz']))
 close(a['Dy'],math.sqrt(1+dd)*math.exp(a['P_endpoint']/2)*a['I_minus']/.75)
 close(a['Dz'],math.sqrt(1+dd)*math.exp(-a['P_endpoint']/2)*a['I_plus']/.75)
 close(a['area'],a['Dy']*a['Dz'])
 rows.append({k:a[k] for k in ['Q','eta','a1','d','R','H','Dy','Dz','area','deta_logR','deta_H']})
with (P/'RECORDS.tsv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0]),delimiter='\t',lineterminator='\n');w.writeheader();w.writerows(rows)
out={'status':'PASS_SAVED_EVIDENCE_FIDELITY','scientific_finite_plan':'FAIL_ONE_ORIGINAL_FROZEN_CONVERGENCE_GATE','original_guard_count':388,'passed_guards':387,'failed_guards':d['failed_guards'],'record_count':30,'all_original_records_and_guard_prefix_exactly_preserved':True,'all_source_pins_and_original_freezes_authentic':True,'mutation_fails_shape_guards':len(shape_fail),'mutation_failed_guards':mut['failed_guards'],'limits':'Separate standard-library readout arithmetic and source correspondence; not independent metric propagation, symbolic proof or approval of the failed plan.'}
for prefix in ['original_lapse','quadrature','eta_difference','zero_Q']:
 guards=[g for g in d['guards'] if g['name'].startswith(prefix)];out[prefix]={'count':len(guards),'max_error':max(g['error'] for g in guards)}
print(json.dumps(out,indent=2))
