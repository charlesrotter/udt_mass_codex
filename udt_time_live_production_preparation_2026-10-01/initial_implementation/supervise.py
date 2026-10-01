"""Serial resumable case supervisor with a persistent wall/output budget.

It launches only an explicit byte-bound queue. No queue or new physics is inferred.
"""
import argparse,fcntl,hashlib,json,os,re,signal,subprocess,sys,time
from pathlib import Path
B=Path(__file__).resolve().parent;ROOT=B.parent
def sha(q):return hashlib.sha256(Path(q).read_bytes()).hexdigest()
def write(q,x):
    with Path(q).open('x') as f:json.dump(x,f,indent=2,sort_keys=True);f.write('\n')
def owned(q):
    q=Path(q).resolve()
    if not q.is_relative_to(B):raise ValueError('SUPERVISOR_PATH_SCOPE')
    return q
def main():
    ap=argparse.ArgumentParser();ap.add_argument('manifest');ap.add_argument('runtime');args=ap.parse_args()
    manifest=owned(args.manifest);m=json.loads(manifest.read_text());runtime=owned(args.runtime)
    if set(m)!={'wall_seconds','output_bytes','storage_roots','source_sha256','cases'}:raise ValueError('QUEUE_SCHEMA')
    if type(m['wall_seconds']) not in (int,float) or not 0<m['wall_seconds']<=21600:raise ValueError('QUEUE_WALL_LIMIT')
    if type(m['output_bytes'])!=int or not 0<m['output_bytes']<=64*1024**3:raise ValueError('QUEUE_OUTPUT_LIMIT')
    roots=[owned(q) for q in m['storage_roots']]
    if not roots or not any(runtime.is_relative_to(q) for q in roots):raise ValueError('RUNTIME_NOT_BUDGETED')
    if not m['cases'] or len(m['cases'])>512:raise ValueError('QUEUE_CASE_COUNT')
    ids=set()
    for row in m['cases']:
        if set(row)!={'id','spec','spec_sha256','run'} or not re.fullmatch('[a-z0-9_-]+',row['id']) or row['id'] in ids:raise ValueError('QUEUE_CASE_SCHEMA')
        ids.add(row['id']);spec=owned(row['spec']);run=owned(row['run'])
        if not run.is_relative_to(B/'runs') or not any(run.is_relative_to(q) for q in roots):raise ValueError('RUN_NOT_BUDGETED')
        if sha(spec)!=row['spec_sha256']:raise ValueError('QUEUE_SPEC_CHANGED')
    if not m['source_sha256']:raise ValueError('QUEUE_SOURCE_BINDINGS')
    for q,h in m['source_sha256'].items():
        q=Path(q).resolve()
        if not q.is_relative_to(ROOT) or sha(q)!=h:raise ValueError('QUEUE_SOURCE_CHANGED')
    runtime.mkdir(parents=True,exist_ok=True)
    with (runtime/'supervisor.lock').open('a+') as lock:
        fcntl.flock(lock.fileno(),fcntl.LOCK_EX|fcntl.LOCK_NB)
        binding=runtime/'manifest.sha256'
        if binding.exists():
            if binding.read_text().strip()!=sha(manifest):raise ValueError('QUEUE_RESUME_MISMATCH')
        else:
            with binding.open('x') as f:f.write(sha(manifest)+'\n')
        attempts=runtime/'attempts';attempts.mkdir(exist_ok=True)
        previous=[json.loads(q.read_text()) for q in attempts.glob('*/receipt.json')]
        completed={r['case'] for r in previous if r['returncode']==0}
        spent=sum(r['wall_seconds'] for r in previous);start=time.monotonic();requested={'signal':None}
        def stop(signum,frame):requested['signal']=signum
        signal.signal(signal.SIGTERM,stop);signal.signal(signal.SIGINT,stop)
        # A missing receipt represents unknown consumed time. Do not silently resume.
        if any(not (q/'receipt.json').exists() for q in attempts.iterdir() if q.is_dir()):raise RuntimeError('INCOMPLETE_ATTEMPT_REQUIRES_REVIEW')
        def used():return sum(q.stat().st_size for root in roots if root.exists() for q in root.rglob('*') if q.is_file())
        for row in m['cases']:
            if row['id'] in completed:continue
            remaining=m['wall_seconds']-spent-(time.monotonic()-start)
            spec=json.loads(owned(row['spec']).read_text());run=owned(row['run'])
            if requested['signal'] or remaining<5 or used()+spec['output_bytes']>m['output_bytes']:
                print(json.dumps(dict(status='QUEUE_STOP',remaining_seconds=remaining,used_bytes=used(),signal=requested['signal'])));return 75
            folder=attempts/f'{len(list(attempts.iterdir())):05d}_{row["id"]}';folder.mkdir()
            command=[sys.executable,str(B/'production_worker.py'),str(owned(row['spec'])),str(run)]
            resume=run.exists()
            if resume:command.append('--resume')
            env=os.environ.copy();env['CUBLAS_WORKSPACE_CONFIG']=':4096:8';began=time.monotonic();sent=False;killed=False
            write(folder/'launch.json',dict(case=row['id'],command=command,remaining_seconds=remaining,manifest_sha256=sha(manifest)))
            with (folder/'stdout').open('x') as out,(folder/'stderr').open('x') as err:
                proc=subprocess.Popen(command,stdout=out,stderr=err,env=env,start_new_session=True)
                deadline=began+min(175,remaining-5)
                while proc.poll() is None:
                    if (requested['signal'] or time.monotonic()>=deadline) and not sent:
                        os.killpg(proc.pid,signal.SIGTERM);sent=True;kill_at=time.monotonic()+5
                    if sent and time.monotonic()>=kill_at:
                        os.killpg(proc.pid,signal.SIGKILL);killed=True;break
                    time.sleep(.05)
                rc=proc.wait()
            elapsed=time.monotonic()-began
            write(folder/'receipt.json',dict(case=row['id'],command=command,returncode=rc,wall_seconds=elapsed,resume=resume,sigterm_sent=sent,sigkill_sent=killed,stdout_sha256=sha(folder/'stdout'),stderr_sha256=sha(folder/'stderr')))
            print(json.dumps(dict(case=row['id'],returncode=rc,seconds=elapsed,used_bytes=used())),flush=True)
            if rc!=0:return 75 if rc==75 else 2
        print(json.dumps(dict(status='QUEUE_COMPLETE',cases=len(m['cases']),previously_completed=len(completed),execution_seconds=spent+time.monotonic()-start,used_bytes=used())));return 0
if __name__=='__main__':
    try:raise SystemExit(main())
    except Exception as exc:print(json.dumps(dict(status='SUPERVISOR_FAILED',reason=str(exc),type=type(exc).__name__)),file=sys.stderr);raise SystemExit(2)
