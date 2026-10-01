"""Independent actual supervisor smoke receipt, final-state and stop inspection."""
import hashlib,json,math
from pathlib import Path
import numpy as np
HERE=Path(__file__).resolve().parent;BASE=HERE.parents[1];ROOT=BASE.parent
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def final(run):
    path=sorted(run.glob('checkpoints/*/COMMITTED'))[-1].parent
    raw=(path/'metadata.json').read_bytes();meta=json.loads(raw)
    assert (path/'COMMITTED').read_text().strip()==hashlib.sha256(raw).hexdigest()
    assert sha(path/'state.npz')==meta['payload_sha256'] and meta['eligible_for_resume']
    assert meta['step']==320 and meta['t']==1.1
    with np.load(path/'state.npz',allow_pickle=False) as data:return data['state'],meta
expected,_=final(BASE/'runs/engineering_full');state_records=[]
for name in ['case_a','case_b','case_c']:
    state,meta=final(BASE/'runs/supervisor_smoke'/name)
    assert np.array_equal(state,expected)
    state_records.append(dict(case=name,bitwise_equal_to_uninterrupted_engineering=True,payload_sha256=meta['payload_sha256']))
attempts=[];worker_wall=0
for kind in ['pause','signal']:
    directory=BASE/'supervisor_smoke'/('runtime_'+kind)
    manifest=BASE/'supervisor_smoke'/(kind+'.json');mh=sha(manifest)
    assert (directory/'manifest.sha256').read_text().strip()==mh
    budget=json.loads((directory/'wall_budget.json').read_text())
    assert budget['manifest_sha256']==mh and math.isfinite(budget['deadline_unix'])
    folders=sorted((directory/'attempts').iterdir());assert len(folders)==2
    for folder in folders:
        receipt=json.loads((folder/'receipt.json').read_text());worker_wall+=receipt['wall_seconds']
        assert receipt['wall_seconds']<180 and not receipt['sigkill_sent']
        for stream in ['stdout','stderr']:assert sha(folder/stream)==receipt[stream+'_sha256']
        rows=[json.loads(line) for line in (folder/'stdout').read_text().splitlines()]
        last=rows[-1];assert last['status']==receipt['worker_status']
        if receipt['returncode']==75:
            assert kind=='signal' and receipt['sigterm_sent']
            assert last['status']=='CHECKPOINTED_STOP' and last['reason']=='SIGNAL' and last['signal']==15
        else:assert receipt['returncode']==0 and last['status']=='TPP1_RUN_COMPLETE' and last['tick']==320
        attempts.append(dict(path=str(folder.relative_to(ROOT)),receipt_sha256=sha(folder/'receipt.json'),
            returncode=receipt['returncode'],resume=receipt['resume'],worker_status=last['status'],
            stop_reason=last.get('reason'),wall_seconds=receipt['wall_seconds']))
assert [r['returncode'] for r in attempts]==[0,0,75,0]
assert [r['resume'] for r in attempts]==[False,False,False,True]
for name,status in [('pause','QUEUE_CHECKPOINT'),('resume','QUEUE_COMPLETE'),('complete_again','QUEUE_COMPLETE'),('signal_resume','QUEUE_COMPLETE')]:
    rows=[json.loads(line) for line in (BASE/'supervisor_smoke'/(name+'.stdout')).read_text().splitlines()]
    assert rows[-1]['status']==status
    if name=='complete_again':assert rows[-1]['previously_completed']==2 and len(rows)==1
record=json.loads((BASE/'SUPERVISOR_SMOKE.json').read_text())
assert len(record['invocations'])==5 and all(x['returncode']==x['expected'] for x in record['invocations'])
prior=sum(json.loads(path.read_text())['wall_seconds'] for path in (BASE/'invocations').glob('*.json'))
assert prior+worker_wall<600
print(json.dumps(dict(status='ACTUAL_SUPERVISOR_SMOKE_REVIEW_PASS',states=state_records,attempts=attempts,
    supervisor_worker_attempts=len(attempts),supervisor_worker_wall_seconds=worker_wall,
    total_worker_attempts=len(attempts)+len(list((BASE/'invocations').glob('*.json'))),
    total_worker_wall_seconds=prior+worker_wall,smoke_summary_sha256=sha(BASE/'SUPERVISOR_SMOKE.json'),
    scope='Actual queue pause/resume/idempotence and forwarded SIGTERM with direct saved final arrays; no universal crash or multi-hour guarantee.'),indent=2))
