"""Pin reviewed inputs and the completed review; no source mutation."""
import hashlib
import json
from pathlib import Path
root=Path(__file__).resolve().parents[2]
review=Path(__file__).resolve().parent
package=review.parent
def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()
pins={}
for name in ['INITIAL_CANDIDATE.md','METHOD_SOURCES.md','check_original_metric.py',
 'check_profile.py','original_metric_run.stdout','original_metric_run.stderr',
 'original_metric_run.json','profile_run.stdout','profile_run.stderr',
 'profile_run.json','STARTUP_PREMISE_AUDIT.json','WORK_ORDER.md']:
    pins[name]=sha(package/name)
for line in (review/'SOURCE_FIRST_SHA256SUMS').read_text().splitlines():
    h,p=line.split('  ',1)
    assert sha(root/p)==h, p
assert (package/'original_metric_run.stdout').read_bytes()==(review/'direct_author_metric_replay.stdout').read_bytes()
assert (package/'profile_run.stdout').read_bytes()==(review/'direct_author_profile_replay.stdout').read_bytes()
record=dict(reviewer='/root/nrgeom_review',model='UNKNOWN',fresh_context=True,
 independent_library='UNTESTED',different_model='UNTESTED',
 verdict='VERIFIED-WITH-CAVEATS',scientific_repairs=0,unpromoted=True,
 full365='NOT_PASSED_G325',inputs=pins,
 clarification='Cauchy endpoint statement concerns inextendible curves only',
 source_first_preserved=True,author_replays_byte_identical=True)
with (review/'REVIEW_RECORD.json').open('x') as out:
    json.dump(record,out,indent=2)
    out.write('\n')
files=sorted(p for p in review.iterdir() if p.is_file())
with (review/'DIRECT_REVIEW_SHA256SUMS').open('x') as out:
    for p in files:
        out.write(sha(p)+'  '+str(p.relative_to(root))+'\n')
print('DIRECT_REVIEW.md '+sha(review/'DIRECT_REVIEW.md'))
print('DIRECT_REVIEW_SHA256SUMS '+sha(review/'DIRECT_REVIEW_SHA256SUMS'))
print('REVIEW_RECORD.json '+sha(review/'REVIEW_RECORD.json'))
print('entries '+str(len(files)))
