#!/usr/bin/env python3
"""Authoritative read-only post-review verifier for repository or sealed layout."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path
import subprocess


HERE=Path(__file__).resolve().parent; ROOT=HERE.parent
def rows(n): return list(csv.DictReader((HERE/n).open(),delimiter='\t'))
def H(n): return hashlib.sha256((HERE/n).read_bytes()).hexdigest()

manifest=rows('SOURCE_MANIFEST.tsv'); assert len(manifest)==22
commit=(HERE/'SOURCE_BASE_COMMIT.txt').read_text().strip(); assert len(commit)==40
def git_bytes(path):
    p=subprocess.run(['git','show',f'{commit}:{path}'],cwd=ROOT,capture_output=True,check=False)
    return p.stdout if p.returncode==0 else None
gp={r['path']:git_bytes(r['path']) for r in manifest}; sealed=ROOT/'sources'
counts={'REPOSITORY_GIT_SNAPSHOT':sum(v is not None for v in gp.values()),'SEALED_SOURCES':sum((sealed/r['path']).is_file() for r in manifest)}
complete=[k for k,v in counts.items() if v==22]; assert len(complete)==1 and all(v in (0,22) for v in counts.values()),counts
for r in manifest:
    payload=gp[r['path']] if complete[0]=='REPOSITORY_GIT_SNAPSHOT' else (sealed/r['path']).read_bytes()
    assert payload is not None and hashlib.sha256(payload).hexdigest()==r['sha256']

s=rows('NUMERICAL_SAMPLE_UNIVERSE.tsv'); a=rows('SOLVED_GEOMETRY_ATLAS.tsv'); g=rows('GEODESIC_DIAGNOSTICS.tsv'); p=rows('PATH_DIAGNOSTICS.tsv'); c=rows('SURVIVOR_CLASSIFICATION.tsv'); ir=rows('INDEPENDENT_COMPARISON.tsv')
assert (len(s),len(a),len(g),len(p),len(c),len(ir))==(14,14,28,28,7,56)
assert all(r['endpoint_family']=='REGULAR' for r in a); assert all(r['classification']=='REGULAR_PROPAGATOR' for r in g); assert all(r['classification']=='NONIDENTITY' for r in p); assert all(r['pass']=='TRUE' for r in ir)
d=json.loads((HERE/'DERIVATION_RESULT.json').read_text()); i=json.loads((HERE/'INDEPENDENT_VERIFICATION.json').read_text()); cp=json.loads((HERE/'CATCH_PROOF_RESULT.json').read_text())
assert d['scope']=='bounded_metric_geometry_not_physical_stability'; assert i['status']=='PASS' and i['checks']==i['pass_count']==56; assert cp['status']=='PASS' and cp['tests']==cp['passed']==23
assert all(H(n)==h for n,h in i['production_hashes'].items())
assert (HERE/'EXTERNAL_REVIEW_RAW.md').is_file() and '`MULTIPLE_GEOMETRIC_SURVIVOR_FAMILIES`' in (HERE/'EXTERNAL_REVIEW_RAW.md').read_text()
print(json.dumps({'status':'PASS','layout':complete[0],'sources':22,'samples':14,'geodesics':28,'paths':28,'independent_checks':56,'catch_proof_record':23,'landing':'MULTIPLE_GEOMETRIC_SURVIVOR_FAMILIES'},indent=2,sort_keys=True))
