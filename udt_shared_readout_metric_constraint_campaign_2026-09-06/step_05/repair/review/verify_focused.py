import hashlib
import json
import pathlib

repo=pathlib.Path('/home/udt-admin/udt_mass_codex')
author=repo/'udt_shared_readout_metric_constraint_campaign_2026-09-06/step_05'
repair=author/'repair'
scratch=pathlib.Path('/tmp/tri_step05_focused.UkLQok')
initial=pathlib.Path('/tmp/tri_step05_review.NCKABt')

original=(author/'check_exact.py').read_text()
expected=original.replace('"""Exact controls for bounded-weight overlap constraints, not physical calibration."""',
                         '"""Same-premise repaired controls; initial frozen check_exact.py remains unchanged."""')
expected=expected.replace("'missing_half', 'fixed_weights'))", "'missing_half', 'fixed_weights', 'reject_nonzero'))")
expected=expected.replace('def construct(z, e):\n', "def construct(z, e):\n    if mode == 'reject_nonzero' and any(z):\n        return None\n")
expected=expected.replace('        result = construct(zz, e)\n',
                         "        result = construct(zz, e)\n        feasible = min(zz) >= 0 and (sum(zz) == 0 or\n                    e >= max(Q(0), 2*max(zz)/sum(zz)-1))\n        check('record_feasibility_not_silently_discarded', (result is not None) == feasible)\n")
assert expected==(repair/'check_exact.py').read_text(), 'only_declared_four_delta_blocks'
assert (repair/'author_exact.stdout').read_bytes()==(scratch/'repaired_baseline.stdout').read_bytes()
baseline=json.loads((scratch/'repaired_baseline.stdout').read_text())
assert baseline['status']=='PASS' and baseline['assertions']==1887
assert len(baseline['guard_groups'])==17 and baseline['control_records']==625
assert baseline['constructed_records']==182 and baseline['rejected_records']==443
failures=[]
for name, guard in [
 ('unrelaxed','sharp_boundary_not_rejected'),
 ('wrong_sign','sharp_boundary_not_rejected'),
 ('missing_half','original_weighted_integrals_reconstruct'),
 ('fixed_weights','original_weighted_integrals_reconstruct'),
 ('reject_nonzero','record_feasibility_not_silently_discarded'),
]:
    report=json.loads((scratch/f'repaired_mutant_{name}.stdout').read_text())
    capture=json.loads((scratch/f'repaired_mutant_{name}.json').read_text())
    assert report['status']=='FAIL' and report['guard']==guard
    assert capture['returncode']==1 and not capture['timeout']
    failures.append({'mutant':name,'first_failure':guard})
report=json.loads((scratch/'original_false_pass_reapplied.stdout').read_text())
capture=json.loads((scratch/'original_false_pass_reapplied.json').read_text())
assert report['status']=='FAIL' and report['guard']=='record_feasibility_not_silently_discarded'
assert capture['returncode']==1 and not capture['timeout']
for manifest, root in [(author/'CANDIDATE_SHA256SUMS',repo),
                       (author/'SOURCE_SHA256SUMS',repo),
                       (repair/'REPAIR_SHA256SUMS',repo),
                       (initial/'REVIEW_SHA256SUMS',initial)]:
    for line in manifest.read_text().splitlines():
        digest,path=line.split('  ',1)
        assert hashlib.sha256((root/path).read_bytes()).hexdigest()==digest
print(json.dumps({'exact_declared_delta_only':True,'baseline_byte_match':True,
                  'baseline_assertions':1887,'guard_groups':17,'record_counts':[625,182,443],
                  'registered_mutations':failures,'original_false_pass_now_caught':True,
                  'initial_candidate_sources_review_and_repair_hashes_verified':True,
                  'verdict':'VERIFIED-WITH-CAVEATS; focused regression repair accepted; no theorem or premise change'},indent=2))
