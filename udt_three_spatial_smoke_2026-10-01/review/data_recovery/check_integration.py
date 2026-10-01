"""Scoped packaging/graph comparison against continuing-session baseline."""
import csv
import hashlib
import io
import json
from pathlib import Path
import subprocess
import sys
ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT))
import verify_udt_development as verifier
baseline='d65a7ea0faa0e38b9b1ad5ed5e3743be5178288d'

def old(path):return subprocess.check_output(['git','show',f'{baseline}:{path}'],cwd=ROOT)
def sha(data):return hashlib.sha256(data).hexdigest()

graph_path='development_reconstruction_2026-09-29/DEVELOPMENT_GRAPH.json'
previous=json.loads(old(graph_path));current=json.loads((ROOT/graph_path).read_bytes())
for key in ('nodes','edges','review_support'):
    assert all(value in current[key] for value in previous[key]),key
assert all(current['sources_sha256'].get(path)==value for path,value in previous['sources_sha256'].items())
new_nodes=[n for n in current['nodes'] if n not in previous['nodes']]
assert {n['id'] for n in new_nodes}=={'C_TDS_ARENA','R12T'}
assert next(n for n in new_nodes if n['id']=='R12T')['required_conditions']==['C_EINSTEIN','C_TDS_ARENA','P_NULL']
master=(ROOT/'UDT_DEVELOPMENT.md').read_text()
assert (ROOT/'CURRENT_RESEARCH_PROGRAM.md').read_text()==verifier.program_text(master)
for path in ('CANON.md','CURRENT_SCIENTIFIC_PREMISES.tsv'):
    assert (ROOT/path).read_bytes()==old(path),path
recent_path='development_reconstruction_2026-09-29/RECENT_DISPOSITIONS.tsv'
prior_rows=list(csv.DictReader(io.StringIO(old(recent_path).decode()),delimiter='\t'))
current_rows=list(csv.DictReader((ROOT/recent_path).open(),delimiter='\t'))
assert current_rows[:len(prior_rows)]==prior_rows
assert len(prior_rows)==34 and len(current_rows)==35
paths=['UDT_DEVELOPMENT.md','CURRENT_RESEARCH_PROGRAM.md','LIVE.md','HANDOFF.md',graph_path,recent_path,
       'development_reconstruction_2026-09-29/checks/test_maintenance.py']
print(json.dumps(dict(status='SCOPED_INTEGRATION_CHECK_PASS',baseline=baseline,
    prior_graph_nodes_edges_reviews_preserved=True,prior_scientific_source_pins_preserved=True,
    added_nodes=[n['id'] for n in new_nodes],registered_grades_and_canon_unchanged=True,
    generated_excerpt_exact=True,recent_rows_before=len(prior_rows),recent_rows_now=len(current_rows),
    reviewed_hashes={p:sha((ROOT/p).read_bytes()) for p in paths},
    scope='Packaging/preservation checks plus separately written substantive semantic review; no scientific promotion.'),indent=2))
