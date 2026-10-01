"""Finite orchestration controls with synthetic children/data, no production writes.

Real first-three receipts are also checked as an intentionally incomplete queue.
No synthetic clock data is scientific evidence.
"""
import contextlib,copy,hashlib,io,json,os,resource,signal,sys,types
from pathlib import Path
from unittest.mock import patch
resource.setrlimit(resource.RLIMIT_AS,(2*1024**3,2*1024**3))
HERE=Path(__file__).resolve().parent;BASE=HERE.parents[1];ROOT=BASE.parent;SOURCE=BASE/'postprocess.py'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def write(p,v):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(v,indent=2)+'\n')
mod=types.ModuleType('actual_companion');mod.__file__=str(SOURCE);exec(compile(SOURCE.read_text(),str(SOURCE),'exec'),mod.__dict__)
dest=HERE/'postprocess_fixtures';dest.mkdir(exist_ok=False);real_manifest=json.loads((BASE/'production_runtime/campaign.json').read_text());records=[]
stat=Path('/proc/self/stat').read_text().rsplit(')',1)[1].split();identity=dict(pid=os.getpid(),proc_start_ticks=stat[19]);assert mod.process_alive(identity)
assert not mod.process_alive(dict(identity,proc_start_ticks=str(int(stat[19])+1)))
# Actual currently completed first-three records cannot satisfy the full queue gate.
anchor=dest/'actual_first_three';(anchor/'attempts').mkdir(parents=True)
for original in sorted((BASE/'production_runtime/attempts').iterdir())[:3]:
    d=anchor/'attempts'/original.name;d.mkdir()
    for name in ['receipt.json','launch.json','stdout','stderr']:(d/name).write_bytes((original/name).read_bytes())
real_manifest['_sha256']=sha(BASE/'production_runtime/campaign.json')
try:mod.successful_queue(real_manifest,anchor)
except ValueError as exc:assert str(exc)=='INCOMPLETE_QUEUE'
else:raise AssertionError('Three accepted as234')
records.append(dict(case='actual_first_three_not_full',result='CAUGHT_INCOMPLETE_QUEUE'))
# Actual successful_queue body: complete synthetic234, and command/hash/diagnostic catches.
queue=dest/'synthetic_queue';(queue/'attempts').mkdir(parents=True);m={'cases':[{'id':f'case_{i}'} for i in range(234)],'_sha256':'manifest'}
for i in range(234):
    d=queue/'attempts'/f'{i:05d}';d.mkdir();(d/'stdout').write_text('{}\n');(d/'stderr').write_text('')
    command=['synthetic-worker',str(i)];write(d/'launch.json',dict(case=f'case_{i}',command=command,manifest_sha256='manifest'))
    write(d/'receipt.json',dict(case=f'case_{i}',command=command,returncode=0,worker_status='TPS1_RUN_COMPLETE',stdout_sha256=sha(d/'stdout'),stderr_sha256=sha(d/'stderr')))
assert len(mod.successful_queue(m,queue))==234
p=queue/'attempts/00000/receipt.json';original=json.loads(p.read_text())
for key,value,error in [('command',['changed'],'ATTEMPT_BINDING'),('stdout_sha256','wrong','ATTEMPT_STREAM_CHANGED'),('returncode',2,'DIAGNOSTIC_ATTEMPT')]:
    changed=dict(original);changed[key]=value;write(p,changed)
    try:mod.successful_queue(m,queue)
    except ValueError as exc:assert str(exc)==error
    else:raise AssertionError(error)
    records.append(dict(case='queue_'+key,caught=error))
