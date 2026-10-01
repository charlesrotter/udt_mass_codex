"""CPU control-flow counterexamples against the saved initial supervisor.

All runtime/spec edits are review-owned; Popen is replaced by an explicit fake
child and no worker or GPU process is launched. This is a control-flow proof,
not evidence of an actual production failure.
"""
import contextlib,hashlib,io,json,sys,time,types
from pathlib import Path
from unittest.mock import patch
HERE=Path(__file__).resolve().parent;BASE=HERE.parents[1];ROOT=BASE.parent
SOURCE=HERE/'initial_implementation/supervise.py'
def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def write(path,value):path.write_text(json.dumps(value,indent=2)+'\n')
required=[BASE/'supervise.py',BASE/'production_worker.py',ROOT/'udt_three_spatial_smoke_2026-10-01/evolution.py',ROOT/'udt_three_spatial_smoke_2026-10-01/constraints.py',ROOT/'udt_time_live_smoke_gate_2026-09-30/checkpoint_io.py']
module=types.ModuleType('saved_supervisor');module.__file__=str(BASE/'supervise.py')
exec(compile(SOURCE.read_text(),str(BASE/'supervise.py'),'exec'),module.__dict__)
dest=HERE/'supervisor_initial_proofs';dest.mkdir(exist_ok=False);records=[]
for name in ['missing_initial_binding','duplicate_run','nan_deadline','midqueue_spec_edit']:
    folder=dest/name;folder.mkdir();runtime=folder/'runtime';runtime.mkdir()
    spec1=folder/'one.json';spec2=folder/'two.json'
    config=json.loads((BASE/'specs/engineering.json').read_text());write(spec1,config);write(spec2,config)
    run1=BASE/'runs'/('reviewer_virtual_'+name+'_one');run2=BASE/'runs'/('reviewer_virtual_'+name+'_two')
    cases=[dict(id='one',spec=str(spec1),spec_sha256=sha(spec1),run=str(run1))]
    if name in ['duplicate_run','midqueue_spec_edit']:
        cases.append(dict(id='two',spec=str(spec2),spec_sha256=sha(spec2),run=str(run1 if name=='duplicate_run' else run2)))
    bindings={str(path):sha(path) for path in required}
    if name!='missing_initial_binding':bindings[str(ROOT/config['initial'])]=sha(ROOT/config['initial'])
    manifest=folder/'manifest.json';write(manifest,dict(wall_seconds=10,output_bytes=1024**3,
        storage_roots=[str(runtime),str(run1),str(run2)],source_sha256=bindings,cases=cases))
    if name=='nan_deadline':write(runtime/'wall_budget.json',dict(deadline_unix=float('nan'),manifest_sha256=sha(manifest)))
    launched=[]
    class FakeProcess:
        def __init__(self,command,stdout,stderr,**kwargs):
            launched.append(command);stdout.write(json.dumps(dict(status='TPP1_RUN_COMPLETE',tick=320))+'\n');stdout.flush()
        def poll(self):return 0
        def wait(self):
            if name=='midqueue_spec_edit' and len(launched)==1:
                changed=dict(config,cfl=.1);write(spec2,changed)
            return 0
    with patch.object(sys,'argv',['supervise.py',str(manifest),str(runtime)]),patch.object(module.subprocess,'Popen',FakeProcess),contextlib.redirect_stdout(io.StringIO()):
        result=module.main()
    assert result==0 and len(launched)==len(cases)
    records.append(dict(case=name,status='PRE_REPAIR_GUARD_ACCEPTED',fake_child_count=len(launched),
        source_sha256=sha(SOURCE),no_real_subprocess=True))
print(json.dumps(dict(status='PRE_REPAIR_SUPERVISOR_COUNTEREXAMPLES',records=records),indent=2))
