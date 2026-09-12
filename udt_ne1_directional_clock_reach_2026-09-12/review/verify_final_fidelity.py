#!/usr/bin/env python3
"""Read-only source/document/receipt correspondence; no scientific reproof."""
import datetime
import hashlib
import json
import subprocess
from pathlib import Path

R=Path(__file__).resolve().parents[2]
P=Path(__file__).resolve().parent.parent
sha=lambda b:hashlib.sha256(b).hexdigest()
def git(*args):
    return subprocess.check_output(['git',*args],cwd=R)

launch=json.loads((P/'LAUNCH.json').read_text())
head=git('rev-parse','HEAD').decode().strip()
branch=git('branch','--show-current').decode().strip()
assert head==launch['baseline_head'] and branch=='grok'
allowed=['CURRENT_RESEARCH_PROGRAM.md','HANDOFF.md','INDEX.md','LIVE.md','UDT_RESEARCH_ROADMAP.md']
changed=git('diff','--name-only').decode().splitlines()
assert sorted(changed)==allowed, 'exact five tracked pointer changes'
assert not git('diff','--cached','--name-only'), 'review precedes staging'
subprocess.run(['git','diff','--check'],cwd=R,check=True)
untracked=[line for line in git('status','--short').decode().splitlines() if line.startswith('?? ') and line!='?? '+P.name+'/']
assert untracked==launch['original_untracked_status'], 'original unrelated names/status preservation'

pins=json.loads((P/'SOURCE_PINS.json').read_text())
nav=json.loads((P/'NAVIGATION_AND_PRESERVATION.json').read_text())
pin_changed=[]
for name,h in pins.items():
    assert sha(git('show',head+':'+name))==h, 'baseline source pin'
    if sha((R/name).read_bytes())!=h:pin_changed.append(name)
assert sorted(pin_changed)==sorted(nav['changed_pinned_pointers'])
assert len(pins)-len(pin_changed)==19
assert 'INDEX.md' not in pins
for name,rec in nav['changed_current_pointers'].items():
    assert sha(git('show',head+':'+name))==rec['old_sha256'], 'pointer original bytes'
    assert sha((R/name).read_bytes())==rec['new_sha256'], 'pointer final bytes'
    assert (name in pins)==rec['in_pre_audit23_pin_set']
assert sorted(nav['changed_current_pointers'])==allowed
assert sha((R/'CURRENT_SCIENTIFIC_PREMISES.tsv').read_bytes())==pins['CURRENT_SCIENTIFIC_PREMISES.tsv']

candidate=json.loads((P/'CANDIDATE_FREEZE.json').read_text())
for name,h in candidate['sha256'].items():
    assert sha((P/name).read_bytes())==h, 'complete mathematical candidate freeze'
implementation=json.loads((P/'IMPLEMENTATION_FREEZE.json').read_text())
assert sha((P/'check_numeric.py').read_bytes())==implementation['sha256']
for sealname in ['SOURCE_STAGE_COMPLETE.json','DIRECT_REVIEW_SEAL.json']:
    seal=json.loads((P/'review'/sealname).read_text())
    for name,h in seal['files'].items():
        assert sha((P/'review'/name).read_bytes())==h, 'review seal '+sealname

editorial=json.loads((P/'EDITORIAL_CLARIFICATIONS.json').read_text())
initial=(P/'editorial/INITIAL_DECISION_BRIEF.md').read_bytes()
assert sha(initial)==editorial['changes'][0]['initial_sha256']
assert sha((P/'DECISION_BRIEF.md').read_bytes())==editorial['changes'][0]['final_sha256']
objections=json.loads((P/'review/EDITORIAL_OBJECTIONS.json').read_text())
assert sha(initial)==objections['sha256_at_record']

for name,summary in nav['navigation_results'].items():
    capture=json.loads((P/f'checks/{name}.json').read_text())
    assert summary['receipt']==capture and capture['returncode']==0 and not capture['timeout']
    stdout=(P/f'checks/{name}.stdout').read_text()
    assert stdout.splitlines()[-1]==summary['stdout_tail']
    assert '359 passed, 1 deselected' in stdout
    assert not (P/f'checks/{name}.stderr').read_bytes()
audit=json.loads((P/'CURRENT_AUDIT_RECEIPT.json').read_text())
capture=json.loads((P/'checks/current_full398.json').read_text())
assert audit['actual_audit']==capture and capture['returncode']==0 and not capture['timeout']
assert sha((P/'checks/current_full398.stdout').read_bytes())==audit['stdout_sha256']
assert b'PASS: 398-row premise registry' in (P/'checks/current_full398.stdout').read_bytes()
assert not (P/'checks/current_full398.stderr').read_bytes()

docs=['WORK_ORDER.md','LAUNCH.json','SOURCE_PINS.json','INITIAL_CANDIDATE.md','INITIAL_FREEZE.json',
    'SOURCE_FIRST_ADDENDUM.md','CANDIDATE_FREEZE.json','CHECK_CONTRACT.md','check_numeric.py',
    'IMPLEMENTATION_FREEZE.json','REVIEWED_RESULT.md','DECISION_BRIEF.md','DISCOVERY_HISTORY.md',
    'CHECK_RESULTS.json','CURRENT_AUDIT_RECEIPT.json','NAVIGATION_AND_PRESERVATION.json',
    'NAVIGATION_RECEIPT_DIAGNOSTIC.md','EDITORIAL_CLARIFICATIONS.json','CLOSEOUT.md',
    'editorial/INITIAL_DECISION_BRIEF.md']
record={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'result':'PASS',
    'head':head,'branch':branch,'exact_tracked_pointer_changes':allowed,
    'unrelated_untracked_name_status_count':len(untracked),'unrelated_name_status_matches_launch':True,
    'unchanged_source_pins':19,'changed_pinned_pointers':sorted(pin_changed),'index_separately_authenticated':True,
    'complete_candidate_implementation_and_review_seals_unchanged':True,
    'original_brief_preserved_and_editorial_correspondence':True,
    'new_current398_saved_receipt_authenticated':True,'navigation_runs_each':[359,1],
    'package_final_docs_sha256':{name:sha((P/name).read_bytes()) for name in docs},
    'current_pointer_sha256':{name:sha((R/name).read_bytes()) for name in allowed},
    'scope':'Read-only correspondence/fidelity; no audit replay, independent process monitoring, protected-payload byte verification, backup, scientific promotion, or future publication attestation.'}
print(json.dumps(record,indent=2))
