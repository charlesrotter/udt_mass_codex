"""Bounded new-solver smoke worker; never authorizes multi-hour production."""
import argparse,fcntl,hashlib,io,json,os,signal,sys,time
from pathlib import Path
import numpy as np

B=Path(__file__).resolve().parent;ROOT=B.parent
SMK=ROOT/'udt_time_live_smoke_gate_2026-09-30'
sys.path.insert(0,str(SMK))
from checkpoint_io import save,load_latest,exclusive,json_bytes,digest

def main():
    ap=argparse.ArgumentParser();ap.add_argument('spec');ap.add_argument('run');ap.add_argument('--resume',action='store_true');ap.add_argument('--pause-after',type=int,default=0)
    args=ap.parse_args();spec=json.loads(Path(args.spec).read_text());run=Path(args.run)
    n=spec['n'];dt=spec['dt'];end=spec['end'];initial=ROOT/spec['initial']
    if n not in (8,12,16,24) or not 0<dt<=.01 or not 1<end<=1.5:raise ValueError('INVALID_SMOKE_SPEC')
    if not 0<spec['wall_seconds']<=90 or spec['gpu_bytes']>4*1024**3 or spec['output_bytes']>128*1024**2:raise ValueError('INVALID_BUDGET')
    if os.environ.get('CUBLAS_WORKSPACE_CONFIG')!=':4096:8':raise ValueError('DETERMINISTIC_CUBLAS_REQUIRED')
    sig={'spec':digest(json_bytes(spec)),'initial':digest(initial.read_bytes()),
         'code':{p.name:digest(p.read_bytes()) for p in [B/'evolution.py',B/'constraints.py',B/'run_smoke.py',SMK/'checkpoint_io.py']},
         'CUBLAS_WORKSPACE_CONFIG':os.environ['CUBLAS_WORKSPACE_CONFIG']}
    with open('/tmp/udt_time_live_smoke_gpu0.lock','a+') as lock:
        try:fcntl.flock(lock.fileno(),fcntl.LOCK_EX|fcntl.LOCK_NB)
        except BlockingIOError:raise RuntimeError('GPU_WORKER_LOCKED')
        if args.resume:raw,step,t,_=load_latest(run,sig,(2,n,n,n,4,4),dt,end)
        else:
            if run.exists():raise RuntimeError('REFUSE_EXISTING_RUN')
            run.mkdir(parents=True);exclusive(run/'spec.json',json_bytes(spec))
            with np.load(initial,allow_pickle=False) as data:raw=np.stack([data['g'],data['v']])
            step=0;t=1.
        import torch
        from evolution import Engine
        from constraints import original_constraints
        if raw.shape!=(2,n,n,n,4,4) or raw.dtype!=np.float64:raise RuntimeError('INVALID_INITIAL_SHAPE_DTYPE')
        torch.set_num_threads(1);torch.use_deterministic_algorithms(True);torch.cuda.reset_peak_memory_stats()
        engine=Engine(n,spec['period'],'cuda');g=torch.as_tensor(raw[0],device='cuda');v=torch.as_tensor(raw[1],device='cuda')
        stop={'signal':None}
        def requested(signum,frame):stop['signal']=signum
        signal.signal(signal.SIGTERM,requested);signal.signal(signal.SIGINT,requested)
        start=time.monotonic();written=0
        def checked_save(do_save=True):
            raw=torch.stack([g,v]).cpu().numpy();reason=None
            metrics={}
            if not np.isfinite(raw).all():reason='NONFINITE'
            else:
                eig=torch.linalg.eigvalsh(g[...,1:,1:]);inv=torch.linalg.inv(g)
                metrics['gamma_min_eigenvalue']=float(eig.min());metrics['inverse_g00_max']=float(inv[...,0,0].max())
                if metrics['gamma_min_eigenvalue']<=0 or metrics['inverse_g00_max']>=0:reason='LORENTZ_SIGNATURE'
                else:
                    ham,mom,lapse2=original_constraints(engine,g,v)
                    harmonic=engine.geometry(g,v)[-1]
                    metrics.update(hamiltonian=float(ham.abs().max()),momentum=float(mom.abs().max()),harmonic=float(harmonic.abs().max()))
                    if not all(np.isfinite(x) for x in metrics.values()):reason='NONFINITE_CONSTRAINT'
                    elif max(metrics['hamiltonian'],metrics['momentum'],metrics['harmonic'])>spec['constraint_limit']:reason='CONSTRAINT_LIMIT'
            peak=torch.cuda.max_memory_allocated()
            if peak>spec['gpu_bytes']:reason='GPU_BUDGET'
            if reason:
                folder=save(run,sig,raw,step,t,spec['output_bytes'],diagnostic=reason)
                print(json.dumps({'status':'DIAGNOSTIC_REJECTION','reason':reason,'step':step,'t':t,'metrics':metrics,'path':str(folder)}),flush=True)
                raise RuntimeError(reason)
            folder=save(run,sig,raw,step,t,spec['output_bytes']) if do_save else None
            print(json.dumps({'step':step,'t':t,'metrics':metrics,'gpu_allocated_peak':peak,'elapsed_seconds':time.monotonic()-start,'checkpoint':str(folder) if folder else None}),flush=True)
        checked_save(not args.resume)
        while t<end-1e-12:
            h=min(dt,end-(1+step*dt));g,v=engine.step(g,v,h);step+=1;t=min(1+step*dt,end)
            checked_save();written+=1
            if stop['signal'] or time.monotonic()-start>=spec['wall_seconds'] or (args.pause_after and written>=args.pause_after):
                print(json.dumps({'status':'CHECKPOINTED_STOP','step':step,'t':t,'signal':stop['signal']}),flush=True);return 75
        print(json.dumps({'status':'TDS1_SHORT_RUN_COMPLETE','step':step,'t':t,'seconds':time.monotonic()-start,'torch':torch.__version__,'device':torch.cuda.get_device_name(0)}),flush=True);return 0

if __name__=='__main__':
    try:sys.exit(main())
    except Exception as exc:
        print(json.dumps({'status':'REJECTED_OR_FAILED','reason':str(exc),'type':type(exc).__name__}),file=sys.stderr);sys.exit(2)
