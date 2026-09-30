"""Frozen-byte and old-scope validation for the final bounded fidelity review."""
import hashlib
import json
import subprocess
from pathlib import Path

root=Path.cwd()
p=root/'udt_curved_clock_response_test_2026-09-30'
freeze_path=p/'INTEGRATION_FREEZE.json'
raw=freeze_path.read_bytes()
wanted='b6ad3eda8873cf46f69b42d04b3963e8a326a2cdfd1d501914fb67ac4bfce4af'
assert hashlib.sha256(raw).hexdigest()==wanted
freeze=json.loads(raw)
accepted=freeze['accepted_sha256']
assert len(accepted)==191
bad=[]
for path,h in accepted.items():
    assert not Path(path).is_absolute() and '..' not in Path(path).parts
    assert not path.startswith(('udt_native_onshell_timelive_reset_owner_audit_2026-08-10/',
        'udt_pair_regime_flow_reciprocal_orchestra_amplification_2026-08-12/',
        'udt_sne_xmax_G88_am_radial_compatibility_atlas_2026-08-12/',
        'udt_kernel_plane_global_curvature_holonomy_atlas_2026-08-02/'))
    actual=hashlib.sha256((root/path).read_bytes()).hexdigest()
    if actual!=h:bad.append(path)
assert not bad,bad
prior=json.loads((p/'PREVIOUS_REVIEW_RECORD.json').read_text())['accepted_sha256']
assert len(prior)==128 and set(prior)<=set(accepted)
changed=sorted(path for path,h in prior.items() if accepted[path]!=h)
assert changed==sorted(freeze['changed_previous_paths']) and len(changed)==8
actual_diff=subprocess.check_output(['git','-c','core.preloadIndex=false','diff','--name-only'],text=True).splitlines()
assert sorted(actual_diff)==changed,(actual_diff,changed)
head=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()
branch=subprocess.check_output(['git','branch','--show-current'],text=True).strip()
assert head==freeze['parent_head'] and branch=='grok'
print(json.dumps({'status':'PASS','freeze_sha256':wanted,'frozen_paths_verified':len(accepted),
 'prior_paths_retained':len(prior),'unchanged_prior_paths':len(prior)-len(changed),
 'changed_prior_paths':changed,'new_bound_paths':len(accepted)-len(prior),
 'branch':branch,'head':head,'scope':'Actual byte correspondence and bounded prior-scope retention; no full-corpus scientific reproof.'},indent=2))
