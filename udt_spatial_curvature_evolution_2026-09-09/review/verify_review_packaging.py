"""Correspondence checks only: hashes and replay bytes do not prove science."""
import csv
import hashlib
import json
from pathlib import Path

repo=Path(__file__).resolve().parents[2]
pkg=repo/'udt_spatial_curvature_evolution_2026-09-09'
pins=list(csv.DictReader((pkg/'SOURCE_PINS.tsv').open(),delimiter='\t'))
for row in pins:
    assert hashlib.sha256((repo/row['path']).read_bytes()).hexdigest()==row['sha256'],row['path']
manifests={}
for name in ('INITIAL_FREEZE_SHA256SUMS','review/SOURCE_FIRST_SHA256SUMS'):
    rows=(pkg/name).read_text().splitlines()
    for row in rows:
        expected,path=row.split('  ',1)
        assert hashlib.sha256((repo/path).read_bytes()).hexdigest()==expected,path
    manifests[name]=len(rows)
for name in ('geometry','matched'):
    assert (pkg/f'author_{name}_initial.stdout').read_bytes()==(pkg/f'review/author_{name}_replay.stdout').read_bytes()
captures={}
for name in ('source_first_tensor_run','bianchi_components_run','direct_tensor_run',
             'author_geometry_replay','author_matched_replay','catch_omit_curl',
             'catch_omit_inverse','catch_undefined_probe','catch_wrong_bianchi_curl'):
    capture=json.loads((pkg/f'review/{name}.json').read_text())
    target=1 if name.startswith('catch_') else 0
    assert capture['returncode']==target and not capture['timeout'],name
    captures[name]={'exit':capture['returncode'],'seconds':capture['duration_seconds'],'maxrss_kib':capture['maxrss_kib']}
print(json.dumps({'source_pins_authenticated':len(pins),'manifests':manifests,
    'author_stdout_byte_identical':True,'captures':captures,
    'meaning':'Correspondence/resource/regression checks, not truth or chronology proofs'},indent=2))
