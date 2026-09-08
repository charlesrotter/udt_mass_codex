"""Scoped campaign preservation/receipt closure; not scientific proof or banking."""
import csv
import hashlib
import json
from pathlib import Path
import subprocess
import sys

pkg=Path(__file__).resolve().parent
root=pkg.parent
sys.path.insert(0,str(root))
import verify_current_scientific_premises as v
baseline='7dd52b7a2285a62f2c19dd3707d0eba46739d6d4'
prefix=pkg.name+'/'
checks={}
def check(name,value):
    checks[name]=bool(value)
    assert value,name
def git(*args):
    return subprocess.check_output(['git','-c','core.preloadIndex=false',
        '-c','index.threads=1',*args],cwd=root,text=True)
def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()
def verify_sha_manifest(path,allowed_prefix):
    rows=[line.split(maxsplit=1) for line in path.read_text().splitlines()]
    check('manifest_unique:'+str(path.relative_to(root)),len(rows)==len({p for _,p in rows}))
    for expected,relative in rows:
        check('manifest_scope:'+relative,relative.startswith(allowed_prefix))
        check('manifest_pin:'+relative,sha(root/relative)==expected)
    return len(rows)

check('grok',git('branch','--show-current').strip()=='grok')
check('registry_unchanged_since_authorized_bank',sha(root/'CURRENT_SCIENTIFIC_PREMISES.tsv')
      =='629735b28289e75998b00ff491bca123e6a995c8310980c6dc785f1829f8a31c')
v.validate_startup_surface(root)
v.validate_source_metric_banking(root)
checks['startup_and_original_SM_banking_guard']=True
bank='udt_g367_g369_conditional_banking_2026-09-08/'
bank_rows=verify_sha_manifest(root/bank/'SHA256SUMS',bank)
allowed={'LIVE.md','HANDOFF.md','CURRENT_RESEARCH_PROGRAM.md'}
changes=git('diff',baseline,'--name-only').splitlines()
check('only_campaign_and_current_status_changes',all(p in allowed or p.startswith(prefix) for p in changes))
unrelated=sorted(line for line in git('status','--short').splitlines()
                 if line.startswith('?? ') and not line[3:].startswith(prefix))
check('unrelated_names_count_46',len(unrelated)==46)
check('unrelated_names_hash',hashlib.sha256('\n'.join(unrelated).encode()).hexdigest()
      =='d65d71d63a56b95aabfd61f33317b1f1f2b2a62a85ded8258c525b99a5e156ea')
check('exactly_two_step_directories',sorted(p.name for p in pkg.glob('step_*') if p.is_dir())==['step_01','step_02'])
initial_rows=0
review_rows=0
for step in ('step_01','step_02'):
    initial_rows+=verify_sha_manifest(pkg/step/'INITIAL_SHA256SUMS',prefix)
    result=(pkg/step/'REVIEWED_RESULT.md').read_text()
    review=(pkg/step/'review/ADVERSARIAL_REVIEW_INITIAL.md').read_text()
    check('reviewed_not_banked:'+step,'VERIFIED-WITH-CAVEATS' in result and 'NOT BANKED' in result)
    check('actual_review_verdict_present:'+step,'VERIFIED-WITH-CAVEATS' in review)
    manifest=pkg/step/'review/REVIEW_MANIFEST.tsv'
    rows=list(csv.DictReader(manifest.open(),delimiter='\t'))
    check('review_manifest_unique:'+step,len(rows)==len({row['path'] for row in rows}))
    for row in rows:
        target=root/row['path']
        if not target.is_file():
            target=manifest.parent/row['path']
        check('review_manifest_scope:'+step+':'+row['path'],target.resolve().is_relative_to((pkg/step/'review').resolve()))
        check('review_manifest_pin:'+step+':'+row['path'],sha(target)==row['sha256'])
        review_rows+=1
dependency_rows=verify_sha_manifest(pkg/'step_02/DEPENDENCY_SHA256SUMS',prefix)
for row in csv.DictReader((pkg/'SOURCE_LEDGER.tsv').open(),delimiter='\t'):
    check('source_pin:'+row['role'],sha(root/row['path'])==row['sha256'])

expected_failures={'step_02/review/independent_initial.json':1}
receipts=0
for path in sorted(pkg.rglob('*.json')):
    rec=json.loads(path.read_text())
    if 'command' not in rec or 'returncode' not in rec:
        continue
    rel=path.relative_to(pkg).as_posix()
    check('receipt_exit:'+rel,rec['returncode']==expected_failures.get(rel,0))
    check('receipt_caps:'+rel,rec['address_space_bytes']<=512*1024**2 and rec['cpu_seconds']<=60 and not rec['timeout'])
    check('receipt_raw_streams:'+rel,path.with_suffix('.stdout').is_file() and path.with_suffix('.stderr').is_file())
    receipts+=1
failed=pkg/'step_02/review/independent_product_check_initial_failed.py'
corrected=pkg/'step_02/review/independent_product_check.py'
check('syntax_only_failure_retained','SyntaxError' in (pkg/'step_02/review/independent_initial.stderr').read_text())
check('reviewer_correction_one_character_only',failed.read_text().replace(
    '.subs(u:s.Rational(1,4))','.subs(u,s.Rational(1,4))',1)==corrected.read_text())
check('no_python_cache',not list(pkg.rglob('*.pyc')))
print(json.dumps({'kind':'scope/correspondence/receipt closure; NOT mathematical proof or promotion',
 'baseline':baseline,'head':git('rev-parse','HEAD').strip(),
 'checks':checks,'bank_manifest_rows':bank_rows,'initial_manifest_rows':initial_rows,
 'dependency_manifest_rows':dependency_rows,'review_manifest_rows':review_rows,
 'captured_runs_checked':receipts,'expected_preserved_failures':expected_failures,
 'full352_audit':'banked actual receipt; not rerun by this closure',
 'backup_completeness':'UNVERIFIED','pre_reboot_unsaved_state':'UNVERIFIED',
 'host_wide_process_state':'UNVERIFIED','protected_payloads':'NOT_INSPECTED',
 'physical_adoption_and_new_scientific_banking':'NONE'},indent=2,sort_keys=True))
