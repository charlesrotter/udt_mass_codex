import hashlib
import json
import pathlib
import subprocess

root=pathlib.Path('/home/udt-admin/udt_mass_codex')
pin='70034a6faa9264bf054eb473d5eb7a0889f3d2de'
source_paths=[
 'CURRENT_SCIENTIFIC_PREMISES.tsv',
 'udt_g351_source_free_labelwise_carried_measure_conservation_2026-09-05/AUDIT_REPORT.md',
 'udt_g351_source_free_labelwise_carried_measure_conservation_2026-09-05/EXACT_DERIVATION.md',
 'udt_g352_clock_rate_carried_measure_readout_2026-09-05/AUDIT_REPORT.md',
 'udt_g352_clock_rate_carried_measure_readout_2026-09-05/EXACT_DERIVATION.md',
]
out=[]
for path in source_paths:
    current=(root/path).read_bytes()
    pinned=subprocess.run(['git','show',pin+':'+path],cwd=root,capture_output=True,check=True).stdout
    assert current==pinned, path
    out.append({'path':path,'sha256':hashlib.sha256(current).hexdigest(),'matches_pin':True})
for path in [
 'udt_shared_readout_metric_constraint_campaign_2026-09-06/WORK_ORDER.md',
 'udt_shared_readout_metric_constraint_campaign_2026-09-06/step_05/QUESTION.md',
 'udt_shared_readout_metric_constraint_campaign_2026-09-06/step_01/CANDIDATE_ARGUMENT.md',
 'udt_shared_readout_metric_constraint_campaign_2026-09-06/step_01/REVIEW_RECORD.md',
 'udt_shared_readout_metric_constraint_campaign_2026-09-06/step_02/CANDIDATE_ARGUMENT.md',
 'udt_shared_readout_metric_constraint_campaign_2026-09-06/step_02/REVIEW_RECORD.md',
 'udt_shared_readout_metric_constraint_campaign_2026-09-06/step_02/review/PHASE_B_ADVERSARIAL_REVIEW.md',
 'udt_shared_readout_metric_constraint_campaign_2026-09-06/run_capture.py',
]:
    out.append({'path':path,'sha256':hashlib.sha256((root/path).read_bytes()).hexdigest()})
print(json.dumps({'accepted_pin':pin,'sources':out},indent=2))
