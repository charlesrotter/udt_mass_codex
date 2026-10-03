"""Final byte/routing checks; semantic acceptance is separately documented."""
from pathlib import Path
import hashlib,importlib.util,json,subprocess

root=Path.cwd().resolve(); p=Path('udt_curvature_measurement_feasibility_2026-10-02')
f=p/'INTEGRATION_FREEZE.json'; freeze=json.loads(f.read_text())
accepted=freeze['accepted_sha256']
protected=['udt_kernel_plane_global_curvature_holonomy_atlas_2026-08-02/',
'udt_native_onshell_timelive_reset_owner_audit_2026-08-10/',
'udt_pair_regime_flow_reciprocal_orchestra_amplification_2026-08-12/',
'udt_sne_xmax_G88_am_radial_compatibility_atlas_2026-08-12/']
assert not any(x.startswith(tuple(protected)) for x in accepted)
sha=lambda data:hashlib.sha256(data).hexdigest()
mismatches=[]
for path,expected in accepted.items():
    absolute=(root/path).resolve()
    assert absolute.is_relative_to(root),path
    if not absolute.is_file() or sha(absolute.read_bytes())!=expected:mismatches.append(path)
assert not mismatches,mismatches
prior=json.loads((p/'PRIOR_REVIEW_RECORD.json').read_text())['accepted_sha256']
changed=sorted(x for x,h in prior.items() if accepted.get(x)!=h)
assert changed==sorted(freeze['changed_inherited']),(changed,freeze['changed_inherited'])
assert len(prior)==freeze['inherited_count']
spec=importlib.util.spec_from_file_location('development_verifier',root/'verify_udt_development.py')
v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
master=(root/'UDT_DEVELOPMENT.md').read_text()
assert v.program_text(master)==(root/'CURRENT_RESEARCH_PROGRAM.md').read_text()
unchanged=[]
for name in ['CURRENT_SCIENTIFIC_PREMISES.tsv','CANON.md']:
    base=subprocess.check_output(['git','show','HEAD:'+name])
    assert base==(root/name).read_bytes(),name
    unchanged.append(name)
graph=json.loads((root/'development_reconstruction_2026-09-29/DEVELOPMENT_GRAPH.json').read_text())
nodes={x['id']:x for x in graph['nodes']}
for n in ['C_CMF_PREP','C_CMF_ERRORS','C_CMF_TRACE','R8CMF','R17CMF']:
    assert n in nodes,n
    for source in nodes[n]['sources']:assert sha((root/source).read_bytes())==graph['sources_sha256'][source],source
reviewed=(p/'REVIEWED_RESULT.md').read_text()
assert 'practical experiment and native selection OPEN' in reviewed
assert 'OPEN' in nodes['O_PSW_ATTRIBUTION']['statement']
head=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()
branch=subprocess.check_output(['git','branch','--show-current'],text=True).strip()
assert branch=='grok' and head==freeze['base_head']
print(json.dumps({'status':'PASS','scope':'All-map byte correspondence, changed-inherited map, generated program, current registry/CANON preservation, CMF source pins. Not full-corpus semantic reproof.','accepted_paths':len(accepted),'inherited_paths':len(prior),'changed_inherited':changed,'protected_prefix_entries':0,'unchanged':unchanged,'head':head,'branch':branch,'freeze_sha256':sha(f.read_bytes())},indent=2))
