"""Bounded byte/receipt correspondence only; no scientific suite or source edits."""
import csv
import hashlib
import json
from pathlib import Path
import sys
sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parents[3]
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT))
import verify_udt_development as guard
WORK=ROOT/guard.WORK
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
proposal=json.loads((WORK/'FINAL_PACKAGING_PROPOSAL.json').read_text())
accepted=proposal['accepted_sha256']
prior=json.loads((WORK/'G349_ORIENTATION_REPAIR_FREEZE.json').read_text())['accepted_sha256']
assert len(accepted)==22 and all(sha(ROOT/p)==h for p,h in accepted.items())
changed=sorted(p for p in accepted if accepted[p]!=prior[p])
assert changed==['HANDOFF.md','LIVE.md','UDT_RESEARCH_ROADMAP.md']
assert all((ROOT/p).read_bytes()==(ROOT/candidate).read_bytes() for p,candidate in proposal['proposed_files'].items())
receipt=json.loads((WORK/'checks/premise_after_repair.json').read_text())
assert receipt['command']==['python3','verify_current_scientific_premises.py']
assert receipt['returncode']==0 and receipt['timeout'] is False
assert not (WORK/'checks/premise_after_repair.stderr').read_bytes()
assert 'PASS: 406-row premise registry' in (WORK/'checks/premise_after_repair.stdout').read_text()
applied=json.loads((WORK/'PACKAGING_APPLIED.json').read_text())
assert applied['full_audit']==receipt
assert applied['full_audit_stdout_sha256']==sha(WORK/'checks/premise_after_repair.stdout')
assert all(sha(ROOT/p)==h for p,h in applied['applied_file_sha256'].items())
failed=json.loads((WORK/'checks/premise_after.json').read_text())
assert failed['returncode']==1 and 'geometric_not_physical_union_scope' in (WORK/'checks/premise_after.stderr').read_text()
oldpins=json.loads((HERE/'G349_REPAIR_PINS.json').read_text())['sha256']
for path,h in oldpins.items():
    assert sha(ROOT/path)==h, 'changed earlier source/review/evidence: '+path
preserved={
'FINAL_REVIEW.md':'4cea28a48cbc2169b89f8363db69dba9e5aee56004e50f2ad8c720ce54bdbb9d',
'FINAL_ATTESTATION.json':'dd7a185aa18f0b657ab8488061297ab3f4ff4ae3863ba6abc5c146bea5d68e04',
'G349_REPAIR_REVIEW.md':'59b3eb3c3f59f9650a9223db3b91e07316f9b0366c366f878ae47ff03aef9c63',
'G349_REPAIR_ATTESTATION.json':'4925d9ad7296e988408eba647fa924f2595929f72a0a6c61e31a98339dcba7fe'}
assert all(sha(HERE/p)==h for p,h in preserved.items())
master=(ROOT/'UDT_DEVELOPMENT.md').read_text()
assert (ROOT/'CURRENT_RESEARCH_PROGRAM.md').read_text()==guard.program_text(master)
assert master.count('<a id="r18"></a>')==1
rows=list(csv.DictReader((WORK/'RECENT_DISPOSITIONS.tsv').open(),delimiter='\t'))
assert len(rows)==25 and {'OFS1','MGC1'} <= {r['id'] for r in rows}
roadmap=(ROOT/'UDT_RESEARCH_ROADMAP.md').read_text()
assert '(UDT_DEVELOPMENT.md#r18)' in roadmap and 'CURRENT_RESEARCH_PROGRAM.md#trajectory-of-the-recent-work' not in roadmap
stages=list(csv.DictReader((WORK/'STAGES.tsv').open(),delimiter='\t'))
assert len(stages)==9 and all(r['status']=='COMPLETE_WITH_DECLARED_SCOPE' for r in stages)
coherence=guard.validate(draft=True)
assert coherence['status']=='DRAFT_COHERENCE_ONLY'
out={'status':'PASS_PACKAGING_CORRESPONDENCE','accepted_files':22,'changed_from_G349_acceptance':changed,
     'actual_full_audit':receipt,'first_failed_audit_preserved':True,'earlier_attestations_preserved':True,
     'repaired_links_valid':True,'all_nine_stages_explicitly_scoped':True,
     'final_draft_coherence':coherence,'scope':'Receipt and byte correspondence only; strict final review rebinding, final fast checks and publication are parent follow-through.'}
(HERE/'packaging_check_result.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
