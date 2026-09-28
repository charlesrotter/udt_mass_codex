"""Editorial correspondence only. Reuse existing startup validation, not scientific proof.

Initial stdin invocation used plain git diff --check at the last step and hit
Git threaded-lstat failure under the 512MiB cap. This saved version applies the
same Git thread controls already used by every other subprocess. See retained
validation.stderr. No documentation or scientific change repairs that failure.
"""
from pathlib import Path
import hashlib,json,re,subprocess,sys
ROOT=Path.cwd()
sys.path.insert(0,str(ROOT))
from verify_current_scientific_premises import validate_startup_surface
P=ROOT/'udt_repository_cleanup_2026-09-27/trajectory_checkpoint_2026-09-28'
launch=json.loads((P/'LAUNCH.json').read_text())
def git(*a):
    return subprocess.check_output(['git','-c','core.preloadIndex=false','-c','index.threads=1',*a],text=True)
assert git('branch','--show-current').strip()=='grok'
assert git('rev-parse','HEAD').strip()==launch['head']==git('rev-parse','origin/grok').strip()
assert not git('diff','--cached','--name-only').strip()
assert set(git('diff','--name-only').splitlines())==set(launch['scope_files'])
for name,h in launch['source_sha256'].items():
    assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==h,name
old=git('show',launch['head']+':CURRENT_RESEARCH_PROGRAM.md')
now=(ROOT/'CURRENT_RESEARCH_PROGRAM.md').read_text()
assert old.split('## Current next gate\n')[0]==now.split('## Current next gate\n')[0]
assert old.split('## Architecture\n')[1]==now.split('## Architecture\n')[1]
oldroad=git('show',launch['head']+':UDT_RESEARCH_ROADMAP.md')
newroad=(ROOT/'UDT_RESEARCH_ROADMAP.md').read_text()
a='## Accepted calibration inputs'; b='## Other branches and reusable work'
assert oldroad[oldroad.index(a):oldroad.index(b)]==newroad[newroad.index(a):newroad.index(b)]
assert [s for s in oldroad.splitlines() if s.startswith('>')]==[s for s in newroad.splitlines() if s.startswith('>')]
prior=[n for n in git('ls-files','--others','--exclude-standard').splitlines() if not n.startswith(str(P.relative_to(ROOT))+'/')]
assert sorted(prior)==sorted(launch['prior_untracked_paths'])
# Reuse the full audit only with unchanged earlier scientific/registry inputs.
changes=git('diff','--name-only','50cd10b21218a4a8ae68f4ccb61794afd1cfea03',launch['head']).splitlines()
assert all(n in launch['scope_files'] or n.startswith('udt_interframe_clock_network_2026-09-28/') for n in changes)
auditdir=ROOT/'udt_interframe_clock_network_2026-09-28/checks'
audit=json.loads((auditdir/'premise_audit.json').read_text())
assert audit['returncode']==0 and not audit['timeout']
assert 'PASS: 406-row premise registry' in (auditdir/'premise_audit.stdout').read_text()
assert not (auditdir/'premise_audit.stderr').read_text()
links=0
for name in launch['scope_files']:
    for target in re.findall(r'\[[^\]\n]+\]\(([^)]+)\)',(ROOT/name).read_text()):
        if '://' in target: continue
        path,sep,anchor=target.partition('#')
        dest=(ROOT/name).parent/path if path else ROOT/name
        assert dest.exists(),(name,target)
        if anchor:
            heads=re.findall(r'^#+\s+(.+?)\s*$',dest.read_text(),re.M)
            slugs={re.sub(r'[^\w\- ]','',h.lower()).replace(' ','-') for h in heads}
            assert anchor in slugs,(name,target)
        links+=1
validate_startup_surface(ROOT)
git('diff','--check')
print(json.dumps({'status':'PASS','scope':'documentation correspondence and same-code startup regression only','head':launch['head'],'source_pins':len(launch['source_sha256']),'root_docs':len(launch['scope_files']),'local_links_checked':links,'prior_untracked_paths':len(prior),'founding_opening':'byte-preserved','architecture_and_later_program':'byte-preserved','roadmap_owner_direction_sections':'byte-preserved','full_premise_audit':'prior ICN1 exit0,405.819s; reuse with unchanged scientific inputs; not rerun','startup_guard':'PASS after edits','tracked_edits_outside_scope':False,'python':sys.version},indent=2))
