"""Bounded final byte/routing audit; no inherited scientific reproof."""
from pathlib import Path
import hashlib,json,subprocess,sys
root=Path.cwd()
base=root/'udt_tick_readout_identification_2026-09-30'
freeze=base/'INTEGRATION_FREEZE.json'
assert hashlib.sha256(freeze.read_bytes()).hexdigest()=='f535c993d4e27dc0cd13aa01ee3c3fc287beba972d416e3b02f553c7c0e414ca'
f=json.loads(freeze.read_text()); accepted=f['accepted_sha256']
blocked=('udt_kernel_plane_global_curvature_holonomy_atlas_2026-08-02/',
         'udt_native_onshell_timelive_reset_owner_audit_2026-08-10/',
         'udt_pair_regime_flow_reciprocal_orchestra_amplification_2026-08-12/',
         'udt_sne_xmax_G88_am_radial_compatibility_atlas_2026-08-12/')
total_bytes=0
for name,expected in accepted.items():
    p=Path(name)
    assert not p.is_absolute() and '..' not in p.parts and '.git' not in p.parts,name
    assert not name.startswith(blocked),name
    path=root/p
    assert path.resolve()==path and path.is_file(),name
    assert not str(path.relative_to(root)).startswith(blocked),name
    total_bytes+=path.stat().st_size
    h=hashlib.sha256()
    with path.open('rb') as stream:
        for chunk in iter(lambda:stream.read(65536),b''):h.update(chunk)
    assert h.hexdigest()==expected,name
prior=json.loads((base/'PREVIOUS_REVIEW_RECORD.json').read_text())['accepted_sha256']
assert len(prior)==261 and len(accepted)==332
assert set(prior)<=set(accepted)
changed=sorted(p for p,h in prior.items() if accepted[p]!=h)
assert changed==sorted(f['changed_previous_paths']) and len(changed)==8
assert len(set(accepted)-set(prior))==71
diff=set(subprocess.check_output(['git','-c','core.preloadIndex=false','-c','index.threads=1','diff','--name-only'],text=True).splitlines())
assert diff==set(changed),(diff,changed)
head='39126a762222136f917bda5fbf6573faf02370d7'
assert subprocess.check_output(['git','-c','core.preloadIndex=false','-c','index.threads=1','rev-parse','HEAD'],text=True).strip()==head
assert subprocess.check_output(['git','-c','core.preloadIndex=false','-c','index.threads=1','branch','--show-current'],text=True).strip()=='grok'
graphpath='development_reconstruction_2026-09-29/DEVELOPMENT_GRAPH.json'
old=json.loads(subprocess.check_output(['git','-c','core.preloadIndex=false','-c','index.threads=1','show',head+':'+graphpath],text=True))
new=json.loads((root/graphpath).read_text())
oldnodes={n['id']:n for n in old['nodes']};newnodes={n['id']:n for n in new['nodes']}
assert set(newnodes)-set(oldnodes)=={'C_TRI_COUNTS','R6N','R6T'}
for name,node in oldnodes.items():assert newnodes[name]==node,name
for e in old['edges']:assert e in new['edges'],e
for name,h in old['sources_sha256'].items():assert new['sources_sha256'][name]==h,name
assert len(new['sources_sha256'])==len(old['sources_sha256'])+3==93
for r in old['review_support']:assert r in new['review_support']
for target in ['R18O','R18F','R18B']:
    assert {'from':'R6N','to':target,'kind':'interpretation'} in new['edges']
for target in ['R6N','R6T']:
    for source in ['P_NULL','M_GEOMETRY']:
        assert {'from':source,'to':target,'kind':'hypothesis'} in new['edges']
assert {'from':'C_TRI_COUNTS','to':'R6T','kind':'hypothesis'} in new['edges']
central=(root/'UDT_DEVELOPMENT.md').read_text()
program=(root/'CURRENT_RESEARCH_PROGRAM.md').read_text()
orientation=central.split('<!-- DEVELOPMENT_ORIENTATION_BEGIN -->')[1].split('<!-- DEVELOPMENT_ORIENTATION_END -->')[0].strip()
excerpt=program.split('<!-- GENERATED_DEVELOPMENT_BEGIN -->')[1].split('<!-- GENERATED_DEVELOPMENT_END -->')[0].strip()
assert orientation==excerpt
draft=json.loads((base/'checks/draft.stdout').read_text())
assert draft['status']=='DRAFT_COHERENCE_ONLY' and draft['registry_rows']==406 and draft['later_returns']==33 and draft['source_pins']==93
for item in ['draft','maintenance']:
    receipt=json.loads((base/('checks/'+item+'.json')).read_text())
    assert receipt['returncode']==0 and not receipt['timeout']
assert 'Ran 51 tests' in (base/'checks/maintenance.stderr').read_text()
assert (base/'checks/maintenance.stderr').read_text().strip().endswith('OK')
receipt=json.loads((base/'checks/normal_before_binding.json').read_text())
assert receipt['returncode']!=0 and not receipt['timeout']
assert 'REVIEW_REQUIRED' in (base/'checks/normal_before_binding.stdout').read_text()+(base/'checks/normal_before_binding.stderr').read_text()
print(json.dumps({'verdict':'PASS','freeze_sha256':hashlib.sha256(freeze.read_bytes()).hexdigest(),'accepted_paths':len(accepted),'unchanged_inherited_paths':len(prior)-len(changed),'changed_prior_paths':len(changed),'new_paths':len(set(accepted)-set(prior)),'hashed_bytes':total_bytes,'graph_existing_nodes_edges_sources_support_preserved':True,'generated_program_exact':True,'parent_receipts_verified':'draft406/33/93; maintenance51; expected prebinding REVIEW_REQUIRED','omissions':'Inherited scientific content not re-proved; no protected paths; full406 remains parent gate','python':sys.version},indent=2))
