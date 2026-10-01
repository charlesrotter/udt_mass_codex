"""Finite supplied-clock replay via the unchanged TPP1 query implementation."""
import argparse,hashlib,json,subprocess,sys
from pathlib import Path
B=Path(__file__).resolve().parent;ROOT=B.parent;TPP=ROOT/'udt_time_live_production_preparation_2026-10-01'
def sha(q):return hashlib.sha256(Path(q).read_bytes()).hexdigest()
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--limit',type=int,default=0);args=ap.parse_args()
    if args.limit<0:raise ValueError('INVALID_LIMIT')
    manifest=B/'production_runtime/campaign.json';m=json.loads(manifest.read_text());mh=sha(manifest)
    rows=m['cases'][:args.limit] if args.limit else m['cases'];result=[]
    for row in rows:
        directory=B/'production_analysis'/row['id'];assembly=json.loads((directory/'ASSEMBLY.json').read_text())
        if assembly['input_sha256'].get(str(manifest.resolve()))!=mh:raise ValueError('CLOCK_MANIFEST_BINDING')
        history=directory/'histories'/f'{row["id"]}_window2.npz'
        if assembly['output_sha256'].get(str(history.resolve()))!=sha(history):raise ValueError('CLOCK_HISTORY_CHANGED')
        output=directory/'clock.json';prefix=directory/'clock_capture'
        if output.exists():
            old=json.loads(output.read_text());receipt=json.loads(prefix.with_suffix('.json').read_text())
            if old['history_sha256']!=sha(history) or receipt['returncode']!=0:raise ValueError('CLOCK_PRIOR_REQUIRES_REVIEW')
            for stream in ['stdout','stderr']:
                if sha(prefix.with_suffix('.'+stream))!=receipt[stream+'_sha256']:raise ValueError('CLOCK_CAPTURE_CHANGED')
        else:
            command=[sys.executable,str(B/'capture.py'),str(prefix),sys.executable,str(TPP/'clock_checks.py'),str(history),str(output)]
            code=subprocess.call(command)
            if code:return code
        result.append(dict(case=row['id'],path=str(output.relative_to(ROOT)),sha256=sha(output)))
    print(json.dumps(dict(status='SELECTED_CLOCK_REPLAYS_COMPLETE',count=len(result),manifest_sha256=mh,results=result,
        scope='Supplied late-window queries using fixed TPP method; no sign selection or gap-spanning interpolation'),indent=2))
    return 0
if __name__=='__main__':raise SystemExit(main())
