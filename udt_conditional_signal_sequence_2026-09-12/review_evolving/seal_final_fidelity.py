#!/usr/bin/env python3
"""Document/receipt integrity seal only; no scientific computation or project import."""
from pathlib import Path
import json,hashlib,datetime,subprocess
repo=Path.cwd();pack=repo/'udt_conditional_signal_sequence_2026-09-12';review=pack/'review_evolving'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
intake=json.loads((pack/'FINAL_REVIEW_INTAKE.json').read_text())
amend=json.loads((pack/'FINAL_FIDELITY_AMENDMENT.json').read_text())
assert amend['original_intake_sha256']==sha(pack/'FINAL_REVIEW_INTAKE.json')
assert intake['files'][amend['changed_file']]==amend['original_sha256']
expected=dict(intake['files']);expected[amend['changed_file']]=amend['reviewed_replacement_sha256']
final_checks={p:{'expected':v,'actual':sha(repo/p),'pass':sha(repo/p)==v} for p,v in expected.items()}
nav={'LIVE.md','HANDOFF.md','CURRENT_RESEARCH_PROGRAM.md','INDEX.md','UDT_RESEARCH_ROADMAP.md'}
pins=json.loads((pack/'SOURCE_PINS.json').read_text())
source_checks={p:{'expected':v,'actual':sha(repo/p),'pass':sha(repo/p)==v} for p,v in pins.items() if p not in nav}
candidate_checks={}
for step in ['step_03','step_05']:
 f=json.loads((pack/step/'CANDIDATE_FREEZE.json').read_text());a=sha(pack/step/'INITIAL_CANDIDATE.md')
 candidate_checks[step]={'expected':f['sha256'],'actual':a,'pass':a==f['sha256']}
repair=json.loads((pack/'step_03/REPAIR_FREEZE.json').read_text())
repair_checks={p:sha(repo/p)==v for p,v in repair['files'].items()}
processes=json.loads((pack/'CHECK_RESULTS.json').read_text())['processes'];verified=[]
for r in processes:
 actual=json.loads((repo/r['receipt']).read_text())
 keys=['command','started_utc','duration_seconds','returncode','timeout','address_space_bytes','cpu_seconds','maxrss_kib']
 match=all(r[k]==actual[k] for k in keys)
 begin=datetime.datetime.fromisoformat(actual['started_utc']);end=begin+datetime.timedelta(seconds=actual['duration_seconds'])
 verified.append({'receipt':r['receipt'],'context':r['context'],'start':begin,'end':end,'metadata_match':match})
verified.sort(key=lambda r:r['start']);overlaps=[]
for i,a in enumerate(verified):
 for b in verified[i+1:]:
  if b['start']<a['end']:overlaps.append([a['receipt'],b['receipt']])
