"""Authenticate actual direct-review baselines, failures and false passes."""
import json
from pathlib import Path
import sympy as s

folder=Path(__file__).resolve().parent
step=folder.parent
def read(stem,suffix='stdout'):
    return (folder/(stem+'.'+suffix)).read_text()
def receipt(stem):
    obj=json.loads(read(stem,'json'))
    assert obj['timeout'] is False
    assert obj['address_space_bytes']==536870912 and obj['cpu_seconds']==60
    return obj

for name,original,count in [('symbol','symbol_corrected',6),('development','development_corrected',13)]:
    stem='replay_'+name+'_baseline'
    assert receipt(stem)['returncode']==0
    assert read(stem)==(step/(original+'.stdout')).read_text()
    assert read(stem,'stderr')==(step/(original+'.stderr')).read_text()
    assert len(json.loads(read(stem))['checks'])==count

expected={
 'drop_bianchi':'timelike_nonzero_curvature_factor_impossible',
 'wrong_null_sign':'both_explicit_null_polarizations_satisfy_full_bianchi',
 'drop_mixed':'both_explicit_null_polarizations_satisfy_full_bianchi',
 'nonharmonic':'full_neighborhood_Ricci_flat_not_only_u_zero',
 'wrong_K_sign':'K_full_projected_sign_and_Hu_not_squared_constraint_only',
 'omit_Hu':'K_full_projected_sign_and_Hu_not_squared_constraint_only',
 'double_curvature':'all_1024_first_jet_components_match_normalized_null_factor',
}
for name,guard in expected.items():
    stem='replay_'+name
    assert receipt(stem)['returncode']==1
    result=json.loads(read(stem))
    assert result['status']=='FAIL' and result['failed_guard']==guard

falsepasses={}
for stem in ['probe_freeze_profiles','probe_reverse_normal']:
    assert receipt(stem)['returncode']==0
    first,rest=read(stem).split('\n',1)
    metadata=json.loads(first); result=json.loads(rest)
    assert result['status']=='PASS' and len(result['checks'])==13
    falsepasses[stem]={'probe':metadata['probe'],'passed_guards':13,'source_sha256':metadata['source_sha256'],'modified_sha256':metadata['modified_sha256']}
    if stem=='probe_freeze_profiles':
        assert 'A(u)' not in result['metric'] and 'F(u)' not in result['metric']
        assert 'arbitrary smooth' in result['free_profiles']
    else:
        loc={'A':s.Function('A'),'F':s.Function('F')}
        baseline=json.loads(read('replay_development_baseline'))
        diff=s.sympify(result['K'],locals=loc)+s.sympify(baseline['K'],locals=loc)
        assert all(s.simplify(t)==0 for t in diff)

print(json.dumps({'baseline_byte_replays':'PASS, stdout and stderr',
 'seven_actual_mutants':expected,'two_actual_false_passes':falsepasses,
 'guard_repair_required':'declared free-profile liveness and whole-domain future-normal anchor',
 'scope':'original analytic candidate and independent baseline computations survive; no final repaired verdict yet'},indent=2),flush=True)
