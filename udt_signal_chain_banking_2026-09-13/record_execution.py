#!/usr/bin/env python3
"""Record actual captured intervals; no claim to census uncaptured administrative calls."""
from pathlib import Path
import json,datetime
P=Path(__file__).resolve().parent
intervals=[]
for f in sorted(P.rglob('*.json')):
    if f.name=='EXECUTION_INTERVALS.json': continue
    try: d=json.loads(f.read_text())
    except (ValueError,UnicodeError): continue
    if not isinstance(d,dict) or not all(k in d for k in ['started_utc','duration_seconds','returncode','command']):continue
    start=datetime.datetime.fromisoformat(d['started_utc']);end=start+datetime.timedelta(seconds=d['duration_seconds'])
    intervals.append({'capture':str(f.relative_to(P)),'context':'reviewer' if 'review' in f.relative_to(P).parts else 'parent','start_utc':start.isoformat(),'end_utc':end.isoformat(),'seconds':d['duration_seconds'],'exit':d['returncode'],'command':d['command']})
overlaps=[]
for i,a in enumerate(intervals):
    for b in intervals[i+1:]:
        lo=max(datetime.datetime.fromisoformat(a['start_utc']),datetime.datetime.fromisoformat(b['start_utc']))
        hi=min(datetime.datetime.fromisoformat(a['end_utc']),datetime.datetime.fromisoformat(b['end_utc']))
        if hi>lo:overlaps.append({'a':a['capture'],'b':b['capture'],'seconds':(hi-lo).total_seconds(),'same_context':a['context']==b['context']})
assert not any(x['same_context'] for x in overlaps)
result={'recorded_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'scope':'Captured scientific/check processes only; uncaptured administrative/source-reading commands are not a complete CPU census. Reviewer-context overlap is separately recorded in its final receipt.','intervals':intervals,'captured_process_overlaps':overlaps,'same_context_overlap_detected':False,'runtime_model':'UNATTESTED','general_capacity':'UNVERIFIED'}
(P/'EXECUTION_INTERVALS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'captures':len(intervals),'overlaps':overlaps}))
