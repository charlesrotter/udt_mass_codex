"""HB1 source correspondence only. Does not replay or recertify old science."""
import csv
import hashlib
import json
import subprocess
from pathlib import Path

pkg = Path(__file__).resolve().parents[1]
root = pkg.parent
rows = list(csv.DictReader((pkg / 'SOURCE_LEDGER.tsv').open(), delimiter='\t'))
assert len(rows) == len({r['path'] for r in rows}) == 29
checked = []
for row in rows:
    path = row['path']
    subprocess.run(['git', 'ls-files', '--error-unmatch', path], cwd=root,
                   check=True, capture_output=True, timeout=10)
    assert hashlib.sha256((root / path).read_bytes()).hexdigest() == row['sha256'], path
    checked.append(path)
baseline = subprocess.check_output(['git', 'show',
    '7e6d144a9f45fc2cee6d041448e6b6ee9e324cc3:CURRENT_SCIENTIFIC_PREMISES.tsv'], cwd=root)
current = (root / 'CURRENT_SCIENTIFIC_PREMISES.tsv').read_bytes()
old = b''.join(line for line in current.splitlines(keepends=True)
               if not line.startswith((b'G374\t', b'G375\t')))
assert old == baseline
assert hashlib.sha256(old).hexdigest() == 'af5918070b387320f6b53b561707c17474400e78bd4c947617931218a1d2e18a'
ids = {'G143','G176','G180','G270','G289','G306','G310','G312','G313','G321',
       'G330','G331','G332','G333','G335'}
registry = list(csv.DictReader(old.decode().splitlines(), delimiter='\t'))
assert ids <= {r['premise_id'] for r in registry}
f04 = next(r for r in csv.DictReader((root /
    'udt_scientific_arc_recovery_checkpoint_2026-08-04/MASS_BRANCH_AUTHORITY_MAP.tsv').open(),
    delimiter='\t') if 'F04' in r.values())
assert any('SETTLED_STATIC_FINITE_BOX_CONDITIONAL' in value for value in f04.values())
print(json.dumps(dict(kind='SOURCE_CORRESPONDENCE_NOT_SCIENTIFIC_REPLAY',
    sources=checked, preserved_old_registry_rows=len(registry), current_ids=sorted(ids),
    f04=f04, old_large_fields='NOT_READ_OR_REPLAYED', old_certificate='INHERITED_NOT_FRESHLY_CERTIFIED',
    new_hopfion_grade='UNPROMOTED', protected_payloads='NOT_INSPECTED'), indent=2))
