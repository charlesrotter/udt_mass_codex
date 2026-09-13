#!/usr/bin/env python3
"""Record bounded package-owned process receipts and named-source preservation."""
from pathlib import Path
import json,datetime,hashlib,subprocess
P=Path(__file__).resolve().parent
ROOT=P.parent
NAV={'LIVE.md','HANDOFF.md','CURRENT_RESEARCH_PROGRAM.md','INDEX.md','UDT_RESEARCH_ROADMAP.md'}
now=lambda:datetime.datetime.now(datetime.timezone.utc).isoformat()
pins=json.loads((P/'SOURCE_PINS.json').read_text())
checks={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==h for p,h in pins.items() if p not in NAV}
assert all(checks.values())
launch=json.loads((P/'LAUNCH.json').read_text())
status=subprocess.check_output(['git','status','--short','--untracked-files=all'],cwd=ROOT,text=True)
original=''.join(l+'\n' for l in status.splitlines() if l.startswith('?? ') and not l[3:].startswith(P.name+'/'))
assert original==launch['original_status']
tracked=[l[3:] for l in status.splitlines() if not l.startswith('?? ')];assert set(tracked)==NAV
pres={'recorded_utc':now(),'all_non_navigation_pins_unchanged':all(checks.values()),'pin_checks':checks,
'original_untracked_status_sha256':hashlib.sha256(original.encode()).hexdigest(),
'original_untracked_expanded_paths':len(original.splitlines()),'original_untracked_status_names_unchanged':True,
'prestage_tracked_changes_exactly_five_navigation_files':sorted(tracked),'protected_payloads_hashed_or_read':False,
'backup_completeness':'UNVERIFIED','pre_reboot_unsaved_state':'UNVERIFIED','ScratchDisk_scope':'archive-dependent work only'}
(P/'PRESERVATION_CHECK.json').write_text(json.dumps(pres,indent=2)+'\n')
processes=[]
for f in sorted(P.rglob('*.json')):
 try:d=json.loads(f.read_text())
 except Exception:continue
 if isinstance(d,dict) and {'started_utc','duration_seconds','returncode','command'}<=d.keys():
  d=dict(d);d['receipt']=str(f.relative_to(ROOT));d['context']='routes' if '/review_routes/' in str(f) else 'evolving' if '/review_evolving/' in str(f) else 'parent'
  d['end_utc']=(datetime.datetime.fromisoformat(d['started_utc'])+datetime.timedelta(seconds=d['duration_seconds'])).isoformat();processes.append(d)
overlaps=[]
for i,a in enumerate(processes):
 for b in processes[i+1:]:
  start=max(datetime.datetime.fromisoformat(a['started_utc']),datetime.datetime.fromisoformat(b['started_utc']))
  end=min(datetime.datetime.fromisoformat(a['end_utc']),datetime.datetime.fromisoformat(b['end_utc']))
  if start<end:overlaps.append({'a':a['receipt'],'b':b['receipt'],'seconds':(end-start).total_seconds(),'same_context':a['context']==b['context']})
assert not any(o['same_context'] for o in overlaps)
full=next(x for x in processes if x['receipt'].endswith('current_full398.json'))
assert all(datetime.datetime.fromisoformat(x['started_utc'])>datetime.datetime.fromisoformat(full['end_utc']) for x in processes if x['context']=='parent' and x!=full)
record={'recorded_utc':now(),'processes':processes,'actual_process_overlaps':overlaps,'within_each_context_serialized':True,
'parent_full398_completed_before_parent_finite_runs':True,
'navigation':'Three retained passes359/1 deselected after evolving documentation edits; navigation_sealed is final. Actual full398 ran separately.',
'uncaptured_prechild_path_error':'DISCOVERY_AND_REVIEW_HISTORY.md; no scientific child started',
'assertion_counts_are_not_theorems':True,'scope':'Captured scientific/navigation intervals only; not a claim to have polled every process on the host.'}
(P/'CHECK_RESULTS.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps({'status':'PASS','pin_checks':len(checks),'original_untracked':len(original.splitlines()),'captured_processes':len(processes),'overlaps':len(overlaps)}))
