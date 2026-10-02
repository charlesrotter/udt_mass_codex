"""Exposed final correspondence check, streaming files and excluding protected paths."""
import hashlib,json,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent
freeze_path=ROOT/'INTEGRATION_FREEZE.json'
freeze=json.loads(freeze_path.read_text())
assert hashlib.sha256(freeze_path.read_bytes()).hexdigest()=='db88a177e9dcc7230c40c8ad10cf120549d6636ff59f3d32795710a0447c7762'
protected=['udt_kernel_plane_global_curvature_holonomy_atlas_2026-08-02/',
'udt_native_onshell_timelive_reset_owner_audit_2026-08-10/',
'udt_pair_regime_flow_reciprocal_orchestra_amplification_2026-08-12/',
'udt_sne_xmax_G88_am_radial_compatibility_atlas_2026-08-12/']
accepted=freeze['accepted_sha256']
assert not any(any(k.startswith(p) for p in protected) for k in accepted)
def digest(path):
    h=hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda:f.read(1024*1024),b''):h.update(block)
    return h.hexdigest()
bad=[];count=0;bytes_checked=0
for name,wanted in accepted.items():
    p=Path(name)
    if not p.is_file():bad.append((name,'missing'));continue
    got=digest(p)
    if got!=wanted:bad.append((name,got,wanted))
    count+=1;bytes_checked+=p.stat().st_size
assert not bad,bad
prior=json.loads((ROOT/'PRIOR_REVIEW_RECORD.json').read_text())['accepted_sha256']
assert set(prior)<=set(accepted)
changed=[p for p in prior if prior[p]!=accepted[p]]
assert sorted(changed)==sorted(freeze['changed_inherited_paths'])
assert len(prior)-len(changed)==freeze['inherited_unchanged_files']
newfiles=set(accepted)-set(prior)
assert len(newfiles)==freeze['new_package_files']
assert all(p.startswith(ROOT.name+'/') for p in newfiles)
base=freeze['base_head']
head=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()
branch=subprocess.check_output(['git','branch','--show-current'],text=True).strip()
assert head==base and branch=='grok'
graph_path='development_reconstruction_2026-09-29/DEVELOPMENT_GRAPH.json'
old=json.loads(subprocess.check_output(['git','show',base+':'+graph_path],text=True))
new=json.loads(Path(graph_path).read_text())
old_nodes={n['id']:n for n in old['nodes']};new_nodes={n['id']:n for n in new['nodes']}
assert set(old_nodes)<=set(new_nodes)
node_additions=sorted(set(new_nodes)-set(old_nodes))
assert node_additions==sorted(['C_ERC_RESPONSES','C_ERC_WEAK','C_ERC_EVOLUTION','C_ERC_FLAT_EVENT','R17ERC','R8ERC'])
assert all(edge in new['edges'] for edge in old['edges'])
assert all(new['sources_sha256'][p]==h for p,h in old['sources_sha256'].items())
assert all(v in new['review_support'] for v in old['review_support'])
for ident in old_nodes:
    assert old_nodes[ident].get('required_conditions')==new_nodes[ident].get('required_conditions')
conditions={n['id']:n['statement'] for n in new['nodes'] if n['id'].startswith('C_ERC_')}
assert 'UNADOPTED alternatives, not jointly imposed' in conditions['C_ERC_RESPONSES']
assert 'not nonlinear solution error or empirical recovery' in conditions['C_ERC_WEAK']
assert 'different higher derivative data' in conditions['C_ERC_FLAT_EVENT']
old_dispositions=subprocess.check_output(['git','show',base+':development_reconstruction_2026-09-29/RECENT_DISPOSITIONS.tsv'],text=True)
dispositions=Path('development_reconstruction_2026-09-29/RECENT_DISPOSITIONS.tsv').read_text()
assert dispositions.startswith(old_dispositions)
assert len(dispositions.splitlines())==len(old_dispositions.splitlines())+1
assert dispositions.splitlines()[-1].split('\t')[0]=='ERC1_RETURN'
dev=Path('UDT_DEVELOPMENT.md').read_text()
orientation=dev.split('<!-- DEVELOPMENT_ORIENTATION_BEGIN -->')[1].split('<!-- DEVELOPMENT_ORIENTATION_END -->')[0].strip()
program=Path('CURRENT_RESEARCH_PROGRAM.md').read_text().split('<!-- GENERATED_DEVELOPMENT_BEGIN -->')[1].split('<!-- GENERATED_DEVELOPMENT_END -->')[0].strip()
assert orientation==program
assert 'not complete dynamical data' in orientation
assert 'p and q alone are not exact arbitrary finite-interval ratios' in dev
assert 'roundoff' in dev and 'no response or action is adopted' in orientation
result={'pass':True,'freeze_sha256':digest(freeze_path),'accepted_file_count':count,
 'bytes_checked':bytes_checked,'protected_map_entries':0,'changed_inherited_paths':changed,
 'unchanged_inherited_count':len(prior)-len(changed),'new_package_files':len(newfiles),
 'new_graph_nodes':node_additions,'prior_edges_sources_conditions_reviews_preserved':True,
 'prior_dispositions_preserved':True,'generated_orientation_identical':True,
 'actual_branch':branch,'actual_head':head,
 'scope':'File correspondence and scoped semantic assertions after actual prose review; no full406 or physics replay, and hashes are not scientific proof.'}
(ROOT/'math/FINAL_INTEGRATION_CHECK.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
