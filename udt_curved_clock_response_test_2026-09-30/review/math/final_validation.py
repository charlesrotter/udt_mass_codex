"""Final CCR1 bytes/routing verification; scientific review is FINAL_REVIEW.md."""
from pathlib import Path
import csv
import hashlib
import json
import subprocess
import sys
sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT))
import verify_udt_development as v

pkg=ROOT/'udt_curved_clock_response_test_2026-09-30'
freeze_path=pkg/'INTEGRATION_FREEZE.json'
freeze_sha=hashlib.sha256(freeze_path.read_bytes()).hexdigest()
assert freeze_sha=='b6ad3eda8873cf46f69b42d04b3963e8a326a2cdfd1d501914fb67ac4bfce4af'
freeze=json.loads(freeze_path.read_text())
accepted=freeze['accepted_sha256']
assert len(accepted)==191
for p in accepted:
    assert not Path(p).is_absolute() and '..' not in Path(p).parts and not p.startswith(v.PROTECTED)
for p,h in accepted.items():
    got=hashlib.sha256((ROOT/p).read_bytes()).hexdigest()
    assert got==h,(p,h,got)
prior=json.loads((pkg/'PREVIOUS_REVIEW_RECORD.json').read_text())['accepted_sha256']
assert len(prior)==128 and set(prior)<=set(accepted)
changed=sorted(p for p,h in prior.items() if accepted[p]!=h)
assert changed==sorted(freeze['changed_previous_paths']) and len(changed)==8
assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()==freeze['parent_head']
assert subprocess.check_output(['git','branch','--show-current'],cwd=ROOT,text=True).strip()=='grok'
graph=json.loads((ROOT/v.WORK/'DEVELOPMENT_GRAPH.json').read_text())
nodes={n['id']:n for n in graph['nodes']}
for condition,result in [('C_CCR_TUBE','R18T'),('C_CCR_SIGN','R18C'),('C_CCR_UNIVERSAL','R18U')]:
    assert condition in nodes[result]['required_conditions']
    assert {'from':condition,'to':result,'kind':'hypothesis'} in graph['edges']
assert nodes['C_CCR_UNIVERSAL']['kind']=='unadopted_branch'
for a,b in [('R18T','R18C'),('R18C','R18U')]:
    assert {'from':a,'to':b,'kind':'proof'} in graph['edges']
assert {'from':'O_PCW_PROPOSALS','to':'R18T','kind':'context'} in graph['edges']
impact=set(v.affected_nodes(graph,['udt_curved_clock_response_test_2026-09-30/REPAIR.md']))
assert {'R18T','R18C','R18U','R18'}<=impact
assert not {'R6','R9','R10'}&impact
draft=v.validate(draft=True)
assert draft['status']=='DRAFT_COHERENCE_ONLY' and draft['later_returns']==31
try:
    v.validate()
except v.DevelopmentError as exc:
    normal=str(exc)
    assert 'REVIEW_REQUIRED' in normal
else:
    raise AssertionError('Expected final-binding review gate to remain open before attestation')
print(json.dumps({'status':'PASS','freeze_sha256':freeze_sha,'all_hashes_matched':len(accepted),'prior_bindings_retained':len(prior),'changed_previous_paths':changed,'unchanged_prior_paths':len(prior)-len(changed),'new_bindings':len(accepted)-len(prior),'draft':draft,'normal_prebinding_expected':normal,'repair_affected':sorted(impact),'scope':'Byte identity, dependency routing and prebinding regression only; semantic conclusion in FINAL_REVIEW.md; no full406 banking audit'},indent=2))
