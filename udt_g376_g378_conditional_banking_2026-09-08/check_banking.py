"""Proportional exact-source banking checks and executed rejection fixtures, not proof."""
import hashlib
import json
import subprocess
import sys
import tempfile
from pathlib import Path

pkg=Path(__file__).resolve().parent
root=pkg.parent
sys.path.insert(0,str(root))
import verify_current_scientific_premises as v

def git(*args):
    return subprocess.check_output(['git','-c','core.preloadIndex=false',
        '-c','index.threads=1',*args],cwd=root,text=True)

checks={}
def check(n,x):
    checks[n]=bool(x)
    assert x,n

base=v.BERGER_BANKING_SNAPSHOT
owned=(pkg.name+'/', 'udt_closed_fibre_persistence_campaign_2026-09-08/')
allowed={'AGENTS.md','LIVE.md','HANDOFF.md','CURRENT_RESEARCH_PROGRAM.md',
    'CURRENT_SCIENTIFIC_PREMISES.md','CURRENT_SCIENTIFIC_PREMISES.tsv',
    'INDEX.md','MEMORY.md','verify_current_scientific_premises.py'}
check('grok',git('branch','--show-current').strip()=='grok')
check('authorized_tracked_changes',all(n in allowed or n.startswith(owned)
    for n in git('diff',base,'--name-only').splitlines()))
unrelated=sorted(s for s in git('status','--short').splitlines()
    if s.startswith('?? ') and not s[3:].startswith(owned))
check('46_unrelated_names',len(unrelated)==46)
check('unrelated_name_digest',hashlib.sha256('\n'.join(unrelated).encode()).hexdigest()
    =='d65d71d63a56b95aabfd61f33317b1f1f2b2a62a85ded8258c525b99a5e156ea')
check('old_science_and_fixed_manuscript_unchanged',not git('diff',base,'--name-only',
    'CANON.md','UDT_METRIC_KERNEL_DEVELOPMENT.md','UDT_METRIC_KERNEL_COVERAGE.tsv',
    'udt_berger_initial_data_preservation_campaign_2026-09-08',
    'udt_berger_global_constraint_campaign_2026-09-08').strip())
v.validate_berger_banking(root)
checks['source225_and_additive_guard']=True
v.validate_startup_surface(root)
checks['all_prior_banking_and_current_startup_guards']=True

reg=(root/'CURRENT_SCIENTIFIC_PREMISES.tsv').read_text()
rec=(root/v.BERGER_BANKING_SOURCE).read_text()
mutants=[
 ('old_row_changed',reg.replace('G375\t','G375_BAD\t',1),rec,
  'changed an existing scientific registry row'),
 ('missing_required_prerequisite','\n'.join(s for s in reg.split('\n') if not s.startswith('G376\t')),rec,
  'must add exactly three distinct rows'),
 ('duplicate_new_row',reg+next(s for s in reg.splitlines() if s.startswith('G378\t'))+'\n',rec,
  'must add exactly three distinct rows'),
 ('physical_grade',reg.replace(v.CONDITIONAL_BANKING_STATUS,'PHYSICAL_HOPF_STABILITY',1),rec,
  'G376 banking grade changed'),
 ('image_projector_conflated',reg.replace('IMAGE_Y_ZERO_PROJECTOR_Y_AND_K_ZERO_DISTINCT','SAME_STATIONARITY'),rec,
  'G376 scope lacks IMAGE_Y_ZERO'),
 ('zero_strata_omitted',reg.replace('ALL_SIGNS_ZERO_MEAN_ROOT_CONE_STRATA_RETAINED','POSITIVE_ROOT_ONLY'),rec,
  'G376 scope lacks ALL_SIGNS'),
 ('false_pass_erased',reg.replace('ACTUAL_6_OF_8_AUTHOR_CATCHES_TWO_FALSE_PASSES_INDEPENDENT_FULL_TENSOR_CATCH','EIGHT_AUTHOR_CATCHES'),rec,
  'G376 scope lacks ACTUAL_6_OF_8'),
 ('trace_frozen',reg.replace('TRACE_DETERMINED_NOT_ADDITIONALLY_FIXED','FIXED_TRACE'),rec,
  'G377 scope lacks TRACE_DETERMINED'),
 ('kernel_ignored',reg.replace('KILLING_KERNEL_COMPLEMENT_INVERSE_ONLY','INVERSE_ALL_VECTORS'),rec,
  'G377 scope lacks KILLING_KERNEL'),
 ('cotton_bookkeeping_upgraded',reg.replace('EXP_MINUS6T_BOOKKEEPING_ONLY','TRANSFORMATION_PROOF'),rec,
  'G377 scope lacks EXP_MINUS6T'),
 ('homogeneity_imported',reg.replace('BG1_FAMILY_HYPOTHESES_BI1_ARBITRARY_SMOOTH_OPERATOR_ENTIRE_REVIEWS','ALL_BI1_HOMOGENEOUS_ASSUMPTIONS'),rec,
  'G378 scope lacks BG1_FAMILY'),
 ('limit_interchanged',reg.replace('ONE_FINITE_FREQUENCY_SEED_BEFORE_NONLINEAR_AMPLITUDE_LIMIT','UNIFORM_DOUBLE_LIMIT'),rec,
  'G378 scope lacks ONE_FINITE'),
 ('method_hypothesis_removed',reg.replace('SHORT_NORMAL_TIME_CONDITIONAL_SMOOTH_MARKED_CAUCHY_METHOD_AND_GAP','GENERIC_GLOBAL_EVOLUTION'),rec,
  'G378 scope lacks SHORT_NORMAL_TIME'),
 ('bg2_false_pass_erased',reg.replace('THREE_ACTUAL_SYMBOL_ONLY_FALSE_PASSES_FULL_TENSOR_CATCHES','SYMBOL_CHECKS_CERTIFY_FULL_OPERATOR'),rec,
  'G378 scope lacks THREE_ACTUAL'),
 ('different_model_claim',reg.replace('FRESH_SEPARATE_CONTEXT_MODEL_UNKNOWN_DIFFERENT_MODEL_UNTESTED','DIFFERENT_MODEL_VERIFIED',1),rec,
  'G376 review independence changed'),
 ('unrelated_promotion',reg,rec.replace('HB2/HB3 and BI2/BI3 remain UNPROMOTED','ALL PREDECESSORS ACCEPTED'),
  'record lacks HB2/HB3 and BI2/BI3 remain UNPROMOTED'),
]
caught={}
for name,raw,record,reason in mutants:
    with tempfile.TemporaryDirectory(prefix='udt-berger-bank-guard-') as temp:
        fixture=Path(temp)
        (fixture/'CURRENT_SCIENTIFIC_PREMISES.tsv').write_text(raw)
        dest=fixture/v.BERGER_BANKING_SOURCE
        dest.parent.mkdir(parents=True)
        dest.write_text(record)
        try:
            v.validate_berger_banking(fixture,authenticate_sources=False)
        except (AssertionError,RuntimeError,SystemExit) as exc:
            check('expected_rejection:'+name,reason in str(exc))
            caught[name]=str(exc)
        else:
            raise AssertionError('actual false pass:'+name)
print(json.dumps(dict(kind='source correspondence and selected guard rejections NOT proof',
    snapshot=base,checks=checks,actual_mutants_caught=caught,registry_rows=361,
    backup_completeness='UNVERIFIED',pre_reboot_unsaved_state='UNVERIFIED',
    protected_payload_bytes='UNVERIFIED: not inspected',host_wide_process_state='UNVERIFIED'),indent=2))
