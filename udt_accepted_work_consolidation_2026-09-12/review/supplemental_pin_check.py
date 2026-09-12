#!/usr/bin/env python3
"""Supplemental documentary correspondence; no scientific replay."""
import csv
from datetime import datetime, timezone
import hashlib
import io
import json
from pathlib import Path
import subprocess

ROOT=Path(__file__).resolve().parents[2]
OUT=Path(__file__).resolve().parent
BASE='ab6033469c37f63a0f3aa6527804b7e3cd2f5be6'
paths=[]
def add(p,depth='full source argument prose; implementations not rerun'):
    paths.append((p,depth))

dirs={
315:'udt_g315_conditional_cauchy_characteristic_data_interface_2026-09-01',
316:'udt_g316_lawful_constraint_data_construction_2026-09-01',
317:'udt_g317_exact_noncmc_coupled_data_family_2026-09-01',
318:'udt_g318_nonconstant_psi_noncmc_branch_classification_2026-09-01',
319:'udt_g319_ratio_free_noncmc_constraint_descent_2026-09-01',
320:'udt_g320_g319_physical_initial_geometry_quotient_audit_2026-09-01',
321:'udt_g321_g320_local_cauchy_development_uniqueness_2026-09-01',
322:'udt_g322_g321_maximal_globally_hyperbolic_development_2026-09-01',
323:'udt_g323_g320_unmarked_taub_quotient_classification_2026-09-01',
324:'udt_g324_g323_taub_quotient_mghd_identification_2026-09-02'}
for n,p in dirs.items():
    add(p+'/AUDIT_REPORT.md','full controlling audit; G315--G320 full original derivations not reopened')
    if n>=321: add(p+'/EXACT_DERIVATION.md')
for n,names in {
321:['EXTERNAL_REPAIR_FOLLOWUP_RESPONSE.md'],
322:['THEOREM_INTERFACE.tsv','REPAIR_LEDGER.tsv','EXTERNAL_REPAIR_FOLLOWUP_RESPONSE.md'],
324:['REPAIR_LEDGER.tsv','EXTERNAL_REPAIR_FOLLOWUP_RESPONSE.md','EXTERNAL_REPAIR_FOLLOWUP_FINAL_RESPONSE.md']}.items():
    for name in names: add(dirs[n]+'/'+name,'full theorem interface/repair response; external PDFs not reauthenticated')
add('udt_g178_completed_pair_kernel_fresh_adversarial_review_2026-08-19/AUDIT_REPORT.md','full controlling certification audit; original external payloads not reopened')
add('udt_g372_g373_conditional_banking_2026-09-08/BANKING_RECORD.md','full current acceptance overlay')
for s in ('step_01','step_02'):
    p='udt_optional_coupled_development_campaign_2026-09-08/'+s
    for name in ('CANDIDATE_INITIAL.md','REVIEWED_RESULT.md','review/ADVERSARIAL_REVIEW_INITIAL.md'): add(p+'/'+name)
for s in ('step_01','step_02'):
    p='udt_nonlinear_mode_realizability_campaign_2026-09-09/'+s
    add(p+'/INITIAL_CANDIDATE.md')
    add(p+'/review/ADVERSARIAL_REVIEW.md','full controlling review; NR1 truncated subsection subsequently reread')
for s in ('step_01','step_02'):
    p='udt_localized_geometry_campaign_2026-09-09/'+s
    add(p+'/CANDIDATE.md');add(p+'/review/DIRECT_REVIEW.md')
add('udt_localized_geometry_campaign_2026-09-09/step_02/REPAIR.md')
for p in ('udt_localized_evolution_followup_2026-09-09','udt_spatial_curvature_evolution_2026-09-09'):
    add(p+'/CANDIDATE.md');add(p+'/review/DIRECT_REVIEW.md')
for n in ('PROVENANCE_CORRECTION.md','review/PROVENANCE_FOLLOWUP.md'):
    add('udt_spatial_curvature_evolution_2026-09-09/'+n)
for n in ('INITIAL_CANDIDATE.md','REVIEWED_RESULT.md','review/DIRECT_REVIEW.md'):
    add('udt_nonlinear_ripple_geometry_2026-09-09/'+n)
add('udt_reviewed_backlog_banking_2026-09-10/BANKED_CLAIMS.json','targeted NR1/NR2/LG1/LG2/LE1/SE1/NE1 complete source_assessment fields; not all claims')

records=[]
for p,depth in paths:
    raw=(ROOT/p).read_bytes()
    assert raw==subprocess.check_output(['git','show',BASE+':'+p],cwd=ROOT),p
    records.append({'path':p,'sha256':hashlib.sha256(raw).hexdigest(),'read_depth':depth})
known={r['path']:r['sha256'] for r in records}
accepted=[]
def walk(x):
    if isinstance(x,dict):
        if x.get('path') in known and 'sha256' in x:
            assert known[x['path']]==x['sha256'],x['path']
            accepted.append(x['path'])
        for v in x.values(): walk(v)
    elif isinstance(x,list):
        for v in x: walk(v)
claims=json.loads((ROOT/'udt_reviewed_backlog_banking_2026-09-10/BANKED_CLAIMS.json').read_text())['claims']
for c in claims:
    if c['id'] in ('NR1','NR2','LG1','LG2','LE1','SE1','NE1'): walk(c['source_assessment'])
bank=(ROOT/'udt_g372_g373_conditional_banking_2026-09-08/BANKING_RECORD.md').read_text()
for p,h in known.items():
    if p.startswith('udt_optional_coupled_development_campaign_2026-09-08/'):
        assert h in bank,p
        accepted.append(p)

registry=(ROOT/'CURRENT_SCIENTIFIC_PREMISES.tsv').read_bytes()
assert registry==subprocess.check_output(['git','show',BASE+':CURRENT_SCIENTIFIC_PREMISES.tsv'],cwd=ROOT)
rows=list(csv.DictReader(io.StringIO(registry.decode()),delimiter='\t'))
ids={'G178','G372','G373'}|{'G'+str(n) for n in range(315,325)}|{'G'+str(n) for n in range(388,395)}
selected=[r for r in rows if r['premise_id'] in ids]
assert len(rows)==397 and len(selected)==len(ids)
seal=json.loads((OUT/'SOURCE_FIRST_SEAL.json').read_text())
for entry in seal['files']:
    assert hashlib.sha256((ROOT/entry['path']).read_bytes()).hexdigest()==entry['sha256'],entry['path']
receipt={'utc':datetime.now(timezone.utc).isoformat(),'kind':'metadata correspondence only',
 'source_files':records,'acceptance_pin_matches':sorted(set(accepted)),
 'actual_head':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
 'baseline':BASE,'registry_count_metadata':len(rows),'selected_rows':selected,
 'registry_sha256':hashlib.sha256(registry).hexdigest(),'initial_seal_files_unchanged':len(seal['files']),
 'parent_candidate_exposure':'NONE','scientific_replays':0}
with (OUT/'SUPPLEMENTAL_SOURCE_PINS.json').open('x') as f:
    json.dump(receipt,f,indent=2);f.write('\n')
with (OUT/'SUPPLEMENTAL_READ_DEPTH.tsv').open('x') as f:
    w=csv.DictWriter(f,fieldnames=['path','sha256','read_depth'],delimiter='\t');w.writeheader();w.writerows(records)
print(json.dumps({'correspondence':'PASS','sources':len(records),
 'acceptance_matches':len(set(accepted)),'selected_registry_rows':len(selected),
 'initial_seal_files_unchanged':len(seal['files']),'scientific_replays':0}))
