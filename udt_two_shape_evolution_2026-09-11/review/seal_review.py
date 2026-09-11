import datetime,hashlib,json,pathlib
repo=pathlib.Path(__file__).resolve().parents[2]
root=pathlib.Path(__file__).resolve().parents[1]
review=pathlib.Path(__file__).resolve().parent
freeze=json.loads((root/'CANDIDATE_FREEZE.json').read_text())
for p,digest in freeze['sha256'].items(): assert hashlib.sha256((root/p).read_bytes()).hexdigest()==digest,p
files=[p for p in review.iterdir() if p.is_file() and p.name not in ['REVIEW_RECEIPT.json']]
files += [root/'INITIAL_CANDIDATE.md',root/'CANDIDATE_FREEZE.json',root/'DISCOVERY_AND_FREEZE.md']
receipt={'context':'/root/ti2_evolution_review','runtime_model_version':'UNATTESTED',
 'first_observed_utc':'2026-09-11T13:48:06Z','completed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'disposition':'VERIFIED-WITH-CAVEATS_CONDITIONAL_TI2_UNPROMOTED','scientific_repairs_required':0,
 'stage_A_sealed_before_author_TI2_science_exposure':True,
 'whole_candidate_froze_after_reviewer_rate_message':True,
 'parent_audit':'Actual post-repair full396 receipt/stdout/stderr inspected, attributed not rerun',
 'author_scientific_replays':'NOT_PERFORMED; implementations/saved outputs inspected and authenticated',
 'independence':{'fresh_context':True,'source_data_first_ADM_symbolic_route':True,
  'post_exposure_standard_Fraction_full_Gauss_Codazzi_contraction':True,
  'shared_symbolic_library':'SymPy1.13.1','different_model':'UNTESTED','formal_proof':'UNTESTED','human_specialist':'UNTESTED'},
 'scientific_and_metadata_runs':[json.loads((review/(name+'.json')).read_text()) for name in
  ['adm_rate','adm_rate_repaired','fraction_full_rate','fraction_full_rate_repaired','saved_correspondence','fraction_candidate_anchor','candidate_inputs']],
 'sha256':{str(p.relative_to(repo)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(files)}}
with (review/'REVIEW_RECEIPT.json').open('x') as f:json.dump(receipt,f,indent=2);f.write('\n')
print(json.dumps({'completed_utc':receipt['completed_utc'],'status':receipt['disposition'],'files':len(receipt['sha256'])}))
