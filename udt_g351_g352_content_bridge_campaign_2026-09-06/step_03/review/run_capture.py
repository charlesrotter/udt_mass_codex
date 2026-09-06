"""Portable read-only child runner; output requires a new, nonexistent prefix."""
import argparse, datetime, json, os, pathlib, resource, subprocess, sys, time
p=argparse.ArgumentParser()
p.add_argument('--cwd', required=True)
p.add_argument('--prefix', required=True)
p.add_argument('--seconds', type=int, default=60)
p.add_argument('--mib', type=int, default=512)
p.add_argument('command', nargs=argparse.REMAINDER)
a=p.parse_args()
paths=[pathlib.Path(a.prefix+s) for s in ('.stdout','.stderr','.json')]
if any(f.exists() for f in paths): raise SystemExit('Refusing to overwrite output')
cmd=a.command[1:] if a.command[:1]==['--'] else a.command
def limit():
    resource.setrlimit(resource.RLIMIT_AS,(a.mib*1024**2,a.mib*1024**2))
    resource.setrlimit(resource.RLIMIT_CPU,(a.seconds,a.seconds+1))
stamp=datetime.datetime.now(datetime.timezone.utc).isoformat()
start=time.monotonic()
with paths[0].open('xb') as out, paths[1].open('xb') as err:
    try:
        r=subprocess.run(cmd,cwd=a.cwd,stdout=out,stderr=err,timeout=a.seconds,
                         preexec_fn=limit,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'})
        code=r.returncode
    except subprocess.TimeoutExpired:
        code='TIMEOUT'
meta=dict(command=cmd,cwd=a.cwd,start_utc=stamp,wall_seconds=time.monotonic()-start,
          returncode=code,limit_mib=a.mib,timeout_seconds=a.seconds,
          max_rss_kib=resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss)
with paths[2].open('x') as f: json.dump(meta,f,indent=2); f.write('\n')
print(json.dumps(meta,indent=2))
sys.exit(0 if code==0 else 1)
