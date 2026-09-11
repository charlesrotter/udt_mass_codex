#!/usr/bin/env python3
"""Bounded banking preservation check; never open protected payloads."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parent.parent
PACKAGE = Path(__file__).resolve().parent
BASELINE = 'f5faabb43a582fec9a71c1d4a3b065efffae25bd'
EXPECTED_STATUS = '55e7c4508622f912730f9c068cc571c370b3977bc1110eb0a48a8218dbe024c2'
ALLOWED_ROOT = {
    'AGENTS.md', 'CURRENT_RESEARCH_PROGRAM.md', 'CURRENT_SCIENTIFIC_PREMISES.md',
    'CURRENT_SCIENTIFIC_PREMISES.tsv', 'HANDOFF.md', 'INDEX.md', 'LIVE.md', 'MEMORY.md',
    'UDT_RESEARCH_ROADMAP.md', 'verify_current_scientific_premises.py',
    'tests/test_startup_surface.py', 'tests/test_reviewed_backlog_banking.py',
}

def git(*args):
    return subprocess.run(['git', *args], cwd=ROOT, capture_output=True,
                          timeout=30, check=True).stdout

def allowed(name):
    return name in ALLOWED_ROOT or name.startswith(PACKAGE.name + '/')

branch = git('branch', '--show-current').decode().strip()
assert branch == 'grok', branch
status = git('status', '--porcelain=v1').splitlines(keepends=True)
unrelated = b''.join(line for line in status if not allowed(line[3:].decode().rstrip('\n')))
assert all(line.startswith(b'?? ') for line in unrelated.splitlines()), 'Unrelated tracked dirt'
assert len(unrelated.splitlines()) == 46
status_hash = hashlib.sha256(unrelated).hexdigest()
assert status_hash == EXPECTED_STATUS, status_hash
changed = git('diff', '--name-only', BASELINE, '--').decode().splitlines()
assert all(allowed(name) for name in changed), 'Out-of-scope tracked change'
scope = json.loads((PACKAGE / 'SOURCE_MANIFEST_SCOPE.json').read_text())
original_diff = git('diff', '--exit-code', BASELINE, '--', *scope['original_packages'])
assert not original_diff
original_count = len(git('ls-files', '-z', '--', *scope['original_packages']).split(b'\0')) - 1
assert original_count == 2152
raw = (ROOT / 'CURRENT_SCIENTIFIC_PREMISES.tsv').read_bytes()
prefixes = tuple(f'G{i}\t'.encode() for i in range(383, 413))
original = b''.join(line for line in raw.splitlines(keepends=True) if not line.startswith(prefixes))
assert original == git('show', BASELINE + ':CURRENT_SCIENTIFIC_PREMISES.tsv')
manifest_count = 0
for line in (PACKAGE / 'SOURCE_EVIDENCE_SHA256SUMS').read_text().splitlines():
    expected, name = line.split(maxsplit=1)
    path = Path(name)
    assert not path.is_absolute() and '..' not in path.parts
    assert hashlib.sha256((ROOT / path).read_bytes()).hexdigest() == expected, name
    manifest_count += 1
assert manifest_count == 2612
print(json.dumps({
    'observed_utc': datetime.now(timezone.utc).isoformat(),
    'branch': branch, 'head': git('rev-parse', 'HEAD').decode().strip(),
    'origin_grok': git('rev-parse', 'origin/grok').decode().strip(),
    'original365_bytes_and_order_unchanged': True,
    'original_science_packages_unchanged': len(scope['original_packages']),
    'original_tracked_science_files_unchanged': original_count,
    'source_manifest_files_authenticated': manifest_count,
    'all_tracked_changes_within_allowlist': True,
    'unrelated_status_entries': 46, 'unrelated_status_sha256': status_hash,
    'protected_payloads_opened_or_hashed': False,
    'backup_completeness': 'UNVERIFIED', 'pre_reboot_unsaved_state': 'UNVERIFIED',
    'result': 'PASS',
}, indent=2))
