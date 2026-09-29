import datetime
import hashlib
import json
import pathlib
import platform
import subprocess

root = pathlib.Path.cwd()
out = root / 'udt_gr_commitment_audit_2026-09-29/review/fidelity'
launch_path = root / 'udt_gr_commitment_audit_2026-09-29/SOURCE_PINS.json'
launch = json.loads(launch_path.read_text())['sha256']
def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

launch_results = {p: {'expected': h, 'actual': sha(root/p)} for p,h in launch.items()}
assert all(v['expected']==v['actual'] for v in launch_results.values()), launch_results
consulted = [
 'AGENTS.md','CLAUDE.md','CROSS_MODEL_VERIFY.md',
 '.claude/skills/no-shortcuts/SKILL.md',
 '.claude/skills/completeness-map/SKILL.md',
 '.claude/skills/verifier-before-record/SKILL.md',
 'development_reconstruction_2026-09-29/MAINTENANCE.md',
 'development_reconstruction_2026-09-29/SOURCE_CORRECTIONS.md',
 'development_reconstruction_2026-09-29/DEVELOPMENT_GRAPH.json',
 'founding.md','CURRENT_SCIENTIFIC_PREMISES.tsv','UDT_DEVELOPMENT.md',
 'udt_gr_commitment_audit_2026-09-29/WORK_ORDER.md',
 'udt_gr_commitment_audit_2026-09-29/SOURCE_PINS.json',
 'udt_gr_filter_reconciliation_2026-09-09/AUTHORITY_RECORD.md',
 'startup_surface_g310_universal_reciprocity_refresh_2026-08-31/ADOPTION_RECORD.md',
 'udt_g261_universal_metric_coupling_parent_operator_ownership_2026-08-25/EXACT_DERIVATION.md',
 'udt_g261_universal_metric_coupling_parent_operator_ownership_2026-08-25/EXTERNAL_REPAIR_FOLLOWUP_GPT54.md',
 'udt_g301_scale_free_quiet_regular_causal_principal_classification_2026-08-30/EXACT_DERIVATION.md',
 'udt_g301_scale_free_quiet_regular_causal_principal_classification_2026-08-30/EXTERNAL_REVIEW_GPT54.md',
 'udt_g301_scale_free_quiet_regular_causal_principal_classification_2026-08-30/EXTERNAL_REPAIR_FOLLOWUP_GPT54.md',
 'udt_gr_response_selection_2026-09-28/REVIEWED_RESULT.md',
 'udt_gr_response_selection_2026-09-28/INITIAL_DERIVATION.md',
 'udt_gr_response_selection_2026-09-28/OWNERSHIP_MAP.md',
 'udt_gr_response_selection_2026-09-28/review/DIRECT_REVIEW.md',
 'udt_response_measurement_scaling_2026-09-28/REVIEWED_RESULT.md',
 'udt_response_measurement_scaling_2026-09-28/INITIAL_CANDIDATE.md',
 'udt_response_measurement_scaling_2026-09-28/review/DIRECT_REVIEW.md',
 'udt_conservation_variational_response_2026-09-28/REVIEWED_RESULT.md',
 'udt_conservation_variational_response_2026-09-28/INITIAL_CANDIDATE.md',
 'udt_conservation_variational_response_2026-09-28/REPAIR.md',
 'udt_conservation_variational_response_2026-09-28/review/DIRECT_REVIEW.md',
 'udt_local_kernel_symmetry_release_2026-09-13/capture.py',
 'udt_shared_readout_metric_constraint_campaign_2026-09-06/run_capture.py',
]
payloads = ['SOURCE_FIRST.md','CHECK_PLAN.md','check_representatives.py',
 'representatives_01.stdout','representatives_01.stderr','representatives_01.json',
 'representatives_01.capture_provenance.json','seal_source_first.py']
record = {
 'sealed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'reviewer':'/root/gca_fidelity',
 'branch':subprocess.check_output(['git','branch','--show-current'],text=True).strip(),
 'head':subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),
 'tracked_diff_names':subprocess.check_output(['git','-c','index.threads=1','-c','core.preloadIndex=false','diff','--name-only'],text=True).splitlines(),
 'python':platform.python_version(),
 'source_first_exposure':'Historical arguments/reviews exposed; no GCA candidate/code/results or other GCA review read.',
 'launch_pins_verified':launch_results,
 'consulted_sources_sha256':{p:sha(root/p) for p in consulted},
 'review_payloads_sha256':{p:sha(out/p) for p in payloads},
 'external_primary_statement':{
   'url':'https://arxiv.org/html/1202.5811v1',
   'scope':'Definitions and Theorem 1 read through web tool; not full proof replay; no local byte hash claimed',
   'lovelock_followup':'Metadata/page initial response seen; subsequent bounded fetch failed; theorem application remains attributed to CRV1 review'
 },
 'checksum_limit':'Correspondence only; not truth, trusted timestamp or independent authorship'
}
assert record['branch']=='grok'
assert record['head']=='9edec2e528e058cbfab11de7a1eff1f90d0cc970'
with (out/'SOURCE_FIRST_SEAL.json').open('x') as f:
    json.dump(record,f,indent=2);f.write('\n')
print(json.dumps({'launch_pins_match':len(launch_results),
 'consulted_sources':len(consulted),'review_payloads':len(payloads),
 'report_sha256':sha(out/'SOURCE_FIRST.md'),
 'seal_sha256':sha(out/'SOURCE_FIRST_SEAL.json'),
 'head':record['head'],'tracked_diff_names':record['tracked_diff_names']},indent=2))
