"""Final correspondence check; no science/replay rerun."""
import datetime
import hashlib
import json
from pathlib import Path

root=Path(__file__).resolve().parents[3]
review=Path(__file__).resolve().parent
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
seal=json.loads((review/'SOURCE_FIRST_SEAL.stdout').read_text())
for group in ['source_sha256','source_first_sha256']:
    for name,expected in seal[group].items():assert sha(root/name)==expected,name
post=json.loads((review/'post_exposure_check.stdout').read_text())
for name,expected in post['author_sha256'].items():assert sha(review.parent/name)==expected,name
assert post['replay_count']==9 and post['symbol_only_false_passes_reproduced']==3
disposition=json.loads((review/'REVIEW_DISPOSITION.json').read_text())
assert disposition['verdict']=='VERIFIED-WITH-CAVEATS'
assert not disposition['blocking_objections'] and not disposition['scientific_repair_required']
files={str(p.relative_to(root)):sha(p) for p in sorted(review.iterdir())
       if p.is_file() and p.name not in ['FINAL_REVIEW_SEAL.stdout','FINAL_REVIEW_SEAL.stderr','FINAL_REVIEW_SEAL.json']}
print(json.dumps({'completed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'all_source_first_and_author_pins_unchanged':True,
 'review_report_sha256':sha(review/'REVIEW_REPORT.md'),
 'machine_disposition_sha256':sha(review/'REVIEW_DISPOSITION.json'),
 'review_sha256':files},indent=2))
