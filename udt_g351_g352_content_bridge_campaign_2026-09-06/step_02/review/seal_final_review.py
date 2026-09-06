#!/usr/bin/env python3
"""One-time reviewer closure metadata and exact membership seal."""
import datetime, hashlib, json, pathlib, subprocess
p=pathlib.Path(__file__).resolve().parent
repo=pathlib.Path('/home/udt-admin/udt_mass_codex')
stable_sources=[
 'CURRENT_SCIENTIFIC_PREMISES.tsv',
 'startup_surface_g312_two_premise_adoption_refresh_2026-09-01/ADOPTION_RECORD.md',
 'startup_surface_g310_universal_reciprocity_refresh_2026-08-31/ADOPTION_RECORD.md',
 'udt_g313_tracefree_ricci_solution_space_bootstrap_map_2026-09-01/EXACT_DERIVATION.md',
 'udt_g351_source_free_labelwise_carried_measure_conservation_2026-09-05/EXACT_DERIVATION.md',
 'udt_g352_clock_rate_carried_measure_readout_2026-09-05/EXACT_DERIVATION.md',
 'udt_g313_curvature_phase_current_candidate_2026-09-06/CANDIDATE_ARGUMENT.md',
 'udt_g313_curvature_phase_current_candidate_2026-09-06/review_2026-09-06/STAGE_B_ADVERSARIAL_REVIEW.md',
]
commands=[('final_source_snapshot_diff',['git','diff','--exit-code','c19b5fb147d6afbfd91ec248b0693dfc834ce220','--']+stable_sources,repo),
          ('final_stage_a_auth',['sha256sum','--check','STAGE_A_SHA256SUMS'],p),
          ('final_repository_status',['git','status','--short','--branch'],repo)]
records=[]
for name,cmd,cwd in commands:
    with (p/(name+'.stdout')).open('xb') as out,(p/(name+'.stderr')).open('xb') as err:
        result=subprocess.run(cmd,cwd=cwd,stdout=out,stderr=err,timeout=60)
    records.append({'command':cmd,'cwd':str(cwd),'actual_exit':result.returncode,
                    'stdout_file':name+'.stdout','stderr_file':name+'.stderr'})
    assert result.returncode==0
meta={'seal_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'records':records,
      'report_sha256':hashlib.sha256((p/'STAGE_B_ADVERSARIAL_REVIEW.md').read_bytes()).hexdigest(),
      'verdict_sha256':hashlib.sha256((p/'REVIEW_VERDICT.json').read_bytes()).hexdigest(),
      'science_sources_compared_against_snapshot':stable_sources,
      'stage_a_campaign_log_hash_is_historical_exposure_not_current_status_lock':True}
with (p/'FINAL_METADATA.json').open('x') as f:
    json.dump(meta,f,indent=2)
names=sorted([q.name for q in p.iterdir() if q.is_file()]+['ARCHIVE_FILES.txt','REVIEW_SHA256SUMS'])
with (p/'ARCHIVE_FILES.txt').open('x') as f:
    f.write(''.join(n+'\n' for n in names))
with (p/'REVIEW_SHA256SUMS').open('x') as f:
    for name in names:
        if name=='REVIEW_SHA256SUMS': continue
        f.write(hashlib.sha256((p/name).read_bytes()).hexdigest()+'  '+name+'\n')
print(json.dumps({'archive_files':len(names),'manifest_payloads':len(names)-1,
 'report_sha256':meta['report_sha256'],'verdict_sha256':meta['verdict_sha256'],
 'manifest_sha256':hashlib.sha256((p/'REVIEW_SHA256SUMS').read_bytes()).hexdigest()},indent=2))
