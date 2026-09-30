"""Packaging-only final validation; no scientific control rerun."""
import ast
import hashlib
import json
import pathlib
import subprocess
import sys

root=pathlib.Path.cwd()
sys.path.insert(0,str(root))
base=root/'udt_population_response_identification_2026-09-30'
freeze=base/'INTEGRATION_FREEZE.json'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
expected='9cec6caf5c06efd4b53e2924c1713cf18d9ea804b7c9eec60c184ac6572d88d0'
assert sha(freeze)==expected
F=json.loads(freeze.read_text());accepted=F['accepted_sha256']
protected=('udt_kernel_plane_global_curvature_holonomy_atlas_2026-08-02/',
 'udt_native_onshell_timelive_reset_owner_audit_2026-08-10/',
 'udt_pair_regime_flow_reciprocal_orchestra_amplification_2026-08-12/',
 'udt_sne_xmax_G88_am_radial_compatibility_atlas_2026-08-12/')
assert not any(p.startswith(protected) for p in accepted)
for p,h in accepted.items():assert sha(root/p)==h,p
previous=json.loads((base/'PREVIOUS_REVIEW_RECORD.json').read_text())['accepted_sha256']
assert set(previous)<=set(accepted)
changed={p for p,h in previous.items() if accepted[p]!=h}
assert changed==set(F['changed_previous_paths'])
assert (len(accepted),len(previous),len(changed),len(set(accepted)-set(previous)))==(261,191,8,70)
actual_diff=set(subprocess.check_output(['git','-c','core.preloadIndex=false','diff','HEAD','--name-only'],text=True).splitlines())
assert actual_diff==changed,(actual_diff,changed)
assert subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()==F['parent_head']
assert subprocess.check_output(['git','branch','--show-current'],text=True).strip()=='grok'

graph_path='development_reconstruction_2026-09-29/DEVELOPMENT_GRAPH.json'
graph=json.loads((root/graph_path).read_text());nodes={n['id']:n for n in graph['nodes']}
edges={(e['from'],e['to'],e['kind']) for e in graph['edges']}
assert set(nodes['R18O']['required_conditions'])=={'C_PRI_POPULATION','C_PRI_NONBEAM'}
assert set(nodes['R18B']['required_conditions'])=={'C_PRI_POPULATION','C_PRI_RAW'}
assert ('C_PRI_NONBEAM','R18B','hypothesis') not in edges
assert ('R9','R18B','proof') in edges
for condition,target in [('C_PRI_POPULATION','R18O'),('C_PRI_NONBEAM','R18O'),
                         ('C_PRI_POPULATION','R18B'),('C_PRI_RAW','R18B')]:
    assert (condition,target,'hypothesis') in edges

def reach(initial):
    found=set(initial);todo=list(initial)
    while todo:
        x=todo.pop()
        for a,b,k in edges:
            if a==x and b not in found:found.add(b);todo.append(b)
    return found

proof_source='udt_population_response_identification_2026-09-30/INITIAL_CANDIDATE.md'
start={n['id'] for n in graph['nodes'] if proof_source in n.get('sources',[])}
impact=reach(start)
assert {'R18O','R18F','R18B','R18'}<=impact
assert not {'R9','R18T','R18C','R18U'}&impact
assert 'R18B' not in reach({'C_PRI_NONBEAM'})
assert 'R18O' not in reach({'C_PRI_RAW'})

import verify_udt_development as v
master=(root/'UDT_DEVELOPMENT.md').read_text()
assert v.program_text(master)==(root/'CURRENT_RESEARCH_PROGRAM.md').read_text()
draft=v.validate(draft=True)
assert draft['registry_rows']==406 and draft['later_returns']==32 and draft['source_pins']==90

oldgraph=json.loads(subprocess.check_output(['git','show',F['parent_head']+':'+graph_path],text=True))
for p,h in oldgraph['sources_sha256'].items():
    assert graph['sources_sha256'][p]==h,p
assert len(graph['sources_sha256'])-len(oldgraph['sources_sha256'])==3
for n in oldgraph['nodes']:assert nodes[n['id']]==n,n['id']
for e in oldgraph['edges']:assert e in graph['edges']
assert len(graph['nodes'])-len(oldgraph['nodes'])==6
assert len(graph['edges'])-len(oldgraph['edges'])==16

guard_names=['test_pri_observer_requires_nonbeam_hypothesis',
 'test_pri_raw_obstruction_requires_population_domain',
 'test_pri_negative_conclusion_requires_tested_identification',
 'test_pri_source_routes_construction_and_adverse_use']
command=['python3','development_reconstruction_2026-09-29/checks/test_maintenance.py',
         *['Maintenance.'+name for name in guard_names]]
run=subprocess.run(command,capture_output=True,text=True,check=False)
assert run.returncode==0,(run.stdout,run.stderr)
receipt=json.loads((base/'checks/maintenance.json').read_text())
assert receipt['returncode']==0 and not receipt['timeout']
stderr=(base/'checks/maintenance.stderr').read_text()
assert 'Ran 48 tests' in stderr and '\nOK\n' in stderr
normal=json.loads((base/'checks/normal_before_binding.json').read_text())
assert normal['returncode']==1 and not normal['timeout']
normal_text=(base/'checks/normal_before_binding.stdout').read_text()+(base/'checks/normal_before_binding.stderr').read_text()
assert 'REVIEW_REQUIRED' in normal_text

library_audit={}
for name in ('source_first_checks.py','direct_checks.py'):
    p=base/'review/fidelity'/name
    tree=ast.parse(p.read_text())
    imports=[]
    for node in ast.walk(tree):
        if isinstance(node,ast.Import):imports.extend(a.name for a in node.names)
        elif isinstance(node,ast.ImportFrom):imports.append(node.module)
    library_audit[name]=sorted(set(imports))
    assert 'fractions' in imports and 'sympy' not in imports

print(json.dumps({'status':'PASS','freeze_sha256':expected,'accepted_files':len(accepted),
 'prior_files':len(previous),'changed_prior_files':len(changed),'inherited_unchanged':len(previous)-len(changed),
 'new_files':len(set(accepted)-set(previous)),'tracked_diff_paths':sorted(actual_diff),
 'graph_impact_from_PRI1':sorted(impact),'new_graph_nodes':6,'new_graph_edges':16,
 'draft_coherence':draft,'new_guard_command':command,'new_guard_stdout':run.stdout,
 'new_guard_stderr':run.stderr,'fidelity_import_metadata':library_audit,
 'parent_gates':'final normal binding and fresh full406 remain pending; no scientific replay'},indent=2))
