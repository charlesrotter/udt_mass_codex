#!/usr/bin/env python3
"""Reviewer's same-code replays and exact version/row correspondence checks."""
import csv
import datetime
import hashlib
import io
import json
from pathlib import Path
import subprocess
import time

root=Path.cwd()
pkg=root/'udt_exact_metric_kernel_expansion_2026-09-10'
out=pkg/'review'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
utc=lambda:datetime.datetime.now(datetime.timezone.utc).isoformat()
runs=[]
for tag,script,original in [
 ('author',pkg/'check_exact_geometry.py',pkg/'checks/author.stdout.json'),
 ('construction',pkg/'whiteboard/check_construction.py',pkg/'whiteboard/CHECK_STDOUT.json'),
 ('followup',pkg/'whiteboard/check_followup.py',pkg/'whiteboard/FOLLOWUP_STDOUT.json')]:
    argv=['python3','-B',str(script.relative_to(root))]
    rec={'tag':tag,'argv':argv,'cwd':str(root),'timeout_seconds':120,'start_utc':utc(),
         'script_sha256':sha(script),'kind':'same-code replay, not independent derivation'}
    tick=time.monotonic()
    result=subprocess.run(argv,capture_output=True,text=True,timeout=120)
    rec.update(end_utc=utc(),elapsed_seconds=time.monotonic()-tick,exit_code=result.returncode)
    (out/(tag+'_replay.stdout.json')).write_text(result.stdout)
    (out/(tag+'_replay.stderr.txt')).write_text(result.stderr)
    rec['stdout_matches_saved_bytes']=result.stdout.encode()==original.read_bytes()
    if result.returncode==0:
        data=json.loads(result.stdout)
        rec['check_count']=data['check_count']
        rec['control_count']=data.get('control_count')
    runs.append(rec)
    (out/'REPLAY_RUNS.json').write_text(json.dumps(runs,indent=2)+'\n')
    if result.returncode or not rec['stdout_matches_saved_bytes']:
        raise ValueError('Replay mismatch: '+tag)

# Explicit exception-based guard in the author code must reject optimized Python.
argv=['python3','-O','-B',str((pkg/'check_exact_geometry.py').relative_to(root))]
tick=time.monotonic(); start=utc()
r=subprocess.run(argv,capture_output=True,text=True,timeout=120)
(out/'author_optimized_guard.stdout.txt').write_text(r.stdout)
(out/'author_optimized_guard.stderr.txt').write_text(r.stderr)
guard={'argv':argv,'cwd':str(root),'timeout_seconds':120,'start_utc':start,'end_utc':utc(),
       'elapsed_seconds':time.monotonic()-tick,'exit_code':r.returncode,
       'expected_rejection':r.returncode!=0 and 'Scientific evidence requires ordinary Python, not -O' in r.stderr}
(out/'AUTHOR_GUARD_RUN.json').write_text(json.dumps(guard,indent=2)+'\n')
if not guard['expected_rejection']:
    raise ValueError('Author -O guard failed')

freeze=json.loads((pkg/'INITIAL_REVIEW_FREEZE.json').read_text())
initial={name:{'expected':expected,'actual':sha(root/name),'match':sha(root/name)==expected}
         for name,expected in freeze['files'].items()}
source={}
for r in csv.DictReader((pkg/'SOURCE_MANIFEST.tsv').read_text().splitlines(),delimiter='\t'):
    if r['path']=='CANON.md':
        source[r['path']]={'status':'NOT_REHASHED; canon content not load-bearing for this review'}
        continue
    actual=sha(root/r['path'])
    source[r['path']]={'expected':r['sha256'],'actual':actual,'match':actual==r['sha256']}
saved=json.loads((pkg/'SOURCE_REGISTRY_ROWS.json').read_text())
needed={r['premise_id'] for r in saved}
current={r['premise_id']:r for r in csv.DictReader(io.StringIO((root/'CURRENT_SCIENTIFIC_PREMISES.tsv').read_text()),delimiter='\t') if r['premise_id'] in needed}
rows={r['premise_id']:r==current[r['premise_id']] for r in saved}
extra=['udt_g180_completed_pair_smooth_family_descent_2026-08-19/EXACT_DERIVATION.md']
status=subprocess.run(['git','status','--short','--branch'],capture_output=True,text=True,check=True).stdout
diff=subprocess.run(['git','diff','--','AGENTS.md','CURRENT_RESEARCH_PROGRAM.md','UDT_RESEARCH_ROADMAP.md','INDEX.md'],capture_output=True,text=True,check=True).stdout
(out/'VISIBLE_STATUS.txt').write_text(status)
(out/'METHOD_DIFF_REVIEWED.patch').write_text(diff)
head=subprocess.run(['git','rev-parse','HEAD'],capture_output=True,text=True,check=True).stdout.strip()
branch=subprocess.run(['git','branch','--show-current'],capture_output=True,text=True,check=True).stdout.strip()
record={'utc':utc(),'head':head,'branch':branch,'initial_frozen_files':initial,
        'sources':source,'exact_saved_registry_rows_match_current':rows,
        'additional_read_source_hashes':{p:sha(root/p) for p in extra},
        'method_current_hashes':{p:sha(root/p) for p in ['AGENTS.md','CURRENT_RESEARCH_PROGRAM.md','UDT_RESEARCH_ROADMAP.md']},
        'method_initial_hashes':freeze['method_doc_hashes'],
        'status_note':'Visible filenames only; protected contents were not read or hashed.',
        'scope':'Hash correspondence, not truth, chronology or full historical-suite execution.'}
(out/'PRESERVATION.json').write_text(json.dumps(record,indent=2)+'\n')
if not all(v['match'] for v in initial.values()) or not all(v.get('match',True) for v in source.values()) or not all(rows.values()):
    raise ValueError('Preservation mismatch')
print(json.dumps({'status':'PASS','replay_counts':[r['check_count'] for r in runs],
 'initial_freeze_files_matched':len(initial),'source_hashes_matched':sum('match' in v for v in source.values()),
 'selected_registry_rows_matched':len(rows),'optimized_guard_expected_exit':guard['exit_code'],
 'all_replays_stdout_byte_identical':True},indent=2))
