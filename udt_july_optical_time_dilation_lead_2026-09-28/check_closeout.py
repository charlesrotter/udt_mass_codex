#!/usr/bin/env python3
"""Focused preservation/packaging verification, not scientific certification."""
from pathlib import Path
import contextlib,hashlib,io,json,subprocess,sys,time
HERE=Path(__file__).resolve().parent
ROOT=HERE.parent
sys.path.insert(0,str(ROOT))
import verify_current_scientific_premises as v
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
pins=json.loads((HERE/'SOURCE_PINS.json').read_text())
initial=json.loads((HERE/'INITIAL_REVIEW_FREEZE.json').read_text())
repair=json.loads((HERE/'REPAIR_REVIEW_FREEZE.json').read_text())['files']
docs=json.loads((HERE/'FINAL_DOCUMENTATION_FREEZE.json').read_text())
allowed=set(docs['files'])
checks={}
checks['all_pinned_sources_unchanged']=all(sha(ROOT/n)==h for n,h in pins['sources'].items())
changed=set(subprocess.check_output(['git','diff','--name-only'],cwd=ROOT).decode().splitlines())
checks['tracked_edit_whitelist']=changed==allowed
checks['live_surface_freeze']=all(sha(ROOT/n)==h for n,h in docs['files'].items())
checks['package_documentation_freeze']=all(sha(HERE/n)==h for n,h in docs['package_docs'].items())
untracked=set(subprocess.check_output(['git','ls-files','--others','--exclude-standard','-z'],cwd=ROOT).decode().strip('\0').split('\0'))
checks['prior_untracked_names_preserved']=set(pins['prior_untracked_names'])<=untracked
checks['initial_candidate_preserved']=sha(HERE/'INITIAL_CANDIDATE.md')==initial['CANDIDATE.md']
checks['author_science_freeze']=all(sha(HERE/n)==initial[n] for n in ['check_lead.py','CHECK_RESULT.json','WORK_ORDER.md','SOURCE_PINS.json'])
checks['repaired_science_freeze']=all(sha(HERE/n)==h for n,h in repair.items() if n!='DECISION_BRIEF.md')
old_status='Status: CONDITIONAL MATHEMATICAL APPLICATION, UNPROMOTED; direct review pending.\n'
new_status='Status: VERIFIED-WITH-CAVEATS / CONDITIONAL MATHEMATICAL APPLICATION / UNPROMOTED.\nRead with REPAIR.md (domain and next-gate corrections) and\nTIME_DEPENDENT_FOLLOWUP.md. Final review: review/REPAIR_REVIEW.md.\nINITIAL_CANDIDATE.md preserves the original text; only this header has changed.\n'
restored=(HERE/'CANDIDATE.md').read_text().replace(new_status,old_status,1)
checks['candidate_status_only_update']=hashlib.sha256(restored.encode()).hexdigest()==initial['CANDIDATE.md']
new_brief='Reviewed conditional result, VERIFIED-WITH-CAVEATS, UNPROMOTED.\nFresh separate-context source-first/direct review and one bounded repair cycle\nare complete: review/REPAIR_REVIEW.md. No physical premise was adopted.\n'
old_brief='Draft pending completion of the separate-context repair review.\n'
restored_brief=(HERE/'DECISION_BRIEF.md').read_text().replace(new_brief,old_brief,1)
checks['brief_status_only_update']=hashlib.sha256(restored_brief.encode()).hexdigest()==repair['DECISION_BRIEF.md']
audit=json.loads((HERE/'premise_audit/RUN_RECORD.json').read_text())
checks['full_premise_audit_pass']=audit.get('exit_code')==0 and audit['inputs_unchanged'] and not (HERE/'premise_audit/stderr.txt').read_text()
checks['author_checks_pass']=json.loads((HERE/'CHECK_RESULT.json').read_text())['passed'] and json.loads((HERE/'TIME_DEPENDENT_CHECK_RESULT.json').read_text())['passed']
checks['review_records_present']=all((HERE/'review'/n).is_file() for n in ['SOURCE_FIRST_REVIEW.md','DIRECT_REVIEW.md','REPAIR_REVIEW.md','FINAL_DOCUMENTATION_REVIEW.md'])
out=io.StringIO();err=io.StringIO();t=time.monotonic()
with contextlib.redirect_stdout(out),contextlib.redirect_stderr(err):v.validate_startup_surface(ROOT)
checks['focused_startup_surface_pass']=True
(HERE/'final_startup.stdout.txt').write_text(out.getvalue());(HERE/'final_startup.stderr.txt').write_text(err.getvalue())
diffcheck=subprocess.run(['git','diff','--check'],cwd=ROOT,capture_output=True,text=True)
checks['git_diff_check']=diffcheck.returncode==0
r={'scope':'preservation, exact edit scope and focused startup checks; no new scientific evidence','checks':checks,'pinned_source_count':len(pins['sources']),'prior_untracked_name_count':len(pins['prior_untracked_names']),'full_audit_seconds':audit['elapsed_seconds'],'focused_check_seconds':time.monotonic()-t,'passed':all(checks.values())}
(HERE/'FINAL_CHECKS.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))
assert all(checks.values())
