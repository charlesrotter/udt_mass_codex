"""Independently parse preserved false passes and corresponding repaired failures."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CAMPAIGN = ROOT / 'udt_neighboring_tidal_consistency_campaign_2026-09-08'
decoder = json.JSONDecoder()

def documents(path):
    remaining = path.read_text().strip()
    result = []
    while remaining:
        value, end = decoder.raw_decode(remaining)
        result.append(value)
        remaining = remaining[end:].lstrip()
    return result

def capture(step, stem, returncode, status, guard=None, count=None):
    directory = CAMPAIGN / step / 'review'
    receipt = json.loads((directory / (stem + '.json')).read_text())
    assert receipt['returncode'] == returncode and not receipt['timeout'], stem
    assert receipt['address_space_bytes'] == 512 * 1024**2, stem
    assert receipt['cpu_seconds'] == 60, stem
    stream = documents(directory / (stem + '.stdout'))
    result = stream[-1]
    assert result['status'] == status, (stem, result['status'])
    if guard:
        assert result.get('guard', result.get('failed_guard')) == guard, stem
    if count:
        assert len(result['checks']) == count, stem
    return {'step': step, 'stem': stem, 'returncode': returncode,
            'status': status, 'guard': guard, 'checks': count}

history = []
for stem in ['author_scaled_action_falsepass', 'author_zero_kernel_falsepass']:
    history.append(capture('step_01', stem, 0, 'PASS', count=17))
for stem in ['probe_freeze_profiles', 'probe_reverse_normal']:
    history.append(capture('step_02', stem, 0, 'PASS', count=13))

expected_nt1 = {
    'repaired_original_probe_scaled_action': 'finite_frame_derivative_matches_slot_action',
    'repaired_original_probe_zero_kernel': 'kernel_vectors_really_independent',
    'repaired_replay_omit_bianchi': 'weyl_differential_rank_sixteen',
    'repaired_replay_wrong_cycle': 'weyl_differential_rank_sixteen',
    'repaired_replay_omit_connection': 'all_slot_connection_correction',
    'repaired_replay_drop_divergence': 'explicit_six_divergences_ten_evolution_equivalent',
}
expected_nt2 = {
    'focused_drop_bianchi': 'timelike_nonzero_curvature_factor_impossible',
    'focused_wrong_null_sign': 'both_explicit_null_polarizations_satisfy_full_bianchi',
    'focused_drop_mixed': 'both_explicit_null_polarizations_satisfy_full_bianchi',
    'focused_nonharmonic': 'full_neighborhood_Ricci_flat_not_only_u_zero',
    'focused_wrong_K_sign': 'K_full_projected_sign_and_Hu_not_squared_constraint_only',
    'focused_omit_Hu': 'K_full_projected_sign_and_Hu_not_squared_constraint_only',
    'focused_double_curvature': 'all_1024_first_jet_components_match_normalized_null_factor',
    'focused_freeze_profiles': 'declared_free_profiles_live_in_actual_family',
    'focused_reverse_normal': 'future_normal_relative_fixed_frame_on_full_S_positive_domain',
}
for step, expected in [('step_01', expected_nt1), ('step_02', expected_nt2)]:
    for stem, guard in expected.items():
        history.append(capture(step, stem, 1, 'FAIL', guard=guard))

history.append(capture('step_01', 'repaired_baseline_replay', 0, 'PASS', count=21))
history.append(capture('step_02', 'focused_baseline', 0, 'PASS', count=15))
original = json.loads((CAMPAIGN / 'step_01/author_final.stdout').read_text())
repaired = json.loads((CAMPAIGN / 'step_01/author_repaired.stdout').read_text())
assert all(repaired[k] == v for k, v in original.items() if k != 'checks')
original2 = json.loads((CAMPAIGN / 'step_02/development_corrected.stdout').read_text())
repaired2 = json.loads((CAMPAIGN / 'step_02/development_repaired.stdout').read_text())
assert {k: v for k, v in original2.items() if k != 'checks'} == {k: v for k, v in repaired2.items() if k != 'checks'}

lost = json.loads((CAMPAIGN / 'step_01/author_initial.json').read_text())
assert lost['returncode'] == -9 and not lost['timeout']
assert (CAMPAIGN / 'step_01/author_initial.stdout').read_bytes() == b''
assert (CAMPAIGN / 'step_02/development_initial.stdout').read_bytes() == b''
assert not (CAMPAIGN / 'step_01/review/source_first_check_initial.py').exists()

print(json.dumps({'status': 'PASS', 'evidence_type': 'independent receipt/artifact parsing; no new science',
                  'original_false_passes': 4, 'repaired_rejections': 15,
                  'original_scientific_fields_unchanged': True,
                  'NT1_lost_buffered_intermediates': 'NOT_RECOVERED',
                  'NT1_initial_reviewer_code': 'NOT_SEPARATELY_SNAPSHOTTED',
                  'captures': history}, indent=2))
