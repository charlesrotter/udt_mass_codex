"""LKT1 final evidence correspondence; not a mathematical proof."""
import csv
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[2]
WORK=ROOT/'udt_lorentz_kernel_transport_2026-09-29'
sys.path.insert(0,str(ROOT))
import verify_udt_development as development

def git(*args):
    return subprocess.check_output(['git','-c','core.preloadIndex=false',
                                   '-c','index.threads=1','-c','core.packedGitWindowSize=16m',
                                   '-c','core.packedGitLimit=64m',*args],cwd=ROOT)
def sha(data):return hashlib.sha256(data).hexdigest()
launch=json.loads((WORK/'LAUNCH.json').read_text())
freeze=json.loads((WORK/'INTEGRATION_FREEZE.json').read_text())['accepted_sha256']
for name,h in freeze.items():assert sha((ROOT/name).read_bytes())==h,name
initial=json.loads((WORK/'CANDIDATE_FREEZE.json').read_text())['sha256']
for name,h in initial.items():assert sha((ROOT/name).read_bytes())==h,name
sources=json.loads((WORK/'SOURCE_PINS.json').read_text())['sources']
for src in sources:
    old=git('show',launch['head']+':'+src['path'])
    assert sha(old)==src['sha256'],src['path']
    if src['path']!='UDT_DEVELOPMENT.md':assert (ROOT/src['path']).read_bytes()==old,src['path']
for name in ['CANON.md','verify_udt_development.py','verify_current_scientific_premises.py',
             'UDT_METRIC_KERNEL_DEVELOPMENT.md','UDT_METRIC_KERNEL_COVERAGE.tsv',
             'UDT_CONSOLIDATED_RESEARCH_ACCOUNT.md']:
    assert (ROOT/name).read_bytes()==git('show',launch['head']+':'+name),name
oldrecord='development_reconstruction_2026-09-29/REVIEW_RECORD.json'
assert (WORK/'PREVIOUS_REVIEW_RECORD.json').read_bytes()==git('show',launch['head']+':'+oldrecord)
allowed={'UDT_DEVELOPMENT.md','CURRENT_RESEARCH_PROGRAM.md','LIVE.md','HANDOFF.md',
         'UDT_RESEARCH_ROADMAP.md',*(f'development_reconstruction_2026-09-29/{p}' for p in
         ['CLAIM_DISPOSITIONS.tsv','DEVELOPMENT_GRAPH.json','RECENT_DISPOSITIONS.tsv',
          'REVIEW_RECORD.json','checks/test_maintenance.py'])}
assert set(git('diff','--name-only').decode().splitlines())==allowed
untracked=set(filter(None,git('ls-files','--others','--exclude-standard','-z').decode().split('\0')))
prior=set(launch['prior_untracked_names'])
assert prior<=untracked and all(p.startswith(WORK.name+'/') for p in untracked-prior)
result=development.validate()
assert result['status']=='PASS' and result['registry_rows']==406 and result['later_returns']==27
links=0
for name in ['UDT_DEVELOPMENT.md','UDT_RESEARCH_ROADMAP.md','LIVE.md','HANDOFF.md']:
    for link in re.findall(r'\[[^\]]*\]\(([^)]+)\)',(ROOT/name).read_text()):
        if '://' in link or link.startswith('mailto:'):continue
        path,_,anchor=link.partition('#');target=ROOT/(path or name)
        assert target.exists(),(name,link)
        if anchor and target.name=='UDT_DEVELOPMENT.md':assert f'id="{anchor}"' in target.read_text(),link
        links+=1
for stem in ['development_before','development_final','maintenance_final','premise_after']:
    r=json.loads((WORK/'checks'/f'{stem}.json').read_text())
    assert r['returncode']==0 and not r['timeout'],stem
assert '406-row premise registry' in (WORK/'checks/premise_after.stdout').read_text()
assert not (WORK/'checks/premise_after.stderr').read_bytes()
assert 'Ran 31 tests' in (WORK/'checks/maintenance_final.stderr').read_text()
files=[p for p in WORK.rglob('*') if p.is_file() and '__pycache__' not in p.parts]
size=sum(p.stat().st_size for p in files);assert size<20*1024**2
print(json.dumps({'status':'PASS','development':result,'reviewed_files':len(freeze),
  'original_candidate_files':len(initial),'source_versions':len(sources),
  'prior_untracked_names':len(prior),'protected_payloads_read':False,
  'links_checked':links,'workspace_files':len(files),'workspace_bytes':size},indent=2))
