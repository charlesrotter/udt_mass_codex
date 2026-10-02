"""ERC1 final byte/scope correspondence; inherited hashes are not recertification."""
from pathlib import Path
import csv,hashlib,json,subprocess

ROOT=Path.cwd()
B=ROOT/'udt_environment_response_candidates_2026-10-01'
freeze_path=B/'INTEGRATION_FREEZE.json'
digest=lambda path:hashlib.file_digest(path.open('rb'),'sha256').hexdigest() if hasattr(hashlib,'file_digest') else stream_digest(path)
def stream_digest(path):
    h=hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda:f.read(1024*1024),b''):h.update(block)
    return h.hexdigest()
assert digest(freeze_path)=='db88a177e9dcc7230c40c8ad10cf120549d6636ff59f3d32795710a0447c7762'
freeze=json.loads(freeze_path.read_text())
accepted=freeze['accepted_sha256']
protected=['udt_native_onshell_timelive_reset_owner_audit_2026-08-10/',
 'udt_pair_regime_flow_reciprocal_orchestra_amplification_2026-08-12/',
 'udt_sne_xmax_G88_am_radial_compatibility_atlas_2026-08-12/',
 'udt_kernel_plane_global_curvature_holonomy_atlas_2026-08-02/']
assert not any(name.startswith(tuple(protected)) for name in accepted)
for name,want in accepted.items():
    path=Path(name)
    assert not path.is_absolute() and '..' not in path.parts
    assert digest(ROOT/path)==want,name
prior=json.loads((B/'PRIOR_REVIEW_RECORD.json').read_text())['accepted_sha256']
assert all(k in accepted for k in prior)
changed=[k for k,v in prior.items() if accepted[k]!=v]
assert sorted(changed)==sorted(freeze['changed_inherited_paths'])
assert len(prior)-len(changed)==freeze['inherited_unchanged_files']==12462
assert len(accepted)-len(prior)==freeze['new_package_files']==196
assert all(k.startswith('udt_environment_response_candidates_2026-10-01/') for k in accepted if k not in prior)
dev=(ROOT/'UDT_DEVELOPMENT.md').read_text()
program=(ROOT/'CURRENT_RESEARCH_PROGRAM.md').read_text()
excerpt=dev.split('<!-- DEVELOPMENT_ORIENTATION_BEGIN -->')[1].split('<!-- DEVELOPMENT_ORIENTATION_END -->')[0]
generated=program.split('<!-- GENERATED_DEVELOPMENT_BEGIN -->')[1].split('<!-- GENERATED_DEVELOPMENT_END -->')[0]
assert excerpt==generated
graph=json.loads((ROOT/'development_reconstruction_2026-09-29/DEVELOPMENT_GRAPH.json').read_text())
nodes={n['id']:n for n in graph['nodes']}
for name in ['C_ERC_RESPONSES','C_ERC_WEAK','C_ERC_EVOLUTION','C_ERC_FLAT_EVENT','R17ERC','R8ERC']:
    assert name in nodes
assert 'UNADOPTED alternatives, not jointly imposed' in nodes['C_ERC_RESPONSES']['statement']
assert 'remain OPEN' in nodes['O_PSW_ATTRIBUTION']['statement']
for name in ['R17ERC','R8ERC']:
    for condition in nodes[name]['required_conditions']:
        assert {'from':condition,'to':name,'kind':'hypothesis'} in graph['edges']
for support in graph['review_support']:
    if support['path'].startswith('udt_environment_response_candidates_2026-10-01/'):
        assert digest(ROOT/support['path'])==support['sha256']
with (ROOT/'development_reconstruction_2026-09-29/RECENT_DISPOSITIONS.tsv').open() as f:
    rows=list(csv.reader(f,delimiter='\t'))
row=[r for r in rows if r[0]=='ERC1_RETURN']
assert len(row)==1 and row[0][-1]==digest(B/'REVIEWED_RESULT.md')
assert 'UNADOPTED_RESPONSE_COMPARISON' in row[0][2]
assert len(rows)-1==46
for name in ['CURRENT_SCIENTIFIC_PREMISES.tsv','CANON.md']:
    assert subprocess.check_output(['git','diff','HEAD','--',name])==b''
for name in ['normal_prebinding','draft_integration']:
    receipt=json.loads((B/'checks'/f'{name}.json').read_text())
    if name=='draft_integration':assert receipt['returncode']==0
    else:assert receipt['returncode']!=0
source_pins=json.loads((B/'SOURCE_PINS.json').read_text())
base=freeze['base_head']
old_central=subprocess.check_output(['git','show',base+':UDT_DEVELOPMENT.md'])
assert hashlib.sha256(old_central).hexdigest()==source_pins['UDT_DEVELOPMENT.md']
summary=json.loads((B/'parent_full/summary.json').read_text())
assert len(summary['cases'])==8 and summary['solve_count']==24
assert all(not lev['domain_stop'] and lev['end']==6 for case in summary['cases'] for lev in case['levels'])
max_tensor=max(case['levels'][2]['residuals'][-1]['original_tensor_normalized'] for case in summary['cases'])
max_constraint=max(r['constraint_normalized'] for case in summary['cases'] for lev in case['levels'] for r in lev['residuals'])
assert max_tensor<7.585e-12 and max_constraint<2.300e-17
own=json.loads((B/'fidelity/direct_02.stdout').read_text())
assert own['maximum_clock_difference']<3.969e-11
assert own['maximum_metric_original_residual']<1.302e-8
out={'status':'PASS','freeze_sha256':digest(freeze_path),'verified_file_count':len(accepted),
 'inherited_unchanged_correspondence_only':freeze['inherited_unchanged_files'],
 'changed_inherited_paths':changed,'new_package_files':freeze['new_package_files'],
 'protected_payloads_read_or_hashed':False,'generated_excerpt_exact':True,
 'registry_and_CANON_unchanged':True,'recent_dispositions':46,
 'parent_tight_maximum_tensor_normalized':max_tensor,'parent_all_maximum_constraint_normalized':max_constraint,
 'scope':'Actual frozen final integration correspondence, not historical recertification or final banking/premise audit'}
print(json.dumps(out,indent=2))
