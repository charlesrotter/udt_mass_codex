"""Serial short workers with exact receipts and independently readable histories."""
import hashlib,io,json,os,signal,subprocess,sys,time
from pathlib import Path
import numpy as np
B=Path(__file__).resolve().parent;ROOT=B.parent
records=[]

def exclusive(path,data):
    with Path(path).open('xb') as f:f.write(data)

def collect(name):
    run=B/'runs'/name;rows=[];sources=[];signature=None
    for marker in sorted((run/'checkpoints').glob('*/COMMITTED')):
        folder=marker.parent;raw=(folder/'metadata.json').read_bytes();meta=json.loads(raw)
        assert marker.read_text().strip()==hashlib.sha256(raw).hexdigest()
        assert meta['eligible_for_resume'] is True
        if signature is None:signature=meta['signature']
        assert signature==meta['signature']
        payload=(folder/'state.npz').read_bytes();assert hashlib.sha256(payload).hexdigest()==meta['payload_sha256']
        with np.load(io.BytesIO(payload),allow_pickle=False) as data:a=data['state']
        assert a.dtype==np.float64 and np.isfinite(a).all()
        rows.append((meta['step'],meta['t'],a));sources.append({'metadata':str(folder.relative_to(ROOT)/'metadata.json'),'sha256':hashlib.sha256(raw).hexdigest()})
    rows.sort(key=lambda r:r[0]);assert [r[0] for r in rows]==list(range(len(rows)))
    spec=json.loads((run/'spec.json').read_text());times=np.array([r[1] for r in rows]);states=np.stack([r[2] for r in rows])
    assert abs(times[-1]-spec['end'])<1e-12
    buf=io.BytesIO();np.savez_compressed(buf,times=times,g=states[:,0],v=states[:,1],period=np.array(spec['period']))
    path=B/'histories'/f'{name}.npz';exclusive(path,buf.getvalue())
    exclusive(path.with_suffix('.sources.json'),(json.dumps({'checkpoints':sources,'signature':signature,'history_sha256':hashlib.sha256(buf.getvalue()).hexdigest()},indent=2)+'\n').encode())
    return states[-1]

def invoke(label,spec_name,run_name,extra=(),expected=0,interrupt=False):
    cmd=[sys.executable,str(B/'run_smoke.py'),str(B/'specs'/f'{spec_name}.json'),str(B/'runs'/run_name),*extra]
    out=B/'checks'/f'{label}.stdout';err=B/'checks'/f'{label}.stderr';start=time.monotonic();deadline=start+120
    with out.open('xb') as stdout,err.open('xb') as stderr:
        child=subprocess.Popen(cmd,stdout=stdout,stderr=stderr,env=dict(os.environ,CUBLAS_WORKSPACE_CONFIG=':4096:8'),cwd=ROOT)
        try:
            if interrupt:
                while time.monotonic()<min(deadline,start+30):
                    if list((B/'runs'/run_name/'checkpoints').glob('ckpt_000000005_*/COMMITTED')):break
                    if child.poll() is not None:raise RuntimeError('CHILD_ENDED_BEFORE_STOP')
                    time.sleep(.002)
                else:raise RuntimeError('NO_CHECKPOINT_BEFORE_STOP')
                os.kill(child.pid,signal.SIGTERM)
            code=child.wait(timeout=max(.001,deadline-time.monotonic()))
        finally:
            if child.poll() is None:child.kill();child.wait()
    rec={'command':cmd,'label':label,'returncode':code,'expected':expected,'seconds':time.monotonic()-start,'stdout_sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'stderr_sha256':hashlib.sha256(err.read_bytes()).hexdigest(),'SIGTERM_sent':interrupt}
    exclusive(B/'checks'/f'{label}.receipt.json',(json.dumps(rec,indent=2)+'\n').encode());records.append(rec)
    assert code==expected,(label,code,err.read_text());print(json.dumps(rec),flush=True)
    assert sum(r['seconds'] for r in records)<240,'BATCH_TIME_BUDGET'

def main():
    (B/'histories').mkdir(exist_ok=False)
    collect('n8') # retained pre-hardening positive history; numerical code unchanged
    for spec in ['n8','n12','n16','n16_half','kasner','kasner_half']:
        name='n8_repaired' if spec=='n8' else spec
        invoke('history_'+name,spec,name);collect(name)
    invoke('pause','n8','resumed',extra=('--pause-after','5'),expected=75)
    invoke('resume','n8','resumed',extra=('--resume',));resumed=collect('resumed')
    with np.load(B/'histories/n8_repaired.npz') as data:reference=np.stack([data['g'][-1],data['v'][-1]])
    assert np.array_equal(reference,resumed)
    invoke('sigterm','n8','sigterm',expected=75,interrupt=True)
    invoke('sigterm_resume','n8','sigterm',extra=('--resume',));assert np.array_equal(reference,collect('sigterm'))
    report={'status':'SHORT_HISTORY_AND_RESTART_PASS','records':records,'restart_bitwise_equal':True,'SIGTERM_restart_bitwise_equal':True,'scope':'runtime only; independent original Ricci/readout/refinement review still required'}
    exclusive(B/'SHORT_RUN_RESULT.json',(json.dumps(report,indent=2)+'\n').encode())

if __name__=='__main__':main()
