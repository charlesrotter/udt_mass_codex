import datetime
import hashlib
import json
from pathlib import Path

root=Path.cwd()
work=Path('udt_gr_commitment_audit_2026-09-29')
review=work/'review/fidelity'
def h(p):return hashlib.sha256((root/p).read_bytes()).hexdigest()
frozen=json.loads((root/work/'INTEGRATION_FREEZE.json').read_text())
accepted=frozen['accepted_sha256']
assert len(accepted)==52 and {p:h(p) for p in accepted}==accepted
for name in ['final_maintenance_01','final_draft_01','final_correspondence_01']:
    r=json.loads((root/review/(name+'.json')).read_text())
    assert r['returncode']==0 and r['timeout'] is False
source=json.loads((root/review/'SOURCE_FIRST_SEAL.json').read_text())
assert h(review/'SOURCE_FIRST.md')==source['review_payloads_sha256']['SOURCE_FIRST.md']
direct=json.loads((root/review/'DIRECT_REVIEW_PINS.json').read_text())
assert h(review/'DIRECT_REVIEW.md')==direct['own_payloads_sha256'][str(review/'DIRECT_REVIEW.md')]
report=str(review/'FINAL_REVIEW.md')
att={
 'context':'/root/gca_fidelity',
 'reviewer':'/root/gca_fidelity',
 'verdict':'ACCEPT_WITH_LIMITS',
 'date_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'report_path':report,
 'report_sha256':h(report),
 'accepted_sha256':accepted,
 'integration_freeze_sha256':h(work/'INTEGRATION_FREEZE.json'),
 'independence':{
   'context':'Fresh separate source-first context, then exposed direct and proportional integration review',
   'model':'Inherited model; exact runtime unavailable; different-model UNTESTED',
   'implementation':'Own original metric diagnostics before producer code; existing maintenance utilities reused',
   'library':'Shared Python/SymPy; different-library UNTESTED',
   'human_and_formal':'UNTESTED',
   'other_reviewer_exposure':'Scientific report content not read; graph metadata/parent attributed counts only'
 },
 'scope':'Exact frozen GCA1 integration; unchanged predecessor files accepted as correspondence, not scientific reproof',
 'remaining_parent_gates':['actual review binding','normal development validator','fresh normal full406','staged-byte and synchronization review','authorized banking'],
 'independent_final_receipts':{str(review/(name+'.json')):h(review/(name+'.json'))
   for name in ['final_maintenance_01','final_draft_01','final_correspondence_01']},
 'work_record_inspected_sha256':json.loads((root/review/'final_correspondence_01.stdout').read_text())['work_record_sha256_at_review'],
 'checksum_limits':'Byte correspondence only, not scientific truth or trusted chronology'
}
with (root/review/'FINAL_ATTESTATION.json').open('x') as f:
    json.dump(att,f,indent=2);f.write('\n')
print(json.dumps({'context':att['context'],'verdict':att['verdict'],
  'report_sha256':att['report_sha256'],
  'attestation_sha256':h(review/'FINAL_ATTESTATION.json'),
  'accepted_file_count':len(accepted),'source_first_and_direct_unchanged':True},indent=2))
