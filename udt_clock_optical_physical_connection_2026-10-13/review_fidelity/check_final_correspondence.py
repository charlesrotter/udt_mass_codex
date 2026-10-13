"""Streaming hash correspondence and narrow independent packaging checks."""
import datetime
import hashlib
import json
from pathlib import Path
import platform

HERE=Path(__file__).resolve().parent
PKG=HERE.parent
REPO=PKG.parent
protected=('udt_native_onshell_timelive_reset_owner_audit_2026-08-10',
 'udt_pair_regime_flow_reciprocal_orchestra_amplification_2026-08-12',
 'udt_sne_xmax_G88_am_radial_compatibility_atlas_2026-08-12',
 'udt_kernel_plane_global_curvature_holonomy_atlas_2026-08-02')

def sha(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for chunk in iter(lambda:f.read(1024*1024),b''): h.update(chunk)
    return h.hexdigest()

fpath=PKG/'INTEGRATION_FREEZE.json'
freeze=json.loads(fpath.read_text())
accepted=freeze['accepted_sha256']
prior=json.loads((PKG/'PRIOR_REVIEW_RECORD.json').read_text())['accepted_sha256']
assert len(accepted)==14864
new=sorted(set(accepted)-set(prior))
changed=sorted(p for p in prior if p in accepted and prior[p]!=accepted[p])
assert set(prior)<=set(accepted)
assert new==sorted(freeze['new_files']) and len(new)==67
assert changed==sorted(freeze['changed_prior_files']) and len(changed)==8

# Guard all names before any accepted-payload opening.
for name in accepted:
    rel=Path(name)
    assert not rel.is_absolute() and '..' not in rel.parts,name
    assert rel.parts[0] not in protected,name
    resolved=(REPO/rel).resolve()
    assert resolved.is_relative_to(REPO),name
    assert resolved.relative_to(REPO).parts[0] not in protected,name

for name,wanted in accepted.items():
    assert sha(REPO/name)==wanted,name
candidate=json.loads((PKG/'CANDIDATE_FREEZE.json').read_text())['sha256']
for name,wanted in candidate.items(): assert sha(REPO/name)==wanted,name

central=(REPO/'UDT_DEVELOPMENT.md').read_text()
program=(REPO/'CURRENT_RESEARCH_PROGRAM.md').read_text()
block=central.split('<!-- DEVELOPMENT_ORIENTATION_BEGIN -->',1)[1].split('<!-- DEVELOPMENT_ORIENTATION_END -->',1)[0].strip()
pblock=program.split('<!-- GENERATED_DEVELOPMENT_BEGIN -->',1)[1].split('<!-- GENERATED_DEVELOPMENT_END -->',1)[0].strip()
assert block==pblock
graph=json.loads((REPO/'development_reconstruction_2026-09-29/DEVELOPMENT_GRAPH.json').read_text())
nodes={n['id']:n for n in graph['nodes']}
for name,kind in [('C_COC_QUERY','condition'),('C_COC_TRIALS','condition'),
                  ('O_COC_ATTRIBUTION','open_join'),('R8COC','argument')]:
    assert nodes[name]['kind']==kind
assert 'Not a conjunction' in nodes['C_COC_TRIALS']['statement']
assert set(nodes['R8COC']['required_conditions'])=={'C_COC_QUERY','C_COC_TRIALS'}
assert {'from':'O_COC_ATTRIBUTION','to':'R8COC','kind':'open_boundary'} in graph['edges']
support=graph['review_support']
coc_support=[r for r in support if r['path'].startswith(PKG.name+'/')]
for r in coc_support: assert sha(REPO/r['path'])==r['sha256'],r['path']
recent=(REPO/'development_reconstruction_2026-09-29/RECENT_DISPOSITIONS.tsv').read_text()
row=[r for r in recent.splitlines() if r.startswith('COC1_RETURN\t')]
assert len(row)==1
assert 'REPAIRED_CONDITIONAL' in row[0] and 'UNADOPTED' in row[0]
assert candidate[PKG.name+'/INITIAL_CANDIDATE.md'] in row[0]

print(json.dumps({'status':'PASS','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'python':platform.python_version(),'accepted_files_checked':len(accepted),'prior_files':len(prior),
 'new_files':len(new),'changed_prior_files':changed,'initial_candidate_files_checked':len(candidate),
 'protected_payloads_opened':False,'generated_orientation_equal':True,
 'coc_review_support_pins_checked':len(coc_support),'freeze_sha256':sha(fpath),
 'plan_sha256':sha(HERE/'FINAL_CHECK_PLAN.md'),'script_sha256':sha(Path(__file__)),
 'omissions':['No semantic reproof of inherited corpus','No pending normal/57/full406 checks',
              'No publication or empirical/premise/canon approval']},indent=2))
