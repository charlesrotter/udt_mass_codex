#!/usr/bin/env python3
"""Bounded correspondence/preservation checks; not a scientific proof harness."""
from pathlib import Path
from fractions import Fraction
import csv
import datetime
import hashlib
import json
import subprocess

PACKAGE = Path(__file__).resolve().parents[1]
ROOT = PACKAGE.parent
BASELINE = '896da97dc2484b72fa346d0c0ab17055a1dd6fcd'
STATUS_SHA = '55e7c4508622f912730f9c068cc571c370b3977bc1110eb0a48a8218dbe024c2'


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT, text=True).strip()


checks = []
with (PACKAGE/'SOURCE_MANIFEST.tsv').open() as f:
    sources = list(csv.DictReader(f, delimiter='\t'))
for row in sources:
    assert sha(ROOT/row['path']) == row['sha256'], row['path']
checks.append({'name':'source_pins', 'passed':True, 'file_count':len(sources)})

freeze = json.loads((PACKAGE/'INITIAL_REVIEW_FREEZE.json').read_text())
for name, value in freeze['files'].items():
    path = PACKAGE/('checks/INITIAL_check_candidate.py' if name=='check_candidate.py' else name)
    assert sha(path)==value, name
checks.append({'name':'all_initial_freeze_bytes_preserved','passed':True,
               'file_count':len(freeze['files']),
               'author_script_preserved_at':'checks/INITIAL_check_candidate.py'})

for label, directory, manifest in [('partner','whiteboard','ARTIFACT_SHA256SUMS'),
                                    ('reviewer','review','SHA256SUMS')]:
    command=['sha256sum','-c',manifest]
    result=subprocess.run(command,cwd=PACKAGE/directory,capture_output=True,text=True,timeout=120)
    assert result.returncode==0,(label,result.stdout,result.stderr)
    checks.append({'name':label+'_manifest','passed':True,'command':command,
                   'cwd':str((PACKAGE/directory).relative_to(ROOT)),
                   'exit_code':result.returncode,'stdout':result.stdout,'stderr':result.stderr})

for name in ['author_01','author_02','navigation_01','startup_surface_01']:
    run=json.loads((PACKAGE/'checks'/f'{name}.run.json').read_text())
    assert run['exit_code']==0,name
checks.append({'name':'recorded_exit_codes','passed':True,
               'initial_author_check_caveat':'static_time_constancy EXCLUDED; original exit 0 retained'})

author=json.loads((PACKAGE/'checks/author_02.stdout.json').read_text())
assert author['status']=='PASS' and author['check_count']==51
assert author['candidate_sha256']==sha(PACKAGE/'INITIAL_CANDIDATE.md')
assert author['script_sha256']==sha(PACKAGE/'check_candidate.py')
review=json.loads((PACKAGE/'review/COMPLETION.json').read_text())
assert review['candidate_sha256']==sha(PACKAGE/'INITIAL_CANDIDATE.md')
assert review['review_sha256']==sha(PACKAGE/'review/REVIEW.md')

# Standard-library exact arithmetic from saved independent reviewer quantities.
# This checks saved quantity correspondence, not a second computation of metric curvature.
saved=json.loads((PACKAGE/'review/run_01.stdout.json').read_text())
mixed=next(r for r in saved['records'] if r['name']=='mixed_kinematics')
m,dm,V,A,W,R=(Fraction(mixed[k]) for k in ['mean','dot_mean','V','A','W','RicUU'])
value=3*dm-3*m*m-Fraction(15,2)*V+A+W
assert value==R==8
checks.append({'name':'mixed_saved_record_fraction_recomputation','passed':True,
               'input_file':'review/run_01.stdout.json','input_sha256':sha(PACKAGE/'review/run_01.stdout.json'),
               'recomputed_RicUU':str(value),'direct_reviewer_RicUU':str(R),
               'limitation':'same-parent saved-value arithmetic; direct curvature belongs to reviewer implementation'})

assert git('branch','--show-current')=='grok'
changed=git('diff','--name-only',BASELINE).splitlines()
allowed={'INDEX.md','UDT_RESEARCH_ROADMAP.md'}
prefix=PACKAGE.name+'/'
assert all(name in allowed or name.startswith(prefix) for name in changed),changed
status=subprocess.check_output(['git','status','--porcelain=v1'],cwd=ROOT)
unrelated=b''.join(line for line in status.splitlines(keepends=True)
                   if line[3:].decode().strip() not in allowed
                   and not line[3:].decode().strip().startswith(prefix))
assert len(unrelated.splitlines())==46
assert hashlib.sha256(unrelated).hexdigest()==STATUS_SHA
checks.append({'name':'authorized_paths_and_visible_state','passed':True,
               'unrelated_status_entries':46,'unrelated_status_sha256':STATUS_SHA,
               'limitation':'status text only; no protected payload hashing or backup verification'})

print(json.dumps({'status':'PASS','type':'parent closeout correspondence and preservation',
                  'timestamp_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
                  'source_baseline':BASELINE,'head_at_check':git('rev-parse','HEAD'),
                  'command':['python3',str(Path(__file__).resolve().relative_to(ROOT))],
                  'candidate_sha256':sha(PACKAGE/'INITIAL_CANDIDATE.md'),
                  'review_sha256':sha(PACKAGE/'review/REVIEW.md'),
                  'decision_brief_sha256':sha(PACKAGE/'DECISION_BRIEF.md'),
                  'verdict':'VERIFIED-WITH-CAVEATS; conditional UNPROMOTED',
                  'checks':checks,'new_full365_run':False,
                  'premise_audit':'Fresh top-level session run passed before this campaign; unchanged scientific sources verified here.',
                  'publication':'Exact subsequent commit/push evidence is recorded separately; not inferred from these checks.'},indent=2))
