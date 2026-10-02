"""RCD1 exposed frozen-correspondence review; no scientific replay."""
import hashlib,json,subprocess
from pathlib import Path
B=Path(__file__).resolve().parent.parent
freeze_path=B/'INTEGRATION_FREEZE.json'
freeze=json.loads(freeze_path.read_text());accepted=freeze['accepted_sha256']
def sha(path):
    h=hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda:f.read(1024*1024),b''):h.update(block)
    return h.hexdigest()
freeze_sha=sha(freeze_path)
assert freeze_sha=='599409e76a10767746f737d2f41c3247c5a79f3890937f153c6c1b073e73f7fb'
protected=['udt_kernel_plane_global_curvature_holonomy_atlas_2026-08-02/',
'udt_native_onshell_timelive_reset_owner_audit_2026-08-10/',
'udt_pair_regime_flow_reciprocal_orchestra_amplification_2026-08-12/',
'udt_sne_xmax_G88_am_radial_compatibility_atlas_2026-08-12/']
assert not any(any(name.startswith(prefix) for prefix in protected) for name in accepted)
total=0
for name,wanted in accepted.items():
    p=Path(name);assert sha(p)==wanted,name;total+=p.stat().st_size
prior=json.loads((B/'PRIOR_REVIEW_RECORD.json').read_text())['accepted_sha256']
assert set(prior)<=set(accepted)
changed=sorted(k for k,v in prior.items() if accepted[k]!=v)
assert changed==sorted(freeze['changed_inherited_paths'])
assert len(prior)-len(changed)==freeze['inherited_unchanged_files']
added=set(accepted)-set(prior)
assert len(added)==freeze['new_package_files']
assert all(p.startswith(B.name+'/') for p in added)
base=freeze['base_head']
head=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()
branch=subprocess.check_output(['git','branch','--show-current'],text=True).strip()
assert head==base and branch=='grok'
pins=json.loads((B/'SOURCE_PINS.json').read_text());historical=[]
for name,wanted in pins.items():
    if name in changed:
        raw=subprocess.check_output(['git','show',base+':'+name]);historical.append(name)
        assert hashlib.sha256(raw).hexdigest()==wanted,name
    else:assert sha(Path(name))==wanted,name
gp='development_reconstruction_2026-09-29/DEVELOPMENT_GRAPH.json'
old=json.loads(subprocess.check_output(['git','show',base+':'+gp],text=True))
new=json.loads(Path(gp).read_text())
old_nodes={v['id']:v for v in old['nodes']};new_nodes={v['id']:v for v in new['nodes']}
assert set(old_nodes)<=set(new_nodes)
for ident,node in old_nodes.items():assert node.get('required_conditions')==new_nodes[ident].get('required_conditions')
assert all(e in new['edges'] for e in old['edges'])
assert all(new['sources_sha256'][p]==v for p,v in old['sources_sha256'].items())
assert all(v in new['review_support'] for v in old['review_support'])
assert set(new_nodes)-set(old_nodes)=={'C_RCD_EQUATION','C_RCD_CLOCK','C_RCD_FLAT_EVENT','R8RCD','R17RCD'}
dp='development_reconstruction_2026-09-29/RECENT_DISPOSITIONS.tsv'
old_disp=subprocess.check_output(['git','show',base+':'+dp],text=True)
new_disp=Path(dp).read_text()
assert new_disp.startswith(old_disp) and len(new_disp.splitlines())==len(old_disp.splitlines())+1
assert new_disp.splitlines()[-1].split('\t')[0]=='RCD1_RETURN'
dev=Path('UDT_DEVELOPMENT.md').read_text()
orientation=dev.split('<!-- DEVELOPMENT_ORIENTATION_BEGIN -->')[1].split('<!-- DEVELOPMENT_ORIENTATION_END -->')[0].strip()
program=Path('CURRENT_RESEARCH_PROGRAM.md').read_text().split('<!-- GENERATED_DEVELOPMENT_BEGIN -->')[1].split('<!-- GENERATED_DEVELOPMENT_END -->')[0].strip()
assert orientation==program
assert 'Two reused separate contexts' in orientation and 'allocation was unavailable' in orientation
assert 'not a necessary full-tensor' in dev
assert 'fresh-context review is UNAVAILABLE/NOT PASSED' in dev
receipt_checks={}
for stem,code in [('draft_guard',1),('draft_guard_repaired',0),('normal_prebinding',1)]:
    r=json.loads((B/'checks'/f'{stem}.json').read_text());assert r['returncode']==code
    for ext in ['stdout','stderr']:assert sha(B/'checks'/f'{stem}.{ext}')==r[ext+'_sha256']
    receipt_checks[stem]=code
assert 'REVIEW_REQUIRED' in (B/'checks/normal_prebinding.stdout').read_text()
result={'pass':True,'context':'/root/erc_math','fresh_context':False,'freeze_sha256':freeze_sha,
 'accepted_count':len(accepted),'bytes_checked':total,'protected_entries':0,
 'inherited_unchanged_count':len(prior)-len(changed),'changed_inherited_paths':changed,
 'new_package_files':len(added),'source_pin_count':len(pins),'historical_pins_resolved_at_base':historical,
 'prior_graph_edges_sources_conditions_reviews_preserved':True,'prior_dispositions_preserved':True,
 'generated_orientation_identical':True,'actual_head':head,'actual_branch':branch,
 'captured_integration_receipts':receipt_checks,
 'limits':'Exposed byte correspondence and scoped semantic checks after actual prose review; no new science, full406 replay, empirical confirmation or predicted banking pass.'}
with (B/'math/FINAL_INTEGRATION_CHECK.json').open('x') as f:json.dump(result,f,indent=2);f.write('\n')
print(json.dumps(result,indent=2))
