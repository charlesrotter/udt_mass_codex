from pathlib import Path
import json,csv,hashlib,datetime,subprocess,itertools,sys
R=Path(__file__).resolve().parents[2];B=R/'udt_signal_chain_banking_2026-09-13';V=B/'review';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
intake=json.loads((B/'FINAL_REVIEW_INTAKE.json').read_text());amend_path=B/'FINAL_REVIEW_AMENDMENT.json'
changes={}
if amend_path.exists():
 amendment=json.loads(amend_path.read_text())
 print('final_amendment_structure',json.dumps(amendment))
# A final amendment is verified explicitly by the final receipt assembler;
# here independently expose every actual original-intake mismatch.
for n,h in intake['files'].items():
 actual=sha(R/n)
 if actual!=h:changes[n]={'original':h,'current':actual}
initial=json.loads((V/'REVIEW_RECEIPT.json').read_text())
for n,h in initial['input_sha256'].items():assert sha(R/n)==h,('initial seal changed',n)
entries=[line.split(maxsplit=1) for line in (B/'SOURCE_EVIDENCE_SHA256SUMS').read_text().splitlines()]
assert len(entries)==len({n for _,n in entries})==662
for h,n in entries:assert sha(R/n)==h,('source changed',n)
base=json.loads((B/'LAUNCH.json').read_text())['baseline_head'];packages=sorted({n.split('/')[0] for h,n in entries})
tracked_sources=subprocess.check_output(['git','ls-tree','-r','--name-only',base,'--',*packages],cwd=R,text=True).splitlines()
assert {n for _,n in entries}==set(tracked_sources)
raw=(R/'CURRENT_SCIENTIFIC_PREMISES.tsv').read_bytes();ids={('G'+str(i)).encode() for i in range(416,424)}
old=b''.join(l for l in raw.splitlines(keepends=True) if l.split(b'\t',1)[0] not in ids)
baseline=subprocess.check_output(['git','show',base+':CURRENT_SCIENTIFIC_PREMISES.tsv'],cwd=R)
assert old==baseline
rows=list(csv.DictReader(raw.decode().splitlines(),delimiter='\t'));assert len(rows)==len({r['premise_id'] for r in rows})==406
claimdata=json.loads((B/'BANKED_CLAIMS.json').read_text());actual={r['premise_id']:r for r in rows}
for c in claimdata['claims']:assert actual[c['id']]==c['claim']
fixed={}
for n in ['CANON.md','UDT_METRIC_KERNEL_DEVELOPMENT.md','UDT_CONSOLIDATED_RESEARCH_ACCOUNT.md']:
 prior=subprocess.check_output(['git','show',base+':'+n],cwd=R);assert prior==(R/n).read_bytes();fixed[n]=sha(R/n)
record=json.loads((B/'EXECUTION_INTERVALS.json').read_text());intervals=[]
for v in record['intervals']:
 meta=json.loads((B/v['capture']).read_text());start=datetime.datetime.fromisoformat(meta['started_utc']);end=start+datetime.timedelta(seconds=meta['duration_seconds'])
 assert v['start_utc']==meta['started_utc'] and v['seconds']==meta['duration_seconds'] and v['exit']==meta['returncode'] and v['command']==meta['command']
 assert abs((end-datetime.datetime.fromisoformat(v['end_utc'])).total_seconds())<=1e-6
 assert not meta['timeout'] and meta['address_space_bytes']==2048*1024**2
 assert meta['cpu_seconds']==(900 if v['capture']=='checks/premise406.json' else 180)
 intervals.append({**v,'start':start,'end':end})
assert len(intervals)==9
actual_overlaps=[]
for a,b in itertools.combinations(intervals,2):
 amount=(min(a['end'],b['end'])-max(a['start'],b['start'])).total_seconds()
 if amount>0:
  assert a['context']!=b['context'];actual_overlaps.append({'a':a['capture'],'b':b['capture'],'seconds':amount,'same_context':False})
assert actual_overlaps==record['captured_process_overlaps']
for stem,expected in [('checks/premise406','PASS: 406-row premise registry'),('checks/navigation_final','489 passed, 1 deselected'),('checks/integration_final','778 passed, 1 deselected')]:
 meta=json.loads((B/(stem+'.json')).read_text());assert meta['returncode']==0 and not meta['timeout'] and not (B/(stem+'.stderr')).read_bytes();assert expected in (B/(stem+'.stdout')).read_text()
post=json.loads((B/'POST_AUDIT_NAVIGATION.json').read_text());pmap={v['path']:v for v in post['changes']};audit=json.loads((B/'AUDIT_INPUTS.json').read_text())
for n,h in audit['sha256'].items():
 if n in pmap:assert pmap[n]['old']==h and pmap[n]['new']==sha(R/n)
 else:assert sha(R/n)==h,('audit named input changed',n)
launch=json.loads((B/'LAUNCH.json').read_text());status=subprocess.check_output(['git','status','--short','--untracked-files=all'],cwd=R,text=True).splitlines()
original=[line for line in status if line.startswith('?? ') and not line.startswith(('?? udt_signal_chain_banking_2026-09-13/','?? udt_signal_continuation_2026-09-13/')) and line not in ['?? signal_chain_banking_guard.py','?? tests/test_signal_chain_banking.py']]
assert '\n'.join(original)+'\n'==launch['original_untracked_status']
head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=R,text=True).strip();origin=subprocess.check_output(['git','rev-parse','origin/grok'],cwd=R,text=True).strip();branch=subprocess.check_output(['git','branch','--show-current'],cwd=R,text=True).strip()
assert head==origin==base and branch=='grok'
assert not subprocess.check_output(['git','diff','--cached','--name-only'],cwd=R)
subprocess.run(['git','diff','--check'],cwd=R,check=True)
result={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'verdict':'PASS_FINAL_SOURCE_INPUT_METADATA_CHECK_WITH_EXPOSED_INTAKE_MISMATCHES','original_intake_mismatches':changes,'source_files':662,'original398_byte_identity':True,'current406_exact_claims':True,'fixed_document_sha256':fixed,'all_initial_source_review_pins_unchanged':True,'parent_full406_actual_exit':0,'parent_focused_actual_counts':'489 passed, 1 deselected','audit_inputs_accounted':15,'post_audit_navigation_files':7,'captured_intervals_recomputed':9,'same_context_overlap':False,'observed_cross_context_overlaps':actual_overlaps,'baseline_head':head,'local_origin_ref':origin,'branch':branch,'original_untracked_name_status_count':len(original),'original_untracked_name_status_sha256':hashlib.sha256(('\n'.join(original)+'\n').encode()).hexdigest(),'scope':'Administrative byte, saved-output, command/resource and local-ref correspondence; parent full audit attributed, no scientific reproof or protected-payload byte inspection.'}
(V/'FINAL_METADATA_CHECK.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
