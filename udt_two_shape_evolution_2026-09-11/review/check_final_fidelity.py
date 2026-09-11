"""Proportional final document/receipt/pin checks, not a scientific verifier."""
import datetime,hashlib,json,pathlib,subprocess
repo=pathlib.Path(__file__).resolve().parents[2]
root=pathlib.Path(__file__).resolve().parents[1]
review=pathlib.Path(__file__).resolve().parent
nav=['CURRENT_RESEARCH_PROGRAM.md','HANDOFF.md','INDEX.md','LIVE.md','UDT_RESEARCH_ROADMAP.md']
for record,base in [('CANDIDATE_FREEZE.json',root),('PRECOMPUTATION_FREEZE.json',repo),('SOURCE_PINS.json',repo),('review/REVIEW_RECEIPT.json',repo)]:
 for p,d in json.loads((root/record).read_text())['sha256'].items(): assert hashlib.sha256((base/p).read_bytes()).hexdigest()==d,(record,p)
changed=subprocess.check_output(['git','diff','--name-only'],cwd=repo,text=True).splitlines()
assert sorted(changed)==nav,changed
assert subprocess.check_output(['git','diff','--cached','--name-only'],cwd=repo,text=True).strip()==''
head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=repo,text=True).strip()
origin=subprocess.check_output(['git','rev-parse','origin/grok'],cwd=repo,text=True).strip()
assert head==origin=='1de84bf0e8b8781201ede8d0486489a22dbf7d07'
subprocess.run(['git','diff','--check'],cwd=repo,check=True)
gate='G383--G412 exact-scope banking is COMPLETE; G413=TI1 is banked; TI2 is reviewed conditional, UNPROMOTED; scope: INDEX.\nG312 membership unclosed; G352 physical-realization: physical identification remains OPEN.\nStop for lay discussion with Charles on TI2 promotion and profile-dependence proposal; no new campaign is authorized.'
for p in ['LIVE.md','HANDOFF.md','CURRENT_RESEARCH_PROGRAM.md']:assert gate in (repo/p).read_text(),p
receipts=[]
for name,word in [('current396_closeout','PASS: 396-row premise registry'),('final_navigation','539 passed, 1 deselected'),('preservation','"verdict": "PASS"')]:
 r=json.loads((root/f'checks/{name}.json').read_text())
 assert r['returncode']==0 and not r['timeout']
 assert (root/f'checks/{name}.stderr').read_bytes()==b''
 assert word in (root/f'checks/{name}.stdout').read_text()
 receipts.append({'name':name,'duration_seconds':r['duration_seconds']})
summary=json.loads((root/'CLOSEOUT_PREMISE_RESULT.json').read_text())
assert summary['audit']==json.loads((root/'checks/current396_closeout.json').read_text())
assert hashlib.sha256((root/'CLOSEOUT_PREMISE_INPUTS.json').read_bytes()).hexdigest()==summary['audit_input_record_sha256']
session=' '.join((root/'SESSION_RECORD.md').read_text().split())
assert 'checked the 33 candidate pins, then failed before comparing the precomputation-file bytes' in session
assert 'transcribed from the tool output' in (root/'checks/PRESERVATION_PROBE_PATH_ERROR.md').read_text()
sync=json.loads((root/'PREPUBLICATION_SYNC.json').read_text())
assert sync['actual_exit_code']==0 and sync['HEAD']==head and sync['origin_grok_after_actual_fetch']==origin
assert not (repo/'udt_two_shape_profile_dependence_2026-09-11').exists()
scratch=[str(p.relative_to(root)) for p in root.rglob('*') if p.is_dir() and p.name in ['__pycache__','.pytest_cache']]
files=[root/p for p in ['REVIEWED_RESULT.md','DECISION_BRIEF.md','SESSION_RECORD.md','MANIFEST_SCOPE.md','PREPUBLICATION_SYNC.json','CLOSEOUT_PREMISE_INPUTS.json','CLOSEOUT_PREMISE_RESULT.json','check_preservation.py','checks/PRESERVATION_PROBE_PATH_ERROR.md']]
files += [repo/p for p in nav]
pins={str(p.relative_to(repo)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
sizes={p:{'lines':len((repo/p).read_text().splitlines()),'words':len((repo/p).read_text().split())} for p in ['LIVE.md','HANDOFF.md','CURRENT_RESEARCH_PROGRAM.md','INDEX.md']}
print(json.dumps({'status':'PASS','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'scope':'Final prose/correspondence checks; fresh network fetch and full audit attributed, not reviewer reruns',
 'head':head,'local_origin_grok':origin,'exact_tracked_changes':changed,'matched_next_gate':True,
 'parent_receipts_inspected_not_replayed':receipts,'navigation_sizes':sizes,'excluded_cache_directories_present':scratch,
 'prospective_TI3_directory_absent':True,'final_document_sha256':pins},indent=2))
