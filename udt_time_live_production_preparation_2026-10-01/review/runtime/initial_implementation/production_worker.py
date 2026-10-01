"""TPP1 bounded worker: unchanged conditional engine, adaptive lattice and output.

Checkpoint step is integer time tick, never the number of adaptive RK steps.
Only supplied numerical controls are introduced. This file does not launch jobs.
"""
import argparse, bisect, fcntl, json, math, os, signal, sys, time
from pathlib import Path
import numpy as np

B=Path(__file__).resolve().parent;ROOT=B.parent
TDS=ROOT/'udt_three_spatial_smoke_2026-10-01';SMK=ROOT/'udt_time_live_smoke_gate_2026-09-30'
sys.path.insert(0,str(SMK));sys.path.insert(0,str(TDS))
from checkpoint_io import save,load_latest,exclusive,json_bytes,digest

def positive_int(value,high,name):
    if type(value)!=int or not 0<value<=high:raise ValueError('INVALID_'+name)
    return value

def validate(spec):
    required={'n','initial','period','dt_min','end_tick','max_step_ticks','cfl','check_ticks','checkpoint_ticks','windows','wall_seconds','gpu_bytes','output_bytes','constraint_limit'}
    if set(spec)!=required:raise ValueError('SPEC_SCHEMA')
    n=positive_int(spec['n'],64,'GRID')
    if n<8 or n%2:raise ValueError('INVALID_GRID')
    for key,lo,hi in [('dt_min',1e-6,.005),('cfl',1e-6,.5),('wall_seconds',0,180),('constraint_limit',0,2e-5),('period',0,100)]:
        val=spec[key]
        if type(val) not in (int,float) or not math.isfinite(val) or not lo<val<=hi:raise ValueError('INVALID_'+key.upper())
    end=positive_int(spec['end_tick'],3000000,'END_TICK')
    if end*spec['dt_min']>3:raise ValueError('END_RANGE')
    maximum=positive_int(spec['max_step_ticks'],4096,'MAX_STEP')
    if maximum&(maximum-1) or maximum*spec['dt_min']>.01:raise ValueError('INVALID_DYADIC_STEP')
    positive_int(spec['check_ticks'],end,'CHECK_CADENCE');positive_int(spec['checkpoint_ticks'],end,'CHECKPOINT_CADENCE')
    positive_int(spec['gpu_bytes'],8*1024**3,'GPU_BUDGET');positive_int(spec['output_bytes'],512*1024**2,'OUTPUT_BUDGET')
    if not isinstance(spec['windows'],list) or len(spec['windows'])>12:raise ValueError('INVALID_WINDOWS')
    ticks={0,end};checks={0,end}
    ticks.update(range(spec['checkpoint_ticks'],end,spec['checkpoint_ticks']))
    checks.update(range(spec['check_ticks'],end,spec['check_ticks']))
    for w in spec['windows']:
        if set(w)!={'center','stride','count'} or type(w['center'])!=int:raise ValueError('WINDOW_SCHEMA')
        count=positive_int(w['count'],25,'WINDOW_COUNT');stride=positive_int(w['stride'],end,'WINDOW_STRIDE')
        if count<5 or count%2==0:raise ValueError('INVALID_WINDOW_COUNT')
        wt=[w['center']+(i-count//2)*stride for i in range(count)]
        if min(wt)<0 or max(wt)>end:raise ValueError('WINDOW_RANGE')
        ticks.update(wt)
    checks.update(ticks)
    initial=Path(spec['initial'])
    if initial.is_absolute() or '..' in initial.parts or not str(initial).startswith('udt_time_live_production_preparation_2026-10-01/initial/'):
        raise ValueError('INITIAL_PATH_SCOPE')
    with np.load(ROOT/initial,allow_pickle=False) as data:
        if data['g'].shape!=(n,n,n,4,4) or data['v'].shape!=data['g'].shape or data['g'].dtype!=np.float64 or data['v'].dtype!=np.float64:raise ValueError('INITIAL_SHAPE_DTYPE')
        if not np.isfinite(data['g']).all() or not np.isfinite(data['v']).all():raise ValueError('INITIAL_NONFINITE')
        if float(data['period'])!=spec['period']:raise ValueError('INITIAL_PERIOD_MISMATCH')
    return sorted(ticks),sorted(checks),ROOT/initial

def geometry_bound(torch,g,n,period):
    if not bool(torch.isfinite(g).all()):raise RuntimeError('NONFINITE_METRIC')
    gamma=g[...,1:,1:];eig=torch.linalg.eigvalsh(gamma)
    if float(eig.min())<=0:raise RuntimeError('NONSPACELIKE_SLICE')
    inv=torch.linalg.inv(g)
    if float(inv[...,0,0].max())>=0:raise RuntimeError('LORENTZ_SIGNATURE')
    alpha=(-inv[...,0,0]).rsqrt();beta=-inv[...,0,1:]/inv[...,0,0,None]
    # lambda_max(gamma^-1)=1/lambda_min(gamma), pointwise for positive gamma.
    speed=beta.abs().sum(-1)+alpha*torch.sqrt(3/eig[...,0])
    omega=float(speed.max())*(math.pi*n/period)
    if not math.isfinite(omega) or omega<=0:raise RuntimeError('INVALID_CHARACTERISTIC_BOUND')
    return omega,{'gamma_min':float(eig.min()),'inverse_g00_max':float(inv[...,0,0].max()),'omega_bound':omega}

def checked_rk4(torch,engine,g,v,dt,cfl):
    maximum=0.
    def rhs(x,y):
        nonlocal maximum
        if not bool(torch.isfinite(y).all()):raise RuntimeError('NONFINITE_VELOCITY')
        omega,_=geometry_bound(torch,x,engine.n,engine.period);maximum=max(maximum,omega)
        if dt*omega>cfl*(1+1e-12):raise RuntimeError('STAGE_CFL')
        return engine.rhs(x,y)
    a,b=rhs(g,v);c,d=rhs(g+dt*a/2,v+dt*b/2)
    e,f=rhs(g+dt*c/2,v+dt*d/2);h,j=rhs(g+dt*e,v+dt*f)
    newg=g+dt*(a+2*c+2*e+h)/6;newv=v+dt*(b+2*d+2*f+j)/6
    omega,_=geometry_bound(torch,newg,engine.n,engine.period);maximum=max(maximum,omega)
    if dt*omega>cfl*(1+1e-12):raise RuntimeError('STAGE_CFL')
    if not bool(torch.isfinite(newv).all()):raise RuntimeError('NONFINITE_VELOCITY')
    return newg,newv,maximum

def main():
    ap=argparse.ArgumentParser();ap.add_argument('spec');ap.add_argument('run');ap.add_argument('--resume',action='store_true');ap.add_argument('--pause-after',type=int,default=0);args=ap.parse_args()
    if args.pause_after<0:raise ValueError('INVALID_PAUSE')
    spec=json.loads(Path(args.spec).read_text());saves,checks,initial=validate(spec);run=Path(args.run)
    if os.environ.get('CUBLAS_WORKSPACE_CONFIG')!=':4096:8':raise ValueError('DETERMINISTIC_CUBLAS_REQUIRED')
    sources=[B/'production_worker.py',TDS/'evolution.py',TDS/'constraints.py',SMK/'checkpoint_io.py']
    sig={'spec':digest(json_bytes(spec)),'initial':digest(initial.read_bytes()),'code':{str(p.relative_to(ROOT)):digest(p.read_bytes()) for p in sources},'CUBLAS_WORKSPACE_CONFIG':os.environ['CUBLAS_WORKSPACE_CONFIG'],'step_semantics':'integer_time_tick'}
    with open('/tmp/udt_time_live_smoke_gpu0.lock','a+') as lock:
        try:fcntl.flock(lock.fileno(),fcntl.LOCK_EX|fcntl.LOCK_NB)
        except BlockingIOError:raise RuntimeError('GPU_WORKER_LOCKED')
        if args.resume:raw,tick,t,_=load_latest(run,sig,(2,spec['n'],spec['n'],spec['n'],4,4),spec['dt_min'],1+spec['end_tick']*spec['dt_min'])
        else:
            if run.exists():raise RuntimeError('REFUSE_EXISTING_RUN')
            run.mkdir(parents=True);exclusive(run/'spec.json',json_bytes(spec))
            with np.load(initial,allow_pickle=False) as data:raw=np.stack([data['g'],data['v']])
            tick=0;t=1.
        import torch
        from evolution import Engine
        from constraints import original_constraints
        torch.set_num_threads(1);torch.use_deterministic_algorithms(True);torch.cuda.reset_peak_memory_stats()
        engine=Engine(spec['n'],spec['period'],'cuda');g=torch.as_tensor(raw[0],device='cuda');v=torch.as_tensor(raw[1],device='cuda')
        start=time.monotonic();stop={'signal':None};steps=0;retries=0;step_ticks=[];max_cfl=0.
        def requested(signum,frame):stop['signal']=signum
        signal.signal(signal.SIGTERM,requested);signal.signal(signal.SIGINT,requested)
        def emit(status,**kw):print(json.dumps(dict(status=status,tick=tick,t=1+tick*spec['dt_min'],elapsed_seconds=time.monotonic()-start,**kw),allow_nan=False),flush=True)
        def checked_save(do_save,reason=None):
            try:
                _,metrics=geometry_bound(torch,g,spec['n'],spec['period'])
                if not bool(torch.isfinite(v).all()):raise RuntimeError('NONFINITE_VELOCITY')
                ham,mom,_=original_constraints(engine,g,v);harmonic=engine.geometry(g,v)[-1]
                metrics.update(hamiltonian=float(ham.abs().max()),momentum=float(mom.abs().max()),harmonic=float(harmonic.abs().max()))
                if not all(math.isfinite(x) for x in metrics.values()):raise RuntimeError('NONFINITE_CONSTRAINT')
                if max(metrics[k] for k in ['hamiltonian','momentum','harmonic'])>spec['constraint_limit']:raise RuntimeError('CONSTRAINT_LIMIT')
                if torch.cuda.max_memory_allocated()>spec['gpu_bytes']:raise RuntimeError('GPU_BUDGET')
            except Exception as exc:
                folder=save(run,sig,torch.stack([g,v]).cpu().numpy(),tick,1+tick*spec['dt_min'],spec['output_bytes'],diagnostic=str(exc))
                emit('DIAGNOSTIC_REJECTION',reason=str(exc),path=str(folder));raise
            folder=save(run,sig,torch.stack([g,v]).cpu().numpy(),tick,1+tick*spec['dt_min'],spec['output_bytes']) if do_save else None
            free,total=torch.cuda.mem_get_info()
            emit('CHECKED_STATE',metrics=metrics,checkpoint=str(folder) if folder else None,reason=reason,gpu_allocated_peak=torch.cuda.max_memory_allocated(),gpu_reserved=torch.cuda.memory_reserved(),device_used_bytes=total-free)
        checked_save(not args.resume)
        while tick<spec['end_tick']:
            omega,_=geometry_bound(torch,g,spec['n'],spec['period'])
            available=math.floor(spec['cfl']/omega/spec['dt_min'])
            if available<1:
                checked_save(True,'TIMESTEP_FLOOR');emit('CHECKPOINTED_STOP',reason='TIMESTEP_FLOOR');return 75
            next_event=checks[bisect.bisect_right(checks,tick)]
            allowed=min(available,spec['max_step_ticks'],next_event-tick)
            jump=1<<(allowed.bit_length()-1)
            while True:
                try:newg,newv,stage_omega=checked_rk4(torch,engine,g,v,jump*spec['dt_min'],spec['cfl']);break
                except RuntimeError as exc:
                    emit('REJECTED_TRIAL_STEP',reason=str(exc),attempted_ticks=jump)
                    retries+=1
                    if jump==1:
                        checked_save(True,'TIMESTEP_FLOOR');emit('CHECKPOINTED_STOP',reason='TIMESTEP_FLOOR',trial_reason=str(exc));return 75
                    jump//=2
            g,v=newg,newv;tick+=jump;steps+=1;step_ticks.append(jump);max_cfl=max(max_cfl,jump*spec['dt_min']*stage_omega)
            due=tick in checks;publish=tick in saves
            reason='SIGNAL' if stop['signal'] else ('WALL_LIMIT' if time.monotonic()-start>=spec['wall_seconds'] else ('REQUESTED_PAUSE' if args.pause_after and steps>=args.pause_after else None))
            if due or reason:checked_save(publish or bool(reason),reason)
            if reason:
                emit('CHECKPOINTED_STOP',reason=reason,signal=stop['signal'],steps=steps,min_step_ticks=min(step_ticks),max_step_ticks=max(step_ticks),max_stage_cfl=max_cfl,retries=retries);return 75
        emit('TPP1_RUN_COMPLETE',steps=steps,min_step_ticks=min(step_ticks) if steps else None,max_step_ticks=max(step_ticks) if steps else None,max_stage_cfl=max_cfl,retries=retries,torch=torch.__version__,device=torch.cuda.get_device_name(0));return 0

if __name__=='__main__':
    try:sys.exit(main())
    except Exception as exc:
        print(json.dumps({'status':'REJECTED_OR_FAILED','reason':str(exc),'type':type(exc).__name__}),file=sys.stderr);sys.exit(2)
