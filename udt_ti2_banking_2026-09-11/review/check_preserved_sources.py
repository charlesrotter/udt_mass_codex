"""Scoped read-only byte correspondence, independent of banking guard code."""
from pathlib import Path
import csv
import datetime
import hashlib
import io
import json
import platform
import subprocess

ROOT = Path(__file__).resolve().parents[2]
BASE = 'b95ace99315b816b9a53abe8102b478d1e1cd188'
ORIGINAL = 'udt_two_shape_evolution_2026-09-11'
BANK = 'udt_ti2_banking_2026-09-11'

def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT, timeout=15)

def digest(raw):
    return hashlib.sha256(raw).hexdigest()

assert git('branch', '--show-current').strip() == b'grok'
assert git('rev-parse', 'HEAD').decode().strip() == BASE
baseline = git('show', BASE + ':CURRENT_SCIENTIFIC_PREMISES.tsv')
current = (ROOT / 'CURRENT_SCIENTIFIC_PREMISES.tsv').read_bytes()
new = [x for x in current.splitlines(keepends=True) if x.startswith(b'G414\t')]
assert len(new) <= 1
without_new = b''.join(x for x in current.splitlines(keepends=True) if not x.startswith(b'G414\t'))
assert without_new == baseline, 'original396 registry bytes changed'
rows = list(csv.DictReader(io.StringIO(baseline.decode()), delimiter='\t'))
assert len(rows) == 396
paths = git('ls-tree', '-r', '--name-only', BASE, '--', ORIGINAL).decode().splitlines()
assert len(paths) == 120
actual_manifest = {}
for path in paths:
    raw = (ROOT / path).read_bytes()
    assert raw == git('show', BASE + ':' + path), path
    actual_manifest[path] = digest(raw)
manifest = {}
for line in (ROOT / BANK / 'SOURCE_EVIDENCE_SHA256SUMS').read_text().splitlines():
    sha, path = line.split(maxsplit=1)
    assert path not in manifest
    manifest[path] = sha
assert manifest == actual_manifest
assert digest((ROOT / ORIGINAL / 'INITIAL_CANDIDATE.md').read_bytes()) == '1d9b24c359636dd212f684b45793f2f02cfa8959df0e8a8dc0c19bcb5c8ae0a9'
assert (ROOT / 'udt_ti1_banking_2026-09-11/BANKING_RECORD.md').read_bytes() == git('show', BASE + ':udt_ti1_banking_2026-09-11/BANKING_RECORD.md')
assert (ROOT / 'udt_ti1_banking_2026-09-11/SOURCE_EVIDENCE_SHA256SUMS').read_bytes() == git('show', BASE + ':udt_ti1_banking_2026-09-11/SOURCE_EVIDENCE_SHA256SUMS')
source_rows = json.loads((ROOT / ORIGINAL / 'SOURCE_REGISTRY_ROWS.json').read_text())
by_id = {r['premise_id']:r for r in rows}
# Schema is inspected explicitly; no broad historical registry dump.
if isinstance(source_rows, dict):
    values = source_rows.get('rows', source_rows)
    if isinstance(values, dict):
        values = list(values.values())
else:
    values = source_rows
assert isinstance(values,list)
for row in values:
    assert row == by_id[row['premise_id']], row['premise_id']
print(json.dumps({
    'utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'verdict':'PASS', 'baseline':BASE, 'python':platform.python_version(),
    'current_added_G414_rows':len(new), 'original396_bytes_preserved':True,
    'original_registry_sha256':digest(baseline),
    'original_TI2_files_byte_equal_to_git':len(paths),
    'source_manifest_complete_and_exact':True,
    'source_registry_ids_equal_to_current_baseline':[r['premise_id'] for r in values],
    'G413_acceptance_and103_source_manifest_unchanged':True,
    'runtime_model_version':'UNATTESTED', 'protected_payloads':'excluded',
    'omissions':'No original symbolic science or full premise audit rerun.'
},indent=2))
