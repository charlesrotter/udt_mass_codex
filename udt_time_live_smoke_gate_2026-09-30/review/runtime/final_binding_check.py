"""Streaming byte audit of the exact final SMK1 integration map, no re-proof."""
from pathlib import Path
import hashlib, json, resource, subprocess, time

HERE = Path(__file__).resolve().parent
PKG = HERE.parents[1]
ROOT = PKG.parent
started = time.monotonic()
freeze_path = PKG / 'FINAL_INTEGRATION_FREEZE.json'
freeze = json.loads(freeze_path.read_text())
previous = json.loads((PKG / 'PREVIOUS_REVIEW_RECORD.json').read_text())
accepted = freeze['accepted_sha256']
assert len(accepted) == 1351 and len(previous['accepted_sha256']) == 643
changed = sorted(k for k,v in previous['accepted_sha256'].items() if accepted.get(k) != v)
assert changed == sorted(freeze['changed_prior_paths']) == ['AGENTS.md', 'HANDOFF.md', 'LIVE.md']
protected = ('udt_kernel_plane_global_curvature_holonomy_atlas_2026-08-02/',
             'udt_native_onshell_timelive_reset_owner_audit_2026-08-10/',
             'udt_pair_regime_flow_reciprocal_orchestra_amplification_2026-08-12/',
             'udt_sne_xmax_G88_am_radial_compatibility_atlas_2026-08-12/')
assert not any(p.startswith(protected) for p in accepted)
total_bytes = 0
for name, expected in accepted.items():
    h = hashlib.sha256()
    with (ROOT / name).open('rb') as f:
        while chunk := f.read(1024**2):
            total_bytes += len(chunk); h.update(chunk)
    assert h.hexdigest() == expected, name
tracked_delta = subprocess.check_output(['git', 'diff', '--name-only', 'HEAD'], cwd=ROOT, text=True).splitlines()
assert sorted(tracked_delta) == changed
out = {'status': 'FINAL_1351_BYTE_BINDINGS_PASS', 'checked_paths': len(accepted),
       'retained_prior_paths': len(previous['accepted_sha256']), 'changed_prior_paths': changed,
       'new_package_input_paths': len(accepted)-len(previous['accepted_sha256']),
       'bytes_hashed': total_bytes, 'tracked_delta': tracked_delta,
       'head': subprocess.check_output(['git','rev-parse','HEAD'], cwd=ROOT,text=True).strip(),
       'branch': subprocess.check_output(['git','branch','--show-current'], cwd=ROOT,text=True).strip(),
       'freeze_sha256': hashlib.sha256(freeze_path.read_bytes()).hexdigest(),
       'elapsed_seconds': time.monotonic()-started,
       'max_rss_kib': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
       'scope': 'Byte correspondence plus exact three-file operational delta review; retained historical science not re-proved'}
assert out['elapsed_seconds'] < 180 and out['max_rss_kib'] < 2*1024**2
(HERE/'FINAL_BINDING_CHECK_RESULT.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
