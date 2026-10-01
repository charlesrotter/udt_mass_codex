"""Bounded graph/source correspondence after direct scientific integration review."""
import hashlib
import json
from pathlib import Path
import subprocess

graph_path=Path('development_reconstruction_2026-09-29/DEVELOPMENT_GRAPH.json')
old=json.loads(subprocess.check_output(['git','show','HEAD:'+str(graph_path)],text=True))
new=json.loads(graph_path.read_text())
assert new['edges']==old['edges']
oldnodes={n['id']:n for n in old['nodes']};newnodes={n['id']:n for n in new['nodes']}
assert set(oldnodes)==set(newnodes)
for key,previous in oldnodes.items():
    current=newnodes[key]
    assert current.get('required_conditions')==previous.get('required_conditions')
    assert current['kind']==previous['kind']
    if key not in ['C_TDS_ARENA','R12T']:assert current==previous
assert newnodes['R12T']['required_conditions']==['C_EINSTEIN','C_TDS_ARENA','P_NULL']
assert all(new['sources_sha256'][p]==h for p,h in old['sources_sha256'].items())
added={p:h for p,h in new['sources_sha256'].items() if p not in old['sources_sha256']}
for p,h in added.items():
    assert p.startswith('udt_time_live_production_preparation_2026-10-01/')
    assert hashlib.sha256(Path(p).read_bytes()).hexdigest()==h
reviews=[r for r in new['review_support'] if r not in old['review_support']]
for r in reviews:
    assert r['role'] in ['review_evidence','repair_scope']
    assert r['targets']==['R12T','R18']
    assert hashlib.sha256(Path(r['path']).read_bytes()).hexdigest()==r['sha256']
recent=Path('development_reconstruction_2026-09-29/RECENT_DISPOSITIONS.tsv')
previous=subprocess.check_output(['git','show','HEAD:'+str(recent)],text=True)
current=recent.read_text();assert current.startswith(previous)
addedrow=current[len(previous):];assert addedrow.startswith('TPP1\t') and len(addedrow.splitlines())==1
assert 'CONDITIONAL_NUMERICAL_UNPROMOTED' in addedrow and 'center-only' in addedrow
print(json.dumps(dict(status='PASS',unchanged_edges=len(new['edges']),unchanged_node_kinds_and_hypotheses=True,
    prior_source_pins_preserved=len(old['sources_sha256']),new_source_pins=len(added),typed_new_reviews=len(reviews),
    graph_sha256=hashlib.sha256(graph_path.read_bytes()).hexdigest(),recent_sha256=hashlib.sha256(recent.read_bytes()).hexdigest(),
    source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    scope='Current typed dependency and newsource hash correspondence; no reproof of historical sources or full audit.'),indent=2,sort_keys=True))
