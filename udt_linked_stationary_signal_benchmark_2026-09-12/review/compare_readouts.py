"""Compare independently saved ODE and parent quadrature outputs; no production imports."""
import hashlib
import json
from pathlib import Path

review=Path(__file__).resolve().parent
pkg=review.parent
ours=json.loads((review/'INDEPENDENT_GEODESIC_RESULT.json').read_text())
parent=json.loads((pkg/'checks/benchmark.stdout').read_text())
lookup={(r['a'],r['b']):r for r in ours['rows'] if r['control']=='fine'}
rows=[]
for prod in parent['records']:
    key=tuple(prod['supplied_coefficients'])
    own=lookup[key]
    row={'a':key[0],'b':key[1],'differences':{}}
    for own_key,parent_key in [('p','p'),('psi_B','psi_B'),('tau_round_over_L_cE','roundtrip_cE_over_L')]:
        x=own[own_key];y=prod['tighter_readouts'][parent_key]
        err=abs(x-y);scale=max(1.,abs(x));passed=err<=2e-8*scale
        row['differences'][parent_key]={'independent_ode':x,'parent_tight_quadrature':y,
                                      'absolute':err,'scaled':err/scale,'passed':passed}
    rows.append(row)
result={'status':'PASS' if all(v['passed'] for row in rows for v in row['differences'].values()) else 'FAIL',
        'comparisons':rows,'max_absolute_by_readout':{k:max(r['differences'][k]['absolute'] for r in rows)
                                                  for k in ['p','psi_B','roundtrip_cE_over_L']},
        'max_scaled':max(v['scaled'] for row in rows for v in row['differences'].values()),
        'same_systematic_premises':True,'different_scientific_numerical_method':True,
        'independence':'separate agent code and affine ODE; common supplied metric, NumPy/SciPy/FLOAT64 platform and Brent scalar root library',
        'hashes':{str(p.relative_to(pkg)):hashlib.sha256(p.read_bytes()).hexdigest()
                  for p in [review/'INDEPENDENT_GEODESIC_RESULT.json',pkg/'checks/benchmark.stdout',Path(__file__)]}}
with (review/'CROSS_METHOD_COMPARISON.json').open('x') as out:json.dump(result,out,indent=2);out.write('\n')
print(json.dumps({k:result[k] for k in ['status','max_absolute_by_readout','max_scaled']},sort_keys=True))
if result['status']!='PASS':raise SystemExit(1)
