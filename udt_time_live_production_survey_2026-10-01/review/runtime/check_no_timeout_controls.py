"""Authored-edition regression: actual supervisor flow with explicit fake children.

No GPU or production initial-data emission. Synthetic monotonic increments one
 day per call, so legacy elapsed limits would fail the valid control. AST checks
 compare scientific functions; parent owns independent source review.
"""
import ast,contextlib,copy,hashlib,importlib.util,io,json,os,resource,signal,sys,types
from pathlib import Path
from unittest.mock import patch
resource.setrlimit(resource.RLIMIT_AS,(2*1024**3,2*1024**3))
HERE=Path(__file__).resolve().parent;BASE=HERE.parents[1];ROOT=BASE.parent;OLD=ROOT/'udt_time_live_production_preparation_2026-10-01'
def sha(q):return hashlib.sha256(Path(q).read_bytes()).hexdigest()
def write(q,x):
    with Path(q).open('x') as f:json.dump(x,f,indent=2);f.write('\n')
def module(name,path):
    mod=types.ModuleType(name);mod.__file__=str(path);exec(compile(path.read_text(),str(path),'exec'),mod.__dict__);return mod
source=BASE/'supervise.py';sup=module('actual_supervisor',source);worker=module('actual_worker',BASE/'production_worker.py')
oldtree=ast.parse((OLD/'production_worker.py').read_text());newtree=ast.parse((BASE/'production_worker.py').read_text())
def fn(tree,name):return next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name==name)
scientific={name:ast.dump(fn(oldtree,name))==ast.dump(fn(newtree,name)) for name in ['positive_int','geometry_bound','checked_rk4']}
assert all(scientific.values())
reason=next(n.value for n in ast.walk(fn(newtree,'main')) if isinstance(n,ast.Assign) and len(n.targets)==1 and isinstance(n.targets[0],ast.Name) and n.targets[0].id=='reason')
reason_code=compile(ast.Expression(reason),'<actual-worker-stop-expression>','eval')
reason_checks=[]
for s,p,steps,expected in [(None,0,999999,None),(None,3,3,'REQUESTED_PAUSE'),(15,0,999999,'SIGNAL')]:
    value=eval(reason_code,dict(stop={'signal':s},args=types.SimpleNamespace(pause_after=p),steps=steps,time=types.SimpleNamespace(monotonic=lambda:10**12),start=0,spec={'wall_seconds':None}))
    assert value==expected;reason_checks.append(dict(signal=s,pause_after=p,steps=steps,result=value))
