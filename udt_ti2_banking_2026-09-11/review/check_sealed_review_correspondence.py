"""Allow only the explicit two-review-pin augmentation after substantive seal."""
from pathlib import Path
import datetime
import hashlib
import json
repo=Path(__file__).resolve().parents[2]
review=Path(__file__).resolve().parent
receipt=json.loads((review/'REVIEW_RECEIPT.json').read_text())
changed=[]
for path,expected in receipt['sha256'].items():
 raw=(repo/path).read_bytes()
 if hashlib.sha256(raw).hexdigest()!=expected:
  changed.append(path)
assert changed==['ti2_banking_guard.py'],changed
raw=(repo/'ti2_banking_guard.py').read_bytes()
lines=raw.splitlines(keepends=True)
added=[x for x in lines if x.startswith(b'# Fresh source-exposed banking review;') or x.startswith(b'TI2_PINS.update(')]
assert len(added)==2
restored=b''.join(x for x in lines if x not in added)
assert hashlib.sha256(restored).hexdigest()==receipt['sha256']['ti2_banking_guard.py']
import ast
update=ast.parse(added[1].decode()).body[0].value
pins=ast.literal_eval(update.args[0])
expected_names={str(p.relative_to(repo)) for p in [review/'REVIEW.md',review/'REVIEW_RECEIPT.json']}
assert set(pins)==expected_names
for path,sha in pins.items(): assert hashlib.sha256((repo/path).read_bytes()).hexdigest()==sha
print(json.dumps({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'verdict':'PASS','sealed_pin_count':len(receipt['sha256']),
 'only_changed_file':changed[0],'change':'exact two-review-pin augmentation; every other byte equals sealed source',
 'review_and_receipt_authentication':pins},indent=2))
