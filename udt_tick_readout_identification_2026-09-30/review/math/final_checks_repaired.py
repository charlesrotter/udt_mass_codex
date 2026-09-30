from pathlib import Path
import hashlib,json,subprocess,sys
root=Path(__file__).resolve().parents[3]
package=root/'udt_tick_readout_identification_2026-09-30'
freeze_path=package/'INTEGRATION_FREEZE.json'
expected_freeze='f535c993d4e27dc0cd13aa01ee3c3fc287beba972d416e3b02f553c7c0e414ca'
assert hashlib.sha256(freeze_path.read_bytes()).hexdigest()==expected_freeze
freeze=json.loads(freeze_path.read_text()); bindings=freeze['accepted_sha256']
protected=['udt_native_onshell_timelive_reset_owner_audit_2026-08-10/','udt_pair_regime_flow_reciprocal_orchestra_amplification_2026-08-12/','udt_sne_xmax_G88_am_radial_compatibility_atlas_2026-08-12/','udt_kernel_plane_global_curvature_holonomy_atlas_2026-08-02/']
for name in bindings:
    assert not any(name.startswith(p) for p in protected),name
    path=Path(name)
    assert not path.is_absolute() and '..' not in path.parts,name
    target=(root/path).resolve()
    relative=str(target.relative_to(root))
    assert relative==name and not any(relative.startswith(p) for p in protected),name
for name,digest in bindings.items():
    assert hashlib.sha256((root/name).read_bytes()).hexdigest()==digest,name
prior=json.loads((package/'PREVIOUS_REVIEW_RECORD.json').read_text())['accepted_sha256']
changed=sorted(k for k in prior if prior[k]!=bindings[k])
unchanged=[k for k in prior if prior[k]==bindings[k]]
new=sorted(set(bindings)-set(prior))
assert (len(bindings),len(prior),len(changed),len(unchanged),len(new))==(332,261,8,253,71)
assert changed==sorted(freeze['changed_previous_paths'])
diff=subprocess.check_output(['git','-c','core.preloadIndex=false','-c','index.threads=1','diff','--name-only'],cwd=root,text=True).splitlines()
assert sorted(diff)==changed,(diff,changed)
gpath='development_reconstruction_2026-09-29/DEVELOPMENT_GRAPH.json'
g=json.loads((root/gpath).read_text())
old=json.loads(subprocess.check_output(['git','show',freeze['parent_head']+':'+gpath],cwd=root,text=True))
oldnodes={n['id']:n for n in old['nodes']}; nodes={n['id']:n for n in g['nodes']}
assert all(nodes[k]==v for k,v in oldnodes.items())
assert set(nodes)-set(oldnodes)=={'C_TRI_COUNTS','R6N','R6T'}
assert all(e in g['edges'] for e in old['edges'])
assert all(g['sources_sha256'][k]==v for k,v in old['sources_sha256'].items())
triroot='udt_tick_readout_identification_2026-09-30/'
new_sources=set(g['sources_sha256'])-set(old['sources_sha256'])
assert new_sources=={triroot+n for n in ['INITIAL_CANDIDATE.md','REPAIR.md','REVIEWED_RESULT.md']}
for n in new_sources:
    assert g['sources_sha256'][n]==bindings[n]
seed={n['id'] for n in g['nodes'] if new_sources & set(n.get('sources',[]))}
reach=set(seed)
while True:
    nxt=reach|{e['to'] for e in g['edges'] if e['from'] in reach}
    if nxt==reach:break
    reach=nxt
assert {'R6N','R6T','R18O','R18F','R18B','R18'}<=reach
assert not {'R6','R7','R9','R18T','R18C','R18U'}&reach
for a,b in [('P_NULL','R6N'),('M_GEOMETRY','R6N'),('P_NULL','R6T'),('M_GEOMETRY','R6T'),('C_TRI_COUNTS','R6T')]:
    assert {'from':a,'to':b,'kind':'hypothesis'} in g['edges']
master=(root/'UDT_DEVELOPMENT.md').read_text()
orientation=master.split('<!-- DEVELOPMENT_ORIENTATION_BEGIN -->',1)[1].split('<!-- DEVELOPMENT_ORIENTATION_END -->',1)[0].strip()
program=(root/'CURRENT_RESEARCH_PROGRAM.md').read_text().split('<!-- GENERATED_DEVELOPMENT_BEGIN -->',1)[1].split('<!-- GENERATED_DEVELOPMENT_END -->',1)[0].strip()
assert orientation==program
assert 'almost everywhere' in master and 'sum active channels' in master and 'separately supplied continuous measure' in master
print(json.dumps({'status':'PASS','freeze_sha256':expected_freeze,'bindings_verified':len(bindings),'protected_prefixes_rejected_before_hashing':protected,'prior_paths':len(prior),'changed_prior':changed,'inherited_unchanged':len(unchanged),'new_paths':len(new),'new_graph_nodes':sorted(set(nodes)-set(oldnodes)),'tri_source_descendants':sorted(reach),'unchanged_existing_graph_nodes':len(oldnodes),'new_source_count':len(new_sources),'generated_orientation_identical':True,'scope':'Byte/routing/regression correspondence; inherited corpus not re-proved.'},indent=2))
