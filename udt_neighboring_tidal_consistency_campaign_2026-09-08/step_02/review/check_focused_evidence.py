"""Verify exact focused repairs and unchanged original scientific outputs."""
import json
from pathlib import Path

review=Path(__file__).resolve().parent
step=review.parent
def receipt(stem):
    result=json.loads((review/(stem+'.json')).read_text())
    assert result['timeout'] is False
    assert result['address_space_bytes']==536870912 and result['cpu_seconds']==60
    return result
baseline=json.loads((review/'focused_baseline.stdout').read_text())
original=json.loads((step/'development_corrected.stdout').read_text())
newguards=['declared_free_profiles_live_in_actual_family','future_normal_relative_fixed_frame_on_full_S_positive_domain']
assert receipt('focused_baseline')['returncode']==0
assert baseline['status']=='PASS' and len(baseline['checks'])==15
assert [g for g in baseline['checks'] if g not in newguards]==original['checks']
assert {k:v for k,v in baseline.items() if k!='checks'}=={k:v for k,v in original.items() if k!='checks'}
for ext in ['stdout','stderr']:
    assert (review/('focused_baseline.'+ext)).read_bytes()==(step/('development_repaired.'+ext)).read_bytes()

expected={
 'drop_bianchi':'timelike_nonzero_curvature_factor_impossible',
 'wrong_null_sign':'both_explicit_null_polarizations_satisfy_full_bianchi',
 'drop_mixed':'both_explicit_null_polarizations_satisfy_full_bianchi',
 'nonharmonic':'full_neighborhood_Ricci_flat_not_only_u_zero',
 'wrong_K_sign':'K_full_projected_sign_and_Hu_not_squared_constraint_only',
 'omit_Hu':'K_full_projected_sign_and_Hu_not_squared_constraint_only',
 'double_curvature':'all_1024_first_jet_components_match_normalized_null_factor',
 'freeze_profiles':newguards[0],
 'reverse_normal':newguards[1],
}
for name,guard in expected.items():
    stem='focused_'+name
    assert receipt(stem)['returncode']==1
    stream=(review/(stem+'.stdout')).read_text()
    if name in ['freeze_profiles','reverse_normal']:
        wrapper,probe,stream=stream.split('\n',2)
        wrapper=json.loads(wrapper);probe=json.loads(probe)
        oldstem='probe_freeze_profiles' if name=='freeze_profiles' else 'probe_reverse_normal'
        oldprobe=json.loads((review/(oldstem+'.stdout')).read_text().split('\n',1)[0])
        assert probe['replacements']==oldprobe['replacements']
        assert probe['source_sha256']=='5f1a71286b24590d83530fe1696f7a5809c7554cac18e48553703f509b3958eb'
        assert wrapper['replay_change_only']==["/'check_development.py'","/'check_development_repaired.py'"]
    result=json.loads(stream)
    assert result['status']=='FAIL' and result['failed_guard']==guard

print(json.dumps({'status':'PASS','repaired_guard_count':15,
 'original_scientific_output_fields':'EXACTLY_UNCHANGED',
 'original_13_guards':'UNCHANGED_ORDER',
 'baseline_stdout_and_stderr':'BYTE_IDENTICAL_TO_FROZEN_REPAIR',
 'actual_caught_corruptions':expected,
 'same_two_original_probe_rules':'AUTHENTICATED',
 'scope':'focused same-premise guard repair only; full initial direct review remains controlling'},indent=2),flush=True)