write(p,original)
# Actual main flow; only process liveness, child execution and scientific helpers are synthetic.
for name in ['complete','manual_wait','controller_pause','controller_failure','missing_receipt','bad_controller_command','stage_nonzero','stage_hash_bad','manual_launch_race','storage_limit']:
    base=dest/name;runtime=base/'production_runtime';analysis=base/'production_analysis';runtime.mkdir(parents=True);analysis.mkdir()
    manifest={'wall_seconds':None,'output_bytes':64*1024**3,'storage_roots':[str(runtime),str(analysis)],'cases':real_manifest['cases']};mp=runtime/'campaign.json';write(mp,manifest)
    if name=='storage_limit':manifest['output_bytes']=1;write(mp,manifest)
    prefix=runtime/'continuation';launch_path=runtime/'continuation.launch.json';child=[sys.executable,str(base/'supervise.py'),str(mp),str(runtime)]
    launch=dict(pid=987654,proc_start_ticks='12345',result_receipt=str(prefix)+'.json',manifest_sha256=sha(mp),command=[sys.executable,str(base/'capture.py'),'--gpu',str(prefix),*child]);write(launch_path,launch)
    (runtime/'continuation.stdout').write_text('{}\n');(runtime/'continuation.stderr').write_text('')
    controller=dict(returncode=75 if name=='controller_pause' else 2 if name=='controller_failure' else 0,command=['wrong'] if name=='bad_controller_command' else child,wall_timeout_seconds=None,cpu_timeout_seconds=None,stdout_sha256=sha(runtime/'continuation.stdout'),stderr_sha256=sha(runtime/'continuation.stderr'))
    if name!='missing_receipt':write(runtime/'continuation.json',controller)
    write(base/'POSTPROCESS_DISPATCH.json',dict(manifest_sha256=sha(mp),source_sha256={str(SOURCE.relative_to(ROOT)):sha(SOURCE)}))
    handlers={};signals=[];sleep_count=[0];launch_count=[0];alive_count=[0]
    def alive(_):alive_count[0]+=1;return alive_count[0]<=2
    def sleep(_):
        sleep_count[0]+=1
        if name=='manual_wait':handlers[signal.SIGTERM](signal.SIGTERM,None)
    class FakeProcess:
        pid=123456
        def __init__(self,command,stdout,stderr,**kwargs):
            launch_count[0]+=1;self.code=2 if name=='stage_nonzero' else 75 if name=='manual_launch_race' else 0
            prefix=Path(command[2]);prefix.with_suffix('.stdout').write_text('{}\n');prefix.with_suffix('.stderr').write_text('')
            receipt=dict(returncode=self.code,command=command[3:],wall_timeout_seconds=None,cpu_timeout_seconds=None,stdout_sha256='wrong' if name=='stage_hash_bad' else sha(prefix.with_suffix('.stdout')),stderr_sha256=sha(prefix.with_suffix('.stderr')));write(prefix.with_suffix('.json'),receipt)
            if name=='manual_launch_race':handlers[signal.SIGTERM](signal.SIGTERM,None)
        def poll(self):return None
        def wait(self):return self.code
    out=io.StringIO()
    with patch.object(mod,'B',base),patch.object(sys,'argv',['postprocess.py',str(launch_path)]),patch.object(mod,'process_alive',alive),patch.object(mod.time,'sleep',sleep),patch.object(mod.signal,'signal',lambda s,h:handlers.__setitem__(s,h)),patch.object(mod.os,'killpg',lambda pid,s:signals.append(s)),patch.object(mod.subprocess,'Popen',FakeProcess),patch.object(mod,'successful_queue',lambda *_:[{'synthetic_success':234}]),patch.object(mod,'compare_clocks',lambda *_:True),contextlib.redirect_stdout(out):rc=mod.main()
    result=json.loads((analysis/'postprocess/POSTPROCESS_RESULT.json').read_text());phase=result['phase']
    expected={'complete':(0,'FINITE_CHECK_PIPELINE_COMPLETE',5),'manual_wait':(75,'MANUAL_PAUSE',0),'controller_pause':(75,'CONTROLLER_STOPPED_OR_DIAGNOSTIC',0),'controller_failure':(2,'CONTROLLER_STOPPED_OR_DIAGNOSTIC',0),'missing_receipt':(2,'CONTROLLER_RECEIPT_MISSING',0),'bad_controller_command':(2,'UNRESOLVED_ERROR',0),'stage_nonzero':(2,'CHECK_STOPPED_OR_DIAGNOSTIC',1),'stage_hash_bad':(2,'UNRESOLVED_ERROR',1),'manual_launch_race':(75,'MANUAL_PAUSE',1),'storage_limit':(2,'OUTPUT_LIMIT_BEFORE_ANALYSIS',0)}[name]
    assert (rc,phase,launch_count[0])==expected,(name,rc,phase,launch_count[0],result)
    assert result['status']=='CANDIDATE_PENDING_ADVERSARIAL_REVIEW'
    assert signals==([signal.SIGTERM] if name=='manual_launch_race' else [])
    (base/'captured_stdout').write_text(out.getvalue());records.append(dict(case=name,returncode=rc,phase=phase,stages=launch_count[0],forwarded_signals=signals,simulated_wait_polls=sleep_count[0]))
