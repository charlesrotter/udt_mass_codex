#!/usr/bin/env python3
"""Correspondence/preservation checks only; neither proof nor independent review."""
import hashlib
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PACKAGE = Path(__file__).resolve().parent
EXPECTED_HEAD = 'b318072a9403d6acdd3a6d5749e1b366d76d29c5'
EXPECTED_DIRT = '55e7c4508622f912730f9c068cc571c370b3977bc1110eb0a48a8218dbe024c2'
ALLOWED_NAV = {'LIVE.md','HANDOFF.md','CURRENT_RESEARCH_PROGRAM.md','INDEX.md','UDT_RESEARCH_ROADMAP.md'}

def git(*args):
    return subprocess.check_output(['git',*args],cwd=ROOT,text=True)

pins=[]
for filename, base in [('SOURCE_PINS.json',ROOT),('CANDIDATE_FREEZE.json',PACKAGE)]:
    data=json.loads((PACKAGE/filename).read_text())
    for name,want in data['sha256'].items():
        actual=hashlib.sha256((base/name).read_bytes()).hexdigest()
        assert actual==want, (filename,name,want,actual)
    pins.append({'manifest':filename,'count':len(data['sha256']),'status':'MATCH'})

branch=git('branch','--show-current').strip()
assert branch=='grok',branch
head=git('rev-parse','HEAD').strip()
status=git('status','--porcelain=v1').splitlines()
unrelated=[line for line in status if line.startswith('?? ') and not line[3:].startswith(PACKAGE.name+'/')]
fingerprint=hashlib.sha256(('\n'.join(unrelated)+'\n').encode()).hexdigest()
assert len(unrelated)==46 and fingerprint==EXPECTED_DIRT,(len(unrelated),fingerprint)
changed=git('diff','--name-only',EXPECTED_HEAD).splitlines()
assert all(name in ALLOWED_NAV or name.startswith(PACKAGE.name+'/') for name in changed),changed
staged=git('diff','--cached','--name-only').splitlines()
assert all(name in ALLOWED_NAV or name.startswith(PACKAGE.name+'/') for name in staged),staged

assert Path(ROOT/'CURRENT_SCIENTIFIC_PREMISES.tsv').read_text().count('\n')==396
print(json.dumps({'status':'PASS','meaning':'source and initial candidate correspondence; scoped changed names and unrelated status preservation only',
 'branch':branch,'head':head,'baseline_head':EXPECTED_HEAD,'pin_checks':pins,
 'original_untracked_count':len(unrelated),'original_untracked_status_sha256':fingerprint,
 'changed_since_baseline':changed,'staged_count':len(staged),
 'protected_payloads':'EXCLUDED_NOT_READ_OR_HASHED','backup_completeness':'UNVERIFIED',
 'pre_reboot_unsaved_state':'UNVERIFIED'},indent=2))
