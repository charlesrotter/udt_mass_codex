"""Independent aggregation of actual frozen-worker receipts and load telemetry."""
import hashlib,json
from pathlib import Path
HERE=Path(__file__).resolve().parent;BASE=HERE.parents[1];ROOT=BASE.parent
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
records=[];wall=0
for path in sorted((BASE/'invocations').glob('*.json')):
    receipt=json.loads(path.read_text());wall+=receipt['wall_seconds']
    assert not receipt['timeout'] and receipt['wall_seconds']<180
    assert sha(path.with_suffix('.stdout'))==receipt['stdout_sha256']
    assert sha(path.with_suffix('.stderr'))==receipt['stderr_sha256']
    spec=json.loads(Path(receipt['command'][2]).read_text())
    run=Path(receipt['command'][3]);size=sum(q.stat().st_size for q in run.rglob('*') if q.is_file())
    assert size<=spec['output_bytes']
    rows=[json.loads(line) for line in path.with_suffix('.stdout').read_text().splitlines()]
    checked=[r for r in rows if r['status']=='CHECKED_STATE']
    peak=max(r['gpu_allocated_peak'] for r in checked)
    reserved=max(r['gpu_reserved'] for r in checked);device=max(r['device_used_bytes'] for r in checked)
    assert peak<=spec['gpu_bytes']
    records.append(dict(name=path.stem,wall_seconds=receipt['wall_seconds'],run_bytes=size,
        max_torch_allocated=peak,max_torch_reserved=reserved,max_device_used=device,
        receipt_sha256=sha(path),returncode=receipt['returncode']))
assert wall<600
load=next(r for r in records if r['name']=='load_n48')
assert 30<=load['wall_seconds']<=60 and load['returncode']==0
loadlog=[json.loads(line) for line in (BASE/'invocations/load_n48.stdout').read_text().splitlines()]
done=loadlog[-1];assert done['status']=='TPP1_RUN_COMPLETE' and done['tick']==1600
rejected=[r for r in loadlog if r['status']=='REJECTED_TRIAL_STEP']
assert done['retries']==len(rejected)
size=sum(q.stat().st_size for q in BASE.rglob('*') if q.is_file());assert size<2*1024**3
print(json.dumps(dict(status='MEASURED_RESOURCE_REVIEW_PASS',worker_count=len(records),
    summed_worker_wall_seconds=wall,package_bytes_at_review=size,records=records,
    sustained_load=dict(**load,accepted_steps=done['steps'],minimum_step_ticks=done['min_step_ticks'],
        maximum_step_ticks=done['max_step_ticks'],max_stage_cfl=done['max_stage_cfl'],
        rejected_trials=rejected),
    scope='Aggregation of captured process wall and CUDA telemetry; no total-device profiler or extrapolated long-run stability.48cubed is load-only.'),indent=2,sort_keys=True))
