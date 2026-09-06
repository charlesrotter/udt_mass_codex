#!/usr/bin/env python3
"""One-time scratch evidence capture, preserving raw streams and true exits."""
import datetime, hashlib, json, pathlib, resource, subprocess, time
HERE=pathlib.Path(__file__).resolve().parent
REPO=pathlib.Path('/home/udt-admin/udt_mass_codex')

def run(name,cmd,cwd=REPO,limited=False):
    def limits():
        resource.setrlimit(resource.RLIMIT_AS,(512*1024**2,512*1024**2))
        resource.setrlimit(resource.RLIMIT_CPU,(60,60))
    start=datetime.datetime.now(datetime.timezone.utc).isoformat()
    t=time.monotonic()
    with (HERE/(name+'.stdout')).open('xb') as out, (HERE/(name+'.stderr')).open('xb') as err:
        proc=subprocess.run(cmd,cwd=cwd,stdout=out,stderr=err,timeout=60,
                            preexec_fn=limits if limited else None)
    return {'name':name,'command':cmd,'cwd':str(cwd),'start_utc':start,
            'wall_seconds':round(time.monotonic()-t,6),'actual_exit_code':proc.returncode}

records=[]
records.append(run('stage_a_git',['git','rev-parse','HEAD']))
records.append(run('stage_a_status',['git','status','--short','--branch']))
records.append(run('stage_a_checks',['/usr/bin/time','-v','python3','-B',str(HERE/'stage_a_checks.py')],limited=True))
assert records[-1]['actual_exit_code']==0
paths=[
 'AGENTS.md','LIVE.md','HANDOFF.md','CURRENT_RESEARCH_PROGRAM.md',
 'CURRENT_SCIENTIFIC_PREMISES.md','CURRENT_SCIENTIFIC_PREMISES.tsv',
 'CLAUDE.md','CROSS_MODEL_VERIFY.md','INDEX.md','MEMORY.md',
 '.claude/skills/no-shortcuts/SKILL.md','.claude/skills/verifier-before-record/SKILL.md',
 '.claude/skills/completeness-map/SKILL.md','.claude/skills/solution-space-not-imposition/SKILL.md',
 'udt_g313_tracefree_ricci_solution_space_bootstrap_map_2026-09-01/AUDIT_REPORT.md',
 'udt_g313_tracefree_ricci_solution_space_bootstrap_map_2026-09-01/EXACT_DERIVATION.md',
 'udt_g351_source_free_labelwise_carried_measure_conservation_2026-09-05/AUDIT_REPORT.md',
 'udt_g351_source_free_labelwise_carried_measure_conservation_2026-09-05/EXACT_DERIVATION.md',
 'udt_g352_clock_rate_carried_measure_readout_2026-09-05/AUDIT_REPORT.md',
 'udt_g352_clock_rate_carried_measure_readout_2026-09-05/EXACT_DERIVATION.md',
 'udt_g313_curvature_phase_current_candidate_2026-09-06/CANDIDATE_ARGUMENT.md',
 'udt_g313_curvature_phase_current_candidate_2026-09-06/REVIEW_RECORD.md',
 'udt_g313_curvature_phase_current_candidate_2026-09-06/review_2026-09-06/STAGE_B_ADVERSARIAL_REVIEW.md',
 'udt_g351_g352_content_bridge_campaign_2026-09-06/step_01/CANDIDATE_ARGUMENT.md',
 'udt_g351_g352_content_bridge_campaign_2026-09-06/step_01/review/STAGE_B_ADVERSARIAL_REVIEW.md',
 'udt_g351_g352_content_bridge_campaign_2026-09-06/step_01/review/REVIEW_VERDICT.json',
 'udt_g351_g352_content_bridge_campaign_2026-09-06/step_02/WORK_ORDER.md',
 'udt_g351_g352_content_bridge_campaign_2026-09-06/CAMPAIGN_LOG.md',
]
source_hashes={p:hashlib.sha256((REPO/p).read_bytes()).hexdigest() for p in paths}
(HERE/'STAGE_A_SOURCE_SHA256SUMS').write_text(''.join(f'{digest}  {p}\n' for p,digest in source_hashes.items()))
records.append(run('stage_a_source_auth',['sha256sum','--check',str(HERE/'STAGE_A_SOURCE_SHA256SUMS')]))
(HERE/'STAGE_A_RUN.json').write_text(json.dumps({'records':records,'resource_limits':{'address_space_MiB':512,'CPU_seconds':60,'wall_seconds_per_child':60,'one_child_at_a_time':True},'source_hashes':source_hashes},indent=2)+'\n')
print(json.dumps(records,indent=2))
