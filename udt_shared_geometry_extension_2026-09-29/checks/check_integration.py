"""Final correspondence/preservation check, not a scientific proof."""
import csv
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[2]
WORK=ROOT/'udt_shared_geometry_extension_2026-09-29'
sys.path.insert(0,str(ROOT))
import verify_udt_development as development


def git(*args):
    return subprocess.check_output(['git','-c','core.preloadIndex=false',
                                   '-c','index.threads=1',*args],cwd=ROOT)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


launch=json.loads((WORK/'LAUNCH.json').read_text())
freeze=json.loads((WORK/'INTEGRATION_FREEZE.json').read_text())
for name,expected in freeze['accepted_sha256'].items():
    assert digest(ROOT/name)==expected,name
initial=json.loads((WORK/'CANDIDATE_FREEZE.json').read_text())
for name,expected in initial['sha256'].items():
    assert digest(ROOT/name)==expected,name
for source in json.loads((WORK/'SOURCE_PINS.json').read_text())['sources']:
    assert digest(ROOT/source['path'])==source['sha256'],source['path']
result=development.validate()
assert result['status']=='PASS' and result['registry_rows']==406 and result['later_returns']==26
fixed=['CANON.md','founding.md','CURRENT_SCIENTIFIC_PREMISES.tsv',
       'UDT_METRIC_KERNEL_DEVELOPMENT.md','UDT_METRIC_KERNEL_COVERAGE.tsv',
       'UDT_CONSOLIDATED_RESEARCH_ACCOUNT.md','AGENTS.md','CLAUDE.md',
       'verify_current_scientific_premises.py','verify_udt_development.py']
for name in fixed:
    assert git('show',launch['head']+':'+name)==(ROOT/name).read_bytes(),name
allowed={'UDT_DEVELOPMENT.md','CURRENT_RESEARCH_PROGRAM.md','LIVE.md','HANDOFF.md',
         'UDT_RESEARCH_ROADMAP.md',*(f'development_reconstruction_2026-09-29/{p}' for p in
         ['CLAIM_DISPOSITIONS.tsv','DEVELOPMENT_GRAPH.json','RECENT_DISPOSITIONS.tsv',
          'REVIEW_RECORD.json','checks/test_maintenance.py'])}
assert set(git('diff','--name-only').decode().splitlines())==allowed
untracked=set(filter(None,git('ls-files','--others','--exclude-standard','-z').decode().split('\0')))
prior=set(launch['prior_untracked_names'])
assert prior<=untracked
assert all(p.startswith(WORK.name+'/') for p in untracked-prior)
links=0
for name in ['UDT_DEVELOPMENT.md','UDT_RESEARCH_ROADMAP.md','LIVE.md','HANDOFF.md']:
    for link in re.findall(r'\[[^\]]*\]\(([^)]+)\)',(ROOT/name).read_text()):
        if '://' in link or link.startswith('mailto:'):continue
        path,_,anchor=link.partition('#');dest=ROOT/(path or name)
        assert dest.exists(),(name,link)
        if anchor and dest.name=='UDT_DEVELOPMENT.md':assert f'id="{anchor}"' in dest.read_text(),link
        links+=1
receipts={}
for stem in ['premise_before','premise_after','development_final','maintenance_final']:
    receipt=json.loads((WORK/'checks'/f'{stem}.json').read_text())
    assert receipt['returncode']==0 and not receipt['timeout'],stem
    receipts[stem]=receipt
assert '406-row premise registry' in (WORK/'checks/premise_after.stdout').read_text()
assert not (WORK/'checks/premise_after.stderr').read_bytes()
assert 'Ran 27 tests' in (WORK/'checks/maintenance_final.stderr').read_text()
files=[p for p in WORK.rglob('*') if p.is_file() and '__pycache__' not in p.parts]
assert sum(p.stat().st_size for p in files)<20*1024**2
print(json.dumps({'status':'PASS','development':result,'accepted_files':len(freeze['accepted_sha256']),
      'preserved_initial_files':len(initial['sha256']),'prior_untracked_names':len(prior),
      'protected_payloads_read_or_hashed':False,'fixed_sources_and_validators':fixed,
      'local_links':links,'successful_gate_receipts':list(receipts),
      'workspace_files_at_check':len(files),'workspace_bytes_at_check':sum(p.stat().st_size for p in files)},indent=2))
