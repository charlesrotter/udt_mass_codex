"""Seal this completed fidelity review and authenticate final gate receipts."""
import datetime
import hashlib
import json
from pathlib import Path

review = Path(__file__).resolve().parent
package = review.parent
root = package.parent
def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

integration = package / 'INTEGRATION_SHA256SUMS'
assert sha(integration) == 'a298fd6af1a7880469438e679067f4a17a56677512b8cb9e4df2a7f46517dbf7'
pins = {}
for line in integration.read_text().splitlines():
    expected, relative = line.split(maxsplit=1)
    assert sha(root / relative) == expected, relative
    pins[relative] = expected
assert len(pins) == 32

receipt = json.loads((package / 'postbank_365_repaired.json').read_text())
assert receipt['returncode'] == 0 and not receipt['timeout']
assert receipt['limits'] == {'address_space_bytes': 2147483648, 'cpu_wall_seconds': 900, 'library_threads': 1}
stdout = (package / 'postbank_365_repaired.stdout').read_text()
stderr = (package / 'postbank_365_repaired.stderr').read_text()
assert receipt['stdout'] == stdout and receipt['stderr'] == stderr == ''
assert 'PASS: 365-row premise registry' in stdout
assert 'PASS: G381/NT1 and G382/NT2' in stdout

verdict = json.loads((review / 'VERDICT.json').read_text())
assert verdict['verdict'] == 'PASS_WITH_CAVEATS'
assert verdict['unresolved_load_bearing_objections'] == []
assert 'Review IN PROGRESS' not in (review / 'FIDELITY_REVIEW.md').read_text()
placement = json.loads((review / 'placement_misplaced.json').read_text())
assert placement['returncode'] == 1 and not placement['timeout']
assert (review / 'placement_misplaced.stderr').read_text().strip() == 'neighboring-tidal rows must precede historical rows in dependency order'

payloads = {}
for path in sorted(review.iterdir()):
    if path.is_file() and not path.name.startswith('final_review_seal.'):
        payloads[str(path.relative_to(root))] = sha(path)
extras = ['INTEGRATION_SHA256SUMS', 'postbank_365_repaired.json',
          'postbank_365_repaired.stdout', 'postbank_365_repaired.stderr',
          'check_initial_integration_reconstruction.py', 'initial_integration_reconstruction.json',
          'initial_integration_reconstruction.stdout', 'initial_integration_reconstruction.stderr',
          'REGRESSION_COMPARISON.json']
for name in extras:
    path = package / name
    payloads[str(path.relative_to(root))] = sha(path)
print(json.dumps({'status': 'PASS_WITH_CAVEATS',
                  'utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
                  'context': '/root/nt_banking_fidelity',
                  'full365_receipt_authenticated': True,
                  'repaired_integration_pins_authenticated': len(pins),
                  'payload_count': len(payloads), 'sha256': payloads,
                  'meaning': 'correspondence and review boundary; not proof or externally trusted chronology'}, indent=2))
