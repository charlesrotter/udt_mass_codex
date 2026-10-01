"""Outcome-informed frozen repair: center-only high-order spatial diagnostics."""
import hashlib
import json
from pathlib import Path
import sys
import numpy as np
from diagnose_window_truncation import center_ricci, verify_weights

HERE=Path(__file__).resolve().parent;BASE=HERE.parent.parent
sys.path.insert(0,str(BASE.parent/'udt_three_spatial_smoke_2026-10-01/review/equations_recovery'))
from history_ricci import own_kasner

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def load(name):
    with np.load(BASE/'histories'/f'{name}.npz',allow_pickle=False) as d:return {k:d[k] for k in d.files}

verify_weights();records=[];source_map={};controls=[]
for p in sorted((BASE/'histories').glob('*.npz')):
    source_map[str(p)]=sha(p)
    with np.load(p,allow_pickle=False) as data:
        history,times,period=data['g'],data['times'],float(data['period'])
        assert len(times)==9 and np.max(abs(np.diff(times)-.0025))<1e-12
        case=p.stem.rsplit('_window',1)[0]
        record=dict(name=p.stem,case=case,center_time=float(times[4]),n=history.shape[1],orders={})
        computed={}
        for order in (6,8):
            r=center_ricci(history,times,period,order);computed[order]=r
            record['orders'][str(order)]=dict(ricci_max=float(abs(r).max()),ricci_rms=float(np.sqrt(np.mean(r*r))))
            if history.shape[1]==32:record['orders'][str(order)]['common_n16_points_max']=float(abs(r[::2,::2,::2]).max())
        record['sixth_eighth_tensor_max_difference']=float(abs(computed[6]-computed[8]).max())
        records.append(record)
        if case.startswith('kasner'):
            expected=own_kasner(times,history.shape[1]);velocity=expected*2*np.array([1.,-1/3,2/3,2/3])
            errors=dict(g=float(abs(history-expected).max()),v=float(abs(data['v']-velocity).max()))
            assert max(errors.values())<2e-7
            controls.append(dict(name=p.stem,all_saved_errors=errors))
assert len(records)==39
refinements=[]
for family in ['axial1','oblique1']:
    for order in ['6','8']:
        coarse=[r for r in records if r['case']==family+'_n16']
        middle=[r for r in records if r['case']==family+'_n24']
        fine=[r for r in records if r['case']==family+'_n32']
        assert len(coarse)==len(middle)==len(fine)==3
        assert [r['center_time'] for r in coarse]==[r['center_time'] for r in middle]==[r['center_time'] for r in fine]
        cmax=max(r['orders'][order]['ricci_max'] for r in coarse)
        fmax=max(r['orders'][order]['common_n16_points_max'] for r in fine)
        allmax=max(r['orders'][order]['ricci_max'] for r in coarse+middle+fine)
        passed=cmax/fmax>=10 or allmax<1e-8
        refinements.append(dict(family=family,order=int(order),coarse_max=cmax,fine_common_points_max=fmax,
                                ratio=cmax/fmax,all_three_mesh_max=allmax,status='PASS' if passed else 'FAIL'))
timerecords=[]
for case in ['axial1_n24','oblique1_n24','kasner_n16']:
    coarse=load(case+'_window2');fine=load(case+'_half_window2')
    assert np.array_equal(coarse['times'],fine['times'])
    errors={k:float(abs(coarse[k][-1]-fine[k][-1]).max()) for k in ('g','v')}
    assert max(errors.values())<2e-7
    schedules={}
    for name in [case,case+'_half']:
        path=BASE/'invocations'/f'{name}.stdout';source_map[str(path)]=sha(path)
        receipt=json.loads(path.with_suffix('.json').read_text());assert receipt['stdout_sha256']==sha(path)
        lines=[json.loads(x) for x in path.read_text().splitlines()]
        steps=[d for d in lines if d['status']=='ACCEPTED_STEP']
        assert sum(d['jump_ticks'] for d in steps)==4800
        assert all(d['tick']==sum(q['jump_ticks'] for q in steps[:i+1]) for i,d in enumerate(steps))
        jumps=np.array([d['jump_ticks'] for d in steps])
        maximum=float(max(d['stage_cfl'] for d in steps))
        assert maximum <= (.125 if name.endswith('_half') else .25)*(1+1e-12)
        schedules[name]=dict(steps=len(steps),jump_counts={str(k):int(np.count_nonzero(jumps==k)) for k in np.unique(jumps)},
            min_ticks=int(jumps.min()),max_ticks=int(jumps.max()),time_weighted_mean_jump=float(np.sum(jumps*jumps)/np.sum(jumps)),max_stage_cfl=maximum)
    assert schedules[case+'_half']['steps']>schedules[case]['steps']
    timerecords.append(dict(case=case,final_difference=errors,schedules=schedules))
original=[]
for name in ['RICCI_FIRST.json','RICCI_REMAINING.json']:
    path=HERE/name;source_map[str(path)]=sha(path)
    for row in json.loads(path.read_text())['histories']:
        assert row['ricci_max']<=2e-5
        original.append(row['ricci_max'])
assert len(original)==39
allpass=all(r['status']=='PASS' for r in refinements)
result=dict(status='REPAIRED_SCOPED_GATES_PASS' if allpass else 'UNRESOLVED_REFINEMENT',records=records,
    spatial_refinement=refinements,time_refinement=timerecords,exact_saved_kasner=controls,
    original_five_point_max=max(original),original_five_point_spatial_gate='FAILED_AND_RETAINED',
    source_sha256=sha(__file__),diagnostic_sha256=sha(HERE/'diagnose_window_truncation.py'),
    freeze_sha256=sha(BASE/'REFINEMENT_REPAIR_FREEZE.json'),inputs_sha256=source_map,
    scope='Outcome-informed center-only sixth/eighth order saved-time diagnostic; original five-point all-interior residuals retained. Same equations/data/thresholds, no uniform time or continuum certification.')
with (HERE/'REFINEMENT_RESULT.json').open('x') as f:json.dump(result,f,indent=2,sort_keys=True);f.write('\n')
print(json.dumps(result,sort_keys=True))
if not allpass:raise SystemExit(2)
