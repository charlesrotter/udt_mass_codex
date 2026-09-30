"""Bounded operational control runner. This is NOT the broader production solver."""
from pathlib import Path
import argparse, fcntl, hashlib, importlib.util, json, math, signal, sys, time
import numpy as np
from checkpoint_io import CheckpointError, digest, json_bytes, exclusive, save, load_latest

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent
SOURCE=ROOT/'udt_gpu_time_live_discovery_2026-09-30/evolve.py'
SOURCE_HASH='f67b50e94ae0ffcc6a5f0bc6eaa2cf16f2763fd7a77026e71e6c1159e7e40367'

def signature(spec):
    if digest(SOURCE.read_bytes())!=SOURCE_HASH:raise CheckpointError('CONTROL_SOURCE_CHANGED')
    return {'spec':digest(json_bytes(spec)),'rhs':SOURCE_HASH,
            'runner':digest(Path(__file__).read_bytes()),
            'checkpoint_io':digest((HERE/'checkpoint_io.py').read_bytes())}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('spec');ap.add_argument('run')
    ap.add_argument('--resume',action='store_true')
    ap.add_argument('--pause-after',type=int,default=0)
    ap.add_argument('--lock',default='/tmp/udt_time_live_smoke_gpu0.lock')
    args=ap.parse_args();spec=json.loads(Path(args.spec).read_text())
    dt=spec['dt'];end=spec['end'];n=spec['n'];cadence=spec['checkpoint_steps']
    if not (math.isfinite(dt) and dt>0 and 1<end<=4 and n==32
            and len(spec['cases'])<=3 and 1<=cadence<=100):
        raise CheckpointError('INVALID_SMOKE_SPEC')
    if not (0<spec['wall_seconds']<=45 and 0<spec['gpu_bytes']<=2*1024**3
            and 0<spec['output_bytes']<=64*1024**2):raise CheckpointError('INVALID_BUDGET')
    sig=signature(spec);run=Path(args.run)
    if len(json_bytes(spec))>spec['output_bytes']:raise CheckpointError('OUTPUT_BUDGET')
    if args.resume:
        raw,step,t,_=load_latest(run,sig,(len(spec['cases']),5,n),dt,end)
    else:
        if run.exists():raise CheckpointError('REFUSE_EXISTING_RUN')
        run.mkdir(parents=True)
        exclusive(run/'spec.json',json_bytes(spec))
        raw=None;step=0;t=1.
    # Cooperative per-device lock; external GPU users still need preflight checks.
    with open(args.lock,'a+') as lock:
        try:fcntl.flock(lock.fileno(),fcntl.LOCK_EX|fcntl.LOCK_NB)
        except BlockingIOError:raise CheckpointError('GPU_WORKER_LOCKED')
        module_spec=importlib.util.spec_from_file_location('ngd1_frozen',SOURCE)
        solver=importlib.util.module_from_spec(module_spec);module_spec.loader.exec_module(solver)
        import torch
        if not torch.cuda.is_available():raise CheckpointError('CUDA_UNAVAILABLE')
        torch.use_deterministic_algorithms(True)
        if raw is None:raw,_=solver.initial(spec)
        if raw.nbytes>spec['gpu_bytes']:raise CheckpointError('GPU_BUDGET')
        stop={'signal':None}
        def requested(signum,frame):stop['signal']=signum
        signal.signal(signal.SIGTERM,requested);signal.signal(signal.SIGINT,requested)
        torch.cuda.reset_peak_memory_stats()
        u=torch.as_tensor(raw,device='cuda',dtype=torch.float64)
        dx,rhs=solver.engine(n,spec['k'],'cuda')
        start=time.monotonic();written=0
        if not args.resume:save(run,sig,raw,step,t,spec['output_bytes'])
        while t<end-1e-12:
            now=1+step*dt;h=min(dt,end-now)
            a=rhs(now,u);b=rhs(now+h/2,u+h*a/2)
            c=rhs(now+h/2,u+h*b/2);d=rhs(now+h,u+h*c)
            u=u+h*(a+2*b+2*c+d)/6;step+=1;t=min(1+step*dt,end)
            if step%cadence==0 or t>=end-1e-12 or stop['signal'] or time.monotonic()-start>=spec['wall_seconds']:
                raw=u.detach().cpu().numpy()
                if not np.isfinite(raw).all():raise CheckpointError('NONFINITE_OR_WRONG_DTYPE')
                if torch.cuda.max_memory_allocated()>spec['gpu_bytes']:raise CheckpointError('GPU_BUDGET')
                p,v,q,w,lam=u.unbind(1)
                residual=(dx(lam)-2*t*(v*dx(p)+torch.exp(2*p)*w*dx(q))).abs().max().item()
                checkpoint=save(run,sig,raw,step,t,spec['output_bytes']);written+=1
                event={'step':step,'t':t,'checkpoint':str(checkpoint),'constraint':residual,
                       'gpu_allocated_peak':torch.cuda.max_memory_allocated(),
                       'elapsed_seconds':time.monotonic()-start,'signal':stop['signal']}
                print(json.dumps(event),flush=True)
                if residual>2e-6:raise CheckpointError('CONSTRAINT_LIMIT')
                if stop['signal'] or time.monotonic()-start>=spec['wall_seconds'] or (args.pause_after and written>=args.pause_after):
                    print(json.dumps({'status':'CHECKPOINTED_STOP','t':t,'step':step}),flush=True)
                    return 75
        print(json.dumps({'status':'SMOKE_CONTROL_COMPLETE','t':t,'step':step,'torch':torch.__version__,
                          'device':torch.cuda.get_device_name(0),'dtype':str(u.dtype)}),flush=True)
        return 0

if __name__=='__main__':
    try:sys.exit(main())
    except Exception as exc:
        print(json.dumps({'status':'REJECTED_OR_FAILED','type':type(exc).__name__,'reason':str(exc)}),file=sys.stderr)
        sys.exit(2)
