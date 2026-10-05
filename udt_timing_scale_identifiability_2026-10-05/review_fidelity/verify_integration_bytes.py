"""Bounded final byte correspondence check; no scientific re-proof."""
import hashlib,json,subprocess
from pathlib import Path
root=Path.cwd()
base=Path('udt_timing_scale_identifiability_2026-10-05')
freeze_path=base/'INTEGRATION_FREEZE.json'
freeze=json.loads(freeze_path.read_text())
expected_freeze='32328dad8868ebc2726ae3df0745f87b4f94c9d5bd21e700c063d960edfb21f6'
assert hashlib.sha256(freeze_path.read_bytes()).hexdigest()==expected_freeze
protected=[
 'udt_kernel_plane_global_curvature_holonomy_atlas_2026-08-02/',
 'udt_native_onshell_timelive_reset_owner_audit_2026-08-10/',
 'udt_pair_regime_flow_reciprocal_orchestra_amplification_2026-08-12/',
 'udt_sne_xmax_G88_am_radial_compatibility_atlas_2026-08-12/']
accepted=freeze['accepted_sha256']
assert len(accepted)==14446
assert not any(p.startswith(tuple(protected)) for p in accepted)
errors=[];byte_count=0
for name,expected in accepted.items():
 p=Path(name)
 assert not p.is_absolute() and '..' not in p.parts
 assert p.resolve().is_relative_to(root.resolve())
 h=hashlib.sha256()
 with p.open('rb') as stream:
  for chunk in iter(lambda:stream.read(1024*1024),b''):
   h.update(chunk);byte_count+=len(chunk)
 if h.hexdigest()!=expected:errors.append(name)
assert not errors,errors
changed=subprocess.check_output(['git','diff','--name-only'],text=True).splitlines()
assert set(changed)==set(freeze['changed_inherited']),(changed,freeze['changed_inherited'])
central=Path('UDT_DEVELOPMENT.md').read_text()
program=Path('CURRENT_RESEARCH_PROGRAM.md').read_text()
orientation=central.split('<!-- DEVELOPMENT_ORIENTATION_BEGIN -->')[1].split('<!-- DEVELOPMENT_ORIENTATION_END -->')[0]
generated=program.split('<!-- GENERATED_DEVELOPMENT_BEGIN -->')[1].split('<!-- GENERATED_DEVELOPMENT_END -->')[0]
assert orientation==generated
assert 'negative logarithmic\nfrequency drift, -dlog nu_o/dt_o, is dlog Z/dt_o-dlog nu_e/dt_o.' in central
assert (base/'initial_text/CENTRAL_INSERT.md').read_bytes()==(base/'review_fidelity/CENTRAL_INSERT_BEFORE_DRIFT_WORDING.md').read_bytes()
assert subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()==freeze['base_head']
print(json.dumps(dict(status='PASS',integration_freeze_sha256=expected_freeze,
 accepted_count=len(accepted),byte_count=byte_count,protected_prefix_entries=0,
 changed_inherited=changed,generated_orientation='EXACT',negative_drift_label='CORRECTED',
 original_insert_preservation='BYTE_IDENTICAL',scope='Byte correspondence and specified packaging checks only; semantic review is separate.'),indent=2))
