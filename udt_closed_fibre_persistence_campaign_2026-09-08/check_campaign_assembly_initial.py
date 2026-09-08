"""Read-only campaign correspondence/receipt checks, not mathematical proof."""
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys

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
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def manifest(p):
    rows=p.read_text().splitlines()
    for row in rows:
        expected,relative=row.split('  ',1)
        check('sha:'+relative,sha(root/relative)==expected)
    return len(rows)

base='32d23fb47dc4e440acc8c721aef6cb8201796ded'
bank='e1d165c65c857c8c4e4e343b605482f3da0f19b6'
check('grok',git('branch','--show-current').strip()=='grok')
for p in ['AGENTS.md','CURRENT_SCIENTIFIC_PREMISES.tsv','verify_current_scientific_premises.py']:
    check('unchanged_since_banking:'+p,(root/p).read_bytes()==subprocess.check_output(['git','show',bank+':'+p],cwd=root))
allowed={'LIVE.md','HANDOFF.md','CURRENT_RESEARCH_PROGRAM.md','CURRENT_SCIENTIFIC_PREMISES.md','INDEX.md','MEMORY.md'}
changed=git('diff',bank,'--name-only').splitlines()
check('only_current_tracking_and_campaign',all(p in allowed or p.startswith(pkg.name+'/')
    or p=='udt_g376_g378_conditional_banking_2026-09-08/PUBLICATION_RECEIPT.md' for p in changed))
check('canon_fixed_manuscript_original_evidence_unchanged',not git('diff',base,'--name-only',
    'CANON.md','UDT_METRIC_KERNEL_DEVELOPMENT.md','UDT_METRIC_KERNEL_COVERAGE.tsv',
    'udt_berger_initial_data_preservation_campaign_2026-09-08',
    'udt_berger_global_constraint_campaign_2026-09-08').strip())
names=sorted(x for x in git('status','--short').splitlines() if x.startswith('?? ')
    and not x[3:].startswith((pkg.name+'/','udt_g376_g378_conditional_banking_2026-09-08/')))
check('46_unrelated_names',len(names)==46)
check('unrelated_name_digest',hashlib.sha256('\n'.join(names).encode()).hexdigest()
    =='d65d71d63a56b95aabfd61f33317b1f1f2b2a62a85ded8258c525b99a5e156ea')
v.validate_berger_banking(root)
v.validate_startup_surface(root)
checks['reused_current_and_prior_banking_guards']=True
check('25_exact_scientific_source_pins',manifest(pkg/'step_02/SOURCE_PINS_SHA256SUMS')==25)
check('65_banking_evidence_files',manifest(root/'udt_g376_g378_conditional_banking_2026-09-08/BANKING_EVIDENCE_SHA256SUMS')==65)

modes={1:['baseline','integer_only','all_rational_regular','wrong_period','swap_axes'],
       2:['baseline','omit_inverse','kill_polarization','wrong_slope','wrong_phase']}
for step in [1,2]:
    p=pkg/f'step_{step:02}'
    pins=re.findall(r'^    ([a-f0-9]{64})  (.+)$',(p/'CANDIDATE_FREEZE.md').read_text(),re.M)
    check(f'nonempty_CF{step}_freeze',len(pins)>=3)
    for expected,relative in pins:check(f'CF{step}_freeze:'+relative,sha(p/relative)==expected)
    disposition='REVIEW_RESULT.json' if step==1 else 'REVIEW_DISPOSITION.json'
    review=json.loads((p/'review'/disposition).read_text())
    check(f'CF{step}_reviewed_conditional',review['disposition']=='VERIFIED-WITH-CAVEATS')
    check(f'CF{step}_not_promoted','UNPROMOTED' in (p/'REVIEWED_RESULT.md').read_text())
    for mode in modes[step]:
        receipt=json.loads((p/f'check_{mode}.json').read_text())
        out=json.loads((p/f'check_{mode}.stdout').read_text())
        check(f'CF{step}_{mode}_exit',receipt['returncode']==(0 if mode=='baseline' else 1))
        check(f'CF{step}_{mode}_actual_guard_failure',bool(out['failed'])==(mode!='baseline'))
        check(f'CF{step}_{mode}_no_timeout_or_stderr',not receipt['timeout'] and (p/f'check_{mode}.stderr').read_bytes()==b'')
check('parent_replay_matches_independent_seal',(pkg/'step_02/parent_independent_replay.stdout').read_bytes()
    ==(pkg/'step_02/review/source_first_check.stdout').read_bytes())
false1=json.loads((pkg/'step_01/review/false_pass_either_axis.stdout').read_text())
catch1=json.loads((pkg/'step_01/review/catch_either_axis.stdout').read_text())
check('CF1_actual_false_pass_retained',false1['passed']==29 and not false1['failed'])
check('CF1_focused_catch_retained',catch1['failed']==['regular_2','regular_1/2'])
false2=json.loads((pkg/'step_02/review/post_exposure_check_corrected.stdout').read_text())
check('CF2_two_actual_false_passes_retained',len(false2['actual_false_pass_probes'])==2
    and all(r['author_suite_false_pass'] for r in false2['actual_false_pass_probes']))
check('CF2_two_focused_catches_retained',len(false2['focused_reviewer_catches'])==2
    and all(r['returncode']==1 for r in false2['focused_reviewer_catches']))
check('CF2_reviewer_original_failure_retained',json.loads((pkg/'step_02/review/post_exposure_check.json').read_text())['returncode']==1)
print(json.dumps({'kind':'source/freeze/receipt correspondence and current tracking; NOT proof',
    'head':git('rev-parse','HEAD').strip(),'checks':checks,
    'new_scientific_results_promoted':False,'protected_payload_bytes':'UNVERIFIED/not inspected',
    'backup_completeness':'UNVERIFIED','pre_reboot_unsaved_state':'UNVERIFIED'},indent=2))
