"""Independent byte/row correspondence; no import of the production verifier."""
import csv
import hashlib
import io
import json
from pathlib import Path
import subprocess

ROOT = Path('/home/udt-admin/udt_mass_codex')
BASE = '32d23fb47dc4e440acc8c721aef6cb8201796ded'
NEW_IDS = {'G376', 'G377', 'G378'}
BANK = 'udt_g376_g378_conditional_banking_2026-09-08'
files = ['AGENTS.md', 'LIVE.md', 'HANDOFF.md', 'CURRENT_RESEARCH_PROGRAM.md',
         'CURRENT_SCIENTIFIC_PREMISES.md', 'CURRENT_SCIENTIFIC_PREMISES.tsv',
         'INDEX.md', 'MEMORY.md', 'verify_current_scientific_premises.py']

def original(path):
    return subprocess.check_output(['git', 'show', BASE + ':' + path], cwd=ROOT)

raw = (ROOT / 'CURRENT_SCIENTIFIC_PREMISES.tsv').read_bytes()
lines = raw.splitlines(keepends=True)
kept = b''.join(line for line in lines
                if line.partition(b'\t')[0].decode() not in NEW_IDS)
assert kept == original('CURRENT_SCIENTIFIC_PREMISES.tsv')
rows = list(csv.DictReader(io.StringIO(raw.decode()), delimiter='\t'))
old_rows = list(csv.DictReader(io.StringIO(kept.decode()), delimiter='\t'))
assert len(rows) == 361 and len(old_rows) == 358
assert len({row['premise_id'] for row in rows}) == 361
new_rows = [row for row in rows if row['premise_id'] in NEW_IDS]
assert {row['premise_id'] for row in new_rows} == NEW_IDS
for row in new_rows:
    assert row['current_status'] == ('BANKED_DERIVED_CONDITIONAL__VERIFIED_WITH_CAVEATS'
        '__OWNER_AUTHORIZED__NOT_PHYSICAL_ADOPTION__NOT_CANON')
    assert row['controlling_source'] == BANK + '/BANKING_RECORD.md'
changed = subprocess.check_output(['git', '-c', 'core.preloadIndex=false', 'diff', '--name-only'], cwd=ROOT,
                                  text=True).splitlines()
assert set(changed) == set(files), changed
protected = ['CANON.md', 'UDT_METRIC_KERNEL_DEVELOPMENT.md', 'UDT_METRIC_KERNEL_COVERAGE.tsv']
for relative in protected:
    assert (ROOT / relative).read_bytes() == original(relative)
for relative in ['BANKING_RECORD.md', 'SOURCE_EVIDENCE_SHA256SUMS',
                 'INITIAL_BANKING_RECORD.md', 'INITIAL_BANKING_CLAIMS.tsv',
                 'REPAIR_RECORD.md', 'WORK_ORDER.md']:
    files.append(BANK + '/' + relative)
print(json.dumps({
    'verdict': 'PASS',
    'scope': 'independent byte/row correspondence and reviewed file hashes, not scientific proof',
    'base': BASE,
    'new_entries': {row['premise_id']: row['term'] for row in new_rows},
    'current_count': len(rows), 'prior_count': len(old_rows),
    'all_prior_registry_bytes_equal_base': True,
    'changed_tracked_files': changed,
    'unchanged_canon_and_fixed_manuscript': protected,
    'reviewed_sha256': {relative: hashlib.sha256((ROOT / relative).read_bytes()).hexdigest()
                        for relative in files},
}, indent=2, sort_keys=True))
