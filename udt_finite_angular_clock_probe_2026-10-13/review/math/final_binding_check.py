"""FAC1 final version/routing audit, with protected paths excluded before reads."""
import argparse,hashlib,json,subprocess,sys,time
from pathlib import Path

sys.dont_write_bytecode=True
ap=argparse.ArgumentParser()
ap.add_argument('expected_freeze_sha256')
ap.add_argument('output')
args=ap.parse_args()
root=Path(__file__).resolve().parents[3]
base=root/'udt_finite_angular_clock_probe_2026-10-13'
protected=('udt_native_onshell_timelive_reset_owner_audit_2026-08-10/',
 'udt_pair_regime_flow_reciprocal_orchestra_amplification_2026-08-12/',
 'udt_sne_xmax_G88_am_radial_compatibility_atlas_2026-08-12/',
 'udt_kernel_plane_global_curvature_holonomy_atlas_2026-08-02/')

def sha(path):
    h=hashlib.sha256()
    with Path(path).open('rb') as f:
        for block in iter(lambda:f.read(1024*1024),b''):h.update(block)
    return h.hexdigest()

started=time.monotonic()
freeze_path=base/'INTEGRATION_FREEZE.json'
assert sha(freeze_path)==args.expected_freeze_sha256
freeze=json.loads(freeze_path.read_text())
prior_path=root/freeze['prior_review_record']
assert sha(prior_path)==freeze['prior_review_record_sha256']
prior=json.loads(prior_path.read_text())
accepted=freeze['accepted_sha256']; inherited=prior['accepted_sha256']

# No bound payload is opened until all lexical/resolved paths are approved.
for name in set(accepted)|set(inherited):
    assert not Path(name).is_absolute() and '..' not in Path(name).parts,name
    assert not name.startswith(protected),'PROTECTED_BINDING'
    resolved=(root/name).resolve().relative_to(root).as_posix()
    assert not resolved.startswith(protected),'PROTECTED_RESOLUTION'
assert not set(inherited)-set(accepted)
changed={p for p,d in inherited.items() if accepted[p]!=d}
added=set(accepted)-set(inherited)
assert changed==set(freeze['changed_prior_files'])
assert added==set(freeze['new_files'])
for p in changed:
    assert freeze['changed_prior_files'][p]=={'old':inherited[p],'new':accepted[p]}
    historical=subprocess.check_output(['git','show',freeze['baseline_head']+':'+p],cwd=root)
    assert hashlib.sha256(historical).hexdigest()==inherited[p],p
current_head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=root,text=True).strip()
assert current_head==freeze['baseline_head']
tracked_changed=set(subprocess.check_output(['git','diff','--name-only'],cwd=root,text=True).splitlines())
assert tracked_changed==changed,sorted(tracked_changed^changed)

byte_count=0
for name,digest in accepted.items():
    p=root/name
    assert sha(p)==digest,name
    byte_count+=p.stat().st_size
science=json.loads((base/'SCIENCE_FREEZE.json').read_text())
for p,d in science['files'].items():assert accepted[p]==d,p
supplement=json.loads((base/'SCIENCE_SUPPLEMENT.json').read_text())
for p,d in supplement['files'].items():assert accepted[p]==d,p

sys.path.insert(0,str(root))
from verify_udt_development import program_text
assert program_text((root/'UDT_DEVELOPMENT.md').read_text())==(root/'CURRENT_RESEARCH_PROGRAM.md').read_text()
graph=json.loads((root/'development_reconstruction_2026-09-29/DEVELOPMENT_GRAPH.json').read_text())
nodes={n['id']:n for n in graph['nodes']}
assert nodes['R8FAC']['required_conditions']==['C_FAC_QUERY']
assert nodes['R8FACP']['required_conditions']==['C_FAC_TRIALS']
edges={(e['from'],e['to'],e['kind']) for e in graph['edges']}
for edge in [('C_FAC_QUERY','R8FAC','hypothesis'),('R8FAC','R8FACP','proof'),
             ('C_FAC_TRIALS','R8FACP','hypothesis'),('O_FAC_ATTRIBUTION','R8FACP','open_boundary')]:
    assert edge in edges,edge
for p,d in graph['sources_sha256'].items():
    if p.startswith(base.name+'/'):assert accepted[p]==d,p

result={'status':'PASS_SCOPED_VERSION_AND_ROUTING_CHECK','head':current_head,
 'freeze_sha256':args.expected_freeze_sha256,'accepted_files_checked':len(accepted),
 'accepted_bytes_streamed':byte_count,'changed_inherited_files':sorted(changed),
 'unchanged_inherited_files':len(inherited)-len(changed),'new_files':len(added),
 'original_science_files_unchanged':len(science['files']),
 'protected_paths_or_resolutions_read':0,'generated_program_matches':True,
 'mathematical_and_physical_graph_conditions_separate':True,
 'duration_seconds':time.monotonic()-started,'script_sha256':sha(__file__),
 'scope':'byte correspondence, changed-scope and selected routing only; no inherited-corpus scientific reproof or normal/maintenance/full406 gate claim'}
with Path(args.output).open('x') as f:json.dump(result,f,indent=2);f.write('\n')
print(json.dumps(result,indent=2))