own=[r for r in processes if r['context']=='evolving'];own_total=sum(r['duration_seconds'] for r in own)
navreceipt=json.loads((pack/'checks/navigation_sealed.json').read_text());navtext=(pack/'checks/navigation_sealed.stdout').read_text()
navpass=navreceipt['returncode']==0 and '359 passed, 1 deselected' in navtext
summary=json.loads((pack/'CHECK_SUMMARY.json').read_text())
assert summary['max_scaled_errors']['original_endpoint']==5.522249324485529e-13
assert len(final_checks)==20 and all(c['pass'] for c in final_checks.values())
assert len(source_checks)==27 and all(c['pass'] for c in source_checks.values())
assert all(c['pass'] for c in candidate_checks.values()) and all(repair_checks.values())
assert len(verified)==24 and all(r['metadata_match'] for r in verified) and not overlaps and navpass
now=datetime.datetime.now(datetime.timezone.utc);start=datetime.datetime.fromisoformat('2026-09-13T00:08:20+00:00');deadline=start+datetime.timedelta(minutes=40)
assert now<deadline
record={'verdict':'VERIFIED-WITH-CAVEATS__REVIEWED_CONDITIONAL__UNPROMOTED','required_repairs_remaining':[],
 'context':'/root/css_evolving_review','source_base_HEAD':subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),
 'branch':subprocess.check_output(['git','branch','--show-current'],text=True).strip(),
 'conservative_allocation_start_utc':start.isoformat(),'first_observed_action_utc':'2026-09-13T00:09:12+00:00',
 'final_sealed_utc':now.isoformat(),'deadline_utc':deadline.isoformat(),'elapsed_seconds_from_conservative_start':(now-start).total_seconds(),
 'within40minutes':True,'runtime_model_version':'UNATTESTED','configured_parent_attribution':'gpt-6-astra/xhigh; attribution only',
 'fresh_context':True,'different_model_claimed':False,'distinct_implementation':'full affine8 Hamiltonian from original metric versus parent reduced6+Hessian; independent code before parent code/output exposure',
 'shared_dependencies':'same supplied source metric and scipy Bessel/FLOAT64 libraries; not independent physical premises',
 'source_first_notes_sha256':sha(review/'SOURCE_FIRST_NOTES.md'),'original_intake_sha256':sha(pack/'FINAL_REVIEW_INTAKE.json'),
 'amendment_sha256':sha(pack/'FINAL_FIDELITY_AMENDMENT.json'),'amendment':amend,
 'first_final_pin_attempt':'Stopped at original CLOSEOUT hash mismatch while authorized amendment arrived; no seal emitted. Tool transcript and FINAL_FIDELITY.md retain this documentary check history.',
 'intake_frozen_utc':intake['frozen_utc'],'final_intake_checks_with_amendment':final_checks,'source_pin_checks':source_checks,
 'original_candidate_checks':candidate_checks,'repaired_code_freeze_checks':repair_checks,
 'capture_count_this_context':len(own),'captured_subprocess_seconds_this_context':own_total,
 'maxrss_kib_this_context':max(r['maxrss_kib'] for r in own),'all_own_captures_within180s_2048MiB':all(r['duration_seconds']<180 and r['address_space_bytes']<=2048*1024**2 for r in own),
 'campaign24_receipt_metadata_matches':all(r['metadata_match'] for r in verified),'captured_process_overlaps':overlaps,
 'navigation_final_receipt_sha256':sha(pack/'checks/navigation_sealed.json'),'navigation_final_stdout_sha256':sha(pack/'checks/navigation_sealed.stdout'),
 'navigation359passed1deselected':navpass,'parent_full398':'Actual parent capture attributed/read; not independently rerun',
 'scope':'Substantive CSS3/5 proof/code/numerics and same-premise repair; combined final20-file documentary fidelity with exact CLOSEOUT amendment. CSS4 proof credited to actual separate routes review.',
 'omissions':['independent full398 and historical source campaigns','global path/caustic proof','interval or proof-assistant certification','physical light/EM/flux/initial-record acquisition','empirical data','different-model or human review','eventual git publication verification'],
 'no_protected_payload_read_or_hashed':True,'no_git_mutation':True,'writes_only':'udt_conditional_signal_sequence_2026-09-12/review_evolving/',
 'hash_limit':'Correspondence, not scientific truth, independent authorship or external chronology','seal_script_sha256':sha(Path(__file__)),
 'final_report_sha256':sha(review/'FINAL_FIDELITY.md')}
with (review/'FINAL_FIDELITY.json').open('x') as f:f.write(json.dumps(record,indent=2)+'\n')
manifest=[]
for p in sorted(review.iterdir()):
 if p.is_file() and p.name!='REVIEW_SHA256SUMS':manifest.append(sha(p)+'  '+p.name)
with (review/'REVIEW_SHA256SUMS').open('x') as f:f.write('\n'.join(manifest)+'\n')
print(json.dumps({'verdict':record['verdict'],'sealed_utc':record['final_sealed_utc'],'elapsed_seconds':record['elapsed_seconds_from_conservative_start'],'final20pins_with_amendment_pass':True,'source27pins_pass':True,'process24metadata_pass':True,'own_capture_seconds':own_total,'files_in_review_manifest':len(manifest)}))
