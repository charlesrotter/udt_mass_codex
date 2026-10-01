"""Scoped structural audit of the launch integration, not a scientific proof."""
import hashlib
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT/'udt_time_live_production_survey_2026-10-01'
OLD = '68cf144b49829bc5a3b8ad924afad243d62f5bef'
GRAPH = 'development_reconstruction_2026-09-29/DEVELOPMENT_GRAPH.json'
RECENT = 'development_reconstruction_2026-09-29/RECENT_DISPOSITIONS.tsv'
sha = lambda path: hashlib.sha256(Path(path).read_bytes()).hexdigest()
old = json.loads(subprocess.check_output(['git', 'show', OLD+':'+GRAPH], cwd=ROOT))
new = json.loads((ROOT/GRAPH).read_text())
assert old['edges'] == new['edges']
old_nodes = {row['id']: row for row in old['nodes']}
new_nodes = {row['id']: row for row in new['nodes']}
assert old_nodes.keys() == new_nodes.keys()
changed = []
for key in old_nodes:
    before, after = old_nodes[key], new_nodes[key]
    if before == after:
        continue
    changed.append(key)
    assert key in ['C_TDS_ARENA', 'R12T']
    allowed = ['sources', 'title'] if key == 'R12T' else ['sources']
    assert {k:v for k,v in before.items() if k not in allowed} == {k:v for k,v in after.items() if k not in allowed}
    assert after['sources'][:len(before['sources'])] == before['sources']
for path, digest in old['sources_sha256'].items():
    assert new['sources_sha256'][path] == digest
added = set(new['sources_sha256']) - set(old['sources_sha256'])
for path in added:
    assert path.startswith(BASE.name+'/')
    assert sha(ROOT/path) == new['sources_sha256'][path]
assert new['review_support'][:len(old['review_support'])] == old['review_support']
before = subprocess.check_output(['git','show',OLD+':'+RECENT],cwd=ROOT).decode().splitlines()
after = (ROOT/RECENT).read_text().splitlines()
assert after[:len(before)] == before and len(after) == len(before)+1
assert after[-1].split('\t')[0] == 'TPS1_LAUNCH'
central = (ROOT/'UDT_DEVELOPMENT.md').read_text()
program = (ROOT/'CURRENT_RESEARCH_PROGRAM.md').read_text()
orientation = central.split('<!-- DEVELOPMENT_ORIENTATION_BEGIN -->\n',1)[1].split('<!-- DEVELOPMENT_ORIENTATION_END -->',1)[0]
generated = program.split('<!-- GENERATED_DEVELOPMENT_BEGIN -->\n',1)[1].split('<!-- GENERATED_DEVELOPMENT_END -->',1)[0]
assert orientation == generated
result = dict(status='PASS', baseline=OLD, changed_nodes=changed,
    all_old_edges_identical=True, all_old_node_hypotheses_identical=True,
    old_source_pin_count=len(old['sources_sha256']), old_source_pins_unchanged=True,
    new_pins_verified=sorted(added), prior_review_support_preserved=True,
    existing_recent_rows_preserved=True, generated_orientation_matches=True,
    current_sha256={p:sha(ROOT/p) for p in [GRAPH,RECENT,'UDT_DEVELOPMENT.md','CURRENT_RESEARCH_PROGRAM.md','LIVE.md','HANDOFF.md','.gitignore']},
    source_sha256=sha(__file__),
    scope='Version/graph/editorial correspondence only. No old scientific reproof, grade change, raw-payload availability or running-process liveness established.')
print(json.dumps(result,indent=2,sort_keys=True))
