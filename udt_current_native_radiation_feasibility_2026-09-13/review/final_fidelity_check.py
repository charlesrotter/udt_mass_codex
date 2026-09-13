"""Final documentary correspondence check; no scientific rerun or protected reads.

Freeze: check known reviewed-source hashes, exact current nav bytes and allowed
git diff/status names; inspect capture results and final lay repair hashes.
One metadata subprocess under180s/2048MiB. This does not re-prove source science
or preclaim commit/push. Hash only the named authorized documents and sources.
"""
from pathlib import Path
import datetime,hashlib,json,subprocess,sys

root=Path(__file__).resolve().parents[2]
pkg=root/'udt_current_native_radiation_feasibility_2026-09-13'
r=pkg/'review'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def git(*args):return subprocess.check_output(['git',*args],cwd=root,text=True)
nav=['LIVE.md','HANDOFF.md','CURRENT_RESEARCH_PROGRAM.md','INDEX.md','MEMORY.md','UDT_RESEARCH_ROADMAP.md']
reviewed=json.loads((r/'DIRECT_REVIEW_PINS.json').read_text())
reuse=json.loads((pkg/'AUDIT_REUSE.json').read_text())
launch=json.loads((pkg/'LAUNCH.json').read_text())
repair=json.loads((pkg/'FIDELITY_REPAIRS.json').read_text())
direct_drift=[n for n,h in reviewed['pins'].items() if sha(pkg/n)!=h]
input_drift=[n for n,h in reuse['audited_scientific_input_pins_unchanged'].items() if sha(root/n)!=h]
nav_drift=[n for n,h in reuse['final_navigation_pins'].items() if sha(root/n)!=h]
status=git('status','--short','--untracked-files=all')
original=''.join(s+'\n' for s in status.splitlines() if s.startswith('?? ') and not s.startswith('?? '+pkg.name+'/'))
changed=git('diff','--name-only').splitlines();staged=git('diff','--cached','--name-only').splitlines()
captures={}
for name in ['premise406','candidate_exact','non_einstein_exact','startup_active','startup_active_isolated','current_surface_final','navigation_final']:
    d=json.loads((pkg/'checks'/f'{name}.json').read_text())
    captures[name]={'exit':d['returncode'],'timeout':d['timeout'],'start':d['started_utc'],'seconds':d['duration_seconds']}
brief_ok=sha(pkg/repair['file'])==repair['after_sha256']
sourcefirst_ok=sha(r/'SOURCE_FIRST.md')==json.loads((r/'INDEPENDENT_FREEZE.json').read_text())['pins']['SOURCE_FIRST.md']
metadata_timing_ok='initial_recorded_utc' in reuse and 'final_navigation_record_updated_utc' in reuse
nav_stdout=(pkg/'checks/navigation_final.stdout').read_text()
audit_stdout=(pkg/'checks/premise406.stdout').read_text()
checks={'direct_scientific_pins_unchanged':not direct_drift,'audited_inputs_unchanged':not input_drift,'six_actual_navigation_pins_match':not nav_drift,'exact_original51_status_names':original==launch['original_untracked_status'] and len(original.splitlines())==51,'only_six_authorized_tracked_changes':set(changed)==set(nav),'index_empty_before_publication':not staged,'brief_repair_hash_matches':brief_ok,'source_first_preserved':sourcefirst_ok,'audit_reuse_timing_scope_repaired':metadata_timing_ok,'final_startup_actual359_1':'359 passed, 1 deselected' in nav_stdout and captures['navigation_final']['exit']==0,'new_full406_actual_pass':'PASS: 406-row premise registry' in audit_stdout and captures['premise406']['exit']==0,'current_surface_actual_pass':captures['current_surface_final']['exit']==0,'startup_initial_failure_retained':captures['startup_active']['exit']==4,'startup_repaired_actual_pass':captures['startup_active_isolated']['exit']==0}
documents=['REVIEWED_RESULT.md','DECISION_BRIEF.md','COMPARISON_BOUNDARY.md','RESULT_SCOPE.tsv','README.md','CLOSEOUT.md','CHECKPOINT.md','SOURCE_MAP.md','SOURCE_MAP_ADDENDUM.md','AUDIT_REUSE.json','AUDIT_INPUT_PINS.json','PRESERVATION_CHECK.json','FIDELITY_REPAIRS.json','PREPUBLICATION_SYNC.json','EXECUTION_INTERVALS.json','EXECUTION_INTERVALS_PRE_FIDELITY.json','STARTUP_CHECK_DIAGNOSTIC.md','LAUNCH.json','PROFILE_SCOPE_CLARIFICATION.md','NON_EINSTEIN_CONTROL.md','review/DIRECT_REVIEW.md','review/DIRECT_REVIEW_PINS.json','review/ALLOCATION.json','review/SOURCE_FIRST.md','review/FINAL_FIDELITY_REQUEST.md']
pins={str((pkg/n).relative_to(root)):sha(pkg/n) for n in documents}
pins.update({n:sha(root/n) for n in nav})
now=datetime.datetime.now(datetime.timezone.utc)
out={'utc':now.isoformat(),'kind':'final documentation/preservation/capture correspondence; not a scientific rerun','checks':checks,'all_pass':all(checks.values()),'head':git('rev-parse','HEAD').strip(),'origin_grok':git('rev-parse','origin/grok').strip(),'branch':git('branch','--show-current').strip(),'source_drift':direct_drift,'audited_input_drift':input_drift,'nav_drift':nav_drift,'original_untracked_count':len(original.splitlines()),'original_status_sha256':hashlib.sha256(original.encode()).hexdigest(),'tracked_changed_paths':changed,'staged_paths':staged,'captures':captures,'document_pins':pins,'publication':'not yet performed; parent-owned administrative gate','reviewer_runtime_model':'UNATTESTED','different_model':'UNTESTED','code_sha256':sha(Path(__file__))}
with Path(sys.argv[1]).open('x') as f:json.dump(out,f,indent=2);f.write('\n')
print(json.dumps({'all_pass':out['all_pass'],'checks':checks,'document_count':len(pins),'head':out['head'],'origin_grok':out['origin_grok'],'original_untracked_count':out['original_untracked_count']}))
sys.exit(0 if out['all_pass'] else 1)