oldreason=next(n.value for n in ast.walk(fn(oldtree,'main')) if isinstance(n,ast.Assign) and len(n.targets)==1 and isinstance(n.targets[0],ast.Name) and n.targets[0].id=='reason')
assert eval(compile(ast.Expression(oldreason),'<legacy-time-stop>','eval'),dict(stop={'signal':None},args=types.SimpleNamespace(pause_after=0),steps=999999,time=types.SimpleNamespace(monotonic=lambda:10**12),start=0,spec={'wall_seconds':150}))=='WALL_LIMIT'
# Both recipes must be numerically identical, not only the same case count.
sys.path.insert(0,str(BASE));newgen=module('new_generator',BASE/'prepare_campaign.py');oldgen=module('old_generator',OLD/'prepare_campaign.py')
assert newgen.families()==oldgen.families() and len(newgen.families())==78
fixed_family=module('fixed_family',OLD/'initial_family.py');adapter=module('adapter',BASE/'initial_family.py')
assert adapter.construct.__code__.co_code==fixed_family.construct.__code__.co_code
assert adapter.tt_tensor.__code__.co_code==fixed_family.tt_tensor.__code__.co_code
required=[BASE/'supervise.py',BASE/'production_worker.py',BASE/'initial_family.py',OLD/'initial_family.py',ROOT/'udt_three_spatial_smoke_2026-10-01/initial_data.py',ROOT/'udt_three_spatial_smoke_2026-10-01/evolution.py',ROOT/'udt_three_spatial_smoke_2026-10-01/constraints.py',ROOT/'udt_time_live_smoke_gate_2026-09-30/checkpoint_io.py']
dest=HERE/'guard_fixtures';dest.mkdir(exist_ok=False);initialroot=BASE/'initial/runtime_review';initialroot.mkdir(parents=True,exist_ok=False)
records=[];worker_guards=[]
cases=[('long_elapsed',None),('manual_signal',75),('missing_initial_binding','INITIAL_SOURCE_BINDINGS'),('duplicate_run','DUPLICATE_RUN_PATH'),('midqueue_spec_edit','QUEUE_SPEC_CHANGED'),('wall_present','QUEUE_TIME_LIMIT_NOT_AUTHORIZED'),('wall_nan','QUEUE_TIME_LIMIT_NOT_AUTHORIZED'),('zero_output','QUEUE_OUTPUT_LIMIT'),('bool_output','QUEUE_OUTPUT_LIMIT'),('empty_cases','QUEUE_CASE_COUNT'),('too_many_cases','QUEUE_CASE_COUNT'),('duplicate_id','QUEUE_CASE_SCHEMA'),('spec_changed','QUEUE_SPEC_CHANGED'),('source_changed','QUEUE_SOURCE_CHANGED'),('missing_code','QUEUE_SOURCE_BINDINGS'),('runtime_unbudgeted','RUNTIME_NOT_BUDGETED'),('missing_receipt','INCOMPLETE_ATTEMPT_REQUIRES_REVIEW'),('prior_failure','DIAGNOSTIC_ATTEMPT_REQUIRES_REVIEW'),('prior_floor','DIAGNOSTIC_ATTEMPT_REQUIRES_REVIEW'),('prior_wall','DIAGNOSTIC_ATTEMPT_REQUIRES_REVIEW'),('resume_manifest','QUEUE_RESUME_MISMATCH'),('output_reserve',75)]
for name,expected in cases:
    folder=dest/name;folder.mkdir();runtime=folder/'runtime';runtime.mkdir()
    initial=initialroot/(name+'.npz');initial.write_bytes((OLD/'initial/axial1_n8.npz').read_bytes())
    config=json.loads((OLD/'specs/engineering.json').read_text());config['initial']=str(initial.relative_to(ROOT));config['wall_seconds']=None
    spec1=folder/'one.json';spec2=folder/'two.json';write(spec1,config);write(spec2,config)
    run1=BASE/'runs'/('reviewer_virtual_'+name+'_one');run2=BASE/'runs'/('reviewer_virtual_'+name+'_two')
    rows=[dict(id='one',spec=str(spec1),spec_sha256=sha(spec1),run=str(run1))]
    if name in ['long_elapsed','duplicate_run','duplicate_id','midqueue_spec_edit']:
        rows.append(dict(id='one' if name=='duplicate_id' else 'two',spec=str(spec2),spec_sha256=sha(spec2),run=str(run1 if name=='duplicate_run' else run2)))
    bindings={str(q):sha(q) for q in required}
    if name!='missing_initial_binding':bindings[str(initial)]=sha(initial)
    m=dict(wall_seconds=None,output_bytes=1024**3,storage_roots=[str(runtime),str(run1),str(run2)],source_sha256=bindings,cases=rows)
    if name=='wall_present':m['wall_seconds']=21600
    if name=='wall_nan':m['wall_seconds']=float('nan')
    if name=='zero_output':m['output_bytes']=0
    if name=='bool_output':m['output_bytes']=True
    if name=='empty_cases':m['cases']=[]
    if name=='too_many_cases':m['cases']=rows*235
    if name=='spec_changed':m['cases'][0]['spec_sha256']='0'*64
    if name=='source_changed':m['source_sha256'][str(source)]='0'*64
    if name=='missing_code':del m['source_sha256'][str(source)]
    if name=='runtime_unbudgeted':m['storage_roots']=[str(run1),str(run2)]
    if name=='output_reserve':m['output_bytes']=10
    manifest=folder/'manifest.json';write(manifest,m)
    if name in ['missing_receipt','prior_failure','prior_floor','prior_wall']:
        attempt=runtime/'attempts/00000_prior';attempt.mkdir(parents=True)
        if name!='missing_receipt':write(attempt/'receipt.json',dict(case='one',returncode=2 if name=='prior_failure' else 75,worker_stop_reason='WALL_LIMIT' if name=='prior_wall' else 'TIMESTEP_FLOOR',wall_seconds=.1))
    if name=='resume_manifest':(runtime/'manifest.sha256').write_text('0'*64+'\n')
    launched=[];signals=[];handlers={};clock=[0.]
    def monotonic():clock[0]+=86400.;return clock[0]
    class FakeProcess:
        pid=987654
        def __init__(self,command,stdout,stderr,**kwargs):
            launched.append(command);self.polls=0
            stdout.write(json.dumps(dict(status='CHECKPOINTED_STOP' if name=='manual_signal' else 'TPS1_RUN_COMPLETE',tick=320,reason='SIGNAL' if name=='manual_signal' else None))+'\n');stdout.flush()
        def poll(self):
            self.polls+=1
            if self.polls==1:
                if name=='manual_signal':handlers[signal.SIGTERM](signal.SIGTERM,None)
                return None
            return 75 if name=='manual_signal' else 0
        def wait(self):
            if name=='midqueue_spec_edit' and len(launched)==1:spec2.write_text(json.dumps(dict(config,cfl=.1)))
            return 75 if name=='manual_signal' else 0
    output=io.StringIO();error=None;result=None
    with patch.object(sys,'argv',['supervise.py',str(manifest),str(runtime)]),patch.object(sup.subprocess,'Popen',FakeProcess),patch.object(sup.time,'monotonic',monotonic),patch.object(sup.time,'sleep',lambda _:None),patch.object(sup.os,'killpg',lambda pid,s:signals.append(s)),patch.object(sup.signal,'signal',lambda s,h:handlers.__setitem__(s,h)),contextlib.redirect_stdout(output):
        try:result=sup.main()
        except (ValueError,RuntimeError) as exc:error=str(exc)
    if expected is None:assert result==0 and len(launched)==2 and error is None and not signals
    elif isinstance(expected,int):assert result==expected and len(launched)==(1 if name=='manual_signal' else 0) and error is None
    else:assert error==expected and len(launched)==(1 if name=='midqueue_spec_edit' else 0),(name,error,result,launched)
    assert not (runtime/'wall_budget.json').exists()
    assert signals==([signal.SIGTERM] if name=='manual_signal' else [])
    for p in (runtime/'attempts').glob('*/receipt.json'):
        r=json.loads(p.read_text())
        if p.parent.name!='00000_prior':assert r['wall_seconds']>=86400 and not r['sigkill_sent']
    (folder/'captured_stdout').write_text(output.getvalue())
    records.append(dict(case=name,result=result,error=error,fake_children=len(launched),signals=signals,synthetic_clock_seconds=clock[0]))
    if name=='long_elapsed':
        saves,checks,_=worker.validate(config);assert saves[-1]==320
        worker_guards.append(dict(case='null_wall_accepted',result='PASS'))
        for key,value,reason in [('wall_seconds',150,'TIME_LIMIT_NOT_AUTHORIZED'),('wall_seconds',float('nan'),'TIME_LIMIT_NOT_AUTHORIZED'),('gpu_bytes',8*1024**3+1,'INVALID_GPU_BUDGET'),('output_bytes',512*1024**2+1,'INVALID_OUTPUT_BUDGET'),('constraint_limit',3e-5,'INVALID_CONSTRAINT_LIMIT'),('n',7,'INVALID_GRID')]:
            mutated=copy.deepcopy(config);mutated[key]=value
            try:worker.validate(mutated)
            except ValueError as exc:assert str(exc)==reason
            else:raise AssertionError((key,value,'MISSING_GUARD'))
            worker_guards.append(dict(key=key,expected=reason,result='CAUGHT'))
result=dict(status='NO_TIMEOUT_CONTROLS_PASS',context='/root/survey_runtime, adapter author; regression not independent source review',scientific_functions_AST_equal=scientific,recipe_equal_all78=True,imported_initial_function_bytecode_equal=True,worker_stop_expression=reason_checks,legacy_time_branch_mutation_detected=True,worker_guards=worker_guards,supervisor_controls=records,source_sha256={str(p.relative_to(ROOT)):sha(p) for p in required+[BASE/'prepare_campaign.py',BASE/'assemble_windows.py',BASE/'assemble_campaign.py',Path(__file__)]},scope='CPU actual validation/main control flow with fake children and one-day synthetic clock increments. No GPU, process interruption, checkpoint physics or production emission claim.')
write(HERE/'NO_TIMEOUT_CONTROLS.json',result);print(json.dumps(result,indent=2))
