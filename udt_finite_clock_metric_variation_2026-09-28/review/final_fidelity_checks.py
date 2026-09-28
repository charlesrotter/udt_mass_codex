"""Final source/pointer/preservation correspondence only; no scientific replay."""
import csv
import hashlib
import json
import pathlib
import subprocess

root=pathlib.Path.cwd()
pkg=root/'udt_finite_clock_metric_variation_2026-09-28'
maintained={'LIVE.md','HANDOFF.md','CURRENT_RESEARCH_PROGRAM.md','MEMORY.md','INDEX.md','UDT_RESEARCH_ROADMAP.md'}
launch=json.loads((pkg/'LAUNCH.json').read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def git(*args):
    return subprocess.check_output(['git','-c','core.preloadIndex=false','-c','index.threads=1',*args],text=True)
unchanged={p:sha(root/p)==h for p,h in launch['source_pins'].items() if p not in maintained}
assert all(unchanged.values()),unchanged
assert git('branch','--show-current').strip()=='grok'
assert git('rev-parse','HEAD').strip()==launch['head']
assert git('rev-parse','origin/grok').strip()==launch['origin_grok']
assert set(git('diff','--name-only').splitlines())==maintained
assert not git('diff','--cached','--name-only').strip()
assert not git('diff','--check')
untracked=set(git('ls-files','--others','--exclude-standard').splitlines())
unrelated={p for p in untracked if not p.startswith(pkg.name+'/')}
assert unrelated==set(launch['prior_untracked_paths'])
# Path listing only for protected/unrelated data. No content reads or hashes.
with (root/'CURRENT_SCIENTIFIC_PREMISES.tsv').open() as f:
    rows={r['premise_id']:r for r in csv.DictReader(f,delimiter='\t')}
assert len(rows)==406
selected=json.loads((pkg/'SCOPED_REGISTRY.json').read_text())
assert all(rows[r['premise_id']]==r for r in selected)
before=git('show',launch['head']+':CURRENT_RESEARCH_PROGRAM.md').split('## Current next gate')[0]
assert before==(root/'CURRENT_RESEARCH_PROGRAM.md').read_text().split('## Current next gate')[0]
freeze=json.loads((pkg/'CANDIDATE_FREEZE.json').read_text())
assert all(sha(pkg/p)==h for p,h in freeze['candidate_and_checks'].items())
for name in ['SOURCE_FIRST_SEAL','DIRECT_INDEPENDENT_SEAL','DIRECT_REVIEW_SEAL']:
    seal=json.loads((pkg/'review'/(name+'.json')).read_text())
    assert all(sha(root/p)==h for p,h in seal['files'].items()),name
receipts={}
for name in ['premise_audit','startup_surface','preservation']:
    rec=json.loads((pkg/'checks'/(name+'.json')).read_text())
    assert rec['returncode']==0 and not rec['timeout']
    assert (pkg/'checks'/(name+'.stderr')).read_bytes()==b''
    assert 'PASS' in (pkg/'checks'/(name+'.stdout')).read_text()
    receipts[name]=rec
assert '406-row premise registry' in (pkg/'checks/premise_audit.stdout').read_text()
assert receipts['premise_audit']['cpu_seconds']==900
assert receipts['premise_audit']['address_space_bytes']==2*1024**3
assert receipts['premise_audit']['maxrss_kib']==120384
import sys
sys.path.insert(0,str(root))
from verify_current_scientific_premises import validate_startup_surface
validate_startup_surface(root)
print(json.dumps(dict(status='PASS',evidence='final fidelity correspondence and existing startup-guard regression only',
    sources_unchanged=unchanged,protected_unrelated_paths_present=len(unrelated),protected_payloads_read=False,
    maintained_pointers=sorted(maintained),registry_rows=406,selected_rows=len(selected),candidate_pins=len(freeze['candidate_and_checks']),
    review_seals_unchanged=3,founding_opening_unchanged=True,premise_receipt_exit=receipts['premise_audit']['returncode'],
    premise_receipt_seconds=receipts['premise_audit']['duration_seconds'],startup_surface_replayed=True),indent=2))
