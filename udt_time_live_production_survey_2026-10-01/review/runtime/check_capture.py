"""Separate-context test of parent-authored no-timeout capture wrapper."""
import ast,hashlib,json,os,resource,signal,subprocess,sys,time,types
from pathlib import Path
from unittest.mock import patch
resource.setrlimit(resource.RLIMIT_AS,(2*1024**3,2*1024**3))
HERE=Path(__file__).resolve().parent;BASE=HERE.parents[1];SOURCE=BASE/'capture.py'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def write(p,v):
    with p.open('x') as f:json.dump(v,f,indent=2);f.write('\n')
folder=HERE/'capture_fixtures';folder.mkdir(exist_ok=False)
child=folder/'child.py';child.write_text('''import json,resource,signal,sys,time
requested=[]
def stop(s,f):requested.append(s)
signal.signal(signal.SIGTERM,stop)
print(json.dumps({'ready':True,'cpu_limit':resource.getrlimit(resource.RLIMIT_CPU),'as_limit':resource.getrlimit(resource.RLIMIT_AS)}),flush=True)
if sys.argv[1]=='delay':time.sleep(.25)
else:
    while not requested:time.sleep(.01)
print(json.dumps({'complete':True,'signals':requested}),flush=True)
raise SystemExit(75 if requested else 0)
''')
records=[]
for name in ['delay','signal']:
    prefix=folder/name;command=[sys.executable,str(SOURCE),str(prefix),sys.executable,str(child),name]
    with (folder/(name+'.wrapper_stdout')).open('x') as out,(folder/(name+'.wrapper_stderr')).open('x') as err:
        proc=subprocess.Popen(command,stdout=out,stderr=err)
        if name=='signal':
            while proc.poll() is None:
                if Path(str(prefix)+'.stdout').exists() and 'ready' in Path(str(prefix)+'.stdout').read_text():break
                time.sleep(.01)
            assert proc.poll() is None
            os.kill(proc.pid,signal.SIGTERM)
        rc=proc.wait()
    receipt=json.loads(Path(str(prefix)+'.json').read_text());lines=[json.loads(s) for s in Path(str(prefix)+'.stdout').read_text().splitlines()]
    assert rc==(75 if name=='signal' else 0)==receipt['returncode']
    assert receipt['wall_timeout_seconds'] is None and receipt['cpu_timeout_seconds'] is None
    assert receipt['forwarded_signals']==([15] if name=='signal' else [])
    assert lines[0]['cpu_limit']==[-1,-1] and lines[0]['as_limit']==[2*1024**3]*2
    assert lines[-1]['complete'] and lines[-1]['signals']==([15] if name=='signal' else [])
    assert receipt['stdout_sha256']==sha(Path(str(prefix)+'.stdout')) and receipt['stderr_sha256']==sha(Path(str(prefix)+'.stderr')) and receipt['capture_sha256']==sha(SOURCE)
    if name=='delay':assert receipt['duration_seconds']>=.25
    records.append(dict(case=name,command=command,receipt_sha256=sha(Path(str(prefix)+'.json')),returncode=rc,elapsed_seconds=receipt['duration_seconds']))
mod=types.ModuleType('capture_actual');mod.__file__=str(SOURCE);exec(compile(SOURCE.read_text(),str(SOURCE),'exec'),mod.__dict__)
catches=[]
for name,args,limits,expected in [('invalid_memory',['--memory-mib','4097'],(-1,-1),'CAPTURE_SCHEMA'),('inherited_cpu',[],(180,180),'INHERITED_CPU_TIMEOUT_REQUIRES_REVIEW'),('overwrite',[],(-1,-1),'REFUSE_CAPTURE_OVERWRITE')]:
    prefix=folder/'delay' if name=='overwrite' else folder/name
    with patch.object(sys,'argv',['capture.py',*args,str(prefix),sys.executable,str(child),'delay']),patch.object(mod.resource,'getrlimit',lambda kind:limits),patch.object(mod.subprocess,'Popen',side_effect=AssertionError('must reject before child')):
        try:mod.main()
        except (ValueError,RuntimeError) as exc:assert str(exc)==expected
        else:raise AssertionError(name)
    catches.append(dict(case=name,caught=expected))
# Bound call-tree review: no timeout-bearing wait/communicate/run, deadline, CPU setrlimit or SIGKILL.
tree=ast.parse(SOURCE.read_text());calls=[n for n in ast.walk(tree) if isinstance(n,ast.Call)]
assert not any(k.arg=='timeout' for n in calls for k in n.keywords)
assert not any(isinstance(n,ast.Attribute) and n.attr=='SIGKILL' for n in ast.walk(tree))
assert 'RLIMIT_CPU' not in ast.unparse(next(n for n in ast.walk(tree) if isinstance(n,ast.FunctionDef) and n.name=='memory_limit'))
result=dict(status='CAPTURE_INDEPENDENT_REVIEW_PASS',context='/root/survey_runtime, fresh same-model context; parent authored capture.py, reviewer did not',source_sha256=sha(SOURCE),actual_subprocess_checks=records,rejection_controls=catches,scope='Two finite actual CPU subprocess checks and static call review. Real signal forwarding and readable receipts observed. GPU mapping not exercised, no universal signal/crash guarantee.')
write(HERE/'CAPTURE_REVIEW.json',result);print(json.dumps(result,indent=2))
