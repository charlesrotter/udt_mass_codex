"""Seal the completed same-R2 repair, retaining all intermediate evidence."""
import hashlib
import json
from pathlib import Path
import subprocess

R = Path(__file__).resolve().parent
P = R.parent
ROOT = P.parent
BASE = 'a9896cb190e9c4aa8fd8a317cfaaa942d64e0a19'

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def pins(name):
    return {p: h for h, p in [line.split(maxsplit=1)
            for line in (P / name).read_text().splitlines()]}

initial = pins('INITIAL_IMPLEMENTATION_SHA256SUMS')
final = pins('FINAL_IMPLEMENTATION_SHA256SUMS')
assert len(initial) == 12 and len(final) == 15
for path, expected in final.items():
    assert digest(ROOT / path) == expected, path
changed = [p for p, h in initial.items() if digest(ROOT / p) != h]
assert set(changed) == {'verify_current_scientific_premises.py', 'tests/test_startup_surface.py'}
assert digest(P / 'INITIAL_IMPLEMENTATION.patch') == \
    '2922c2094a152f36e186f1dd2e10afe7f4ee5c41c0c31217da136ba64980a618'
assert digest(P / 'REPAIRED_IMPLEMENTATION.patch') == \
    '9ac4e0858334e95e3f1d8da1706dd69a413a4fef5354bae37fef240026267fd9'
assert digest(R / 'INITIAL_DIRECT_REVIEW.md') == \
    '62911679ec20805b41326b40c7496949af5995deba3a4ba35af078e428a0570b'
assert digest(R / 'probe_guards.py') == \
    '01c00ab87bbe14ff7a355046401cdeff70d90e866b808dfac092e709d6186137'
initial_result = json.loads((R / 'guard_probes_initial.stdout').read_text())
final_result = json.loads((R / 'guard_probes_final.stdout').read_text())
assert initial_result['failures'] == 13 and final_result['failures'] == 0
assert initial_result['cases'] == final_result['cases'] == 71
assert initial_result['reviewer_source_sha256'] == final_result['reviewer_source_sha256']
assert final_result['guard_source_sha256'] == final['verify_current_scientific_premises.py']
assert final_result['fixture_source_sha256'] == final['tests/test_startup_surface.py']
assert sum(x['result'] == 'REJECTED_AS_REQUIRED' for x in final_result['results']) == 56
assert sum(x['result'] == 'PASS' for x in final_result['results']) == 15
old_supplement = json.loads((R / 'transition_snapshot_reconstructed_old.stdout').read_text())
new_supplement = json.loads((R / 'transition_snapshot_final.stdout').read_text())
assert old_supplement['chronology'] == 'POST_HOC_FIRST_REPAIR_RECONSTRUCTION_AND_EXECUTION'
assert old_supplement['probe']['false_passes'] == 3
assert new_supplement['false_passes'] == 0 and new_supplement['actual_transition_text_swaps'] == 0
assert all(x['result'] == 'REJECTED_AS_REQUIRED' for x in new_supplement['results'])
assert json.loads((R / 'transition_snapshot_first_repair.stdout').read_text())['false_passes'] == 0
full = json.loads((P / 'COMPLETED_REPAIR_FULL_PREMISE_AUDIT.json').read_text())
assert full['returncode'] == 1 and 'G325 dependency-free replay failed' in full['stderr']
assert 'replay_exact:DERIVATION_RESULT.json' in full['stderr']
assert full['stdout'] == ''
paths = sorted(p for p in initial if '/' not in p or p == 'tests/test_startup_surface.py')
diff = subprocess.run(['git', '-c', 'core.preloadIndex=false', '-c', 'index.threads=1',
    'diff', '--binary', BASE, '--', *paths], cwd=ROOT,
    capture_output=True, check=True, timeout=10).stdout
assert diff == (P / 'FINAL_IMPLEMENTATION.patch').read_bytes()
print(json.dumps({'status': 'PASS', 'final_pins': 15,
    'authority_registry_six_surfaces_unchanged_through_repairs': True,
    'initial_actual_false_passes_preserved': 13,
    'first_repair_additional_false_passes_posthoc_execution': 3,
    'final_original_probe': {'cases': 71, 'rejections': 56, 'positive_controls': 15},
    'final_supplemental_rejections': 3,
    'misnamed_capture_preserved_as_actual_completed_implementation_run': True,
    'full365': 'NOT_PASSED_G325_NO_WAIVER'}, indent=2))
