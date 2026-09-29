"""Independent, synthetic, in-memory integration controls; no scientific adoption."""
import ast
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
import verify_udt_development as guard

def digest(data):
    return hashlib.sha256(data).hexdigest()

def dump(value):
    return json.dumps(value, sort_keys=True).encode()

freeze = json.loads((ROOT / guard.WORK / 'INTEGRATION_CANDIDATE_FREEZE.json').read_text())
accepted = freeze['accepted_sha256']
assert all(digest((ROOT/p).read_bytes()) == h for p,h in accepted.items())
graph = json.loads((ROOT/guard.WORK/'DEVELOPMENT_GRAPH.json').read_text())

observations = {'freeze_sha256': digest((ROOT/guard.WORK/'INTEGRATION_CANDIDATE_FREEZE.json').read_bytes()),
                'freeze_bindings_match': True, 'synthetic_not_actual_reviews': True}
fixture = {}
reviewers = []
for index in range(2):
    context = 'SYNTHETIC_MATH_CONTROL_'+str(index)
    path = guard.WORK+'review/math/synthetic_attestation_'+str(index)+'.json'
    att = {'context': context, 'verdict': 'ACCEPT_WITH_LIMITS', 'accepted_sha256': accepted}
    fixture[path] = dump(att)
    reviewers.append({'context': context, 'attestation': path, 'sha256':digest(fixture[path])})
recordpath = guard.WORK+'REVIEW_RECORD.json'
fixture[recordpath] = dump({'status':'REVIEWED_WITH_LIMITS','accepted_sha256': accepted,'reviewers': reviewers})
observations['missing_reports_result'] = guard.validate(overrides=fixture)['status']

for index, reviewer in enumerate(reviewers):
    path = reviewer['attestation']
    att = json.loads(fixture[path])
    report = guard.WORK+'review/math/synthetic_report_'+str(index)+'.md'
    att.update(report_path=report, report_sha256=digest(b'Accepted original synthetic report'))
    fixture[report] = b'Altered synthetic report'
    fixture[path] = dump(att)
    reviewer['sha256'] = digest(fixture[path])
fixture[recordpath] = dump({'status':'REVIEWED_WITH_LIMITS','accepted_sha256':accepted,'reviewers':reviewers})
observations['changed_reports_result'] = guard.validate(overrides=fixture)['status']

source = 'udt_g310_differential_dual_reciprocity_tracefree_ownership_2026-08-31/EXACT_DERIVATION.md'
correction = guard.WORK+'SOURCE_CORRECTIONS.md'
pair = 'udt_g176_completed_pair_dual_reciprocity_consolidation_2026-08-19/EXACT_DERIVATION.md'
for name, path in [('g310_original',source),('g310_correction',correction),('g176_pair',pair)]:
    observations[name+'_affected'] = guard.affected_nodes(graph, changed_sources=[path])
assert {'R9','R10','R11','R12','R17','R18'} <= set(observations['g310_original_affected'])
assert observations['g310_correction_affected'] == []
assert not {'R5','R6'} & set(observations['g176_pair_affected'])

before = subprocess.check_output(['git','show','26da433f090a7c10717649a47c4f2383612f05cd:verify_current_scientific_premises.py'],cwd=ROOT)
after = (ROOT/'verify_current_scientific_premises.py').read_bytes()
def functions(data):
    return {node.name:ast.dump(node,include_attributes=False) for node in ast.parse(data).body if isinstance(node,(ast.FunctionDef,ast.AsyncFunctionDef))}
old,new = functions(before),functions(after)
observations['changed_verifier_functions'] = sorted(n for n in old.keys() | new.keys() if old.get(n)!=new.get(n))
assert observations['changed_verifier_functions']==['validate_startup_surface']
observations['guard_sha256'] = digest((ROOT/'verify_udt_development.py').read_bytes())
observations['graph_sha256'] = digest((ROOT/guard.WORK/'DEVELOPMENT_GRAPH.json').read_bytes())
(HERE/'integration_initial_results.json').write_text(json.dumps(observations,indent=2)+'\n')
print(json.dumps(observations,indent=2))
