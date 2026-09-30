"""Sequential actual child-process smoke checks. Only children initialize CUDA."""
from pathlib import Path
import argparse, fcntl, hashlib, io, json, os, signal, subprocess, sys, time
from unittest.mock import patch
import numpy as np
from checkpoint_io import digest, json_bytes, exclusive, save, load_latest

SOURCE_DIR=Path(__file__).resolve().parent
ROOT=SOURCE_DIR.parent
parser=argparse.ArgumentParser();parser.add_argument('--evidence-root',type=Path,required=True)
B=parser.parse_args().evidence_root.resolve()
RUNS=B/'runs'
spec=json.loads((ROOT/'udt_gpu_time_live_discovery_2026-09-30/specs/pilot_n32.json').read_text())
spec.update(checkpoint_steps=50,wall_seconds=30,gpu_bytes=2*1024**3,output_bytes=64*1024**2)
records=[]
lockpath=B/'checks/gpu_smoke.lock'

def invoke(label,run,specification=spec,extra=(),expected=0,needle=None,interrupt=None):
    cfg=B/'checks'/f'{label}.spec.json';exclusive(cfg,json_bytes(specification))
    cmd=[sys.executable,str(SOURCE_DIR/'smoke_runner.py'),str(cfg),str(run),'--lock',str(lockpath),*extra]
    stdout=B/'checks'/f'{label}.stdout';stderr=B/'checks'/f'{label}.stderr'
    start=time.monotonic()
    child_deadline=start+60
    with stdout.open('xb') as out,stderr.open('xb') as err:
        child=subprocess.Popen(cmd,stdout=out,stderr=err,cwd=ROOT)
        try:
            if interrupt is not None:
                deadline=min(child_deadline,start+20)
                while time.monotonic()<deadline:
                    paths=list((run/'checkpoints').glob('ckpt_000000050_*/COMMITTED'))
                    if paths:break
                    if child.poll() is not None:raise AssertionError('worker ended before requested interrupt')
                    time.sleep(.005)
                else:raise AssertionError('no checkpoint before interrupt deadline')
                os.kill(child.pid,interrupt)
            code=child.wait(timeout=max(.001,child_deadline-time.monotonic()))
        finally:
            if child.poll() is None:child.kill();child.wait()
    out=stdout.read_text();err=stderr.read_text()
    rec={'label':label,'command':cmd,'returncode':code,'expected':expected,
         'seconds':time.monotonic()-start,'stdout_sha256':digest(stdout.read_bytes()),
         'stderr_sha256':digest(stderr.read_bytes()),'signal_sent':interrupt}
    records.append(rec)
    # Record partial results even if this assertion uncovers an implementation defect.
    progress=B/'checks'/f'{label}.receipt.json';exclusive(progress,json_bytes(rec))
    assert code==expected,(label,code,out,err)
    if needle:assert needle in out+err,(label,needle,out,err)
    return rec

def latest(run):
    return sorted(p.parent for p in (run/'checkpoints').glob('ckpt_*/COMMITTED'))[-1]

def state(run):
    with np.load(latest(run)/'state.npz',allow_pickle=False) as data:return data['state']

def fixture(name,change):
    # Deliberate new invalid fixtures; never mutate any original grid/checkpoint.
    run=RUNS/name;run.mkdir();(run/'checkpoints').mkdir()
    original=latest(RUNS/'uninterrupted');folder=run/'checkpoints'/original.name;folder.mkdir()
    payload=(original/'state.npz').read_bytes();meta=json.loads((original/'metadata.json').read_text())
    if change=='corrupt':payload=payload[:-1]+bytes([payload[-1]^1])
    if change in ('nonfinite','constraint','overflow'):
        a=state(RUNS/'uninterrupted').copy()
        if change=='nonfinite':a[0,0,0]=np.nan
        if change=='constraint':a[:,4]+=np.sin(np.arange(32)*2*np.pi/32)
        if change=='overflow':a[:,0]=1000
        buf=io.BytesIO();np.savez_compressed(buf,state=a);payload=buf.getvalue();meta['payload_sha256']=digest(payload)
    exclusive(folder/'state.npz',payload);raw=json_bytes(meta)
    exclusive(folder/'metadata.json',raw);exclusive(folder/'COMMITTED',(digest(raw)+'\n').encode())
    return run