# Actual clock comparator on small synthetic payloads: all234signs plus30subset, method/hash/NaN and difference catches.
base=dest/'clock_compare';analysis=base/'production_analysis';queries=json.loads((BASE/'review/runtime/SUBSET_CLOCK_QUERIES.json').read_text());write(base/'review/runtime/SUBSET_CLOCK_QUERIES.json',queries)
dispatch=json.loads((BASE/'CLOCK_DISPATCH.json').read_text());write(base/'CLOCK_DISPATCH.json',dispatch)
producer={};own={};history_hashes={};signs=[-.01,.02,0.,.003]
directions=[[1.,0.,0.],[0.,1.,0.],[0.,0.,1.],[3**-.5]*3]
for row in real_manifest['cases']:
    name=row['id'];folder=analysis/name;history=folder/'histories'/(name+'_window2.npz');history.parent.mkdir(parents=True);history.write_bytes(('synthetic:'+name).encode());rays=[]
    for d,z in zip(directions,signs):rays.append(dict(te=2.484,to=2.496,Z=1.,logZ=z,max_sampled_abs_null_norm=0.,initial_coordinate_direction=d,emitter_position=[.31,.47,.19],receiver_position=[1.,2.,3.]))
    data=dict(status='FINITE_CLOCK_CHECK_PASS',history_sha256=sha(history),readouts=rays);write(folder/'clock.json',data);producer[name]=data
for row in queries['cases']:
    name=row['name'];history_hashes[row['history']]=producer[name]['history_sha256'];own[name]=[dict(emission=x['te'],reception=x['to'],Z=x['Z'],logZ=x['logZ'],max_sampled_abs_null_norm=0.,initial_coordinate_direction=x['initial_coordinate_direction'],receiver_position=x['receiver_position']) for x in producer[name]['readouts']]
independent=dict(status='HAMILTON_CLOCK_REVIEW_PASS',queries_sha256=sha(base/'review/runtime/SUBSET_CLOCK_QUERIES.json'),checker_sha256=sha(mod.TPP/'review/runtime/check_clock_hamilton.py'),readouts=own,history_sha256=history_hashes);ip=base/'independent.json';write(ip,independent)
with patch.object(mod,'B',base):assert mod.compare_clocks(real_manifest,analysis,ip,base/'good.json')
good=json.loads((base/'good.json').read_text());assert len(good['all_supplied_signs'])==234 and {x['sign'] for x in next(iter(good['all_supplied_signs'].values()))}=={'positive','negative','zero'}
for name,error in [('nan_null','INDEPENDENT_CLOCK_VALIDITY'),('nan_endpoint','INDEPENDENT_CLOCK_VALIDITY'),('changed_query','INDEPENDENT_METHOD_OR_QUERIES'),('changed_checker','INDEPENDENT_METHOD_OR_QUERIES')]:
    bad=copy.deepcopy(independent);first=next(iter(bad['readouts']))
    if name=='nan_null':bad['readouts'][first][0]['max_sampled_abs_null_norm']=float('nan')
    if name=='nan_endpoint':bad['readouts'][first][0]['receiver_position'][0]=float('nan')
    if name=='changed_query':bad['queries_sha256']='wrong'
    if name=='changed_checker':bad['checker_sha256']='wrong'
    path=base/(name+'.json');write(path,bad)
    with patch.object(mod,'B',base):
        try:mod.compare_clocks(real_manifest,analysis,path,base/(name+'_result.json'))
        except ValueError as exc:assert str(exc)==error,(name,exc)
        else:raise AssertionError(name)
    records.append(dict(case=name,caught=error))
bad=copy.deepcopy(independent);bad['readouts'][next(iter(bad['readouts']))][0]['logZ']+=1e-3;write(base/'difference.json',bad)
with patch.object(mod,'B',base):assert not mod.compare_clocks(real_manifest,analysis,base/'difference.json',base/'difference_result.json')
assert json.loads((base/'difference_result.json').read_text())['machine_diagnostic']=='FAIL';records.append(dict(case='clock_difference',result='FAIL_RETAINED_AS_CANDIDATE'))
result=dict(status='POSTPROCESS_FINITE_CONTROLS_PASS',source_sha256=sha(SOURCE),actual_first_three_incomplete_guard=True,current_PID_identity_checked=True,records=records,scope='Actual control-flow with fakeprocesses and synthetic234clock/receiptfixtures; realfirst3anchor. No GPU, production writes, new equation checks or fullsurvey qualification.')
write(HERE/'POSTPROCESS_CONTROLS.json',result);print(json.dumps(result,indent=2))
