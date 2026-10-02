from pathlib import Path
import json,hashlib,datetime
B=Path('udt_response_clock_discriminator_2026-10-01');W=Path('development_reconstruction_2026-09-29');h=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
freeze=json.loads((B/'INTEGRATION_FREEZE.json').read_text());reviewers=[]
for name in ['math','fidelity']:
 p=B/name/'FINAL_ATTESTATION.json';a=json.loads(p.read_text())
 assert a['verdict']=='ACCEPT_WITH_LIMITS',name
 assert a['context']=={'math':'/root/erc_math','fidelity':'/root/connection_prior'}[name]
 assert a['accepted_sha256']==freeze['accepted_sha256']
 assert h(a['report_path'])==a['report_sha256']
 reviewers.append({'context':a['context'],'attestation':str(p),'sha256':h(p)})
for p,d in freeze['accepted_sha256'].items():assert h(p)==d,p
record={'status':'REVIEWED_WITH_LIMITS','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'scope':freeze['scope'],'independence':'Two reused separate contexts with prior exposure; fresh allocation failed and fresh-context review is UNAVAILABLE/NOT PASSED. Source-first new-question derivations preceded exposed actual-candidate and final correspondence reviews. Shared inherited model/SymPy, independent code and saved-series implementations; parent received source-first formulas and raised scope concern before direct reviews. One controlling scope repair, no equation change or physical adoption. Reports preserve actual exposure, omissions and packaging diagnostics.','freeze':str(B/'INTEGRATION_FREEZE.json'),'freeze_sha256':h(B/'INTEGRATION_FREEZE.json'),'prior_review_record':str(B/'PRIOR_REVIEW_RECORD.json'),'prior_review_record_sha256':h(B/'PRIOR_REVIEW_RECORD.json'),'reviewers':reviewers,'accepted_sha256':freeze['accepted_sha256']}
(W/'REVIEW_RECORD.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps({'status':record['status'],'frozen_files':len(freeze['accepted_sha256']),'reviewers':reviewers,'review_record_sha256':h(W/'REVIEW_RECORD.json')},indent=2))
