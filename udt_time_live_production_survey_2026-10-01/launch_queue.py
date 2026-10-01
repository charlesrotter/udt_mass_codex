"""Start the explicit TPS1 queue with durable logs and no elapsed-time limit."""
import argparse,datetime,hashlib,json,os,re,subprocess,sys
from pathlib import Path
B=Path(__file__).resolve().parent;ROOT=B.parent

def main():
    ap=argparse.ArgumentParser();ap.add_argument('label');ap.add_argument('--stop-after',type=int,default=0)
    args=ap.parse_args()
    if not re.fullmatch(r'first_gate|continuation|resume_[1-9][0-9]*',args.label) or args.stop_after<0:raise ValueError('LAUNCH_SCOPE')
    if args.label=='first_gate' and args.stop_after!=3:raise ValueError('FIRST_GATE_MUST_STOP_AFTER_THREE')
    runtime=B/'production_runtime';manifest=runtime/'campaign.json'
    if not manifest.exists():raise ValueError('CAMPAIGN_NOT_GENERATED')
    if args.label!='first_gate':
        gate=json.loads((B/'FIRST_GATE.json').read_text())
        if gate.get('status')!='PASS' or gate.get('manifest_sha256')!=hashlib.sha256(manifest.read_bytes()).hexdigest():
            raise ValueError('FIRST_GATE_NOT_PASSED_FOR_MANIFEST')
        for p,h in gate['source_sha256'].items():
            if hashlib.sha256((ROOT/p).read_bytes()).hexdigest()!=h:raise ValueError('GATE_SOURCE_CHANGED')
    prefix=runtime/args.label
    paths={suffix:Path(str(prefix)+'.'+suffix) for suffix in ['launch.json','controller.stdout','controller.stderr']}
    if any(p.exists() for p in paths.values()) or any(Path(str(prefix)+'.'+x).exists() for x in ['json','stdout','stderr']):
        raise ValueError('REFUSE_LAUNCH_OVERWRITE')
    command=[sys.executable,str(B/'capture.py'),'--gpu',str(prefix),sys.executable,
             str(B/'supervise.py'),str(manifest),str(runtime)]
    if args.stop_after:command+=['--stop-after',str(args.stop_after)]
    with paths['controller.stdout'].open('x') as out,paths['controller.stderr'].open('x') as err:
        process=subprocess.Popen(command,cwd=ROOT,stdin=subprocess.DEVNULL,stdout=out,stderr=err,
                                 start_new_session=True,close_fds=True)
    stat=Path('/proc')/str(process.pid)/'stat'
    try:identity=stat.read_text().rsplit(')',1)[1].split()[19]
    except FileNotFoundError:identity=None
    record=dict(pid=process.pid,proc_start_ticks=identity,command=command,cwd=str(ROOT),
        utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),wall_timeout_seconds=None,
        manifest_sha256=hashlib.sha256(manifest.read_bytes()).hexdigest(),
        launch_source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        result_receipt=str(prefix)+'.json',stdout=str(prefix)+'.stdout',stderr=str(prefix)+'.stderr',
        stop='Verify PID/start identity, then send SIGTERM to this capture PID for forwarding and checkpointing; no automatic timed kill')
    with paths['launch.json'].open('x') as f:json.dump(record,f,indent=2);f.write('\n')
    print(json.dumps(record,indent=2),flush=True)

if __name__=='__main__':main()
