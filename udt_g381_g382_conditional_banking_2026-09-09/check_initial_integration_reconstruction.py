"""Exact initial failed-version reconstruction in memory; never an original snapshot.

The inverse edits below, together with INITIAL_REGISTRY_DIFF.patch and the
unchanged ca6f092d baseline, retain the exact small implementation deltas.
No reconstructed byte is written over a source. Hash matching is correspondence,
not proof of initial chronology or a claim that the initial version was saved.
"""
import hashlib
import json
from pathlib import Path

package = Path(__file__).resolve().parent
root = package.parent
initial_pins = {}
for line in (package/'INITIAL_INTEGRATION_SHA256SUMS').read_text().splitlines():
    digest, path = line.split(maxsplit=1)
    initial_pins[path] = digest

verifier_addition = '''    require(tuple(row["premise_id"] for row in rows[:2]) == NEIGHBORING_TIDAL_BANKING_IDS,
            "neighboring-tidal rows must precede historical rows in dependency order")
'''
check_addition = '''lines = reg.splitlines(keepends=True)
new_prefixes = tuple(pid+'\\t' for pid in v.NEIGHBORING_TIDAL_BANKING_IDS)
misplaced = ''.join(line for line in lines if not line.startswith(new_prefixes))
misplaced += ''.join(line for line in lines if line.startswith(new_prefixes))
mutants.append(('new_rows_misplaced_after_history', misplaced, record,
    'rows must precede historical rows in dependency order'))
'''
inverse = {'verify_current_scientific_premises.py': verifier_addition,
           package.name+'/check_banking.py': check_addition}
reconstructed = {}
for path, addition in inverse.items():
    current = (root/path).read_bytes()
    exact = addition.encode()
    assert current.count(exact) == 1, path
    reconstructed[path] = current.replace(exact, b'', 1)

lines = (root/'CURRENT_SCIENTIFIC_PREMISES.tsv').read_bytes().splitlines(keepends=True)
new = [line for line in lines if line.startswith((b'G381\t', b'G382\t'))]
old = [line for line in lines if not line.startswith((b'G381\t', b'G382\t'))]
assert len(new) == 2
reconstructed['CURRENT_SCIENTIFIC_PREMISES.tsv'] = b''.join(old+new)
path = package.name+'/REPAIR_RECORD.md'
current = (root/path).read_bytes()
marker = b'\n## Registry placement integration repair\n'
assert current.count(marker) == 1
reconstructed[path] = current.split(marker)[0]

checked = {}
for path, expected in initial_pins.items():
    payload = reconstructed.get(path)
    if payload is None:
        payload = (root/path).read_bytes()
    actual = hashlib.sha256(payload).hexdigest()
    assert actual == expected, (path, actual, expected)
    checked[path] = {'sha256': actual,
                     'method': 'RECONSTRUCTED_IN_MEMORY_NOT_ORIGINAL_SNAPSHOT'
                     if path in reconstructed else 'UNCHANGED_ORIGINAL_BYTES'}
assert len(checked) == 21 and len(reconstructed) == 4
print(json.dumps({'status':'PASS', 'initial_integration_pins':checked,
    'reconstruction_limits':'exact inverse edits authenticated to first seal; NOT recovered original snapshots or chronology proof'}, indent=2))
