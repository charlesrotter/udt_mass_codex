"""Read-only progress from durable queue records; no scientific promotion."""
import json
from pathlib import Path
B=Path(__file__).resolve().parent;r=B/'production_runtime';manifest=r/'campaign.json'
if not manifest.exists():print(json.dumps(dict(status='NOT_GENERATED')));raise SystemExit(0)
m=json.loads(manifest.read_text());attempts=[]
for p in sorted((r/'attempts').glob('*')):
    if (p/'receipt.json').exists():attempts.append(json.loads((p/'receipt.json').read_text()))
complete={a['case'] for a in attempts if a['returncode']==0}
bad=[dict(case=a['case'],returncode=a['returncode'],reason=a.get('worker_stop_reason')) for a in attempts if a['returncode']!=0 and not (a['returncode']==75 and a.get('worker_stop_reason') in ['SIGNAL','REQUESTED_PAUSE'])]
active=[]
for p in r.glob('*.launch.json'):
    d=json.loads(p.read_text());stat=Path('/proc')/str(d['pid'])/'stat'
    alive=False;state=None
    if stat.exists():
        parts=stat.read_text().rsplit(')',1)[1].split();state=parts[0]
        alive=parts[19]==d.get('proc_start_ticks') and state!='Z'
    active.append(dict(label=p.stem,pid=d['pid'],same_process_alive=alive,process_state=state,receipt_exists=Path(d['result_receipt']).exists()))
incomplete=[]
for p in sorted((r/'attempts').glob('*')):
    if (p/'launch.json').exists() and not (p/'receipt.json').exists():
        d=json.loads((p/'launch.json').read_text());last={}
        if (p/'stdout').exists():
            for line in reversed((p/'stdout').read_text().splitlines()):
                try:last=json.loads(line);break
                except json.JSONDecodeError:pass
        incomplete.append(dict(case=d['case'],last_status=last.get('status'),tick=last.get('tick'),t=last.get('t')))
print(json.dumps(dict(status='QUEUE_COMPLETE_PENDING_SCIENTIFIC_REVIEW' if len(complete)==len(m['cases']) else 'INCOMPLETE',
    total_cases=len(m['cases']),completed_cases=len(complete),diagnostic_attempts=bad,
    unfinished_attempts=incomplete,controllers=active,worker_seconds=sum(a['wall_seconds'] for a in attempts),
    wall_limit_seconds=m['wall_seconds']),indent=2))
