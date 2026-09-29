"""Version/preservation/receipt checks only; no scientific proof or protected reads."""
from pathlib import Path
import hashlib,json,re,subprocess

root=Path.cwd();w=root/'udt_gr_commitment_audit_2026-09-29'
def h(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def git(*args):
    return subprocess.check_output(['git','-c','core.preloadIndex=false','-c','index.threads=1',
        '-c','core.packedGitWindowSize=16m','-c','core.packedGitLimit=64m',*args])
launch=json.loads((w/'LAUNCH.json').read_text())
assert git('rev-parse','HEAD').decode().strip()==launch['head']
assert git('rev-parse','origin/grok').decode().strip()==launch['origin_grok']
assert git('branch','--show-current').decode().strip()=='grok'
for name in ['CANDIDATE_FREEZE.json','DIRECT_FREEZE.json']:
    for p,d in json.loads((w/name).read_text())['sha256'].items():assert h(root/p)==d,p
for p,d in json.loads((w/'SOURCE_PINS.json').read_text())['sha256'].items():
    current=hashlib.sha256(git('show',launch['head']+':'+p)).hexdigest() if p=='UDT_DEVELOPMENT.md' else h(root/p)
    assert current==d,p
record=json.loads((root/'development_reconstruction_2026-09-29/REVIEW_RECORD.json').read_text())
for p,d in record['accepted_sha256'].items():assert h(root/p)==d,p
for r in record['reviewers']:
    assert h(root/r['attestation'])==r['sha256']
    a=json.loads((root/r['attestation']).read_text())
    assert a['accepted_sha256']==record['accepted_sha256']
    assert h(root/a['report_path'])==a['report_sha256']
names=git('ls-files','--others','--exclude-standard').decode().splitlines()
assert sorted(p for p in names if not p.startswith(w.name+'/'))==sorted(launch['unrelated_untracked_names'])
owned={'UDT_DEVELOPMENT.md','CURRENT_RESEARCH_PROGRAM.md','LIVE.md','HANDOFF.md','UDT_RESEARCH_ROADMAP.md',
 'development_reconstruction_2026-09-29/DEVELOPMENT_GRAPH.json',
 'development_reconstruction_2026-09-29/CLAIM_DISPOSITIONS.tsv',
 'development_reconstruction_2026-09-29/RECENT_DISPOSITIONS.tsv',
 'development_reconstruction_2026-09-29/REVIEW_RECORD.json',
 'development_reconstruction_2026-09-29/checks/test_maintenance.py'}
assert set(git('diff','--name-only',launch['head']).decode().splitlines())==owned
receipts={}
for name in ['comparisons_02','development_final','maintenance_final','premise_final']:
    p=w/'checks'/f'{name}.json';r=json.loads(p.read_text())
    assert r['returncode']==0 and not r['timeout'],name
    receipts[name]={'seconds':r['duration_seconds'],'maxrss_kib':r['maxrss_kib']}
links=[]
for link in re.findall(r'\]\(([^)]+)\)',(root/'UDT_DEVELOPMENT.md').read_text()):
    if link.startswith(('http:','https:','#')):continue
    path=link.split('#')[0];assert (root/path).exists(),path;links.append(path)
files=[p for p in w.rglob('*') if p.is_file() and '__pycache__' not in p.parts]
size=sum(p.stat().st_size for p in files);assert size<20*1024**2
print(json.dumps({'status':'PASS','reviewed_files':len(record['accepted_sha256']),
 'unrelated_names_preserved':len(launch['unrelated_untracked_names']),
 'tracked_owned_changes':len(owned),'central_local_links':len(links),
 'workspace_files':len(files),'workspace_bytes':size,'receipts':receipts,
 'scope':'Byte correspondence, receipts and preservation. No protected payload read, physical promotion or proof claim.'},indent=2))
