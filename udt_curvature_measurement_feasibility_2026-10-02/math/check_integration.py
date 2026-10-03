"""Read-only correspondence checks of CMF1's explicitly supplied final map."""
from pathlib import Path
import hashlib,json,subprocess,sys

root=Path.cwd().resolve()
base=root/'udt_curvature_measurement_feasibility_2026-10-02'
freeze_file=base/'INTEGRATION_FREEZE.json'
freeze=json.loads(freeze_file.read_text())
accepted=freeze['accepted_sha256']
protected=[root/p for p in [
 'udt_native_onshell_timelive_reset_owner_audit_2026-08-10',
 'udt_pair_regime_flow_reciprocal_orchestra_amplification_2026-08-12',
 'udt_sne_xmax_G88_am_radial_compatibility_atlas_2026-08-12',
 'udt_kernel_plane_global_curvature_holonomy_atlas_2026-08-02']]

paths={}
for name in accepted:
    rel=Path(name)
    assert not rel.is_absolute() and '..' not in rel.parts,name
    path=(root/rel).resolve()
    assert path.is_relative_to(root),name
    assert not any(path==p or path.is_relative_to(p) for p in protected),name
    paths[name]=path
# No accepted payload is opened until the entire map passes protected-path checks.
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
changed=[name for name,path in paths.items() if sha(path)!=accepted[name]]
assert not changed,changed

prior_raw=subprocess.check_output(['git','show',freeze['base_head']+':development_reconstruction_2026-09-29/REVIEW_RECORD.json'])
prior=json.loads(prior_raw)['accepted_sha256']
assert len(prior)==freeze['inherited_count']
assert prior.keys()<=accepted.keys()
changed_inherited=sorted(p for p,v in prior.items() if accepted[p]!=v)
assert changed_inherited==sorted(freeze['changed_inherited'])
new=sorted(accepted.keys()-prior.keys())
assert all(p.startswith('udt_curvature_measurement_feasibility_2026-10-02/') for p in new)
for name in ['CURRENT_SCIENTIFIC_PREMISES.tsv','CANON.md']:
    old=subprocess.check_output(['git','show',freeze['base_head']+':'+name])
    assert (root/name).read_bytes()==old,name
source_seal=json.loads((base/'math/SOURCE_FIRST_SEAL.json').read_text())
assert all(sha(root/name)==digest for name,digest in source_seal['source_first_files'].items())

# Use the existing audited pure formatter, no regeneration or mutation.
sys.path.insert(0,str(root))
from verify_udt_development import program_text
assert (root/'CURRENT_RESEARCH_PROGRAM.md').read_text()==program_text((root/'UDT_DEVELOPMENT.md').read_text())
graph=json.loads((root/'development_reconstruction_2026-09-29/DEVELOPMENT_GRAPH.json').read_text())
nodes={n['id']:n for n in graph['nodes']}
for node,anchor in [('R8CMF','r8cmf'),('R17CMF','r17cmf')]:
    assert nodes[node]['anchor']==anchor
    assert f'<a id="{anchor}"></a>' in (root/'UDT_DEVELOPMENT.md').read_text()
for path,digest in graph['sources_sha256'].items():
    if path.startswith('udt_curvature_measurement_feasibility_2026-10-02/'):
        assert accepted[path]==digest
for item in graph['review_support']:
    if item['path'].startswith('udt_curvature_measurement_feasibility_2026-10-02/'):
        assert accepted[item['path']]==item['sha256']

result={
 'status':'PASS_FINAL_MAP_CORRESPONDENCE_NOT_FULL_CORPUS_REPROOF',
 'freeze_sha256':sha(freeze_file),'accepted_count':len(accepted),
 'inherited_count':len(prior),'new_count':len(new),
 'changed_inherited':changed_inherited,
 'all_current_hashes_match':True,'protected_payloads_opened':False,
 'canonical_and_exact_registry_bytes_unchanged':True,
 'source_first_seal_unchanged':True,'generated_program_matches':True,
 'new_graph_anchors_source_and_review_pins_match':True,
 'scope':'Actual semantic review separately covers six changed inherited files and load-bearing new result/support documents. Unchanged inherited map retained by byte correspondence; not reread/reproved.'
}
with (base/'math/INTEGRATION_CHECK.json').open('x') as f:
    json.dump(result,f,indent=2);f.write('\n')
print(json.dumps(result,indent=2))
