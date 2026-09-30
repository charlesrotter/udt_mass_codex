#!/usr/bin/env python3
"""Bounded final map integrity/scope inspection; not semantic auto-acceptance."""
import hashlib
import json
from pathlib import Path
import resource
import subprocess
import time
resource.setrlimit(resource.RLIMIT_CPU,(180,180))
resource.setrlimit(resource.RLIMIT_AS,(2*1024**3,2*1024**3))
start=time.monotonic()
root=Path(__file__).resolve().parents[3]
out=Path(__file__).resolve().parent
package=root/'udt_gpu_time_live_discovery_2026-09-30'
freeze_path=package/'INTEGRATION_FREEZE.json'
freeze_bytes=freeze_path.read_bytes()
freeze=json.loads(freeze_bytes)
old=json.loads((package/'PREVIOUS_REVIEW_RECORD.json').read_text())['accepted_sha256']
protected=('udt_native_onshell_timelive_reset_owner_audit_2026-08-10/',
 'udt_pair_regime_flow_reciprocal_orchestra_amplification_2026-08-12/',
 'udt_sne_xmax_G88_am_radial_compatibility_atlas_2026-08-12/',
 'udt_kernel_plane_global_curvature_holonomy_atlas_2026-08-02/')
accepted=freeze['accepted_sha256']
for rel in accepted:
    path=Path(rel)
    assert not path.is_absolute() and '..' not in path.parts and not rel.startswith(protected),rel
    resolved=(root/path).resolve()
    assert resolved.is_relative_to(root),rel
    assert not str(resolved.relative_to(root)).startswith(protected),rel
bad={}
for rel,expected in accepted.items():
    actual=hashlib.sha256((root/rel).read_bytes()).hexdigest()
    if expected!=actual:bad[rel]={'expected':expected,'actual':actual}
assert not bad,bad
assert set(old)<=set(accepted),'Inherited bindings omitted'
changed={rel:{'before':h,'after':accepted[rel]} for rel,h in old.items() if accepted[rel]!=h}
graph=json.loads((root/'development_reconstruction_2026-09-29/DEVELOPMENT_GRAPH.json').read_text())
nodes={q['id']:q for q in graph['nodes']}
assert nodes['R12N']['required_conditions']==['C_EINSTEIN','C_NGD_ARENA','P_NULL']
assert {'from':'R12N','to':'R18','kind':'interpretation'} in graph['edges']
assert {'from':'R6N','to':'R12N','kind':'proof'} in graph['edges']
assert not any(e['to']=='R12N' and e['from']=='R9' and e['kind']=='proof' for e in graph['edges'])
head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=root,text=True).strip()
branch=subprocess.check_output(['git','branch','--show-current'],cwd=root,text=True).strip()
assert head==freeze['base_head'] and branch=='grok'
result={'verdict':'PASS_FILE_CORRESPONDENCE_AND_ROUTING_ONLY',
 'freeze_sha256':hashlib.sha256(freeze_bytes).hexdigest(),
 'checked_count':len(accepted),'old_count':len(old),'new_count':len(set(accepted)-set(old)),
 'changed_inherited_files':changed,'protected_files_opened':False,'mismatches':bad,
 'HEAD':head,'branch':branch,'elapsed_seconds':time.monotonic()-start,
 'peak_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
 'warning':'Semantic acceptance requires the actual separate final integration review.'}
(out/'INTEGRATION_CHECK.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
