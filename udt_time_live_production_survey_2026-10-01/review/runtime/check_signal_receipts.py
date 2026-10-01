"""Focused actual-main regression of parent-requested signal telemetry repair."""
import contextlib,hashlib,io,json,resource,signal,sys,types
from pathlib import Path
from unittest.mock import patch
resource.setrlimit(resource.RLIMIT_AS,(2*1024**3,2*1024**3))
HERE=Path(__file__).resolve().parent;BASE=HERE.parents[1];ROOT=BASE.parent;SOURCE=BASE/'supervise.py';OLD=ROOT/'udt_time_live_production_preparation_2026-10-01'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def write(p,v):
    with p.open('x') as f:json.dump(v,f,indent=2);f.write('\n')
mod=types.ModuleType('actual_supervisor');mod.__file__=str(SOURCE);exec(compile(SOURCE.read_text(),str(SOURCE),'exec'),mod.__dict__)
dest=HERE/'signal_fixtures';dest.mkdir(exist_ok=False);records=[]
initial=BASE/'initial/runtime_review/long_elapsed.npz'
required=[SOURCE,BASE/'production_worker.py',BASE/'initial_family.py',OLD/'initial_family.py',ROOT/'udt_three_spatial_smoke_2026-10-01/initial_data.py',ROOT/'udt_three_spatial_smoke_2026-10-01/evolution.py',ROOT/'udt_three_spatial_smoke_2026-10-01/constraints.py',ROOT/'udt_time_live_smoke_gate_2026-09-30/checkpoint_io.py',initial]
for requested in [None,signal.SIGTERM,signal.SIGINT]:
    name='none' if requested is None else str(int(requested));folder=dest/name;folder.mkdir();runtime=folder/'runtime';spec=folder/'spec.json';run=BASE/'runs'/('review_signal_'+name)
    config=json.loads((OLD/'specs/engineering.json').read_text());config.update(wall_seconds=None,initial=str(initial.relative_to(ROOT)));write(spec,config)
    manifest=folder/'manifest.json';write(manifest,dict(wall_seconds=None,output_bytes=1024**3,storage_roots=[str(runtime),str(run)],source_sha256={str(p):sha(p) for p in required},cases=[dict(id='case',spec=str(spec),spec_sha256=sha(spec),run=str(run))]))
    handlers={};forwarded=[];clock=[0.]
    def monotonic():clock[0]+=86400.;return clock[0]
    class FakeProcess:
        pid=123456
        def __init__(self,command,stdout,stderr,**kwargs):
            self.count=0;stdout.write(json.dumps(dict(status='CHECKPOINTED_STOP' if requested else 'TPS1_RUN_COMPLETE',reason='SIGNAL' if requested else None,tick=320))+'\n');stdout.flush()
        def poll(self):
            self.count+=1
            if self.count==1:
                if requested:handlers[requested](requested,None)
                return None
            return 75 if requested else 0
        def wait(self):return 75 if requested else 0
    out=io.StringIO()
    with patch.object(sys,'argv',['supervise.py',str(manifest),str(runtime)]),patch.object(mod.subprocess,'Popen',FakeProcess),patch.object(mod.time,'monotonic',monotonic),patch.object(mod.time,'sleep',lambda _:None),patch.object(mod.signal,'signal',lambda s,h:handlers.__setitem__(s,h)),patch.object(mod.os,'killpg',lambda pid,s:forwarded.append(s)),contextlib.redirect_stdout(out):rc=mod.main()
    receipt=json.loads(next((runtime/'attempts').glob('*/receipt.json')).read_text())
    assert rc==(75 if requested else 0) and forwarded==([requested] if requested else [])
    assert receipt['forwarded_signal']==requested and receipt['sigterm_sent']==(requested==signal.SIGTERM) and receipt['sigint_sent']==(requested==signal.SIGINT) and not receipt['sigkill_sent']
    assert receipt['wall_seconds']>=86400 and not (runtime/'wall_budget.json').exists()
    (folder/'captured_stdout').write_text(out.getvalue());records.append(dict(signal=requested,returncode=rc,receipt=receipt))
result=dict(status='SIGNAL_TELEMETRY_REPAIR_PASS',source_sha256=sha(SOURCE),records=records,scope='Actual supervisor main with fake child, including no signal and SIGTERM/SIGINT; author regression, parent independently reviews source. No real child in this test.')
write(HERE/'SIGNAL_RECEIPT_CONTROLS.json',result);print(json.dumps(result,indent=2))
