"""Post-freeze exact-byte review protocol; not a new scientific input."""
import hashlib,json
from pathlib import Path
HERE=Path(__file__).resolve().parent;BASE=HERE.parents[1];ROOT=BASE.parent
def sha(path):
    h=hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda:f.read(1024**2),b''):h.update(chunk)
    return h.hexdigest()
freeze=BASE/'FINAL_INTEGRATION_FREEZE.json';f=json.loads(freeze.read_text())
assert sha(freeze)=='367b423b877cee3a1269059d1ba560976ac5a2ca6017d70faa6200f81e63af1c'
accepted=f['accepted_sha256'];protected=[
 'udt_kernel_plane_global_curvature_holonomy_atlas_2026-08-02/',
 'udt_native_onshell_timelive_reset_owner_audit_2026-08-10/',
 'udt_pair_regime_flow_reciprocal_orchestra_amplification_2026-08-12/',
 'udt_sne_xmax_G88_am_radial_compatibility_atlas_2026-08-12/']
assert len(accepted)==5591
for path,value in accepted.items():
    assert not any(path.startswith(prefix) for prefix in protected)
    full=(ROOT/path).resolve();assert full.is_relative_to(ROOT)
    assert sha(full)==value,path
old=json.loads((BASE/'PREVIOUS_REVIEW_RECORD.json').read_text())['accepted_sha256']
assert set(old)<=set(accepted)
changed=sorted(path for path in old if old[path]!=accepted[path])
assert changed==f['changed_previous_paths'] and len(changed)==6
graph=json.loads((ROOT/'development_reconstruction_2026-09-29/DEVELOPMENT_GRAPH.json').read_text())
nodes={row['id']:row for row in graph['nodes']}
assert set(nodes['R12T']['required_conditions'])=={'C_EINSTEIN','C_TDS_ARENA','P_NULL'}
for condition in nodes['R12T']['required_conditions']:
    assert dict(**{'from':condition,'to':'R12T','kind':'hypothesis'}) in graph['edges']
assert {'from':'R12T','to':'R18','kind':'interpretation'} in graph['edges']
for path,value in graph['sources_sha256'].items():
    assert not any(path.startswith(prefix) for prefix in protected)
    assert sha(ROOT/path)==value,path
    if path in accepted:assert accepted[path]==value
for row in graph['review_support']:
    assert not any(row['path'].startswith(prefix) for prefix in protected)
    assert sha(ROOT/row['path'])==row['sha256']
    if row['path'] in accepted:assert accepted[row['path']]==row['sha256']
method=(BASE/'METHOD.md').read_text();assert 'initial g/v symmetry' in method
dispatch=(BASE/'PRODUCTION_DISPATCH.md').read_text();assert 'Run extraction serially' in dispatch
assert 'first-three-case' in (BASE/'REVIEWED_RESULT.md').read_text()
print(json.dumps(dict(status='EXACT_BINDING_AND_SCOPED_GRAPH_PASS',accepted_paths=len(accepted),
    retained_previous_paths=len(old)-len(changed),changed_previous_paths=changed,
    source_pins=len(graph['sources_sha256']),review_support=len(graph['review_support']),
    freeze_sha256=sha(freeze),scope='Actual bytes, retained prior bindings and reviewed conditional graph edges; no historical full reproof or406 rerun.'),indent=2))
