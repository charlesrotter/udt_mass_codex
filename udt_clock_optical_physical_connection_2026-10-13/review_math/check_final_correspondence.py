"""Final version correspondence, no scientific payload output or recomputation."""
import datetime
import hashlib
import json
from pathlib import Path

root = Path.cwd().resolve()
package = Path('udt_clock_optical_physical_connection_2026-10-13')
freeze_path = package/'INTEGRATION_FREEZE.json'
freeze_bytes = freeze_path.read_bytes()
freeze = json.loads(freeze_bytes)
accepted = freeze['accepted_sha256']
protected = (
    'udt_kernel_plane_global_curvature_holonomy_atlas_2026-08-02/',
    'udt_native_onshell_timelive_reset_owner_audit_2026-08-10/',
    'udt_pair_regime_flow_reciprocal_orchestra_amplification_2026-08-12/',
    'udt_sne_xmax_G88_am_radial_compatibility_atlas_2026-08-12/',
)
forbidden = []
for name in accepted:
    path = Path(name)
    if (path.is_absolute() or '..' in path.parts or name.startswith(protected)
            or path.is_symlink() or not path.resolve().is_relative_to(root)):
        forbidden.append(name)
if forbidden:
    raise RuntimeError({'rejected_names_before_any_accepted_content_read': forbidden})

def digest(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as handle:
        for block in iter(lambda: handle.read(1024*1024), b''):
            h.update(block)
    return h.hexdigest()

mismatches = []
byte_count = 0
for name, expected in accepted.items():
    path = Path(name)
    actual = digest(path)
    byte_count += path.stat().st_size
    if actual != expected:
        mismatches.append({'path': name, 'expected': expected, 'actual': actual})
candidate = json.loads((package/'CANDIDATE_FREEZE.json').read_text())['sha256']
candidate_mismatches = [name for name, expected in candidate.items() if digest(name) != expected]
prior = json.loads(Path(freeze['prior_review_record']).read_text())
prior_accepted = prior['accepted_sha256']
actual_changed = sorted(name for name, value in prior_accepted.items()
                        if accepted.get(name) != value)
actual_new = sorted(set(accepted)-set(prior_accepted))
assert actual_changed == sorted(freeze['changed_prior_files'])
assert actual_new == sorted(freeze['new_files'])
central = Path('UDT_DEVELOPMENT.md').read_text()
orientation = central.split('<!-- DEVELOPMENT_ORIENTATION_BEGIN -->', 1)[1].split('<!-- DEVELOPMENT_ORIENTATION_END -->', 1)[0].strip()
program = Path('CURRENT_RESEARCH_PROGRAM.md').read_text()
generated = program.split('<!-- GENERATED_DEVELOPMENT_BEGIN -->', 1)[1].split('<!-- GENERATED_DEVELOPMENT_END -->', 1)[0].strip()
assert orientation == generated
result = {
    'utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'freeze_sha256': hashlib.sha256(freeze_bytes).hexdigest(),
    'accepted_files_checked': len(accepted), 'bytes_hashed': byte_count,
    'protected_prefixes_rejected_before_hashing': list(protected),
    'protected_paths_present': len(forbidden),
    'accepted_map_mismatches': mismatches,
    'initial_candidate_files_checked': len(candidate),
    'initial_candidate_mismatches': candidate_mismatches,
    'changed_prior_count': len(actual_changed), 'new_count': len(actual_new),
    'generated_orientation_matches': True,
    'unchanged_prior_files_inherit_review_not_reproof': len(prior_accepted)-len(actual_changed),
    'status': 'PASS' if not mismatches and not candidate_mismatches else 'FAIL',
}
print(json.dumps(result, indent=2))
assert not mismatches and not candidate_mismatches
