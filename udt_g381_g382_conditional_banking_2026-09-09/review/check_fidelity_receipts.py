"""Authenticate executed fidelity probes and source-scoped author replays."""
import hashlib
import json
from pathlib import Path

review = Path(__file__).resolve().parent
package = review.parent
root = package.parent
campaign = root / 'udt_neighboring_tidal_consistency_campaign_2026-09-08'

expected = {
    'forget_dependency': 'G382 scope lacks REQUIRES_BANKED_G381_AND_G310_G312_OWNER_PROVISIONAL_ARENA_G358_CONVENTIONS',
    'drop_fullslots': 'G381 scope lacks FULL_FOUR_CURVATURE_SLOT_CONNECTION_CORRECTION_NOT_RAW_SLOPES',
    'erase_lost': 'G381 scope lacks LOST_AUTHOR_BUFFERED_INTERMEDIATES_NOT_RECOVERED',
    'widen_scalar': 'G382 scope lacks EVERY_CANONICAL_NULL_JET_ACTUAL_SMOOTH_LOCAL_RICCI_FLAT_REALIZATION_LAMBDA_ZERO_ONLY',
    'change_grade': 'G381 banking grade changed',
    'record_scalar_boundary_corrected': 'neighboring-tidal banking record lacks ALL-Lambda necessity and Lambda=0 realization',
    'source_byte': 'neighboring-tidal original evidence changed: udt_neighboring_tidal_consistency_campaign_2026-09-08/step_01/CANDIDATE_INITIAL.md',
    'prior_row': 'neighboring-tidal banking changed an existing scientific registry row',
}
for mode, error in expected.items():
    receipt = json.loads((review / ('probe_' + mode + '.json')).read_text())
    assert receipt['returncode'] == 1 and not receipt['timeout'], mode
    assert receipt['address_space_bytes'] == 536870912 and receipt['cpu_seconds'] == 60
    assert (review / ('probe_' + mode + '.stderr')).read_text().strip() == error, mode
failed = (review / 'probe_record_scalar_boundary.stderr').read_text()
assert 'LookupError: unknown encoding: locale' in failed
assert 'banking record lacks' not in failed
original_script = (review / 'check_integration_fidelity_initial.py').read_bytes()
assert hashlib.sha256(original_script).hexdigest() == 'c3d9b12df7f3c15d05839dc697a3fde55b208f6b6c7addb99d7d47b3b8004e2b'

replays = {}
for fresh, saved, count in [
    ('nt1_regression', 'step_01/author_repaired', 21),
    ('nt2_symbol_regression', 'step_02/symbol_corrected', 6),
    ('nt2_development_regression', 'step_02/development_repaired', 15),
]:
    receipt = json.loads((package / (fresh + '.json')).read_text())
    assert receipt['returncode'] == 0 and not receipt['timeout'], fresh
    assert receipt['address_space_bytes'] == 536870912 and receipt['cpu_seconds'] == 60
    for suffix in ['.stdout', '.stderr']:
        assert (package / (fresh + suffix)).read_bytes() == (campaign / (saved + suffix)).read_bytes()
    output = json.loads((package / (fresh + '.stdout')).read_text())
    assert len(output['checks']) == count
    replays[fresh] = {'checks': count, 'stdout_and_stderr': 'BYTE_IDENTICAL',
                      'duration_seconds': receipt['duration_seconds']}

print(json.dumps({'status': 'PASS', 'actual_selected_guards_rejected': expected,
                  'reviewer_locale_harness_failure': 'PRESERVED_AND_EXCLUDED_AS_GUARD_REJECTION',
                  'parent_same_code_replays': replays,
                  'classification': 'receipt/correspondence fidelity, not independent science'}, indent=2))
