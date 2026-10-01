"""Separate-context direct array/receipt review of actual TPS1 GPU smoke."""
import hashlib,json,resource
from pathlib import Path
resource.setrlimit(resource.RLIMIT_AS,(2*1024**3,2*1024**3))
import numpy as np
HERE=Path(__file__).resolve().parent;BASE=HERE.parents[1];ROOT=BASE.parent;OLD=ROOT/'udt_time_live_production_preparation_2026-10-01'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def final(run):
    records=[]
    for marker in run.glob('checkpoints/*/COMMITTED'):
        folder=marker.parent;meta=json.loads((folder/'metadata.json').read_text())
        assert marker.read_text().strip()==sha(folder/'metadata.json')
        if meta['eligible_for_resume']:records.append((meta['step'],folder,meta))
    step,folder,meta=max(records,key=lambda item:item[0]);assert step==320 and meta['t']==1.1
    assert sha(folder/'state.npz')==meta['payload_sha256']
    with np.load(folder/'state.npz',allow_pickle=False) as data:return data['state'],meta
expected,_=final(OLD/'runs/engineering_full');states=[]
for name in ['case_a','case_b','case_c']:
    state,meta=final(BASE/'runs/supervisor_smoke'/name)
    assert state.shape==(2,8,8,8,4,4) and state.dtype==np.float64 and np.isfinite(state).all()
    assert np.array_equal(state,expected)
    states.append(dict(case=name,bitwise_equal_to_fixed_TPP_uninterrupted_control=True,final_state_sha256=meta['payload_sha256']))
attempts=[];step_sequences={};peak=0;constraints=0
for kind in ['pause','signal']:
    directory=BASE/'supervisor_smoke'/('runtime_'+kind);manifest=BASE/'supervisor_smoke'/(kind+'.json');mh=sha(manifest);m=json.loads(manifest.read_text())
    assert m['wall_seconds'] is None and (directory/'manifest.sha256').read_text().strip()==mh
    assert not (directory/'wall_budget.json').exists()
    for path,value in m['source_sha256'].items():assert sha(path)==value
    folders=sorted((directory/'attempts').iterdir());assert len(folders)==2
    for folder in folders:
        receipt=json.loads((folder/'receipt.json').read_text());launch=json.loads((folder/'launch.json').read_text())
        assert launch['manifest_sha256']==mh and launch['wall_seconds_limit'] is None
        assert not receipt['sigkill_sent']
        for stream in ['stdout','stderr']:assert sha(folder/stream)==receipt[stream+'_sha256']
        rows=[json.loads(line) for line in (folder/'stdout').read_text().splitlines()];last=rows[-1]
        assert last['status']==receipt['worker_status']
        step_sequences.setdefault(receipt['case'],[]).extend((r['tick'],r['jump_ticks']) for r in rows if r['status']=='ACCEPTED_STEP')
        for row in rows:
            if row['status']=='CHECKED_STATE':
                peak=max(peak,row['gpu_allocated_peak']);constraints=max(constraints,*(row['metrics'][k] for k in ['hamiltonian','momentum','harmonic']))
        if receipt['returncode']==75:
            assert kind=='signal' and receipt['sigterm_sent'] and receipt['forwarded_signal']==15 and not receipt['sigint_sent']
            assert last['status']=='CHECKPOINTED_STOP' and last['reason']=='SIGNAL' and last['signal']==15
        else:
            assert receipt['returncode']==0 and last['status']=='TPS1_RUN_COMPLETE' and last['tick']==320
            assert receipt['forwarded_signal'] is None and not receipt['sigterm_sent'] and not receipt['sigint_sent']
        attempts.append(dict(path=str(folder.relative_to(ROOT)),receipt_sha256=sha(folder/'receipt.json'),returncode=receipt['returncode'],resume=receipt['resume'],status=last['status'],stop_reason=last.get('reason'),wall_seconds=receipt['wall_seconds']))
assert [r['returncode'] for r in attempts]==[0,0,75,0]
assert [r['resume'] for r in attempts]==[False,False,False,True]
assert step_sequences['case_a']==step_sequences['case_b']==step_sequences['case_c']
assert peak<=8*1024**3 and constraints<=2e-5
for name,status in [('pause','QUEUE_CHECKPOINT'),('resume','QUEUE_COMPLETE'),('complete_again','QUEUE_COMPLETE'),('signal_resume','QUEUE_COMPLETE')]:
    rows=[json.loads(line) for line in (BASE/'supervisor_smoke'/(name+'.stdout')).read_text().splitlines()];assert rows[-1]['status']==status
    if name=='complete_again':assert rows[-1]['previously_completed']==2 and len(rows)==1
record=json.loads((BASE/'SUPERVISOR_SMOKE.json').read_text());assert len(record['invocations'])==5 and all(x['returncode']==x['expected'] for x in record['invocations'])
result=dict(status='ACTUAL_NO_TIMEOUT_SMOKE_REVIEW_PASS',context='/root/survey_runtime, independently reviewed parent run artifacts; authored operational adapters and reused fixed solver outputs are not independent solvers',states=states,attempts=attempts,identical_accepted_tick_jump_sequences=True,steps_per_completed_run=len(step_sequences['case_a']),gpu_allocated_peak_bytes=peak,maximum_logged_original_constraint=constraints,total_gpu_worker_seconds=sum(r['wall_seconds'] for r in attempts),smoke_summary_sha256=sha(BASE/'SUPERVISOR_SMOKE.json'),scope='Actual GPU finite queue pause/resume/idempotence and forwardedSIGTERM, authenticated final arrays equal prior uninterrupted control. No elapsed time limit, exhaustive crash recovery or general long-time stability claim.')
with (HERE/'SMOKE_ARTIFACT_REVIEW.json').open('x') as f:json.dump(result,f,indent=2);f.write('\n')
print(json.dumps(result,indent=2))
