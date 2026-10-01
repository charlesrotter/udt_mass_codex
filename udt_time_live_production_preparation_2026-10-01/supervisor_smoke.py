"""Actual tiny queue pause/resume, signal and completion checks on one GPU."""
import hashlib,json,os,signal,subprocess,sys,time
from pathlib import Path
B=Path(__file__).resolve().parent;ROOT=B.parent
def sha(q):return hashlib.sha256(Path(q).read_bytes()).hexdigest()
def dump(q,x):
    with Path(q).open('x') as f:json.dump(x,f,indent=2,sort_keys=True);f.write('\n')
base=B/'supervisor_smoke';base.mkdir()
sources=[B/'supervise.py',B/'production_worker.py',B/'initial_family.py',ROOT/'udt_three_spatial_smoke_2026-10-01/initial_data.py',ROOT/'udt_three_spatial_smoke_2026-10-01/evolution.py',ROOT/'udt_three_spatial_smoke_2026-10-01/constraints.py',ROOT/'udt_time_live_smoke_gate_2026-09-30/checkpoint_io.py',B/'initial/axial1_n8.npz']
spec=B/'specs/engineering.json';runroot=B/'runs/supervisor_smoke'
def queue(name,ids):
    q=base/(name+'.json');dump(q,dict(wall_seconds=120,output_bytes=64*1024**2,storage_roots=[str(runroot),str(base)],source_sha256={str(p):sha(p) for p in sources},cases=[dict(id=i,spec=str(spec),spec_sha256=sha(spec),run=str(runroot/i)) for i in ids]));return q
queue_pause=queue('pause',['case_a','case_b']);queue_signal=queue('signal',['case_c']);results=[]
def execute(name,manifest,runtime,expected,extra=(),interrupt=False):
    command=[sys.executable,str(B/'supervise.py'),str(manifest),str(base/runtime),*extra];started=time.monotonic();sent=False
    with (base/(name+'.stdout')).open('x') as out,(base/(name+'.stderr')).open('x') as err:
        proc=subprocess.Popen(command,stdout=out,stderr=err,start_new_session=True)
        if interrupt:
            while proc.poll() is None and time.monotonic()-started<30:
                if list((runroot/'case_c/checkpoints').glob('*/COMMITTED')):
                    proc.send_signal(signal.SIGTERM);sent=True;break
                time.sleep(.005)
            if not sent:raise RuntimeError('SIGNAL_HANDSHAKE_FAILED')
        try:rc=proc.wait(timeout=40)
        except subprocess.TimeoutExpired:
            os.killpg(proc.pid,signal.SIGKILL);proc.wait();raise
    row=dict(name=name,command=command,returncode=rc,expected=expected,seconds=time.monotonic()-started,sigterm_sent=sent)
    dump(base/(name+'.receipt.json'),row);results.append(row)
    if rc!=expected:raise RuntimeError('SUPERVISOR_SMOKE_FAILED: '+name)
execute('pause',queue_pause,'runtime_pause',75,['--stop-after','1'])
execute('resume',queue_pause,'runtime_pause',0)
execute('complete_again',queue_pause,'runtime_pause',0)
execute('signal',queue_signal,'runtime_signal',75,interrupt=True)
execute('signal_resume',queue_signal,'runtime_signal',0)
dump(B/'SUPERVISOR_SMOKE.json',dict(status='EXPECTED_RETURNS_PASS_PENDING_INDEPENDENT_ARTIFACT_REVIEW',invocations=results,scope='Finite same-worker queue/interruption checks; no exhaustive crash or long-run certification'))
print(json.dumps(results,indent=2))