def main():
    B.mkdir(exist_ok=False);(B/'checks').mkdir()
    RUNS.mkdir(exist_ok=False)
    invoke('uninterrupted',RUNS/'uninterrupted')
    invoke('pause',RUNS/'resumed',extra=('--pause-after','3'),expected=75,needle='CHECKPOINTED_STOP')
    invoke('resume',RUNS/'resumed',extra=('--resume',))
    assert np.array_equal(state(RUNS/'uninterrupted'),state(RUNS/'resumed'))
    invoke('sigterm',RUNS/'sigterm',expected=75,needle='CHECKPOINTED_STOP',interrupt=signal.SIGTERM)
    invoke('sigterm_resume',RUNS/'sigterm',extra=('--resume',))
    assert np.array_equal(state(RUNS/'uninterrupted'),state(RUNS/'sigterm'))
    invoke('sigkill',RUNS/'sigkill',expected=-signal.SIGKILL,interrupt=signal.SIGKILL)
    # A higher uncommitted partial write must be ignored, and retained as evidence.
    partial=RUNS/'sigkill/checkpoints/ckpt_999999999_incomplete';partial.mkdir()
    exclusive(partial/'state.npz',b'deliberate incomplete write')
    invoke('sigkill_resume',RUNS/'sigkill',extra=('--resume',))
    assert np.array_equal(state(RUNS/'uninterrupted'),state(RUNS/'sigkill'))
    assert (partial/'state.npz').read_bytes()==b'deliberate incomplete write'
    # Interrupt the actual save path immediately before atomic publication.
    atomic=RUNS/'atomic_marker';atomic.mkdir()
    arr=np.zeros((1,5,32));marker_sig={'engineering':'atomic-control'}
    good=save(atomic,marker_sig,arr,0,1,1024**2)
    with patch('checkpoint_io.os.link',side_effect=InterruptedError('injected pre-publication interruption')):
        try:save(atomic,marker_sig,arr,1,1.01,1024**2)
        except InterruptedError:pass
        else:raise AssertionError('fault injection did not interrupt actual save')
    assert load_latest(atomic,marker_sig,arr.shape,.01,4)[3]==good
    assert len(list((atomic/'checkpoints').glob('*/COMMITTED.pending')))==2
    assert len(list((atomic/'checkpoints').glob('*/COMMITTED')))==1
    invoke('corrupt',fixture('corrupt','corrupt'),extra=('--resume',),expected=2,needle='PAYLOAD_HASH_MISMATCH')
    invoke('nonfinite',fixture('nonfinite','nonfinite'),extra=('--resume',),expected=2,needle='NONFINITE_OR_WRONG_DTYPE')
    for label in ('constraint','overflow'):
        run=fixture(label,label)
        invoke(label,run,extra=('--resume',),expected=2,needle='CONSTRAINT_LIMIT')
        assert len(list((run/'diagnostics').glob('*/DIAGNOSTIC')))==1
        assert len(list((run/'checkpoints').glob('*/COMMITTED')))==1
        assert not list((run/'diagnostics').glob('*/COMMITTED'))
    changed=dict(spec,dt=.006)
    invoke('changed_spec',RUNS/'resumed',changed,extra=('--resume',),expected=2,needle='SPEC_OR_CODE_MISMATCH')
    invoke('overwrite',RUNS/'uninterrupted',expected=2,needle='REFUSE_EXISTING_RUN')
    invoke('invalid_dt',RUNS/'invalid_dt',dict(spec,dt=0),expected=2,needle='INVALID_SMOKE_SPEC')
    invoke('memory_limit',RUNS/'memory_limit',dict(spec,gpu_bytes=1),expected=2,needle='GPU_BUDGET')
    invoke('output_limit',RUNS/'output_limit',dict(spec,output_bytes=1),expected=2,needle='OUTPUT_BUDGET')
    invoke('wall_stop',RUNS/'wall_stop',dict(spec,wall_seconds=1e-8),expected=75,needle='CHECKPOINTED_STOP')
    with lockpath.open('a+') as lease:
        fcntl.flock(lease.fileno(),fcntl.LOCK_EX|fcntl.LOCK_NB)
        invoke('worker_lock',RUNS/'worker_lock',expected=2,needle='GPU_WORKER_LOCKED')
    # Compare final fields with the independently checked prior control artifact.
    with np.load(ROOT/'udt_gpu_time_live_discovery_2026-09-30/runs/pilot_n32/fields.npz',allow_pickle=False) as data:
        anchor=data['state'][-1];initial=data['state'][0]
    final=state(RUNS/'uninterrupted');error=float(np.max(np.abs(final-anchor)));assert error<2e-7
    # Actual longitudinal supplied-clock endpoint ratio for te=1,to=4,d=3.
    freq=np.fft.fftfreq(32,1/32)*.75
    def clock(a):return (np.fft.ifft(np.fft.fft(a[:,4],axis=-1)*np.exp(3j*freq),axis=-1).real-initial[:,4])/4-.25*np.log(4)
    clockerr=float(np.max(np.abs(clock(final)-clock(anchor))));assert clockerr<2e-7
    clock_output={'query':{'te':1,'to':4,'longitudinal_coordinate_displacement':3,
                          'observers':'supplied fixed-coordinate congruence',
                          'convention':'Z=received interval/emitted interval; logZ=Delta(lambda)/4-log(to/te)/4'},
                  'cases':spec['cases'],'x':(np.arange(32)*2*np.pi/(32*.75)).tolist(),
                  'logZ':clock(final).tolist(),'Z':np.exp(clock(final)).tolist(),
                  'scope':'sampled conditional control readout; not a native UDT prediction'}
    exclusive(B/'CLOCK_READOUT.json',json_bytes(clock_output))
    events=[json.loads(l) for l in (B/'checks/uninterrupted.stdout').read_text().splitlines()]
    constraints=[e['constraint'] for e in events if 'constraint' in e];assert constraints and max(constraints)<2e-6
    total=sum(p.stat().st_size for p in B.rglob('*') if p.is_file());assert total<256*1024**2
    report={'status':'SMOKE_CONTROL_PASS','scope':'operational control runner only; broader solver NOT certified',
            'checks':records,'restart_bitwise_equal':True,'sigterm_restart_bitwise_equal':True,
            'sigkill_restart_bitwise_equal':True,'partial_checkpoint_preserved':True,
            'atomic_marker_interruption_recovery':True,'invalid_endpoint_rejected':True,
            'nonfinite_derived_constraint_rejected':True,'failed_state_diagnostic_only':True,
            'prior_validated_control_max_field_error':error,'clock_log_ratio_error':clockerr,
            'max_constraint':max(constraints),'bytes_at_end':total,
            'scientific_equations_changed':False,'multi_hour_production_started':False}
    exclusive(B/'SMOKE_RESULT.json',json_bytes(report));print(json.dumps(report,indent=2))

if __name__=='__main__':main()
