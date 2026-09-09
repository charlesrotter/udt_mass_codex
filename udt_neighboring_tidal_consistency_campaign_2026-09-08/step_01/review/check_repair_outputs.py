"""Authenticate repair output equality and exact dispositions without wide output dumps."""
import json
from pathlib import Path
root=Path(__file__).resolve().parents[1]
review=Path(__file__).parent
original=json.loads((root/'author_final.stdout').read_text())
repaired=json.loads((root/'author_repaired.stdout').read_text())
assert (root/'author_repaired.stdout').read_bytes()==(review/'repaired_baseline_replay.stdout').read_bytes()
assert (root/'author_repaired.stderr').read_bytes()==(review/'repaired_baseline_replay.stderr').read_bytes()
for key in original:
    if key!='checks':assert original[key]==repaired[key],key
assert [x for x in repaired['checks'] if x in original['checks']]==original['checks']
assert len(repaired['checks'])==21
assert repaired['finite_frame_derivative_anchors']==6*6*6==216
assert repaired['finite_frame_nonzero_derivatives']==192
expected={
    'repaired_original_probe_scaled_action':'finite_frame_derivative_matches_slot_action',
    'repaired_original_probe_zero_kernel':'kernel_vectors_really_independent',
    'repaired_replay_omit_bianchi':'weyl_differential_rank_sixteen',
    'repaired_replay_wrong_cycle':'weyl_differential_rank_sixteen',
    'repaired_replay_omit_connection':'all_slot_connection_correction',
    'repaired_replay_drop_divergence':'explicit_six_divergences_ten_evolution_equivalent',
}
decoder=json.JSONDecoder()
failures=[]
for stem,guard in expected.items():
    receipt=json.loads((review/(stem+'.json')).read_text())
    contents=(review/(stem+'.stdout')).read_text()
    data,end=decoder.raw_decode(contents)
    if 'probe' in data:data,_=decoder.raw_decode(contents[end:].lstrip())
    assert receipt['returncode']==1 and not receipt['timeout']
    assert data['status']=='FAIL' and data['guard']==guard
    failures.append(dict(capture=stem,guard=guard,exit=receipt['returncode']))
print(json.dumps(dict(status='PASS_REPAIR_FOCUSED_CHECKS',
    original_scientific_output_fields_equal=True,baseline_stdout_and_stderr_byte_identical=True,
    old_guards=17,repaired_guards=21,finite_component_anchors=216,nonzero_derivatives=192,
    failures=failures),indent=2))
