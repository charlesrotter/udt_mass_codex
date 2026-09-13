"""NR2 administrative correspondence and final-fidelity evidence checks; no science replay."""
from pathlib import Path
import datetime,hashlib,json,subprocess,sys
root=Path(__file__).resolve().parents[2]
pkg=root/'udt_geometric_field_choice_discrimination_2026-09-13'
checks=[]
def get(name):return json.loads((pkg/name).read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def gate(name,value,**evidence):checks.append({'name':name,'pass':bool(value),**evidence})
def pincheck(name,pins,base):
    actual={p:sha(base/p) for p in pins};gate(name,all(actual[p]==h for p,h in pins.items()),count=len(pins),actual=actual)
pincheck('13_scientific_sources',get('SOURCE_PINS.json')['sources'],root)
pincheck('5_full_audit_inputs',get('AUDIT_INPUT_PINS.json')['pins'],root)
pincheck('6_initial_candidate_freeze',get('CANDIDATE_FREEZE.json')['pins'],pkg)
pincheck('6_repair_freeze',get('REPAIR_FREEZE.json')['pins'],pkg)
pincheck('independent_check_freeze',get('review/INDEPENDENT_FREEZE.json')['pins'],pkg)
pincheck('6_tested_navigation_files',get('AUDIT_REUSE.json')['final_navigation_pins'],root)
sourcefirst=get('review/SOURCE_FIRST_PINS.json')
gate('source_first_unchanged',sha(pkg/'review/SOURCE_FIRST.md')==sourcefirst['source_first_sha256'])
indep=get('review/INDEPENDENT_RESULT.json')
gate('independent_code_result_correspondence',sha(pkg/'review/independent_checks.py')==indep['code_sha256'])
gate('126_independent_recorded_passes',indep['count']==126 and indep['passed']==126 and indep['all_pass'] and len(indep['checks'])==126 and all(c['pass'] for c in indep['checks']))
initial=get('EXACT_RESULT.json');repair=get('REPAIRED_RESULT.json');diag=get('COINCIDENT_DIAGNOSTIC.json')
gate('original_failures_preserved',initial['count']==50 and initial['passed']==49 and not initial['all_pass'] and sum(diag['checks'].values())==5 and len(diag['checks'])==6 and not diag['all_pass'])
gate('52_repaired_recorded_passes',repair['count']==52 and repair['passed']==52 and repair['all_pass'])
for name,want in [('checks/premise406',0),('checks/candidate_exact',1),('checks/coincident_diagnostic',1),('checks/candidate_repaired',0),('review/independent_capture',0),('checks/current_surface',0),('checks/navigation',0),('checks/prepublication_fetch',0)]:
    cap=get(name+'.json');gate(name+'_actual_capture_exit',cap['returncode']==want and not cap['timeout'],start=cap['started_utc'],seconds=cap['duration_seconds'])
gate('actual_full406_stdout','PASS: 406-row premise registry' in (pkg/'checks/premise406.stdout').read_text())
gate('actual_startup_stdout','359 passed, 1 deselected' in (pkg/'checks/navigation.stdout').read_text())
gate('actual_current_surface_stdout','PASS: actual NR2 current startup surface' in (pkg/'checks/current_surface.stdout').read_text())
names_raw=subprocess.check_output(['git','status','--porcelain=v1','--untracked-files=all'],cwd=root,text=True)
old_lines=[s for s in names_raw.splitlines() if s.startswith('?? ') and not s[3:].startswith(pkg.name+'/')]
name_digest=hashlib.sha256(('\n'.join(old_lines)+'\n').encode()).hexdigest()
preserve=get('PRESERVATION.json')
gate('original51_names_exact',len(old_lines)==51 and name_digest==preserve['status_names_sha256'],count=len(old_lines),sha256=name_digest,boundary='names only; protected payload bytes not read or hashed')
changed=subprocess.check_output(['git','diff','--name-only'],cwd=root,text=True).splitlines()
gate('only_six_reviewed_navigation_changes',changed==preserve['tracked_changes'],paths=changed)
index=subprocess.check_output(['git','diff','--cached','--name-only'],cwd=root,text=True)
gate('index_empty_before_publication',not index)
refs=subprocess.check_output(['git','rev-parse','HEAD','origin/grok'],cwd=root,text=True).splitlines()
branch=subprocess.check_output(['git','branch','--show-current'],cwd=root,text=True).strip()
gate('baseline_refs_and_branch',refs==preserve['refs'] and branch=='grok',refs=refs,branch=branch)
ledger=get('EXECUTION_INTERVALS.json');intervals=[]
for item in ledger['intervals']:
    cap=get(item['capture']);start=datetime.datetime.fromisoformat(cap['started_utc']);end=start+datetime.timedelta(seconds=cap['duration_seconds'])
    gate('interval_correspondence_'+item['capture'],item['start_utc']==start.isoformat() and item['end_utc']==end.isoformat() and item['seconds']==cap['duration_seconds'] and item['exit']==cap['returncode'])
    intervals.append((item['capture'],start,end))
overlaps=[]
for i,a in enumerate(intervals):
    for b in intervals[i+1:]:
        seconds=(min(a[2],b[2])-max(a[1],b[1])).total_seconds()
        if seconds>0:overlaps.append({'first':a[0],'second':b[0],'seconds':seconds})
gate('eight_existing_captured_operations_no_overlap',len(intervals)==8 and not overlaps and not ledger['captured_process_overlaps'],count=len(intervals),overlaps=overlaps)
out={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'meaning':'administrative correspondence checks; no science replay; counts are not proofs','checks':checks,'count':len(checks),'passed':sum(c['pass'] for c in checks),'all_pass':all(c['pass'] for c in checks),'code_sha256':sha(Path(__file__))}
with Path(sys.argv[1]).open('x') as f:json.dump(out,f,indent=2);f.write('\n')
print(json.dumps({k:out[k] for k in ['count','passed','all_pass']}))
sys.exit(0 if out['all_pass'] else 1)
