"""Serial bounded preparation driver; one GPU worker, immutable per-call receipts."""
import argparse,hashlib,json,os,signal,subprocess,sys,time
from pathlib import Path

B=Path(__file__).resolve().parent;ROOT=B.parent
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def write(path,data):
    with Path(path).open('x') as f:json.dump(data,f,indent=2,sort_keys=True);f.write('\n')

def execute(name,spec,run,expected=0,extra=(),interrupt=False):
    receipts=B/'invocations';receipts.mkdir(exist_ok=True)
    spent=sum(json.loads(q.read_text())['wall_seconds'] for q in receipts.glob('*.json'))
    if spent>=600:raise RuntimeError('PREPARATION_TIME_BUDGET')
    used=sum(q.stat().st_size for q in B.rglob('*') if q.is_file())
    if used>=2*1024**3:raise RuntimeError('PREPARATION_OUTPUT_BUDGET')
    # Refuse a child whose maximum additional outputs would exceed the aggregate cap.
    config=json.loads((B/'specs'/f'{spec}.json').read_text())
    if used+config['output_bytes']>2*1024**3:raise RuntimeError('PREPARATION_OUTPUT_RESERVE')
    command=[sys.executable,str(B/'production_worker.py'),str(B/'specs'/f'{spec}.json'),str(B/'runs'/run),*extra]
    env=os.environ.copy();env['CUBLAS_WORKSPACE_CONFIG']=':4096:8'
    stdout_path=receipts/(name+'.stdout');stderr_path=receipts/(name+'.stderr')
    start=time.monotonic();sent=False;timed_out=False
    timeout=min(195,max(.01,600-spent))
    with stdout_path.open('x') as out,stderr_path.open('x') as err:
        proc=subprocess.Popen(command,stdout=subprocess.PIPE if interrupt else out,stderr=err,text=True,env=env,start_new_session=True)
        if interrupt:
            import selectors
            selector=selectors.DefaultSelector();selector.register(proc.stdout,selectors.EVENT_READ)
            while proc.poll() is None:
                if time.monotonic()-start>timeout:
                    os.killpg(proc.pid,signal.SIGKILL);timed_out=True;break
                for key,_ in selector.select(.05):
                    line=key.fileobj.readline()
                    if line:
                        out.write(line);out.flush()
                        try:row=json.loads(line)
                        except json.JSONDecodeError:continue
                        if not sent and row.get('status')=='CHECKED_STATE' and row.get('checkpoint'):
                            proc.send_signal(signal.SIGTERM);sent=True
            out.write(proc.stdout.read());proc.stdout.close();selector.close();rc=proc.wait()
        else:
            try:rc=proc.wait(timeout=timeout)
            except subprocess.TimeoutExpired:
                os.killpg(proc.pid,signal.SIGKILL);rc=proc.wait();timed_out=True
    elapsed=time.monotonic()-start
    row=dict(command=command,wall_seconds=elapsed,returncode=rc,expected=expected,timeout=timed_out,sigterm_sent=sent,spec_sha256=sha(B/'specs'/f'{spec}.json'),worker_sha256=sha(B/'production_worker.py'),stdout_sha256=sha(stdout_path),stderr_sha256=sha(stderr_path),aggregate_worker_wall_seconds=spent+elapsed)
    write(receipts/(name+'.json'),row);print(json.dumps(dict(name=name,**row)),flush=True)
    if timed_out or rc!=expected:raise RuntimeError('UNEXPECTED_WORKER_RETURN: '+name)
    return row

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('stage',choices=['engineering','science','load']);args=ap.parse_args()
    if args.stage=='engineering':
        execute('engineering_full','engineering','engineering_full')
        execute('engineering_pause','engineering','engineering_paused',75,['--pause-after','8'])
        execute('engineering_resume','engineering','engineering_paused',0,['--resume'])
        execute('engineering_signal','engineering','engineering_signal',75,interrupt=True)
        execute('engineering_signal_resume','engineering','engineering_signal',0,['--resume'])
        execute('wall_stop','wall_stop','wall_stop',75)
        execute('floor_stop','floor_stop','floor_stop',75)
        execute('output_stop','output_stop','output_stop',2)
    elif args.stage=='science':
        cases=['kasner_n16','kasner_n16_half','axial1_n16','axial1_n24','axial1_n24_half','axial1_n32','oblique1_n16','oblique1_n24','oblique1_n24_half','oblique1_n32','axial3_n24','oblique3_n24','phase1_n24']
        for name in cases:execute(name,name,name)
    else:execute('load_n48','load_n48','load_n48')
