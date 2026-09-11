"""Seal final fidelity; no future aggregate publication result is anticipated."""
from pathlib import Path
import datetime
import hashlib
import json
repo=Path(__file__).resolve().parents[2]
review=Path(__file__).resolve().parent
bank=review.parent
files=[p for p in bank.rglob('*') if p.is_file() and not {'__pycache__','.pytest_cache'} & set(p.parts)
       and p.name not in ['FINAL_FIDELITY_RECEIPT.json','ARTIFACT_SHA256SUMS','PREPUBLICATION_RECEIPT.json']]
inputs=json.loads((bank/'FULL397_INPUTS.json').read_text())
files += [repo/p for p in inputs['sha256']]
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
record={'context':'/root/ti2_banking_fidelity','runtime_model_version':'UNATTESTED',
 'first_observed_utc':'2026-09-11T18:54:40Z',
 'sealed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'verdict':'FIDELITY_REVIEWED_WITH_CAVEATS__G414_FULL_CONDITIONAL_SCOPE',
 'scientific_repairs':0,'integration_objections_remaining':0,
 'actual_parent_full397_seconds':403.0194429080002,
 'actual_parent_final_navigation':'592passed/1duplicate-full-wrapper-deselected',
 'parent_audit_and_suite':'Inspected actual receipts/streams; not reviewer reruns',
 'reviewer_final_captures':[json.loads((review/(n+'.json')).read_text()) for n in [
 'full397_running_inputs','sealed_review_correspondence','final_metadata','final_source_preservation']],
 'original_substantive_review_sha256':sha(review/'REVIEW.md'),
 'original_substantive_receipt_sha256':sha(review/'REVIEW_RECEIPT.json'),
 'cache_exclusions':['__pycache__','.pytest_cache'],
 'future_parent_gates':['aggregate_manifest','explicit_staging_inventory','commit','push'],
 'sha256':{str(p.relative_to(repo)):sha(p) for p in sorted(set(files))}}
assert record['original_substantive_review_sha256']=='a67d9c4d2c455e74a2eef144cbd4273ccdb045b948c18fa832104f3ac4715fc4'
assert record['original_substantive_receipt_sha256']=='fe8ca6f6d67b1a07500270a293d0adff193a338f5e6672910c45aad7332708ab'
with (review/'FINAL_FIDELITY_RECEIPT.json').open('x') as stream:
 json.dump(record,stream,indent=2);stream.write('\n')
print(json.dumps({'sealed_utc':record['sealed_utc'],'pins':len(record['sha256']),
 'final_fidelity_sha256':sha(review/'FINAL_FIDELITY.md'),
 'final_receipt_sha256':sha(review/'FINAL_FIDELITY_RECEIPT.json')},indent=2))
