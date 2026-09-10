#!/usr/bin/env python3
"""Package correspondence and preservation only; not additional scientific review."""
from pathlib import Path
import csv, datetime, hashlib, json, subprocess

P=Path(__file__).resolve().parents[1]
R=P.parent
BASE='e1b43cc41ec1a8456bfac5096bf02f74801b7123'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
read=lambda p:json.loads(p.read_text())
checks=[]

def manifest(path,label):
    with path.open() as f:rows=list(csv.DictReader(f,delimiter='\t'))
    for row in rows:
        p=R/row['path']
        assert sha(p)==row['sha256'],row['path']
        if 'bytes' in row:assert p.stat().st_size==int(row['bytes'])
    checks.append({'name':label,'entries':len(rows),'passed':True})

manifest(P/'SOURCE_MANIFEST.tsv','source_pins')
manifest(P/'whiteboard/ARTIFACT_MANIFEST.tsv','construction_artifacts')
manifest(P/'whiteboard/SOURCE_MANIFEST.tsv','construction_sources')
manifest(P/'review/ARTIFACT_MANIFEST.tsv','review_artifacts')
freeze=read(P/'INITIAL_REVIEW_FREEZE.json')
for name,digest in freeze['files'].items():assert sha(P/name)==digest,name
checks.append({'name':'initial_bytes_preserved','entries':len(freeze['files']),'passed':True})
completion=read(P/'review/COMPLETION.json')
for key,name in [('candidate_sha256','INITIAL_CANDIDATE.md'),('review_sha256','review/REVIEW.md'),('final_brief_sha256','DECISION_BRIEF.md')]:
    assert completion[key]==sha(P/name),name
assert read(P/'review/FINAL_FIDELITY.json')['final_brief_sha256']==sha(P/'DECISION_BRIEF.md')
checks.append({'name':'reviewed_versions_correspond','passed':True})
for name,expected in [('author_01',1),('author_02',0),('navigation_01',0),('startup_surface_01',0)]:
    assert read(P/'checks'/f'{name}.run.json')['exit_code']==expected,name
assert read(P/'checks/author_02.stdout.json')['check_count']==96
assert read(P/'review/independent.run.json')['exit_code']==0
ind=read(P/'review/independent.stdout.json')
assert (ind['positive_count'],ind['negative_count'])==(88,18)
for run in read(P/'review/REPLAY_RESULTS.json'):
    assert run['exit_code']==run['expected_exit_code'] and run['expected_result_observed'],run['case']
    for stream in ['stdout','stderr']:
        assert sha(P/'review'/f"{run['case']}.{stream}.txt")==run[f'{stream}_sha256']
checks.append({'name':'actual_run_results_and_expected_rejections','passed':True,
               'caveat':'author_01 exit1 is a preserved failed construction run; reviewer expected exits1 are explicit guard/failure reproduction checks'})
saved=read(P/'checks/SAVED_RECORD_RECOMPUTATION.json')
assert saved['status']=='PASS' and saved['recomputed_W']=='9/8'
assert saved['input_sha256']==sha(P/saved['input'])
checks.append({'name':'saved_value_recomputation_correspondence','passed':True,'scope':saved['scope']})
git=lambda *a:subprocess.check_output(['git',*a],cwd=R,text=True).strip()
assert git('branch','--show-current')=='grok'
allowed={'INDEX.md','UDT_RESEARCH_ROADMAP.md'}
assert all(v in allowed or v.startswith(P.name+'/') for v in git('diff','--name-only',BASE).splitlines())
status=subprocess.check_output(['git','status','--porcelain=v1'],cwd=R,text=True)
other=''.join(v+'\n' for v in status.splitlines() if v[3:] not in allowed and not v[3:].startswith(P.name+'/'))
assert len(other.splitlines())==46
assert hashlib.sha256(other.encode()).hexdigest()=='55e7c4508622f912730f9c068cc571c370b3977bc1110eb0a48a8218dbe024c2'
checks.append({'name':'authorized_scope_and_original_visible_state','passed':True,'unrelated_entries':46,
               'limitation':'status text only; protected payloads not inspected/hashed; not backup verification'})
print(json.dumps({'status':'PASS','type':'parent correspondence and preservation closeout',
    'timestamp_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'command':['python3',str(Path(__file__).resolve().relative_to(R))],
    'script_sha256':sha(Path(__file__)),'baseline':BASE,'head_at_check':git('rev-parse','HEAD'),
    'verdict':'VERIFIED-WITH-CAVEATS; conditional UNPROMOTED','candidate_sha256':completion['candidate_sha256'],
    'review_sha256':completion['review_sha256'],'final_brief_sha256':completion['final_brief_sha256'],
    'checks':checks,'new_full365_run':False,
    'premise_audit':'Actual required full365 passed earlier this top-level session; present sources unchanged; no new run claimed.',
    'publication':'Subsequent actual commit/push evidence belongs to PUBLICATION.json and parent tool receipts.'},indent=2))
