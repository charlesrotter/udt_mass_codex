"""Independent first-three queue identity, stage CFL, resources and checkpoint review."""
import hashlib,json,math,resource
from pathlib import Path
resource.setrlimit(resource.RLIMIT_AS,(2*1024**3,2*1024**3))
HERE=Path(__file__).resolve().parent;BASE=HERE.parents[1];ROOT=BASE.parent
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
mfile=BASE/'production_runtime/campaign.json';m=json.loads(mfile.read_text());runtime=BASE/'production_runtime'
assert m['wall_seconds'] is None and len(m['cases'])==234
assert (runtime/'manifest.sha256').read_text().strip()==sha(mfile)
assert not (runtime/'wall_budget.json').exists()
for p,h in m['source_sha256'].items():assert sha(p)==h,(p,'source')
first=m['cases'][:3];expected=[r['id'] for r in first];assert expected==['axial_a0_n24','axial_a0_n24_half','axial_a0_n32']
folders=sorted((runtime/'attempts').iterdir());assert len(folders)==3
reports=[];specs=[]
for case,folder in zip(first,folders,strict=True):
    spec=json.loads(Path(case['spec']).read_text());specs.append(spec);receipt=json.loads((folder/'receipt.json').read_text());launch=json.loads((folder/'launch.json').read_text())
    assert sha(case['spec'])==case['spec_sha256'] and receipt['case']==launch['case']==case['id']
    assert receipt['returncode']==0 and receipt['worker_status']=='TPS1_RUN_COMPLETE'
    assert launch['manifest_sha256']==sha(mfile) and launch['wall_seconds_limit'] is None and spec['wall_seconds'] is None
    assert not receipt['sigterm_sent'] and not receipt['sigint_sent'] and not receipt['sigkill_sent'] and receipt['forwarded_signal'] is None
    for stream in ['stdout','stderr']:assert sha(folder/stream)==receipt[stream+'_sha256']
    rows=[json.loads(line) for line in (folder/'stdout').read_text().splitlines()];accepted=[r for r in rows if r['status']=='ACCEPTED_STEP'];previous=0;maximum_cfl=0.
    for row in accepted:
        tick=row['tick'];jump=row['jump_ticks'];assert tick-previous==jump and jump>0 and not jump&(jump-1) and jump<=spec['max_step_ticks'];previous=tick
        assert abs(row['t']-(1+tick*spec['dt_min']))<1e-12
        assert math.isclose(row['stage_cfl'],jump*spec['dt_min']*row['stage_omega'],rel_tol=1e-13)
        assert row['stage_cfl']<=spec['cfl']*(1+1e-12);maximum_cfl=max(maximum_cfl,row['stage_cfl'])
    assert previous==spec['end_tick'] and rows[-1]['tick']==spec['end_tick'] and rows[-1]['steps']==len(accepted)
    checked=[r for r in rows if r['status']=='CHECKED_STATE'];peak=max(r['gpu_allocated_peak'] for r in checked)
    maximum_constraint=max(r['metrics'][k] for r in checked for k in ['hamiltonian','momentum','harmonic'])
    assert peak<=spec['gpu_bytes']<=8*1024**3 and maximum_constraint<=spec['constraint_limit']<=2e-5
    checkpoint_count=0;run=Path(case['run']);initial=(ROOT/spec['initial']).resolve()
    for marker in run.glob('checkpoints/*/COMMITTED'):
        folder2=marker.parent;metadata=json.loads((folder2/'metadata.json').read_text());assert marker.read_text().strip()==sha(folder2/'metadata.json')
        assert metadata['eligible_for_resume'] and metadata['diagnostic'] is None
        assert metadata['signature']['initial']==m['source_sha256'][str(initial)] and metadata['signature']['spec']==sha(run/'spec.json')
        for p,h in metadata['signature']['code'].items():assert m['source_sha256'][str((ROOT/p).resolve())]==h
        assert sha(folder2/'state.npz')==metadata['payload_sha256'];checkpoint_count+=1
    casebytes=sum(p.stat().st_size for p in run.rglob('*') if p.is_file());assert casebytes<=spec['output_bytes']
    reports.append(dict(case=case['id'],steps=len(accepted),mean_step_ticks=spec['end_tick']/len(accepted),largest_stage_cfl=maximum_cfl,peak_allocated_gpu_bytes=peak,maximum_logged_original_constraint=maximum_constraint,authenticated_checkpoints=checkpoint_count,case_bytes=casebytes,worker_wall_seconds=receipt['wall_seconds'],receipt_sha256=sha(folder/'receipt.json')))
assert specs[1]['max_step_ticks']*2==specs[0]['max_step_ticks'] and specs[1]['cfl']*2==specs[0]['cfl']
assert reports[1]['steps']>reports[0]['steps']
assert (BASE/'production_runtime/first_gate.json').exists();controller=json.loads((BASE/'production_runtime/first_gate.json').read_text())
assert controller['returncode']==75 and controller['wall_timeout_seconds'] is None and controller['cpu_timeout_seconds'] is None
last=json.loads((BASE/'production_runtime/first_gate.stdout').read_text().splitlines()[-1]);assert last['status']=='QUEUE_CHECKPOINT' and last['newly_completed']==3
files={p.resolve() for root in m['storage_roots'] for p in Path(root).rglob('*') if p.is_file()};used=sum(p.stat().st_size for p in files);assert used<=m['output_bytes']<=64*1024**3
result=dict(status='FIRST_THREE_OPERATIONS_PASS',manifest_sha256=sha(mfile),reports=reports,used_production_bytes=used,fine_ceiling_and_CFL_both_halved=True,source_sha256={str(p.relative_to(ROOT)):sha(p) for p in [BASE/'supervise.py',BASE/'production_worker.py',BASE/'capture.py',BASE/'launch_queue.py',BASE/'status.py',Path(__file__)]},scope='Independent receipt/log/checkpoint/hash accounting and actual stage controls; logged original constraints are producer evidence. Separate math reviewer owns original-equation recomputation.')
with (HERE/'FIRST_THREE_OPERATIONS.json').open('x') as f:json.dump(result,f,indent=2);f.write('\n')
print(json.dumps(result,indent=2))
