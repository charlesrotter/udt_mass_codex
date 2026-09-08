"""Read-only receipt/candidate authentication; no audit replay or Git mutation."""
import csv
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess

root=Path.cwd()
campaign=root/'udt_berger_initial_data_preservation_campaign_2026-09-08'
step=campaign/'step_01'
review=step/'review'
checks=[]
hashes={}
def digest(path):
    value=hashlib.sha256(path.read_bytes()).hexdigest()
    hashes[str(path.relative_to(root))]=value
    return value
def check(name,condition):
    checks.append({'name':name,'pass':bool(condition)})
def run_git(*args):
    command=['git',*args]
    result=subprocess.run(command,text=True,capture_output=True,check=False,
        env={**os.environ,'GIT_OPTIONAL_LOCKS':'0'},timeout=10)
    return {'command':command,'returncode':result.returncode,
            'stdout':result.stdout,'stderr':result.stderr}

freeze=step/'CANDIDATE_FREEZE.md'
digest(freeze)
entries=re.findall(r'^    ([0-9a-f]{64})  (\S+)\s*$',freeze.read_text(),re.M)
check('freeze contains three declared payloads',len(entries)==3)
for expected,name in entries:
    check('frozen '+name,digest(step/name)==expected)
for line in (review/'source_first_hashes.stdout').read_text().splitlines():
    expected,name=line.split('  ',1)
    check('sealed source '+name,digest(root/name)==expected)
check('seal manifest hash',digest(review/'source_first_hashes.stdout')==
    'f33db4ea6bb25ebc090ec83bd7b7cbce443484aa22ee1e24430b0efed9227bec')
check('source first seal hash',digest(review/'SOURCE_FIRST_SEAL.md')==
    'eae600025c2602e6fb704497d7b11f0eab2b6c5f08cd56aebb1fd148baed7a6e')

receipt=json.loads((campaign/'STARTUP_AUDIT.json').read_text())
for suffix in ['json','stdout','stderr','command.txt']:
    digest(campaign/('STARTUP_AUDIT.'+suffix))
check('parent full audit command',receipt['command']==['python3','-B','verify_current_scientific_premises.py'])
check('parent full audit cwd',receipt['cwd']==str(root))
check('parent full audit successful no timeout',receipt['returncode']==0 and receipt['timeout'] is False)
check('parent full audit 358 row statement','PASS: 358-row premise registry' in receipt['stdout'])
check('parent full audit stdout byte correspondence',receipt['stdout'].encode()==(campaign/'STARTUP_AUDIT.stdout').read_bytes())
check('parent full audit stderr byte correspondence',receipt['stderr'].encode()==(campaign/'STARTUP_AUDIT.stderr').read_bytes())
check('parent full audit resource bounds',receipt['address_space_bytes']==2147483648
      and receipt['cpu_seconds']==900 and receipt['wall_seconds']==900
      and receipt['duration_seconds']<900 and receipt['maxrss_kib']*1024<2147483648)
check('registry matches audit declaration',digest(root/'CURRENT_SCIENTIFIC_PREMISES.tsv')==
      '2bb885062dce0f47f7ea37562aee882d5d5d41f25cb539e9dd37755bbe722b63')
check('verifier matches audit declaration',digest(root/'verify_current_scientific_premises.py')==
      '5eac2b421d52b7b45e060332d4b2c2d333e57f177f4103f9c30abf9e28df0540')

git_records=[run_git('rev-parse','HEAD','refs/remotes/origin/grok'),
             run_git('branch','--show-current'),
             run_git('reflog','-3','--date=iso-strict','refs/remotes/origin/grok')]
expected_head='8593f11cd96a575be3513d1ec56e92ac4f5811ff'
check('local HEAD and origin grok match parent',git_records[0]['returncode']==0
      and git_records[0]['stdout'].splitlines()==[expected_head,expected_head])
check('branch grok',git_records[1]['stdout'].strip()=='grok')
fetch=root/'.git/FETCH_HEAD'
fetch_record={'exists':fetch.exists()}
if fetch.exists():
    fetch_record.update({'content':fetch.read_text(),'mtime_ns':fetch.stat().st_mtime_ns,'sha256':digest(fetch)})
    check('FETCH_HEAD contains parent snapshot',expected_head in fetch_record['content'])
digest(campaign/'CAMPAIGN_LOG.md')

for stem in ['author_check_01','author_check_02']:
    for suffix in ['json','stdout','stderr']:
        digest(step/(stem+'.'+suffix))
old=(step/'check_bi1_initial_failed.py').read_text()
new=(step/'check_bi1.py').read_text()
digest(step/'check_bi1_initial_failed.py')
check('only prefreeze scalar iteration repair',old.replace(
    '    if all(s.simplify(x)==0 for x in expr):',
    '    values=list(expr) if isinstance(expr,s.MatrixBase) else [expr]\n'
    '    if all(s.simplify(x)==0 for x in values):')==new)
author=json.loads((step/'author_check_02.stdout').read_text())
check('saved author output code identity',author['source_sha256']==digest(step/'check_bi1.py'))
check('saved author counts/flags',author['status']=='PASS' and len(author['checks'])==67
      and all(item['pass_'] for item in author['checks']) and len(author['fixtures'])==18
      and len(author['hostiles_caught'])==8)

# Exact relevant rows only, after parent audit authentication. Do not dump wide rows.
with (root/'CURRENT_SCIENTIFIC_PREMISES.tsv').open() as f:
    reader=csv.DictReader(f,delimiter='\t')
    columns=reader.fieldnames
    selected=[]
    for row in reader:
        if any(value in {'G310','G312','G315','G330','G332','G337'} for value in row.values()):
            selected.append({key:value for key,value in row.items()
                             if any(token in key.lower() for token in ['id','grade','status','source'])})

out={'checks':checks,'all_pass':all(c['pass'] for c in checks),'hashes':hashes,
     'parent_audit_receipt':receipt,'git_records':git_records,'fetch_record':fetch_record,
     'registry_columns':columns,'selected_registry_fields':selected,
     'limits':['receipt authentication and source-byte correspondence reuse the parent execution; not an independent full358 replay',
               'local refs/FETCH_HEAD and parent campaign log authenticate snapshot consistency; this reviewer did not observe parent network commands live',
               'hashes alone do not prove truth, author independence or chronology']}
print(json.dumps(out,indent=2,sort_keys=True))
raise SystemExit(0 if out['all_pass'] else 1)
