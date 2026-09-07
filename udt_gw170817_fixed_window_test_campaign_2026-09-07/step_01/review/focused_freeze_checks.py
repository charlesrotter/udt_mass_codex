"""R1 source-preserving freeze verification and independent finite guard examples.

No strain samples; not a replay/catch-proof of the future FW2 implementation.
"""
import hashlib
import json
import math
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[1]
pins={
    'initial/CANDIDATE.md':'5cf764588c4b2abc627d89b7256837ad60975e61068bb93af8b83f0f4a139b08',
    'initial/FREEZE.json':'05a3fdfc8920e4255603696d0abc3a98fc388b09645647b8aee468a500cb8b7d',
    'CANDIDATE.md':'0a485434b9647ffa96dc76d5dd9bae921619d5ca6264e5025237ba6565c3ab76',
    'FREEZE.json':'fa0506eaea5ef20dcd92aabf3b2d1a0efc7fb75ef6c7272c00e5e6764c591324',
    'metadata_filtered_run.stdout':'9e6c1d6fa98e14e0b2c060e18d4e7b46aacc35890aff46c51474ca03ce1f74af',
}
for name,digest in pins.items():
    assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==digest,name
old=json.loads((ROOT/'initial/FREEZE.json').read_text())
new=json.loads((ROOT/'FREEZE.json').read_text())
added=set(new)-set(old)
assert added=={'rng','hrss_normalization','numeric_guard','PSD_validity'}
assert {k for k in old if old[k]!=new[k]}=={'version'}
assert new['event_unseal_authorized_by_this_freeze'] is False
assert new['phase_draws_per_family']==8 and len(new['injection_spectral_families_hz'])==3
seeds=[new['injection_seed_base']+1000*f+d for f in range(3) for d in range(8)]
assert len(set(seeds))==24
assert 'PCG64' in new['rng'] and 'real standard_normals first' in new['rng']
assert 'NumPy2.2.6' in new['rng'] and 'normalize' in new['hrss_normalization']
fs=new['fs_hz']; seconds=new['core_seconds']; target=new['effect_target']
N=fs*seconds
constant_sample=target/math.sqrt(seconds)
correct_hrss=math.sqrt(N*constant_sample**2/fs)
wrong_hrss=math.sqrt(N*constant_sample**2)
assert math.isclose(correct_hrss,target,rel_tol=1e-15)
assert math.isclose(wrong_hrss/target,64,rel_tol=1e-15)
wrong_normalization_caught=False
try:
    assert math.isclose(wrong_hrss,target,rel_tol=1e-10)
except AssertionError:
    wrong_normalization_caught=True
assert wrong_normalization_caught

def pre_floor_gate(values):
    assert all(math.isfinite(x) and x>0 for x in values)
    assert all(x>=1e-60 for x in values)

pre_floor_gate([1e-46,2e-46])
bad_cases=[[0.0],[-1e-46],[float('nan')],[float('inf')],[1e-62]]
catches=[]
for values in bad_cases:
    try:
        pre_floor_gate(values)
    except AssertionError:
        catches.append(True)
    else:
        catches.append(False)
assert all(catches)
# Actually reintroduce clipping-before-validity for the zero case: this falsely
# passes the defective positivity check, while the preceding correct guard fails.
clipped_false_pass=all(x>0 for x in [max(0.0,1e-60)])
assert clipped_false_pass
# A unit fractional residual at physical1e-22 passes a loose absolute tolerance;
# the stipulated dimensionless comparison rejects it without relying on units.
input_size=1e-22; broken_residual=1e-22
loose_absolute_false_pass=broken_residual<1e-10
scaled_relative=abs(1e21*broken_residual)/abs(1e21*input_size)
assert loose_absolute_false_pass and scaled_relative==1.0
relative_caught=False
try:
    assert scaled_relative<=new['numeric_relative_tolerance']
except AssertionError:
    relative_caught=True
assert relative_caught
print(json.dumps(dict(python=sys.version,pinned_sha256=pins,
    changed_initial_fields=['version'],added_controls=sorted(added),seeds=seeds,
    exact_effect_definition='sqrt(sum samples_squared/fs) before Hann',
    target_rms=constant_sample,correct_constant_hrss=correct_hrss,
    wrong_euclidean_hrss=wrong_hrss,missing_sample_duration_caught=wrong_normalization_caught,
    PSD_bad_cases_caught=catches,clipped_before_check_false_pass=clipped_false_pass,
    loose_absolute_false_pass=loose_absolute_false_pass,
    corrected_dimensionless_residual=scaled_relative,relative_guard_caught=relative_caught,
    positive90s_bins_inclusive_30_to_500=500*90-30*90+1,
    welch4s_segments_per90s=(90*4096-4*4096)//(2*4096)+1,
    threshold_crossings_needed_per_family=math.ceil(.9*21*8),
    scope='Finite independent method controls only; no FW2 implementation, strain or population power tested.'),indent=2,sort_keys=True))
