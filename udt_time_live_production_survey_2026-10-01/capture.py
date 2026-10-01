"""Capture a finite authorized command with memory limits and no time cutoff."""
import argparse,datetime,hashlib,json,os,resource,signal,subprocess,time
from pathlib import Path

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--gpu',action='store_true')
    ap.add_argument('--memory-mib',type=int,default=2048)
    ap.add_argument('prefix');ap.add_argument('command',nargs=argparse.REMAINDER)
    args=ap.parse_args()
    if not args.command or not 1<=args.memory_mib<=4096:raise ValueError('CAPTURE_SCHEMA')
    if resource.getrlimit(resource.RLIMIT_CPU)!=(resource.RLIM_INFINITY,resource.RLIM_INFINITY):
        raise RuntimeError('INHERITED_CPU_TIMEOUT_REQUIRES_REVIEW')
    prefix=Path(args.prefix).resolve();prefix.parent.mkdir(parents=True,exist_ok=True)
    outputs={k:Path(str(prefix)+'.'+k) for k in ['stdout','stderr','json']}
    if any(q.exists() for q in outputs.values()):raise RuntimeError('REFUSE_CAPTURE_OVERWRITE')
    mapping_bytes=(128*1024**3) if args.gpu else args.memory_mib*1024**2
    def memory_limit():resource.setrlimit(resource.RLIMIT_AS,(mapping_bytes,mapping_bytes))
    env=os.environ.copy()
    for key in ['OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS']:env[key]='1'
    env['CUBLAS_WORKSPACE_CONFIG']=':4096:8'
    start=time.monotonic();utc=datetime.datetime.now(datetime.timezone.utc).isoformat();signals=[]
    with outputs['stdout'].open('x') as out,outputs['stderr'].open('x') as err:
        process=subprocess.Popen(args.command,stdout=out,stderr=err,env=env,
            start_new_session=True,preexec_fn=memory_limit)
        def forward(signum,frame):
            signals.append(signum)
            if process.poll() is None:os.killpg(process.pid,signum)
        signal.signal(signal.SIGTERM,forward);signal.signal(signal.SIGINT,forward)
        code=process.wait()
    sha=lambda q:hashlib.sha256(Path(q).read_bytes()).hexdigest()
    result=dict(command=args.command,cwd=str(Path.cwd()),started_utc=utc,
        duration_seconds=time.monotonic()-start,returncode=code,wall_timeout_seconds=None,
        cpu_timeout_seconds=None,address_space_bytes=mapping_bytes,
        memory_scope='Virtual mapping allowance; worker separately enforces allocated GPU bytes' if args.gpu else 'Process virtual address limit',
        maxrss_kib=resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,
        forwarded_signals=signals,stdout_sha256=sha(outputs['stdout']),stderr_sha256=sha(outputs['stderr']),
        capture_sha256=sha(__file__))
    with outputs['json'].open('x') as f:json.dump(result,f,indent=2);f.write('\n')
    print(json.dumps(result),flush=True)
    return code if 0<=code<=255 else 1

if __name__=='__main__':raise SystemExit(main())
