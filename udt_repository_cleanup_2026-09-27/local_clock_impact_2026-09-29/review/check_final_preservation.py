"""One-off LCIA1 reviewer byte/navigation audit; no scientific-proof claim."""
from pathlib import Path
import csv
import hashlib
import json
import re
import subprocess

root=Path.cwd()
p=root/'udt_repository_cleanup_2026-09-27/local_clock_impact_2026-09-29'
j=json.loads((p/'LAUNCH.json').read_text())
def git(*args):
    return subprocess.check_output(['git','-c','core.preloadIndex=false','-c','index.threads=1',*args],cwd=root)
def sha(b): return hashlib.sha256(b).hexdigest()
assert git('branch','--show-current').decode().strip()=='grok'
assert git('rev-parse','HEAD').decode().strip()==j['head']
rows=list(csv.DictReader((p/'NOTICE_LEDGER.tsv').open(),delimiter='\t'))
assert len(rows)==10 and {r['package'] for r in rows}==set(j['packages'])
briefs={r['path'] for r in rows}
for r in rows:
    path=r['path']; old=git('show',j['head']+':'+path); now=(root/path).read_bytes()
    n=int(r['prefix_bytes']); prefix=now[:n]
    assert old==now[n:],path
    assert sha(old)==r['original_body_sha256']==j['package_baseline_sha256'][path]
    assert sha(prefix)==r['notice_sha256'] and sha(now)==r['current_sha256']
    assert prefix.count(b'LCIA1_CURRENT_USE_BEGIN')==1
    assert prefix.count(b'LCIA1_CURRENT_USE_END')==1
    assert r['baseline_commit']==j['head']
unchanged=[]
for f,h in j['package_baseline_sha256'].items():
    if f not in briefs:
        assert sha((root/f).read_bytes())==h,f
        unchanged.append(f)
for f,h in j['source_pins'].items(): assert sha((root/f).read_bytes())==h,f
freeze=json.loads((p/'CANDIDATE_FREEZE.json').read_text())
for f,h in freeze['sha256'].items(): assert sha((p/f).read_bytes())==h,f
seal=json.loads((p/'review/SOURCE_FIRST_SEAL.json').read_text())
for f,h in seal['sha256'].items(): assert sha((p/'review'/f).read_bytes())==h,f
expected=briefs|set(j['maintained_pointers'])
actual=set(git('diff','HEAD','--name-only').decode().splitlines())
assert actual==expected,(actual-expected,expected-actual)
git('diff','--check')
now_untracked=set(git('ls-files','--others','--exclude-standard').decode().splitlines())
assert set(j['prior_untracked_names'])<=now_untracked
# Check local Markdown destinations in changed pointers, prefixes and final packet.
# Old preserved brief bodies may retain historical navigation; inspect new prefixes.
documents={f:(root/f).read_text() for f in j['maintained_pointers']}
documents.update({r['path']:(root/r['path']).read_bytes()[:int(r['prefix_bytes'])].decode() for r in rows})
names=['REVIEWED_AUDIT.md','DECISION_BRIEF.md','REPAIR_1.md','OWNER_CONCERN.md','CLOSEOUT.md']
documents.update({str((p/n).relative_to(root)):(p/n).read_text() for n in names})
checked=[]
for f,t in documents.items():
    for target in re.findall(r'\[[^\]]*\]\(([^)\s]+)\)',t):
        if '://' in target or target.startswith('#'): continue
        path=target.split('#')[0]
        if not path: continue
        dest=(root/f).parent/path
        assert dest.exists(),(f,target)
        checked.append([f,target])
pins={f:sha((root/f).read_bytes()) for f in sorted(expected)}
pins.update({str((p/n).relative_to(root)):sha((p/n).read_bytes()) for n in names})
pins[str((p/'NOTICE_LEDGER.tsv').relative_to(root))]=sha((p/'NOTICE_LEDGER.tsv').read_bytes())
print(json.dumps({'status':'PASS','scope':'byte correspondence and local-link existence, not science or whole-link completeness','head':j['head'],'ten_original_brief_bodies_preserved':len(rows),'other_unchanged_package_files':len(unchanged),'unchanged_authority_pins':len(j['source_pins']),'preserved_prior_untracked_names':len(j['prior_untracked_names']),'exact_tracked_change_count':len(actual),'local_links_checked':len(checked),'candidate_and_source_first_freezes_unchanged':True,'protected_payloads_read_or_hashed':False,'final_document_pins':pins},indent=2))
