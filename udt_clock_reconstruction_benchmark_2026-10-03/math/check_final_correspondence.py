"""Final CBR1 frozen-map correspondence; no scientific promotion by hashes."""
import csv,hashlib,json,subprocess
from pathlib import Path
B=Path('udt_clock_reconstruction_benchmark_2026-10-03');root=Path.cwd().resolve()
freeze=B/'INTEGRATION_FREEZE.json';raw=freeze.read_bytes()
assert hashlib.sha256(raw).hexdigest()=='ed43ff1a1d4f73b2e07c73079e57d4638900e6fed303bbd010d206f365b0be28'
f=json.loads(raw);m=f['accepted_sha256'];assert len(m)==13024
blocked=('udt_native_onshell_timelive_reset_owner_audit_2026-08-10/',
 'udt_pair_regime_flow_reciprocal_orchestra_amplification_2026-08-12/',
 'udt_sne_xmax_G88_am_radial_compatibility_atlas_2026-08-12/',
 'udt_kernel_plane_global_curvature_holonomy_atlas_2026-08-02/')
for name,digest in m.items():
 assert not name.startswith(blocked),name
 p=Path(name);real=str(p.resolve().relative_to(root));assert not real.startswith(blocked),name
 assert hashlib.sha256(p.read_bytes()).hexdigest()==digest,name
prior=json.loads((B/'PRIOR_REVIEW_RECORD.json').read_text())['accepted_sha256']
changed=[p for p,d in prior.items() if m[p]!=d]
assert set(changed)==set(f['changed_inherited']) and len(changed)==6
assert len(prior)==12892
assert subprocess.check_output(['git','branch','--show-current']).decode().strip()=='grok'
assert subprocess.check_output(['git','rev-parse','HEAD']).decode().strip()==f['base_head']
assert set(subprocess.check_output(['git','diff','--name-only']).decode().splitlines())==set(changed)

central=Path('UDT_DEVELOPMENT.md').read_text();program=Path('CURRENT_RESEARCH_PROGRAM.md').read_text()
orientation=central.split('<!-- DEVELOPMENT_ORIENTATION_BEGIN -->',1)[1].split('<!-- DEVELOPMENT_ORIENTATION_END -->',1)[0].strip()
generated=program.split('<!-- GENERATED_DEVELOPMENT_BEGIN -->',1)[1].split('<!-- GENERATED_DEVELOPMENT_END -->',1)[0].strip()
assert orientation==generated
g=json.loads(Path('development_reconstruction_2026-09-29/DEVELOPMENT_GRAPH.json').read_text())
for name,digest in g['sources_sha256'].items():
 if name.startswith(str(B)+'/'):assert m[name]==digest
for row in g['review_support']:
 if row['path'].startswith(str(B)+'/'):assert m[row['path']]==row['sha256'] and row['role']=='review_evidence'
rows=list(csv.DictReader(Path('development_reconstruction_2026-09-29/RECENT_DISPOSITIONS.tsv').open(),delimiter='\t'))
assert len(rows)==50
r=next(r for r in rows if r['id']=='CBR1_RETURN');assert m[r['source']]==r['source_sha256']
for name in ['draft','normal_before_binding']:
 receipt=json.loads((B/f'checks/{name}.json').read_text())
 for ext in ['stdout','stderr']:
  p=B/f'checks/{name}.{ext}';assert hashlib.sha256(p.read_bytes()).hexdigest()==receipt[ext+'_sha256']
 assert receipt['returncode']==(0 if name=='draft' else 1)
assert 'REVIEW_REQUIRED' in (B/'checks/normal_before_binding.stdout').read_text()
out=dict(status='PASS frozen final correspondence and scoped integration checks',
 freeze_sha256=hashlib.sha256(raw).hexdigest(),accepted_paths=len(m),inherited_paths=len(prior),
 new_paths=len(set(m)-set(prior)),changed_inherited=changed,protected_payloads_hashed=0,
 generated_program_exact=True,graph_and_disposition_bindings=True,
 expected_draft_pass_and_normal_review_required=True,
 limits='Correspondence only for inherited entries; no full-corpus scientific reproof. Final bound normal/maintenance/full406 and banking receipts remain parent closure gates.')
with (B/'math/FINAL_CORRESPONDENCE.json').open('x') as z:json.dump(out,z,indent=2);z.write('\n')
print(json.dumps(out))
