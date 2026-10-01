"""Actual repaired supervisor control-flow catches with explicit fake children.

All writable fixtures are review-owned. No GPU worker or subprocess is launched;
real subprocess smoke and saved-artifact inspection remain separate evidence.
"""
import contextlib,hashlib,io,json,sys,time,types
from pathlib import Path
from unittest.mock import patch
HERE=Path(__file__).resolve().parent;BASE=HERE.parents[1];ROOT=BASE.parent;SOURCE=BASE/'supervise.py'
def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def write(path,value):path.write_text(json.dumps(value,indent=2)+'\n')
required=[BASE/'supervise.py',BASE/'production_worker.py',BASE/'initial_family.py',
    ROOT/'udt_three_spatial_smoke_2026-10-01/initial_data.py',ROOT/'udt_three_spatial_smoke_2026-10-01/evolution.py',
    ROOT/'udt_three_spatial_smoke_2026-10-01/constraints.py',ROOT/'udt_time_live_smoke_gate_2026-09-30/checkpoint_io.py']
module=types.ModuleType('actual_supervisor');module.__file__=str(SOURCE)
exec(compile(SOURCE.read_text(),str(SOURCE),'exec'),module.__dict__)
dest=HERE/'supervisor_guard_fixtures';dest.mkdir(exist_ok=False);records=[]
cases=[('valid',None),('missing_initial_binding','INITIAL_SOURCE_BINDINGS'),('duplicate_run','DUPLICATE_RUN_PATH'),
    ('nan_deadline','INVALID_SAVED_DEADLINE'),('midqueue_spec_edit','QUEUE_SPEC_CHANGED'),
    ('nan_wall','QUEUE_WALL_LIMIT'),('zero_wall','QUEUE_WALL_LIMIT'),('zero_output','QUEUE_OUTPUT_LIMIT'),
    ('bool_output','QUEUE_OUTPUT_LIMIT'),('empty_cases','QUEUE_CASE_COUNT'),('duplicate_id','QUEUE_CASE_SCHEMA'),
    ('spec_changed','QUEUE_SPEC_CHANGED'),('source_changed','QUEUE_SOURCE_CHANGED'),
    ('missing_code','QUEUE_SOURCE_BINDINGS'),('runtime_unbudgeted','RUNTIME_NOT_BUDGETED'),
    ('missing_receipt','INCOMPLETE_ATTEMPT_REQUIRES_REVIEW'),('prior_failure','DIAGNOSTIC_ATTEMPT_REQUIRES_REVIEW'),
    ('prior_floor','DIAGNOSTIC_ATTEMPT_REQUIRES_REVIEW'),('resume_manifest','QUEUE_RESUME_MISMATCH'),
    ('expired_deadline',75),('output_reserve',75)]
for name,expected in cases:
    folder=dest/name;folder.mkdir();runtime=folder/'runtime';runtime.mkdir()
    spec1=folder/'one.json';spec2=folder/'two.json';config=json.loads((BASE/'specs/engineering.json').read_text())
    write(spec1,config);write(spec2,config)
    run1=BASE/'runs'/('reviewer_virtual_'+name+'_one');run2=BASE/'runs'/('reviewer_virtual_'+name+'_two')
    rows=[dict(id='one',spec=str(spec1),spec_sha256=sha(spec1),run=str(run1))]
    if name in ['valid','duplicate_run','duplicate_id','midqueue_spec_edit']:
        rows.append(dict(id='one' if name=='duplicate_id' else 'two',spec=str(spec2),spec_sha256=sha(spec2),run=str(run1 if name=='duplicate_run' else run2)))
    bindings={str(path):sha(path) for path in required}
    if name!='missing_initial_binding':bindings[str(ROOT/config['initial'])]=sha(ROOT/config['initial'])
    m=dict(wall_seconds=10,output_bytes=1024**3,storage_roots=[str(runtime),str(run1),str(run2)],source_sha256=bindings,cases=rows)
    if name=='nan_wall':m['wall_seconds']=float('nan')
    if name=='zero_wall':m['wall_seconds']=0
    if name=='zero_output':m['output_bytes']=0
    if name=='bool_output':m['output_bytes']=True
    if name=='empty_cases':m['cases']=[]
    if name=='spec_changed':m['cases'][0]['spec_sha256']='0'*64
    if name=='source_changed':m['source_sha256'][str(SOURCE)]='0'*64
    if name=='missing_code':del m['source_sha256'][str(SOURCE)]
    if name=='runtime_unbudgeted':m['storage_roots']=[str(run1),str(run2)]
    if name=='output_reserve':m['output_bytes']=10
    manifest=folder/'manifest.json';write(manifest,m)
    if name in ['nan_deadline','expired_deadline']:
        write(runtime/'wall_budget.json',dict(deadline_unix=float('nan') if name=='nan_deadline' else time.time()-1,manifest_sha256=sha(manifest)))
    if name in ['missing_receipt','prior_failure','prior_floor']:
        attempt=runtime/'attempts/00000_prior';attempt.mkdir(parents=True)
        if name!='missing_receipt':write(attempt/'receipt.json',dict(case='one',returncode=2 if name=='prior_failure' else 75,worker_stop_reason='TIMESTEP_FLOOR',wall_seconds=.1))
    if name=='resume_manifest':(runtime/'manifest.sha256').write_text('0'*64+'\n')
    launched=[]
    class FakeProcess:
        def __init__(self,command,stdout,stderr,**kwargs):
            launched.append(command);stdout.write(json.dumps(dict(status='TPP1_RUN_COMPLETE',tick=320))+'\n');stdout.flush()
        def poll(self):return 0
        def wait(self):
            if name=='midqueue_spec_edit' and len(launched)==1:write(spec2,dict(config,cfl=.1))
            return 0
    output=io.StringIO();error=None;result=None
    with patch.object(sys,'argv',['supervise.py',str(manifest),str(runtime)]),patch.object(module.subprocess,'Popen',FakeProcess),contextlib.redirect_stdout(output):
        try:result=module.main()
        except (ValueError,RuntimeError) as exc:error=str(exc)
    if expected is None:assert result==0 and len(launched)==2 and error is None
    elif isinstance(expected,int):assert result==expected and not launched and error is None
    else:assert error==expected and len(launched)==(1 if name=='midqueue_spec_edit' else 0),(name,error,result,launched)
    (folder/'captured_stdout').write_text(output.getvalue())
    records.append(dict(case=name,result=result,error=error,fake_child_count=len(launched),no_real_subprocess=True))
print(json.dumps(dict(status='REPAIRED_SUPERVISOR_GUARDS_PASS',source_sha256=sha(SOURCE),records=records,
    scope='Actual supervisor main with review-owned fixtures and replaced Popen; not GPU or full-process signal evidence.'),indent=2))
