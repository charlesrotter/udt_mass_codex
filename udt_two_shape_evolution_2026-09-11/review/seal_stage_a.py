import datetime,hashlib,json,pathlib,subprocess
repo=pathlib.Path(__file__).resolve().parents[2]
review=pathlib.Path(__file__).resolve().parent
source_paths=[
 'AGENTS.md','CLAUDE.md','.claude/skills/no-shortcuts/SKILL.md',
 '.claude/skills/completeness-map/SKILL.md','.claude/skills/verifier-before-record/SKILL.md',
 'udt_ti1_banking_2026-09-11/WORK_ORDER.md','udt_ti1_banking_2026-09-11/LAUNCH.json',
 'udt_ti1_banking_2026-09-11/CLOSEOUT.md','udt_ti1_banking_2026-09-11/BANKING_RECORD.md',
 'udt_gr_filter_reconciliation_2026-09-09/AUTHORITY_RECORD.md',
 'udt_two_shape_evolution_2026-09-11/REVIEW_DISPATCH.md',
 'udt_two_shape_evolution_2026-09-11/FRAME_AND_DISCOVERY.md',
 'udt_two_shape_evolution_2026-09-11/BANKED_DEPENDENCY_ADOPTION.json',
 'udt_reviewed_backlog_banking_2026-09-10/capture_existing.py',
 'udt_shared_readout_metric_constraint_campaign_2026-09-06/run_capture.py',
]
for q in ['INITIAL_CANDIDATE.md','DISCOVERY_AND_DATA_FREEZE.md','REVIEWED_RESULT.md','review/REVIEW.md','review/STAGE_A.md','review/FINAL_FIDELITY.md','review/REVIEW_RECEIPT.json']:
 source_paths.append('udt_two_shape_nonlinear_interaction_2026-09-11/'+q)
for p in review.iterdir():
 if p.is_file() and p.name!='STAGE_A_SEAL.json': source_paths.append(str(p.relative_to(repo)))
digests={p:hashlib.sha256((repo/p).read_bytes()).hexdigest() for p in sorted(set(source_paths))}
status=subprocess.check_output(['git','status','--porcelain=v1','--untracked-files=normal'],cwd=repo).decode()
original=''.join(line+'\n' for line in status.splitlines() if not line.endswith('udt_two_shape_evolution_2026-09-11/'))
assert hashlib.sha256(original.encode()).hexdigest()=='55e7c4508622f912730f9c068cc571c370b3977bc1110eb0a48a8218dbe024c2'
row_lines=(repo/'CURRENT_SCIENTIFIC_PREMISES.tsv').read_text().splitlines()
selected={q:next(x for x in row_lines if x.startswith(q+'\t')) for q in ['G413','G312','G176','G166']}
result={'sealed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'context':'/root/ti2_evolution_review','runtime_model_version':'UNATTESTED',
 'first_observed_utc':'2026-09-11T13:48:06Z','conservative_return_utc':'2026-09-11T14:47:00Z',
 'author_TI2_science_exposure_before_seal':False,'sha256':digests,
 'original46_status_sha256':hashlib.sha256(original.encode()).hexdigest(),
 'selected_registry_rows':selected,
 'head':subprocess.check_output(['git','rev-parse','HEAD'],cwd=repo).decode().strip(),
 'branch':subprocess.check_output(['git','branch','--show-current'],cwd=repo).decode().strip(),
 'scope':'Source/data-first provisional ADM rate; author whole-candidate stage pending'}
with (review/'STAGE_A_SEAL.json').open('x') as f: json.dump(result,f,indent=2);f.write('\n')
print(json.dumps({'seal_utc':result['sealed_utc'],'files':len(digests),'status':'PASS'}))
