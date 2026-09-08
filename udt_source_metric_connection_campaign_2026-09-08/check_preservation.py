"""Scoped source/preservation checks; no protected payload access or science proof."""
import csv
import hashlib
import json
import subprocess
from pathlib import Path

root = Path(__file__).resolve().parent.parent
package = Path(__file__).resolve().parent
prefix = package.name + '/'
baseline = 'cc71a324a61bf2711a4b52c8ebee8a8e4d9b8269'
def git(*args):
    return subprocess.check_output(['git','-c','core.preloadIndex=false',
        '-c','index.threads=1',*args],cwd=root,text=True)
checks = {}
def check(name, value):
    checks[name] = bool(value)
    assert value, name
check('grok',git('branch','--show-current').strip() == 'grok')
for row in csv.DictReader((package/'SOURCE_LEDGER.tsv').open(),delimiter='\t'):
    actual = hashlib.sha256((root/row['path']).read_bytes()).hexdigest()
    check('source_pin:'+row['role'],actual == row['sha256'])
allowed = {'LIVE.md','HANDOFF.md','CURRENT_RESEARCH_PROGRAM.md'}
changes = git('diff',baseline,'--name-only').splitlines()
check('tracked_change_scope',all(p in allowed or p.startswith(prefix) for p in changes))
status = git('status','--short').splitlines()
unrelated = sorted(line for line in status if line.startswith('?? ') and not line[3:].startswith(prefix))
name_hash = hashlib.sha256('\n'.join(unrelated).encode()).hexdigest()
check('unrelated_untracked_count',len(unrelated) == 46)
check('unrelated_untracked_name_hash',name_hash == 'd65d71d63a56b95aabfd61f33317b1f1f2b2a62a85ded8258c525b99a5e156ea')
check('no_frozen_source_or_manuscript_changes',not any(p not in allowed and not p.startswith(prefix) for p in changes))
print(json.dumps({'kind':'source correspondence and names-only preservation; not proof',
    'baseline':baseline,'head':git('rev-parse','HEAD').strip(),'checks':checks,
    'unrelated_untracked_count':len(unrelated),'unrelated_names_sha256':name_hash,
    'backup_completeness':'UNVERIFIED','pre_reboot_unsaved_state':'UNVERIFIED',
    'host_wide_process_inventory':'UNVERIFIED','protected_payloads':'NOT_INSPECTED'},indent=2,sort_keys=True))
