import csv
import hashlib
import io
import json
from pathlib import Path
import subprocess

ROOT=Path('/home/udt-admin/udt_mass_codex')
P=ROOT/'udt_shared_geometry_extension_2026-09-29'
BASE='2187825a5a9077d2078deeecb386632d7ab31018'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def old(path):return subprocess.check_output(['git','show',BASE+':'+path],cwd=ROOT)
freeze=json.loads((P/'INTEGRATION_FREEZE.json').read_text())
initial=json.loads((P/'INTEGRATION_INITIAL_FREEZE.json').read_text())
accepted=freeze['accepted_sha256']
assert len(accepted)==31
for p,h in accepted.items():assert sha(ROOT/p)==h,p
differences=[p for p in accepted if initial['accepted_sha256'][p]!=accepted[p]]
assert differences==['UDT_DEVELOPMENT.md'],differences
oldmaster=old('UDT_DEVELOPMENT.md').decode()
master=(ROOT/'UDT_DEVELOPMENT.md').read_text()
assert '[26 later returns]' in master and '[25 later returns]' not in master
assert (P/'CENTRAL_INSERTION.md').read_text() in master
assert sha(P/'INITIAL_DERIVATION.md')=='7fe9dd385437f927504d90ebe27e70b8751e889efe9140c240a3ee1913aa0484'
assert 'Every use of this U in sections2,4,5 inherits the extension hypothesis.' in (P/'REPAIR.md').read_text()
for path in ['CURRENT_SCIENTIFIC_PREMISES.tsv','CANON.md','verify_current_scientific_premises.py','verify_udt_development.py']:
    assert (ROOT/path).read_bytes()==old(path),path

gp='development_reconstruction_2026-09-29/DEVELOPMENT_GRAPH.json'
graph=json.loads((ROOT/gp).read_text());prior=json.loads(old(gp))
for path,h in prior['sources_sha256'].items():assert graph['sources_sha256'][path]==h,path
nodes={n['id']:n for n in graph['nodes']}
assert 'C_STATIONARY_CLOCKS' in nodes['R8S']['required_conditions']
assert {'from':'C_STATIONARY_CLOCKS','to':'R8S','kind':'hypothesis'} in graph['edges']
for node in ['R8','R18','R8S']:
    assert 'udt_shared_geometry_extension_2026-09-29/REPAIR.md' in nodes[node]['sources']
for rec in graph['review_support']:
    if '/udt_shared_geometry_extension' in '/'+rec['path']:
        assert rec['role']=='review_evidence'
        assert sha(ROOT/rec['path'])==rec['sha256']

dp='development_reconstruction_2026-09-29/CLAIM_DISPOSITIONS.tsv'
newrows=list(csv.DictReader(io.StringIO((ROOT/dp).read_text()),delimiter='\t'))
oldrows=list(csv.DictReader(io.StringIO(old(dp).decode()),delimiter='\t'))
assert len(newrows)==len(oldrows)==406
changes=[(a,b) for a,b in zip(oldrows,newrows) if a!=b]
assert len(changes)==1 and 'G403' in changes[0][0].values()
rp='development_reconstruction_2026-09-29/RECENT_DISPOSITIONS.tsv'
newrecent=list(csv.DictReader(io.StringIO((ROOT/rp).read_text()),delimiter='\t'))
oldrecent=list(csv.DictReader(io.StringIO(old(rp).decode()),delimiter='\t'))
assert len(newrecent)==26 and newrecent[:-1]==oldrecent
assert 'SGE1' in newrecent[-1].values()
assert sha(ROOT/freeze['prior_review_record'])==freeze['prior_review_record_sha256']
for src in json.loads((P/'SOURCE_PINS.json').read_text())['sources']:
    assert sha(ROOT/src['path'])==src['sha256']
print(json.dumps({'status':'PASS','accepted_files':31,'changed_files_since_initial_integration_freeze':differences,
 'registry_rows_unchanged':406,'recent_returns':26,'original_candidate_preserved':True,
 'old_graph_source_versions_preserved':len(prior['sources_sha256']),
 'full_premise_audit_run_here':False,'publication_claimed':False},indent=2))
