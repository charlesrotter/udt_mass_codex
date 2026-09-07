"""Exact frozen banking integration correspondence, not a scientific check."""
import csv
import hashlib
import io
import json
from pathlib import Path
import subprocess

ROOT = Path('/home/udt-admin/udt_mass_codex')
PKG = 'udt_g361_g363_conditional_banking_2026-09-07'
BASE = 'c663c3ebee1755c348388170df4906eb00d1a8e8'
EXPECTED_CHANGED = {'AGENTS.md', 'LIVE.md', 'HANDOFF.md', 'CURRENT_RESEARCH_PROGRAM.md',
    'CURRENT_SCIENTIFIC_PREMISES.md', 'CURRENT_SCIENTIFIC_PREMISES.tsv', 'MEMORY.md',
    'INDEX.md', 'verify_current_scientific_premises.py', 'tests/test_startup_surface.py'}

def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT)

def sha(data):
    return hashlib.sha256(data).hexdigest()

seals = []
for name in ('INTEGRATION_CANDIDATE_SHA256SUMS', 'TEXT_FREEZE_SHA256SUMS',
             'review/STAGE_A_SHA256SUMS'):
    manifest = ROOT / PKG / name
    entries = [line.split(None, 1) for line in manifest.read_text().splitlines()]
    assert len(entries) == len({path for expected, path in entries})
    for expected, path in entries:
        assert sha((ROOT / path).read_bytes()) == expected, path
    seals.append(dict(path=str(manifest.relative_to(ROOT)), sha256=sha(manifest.read_bytes()),
                      payloads=len(entries), result='PASS'))

current = (ROOT / 'CURRENT_SCIENTIFIC_PREMISES.tsv').read_bytes()
baseline = git('show', f'{BASE}:CURRENT_SCIENTIFIC_PREMISES.tsv')
retained = b''.join(line for line in current.splitlines(keepends=True)
                    if line.split(b'\t', 1)[0] not in {b'G361', b'G362', b'G363'})
assert retained == baseline
rows = list(csv.DictReader(io.StringIO(current.decode()), delimiter='\t'))
old_rows = list(csv.DictReader(io.StringIO(baseline.decode()), delimiter='\t'))
assert len(rows) == len({row['premise_id'] for row in rows}) == 346
assert len(old_rows) == 343
assert {row['premise_id'] for row in rows} - {row['premise_id'] for row in old_rows} == {'G361','G362','G363'}
changed = set(git('diff', '--name-only', BASE).decode().splitlines())
assert changed == EXPECTED_CHANGED, changed

initial = (ROOT / PKG / 'diagnostics/INITIAL_REVIEWED_PROPOSAL.md').read_bytes()
final = (ROOT / PKG / 'NEXT_CAMPAIGN_PROPOSAL.md').read_bytes()
assert sha(initial) == '09f6d2bc705f4d4a014d557f33d31a623a99daf282c9fb5f7f9b370c0742ddd1'
assert initial.count(b'|Y|') == 1
assert final == initial.replace(b'|Y|', b'\\|Y\\|')

preserved = []
for path in ('CANON.md', 'UDT_METRIC_KERNEL_DEVELOPMENT.md', 'UDT_METRIC_KERNEL_COVERAGE.tsv'):
    data = (ROOT / path).read_bytes()
    assert data == git('show', f'{BASE}:{path}'), path
    preserved.append(dict(path=path, sha256=sha(data)))

print(json.dumps(dict(status='PASS', baseline=BASE,
    observed_head=git('rev-parse','HEAD').decode().strip(), seals=seals,
    old_registry_rows=len(old_rows), new_registry_rows=len(rows), added_ids=['G361','G362','G363'],
    old_registry_bytes_exact=True, old_registry_sha256=sha(retained),
    exact_changed_tracked_paths=sorted(changed), unchanged_fixed_files=preserved,
    proposal_change='EXACTLY_ESCAPE_TWO_MARKDOWN_TABLE_VERTICAL_BARS_NO_SEMANTIC_CHANGE',
    proposal_initial_sha256=sha(initial), proposal_current_sha256=sha(final),
    scientific_calculations='NONE', new_campaign_tests='NONE'), indent=2))
