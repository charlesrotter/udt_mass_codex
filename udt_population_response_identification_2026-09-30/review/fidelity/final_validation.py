"""PRI1 final exact-byte and scoped integration regression."""
import hashlib
import json
import subprocess
import sys
from pathlib import Path

root=Path.cwd()
sys.path.insert(0,str(root))
import verify_udt_development as v
base=Path('udt_population_response_identification_2026-09-30')
freeze_path=base/'INTEGRATION_FREEZE.json'
expected='9cec6caf5c06efd4b53e2924c1713cf18d9ea804b7c9eec60c184ac6572d88d0'
digest=lambda b:hashlib.sha256(b).hexdigest()
checks={}
def check(name,truth):
    checks[name]=bool(truth)
    assert truth,name
check('integration_freeze_exact',digest(freeze_path.read_bytes())==expected)
freeze=json.loads(freeze_path.read_text())
accepted=freeze['accepted_sha256']
protected=('udt_kernel_plane_global_curvature_holonomy_atlas_2026-08-02/',
 'udt_native_onshell_timelive_reset_owner_audit_2026-08-10/',
 'udt_pair_regime_flow_reciprocal_orchestra_amplification_2026-08-12/',
 'udt_sne_xmax_G88_am_radial_compatibility_atlas_2026-08-12/')
check('no_protected_binding',not any(p.startswith(protected) for p in accepted))
mismatch=[p for p,sha in accepted.items() if digest(Path(p).read_bytes())!=sha]
check('all261_accepted_bytes_match',len(accepted)==261 and not mismatch)
previous=json.loads((base/'PREVIOUS_REVIEW_RECORD.json').read_text())['accepted_sha256']
changed={p for p,sha in previous.items() if accepted.get(p)!=sha}
check('old191_bindings_retained',len(previous)==191 and set(previous)<=set(accepted))
check('exact_eight_changed_previous',changed==set(freeze['changed_previous_paths']) and len(changed)==8)
check('183_unchanged70_new',len(previous)-len(changed)==183 and len(set(accepted)-set(previous))==70)
diff=subprocess.check_output(['git','-c','core.preloadIndex=false','diff','--name-only'],text=True).splitlines()
check('tracked_diff_exact_eight',set(diff)==changed)
for p in ('CURRENT_SCIENTIFIC_PREMISES.tsv','CANON.md'):
    old=subprocess.check_output(['git','show','HEAD:'+p])
    check('unchanged_'+p,digest(old)==digest(Path(p).read_bytes()))
check('generated_program_exact',v.program_text(Path(v.MASTER).read_text())==Path('CURRENT_RESEARCH_PROGRAM.md').read_text())
graph_path='development_reconstruction_2026-09-29/DEVELOPMENT_GRAPH.json'
graph=json.loads(Path(graph_path).read_text())
oldgraph=json.loads(subprocess.check_output(['git','show','HEAD:'+graph_path]))
nodes={x['id']:x for x in graph['nodes']}
check('prior_graph_nodes_unchanged',all(nodes[x['id']]==x for x in oldgraph['nodes']))
check('prior_graph_edges_unchanged',all(x in graph['edges'] for x in oldgraph['edges']))
check('prior_graph_source_pins_unchanged',all(graph['sources_sha256'][p]==sha for p,sha in oldgraph['sources_sha256'].items()))
check('observer_requires_positive_population_nonbeam',set(nodes['R18O']['required_conditions'])=={'C_PRI_POPULATION','C_PRI_NONBEAM'})
check('raw_requires_population_and_diagnostic_only',set(nodes['R18B']['required_conditions'])=={'C_PRI_POPULATION','C_PRI_RAW'})
check('negative_has_no_nonbeam_requirement',not any(x['from']=='C_PRI_NONBEAM' and x['to']=='R18B' for x in graph['edges']))
impact=set(v.affected_nodes(graph,[str(base/'INITIAL_CANDIDATE.md')]))
check('positive_negative_descendants',{'R18O','R18F','R18B','R18'}<=impact and not ({'R9','R18T','R18C','R18U'}&impact))
for seal_name in ('SOURCE_FIRST_SEAL.json','DIRECT_REVIEW_SEAL.json'):
    seal=json.loads((base/'review/fidelity'/seal_name).read_text())
    check('unchanged_'+seal_name,all(digest(Path(x['path']).read_bytes())==x['sha256'] for x in seal['files']))
print(json.dumps({'status':'PASS','checks':checks,'accepted_paths':len(accepted),'prior_paths':len(previous),'prior_unchanged':183,'prior_changed':8,'new_paths':70,'scope':'Byte/routing regression; actual scientific and repair fidelity independently read. Parent normal/full406 gates separate.'},indent=2))
