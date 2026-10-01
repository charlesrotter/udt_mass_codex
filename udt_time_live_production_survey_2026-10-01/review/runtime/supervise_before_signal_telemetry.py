"""Serial resumable case supervisor with a persistent finite queue/output budget and no elapsed-time stop.

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
    ap=argparse.ArgumentParser();ap.add_argument('manifest');ap.add_argument('runtime');ap.add_argument('--stop-after',type=int,default=0);args=ap.parse_args()
    if args.stop_after<0:raise ValueError('INVALID_QUEUE_PAUSE')
    manifest=owned(args.manifest);m=json.loads(manifest.read_text());runtime=owned(args.runtime)
    if set(m)!={'wall_seconds','output_bytes','storage_roots','source_sha256','cases'}:raise ValueError('QUEUE_SCHEMA')
    if m['wall_seconds'] is not None:raise ValueError('QUEUE_TIME_LIMIT_NOT_AUTHORIZED')
    if type(m['output_bytes'])!=int or not 0<m['output_bytes']<=64*1024**3:raise ValueError('QUEUE_OUTPUT_LIMIT')
    roots=[owned(q) for q in m['storage_roots']]
    if not roots or not any(runtime.is_relative_to(q) for q in roots):raise ValueError('RUNTIME_NOT_BUDGETED')
    if not m['cases'] or len(m['cases'])>234:raise ValueError('QUEUE_CASE_COUNT')
    ids=set();run_paths=set();initials={}
    for row in m['cases']:
        if set(row)!={'id','spec','spec_sha256','run'} or not re.fullmatch('[a-z0-9_-]+',row['id']) or row['id'] in ids:raise ValueError('QUEUE_CASE_SCHEMA')
        ids.add(row['id']);spec=owned(row['spec']);run=owned(row['run'])
        if run in run_paths:raise ValueError('DUPLICATE_RUN_PATH')
        run_paths.add(run)
        if not run.is_relative_to(B/'runs') or not any(run.is_relative_to(q) for q in roots):raise ValueError('RUN_NOT_BUDGETED')
        if sha(spec)!=row['spec_sha256']:raise ValueError('QUEUE_SPEC_CHANGED')
        initials[row['id']]=owned(ROOT/json.loads(spec.read_text())['initial'])
    required={B/'supervise.py',B/'production_worker.py',B/'initial_family.py',ROOT/'udt_three_spatial_smoke_2026-10-01/initial_data.py',ROOT/'udt_three_spatial_smoke_2026-10-01/evolution.py',ROOT/'udt_three_spatial_smoke_2026-10-01/constraints.py',ROOT/'udt_time_live_smoke_gate_2026-09-30/checkpoint_io.py'}
    external={ROOT/'udt_time_live_production_preparation_2026-10-01'/p for p in ['initial_family.py','families/axial1.json','families/oblique1.json','specs/axial1_n24.json','specs/axial1_n24_half.json','specs/axial1_n32.json']}
    required.add(ROOT/'udt_time_live_production_preparation_2026-10-01/initial_family.py')
    if not required<={Path(q).resolve() for q in m['source_sha256']}:raise ValueError('QUEUE_SOURCE_BINDINGS')
    resolved_bindings={Path(q).resolve():h for q,h in m['source_sha256'].items()}
    if not set(initials.values())<=set(resolved_bindings):raise ValueError('INITIAL_SOURCE_BINDINGS')
    for q,h in m['source_sha256'].items():
        q=Path(q).resolve()
        if not (q.is_relative_to(B) or q in required or q in external) or sha(q)!=h:raise ValueError('QUEUE_SOURCE_CHANGED')
    runtime.mkdir(parents=True,exist_ok=True)
    with (runtime/'supervisor.lock').open('a+') as lock:
        fcntl.flock(lock.fileno(),fcntl.LOCK_EX|fcntl.LOCK_NB)
        binding=runtime/'manifest.sha256'
        if binding.exists():
            if binding.read_text().strip()!=sha(manifest):raise ValueError('QUEUE_RESUME_MISMATCH')
        else:
            with binding.open('x') as f:f.write(sha(manifest)+'\n')
        # Null is a bound declaration; no deadline or elapsed-time stop is created.
        attempts=runtime/'attempts';attempts.mkdir(exist_ok=True)
        previous=[json.loads(q.read_text()) for q in attempts.glob('*/receipt.json')]
        if any(r['returncode'] not in (0,75) or (r['returncode']==75 and r.get('worker_stop_reason') not in ['SIGNAL','REQUESTED_PAUSE']) for r in previous):raise RuntimeError('DIAGNOSTIC_ATTEMPT_REQUIRES_REVIEW')
        completed={r['case'] for r in previous if r['returncode']==0}
        spent=sum(r['wall_seconds'] for r in previous);start=time.monotonic();requested={'signal':None}
        def stop(signum,frame):requested['signal']=signum
        signal.signal(signal.SIGTERM,stop);signal.signal(signal.SIGINT,stop)
        # A missing receipt leaves an unknown execution outcome. Do not silently resume.
        if any(not (q/'receipt.json').exists() for q in attempts.iterdir() if q.is_dir()):raise RuntimeError('INCOMPLETE_ATTEMPT_REQUIRES_REVIEW')
        def used():return sum(q.stat().st_size for root in roots if root.exists() for q in root.rglob('*') if q.is_file())
        newly_completed=0
        for row in m['cases']:
            if row['id'] in completed:continue
            spec=json.loads(owned(row['spec']).read_text());run=owned(row['run'])
            if sha(owned(row['spec']))!=row['spec_sha256']:raise ValueError('QUEUE_SPEC_CHANGED')
            for q in required|{initials[row['id']]}:
                if sha(q)!=resolved_bindings[q]:raise ValueError('QUEUE_SOURCE_CHANGED')
            if requested['signal'] or used()+spec['output_bytes']>m['output_bytes']:
                print(json.dumps(dict(status='QUEUE_STOP',wall_seconds_limit=None,used_bytes=used(),signal=requested['signal'])));return 75
            folder=attempts/f'{len(list(attempts.iterdir())):05d}_{row["id"]}';folder.mkdir()
            command=[sys.executable,str(B/'production_worker.py'),str(owned(row['spec'])),str(run)]
            resume=run.exists()
            if resume:command.append('--resume')
            env=os.environ.copy();env['CUBLAS_WORKSPACE_CONFIG']=':4096:8';began=time.monotonic();sent=False
            write(folder/'launch.json',dict(case=row['id'],command=command,wall_seconds_limit=None,manifest_sha256=sha(manifest)))
            with (folder/'stdout').open('x') as out,(folder/'stderr').open('x') as err:
                proc=subprocess.Popen(command,stdout=out,stderr=err,env=env,start_new_session=True)
                while proc.poll() is None:
                    if requested['signal'] and not sent:
                        os.killpg(proc.pid,requested['signal']);sent=True
                    # Manual signals request a checkpoint. No timer escalates them.
                    time.sleep(.05)
                rc=proc.wait()
            elapsed=time.monotonic()-began
            worker_rows=[]
            for line in (folder/'stdout').read_text().splitlines():
                try:worker_rows.append(json.loads(line))
                except json.JSONDecodeError:pass
            last=worker_rows[-1] if worker_rows else {}
            write(folder/'receipt.json',dict(case=row['id'],command=command,returncode=rc,wall_seconds=elapsed,resume=resume,sigterm_sent=sent,sigkill_sent=False,worker_status=last.get('status'),worker_stop_reason=last.get('reason'),stdout_sha256=sha(folder/'stdout'),stderr_sha256=sha(folder/'stderr')))
            print(json.dumps(dict(case=row['id'],returncode=rc,seconds=elapsed,used_bytes=used())),flush=True)
            if rc!=0:return 75 if rc==75 else 2
            newly_completed+=1
            completed.add(row['id'])
            if args.stop_after and newly_completed>=args.stop_after and len(completed)<len(m['cases']):
                print(json.dumps(dict(status='QUEUE_CHECKPOINT',newly_completed=newly_completed)));return 75
        print(json.dumps(dict(status='QUEUE_COMPLETE',cases=len(m['cases']),previously_completed=len(completed),execution_seconds=spent+time.monotonic()-start,used_bytes=used())));return 0
if __name__=='__main__':
    try:raise SystemExit(main())
    except Exception as exc:print(json.dumps(dict(status='SUPERVISOR_FAILED',reason=str(exc),type=type(exc).__name__)),file=sys.stderr);raise SystemExit(2)
