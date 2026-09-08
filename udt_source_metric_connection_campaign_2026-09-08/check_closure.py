"""Packaging/provenance closure only; does not prove or promote science."""
import csv
import hashlib
import json
import runpy
import sys
from pathlib import Path

pkg=Path(__file__).resolve().parent
root=pkg.parent
runpy.run_path(str(pkg/'check_preservation.py'),run_name='__main__')
sys.path.insert(0,str(root))
import verify_current_scientific_premises as premise_checks
premise_checks.validate_startup_surface(root)
pins={
 'step_01/CANDIDATE_INITIAL.md':'b9c883ebb807ea2aea6b6bc7487d407cc218a04c0c8852426ffa899a99dd7e8d',
 'step_01/review/ADVERSARIAL_REVIEW_INITIAL.md':'55b8e25734f9cf4fdfea6cec39d71386bd7468869b1dbe67003289adb1047554',
 'step_02/CANDIDATE_INITIAL.md':'fb016f86187e5b7a29cb934ed8e0cff9a8984fddd181b13bbcdee4c9fb190c17',
 'step_02/review/ADVERSARIAL_REVIEW_INITIAL.md':'82afcc5763afa03b979f1e8c3e00fe2ef8fefc389881ab27cb01c1d4f7e51403',
 'step_03/CANDIDATE_INITIAL.md':'7178ad76d6fb20d7b590b65ffc5a3dc7133c22e7ca612b38375322b8d5b5b009',
 'step_03/review/ADVERSARIAL_REVIEW_INITIAL.md':'273b0827da26bd8def82b576945e711f5db343a2ec243ad4f1ef3a7c1a1bcde0',
 'step_03/review/FIDELITY_REVIEW.md':'04283aad821bd6bd58d58ac950cc82ec2d8c35fa2d8ccc5574172bee0f647336',
 'DECISION_BRIEF.md':'5ec90790693903190bd224328e2c684e81a4f42286bed73af65a541a3a7584ca',
}
for path,expected in pins.items():
    assert hashlib.sha256((pkg/path).read_bytes()).hexdigest()==expected,path
review_rows=0
for manifest in sorted(pkg.glob('step_*/review/REVIEW_MANIFEST.tsv')):
    for row in csv.DictReader(manifest.open(),delimiter='\t'):
        target=(manifest.parent/row['path']).resolve()
        assert target.is_relative_to(pkg),str(target)
        assert hashlib.sha256(target.read_bytes()).hexdigest()==row['sha256'],str(target)
        review_rows+=1
expected_failures={
 'step_02/author_checks_initial.json':1,
 'step_02/review/author_initial_replay.json':1,
 'integration_fetch.json':255,
}
runs=0
for path in sorted(pkg.rglob('*.json')):
    rec=json.loads(path.read_text())
    if 'returncode' not in rec or 'command' not in rec:
        continue
    rel=path.relative_to(pkg).as_posix()
    assert rec['returncode']==expected_failures.get(rel,0),(rel,rec['returncode'])
    assert not rec['timeout'],rel
    assert rec['address_space_bytes']<=512*1024**2,rel
    runs+=1
assert all((pkg/p).is_file() for p in expected_failures)
assert not list(pkg.rglob('*.pyc'))
print(json.dumps({'kind':'scoped packaging checks, not new mathematical proof',
 'startup_surface':'PASS; full349 audit not repeated',
 'candidate_review_brief_pins':len(pins),'review_manifest_rows':review_rows,
 'captured_runs_checked':runs,'preserved_expected_failures':expected_failures,
 'physical_promotion':'NONE','manifest_and_staging':'checked separately at integration'},
 sort_keys=True,indent=2))
