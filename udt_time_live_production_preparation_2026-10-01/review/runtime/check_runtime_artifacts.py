"""Independent saved-record and array checks for the changed TPP1 worker.

No producer/checkpoint module imports and no GPU. Metadata and payload SHA values
are recomputed; shared output records do not constitute independent evolution.
"""
import hashlib,json,math
from pathlib import Path
import numpy as np
HERE=Path(__file__).resolve().parent;BASE=HERE.parents[1];ROOT=BASE.parent
def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def canonical(value):return (json.dumps(value,sort_keys=True,indent=2,allow_nan=False)+'\n').encode()

names=['engineering_full','engineering_pause','engineering_resume','engineering_signal',
       'engineering_signal_resume','wall_stop','floor_stop','output_stop']
logs={};receipts={};bindings={};runs={}
for name in names:
    path=BASE/'invocations'/f'{name}.json';receipt=json.loads(path.read_text());receipts[name]=receipt
    assert not receipt['timeout'] and receipt['returncode']==receipt['expected']
    for kind in ['stdout','stderr']:
        p=path.with_suffix('.'+kind);assert sha(p)==receipt[kind+'_sha256'];bindings[str(p.relative_to(ROOT))]=sha(p)
    bindings[str(path.relative_to(ROOT))]=sha(path)
    rows=[json.loads(line) for line in path.with_suffix('.stdout').read_text().splitlines()]
    logs[name]=rows
    specpath=Path(receipt['command'][2]);run=Path(receipt['command'][3]);spec=json.loads(specpath.read_text())
    assert sha(specpath)==receipt['spec_sha256'] and sha(BASE/'production_worker.py')==receipt['worker_sha256']
    oldtick=next(row['tick'] for row in rows if row['status']=='CHECKED_STATE')
    for row in rows:
        if row['status']=='ACCEPTED_STEP':
            jump=row['jump_ticks'];assert type(jump)==int and jump>0 and jump&(jump-1)==0
            assert row['tick']==oldtick+jump and abs(row['t']-(1+row['tick']*spec['dt_min']))<1e-12
            assert row['stage_cfl']<=spec['cfl']*(1+1e-12)
            assert math.isclose(row['stage_cfl'],jump*spec['dt_min']*row['stage_omega'],rel_tol=1e-14)
            oldtick=row['tick']
    if run not in runs:
        records=[]
        for marker in sorted(run.glob('checkpoints/ckpt_*/COMMITTED')):
            folder=marker.parent;raw=(folder/'metadata.json').read_bytes();meta=json.loads(raw)
            assert marker.read_text().strip()==hashlib.sha256(raw).hexdigest()
            assert meta['eligible_for_resume'] is True and meta['diagnostic'] is None
            assert sha(folder/'state.npz')==meta['payload_sha256']
            assert meta['signature']['spec']==hashlib.sha256(canonical(spec)).hexdigest()
            assert meta['signature']['step_semantics']=='integer_time_tick'
            assert meta['signature']['initial']==sha(ROOT/spec['initial'])
            for source,value in meta['signature']['code'].items():assert sha(ROOT/source)==value
            tick=meta['step'];assert type(tick)==int and 0<=tick<=spec['end_tick']
            assert f'ckpt_{tick:09d}_' in folder.name and abs(meta['t']-(1+tick*spec['dt_min']))<1e-12
            with np.load(folder/'state.npz',allow_pickle=False) as data:
                assert set(data.files)=={'state'};state=data['state']
                assert state.shape==(2,spec['n'],spec['n'],spec['n'],4,4)
                assert state.dtype==np.float64 and np.isfinite(state).all()
            records.append(dict(tick=tick,metadata_sha256=hashlib.sha256(raw).hexdigest(),payload_sha256=meta['payload_sha256'],path=str(folder.relative_to(ROOT))))
        assert records and not list(run.glob('diagnostics/*/DIAGNOSTIC'))
        used=sum(p.stat().st_size for p in run.rglob('*') if p.is_file());assert used<=spec['output_bytes']
        runs[run]=dict(records=records,bytes=used,last=state,spec=spec)

full=runs[BASE/'runs/engineering_full']['last']
equal={name:bool(np.array_equal(full,runs[BASE/'runs'/name]['last'])) for name in ['engineering_paused','engineering_signal']}
assert all(equal.values())
schedule=lambda name:[(r['tick'],r['jump_ticks']) for r in logs[name] if r['status']=='ACCEPTED_STEP']
assert schedule('engineering_full')==schedule('engineering_pause')+schedule('engineering_resume')
assert schedule('engineering_full')==schedule('engineering_signal')+schedule('engineering_signal_resume')
stops={}
for name,reason in [('engineering_pause','REQUESTED_PAUSE'),('engineering_signal','SIGNAL'),('wall_stop','WALL_LIMIT'),('floor_stop','TIMESTEP_FLOOR')]:
    row=logs[name][-1];assert row['status']=='CHECKPOINTED_STOP' and row['reason']==reason
    if name=='engineering_signal':assert row['signal']==15 and receipts[name]['sigterm_sent'] is True
    stops[name]=row
error=json.loads((BASE/'invocations/output_stop.stderr').read_text());assert error['reason']=='OUTPUT_BUDGET'
assert receipts['output_stop']['returncode']==2
for run,entry in runs.items():
    if run.name in ['engineering_full','engineering_paused','engineering_signal']:
        ticks={record['tick'] for record in entry['records']};spec=entry['spec']
        needed={0,spec['end_tick'],*range(spec['checkpoint_ticks'],spec['end_tick'],spec['checkpoint_ticks'])}
        for w in spec['windows']:needed.update(w['center']+(i-w['count']//2)*w['stride'] for i in range(w['count']))
        assert needed<=ticks
    del entry['last'];del entry['spec']
print(json.dumps(dict(status='TPP1_RUNTIME_ARTIFACTS_PASS',restart_final_bitwise_equal=equal,
    accepted_schedules_bitwise_equal=True,stops=stops,output_failure=error,
    runs={str(k.relative_to(ROOT)):v for k,v in runs.items()},receipt_sha256=bindings,
    scope='Direct immutable payload, full accepted schedule, final-array and explicit stop-record checks. No independent time evolution or universal crash guarantee.'),indent=2,sort_keys=True))
