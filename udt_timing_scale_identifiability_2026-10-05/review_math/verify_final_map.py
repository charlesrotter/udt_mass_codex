"""Final scoped version audit; hashes establish correspondence, not truth."""
from pathlib import Path
import hashlib,json,subprocess,datetime
P=Path(__file__).resolve().parent
root=Path.cwd().resolve()
fpath=P.parent/'INTEGRATION_FREEZE.json'
expected='32328dad8868ebc2726ae3df0745f87b4f94c9d5bd21e700c063d960edfb21f6'
blocked=('udt_kernel_plane_global_curvature_holonomy_atlas_2026-08-02/',
'udt_native_onshell_timelive_reset_owner_audit_2026-08-10/',
'udt_pair_regime_flow_reciprocal_orchestra_amplification_2026-08-12/',
'udt_sne_xmax_G88_am_radial_compatibility_atlas_2026-08-12/')
def sha(p):
    h=hashlib.sha256()
    with Path(p).open('rb') as f:
        for chunk in iter(lambda:f.read(1048576),b''):h.update(chunk)
    return h.hexdigest()
assert sha(fpath)==expected
freeze=json.loads(fpath.read_text());accepted=freeze['accepted_sha256']
assert len(accepted)==14446
assert not any(p.startswith(blocked) for p in accepted)
failures=[]
for p,d in accepted.items():
    path=Path(p)
    assert not path.is_absolute() and '..' not in path.parts
    resolved=path.resolve().relative_to(root).as_posix()
    assert not resolved.startswith(blocked)
    if not path.is_file() or sha(path)!=d:failures.append(p)
assert not failures,failures
prior=json.loads((P.parent/'PRIOR_REVIEW_RECORD.json').read_text())['accepted_sha256']
changed=[p for p,d in prior.items() if accepted[p]!=d]
assert set(changed)==set(freeze['changed_inherited']) and len(changed)==6
assert len(prior)==14377
assert subprocess.check_output(['git','branch','--show-current']).decode().strip()=='grok'
assert subprocess.check_output(['git','rev-parse','HEAD']).decode().strip()==freeze['base_head']
graph=json.loads(Path('development_reconstruction_2026-09-29/DEVELOPMENT_GRAPH.json').read_text())
nodes={n['id']:n for n in graph['nodes']}
assert nodes['R16TSI']['required_conditions']==['C_TSI_HISTORY','C_TSI_RECORD']
assert nodes['O_TSI_ADMISSION']['kind']=='open_join'
for e in graph['edges']:
    if e['from']=='O_TSI_ADMISSION':assert e['kind']=='open_boundary'
assert all(accepted[p]==d for p,d in graph['sources_sha256'].items() if p.startswith('udt_timing_scale_identifiability_2026-10-05/'))
for name in ['construction','draft','final_maintenance']:
    prefix=P.parent/'checks'/name
    meta=json.loads(Path(str(prefix)+'.json').read_text())
    assert meta['returncode']==0
    for ext in ['stdout','stderr']:
        assert sha(str(prefix)+'.'+ext)==meta[ext+'_sha256']
result={'status':'PASS','created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
'freeze_sha256':expected,'accepted_map_entries_checked':len(accepted),'changed_inherited':changed,
'protected_map_entries':0,'inherited_binding_only_not_full_semantic_reproof':len(prior)-len(changed),
'base_head':freeze['base_head'],'checks_inspected':['construction','draft','final_maintenance'],
'pending_parent_banking_gates':['actual final review binding','final_normal_bound','final_premises_windowed','manifest/stage/commit/push/remote verification']}
out=P/'FINAL_MAP_CHECK.json';assert not out.exists();out.write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
