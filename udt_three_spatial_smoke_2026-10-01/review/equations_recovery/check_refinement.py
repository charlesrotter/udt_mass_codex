#!/usr/bin/env python3
"""Reviewer-owned frozen-threshold check at common marked events, plus exact control."""
import hashlib
import json
from pathlib import Path
import numpy as np
from history_ricci import metric_jets,original_ricci,own_kasner

HERE=Path(__file__).resolve().parent
BASE=HERE.parent.parent
histories=BASE/'histories'
def load(name):
    with np.load(histories/(name+'.npz'),allow_pickle=False) as data:return {k:data[k] for k in data.files}
coarse=load('n8');fine=load('n16');half=load('n16_half');repaired=load('n8_repaired')
assert np.array_equal(coarse['times'],fine['times'])
assert float(coarse['period'])==float(fine['period'])
assert fine['g'].shape[1]==2*coarse['g'].shape[1]
rows=[]
for t in range(2,len(coarse['times'])-2):
    c=original_ricci(*metric_jets(coarse['g'],coarse['times'],t,float(coarse['period'])))[0]
    f=original_ricci(*metric_jets(fine['g'],fine['times'],t,float(fine['period'])))[0][::2,::2,::2]
    rows.append({'time':float(coarse['times'][t]),'coarse_max':float(abs(c).max()),'fine_common_points_max':float(abs(f).max())})
cmax=max(q['coarse_max'] for q in rows);fmax=max(q['fine_common_points_max'] for q in rows)
assert cmax/fmax>=10 or max(cmax,fmax)<1e-9
time_error={k:float(abs(fine[k][-1]-half[k][-1]).max()) for k in ['g','v']}
assert max(time_error.values())<2e-7
assert all(np.array_equal(coarse[k],repaired[k]) for k in ['g','v','times'])
controls=[]
for name in ['kasner','kasner_half']:
    data=load(name);expected=own_kasner(data['times'],data['g'].shape[1]);rates=np.array([1.,-1/3,2/3,2/3])
    velocity=expected*2*rates
    errors={'g':float(abs(data['g']-expected).max()),'v':float(abs(data['v']-velocity).max())}
    assert max(errors.values())<2e-7
    controls.append({'name':name,'all_saved_time_error':errors})
results=json.loads((HERE/'HISTORY_RICCI_RESULT.json').read_text())
assert all(q['ricci_max']<=2e-5 for q in results['histories'])
result={'status':'FROZEN_NUMERICAL_GATES_PASS','common_marked_events':rows,'spatial_refinement_ratio':cmax/fmax,
        'final_timestep_halving_max_error':time_error,'kasner_controls':controls,'guard_repair_preserves_history_bitwise':True,
        'scope':'Finite supplied short-slab grid histories and stated numerical tolerances only; neither continuum certification nor long-time stability.',
        'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'history_checker_sha256':hashlib.sha256((HERE/'history_ricci.py').read_bytes()).hexdigest(),
        'smoke_plan_sha256':hashlib.sha256((BASE/'SMOKE_PLAN.md').read_bytes()).hexdigest(),
        'history_hashes':{str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(histories.glob('*.npz')) if p.stem in ['n8','n8_repaired','n12','n16','n16_half','kasner','kasner_half']}}
with (HERE/'REFINEMENT_RESULT.json').open('x') as f:json.dump(result,f,indent=2,sort_keys=True,allow_nan=False);f.write('\n')
print(json.dumps(result,sort_keys=True))
