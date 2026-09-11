import datetime,hashlib,json,pathlib
repo=pathlib.Path(__file__).resolve().parents[2]
root=pathlib.Path(__file__).resolve().parents[1]
review=pathlib.Path(__file__).resolve().parent
original=json.loads((review/'REVIEW_RECEIPT.json').read_text())
for p,d in original['sha256'].items(): assert hashlib.sha256((repo/p).read_bytes()).hexdigest()==d,p
final=json.loads((review/'final_fidelity_check.stdout').read_text())
for p,d in final['final_document_sha256'].items():assert hashlib.sha256((repo/p).read_bytes()).hexdigest()==d,p
now=datetime.datetime.now(datetime.timezone.utc)
assert now<datetime.datetime(2026,9,11,14,47,tzinfo=datetime.timezone.utc)
files=[p for p in review.iterdir() if p.is_file() and p.name!='FINAL_FIDELITY_RECEIPT.json']
files += [repo/p for p in final['final_document_sha256']]
for name in ['current396_closeout','final_navigation','preservation']:
 files += [root/f'checks/{name}.{suffix}' for suffix in ['stdout','stderr','json','capture_provenance.json']]
pins={str(p.relative_to(repo)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(set(files))}
receipt={'context':'/root/ti2_evolution_review','runtime_model_version':'UNATTESTED',
 'first_observed_utc':'2026-09-11T13:48:06Z','completed_utc':now.isoformat(),
 'elapsed_from_first_observed_seconds':(now-datetime.datetime(2026,9,11,13,48,6,tzinfo=datetime.timezone.utc)).total_seconds(),
 'elapsed_from_earliest_allocation_bracket_seconds':(now-datetime.datetime(2026,9,11,13,47,22,tzinfo=datetime.timezone.utc)).total_seconds(),
 'conservative_allocation_return_utc':'2026-09-11T14:47:00Z',
 'disposition':'FIDELITY_REVIEWED_WITH_CAVEATS; TI2_CONDITIONAL_UNPROMOTED',
 'substantive_review_preserved':True,'scientific_repairs_required':0,
 'final_prose_correction':'Metadata probe checked candidate pins before failing on precomputation path namespace; wording narrowed',
 'science_repeated_in_fidelity':False,'parent_full396_and539_suite':'Actual saved captures inspected, not reviewer reruns',
 'reviewer_metadata_captures':[json.loads((review/(name+'.json')).read_text()) for name in ['closeout_audit_inputs','final_preservation_replay','final_fidelity_check']],
 'scratch_directories_present':final['excluded_cache_directories_present'],
 'publication':'FUTURE; aggregate manifest/staging/commit/push outcomes not prewritten',
 'sha256':pins}
with (review/'FINAL_FIDELITY_RECEIPT.json').open('x') as f:json.dump(receipt,f,indent=2);f.write('\n')
print(json.dumps({'status':receipt['disposition'],'completed_utc':receipt['completed_utc'],
 'seconds_from_earliest_allocation':receipt['elapsed_from_earliest_allocation_bracket_seconds'],'pins':len(pins)}))
