"""Focused pointer-only packaging correspondence; no scientific re-verification."""
from pathlib import Path
import hashlib,json,sys
sys.path.insert(0,str(Path.cwd()))
import verify_current_scientific_premises as v
P=Path('udt_physical_connection_whiteboard_2026-09-30')
H=lambda b:hashlib.sha256(b).hexdigest()
old=json.loads((P/'PRE_REGISTRY_POINTER_INTEGRATION_FREEZE.json').read_text())
new=json.loads((P/'INTEGRATION_FREEZE.json').read_text())
a,b=old['accepted_sha256'],new['accepted_sha256']
assert len(a)==100 and len(b)==101
assert set(a)-set(b)==set()
assert set(b)-set(a)=={str(P/'PACKAGING_REPAIR.md')}
assert [p for p in a if a[p]!=b[p]]==['HANDOFF.md']
for p,h in b.items(): assert H(Path(p).read_bytes())==h,p
oldatt=json.loads((P/'review/math/FINAL_ATTESTATION.json').read_text())
assert oldatt['accepted_sha256']==a
assert oldatt['freeze_sha256']==H((P/'PRE_REGISTRY_POINTER_INTEGRATION_FREEZE.json').read_bytes())
assert oldatt['report_sha256']==H((P/'review/math/FINAL_REVIEW.md').read_bytes())
handoff=Path('HANDOFF.md').read_text()
inserted='Exact406 grades in CURRENT_SCIENTIFIC_PREMISES.tsv are unchanged;'
before='Exact406 grades are unchanged;'
assert handoff.count(inserted)==1
assert H(handoff.replace(inserted,before).encode())==a['HANDOFF.md']
missing=[p for p in v.PREMISE_REGISTRY_CONTROLS
         if 'CURRENT_SCIENTIFIC_PREMISES.tsv' not in Path(p).read_text()]
assert not missing,missing
failed=json.loads((P/'checks/premise_final.json').read_text())
assert failed['returncode']==1 and not failed['timeout']
assert (P/'checks/premise_final.stderr').read_text().strip()=='control lacks premise registry: HANDOFF.md'
print(json.dumps({'status':'PASS','accepted_count':101,
 'changed_old_files':['HANDOFF.md'],'added_files':[str(P/'PACKAGING_REPAIR.md')],
 'exact_handoff_change':{'old':before,'new':inserted},
 'pointer_controls':len(v.PREMISE_REGISTRY_CONTROLS),
 'failed_full_audit_seconds':failed['duration_seconds'],
 'current_freeze_sha256':H((P/'INTEGRATION_FREEZE.json').read_bytes()),
 'scope':'hash/pointer packaging only; full audit rerun remains pending'},indent=2))
