#!/usr/bin/env python3
"""Final navigation/receipt correspondence only, no scientific calculation."""
import hashlib
import json
from pathlib import Path
import subprocess
import datetime

root=Path(__file__).resolve().parents[2]
pkg=root/'udt_two_shape_nonlinear_interaction_2026-09-11'
review=pkg/'review'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def git(*args):return subprocess.check_output(['git','-c','core.preloadIndex=false','-c','index.threads=1',*args],cwd=root,text=True).strip()
texts={name:(root/name).read_text() for name in ('LIVE.md','HANDOFF.md','CURRENT_RESEARCH_PROGRAM.md','INDEX.md','UDT_RESEARCH_ROADMAP.md')}
live=texts['LIVE.md'].split('### Next gate\n',1)[1].split('<!-- STARTUP_CURRENT_END -->',1)[0].strip()
handoff=texts['HANDOFF.md'].split('\nNext: ',1)[1].split('<!-- STARTUP_CURRENT_END -->',1)[0].strip()
program=texts['CURRENT_RESEARCH_PROGRAM.md'].split('## Current next gate\n',1)[1].strip()
assert live==handoff==program,('current next gate mismatch',live,handoff,program)
assert 'reviewed conditional candidate, UNPROMOTED' in live
assert 'no new campaign is authorized' in live
assert 'G312 membership unclosed' in live and 'physical identification remains OPEN' in live
counts={name:{'lines':len(text.splitlines()),'words':len(text.split())} for name,text in texts.items()}
assert counts['LIVE.md']=={'lines':112,'words':898}
assert counts['HANDOFF.md']=={'lines':84,'words':596}
assert counts['CURRENT_RESEARCH_PROGRAM.md']=={'lines':117,'words':1094}
assert counts['INDEX.md']=={'lines':118,'words':566}
expected_roots=set(texts)
assert set(git('diff','--name-only').splitlines())==expected_roots
baseline='b318072a9403d6acdd3a6d5749e1b366d76d29c5'
assert git('branch','--show-current')=='grok'
assert git('rev-parse','HEAD')==git('rev-parse','origin/grok')==baseline
for name in ('REVIEWED_RESULT.md','DECISION_BRIEF.md','SESSION_RECORD.md','review/REVIEW.md','review/REVIEW_RECEIPT.json'):
    assert (pkg/name).is_file(),name
result=(pkg/'REVIEWED_RESULT.md').read_text()
assert 'SECOND record derivatives' in result
assert 'Whole smooth density fields already contain' in result
assert 'HOLD FOR CHARLES\'S SEPARATE EXACT-SCOPE PROMOTION AUTHORIZATION' in result
assert 'Git could not create threaded lstat under the256MiB metadata cap' in ' '.join((pkg/'SESSION_RECORD.md').read_text().split())
guard=json.loads((pkg/'checks/final_guards.json').read_text())
assert guard['returncode']==0 and not guard['timeout']
assert guard['command']==['python3','-m','pytest','--noconftest','-q','tests/test_reviewed_backlog_banking.py','tests/test_startup_surface.py','-k','not full_foundational_premise_verifier']
assert '500 passed, 1 deselected' in (pkg/'checks/final_guards.stdout').read_text()
assert not (pkg/'checks/final_guards.stderr').read_bytes()
oldreview=json.loads((review/'REVIEW_RECEIPT.json').read_text())
for name,value in oldreview['sha256'].items():
    assert sha(root/name)==value,('changed prior review seal input',name)
files=[root/name for name in texts]+[pkg/name for name in ('REVIEWED_RESULT.md','DECISION_BRIEF.md','SESSION_RECORD.md')]
print(json.dumps({'status':'PASS','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'head':baseline,
 'local_origin_ref_matches':True,'next_gate_identical':True,'counts':counts,
 'all_prior_review_receipt_pins_match_current_bytes':True,
 'brief_chronology':'Prior review receipt pins seal-time final brief, not authentication of an earlier unsealed draft read; final brief read completely in this followup.',
 'parent_guard_result':'500 passed, 1 deselected, actual streams inspected; not rerun here',
 'sha256':{str(p.relative_to(root)):sha(p) for p in files}},indent=2))
