import hashlib
import json
import pathlib

repo=pathlib.Path('/home/udt-admin/udt_mass_codex')
author=repo/'udt_shared_readout_metric_constraint_campaign_2026-09-06/step_05'
scratch=pathlib.Path('/tmp/tri_step05_review.NCKABt')
assert (author/'author_exact.stdout').read_bytes()==(scratch/'author_baseline.stdout').read_bytes()
results=[]
for name, expected in [
 ('unrelaxed','sharp_boundary_not_rejected'),
 ('wrong_sign','sharp_boundary_not_rejected'),
 ('missing_half','original_weighted_integrals_reconstruct'),
 ('fixed_weights','original_weighted_integrals_reconstruct'),
]:
    output=json.loads((scratch/f'author_mutant_{name}.stdout').read_text())
    capture=json.loads((scratch/f'author_mutant_{name}.json').read_text())
    assert output['status']=='FAIL' and output['guard']==expected
    assert capture['returncode']==1 and not capture['timeout']
    results.append({'mutant':name,'first_failure':expected})
false_pass=json.loads((scratch/'false_pass_overreject.stdout').read_text())
assert false_pass['status']=='PASS' and false_pass['constructed_records']==5
assert false_pass['rejected_records']==620
for line in (scratch/'phase_A_seal.stdout').read_text().splitlines():
    digest, path=line.split('  ',1)
    assert hashlib.sha256((scratch/path).read_bytes()).hexdigest()==digest
for manifest in ('CANDIDATE_SHA256SUMS','SOURCE_SHA256SUMS'):
    for line in (author/manifest).read_text().splitlines():
        digest,path=line.split('  ',1)
        assert hashlib.sha256((repo/path).read_bytes()).hexdigest()==digest
print(json.dumps({'baseline_byte_match':True,'mutations':results,
                  'false_pass_overreject':false_pass,
                  'phase_A_seal_unchanged':True,'author_manifests_unchanged':True},indent=2))
